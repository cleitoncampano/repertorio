"""Coleções de apresentações em PDF de terceiros: cada PDF vira uma apresentação no mapa
e cada página escolhida vira um slide dela, com a mesma ficha (técnicas, intenções, ideia) dos slides de Referências.

As fichas ficam em dados/<coleção>/*.jsonl, uma por linha: `doc: arquivo` para o PDF (capa e original)
e `doc: slide` para a página (imagem da página, `deck` aponta para o PDF). Os métodos escritos a partir
do mesmo material ficam em biblioteca/metodos/<coleção>/ e chegam ao agente por get_guide.
"""
import hashlib
from pathlib import Path
from sqlalchemy import text
from .db import dumps, now
from .importer import asset, image_aspect, index_text, read_jsonl

USAGE = 'Material de terceiros: estude a composição e o método, e recrie a ideia com o tema e a identidade do projeto. Não copie a página.'


def payload(d, root):
    return dict(
        title=d['title'],description=d.get('description',''),idea=d.get('idea',''),how=d.get('how',''),html='',
        techniques=d.get('techniques') or [],intentions=d.get('intentions') or [],movements=d.get('movements') or [],
        aesthetics=d.get('aesthetics') or [],tone=d.get('tone') or [],strength=d.get('strength') or 3,reusable=False,
        usage_notes=' '.join(x for x in [USAGE,d.get('cautions','')] if x),text=d.get('text',''),
        good_for=d.get('good_for') or [],number=d.get('n'),format='pdf',
        aspect=image_aspect(root/d['preview']) if d.get('preview') and d['doc']=='arquivo' else None,
        keywords=' '.join([d.get('collection',''),' '.join(d.get('concepts') or []),d.get('keywords','')]).strip(),
        concepts=d.get('concepts') or [],source={k:d[k] for k in ('collection','file','page') if d.get(k)},
    )


def import_decks(db, workspace_id, folder):
    from .workspaces import Workspaces
    manager=Workspaces();manager.db=db
    manager.workspace(workspace_id)
    folder=Path(folder)
    records=[d for f in sorted(folder.glob('*.jsonl')) for d in read_jsonl(f)]
    if not records:
        raise ValueError('Nenhuma ficha de apresentação encontrada em '+str(folder))
    # A apresentação entra antes dos slides, para eles já nascerem dentro dela.
    records.sort(key=lambda d:d['doc']!='arquivo')
    report=dict(inserted=0,updated=0,preserved=0,total=len(records),missing_assets=0)
    stamp=now();root=db.settings.root
    with db.engine.begin() as conn:
        existing={r['id']:dict(r) for r in conn.execute(text("SELECT id,source_hash,curated FROM refs WHERE id IN (SELECT value FROM json_each(:ids))"),dict(ids=dumps([d['id'] for d in records]))).mappings()}
        for d in records:
            rid=d['id']
            digest=hashlib.sha256(('decks-1:'+dumps(d)).encode()).hexdigest()
            old=existing.get(rid)
            conn.execute(text('''INSERT OR IGNORE INTO workspace_references(workspace_id,ref_id,state,created,updated)
                SELECT :w,id,'published',:t,:t FROM refs WHERE id=:r'''),dict(w=workspace_id,t=stamp,r=rid))
            if old and (old['source_hash']==digest or old['curated']):
                report['preserved']+=1
                continue
            data=payload(d,root)
            params=dict(id=rid,kind=d['doc'],title=data['title'],parent=d.get('deck'),origin='externa',hash=digest,payload=dumps(data),search=index_text(data),t=stamp)
            if old:
                conn.execute(text('UPDATE refs SET title=:title,payload=:payload,search_text=:search,source_hash=:hash,revision=revision+1,updated=:t WHERE id=:id'),params)
                report['updated']+=1
            else:
                conn.execute(text('INSERT INTO refs(id,kind,title,parent_id,origin,source_hash,payload,search_text,created,updated) VALUES(:id,:kind,:title,:parent,:origin,:hash,:payload,:search,:t,:t)'),params)
                conn.execute(text("INSERT INTO workspace_references(workspace_id,ref_id,state,created,updated) VALUES(:w,:r,'published',:t,:t)"),dict(w=workspace_id,r=rid,t=stamp))
                report['inserted']+=1
            if d.get('preview'):asset(conn,db.settings,rid,d['preview'],'preview')
            if d.get('original'):asset(conn,db.settings,rid,d['original'],'original')
        report['missing_assets']=conn.execute(text("SELECT COUNT(*) FROM assets WHERE missing=1 AND ref_id IN (SELECT value FROM json_each(:ids))"),dict(ids=dumps([d['id'] for d in records]))).scalar()
        db.log(conn,'library_imported',workspace_ids=[workspace_id],collection=folder.name,**report)
    return report
