## Receita com o motor

```html
<section class="slide"><img data-m="mapa" src="detalhe.jpg" class="sangria"></section>
<section class="slide" data-dur="1200">
  <img data-m="mapa" src="detalhe.jpg" style="position:absolute;left:760px;top:330px;width:400px;height:420px;object-fit:cover">
  <div data-passo="0" data-entra="escala" style="position:absolute;inset:0;border:2px solid #fff;...">contexto em volta</div>
</section>
```

- O que ocupava a tela encolhe e o contexto aparece em volta. Revela que o detalhe é parte de algo maior.
- Combine com `fechamento` ou `conexao`: o item volta ao lugar dele num mapa, numa grade ou numa linha do tempo.
