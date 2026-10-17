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
