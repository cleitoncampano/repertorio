import errno
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from repertorio.app import create_app
from repertorio.config import Settings
from repertorio.db import Database
from repertorio.demo import prepare_demo
from repertorio.locking import lock_file
from repertorio.starter import initialize


def test_new_installation_starts_empty_and_existing_curation_is_preserved(library, tmp_path):
    before = library.db.query('SELECT * FROM refs ORDER BY id')
    spaces = library.workspaces()
    assert initialize(library.settings)['preserved_existing_library']
    assert library.db.query('SELECT * FROM refs ORDER BY id') == before
    assert library.workspaces() == spaces
    fresh = Settings(library.settings.root, tmp_path / 'fresh')
    assert initialize(fresh)['initialized']
    db = Database(fresh)
    try:
        assert db.one('SELECT COUNT(*) AS n FROM refs')['n'] == 0
        assert db.one('SELECT name FROM workspaces')['name'] == 'Meu repertório'
        assert 'escala' in db.one("SELECT value FROM meta WHERE key='vocabulary'")['value']
    finally:
        db.engine.dispose()


def test_demo_isolated_with_working_search_and_assets(library, tmp_path):
    before = library.db.query('SELECT * FROM refs ORDER BY id')
    settings = prepare_demo(library.settings, tmp_path / 'demo')
    marker = json.loads((settings.home / 'demo.json').read_text())
    assert prepare_demo(library.settings, settings.home) == settings
    with TestClient(create_app(settings, run_worker=False), base_url=settings.url) as client:
        assert client.get('/api/health').json()['demo'] is True
        spaces = client.get('/api/workspaces').json()
        assert {w['name'] for w in spaces} == {'Estúdio Aurora', 'Marca Horizonte'}
        graph = client.get('/api/graph', params={'workspace_id': 'pp-treta'}).json()
        assert {r['id'] for r in graph['items']} == {'demo-01', 'demo-02', 'demo-03'}
        detail = client.get('/api/references/demo-01', params={'workspace_id': 'pp-treta'}).json()
        assert detail['reusable'] is True and detail['how']
        assert client.get(detail['assets'][0]['url']).status_code == 200
        found = client.post('/api/search', json={'workspace_ids': ['pp-treta'], 'query': 'escala'}).json()
        assert 'demo-01' in {r['id'] for r in found['items']}
    assert library.db.query('SELECT * FROM refs ORDER BY id') == before


def test_demo_refuses_real_library_and_unrelated_existing_directory(library, tmp_path):
    for path in [library.settings.home, library.settings.home.parent, library.settings.home / 'child']:
        with pytest.raises(ValueError, match='separada'):
            prepare_demo(library.settings, path)
    existing = tmp_path / 'unrelated'
    existing.mkdir()
    sentinel = existing / 'keep.txt'
    sentinel.write_text('preservar')
    with pytest.raises(ValueError, match='já existe'):
        prepare_demo(library.settings, existing)
    assert sentinel.read_text() == 'preservar'
    assert not (existing / 'library.sqlite3').exists()


def test_lock_is_exclusive_and_released_when_file_closes(tmp_path):
    path = tmp_path / 'library.lock'
    with path.open('a+b') as first:
        lock_file(first)
        with path.open('a+b') as second:
            with pytest.raises(BlockingIOError):
                lock_file(second)
    with path.open('a+b') as third:
        lock_file(third)


def test_windows_lock_normalizes_busy_error(monkeypatch, tmp_path):
    import repertorio.locking as locking
    def busy(fd, mode, size):
        assert size == 1
        raise OSError(errno.EACCES, 'locked')
    monkeypatch.setattr(locking.sys, 'platform', 'win32')
    monkeypatch.setitem(__import__('sys').modules, 'msvcrt', SimpleNamespace(locking=busy, LK_NBLCK=2))
    with (tmp_path / 'windows.lock').open('a+b') as handle:
        with pytest.raises(BlockingIOError):
            lock_file(handle)
