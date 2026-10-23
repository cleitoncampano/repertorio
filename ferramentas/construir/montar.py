#!/usr/bin/env python3
"""Monta a biblioteca a partir das fichas e dos dados extraídos:

  dados/fichas.jsonl     fichas dos arquivos (uma por arquivo do acervo)
  dados/indice.jsonl     índice único que a busca lê (arquivos, slides, referências externas, mídia)
  dados/grafo.json       nós e ligações (itens -> técnicas -> operações; itens -> intenções e movimentos)
  biblioteca/...         páginas por intenção, técnica, movimento e os índices de modelos, efeitos e componentes

Uso, da raiz do projeto:  python3 -I ferramentas/construir/montar.py
"""
import collections
import glob
import json
import os
import re
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DADOS = os.path.join(RAIZ, 'dados')
TRAB = os.path.join(DADOS, '_trabalho')
BIB = os.path.join(RAIZ, 'biblioteca')
VOC = json.load(open(os.path.join(DADOS, 'vocabulario.json')))


def jsonl(caminho):
    if not os.path.exists(caminho):
        return []
    return [json.loads(l) for l in open(caminho)]


def norm(s):
    s = unicodedata.normalize('NFKD', str(s or '')).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9%]+', ' ', s).strip()


def junta(*partes):
    out = []
    for p in partes:
        if isinstance(p, list):
            out.extend(str(x) for x in p)
        elif p:
            out.append(str(p))
    return ' '.join(out)


ECO = re.compile(r'repetid|em pilha|empilhad|\beco\b|repete a palavra|repetição da palavra|palavra repetida', re.I)


UI = re.compile(r'interface|tela de (app|aplicativo|streaming|celular|login|perfil)|cursor|barra de busca|notifica|bot[aã]o (de )?liga|player|chat|mensagem de|aplicativo', re.I)
NOVAS = [  # (técnica nova, regex na nota/descrição, técnicas vizinhas que precisam estar presentes)
    ('eco-tipografico', ECO, {'tipografia-como-imagem', 'padrao-e-quebra', 'destaque-tipografico', 'palavra-fantasma'}),
    ('interface-imitada', UI, {'emprestimo-de-codigo', 'objeto-como-suporte', 'referencia-cultural'}),
    ('cor-por-capitulo', re.compile(r'(fundo|cor) (inteiro |inteira )?(muda|troca)\w* (de cor )?a cada (cap[ií]tulo|parte|se[cç][aã]o|bloco)|cada (cap[ií]tulo|parte|se[cç][aã]o|bloco) (tem|ganha) (a )?(sua|uma) (pr[oó]pria )?cor|cor por (cap[ií]tulo|se[cç][aã]o)', re.I),
     {'contraste-de-cor', 'similaridade', 'transformacao', 'camera-continua', 'regiao-comum'}),
    ('dupla-exposicao', re.compile(r'dupla exposi|double exposure|dentro da silhueta|dentro de (outra|uma) (foto|silhueta|cabe[cç]a)|foto dentro d[ao] (rosto|cabe[cç]a|corpo|perfil)', re.I),
     {'metafora-visual', 'mascara-de-forma', 'profundidade-em-camadas', 'tipografia-como-imagem'}),
    ('sanfona', re.compile(r'sanfona|acorde[aã]o|se alarga|alarga e os outros|faixas? vertica\w+ .{0,60}(abre|alarga|expande)', re.I),
     {'regiao-comum', 'grade-modular', 'revelacao-progressiva', 'foco-seletivo', 'reorganizar', 'similaridade'}),
]


