#!/usr/bin/env python3
"""Baixa famílias do Google Fonts para uma pasta local, para a apresentação funcionar sem internet.
Uso: python3 -I ferramentas/fontes_google.py "Bricolage Grotesque" "Inter" "Instrument Serif" --pasta minha-apresentacao/fontes
Gera <pasta>/fontes.css (use com <link rel="stylesheet" href="fontes/fontes.css">) e os arquivos .woff2.
Baixa os pesos variáveis inteiros (ou 400/700 para fontes sem eixo) e a versão itálica quando existir.
"""
import argparse
import json
import os
import re
import urllib.parse
import urllib.request

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'


def baixar(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60).read()


def eixos(familia, meta):
    for f in meta['familyMetadataList']:
        if f['family'].lower() == familia.lower():
            peso = next((a for a in f.get('axes', []) if a['tag'] == 'wght'), None)
            estilos = set(f.get('fonts', {}).keys())
            italico = any(k.endswith('i') for k in estilos)
            if peso:
                return f['family'], 'wght', '%d..%d' % (peso['min'], peso['max']), italico
            pesos = sorted({int(re.sub(r'\D', '', k) or 400) for k in estilos})
            return f['family'], 'wght', ';'.join(str(p) for p in pesos), italico
    raise SystemExit('Família não encontrada no Google Fonts: %s' % familia)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('familias', nargs='+')
    ap.add_argument('--pasta', required=True)
    a = ap.parse_args()
    os.makedirs(a.pasta, exist_ok=True)
    meta = baixar('https://fonts.google.com/metadata/fonts').decode()
    meta = json.loads(meta[meta.index('{'):])
    partes = []
    for fam in a.familias:
        nome, eixo, faixa, italico = eixos(fam, meta)
        if '..' in faixa:
            spec = 'ital,wght@0,%s;1,%s' % (faixa, faixa) if italico else 'wght@%s' % faixa
        else:
            ps = faixa.split(';')
            spec = 'ital,wght@' + ';'.join(['0,%s' % p for p in ps] + (['1,%s' % p for p in ps] if italico else []))
        partes.append('family=%s:%s' % (urllib.parse.quote_plus(nome), spec))
    css = baixar('https://fonts.googleapis.com/css2?%s&display=swap' % '&'.join(partes)).decode()
    saida, n = [], 0
    for sub, bloco in re.findall(r'/\* ([^*]+) \*/\s*@font-face \{(.*?)\}', css, re.S):
        if sub.strip() not in ('latin', 'latin-ext'):
            continue
        fam = re.search(r"font-family: '([^']+)'", bloco).group(1)
        est = re.search(r'font-style: (\w+)', bloco).group(1)
        pes = re.search(r'font-weight: ([\d ]+)', bloco).group(1).replace(' ', '_')
        url = re.search(r'url\((https[^)]+)\)', bloco).group(1)
        arq = '%s-%s-%s-%s.woff2' % (fam.replace(' ', ''), est, pes, sub.strip())
        open(os.path.join(a.pasta, arq), 'wb').write(baixar(url))
        saida.append('/* %s */\n@font-face {%s}' % (sub.strip(), re.sub(r'url\(https[^)]+\)', 'url(%s)' % arq, bloco)))
        n += 1
    open(os.path.join(a.pasta, 'fontes.css'), 'w').write('\n'.join(saida) + '\n')
    print('%d arquivos de fonte em %s' % (n, a.pasta))
    print('No HTML: <link rel="stylesheet" href="%s/fontes.css">' % os.path.basename(os.path.normpath(a.pasta)))


if __name__ == '__main__':
    main()
