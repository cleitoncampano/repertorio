#!/usr/bin/env python3
"""Confere uma apresentação HTML feita com o motor do kit: fotografa os slides, monta pranchas e aponta problemas.

Uso: python3 -I ferramentas/ver.py apresentacao.html [--passos] [--transicoes] [--pdf] [--saida pasta]

Gera em <pasta> (padrão: <apresentacao>_ver/):
  prancha.jpg              cada slide no estado final (tudo revelado)
  prancha-passos.jpg       com --passos: cada clique dos slides que têm revelação
  prancha-transicoes.jpg   com --transicoes: o meio de cada passagem de slide (para ver o Morph)
  apresentacao.pdf         com --pdf
e imprime avisos: texto menor que 24 px, texto saindo do slide, data-m repetido, erros do navegador.
Precisa do Playwright para Python com Chromium (pip install playwright && playwright install chromium).
"""
import argparse
import asyncio
import os

from PIL import Image, ImageDraw, ImageFont

CHECAGEM = """() => {
  const s = document.querySelector('.slide.ativo'), pr = document.querySelector('.palco').getBoundingClientRect();
  const out = [];
  s.querySelectorAll('*').forEach((el) => {
    if (el.closest('.notas')) return;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) return;
    const txt = [...el.childNodes].filter((n) => n.nodeType === 3).map((n) => n.textContent.trim()).join(' ').trim();
    if (!txt) return;
    const fs = parseFloat(cs.fontSize);
    if (fs < 24) out.push('texto pequeno (' + Math.round(fs) + ' px): "' + txt.slice(0, 50) + '"');
    if (el.closest('.fora-esq,.fora-dir,.fora-cima,.fora-baixo')) return;
    const r = el.getBoundingClientRect();
    if (r.right > pr.right + 3 || r.left < pr.left - 3 || r.bottom > pr.bottom + 3 || r.top < pr.top - 3)
      out.push('texto passando da borda (de propósito?): "' + txt.slice(0, 50) + '"');
  });
  return out;
}"""


def fonte(t):
    try:
        return ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', t)
    except OSError:
        return ImageFont.load_default()


