import json
from pathlib import Path
from alembic.config import Config
from alembic.script import ScriptDirectory
from fastapi.testclient import TestClient
import repertorio
from repertorio.app import create_app
from repertorio.schemas import Search


def test_api_search_matches_service_and_origins(library):
    with TestClient(create_app(library.settings,run_worker=False),base_url='http://127.0.0.1:8767') as client:
        query={'query':'abertura','kind':'slide','workspace_ids':['referencias']}
        response=client.post('/api/search',json=query)
        assert response.status_code==200
        assert response.json()==library.search(Search(**query))
        health=client.get('/api/health').json()
        script=ScriptDirectory.from_config(Config(str(Path(repertorio.__file__).parents[1]/'alembic.ini')))
        assert health['version']==repertorio.__version__ and health['schema']==script.get_current_head() and health['database']=='ready'
        assert client.get('/api/health',headers={'Origin':'https://attacker.test'}).status_code==403
        assert client.get('/api/health',headers={'Host':'attacker.test'}).status_code==400
        assert client.get('/api/assets/missing').status_code==404
        assert client.post('/api/search',json={'limit':50000}).status_code==422
        smart=client.post('/api/agent/search',json={'query':'abertura com fundo escuro','workspace_ids':['referencias']}).json()
        assert smart['items'][0]['id']=='deck' and smart['understood']
        sheet=client.post('/api/sheet',json={'workspace_ids':['referencias'],'ids':['deck','deck#1']})
        assert sheet.status_code==200 and sheet.headers['content-type']=='image/jpeg'
        assert client.post('/api/sheet',json={'workspace_ids':['referencias'],'ids':['nada']}).status_code==404


def test_mcp_protocol_tools_and_image(library,context):
    with TestClient(create_app(library.settings,run_worker=False),base_url='http://127.0.0.1:8767') as client:
        headers={'Accept':'application/json, text/event-stream','MCP-Protocol-Version':'2025-11-25'}
        def rpc(method,params=None):
            response=client.post('/mcp',headers=headers,json={'jsonrpc':'2.0','id':1,'method':method,'params':params or {}})
            assert response.status_code==200,response.text
            return response.json()
        init=rpc('initialize',{'protocolVersion':'2025-11-25','capabilities':{},'clientInfo':{'name':'repertorio-test','version':'1'}})
        assert init['result']['serverInfo']['name']=='Repertorio'
        result=rpc('tools/list')['result']
        assert {'list_workspaces','create_workspace','delete_workspace','set_reference_workspaces'}.issubset({t['name'] for t in result['tools']})
        result=rpc('tools/call',{'name':'search_references','arguments':{'request':{'query':'abertura','context_id':context['id']}}})['result']
        assert not result.get('isError'),result
        assert any(c['type']=='image' for c in result['content'])
        assert '"understood"' in result['content'][0]['text']
        result=rpc('tools/call',{'name':'get_reference','arguments':{'reference_id':'deck','include_image':True,'workspace_ids':['referencias']}})['result']
        assert not result.get('isError'),result
        assert any(c['type']=='image' for c in result['content'])
        ref=json.loads(result['content'][0]['text'])
        assert ref['children']==[{'id':'deck#1','number':1,'title':'Abertura','idea':ref['children'][0]['idea'],'url':ref['children'][0]['url']}]
        resources=rpc('resources/read',{'uri':'repertorio://projects'})['result']
        assert 'Marketing' in resources['contents'][0]['text']


def test_resized_previews_keep_originals(library,tmp_path):
    from PIL import Image
    from repertorio import thumbs
    big=library.settings.root/'assets/big.jpg';Image.new('RGB',(1600,900),'#336699').save(big)
    small=thumbs.thumbnail(library.settings,'a1',big,512)
    with Image.open(small) as im:assert im.format=='WEBP' and im.size==(512,288)
    stamp=small.stat().st_mtime_ns
    assert thumbs.thumbnail(library.settings,'a1',big,512).stat().st_mtime_ns==stamp
    assert thumbs.thumbnail(library.settings,'a1',big,2048) is None
    aid=library.db.one("SELECT id FROM assets WHERE ref_id='deck' AND role='preview'")['id']
    with TestClient(create_app(library.settings,run_worker=False),base_url='http://127.0.0.1:8767') as client:
        assert client.get(f'/api/assets/{aid}?w=999').status_code==422
        response=client.get(f'/api/assets/{aid}?w=128')
        assert response.status_code==200 and response.headers['content-type']=='image/png'
        bundle=client.get('/api/previews?workspace_id=referencias&w=128').json()
        assert bundle and all(v['src'].startswith('data:image/') and v['width']>0 for v in bundle.values())
        assert client.get('/api/previews?workspace_id=referencias&w=100').status_code==422


