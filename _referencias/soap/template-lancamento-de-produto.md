# template-lancamento-de-produto: Template Lançamento de Produto (SOAP)

## O que é

Template de PowerPoint da SOAP para apresentar o lançamento de um produto (para equipe, força de vendas ou parceiros), exportado para PDF a partir de `soap/templates/Template_Lancamento_de_Produto.pptx`. 13 páginas: 12 slides de roteiro e a página de divulgação dos cursos da SOAP. Previsão de exemplo "para 2018". Sem parceiros citados.

## O que ensina

**Roteiro de lançamento de produto** (`roteiro-lancamento-de-produto`, p1-12). Os títulos e as perguntas dos campos são o método:

1. Capa (p1): nome do produto, frase, logo.
2. Agenda (p2): quatro partes, cada uma com ícone e texto.
3. Introdução da marca (p3): "Esse é o espaço para uma introdução"; três blocos: "Fale sobre sua marca", "Quem é o foco da marca?", "Como ela atinge o target?".
4. Cenário do mercado (p4): gráfico "Crescimento de consumo" e um texto de destaque.
5. Cenário do mercado (p5): texto e "Market Share" por trimestre em duas roscas.
6. Oportunidade (p6): "Qual a oportunidade/GAP encontrado?".
7. Revelação do produto (p7): "Apresente aqui o novo produto"; frase de ligação "E por isso, lançamos o..." e a imagem do produto.
8. Defesa (p8): três perguntas: "Qual o conceito por trás desse lançamento?", "Qual o diferencial do produto?", "Qual o público alvo?".
9. Plano de lançamento (p9): data de lançamento, canais, valor (preço), divulgação e cinco etapas numeradas.
10. Crescimento esperado (p10): texto de destaque e previsão por categoria.
11. Próximos passos (p11): cinco itens.
12. Mensagem motivacional (p12): texto de fechamento para engajar a equipe.

A lógica: primeiro o contexto (marca e mercado), depois o problema (oportunidade ou lacuna), só então o produto como resposta ("E por isso, lançamos o..."), seguido da defesa, do plano, da projeção e da chamada para agir. O produto aparece no meio, depois de a plateia entender por que ele existe.

**Gráficos** (`design-de-informacao`, p4, p5, p10): colunas crescentes com valores no topo, roscas por trimestre e por categoria, sempre com uma fita amarela de "Texto de destaque" para a conclusão.

**Metáforas de objeto por slide**: lâmpadas da vela ao LED (capa: evolução), lupa sobre a palavra mercado (cenário), anzol na água (oportunidade), pôster pendurado com fogos (revelação), lápis e papel amassado (defesa), foguete (plano de lançamento), regador e broto (crescimento), placa com seta para cima (próximos passos), troféu (mensagem motivacional).

Divulgação dos cursos da SOAP na p13.

## Frases-chave

- "Esse é o espaço para uma introdução." (p3)
- "Quem é o foco da marca?" (p3)
- "Como ela atinge o target?" (p3)
- "Qual a oportunidade/GAP encontrado?" (p6)
- "E por isso, lançamos o..." (p7)
- "Qual o conceito por trás desse lançamento?" (p8)
- "Qual o diferencial do produto?" (p8)

## Linguagem visual do deck

- Paleta: degradês alternados de laranja #F49E23 para rosa #FF1F55, de verde-água #03E1B8 para azul #1A9BE0, e rosa para roxo #A73477; amarelo #FEB100 nas fitas e gráficos; branco no texto.
- Tipografia: títulos em serifada itálica negrito com espaçamento largo entre letras; corpo em Segoe UI (ou muito parecida) com trechos em negrito itálico.
- Modelos que se repetem: fitas coloridas inclinadas com o título, padrão de cubos em linha no fundo, ícones de linha brancos soltos, objeto fotografado recortado como metáfora, círculos com ponto e fios finos.
- Marcante: alternância de degradês quentes e frios a cada slide e a frase-ponte antes da revelação do produto.
- Falhas de exportação (dúvida): os títulos serifados itálicos e as etiquetas dos cursos na p13 aparecem numa serifada tipo Times New Roman, o que pode ser substituição de fonte na exportação; não há como confirmar sem o original aberto.

## Ficha do deck

```json
{"titulo":"Lançamento de produto em degradês vibrantes",
 "resumo":"Template de lançamento em 12 slides (marca, mercado, oportunidade, revelação, defesa, plano, projeção, próximos passos) com degradês laranja, rosa e verde-água e um objeto-metáfora por slide: lâmpadas, anzol, pôster, foguete, troféu.",
 "ideia":"Antes de mostrar o produto, mostre o mercado e a lacuna; depois revele o produto com uma frase-ponte que termina em reticências.",
 "como_funciona":"Os degradês alternados dão ritmo de festa; cada slide tem um objeto que resume o passo (anzol para oportunidade, foguete para plano). A revelação no meio do deck vira o clímax porque a plateia já sabe o problema que ele resolve.",
 "intencoes":["ABRIR","MOSTRAR","SEQUENCIAR"],
 "tecnicas":["metafora-visual","pergunta-aberta","cor-por-capitulo","progressao-de-escala"],
 "movimento":["estatico"],
 "estetica":["colorido","gradiente","fotografico"],
 "tom":["energetico","inspirador"],
 "forca":4,
 "bom_para":["lançamento de produto para equipe de vendas","convenção comercial","apresentação de nova versão de serviço"],
 "capa":7}
```

## Repetições

- Página de divulgação (p13): mesma lista de seis cursos de `template-saude` p15 e `template-bancos` p38, com outro desenho e frases explicando cada curso.
- Pôster pendurado por prendedores (p7): mesmo recurso de `template-rh` p8.
- Troféu como imagem de vitória (p12): também em `template-curriculo` p19 (ícone) e na capa de `template-copa-do-mundo` p1.

## Ids de conceito usados

- `roteiro-lancamento-de-produto`: sequência para lançar um produto (marca, cenário do mercado, oportunidade, revelação com frase-ponte, defesa com conceito, diferencial e público, plano com data, canais, valor e divulgação, crescimento esperado, próximos passos, mensagem motivacional).
- `design-de-informacao`: id da Perestroika; gráficos de mercado e projeção com texto de destaque.

## Páginas puladas ou duvidosas

- Nenhuma ilegível. p13 é divulgação. Dúvida sobre substituição de fonte nos títulos serifados (ver acima).
