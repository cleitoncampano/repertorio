# Método SOAP no Repertório

O material da agência SOAP (pasta `soap/`, fora do Git e dos pacotes: 55 e-books e guias, 3 checklists, 16 templates de PowerPoint e o kit de aprovação de projeto) virou três coisas que os modelos usam:

| o quê | onde | como o agente chega |
|---|---|---|
| Guias de entrada | `guias/` | `get_guide("metodo-soap")` (índice), `apresentar-ao-vivo`, `pitch-e-proposta`, `comunicacao-na-empresa`; camada SOAP no guia `revisao-apresentacao` da Perestroika |
| Fichas de conceito | `conceitos/<ficha>.md` | `get_guide("soap/<ficha>")`, indicadas pelo índice |
| Modelos para preencher | `modelos/<ficha>.md` | `get_guide("soap/<ficha>")` |
| Slides como referência visual | espaço **SOAP** no app (75 apresentações, 500 slides; 7 páginas do template de gráficos com texto sobreposto ficaram de fora, `SOAP_SKIP` na ferramenta) | `search_references` com o espaço SOAP |
| Skills | `~/.agents/skills/soap-fala` e `soap-pitch` (ligadas em `~/.claude/skills`); a `perestroika-revisao` usa o checklist SOAP como camada extra | disparam sozinhas pelo pedido; aparecem no catálogo de Skills do app, categoria Método |

O serviço lê `guias/` como guias e `conceitos/` e `modelos/` como fichas (`app/server/repertorio/service.py`, `guide_files` e `method_files`). Guias de coleções diferentes dividem o mesmo espaço de nomes: um guia novo não pode ter o nome de outro (`validar` confere).

## Como foi feito e como refazer

Plano e andamento em `docs/SOAP-PLANO.md`. Ferramenta: `ferramentas/incorporar_colecao.py soap <comando>`.

1. Templates `.ppt` e `.pptx` exportados para PDF pelo PowerPoint (o de gráficos pelo Keynote, porque o PowerPoint o exportava incompleto) em `soap/_trabalho/pdf-templates/`; a planilha do kit transcrita em `soap/_trabalho/kit-express/`.
2. `paginas`: renderiza as 1.755 páginas, o texto por página e as folhas de contato em `soap/_trabalho/`.
3. Leitura página por página (texto e imagem) por 10 agentes, com `dados/_trabalho/INSTRUCOES-SOAP-LEITURA.md`; `conferir` valida. Saída em `soap/_trabalho/leitura/` (fora do Git); o resumo de cada PDF fica também em `_referencias/soap/<slug>.md`. Lotes e conclusões em `soap/_trabalho/relatorios/`.
4. `montar` grava `dados/soap/decks.jsonl` e copia as páginas para `_originais/soap/`; `pranchas` gera a conferência em `app/.runtime/qa/soap/`; depois `./app/run.sh import-decks --workspace ID --folder dados/soap`.
5. Fichas escritas por 5 redatores com `dados/_trabalho/INSTRUCOES-SOAP-METODOS.md` e a lista `soap/_trabalho/relatorios/fichas.md` (um tema diferente por ficha para o exemplo aplicado). Guias de entrada escritos à mão sobre as fichas. `validar` confere travessão, nomes repetidos, fichas e guias citados e links de slide (`%23`).

## Cuidados

- Material de terceiros: as fichas explicam o método com palavras próprias e citam a página; as referências entram com `reusable=false`. Não incluir em pacotes de demonstração ou venda.
- Os templates de presente (2014 a 2017) liberam copiar elementos para as próprias apresentações, sem licença formal nem redistribuição, e as fotos vêm de bancos cujas licenças não acompanham o arquivo; a observação está nas fichas. O template de gráficos usa imagens de terceiros sem crédito.
- O que é aplicação do Repertório (e não da fonte) vem marcado com "Aplicação no Repertório". As diferenças com a Perestroika estão registradas em cada ficha e resumidas no índice `metodo-soap`.
- Erros do material corrigidos com ressalva nas fichas: David A. Kolb (não "Charles"), Kirkpatrick de 1959, Mehrabian de 1967 e restrito a sentimentos ambíguos, frase atribuída a Darwin.
- Repetições: Dicas 2018 e 2019, Tendências 2018 e 2020, as quatro partes do guia do RH e o template Copa (igual ao de aprovação de projeto) repetem conteúdo; as fichas citam as duas fontes.
