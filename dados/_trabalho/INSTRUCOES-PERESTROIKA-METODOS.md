# Fichas de método da Perestroika: instruções para os agentes

Objetivo: transformar a leitura dos PDFs da Perestroika em fichas `.md` que um modelo de IA consulta no meio de uma criação (apresentação, carrossel, vídeo, aula, workshop, evento) e consegue aplicar sem ler o material original.

Fontes, em ordem:
1. `perestroika/_trabalho/leitura/<slug>.md`: o que cada PDF ensina, com páginas.
2. `perestroika/_trabalho/leitura/<slug>.jsonl`: texto e descrição de cada página (procure pelo campo `conceitos`).
3. A página original, quando precisar conferir: `perestroika/_trabalho/paginas/<slug>/pNNN.jpg`.
4. Para ligar com o Repertório: `biblioteca/principios/narrativa.md`, `biblioteca/principios/direcao-de-arte.md`, `biblioteca/vocabulario.md` (técnicas e intenções) e os guias em `biblioteca/guias/` (`abertura`, `agenda-e-divisores`, `impacto-e-destaque`, `apresentar-pessoas`, `explicar-e-sequenciar`, `agrupar-e-comparar`, `provar-com-dados`, `mostrar-e-localizar`, `fechamento`, `formatos-e-carrossel`).

Destino: `biblioteca/metodos/perestroika/conceitos/<id>.md` (conceitos) e `biblioteca/metodos/perestroika/modelos/<id>.md` (modelos para preencher). O agente abre cada uma com `get_guide("perestroika/<id>")`.

## Ficha de conceito

```markdown
# Nome do conceito

Perestroika, <material> (<grupo, ex.: Experience Learning, Metodologia de Conteúdo, ponto 2>). Fonte: `<slug>` p7-16[, `<slug>` pN].

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

## Exemplo da Perestroika
Reescrito com suas palavras, com a página. Citação literal só curta (até 25 palavras), entre aspas.

## Em cada formato
- **Apresentação:** ...
- **Carrossel ou post:** ...
- **Vídeo:** ...
- **Aula, workshop ou evento:** ...
(Omita o formato em que o conceito não se aplica.)

## Liga com
- No Repertório: princípio, técnica (`id`), guia (`get_guide("...")`) que se apoiam no conceito, com uma frase de por quê.
- Outras fichas: `perestroika/<id>`.
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

## Exemplo da Perestroika
O exemplo do material, preenchido (reescrito, com página).

## Exemplo aplicado
O mesmo modelo preenchido para um tema de negócio comum (ex.: atendimento ao cliente com IA, onboarding de equipe, lançamento de produto), para mostrar a transferência.

## Modelo em branco
Bloco pronto para o modelo copiar e preencher.
```

## Regras

- Português do Brasil, frases curtas, linguagem simples. Nunca use travessão nem meia-risca (os traços longo e médio); use vírgula, dois-pontos, parênteses ou ponto. Intervalos com hífen simples ("p7-16").
- Fiel ao material: nada inventado. Quando acrescentar uma aplicação que não está na fonte (por exemplo, como levar o conceito a um carrossel), marque com "Aplicação no Repertório:" no começo da frase.
- Material de terceiros: explique com suas palavras e cite páginas; nunca copie parágrafos.
- Escreva para o modelo agir: cada ficha precisa mudar uma decisão de criação.
- Ids em minúsculas com hífen, iguais aos da lista de conceitos da leitura (sem o prefixo `novo:`).
- Tamanho: 40 a 120 linhas por ficha. Conceitos pequenos podem ser mais curtos; não encha.
- Ao terminar, rode: `grep -rlP "\x{2014}|\x{2013}" biblioteca/metodos/perestroika` (deve sair vazio) e confira que todo `perestroika/<id>` citado existe.
