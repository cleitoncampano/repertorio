import json
from PIL import Image
from repertorio import schemas as s
from repertorio.agent import smart_search
from repertorio.decks import import_decks


def deck_library(library):
    root=library.settings.root
    pages=root/'_originais/perestroika/paginas/forma';pages.mkdir(parents=True)
    for n,color in ((1,'#3fd6d4'),(7,'#3c1236')):Image.new('RGB',(1024,768),color).save(pages/f'p{n:03d}.jpg')
    (root/'perestroika').mkdir();(root/'perestroika/forma.pdf').write_bytes(b'%PDF-1.4')
    base={'collection':'perestroika','file':'perestroika/forma.pdf','techniques':['contraste'],'intentions':['ABRIR'],'aesthetics':['escuro'],'strength':4}
    rows=[{**base,'doc':'arquivo','id':'perestroika-forma','title':'Metodologia de Forma','description':'Volume do método.',
           'idea':'Numere os capítulos.','preview':'_originais/perestroika/paginas/forma/p001.jpg','original':'perestroika/forma.pdf','concepts':['treco','tagline']},
          {**base,'doc':'slide','id':'perestroika-forma#7','deck':'perestroika-forma','n':7,'page':7,'title':'O treco',
           'description':'Divisor roxo.','idea':'Ponha o número gigante ao lado do título.','text':'#10 O TRECO',
           'preview':'_originais/perestroika/paginas/forma/p007.jpg','concepts':['treco']}]
    (root/'dados/perestroika').mkdir(parents=True)
    # O slide vem antes da apresentação no arquivo: a importação ordena.
    (root/'dados/perestroika/decks.jsonl').write_text('\n'.join(json.dumps(r,ensure_ascii=False) for r in reversed(rows))+'\n')
    return library.save_workspace(s.Workspace(name='Perestroika'))['id']


def test_pdf_decks_enter_the_map_with_their_pages(library):
    wid=deck_library(library)
    folder=library.settings.root/'dados/perestroika'
    assert import_decks(library.db,wid,folder)=={'inserted':2,'updated':0,'preserved':0,'total':2,'missing_assets':0}
    assert import_decks(library.db,wid,folder)['preserved']==2
    # O mapa mostra a apresentação; a página entra como slide dela, como nos slides de Referências.
    graph=library.graph(wid)['items']
    assert [i['id'] for i in graph]==['perestroika-forma'] and graph[0]['reusable'] is False and graph[0]['aspect']
    deck=library.get('perestroika-forma',workspace_ids=[wid])
    assert [c['id'] for c in deck['children']]==['perestroika-forma#7']
    assert {a['role'] for a in deck['assets']}=={'preview','original'} and 'Não copie a página' in deck['usage_notes']
    slide=library.get('perestroika-forma#7',workspace_ids=[wid])
    assert slide['parent_id']=='perestroika-forma' and slide['number']==7 and slide['concepts']==['treco'] and slide['source']['page']==7
    # O agente acha a página pelo nome do conceito do método.
    found=smart_search(library,s.AgentSearch(query='treco',workspace_ids=[wid]))['items']
    assert found and found[0]['id'].startswith('perestroika-forma')
    # Os outros espaços continuam iguais.
    for other in [w['id'] for w in library.workspaces() if w['id']!=wid]:
        assert 'perestroika-forma' not in {i['id'] for i in library.graph(other)['items']}


def test_method_cards_open_from_the_index_without_crowding_the_guide_list(library,context):
    root=library.settings.root;wid=library.save_workspace(s.Workspace(name='Perestroika'))['id']
    method=root/'biblioteca/metodos/perestroika'
    for folder,name,body in (('guias','metodo-perestroika','# Índice\n\nAbra perestroika/tese.'),('guias','aula-e-workshop','# Aula'),
                             ('conceitos','tese','# Tese\n\nO ponto a provar.'),('modelos','ficha-de-tese','# Ficha de tese')):
        (method/folder).mkdir(parents=True,exist_ok=True);(method/folder/f'{name}.md').write_text(body)
    (method/'LEIA-ME.md').write_text('# Leia')
    assert library.guides()==['aula-e-workshop','metodo-perestroika']
    assert 'O ponto a provar' in library.guide('perestroika/tese') and library.guide('perestroika/ficha-de-tese')=='# Ficha de tese'
    for name in ('tese','perestroika/../guias/aula-e-workshop','LEIA-ME'):
        try:library.guide(name);raise AssertionError(name)
        except Exception as error:assert 'metodo-' in str(error)
    assert library.start(s.StartContext(project_id=context['project_id'],demand='Workshop',workspace_ids=[wid]))['guides_available']==['aula-e-workshop','metodo-perestroika']


def test_methods_from_two_collections_coexist_without_replacing_each_other(library):
    root=library.settings.root
    for coll,guides,cards in (('perestroika',('metodo-perestroika','revisao-apresentacao'),('tese',)),('soap',('metodo-soap','pitch-e-proposta'),('tres-atos','tese'))):
        for folder,names in (('guias',guides),('conceitos',cards)):
            (root/f'biblioteca/metodos/{coll}/{folder}').mkdir(parents=True,exist_ok=True)
            for name in names:(root/f'biblioteca/metodos/{coll}/{folder}/{name}.md').write_text(f'# {coll} {name}')
    assert library.guides()==['metodo-perestroika','revisao-apresentacao','metodo-soap','pitch-e-proposta']
    # A mesma ficha em duas coleções abre cada uma pelo prefixo.
    assert library.guide('soap/tese')=='# soap tese' and library.guide('perestroika/tese')=='# perestroika tese'
    assert library.guide('soap/tres-atos')=='# soap tres-atos' and library.guide('metodo-soap')=='# soap metodo-soap'
