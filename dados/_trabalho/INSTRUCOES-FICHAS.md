# Como escrever as fichas do acervo acervo

Você vai olhar arquivos de apresentação (miniaturas numeradas numa prancha) e escrever uma ficha JSON para cada um.
A ficha é lida depois por modelos de IA que vão CRIAR apresentações novas, para qualquer tema e qualquer marca.
Então o valor da ficha está em responder: **o que dá para aprender aqui e reaplicar em outro contexto?**
Descrever o que está na tela é só o começo; o ouro é a ideia transferível e o como fazer.

## O que você recebe por lote

- `dados/_trabalho/lotes/lote-NNN.json`: lista de pacotes. Cada pacote tem título, grupo do curso, nº de slides,
  slides ocultos, proporção, paleta extraída, fontes, contagem de transições, a análise automática do Morph
  (`morph_auto`: o que cresce, para onde vai, quantos objetos entram e saem) e o título de cada slide.
- As imagens listadas em `imagens` do lote: pranchas com todos os slides numerados (número no canto; vermelho = slide oculto).
- A miniatura às vezes não mostra o efeito (é uma foto estática feita pelo Mac). Por isso cada slide do pacote pode trazer `alertas` tirados do próprio arquivo: `video`, `3d`, `texto com imagem dentro`, `texto vazado ou invisível`, `texto em degradê`, `forma preenchida com imagem (máscara)`, `recorte feito no PowerPoint (fundo removido)`, `efeito artístico na imagem`, `gráfico`. Use esses sinais na descrição. Quando a prancha contradiz um alerta importante e isso muda a ficha, você pode ler o XML do slide só para consulta (`unzip -p "<arquivo do pacote>" ppt/slides/slideN.xml | head -c 20000`), mas faça isso só quando valer a pena. Se a miniatura não mostra o efeito, diga isso no `como_funciona`.

Leia o lote e TODAS as imagens dele na mesma rodada (chamadas em paralelo). Depois escreva o arquivo de saída numa única gravação.

## O que você entrega

Um arquivo `dados/_trabalho/fichas/lote-NNN.json` com uma lista JSON de fichas, uma por pacote, na mesma ordem.
JSON válido, em português do Brasil, sem travessão nem meia-risca (os traços longos de pontuação): use vírgula, dois-pontos ou ponto.

## Campos da ficha

| campo | o que é |
|---|---|
| `id` | o id do pacote, igual |
| `tipo` | `modelo` (arquivo com vários slides de tipos diferentes formando uma apresentação com identidade própria, mesmo que temático, como um calendário: templates e PDFs do Canva), `componente` (peça reaproveitável de layout: gráfico, linha do tempo, mapa, organograma, tabela, padrão de fundo) ou `efeito` (demonstração de um truque visual ou de movimento) |
| `resumo` | 1 frase: o que é, visualmente |
| `antes` | lista dos slides que não servem de referência final: a versão "comum" antes do efeito (geralmente o slide 1, mas às vezes vem no fim) e slides de montagem (forma vazia, peças ainda separadas, estado de partida sem conteúdo). `[]` se não houver. Esses slides serão escondidos da busca, então marque com cuidado |
| `ideia` | 1 ou 2 frases no imperativo com o princípio reaproveitável em QUALQUER tema, sem citar o assunto do exemplo. Ex.: "Transforme o objeto central do tema num personagem que gira e se aproxima a cada slide." |
| `como_funciona` | 2 a 4 frases concretas: o que está onde, o que se move, de onde para onde, em que ordem. Use a análise do Morph + o que você vê |
| `html` | 1 a 3 frases: como reproduzir numa apresentação HTML (CSS/JS). Na biblioteca existe um motor que faz Morph por `data-m` (elementos com o mesmo `data-m` em slides seguidos se transformam um no outro), passos de revelação por `data-passo` e máscara por `clip-path`. Cite técnicas reais: clip-path, mask-image, mix-blend-mode, background-clip:text, backdrop-filter, View Transitions, model-viewer, SVG stroke-dashoffset, etc. |
| `intencoes` | 1 a 3 ids de intenção do arquivo como um todo (ver vocabulário) |
| `tecnicas` | 1 a 5 ids de técnica (ver vocabulário). Se nenhuma servir de verdade, use `"nova:nome-curto"` |
| `movimento` | 0 a 3 ids de família de movimento. Confira com a prancha: a análise automática erra às vezes |
| `estetica` | 2 a 5 rótulos da lista de estéticas |
| `tom` | 1 a 3 tons |
| `bom_para` | 2 a 4 contextos concretos de uso (tipo de palestra, público, momento da apresentação) |
| `cuidados` | 1 frase: quando evitar, o que não copiar, ou o risco (texto miúdo, depende de foto boa, cansa se repetir...) |
| `destaques` | os números dos 1 a 3 slides mais fortes como referência (nunca um slide do `antes`) |
| `forca` | 1 a 5. 5 = referência de nível internacional, ideia forte e execução impecável; 4 = muito bom; 3 = sólido mas comum; 2 = datado ou genérico; 1 = fraco |
| `slides` | uma entrada por slide, inclusive ocultos e os do `antes`: `{"n": 3, "intencao": "AGRUPAR", "tecnicas": ["grade-modular"], "nota": "curta, o que este slide tem de específico"}`. `intencao` é um id de intenção, ou `ANTES` para slide de antes, ou `OCULTO` para oculto sem uso. `tecnicas` 0 a 3. `nota` até 120 caracteres |

