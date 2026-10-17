#!/usr/bin/env python3
"""Confere fichas contra o vocabulário e o pacote de origem.
Uso: python3 -I ferramentas/construir/validar.py dados/_trabalho/fichas/lote-NNN.json [...]
     python3 -I ferramentas/construir/validar.py --todos
"""
import glob
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VOC = json.load(open(os.path.join(RAIZ, 'dados', 'vocabulario.json')))
INT = {x['id'] for x in VOC['intencoes']['itens']}
TEC = {x['id'] for x in VOC['tecnicas']['itens']}
MOV = {x['id'] for x in VOC['movimentos']['itens']}
EST = set(VOC['esteticas']['itens'])
TOM = set(VOC['tons']['itens'])
CAMPOS = ['id', 'tipo', 'resumo', 'antes', 'ideia', 'como_funciona', 'html', 'intencoes', 'tecnicas', 'movimento',
          'estetica', 'tom', 'bom_para', 'cuidados', 'destaques', 'forca', 'slides']
TRACOS = (chr(0x2014), chr(0x2013))


def pacote(fid):
    p = os.path.join(RAIZ, 'dados', '_trabalho', 'pacotes', fid + '.json')
    return json.load(open(p)) if os.path.exists(p) else None


def tec_ok(t):
    return t in TEC or (isinstance(t, str) and t.startswith('nova:'))


def checar(f):
    erros = []
    def e(msg):
        erros.append('%s: %s' % (f.get('id', '?'), msg))
    for c in CAMPOS:
        if c not in f:
            e('falta o campo %s' % c)
    if f.get('tipo') not in ('modelo', 'componente', 'efeito'):
        e('tipo inválido %r' % f.get('tipo'))
    for c, ok, lo, hi in (('intencoes', INT, 1, 3), ('movimento', MOV, 0, 3), ('estetica', EST, 2, 5), ('tom', TOM, 1, 3)):
        v = f.get(c, [])
        if not isinstance(v, list) or not lo <= len(v) <= hi:
            e('%s deve ter de %d a %d itens' % (c, lo, hi))
        for x in v if isinstance(v, list) else []:
            if x not in ok:
                e('%s fora do vocabulário: %r' % (c, x))
    t = f.get('tecnicas', [])
    if not 1 <= len(t) <= 5:
        e('tecnicas deve ter de 1 a 5 itens')
    for x in t:
        if not tec_ok(x):
            e('técnica fora do vocabulário: %r' % x)
    if not isinstance(f.get('forca'), int) or not 1 <= f.get('forca', 0) <= 5:
        e('forca deve ser inteiro de 1 a 5')
    pac = pacote(f.get('id', ''))
    if pac is None:
        e('id não existe nos pacotes')
    else:
        n = pac['n_slides']
        ns = [s.get('n') for s in f.get('slides', [])]
        if sorted(ns) != list(range(1, n + 1)):
            e('slides deve cobrir 1..%d exatamente (veio %s)' % (n, ns[:30]))
        for x in f.get('antes', []) + f.get('destaques', []):
            if not isinstance(x, int) or not 1 <= x <= n:
                e('número de slide inválido %r' % x)
        if set(f.get('destaques', [])) & set(f.get('antes', [])):
            e('destaque não pode ser slide do antes')
    for s in f.get('slides', []):
        if s.get('intencao') not in INT | {'ANTES', 'OCULTO'}:
            e('slide %s: intencao inválida %r' % (s.get('n'), s.get('intencao')))
        for x in s.get('tecnicas', []):
            if not tec_ok(x):
                e('slide %s: técnica fora do vocabulário %r' % (s.get('n'), x))
        if len(s.get('nota', '')) > 160:
            e('slide %s: nota longa demais' % s.get('n'))
    antes = set(f.get('antes', []))
    for s in f.get('slides', []):
        if (s.get('intencao') == 'ANTES') != (s.get('n') in antes):
            e('slide %s: ANTES nos slides não bate com o campo antes' % s.get('n'))
    texto = json.dumps(f, ensure_ascii=False)
    if any(c in texto for c in TRACOS):
        e('tem travessão ou meia-risca; troque por vírgula ou dois-pontos')
    return erros


TIPOS_REF = {'capa', 'anuncio', 'ativacao', 'campanha', 'abertura-de-filme', 'frame-de-filme', 'livro', 'diagrama', 'retrato', 'interface'}


