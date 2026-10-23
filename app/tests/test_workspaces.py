import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from repertorio import schemas as s
from repertorio.agent import smart_search, sheet_items
from repertorio.app import create_app
from repertorio.backup import backup, restore
from repertorio.config import Settings
from repertorio.db import Database
from repertorio.importer import import_library
from repertorio.jobs import register, Worker
from repertorio.service import Library, Problem
from repertorio.thumbs import bundle


PP='referencias'


def space(lib,name='GrowMate'):
    return lib.save_workspace(s.Workspace(name=name))['id']


def link(lib,target,ref='deck',source=PP,move=False):
    current=lib.get(ref,False,workspace_ids=[source])
    return lib.reference_workspaces(ref,s.ReferenceWorkspaces(source_workspace_id=source,target_workspace_ids=[target],
        expected_membership_revision=current['membership_revision'],move=move),from_ui=True)


def state(lib,wid,rid='deck',value='trashed'):
    current=lib.get(rid,False,workspace_ids=[wid])
    return lib.state(rid,s.StateChange(workspace_id=wid,state=value,expected_membership_revision=current['membership_revision']),from_ui=True)


def test_empty_spaces_and_explicit_scope(library,context):
    grow=space(library)
    assert library.graph(grow)['items']==[]
    assert library.stats(grow)['counts']=={}
    assert library.search(s.Search(workspace_ids=[grow]))['total']==0
    assert library.operations(grow)==[]
    assert bundle(library,128,grow)=={}
    for action in [lambda:library.search(s.Search()),lambda:smart_search(library,s.AgentSearch()),lambda:library.get('deck')]:
        with pytest.raises(Problem) as error:action()
        assert error.value.status==422
    assert library.context(context['id'])['workspace_ids']==[PP]
    with pytest.raises(Problem):library.scope([grow],context['id'])


def test_shared_file_and_editorial_update_local_trash(library,context):
    grow=space(library)
    before=library.db.query('SELECT * FROM assets ORDER BY id')
    link(library,grow)
    link(library,grow)
    assert library.db.query('SELECT * FROM assets ORDER BY id')==before
    assert library.db.one('SELECT COUNT(*) AS n FROM workspace_references WHERE workspace_id=:id',id=grow)['n']==3
    ref=library.get('deck',workspace_ids=[grow])
    library.update('deck',s.Update(context_id=context['id'],expected_revision=ref['revision'],data=s.ReferenceData(
        title='Novo título',description='Descrição comum',idea='Ideia comum',techniques=['contraste'])))
    assert library.get('deck',workspace_ids=[grow])['title']=='Novo título'
    state(library,PP)
    assert library.search(s.Search(workspace_ids=[PP],kind='slide'))['total']==0
    assert library.search(s.Search(workspace_ids=[grow],kind='slide'))['total']==1
    assert library.get('deck',workspace_ids=[grow])['state']=='published'
    assert library.get('deck',workspace_ids=[PP])['children']==[]
    assert library.db.query('SELECT * FROM assets ORDER BY id')==before


def test_combined_search_deduplicates_and_respects_scope(library,context):
    grow,other=space(library),space(library,'cVortex')
    link(library,grow)
    combined=library.start(s.StartContext(project_id=context['project_id'],demand='Combinar repertórios',workspace_ids=[PP,grow]))
    query=s.AgentSearch(context_id=combined['id'],query='abertura',per_group=2)
    assert [r['id'] for r in smart_search(library,query)['items']]==['deck','deck#1']
    assert set(library.get('deck',context_id=combined['id'])['workspace_ids'])=={PP,grow}
    state(library,PP)
    assert library.get('deck',context_id=combined['id'])['workspace_ids']==[grow]
    result=smart_search(library,query)['items']
    assert all(r['workspace_ids']==[grow] for r in result)
    state(library,grow)
    exclusive=library.start(s.StartContext(project_id=context['project_id'],demand='Somente cVortex',workspace_ids=[other]))
    with pytest.raises(Problem):library.get('deck',context_id=exclusive['id'])
    with pytest.raises(Problem):sheet_items(library,['deck'],workspace_ids=[other])


def test_move_keeps_other_spaces_and_reimport_does_not_resurrect(library):
    a,b=space(library),space(library,'cVortex')
    link(library,a)
    link(library,b,move=True)
    with pytest.raises(Problem):library.get('deck',workspace_ids=[PP])
    assert library.get('deck',workspace_ids=[a])['children']
    assert library.get('deck',workspace_ids=[b])['children']
    import_library(library.db)
    with pytest.raises(Problem):library.get('deck',workspace_ids=[PP])
    link(library,PP,source=a)
    assert library.get('deck',workspace_ids=[PP])['children']


