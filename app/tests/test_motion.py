import json
from PIL import Image
from fastapi.testclient import TestClient
from repertorio import schemas as s
from repertorio.agent import contact_sheet, smart_search
from repertorio.app import create_app
from repertorio.motion import import_motion


def motion_library(library):
    root=library.settings.root
    media=root/'_originais/motion/giro';media.mkdir(parents=True)
    Image.new('RGB',(720,406),'#202020').save(media/'capa.png')
    Image.new('RGB',(1600,600),'#303030').save(media/'quadros.jpg')
    (media/'loop.mp4').write_bytes(b'\x00'*4000)
    (media/'video.mp4').write_bytes(b'\x01'*9000)
    record={'id':'motion-giro','slug':'giro','collection':'prompt-motion','title':'Logo que gira e se aproxima',
            'description':'Vinheta escura em que o logo gira.','idea':'Faça a marca girar antes de revelar o nome.',
            'how':'0 a 2 s: o logo gira. 2 a 4 s: zoom até o nome.','html':'GSAP com rotação e escala.',
            'techniques':['contraste'],'intentions':['ABRIR'],'movements':['zoom'],'aesthetics':['escuro'],'strength':4,
            'cautions':'Uma vez por vídeo basta.','prompt':'Make a 4 second logo sting that spins and zooms.',
            'author':'Ana','handle':'ana','post':'https://x.com/ana/status/1','page':'https://prompt-motion.com/giro','posted':'2026-10-01',
            'stack':'HyperFrames','content_tags':['kinetic-type'],
            'media':{'poster':'_originais/motion/giro/capa.png','storyboard':'_originais/motion/giro/quadros.jpg',
                     'loop':'_originais/motion/giro/loop.mp4','video':'_originais/motion/giro/video.mp4'},
            'genres':['vinheta'],'aspect':'vertical','width':1080,'height':1920,'duration':4.2,'fps':30,'audio':True}
    (root/'dados/motion').mkdir(parents=True)
    (root/'dados/motion/teste.jsonl').write_text(json.dumps(record,ensure_ascii=False)+'\n')
    return library.save_workspace(s.Workspace(name='Motion'))['id']


def test_motion_import_links_videos_to_the_map_and_preserves_curation(library):
    wid=motion_library(library)
    assert import_motion(library.db,wid)=={'inserted':1,'updated':0,'preserved':0,'total':1,'missing_assets':0}
    assert import_motion(library.db,wid)['preserved']==1
    graph=library.graph(wid)['items']
    assert [i['id'] for i in graph]==['motion-giro']
    video=graph[0]['motion']
    assert video['loop'].startswith('/api/assets/') and video['video'].startswith('/api/assets/') and video['duration']==4.2
    assert graph[0]['techniques']==['contraste'] and graph[0]['reusable'] is False
    # Formato de tela e tipo de vídeo chegam ao mapa e à busca, pelo nome da plataforma.
    assert video['aspect']=='vertical' and video['genres']==['vinheta']
    assert smart_search(library,s.AgentSearch(query='reels',workspace_ids=[wid]))['items'][0]['id']=='motion-giro'
    # O espaço anterior continua igual, sem vídeos.
    assert all('motion' not in i for i in library.graph('pp-treta')['items'])
    ref=library.get('motion-giro',workspace_ids=[wid])
    assert ref['prompt'].startswith('Make a 4 second') and ref['source']['stack']=='HyperFrames' and ref['format']=='mp4'
    assert {a['role'] for a in ref['assets']}=={'preview','storyboard','motion','original'}
    assert 'Uma vez por vídeo basta.' in ref['usage_notes'] and 'Não incorpore a mídia' in ref['usage_notes']
    # Busca pelo prompt em inglês, pela decupagem e pelo pedido comum.
    for query in ['logo sting','vinheta que gira','zoom em vídeo']:
        found=smart_search(library,s.AgentSearch(query=query,workspace_ids=[wid]))['items']
        assert found and found[0]['id']=='motion-giro',query
    assert smart_search(library,s.AgentSearch(query='',format='mp4',workspace_ids=[wid]))['total']==1
    assert contact_sheet(library,smart_search(library,s.AgentSearch(query='logo',workspace_ids=[wid]))['items'])
    # Curadoria feita no app não é sobrescrita por uma nova importação.
    data=s.ReferenceData(**{k:ref[k] for k in ['title','description','idea','techniques','intentions','movements','aesthetics','strength']},usage_notes=ref['usage_notes'])
    ctx=library.start(s.StartContext(project_id=library.project(s.Project(name='Teste',root=str(library.settings.root)))['id'],demand='Curar motion',workspace_ids=[wid]))
    library.update('motion-giro',s.Update(context_id=ctx['id'],expected_revision=ref['revision'],data=data.model_copy(update={'title':'Vinheta girando'})))
    record=json.loads((library.settings.root/'dados/motion/teste.jsonl').read_text())
    (library.settings.root/'dados/motion/teste.jsonl').write_text(json.dumps({**record,'title':'Outro título'})+'\n')
    assert import_motion(library.db,wid)['preserved']==1
    assert library.get('motion-giro',workspace_ids=[wid])['title']=='Vinheta girando'


def test_videos_play_inline_with_partial_requests_and_agent_sees_frames(library):
    wid=motion_library(library);import_motion(library.db,wid)
    loop=library.graph(wid)['items'][0]['motion']['loop']
    with TestClient(create_app(library.settings,run_worker=False),base_url='http://127.0.0.1:8767') as client:
        whole=client.get(loop)
        assert whole.status_code==200 and whole.headers['content-type']=='video/mp4' and whole.headers['content-disposition'].startswith('inline')
        part=client.get(loop,headers={'Range':'bytes=0-99'})
        assert part.status_code==206 and len(part.content)==100
        assert client.get(loop+'?download=true').headers['content-disposition'].startswith('attachment')
        headers={'Accept':'application/json, text/event-stream','MCP-Protocol-Version':'2025-11-25'}
        call=lambda method,params:client.post('/mcp',headers=headers,json={'jsonrpc':'2.0','id':1,'method':method,'params':params}).json()
        call('initialize',{'protocolVersion':'2025-11-25','capabilities':{},'clientInfo':{'name':'t','version':'1'}})
        result=call('tools/call',{'name':'get_reference','arguments':{'reference_id':'motion-giro','include_image':True,'workspace_ids':[wid]}})['result']
        assert not result.get('isError'),result
        ref=json.loads(result['content'][0]['text'])
        assert ref['prompt'] and ref['how'] and ref['motion']['video']
        image=next(c for c in result['content'] if c['type']=='image')
        import base64,io
        with Image.open(io.BytesIO(base64.b64decode(image['data']))) as im:
            assert im.size[0]/im.size[1]>2  # a prancha de quadros, não a capa
