# Scripts que constroem a biblioteca

Rodam da raiz do projeto, nesta ordem. Os de máquina levam segundos; as fichas são escritas por modelos (instruções em `dados/_trabalho/`).

| passo | script | gera |
|---|---|---|
| 1 | `extrair.py` | `dados/decks.jsonl`, `slides.jsonl`, `transicoes.jsonl` (Morph analisado), `midia.jsonl`, `acervo/previas/`, `acervo/svg/` |
| 2 | `pranchas.py` | `_catalogo/pranchas/<id>.jpg` (todos os slides numerados numa imagem) |
| 3 | `pacotes.py` | `dados/_trabalho/pacotes/<id>.json` (resumo por arquivo, com alertas de efeitos que a miniatura não mostra) |
| 4 | `lotes.py`, `lotes_referencias.py`, `lotes_midia.py` | lotes de trabalho em `dados/_trabalho/` |
| 5 | modelos escrevem | `dados/_trabalho/fichas/`, `referencias/`, `midia/` seguindo `INSTRUCOES-FICHAS.md`, `INSTRUCOES-REFERENCIAS.md`, `INSTRUCOES-MIDIA.md` |
| 6 | `validar.py --todos` | confere fichas e referências contra o vocabulário |
| 7 | `montar.py` | `dados/indice.jsonl`, `fichas.jsonl`, `grafo.json` e todas as páginas de `biblioteca/` |
| 8 | `pranchas.py --sem-antes` | refaz as pranchas sem os slides "antes" |
| extra | `fontes.py` | `dados/fontes.json` e `biblioteca/tipografia.md` |
| extra | `mapa.py` | dados e miniaturas do mapa visual (`_catalogo/mapa/`, abre com `_catalogo/Abrir mapa.command`); rode depois de `montar.py` |

Vocabulário: `dados/vocabulario.json`. Termo novo entra lá primeiro; depois rode `montar.py`.
Receitas de movimento e dicas de intenção escritas à mão: `biblioteca/movimentos/_receitas/` e `biblioteca/intencoes/_dicas/` (o `montar.py` junta nas páginas).
