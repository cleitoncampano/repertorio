# Fichas de método do SOAP: instruções para os agentes

Objetivo: transformar a leitura dos materiais da agência SOAP em fichas `.md` que um modelo de IA consulta no meio de uma criação (apresentação, pitch, proposta, carrossel, vídeo, fala ao vivo, evento, comunicação interna) e consegue aplicar sem ler o material original.

Fontes, em ordem:
1. `soap/_trabalho/leitura/<slug>.md`: o que cada PDF ensina, com páginas.
2. `soap/_trabalho/leitura/<slug>.jsonl`: texto e descrição de cada página (procure pelo campo `conceitos`).
3. A página original, quando precisar conferir: `soap/_trabalho/paginas/<slug>/pNNN.jpg`.
4. Para ligar com o Repertório: `biblioteca/principios/narrativa.md`, `biblioteca/principios/direcao-de-arte.md`, `biblioteca/vocabulario.md` (técnicas e intenções) e os guias em `biblioteca/guias/` (`abertura`, `agenda-e-divisores`, `impacto-e-destaque`, `apresentar-pessoas`, `explicar-e-sequenciar`, `agrupar-e-comparar`, `provar-com-dados`, `mostrar-e-localizar`, `fechamento`, `formatos-e-carrossel`).
5. O método da Perestroika, que já cobre parte dos assuntos: índice em `biblioteca/metodos/perestroika/guias/metodo-perestroika.md` e fichas em `biblioteca/metodos/perestroika/conceitos/` e `modelos/`.

Destino: `biblioteca/metodos/soap/conceitos/<id>.md` (conceitos) e `biblioteca/metodos/soap/modelos/<id>.md` (modelos para preencher). O agente abre cada uma com `get_guide("soap/<id>")`. A lista de fichas de cada redator, com os ids e os PDFs de origem, vem no pedido.

## Ficha de conceito

```markdown
# Nome do conceito

SOAP, <material> (<assunto>). Fonte: `<slug>` p7-16[, `<slug>` pN].

**Em duas linhas.** O que é e para que serve, sem jargão.

## Quando usar
- 2 a 4 situações concretas de criação em que o conceito decide algo.

## Como aplicar
1. Passos que um modelo executa. Verbos no imperativo. Inclua números, tempos e proporções quando o material der.

## Perguntas
- Para você: perguntas que o modelo responde sozinho a partir do pedido.
- Para o usuário: só o que não dá para deduzir (no máximo 2).

## Deu certo quando
- Sinais verificáveis na peça pronta.

## Erros comuns
- O que o material critica ou o que derruba o conceito na prática.

## Exemplo do SOAP
Reescrito com suas palavras, com a página. Citação literal só curta (até 25 palavras), entre aspas.

## Exemplo aplicado
Aplicação no Repertório: o conceito aplicado ao tema que o pedido indicou para esta ficha (4 a 10 linhas).

## Em cada formato
- **Apresentação:** ...
- **Fala ao vivo:** ...
- **Carrossel ou post:** ...
- **Vídeo:** ...
(Omita o formato em que o conceito não se aplica.)

## Liga com
- No Repertório: princípio, técnica (`id`), guia (`get_guide("...")`) que se apoiam no conceito, com uma frase de por quê.
- Outras fichas: `soap/<id>`, `perestroika/<id>`.
```

## Modelo para preencher

```markdown
# Nome do modelo

Para que serve, em 2 linhas. Fonte: `<slug>` pN.

## Campos
| campo | o que escrever | tamanho |
|---|---|---|

## Como preencher
1. Ordem dos campos e critérios de qualidade de cada um.

## Exemplo do SOAP
O exemplo do material, preenchido (reescrito, com página). Se o material não traz exemplo, diga isso em uma linha.

## Exemplo aplicado
Aplicação no Repertório: o modelo preenchido para o tema que o pedido indicou para esta ficha.

## Modelo em branco
Bloco pronto para o modelo copiar e preencher.
```

## Quando o assunto já está na Perestroika

Tese, tagline, início, meio e fim, planejamento da apresentação, design de slide, ensaio e finalização, objeção na voz do público, formatos de encontro, checklist de apresentação e avaliação de reação já têm ficha `perestroika/<id>`. Nesses assuntos:

- A ficha SOAP traz só o que é próprio do SOAP (a regra, o número, a lista, o exemplo, o ângulo diferente) e começa a seção "Liga com" pela ficha da Perestroika, dizendo em uma frase o que cada uma cobre.
- Não repita a explicação da Perestroika. Se o SOAP não acrescenta nada, não crie a ficha: diga isso no relatório final.
- Se as duas fontes discordam (ex.: tempo de abertura, número de slides), escreva a regra do SOAP e registre a diferença numa linha: "A Perestroika pede X; o SOAP pede Y. Escolha pelo formato: ...".
- Não use para a ficha SOAP um id igual ao de uma ficha da Perestroika; nomeie pelo ângulo do SOAP (ex.: `roteiro-vencedor`, não `tese`).

## Exemplos aplicados com temas diferentes

Cada ficha recebe no pedido um tema próprio para o exemplo aplicado. Use exatamente esse tema, com nomes, números e situações inventados para ele. Nunca use atendimento ao cliente com IA, Growmate, cVortex ou o próprio Repertório. Os testes da Perestroika mostraram que, quando todos os exemplos falam do mesmo tema, os agentes copiam o exemplo em vez de aplicar o método.

## Regras

- Português do Brasil, frases curtas, linguagem simples. Nunca use travessão nem meia-risca (os traços longo e médio); use vírgula, dois-pontos, parênteses ou ponto. Intervalos com hífen simples ("p7-16").
- Fiel ao material: nada inventado. Quando acrescentar uma aplicação que não está na fonte (por exemplo, como levar o conceito a um carrossel), marque com "Aplicação no Repertório:" no começo da frase. O exemplo aplicado inteiro já é aplicação.
- Material de terceiros: explique com suas palavras e cite páginas; nunca copie parágrafos.
- Escreva para o modelo agir: cada ficha precisa mudar uma decisão de criação.
- Cite fichas sempre como `` `soap/<id>` `` ou `` `perestroika/<id>` ``, nunca pelo caminho do arquivo. Guias do Repertório como `get_guide("abertura")`.
- Conceito e modelo nunca com o mesmo id. Modelo ganha nome de objeto (`roteiro-de-pitch`, `matriz-tosw`); conceito, nome de ideia (`pitch-para-investidores`, `analise-tosw`).
- Ids em minúsculas com hífen, os da lista do pedido.
- Tamanho: 40 a 120 linhas por ficha. Conceitos pequenos podem ser mais curtos; não encha.
- Se precisar de script, use só a pasta `soap/_trabalho/tmp/<seu-grupo>/`.
- Ao terminar, rode `app/.venv/bin/python -I ferramentas/incorporar_colecao.py soap validar` e corrija o que for das suas fichas (fichas citadas que ainda não existem porque outro redator está escrevendo podem aparecer: confira contra a lista completa de ids do pedido).
- Relatório final (na resposta, não em arquivo): fichas escritas, fichas da lista que não criou e por quê, contradições com a Perestroika encontradas, e ids citados de outros grupos.
