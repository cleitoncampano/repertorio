# Como escrever as fichas das referências externas

As imagens da pasta `_referencias` são peças de nível mundial (capas de revista, anúncios, ativações, aberturas de filmes,
campanhas, frames de vídeos sobre criação). Elas entram na mesma biblioteca do PPTRETA e se ligam pelas mesmas técnicas.
Quem vai ler as fichas é um modelo de IA criando apresentações, sites e vídeos para qualquer tema. Então a pergunta é:
**qual é o princípio desta peça que eu posso levar para um slide?**

## Por lote

1. Leia `dados/_trabalho/ref-lotes/lote-NNN.json`: lista de itens (id, arquivo, fonte, estudo) e as imagens das folhas (6 por folha, numeradas na ordem dos itens).
2. Leia as folhas do lote na mesma rodada. Se o item tiver `estudo` e você ainda não leu aquele estudo nesta sessão, procure nele o nome do arquivo da imagem (busca por texto) para aproveitar a análise que já existe; não precisa ler o estudo inteiro.
3. Grave `dados/_trabalho/referencias/lote-NNN.json` numa única gravação: lista JSON com uma ficha por item, na mesma ordem.
4. Rode `python3 -I ferramentas/construir/validar.py dados/_trabalho/referencias/lote-NNN.json` e corrija até dar OK.

## Campos

| campo | o que é |
|---|---|
| `id` | igual ao do item |
| `arquivo` | igual ao do item |
| `fonte` | igual ao do item |
| `tipo` | `capa`, `anuncio`, `ativacao`, `campanha`, `abertura-de-filme`, `frame-de-filme`, `livro`, `diagrama` (esquema explicativo), `retrato`, `interface` |
| `o_que` | 1 frase concreta do que se vê |
| `ideia` | 1 ou 2 frases no imperativo com o princípio transferível para um slide de qualquer tema, sem citar a marca |
| `como_levar_para_slide` | 1 frase: como esse princípio vira um slide (layout, imagem, texto, movimento) |
| `intencoes` | 1 ou 2 ids de intenção: que papel essa ideia faria numa apresentação |
| `tecnicas` | 1 a 4 ids de técnica |
| `estetica` | 1 a 4 rótulos |
| `tom` | 1 ou 2 |
| `forca` | 1 a 5 como referência para criar (diagramas e telas costumam ser 2 ou 3; uma capa clássica pode ser 5) |

Vocabulário: o mesmo de `dados/vocabulario.json` (veja a lista resumida em `dados/_trabalho/INSTRUCOES-FICHAS.md`).
Sem travessão nem meia-risca (os traços longos de pontuação). Português do Brasil.

## Exemplo

```json
{"id": "ref-11-02-case-heinz-dipper", "arquivo": "_referencias/sites/11_activation_ideas/imagens/02_case_heinz_dipper.jpg",
 "fonte": "Activation Ideas (ativações)", "tipo": "ativacao",
 "o_que": "Embalagem de batata frita com um compartimento lateral em forma de sachê de ketchup, sobre fundo vermelho.",
 "ideia": "Resolva um incômodo pequeno e conhecido de todos com um ajuste no próprio objeto; a solução vira a imagem e dispensa explicação.",
 "como_levar_para_slide": "Mostre o objeto do dia a dia em close sobre fundo de uma cor só e deixe o detalhe modificado ser o único ponto de atenção, com uma frase curta.",
 "intencoes": ["MOSTRAR", "IMPACTAR"], "tecnicas": ["metafora-visual", "isolamento", "contraste-de-cor"],
 "estetica": ["fotografico", "minimalista", "colorido"], "tom": ["divertido"], "forca": 4}
```
