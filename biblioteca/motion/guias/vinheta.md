# Marca e vinheta

Peça curta que apresenta um nome, um símbolo ou uma série e termina na assinatura: abertura de canal, evento ou palestra, revelação de logo, teaser de lançamento, apresentação de estúdio.
Escolha quando a meta é fixar a marca em poucos segundos, não explicar o produto nem mostrar amplitude técnica (para isso, use o showreel).

## Na galeria

- 9 vídeos, nenhum de força 5: 4 de força 4, 4 de força 3 e 1 de força 2. Três também contam como lançamento.
- Duração mediana de 15 s; faixa de 10 a 69 s (10, 10, 12, 15, 15, 19, 21, 40 e 69 s). Três dos quatro de força 4 têm de 10 a 15 s; acima de 18 s, só o de 40 s se sustenta.
- 6 horizontais, 2 quadrados (redes), 1 vertical. 8 têm som; o único sem som perde nota por repetição.
- Construção citada: GSAP (4), SVG (4), canvas (3), HyperFrames (1), JavaScript puro (1). O mais preciso (12 s) é desenhado por seek(t) quadro a quadro, com tempos em quadros a 29,97 fps.

## Estrutura que funciona

Sting de 10 a 12 s (abertura, nova versão, fechamento de vídeo):

- 0 a 1 s: o nome ou o símbolo já em movimento, sobre fundo de uma cor (em pincel sobre preto granulado, subindo de uma névoa azul).
- 1 a 2,5 s: um segundo plano que muda escala ou contexto: palavra condensada, cursor que clica no logo, barra de menu de notebook.
- 2,5 a 3 s: respiro. Quadro quase vazio (uma linha vermelha fina no preto) logo antes do clímax.
- 3 a 6 s: clímax no drop da música: raios girando, caracteres que entram voando, clarão com tudo invertido, chicote com desfoque.
- 6 a 10 s (ou 8 a 12 s): assinatura parada o bastante para ler. Título, linha de apoio em versalete espaçado, selo ou carimbo que bate por último. O último quadro é a marca.

Anúncio de marca de 15 s (vertical ou horizontal):

- 0 a 12 s: seis planos de cerca de 2 s, cada um num palco diferente (gravura, caligrafia, busto, mapa de estrelas), sempre com o mesmo elemento de marca pintado por cima na única cor.
- 12 a 15 s: frase curta com o ponto final na cor da marca e depois o logotipo.

Teaser de 15 s (pergunta aberta):

- 0 a 4 s: um facho de luz revela o símbolo aos poucos. 4 a 6 s: a leitura óbvia escrita na tela. 6 a 8 s: a resposta vira um ponto de interrogação.
- 8 a 12 s: pistas (cards, cópias do símbolo que se espalham). 12 a 15 s: tudo volta a um só símbolo, frase de virada e "Em breve".

Apresentação de estúdio de 30 a 40 s:

- Um código visual único do começo ao fim, com moldura de instrumento que informa (canal, BPM, tempo).
- 0 a 5 s: a primeira palavra. 5 a 15 s: a forma vira emaranhado (o problema). 15 a 30 s: a forma se acalma e vira linha do tempo dos trabalhos. 30 a 40 s: o símbolo é traçado e assina o nome.

Revelação montada do logo: esqueleto de linhas, peças que chegam e se encaixam, brilho, nome digitado ao lado. Funciona em até 10 s ou com cada peça presa a uma batida.

## Ritmo, câmera e transições

- 6 a 7 planos em 10 a 15 s: cerca de 1,5 a 2 s por plano. No estúdio de 40 s, blocos de 5 a 15 s em que a câmera para e o traço é que se move.
- Corte seco um pouco antes da batida, para parecer inevitável. O drop é o corte principal da peça.
- Nenhum plano começa ou termina parado: entra já em movimento com saída exponencial e sai acelerando ou numa rampa de desfoque. O desfoque segue velocidade e direção.
- Uma pausa curta antes do clímax rende mais que um efeito a mais.
- Câmera: zoom-mergulho rápido em imagens, chicote vertical com clarão, zoom leve no clique, cursor que gira para onde vai e cresce ao passar sobre o logo.
- Som: raios, carimbo e selo pedem acento na trilha. Sem batida marcada, revelação lenta cansa.