def enriquecer(fichas):
    """Técnicas que entraram no vocabulário depois das fichas escritas: marca pelo texto, só onde a técnica vizinha já foi usada."""
    oficiais = {t['id'] for t in VOC['tecnicas']['itens']}
    for f in fichas:
        conv = lambda ts: [t[5:] if t.startswith('nova:') and t[5:] in oficiais else t for t in ts]
        f['tecnicas'] = conv(f.get('tecnicas', []))
        for s in f.get('slides', []):
            s['tecnicas'] = conv(s.get('tecnicas', []))
        for nova, rx, vizinhas in NOVAS:
            marcou = False
            for s in f.get('slides', []):
                ts = s.get('tecnicas', [])
                if nova not in ts and rx.search(s.get('nota', '')) and set(ts) & vizinhas:
                    s['tecnicas'] = ts + [nova]
                    marcou = True
            texto = ' '.join([f.get('resumo', ''), f.get('como_funciona', '')])
            if (marcou or (rx.search(texto) and set(f.get('tecnicas', [])) & vizinhas)) and nova not in f.get('tecnicas', []):
                f['tecnicas'] = f.get('tecnicas', []) + [nova]


def catalogo():
    s = open(os.path.join(RAIZ, '_catalogo', 'dados.js')).read()
    d = json.loads(s[s.index('{'):s.rindex('}') + 1])
    cat = {x['id']: x for x in d['decks']}
    for c in d['canva']:
        cat[c['id']] = {'id': c['id'], 'titulo': 'Canva: ' + c['aula'], 'grupos': ['Canva (PDF)'], 'arq': c['arq'], 'slides': c['paginas'],
                        'canva': c['canva'], 'insta': c['insta']}
    return cat


def thumb(did, n):
    return '_catalogo/miniaturas/%s/%02d.jpg' % (did, n)