def test_join_brings_published_once_and_respects_local_trash(library):
    a,b,joined=space(library),space(library,'cVortex'),space(library,'Apresentações')
    link(library,a)
    state(library,PP,'free')
    first=library.join_workspaces(joined,[PP,a,joined])
    assert first['sources']==[PP,a] and first['added']==4
    assert library.get('deck',workspace_ids=[joined])['children']
    assert {i['id'] for i in library.graph(joined)['items']}=={i['id'] for i in library.graph(PP)['items']}
    with pytest.raises(Problem):library.get('free',workspace_ids=[joined])
    state(library,joined,'thirdparty')
    link(library,b,ref='free',source=PP)
    state(library,b,'free','published')
    again=library.join_workspaces(joined,[PP,b])
    assert again['added']==1 and library.get('free',workspace_ids=[joined])['state']=='published'
    assert library.get('thirdparty',False,workspace_ids=[joined])['state']=='trashed'
    assert library.join_workspaces(joined,[PP,a,b])['added']==0
    with pytest.raises(Problem):library.join_workspaces(joined,[joined])


def test_new_slide_inherits_shared_and_detached_parent(library):
    a=space(library)
    link(library,a,move=True)
    with (library.settings.root/'dados/indice.jsonl').open('a') as f:
        f.write('\n'+json.dumps(dict(doc='slide',id='deck#3',deck='deck',n=3,titulo='Novo slide')))
    import_library(library.db)
    assert library.get('deck#3',workspace_ids=[a])['parent_id']=='deck'
    with pytest.raises(Problem):library.get('deck#3',workspace_ids=[PP])


def test_legacy_registration_can_resume(library,context):
    import hashlib
    from repertorio.db import dumps
    req=s.Register(context_id=context['id'],target_workspace_ids=[PP],request_key='legacy-resume',files=['carrossel.png'],
        user_requested=True,data=s.ReferenceData(title='Envio anterior',description='Mesmo envio',idea='Retomar'))
    op=register(library,req)
    job=json.loads(library.db.one('SELECT payload FROM operations WHERE id=:id',id=op['id'])['payload'])
    job['fingerprint']=hashlib.sha256(dumps(dict(data=req.data.model_dump(),hashes=job['hashes'],user_requested=True)).encode()).hexdigest()
    with library.db.engine.begin() as conn:conn.execute(text('UPDATE operations SET payload=:p WHERE id=:id'),dict(p=dumps(job),id=op['id']))
    assert register(library,req)['id']==op['id']
    other=space(library)
    with pytest.raises(Problem):register(library,req.model_copy(update={'target_workspace_ids':[other]}))


def test_independent_states_and_concurrent_revisions(library):
    a=space(library)
    link(library,a)
    def trash(wid):return state(library,wid)['membership_revision']
    with ThreadPoolExecutor(2) as pool:
        assert list(pool.map(trash,[PP,a]))==[2,2]
    req=s.StateChange(workspace_id=a,state='published',expected_membership_revision=2)
    def publish(_):
        try:library.state('deck',req,from_ui=True);return 200
        except Problem as error:return error.status
    with ThreadPoolExecutor(2) as pool:assert sorted(pool.map(publish,[1,2]))==[200,409]


