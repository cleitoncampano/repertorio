import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import pytest
from repertorio.schemas import Search,StateChange,Update,ReferenceData,Register,Pack,Project,StartContext
from repertorio.service import Problem
from repertorio.importer import import_library
from repertorio.jobs import Worker,register
from repertorio.backup import backup,restore
from repertorio.config import Settings
from repertorio.db import Database


def data(**kwargs):
    return ReferenceData(title='Carrossel aprovado',description='Sequência de ideias',idea='Organize o raciocínio por contraste',techniques=['contraste'],intentions=['ABRIR'],**kwargs)


def test_import_is_idempotent_and_keeps_curation(library,context):
    updated=library.update('deck',Update(context_id=context['id'],expected_revision=1,data=data()))
    library.state('deck',StateChange(expected_revision=updated['revision'],state='trashed'),from_ui=True)
    report=import_library(library.db)
    assert report['inserted']==report['updated']==0
    assert library.get('deck')['title']=='Carrossel aprovado'
    assert library.get('deck')['state']=='trashed'
    assert library.search(Search(kind='slide'))['total']==0
    assert library.search(Search(kind='midia'))['total']==2
    assert (library.settings.root/'assets/demo.pptx').read_bytes()==b'original'


def test_strict_filters_and_operations(library):
    assert library.search(Search(reusable=True,query='verde'))['items'][0]['id']=='free'
    assert library.search(Search(reusable=True,query='Marca'))['total']==0
    assert library.search(Search(reusable=True,query='inexistente'))['total']==0
    assert library.search(Search(operation='diferenciacao'))['total']==2
    assert library.search(Search(query='\" OR *'))['total']==0
    assert library.search(Search(kind='slide'))['total']==1


def test_delete_restore_and_revision_conflict(library):
    deleted=library.state('deck',StateChange(expected_revision=1,state='trashed'),from_ui=True)
    with pytest.raises(Problem) as error:library.state('deck',StateChange(expected_revision=1,state='published'),from_ui=True)
    assert error.value.status==409
    library.state('deck',StateChange(expected_revision=deleted['revision'],state='published'),from_ui=True)
    assert library.search(Search(kind='slide'))['total']==1


def test_parallel_contexts_do_not_mix(library,context,tmp_path):
    other=tmp_path/'sales';other.mkdir()
    p=library.project(Project(name='Comercial',root=str(other)))
    c=library.start(StartContext(project_id=p['id'],demand='Apresentação comercial'))
    def work(cid):
        library.search(Search(query='Abertura',context_id=cid))
        return library.pack(Pack(context_id=cid,title='Seleção',reference_ids=['deck']))
    with ThreadPoolExecutor(2) as pool:a,b=list(pool.map(work,[context['id'],c['id']]))
    assert a['context_id']!=b['context_id']
    assert library.db.one('SELECT COUNT(*) AS n FROM packs')['n']==2
    assert {e['context_id'] for e in library.events() if e['action']=='references_searched'}=={context['id'],c['id']}


def test_parallel_updates_have_one_winner(library,context):
    req=Update(context_id=context['id'],expected_revision=1,data=data())
    def update(_):
        try:library.update('deck',req);return 200
        except Problem as e:return e.status
    with ThreadPoolExecutor(2) as pool:statuses=list(pool.map(update,range(2)))
    assert sorted(statuses)==[200,409]


def test_explicit_creation_cycle_and_idempotency(library,context):
    req=Register(context_id=context['id'],request_key='carrossel-v1',data=data(source_reference_ids=['deck']),files=['carrossel.png'],user_requested=True)
    op=register(library,req)
    assert register(library,req)['id']==op['id']
    Worker(library).process(op['id'])
    assert library.operation(op['id'])['state']=='completed'
    ref=library.get(op['ref_id'])
    assert ref['ready']==1 and ref['state']=='published'
    assert len(ref['assets'])==3
    # Managed copy survives removal of the project artifact.
    Path(library.context(context['id'])['root'],'carrossel.png').unlink()
    assert all(Path(r['path']).is_file() for r in library.db.query('SELECT path FROM assets WHERE ref_id=:id',id=ref['id']))
    assert library.search(Search(query='Carrossel',kind='criacao'))['total']==1


def test_spontaneous_creation_stays_pending(library,context):
    op=register(library,Register(context_id=context['id'],request_key='suggestion',data=data(),files=['carrossel.png']))
    Worker(library).process(op['id'])
    assert library.search(Search(kind='criacao'))['total']==0
    assert library.search(Search(kind='criacao',state='pending'))['total']==1
    with pytest.raises(Problem):library.state(op['ref_id'],StateChange(context_id=context['id'],expected_revision=1,state='published'))
    library.state(op['ref_id'],StateChange(context_id=context['id'],expected_revision=1,state='published',user_requested=True))
    assert library.search(Search(kind='criacao'))['total']==1


