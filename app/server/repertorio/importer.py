import hashlib
import json
import mimetypes
from pathlib import Path
from sqlalchemy import text
from .db import dumps, now


def read_jsonl(path):
    if path.exists():
        with path.open() as f:
            for line in f:
                if line.strip():
                    yield json.loads(line)


def index_text(data):
    fields = ('title', 'description', 'idea', 'techniques', 'intentions', 'movements', 'aesthetics', 'text', 'usage_notes', 'keywords')
    return ' '.join(' '.join(map(str, data[k])) if isinstance(data.get(k), list) else str(data.get(k) or '') for k in fields)


def asset(conn, settings, rid, path, role, member=None):
    p = Path(path)
    p = (settings.root / p).resolve() if not p.is_absolute() else p.resolve()
    if not p.is_relative_to(settings.root) and not p.is_relative_to(settings.home):
        return None
    existing = conn.execute(text('SELECT id FROM assets WHERE ref_id=:rid AND path=:p AND role=:r AND member IS :m LIMIT 1'),
                            dict(rid=rid,p=str(p),r=role,m=member)).scalar()
    if existing:
        return existing
    aid = hashlib.sha256(f'{rid}|{p}|{member}|{role}'.encode()).hexdigest()[:32]
    conn.execute(text('INSERT OR IGNORE INTO assets(id,ref_id,path,role,member,mime,missing) VALUES(:id,:rid,:p,:r,:m,:mime,:missing)'),
                 dict(id=aid,rid=rid,p=str(p),r=role,m=member,mime=mimetypes.guess_type(member or str(p))[0] or 'application/octet-stream',missing=int(not p.is_file())))
    return aid


