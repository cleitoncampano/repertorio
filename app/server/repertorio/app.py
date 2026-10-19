import asyncio
import json
import mimetypes
import subprocess
import sys
import threading
import zipfile
from contextlib import asynccontextmanager
from pathlib import Path
from urllib.parse import urlparse

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.trustedhost import TrustedHostMiddleware
from .config import Settings
from .db import Database, dumps
from .service import Library, Problem
from .jobs import Worker, register
from .agent import smart_search, contact_sheet, sheet_items
from . import thumbs
from .backup import weekly
from .locking import lock_file
from .mcp_server import create_mcp
from . import schemas


def create_app(settings=None,run_worker=True):
    settings=settings or Settings.load()
    db=Database(settings);db.migrate();lib=Library(db);worker=Worker(lib)
    mcp=create_mcp(lib,worker);mcp_app=mcp.streamable_http_app()

    @asynccontextmanager
    async def lifespan(app):
        lock=(settings.home.parent/(settings.home.name+'.lock')).open('a+b')
        try:
            lock_file(lock)
        except BlockingIOError:
            lock.close()
            raise RuntimeError('Já existe um serviço usando esta biblioteca.')
        stop_warm=threading.Event()
        try:
            if run_worker:
                worker.start()
                threading.Thread(target=thumbs.warm,args=(lib,stop_warm),daemon=True,name='repertorio-miniaturas').start()
                threading.Thread(target=weekly,args=(lib,stop_warm),daemon=True,name='repertorio-backup').start()
            async with mcp.session_manager.run():yield
        finally:
            stop_warm.set()
            if run_worker:worker.stop()
            db.engine.dispose()
            lock.close()

    app=FastAPI(title='Repertório',version='0.2.1',lifespan=lifespan)
    app.state.library=lib;app.state.worker=worker
    app.add_middleware(TrustedHostMiddleware,allowed_hosts=['localhost','127.0.0.1','testserver'])

    @app.middleware('http')
    async def local_only(request:Request,call_next):
        origin=request.headers.get('origin')
        allowed={settings.url,f'http://localhost:{settings.port}','http://127.0.0.1:5173','http://localhost:5173'}
        if origin and origin not in allowed:
            return JSONResponse({'detail':'Origem não permitida.'},status_code=403)
        if request.headers.get('sec-fetch-site')=='cross-site':
            return JSONResponse({'detail':'Requisição externa bloqueada.'},status_code=403)
        response=await call_next(request)
        response.headers['X-Content-Type-Options']='nosniff'
        response.headers['Referrer-Policy']='same-origin'
        return response

    @app.exception_handler(Problem)
    async def problem_handler(request,exc):
        return JSONResponse({'detail':exc.message},status_code=exc.status)

    @app.get('/api/health')
    def health():return dict(status='ok',version='0.2.1',database='ready',schema='0004',platform=sys.platform,demo=bool(lib.meta('demo',False)))

    @app.get('/api/stats')
    def stats(workspace_id:str):return lib.stats(workspace_id)

    @app.get('/api/workspaces')
    def workspaces():return lib.workspaces()

    @app.post('/api/workspaces')
    def create_workspace(req:schemas.Workspace):return lib.save_workspace(req)

    @app.put('/api/workspaces/{wid}')
    def rename_workspace(wid:str,req:schemas.WorkspaceUpdate):return lib.save_workspace(req,wid)

    @app.post('/api/workspaces/{wid}/state')
    def workspace_state(wid:str,req:schemas.WorkspaceState):return lib.workspace_state(wid,req)

    @app.get('/api/vocabulary')
    def vocab():return lib.meta('vocabulary',{})

    @app.get('/api/fonts')
    def fonts():return lib.meta('fonts',{})

    @app.get('/api/principles/{name}')
    def principles(name:str):return {'text':lib.meta('principles',{}).get(name,'')}

    @app.post('/api/search')
    def search(req:schemas.Search):return lib.search(req)

    @app.post('/api/agent/search')
    def agent_search(req:schemas.AgentSearch):return smart_search(lib,req)

    @app.post('/api/sheet')
    def sheet(req:schemas.Sheet):
        image=contact_sheet(lib,sheet_items(lib,req.ids,req.workspace_ids,req.context_id))
        if not image:raise Problem(404,'Nenhuma referência encontrada.')
        return Response(image,media_type='image/jpeg')

    @app.get('/api/graph')
    def graph(workspace_id:str):return lib.graph(workspace_id)

    @app.get('/api/previews')
    def previews(workspace_id:str,w:int=128):
        if w not in thumbs.SIZES:raise Problem(422,'Tamanhos disponíveis: '+', '.join(map(str,sorted(thumbs.SIZES))))
        return JSONResponse(thumbs.bundle(lib,w,workspace_id),headers={'Cache-Control':'private, max-age=300'})

    @app.get('/api/references/{rid}')
    def reference(rid:str,workspace_id:str|None=None,context_id:str|None=None):return lib.get(rid,workspace_ids=[workspace_id] if workspace_id else None,context_id=context_id)

    @app.post('/api/references/{rid}/workspaces')
    def reference_workspaces(rid:str,req:schemas.ReferenceWorkspaces):return lib.reference_workspaces(rid,req,from_ui=True)

    @app.post('/api/agent/references/{rid}/workspaces')
    def agent_reference_workspaces(rid:str,req:schemas.ReferenceWorkspaces):return lib.reference_workspaces(rid,req)

    @app.put('/api/references/{rid}')
    def update(rid:str,req:schemas.Update):return lib.update(rid,req)

    @app.post('/api/references/{rid}/state')
    def state(rid:str,req:schemas.StateChange):return lib.state(rid,req,from_ui=True)

    @app.post('/api/references')
    def create(req:schemas.Register):return register(lib,req)

    @app.get('/api/projects')
    def projects():return db.query('SELECT * FROM projects ORDER BY name')

    @app.post('/api/projects')
    def project(req:schemas.Project):return lib.project(req)

    @app.post('/api/contexts')
    def context(req:schemas.StartContext):return lib.start(req)

    @app.get('/api/contexts/{cid}')
    def get_context(cid:str):return {'context':lib.context(cid),'packs':db.query('SELECT id,title,created FROM packs WHERE context_id=:id',id=cid)}

    @app.post('/api/packs')
    def pack(req:schemas.Pack):return lib.pack(req)

    @app.get('/api/packs/{pid}')
    def get_pack(pid:str):return lib.pack_detail(pid)

    @app.post('/api/packs/{pid}/reviews')
    def review_pack(pid:str,req:schemas.Review):return lib.review(pid,req)

    @app.get('/api/demands')
    def demands(workspace_id:str):return lib.demands(workspace_id)

    @app.get('/api/operations')
    def operations(workspace_id:str):return lib.operations(workspace_id)

    @app.get('/api/operations/{oid}')
    def operation(oid:str):return lib.operation(oid)

    @app.post('/api/operations/{oid}/retry')
    def retry(oid:str):return worker.retry(oid)

    @app.get('/api/activity')
    def activity(workspace_id:str):return lib.events(workspace_id=workspace_id)

    @app.get('/api/events')
    async def events(request:Request,after:int=0,workspace_id:str|None=None):
        if workspace_id:lib.workspace(workspace_id)
        async def stream():
            cursor=after
            while not await request.is_disconnected():
                items=await asyncio.to_thread(lib.events,cursor,workspace_id)
                for item in reversed(items):
                    cursor=max(cursor,item['id'])
                    yield f'id: {cursor}\ndata: {dumps(item)}\n\n'
                if not items:yield ': heartbeat\n\n'
                await asyncio.sleep(1)
        return StreamingResponse(stream(),media_type='text/event-stream',headers={'Cache-Control':'no-cache'})

    def get_asset(aid):
        row=db.one('SELECT * FROM assets WHERE id=:id',id=aid)
        if not row:raise Problem(404,'Arquivo não encontrado.')
        path=Path(row['path']).resolve()
        if not (path.is_relative_to(settings.root) or path.is_relative_to(settings.home)):
            raise Problem(403,'Arquivo fora do acervo.')
        if not path.is_file():raise Problem(404,'O arquivo original não está disponível neste computador.')
        return row,path

    @app.get('/api/assets/{aid}')
    def get_file(aid:str,download:bool=False,w:int|None=None):
        row,path=get_asset(aid)
        if w is not None and w not in thumbs.SIZES:raise Problem(422,'Tamanhos disponíveis: '+', '.join(map(str,sorted(thumbs.SIZES))))
        if row['member']:
            with zipfile.ZipFile(path) as z:
                try:info=z.getinfo(row['member'])
                except KeyError:raise Problem(404,'Mídia não encontrada no arquivo original.')
                if info.file_size>200_000_000:raise Problem(413,'Mídia muito grande para extração direta.')
                return Response(z.read(info),media_type='application/octet-stream',headers={'Content-Disposition':f'attachment; filename="media{Path(info.filename).suffix}"'})
        raster=path.suffix.lower() in {'.jpg','.jpeg','.png','.webp','.gif'}
        inline=row['role'] in ('preview','thumbnail') and raster and not download
        if inline and w:
            small=thumbs.thumbnail(settings,aid,path,w)
            if small:return FileResponse(small,media_type='image/webp',headers={'Cache-Control':'private, max-age=604800'})
        return FileResponse(path,media_type=row['mime'] if inline else 'application/octet-stream',filename=path.name,
                            content_disposition_type='inline' if inline else 'attachment',headers={'Cache-Control':'private, max-age=3600'} if inline else {})

    @app.post('/api/assets/{aid}/open')
    def open_file(aid:str):
        row,path=get_asset(aid)
        if row['member'] or path.suffix.lower() not in {'.pptx','.pdf'}:raise Problem(422,'Abertura local disponível para PPTX e PDF.')
        if sys.platform=='win32':
            import os
            os.startfile(str(path))
        elif sys.platform=='darwin':subprocess.run(['open',str(path)],check=True)
        else:raise Problem(422,'Use Baixar original neste sistema.')
        return {'ok':True}

    # Mount at the root after API routes, before the SPA catch-all; /mcp is handled by the SDK.
    for route in mcp_app.routes:app.router.routes.append(route)
    dist=settings.root/'app/web/dist'
    if dist.exists():
        if (dist/'assets').exists():app.mount('/assets',StaticFiles(directory=dist/'assets'),name='web-assets')
        @app.get('/{path:path}')
        def spa(path:str):
            if path.startswith(('api/','mcp')):raise Problem(404,'Rota não encontrada.')
            return FileResponse(dist/'index.html')
    return app
