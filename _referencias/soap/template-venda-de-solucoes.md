# template-venda-de-solucoes: Template Venda de Soluções (SOAP)

## O que é

Template de PowerPoint da SOAP, em formato 4:3, para apresentar uma solução a um cliente (venda consultiva, B2B), exportado para PDF a partir de `soap/templates/Template_Venda_de_Solucoes.ppt`. 9 páginas: capa, cinco slides de roteiro, dois modelos de caixa de texto e a página de contato da SOAP (Brasil, Estados Unidos e Portugal). Sem data; logo antigo da SOAP.

## O que ensina

**Roteiro de venda de soluções** (`roteiro-venda-de-solucoes`, p1-6):

1. Capa (p1): "A nossa solução", nome do apresentador, logo.
2. Sua necessidade (p2): o problema do cliente, em tópicos.
3. Nossa solução (p3): subtítulo que resume a solução e tópicos.
4. Benefícios da solução (p4): até quatro tópicos.
5. Como implementar (p5): passos de implantação.
6. Resultados (p6): o que o cliente vai obter.

O roteiro começa pelo cliente ("sua necessidade") e só depois fala da empresa ("nossa solução"): a ordem dos pronomes nos títulos é o método. Cada slide de conteúdo tem até três ou quatro tópicos e um título grande em minúsculas.

Modelos de caixa de texto (p7-8): caixa azul chapada e caixa branca com sombra sobre fundo preto; caixa de contorno fino sobre branco e sobre preto.

**Metáfora condutora** (`metafora-condutora`, p1-6): três sólidos geométricos (cubo, prisma em forma de casa e cilindro) contam a venda em paralelo ao texto. Na capa estão desenhados na prancheta (projeto); na necessidade são só linhas de construção com setas para baixo (falta, queda); na solução ganham volume e sombra; nos benefícios encaixam nos buracos certos de uma caixa de encaixe; na implementação aparecem as ferramentas de desenho (lapiseira, compasso, pincel); nos resultados a caixa está cheia de peças encaixadas.

Contato da SOAP na p9.

## Frases-chave

- "sua necessidade" (p2, título que abre o roteiro pelo cliente)
- "nossa solução" (p3)
- "benefícios da solução" (p4)
- "como implementar" (p5)
- "resultados" (p6)

## Linguagem visual do deck

- Paleta: branco dominante, preto nos títulos e na faixa de rodapé, azul #0A7DC8 na faixa da capa e nos subtítulos, formas em cinza-azulado aquarelado.
- Tipografia: sem serifa humanista (parece Tahoma), títulos enormes em minúsculas negrito, tópicos com marcador quadrado azul.
- Modelos que se repetem: formas geométricas desenhadas com linhas de construção a lápis e sombra de aquarela, linhas verticais finas de esboço atravessando a página, rodapé preto com um pequeno retângulo branco (espaço do logo).
- Marcante: as mesmas três formas mudam de estado (esboço, sólido, encaixado, caixa cheia) a cada passo da venda.
- Falhas de exportação: nenhuma visível. O retângulo branco no rodapé é o espaço vazio para o logo.

## Ficha do deck

```json
{"titulo":"Venda de soluções com sólidos que se encaixam",
 "resumo":"Template 4:3 de venda consultiva com roteiro de seis slides (necessidade, solução, benefícios, implementação, resultados) e três sólidos geométricos que passam de esboço a peças encaixadas numa caixa.",
 "ideia":"Comece pela necessidade do cliente e faça um mesmo conjunto de formas evoluir de esboço vazio a peças que encaixam, acompanhando o argumento.",
 "como_funciona":"Os títulos em minúsculas gigantes dão o passo da conversa e a imagem mostra o estado da solução: incompleta no problema, encaixada nos benefícios, completa nos resultados.",
 "intencoes":["EXPLICAR","ABRIR","PROVAR"],
 "tecnicas":["metafora-visual","transformacao","contraste-de-escala"],
 "movimento":["estatico"],
 "estetica":["ilustrado","minimalista","claro"],
 "tom":["serio"],
 "forca":4,
 "bom_para":["proposta comercial B2B","apresentação de solução para cliente","venda consultiva"],
 "capa":4}
```

## Repetições

- A estrutura de metáfora que evolui do esboço ao objeto real é a mesma de `template-conquistar-recursos` p1-6 (balão do desenho à cor).
- Página de contato (p9) com os três sites da SOAP: mesmo conteúdo de `template-conquistar-recursos` p7, com outra imagem.

## Ids de conceito usados

- `roteiro-venda-de-solucoes`: sequência para vender uma solução (sua necessidade, nossa solução, benefícios, como implementar, resultados), começando pelo cliente.
- `metafora-condutora`: um mesmo conjunto de objetos atravessa o deck e muda de estado junto com o argumento.

## Páginas puladas ou duvidosas

- Nenhuma ilegível. p7 e p8 são caixas de texto vazias; p9 é contato da SOAP (sem texto extraível, lida pela imagem).
