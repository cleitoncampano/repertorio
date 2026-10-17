#!/usr/bin/env python3
"""Prepara as imagens da _referencias (capas, anúncios, ativações, aberturas, frames de vídeo) para a escrita das fichas:
pranchas de 6 imagens numeradas e lotes com 3 pranchas.
Saída: dados/_trabalho/ref-lotes/lote-NNN.json + .jpg
Uso, da raiz do projeto:  python3 -I ferramentas/construir/lotes_referencias.py
"""
import glob
import json
import os
import re

from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REF = os.path.join(RAIZ, '_referencias')
SAIDA = os.path.join(RAIZ, 'dados', '_trabalho', 'ref-lotes')
FONTE = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
FONTES = {
    '03_jason_murray_portfolio': ('Jason Murray (portfólio)', 'sites/03_jason_murray_portfolio/ESTUDO-COMPLETO.md'),
    '04_manifesto_writing': ('Manifesto Writing', 'sites/04_manifesto_writing/ESTUDO-COMPLETO.md'),
    '05_dave_dye_pinterest': ('Dave Dye (anúncios)', 'sites/05_dave_dye_pinterest/ESTUDO-COMPLETO.md'),
    '06_eyecannndy': ('Eyecannndy (técnicas de câmera e edição)', 'sites/06_eyecannndy/ESTUDO-COMPLETO.md'),
    '08_art_of_the_title': ('Art of the Title (aberturas de filmes)', None),
    '09_coverjunkie': ('Coverjunkie (capas de revista)', 'sites/09_coverjunkie/ESTUDO-COMPLETO.md'),
    '11_activation_ideas': ('Activation Ideas (ativações)', 'sites/11_activation_ideas/ESTUDO-COMPLETO.md'),
}
POR_FOLHA, FOLHAS_POR_LOTE = 6, 3


def imagens():
    out = []
    for pasta, (nome, estudo) in FONTES.items():
        for p in sorted(glob.glob(os.path.join(REF, 'sites', pasta, 'imagens', '*'))):
            b = os.path.basename(p)
            if not b.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')) or b.startswith('00_') or '_ui_' in b:
                continue
            out.append({'arquivo': os.path.relpath(p, RAIZ), 'fonte': nome, 'estudo': '_referencias/' + estudo if estudo else None,
                        'id': 'ref-%s-%s' % (pasta[:2], re.sub(r'[^a-z0-9]+', '-', os.path.splitext(b)[0].lower()).strip('-'))})
    for d in sorted(glob.glob(os.path.join(REF, 'videos', '*'))):
        info = json.load(open(os.path.join(d, 'video.info.json')))
        nome = '%s (vídeo: %s)' % (info.get('uploader') or info.get('channel'), info.get('title'))
        for p in sorted(glob.glob(os.path.join(d, 'frames_curados', '*.jpg'))):
            b = os.path.basename(p)
            out.append({'arquivo': os.path.relpath(p, RAIZ), 'fonte': nome, 'estudo': os.path.relpath(os.path.join(d, 'ESTUDO-COMPLETO.md'), RAIZ),
                        'id': 'ref-v-%s-%s' % (os.path.basename(d)[:6].lower(), re.sub(r'[^a-z0-9]+', '-', os.path.splitext(b)[0].lower()).strip('-'))})
    return out


def folha(itens, destino, base_n):
    cw, ch, cab = 510, 400, 30
    f = ImageFont.truetype(FONTE, 18)
    img = Image.new('RGB', (3 * cw + 4 * 8, 2 * (ch + cab) + 3 * 8), (24, 24, 24))
    d = ImageDraw.Draw(img)
    for k, it in enumerate(itens):
        x, y = 8 + (k % 3) * (cw + 8), 8 + (k // 3) * (ch + cab + 8)
        im = Image.open(os.path.join(RAIZ, it['arquivo'])).convert('RGB')
        im.thumbnail((cw, ch))
        img.paste(im, (x + (cw - im.size[0]) // 2, y + cab + (ch - im.size[1]) // 2))
        d.rectangle([x, y, x + cw, y + cab - 4], fill=(0, 0, 0))
        d.text((x + 6, y + 4), '%d  %s' % (base_n + k, it['id'][:44]), font=f, fill=(255, 220, 0))
    img.save(destino, quality=84)


def main():
    os.makedirs(SAIDA, exist_ok=True)
    for f in glob.glob(os.path.join(SAIDA, '*')):
        os.remove(f)
    its = imagens()
    blocos = [its[i:i + POR_FOLHA * FOLHAS_POR_LOTE] for i in range(0, len(its), POR_FOLHA * FOLHAS_POR_LOTE)]
    for k, bloco in enumerate(blocos, 1):
        nome = 'lote-%03d' % k
        figs = []
        for j in range(0, len(bloco), POR_FOLHA):
            caminho = os.path.join(SAIDA, '%s-%d.jpg' % (nome, j // POR_FOLHA + 1))
            folha(bloco[j:j + POR_FOLHA], caminho, j + 1)
            figs.append(os.path.relpath(caminho, RAIZ))
        for n, it in enumerate(bloco, 1):
            it['n'] = n
        estudos = sorted({it['estudo'] for it in bloco if it['estudo']})
        json.dump({'lote': nome, 'imagens': figs, 'estudos': estudos, 'saida': 'dados/_trabalho/referencias/%s.json' % nome, 'itens': bloco},
                  open(os.path.join(SAIDA, nome + '.json'), 'w'), ensure_ascii=False, indent=1)
    print('referências', len(its), 'lotes', len(blocos))


if __name__ == '__main__':
    main()
