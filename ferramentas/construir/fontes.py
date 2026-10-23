#!/usr/bin/env python3
"""Índice de tipografia: famílias usadas nos arquivos do acervo, onde está o arquivo da fonte, se existe no Google Fonts
e os pares de fonte (título + texto) mais comuns.
Saída: dados/fontes.json e biblioteca/tipografia.md
Uso, da raiz do projeto:  python3 -I ferramentas/construir/fontes.py [caminho do metadata do Google Fonts]
(sem o caminho, baixa https://fonts.google.com/metadata/fonts)
"""
import collections
import json
import os
import re
import struct
import sys
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, '_catalogo', 'gerador'))
from fontnames_lib import names_at  # noqa: E402

PASTA = os.path.join(RAIZ, '_originais', 'fontes', 'arquivos')
COMERCIAIS = re.compile(r'helvetica|din|gotham|sf pro|circular|druk|sequel|futura|avenir|proxima|gilroy|neue haas|akzidenz|brandon|'
                        r'unilever|3m |rockwell|georgia|arial|calibri|aptos|segoe|trebuchet|gill sans|biggerdisplay|atomic|etna', re.I)
SISTEMA = {'arial', 'calibri', 'calibri light', 'aptos', 'aptos display', 'georgia', 'trebuchet ms', 'segoe ui', 'times new roman', 'verdana', 'tahoma', 'impact'}


def chave(n):
    return re.sub(r'[^a-z0-9]', '', n.lower())


def ler_familias():
    fam = collections.defaultdict(list)
    for r, _, fs in os.walk(PASTA):
        for f in fs:
            p = os.path.join(r, f)
            try:
                data = open(p, 'rb').read()
            except OSError:
                continue
            if data[:4] == b'ttcf':
                n = struct.unpack('>I', data[8:12])[0]
                offs = struct.unpack('>%dI' % n, data[12:12 + 4 * n])
            elif data[:4] in (b'\x00\x01\x00\x00', b'OTTO', b'true'):
                offs = [0]
            else:
                continue
            for o in offs:
                try:
                    nm = names_at(data, o)
                except Exception:
                    continue
                familia = nm.get(16) or nm.get(1)
                if not familia:
                    continue
                fam[familia.strip()].append({'estilo': (nm.get(17) or nm.get(2) or '').strip(), 'nome': (nm.get(4) or '').strip(),
                                             'arquivo': os.path.relpath(p, RAIZ)})
    return fam


