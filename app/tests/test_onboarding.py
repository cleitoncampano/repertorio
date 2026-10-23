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
        graph = client.get('/api/graph', params={'workspace_id': 'referencias'}).json()
        assert {r['id'] for r in graph['items']} == {'demo-01', 'demo-02', 'demo-03'}
        detail = client.get('/api/references/demo-01', params={'workspace_id': 'referencias'}).json()
        assert detail['reusable'] is True and detail['how']
        assert client.get(detail['assets'][0]['url']).status_code == 200
        found = client.post('/api/search', json={'workspace_ids': ['referencias'], 'query': 'escala'}).json()
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


def test_agent_instructions_cite_only_installed_guides(library):
    from repertorio.cli import agent_instructions
    from repertorio.mcp_server import create_mcp
    settings=library.settings
    fresh=agent_instructions(settings,settings.url,'projeto-1','run.sh')
    assert 'get_guide' not in fresh and 'Perestroika' not in fresh and '\n5. Mantenha o `context_id`' in fresh
    assert library.guide_summary()==''
    mcp=create_mcp(library,None)
    tools={t.name:t for t in mcp._tool_manager.list_tools()}
    assert 'ainda não tem guias' in tools['get_guide'].description and 'get_guide' not in mcp.instructions
    folder=settings.root/'biblioteca/guias';folder.mkdir(parents=True)
    (folder/'abertura.md').write_text('# Abertura')
    method=settings.root/'biblioteca/metodos/escola/guias';method.mkdir(parents=True)
    (method/'metodo-escola.md').write_text('# Método')
    full=agent_instructions(settings,settings.url,'projeto-1','run.sh')
    assert '2. Leia com `get_guide`' in full and '`metodo-escola`' in full and 'para vídeos' not in full
    assert 'abertura' in library.guide_summary() and 'Método escola: metodo-escola é o índice' in library.guide_summary()
    tools={t.name:t for t in create_mcp(library,None)._tool_manager.list_tools()}
    assert 'abertura' in tools['get_guide'].description


def test_library_lives_outside_the_program_folder(tmp_path, monkeypatch):
    from repertorio import config
    monkeypatch.setattr(config.Path, 'home', classmethod(lambda cls: tmp_path / 'usuario'))
    monkeypatch.delenv('REPERTORIO_HOME', raising=False)
    monkeypatch.setattr(config.sys, 'platform', 'darwin')
    program = tmp_path / 'programa'
    assert config.default_home(program) == tmp_path / 'usuario/Library/Application Support/Repertorio'
    monkeypatch.setattr(config.sys, 'platform', 'win32')
    monkeypatch.setenv('LOCALAPPDATA', str(tmp_path / 'local'))
    assert config.default_home(program) == tmp_path / 'local/Repertorio'
    # Instalação anterior continua com a biblioteca onde estava.
    (program / 'app/.runtime').mkdir(parents=True)
    (program / 'app/.runtime/library.sqlite3').write_bytes(b'')
    assert config.default_home(program) == program / 'app/.runtime'


def test_backups_stay_local_unless_chosen(tmp_path, monkeypatch):
    from repertorio import backup
    from repertorio.config import Settings
    monkeypatch.setattr(backup.Path, 'home', classmethod(lambda cls: tmp_path / 'usuario'))
    monkeypatch.delenv('REPERTORIO_BACKUP_DIR', raising=False)
    (tmp_path / 'usuario/Library/Mobile Documents/com~apple~CloudDocs').mkdir(parents=True)
    fresh = Settings(tmp_path, tmp_path / 'dados/Repertorio')
    assert backup.backup_dir(fresh) == tmp_path / 'dados/Repertorio Backups'
    assert backup.backup_dir(Settings(tmp_path, tmp_path / 'app/.runtime')) == tmp_path / 'app/backups'
    icloud = tmp_path / 'usuario/Library/Mobile Documents/com~apple~CloudDocs/Backups/Repertório'
    icloud.mkdir(parents=True);(icloud / 'repertorio-2026-01-01-000000.zip').write_bytes(b'')
    assert backup.backup_dir(fresh) == icloud
    monkeypatch.setenv('REPERTORIO_BACKUP_DIR', str(tmp_path / 'escolhida'))
    assert backup.backup_dir(fresh) == tmp_path / 'escolhida'


