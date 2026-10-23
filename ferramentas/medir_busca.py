#!/usr/bin/env python3
"""Mede a busca dos agentes (search_references) com pedidos reais e o resultado esperado de cada um.

Pedidos e julgamentos ficam em ferramentas/busca_pedidos.json: para cada pedido, os espaços e as referências já julgadas
(2 = é o que foi pedido, 1 = serve em parte, 0 = não serve). A busca roda numa cópia do banco, migrada com o código atual,
sem gravar nada no acervo.

  app/.venv/bin/python ferramentas/medir_busca.py medir [--salvar ARQ] [--comparar ARQ]
  app/.venv/bin/python ferramentas/medir_busca.py candidatos [--saida ARQ] [N ...]
  app/.venv/bin/python ferramentas/medir_busca.py julgar ARQ_JSON
  --ajuste NOME=VALOR troca um peso de repertorio.agent só nesta medição (ex.: --ajuste COVER_WEIGHT=4).
  --codigo PASTA mede outra versão do servidor (ex.: `git archive HEAD app/server | tar -x -C /tmp/base`, depois
  --codigo /tmp/base/app/server), para comparar antes e depois de uma mudança.

`candidatos` lista o que a busca atual e a busca só por texto trazem e ainda não foi julgado, sem dizer a posição de cada
item, para quem julga não se guiar pela ordem. `julgar` junta ao arquivo de pedidos um JSON {"N": {"id": nota}}.
`medir` mostra, por pedido, a posição do primeiro item que é o pedido (nota 2), quantos servem entre os 8 primeiros e
quantos ainda não foram julgados; no fim, a média de nDCG@8 (1 = os melhores itens nas primeiras posições).
"""
import argparse
import json
import math
import random
import sqlite3
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODIGO = sys.argv[sys.argv.index('--codigo') + 1] if '--codigo' in sys.argv else str(ROOT / 'app/server')
sys.path.insert(0, CODIGO)

from repertorio.agent import STOP, KINDS, interpret, norm, singular, smart_search  # noqa: E402
from repertorio.config import Settings  # noqa: E402
from repertorio.db import Database  # noqa: E402
from repertorio.schemas import AgentSearch  # noqa: E402
from repertorio.service import Library  # noqa: E402

PEDIDOS = ROOT / 'ferramentas/busca_pedidos.json'
TOPO = 8


def abrir(origem):
    pasta = Path(tempfile.mkdtemp(prefix='medir-busca-'))
    with sqlite3.connect(f'file:{origem}?mode=ro', uri=True) as fonte, sqlite3.connect(pasta / 'library.sqlite3') as copia:
        fonte.backup(copia)
    db = Database(Settings(ROOT, pasta))
    db.migrate()
    return Library(db)


def espacos(lib, nomes):
    ids = {w['name']: w['id'] for w in lib.db.query('SELECT id,name FROM workspaces WHERE deleted IS NULL')}
    return [ids[n] for n in nomes]


def buscar(lib, pedido, limite=16):
    args = AgentSearch(query=pedido['pedido'], workspace_ids=espacos(lib, pedido['espacos']), limit=limite,
                       contact_sheet=False, **pedido.get('opcoes', {}))
    return [i['id'] for i in smart_search(lib, args, log=False)['items']]


def so_texto(lib, pedido, juntar, limite=12):
    """Busca só pelas palavras do pedido, para achar itens que a leitura do vocabulário esconde."""
    termos = [singular(w) for w in norm(pedido['pedido']) if w not in STOP and len(w) > 1]
    if not termos:
        return []
    params = {'match': juntar.join('"' + t + '"*' for t in termos)}
    args = AgentSearch(workspace_ids=espacos(lib, pedido['espacos']), **pedido.get('opcoes', {}))
    clauses = lib.filters(args.model_copy(update={'kind': args.kind or KINDS}), params)
    rows = lib.db.query(f'''SELECT r.id FROM ref_search s JOIN refs r ON r.id=s.id
        WHERE ref_search MATCH :match AND {' AND '.join(clauses)} ORDER BY bm25(ref_search,0,5,1) LIMIT {limite}''', **params)
    return [r['id'] for r in rows]


def ndcg(ids, notas):
    ganho = lambda n: 2 ** n - 1
    dcg = sum(ganho(notas.get(i, 0)) / math.log2(p + 2) for p, i in enumerate(ids[:TOPO]))
    ideal = sum(ganho(n) / math.log2(p + 2) for p, n in enumerate(sorted(notas.values(), reverse=True)[:TOPO]))
    return dcg / ideal if ideal else 0.0


def medir(lib, pedidos):
    linhas = []
    for n, pedido in enumerate(pedidos, 1):
        ids = buscar(lib, pedido)
        notas = pedido.get('notas', {})
        primeiro = next((p for p, i in enumerate(ids, 1) if notas.get(i) == 2), None)
        linhas.append(dict(n=n, pedido=pedido['pedido'], primeiro=primeiro, ids=ids,
                           uteis=sum(1 for i in ids[:TOPO] if notas.get(i, 0) >= 1),
                           sem_nota=sum(1 for i in ids[:TOPO] if i not in notas), ndcg=round(ndcg(ids, notas), 3),
                           entendido=[u['term'] + ' = ' + ', '.join(u['meaning'])
                                      for u in interpret(pedido['pedido'], lib.meta('vocabulary', {}))[1]]))
    return linhas