## Vocabulário

Use somente os ids de `dados/vocabulario.json` (intenções, técnicas, movimentos, estéticas, tons). Resumo dos ids:

- intenções: ABRIR, SITUAR, DIVIDIR, IMPACTAR, DESTACAR, CITAR, APRESENTAR, EXPLICAR, SEQUENCIAR, AGRUPAR, COMPARAR, PROVAR, MOSTRAR, LOCALIZAR, FECHAR
- técnicas: contraste-de-cor, contraste-de-escala, destaque-tipografico, isolamento, foco-seletivo, intruso, sangria-total, corte-radical, textura-e-materia, tipografia-como-imagem, palavra-fantasma, eco-tipografico, mascara-de-forma, profundidade-em-camadas, dado-como-heroi, rosto-que-encara, proximidade, similaridade, cor-por-capitulo, regiao-comum, conexao, grade-modular, sanfona, simetria-e-eixo, fechamento, hierarquia-de-leitura, numeracao, linha-guia, direcao-de-leitura, olhar-que-guia, revelacao-progressiva, camera-continua, sumario-navegavel, progressao-de-escala, padrao-e-quebra, metafora-visual, dupla-exposicao, trompe-loeil, transformacao, escala-impossivel, escala-inversa, pergunta-aberta, emprestimo-de-codigo, interface-imitada, referencia-cultural, quebra-de-moldura, inversao-figura-fundo, objeto-como-suporte
- movimentos: zoom-mergulho, zoom-recuo, panorama, voo, reorganizar, transformacao, texto, giro, revelacao, troca, escalonado, foco, loop, contagem, estatico
- estéticas: minimalista, editorial, revista, corporativo, tecnologico, futurista, neon, vintage, retro, organico, natureza, ludico, colorido, pastel, luxo, brutalista, suico, vidro, 3d, fotografico, preto-e-branco, ilustrado, colagem, escuro, claro, gradiente, monocromatico, alto-contraste, artesanal, cinematografico, esportivo, gastronomico, moda, infantil, cientifico, dados
- tons: serio, inspirador, divertido, tecnico, emocional, provocador, elegante, energetico, calmo, urgente, acolhedor, solene

As definições completas estão em `dados/vocabulario.json`; leia uma vez no início.

## Régua de qualidade: dois exemplos

Modelo (template de 20 slides):

