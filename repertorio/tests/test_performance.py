import json

from sqlalchemy import event, text

from repertorio import schemas as s
from repertorio.importer import import_library


def test_batch_preserves_memberships_and_parent_availability(library):
    other=library.save_workspace(s.Workspace(name='Compartilhado QA'))['id']
    ref=library.get('deck',False,workspace_ids=['pp-treta'])
    library.reference_workspaces('deck',s.ReferenceWorkspaces(source_workspace_id='pp-treta',target_workspace_ids=[other],expected_membership_revision=ref['membership_revision']),from_ui=True)
    library.state('deck',s.StateChange(workspace_id='pp-treta',state='trashed',expected_membership_revision=ref['membership_revision']),from_ui=True)
    for hidden,ready in [(0,1),(1,1),(0,0)]:
        with library.db.engine.begin() as conn:
            conn.execute(text('UPDATE refs SET hidden=:hidden,ready=:ready WHERE id=\'deck\''),dict(hidden=hidden,ready=ready))
        for ids in [['pp-treta'],[other],['pp-treta',other]]:
            rows=[r for r in library.db.query('SELECT * FROM refs ORDER BY id') if library.memberships(r['id'],ids)]
            for state in [None,'published','pending','trashed']:
                expected=[library.scoped_summary(row,ids,state) for row in rows]
                assert library.scoped_summaries(rows,ids,state)==expected
    assert library.scoped_summaries([],['pp-treta'])==[]


def test_query_count_does_not_grow_with_page_or_graph(library):
    statements=[]
    def count(_conn,_cursor,statement,*_):
        statements.append(statement)
    event.listen(library.db.engine,'before_cursor_execute',count)
    try:
        def measure():
            statements.clear();graph=library.graph('pp-treta');graph_queries=len(statements)
            statements.clear();search=library.search(s.Search(workspace_ids=['pp-treta'],limit=48),log=False);search_queries=len(statements)
            return graph,search,graph_queries,search_queries
        before=measure()
        with (library.settings.root/'dados/indice.jsonl').open('a') as file:
            for index in range(30):
                file.write('\n'+json.dumps(dict(doc='arquivo',id=f'performance-{index}',titulo=f'Peça {index}',tecnicas=['contraste'],imagem='assets/cover.png')))
        import_library(library.db)
        after=measure()
        assert len(after[0]['items'])==len(before[0]['items'])+30
        assert len(after[1]['items'])==len(before[1]['items'])+30
        assert before[2]==after[2]<=4
        assert before[3]==after[3]<=5
    finally:
        event.remove(library.db.engine,'before_cursor_execute',count)
