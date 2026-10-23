# Arte abstrata e 3D

Forma, matéria, luz e ritmo no lugar de personagem e argumento: vinheta com o símbolo da marca, visualizer de música, abertura de evento, celebração de um número, showreel.
Escolha este tipo quando um elemento simples da marca ou a própria trilha podem ser o protagonista, e quando existe uma ideia que a transformação vai provar.

## Na galeria

- 22 vídeos, 15 de força 4 e 5. Duração mediana de 15 s, faixa de 10 a 98 s; 13 ficam entre 10 e 15 s.
- 17 horizontais, 4 verticais e 1 quadrado. 21 têm som; 5 declaram o andamento (120 a 140 BPM) e cortam no compasso.
- 10 são showreels de "mostre que você é um grande motion designer". Ferramenta declarada em 7 (HTML, three.js, Remotion, HyperFrames); as notas citam canvas (12), three.js (10), SVG (7), HyperFrames e Remotion (6 cada).
- A diferença está no movimento de transformação: 11 de 15 nos fortes contra 2 de 7 nos fracos. Os fortes usam também numeração de capítulo (6) e estética escura (10), 3D (7) e tecnológica (7).
- Nos fracos, 5 dos 7 cuidados dizem a mesma coisa: catálogo de efeitos, prova técnica, enfeite ou formato batido, sem uma ideia que ligue as cenas.

## Estrutura que funciona

Os melhores seguem um arco de complexidade com um único elemento: semente, transformações no tempo da batida, clímax de densidade, recolhimento e assinatura com o elemento de volta ao começo.

Versão de 10 a 15 s (vinheta, showreel, celebração):
- 0 a 1 s: a semente sozinha. Um ponto de luz, uma linha, uma curva de easing, um clique num toggle.
- 1 a 4 s: a semente encontra a palavra ou o símbolo (vira o pingo do i, monta as letras com barras).
- 4 a 10 s: 3 ou 4 capítulos de cerca de 2 s, um por compasso. Cada um muda a dimensão do mesmo elemento (plano, volume, fluido, partículas) com a mesma paleta e as mesmas formas.
- 10 a 13 s: clímax de densidade (cem mil partículas explodem) e recolhimento (o redemoinho rebobina).
- 13 a 15 s: assinatura sobre fundo calmo, com o elemento de volta à forma inicial. Último quadro igual ao primeiro, se for loop.

Versão de 30 s (manifesto, abertura de palestra):
- Figuras numeradas de 4 a 5 s cada ("fig. 1, um ponto"), com o objeto mantendo posição e tamanho entre elas e trocando só de natureza.
- A última figura reencontra o elemento inicial com outro sentido: o mundo encolhe até virar o ponto final da frase.

Versão musical de 45 a 60 s (visualizer):
- 0 a 10 s: poucos elementos e uma camada da música. A receita do som pode estar na tela (o código da faixa, os instrumentos).
- 10 a 30 s: entra uma camada por vez, cada uma com sua forma e cor.
- 30 a 45 s: densidade máxima no drop. A receita se corrompe em textura (caracteres ASCII que pulsam com o grave).
- Últimos 5 a 10 s: coda limpa que volta ao quadro inicial.

Explicação 3D longa (60 a 100 s): uma viagem de câmera contínua do todo até a menor peça e de volta, com capítulos numerados e uma cor fixa para cada fluxo.

## Ritmo, câmera e transições

Forma e partícula seguindo o som:
- Faça a conta antes: a 120 BPM a batida dura 0,5 s e um capítulo de 4 batidas dura 2 s. Em 15 s cabem 7 ou 8 capítulos.
- Meça as batidas da trilha e derive delas o quadro de cada evento. Não confie em cortes a olho.
- Som e imagem são o mesmo evento: cada nota nasce de uma colisão visível. Resolva a física ao contrário, marcando o impacto na nota e calculando o lançamento para chegar nela.
- Cada batida acende um objeto no instante do contato (brilho ligado ao impacto, não a um pulso genérico).
- A intensidade do grave comanda a matéria: quantos caracteres acendem, quanto o texto se corrompe, o raio dos pontos do meio-tom.
- Gráfico e movimento saem da mesma função: a curva de mola desenhada é a mesma que move o ponto, então a anotação é verdadeira.
- Partícula forma algo legível (a palavra, o número, a silhueta, o globo) por alguns quadros parados e depois volta a ser matéria. Explosão só no clímax ou no instante da conquista.

Câmera e passagem entre cenas:
- O próprio elemento faz a ponte: preenche a tela e contrai na cena seguinte, muda de estado sem mudar de lugar, inverte o fundo com o símbolo parado na mesma posição. Evite crossfade.
- Câmera quase fixa nos 2D; a forma se move. Zoom que acompanha o elemento quando ele cresce (o anel seguinte, o próximo nível).
- No 3D, câmera em trilha contínua entre pontos de interesse, com legendas presas à posição dos objetos.
- Respiro antes do fecho: um quadro calmo ou 1 s de preto.

