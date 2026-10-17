from fastapi.testclient import TestClient
from repertorio.app import create_app
from repertorio.schemas import Search


def test_api_search_matches_service_and_origins(library):
    with TestClient(create_app(library.settings,run_worker=False),base_url='http://127.0.0.1:8767') as client:
        query={'query':'abertura','kind':'slide'}
        response=client.post('/api/search',json=query)
        assert response.status_code==200
        assert response.json()==library.search(Search(**query))
        assert client.get('/api/health',headers={'Origin':'https://attacker.test'}).status_code==403
        assert client.get('/api/health',headers={'Host':'attacker.test'}).status_code==400
        assert client.get('/api/assets/missing').status_code==404
        assert client.post('/api/search',json={'limit':50000}).status_code==422
        smart=client.post('/api/agent/search',json={'query':'abertura com fundo escuro'}).json()
        assert smart['items'][0]['id']=='deck' and smart['understood']
        sheet=client.post('/api/sheet',json={'ids':['deck','deck#1']})
        assert sheet.status_code==200 and sheet.headers['content-type']=='image/jpeg'
        assert client.post('/api/sheet',json={'ids':['nada']}).status_code==404


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
        assert len(result['tools'])==8
        result=rpc('tools/call',{'name':'search_references','arguments':{'request':{'query':'abertura','context_id':context['id']}}})['result']
        assert not result.get('isError'),result
        assert any(c['type']=='image' for c in result['content'])
        assert '"understood"' in result['content'][0]['text']
        result=rpc('tools/call',{'name':'get_reference','arguments':{'reference_id':'deck','include_image':True}})['result']
        assert not result.get('isError'),result
        assert any(c['type']=='image' for c in result['content'])
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
        bundle=client.get('/api/previews?w=128').json()
        assert bundle and all(v['src'].startswith('data:image/') and v['width']>0 for v in bundle.values())
        assert client.get('/api/previews?w=100').status_code==422
