import fcntl
from pathlib import Path

import pytest

from repertorio.config import Settings
from repertorio.db import Database
from repertorio.importer import asset
from repertorio.relocate import relocate
from repertorio.schemas import Project


def test_relocation_preserves_links_and_asset_ids(library, tmp_path):
    old = library.settings.root
    project = library.project(Project(name='Repertório', root=str(old)))
    before = library.db.query('SELECT id,ref_id,path,role,member FROM assets ORDER BY id')
    memberships = library.db.query('SELECT * FROM workspace_references ORDER BY ref_id')
    target = tmp_path / 'repertorio'
    old.rename(target)
    # A raiz anterior pode continuar acessível aos atalhos de uma sessão antiga.
    old.symlink_to(target, target_is_directory=True)
    settings = Settings(target, library.settings.home)
    result = relocate(settings, old, tmp_path / 'before.sqlite3')
    assert result['identifiers_preserved']
    assert result['previous_root'] == str(old)
    assert library.db.one('SELECT * FROM projects WHERE id=:id', id=project['id'])['root'] == str(target)
    assert library.db.query('SELECT * FROM workspace_references ORDER BY ref_id') == memberships
    assert library.db.query('SELECT id FROM assets ORDER BY id') == [{'id': r['id']} for r in before]
    assert all(Path(r['path']).is_file() for r in library.db.query('SELECT path FROM assets'))
    moved = Database(settings)
    try:
        with moved.engine.begin() as conn:
            row = before[0]
            path = target / Path(row['path']).relative_to(old)
            assert asset(conn, settings, row['ref_id'], path, row['role'], row['member']) == row['id']
        assert moved.one('SELECT COUNT(*) AS n FROM assets')['n'] == len(before)
    finally:
        moved.engine.dispose()


def test_relocation_rolls_back_when_target_files_are_missing(library, tmp_path):
    target = tmp_path / 'empty'
    target.mkdir()
    original = library.db.query('SELECT id,path FROM assets ORDER BY id')
    with pytest.raises(ValueError, match='não encontrados'):
        relocate(Settings(target, library.settings.home), library.settings.root, tmp_path / 'before.sqlite3')
    assert library.db.query('SELECT id,path FROM assets ORDER BY id') == original


def test_relocation_refuses_running_service(library, tmp_path):
    home = library.settings.home
    with (home.parent / (home.name + '.lock')).open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        with pytest.raises(ValueError, match='Encerre o serviço'):
            relocate(library.settings, tmp_path / 'old', tmp_path / 'unused.sqlite3')
    assert not (tmp_path / 'unused.sqlite3').exists()