def test_live_events_start_at_latest_and_keep_bursts_in_order(library):
    start=library.last_event()
    with library.db.engine.begin() as conn:
        for n in range(150):library.db.log(conn,'workspace_created',workspace_ids=['referencias'],title=f'espaço {n}')
    first=library.events(start,'referencias',True)
    assert [e['payload']['title'] for e in first]==[f'espaço {n}' for n in range(100)]
    rest=library.events(first[-1]['id'],'referencias',True)
    assert [e['payload']['title'] for e in rest]==[f'espaço {n}' for n in range(100,150)]
    assert library.last_event()==rest[-1]['id']
    assert library.events(library.last_event(),None,True)==[]
    assert library.events(workspace_id='referencias')[0]['payload']['title']=='espaço 149'


def test_slow_mcp_tool_does_not_freeze_the_service(library,monkeypatch):
    import asyncio,time,httpx
    app=create_app(library.settings,run_worker=False)
    real=library.workspaces
    def slow():
        time.sleep(1.2);return real()
    monkeypatch.setattr(app.state.library,'workspaces',slow)
    async def scenario():
        async with app.router.lifespan_context(app):
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://127.0.0.1:8767') as client:
                headers={'Accept':'application/json, text/event-stream','MCP-Protocol-Version':'2025-11-25'}
                # A ferramenta leva 1,2 s; com o serviço livre, a verificação de saúde volta bem antes disso.
                started=time.monotonic()
                call=asyncio.create_task(client.post('/mcp',headers=headers,json={'jsonrpc':'2.0','id':1,'method':'tools/call','params':{'name':'list_workspaces','arguments':{}}}))
                await asyncio.sleep(.2)
                health=await client.get('/api/health');waited=time.monotonic()-started
                tool=await call
                return health.status_code,waited,tool.json()
    status,waited,tool=asyncio.run(scenario())
    assert status==200 and waited<.9,waited
    assert not tool['result'].get('isError'),tool


def test_skill_content_reads_installed_text_only(library,tmp_path,monkeypatch):
    first,second=tmp_path/'claude',tmp_path/'agents'
    skill=second/'frontend-design';(skill/'references').mkdir(parents=True);(skill/'node_modules').mkdir();(skill/'.git').mkdir()
    (skill/'SKILL.md').write_text('---\nname: frontend-design\ndescription: Interfaces.\n---\n\n# Frontend\n\nUse [o guia](references/guia.md).\n')
    (skill/'references/guia.md').write_text('# Guia')
    (skill/'node_modules/x.md').write_text('fora');(skill/'.git/HEAD.md').write_text('fora');(skill/'script.py').write_text('fora')
    (tmp_path/'segredo.md').write_text('fora')
    (first/'impeccable').mkdir(parents=True)
    monkeypatch.setenv('REPERTORIO_SKILL_DIRS',f'{first}:{second}')
    (library.settings.home/'catalogo.json').write_text(json.dumps({'skills':[{'id':'frontend-design'},{'id':'impeccable'},{'id':'plugin:Nome'},{'id':'..'}]}))
    data=library.skill_content('frontend-design')
    assert data['content'].startswith('# Frontend') and 'description:' not in data['content']
    assert data['files']==['references/guia.md'] and data['file']=='SKILL.md'
    assert library.skill_content('frontend-design','references/guia.md')['content']=='# Guia'
    with TestClient(create_app(library.settings,run_worker=False),base_url='http://127.0.0.1:8767') as client:
        assert client.get('/api/skills/frontend-design/content').json()['files']==['references/guia.md']
        for path in ['/api/skills/frontend-design/content?file=../../segredo.md','/api/skills/frontend-design/content?file=script.py',
                     '/api/skills/frontend-design/content?file=node_modules/x.md','/api/skills/impeccable/content','/api/skills/nao-existe/content',
                     '/api/skills/plugin:Nome/content','/api/skills/../content']:
            response=client.get(path)
            assert response.status_code==404 and response.json()['detail'],path
        assert client.get('/api/skills/plugin:Nome/content').json()['detail']=='Esta skill não está instalada neste computador.'


def test_catalog_prefers_user_file_then_library_then_package(library):
    import json
    default=library.catalog()
    assert not default['personal'] and default['skills'] and default['repos']
    assert not any(s['id'].startswith(('perestroika','soap')) for s in default['skills'])
    assert all(s.get('source','').startswith('https://github.com/') for s in default['skills'])
    (library.settings.root/'dados/catalogo.json').write_text(json.dumps({'skills':[{'id':'a'}],'repos':[]}))
    assert library.catalog()=={'skills':[{'id':'a'}],'repos':[],'personal':True}
    (library.settings.home/'catalogo.json').write_text(json.dumps({'skills':[{'id':'b'}]}))
    with TestClient(create_app(library.settings,run_worker=False),base_url='http://127.0.0.1:8767') as client:
        assert client.get('/api/catalog').json()=={'skills':[{'id':'b'}],'repos':[],'personal':True}
