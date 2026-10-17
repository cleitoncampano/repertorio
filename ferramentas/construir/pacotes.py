#!/usr/bin/env python3
"""Junta, para cada arquivo do acervo, um resumo curto (pacote) usado na hora de escrever a ficha:
metadados do catálogo + paleta, fontes, títulos dos slides e o que cada Morph faz.
Saída: dados/_trabalho/pacotes/<id>.json
Uso, da raiz do projeto:  python3 -I ferramentas/construir/pacotes.py
"""
import collections
import json
import os
import re
import zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DADOS = os.path.join(RAIZ, 'dados')
SAIDA = os.path.join(DADOS, '_trabalho', 'pacotes')


RPR = re.compile(r'<a:rPr\b[^>]*>(.*?)</a:rPr>', re.S)
LIMPA = re.compile(r'<a:ln\b.*?</a:ln>|<a:effectLst>.*?</a:effectLst>|<a:highlight>.*?</a:highlight>|<a:uFill>.*?</a:uFill>', re.S)
SPPR = re.compile(r'<p:sp>.*?<p:spPr\b[^>]*>(.*?)</p:spPr>', re.S)


def alertas_xml(x):
    al = []
    if 'videoFile' in x or '<p14:media' in x:
        al.append('video')
    if 'am3d' in x or 'model3d' in x:
        al.append('3d')
    runs = [LIMPA.sub('', m) for m in RPR.findall(x)]
    if any('<a:blipFill' in r for r in runs):
        al.append('texto com imagem dentro')
    if any('<a:noFill/>' in r for r in runs):
        al.append('texto vazado ou invisível')
    if any(r.count('<a:gradFill') for r in runs):
        al.append('texto em degradê')
    if any('<a:blipFill' in sp for sp in SPPR.findall(x)):
        al.append('forma preenchida com imagem (máscara)')
    if 'backgroundRemoval' in x:
        al.append('recorte feito no PowerPoint (fundo removido)')
    if re.search(r'<a14:artistic', x):
        al.append('efeito artístico na imagem')
    if '/chart"' in x or '<c:chart' in x:
        al.append('gráfico')
    return al


def alertas_por_slide(arq):
    out = {}
    try:
        z = zipfile.ZipFile(os.path.join(RAIZ, '_originais', 'pptx', arq))
        pres = z.read('ppt/presentation.xml').decode('utf8', 'ignore')
        rels = z.read('ppt/_rels/presentation.xml.rels').decode('utf8', 'ignore')
        alvo = {}
        for e in re.findall(r'<Relationship\b[^>]*/>', rels):
            a, b = re.search(r'Id="([^"]+)"', e), re.search(r'Target="([^"]+)"', e)
            if a and b:
                alvo[a.group(1)] = b.group(1).lstrip('/').replace('ppt/', '', 1)
        ids = re.findall(r'<p:sldId\b[^>]*r:id="([^"]+)"', pres)
        for k, rid in enumerate(ids, 1):
            al = alertas_xml(z.read('ppt/' + alvo[rid]).decode('utf8', 'ignore'))
            if al:
                out[k] = al
    except Exception:
        pass
    return out


def jsonl(nome):
    return [json.loads(l) for l in open(os.path.join(DADOS, nome))]


def main():
    os.makedirs(SAIDA, exist_ok=True)
    s = open(os.path.join(RAIZ, '_catalogo', 'dados.js')).read()
    cat = json.loads(s[s.index('{'):s.rindex('}') + 1])
    pranchas = json.load(open(os.path.join(RAIZ, '_catalogo', 'pranchas', 'pranchas.json')))
    decks = {d['id']: d for d in jsonl('decks.jsonl')}
    slides = collections.defaultdict(list)
    for x in jsonl('slides.jsonl'):
        slides[x['deck']].append(x)
    trans = collections.defaultdict(list)
    for t in jsonl('transicoes.jsonl'):
        trans[t['deck']].append(t)
    n = 0
    for c in cat['decks']:
        d = decks[c['id']]
        morphs = [t for t in trans[c['id']] if t['tipo'] == 'morph' and t.get('familias')]
        morphs.sort(key=lambda t: (t['familias'] in (['estatico'], ['so-entradas']), t['para']))
        pac = {
            'id': c['id'], 'titulo': c['titulo'], 'grupos': c['grupos'], 'modulo': c['modulo'], 'arquivo': '_originais/pptx/' + c['arq'],
            'n_slides': c['slides'], 'ocultos': c['ocultos'], 'proporcao': d['proporcao'], 'pranchas': pranchas.get(c['id'], []),
            'paleta': [p['hex'] for p in d['paleta']], 'fundos': d['fundos'], 'fontes': [f['nome'] for f in d['fontes'][:5]],
            'transicoes': d['transicoes'], 'familias_morph_auto': d['familias_morph'], 'midias': d['midias'],
            'tem_video': c['video'], 'tem_3d': c['tres_d'], 'tem_grafico': c['grafico'], 'tem_tabela': c['tabela'],
            'morph_auto': [{'de': t['de'], 'para': t['para'], 'familias': t['familias'], 'resumo': t['resumo'][:260]} for t in morphs[:10]],
            'slides': [{'n': x['n'], 'titulo': (x['titulo'] or '')[:70], 'transicao': (x['transicao'] or {}).get('tipo'),
                        'animacoes': sum(a['vezes'] for a in x['animacoes'])} for x in sorted(slides[c['id']], key=lambda x: x['n'])],
        }
        al = alertas_por_slide(c['arq'])
        for x in pac['slides']:
            if al.get(x['n']):
                x['alertas'] = al[x['n']]
        json.dump(pac, open(os.path.join(SAIDA, c['id'] + '.json'), 'w'), ensure_ascii=False, indent=1)
        n += 1
    for c in cat['canva']:
        pac = {'id': c['id'], 'titulo': 'Canva: ' + c['aula'], 'grupos': ['Canva (PDF)'], 'modulo': 'Canva', 'arquivo': '_originais/canva/' + c['arq'],
               'n_slides': c['paginas'], 'pranchas': pranchas.get(c['id'], []), 'canva': c['canva'], 'instagram': c['insta'],
               'obs': 'PDF exportado do Canva: só imagem, sem dados de transição. O link do Instagram mostra o efeito animado.'}
        json.dump(pac, open(os.path.join(SAIDA, c['id'] + '.json'), 'w'), ensure_ascii=False, indent=1)
        n += 1
    print('pacotes', n)


if __name__ == '__main__':
    main()