```json
{"id": "002-26-0102-cinema", "tipo": "modelo",
 "resumo": "Modelo preto, branco e vermelho com fotos P&B, faixa vertical vermelha à esquerda e títulos condensados em caixa alta; fecha com uma tela curva de cinema onde o conteúdo troca.",
 "antes": [],
 "ideia": "Escolha um único acento de cor e aplique sempre na palavra-chave de cada título; todo o resto fica em preto, branco e fotos sem cor, e a repetição vira identidade.",
 "como_funciona": "Grade fixa em todos os slides: faixa vermelha à esquerda, rodapé com data e quadradinhos de navegação. Títulos em duas cores (branco e vermelho) e fotos sempre P&B. O Morph reorganiza as mesmas fotos entre slides (3 para 4, a do meio cresce), faz a palavra CINEMA crescer e trocar de lugar nos divisores (6 e 11) e mantém o painel curvo parado enquanto o conteúdo muda (16 a 19).",
 "html": "Tokens --acento e filter: grayscale(1) em todas as fotos; título com <em> na cor de acento. Painel curvo com clip-path em elipse; fotos com o mesmo data-m nos slides 16 a 19 para a câmera ficar parada e só o conteúdo trocar.",
 "intencoes": ["AGRUPAR", "PROVAR", "DIVIDIR"],
 "tecnicas": ["contraste-de-cor", "tipografia-como-imagem", "grade-modular", "camera-continua", "similaridade"],
 "movimento": ["reorganizar", "texto", "voo"],
 "estetica": ["cinematografico", "preto-e-branco", "alto-contraste", "escuro", "esportivo"],
 "tom": ["energetico", "serio"],
 "bom_para": ["palestra sobre esporte, performance ou superação", "apresentação de produtora, audiovisual ou evento", "pitch com muitas fotos e poucos dados"],
 "cuidados": "Muito texto miúdo nos slides de conteúdo; em palco, aumente o corpo e corte itens.",
 "destaques": [6, 16, 4],
 "forca": 4,
 "slides": [
  {"n": 1, "intencao": "ABRIR", "tecnicas": ["contraste-de-cor"], "nota": "setas vermelhas de claquete, título CINEMA em caixa branca, tira de fotos pequena"},
  {"n": 2, "intencao": "AGRUPAR", "tecnicas": ["hierarquia-de-leitura"], "nota": "título em duas cores, 4 tópicos em duas colunas, foto P&B vertical à direita"},
  {"n": 3, "intencao": "AGRUPAR", "tecnicas": ["grade-modular", "similaridade"], "nota": "três fotos de estátuas em linha com subtítulos vermelhos"},
  {"n": 4, "intencao": "DESTACAR", "tecnicas": ["contraste-de-escala"], "nota": "as mesmas três fotos se reorganizam e a do meio cresce"},
  {"n": 5, "intencao": "MOSTRAR", "tecnicas": ["sangria-total"], "nota": "foto de carro em movimento ocupa dois terços, título à direita"},
  {"n": 6, "intencao": "DIVIDIR", "tecnicas": ["tipografia-como-imagem", "profundidade-em-camadas"], "nota": "CINEMA gigante em vermelho e preto sobre foto de motocross"},
  {"n": 7, "intencao": "COMPARAR", "tecnicas": ["simetria-e-eixo"], "nota": "duas fotos lado a lado com títulos sobrepostos"},
  {"n": 8, "intencao": "MOSTRAR", "tecnicas": ["contraste-de-escala"], "nota": "foto grande do jogador e coluna de três fotos pequenas"},
  {"n": 9, "intencao": "AGRUPAR", "tecnicas": ["similaridade"], "nota": "título grande, coluna de fotos e lista com ícones vermelhos"},
  {"n": 10, "intencao": "PROVAR", "tecnicas": ["objeto-como-suporte", "dado-como-heroi"], "nota": "celular com foto e quatro percentuais em vermelho"},
  {"n": 11, "intencao": "DIVIDIR", "tecnicas": ["tipografia-como-imagem"], "nota": "variação do divisor 6 com a palavra cortada pela borda"},
  {"n": 12, "intencao": "PROVAR", "tecnicas": ["dado-como-heroi"], "nota": "pictogramas de pessoas com 40% e 80%"},
  {"n": 13, "intencao": "PROVAR", "tecnicas": ["grade-modular"], "nota": "três preços em colunas"},
  {"n": 14, "intencao": "MOSTRAR", "tecnicas": ["grade-modular"], "nota": "galeria de três fotos horizontais, título embaixo"},
  {"n": 15, "intencao": "COMPARAR", "tecnicas": ["regiao-comum"], "nota": "tabela de planos com cabeçalho vermelho"},
  {"n": 16, "intencao": "IMPACTAR", "tecnicas": ["camera-continua", "tipografia-como-imagem"], "nota": "tela curva de cinema com três fotos e CINEMA vermelho"},
  {"n": 17, "intencao": "AGRUPAR", "tecnicas": ["camera-continua"], "nota": "a tela curva fica e o conteúdo troca para tópicos"},
  {"n": 18, "intencao": "PROVAR", "tecnicas": ["camera-continua"], "nota": "a tela curva fica e entram barras de progresso"},
  {"n": 19, "intencao": "PROVAR", "tecnicas": ["camera-continua", "dado-como-heroi"], "nota": "a tela curva fica e entram percentuais grandes"},
  {"n": 20, "intencao": "FECHAR", "tecnicas": [], "nota": "repete a capa, com redes sociais no rodapé"}
 ]}
```

