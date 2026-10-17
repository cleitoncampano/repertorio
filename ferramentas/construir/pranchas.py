#!/usr/bin/env python3
"""Monta uma prancha (imagem única com os slides numerados) para cada arquivo do acervo,
a partir das miniaturas do catálogo. Saída: _catalogo/pranchas/<id>.jpg (e <id>-2.jpg ... quando passa de 40 slides).
Uso, da raiz do projeto:  python3 -I ferramentas/construir/pranchas.py [--sem-antes] [ids...]
(--sem-antes tira os slides marcados como antes ou ocultos nas fichas; use depois de montar.py)
"""
import glob
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor

from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MINI = os.path.join(RAIZ, '_catalogo', 'miniaturas')
SAIDA = os.path.join(RAIZ, '_catalogo', 'pranchas')
LARGURA, GAP, TOPO, POR_PRANCHA = 1560, 8, 44, 40
FONTE = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'


def catalogo(sem_antes=False):
    s = open(os.path.join(RAIZ, '_catalogo', 'dados.js')).read()
    d = json.loads(s[s.index('{'):s.rindex('}') + 1])
    fora = {}
    if sem_antes:
        for l in open(os.path.join(RAIZ, 'dados', 'fichas.jsonl')):
            f = json.loads(l)
            fora[f['id']] = set(f.get('antes', [])) | {x['n'] for x in f.get('slides', []) if x.get('intencao') in ('ANTES', 'OCULTO')}
    itens = [(x['id'], x['titulo'], set(x.get('ocultos', [])), fora.get(x['id'], set())) for x in d['decks']]
    itens += [(c['id'], 'Canva: ' + c['aula'], set(), fora.get(c['id'], set())) for c in d['canva']]
    return itens


def montar(item):
    did, titulo, ocultos, fora = item
    arqs = sorted(glob.glob(os.path.join(MINI, did, '*.jpg')), key=lambda p: int(os.path.basename(p)[:-4]))
    todos = len(arqs)
    arqs = [p for p in arqs if int(os.path.basename(p)[:-4]) not in fora] or arqs
    if not arqs:
        return did, []
    w0, h0 = Image.open(arqs[0]).size
    deitado = w0 >= h0
    f_num = ImageFont.truetype(FONTE, 17)
    f_tit = ImageFont.truetype(FONTE, 20)
    feitas = []
    lotes = [arqs[i:i + POR_PRANCHA] for i in range(0, len(arqs), POR_PRANCHA)]
    for k, lote in enumerate(lotes, 1):
        n = len(lote)
        if deitado:
            cols = n if n <= 4 else 4 if n <= 12 else 5 if n <= 25 else 6
        else:
            cols = min(n, 8)
        cw = (LARGURA - GAP * (cols + 1)) // cols
        ch = round(cw * h0 / w0)
        linhas = -(-n // cols)
        img = Image.new('RGB', (LARGURA, TOPO + linhas * (ch + GAP) + GAP), (24, 24, 24))
        d = ImageDraw.Draw(img)
        extra = '  ·  sem %d slide(s) de antes' % (todos - len(arqs)) if todos > len(arqs) else ''
        cab = '%s  ·  %s  ·  %d slides%s%s' % (did, titulo, todos, extra, '  ·  parte %d/%d' % (k, len(lotes)) if len(lotes) > 1 else '')
        d.text((GAP + 2, 12), cab, font=f_tit, fill=(235, 235, 235))
        for i, p in enumerate(lote):
            num = int(os.path.basename(p)[:-4])
            x = GAP + (i % cols) * (cw + GAP)
            y = TOPO + (i // cols) * (ch + GAP)
            im = Image.open(p).convert('RGB').resize((cw, ch), Image.LANCZOS)
            img.paste(im, (x, y))
            rot = str(num) + (' oculto' if num in ocultos else '')
            tw = d.textlength(rot, font=f_num)
            d.rectangle([x, y, x + tw + 12, y + 24], fill=(200, 30, 30) if num in ocultos else (0, 0, 0))
            d.text((x + 6, y + 3), rot, font=f_num, fill=(255, 255, 255))
        nome = did + ('' if k == 1 else '-%d' % k) + '.jpg'
        img.save(os.path.join(SAIDA, nome), quality=80, optimize=True)
        feitas.append('_catalogo/pranchas/' + nome)
    return did, feitas


def main():
    os.makedirs(SAIDA, exist_ok=True)
    sem_antes = '--sem-antes' in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    itens = catalogo(sem_antes)
    if args:
        itens = [x for x in itens if x[0] in set(args)]
    mapa = {}
    with ProcessPoolExecutor() as ex:
        for did, feitas in ex.map(montar, itens, chunksize=8):
            mapa[did] = feitas
    if not args:
        json.dump(mapa, open(os.path.join(SAIDA, 'pranchas.json'), 'w'), ensure_ascii=False, indent=0)
    print('pranchas', sum(len(v) for v in mapa.values()), 'de', len(mapa), 'arquivos')


if __name__ == '__main__':
    main()