def test_upgrade_makes_a_copy_first_and_restore_refuses_newer_backups(tmp_path, monkeypatch):
    import sqlite3, zipfile, json
    from contextlib import closing
    from alembic import command
    from alembic.config import Config
    from repertorio import backup
    from repertorio.config import Settings
    from repertorio.db import Database
    monkeypatch.setenv('REPERTORIO_BACKUP_DIR', str(tmp_path / 'copias'))
    settings = Settings(tmp_path / 'raiz', tmp_path / 'dados')
    db = Database(settings)
    config = Config(str(Path(backup.__file__).resolve().parents[1] / 'alembic.ini'))
    with db.engine.connect() as conn:
        config.attributes['connection'] = conn
        command.upgrade(config, '0004')
    db.engine.dispose()
    copy = backup.before_upgrade(settings)
    assert copy and Path(copy).exists() and 'antes-da-atualizacao' in copy
    db = Database(settings);db.migrate();db.engine.dispose()
    assert backup.before_upgrade(settings) is None
    newer = tmp_path / 'nova.zip'
    backup.backup(settings, newer)
    with zipfile.ZipFile(newer) as z:
        data = z.read('library.sqlite3');manifest = json.loads(z.read('manifest.json'))
    stage = tmp_path / 'banco.sqlite3';stage.write_bytes(data)
    with closing(sqlite3.connect(stage)) as con:
        con.execute('PRAGMA journal_mode=DELETE');con.execute("UPDATE alembic_version SET version_num='9999_futuro'");con.commit()
    import hashlib
    manifest['checksums']['library.sqlite3'] = hashlib.sha256(stage.read_bytes()).hexdigest()
    with zipfile.ZipFile(tmp_path / 'futuro.zip', 'w') as z:
        z.write(stage, 'library.sqlite3');z.writestr('manifest.json', json.dumps(manifest))
    with pytest.raises(ValueError, match='versão mais nova'):
        backup.restore(settings, tmp_path / 'futuro.zip')
    assert settings.db.exists()


def test_second_service_gets_a_clear_message(tmp_path):
    from repertorio.app import open_lock
    from repertorio.config import Settings
    settings = Settings(tmp_path, tmp_path / 'dados')
    first = open_lock(settings)
    try:
        with pytest.raises(RuntimeError, match='Já existe um serviço'):
            open_lock(settings)
    finally:
        first.close()


def test_stop_ends_the_service_and_releases_the_library(tmp_path):
    import os, socket, subprocess, sys, time
    import httpx
    with socket.socket() as probe:
        probe.bind(('127.0.0.1', 0));port = probe.getsockname()[1]
    root = tmp_path / 'raiz';root.mkdir()
    env = {**os.environ, 'PYTHONPATH': str(Path(__file__).resolve().parents[1] / 'server'), 'REPERTORIO_ROOT': str(root),
           'REPERTORIO_HOME': str(tmp_path / 'dados'), 'REPERTORIO_PORT': str(port), 'REPERTORIO_BACKUP_DIR': str(tmp_path / 'copias')}
    cli = [sys.executable, '-m', 'repertorio.cli']
    service = subprocess.Popen(cli + ['serve'], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    try:
        for _ in range(80):
            try:
                if httpx.get(f'http://127.0.0.1:{port}/api/health', timeout=.5).status_code == 200:break
            except httpx.HTTPError:time.sleep(.25)
        again = subprocess.run(cli + ['serve'], env=env, capture_output=True, text=True, timeout=30)
        assert again.returncode == 1 and 'já está ligado' in again.stderr
        stopped = subprocess.run(cli + ['stop'], env=env, capture_output=True, text=True, timeout=30)
        assert stopped.returncode == 0 and 'Serviço encerrado' in stopped.stdout, stopped.stderr
        service.wait(timeout=15)
        assert subprocess.run(cli + ['stop'], env=env, capture_output=True, text=True, timeout=30).stdout.strip() == 'O serviço não está ligado.'
    finally:
        if service.poll() is None:service.kill()


def test_connect_writes_agents_and_claude_files_without_losing_content(tmp_path):
    from repertorio.cli import write_instructions
    block = '<!-- repertorio:start -->\nNovo\n<!-- repertorio:end -->\n'
    write_instructions(tmp_path, block)
    assert (tmp_path / 'AGENTS.md').read_text(encoding='utf-8') == block
    assert (tmp_path / 'CLAUDE.md').read_text(encoding='utf-8') == '@AGENTS.md\n'
    (tmp_path / 'AGENTS.md').write_text('# Projeto\n\nRegras próprias.\n\n' + block.replace('Novo', 'Antigo'), encoding='utf-8')
    (tmp_path / 'CLAUDE.md').write_text('# Claude\n\n@AGENTS.md\n', encoding='utf-8')
    write_instructions(tmp_path, block)
    assert (tmp_path / 'AGENTS.md').read_text(encoding='utf-8') == '# Projeto\n\nRegras próprias.\n\n' + block
    assert (tmp_path / 'CLAUDE.md').read_text(encoding='utf-8') == '# Claude\n\n@AGENTS.md\n'


def test_service_started_before_init_still_gets_vocabulary(tmp_path):
    from repertorio.starter import initialize
    settings = Settings(tmp_path, tmp_path / 'dados')
    db = Database(settings);db.migrate();db.engine.dispose()
    out = initialize(settings)
    assert out['initialized'] and out['preserved_existing_library']
    db = Database(settings)
    try:
        assert db.one("SELECT value FROM meta WHERE key='vocabulary'")
        assert db.one("SELECT name FROM workspaces WHERE id='referencias'")['name'] == 'Meu repertório'
    finally:
        db.engine.dispose()
    assert not initialize(settings)['initialized']