Efeito (reel de 5 slides):

```json
{"id": "284-reel-cerebro-3d", "tipo": "efeito",
 "resumo": "Um cérebro 3D gira e se aproxima a cada slide enquanto o título gigante se repete e vaza pelas bordas; o slide 1 é a versão comum.",
 "antes": [1],
 "ideia": "Transforme o objeto central do tema num personagem 3D que gira e se aproxima a cada slide, e use o nome do tema como textura tipográfica gigante atrás dele.",
 "como_funciona": "Slide 2: modelo 3D centralizado sobre fundo salmão, palavra enorme atravessada pelo objeto. Slide 3: o modelo gira para a vista em corte e vai para a direita enquanto a palavra se repete em pilha preta vazando pela esquerda. Slide 4: o objeto cresce para a esquerda e uma linha aponta uma região, com o texto à direita. Slide 5: mergulho no detalhe interno, que ocupa quase a tela toda.",
 "html": "<model-viewer> com camera-orbit e camera-target diferentes por slide, animando a troca; sem 3D, use PNGs recortados do objeto em ângulos diferentes com o mesmo data-m. A palavra repetida é uma pilha de spans com overflow: hidden.",
 "intencoes": ["IMPACTAR", "EXPLICAR"],
 "tecnicas": ["tipografia-como-imagem", "profundidade-em-camadas", "padrao-e-quebra", "linha-guia", "contraste-de-escala"],
 "movimento": ["giro", "zoom-mergulho", "reorganizar"],
 "estetica": ["3d", "cientifico", "pastel"],
 "tom": ["inspirador", "tecnico"],
 "bom_para": ["aula ou palestra de ciência e saúde", "lançamento de produto físico que tenha modelo 3D", "abrir um capítulo sobre o objeto central do tema"],
 "cuidados": "Depende de um modelo 3D de qualidade; com foto plana perde a força. Uma vez por apresentação basta.",
 "destaques": [3, 5],
 "forca": 5,
 "slides": [
  {"n": 1, "intencao": "ANTES", "tecnicas": [], "nota": "slide comum: título, tópicos e duas figuras pequenas"},
  {"n": 2, "intencao": "ABRIR", "tecnicas": ["profundidade-em-camadas", "tipografia-como-imagem"], "nota": "objeto 3D atravessando a palavra gigante"},
  {"n": 3, "intencao": "DESTACAR", "tecnicas": ["padrao-e-quebra", "tipografia-como-imagem"], "nota": "palavra repetida em pilha vazando a borda; objeto em corte à direita"},
  {"n": 4, "intencao": "EXPLICAR", "tecnicas": ["linha-guia"], "nota": "linha aponta uma região do objeto; texto à direita"},
  {"n": 5, "intencao": "IMPACTAR", "tecnicas": ["corte-radical", "contraste-de-escala"], "nota": "mergulho no detalhe interno ocupando quase a tela"}
 ]}
```

## Regras finais

- Seja específico. "Layout moderno e bonito" não ajuda ninguém. "Foto recortada do atleta invade o título por cima das letras" ajuda.
- A `ideia` não pode citar o tema do exemplo (cérebro, cinema, pizza...). Ela precisa servir para uma palestra sobre qualquer assunto.
- Textos em lorem ipsum não importam; descreva a estrutura.
- Marcas e fotos de famosos (Nike, Apple, Messi...) são exemplo de linguagem visual, não material para reutilizar. Escreva a ideia sem depender da marca.
- Não invente o que não dá para ver. Se a prancha estiver pequena demais para ler um detalhe, descreva o que dá para afirmar.
- Grave o arquivo do lote uma única vez, com todas as fichas. Depois confira com:
  `python3 -I ferramentas/construir/validar.py dados/_trabalho/fichas/lote-NNN.json`
  e corrija o que ele apontar.
