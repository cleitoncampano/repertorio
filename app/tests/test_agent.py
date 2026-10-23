import io
import json
from PIL import Image
from sqlalchemy import text
from repertorio.agent import interpret,smart_search,contact_sheet
from repertorio.config import Settings
from repertorio.db import Database
from repertorio.schemas import AgentSearch


def test_interpret_reads_common_phrases(library):
    found,understood,terms,parts,weak=interpret('Abertura com números em fundo escuro sobre tecnologia',library.meta('vocabulary'))
    assert found['intentions']==['ABRIR','PROVAR']
    assert found['aesthetics']==['escuro']
    assert understood[0]=={'term':'abertura','meaning':['intenção: ABRIR']}
    # palavra solta e comum vale pouco como item do vocabulário e continua sendo buscada no texto
    assert weak=={('intentions','ABRIR'),('intentions','PROVAR')}
    assert terms==['abertura','numero','fundo','escuro','tecnologia']
    assert parts[0]==((('intentions','ABRIR'),),('abertura',)) and parts[-1]==((),('tecnologia',))
    found,_,terms,parts,weak=interpret('números grandes de abertura',library.meta('vocabulary'))
    assert found['intentions']==['PROVAR','ABRIR'] and weak=={('intentions','ABRIR')} and terms==['abertura']
    assert parts[0]==((('intentions','PROVAR'),),())


def test_descriptive_request_prefers_items_with_all_its_words(library):
    with library.db.engine.begin() as conn:
        conn.execute(text("""INSERT INTO refs(id,kind,title,origin,state,payload,search_text,created,updated)
            VALUES('timer','arquivo','Cronômetro grande','acervo','published',:p,'Cronômetro contando os segundos na tela','t','t')"""),dict(p=json.dumps({'strength':3})))
        conn.execute(text("INSERT INTO workspace_references(workspace_id,ref_id,state,created,updated) VALUES('referencias','timer','published','t','t')"))
    # "capa" marca ABRIR, mas o deck de força 5 com ABRIR não passa à frente de quem tem todas as palavras do pedido
    result=smart_search(library,AgentSearch(query='capa com cronômetro contando os segundos',workspace_ids=['referencias']))
    assert [i['id'] for i in result['items']]==['timer','deck']
    assert result['items'][0]['matched_by']==['texto: cronometro contando segundo']


def test_search_text_migration_adds_how_and_good_for(tmp_path):
    from alembic import command
    from alembic.config import Config
    from pathlib import Path
    db=Database(Settings(tmp_path,tmp_path/'runtime'))
    config=Config(str(Path(__file__).resolve().parents[1]/'server/alembic.ini'))
    with db.engine.connect() as conn:
        config.attributes['connection']=conn;command.upgrade(config,'0004')
    payload={'title':'Ficha','idea':'Ideia','how':'O olhar guia a leitura','good_for':['capa de evento']}
    with db.engine.begin() as conn:
        conn.execute(text("INSERT INTO refs(id,kind,title,origin,payload,search_text,created,updated) VALUES('padrao','slide','Ficha','acervo',:p,'Ficha  Ideia        ','t','t')"),dict(p=json.dumps(payload)))
        conn.execute(text("INSERT INTO refs(id,kind,title,origin,payload,search_text,created,updated) VALUES('propria','slide','Ficha','acervo',:p,'texto próprio','t','t')"),dict(p=json.dumps(payload)))
    db.migrate()
    rows={r['id']:r['search_text'] for r in db.query('SELECT id,search_text FROM refs')}
    assert 'O olhar guia a leitura capa de evento' in rows['padrao'] and rows['propria']=='texto próprio'
    assert db.one("SELECT id FROM ref_search WHERE ref_search MATCH 'olhar'")['id']=='padrao'
    db.engine.dispose()


def test_smart_search_groups_decks_and_skips_loose_media(library,context):
    result=smart_search(library,AgentSearch(query='abertura',context_id=context['id'],workspace_ids=['referencias']))
    assert [(i['n'],i['id']) for i in result['items']]==[(1,'deck')]
    assert 'intenção: ABRIR' in result['items'][0]['matched_by']
    assert [i['id'] for i in smart_search(library,AgentSearch(query='abertura',per_group=2,workspace_ids=['referencias']))['items']]==['deck','deck#1']
    assert smart_search(library,AgentSearch(query='verde',workspace_ids=['referencias']))['total']==0
    assert smart_search(library,AgentSearch(query='verde',kind='midia',workspace_ids=['referencias']))['total']==2
    assert smart_search(library,AgentSearch(query='verde',kind='midia',reusable=True,workspace_ids=['referencias']))['items'][0]['id']=='free'
    assert any(e['action']=='references_searched' and e['context_id']==context['id'] for e in library.events())


def test_contact_sheet_is_a_numbered_image(library):
    items=smart_search(library,AgentSearch(query='abertura',per_group=2,workspace_ids=['referencias']))['items']
    image=Image.open(io.BytesIO(contact_sheet(library,items)))
    assert image.format=='JPEG' and image.width==2*380+3*12
    assert contact_sheet(library,[]) is None
