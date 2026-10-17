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
