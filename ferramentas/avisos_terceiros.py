#!/usr/bin/env python3
"""Gera docs/produto/AVISOS-DE-TERCEIROS.md com as licenças do que vai no pacote do cliente.

Uso: python3 ferramentas/avisos_terceiros.py --python CAMINHO_DO_PYTHON
O Python indicado precisa ter só as dependências de app/requirements.lock (o ambiente do cliente, sem as de teste).
A lista da interface vem de `pnpm licenses list --prod`.
"""
import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESTINO = ROOT / 'docs/produto/AVISOS-DE-TERCEIROS.md'

LER_PYTHON = r'''
import json, re, sys
from importlib.metadata import distribution
out = []
for name in sys.argv[1:]:
    meta = distribution(name).metadata
    lic = meta.get('License-Expression') or ''
    if not lic:
        classes = [c.split('::')[-1].strip() for c in meta.get_all('Classifier') or [] if c.startswith('License ::')]
        lic = ', '.join(classes) or (meta.get('License') or '').splitlines()[0][:80]
    out.append({'name': meta['Name'], 'version': meta['Version'], 'license': lic or 'ver projeto', 'url': meta.get('Home-page') or ''})
print(json.dumps(out))
'''


def python_packages(python):
    lock = (ROOT / 'app/requirements.lock').read_text(encoding='utf-8')
    names = re.findall(r'^([A-Za-z0-9_.-]+)==', lock, flags=re.M)
    win_only = set(re.findall(r"^([A-Za-z0-9_.-]+)==\S+ ; sys_platform == 'win32'", lock, flags=re.M))
    found = subprocess.run([python, '-c', LER_PYTHON, *[n for n in names if n not in win_only]],
                           capture_output=True, text=True, check=True)
    return sorted(json.loads(found.stdout), key=lambda p: p['name'].lower())


def web_packages():
    found = subprocess.run(['pnpm', 'licenses', 'list', '--prod', '--json'], cwd=ROOT / 'app/web',
                           capture_output=True, text=True, check=True)
    items = [{'name': i['name'], 'version': ', '.join(i.get('versions') or []), 'license': lic}
             for lic, group in json.loads(found.stdout).items() for i in group]
    return sorted(items, key=lambda p: p['name'].lower())


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--python', required=True, help='Python com as dependências de app/requirements.lock')
    args = parser.parse_args()
    linhas = ['# Avisos de terceiros', '',
              'O Repertório usa bibliotecas de código aberto. Esta lista é gerada por `ferramentas/avisos_terceiros.py` '
              'a partir das dependências que vão para o computador do cliente. O texto completo de cada licença '
              'acompanha a própria biblioteca instalada.', '', '## Serviço local (Python)', '',
              '| Biblioteca | Versão | Licença |', '| --- | --- | --- |']
    linhas += [f"| {p['name']} | {p['version']} | {p['license']} |" for p in python_packages(args.python)]
    linhas += ['', '## Interface (navegador)', '', '| Biblioteca | Versão | Licença |', '| --- | --- | --- |']
    linhas += [f"| {p['name']} | {p['version']} | {p['license']} |" for p in web_packages()]
    DESTINO.write_text('\n'.join(linhas) + '\n', encoding='utf-8')
    print(DESTINO)


if __name__ == '__main__':
    main()
