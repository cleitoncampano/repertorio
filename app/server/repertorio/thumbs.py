"""Cópias reduzidas das prévias para o mapa e as listas. O original continua intacto e é o que vai para download."""
import base64
import logging
import os
import threading
from pathlib import Path
from PIL import Image, ImageOps

# Maior lado em pixels. O mapa usa 128 a 1024 conforme o zoom (o maior nó, no zoom máximo de 400% e em tela Retina, ocupa 720 px).
SIZES={128,256,512,1024,2048}
RASTER={'.jpg','.jpeg','.png','.webp','.gif'}


def thumbnail(settings,aid,path,width):
    """Devolve o caminho da cópia em WebP, ou None quando o original já é pequeno o bastante."""
    path=Path(path)
    out=settings.home/'miniaturas'/f'{aid}-{width}.webp'
    try:
        if out.stat().st_mtime>=path.stat().st_mtime:return out
    except FileNotFoundError:
        pass
    with Image.open(path) as im:
        if max(im.size)<=width:return None
        im.draft('RGB',(width,width))  # JPEG já decodifica reduzido, sem abrir o arquivo inteiro
        im=ImageOps.exif_transpose(im)
        im.thumbnail((width,width),Image.LANCZOS)
        alpha=im.mode in ('RGBA','LA','PA') or (im.mode=='P' and 'transparency' in im.info)
        im=im.convert('RGBA' if alpha else 'RGB')
        out.parent.mkdir(parents=True,exist_ok=True)
        temporary=out.with_name(f'{out.stem}.{os.getpid()}.{threading.get_ident()}.tmp')
        im.save(temporary,'WEBP',quality=86,method=4)
        os.replace(temporary,out)
    return out


def graph_assets(lib,workspace_id=None):
    """Prévia de cada peça do mapa: (id do arquivo, caminho), só imagens."""
    ids=lib.scope([workspace_id]) if workspace_id else [w['id'] for w in lib.workspaces()]
    params={}
    clause=lib.membership_clause(ids,params,'published')
    rows=lib.db.query(f"""SELECT a.id AS aid,a.path FROM refs r JOIN assets a ON a.id=(SELECT b.id FROM assets b WHERE b.ref_id=r.id AND b.missing=0 AND b.role IN ('thumbnail','preview') ORDER BY CASE b.role WHEN 'thumbnail' THEN 0 ELSE 1 END,b.id LIMIT 1)
        WHERE {clause} AND r.ready=1 AND r.hidden=0 AND r.kind IN ('arquivo','referencia','criacao')""",**params)
    return [(r['aid'],Path(r['path'])) for r in rows if Path(r['path']).suffix.lower() in RASTER]


def image_aspect(path):
    """Formato de tela de uma imagem, pelo tamanho gravado no cabeçalho (não decodifica a imagem)."""
    from .motion import aspect
    try:
        with Image.open(path) as im:return aspect(*im.size)
    except (OSError,ValueError):return ''


def backfill_aspects(lib,stop=None):
    """Grava o formato de tela das peças do mapa que ainda não têm, para a organização por formato.
    Fica na própria ficha: o mapa continua com as mesmas consultas."""
    from sqlalchemy import text
    rows=lib.db.query("""SELECT r.id,(SELECT a.path FROM assets a WHERE a.ref_id=r.id AND a.missing=0 AND a.role IN ('preview','thumbnail')
        ORDER BY CASE a.role WHEN 'preview' THEN 0 ELSE 1 END,a.id LIMIT 1) AS path FROM refs r
        WHERE r.kind IN ('arquivo','referencia','criacao') AND json_extract(r.payload,'$.aspect') IS NULL""")
    found=[(r['id'],image_aspect(r['path'])) for r in rows if r['path'] and not (stop and stop.is_set())]
    with lib.db.engine.begin() as conn:
        for rid,value in found:
            if value:conn.execute(text("UPDATE refs SET payload=json_set(payload,'$.aspect',:a) WHERE id=:id"),dict(a=value,id=rid))
    return sum(1 for _,v in found if v)


def warm(lib,stop,sizes=(128,256)):
    """Prepara as cópias que a primeira abertura do mapa pede, para ela não esperar por elas."""
    try:backfill_aspects(lib,stop)
    except Exception:logging.exception('Não foi possível gravar os formatos de tela')
    for aid,path in graph_assets(lib):
        if stop.is_set():return
        for width in sizes:
            try:thumbnail(lib.settings,aid,path,width)
            except Exception:logging.exception('Não foi possível reduzir %s',path)


def bundle(lib,width,workspace_id):
    """Todas as miniaturas já preparadas do mapa numa resposta só, por endereço da prévia.
    As que ainda não existem ficam de fora e o mapa as pede uma a uma."""
    out={}
    for aid,path in graph_assets(lib,workspace_id):
        small=lib.settings.home/'miniaturas'/f'{aid}-{width}.webp'
        try:
            fresh=small.exists() and small.stat().st_mtime>=path.stat().st_mtime
            with Image.open(small if fresh else path) as im:
                if not fresh and max(im.size)>width:continue  # ainda sem cópia: fica para o pedido individual
                size,mime=im.size,Image.MIME.get(im.format,'image/jpeg')
            data=(small if fresh else path).read_bytes()
        except (OSError,ValueError):
            continue
        out[f'/api/assets/{aid}']={'src':f'data:{mime};base64,'+base64.b64encode(data).decode(),'width':size[0],'height':size[1]}
    return out