def main():
    if len(sys.argv) > 1:
        meta = open(sys.argv[1]).read()
    else:
        meta = urllib.request.urlopen('https://fonts.google.com/metadata/fonts', timeout=60).read().decode()
    meta = meta[meta.index('{'):]
    google = {chave(x['family']): x['family'] for x in json.loads(meta)['familyMetadataList']}

    locais = ler_familias()
    locais_k = {chave(k): k for k in locais}
    uso = collections.Counter()
    decks_por = collections.Counter()
    pares = collections.Counter()
    for l in open(os.path.join(RAIZ, 'dados', 'decks.jsonl')):
        d = json.loads(l)
        fs = [f['nome'] for f in d['fontes']]
        for f in d['fontes']:
            uso[f['nome']] += f['usos']
            decks_por[f['nome']] += 1
        reais = [f for f in fs if f.lower() not in SISTEMA]
        if len(reais) >= 2:
            pares[tuple(reais[:2])] += 1

    def base(nome):
        """'Montserrat Black' -> 'Montserrat' quando a família base existe."""
        k = chave(nome)
        if k in google or k in locais_k:
            return nome
        partes = nome.split()
        for i in range(len(partes) - 1, 0, -1):
            cand = ' '.join(partes[:i])
            if chave(cand) in google or chave(cand) in locais_k:
                return cand
        return nome

    pares_fam, mesma = collections.Counter(), collections.Counter()
    for (a, b), n in pares.items():
        ba, bb = base(a), base(b)
        if chave(ba) == chave(bb):
            mesma[ba] += n
        else:
            pares_fam[(ba, bb)] += n
    familias = collections.OrderedDict()
    for nome, n in sorted(uso.items(), key=lambda x: -decks_por[x[0]]):
        b = base(nome)
        f = familias.setdefault(b, {'familia': b, 'variantes_usadas': [], 'arquivos_pptx': 0, 'usos': 0})
        if nome != b:
            f['variantes_usadas'].append(nome)
        f['arquivos_pptx'] += decks_por[nome]
        f['usos'] += n
    for f in familias.values():
        k = chave(f['familia'])
        f['google_fonts'] = google.get(k)
        f['arquivos_locais'] = sorted({x['arquivo'] for x in locais.get(locais_k.get(k, ''), [])})[:12]
        f['sistema'] = f['familia'].lower() in SISTEMA
        f['licenca'] = 'livre (Google Fonts)' if f['google_fonts'] else 'sistema/Office' if f['sistema'] else \
            'provavelmente comercial' if COMERCIAIS.search(f['familia']) else 'verificar'
    lista = list(familias.values())
    json.dump({'familias': lista, 'pares': [{'titulo': a, 'texto': b, 'arquivos': n} for (a, b), n in pares_fam.most_common(40)],
               'familia_unica': [{'familia': a, 'arquivos': n} for a, n in mesma.most_common(30)],
               'locais_sem_uso': sorted(set(locais) - set(familias))}, open(os.path.join(RAIZ, 'dados', 'fontes.json'), 'w'), ensure_ascii=False, indent=1)

    p = ['# Tipografia', '',
         'Fontes usadas nos %d arquivos do acervo. Para HTML publicado, prefira as do Google Fonts (livres e carregam por link).' % len(open(os.path.join(RAIZ, 'dados', 'decks.jsonl')).readlines()),
         'As comerciais servem de referência de estilo: troque por uma livre parecida.', '',
         '## Como usar no HTML', '',
         'Google Fonts (funciona em qualquer lugar):', '',
         '```html', '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
         '<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&family=Inter:wght@400;600&display=swap" rel="stylesheet">', '```', '',
         'Arquivo local (só para uso interno; confira a licença antes de publicar):', '',
         '```css', '@font-face { font-family: "Minha Fonte"; src: url("../_originais/fontes/arquivos/Fontes/Arquivo.otf"); font-weight: 700; }', '```', '',
         '## Uma família só, com pesos bem contrastantes (o mais comum no acervo)', '',
         'Título em peso extremo (Black, ExtraBold) e texto em peso leve da mesma família. É o jeito mais seguro de ter contraste sem brigar.', '']
    for a, n in mesma.most_common(12):
        g = ' (Google Fonts)' if chave(a) in google else ''
        p.append('- %s%s: %d arquivos' % (a, g, n))
    p += ['', '## Pares de famílias diferentes (título + texto)', '']
    for (a, b), n in pares_fam.most_common(15):
        p.append('- %s + %s (%d arquivos)' % (a, b, n))
    p += ['', '## Famílias', '', '| família | arquivos | Google Fonts | licença | arquivo local |', '|---|---|---|---|---|']
    for f in lista:
        if f['arquivos_pptx'] < 2 and not f['google_fonts']:
            continue
        g = '[sim](https://fonts.google.com/specimen/%s)' % f['google_fonts'].replace(' ', '+') if f['google_fonts'] else 'não'
        loc = '`%s`' % f['arquivos_locais'][0] if f['arquivos_locais'] else ''
        p.append('| %s | %d | %s | %s | %s |' % (f['familia'], f['arquivos_pptx'], g, f['licenca'], loc))
    p += ['', 'Lista completa (com variantes e todos os arquivos locais): `dados/fontes.json`.']
    open(os.path.join(RAIZ, 'biblioteca', 'tipografia.md'), 'w').write('\n'.join(p) + '\n')
    print('famílias usadas', len(lista), '| no Google Fonts', sum(1 for f in lista if f['google_fonts']),
          '| com arquivo local', sum(1 for f in lista if f['arquivos_locais']), '| famílias locais', len(locais))


if __name__ == '__main__':
    main()
