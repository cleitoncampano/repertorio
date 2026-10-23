# template-educacao: Template Educação (SOAP)

## O que é

Template de PowerPoint da SOAP, em formato 4:3, para apresentação institucional de escola, curso ou empresa de educação, exportado para PDF a partir de `soap/templates/Template_Educacao.ppt`. 9 páginas: capa, agenda, seis slides de conteúdo institucional e a página de contato da SOAP (Estados Unidos e Brasil). Sem data; logo antigo da SOAP.

## O que ensina

**Roteiro de apresentação institucional** (`apresentacao-institucional`, p1-8):

1. Capa (p1): título e nome do apresentador.
2. Agenda (p2): quatro itens numerados.
3. Posicionamento (p3): como a instituição quer ser vista; tópicos.
4. Visão (p4): parágrafo.
5. Missão (p5): parágrafo.
6. Valores (p6): tópicos.
7. Nossa linha de produtos (p7): quatro chamadas ligadas a uma imagem.
8. Clientes (p8): parede de até dez logos.

**Regras de slide como texto de exemplo** (`design-de-slide`, p3 e p6): "Não mais que seis bullets por slide.", "Não mais que uma mensagem por slide.", "Use linguagem visual como apoio para o texto." (p3) e "Sua audiência lerá seus slides, não você." (p6).

**Motivo visual do setor** (`motivo-visual-do-setor`, p1-7): material escolar fotografado como metáfora de cada slide: lápis desenhando o balão de pensamento (capa), pilha de livros cujas páginas viram as faixas da agenda, compasso desenhando um círculo (posicionamento), livro e óculos (visão), boneco de madeira com maçã e linha de crescimento (missão), caça-palavras com marca-texto (valores), porta-lápis de cor (linha de produtos), estudante com cadernos (clientes). Em duas páginas o objeto vira a própria estrutura da informação: os livros viram as barras da agenda (p2) e o caça-palavras esconde a palavra-chave (p6).

Página de contato da SOAP na p9.

## Frases-chave

- "Não mais que seis bullets por slide." (p3)
- "Não mais que uma mensagem por slide." (p3)
- "Use linguagem visual como apoio para o texto." (p3)
- "Sua audiência lerá seus slides, não você." (p6)

## Linguagem visual do deck

- Paleta: cinza-claro #E6E6E6 de fundo, azul #1084C9 de destaque, azul-escuro #23597C nas sombras dos livros, preto #030303 nas caixas de título, amarelo-limão do marca-texto, vermelho da maçã.
- Tipografia: sem serifa humanista, títulos em minúsculas negrito grandes (parece Tahoma ou Segoe UI), trechos do texto em azul negrito.
- Modelos que se repetem: fundo cinza em degradê suave, objeto escolar recortado com sombra, caixa preta com título branco ou azul, fios finos e linhas tracejadas.
- Marcante: objetos escolares reais que se transformam em gráfico (livros em faixas, maçã em linha de crescimento).
- Falhas de exportação ou do original: nenhuma de exportação. No caça-palavras da p6 a palavra marcada está em inglês ("VALUES"), herdada da foto, num template em português.

## Ficha do deck

```json
{"titulo":"Template Educação com material escolar",
 "resumo":"Template institucional 4:3 para escola ou empresa de educação com lápis, livros, compasso e marca-texto fotografados que viram parte da informação (livros como faixas da agenda, caça-palavras para os valores).",
 "ideia":"Transforme o material do setor em estrutura do slide: as páginas dos livros viram as barras da agenda, o marca-texto acha a palavra-chave num caça-palavras.",
 "como_funciona":"Cada slide do roteiro institucional tem um objeto escolar que dá o tema sem texto; o azul aparece só em barras, títulos e trechos de destaque, e as caixas pretas concentram a leitura.",
 "intencoes":["SITUAR","DESTACAR","ABRIR"],
 "tecnicas":["objeto-como-suporte","metafora-visual","destaque-tipografico"],
 "movimento":["estatico"],
 "estetica":["claro","fotografico","corporativo"],
 "tom":["acolhedor","calmo"],
 "forca":3,
 "bom_para":["apresentação institucional de escola","abertura de curso","apresentação de empresa de educação"],
 "capa":2}
```

## Repetições

- Regras de slide (p3): iguais às de `template-copa-do-mundo` p3-9 e `template-aprovacao-de-projeto`; a da p6 ("Sua audiência lerá seus slides, não você") aparece também em `template-conquistar-recursos` p2-6.
- Página de contato (p9): mesmo fundo de canetas e laser de `template-conquistar-recursos` p7 (aqui sem Portugal).
- O roteiro institucional (posicionamento, visão, missão, valores, produtos, clientes) dialoga com o e-book "Guia SOAP para uma apresentação institucional", de outro lote.

## Ids de conceito usados

- `apresentacao-institucional`: roteiro de apresentação da instituição (posicionamento, visão, missão, valores, produtos, clientes).
- `motivo-visual-do-setor`: objetos do universo do tema (material escolar) como metáfora e estrutura de cada slide.
- `design-de-slide`: id da Perestroika; regras de slide usadas como texto de exemplo.

## Páginas puladas ou duvidosas

- Nenhuma ilegível. p8 é parede de logos e p9 é contato da SOAP. As páginas com pouco ou nenhum texto extraível (p2 e p9) foram lidas pela imagem.
