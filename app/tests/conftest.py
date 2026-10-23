import json
import pytest
from PIL import Image
from repertorio.config import Settings
from repertorio.db import Database
from repertorio.importer import import_library
from repertorio.service import Library
from repertorio.schemas import Project,StartContext


@pytest.fixture
def library(tmp_path):
    root=tmp_path/'acervo';root.mkdir();(root/'dados').mkdir();(root/'assets').mkdir()
    Image.new('RGB',(120,80),'#567345').save(root/'assets/cover.png')
    (root/'assets/demo.pptx').write_bytes(b'original')
    vocab={'tecnicas':{'itens':[{'id':'contraste','operacao':'diferenciacao','def':'Contraste'}]},'operacoes':{'itens':[{'id':'diferenciacao','nome':'Diferenciação','def':'Diferenciar'}]},'intencoes':{'itens':[{'id':'ABRIR','def':'Abrir'},{'id':'PROVAR','def':'Provar'}]},'movimentos':{'itens':[{'id':'zoom','def':'Zoom'}]},'esteticas':{'itens':['escuro']}}
    (root/'dados/vocabulario.json').write_text(json.dumps(vocab))
    rows=[
      {'doc':'arquivo','id':'deck','titulo':'Abertura criativa','resumo':'Impacto visual','ideia':'Amplie o contraste','tecnicas':['contraste'],'intencoes':['ABRIR'],'forca':5,'imagem':'assets/cover.png','arquivo':'assets/demo.pptx','antes':[2]},
      {'doc':'slide','id':'deck#1','deck':'deck','n':1,'titulo':'Abertura','nota':'Texto grande','tecnicas':['contraste'],'intencoes':['ABRIR'],'imagem':'assets/cover.png'},
      {'doc':'slide','id':'deck#2','deck':'deck','n':2,'titulo':'Antes','antes':True,'imagem':'assets/cover.png'},
      {'doc':'midia','id':'free','o_que':'Textura verde','terceiros':False,'imagem':'assets/cover.png'},
      {'doc':'midia','id':'thirdparty','o_que':'Marca verde','terceiros':True,'imagem':'assets/cover.png'},
    ]
    (root/'dados/indice.jsonl').write_text('\n'.join(json.dumps(d) for d in rows))
    settings=Settings(root,tmp_path/'runtime',8767)
    db=Database(settings);db.migrate();import_library(db)
    lib=Library(db)
    yield lib
    db.engine.dispose()


@pytest.fixture
def context(library,tmp_path):
    project=tmp_path/'marketing';project.mkdir()
    Image.new('RGB',(300,200),'#e5ab8c').save(project/'carrossel.png')
    p=library.project(Project(name='Marketing',root=str(project)))
    return library.start(StartContext(project_id=p['id'],demand='Criar carrossel',workspace_ids=['referencias']))
