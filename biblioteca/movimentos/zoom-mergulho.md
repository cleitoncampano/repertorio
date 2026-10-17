# Zoom mergulho

`zoom-mergulho`

A câmera entra num elemento, que cresce e vira a próxima cena.

**Em HTML:** data-m no elemento: pequeno no slide A, tela cheia no slide B.

## Receita com o motor

```html
<section class="slide">
  <img data-m="foto" src="foto.jpg" style="position:absolute;right:160px;top:300px;width:420px;height:280px;object-fit:cover;border-radius:16px">
  <h2 data-m="titulo" style="position:absolute;left:120px;top:300px;font-size:120px">Um detalhe</h2>
</section>
<section class="slide" data-dur="1100">
  <img data-m="foto" src="foto.jpg" class="sangria">
  <h2 data-passo="0" data-entra="sobe" style="position:absolute;left:120px;bottom:120px;font-size:140px;color:#fff">vira o mundo</h2>
</section>
```

- O elemento pequeno do slide A vira a tela inteira no B. Use a mesma imagem nos dois para não haver fusão estranha.
- 1000 a 1300 ms. O texto do slide B entra depois (`data-passo="0"`), nunca junto com o mergulho.
- Bom para entrar num capítulo, num caso ou num detalhe de produto. Uma ou duas vezes por apresentação.

## Arquivos que usam (136)

- **129-reel-17-06** (Table top com zoom, força 5): Transforme a agenda numa cena real em que cada objeto representa uma etapa, e use cada objeto como porta: o zoom entra nele e abre o capítulo correspondente.  
  `_catalogo/pranchas/129-reel-17-06.jpg`
- **157-reel-21-08-efeito-wow-rio-de-janeiro** (Rio de Janeiro, força 5): Vaze o nome do lugar numa tela branca para a foto aparecer só dentro das letras, e no avanço mergulhe numa das letras até a foto ocupar tudo: o nome vira a porta de entrada.  
  `_catalogo/pranchas/157-reel-21-08-efeito-wow-rio-de-janeiro.jpg`
- **219-reel-30-07** (SWOT, força 5): Quando o tema é uma sigla, use a própria palavra como mapa: mergulhe nela e visite uma letra por vez, deixando a letra gigante e cortada servir de fundo para a explicação daquele item.  
  `_catalogo/pranchas/219-reel-30-07.jpg`
- **283-reel-celula-3d** (Célula, força 5): Faça um tour guiado pelo interior do objeto do tema: gire o modelo para a vista em corte e, a cada slide, aproxime e desloque a câmera até uma parte diferente, nomeada por uma linha fina e um rótulo discreto.  
  `_catalogo/pranchas/283-reel-celula-3d.jpg`
- **284-reel-cerebro-3d** (Cérebro, força 5): Transforme o objeto central do tema num personagem 3D que gira e se aproxima a cada slide, e use o nome do tema como textura tipográfica gigante atrás dele.  
  `_catalogo/pranchas/284-reel-cerebro-3d.jpg`
- **388-reel-instax** (Instax, força 5): Faça o produto produzir o próprio conteúdo: o objeto age (dispara, imprime, entrega), a câmera mergulha no resultado em tela cheia e depois recua para mostrar vários resultados lado a lado.  
  `_catalogo/pranchas/388-reel-instax.jpg`
- **462-reel-portfolio** (Portfolio, força 5): Amplie o título da capa até as letras virarem formas abstratas de fundo e passeie por dentro delas, uma imagem por slide; no fim, recue até a palavra caber de novo na tela.  
  `_catalogo/pranchas/462-reel-portfolio.jpg`
- **562-reel-zoom** (Table Top Zoom, força 5): Monte uma mesa vista de cima e faça de cada papel, caderno ou cartão a miniatura de um slide; clique num objeto para mergulhar no conteúdo e volte à mesa entre um capítulo e outro.  
  `_catalogo/pranchas/562-reel-zoom.jpg`
- **022-3d-reels** (Nasa, força 4): Coloque o personagem 3D do tema na frente da palavra ou marca gigante, cobrindo parte das letras; nos slides seguintes empurre o personagem para um lado e use o espaço liberado como painel de texto, aproximando a câmera a cada passo.  
  `_catalogo/pranchas/022-3d-reels.jpg`
- **023-apple-reels** (Apple, força 4): Mostre o objeto inteiro pequeno e depois mergulhe com a câmera num detalhe dele, deslizando de lado pela parte que interessa, sem texto: o próprio zoom vira a explicação.  
  `_catalogo/pranchas/023-apple-reels.jpg`

## Passagens de slide analisadas

- **157-reel-21-08-efeito-wow-rio-de-janeiro#2**: forma "Forma Livre 5" cresce 27,6x, vai para a direita, termina ocupando a tela; 1 objeto(s) novo(s) surgem  
  `_catalogo/miniaturas/157-reel-21-08-efeito-wow-rio-de-janeiro/02.jpg`
- **219-reel-30-07#2**: "swot" cresce 7,2x, vai para a direita, termina ocupando a tela; 1 objeto(s) novo(s) surgem  
  `_catalogo/miniaturas/219-reel-30-07/02.jpg`
- **388-reel-instax#4**: imagem "Imagem 15" cresce 4,8x, vai para cima, termina ocupando a tela; imagem "Imagem 2" cresce 3,8x, vai para a esquerda, termina ocupando a tela; 14 objeto(s) somem  
  `_catalogo/miniaturas/388-reel-instax/04.jpg`
- **462-reel-portfolio#2**: "Portfolio" cresce 16,2x, vai para a direita, termina ocupando a tela; "NOME DO PROFISSIONAL" sai da tela (baixo); imagem "Imagem 7" entra vindo de fora (direita); 1 objeto(s) novo(s) surgem  
  `_catalogo/miniaturas/462-reel-portfolio/02.jpg`
- **585-reels-nestle-grafico#5**: forma "Retângulo Arredondado 8" encolhe para 34%, vai para a esquerda, muda de proporção; forma "Retângulo Arredondado 9" cresce 2,9x, vai para a esquerda, muda de proporção, troca de cor #FFFFFF→#2E4  
  `_catalogo/miniaturas/585-reels-nestle-grafico/05.jpg`
- **585-reels-nestle-grafico#6**: forma "Retângulo Arredondado 10" cresce 3,0x, vai para a esquerda, muda de proporção, troca de cor #FFFFFF→#4472C4; forma "Retângulo Arredondado 9" encolhe para 34%, vai para a esquerda, muda de propo  
  `_catalogo/miniaturas/585-reels-nestle-grafico/06.jpg`
- **585-reels-nestle-grafico#7**: forma "Retângulo Arredondado 11" cresce 3,0x, vai para a esquerda, muda de proporção, troca de cor #FFFFFF→#743C00; forma "Retângulo Arredondado 10" encolhe para 34%, vai para a esquerda, muda de prop  
  `_catalogo/miniaturas/585-reels-nestle-grafico/07.jpg`
- **022-3d-reels#4**: imagem "Imagem 6" cresce 2,0x, entra vindo de fora (cima), termina ocupando a tela; 3d "Modelo 3D 4" cresce 1,4x, vai para a direita, termina ocupando a tela; "NATIONAL AERONAUTICS AND SPACE ADMINISTR  
  `_catalogo/miniaturas/022-3d-reels/04.jpg`

Mais: `python3 -I ferramentas/buscar.py -m zoom-mergulho --doc arquivo --prancha`