def main():
    cat = catalogo()
    decks = {d['id']: d for d in jsonl(os.path.join(DADOS, 'decks.jsonl'))}
    slides_x = {(s['deck'], s['n']): s for s in jsonl(os.path.join(DADOS, 'slides.jsonl'))}
    trans = {(t['deck'], t['para']): t for t in jsonl(os.path.join(DADOS, 'transicoes.jsonl'))}
    pranchas = json.load(open(os.path.join(RAIZ, '_catalogo', 'pranchas', 'pranchas.json')))

    fichas = []
    for arq in sorted(glob.glob(os.path.join(TRAB, 'fichas', 'lote-*.json'))):
        fichas.extend(json.load(open(arq)))
    enriquecer(fichas)
    vistos = set()
    fichas = [f for f in fichas if not (f['id'] in vistos or vistos.add(f['id']))]

    indice, fichas_out = [], []
    for f in fichas:
        c = cat.get(f['id'], {})
        dx = decks.get(f['id'], {})
        arquivo = ('_originais/canva/' if f['id'].startswith('canva-') else '_originais/pptx/') + c.get('arq', '')
        ficha = dict(f)
        ficha.update({'titulo': c.get('titulo'), 'grupos': c.get('grupos', []), 'arquivo': arquivo,
                      'pranchas': pranchas.get(f['id'], []), 'paleta': [p['hex'] for p in dx.get('paleta', [])][:6],
                      'fontes': [x['nome'] for x in dx.get('fontes', [])][:4], 'proporcao': dx.get('proporcao', '16:9')})
        if c.get('canva'):
            ficha['links'] = {'canva': c['canva'], 'instagram': c.get('insta')}
        fichas_out.append(ficha)
        doc = {k: ficha.get(k) for k in ('id', 'titulo', 'tipo', 'resumo', 'ideia', 'como_funciona', 'html', 'intencoes', 'tecnicas', 'movimento',
                                          'estetica', 'tom', 'bom_para', 'cuidados', 'forca', 'destaques', 'paleta', 'fontes', 'proporcao', 'arquivo', 'grupos')}
        doc['doc'] = 'arquivo'
        doc['slides_antes'] = f.get('antes', [])
        doc['imagem'] = (ficha['pranchas'] or [None])[0]
        doc['texto'] = junta(ficha.get('titulo'), f.get('resumo'), f.get('ideia'), f.get('como_funciona'), f.get('bom_para'), f.get('estetica'),
                             f.get('tom'), ficha.get('grupos'), [s.get('nota') for s in f.get('slides', [])])
        indice.append(doc)
        destaques = set(f.get('destaques', []))
        antes = set(f.get('antes', []))
        for s in f.get('slides', []):
            n = s['n']
            sx = slides_x.get((f['id'], n), {})
            t = trans.get((f['id'], n))
            mov = list(t.get('familias', [])) if t and t.get('tipo') == 'morph' else ([{'push': 'panorama', 'fade': 'troca', 'cover': 'voo', 'wipe': 'revelacao'}.get(t['tipo'], 'troca')] if t else [])
            sd = {'doc': 'slide', 'id': '%s#%d' % (f['id'], n), 'deck': f['id'], 'n': n, 'titulo': c.get('titulo'), 'tipo': f.get('tipo'),
                  'intencoes': [s.get('intencao')] if s.get('intencao') not in ('ANTES', 'OCULTO') else [],
                  'intencao': s.get('intencao'), 'tecnicas': s.get('tecnicas', []), 'nota': s.get('nota'),
                  'movimento': [m for m in mov if m not in ('estatico', 'so-entradas')], 'estetica': f.get('estetica', []), 'tom': f.get('tom', []),
                  'forca': f.get('forca'), 'destaque': n in destaques, 'antes': n in antes or s.get('intencao') == 'ANTES',
                  'oculto': s.get('intencao') == 'OCULTO' or sx.get('oculto', False), 'imagem': thumb(f['id'], n),
                  'proporcao': ficha['proporcao'], 'ideia_arquivo': f.get('ideia')}
            if t:
                sd['transicao'] = t['tipo']
                if t.get('resumo'):
                    sd['morph'] = t['resumo']
            if sx.get('titulo'):
                sd['texto_slide'] = sx['titulo']
            sd['texto'] = junta(s.get('nota'), sd.get('texto_slide'), c.get('titulo'), f.get('estetica'), f.get('tom'), s.get('tecnicas'))
            if s.get('intencao') == 'OCULTO':
                sd['antes'] = True
            indice.append(sd)

    # referências externas (capas, anúncios, frames de vídeo), quando já fichadas
    for arq in sorted(glob.glob(os.path.join(TRAB, 'referencias', 'lote-*.json'))):
        for r in json.load(open(arq)):
            r = dict(r)
            r['doc'] = 'referencia'
            r['texto'] = junta(r.get('o_que'), r.get('ideia'), r.get('fonte'), r.get('estetica'), r.get('tom'), r.get('bom_para'))
            r['imagem'] = r.get('arquivo')
            indice.append(r)

    # mídia: imagens, recortes, fundos, vídeos, 3D (ícones SVG entram pelo arquivo)
    etiquetas = {}
    for arq in glob.glob(os.path.join(TRAB, 'midia', 'lote-*.json')):
        etiquetas.update(json.load(open(arq)))
    for m in jsonl(os.path.join(DADOS, 'midia.jsonl')):
        if m['tipo'] not in ('imagem', 'video', '3d', 'svg') or m.get('fallback_de'):
            continue
        if m['tipo'] == 'imagem' and max(m.get('w') or 0, m.get('h') or 0) < 120:
            continue
        papeis = collections.Counter(u.get('papel') for u in m['usos'])
        if m['tipo'] == 'imagem':
            uso = 'recorte' if (m.get('transparencia') or 0) > 0.15 else 'fundo' if papeis.get('fundo') else 'foto'
        else:
            uso = {'video': 'video', '3d': '3d', 'svg': 'icone'}[m['tipo']]
        et = etiquetas.get(m['id']) or etiquetas.get(m['id'][:8]) or {}
        decks_m = sorted({u['deck'] for u in m['usos']})
        usos = [et.get('uso') or uso]
        if uso == 'recorte' and 'recorte' not in usos:
            usos.append('recorte')
        if uso == 'fundo' and 'fundo' not in usos:
            usos.append('fundo')
        doc = {'doc': 'midia', 'id': m['id'], 'uso': usos, 'sem_fundo': uso == 'recorte', 'tipo': m['tipo'], 'ext': m['ext'], 'w': m.get('w'), 'h': m.get('h'),
               'o_que': et.get('o_que'), 'tags': et.get('tags', []), 'terceiros': et.get('terceiros'), 'imagem': m.get('previa') or m.get('arquivo'),
               'arquivo': m.get('arquivo'), 'decks': decks_m[:5], 'origem': m['origem'],
               'fonte_extra': 'pegar em alta: python3 -I ferramentas/midia.py %s pasta-destino' % m['id']}
        if m.get('dur_s'):
            doc['dur_s'] = m['dur_s']
        doc['texto'] = junta(doc['o_que'], doc['tags'], doc['uso'], 'sem fundo' if doc['sem_fundo'] else '', [cat.get(x, {}).get('titulo') for x in decks_m[:5]])
        indice.append(doc)

    for d in indice:
        d['_t'] = norm(d.get('texto'))
    with open(os.path.join(DADOS, 'indice.jsonl'), 'w') as f:
        for d in indice:
            f.write(json.dumps(d, ensure_ascii=False) + '\n')
    with open(os.path.join(DADOS, 'fichas.jsonl'), 'w') as f:
        for d in fichas_out:
            f.write(json.dumps(d, ensure_ascii=False) + '\n')

    grafo(indice)
    paginas(indice, fichas_out)
    pagina_vocab()
    c = collections.Counter(d['doc'] for d in indice)
    print('fichas', len(fichas_out), '| índice', dict(c))


