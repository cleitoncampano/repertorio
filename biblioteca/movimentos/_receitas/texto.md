## Receita com o motor

```html
<section class="slide">
  <span data-m="w1" class="palavra" style="left:120px;top:300px;font-size:150px">Menos</span>
  <span data-m="w2" class="palavra" style="left:120px;top:470px;font-size:150px">slides</span>
</section>
<section class="slide">
  <span data-m="w1" class="palavra" style="left:120px;top:140px;font-size:60px;opacity:.5">Menos</span>
  <span data-m="w2" class="palavra" style="left:100px;top:300px;font-size:420px;color:var(--acento)">slides</span>
  <span class="palavra" data-passo="0" data-entra="sobe" style="left:120px;top:820px;font-size:60px">mais conversa</span>
</section>
```

- Uma palavra por elemento (`.palavra { position:absolute; white-space:nowrap }`). As que continuam ganham `data-m`; as novas entram com passo.
- Ótimo para frase de efeito que se reorganiza, título que vira subtítulo, palavra-chave que cresce.
