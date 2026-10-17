# Giro

`giro`

Rotação 2D ou 3D, inclusive de modelos 3D.

**Em HTML:** rotate no estado final; para 3D, <model-viewer> com camera-orbit animado.

## Receita com o motor

2D: mesmo `data-m` com `rotate` diferente no slide B.

3D (modelo .glb):

```html
<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer@3.5.0/dist/model-viewer.min.js"></script>
<model-viewer src="objeto.glb" camera-orbit="0deg 75deg 2.5m" interpolation-decay="120" disable-zoom
  style="position:absolute;right:0;top:0;width:1100px;height:1080px"></model-viewer>
<script>
  // a cada slide, gire a câmera: document.querySelector('model-viewer').cameraOrbit = '120deg 70deg 1.6m'
</script>
```

- Os modelos 3D do acervo saem com `python3 -I ferramentas/midia.py <id> pasta` (busque com `--doc midia --uso 3d`).
- Sem 3D: PNGs recortados do objeto em ângulos diferentes, mesmo `data-m`.

## Arquivos que usam (115)

- **252-reel-bk** (Buerger King, força 5): Desmonte o produto diante da plateia: mostre o todo, depois desça por cada peça em close, uma de cada vez, e termine recuando para a vista explodida com tudo separado e alinhado.  
  `_catalogo/pranchas/252-reel-bk.jpg`
- **283-reel-celula-3d** (Célula, força 5): Faça um tour guiado pelo interior do objeto do tema: gire o modelo para a vista em corte e, a cada slide, aproxime e desloque a câmera até uma parte diferente, nomeada por uma linha fina e um rótulo discreto.  
  `_catalogo/pranchas/283-reel-celula-3d.jpg`
- **284-reel-cerebro-3d** (Cérebro, força 5): Transforme o objeto central do tema num personagem 3D que gira e se aproxima a cada slide, e use o nome do tema como textura tipográfica gigante atrás dele.  
  `_catalogo/pranchas/284-reel-cerebro-3d.jpg`
- **025-cartao-namorados** (Namorados 2025, força 4): Monte uma mensagem como galeria de fotos em molduras de polaroide, cada uma com uma única palavra; o mural vira menu e cada foto se abre em tela cheia, terminando numa frase curta sozinha.  
  `_catalogo/pranchas/025-cartao-namorados.jpg`
- **028-reel-01-07** (New Balance - Retângulos, força 4): Divida a tela em colunas iguais, uma por item, e alterne dois estados: visão geral com todas iguais e foco com uma coluna aberta para metade da tela, o item maior e o número em cor de acento; volte à visão geral entre um item e outro.  
  `_catalogo/pranchas/028-reel-01-07.jpg`
- **038-reel-03-01** (BYD, força 4): Cubra uma grade de quatro fotos com uma forma que só deixa um quarto à mostra e gire essa forma a cada slide: a janela passeia pelos itens como um relógio e o texto ocupa as áreas fechadas.  
  `_catalogo/pranchas/038-reel-03-01.jpg`
- **049-reel-04-02** (Curriculum Dinâmico, força 4): Organize as partes do conteúdo como abas estreitas lado a lado, com o nome de cada uma escrito em pé; a cada avanço uma aba se abre num painel largo, o título gira para a horizontal e as outras se encolhem, como uma sanfona.  
  `_catalogo/pranchas/049-reel-04-02.jpg`
- **061-reel-05-10** (Eleições 2026, força 4): Num duelo entre dois, cubra a tela com uma forma gigante que tenha uma fatia aberta como janela: ela mostra um lado e esconde o outro, e girar a forma meia volta passa a vez ao rival sem trocar de cena.  
  `_catalogo/pranchas/061-reel-05-10.jpg`
- **064-reel-06-05** (Álbum da Copa, força 4): Use a linguagem de um objeto colecionável que a plateia conhece e coloque você mesmo dentro dele: folheie as páginas e, no momento certo, faça a sua peça saltar, girar diante da câmera e voltar para o lugar.  
  `_catalogo/pranchas/064-reel-06-05.jpg`
- **068-reel-06-09** (Destinos rotatórios, força 4): Monte as opções numa roda gigante quase toda escondida abaixo da tela, com um ponteiro fixo no centro; a cada slide gire a roda um quarto de volta para a próxima opção subir, crescer e ganhar a etiqueta.  
  `_catalogo/pranchas/068-reel-06-09.jpg`

## Passagens de slide analisadas

- **252-reel-bk#2**: imagem "Picture 13" cresce 1,9x, vai para baixo, gira -347°; imagem "Picture 7" cresce 1,9x, sai da tela (baixo); imagem "Picture 6" cresce 1,9x, sai da tela (baixo)  
  `_catalogo/miniaturas/252-reel-bk/02.jpg`
- **252-reel-bk#5**: imagem "Picture 5" vai para cima, gira -351°; imagem "Picture 13" sai da tela (cima), gira 348°; imagem "Picture 6" vai para cima, gira 345°; 1 objeto(s) somem  
  `_catalogo/miniaturas/252-reel-bk/05.jpg`
- **252-reel-bk#7**: imagem "Picture 16" encolhe para 51%, entra vindo de fora (cima), gira -340°; imagem "Picture 13" encolhe para 51%, entra vindo de fora (cima), gira 348°; imagem "Picture 5" encolhe para 51%, entra vi  
  `_catalogo/miniaturas/252-reel-bk/07.jpg`
- **388-reel-instax#5**: quadro "Zoom de Slide 36" encolhe para 26%, vai para a direita, gira 329°, muda de proporção; imagem "Imagem 1" encolhe para 21%, sai da tela (direita), muda de proporção; 11 objeto(s) novo(s) surgem  
  `_catalogo/miniaturas/388-reel-instax/05.jpg`
- **252-reel-bk#3**: imagem "Picture 13" vai para cima, gira 347°; imagem "Picture 16" vai para cima, gira -336°; imagem "Picture 5" entra vindo de fora (baixo)  
  `_catalogo/miniaturas/252-reel-bk/03.jpg`
- **252-reel-bk#4**: imagem "Picture 13" vai para cima, gira -347°; imagem "Picture 16" sai da tela (cima), gira 344°; imagem "Picture 5" vai para cima, gira 342°  
  `_catalogo/miniaturas/252-reel-bk/04.jpg`
- **252-reel-bk#6**: imagem "Picture 1" cresce 6,2x, sai da tela (cima), muda de proporção; imagem "Picture 7" vai para cima, gira 349°; imagem "Picture 6" vai para cima, gira -346°; 1 objeto(s) novo(s) surgem  
  `_catalogo/miniaturas/252-reel-bk/06.jpg`
- **388-reel-instax#2**: quadro "Zoom de Slide 36" cresce 1,3x, vai para a esquerda; imagem "Imagem 33" cresce 1,2x, vai para a esquerda, gira 90°; imagem "Imagem 45" entra vindo de fora (esquerda); 6 objeto(s) novo(s) surgem  
  `_catalogo/miniaturas/388-reel-instax/02.jpg`

Mais: `python3 -I ferramentas/buscar.py -m giro --doc arquivo --prancha`
