#!/usr/bin/env python3
"""Prepara um candidato de avaliação do software, sem o acervo de desenvolvimento."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FIXED = [
    'app/run.sh', 'app/run.ps1', 'app/setup.sh', 'app/setup.ps1', 'app/Iniciar Repertorio.cmd', 'app/Abrir Repertório.command',
    'app/requirements.lock', 'app/pyproject.toml',
    'app/mac/main.swift', 'app/mac/build.sh', 'app/mac/icone.png',
]
CLIENT_DOCS = ['PRODUTO.md', 'INSTALACAO.md', 'DEMONSTRACAO.md', 'OPERACAO.md', 'AVISOS-DE-TERCEIROS.md']
# Só as imagens citadas pelos documentos do pacote.
DEMO_IMAGES = ['mapa-demo.png', 'guia-demo.png']
# Nada pessoal, de cursos de terceiros ou de caminhos do computador de desenvolvimento pode ir no pacote.
FORBIDDEN = re.compile(r'cleiton|growmate|cvortex|perestroika|\bsoap\b|soap-|/users/|repert-rio-87e17c', re.IGNORECASE)


def cut(text, marker, name):
    """Corta a parte comercial e interna; se o título mudar, o pacote não sai em vez de levar a parte errada."""
    if marker not in text:
        raise ValueError(f'Marcador "{marker}" não encontrado em {name}. Atualize o empacotador.')
    return text.split(marker)[0].rstrip()


def check_clean(root, paths):
    """Na cópia com Git, o pacote sai só de arquivos sem alterações pendentes."""
    if not (root / '.git').exists():
        return
    pending = subprocess.run(['git', '-C', str(root), 'status', '--porcelain', '--', *paths], capture_output=True, text=True, check=True).stdout
    if pending.strip():
        raise ValueError('Há alterações sem commit nos arquivos do pacote:\n' + pending)


def check_content(files):
    found = []
    for name, data in files.items():
        text = data.decode('utf-8', 'ignore')
        for match in FORBIDDEN.finditer(name + '\n' + text):
            found.append(f'{name}: {match.group(0)}')
    if found:
        raise ValueError('Conteúdo pessoal ou de terceiros no pacote:\n' + '\n'.join(sorted(set(found))[:40]))


def package_product(root, destination):
    root = Path(root).resolve()
    destination = Path(destination).expanduser().resolve()
    if destination.is_relative_to(root):
        raise ValueError('Salve o pacote no projeto de destino, fora do Repertório.')
    if not (root / 'app/web/dist/index.html').is_file():
        raise ValueError('Compile a interface antes de preparar o pacote.')
    files = {}
    def add(path):
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            raise ValueError(f'Link ou origem externa não permitida: {path}')
        files[path.relative_to(root).as_posix()] = path.read_bytes()
    for name in FIXED:
        add(root / name)
    for directory, suffixes in [('app/server', {'.py', '.ini', '.mako', '.json'}), ('app/web/dist', None)]:
        for path in sorted((root / directory).rglob('*')):
            if path.is_file() and not any(part.startswith('.') or part == '__pycache__' for part in path.relative_to(root).parts):
                if suffixes is None or path.suffix in suffixes:
                    add(path)
    for name in CLIENT_DOCS:
        add(root / 'docs/produto' / name)
    product_key = 'docs/produto/PRODUTO.md'
    files[product_key] = (cut(files[product_key].decode('utf-8'), '## Capacidade atual e decisões abertas', product_key) + '\n').encode()
    for name in DEMO_IMAGES:
        add(root / 'docs/produto' / name)
    readme = cut((root / 'README.md').read_text(encoding='utf-8'), '## Preparação comercial', 'README.md')
    readme = readme.replace('[app/README.md](app/README.md)', '[guia de operação](docs/produto/OPERACAO.md)')
    files['README.md'] = (readme + '\n').encode()
    files['LEIA-ME.md'] = ('# Comece pelo Repertório\n\nLeia README.md e docs/produto/INSTALACAO.md. '
                          'A biblioteca começa vazia; a demonstração usa exemplos originais em dados separados.\n').encode()
    files['AGENTS.md'] = ('# Repertório\n\nConsulte docs/produto/PRODUTO.md e docs/produto/OPERACAO.md. '
                         'Mantenha a biblioteca e a curadoria neste produto. Crie materiais nos respectivos projetos de destino. '
                         'Incorpore apenas materiais próprios ou autorizados, com os espaços indicados pelo usuário.\n').encode()
    files['AVALIACAO.md'] = ('# Candidato de avaliação interna\n\n'
                            'Este pacote prepara a demonstração e a avaliação local do software. '
                            'Não define a licença de distribuição do Repertório. As licenças das dependências estão em '
                            'docs/produto/AVISOS-DE-TERCEIROS.md. A decisão de licenciamento e os termos de oferta precisam ser '
                            'tratados antes da distribuição comercial. '
                            'Não contém a biblioteca particular nem materiais de cursos.\n').encode()
    check_content(files)
    check_clean(root, sorted(name for name in files if (root / name).exists()))
    manifest = {'kind': 'repertorio-evaluation-candidate', 'includes_private_library': False,
                'license_status': 'owner_decision_required',
                'files': {name: {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()} for name, data in sorted(files.items())}}
    files['PACOTE.json'] = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo('repertorio/' + name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            mode = 0o755 if name.endswith(('.sh', '.command')) else 0o644
            info.external_attr = (0o100000 | mode) << 16
            archive.writestr(info, data)
    return {'destination': str(destination), 'files': len(files), 'bytes': destination.stat().st_size,
            'sha256': hashlib.sha256(destination.read_bytes()).hexdigest()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destino', required=True)
    args = parser.parse_args()
    print(json.dumps(package_product(ROOT, args.destino), ensure_ascii=False, indent=2))