def grafo(indice):
    nos, arestas = [], []
    for it in VOC['operacoes']['itens']:
        nos.append({'id': 'op:' + it['id'], 'tipo': 'operacao', 'nome': it['nome']})
    for it in VOC['tecnicas']['itens']:
        nos.append({'id': 'tec:' + it['id'], 'tipo': 'tecnica', 'nome': it['nome'], 'pista': it['pista']})
        arestas.append(['tec:' + it['id'], 'op:' + it['operacao']])
    for it in VOC['intencoes']['itens']:
        nos.append({'id': 'int:' + it['id'], 'tipo': 'intencao', 'nome': it['nome']})
    for it in VOC['movimentos']['itens']:
        nos.append({'id': 'mov:' + it['id'], 'tipo': 'movimento', 'nome': it['nome']})
    for d in indice:
        if d['doc'] == 'midia' or (d['doc'] == 'slide' and not d.get('destaque')):
            continue
        nid = d['doc'][:3] + ':' + d['id']
        nos.append({'id': nid, 'tipo': d['doc'], 'nome': d.get('titulo') or d.get('o_que') or d['id'], 'imagem': d.get('imagem'), 'forca': d.get('forca')})
        for t in d.get('tecnicas') or []:
            if not t.startswith('nova:'):
                arestas.append([nid, 'tec:' + t])
        for i in d.get('intencoes') or []:
            arestas.append([nid, 'int:' + i])
        for m in d.get('movimento') or []:
            arestas.append([nid, 'mov:' + m])
        if d['doc'] == 'slide':
            arestas.append([nid, 'arq:' + d['deck']])
    json.dump({'nos': nos, 'arestas': arestas}, open(os.path.join(DADOS, 'grafo.json'), 'w'), ensure_ascii=False)


# ---------- páginas ----------

