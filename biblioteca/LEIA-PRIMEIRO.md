# Mapa da biblioteca

Leia na ordem em que precisar. Nada aqui precisa ser lido inteiro de uma vez: a busca do Repertório (MCP `search_references`) leva direto ao exemplo certo.

| arquivo | quando ler |
|---|---|
| `processo.md` | sempre que for criar: do pedido à entrega, com os comandos de cada etapa |
| `principios/narrativa.md` | para montar a história e o roteiro de slides (estruturas, ganchos, tensão, viradas, fechamento, checklist) |
| `principios/direcao-de-arte.md` | para decidir o visual (insight, ideia, execução; menu de ingredientes; capa; anúncio; 15 movimentos do comum ao memorável) |
| `principios/fontes.md` | para saber o que cada referência externa ensina e onde estão os estudos completos |
| `intencoes/<INTENÇÃO>.md` | o que um bom slide de cada tipo faz, técnicas e movimentos mais usados, melhores exemplos com caminho da imagem |
| `tecnicas/<id>.md` | definição, como fazer em HTML, com o que combina, exemplos do acervo e de referências externas |
| `movimentos/<id>.md` | receita com o motor do kit e exemplos reais de Morph analisados objeto a objeto |
| `estilos.md` | todos os modelos completos, do mais forte ao mais fraco, com estética, tom, ideia e prancha |
| `efeitos.md` | todos os efeitos (os "reels" do curso) |
| `componentes.md` | gráficos, linhas do tempo, mapas, organogramas, tabelas |
| `tipografia.md` | famílias usadas, pares, o que existe no Google Fonts e onde estão os arquivos de fonte |
| `vocabulario.md` | as listas de intenções, operações do olhar, técnicas, movimentos, estéticas e tons |

As pastas `intencoes/_dicas/` e `movimentos/_receitas/` são fontes escritas à mão que o `montar.py` junta nas páginas principais: leia as páginas, não as pastas.

**Atenção às miniaturas:** são fotos estáticas feitas pelo Mac. Em vários arquivos elas não mostram o efeito real (texto vazado, vídeo dentro das letras, máscaras, fontes que faltavam).
As fichas foram escritas conferindo o arquivo original; quando a miniatura engana, o `como_funciona` avisa. Confie no texto da ficha.

## Como as peças se conectam

```
operação do olhar  (diferenciação · agrupamento · sequência · previsão)
        │
     técnica       (contraste-de-escala, metafora-visual, camera-continua...)
        │
   referência      (arquivo do acervo, slide, capa, anúncio, ativação, frame de vídeo)
        │
 intenção · movimento · estética · tom
```

Uma referência sempre aponta para técnicas; cada técnica pertence a uma operação do olhar. Assim, "quero que a plateia
perceba a diferença" leva a técnicas de diferenciação, que levam a slides do acervo e a capas e anúncios que usam essas técnicas.

## Números

Os totais atualizados (arquivos fichados, slides, referências, mídias) aparecem ao rodar `python3 -I ferramentas/construir/montar.py`.
