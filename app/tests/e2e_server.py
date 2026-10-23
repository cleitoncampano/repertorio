"""Servidor descartável para Playwright. Nunca altera o acervo real."""
import sys
import os
import tempfile
from pathlib import Path
import uvicorn

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'server'))
from conftest import library,context
from repertorio.app import create_app
from repertorio.schemas import Project

with tempfile.TemporaryDirectory(prefix='repertorio-e2e-') as temp:
    tmp=Path(temp)
    os.environ.setdefault('REPERTORIO_BACKUP_DIR',str(tmp/'backups'))
    fixture=library.__wrapped__(tmp)
    lib=next(fixture)
    context.__wrapped__(lib,tmp)
    sales=tmp/'sales';sales.mkdir()
    lib.project(Project(name='Comercial',root=str(sales)))
    # Espaço com um vídeo de motion; com ffmpeg, o arquivo toca de verdade no navegador.
    from test_motion import motion_library
    from repertorio.motion import import_motion
    import shutil,subprocess
    motion=motion_library(lib)
    if shutil.which('ffmpeg'):
        for name in ('loop.mp4','video.mp4'):
            subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-f','lavfi','-i','testsrc=size=320x180:rate=24:duration=2','-pix_fmt','yuv420p',str(lib.settings.root/'_originais/motion/giro'/name)],check=True)
    # Um segundo vídeo para passar de um a outro no player.
    import json
    fichas=lib.settings.root/'dados/motion/teste.jsonl';first=json.loads(fichas.read_text())
    fichas.write_text(fichas.read_text()+json.dumps({**first,'id':'motion-onda','slug':'onda','title':'Onda de partículas que vira logo','strength':3},ensure_ascii=False)+'\n')
    import_motion(lib.db,motion)
    web=lib.settings.root/'app/web';web.mkdir(parents=True)
    (web/'dist').symlink_to(BASE/'web/dist',target_is_directory=True)
    try:uvicorn.run(create_app(lib.settings),host='127.0.0.1',port=8767,log_level='warning')
    finally:fixture.close()