def pagina_vocab():
    p = ['# Vocabulário', '', VOC['sobre'], '']
    p += ['## Intenções', '', VOC['intencoes']['sobre'], '', '| id | o que é |', '|---|---|']
    p += ['| `%s` | %s |' % (i['id'], i['def']) for i in VOC['intencoes']['itens']]
    p += ['', '## Operações do olhar', '', VOC['operacoes']['sobre'], '']
    for o in VOC['operacoes']['itens']:
        p += ['### %s' % o['nome'], '', o['def'], '', '| técnica | pista | o que é |', '|---|---|---|']
        p += ['| [`%s`](tecnicas/%s.md) | %s | %s |' % (t['id'], t['id'], t['pista'], t['def']) for t in VOC['tecnicas']['itens'] if t['operacao'] == o['id']]
        p.append('')
    p += ['## Movimentos', '', VOC['movimentos']['sobre'], '', '| id | o que é |', '|---|---|']
    p += ['| [`%s`](movimentos/%s.md) | %s |' % (m['id'], m['id'], m['def']) for m in VOC['movimentos']['itens']]
    p += ['', '## Estéticas', '', ', '.join(VOC['esteticas']['itens']), '', '## Tons', '', ', '.join(VOC['tons']['itens'])]
    escrever(os.path.join(BIB, 'vocabulario.md'), '\n'.join(p))

def linha_exemplo(d):
    if d['doc'] == 'slide':
        return '- **%s** (%s, força %s): %s  \n  `%s`' % (d['id'], d.get('titulo'), d.get('forca'), d.get('nota') or '', d.get('imagem'))
    if d['doc'] == 'referencia':
        return '- **%s** (%s): %s  \n  `%s`' % (d['id'], d.get('fonte', ''), d.get('ideia') or d.get('o_que') or '', d.get('imagem'))
    return '- **%s** (%s, força %s): %s  \n  `%s`' % (d['id'], d.get('titulo'), d.get('forca'), d.get('ideia') or '', d.get('imagem'))


def melhores(docs, n):
    return sorted(docs, key=lambda d: (-(d.get('forca') or 0), not d.get('destaque'), d['id']))[:n]


def escrever(caminho, texto):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    open(caminho, 'w').write(texto.rstrip() + '\n')