## Visual

- Disciplina de cor: preto e branco mais uma cor de marca. Laranja pintado sobre gravuras; vermelho sobre preto granulado; só azuis, sem roxo nem laranja; verde de fósforo monocromático.
- Tipografia com caráter de gênero: serifa pesada editorial, pincel japonês com romanização em versalete espaçado, Inter limpa de keynote, contorno luminoso de instrumento.
- Textura que dá matéria: grão no preto, vidro fosco feito de cópia borrada do fundo, persistência de fósforo, cores de risografia fora de registro.
- Imagens só de domínio público ou licenciadas, com peso cultural. Foto de banco genérica apaga o contraste entre o clássico e a marca.
- Interface real quando a marca é um app: janela, barra de menu, cursor, card. Um único SVG de cursor em todas as cenas.
- Assinatura: o símbolo sozinho no centro antes de ganhar o nome; faixa inclinada com carimbo; ou a palavra-marca com brilho que encolhe e colapsa no último quadro.

## O que os melhores fazem

1. Uma só cor de marca sobre um mundo em preto e branco: o traço, o ponto e o símbolo laranjas conversam com gravuras, busto e constelação. [Anúncio vertical com gravuras clássicas e marca pintada por cima](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-lexnlin-038035)
2. Código emprestado de um gênero que a plateia reconhece (faixa inclinada, raios, carimbo, clarão invertido) para dar peso épico a um nome curto em 10 s. [Vinheta de título no estilo de abertura de filme japonês](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-majin-appsheet-2d3c1a)
3. Respiro antes do pico: um segundo de linha fina no preto, depois raios e o clarão com as cores invertidas. [Vinheta de título no estilo de abertura de filme japonês](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-majin-appsheet-2d3c1a)
4. Nunca parar: todo plano entra em movimento e sai acelerando, e o corte cai logo antes da batida. [Vinheta quadrada de produto em estilo keynote com cursor e vidro fosco](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-notdwd-7de38a)
5. Prompt com entradas, paleta em hexadecimal, fps, tempos em quadros e cores proibidas por nome. [Vinheta quadrada de produto em estilo keynote com cursor e vidro fosco](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-notdwd-7de38a)
6. Um instrumento visual para tudo, texto e imagem, e a forma conta a mensagem: emaranhado, senoide calma, onda quadrada que vira linha do tempo. [Apresentação de estúdio desenhada como traço de osciloscópio](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-rneayan-ea6129)
7. O símbolo cresce sozinho antes do fecho: só depois vêm a frase curta e o logotipo. [Anúncio vertical com gravuras clássicas e marca pintada por cima](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-lexnlin-038035)

## Erros que derrubam

1. Revelação longa sem batida: 21 s montando o logo sem música marcada. Corte para menos de 10 s ou prenda cada peça à trilha. [Revelação lenta de logo montado de facetas em baixo polígono](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-tdinh-me-815acb)
2. Escuro demais: fachos de luz sobre quase preto e pouco contraste por boa parte do tempo; em celular ou projetor fraco, a revelação passa despercebida. [Teaser escuro que questiona o significado de um símbolo conhecido](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-robj3d3-b18fad)
3. Visual de modelo de festa: raios, confete e selo genéricos, e um ano errado no texto. Confira datas, nomes e números antes de renderizar. [Aniversário de 20 anos de marca de receitas com selo e confete](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-deebeeeff-50fcd0)
4. Longo para o que diz: 69 s de frases curtas e telas quase vazias. O estilo carrega, o ritmo arrasta. [Apresentação de estúdio em estética de risografia](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-rneayan-474bcf)
5. Sem som e sem variação: personagem no mesmo ponto, cenário que não muda, câmera fixa; a repetição aparece. [Samurai em silhueta executa golpes de fogo com nome em caligrafia](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-chrisjdimarco-f068db)
6. Referência que só um nicho entende, nome longo demais para a faixa inclinada, texto em contorno fino em frase longa.

## Prompt base

