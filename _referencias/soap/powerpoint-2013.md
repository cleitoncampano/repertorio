# Guia básico de ferramentas do PowerPoint 2013 (SOAP)

## O que é

Guia horizontal de 24 páginas da SOAP: "10 ferramentas do PowerPoint que você não pode deixar de conhecer", para a versão 2013. Público: quem monta os próprios slides. Cada ferramenta tem duas páginas: um divisor colorido com o motivo de usar e um tutorial com quatro passos (A a D) em capturas de tela; fecha com duas páginas de dicas e uma de divulgação. Os menus são do PowerPoint 2013; abaixo fica o que é transferível.

## O que ensina

### As 10 ferramentas, com o motivo de usar (menus resumidos)

1. **Réguas, linhas de grade e guias** (p2-3) `alinhamento-e-grade`: usar "sempre que houver a necessidade de alinhamento"; o slide fica quadriculado e facilita alinhar um objeto com o outro; desligar depois para o slide ficar limpo. (2013: aba Exibição.)
2. **Tamanho do slide** (p4-5) `formato-de-tela`: ajustar para "se adequar ao tamanho de telões". O padrão antigo é 4x3 (quase quadrado); o usado hoje é 16x9 (widescreen); há tamanho personalizado para telas especiais. Regra transferível: saber o formato da tela onde será projetado antes de diagramar. (2013: aba Design, Tamanho do Slide.)
3. **Inserir vídeo** (p6-7) `video-na-apresentacao`: vídeos "podem ajudar a audiência a entender melhor o conteúdo" e deixam a apresentação "mais dinâmica". Cuidados que valem para qualquer versão: guardar a apresentação na mesma pasta do vídeo para não corromper o link e usar nome de arquivo de vídeo curto. (2013: Inserir, Vídeo, Vídeo em meu PC.)
4. **Cortar imagem** (p8-9) `tratamento-de-imagem`: cortar partes de imagens .jpg e .png, "deixando apenas o importante".
5. **Redefinir imagem** (p10-11) `tratamento-de-imagem`: voltar a imagem ao tamanho original "sem perda de qualidade" depois de redimensionar.
6. **Girar a imagem** (p12-13) `tratamento-de-imagem`: "A posição de uma imagem pode influenciar na diagramação e/ou no contexto de um slide."
7. **Recorte de fundo (remover plano de fundo)** (p14-15) `tratamento-de-imagem`: útil para quem muda a cor do fundo do slide e dá "um toque de capricho". O programa marca em rosa o que vai recortar e costuma "se enganar"; corrige-se marcando áreas para manter ou para remover. Exemplo do material: uma bola de futebol recortada ocupa o lugar da letra O na palavra BOLA (p15).
8. **Ordenar objetos** (p16-17) `alinhamento-e-grade`: organizar a sobreposição (trazer para frente, enviar para trás). Diferença: "Avançar" põe o objeto à frente só do seguinte; "Trazer para frente" põe à frente de todos.
9. **Alinhar** (p18-19) `alinhamento-e-grade`: vale para qualquer objeto, "a ferramenta ideal para uma boa diagramação"; para alinhar objetos entre si, selecionar dois ou mais (com Shift) e escolher o alinhamento.
10. **Pincel de formatação** (p20-21) `consistencia-de-formatacao`: copia a formatação de um objeto para outro (formas e textos), garantindo consistência; ESC para parar.

### Dicas (p22-23)

- **Redimensionar imagens** (p22) `tratamento-de-imagem`: certo: ampliar ou reduzir imagens e formas circulares pelo canto, segurando Shift, para manter a proporção. Errado: "Nunca redimensione a imagem pelas laterais" (deforma).
- **Copiar slides de outra apresentação** (p23) `consistencia-de-formatacao`: em três passos (copiar os slides, colar na barra de slides da apresentação de destino, escolher "Manter Formatação Original" nas opções de colagem) para não perder o visual do slide de origem.

### Modelo de página do guia (método de tutorial)

Cada ferramenta segue o par: (1) divisor em cor chapada com número, nome da ferramenta, uma frase com o motivo de usar e um objeto real que encena a ferramenta (régua, tesoura, binóculo meio pixelado, maçã sobre laranja, lápis alinhados, pincel); (2) tutorial com barra lateral na mesma cor e grade 2 por 2 de capturas com letras A a D. A cor muda a cada capítulo (roxo, azul, verde, vermelho, laranja), o que ajuda a perceber a troca de assunto.

