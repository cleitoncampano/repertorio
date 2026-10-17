#!/usr/bin/env python3
"""Copia uma mídia do acervo em resolução original para uma pasta (para usar numa apresentação nova).
Uso: python3 -I ferramentas/midia.py <id> [<id> ...] pasta-destino
O id vem da busca (--doc midia). SVGs já estão soltos em acervo/svg/.
Atenção: fotos de marcas, famosos e bancos pagos servem de referência; confirme o direito de uso antes de publicar.
"""
import json
import os
import sys
import zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    ids, destino = sys.argv[1:-1], sys.argv[-1]
    os.makedirs(destino, exist_ok=True)
    falta = set(ids)
    with open(os.path.join(RAIZ, 'dados', 'midia.jsonl')) as f:
        for linha in f:
            m = json.loads(linha)
            alvo = next((i for i in falta if m['id'].startswith(i)), None)
            if not alvo:
                continue
            arq = os.path.join(RAIZ, '_originais', 'pptx', m['origem']['arq'])
            with zipfile.ZipFile(arq) as z:
                dados = z.read(m['origem']['parte'])
            saida = os.path.join(destino, m['id'] + m['ext'])
            open(saida, 'wb').write(dados)
            print(saida, '(%sx%s)' % (m.get('w'), m.get('h')) if m.get('w') else '')
            falta.discard(alvo)
            if not falta:
                break
    for i in falta:
        print('não achei', i)


if __name__ == '__main__':
    main()