def prancha(fotos, destino, cols=None):
    if not fotos:
        return
    cols = cols or (4 if len(fotos) > 6 else 3)
    cw = (1560 - 8 * (cols + 1)) // cols
    w0, h0 = Image.open(fotos[0][0]).size
    ch = round(cw * h0 / w0)
    linhas = -(-len(fotos) // cols)
    img = Image.new('RGB', (1560, 8 + linhas * (ch + 8)), (24, 24, 24))
    d = ImageDraw.Draw(img)
    f = fonte(18)
    for i, (p, rot) in enumerate(fotos):
        x, y = 8 + (i % cols) * (cw + 8), 8 + (i // cols) * (ch + 8)
        img.paste(Image.open(p).convert('RGB').resize((cw, ch)), (x, y))
        tw = d.textlength(rot, font=f)
        d.rectangle([x, y, x + tw + 12, y + 24], fill=(0, 0, 0))
        d.text((x + 6, y + 3), rot, font=f, fill=(255, 255, 255))
    img.save(destino, quality=84)


async def rodar(html, pasta, a):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        nav = await p.chromium.launch()
        pg = await nav.new_page(viewport={'width': 1920, 'height': 1080})
        erros = []
        pg.on('pageerror', lambda e: erros.append('erro na página: ' + str(e)))
        pg.on('console', lambda m: erros.append(m.text) if m.type in ('error', 'warning') else None)
        await pg.goto('file://' + os.path.abspath(html))
        await pg.wait_for_timeout(700)
        total = await pg.evaluate('window.motor ? motor.total : 0')
        if not total:
            raise SystemExit('Não achei o motor (window.motor). A página usa kit/motor.js?')
        finais, passos_f, trans_f, avisos = [], [], [], {}
        # 1) estado final de cada slide + checagens + passos
        await pg.evaluate("document.documentElement.style.setProperty('--dur','1ms')")
        for n in range(1, total + 1):
            await pg.evaluate('motor.ir(%d)' % n)
            await pg.wait_for_timeout(300)
            if a.passos:
                ps = await pg.evaluate('motor.passos')
                if ps:
                    await pg.wait_for_timeout(1200)
                    cam = os.path.join(pasta, 'passo-%02d-0.png' % n)
                    await pg.screenshot(path=cam)
                    passos_f.append((cam, '%d.0' % n))
                    for k in range(len(ps)):
                        await pg.evaluate('motor.avancar()')
                        await pg.wait_for_timeout(1300)
                        cam = os.path.join(pasta, 'passo-%02d-%d.png' % (n, k + 1))
                        await pg.screenshot(path=cam)
                        passos_f.append((cam, '%d.%d' % (n, k + 1)))
            await pg.evaluate('motor.revelarTudo()')
            await pg.wait_for_timeout(1500)
            cam = os.path.join(pasta, 'slide-%02d.png' % n)
            await pg.screenshot(path=cam)
            finais.append((cam, str(n)))
            av = await pg.evaluate(CHECAGEM)
            if av:
                avisos[n] = av
        # 2) meio das transições, na duração real
        if a.transicoes:
            await pg.goto('file://' + os.path.abspath(html) + '#1')
            await pg.wait_for_timeout(900)
            # desacelera as passagens só para a foto pegar o meio do movimento
            await pg.add_style_tag(content=':root { --dur: 3600ms !important; }')
            for n in range(2, total + 1):
                await pg.evaluate('motor.ir(%d)' % (n - 1))
                await pg.wait_for_timeout(4000)
                await pg.evaluate('motor.revelarTudo()')
                await pg.wait_for_timeout(600)
                await pg.evaluate('() => { motor.ir(%d); }' % n)  # dispara sem esperar a passagem terminar
                await pg.wait_for_timeout(1100)
                cam = os.path.join(pasta, 'trans-%02d.png' % n)
                await pg.screenshot(path=cam)
                trans_f.append((cam, '%d > %d' % (n - 1, n)))
                await pg.wait_for_timeout(3600)
        if a.pdf:
            await pg.emulate_media(media='print')
            await pg.pdf(path=os.path.join(pasta, 'apresentacao.pdf'), prefer_css_page_size=True, print_background=True)
        await nav.close()
        return finais, passos_f, trans_f, avisos, erros


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('html')
    ap.add_argument('--passos', action='store_true', help='fotografa cada clique dos slides com revelação')
    ap.add_argument('--transicoes', action='store_true', help='fotografa o meio de cada passagem de slide')
    ap.add_argument('--pdf', action='store_true')
    ap.add_argument('--saida')
    a = ap.parse_args()
    pasta = a.saida or os.path.splitext(a.html)[0] + '_ver'
    os.makedirs(pasta, exist_ok=True)
    finais, passos_f, trans_f, avisos, erros = asyncio.run(rodar(a.html, pasta, a))
    prancha(finais, os.path.join(pasta, 'prancha.jpg'))
    print('%d slides em %s' % (len(finais), pasta))
    print('prancha: ' + os.path.join(pasta, 'prancha.jpg'))
    if passos_f:
        prancha(passos_f, os.path.join(pasta, 'prancha-passos.jpg'), cols=5)
        print('cliques: ' + os.path.join(pasta, 'prancha-passos.jpg'))
    if trans_f:
        prancha(trans_f, os.path.join(pasta, 'prancha-transicoes.jpg'), cols=5)
        print('transições: ' + os.path.join(pasta, 'prancha-transicoes.jpg'))
    if a.pdf:
        print('pdf: ' + os.path.join(pasta, 'apresentacao.pdf'))
    if avisos:
        print('\nAvisos por slide:')
        for n, av in avisos.items():
            for x in sorted(set(av))[:6]:
                print('  slide %d: %s' % (n, x))
    if erros:
        print('\nAvisos do navegador:\n  ' + '\n  '.join(sorted(set(erros))[:10]))


if __name__ == '__main__':
    main()
