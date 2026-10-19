import hashlib
import importlib.util
import json
from pathlib import Path
import zipfile

import pytest


spec = importlib.util.spec_from_file_location('product_package', Path(__file__).resolve().parents[2] / 'ferramentas/empacotar_produto.py')
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


def test_package_has_verified_inventory_and_excludes_private_material(tmp_path):
    root = tmp_path / 'source'
    for name in package.FIXED + ['README.md', 'app/web/dist/index.html', 'app/server/repertorio/cli.py'] + ['docs/produto/' + p for p in package.CLIENT_DOCS]:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('conteúdo próprio', encoding='utf-8')
    for name in ['app/.runtime/library.sqlite3', 'dados/indice.jsonl', 'perestroika/original.pdf', 'soap/aula.pdf', '.env', 'app/server/__pycache__/secret.pyc']:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('material privado', encoding='utf-8')
    destination = tmp_path / 'evaluation.zip'
    result = package.package_product(root, destination)
    with zipfile.ZipFile(destination) as archive:
        manifest = json.loads(archive.read('repertorio/PACOTE.json'))
        assert result['files'] == len(archive.namelist())
        assert not manifest['includes_private_library']
        assert all('material privado' not in archive.read(name).decode('utf-8') for name in archive.namelist())
        for name, item in manifest['files'].items():
            assert hashlib.sha256(archive.read('repertorio/' + name)).hexdigest() == item['sha256']
        assert archive.getinfo('repertorio/app/run.sh').external_attr >> 16 & 0o111
    with pytest.raises(FileExistsError):
        package.package_product(root, destination)
    with pytest.raises(ValueError, match='fora do Repertório'):
        package.package_product(root, root / 'output.zip')
