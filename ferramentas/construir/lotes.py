#!/usr/bin/env python3
"""Divide os pacotes em lotes para a escrita das fichas.
Modelos completos vão de 2 em 2 (cada um com a sua prancha); os demais são empilhados numa imagem só por lote.
Saída: dados/_trabalho/lotes/lote-NNN.json (+ lote-NNN.jpg quando empilhado)
Uso, da raiz do projeto:  python3 -I ferramentas/construir/lotes.py
"""
import glob
import json
import os

from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TRAB = os.path.join(RAIZ, 'dados', '_trabalho')
SAIDA = os.path.join(TRAB, 'lotes')
GRANDES = {'Templates completos', 'Templates temáticos', 'Canva (PDF)'}
ALTURA_MAX, POR_LOTE = 1700, 5
FEITOS = {'002-26-0102-cinema', '284-reel-cerebro-3d'}


def main():
    os.makedirs(SAIDA, exist_ok=True)
    for f in glob.glob(os.path.join(SAIDA, 'lote-*')):
        os.remove(f)
    pacs = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(TRAB, 'pacotes', '*.json')))]
    pacs = [p for p in pacs if p['id'] not in FEITOS]
    grandes = [p for p in pacs if GRANDES & set(p['grupos']) or len(p['pranchas']) > 1]
    pequenos = [p for p in pacs if p not in grandes]
    pequenos.sort(key=lambda p: (sorted(p['grupos'])[0], p['id']))
    lotes = []
    for i in range(0, len(grandes), 2):
        par = grandes[i:i + 2]
        lotes.append({'pacotes': par, 'imagens': [im for p in par for im in p['pranchas']]})
    atual, altura = [], 0
    for p in pequenos:
        h = Image.open(os.path.join(RAIZ, p['pranchas'][0])).size[1]
        if atual and (altura + h > ALTURA_MAX or len(atual) >= POR_LOTE):
            lotes.append({'pacotes': atual}); atual, altura = [], 0
        atual.append(p); altura += h
    if atual:
        lotes.append({'pacotes': atual})
    for k, lote in enumerate(lotes, 1):
        nome = 'lote-%03d' % k
        if 'imagens' not in lote:
            ims = [Image.open(os.path.join(RAIZ, p['pranchas'][0])) for p in lote['pacotes']]
            alvo = Image.new('RGB', (max(i.size[0] for i in ims), sum(i.size[1] for i in ims) + 6 * (len(ims) - 1)), (255, 255, 255))
            y = 0
            for im in ims:
                alvo.paste(im, (0, y)); y += im.size[1] + 6
            alvo.save(os.path.join(SAIDA, nome + '.jpg'), quality=82, optimize=True)
            lote['imagens'] = ['dados/_trabalho/lotes/%s.jpg' % nome]
        for p in lote['pacotes']:
            p.pop('pranchas', None)
        lote = {'lote': nome, 'imagens': lote['imagens'], 'saida': 'dados/_trabalho/fichas/%s.json' % nome, 'pacotes': lote['pacotes']}
        json.dump(lote, open(os.path.join(SAIDA, nome + '.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
    print('lotes', len(lotes), 'grandes', -(-len(grandes) // 2), 'itens', len(pacs))


if __name__ == '__main__':
    main()
