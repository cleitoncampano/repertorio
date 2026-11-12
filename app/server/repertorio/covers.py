"""Capas alternativas, independentes dos originais e dos slides da apresentação."""
import hashlib
import os
from pathlib import Path

from PIL import Image
from sqlalchemy import text

from .importer import asset


def set_cover(lib, rid, source):
    row = lib.db.one('SELECT kind FROM refs WHERE id=:id', id=rid)
    if not row or row['kind'] != 'arquivo':
        raise ValueError('A capa alternativa exige uma apresentação existente.')
    source = Path(source).resolve()
    with Image.open(source) as image:
        image.verify()
    # Conteúdo imutável: uma troca ganha outro endereço e não reutiliza o cache antigo.
    data = source.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    folder = lib.settings.home / 'assets' / 'covers' / rid
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / (digest + source.suffix.lower())
    if not target.exists():
        temporary = target.with_name(target.name + f'.{os.getpid()}.tmp')
        temporary.write_bytes(data)
        os.replace(temporary, target)
    with lib.db.engine.begin() as conn:
        current = conn.execute(text("SELECT id,path FROM assets WHERE ref_id=:id AND role='cover'"), dict(id=rid)).mappings().all()
        if len(current) == 1 and current[0]['path'] == str(target):
            return current[0]['id']
        # Os arquivos anteriores ficam no armazenamento para permitir recuperação.
        conn.execute(text("DELETE FROM assets WHERE ref_id=:id AND role='cover'"), dict(id=rid))
        aid = asset(conn, lib.settings, rid, target, 'cover')
        lib.db.log(conn, 'cover_changed', ref_id=rid, asset_id=aid, sha256=digest)
    return aid


def clear_cover(lib, rid):
    """Remove só a seleção alternativa; as prévias originais voltam automaticamente."""
    with lib.db.engine.begin() as conn:
        result = conn.execute(text("DELETE FROM assets WHERE ref_id=:id AND role='cover'"), dict(id=rid))
        if result.rowcount:
            lib.db.log(conn, 'cover_restored', ref_id=rid)
    return bool(result.rowcount)
