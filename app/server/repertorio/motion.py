"""Coleções de vídeos de motion: cada vídeo vira uma referência externa ligada ao vocabulário do mapa.

As fichas ficam em dados/motion/*.jsonl (uma por linha, montadas por ferramentas/incorporar_prompt_motion.py).
Cada uma traz a classificação criativa, o prompt original, a procedência e os caminhos da mídia:
capa (prévia do mapa), quadros (o que o agente vê do movimento), loop curto (o mapa e as listas tocam) e vídeo completo.
"""
import hashlib
from pathlib import Path
from sqlalchemy import text
from .db import dumps, now
from .importer import asset, index_text, read_jsonl

# A mídia continua dos autores: entra só como referência.
USAGE = 'Vídeo de terceiros: estude o movimento, o ritmo e o prompt, e recrie a ideia com o tema e a identidade do projeto. Não incorpore a mídia.'
# Formato de tela e tipo de vídeo organizam o espaço no mapa; os nomes também valem para a busca.
ASPECTS = {'horizontal':'horizontal 16:9 youtube site apresentação tela larga','vertical':'vertical 9:16 reels tiktok shorts stories celular',
           'quadrado':'quadrado 1:1 4:5 feed instagram linkedin','modelo':'prompt modelo'}
GENRES = {'lancamento':'lançamento de produto','showreel':'showreel de motion','explicativo':'explicativo','dados':'dados e números',
          'tipografia':'tipografia e mensagem','historia':'histórias e personagens','abstrato':'arte abstrata e 3D','vinheta':'marca e vinheta','modelo':'prompt-modelo'}
TAGS = {'product-ui':'interface de produto','kinetic-type':'tipografia cinética','music':'trilha sonora','particles':'partículas',
        'shapes':'formas geométricas','charts':'gráficos animados','diagrams':'diagramas','characters':'personagens',
        'photos':'fotografias','phone':'celular','code':'código'}


def payload(d):
    tags=[TAGS.get(t,t) for t in d.get('content_tags') or []]
    source={k:d.get(k) for k in ('collection','page','post','author','handle','posted','model','iterations','stack','effort','skill','title_original') if d.get(k)}
    source['content_tags']=d.get('content_tags') or []
    return dict(
        title=d['title'],description=d['description'],idea=d['idea'],how=d.get('how',''),html=d.get('html',''),
        techniques=d.get('techniques') or [],intentions=d.get('intentions') or [],movements=d.get('movements') or [],
        aesthetics=d.get('aesthetics') or [],tone=d.get('tone') or [],strength=d.get('strength') or 3,reusable=False,
        usage_notes=' '.join(x for x in [USAGE,d.get('cautions',''),f"Autor: {d.get('author')} (@{d['handle']})." if d.get('handle') else ''] if x),
        text=d.get('prompt') or '',prompt=d.get('prompt') or '',prompt_note=d.get('prompt_note') or '',
        good_for=d.get('good_for') or [],format='mp4' if (d.get('media') or {}).get('video') else 'txt',
        genres=d.get('genres') or [],aspect=d.get('aspect') or '',
        keywords=' '.join(['motion','vídeo','animação',ASPECTS.get(d.get('aspect') or '','')]+[GENRES.get(g,g) for g in d.get('genres') or []]+tags+[d.get('how',''),d.get('author',''),d.get('handle',''),' '.join(d.get('good_for') or [])]),
        source=source,template=bool(d.get('template')),
        video=({k:d.get(k) for k in ('duration','width','height','fps','audio')} if (d.get('media') or {}).get('video') else None),
    )


def import_motion(db, workspace_id, folder=None):
    from .workspaces import Workspaces
    manager=Workspaces();manager.db=db
    manager.workspace(workspace_id)
    folder=Path(folder or db.settings.root/'dados/motion')
    records=[d for f in sorted(folder.glob('*.jsonl')) for d in read_jsonl(f)]
    if not records:
        raise ValueError('Nenhuma ficha de motion encontrada em '+str(folder))
    report=dict(inserted=0,updated=0,preserved=0,total=len(records),missing_assets=0)
    stamp=now()
    with db.engine.begin() as conn:
        existing={r['id']:dict(r) for r in conn.execute(text("SELECT id,source_hash,curated FROM refs WHERE id IN (SELECT value FROM json_each(:ids))"),dict(ids=dumps([d['id'] for d in records]))).mappings()}
        for d in records:
            rid=d['id']
            digest=hashlib.sha256(('motion-2:'+dumps(d)).encode()).hexdigest()
            old=existing.get(rid)
            conn.execute(text('''INSERT OR IGNORE INTO workspace_references(workspace_id,ref_id,state,created,updated)
                SELECT :w,id,'published',:t,:t FROM refs WHERE id=:r'''),dict(w=workspace_id,t=stamp,r=rid))
            if old and (old['source_hash']==digest or old['curated']):
                report['preserved']+=1
                continue
            data=payload(d)
            media=d.get('media') or {}
            ids={}
            params=dict(id=rid,kind='referencia',title=data['title'],origin='externa',hash=digest,search=index_text(data),t=stamp)
            if old:
                conn.execute(text('UPDATE refs SET title=:title,search_text=:search,source_hash=:hash,revision=revision+1,updated=:t WHERE id=:id'),params)
                report['updated']+=1
            else:
                conn.execute(text("INSERT INTO refs(id,kind,title,origin,source_hash,payload,search_text,created,updated) VALUES(:id,:kind,:title,:origin,:hash,'{}',:search,:t,:t)"),params)
                conn.execute(text("INSERT INTO workspace_references(workspace_id,ref_id,state,created,updated) VALUES(:w,:r,'published',:t,:t)"),dict(w=workspace_id,r=rid,t=stamp))
                report['inserted']+=1
            for key,role in (('poster','preview'),('storyboard','storyboard'),('loop','motion'),('video','original')):
                if media.get(key):ids[key]=asset(conn,db.settings,rid,media[key],role)
            # O mapa e a ficha tocam o vídeo sem consultar os arquivos de cada referência.
            data['motion']={k:v for k,v in (('loop',ids.get('loop')),('video',ids.get('video')),('storyboard',ids.get('storyboard'))) if v}
            conn.execute(text('UPDATE refs SET payload=:p WHERE id=:id'),dict(p=dumps(data),id=rid))
        report['missing_assets']=conn.execute(text("SELECT COUNT(*) FROM assets WHERE missing=1 AND ref_id IN (SELECT value FROM json_each(:ids))"),dict(ids=dumps([d['id'] for d in records]))).scalar()
        db.log(conn,'library_imported',workspace_ids=[workspace_id],collection='motion',**report)
    return report
