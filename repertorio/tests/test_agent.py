import io
from PIL import Image
from repertorio.agent import interpret,smart_search,contact_sheet
from repertorio.schemas import AgentSearch


def test_interpret_reads_common_phrases(library):
    found,understood,terms=interpret('Abertura com números em fundo escuro sobre tecnologia',library.meta('vocabulary'))
    assert found['intentions']==['ABRIR','PROVAR']
    assert found['aesthetics']==['escuro']
    assert understood[0]=={'term':'abertura','meaning':['intenção: ABRIR']}
    assert 'tecnologia' in terms and 'abertura' not in terms and 'numeros' not in terms


def test_smart_search_groups_decks_and_skips_loose_media(library,context):
    result=smart_search(library,AgentSearch(query='abertura',context_id=context['id']))
    assert [(i['n'],i['id']) for i in result['items']]==[(1,'deck')]
    assert 'intenção: ABRIR' in result['items'][0]['matched_by']
    assert [i['id'] for i in smart_search(library,AgentSearch(query='abertura',per_group=2))['items']]==['deck','deck#1']
    assert smart_search(library,AgentSearch(query='verde'))['total']==0
    assert smart_search(library,AgentSearch(query='verde',kind='midia'))['total']==2
    assert smart_search(library,AgentSearch(query='verde',kind='midia',reusable=True))['items'][0]['id']=='free'
    assert any(e['action']=='references_searched' and e['context_id']==context['id'] for e in library.events())


def test_contact_sheet_is_a_numbered_image(library):
    items=smart_search(library,AgentSearch(query='abertura',per_group=2))['items']
    image=Image.open(io.BytesIO(contact_sheet(library,items)))
    assert image.format=='JPEG' and image.width==2*380+3*12
    assert contact_sheet(library,[]) is None