def checar_ref(f):
    erros = []
    def e(msg):
        erros.append('%s: %s' % (f.get('id', '?'), msg))
    for c in ('id', 'arquivo', 'fonte', 'tipo', 'o_que', 'ideia', 'como_levar_para_slide', 'intencoes', 'tecnicas', 'estetica', 'tom', 'forca'):
        if c not in f:
            e('falta o campo %s' % c)
    if f.get('tipo') not in TIPOS_REF:
        e('tipo inválido %r' % f.get('tipo'))
    for c, ok, lo, hi in (('intencoes', INT, 1, 2), ('estetica', EST, 1, 4), ('tom', TOM, 1, 2)):
        v = f.get(c, [])
        if not isinstance(v, list) or not lo <= len(v) <= hi:
            e('%s deve ter de %d a %d itens' % (c, lo, hi))
        for x in v if isinstance(v, list) else []:
            if x not in ok:
                e('%s fora do vocabulário: %r' % (c, x))
    t = f.get('tecnicas', [])
    if not 1 <= len(t) <= 4:
        e('tecnicas deve ter de 1 a 4 itens')
    for x in t:
        if not tec_ok(x):
            e('técnica fora do vocabulário: %r' % x)
    if not isinstance(f.get('forca'), int) or not 1 <= f.get('forca', 0) <= 5:
        e('forca deve ser inteiro de 1 a 5')
    if not os.path.exists(os.path.join(RAIZ, f.get('arquivo', ''))):
        e('arquivo não existe')
    if any(c in json.dumps(f, ensure_ascii=False) for c in TRACOS):
        e('tem travessão ou meia-risca; troque por vírgula ou dois-pontos')
    return erros


USOS_MIDIA = {'foto', 'recorte', 'fundo', 'textura', 'padrao', 'icone', 'ilustracao', 'mockup', 'logo', 'grafico', '3d', 'tipografia', 'interface', 'video'}


def checar_midia(a):
    erros = []
    try:
        et = json.load(open(a))
    except Exception as ex:
        return ['%s: JSON inválido: %s' % (a, ex)]
    lote = json.load(open(os.path.join(RAIZ, 'dados', '_trabalho', 'midia-lotes', os.path.basename(a))))
    ids = [x['id'] for x in lote['itens']]
    falta = [i for i in ids if i not in et]
    if falta:
        erros.append('faltam %d ids: %s' % (len(falta), falta[:8]))
    for k, v in et.items():
        if k not in ids:
            erros.append('id que não é do lote: %s' % k)
        if not isinstance(v, dict) or v.get('uso') not in USOS_MIDIA or not isinstance(v.get('tags'), list) or not isinstance(v.get('terceiros'), bool) or not v.get('o_que'):
            erros.append('%s: campos inválidos %s' % (k, json.dumps(v, ensure_ascii=False)[:120]))
    if any(c in json.dumps(et, ensure_ascii=False) for c in TRACOS):
        erros.append('tem travessão ou meia-risca')
    return erros


def main():
    if len(sys.argv) > 1 and os.path.basename(os.path.dirname(os.path.abspath(sys.argv[1]))) == 'midia':
        er = [x for a in sys.argv[1:] for x in checar_midia(a)]
        print('\n'.join(er) if er else 'OK')
        sys.exit(1 if er else 0)
    if '--todos' in sys.argv:
        arqs = sorted(glob.glob(os.path.join(RAIZ, 'dados', '_trabalho', 'fichas', 'lote-*.json'))) + \
            sorted(glob.glob(os.path.join(RAIZ, 'dados', '_trabalho', 'referencias', 'lote-*.json')))
    else:
        arqs = sys.argv[1:]
    total, ruins = 0, 0
    for a in arqs:
        try:
            fichas = json.load(open(a))
        except Exception as ex:
            print('%s: JSON inválido: %s' % (a, ex)); ruins += 1; continue
        ref = os.path.basename(os.path.dirname(os.path.abspath(a))) == 'referencias'
        lote = os.path.join(RAIZ, 'dados', '_trabalho', 'ref-lotes' if ref else 'lotes', os.path.basename(a))
        if os.path.exists(lote):
            dl = json.load(open(lote))
            esperados = [p['id'] for p in (dl['itens'] if ref else dl['pacotes'])]
            if [f.get('id') for f in fichas] != esperados:
                print('%s: ids diferentes do lote (esperado %s)' % (a, esperados)); ruins += 1
        for f in fichas:
            total += 1
            er = checar_ref(f) if ref else checar(f)
            if er:
                ruins += 1
                print('\n'.join(er))
    print('OK' if not ruins else 'COM PROBLEMAS', '| fichas', total, '| com erro', ruins)
    sys.exit(1 if ruins else 0)


if __name__ == '__main__':
    main()