def test_workspace_lifecycle_names_and_conflicts(library,context):
    a=space(library)
    with pytest.raises(Problem):space(library,'  growmate  ')
    with pytest.raises(Problem):space(library,'   ')
    link(library,a)
    source=library.start(s.StartContext(project_id=context['project_id'],workspace_ids=[a],demand='Histórico preservado'))
    assets=library.db.query('SELECT * FROM assets ORDER BY id')
    renamed=library.save_workspace(s.WorkspaceUpdate(name='GrowMate novo',expected_revision=1),a)
    assert renamed['id']==a and renamed['revision']==2
    with pytest.raises(Problem):library.workspace_state(a,s.WorkspaceState(deleted=True,expected_revision=1))
    library.workspace_state(a,s.WorkspaceState(deleted=True,expected_revision=2))
    assert a not in {w['id'] for w in library.workspaces()}
    # Os vínculos ficam guardados para restaurar; o espaço some da lista, da busca e do mapa.
    assert library.db.one('SELECT COUNT(*) AS n FROM workspace_references WHERE workspace_id=:id',id=a)['n']>0
    assert [w['id'] for w in library.deleted_workspaces()]==[a]
    assert library.db.query('SELECT * FROM assets ORDER BY id')==assets
    assert library.get('deck',workspace_ids=[PP])['state']=='published'
    with pytest.raises(Problem):library.graph(a)
    assert library.context(source['id'])['workspace_ids']==[a]
    replacement=space(library,'GrowMate novo')
    assert replacement!=a and library.graph(replacement)['items']==[]
    with TestClient(create_app(library.settings,run_worker=False)) as client:
        assert client.get('/api/workspaces?deleted=true').json()==library.workspaces()
        assert client.get('/api/workspaces/deleted').json()[0]['id']==a
        # Outro espaço ativo com o mesmo nome impede restaurar até ser renomeado.
        assert client.post('/api/workspaces/'+a+'/state',json={'deleted':False,'expected_revision':3}).status_code==409
        library.save_workspace(s.WorkspaceUpdate(name='Outro nome',expected_revision=1),replacement)
        assert client.post('/api/workspaces/'+a+'/state',json={'deleted':False,'expected_revision':2}).status_code==409
        restored=client.post('/api/workspaces/'+a+'/state',json={'deleted':False,'expected_revision':3})
        assert restored.status_code==200 and restored.json()['revision']==4
    assert a in {w['id'] for w in library.workspaces()} and library.deleted_workspaces()==[]
    assert library.graph(a)['items'] and library.context(source['id'])['workspace_ids']==[a]
    assert library.events(workspace_id=a)[0]['action']=='workspace_restored'


def test_explicit_destinations_one_processing_deleted_destination(library,context):
    a,b=space(library),space(library,'cVortex')
    req=s.Register(context_id=context['id'],target_workspace_ids=[a,b],request_key='spaces-job',files=['carrossel.png'],
        user_requested=True,data=s.ReferenceData(title='Material compartilhado',description='Dois destinos',idea='Uma única ficha'))
    op=register(library,req)
    assert register(library,req)['id']==op['id']
    with pytest.raises(Problem):register(library,req.model_copy(update={'target_workspace_ids':[PP]}))
    library.workspace_state(a,s.WorkspaceState(deleted=True,expected_revision=1))
    Worker(library).process(op['id'])
    assert library.operation(op['id'])['state']=='completed'
    assert library.workspace(a,active=False)['deleted']
    assert library.get(op['ref_id'],workspace_ids=[b])['ready']==1
    assert library.search(s.Search(workspace_ids=[PP],kind='criacao'))['total']==0
    assert len(library.db.query('SELECT * FROM assets WHERE ref_id=:id',id=op['ref_id']))==3
    assert library.operations(PP)==[]
    assert len(library.operations(b))==1
    assert all(e['ref_id']!=op['ref_id'] for e in library.events(workspace_id=PP))


def test_scope_for_detail_related_sheet_and_api(library):
    a=space(library)
    link(library,a)
    with TestClient(create_app(library.settings,run_worker=False)) as client:
        assert client.get('/api/graph').status_code==422
        assert client.post('/api/search',json={}).status_code==422
        assert client.post('/api/contexts',json={'project_id':'x','demand':'Teste'}).status_code==422
        assert client.get('/api/references/free',params={'workspace_id':a}).status_code==404
        detail=client.get('/api/references/deck',params={'workspace_id':a}).json()
        assert {r['id'] for r in detail['related']}==set()
        assert detail['url'].startswith(library.settings.url+'/?workspace='+a)
        assert client.post('/api/sheet',json={'workspace_ids':[a],'ids':['free']}).status_code==404
        assert client.get('/api/previews',params={'workspace_id':a}).status_code==200


def test_backup_preserves_shared_memberships(library,tmp_path):
    a=space(library)
    link(library,a)
    state(library,PP)
    archive=tmp_path/'spaces.zip'
    backup(library.settings,archive)
    settings=Settings(library.settings.root,tmp_path/'restored')
    restore(settings,archive)
    db=Database(settings);db.migrate();restored=Library(db)
    try:
        assert restored.get('deck',workspace_ids=[PP])['state']=='trashed'
        assert restored.get('deck',workspace_ids=[a])['state']=='published'
    finally:db.engine.dispose()


