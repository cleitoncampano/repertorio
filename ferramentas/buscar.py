#!/usr/bin/env python3
"""Busca na biblioteca (arquivos, slides, referências externas e mídia) e, se pedido, monta uma prancha com os resultados.

Exemplos:
  python3 -I ferramentas/buscar.py "abertura impactante" -i ABRIR --forca 4
  python3 -I ferramentas/buscar.py -t metafora-visual,escala-impossivel --doc referencia --prancha
  python3 -I ferramentas/buscar.py "número grande" -i PROVAR -e escuro -n 8 --prancha
  python3 -I ferramentas/buscar.py -m zoom-mergulho --doc arquivo --tipo efeito
  python3 -I ferramentas/buscar.py "astronauta" --doc midia --uso recorte --prancha
  python3 -I ferramentas/buscar.py --ver 284-reel-cerebro-3d
  python3 -I ferramentas/buscar.py --vocab

Filtros: vírgula = qualquer um dos valores; filtros diferentes = todos ao mesmo tempo.
Slides marcados como "antes" (a versão comum antes do efeito) ficam fora, a não ser com --antes.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDICE = os.path.join(RAIZ, 'dados', 'indice.jsonl')
SAIDA = os.path.join(os.path.expanduser(os.getenv('REPERTORIO_HOME', os.path.join(RAIZ, 'app', '.runtime'))), 'search-previews')


def norm(s):
    s = unicodedata.normalize('NFKD', str(s or '')).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9%]+', ' ', s).strip()


PARADAS = set('a o e de da do das dos em no na nos nas um uma uns umas para por com que se ao aos as os the of and'.split())


def termos(q):
    return [t for t in norm(q).split() if t not in PARADAS and len(t) > 1]


def lista(v):
    return [x.strip() for x in v.split(',') if x.strip()] if v else []


def casa_termo(t, palavras, texto):
    if t in palavras:
        return 1.0
    if len(t) >= 5 and any(p.startswith(t[:max(5, len(t) - 2)]) for p in palavras):
        return 0.7
    return 0.5 if t in texto else 0.0


def pontuar(doc, q, filtros):
    for campo, valores in filtros.items():
        if not valores:
            continue
        v = doc.get(campo)
        v = v if isinstance(v, list) else [v]
        if not set(valores) & set(x for x in v if x is not None):
            return None
    s = 0.0
    if q:
        texto = doc.get('_t') or norm(doc.get('texto', ''))
        palavras = set(texto.split())
        achados = [casa_termo(t, palavras, texto) for t in q]
        # com 3 ou mais termos, exige que pelo menos metade apareça (evita centenas de resultados soltos)
        if not any(achados) or (len(q) >= 3 and sum(1 for x in achados if x) < len(q) / 2):
            return None
        s += 4 * sum(achados) / len(q)
    s += 0.6 * (doc.get('forca') or 3)
    if doc.get('destaque'):
        s += 0.8
    return s


def carregar():
    if not os.path.exists(INDICE):
        sys.exit('Índice não encontrado. Rode antes: python3 -I ferramentas/construir/montar.py')
    with open(INDICE) as f:
        return [json.loads(l) for l in f]


def legenda(doc):
    t = doc.get('nota') or doc.get('ideia') or doc.get('o_que') or doc.get('resumo') or ''
    return t


def quebrar(txt, fonte, larg, d, linhas=2):
    palavras, out, atual = txt.split(), [], ''
    for p in palavras:
        teste = (atual + ' ' + p).strip()
        if d.textlength(teste, font=fonte) <= larg:
            atual = teste
        else:
            out.append(atual); atual = p
            if len(out) == linhas:
                break
    if len(out) < linhas and atual:
        out.append(atual)
    if len(out) == linhas and ' '.join(out) != txt.strip():
        out[-1] = out[-1].rstrip('.,;: ') + '...'
    return out[:linhas]


def prancha(res, nome):
    from PIL import Image, ImageDraw, ImageFont
    os.makedirs(SAIDA, exist_ok=True)
    antigas = sorted((os.path.join(SAIDA, f) for f in os.listdir(SAIDA)), key=os.path.getmtime)
    for f in antigas[:-40]:
        os.remove(f)
    caminhos = [(i + 1, d) for i, d in enumerate(res) if d.get('imagem') and os.path.exists(os.path.join(RAIZ, d['imagem']))]
    if not caminhos:
        return None
    cols = 3 if len(caminhos) > 4 else 2 if len(caminhos) > 1 else 1
    cw = (1560 - 12 * (cols + 1)) // cols
    ch = round(cw * 9 / 16)
    cab = 86
    linhas = -(-len(caminhos) // cols)
    img = Image.new('RGB', (1560, 12 + linhas * (ch + cab + 12)), (24, 24, 24))
    d = ImageDraw.Draw(img)
    try:
        f = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 22)
        f2 = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 19)
    except OSError:
        f = f2 = ImageFont.load_default()
    for k, (n, doc) in enumerate(caminhos):
        x, y = 12 + (k % cols) * (cw + 12), 12 + (k // cols) * (ch + cab + 12)
        im = Image.open(os.path.join(RAIZ, doc['imagem'])).convert('RGBA')
        im.thumbnail((cw, ch))
        fundo = Image.new('RGB', (cw, ch), (44, 44, 44))
        fundo.paste(im, ((cw - im.size[0]) // 2, (ch - im.size[1]) // 2), im)
        img.paste(fundo, (x, y))
        d.rectangle([x, y, x + 40, y + 30], fill=(220, 60, 20))
        d.text((x + 8, y + 4), str(n), font=f, fill=(255, 255, 255))
        d.text((x, y + ch + 6), doc['id'][:60], font=f, fill=(240, 240, 240))
        for j, l in enumerate(quebrar(legenda(doc), f2, cw, d)):
            d.text((x, y + ch + 34 + j * 23), l, font=f2, fill=(185, 185, 185))
    caminho = os.path.join(SAIDA, nome + '.jpg')
    img.save(caminho, quality=84)
    return os.path.relpath(caminho, RAIZ)


def mostrar(doc, n):
    tag = {'arquivo': doc.get('tipo', 'arquivo'), 'slide': 'slide', 'referencia': 'ref', 'midia': 'mídia'}.get(doc['doc'], doc['doc'])
    linha = '%2d. [%s] %s' % (n, tag, doc['id'])
    if doc.get('forca'):
        linha += '  força %s' % doc['forca']
    marcas = (doc.get('intencoes') or []) + (doc.get('tecnicas') or [])[:4] + (doc.get('movimento') or [])[:2]
    if marcas:
        linha += '  ' + ' '.join(marcas)
    print(linha)
    for campo in ('nota', 'ideia', 'resumo', 'o_que'):
        if doc.get(campo):
            print('    ' + doc[campo])
            break
    if doc['doc'] in ('arquivo', 'referencia') and doc.get('como_levar_para_slide'):
        print('    no slide: ' + doc['como_levar_para_slide'])
    if doc['doc'] == 'slide' and doc.get('ideia_arquivo'):
        print('    ideia do arquivo de origem: ' + doc['ideia_arquivo'])
    if doc['doc'] == 'slide' and doc.get('morph'):
        print('    movimento ao entrar: ' + doc['morph'])
    if doc.get('terceiros'):
        print('    atenção: marca, celebridade ou obra de terceiros; use só como referência')
    if doc.get('imagem'):
        print('    ver: ' + doc['imagem'])
    if doc.get('fonte_extra'):
        print('    ' + doc['fonte_extra'])


def ver(idx, alvo):
    docs = [d for d in idx if d['id'] == alvo]
    if not docs:
        sys.exit('Não achei %s' % alvo)
    d = dict(docs[0])
    d.pop('_t', None); d.pop('texto', None)
    print(json.dumps(d, ensure_ascii=False, indent=1))
    if d['doc'] == 'arquivo':
        for s in sorted((x for x in idx if x['doc'] == 'slide' and x.get('deck') == alvo), key=lambda x: x['n']):
            print('  slide %2d %-10s %s  %s' % (s['n'], s.get('intencao'), ','.join(s.get('tecnicas', [])), s.get('nota', '')))


def vocab():
    v = json.load(open(os.path.join(RAIZ, 'dados', 'vocabulario.json')))
    for chave in ('intencoes', 'operacoes', 'tecnicas', 'movimentos'):
        print('\n## %s' % chave)
        for it in v[chave]['itens']:
            extra = ' (%s)' % it['operacao'] if 'operacao' in it else ''
            print('%-24s %s%s' % (it['id'], it['def'], extra))
    print('\n## esteticas\n' + ', '.join(v['esteticas']['itens']))
    print('\n## tons\n' + ', '.join(v['tons']['itens']))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('q', nargs='*', help='texto livre')
    ap.add_argument('-i', '--intencao', help='ABRIR, IMPACTAR, PROVAR...')
    ap.add_argument('-t', '--tecnica')
    ap.add_argument('-m', '--movimento')
    ap.add_argument('-e', '--estetica')
    ap.add_argument('--tom')
    ap.add_argument('--doc', help='arquivo, slide, referencia, midia')
    ap.add_argument('--tipo', help='modelo, efeito, componente (arquivos e slides); capa, anuncio, frame... (referências)')
    ap.add_argument('--uso', help='mídia: recorte, foto, fundo, icone, textura, ilustracao, mockup, video, 3d...')
    ap.add_argument('--proporcao', help='16:9, 9:16, 1:1...')
    ap.add_argument('--forca', type=int, default=0, help='força mínima (1 a 5)')
    ap.add_argument('--livre', action='store_true', help='mídia: só o que não é de terceiros (sem marca, celebridade ou obra protegida)')
    ap.add_argument('-n', type=int, default=12)
    ap.add_argument('--prancha', action='store_true', help='monta uma imagem única com os resultados')
    ap.add_argument('--antes', action='store_true', help='inclui slides "antes"')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--ver', help='mostra a ficha completa de um id')
    ap.add_argument('--vocab', action='store_true', help='lista o vocabulário')
    a = ap.parse_args()
    if a.vocab:
        return vocab()
    idx = carregar()
    if a.ver:
        return ver(idx, a.ver)
    q = termos(' '.join(a.q))
    intencoes = lista(a.intencao and a.intencao.upper())
    filtros = {'intencoes': intencoes, 'tecnicas': lista(a.tecnica), 'movimento': lista(a.movimento),
               'estetica': lista(a.estetica), 'tom': lista(a.tom), 'doc': lista(a.doc), 'tipo': lista(a.tipo),
               'uso': lista(a.uso), 'proporcao': lista(a.proporcao)}
    res = []
    for d in idx:
        if d.get('antes') and not a.antes:
            continue
        if a.forca and (d.get('forca') or 0) < a.forca:
            continue
        if a.livre and d['doc'] == 'midia' and d.get('terceiros') is not False:
            continue
        s = pontuar(d, q, filtros)
        if s is not None:
            res.append((s, d))
    aviso = ''
    if not res and q and any(filtros.values()):
        for d in idx:
            if d.get('antes') and not a.antes:
                continue
            if a.forca and (d.get('forca') or 0) < a.forca:
                continue
            s = pontuar(d, [], filtros)
            if s is not None:
                res.append((s, d))
        aviso = 'Nada casou com o texto dentro desses filtros; mostrando só pelos filtros (tente outras palavras).'
    res.sort(key=lambda x: -x[0])
    total = len(res)
    res = [d for _, d in res[:a.n]]
    if a.json:
        for d in res:
            d = dict(d); d.pop('_t', None)
            print(json.dumps(d, ensure_ascii=False))
        return
    if aviso:
        print(aviso)
    print('%d resultado(s), mostrando os %d melhores' % (total, len(res)))
    for n, d in enumerate(res, 1):
        mostrar(d, n)
    if a.prancha and res:
        nome = hashlib.sha1(' '.join(sys.argv[1:]).encode()).hexdigest()[:10]
        p = prancha(res, nome)
        if p:
            print('\nPrancha dos resultados (abra esta imagem): ' + p)


if __name__ == '__main__':
    main()