def import_library(db, workspace_id='pp-treta'):
    from .workspaces import Workspaces
    manager=Workspaces();manager.db=db
    manager.workspace(workspace_id)
    root = db.settings.root
    index = list(read_jsonl(root / 'dados/indice.jsonl'))
    if not index:
        raise ValueError('Índice do acervo não encontrado.')
    fichas = {d['id']: d for d in read_jsonl(root / 'dados/fichas.jsonl')}
    media = list(read_jsonl(root / 'dados/midia.jsonl'))
    known = {d['id'] for d in index}
    for d in media:
        if d['id'] not in known:
            index.append({**d, 'doc': 'midia', 'unclassified': True, 'o_que': 'Mídia ainda sem classificação'})
    report = dict(inserted=0, updated=0, preserved=0, total=len(index), missing_assets=0)
    stamp = now()
    inserted_ids=[]
    with db.engine.begin() as conn:
        existing = {r['id']: dict(r) for r in conn.execute(text('SELECT id,source_hash,curated,revision FROM refs')).mappings()}
        for source in index:
            kind, rid = source['doc'], source['id']
            d = {**fichas.get(rid, {}), **source}
            digest = hashlib.sha256(('schema-2:'+dumps(d)).encode()).hexdigest()
            old = existing.get(rid)
            if old:
                conn.execute(text('''INSERT OR IGNORE INTO workspace_references(workspace_id,ref_id,state,created,updated)
                    SELECT :w,id,'published',:t,:t FROM refs WHERE id=:r'''),dict(w=workspace_id,t=stamp,r=rid))
            if old and (old['source_hash'] == digest or old['curated']):
                report['preserved'] += 1
                continue
            payload = dict(
                title=d.get('titulo') or d.get('fonte') or d.get('o_que') or rid,
                description=d.get('resumo') or d.get('nota') or d.get('o_que') or '',
                idea=d.get('ideia') or d.get('ideia_arquivo') or '',
                techniques=d.get('tecnicas') or [], intentions=d.get('intencoes') or [],
                movements=d.get('movimento') or [], aesthetics=d.get('estetica') or [],
                strength=d.get('forca') or 3, reusable=(not d['terceiros']) if isinstance(d.get('terceiros'),bool) else None,
                usage_notes=d.get('cuidados') or '', text=d.get('texto_slide') or d.get('texto') or '',
                how=d.get('como_funciona') or d.get('como_levar_para_slide') or '', html=d.get('html') or '',
                good_for=d.get('bom_para') or [], number=d.get('n'), format=Path(d.get('arquivo') or '').suffix.lstrip('.') or str(d.get('ext') or '').lstrip('.'),
                unclassified=d.get('unclassified',False), legacy=d,
            )
            origin = 'externa' if kind == 'referencia' else 'pptreta'
            params = dict(id=rid,kind=kind,title=payload['title'],parent=d.get('deck'),origin=origin,
                          hidden=int(kind=='slide' and bool(d.get('antes') or d.get('oculto'))),hash=digest,payload=dumps(payload),search=index_text(payload),t=stamp)
            if old:
                conn.execute(text('UPDATE refs SET title=:title,payload=:payload,search_text=:search,source_hash=:hash,hidden=:hidden,revision=revision+1,updated=:t WHERE id=:id'),params)
                report['updated'] += 1
            else:
                conn.execute(text('INSERT INTO refs(id,kind,title,parent_id,origin,hidden,source_hash,payload,search_text,created,updated) VALUES(:id,:kind,:title,:parent,:origin,:hidden,:hash,:payload,:search,:t,:t)'),params)
                conn.execute(text("INSERT INTO workspace_references(workspace_id,ref_id,state,created,updated) VALUES(:w,:r,'published',:t,:t)"),dict(w=workspace_id,r=rid,t=stamp))
                inserted_ids.append(rid)
                report['inserted'] += 1
            if d.get('imagem'):
                asset(conn, db.settings, rid, d['imagem'], 'preview')
            if d.get('arquivo'):
                asset(conn, db.settings, rid, d['arquivo'], 'original')
            if kind == 'arquivo':
                thumb = root / '_catalogo/mapa/m' / f'{rid}.jpg'
                if thumb.exists():
                    asset(conn, db.settings, rid, thumb, 'thumbnail')
            if kind == 'midia' and d.get('origem',{}).get('arq'):
                orig = d['origem']
                asset(conn, db.settings, rid, root / '_originais/pptx' / orig['arq'], 'original', orig.get('parte'))
        # Slides novos acompanham todos os vínculos da apresentação, inclusive as retiradas.
        # O passe final também cobre índices que listam o slide antes da apresentação.
        conn.execute(text('''DELETE FROM workspace_references WHERE ref_id IN
            (SELECT r.id FROM refs r WHERE r.id IN (SELECT value FROM json_each(:ids))
             AND EXISTS(SELECT 1 FROM workspace_references pm WHERE pm.ref_id=r.parent_id))'''),dict(ids=dumps(inserted_ids)))
        conn.execute(text('''INSERT INTO workspace_references(workspace_id,ref_id,state,detached,created,updated)
            SELECT pm.workspace_id,r.id,'published',pm.detached,:t,:t FROM refs r
            JOIN workspace_references pm ON pm.ref_id=r.parent_id WHERE r.id IN (SELECT value FROM json_each(:ids))'''),
            dict(ids=dumps(inserted_ids),t=stamp))
        for name, file in [('vocabulary','dados/vocabulario.json'),('fonts','dados/fontes.json')]:
            if (root / file).exists():
                conn.execute(text('INSERT OR REPLACE INTO meta(key,value) VALUES(:k,:v)'),dict(k=name,v=(root/file).read_text()))
        transitions = list(read_jsonl(root / 'dados/transicoes.jsonl'))
        by_deck = {}
        for t in transitions:
            by_deck.setdefault(t['deck'],[]).append(t)
        for rid, items in by_deck.items():
            conn.execute(text('INSERT OR REPLACE INTO meta(key,value) VALUES(:k,:v)'),dict(k='transitions:'+rid,v=dumps(items)))
        principles = {}
        for name in ['narrativa','direcao-de-arte']:
            path = root / 'biblioteca/principios' / f'{name}.md'
            if path.exists():
                principles[name] = path.read_text()
        conn.execute(text('INSERT OR REPLACE INTO meta(key,value) VALUES(:k,:v)'),dict(k='principles',v=dumps(principles)))
        report['missing_assets'] = conn.execute(text('SELECT COUNT(*) FROM assets WHERE missing=1')).scalar()
        conn.execute(text('INSERT OR REPLACE INTO meta(key,value) VALUES(:k,:v)'),dict(k='import_report',v=dumps({**report,'at':stamp})))
        db.log(conn,'library_imported',workspace_ids=[workspace_id],**report)
    return report