## Visual

- Disciplina de paleta: duas cores e um acento (creme, preto e terracota; off-white, quase preto e laranja), ou as três primárias da Bauhaus repetidas em todas as técnicas.
- Formas básicas e sistemas: ponto, círculo, quadrado, triângulo, grade modular, meio-tom, voxels, caracteres ASCII.
- 3D com material que se nomeia: vidro que refrata, cromo com reflexo, plástico fosco, chão que recebe sombra. Contraste suficiente para o protagonista não sumir no escuro.
- Uma família tipográfica (grotesca pesada) com serifa itálica de apoio. Texto só em rótulos curtos numerados e no cartão final.
- Fundo chapado, papel creme ou quase preto com grade de pontos.
- Moldura com timecode e cantos já virou clichê de vídeo gerado por IA. Só vale se carregar capítulo ou compasso.
- Cara de profissional: o mesmo elemento presente em todas as cenas e nenhum efeito que não nasça de algo já na tela.

## O que os melhores fazem

1. Progressão de dimensões (ponto, linha, plano, volume, fluido, partícula) com as mesmas três formas e cores em todas as técnicas. [Showreel que vai do ponto à linha, ao plano, ao volume e às partículas](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-lukasersil-0ed38e)
2. Um único objeto evolui em figuras numeradas e volta como ponto final da frase, num fechamento que parece inevitável. [Um ponto que vira círculo, lente, bola, bando, mundo e ponto final](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-hbcoop-de365c)
3. O ponto da marca nunca teletransporta nem muda de cor: liga toggle, letra, gráfico, forma e cartão final, e o loop fecha sem salto. [Sistema de movimento em que um ponto laranja liga todas as cenas](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-ultimaxbt-bbebf5)
4. Cada som nasce de uma colisão visível e a sincronia vira o espetáculo. [Máquina musical em que cada nota nasce de uma colisão visível](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-kamstudiolabs-447565)
5. A receita do som aparece na tela e se desfaz em textura no drop, ligada à intensidade do grave. [Faixa eletrônica com código ao vivo que se desfaz em arte ASCII](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-rames-jusso-589f80)
6. Uma nuvem de partículas é a matéria única e assume uma forma por tema, sempre com um título que diz o que ela é. [Apresentação pessoal com nuvem de partículas que vira cada conquista](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-madhav-xo-f97f20)
7. Um número que importa recontado em várias técnicas, uma por batida, a 120 BPM. [Agradecimento aos primeiros 100 usuários com o número em cada técnica](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-sudiyasa-f48ac9)
8. Viagem contínua do prédio até o chip, com uma cor fixa para energia, dados e calor. [Viagem 3D por dentro de um data center, do prédio ao chip](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-mdaman010-e7226a)

## Erros que derrubam

Teste da demo sem ideia: descreva a peça numa frase sem nome de técnica ("um ponto que vira o mundo e volta a ser o ponto final"). Se só der para listar efeitos (partículas, fluido, 3D, interface), falta a ideia.
1. Catálogo de efeitos: cada cena bem feita, nenhum conceito que as ligue além da paleta e da moldura. [Showreel de formas, partículas e interface com HUD](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-shinskinakamoto-20190b)
2. Prova técnica gravada: objeto girando com uma legenda por recurso, no ritmo lento de gravação de tela. [Demonstração de avião 3D feito em código com legenda por recurso](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-buildfastwithai-ed9447)
3. Partículas como enfeite ou fumaça brilhante: em excesso, ou abstratas demais para serem lidas em poucos quadros. [Tela de conquista em app com medalha 3D e partículas douradas](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-bthreeagency-b9b8d9)
4. Formato viral batido de física sem melodia reconhecível nem marca por trás. [Bola que tenta escapar de 12 anéis, cada quique uma nota](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-kantamk-61f410)
5. Cena escura demais em que o protagonista se perde entre os objetos. [Bola 3D que quica no ritmo de música clássica acendendo objetos](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-gorden-sun-041f56)
6. Duas linguagens sem ponte (estudos abstratos e depois cartazes 3D) ou troca de estilo a cada batida sem um elemento fixo forte: parecem dois filmes colados. [Showreel de tipografia pesada com objetos 3D cromados e verde-limão](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-shneural-2abdfa)

## Prompt base

