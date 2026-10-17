#!/usr/bin/env python3
"""Empacota os dados do mapa visual (_catalogo/mapa/): os mesmos campos e o mesmo texto de busca que o modelo usa
(dados/indice.jsonl e dados/fichas.jsonl), mais miniaturas pequenas para desenhar o grafo.
Saída: _catalogo/mapa/dados.js, _catalogo/mapa/m/<id>.jpg (miniatura) e _catalogo/mapa/r/<id>.jpg (referência maior)
Uso, da raiz do projeto:  python3 -I ferramentas/construir/mapa.py
"""
import json
import os
from concurrent.futures import ThreadPoolExecutor

from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SAIDA = os.path.join(RAIZ, '_catalogo', 'mapa')


def jsonl(p):
    return [json.loads(l) for l in open(os.path.join(RAIZ, p))]


def miniatura(origem, destino, largura):
    if os.path.exists(destino):
        return Image.open(destino).size
    im = Image.open(origem).convert('RGB')
    im.thumbnail((largura, largura))
    im.save(destino, quality=78, optimize=True)
    return im.size


def main():
    os.makedirs(os.path.join(SAIDA, 'm'), exist_ok=True)
    os.makedirs(os.path.join(SAIDA, 'r'), exist_ok=True)
    voc = json.load(open(os.path.join(RAIZ, 'dados', 'vocabulario.json')))
    fichas = {f['id']: f for f in jsonl('dados/fichas.jsonl')}
    indice = jsonl('dados/indice.jsonl')
    oficiais = {t['id'] for t in voc['tecnicas']['itens']}

    itens, slides, tarefas = [], [], []
    for d in indice:
        if d['doc'] == 'arquivo':
            f = fichas.get(d['id'], {})
            antes = set(f.get('antes', []))
            ns = [s['n'] for s in f.get('slides', []) if s['n'] not in antes and s.get('intencao') not in ('ANTES', 'OCULTO')]
            capa = next((n for n in f.get('destaques', []) if n in ns), ns[0] if ns else 1)
            origem = os.path.join(RAIZ, '_catalogo', 'miniaturas', d['id'], '%02d.jpg' % capa)
            tarefas.append((origem, os.path.join(SAIDA, 'm', d['id'] + '.jpg'), 220, d['id']))
            itens.append({'id': d['id'], 'k': 'a', 'ti': d.get('titulo'), 'tp': d.get('tipo'), 'fo': d.get('forca'),
                          'it': d.get('intencoes') or [], 'te': [t for t in d.get('tecnicas') or [] if t in oficiais],
                          'mo': d.get('movimento') or [], 'es': d.get('estetica') or [], 'to': d.get('tom') or [],
                          're': f.get('resumo'), 'ide': f.get('ideia'), 'co': f.get('como_funciona'), 'ht': f.get('html'),
                          'bp': f.get('bom_para') or [], 'cu': f.get('cuidados'), 'gr': d.get('grupos') or [],
                          'ar': os.path.basename(d.get('arquivo') or ''), 'pr': '../pranchas/%s.jpg' % d['id'],
                          'cp': capa, 'antes': sorted(antes), 't': d.get('_t', '')})
        elif d['doc'] == 'referencia':
            origem = os.path.join(RAIZ, d['arquivo'])
            tarefas.append((origem, os.path.join(SAIDA, 'm', d['id'] + '.jpg'), 220, d['id']))
            tarefas.append((origem, os.path.join(SAIDA, 'r', d['id'] + '.jpg'), 900, None))
            itens.append({'id': d['id'], 'k': 'r', 'ti': d.get('fonte'), 'tp': d.get('tipo'), 'fo': d.get('forca'),
                          'it': d.get('intencoes') or [], 'te': [t for t in d.get('tecnicas') or [] if t in oficiais],
                          'mo': [], 'es': d.get('estetica') or [], 'to': d.get('tom') or [],
                          're': d.get('o_que'), 'ide': d.get('ideia'), 'co': d.get('como_levar_para_slide'), 'fn': d.get('fonte'),
                          'orig': d.get('arquivo'), 't': d.get('_t', '')})
        elif d['doc'] == 'slide' and not d.get('antes'):
            slides.append([d['deck'], d['n'], d.get('intencao'), [t for t in d.get('tecnicas') or [] if t in oficiais],
                           d.get('nota') or '', d.get('forca') or 3, 1 if d.get('destaque') else 0, d.get('_t', ''),
                           d.get('morph') or ''])
    tamanhos = {}
    with ThreadPoolExecutor(8) as ex:
        for tam, (_, _, _, iid) in zip(ex.map(lambda t: miniatura(*t[:3]), tarefas), tarefas):
            if iid:
                tamanhos[iid] = tam
    for it in itens:
        w, h = tamanhos.get(it['id'], (220, 124))
        it['ra'] = round(w / float(h), 3)
    dados = {'voc': {k: voc[k]['itens'] for k in ('intencoes', 'operacoes', 'pistas', 'tecnicas', 'movimentos')},
             'esteticas': voc['esteticas']['itens'], 'itens': itens, 'slides': slides}
    with open(os.path.join(SAIDA, 'dados.js'), 'w') as f:
        f.write('window.MAPA = ' + json.dumps(dados, ensure_ascii=False, separators=(',', ':')) + ';\n')
    print('itens', len(itens), '| slides', len(slides), '| dados.js %.1f MB' % (os.path.getsize(os.path.join(SAIDA, 'dados.js')) / 1e6))


if __name__ == '__main__':
    main()
