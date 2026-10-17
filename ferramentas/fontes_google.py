#!/usr/bin/env python3
"""Baixa famílias do Google Fonts para uma pasta local, para a apresentação funcionar sem internet.
Uso: python3 -I ferramentas/fontes_google.py "Bricolage Grotesque" "Inter" "Instrument Serif" --pasta minha-apresentacao/fontes
Gera <pasta>/fontes.css (use com <link rel="stylesheet" href="fontes/fontes.css">) e os arquivos de fonte.
Baixa os pesos variáveis inteiros (ou 400/700 para fontes sem eixo) e a versão itálica quando existir.

No fim mostra o que cada família tem de verdade (pesos, itálico, versalete, algarismos, ligaduras, acentos do português).
A versão servida pelo Google vem sem versalete, algarismos de texto e variantes estilísticas.
Com --completa, baixa os arquivos inteiros do repositório google/fonts (maiores, com todos os recursos).
Precisa do fontTools para o relatório e para --completa (já instalado neste Mac).
"""
import argparse
import io
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
PORTUGUES = 'ãõçáéíóúâêôàÃÕÇÁÉÍÓÚÂÊÔÀ“”‘’…×'


def baixar(url, ua=UA):
    return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': ua} if ua else {}), timeout=60).read()


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


def recursos(dados):
    """O que um arquivo de fonte (TTF/OTF) tem: recursos OpenType e acentos do português que faltam."""
    from fontTools.ttLib import TTFont
    f = TTFont(io.BytesIO(dados))
    tags = {r.FeatureTag for t in ('GSUB', 'GPOS') if t in f for r in f[t].table.FeatureList.FeatureRecord}
    cmap = f.getBestCmap()
    peso = next((('%g %g' % (a.minValue, a.maxValue)) for a in f['fvar'].axes if a.axisTag == 'wght'), None) if 'fvar' in f else None
    return tags, [c for c in PORTUGUES if ord(c) not in cmap], peso or str(f['OS/2'].usWeightClass)


def relatorio(nome, tags, faltam, pesos, italico):
    sim = lambda *t: 'sim' if all(x in tags for x in t) else 'não'
    print('%s: pesos %s, itálico %s | versalete %s, algarismos de texto %s, tabulares %s, ligaduras %s | português %s' % (
        nome, pesos, 'sim' if italico else 'não', sim('smcp'), sim('onum'), sim('tnum'), sim('liga'),
        'ok' if not faltam else 'faltam ' + ' '.join(faltam)))


def completa(familia, pasta):
    """Baixa os TTF inteiros de google/fonts (ofl, apache ou ufl) e devolve as regras @font-face."""
    slug = re.sub(r'[^a-z0-9]', '', familia.lower())
    for lic in ('ofl', 'apache', 'ufl'):
        try:
            itens = json.loads(baixar('https://api.github.com/repos/google/fonts/contents/%s/%s' % (lic, slug)))
            break
        except urllib.error.HTTPError:
            continue
    else:
        raise SystemExit('Não achei %s no repositório google/fonts. Rode sem --completa.' % familia)
    regras, tags, faltam, pesos, italico = [], set(), [], [], False
    for it in itens:
        if not it['name'].endswith('.ttf'):
            continue
        dados = baixar(it['download_url'])
        open(os.path.join(pasta, it['name']), 'wb').write(dados)
        t, f, p = recursos(dados)
        est = 'italic' if 'Italic' in it['name'] else 'normal'
        if est == 'normal':
            tags, faltam = tags | t, f
        italico = italico or est == 'italic'
        pesos.append(p)
        regras.append("@font-face {\n  font-family: '%s';\n  font-style: %s;\n  font-weight: %s;\n  font-display: swap;\n  src: url(%s) format('truetype');\n}" % (
            familia, est, p, urllib.parse.quote(it['name'])))
    if not regras:
        raise SystemExit('Nenhum TTF de %s no repositório google/fonts. Rode sem --completa.' % familia)
    relatorio(familia, tags, faltam, ' / '.join(sorted(set(pesos))), italico)
    return regras


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('familias', nargs='+')
    ap.add_argument('--pasta', required=True)
    ap.add_argument('--completa', action='store_true', help='arquivos inteiros, com versalete e algarismos de texto (maiores)')
    a = ap.parse_args()
    os.makedirs(a.pasta, exist_ok=True)
    meta = baixar('https://fonts.google.com/metadata/fonts').decode()
    meta = json.loads(meta[meta.index('{'):])
    partes, saida, n = [], [], 0
    for fam in a.familias:
        nome, eixo, faixa, italico = eixos(fam, meta)
        if a.completa:
            regras = completa(nome, a.pasta)
            saida += regras
            n += len(regras)
            continue
        if '..' in faixa:
            spec = 'ital,wght@0,%s;1,%s' % (faixa, faixa) if italico else 'wght@%s' % faixa
        else:
            ps = faixa.split(';')
            spec = 'ital,wght@' + ';'.join(['0,%s' % p for p in ps] + (['1,%s' % p for p in ps] if italico else []))
        partes.append('family=%s:%s' % (urllib.parse.quote_plus(nome), spec))
        try:
            # o mesmo arquivo da API em TTF (sem User-Agent de navegador), só para o relatório
            ttf = re.search(r'url\((https[^)]+)\)', baixar('https://fonts.googleapis.com/css2?family=%s' % urllib.parse.quote_plus(nome), ua=None)).group(1)
            t, f, _ = recursos(baixar(ttf, ua=None))
            relatorio(nome, t, f, faixa.replace('..', '-').replace(';', ' '), italico)
        except Exception as e:  # o relatório não pode impedir o download
            print('%s: sem relatório (%s)' % (nome, e))
    if partes:
        css = baixar('https://fonts.googleapis.com/css2?%s&display=swap' % '&'.join(partes)).decode()
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