def test_migrate_legacy_ids_and_history(tmp_path):
    from alembic import command
    from alembic.config import Config
    from pathlib import Path
    settings=Settings(tmp_path,tmp_path/'legacy')
    db=Database(settings)
    config=Config(str(Path(__file__).resolve().parents[1]/'server/alembic.ini'))
    with db.engine.connect() as conn:
        config.attributes['connection']=conn;command.upgrade(config,'0003')
    with db.engine.begin() as conn:
        for sql in [
            "INSERT INTO refs(id,kind,title,origin,state,payload,search_text,created,updated) VALUES('original','arquivo','Original','acervo','trashed','{}','','t','t')",
            "INSERT INTO projects VALUES('project','Projeto','/tmp','t')",
            "INSERT INTO contexts VALUES('context','project','Demanda antiga','t')",
            "INSERT INTO packs VALUES('pack','context','Seleção','{\"references\":[]}','t')",
            "INSERT INTO pack_reviews VALUES('pack','original','approved','Manter','t')",
            "INSERT INTO operations(id,context_id,ref_id,request_key,state,payload,created,updated) VALUES('job','context','original','legacy','completed','{}','t','t')",
        ]:conn.execute(text(sql))
    db.migrate();lib=Library(db)
    try:
        assert lib.get('original',workspace_ids=[PP])['state']=='trashed'
        assert lib.context('context')['workspace_ids']==[PP]
        assert lib.operation('job')['target_workspace_ids']==[PP]
        assert lib.db.one('SELECT note FROM pack_reviews')['note']=='Manter'
        assert lib.db.one('SELECT COUNT(*) AS n FROM refs')['n']==1
        db.migrate()
        assert len(lib.workspaces())==1
    finally:db.engine.dispose()


def test_purge_trash_for_good_keeps_other_spaces_and_originals(library):
    a=space(library)
    link(library,a)
    state(library,PP);state(library,PP,'free')
    with pytest.raises(Problem) as error:library.purge_trash(PP,s.TrashPurge(ids=['thirdparty']))
    assert error.value.status==409
    with pytest.raises(Problem) as error:library.purge_trash(PP,s.TrashPurge())
    assert error.value.status==422
    assert library.purge_trash(PP,s.TrashPurge(ids=['deck']))['purged']==1
    with pytest.raises(Problem):library.get('deck',workspace_ids=[PP])
    assert library.get('deck',workspace_ids=[a])['children']
    assert [r['id'] for r in library.search(s.Search(workspace_ids=[PP],state='trashed'))['items']]==['free']
    import_library(library.db)
    with pytest.raises(Problem):library.get('deck',workspace_ids=[PP])
    # Sem outro espaço, a ficha some; o original fora da pasta do app continua no disco.
    original=library.db.one("SELECT path FROM assets WHERE ref_id='free'")['path']
    assert library.purge_trash(PP,s.TrashPurge(all=True))['purged']==1
    assert library.db.one("SELECT payload,search_text FROM refs WHERE id='free'")['search_text']==''
    assert not library.db.query("SELECT 1 FROM assets WHERE ref_id='free'")
    assert Path(original).exists()
    assert any(e['action']=='reference_purged' for e in library.events(workspace_id=PP))


def test_purge_all_respects_kept_items_and_removes_app_copies(library,context):
    req=s.Register(context_id=context['id'],target_workspace_ids=[PP],request_key='purge-job',files=['carrossel.png'],
        user_requested=True,data=s.ReferenceData(title='Criação para excluir',description='Teste',idea='Some de vez'))
    op=register(library,req);Worker(library).process(op['id'])
    copies=[Path(r['path']) for r in library.db.query('SELECT path FROM assets WHERE ref_id=:id',id=op['ref_id'])]
    assert copies and all(p.exists() for p in copies)
    state(library,PP,op['ref_id']);state(library,PP,'free')
    with TestClient(create_app(library.settings,run_worker=False)) as client:
        # A pessoa marcou tudo vendo 2 itens; se a lixeira mudou (aqui ficou 1 a excluir), nada sai.
        assert client.post(f'/api/workspaces/{PP}/trash/purge',json={'all':True,'keep':['free'],'expected':2}).status_code==409
        assert all(p.exists() for p in copies)
        out=client.post(f'/api/workspaces/{PP}/trash/purge',json={'all':True,'keep':['free'],'expected':1}).json()
    assert out['purged']==1 and out['files_removed']>=1
    assert not any(p.exists() for p in copies)
    assert library.get('free',workspace_ids=[PP])['state']=='trashed'
    assert library.search(s.Search(workspace_ids=[PP],kind='criacao'))['total']==0
