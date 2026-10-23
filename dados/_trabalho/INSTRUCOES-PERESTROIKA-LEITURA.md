# Leitura da Perestroika: instruções para os agentes

Objetivo: ler cada página dos PDFs da Perestroika (texto e imagem) e produzir dois arquivos por PDF. Eles alimentam (a) as fichas de método em `.md` que os modelos vão consultar e (b) o espaço visual Perestroika do app.

## Onde está o material

- Páginas renderizadas: `perestroika/_trabalho/paginas/<slug>/pNNN.jpg` (até 1600 px).
- Folhas de contato (6 páginas por imagem, numeradas no canto): `perestroika/_trabalho/folhas/<slug>_NN.jpg`. Comece por elas.
- Texto extraído do PDF por página: `perestroika/_trabalho/texto/<slug>.txt` (incompleto: metade das páginas tem texto só na imagem).
- Vocabulário visual: `perestroika/_trabalho/VOCABULARIO.md`.

Abra a folha de contato com a ferramenta de leitura de arquivos. Quando uma página tiver texto pequeno ou um diagrama, abra a página inteira (`paginas/<slug>/pNNN.jpg`). Não pule páginas.

## Saída 1: `perestroika/_trabalho/leitura/<slug>.jsonl`

Uma linha JSON por página, na ordem, com estes campos:

```json
{"arquivo":"04-forma","pagina":7,
 "texto":"o que a página diz, completo e limpo, em português (inclua o texto que só aparece na imagem)",
 "visual":"como a página é construída: cores, tipografia, imagem, composição (1 a 2 frases)",
 "conceitos":["design-de-informacao"],
 "selecionar":true,
 "motivo":"",
 "ficha":{...}}
```

- `conceitos`: ids da lista abaixo que a página trata. Conceito que não está na lista: crie um id curto em minúsculas com hífen e prefixo `novo:` (ex.: `novo:coolhunting`).
- `selecionar`: `true` se a página vale como referência visual no espaço (tem uma ideia de composição que alguém pode transferir para outra peça). `false` para: preço, endereço, contato, ficha técnica, parede de logos, retrato isolado de professor, página vazia, página repetida, texto corrido sem desenho. Em decks que repetem o mesmo modelo de página muitas vezes, selecione no máximo 2 exemplos de cada modelo. Meta: 20% a 40% das páginas.
- `motivo`: quando `selecionar` é `false`, diga por quê em poucas palavras.
- `ficha`: só quando `selecionar` é `true`:

```json
{"titulo":"nome curto do slide (até 8 palavras)",
 "resumo":"o que é e como é, em 1 a 2 frases",
 "ideia":"a ideia transferível, no imperativo, em 1 frase (ex.: 'Escreva o número do capítulo em tamanho gigante e meio apagado atrás do título.')",
 "como_funciona":"como a composição conduz o olhar (1 a 3 frases)",
 "intencoes":["DIVIDIR"],"tecnicas":["numeracao","palavra-fantasma"],"movimento":["estatico"],
 "estetica":["editorial","colorido"],"tom":["energetico"],"forca":3,
 "bom_para":["divisor de capítulo em treinamento","carrossel com passos numerados"]}
```

`forca`: 1 a 5, quão bom e transferível é o slide como referência (5 = exemplar raro). Use só ids do `VOCABULARIO.md`.

## Saída 2: `perestroika/_trabalho/leitura/<slug>.md`

Resumo do PDF para quem vai escrever as fichas de método. Seções:

1. **O que é** (2 a 3 linhas: tipo de material, público, ano se aparecer).
2. **O que ensina**: cada conceito, método, ferramenta ou regra encontrada, com a explicação fiel ao material (com suas palavras), as páginas (`p12-14`) e o id do conceito. Aqui está o valor: seja completo e preciso. Inclua os exemplos que o material dá, os passos, as perguntas, as tabelas e os modelos de preenchimento (descreva campos e estrutura).
3. **Frases-chave**: até 8 citações curtas (no máximo 25 palavras cada), com página.
4. **Linguagem visual do deck**: paleta (hex aproximado), tipografia (estilo; nome se reconhecer), modelos de página que se repetem, o que é marcante.
5. **Ficha do deck** (para a referência principal do espaço), em JSON: `{"titulo","resumo","ideia","como_funciona","intencoes","tecnicas","movimento","estetica","tom","forca","bom_para","capa":N}`, onde `capa` é a página que melhor representa o deck no mapa.
6. **Páginas puladas ou duvidosas**, com o motivo.

## Lista de conceitos conhecidos

Experience Learning: `autoralidade`, `tese`, `entrega-minima`, `fator-dia-seguinte`, `ignite`, `mapa-conectivo`, `nao-e-palestra-e-aula`, `design-de-informacao`, `tagline`, `treco`, `fluxo-ttt`, `check-in-check-out`, `hosting`, `aula-inaugural`, `happy-hour-festa-final`, `ambiente-criativo`, `empoderamento-criativo`, `arco`, `framework-de-curso`, `framework-de-aula`, `checkpoint`, `modulo-vivencial`, `projetos-banca-go-pro`, `experience-learning` (visão geral, pilares, origem).

Mapa do Storytelling (8 cartas): `catraca`, `tenho-dados`, `didatismo-na-veia`, `sou-foda`, `poder-de-escuta`, `quebra-gelo`, `vulnerabilidade`, `fator-surpresa`.

Checklist e Chora PPT: `planejamento` (formato, tempo, público, tese), `inicio-meio-fim`, `menos-e-mais`, `cor-com-funcao`, `fontes-funcionais`, `alinhamento`, `contraste-protagonista`, `imagens-e-icones`, `animacoes-discretas`, `ensaio`, `layout`, `graficos`, `storytelling`, `performance-oratoria`.

## Regras

- Português do Brasil. Nunca use travessão nem meia-risca (os caracteres de traço longo e médio); use vírgula, dois-pontos ou parênteses.
- Material de terceiros: no `.md`, explique com fidelidade e cite página; citações literais só nas Frases-chave, curtas.
- Não invente: se não der para ler, diga `ilegível` e siga.
- Retratos de pessoas reais: descreva o papel ("retrato de professor"), sem identificar ninguém além do nome que estiver escrito na página.
- Grave os arquivos com a ferramenta de escrita. Ao terminar, confira que o `.jsonl` tem exatamente uma linha por página e que todo JSON é válido.
