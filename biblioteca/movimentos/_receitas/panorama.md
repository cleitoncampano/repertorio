## Receita com o motor

Opção 1, câmera andando por um cenário largo (todos os elementos se deslocam juntos):

```html
<section class="slide"><div data-m="cena" style="position:absolute;left:0;top:0;width:5760px;height:1080px;background:url(panorama.jpg) 0 0/cover"></div></section>
<section class="slide"><div data-m="cena" style="position:absolute;left:-1920px;top:0;width:5760px;height:1080px;background:url(panorama.jpg) 0 0/cover"></div></section>
```

Opção 2, troca lateral do slide inteiro: `<section class="slide" data-trans="empurrar">`.

- Bom para jornada, linha do tempo, antes e depois lado a lado. Deixe a direção constante (sempre para a esquerda = avançar).
