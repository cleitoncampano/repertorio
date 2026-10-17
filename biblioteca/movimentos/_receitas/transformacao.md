## Receita com o motor

```html
<!-- A: um círculo pequeno de cor -->
<div data-m="forma" style="position:absolute;left:1500px;top:700px;width:180px;height:180px;border-radius:50%;background:var(--acento)"></div>
<!-- B: a mesma forma vira o painel de fundo do conteúdo -->
<div data-m="forma" style="position:absolute;left:0;top:0;width:960px;height:1080px;border-radius:0;background:var(--acento)"></div>
```

- Uma forma da identidade muda de papel ao longo da apresentação: ponto, moldura, painel, véu sobre foto, anel de dado.
- Antes e depois: duas imagens com o mesmo `data-m` no mesmo lugar fazem fusão; para revelar com cortina use `data-entra="mascara"`.
- Limite: contornos muito diferentes (círculo para retângulo) se fundem, não deformam continuamente.
