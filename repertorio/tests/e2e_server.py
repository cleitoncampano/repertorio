"""Servidor descartável para Playwright. Nunca altera o acervo real."""
import sys
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
    fixture=library.__wrapped__(tmp)
    lib=next(fixture)
    context.__wrapped__(lib,tmp)
    sales=tmp/'sales';sales.mkdir()
    lib.project(Project(name='Comercial',root=str(sales)))
    web=lib.settings.root/'repertorio/web';web.mkdir(parents=True)
    (web/'dist').symlink_to(BASE/'web/dist',target_is_directory=True)
    try:uvicorn.run(create_app(lib.settings),host='127.0.0.1',port=8767,log_level='warning')
    finally:fixture.close()