def mostrar(linhas, antes=None):
    anterior = {l['pedido']: l for l in antes or []}
    print(f'{"n":>3} {"1º certo":>8} {"úteis/8":>7} {"s/ nota":>7} {"nDCG@8":>7}  pedido')
    for l in linhas:
        a = anterior.get(l['pedido'])
        delta = f' ({l["ndcg"] - a["ndcg"]:+.2f})' if a else ''
        print(f'{l["n"]:>3} {l["primeiro"] or "-":>8} {l["uteis"]:>7} {l["sem_nota"]:>7} {l["ndcg"]:>7.2f}{delta}  {l["pedido"]}')
        if l['entendido']:
            print(' ' * 38 + 'entendido: ' + '; '.join(l['entendido']))
    total = len(linhas)
    media = sum(l['ndcg'] for l in linhas) / total
    em3 = sum(1 for l in linhas if l['primeiro'] and l['primeiro'] <= 3)
    em8 = sum(1 for l in linhas if l['primeiro'] and l['primeiro'] <= TOPO)
    print(f'\nnDCG@8 médio: {media:.3f} | item certo entre os 3 primeiros: {em3}/{total} | entre os 8: {em8}/{total}'
          f' | itens sem nota entre os 8: {sum(l["sem_nota"] for l in linhas)}')
    if antes:
        print(f'antes: nDCG@8 médio {sum(l["ndcg"] for l in antes) / len(antes):.3f}')


def candidatos(lib, pedidos, escolhidos, saida):
    partes = []
    for n, pedido in enumerate(pedidos, 1):
        if escolhidos and n not in escolhidos:
            continue
        notas = pedido.get('notas', {})
        pool = dict.fromkeys(buscar(lib, pedido) + so_texto(lib, pedido, ' AND ') + so_texto(lib, pedido, ' OR '))
        novos = [i for i in pool if i not in notas]
        random.Random(n).shuffle(novos)
        if not novos:
            continue
        partes.append(f'## {n}. {pedido["pedido"]}\n\nEspaços: {", ".join(pedido["espacos"])}. {pedido.get("nota", "")}\n')
        rows = {r['id']: r for r in lib.db.query('SELECT id,kind,title,payload FROM refs WHERE id IN (SELECT value FROM json_each(:ids))',
                                                 ids=json.dumps(novos))}
        for i in novos:
            r = rows[i]
            d = json.loads(r['payload'] or '{}')
            tags = ', '.join((d.get('intentions') or []) + (d.get('techniques') or []))
            partes.append(f'- `{i}` [{r["kind"]}] **{r["title"]}**: {d.get("idea") or d.get("description") or ""}'
                          f' | como: {(d.get("how") or "")[:220]} | serve para: {"; ".join(d.get("good_for") or [])} | {tags}')
        partes.append('')
    texto = '\n'.join(partes)
    if saida:
        Path(saida).write_text(texto, encoding='utf-8')
        print(f'{saida}: {texto.count(chr(10) + "- ")} itens para julgar')
    else:
        print(texto)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('comando', choices=('medir', 'candidatos', 'julgar'))
    parser.add_argument('extra', nargs='*')
    parser.add_argument('--banco', default=str(ROOT / 'app/.runtime/library.sqlite3'))
    parser.add_argument('--salvar')
    parser.add_argument('--comparar')
    parser.add_argument('--saida')
    parser.add_argument('--codigo')
    parser.add_argument('--ajuste', action='append', default=[])
    opts = parser.parse_args()
    import repertorio.agent as agente
    for ajuste in opts.ajuste:
        nome, valor = ajuste.split('=', 1)
        setattr(agente, nome, json.loads(valor))
    pedidos = json.loads(PEDIDOS.read_text(encoding='utf-8'))
    if opts.comando == 'julgar':
        for arquivo in opts.extra:
            for n, notas in json.loads(Path(arquivo).read_text(encoding='utf-8')).items():
                pedidos[int(n) - 1].setdefault('notas', {}).update(notas)
        PEDIDOS.write_text(json.dumps(pedidos, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        print(f'{sum(len(p.get("notas", {})) for p in pedidos)} notas em {PEDIDOS.name}')
        return
    lib = abrir(opts.banco)
    if opts.comando == 'candidatos':
        candidatos(lib, pedidos, {int(x) for x in opts.extra}, opts.saida)
        return
    linhas = medir(lib, pedidos)
    antes = json.loads(Path(opts.comparar).read_text(encoding='utf-8')) if opts.comparar else None
    mostrar(linhas, antes)
    if opts.salvar:
        Path(opts.salvar).write_text(json.dumps(linhas, ensure_ascii=False, indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()