```
<direção>
Filme abstrato de 15 s, [1920x1080 | 1080x1920 | 1080x1080], para [MARCA OU TEMA], com trilha de [120] BPM.
A ideia em uma frase, sem nome de técnica: "[O QUE A TRANSFORMAÇÃO PROVA, ex.: tudo começa num ponto]".
Um único elemento, [O PONTO | A LINHA | O SÍMBOLO DA MARCA], atravessa todas as cenas e muda de natureza a cada compasso
([forma plana, volume de vidro, fluido, nuvem de partículas]), sem sumir, sem saltar de lugar e sem mudar de cor.
Paleta fixa: fundo [COR], formas [COR], um acento [COR]. Uma família tipográfica, só em rótulos numerados e no cartão final.
Proibido: efeito que não nasça do elemento em cena, paleta nova por capítulo, crossfade, partículas como enfeite,
brilho genérico, moldura com timecode nos cantos, texto em desfoque, cena escura em que o elemento se perde.
</direção>

<estrutura>
Uma batida a cada 0,5 s, um capítulo a cada 4 batidas (2 s).
0 a 1 s: a semente, [ELEMENTO] sozinho no centro.
1 a 3 s: 01 [NOME]: o elemento encontra [A PALAVRA OU O SÍMBOLO].
3 a 5 s: 02 [NOME]: [FORMA PLANA OU GRADE].
5 a 7 s: 03 [NOME]: [VOLUME 3D COM MATERIAL].
7 a 9 s: 04 [NOME]: [FLUIDO OU PARTÍCULAS] que formam [O NÚMERO | A PALAVRA | O SÍMBOLO], legível parado.
9 a 12 s: clímax de densidade no ponto mais forte da trilha, depois tudo se recolhe ao elemento.
12 a 15 s: cartão final "[TEXTO]"; o último quadro repete o primeiro para fechar em loop.
Cada impacto, contato ou acender cai numa batida e toca o som correspondente no mesmo quadro.
</estrutura>

<construção>
1. Um arquivo HTML no HyperFrames, 60 fps, tudo calculado a partir do tempo em seek(t); acaso só com semente fixa; molas em forma fechada.
2. Meça as batidas da trilha e guarde numa lista; cada evento visual é derivado dela. Em física, marque o impacto na batida e calcule o lançamento.
3. O elemento é o mesmo objeto em todos os estados: posição, tamanho e cor contínuos entre capítulos.
4. Partículas amostradas de formas-alvo (texto rasterizado, símbolo, grade), com ruído e atraso por partícula; cada forma fica legível por pelo menos 0,5 s.
5. 3D em three.js com material nomeado (vidro, cromo, fosco) e chão com sombra; o elemento sempre com contraste sobre o fundo.
6. Antes de exportar, renderize um quadro por compasso e confira: o elemento está em todos, a paleta não mudou,
   cada forma se lê parada, primeiro e último quadros são iguais. Depois assista com som: impacto e nota no mesmo quadro.
</construção>

<começo>
Escreva a ideia em uma frase e o mapa de batidas (batida, capítulo, estado do elemento, som).
Mostre quatro quadros parados (semente, volume, clímax, cartão final) antes de construir o vídeo inteiro.
</começo>
```

## Abra primeiro

- [Um ponto que vira círculo, lente, bola, bando, mundo e ponto final](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-hbcoop-de365c): como um elemento único dá ideia e fechamento a uma peça abstrata.
- [Showreel que vai do ponto à linha, ao plano, ao volume e às partículas](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-lukasersil-0ed38e): progressão de técnicas presa por paleta e formas fixas.
- [Sistema de movimento em que um ponto laranja liga todas as cenas](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-ultimaxbt-bbebf5): continuidade sem salto, loop perfeito e um prompt completo no formato do Prompt Motion.
- [Máquina musical em que cada nota nasce de uma colisão visível](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-kamstudiolabs-447565): física calculada a partir da partitura.
- [Faixa eletrônica com código ao vivo que se desfaz em arte ASCII](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-rames-jusso-589f80): visualizer quadrado em que o texto reage ao grave.
- [Agradecimento aos primeiros 100 usuários com o número em cada técnica](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-sudiyasa-f48ac9): um dado de marca virando celebração em 15 s a 120 BPM.
- [Showreel de formas, partículas e interface com HUD](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-shinskinakamoto-20190b): contraexemplo, o catálogo de efeitos que não se deve repetir.

## Blocos do kit

Movimentos prontos no HyperFrames para este tipo (detalhes e o projeto inicial testado em `kit/motion/LEIA-ME.md`; instale com `npx hyperframes add <nome>`):

- `facet-morph`: massa de triângulos que vira outra silhueta
- `locked-nucleus-orbit`: satélites orbitam um centro e formam a marca
- `match-cut`: um círculo acelera e casa com o da cena seguinte
- `beat-accent`: um impacto na batida: clarão e pulso no elemento
- `svg-stroke-trace`: desenho de linha que se traça e preenche
