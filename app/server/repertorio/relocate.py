"""Atualiza caminhos locais depois de mover a pasta, preservando os identificadores."""
import json
import os
import re
import sqlite3
from pathlib import Path
from .locking import lock_file


def relocate(settings, previous_root, backup_path):
    # O caminho antigo pode ser um link de compatibilidade. Não o resolva.
    previous = os.path.abspath(os.path.expanduser(str(previous_root))).rstrip('/\\')
    current = str(settings.root)
    backup_path = Path(backup_path).expanduser().resolve()
    if previous == current:
        raise ValueError('Informe uma raiz anterior diferente da raiz atual.')
    if backup_path.exists() or backup_path.is_relative_to(settings.home):
        raise ValueError('Use um backup novo fora da pasta de dados.')
    patterns = []
    for old, new in [(os.path.join(previous, 'repertorio'), os.path.join(current, 'app')), (previous, current)]:
        for source, target in dict.fromkeys([
            (old, new),
            (json.dumps(old, ensure_ascii=False)[1:-1], json.dumps(new, ensure_ascii=False)[1:-1]),
            (old.replace('\\', '/'), new.replace('\\', '/')),
        ]):
            patterns.append((re.compile(re.escape(source) + r'(?=[/\\]|$|["\s])'), target))
    def rewritten(value):
        for pattern, replacement in patterns:
            value = pattern.sub(lambda _: replacement, value)
        return value

    lock_path = settings.home.parent / (settings.home.name + '.lock')
    with lock_path.open('a+b') as lock:
        try:
            lock_file(lock)
        except BlockingIOError:
            raise ValueError('Encerre o serviço antes de atualizar os caminhos.') from None
        with sqlite3.connect(settings.db) as db:
            if db.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
                raise ValueError('O banco precisa passar pela verificação de integridade.')
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            with sqlite3.connect(backup_path) as backup:
                db.backup(backup)
            db.execute('PRAGMA foreign_keys=ON')
            tables = [r[0] for r in db.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE 'ref_search%'"
            )]
            counts = {t: db.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0] for t in tables}
            asset_ids = db.execute('SELECT id FROM assets ORDER BY id').fetchall()
            changed = {}
            for table in tables:
                columns = [r[1] for r in db.execute(f'PRAGMA table_info("{table}")')
                           if r[1] in {'path', 'root', 'payload', 'value'} and r[2].upper() == 'TEXT' and not r[5]]
                for column in columns:
                    rows = db.execute(
                        f'SELECT rowid,"{column}" FROM "{table}" WHERE instr("{column}",?)>0', (previous,)
                    ).fetchall()
                    updates = [(rewritten(value), rowid) for rowid, value in rows if rewritten(value) != value]
                    if updates:
                        db.executemany(f'UPDATE "{table}" SET "{column}"=? WHERE rowid=?', updates)
                        changed[f'{table}.{column}'] = len(updates)
            if db.execute('SELECT id FROM assets ORDER BY id').fetchall() != asset_ids:
                raise ValueError('Os identificadores dos arquivos precisam ser preservados.')
            if any(db.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0] != n for t, n in counts.items()):
                raise ValueError('As contagens do acervo precisam ser preservadas.')
            missing = [aid for aid, path in db.execute('SELECT id,path FROM assets WHERE missing=0') if not Path(path).is_file()]
            if missing:
                raise ValueError(f'{len(missing)} arquivos não encontrados no destino. As alterações foram desfeitas.')
            if db.execute('PRAGMA foreign_key_check').fetchall():
                raise ValueError('Os vínculos precisam passar pela verificação de integridade.')
    return {'previous_root': previous, 'root': current, 'backup': str(backup_path),
            'updated': changed, 'assets': len(asset_ids), 'identifiers_preserved': True}