def test_paths_and_vocabulary_are_validated(library,context,tmp_path):
    with pytest.raises(Problem):register(library,Register(context_id=context['id'],request_key='outside',data=data(),files=['../private.png']))
    req=data();req.techniques=['inventada']
    with pytest.raises(Problem):library.update('deck',Update(context_id=context['id'],expected_revision=1,data=req))
    root=Path(library.context(context['id'])['root'])
    (root/'link.png').symlink_to(library.settings.root/'assets/cover.png')
    with pytest.raises(Problem):register(library,Register(context_id=context['id'],request_key='symlink',data=data(),files=['link.png']))


def test_pack_keeps_snapshot(library,context):
    p=library.pack(Pack(context_id=context['id'],title='Direção',reference_ids=['deck']))
    library.update('deck',Update(context_id=context['id'],expected_revision=1,data=data()))
    stored=json.loads(library.db.one('SELECT payload FROM packs WHERE id=:id',id=p['id'])['payload'])
    assert stored['references'][0]['title']=='Abertura criativa'
    with pytest.raises(Problem):library.pack(Pack(context_id=context['id'],title='Antes',reference_ids=['deck#2']))


def test_backup_restore_managed_assets(library,context,tmp_path):
    op=register(library,Register(context_id=context['id'],request_key='backup-test',data=data(),files=['carrossel.png'],user_requested=True))
    Worker(library).process(op['id'])
    archive=tmp_path/'snapshot.zip';report=backup(library.settings,archive)
    assert report['managed_files']==3
    settings=Settings(library.settings.root,tmp_path/'restored')
    restore(settings,archive)
    restored=Database(settings)
    try:
        assert restored.one('SELECT COUNT(*) AS n FROM refs')['n']==6
        rows=restored.query('SELECT path FROM assets WHERE ref_id=:id',id=op['ref_id'])
        assert all(Path(row['path']).is_file() for row in rows)
        assert all(Path(row['path']).is_relative_to(settings.home) for row in rows)
    finally:restored.engine.dispose()


def test_worker_restart_recovers_running_jobs(library,context):
    from sqlalchemy import text
    op=register(library,Register(context_id=context['id'],request_key='restart-test',data=data(),files=['carrossel.png'],user_requested=True))
    with library.db.engine.begin() as conn:conn.execute(text("UPDATE operations SET state='running' WHERE id=:id"),dict(id=op['id']))
    worker=Worker(library);worker.start()
    import time
    try:
        for _ in range(60):
            if library.operation(op['id'])['state']=='completed':break
            time.sleep(.05)
        assert library.operation(op['id'])['state']=='completed'
    finally:worker.stop()


def test_html_requires_preview_and_is_not_executed(library,context):
    root=Path(library.context(context['id'])['root'])
    (root/'demo.html').write_text('<script>fetch("http://external.test")</script>')
    req=Register(context_id=context['id'],request_key='html-no-preview',data=data(),files=['demo.html'])
    op=register(library,req);Worker(library).process(op['id'])
    assert library.operation(op['id'])['state']=='failed'
    req.request_key='html-preview';req.previews=['carrossel.png']
    op=register(library,req);Worker(library).process(op['id'])
    assert library.operation(op['id'])['state']=='completed'


def test_backup_now_keeps_recent_copies(library,tmp_path):
    from repertorio.backup import backup_now
    target=tmp_path/'copias'
    for _ in range(3):
        result=backup_now(library,target,keep=2)
        import time;time.sleep(1.1)
    assert len(list(target.glob('repertorio-*.zip')))==2
    assert result['managed_files']==0 and 'history' not in result
    assert any(e['action']=='backup_created' for e in library.events())


def test_user_reviews_agent_selection(library,context):
    from repertorio.schemas import Review
    p=library.pack(Pack(context_id=context['id'],title='Abertura',reference_ids=['deck','free'],rationale='Contraste forte'))
    assert p['review_url'].endswith('?escolha='+p['id'])
    demands=library.demands()
    assert demands[0]['demand']=='Criar carrossel' and demands[0]['packs'][0]['total']==2
    library.review(p['id'],Review(reference_id='deck',verdict='approved',note='Usar a tipografia'))
    detail=library.review(p['id'],Review(reference_id='free',verdict='cut'))
    reviews={r['id']:r['review'] for r in detail['references']}
    assert reviews['deck']['verdict']=='approved' and reviews['deck']['note']=='Usar a tipografia'
    assert reviews['free']['verdict']=='cut' and detail['references'][0]['thumbnail']
    assert library.demands()[0]['packs'][0]['approved']==1 and library.demands()[0]['packs'][0]['cut']==1
    assert library.review(p['id'],Review(reference_id='free'))['references'][1]['review'] is None
    with pytest.raises(Problem):library.review(p['id'],Review(reference_id='deck#1',verdict='cut'))
    assert any(e['action']=='pack_reviewed' for e in library.events())
