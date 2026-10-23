# Como etiquetar a mídia do acervo

São imagens e vídeos tirados de dentro dos arquivos do acervo. A etiqueta serve para um modelo de IA achar a peça
certa pela busca ("recorte de pessoa sorrindo", "textura de papel", "celular na mão") e saber se pode usar.

## Por lote

1. Leia `dados/_trabalho/midia-lotes/lote-NNN.json` (lista de itens com `id` de 8 caracteres e `uso_auto`) e, na mesma rodada, as folhas do lote (30 prévias por folha, cada uma com o `id` em amarelo no topo; fundo xadrez = transparente).
2. Grave `dados/_trabalho/midia/lote-NNN.json` numa única gravação: um objeto JSON cujas chaves são os `id` e os valores são:

```json
{"o_que": "mulher de blazer azul sorrindo, braços cruzados", "tags": ["pessoa", "profissional", "sorriso", "corporativo"], "uso": "recorte", "terceiros": false}
```

| campo | o que é |
|---|---|
| `o_que` | até 12 palavras, concreto: sujeito, ação, cor ou material marcante |
| `tags` | 2 a 5 palavras-chave em português, minúsculas, singular |
| `uso` | um de: `foto`, `recorte` (fundo transparente), `fundo` (imagem para ocupar o slide inteiro), `textura`, `padrao`, `icone`, `ilustracao`, `mockup` (aparelho, embalagem ou tela para colocar conteúdo), `logo`, `grafico`, `3d` (render 3D), `tipografia` (texto transformado em imagem), `interface`, `video` |
| `terceiros` | `true` quando mostra marca, logo, produto de marca reconhecível, celebridade, atleta, personagem ou obra protegida; `false` para pessoas e objetos genéricos de banco de imagem |

3. Confira se todas as chaves do lote estão presentes (mesma quantidade de itens do JSON do lote). Prévia ilegível ou vazia: `{"o_que": "ilegível", "tags": [], "uso": "<uso_auto>", "terceiros": false}`.

Português do Brasil, sem travessão nem meia-risca (os traços longos de pontuação).