## Frases-chave

- "As ferramentas 'Régua, Linhas de Grade e Guias' devem ser utilizadas sempre que houver a necessidade de alinhamento" (p2)
- "Vídeos podem ajudar a audiência a entender melhor o conteúdo da sua apresentação, além de torná-la mais dinâmica" (p6)
- "Serve para cortar partes das imagens, deixando apenas o importante" (p8)
- "A posição de uma imagem pode influenciar na diagramação e/ou no contexto de um slide" (p12)
- "É a ferramenta ideal para uma boa diagramação" (p18)
- "Nunca redimensione a imagem pelas laterais" (p22)

## Linguagem visual do deck

- Paleta: laranja SOAP (#FF6A00), roxo (#5E4A9C), azul (#25A0C8), verde (#8DBE3F), vermelho (#E1262B), cinza claro (#EDEDED) nas páginas de tutorial, grafite (#2B2B2B) em capa, dicas e contracapa.
- Tipografia: slab serif condensada pesada em caixa alta para títulos (estilo Ultra/Rockwell condensada), sem serifa (estilo DIN) para o corpo; números de capítulo grandes.
- Modelos de página: capa laranja; divisor colorido com objeto-metáfora recortado; tutorial com barra lateral e grade de capturas A a D; dicas com faixa preta "DICAS!"; contracapa de divulgação.
- Marcante: cada ferramenta ganha um objeto que a encena e uma cor de capítulo.

## Ficha do deck

```json
{"titulo":"Guia básico do PowerPoint 2013","resumo":"Guia da SOAP com dez ferramentas do PowerPoint (réguas, tamanho do slide, vídeo, cortar, redefinir, girar, remover fundo, ordenar, alinhar, pincel) em pares de divisor colorido e tutorial de quatro passos, mais dicas de redimensionar e copiar slides.","ideia":"Abra cada ferramenta com um divisor de cor própria e um objeto real que encena o verbo (tesoura para cortar, lápis enfileirados para alinhar) e siga com o passo a passo em grade.","como_funciona":"A troca de cor a cada capítulo marca o assunto; o divisor diz para que serve a ferramenta e a página seguinte mostra como usar, com letras A a D ligando texto e capturas.","intencoes":["SEQUENCIAR","DIVIDIR","EXPLICAR"],"tecnicas":["cor-por-capitulo","metafora-visual","grade-modular","numeracao"],"movimento":["estatico"],"estetica":["corporativo","colorido","fotografico"],"tom":["tecnico"],"forca":3,"bom_para":["tutorial de software em slides","manual com capítulos coloridos","divisores com objeto-metáfora"],"capa":10}
```

## Repetições

- A contracapa p24 tem o mesmo desenho da contracapa do `swot-tosw` p20 (teclado com cursor no logo da SOAP).
- Alinhamento e respiro (p2-3, p18-19) é a versão prática do item "Utilize a diagramação para organizar e dar os respiros necessários" do `checklist-apresentacao-impactante` p2.
- Vídeo para a audiência entender melhor (p6) se relaciona com o item "Adicione animações [...] para que a audiência acompanhe o seu discurso" do mesmo checklist.

## Ids de conceito usados

- `alinhamento-e-grade`: réguas, grades e guias, alinhar objetos entre si e ordenar camadas para uma boa diagramação.
- `formato-de-tela`: escolher 16x9, 4x3 ou tamanho personalizado conforme o telão.
- `video-na-apresentacao`: vídeo para a audiência entender e para dinamizar; cuidados com pasta e nome do arquivo.
- `tratamento-de-imagem`: cortar, redefinir, girar, remover fundo e redimensionar sem deformar.
- `consistencia-de-formatacao`: pincel de formatação e manter a formatação original ao copiar slides.

## Páginas puladas ou duvidosas

- Nenhuma ilegível. p1 não tem texto extraível; foi lida pela imagem.
- Na p15 o material escreve "Manter Áreas para Remover"; o nome do botão no PowerPoint é "Marcar Áreas para Remover" (corrigido no texto).
- Não selecionadas: p1 (capa genérica), divisores p2, p4, p6, p8, p12, p14, p16, p20 (mesmo modelo de p10 e p18), tutoriais p5, p7, p9, p11, p13, p15, p17, p19, p21 (mesmo modelo de p3), p24 (divulgação).
- A capa do deck no mapa é a p10 (binóculo meio pixelado), que representa melhor o modelo do guia do que a capa com o ícone do software.
