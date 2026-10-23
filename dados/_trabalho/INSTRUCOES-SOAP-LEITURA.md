# Leitura do SOAP: instruções para os agentes

Objetivo: ler cada página dos materiais da agência SOAP (e-books, guias, checklists e templates de PowerPoint), texto e imagem, e produzir dois arquivos por PDF. Eles alimentam (a) as fichas de método em `.md` que os modelos vão consultar e (b) o espaço visual SOAP do app.

O SOAP é uma agência de apresentações corporativas. O material ensina a montar o roteiro, desenhar os slides, falar em público, vender, fazer pitch, organizar eventos e se comunicar dentro da empresa (liderança, RH, feedback). Os templates são apresentações prontas para preencher.

## Onde está o material

- Páginas renderizadas: `_originais/soap/_trabalho/paginas/<slug>/pNNN.jpg` (1600 px no lado maior).
- Folhas de contato (6 páginas por imagem, numeradas no canto): `_originais/soap/_trabalho/folhas/<slug>_NN.jpg`. Comece por elas.
- Texto extraído do PDF por página: `_originais/soap/_trabalho/texto/<slug>.txt`. Cerca de 400 páginas não têm texto extraível (o texto está na imagem): nesses decks a leitura é visual.
- Inventário (slug, arquivo, páginas, páginas sem texto): `_originais/soap/_trabalho/inventario.json`.
- Vocabulário visual: `_originais/soap/_trabalho/VOCABULARIO.md`.
- Templates (`template-*`, `presente-*`) foram exportados do PowerPoint para PDF; o PowerPoint de origem saiu do projeto na limpeza de 23/10/2026.

Abra a folha de contato com a ferramenta de leitura de arquivos. Quando uma página tiver texto pequeno, tabela ou diagrama, abra a página inteira (`paginas/<slug>/pNNN.jpg`). Não pule páginas. Use o `.txt` para conferir a grafia, mas descreva o que a página mostra pela imagem.

## Saída 1: `_originais/soap/_trabalho/leitura/<slug>.jsonl`

Uma linha JSON por página, na ordem, com estes campos:

```json
{"arquivo":"12-formas-de-diagramacao","pagina":9,
 "texto":"o que a página diz, completo e limpo, em português (inclua o texto que só aparece na imagem)",
 "visual":"como a página é construída: cores, tipografia, imagem, composição (1 a 2 frases)",
 "conceitos":["regra-dos-tercos"],
 "selecionar":true,
 "motivo":"",
 "ficha":{...}}
```

- `texto`: o conteúdo da página. Em página de texto corrido longo, pode resumir o que passar de 120 palavras, preservando listas, números, passos e exemplos. Em template, o texto de exemplo (ex.: "Título do slide", "Lorem ipsum") vira uma linha curta: `texto de exemplo: título, três tópicos e gráfico de barras`.
- `conceitos`: ids do assunto que a página ensina (ver "Ids de conceito" abaixo). Página sem ensinamento (capa, contato, divulgação): lista vazia.
- `selecionar`: `true` se a página vale como referência visual no espaço (tem uma ideia de composição que alguém pode transferir para outra peça). `false` para: contato, endereço, divulgação da agência ou de cursos, ficha técnica, parede de logos, retrato isolado, página vazia, página repetida, sumário sem desenho, texto corrido sem desenho. Em decks que repetem o mesmo modelo de página, selecione no máximo 2 exemplos de cada modelo. Meta: 15% a 35% das páginas nos e-books; nos templates, cada modelo de página diferente que tenha uma ideia transferível (capa, divisor, gráfico, linha do tempo, equipe, comparação), até 40%.
- `motivo`: quando `selecionar` é `false`, diga por quê em poucas palavras.
- `ficha`: só quando `selecionar` é `true`:

```json
{"titulo":"nome curto do slide (até 8 palavras)",
 "resumo":"o que é e como é, em 1 a 2 frases",
 "ideia":"a ideia transferível, no imperativo, em 1 frase (ex.: 'Corte a foto na diagonal e use o triângulo que sobra para o título.')",
 "como_funciona":"como a composição conduz o olhar (1 a 3 frases)",
 "intencoes":["EXPLICAR"],"tecnicas":["linha-guia","numeracao"],"movimento":["estatico"],
 "estetica":["corporativo","claro"],"tom":["tecnico"],"forca":3,
 "bom_para":["processo em quatro etapas","carrossel de passos"]}
```

