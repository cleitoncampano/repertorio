#!/usr/bin/env python3
"""Prepara as imagens e vídeos do acervo para etiquetagem: folhas de 30 prévias com o código de cada uma, 4 folhas por lote.
Saída: dados/_trabalho/midia-lotes/lote-NNN.json + lote-NNN-K.jpg
Uso, da raiz do projeto:  python3 -I ferramentas/construir/lotes_midia.py
"""
import glob
import json
import os

from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SAIDA = os.path.join(RAIZ, 'dados', '_trabalho', 'midia-lotes')
FONTE = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
COLS, LINS, FOLHAS = 6, 5, 4


def selecionar():
    out = []
    for l in open(os.path.join(RAIZ, 'dados', 'midia.jsonl')):
        m = json.loads(l)
        if m.get('fallback_de') or not m.get('previa'):
            continue
        if m['tipo'] == 'imagem' and max(m.get('w') or 0, m.get('h') or 0) < 120:
            continue
        if m['tipo'] not in ('imagem', 'video'):
            continue
        papeis = {u.get('papel') for u in m['usos']}
        uso = 'video' if m['tipo'] == 'video' else 'recorte' if (m.get('transparencia') or 0) > 0.15 else 'fundo' if 'fundo' in papeis else 'foto'
        out.append({'id': m['id'][:8], 'previa': m['previa'], 'uso_auto': uso, 'w': m.get('w'), 'h': m.get('h')})
    ordem = {'recorte': 0, 'foto': 1, 'fundo': 2, 'video': 3}
    out.sort(key=lambda x: (ordem[x['uso_auto']], x['id']))
    return out


def folha(itens, destino):
    cw, ch, cab = 254, 200, 24
    f = ImageFont.truetype(FONTE, 16)
    img = Image.new('RGB', (COLS * cw + (COLS + 1) * 6, LINS * (ch + cab) + (LINS + 1) * 6), (60, 60, 60))
    d = ImageDraw.Draw(img)
    xadrez = Image.new('RGB', (cw, ch), (200, 200, 200))
    dx = ImageDraw.Draw(xadrez)
    for i in range(0, cw, 16):
        for j in range(0, ch, 16):
            if (i // 16 + j // 16) % 2:
                dx.rectangle([i, j, i + 15, j + 15], fill=(235, 235, 235))
    for k, it in enumerate(itens):
        x, y = 6 + (k % COLS) * (cw + 6), 6 + (k // COLS) * (ch + cab + 6)
        im = Image.open(os.path.join(RAIZ, it['previa'])).convert('RGBA')
        im.thumbnail((cw, ch))
        base = xadrez.copy() if it['uso_auto'] == 'recorte' else Image.new('RGB', (cw, ch), (30, 30, 30))
        base.paste(im, ((cw - im.size[0]) // 2, (ch - im.size[1]) // 2), im)
        img.paste(base, (x, y + cab))
        d.rectangle([x, y, x + cw, y + cab - 2], fill=(0, 0, 0))
        d.text((x + 5, y + 3), it['id'] + ('  vídeo' if it['uso_auto'] == 'video' else ''), font=f, fill=(255, 220, 0))
    img.save(destino, quality=82)


def main():
    os.makedirs(SAIDA, exist_ok=True)
    for f in glob.glob(os.path.join(SAIDA, '*')):
        os.remove(f)
    its = selecionar()
    por_folha = COLS * LINS
    por_lote = por_folha * FOLHAS
    lotes = [its[i:i + por_lote] for i in range(0, len(its), por_lote)]
    for k, bloco in enumerate(lotes, 1):
        nome = 'lote-%03d' % k
        figs = []
        for j in range(0, len(bloco), por_folha):
            caminho = os.path.join(SAIDA, '%s-%d.jpg' % (nome, j // por_folha + 1))
            folha(bloco[j:j + por_folha], caminho)
            figs.append(os.path.relpath(caminho, RAIZ))
        json.dump({'lote': nome, 'imagens': figs, 'saida': 'dados/_trabalho/midia/%s.json' % nome,
                   'itens': [{'id': x['id'], 'uso_auto': x['uso_auto'], 'w': x['w'], 'h': x['h']} for x in bloco]},
                  open(os.path.join(SAIDA, nome + '.json'), 'w'), ensure_ascii=False)
    print('mídias', len(its), 'lotes', len(lotes))


if __name__ == '__main__':
    main()
