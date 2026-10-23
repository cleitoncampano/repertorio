# template-copa-do-mundo: Template Copa do Mundo (SOAP)

## O que é

Template de PowerPoint da SOAP com tema de Copa do Mundo de futebol (pela bola e pelas cidades-sede no mapa, a Copa de 2014 no Brasil), exportado para PDF a partir de `soap/templates/Template_Copa_do_Mundo.ppt`. 10 páginas: capa, agenda, sete slides de roteiro e a página de divulgação da SOAP. Sem parceiros citados.

## O que ensina

**Roteiro de aprovação de projeto** (`roteiro-aprovacao-de-projeto`, p2-9). A agenda (p2) lista os sete passos, e cada um ganha um slide:

1. Cenário atual (p3): onde estamos hoje.
2. Oportunidade (p4): o que dá para ganhar.
3. Projeto (p5): o que se propõe fazer.
4. Plano de ação (p6): as etapas; único slide sem tópicos, com quatro chamadas ligadas a uma jogada na prancheta.
5. Benefícios e melhorias (p7): o que muda; até seis tópicos.
6. Budget (p8): o orçamento.
7. Próximos passos (p9): o que precisa acontecer depois da reunião.

É o mesmo roteiro do `template-aprovacao-de-projeto`, com "Budget" no lugar de "Análise financeira".

**Regras de slide como texto de exemplo** (`design-de-slide`, p3-9): em vez de Lorem ipsum, os tópicos dizem: "Não mais que seis bullets por slide", "Não mais que uma mensagem por slide", "Use linguagem visual como apoio para o texto".

**Motivo visual do tema** (`motivo-visual-do-setor`, p1-9): cada passo do roteiro ganha um objeto do futebol que funciona como metáfora do passo: a taça na capa (o objetivo), o campo com posições na agenda (a escalação), a bola no cenário atual, a chuteira chutando na oportunidade, a planta técnica do estádio no projeto, a prancheta tática no plano de ação, o apito nos benefícios, a moeda que vira globo no budget e as chuteiras paradas nos próximos passos. Triângulos amarelos, verdes e vermelhos sobre azul-petróleo amarram tudo às cores da bandeira.

Divulgação da SOAP na p10 ("Conheça os produtos SOAP", "Baixe outros materiais gratuitos", "Gostou? Compartilhe.").

## Frases-chave

- "Não mais que seis bullets por slide" (p3)
- "Não mais que uma mensagem por slide" (p3)
- "Use linguagem visual como apoio para o texto" (p3)

## Linguagem visual do deck

- Paleta: azul-petróleo #306B76 dominante, amarelo #FCD235, verde #6AA338 (capa #769B43), vermelho #E8173F nos títulos de plano e benefícios, cinza-claro #E5E5E5 nos slides claros, branco.
- Tipografia: títulos em sem serifa condensada negrito em caixa alta (tipo Bebas Neue ou Impact condensada); tópicos em sem serifa geométrica (parece Century Gothic) com a palavra-chave em negrito.
- Modelos que se repetem: triângulo colorido (às vezes invertido) atrás do título, objeto fotografado recortado do futebol, alternância de slides azul-petróleo e cinza-claro, fios finos ligando texto a pontos da imagem.
- Marcante: cada passo do roteiro tem um objeto-metáfora próprio; agenda e plano de ação usam o código do esquema tático.
- Falhas de exportação ou do original: nenhuma de exportação visível. No original, "mensagempor" sem espaço (p7) e endereços "ww.soap.com.br" sem o terceiro w (p10).

## Ficha do deck

```json
{"titulo":"Copa do Mundo: aprovação de projeto em campo",
 "resumo":"Template esportivo com roteiro de aprovação de projeto em sete passos, cada um ilustrado por um objeto do futebol (bola, chuteira, prancheta, apito, moeda-globo) sobre azul-petróleo com triângulos amarelos.",
 "ideia":"Use um único universo temático e dê a cada passo do roteiro um objeto desse universo que funcione como metáfora do passo.",
 "como_funciona":"A agenda já mostra o roteiro como um time escalado e cada slide seguinte retoma o tema com um objeto diferente; os triângulos e a paleta da bandeira mantêm a unidade enquanto o título condensado gigante dá o ritmo.",
 "intencoes":["SITUAR","EXPLICAR","ABRIR"],
 "tecnicas":["metafora-visual","conexao","contraste-de-cor","referencia-cultural"],
 "movimento":["estatico"],
 "estetica":["esportivo","colorido","fotografico"],
 "tom":["energetico"],
 "forca":4,
 "bom_para":["apresentação de projeto em época de Copa","campanha interna com tema de futebol","kick off de vendas"],
 "capa":2}
```

## Repetições

- Roteiro (p2): igual ao de `template-aprovacao-de-projeto` p2, trocando "Análise financeira" por "Budget".
- Regras de slide (p3-9): iguais às de `template-aprovacao-de-projeto` p3-11; variante das cinco regras de `template-conquistar-recursos` p2-6.
- Página de divulgação (p10): mesmo fundo de canetas e laser de `template-conquistar-recursos` p7, com outro texto.

## Ids de conceito usados

- `roteiro-aprovacao-de-projeto`: sequência para aprovar um projeto (cenário atual, oportunidade, projeto, plano de ação, benefícios e melhorias, budget ou análise financeira, próximos passos).
- `motivo-visual-do-setor`: identidade construída com objetos e padrões do universo do tema, que viram metáfora de cada slide.
- `design-de-slide`: id da Perestroika; as três regras de slide usadas como texto de exemplo.

## Páginas puladas ou duvidosas

- Nenhuma ilegível. p10 é divulgação; o texto dela só está na imagem.
