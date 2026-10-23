import hashlib
import json
import shutil
import threading
import uuid
import zipfile
from pathlib import Path
from PIL import Image, ImageOps
from sqlalchemy import text
from .db import dumps, now
from .importer import asset, index_text
from .service import Problem
from .motion import VIDEO_SUFFIXES, aspect, frame, loop_clip, probe, search_words, storyboard

ALLOWED={'.png','.jpg','.jpeg','.webp','.gif','.pdf','.pptx','.html','.mp4','.mov','.webm'}
PREVIEWS={'.png','.jpg','.jpeg','.webp'}


def file_digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def project_file(root,value,preview=False):
    p=Path(value).expanduser()
    p=(root/p).resolve() if not p.is_absolute() else p.resolve()
    if not p.is_relative_to(root) or not p.is_file():
        raise Problem(422,'O arquivo deve existir dentro da pasta cadastrada do projeto.')
    if p.suffix.lower() not in (PREVIEWS if preview else ALLOWED):
        raise Problem(422,'Formato não aceito: '+p.suffix)
    if p.stat().st_size>1024*1024*1024:
        raise Problem(422,'O limite é 1 GB por arquivo.')
    return p


def register(lib,req):
    context=lib.context(req.context_id)
    source_ids=lib.scope(context_id=req.context_id)
    targets=lib.scope(req.target_workspace_ids)
    lib.validate_data(req.data,source_ids)
    root=Path(context['root'])
    paths=[project_file(root,p) for p in req.files]
    previews=[project_file(root,p,True) for p in req.previews]
    hashes=[file_digest(p) for p in paths+previews]
    request_key=context['project_id']+':'+req.request_key
    fingerprint=hashlib.sha256(dumps(dict(data=req.data.model_dump(),hashes=hashes,user_requested=req.user_requested,target_workspace_ids=sorted(targets))).encode()).hexdigest()
    previous=lib.db.one('SELECT id,payload FROM operations WHERE request_key=:k',k=request_key)
    def same_request(previous):
        saved=json.loads(previous['payload'])['fingerprint']
        if saved==fingerprint:return True
        # Envios feitos antes dos espaços continuam retomáveis no destino migrado.
        legacy=hashlib.sha256(dumps(dict(data=req.data.model_dump(),hashes=hashes,user_requested=req.user_requested)).encode()).hexdigest()
        return saved==legacy and set(lib.operation(previous['id'])['target_workspace_ids'])==set(targets)
    if previous:
        if not same_request(previous):
            raise Problem(409,'Esta chave de envio já foi usada para outro conteúdo.')
        return lib.operation(previous['id'])
    oid=str(uuid.uuid4()); rid='criacao-'+str(uuid.uuid4()); stamp=now()
    data={**req.data.model_dump(),'project_id':context['project_id'],'project_name':context['project_name'],
          'format':paths[0].suffix.lstrip('.'),'fingerprint':fingerprint}
    job=dict(files=[str(p) for p in paths],previews=[str(p) for p in previews],hashes=hashes,fingerprint=fingerprint)
    from sqlalchemy.exc import IntegrityError
    try:
        with lib.db.engine.begin() as conn:
            conn.execute(text("INSERT INTO refs(id,kind,title,origin,state,ready,curated,payload,search_text,created,updated) VALUES(:id,'criacao',:t,'criacao',:state,0,1,:p,:s,:d,:d)"),
                         dict(id=rid,t=data['title'],state='published' if req.user_requested else 'pending',p=dumps(data),s=index_text(data),d=stamp))
            conn.execute(text("INSERT INTO operations(id,context_id,ref_id,request_key,state,payload,created,updated) VALUES(:id,:c,:r,:k,'queued',:p,:d,:d)"),
                         dict(id=oid,c=req.context_id,r=rid,k=request_key,p=dumps(job),d=stamp))
            for wid in targets:
                conn.execute(text('INSERT INTO workspace_references(workspace_id,ref_id,state,created,updated) VALUES(:w,:r,:s,:t,:t)'),dict(w=wid,r=rid,s='published' if req.user_requested else 'pending',t=stamp))
                conn.execute(text('INSERT INTO operation_workspaces VALUES(:o,:w)'),dict(o=oid,w=wid))
            lib.db.log(conn,'reference_submitted',rid,req.context_id,workspace_ids=targets,user_requested=req.user_requested,operation_id=oid)
    except IntegrityError:
        previous=lib.db.one('SELECT id,payload FROM operations WHERE request_key=:k',k=request_key)
        if not previous or not same_request(previous):raise Problem(409,'Envio concorrente com conteúdo diferente.')
        return lib.operation(previous['id'])
    return lib.operation(oid)


