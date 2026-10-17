#!/usr/bin/env python3
"""Recebe o roteiro de slides e devolve, para cada linha, as melhores referências da biblioteca numa prancha só.

Formato do roteiro (o mesmo de biblioteca/principios/narrativa.md, seção 8), uma linha por slide:
  n | INTENÇÃO | batida (o que a plateia entende) | conector | fala | visual
Linhas de tabela markdown com essas colunas também servem. Só as duas primeiras colunas e a batida são obrigatórias.

Uso: python3 -I ferramentas/roteiro.py roteiro.md [--saida pasta] [--forca 4] [-n 4]
Gera em <pasta> (padrão: _saida/roteiro/): uma prancha por slide (slide-NN.jpg) e referencias.md com ids, notas e ideias.
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import buscar  # noqa: E402

RAIZ = buscar.RAIZ
VOC = json.load(open(os.path.join(RAIZ, 'dados', 'vocabulario.json')))
INTENCOES = {i['id'] for i in VOC['intencoes']['itens']}


def exibir(caminho):
    c = os.path.normpath(os.path.join(RAIZ, caminho)) if caminho else ''
    return os.path.relpath(c, RAIZ) if c.startswith(RAIZ + os.sep) else c


def ler_roteiro(caminho):
    linhas = []
    for bruta in open(caminho, encoding='utf8'):
        cols = [c.strip() for c in bruta.strip().strip('|').split('|')]
        if len(cols) < 3 or not re.fullmatch(r'\d+', cols[0] or ''):
            continue
        intencao = cols[1].upper().strip('` ')
        if intencao not in INTENCOES:
            continue
        linhas.append({'n': int(cols[0]), 'intencao': intencao, 'batida': cols[2], 'visual': cols[5] if len(cols) > 5 else ''})
    return linhas


def melhores(idx, intencao, texto, doc, forca, n):
    q = buscar.termos(texto)
    filtros = {'intencoes': [intencao], 'doc': [doc]}
    res = []
    for d in idx:
        if d.get('antes') or (forca and (d.get('forca') or 0) < forca):
            continue
        s = buscar.pontuar(d, q, filtros)
        if s is not None:
            res.append((s, d))
    if len(res) < n:  # texto não casou: completa só pela intenção
        vistos = {d['id'] for _, d in res}
        for d in idx:
            if d['id'] in vistos or d.get('antes') or (forca and (d.get('forca') or 0) < forca):
                continue
            s = buscar.pontuar(d, [], filtros)
            if s is not None:
                res.append((s - 3, d))
    res.sort(key=lambda x: -x[0])
    return [d for _, d in res[:n]]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('roteiro')
    ap.add_argument('--saida', default=os.path.join(RAIZ, '_saida', 'roteiro'))
    ap.add_argument('--forca', type=int, default=4)
    ap.add_argument('-n', type=int, default=4, help='slides do PPTRETA por linha (mais 2 referências externas)')
    a = ap.parse_args()
    linhas = ler_roteiro(a.roteiro)
    if not linhas:
        sys.exit('Não achei linhas no formato "n | INTENÇÃO | batida | ...". Veja a seção 8 de biblioteca/principios/narrativa.md.')
    os.makedirs(a.saida, exist_ok=True)
    idx = buscar.carregar()
    buscar.SAIDA = a.saida
    md = ['# Referências por slide', '', 'Roteiro: `%s`' % a.roteiro, '']
    for l in linhas:
        texto = l['batida'] + ' ' + l['visual']
        sel = melhores(idx, l['intencao'], texto, 'slide', a.forca, a.n) + melhores(idx, l['intencao'], texto, 'referencia', 3, 2)
        p = buscar.prancha(sel, 'slide-%02d' % l['n'])
        md += ['## Slide %d · %s' % (l['n'], l['intencao']), '', l['batida'], '', 'Prancha: `%s`' % exibir(p), '']
        for k, d in enumerate(sel, 1):
            ideia = d.get('ideia_arquivo') if d['doc'] == 'slide' else d.get('ideia')
            md.append('%d. **%s** (%s): %s  ' % (k, d['id'], ', '.join((d.get('tecnicas') or [])[:3]), d.get('nota') or d.get('o_que') or ''))
            if ideia:
                md.append('   ideia: %s' % ideia)
        md.append('')
    open(os.path.join(a.saida, 'referencias.md'), 'w').write('\n'.join(md) + '\n')
    a.saida = os.path.abspath(a.saida)
    print('%d slides do roteiro; pranchas e resumo em %s' % (len(linhas), exibir(a.saida)))
    print('Abra %s e as pranchas slide-NN.jpg.' % exibir(os.path.join(a.saida, 'referencias.md')))


if __name__ == '__main__':
    main()