`forca`: 1 a 5, quão bom e transferível é o slide como referência (5 = exemplar raro; um template genérico de banco de imagens raramente passa de 3). Use só ids do `VOCABULARIO.md`. Quando um e-book mostra exemplos de "antes e depois" ou de "certo e errado", selecione a página que mostra o certo, ou a comparação inteira se ela for o ensinamento.

## Saída 2: `_originais/soap/_trabalho/leitura/<slug>.md`

Resumo do PDF para quem vai escrever as fichas de método. Seções:

1. **O que é** (2 a 3 linhas: tipo de material, público, ano se aparecer, parceiros citados).
2. **O que ensina**: cada conceito, método, ferramenta, regra, lista numerada ou checklist encontrado, com a explicação fiel ao material (com suas palavras), as páginas (`p12-14`) e o id do conceito entre crases. Aqui está o valor: seja completo e preciso. Inclua os exemplos que o material dá, os passos, os números (tempos, proporções, quantidades), as perguntas, as tabelas e os modelos de preenchimento (descreva campos e estrutura). Nos templates, descreva a sequência de slides que o template propõe (ex.: capa, problema, solução, números, equipe, próximos passos) e os modelos de página: isso também é método.
3. **Frases-chave**: até 8 citações curtas (no máximo 25 palavras cada), com página.
4. **Linguagem visual do deck**: paleta (hex aproximado), tipografia (estilo; nome se reconhecer), modelos de página que se repetem, o que é marcante.
5. **Ficha do deck** (para a referência principal do espaço), em JSON: `{"titulo","resumo","ideia","como_funciona","intencoes","tecnicas","movimento","estetica","tom","forca","bom_para","capa":N}`, onde `capa` é a página que melhor representa o deck no mapa.
6. **Repetições**: páginas iguais ou quase iguais a outro material do seu lote (ex.: dica que aparece em 2018 e 2019), com slug e página dos dois lados.
7. **Ids de conceito usados**: cada id que você usou, com uma linha dizendo o que é.
8. **Páginas puladas ou duvidosas**, com o motivo.

## Ids de conceito

Não há lista fechada: crie ids curtos, em minúsculas com hífen, que nomeiem o ensinamento, não a página (`regra-dos-tercos`, `pitch-para-investidores`, `contato-visual`, `feedback-sanduiche`, `comunicacao-interna`). Um id por ideia que mereça uma ficha própria; não crie um id para cada dica solta (agrupe dicas do mesmo assunto, ex.: `postura-e-gestos`). Reaproveite seus próprios ids entre os PDFs do lote.

Quando o assunto já existir no método da Perestroika, use o mesmo id: `tese`, `tagline`, `inicio-meio-fim`, `planejamento-da-apresentacao`, `design-de-slide`, `design-de-informacao`, `ensaio-e-finalizacao`, `storytelling`, `objecao-na-voz-do-publico`, `formatos-de-encontro`, `feedback-de-aprendizagem-rapida`, `check-in-check-out`, `escola-corporativa`, `pesquisa-de-tendencias`. O redator une os ids de todos os leitores depois.

## Regras

- Português do Brasil. Nunca use travessão nem meia-risca (os caracteres de traço longo e médio); use vírgula, dois-pontos ou parênteses. O `.txt` extraído pode trazer esses caracteres: troque-os ao copiar.
- Material de terceiros: no `.md`, explique com fidelidade e cite página; citações literais só nas Frases-chave, curtas.
- Não invente: se não der para ler, diga `ilegível` e siga.
- Retratos de pessoas reais: descreva o papel ("retrato de executivo", "foto de banco de imagens"), sem identificar ninguém além do nome que estiver escrito na página.
- Páginas de divulgação da SOAP (cursos, serviços, "fale conosco", redes sociais) entram no `.jsonl` com `selecionar:false` e `motivo:"divulgação"`; no `.md`, só uma linha.
- Grave os arquivos com a ferramenta de escrita, um PDF de cada vez (termine o `.jsonl` e o `.md` de um PDF antes de abrir o próximo). Se precisar de script (por exemplo, para conferir o JSON), use só a pasta `_originais/soap/_trabalho/tmp/<seu-lote>/`: outro leitor pode estar usando outro nome de arquivo na pasta comum.
- Ao terminar cada PDF, confira que o `.jsonl` tem exatamente uma linha por página, que todo JSON é válido e que só há ids do vocabulário nas fichas. Comando pronto: `app/.venv/bin/python -I ferramentas/incorporar_colecao.py soap conferir <slug>`.