def paginas(indice, fichas):
    uteis = [d for d in indice if d['doc'] in ('arquivo', 'slide', 'referencia') and not d.get('antes')]
    tec_nome = {t['id']: t for t in VOC['tecnicas']['itens']}
    # intenções
    for it in VOC['intencoes']['itens']:
        sl = [d for d in uteis if d['doc'] == 'slide' and it['id'] in d.get('intencoes', [])]
        refs = [d for d in uteis if d['doc'] == 'referencia' and it['id'] in d.get('intencoes', [])]
        tc = collections.Counter(t for d in sl for t in d.get('tecnicas', []))
        mv = collections.Counter(m for d in sl for m in d.get('movimento', []))
        p = ['# %s: %s' % (it['id'], it['nome']), '', it['def'], '']
        dica = os.path.join(BIB, 'intencoes', '_dicas', it['id'] + '.md')
        if os.path.exists(dica):
            p += [open(dica).read().strip(), '']
        p += ['## Técnicas que mais aparecem', '', ', '.join('`%s` (%d)' % (t, n) for t, n in tc.most_common(10)) or 'ainda sem dados', '',
              '## Movimentos que mais aparecem', '', ', '.join('`%s` (%d)' % (t, n) for t, n in mv.most_common(6)) or 'ainda sem dados', '',
              '## Melhores slides do acervo (%d no total)' % len(sl), '']
        p += [linha_exemplo(d) for d in melhores(sl, 14)]
        if refs:
            p += ['', '## Referências externas', ''] + [linha_exemplo(d) for d in melhores(refs, 8)]
        p += ['', 'Mais: `python3 -I ferramentas/buscar.py -i %s --doc slide --forca 4 --prancha`' % it['id']]
        escrever(os.path.join(BIB, 'intencoes', it['id'] + '.md'), '\n'.join(p))
    # técnicas
    co = collections.defaultdict(collections.Counter)
    for d in uteis:
        ts = [t for t in d.get('tecnicas', []) if not t.startswith('nova:')]
        for a in ts:
            for b in ts:
                if a != b:
                    co[a][b] += 1
    for it in VOC['tecnicas']['itens']:
        docs = [d for d in uteis if it['id'] in d.get('tecnicas', [])]
        p = ['# %s' % it['nome'], '', '`%s` · operação: %s · pista: %s' % (it['id'], it['operacao'], it['pista']), '', it['def'], '',
             '**Em HTML:** ' + it['html'], '']
        if co[it['id']]:
            p += ['**Combina com:** ' + ', '.join('`%s`' % t for t, _ in co[it['id']].most_common(5)), '']
        for rot, tipo in (('Arquivos do acervo', 'arquivo'), ('Slides do acervo', 'slide'), ('Referências externas', 'referencia')):
            sel = melhores([d for d in docs if d['doc'] == tipo], 8)
            if sel:
                p += ['## %s' % rot, ''] + [linha_exemplo(d) for d in sel] + ['']
        p += ['Mais: `python3 -I ferramentas/buscar.py -t %s --prancha`' % it['id']]
        escrever(os.path.join(BIB, 'tecnicas', it['id'] + '.md'), '\n'.join(p))
    # movimentos
    for it in VOC['movimentos']['itens']:
        arqs = [d for d in uteis if d['doc'] == 'arquivo' and it['id'] in (d.get('movimento') or [])]
        sl = [d for d in uteis if d['doc'] == 'slide' and it['id'] in (d.get('movimento') or []) and d.get('morph')]
        p = ['# %s' % it['nome'], '', '`%s`' % it['id'], '', it['def'], '', '**Em HTML:** ' + it['html'], '']
        receita = os.path.join(BIB, 'movimentos', '_receitas', it['id'] + '.md')
        if os.path.exists(receita):
            p += [open(receita).read().strip(), '']
        p += ['## Arquivos que usam (%d)' % len(arqs), ''] + [linha_exemplo(d) for d in melhores(arqs, 10)]
        if sl:
            p += ['', '## Passagens de slide analisadas', '']
            for d in melhores(sl, 8):
                p.append('- **%s**: %s  \n  `%s`' % (d['id'], d['morph'][:200], d['imagem']))
        p += ['', 'Mais: `python3 -I ferramentas/buscar.py -m %s --doc arquivo --prancha`' % it['id']]
        escrever(os.path.join(BIB, 'movimentos', it['id'] + '.md'), '\n'.join(p))
    # índices de arquivos
    for tipo, titulo, sobre in (('modelo', 'Estilos (modelos completos)', 'Apresentações inteiras com identidade própria. Use para escolher a linguagem visual de uma apresentação nova.'),
                                ('efeito', 'Efeitos', 'Truques visuais e de movimento. Use para criar os momentos de impacto.'),
                                ('componente', 'Componentes', 'Peças de layout reaproveitáveis: gráficos, linhas do tempo, mapas, organogramas, tabelas.')):
        sel = sorted([f for f in fichas if f.get('tipo') == tipo], key=lambda f: (-(f.get('forca') or 0), f['id']))
        p = ['# %s' % titulo, '', sobre, '', '%d arquivos, do mais forte para o mais fraco. Prancha = todos os slides numa imagem.' % len(sel), '',
             '| id | força | estética | tom | ideia | prancha |', '|---|---|---|---|---|---|']
        for f in sel:
            p.append('| %s | %s | %s | %s | %s | `%s` |' % (f['id'], f.get('forca'), ', '.join(f.get('estetica', [])), ', '.join(f.get('tom', [])),
                                                            (f.get('ideia') or '').replace('|', '/'), (f.get('pranchas') or [''])[0]))
        escrever(os.path.join(BIB, {'modelo': 'estilos.md', 'efeito': 'efeitos.md', 'componente': 'componentes.md'}[tipo]), '\n'.join(p))


if __name__ == '__main__':
    main()
