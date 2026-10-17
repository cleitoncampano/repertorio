# Voo

`voo`

Elementos entram ou saem vindo de fora da tela.

**Em HTML:** No slide A, posicionar o elemento fora da área visível (left: 110%) com o mesmo data-m.

## Receita com o motor

```html
<section class="slide">
  <img data-m="tenis" class="fora-dir recorte" src="tenis.png" style="top:300px;width:700px">
  <h2 style="position:absolute;left:120px;top:380px;font-size:120px">Leve</h2>
</section>
<section class="slide">
  <img data-m="tenis" class="recorte" src="tenis.png" style="position:absolute;left:900px;top:240px;width:820px;rotate:-12deg">
  <h2 style="position:absolute;left:120px;top:380px;font-size:120px">Leve</h2>
</section>
```

- No slide A o elemento fica estacionado fora da área (`fora-esq`, `fora-dir`, `fora-cima`, `fora-baixo`); no B ele entra voando. O inverso faz sair.
- Recorte (PNG sem fundo) + leve rotação no destino dá peso. Sombra com `.recorte`.

## Arquivos que usam (238)

- **388-reel-instax** (Instax, força 5): Faça o produto produzir o próprio conteúdo: o objeto age (dispara, imprime, entrega), a câmera mergulha no resultado em tela cheia e depois recua para mostrar vários resultados lado a lado.  
  `_catalogo/pranchas/388-reel-instax.jpg`
- **002-26-0102-cinema** (Cinema, força 4): Escolha um único acento de cor e aplique sempre na palavra-chave de cada título; todo o resto fica em preto, branco e fotos sem cor, e a repetição vira identidade.  
  `_catalogo/pranchas/002-26-0102-cinema.jpg`
- **022-3d-reels** (Nasa, força 4): Coloque o personagem 3D do tema na frente da palavra ou marca gigante, cobrindo parte das letras; nos slides seguintes empurre o personagem para um lado e use o espaço liberado como painel de texto, aproximando a câmera a cada passo.  
  `_catalogo/pranchas/022-3d-reels.jpg`
- **023-apple-reels** (Apple, força 4): Mostre o objeto inteiro pequeno e depois mergulhe com a câmera num detalhe dele, deslizando de lado pela parte que interessa, sem texto: o próprio zoom vira a explicação.  
  `_catalogo/pranchas/023-apple-reels.jpg`
- **025-cartao-namorados** (Namorados 2025, força 4): Monte uma mensagem como galeria de fotos em molduras de polaroide, cada uma com uma única palavra; o mural vira menu e cada foto se abre em tela cheia, terminando numa frase curta sozinha.  
  `_catalogo/pranchas/025-cartao-namorados.jpg`
- **027-reel-01-01** (Africa, força 4): Ponha a palavra-título gigante atrás do sujeito recortado e repita a mesma palavra só em contorno por cima dele: as letras somem atrás da cabeça, mas o traço continua visível e a leitura não se perde.  
  `_catalogo/pranchas/027-reel-01-01.jpg`
- **028-reel-01-07** (New Balance - Retângulos, força 4): Divida a tela em colunas iguais, uma por item, e alterne dois estados: visão geral com todas iguais e foco com uma coluna aberta para metade da tela, o item maior e o número em cor de acento; volte à visão geral entre um item e outro.  
  `_catalogo/pranchas/028-reel-01-07.jpg`
- **037-reel-02-12** (Stranger Things, força 4): Comece com a foto do grupo inteiro e depois apresente cada pessoa desfocando o grupo e acendendo só ela num recorte nítido no lugar onde está: o contexto fica, mas o foco é de um por vez.  
  `_catalogo/pranchas/037-reel-02-12.jpg`
- **050-reel-04-05** (On Running Galeria, força 4): Faça uma moldura de cor cheia com uma janela recortada no meio, deslize as fotos por trás dela como num carrossel e deixe o produto recortado à frente, vazando a janela por cima da moldura.  
  `_catalogo/pranchas/050-reel-04-05.jpg`
- **059-reel-05-08** (Toronto, força 4): Apoie o título gigante, na mesma cor do fundo, sobre a borda de uma faixa lisa para as letras parecerem brotar dela; no avanço, role essa faixa para cima como uma página e traga os cards de conteúdo.  
  `_catalogo/pranchas/059-reel-05-08.jpg`

## Passagens de slide analisadas

- **252-reel-bk#2**: imagem "Picture 13" cresce 1,9x, vai para baixo, gira -347°; imagem "Picture 7" cresce 1,9x, sai da tela (baixo); imagem "Picture 6" cresce 1,9x, sai da tela (baixo)  
  `_catalogo/miniaturas/252-reel-bk/02.jpg`
- **252-reel-bk#5**: imagem "Picture 5" vai para cima, gira -351°; imagem "Picture 13" sai da tela (cima), gira 348°; imagem "Picture 6" vai para cima, gira 345°; 1 objeto(s) somem  
  `_catalogo/miniaturas/252-reel-bk/05.jpg`
- **252-reel-bk#7**: imagem "Picture 16" encolhe para 51%, entra vindo de fora (cima), gira -340°; imagem "Picture 13" encolhe para 51%, entra vindo de fora (cima), gira 348°; imagem "Picture 5" encolhe para 51%, entra vi  
  `_catalogo/miniaturas/252-reel-bk/07.jpg`
- **283-reel-celula-3d#2**: "E SUAS ESTRUTURAS" sai da tela (esquerda); 3d "Modelo 3D 4" cresce 1,3x, vai para a esquerda; "células" sai da tela (esquerda); 2 objeto(s) novo(s) surgem  
  `_catalogo/miniaturas/283-reel-celula-3d/02.jpg`
- **388-reel-instax#3**: grupo "Agrupar 32" vai para a direita; quadro "Zoom de Slide 36" entra vindo de fora (esquerda); 7 objeto(s) novo(s) surgem; 2 objeto(s) somem  
  `_catalogo/miniaturas/388-reel-instax/03.jpg`
- **388-reel-instax#5**: quadro "Zoom de Slide 36" encolhe para 26%, vai para a direita, gira 329°, muda de proporção; imagem "Imagem 1" encolhe para 21%, sai da tela (direita), muda de proporção; 11 objeto(s) novo(s) surgem  
  `_catalogo/miniaturas/388-reel-instax/05.jpg`
- **462-reel-portfolio#2**: "Portfolio" cresce 16,2x, vai para a direita, termina ocupando a tela; "NOME DO PROFISSIONAL" sai da tela (baixo); imagem "Imagem 7" entra vindo de fora (direita); 1 objeto(s) novo(s) surgem  
  `_catalogo/miniaturas/462-reel-portfolio/02.jpg`
- **462-reel-portfolio#3**: "Portfolio" vai para a esquerda, termina ocupando a tela; imagem "Imagem 7" sai da tela (esquerda); imagem "Imagem 1" entra vindo de fora (direita); 1 objeto(s) novo(s) surgem; 1 objeto(s) somem  
  `_catalogo/miniaturas/462-reel-portfolio/03.jpg`

Mais: `python3 -I ferramentas/buscar.py -m voo --doc arquivo --prancha`