class Worker:
    def __init__(self,lib):
        self.lib=lib;self.stop_event=threading.Event();self.thread=None

    def start(self):
        with self.lib.db.engine.begin() as conn:
            conn.execute(text("UPDATE operations SET state='queued',updated=:t WHERE state='running'"),dict(t=now()))
        self.thread=threading.Thread(target=self.loop,daemon=True,name='repertorio-imports');self.thread.start()

    def stop(self):
        self.stop_event.set()
        if self.thread:self.thread.join(timeout=10)

    def loop(self):
        while not self.stop_event.is_set():
            try:
                row=self.lib.db.one("SELECT * FROM operations WHERE state='queued' ORDER BY created LIMIT 1")
                if row:self.process(row['id'])
                else:self.stop_event.wait(.5)
            except Exception:
                import logging
                logging.exception('Falha transitória no worker; a fila permanece persistida.')
                self.stop_event.wait(1)

    def process(self,oid):
        row=self.lib.db.one('SELECT * FROM operations WHERE id=:id',id=oid)
        if not row:return
        with self.lib.db.engine.begin() as conn:
            claimed=conn.execute(text("UPDATE operations SET state='running',error=NULL,updated=:t WHERE id=:id AND state='queued'"),dict(t=now(),id=oid))
            if claimed.rowcount!=1:return
        try:
            job=json.loads(row['payload']);rid=row['ref_id']
            root=Path(self.lib.context(row['context_id'])['root'])
            dest=self.lib.settings.home/'assets'/rid;dest.mkdir(parents=True,exist_ok=True)
            records=[];generated=[]
            allpaths=job['files']+job['previews']
            for i,value in enumerate(allpaths):
                is_preview=i>=len(job['files'])
                p=project_file(root,value,is_preview)
                if file_digest(p)!=job['hashes'][i]:raise ValueError('O arquivo mudou desde o envio. Reenvie com uma nova chave.')
                target=dest/f'{i:03d}{p.suffix.lower()}'
                tmp=target.with_suffix(target.suffix+'.tmp');shutil.copyfile(p,tmp);tmp.replace(target)
                records.append((target,'preview' if is_preview else 'original'))
                if is_preview:generated.append(target)
                elif p.suffix.lower() in PREVIEWS|{'.gif'}:generated.append(target)
                with self.lib.db.engine.begin() as conn:
                    conn.execute(text('UPDATE operations SET progress=:p,updated=:t WHERE id=:id'),dict(p=int(60*(i+1)/len(allpaths)),t=now(),id=oid))
            if not generated:
                first=records[0][0]
                if first.suffix=='.pdf':
                    import pymupdf
                    with pymupdf.open(first) as pdf:
                        for n in range(min(len(pdf),30)):
                            p=dest/f'page-{n+1:03d}.png'
                            pdf[n].get_pixmap(matrix=pymupdf.Matrix(1,1)).save(p);generated.append(p)
                elif first.suffix=='.pptx':
                    with zipfile.ZipFile(first) as z:
                        match=next((n for n in z.namelist() if n.lower() in ('docprops/thumbnail.jpeg','docprops/thumbnail.png')),None)
                        if match and z.getinfo(match).file_size<10_000_000:
                            p=dest/('cover'+Path(match).suffix);p.write_bytes(z.read(match));generated.append(p)
                elif first.suffix in VIDEO_SUFFIXES and shutil.which('ffmpeg'):
                    p=dest/'frame.jpg'
                    duration=probe(first)['duration'] if shutil.which('ffprobe') else 0
                    frame(first,duration*.1,1000).save(p,quality=90)
                    generated.append(p)
            if not generated:
                raise ValueError('Prévia necessária. Envie imagens em previews junto com o material; HTML nunca é executado para gerar a prévia.')
            # Normalize all previews to raster images before exposing to browser/MCP.
            normalized=[]
            for i,p in enumerate(generated):
                target=dest/f'preview-{i:03d}.jpg'
                with Image.open(p) as image:
                    image=ImageOps.exif_transpose(image).convert('RGB');image.thumbnail((1600,1600));image.save(target,quality=87)
                normalized.append(target)
            thumb=dest/'thumbnail.jpg'
            with Image.open(normalized[0]) as image:
                image.thumbnail((320,320));image.save(thumb,quality=80)
            # Vídeo criado entra como os da galeria de motion: prancha de quadros, loop curto, formato e player.
            video=next((p for p,role in records if role=='original' and p.suffix in VIDEO_SUFFIXES),None)
            motion=None
            if video and shutil.which('ffmpeg') and shutil.which('ffprobe'):
                meta=probe(video);board=dest/'quadros.jpg';clip=dest/'loop.mp4'
                storyboard(video,board,meta['duration']);loop_clip(video,clip,meta['duration'])
                motion=(video,board,clip,meta)
            with self.lib.db.engine.begin() as conn:
                originals={p:asset(conn,self.lib.settings,rid,p,role) for p,role in records if role=='original'}
                for p in normalized:asset(conn,self.lib.settings,rid,p,'preview')
                asset(conn,self.lib.settings,rid,thumb,'thumbnail')
                if not motion:
                    # Imagem: o formato de tela vem da primeira prévia, para a organização por formato.
                    with Image.open(normalized[0]) as image:shape=aspect(*image.size)
                    conn.execute(text("UPDATE refs SET payload=json_set(payload,'$.aspect',:a) WHERE id=:id"),dict(a=shape,id=rid))
                if motion:
                    video,board,clip,meta=motion
                    payload=json.loads(conn.execute(text('SELECT payload FROM refs WHERE id=:id'),dict(id=rid)).scalar())
                    payload.update(motion={'video':originals[video],'storyboard':asset(conn,self.lib.settings,rid,board,'storyboard'),'loop':asset(conn,self.lib.settings,rid,clip,'motion')},
                                   video={k:meta[k] for k in ('duration','width','height','fps','audio')},aspect=aspect(meta['width'],meta['height']),text=payload.get('prompt') or '')
                    payload['keywords']=search_words(payload)
                    conn.execute(text('UPDATE refs SET payload=:p,search_text=:s WHERE id=:id'),dict(p=dumps(payload),s=index_text(payload),id=rid))
                conn.execute(text('UPDATE refs SET ready=1,updated=:t WHERE id=:id'),dict(t=now(),id=rid))
                conn.execute(text("UPDATE operations SET state='completed',progress=100,updated=:t WHERE id=:id"),dict(t=now(),id=oid))
                self.lib.db.log(conn,'reference_ready',rid,row['context_id'],workspace_ids=self.lib.operation(oid)['target_workspace_ids'],operation_id=oid)
        except Exception as exc:
            with self.lib.db.engine.begin() as conn:
                conn.execute(text("UPDATE operations SET state='failed',error=:e,updated=:t WHERE id=:id"),dict(e=str(exc)[:1500],t=now(),id=oid))
                self.lib.db.log(conn,'operation_failed',row['ref_id'],row['context_id'],workspace_ids=self.lib.operation(oid)['target_workspace_ids'],operation_id=oid,error=str(exc)[:1500])

    def retry(self,oid):
        with self.lib.db.engine.begin() as conn:
            conn.execute(text("UPDATE operations SET state='queued',error=NULL,progress=0,updated=:t WHERE id=:id AND state='failed'"),dict(t=now(),id=oid))
        return self.lib.operation(oid)
