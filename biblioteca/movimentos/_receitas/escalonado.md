## Receita com o motor

```html
<div class="card" data-passo="1" data-entra="sobe">...</div>
<div class="card" data-passo="1" data-entra="sobe">...</div>
<div class="card" data-passo="1" data-entra="sobe">...</div>
```

- Itens com o mesmo número de passo entram juntos com 90 ms de diferença (ajuste com `style="--i:3"`).
- `data-passo="0"` faz a cascata começar sozinha ao entrar no slide.