```
<direção>
Vinheta de marca de 10 s, 1920x1080 (1080x1080 ou 1080x1920 para redes), trilha a cerca de 120 BPM com um drop claro perto de 3 s.
Marca: [nome curto]. Símbolo: [logo ou forma simples]. Frase final: [até cinco palavras].
Escolha um código visual único e reconhecível e nomeie-o em uma linha (ex.: abertura de filme, gravura com cor pintada por cima, keynote de vidro fosco, traço de instrumento). Tudo na peça pertence a esse código.
Paleta: preto e branco (ou creme) mais uma só cor de marca, em hexadecimal; diga por nome as cores proibidas. Uma fonte de título com caráter e uma de apoio em versalete espaçado.
Nenhum plano começa nem termina parado: entra já em movimento com saída exponencial e sai acelerando ou numa rampa de desfoque.
Proibido: raios e confete de modelo pronto, foto de banco, símbolo sem contraste sobre quase preto, revelação lenta sem batida, plano vazio sem função, dado ou nome não conferido.
</direção>

<estrutura>
0 a 1 s: o nome ou o símbolo já em movimento.
1 a 2,5 s: um segundo plano que muda escala ou contexto (palavra-chave, clique no logo, close).
2,5 a 3 s: respiro de meio segundo, quadro quase vazio.
3 a 6 s: clímax no drop, com a assinatura visual do código escolhido.
6 a 10 s: assinatura legível: nome, linha de apoio, selo ou ponto de marca que bate por último. O último quadro é a marca.
</estrutura>

<construção>
1. Composição HyperFrames em HTML, tudo calculado do tempo em seek(t), sem animação CSS nem timers.
2. Marque as batidas em quadros e ponha cada corte um ou dois quadros antes do tempo forte.
3. Símbolo em SVG, com traços por stroke-dashoffset e morph entre variações. O mesmo SVG do começo ao fim.
4. Desfoque direcional proporcional à velocidade; grão ou textura numa única camada por cima de tudo.
5. Qualquer aleatoriedade com semente fixa.
</construção>

<começo>
Escreva o código visual em uma linha e uma lista de planos com o tempo de cada um. Construa sem perguntar.
Antes do MP4, exporte quadros em 0,5 s, 2 s, 2,8 s, 4 s, 6 s e no último quadro, e confira: a marca se lê em tela de celular, nenhuma cor além do preto, do branco e da cor de marca, nenhum plano parado na entrada ou na saída, nome e frase corretos, último quadro na marca. Corrija e só então renderize.
</começo>
```

## Abra primeiro

- [Anúncio vertical com gravuras clássicas e marca pintada por cima](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-lexnlin-038035): disciplina de uma cor e planos de 2 s em formato vertical.
- [Vinheta de título no estilo de abertura de filme japonês](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-majin-appsheet-2d3c1a): o sting de 10 s mais completo, com respiro, clarão invertido e carimbo final.
- [Vinheta quadrada de produto em estilo keynote com cursor e vidro fosco](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-notdwd-7de38a): planos que nunca param, cortes antes da batida e o prompt mais preciso da galeria.
- [Apresentação de estúdio desenhada como traço de osciloscópio](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-rneayan-ea6129): como sustentar 40 s com um código visual só e a forma mudando com a mensagem.
- [Teaser escuro que questiona o significado de um símbolo conhecido](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-robj3d3-b18fad): a estrutura de pergunta aberta para teaser; leve a estrutura e suba o contraste.
- [Revelação lenta de logo montado de facetas em baixo polígono](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-tdinh-me-815acb): a montagem do logo em três etapas, para refazer em menos de 10 s.
- [Sistema de movimento em que um ponto laranja liga todas as cenas](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-ultimaxbt-bbebf5): do showreel, um único ponto de marca que muda de papel e volta ao início, útil para vinheta de símbolo simples.

## Blocos do kit

Movimentos prontos no HyperFrames para este tipo (detalhes e o projeto inicial testado em `kit/motion/LEIA-ME.md`; instale com `npx hyperframes add <nome>`):

- `logo-sting`: a marca entra com impacto e fica parada
- `logo-brand-close`: nome entra letra a letra e trava no centro
- `svg-mask-reveal`: imagem aparece só dentro das letras da marca
- `titlecard-lockup`: cartão de título calmo para respiro
- `beat-accent`: um impacto na batida: clarão e pulso no elemento
