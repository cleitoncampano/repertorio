from pathlib import Path

import pytest
from PIL import Image
from fastapi.testclient import TestClient

from repertorio.app import create_app
from repertorio.agent import picture, smart_search
from repertorio.covers import clear_cover, set_cover
from repertorio.importer import import_library
from repertorio.schemas import Search, AgentSearch
from repertorio.thumbs import bundle, graph_assets


def test_cover_replaces_cards_without_changing_originals(library, tmp_path):
    original = library.db.query("SELECT * FROM assets WHERE role!='cover' ORDER BY id")
    original_refs = library.db.query('SELECT * FROM refs ORDER BY id')
    image = tmp_path/'new.jpg'
    Image.new('RGB', (1600,900), 'orange').save(image)
    aid = set_cover(library, 'deck', image)
    path = next(path for asset_id,path in graph_assets(library,'referencias') if asset_id==aid)
    assert path.read_bytes() == image.read_bytes()
    assert library.search(Search(kind='arquivo',workspace_ids=['referencias']))['items'][0]['thumbnail'] == '/api/assets/'+aid
    assert library.graph('referencias')['items'][0]['thumbnail'] == '/api/assets/'+aid
    result = smart_search(library,AgentSearch(query='abertura',workspace_ids=['referencias']),log=False)
    assert next(r for r in result['items'] if r['id']=='deck')['thumbnail'] == '/api/assets/'+aid
    assert picture(library, library.get('deck',workspace_ids=['referencias'])) == path
    assert set_cover(library,'deck',image) == aid
    # A importação normal não apaga a escolha, nem altera slides e originais.
    import_library(library.db)
    assert library.db.query("SELECT * FROM assets WHERE role!='cover' ORDER BY id") == original
    assert library.db.query('SELECT * FROM refs ORDER BY id') == original_refs
    image.unlink()
    app = create_app(library.settings,run_worker=False)
    with TestClient(app) as client:
        response=client.get('/api/assets/'+aid)
        assert response.status_code==200 and response.headers['content-type']=='image/jpeg'
        assert 'inline' in response.headers['content-disposition']
        small=client.get('/api/assets/'+aid+'?w=128')
        assert small.status_code==200 and small.headers['content-type']=='image/webp'
        assert '/api/assets/'+aid in bundle(app.state.library,128,'referencias')
    assert clear_cover(library,'deck')
    assert not clear_cover(library,'deck')
    assert library.search(Search(kind='arquivo',workspace_ids=['referencias']))['items'][0]['thumbnail'] != '/api/assets/'+aid
    assert library.db.query("SELECT * FROM assets WHERE role!='cover' ORDER BY id") == original


def test_cover_validation_and_new_cache_address(library,tmp_path):
    first=tmp_path/'first.png';second=tmp_path/'second.png'
    Image.new('RGB',(400,225),'red').save(first)
    Image.new('RGB',(400,225),'blue').save(second)
    with pytest.raises(ValueError):set_cover(library,'deck#1',first)
    a=set_cover(library,'deck',first);b=set_cover(library,'deck',second)
    assert a!=b
    assert library.db.one("SELECT COUNT(*) AS n FROM assets WHERE role='cover'")['n']==1
    second.write_text('broken image')
    with pytest.raises(OSError):set_cover(library,'deck',second)
    assert library.db.one("SELECT id FROM assets WHERE role='cover'")['id']==b
