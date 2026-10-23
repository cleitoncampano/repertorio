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


# Mídia de vídeo: as mesmas peças para a galeria importada e para os vídeos criados e incorporados ao acervo.
VIDEO_SUFFIXES={'.mp4','.mov','.webm'}


def aspect(width,height):
    """Formato de tela: horizontal (16:9, YouTube e sites), vertical (9:16, Reels e TikTok) ou quadrado (1:1 e 4:5, feed)."""
    if not width or not height:
        return ''
    ratio=width/height
    return 'horizontal' if ratio>1.2 else 'vertical' if ratio<.85 else 'quadrado'


def probe(path):
    import json,subprocess
    r=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,width,height,r_frame_rate','-of','json',str(path)],capture_output=True,text=True,check=True,timeout=60)
    info=json.loads(r.stdout)
    video=next(s for s in info['streams'] if s['codec_type']=='video')
    num,den=(video.get('r_frame_rate') or '30/1').split('/')
    return {'duration':round(float(info['format']['duration']),2),'width':video['width'],'height':video['height'],
            'fps':round(int(num)/max(1,int(den)),2),'audio':any(s['codec_type']=='audio' for s in info['streams'])}


def frame(video,at,size=480):
    import io,subprocess
    from PIL import Image
    r=subprocess.run(['ffmpeg','-nostdin','-v','error','-ss',f'{at:.2f}','-i',str(video),'-frames:v','1',
                      '-vf',f'scale={size}:{size}:force_original_aspect_ratio=decrease','-f','image2pipe','-vcodec','png','-'],capture_output=True,check=True,timeout=120)
    return Image.open(io.BytesIO(r.stdout)).convert('RGB')


def storyboard(video,out,duration,frames=8):
    """Oito momentos do vídeo numa prancha 4x2, com o tempo de cada um. É o que o agente vê do movimento."""
    from PIL import Image,ImageDraw,ImageFont
    times=[duration*(i+.5)/frames for i in range(frames)]
    shots=[frame(video,t) for t in times]
    w=max(s.width for s in shots);h=max(s.height for s in shots);gap,label=8,26
    sheet=Image.new('RGB',(gap+4*(w+gap),gap+2*(h+label+gap)),(16,16,16))
    draw=ImageDraw.Draw(sheet)
    try:face=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',17)
    except OSError:face=ImageFont.load_default()
    for i,(shot,t) in enumerate(zip(shots,times)):
        x=gap+(i%4)*(w+gap);y=gap+(i//4)*(h+label+gap)
        sheet.paste(shot,(x+(w-shot.width)//2,y+label+(h-shot.height)//2))
        draw.text((x,y+3),f'{i+1} · {t:.1f}s',font=face,fill=(255,140,110))
    sheet.save(out,quality=86)


def loop_clip(video,out,duration,seconds=4):
    """Trecho curto, leve e sem som para o mapa e as listas tocarem sem pesar."""
    import subprocess
    start=0 if duration<=seconds+1 else min(duration*.1,duration-seconds)
    subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-ss',f'{start:.2f}','-t',str(seconds),'-i',str(video),'-an',
                    '-vf','scale=720:-2','-c:v','libx264','-crf','28','-preset','veryfast','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],
                   check=True,capture_output=True,timeout=300)


def search_words(data):
    """Palavras de busca de um vídeo: formato, plataformas e tipos, além do texto da ficha."""
    return ' '.join(['motion','vídeo','animação',ASPECTS.get(data.get('aspect') or '','')]+[GENRES.get(g,g) for g in data.get('genres') or []])
