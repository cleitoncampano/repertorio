# Método Perestroika no Repertório

O material da escola Perestroika (pasta `perestroika/`, fora do Git e dos pacotes) virou três coisas que os modelos usam:

| o quê | onde | como o agente chega |
|---|---|---|
| Guias de entrada | `guias/` | `get_guide("metodo-perestroika")` (índice), `aula-e-workshop`, `curso-e-programa`, `encontro-e-evento`, `revisao-apresentacao` |
| Fichas de conceito | `conceitos/<ficha>.md` | `get_guide("perestroika/<ficha>")`, indicadas pelo índice |
| Modelos para preencher | `modelos/<ficha>.md` | `get_guide("perestroika/<ficha>")` |
| Slides como referência visual | espaço **Perestroika** no app (23 apresentações, 191 slides; o vídeo de abertura do Chora PPT saiu do espaço a pedido do Cleiton em 23/10/2026) | `search_references` com o espaço Perestroika |
| Skills | `~/.agents/skills/perestroika-tese`, `perestroika-experiencia`, `perestroika-revisao` (ligadas em `~/.claude/skills`) | disparam sozinhas pelo pedido; aparecem no catálogo de Skills do app, categoria Método |

O serviço lê `guias/` como guias e `conceitos/` e `modelos/` como fichas (`app/server/repertorio/service.py`, `guide_files` e `method_files`). O bloco de instruções gerado por `connect --write-instructions` cita `metodo-perestroika` só quando este índice existe.

## Como foi feito e como refazer

1. Páginas renderizadas e lidas uma a uma (texto e imagem) por agentes, com `dados/_trabalho/INSTRUCOES-PERESTROIKA-LEITURA.md`. Saída em `perestroika/_trabalho/leitura/` (fora do Git); o resumo de cada PDF fica também em `_referencias/perestroika/<slug>.md`.
2. Fichas e modelos escritos a partir da leitura com `dados/_trabalho/INSTRUCOES-PERESTROIKA-METODOS.md`. Os guias de entrada foram escritos à mão sobre as fichas.
3. Espaço visual: `app/.venv/bin/python -I ferramentas/incorporar_perestroika.py montar` (grava `dados/perestroika/`, copia as páginas para `_originais/perestroika/`), `... pranchas` para conferir, depois `./app/run.sh import-decks --workspace ID --folder dados/perestroika`.

## Cuidados

- Material de terceiros: as fichas explicam o método com palavras próprias e citam a página; as referências entram com `reusable=false`. Não incluir em pacotes de demonstração ou venda.
- O que é aplicação do Repertório (e não da fonte) vem marcado com "Aplicação no Repertório".
- O Mood SP é cópia do Mood RIO e ficou fora do espaço; o "Swag" é um curso de skate e o "Tetris" é de pesquisa e comportamento, ao contrário do que diz o `perestroika/INDICE_MATERIAIS.md` antigo.
