# template-saude: Template Área da Saúde (SOAP)

## O que é

Template de PowerPoint da SOAP para apresentações da área da saúde (clínicas, hospitais, farmacêuticas, bem-estar), exportado para PDF a partir de `soap/templates/Template_Area_da_Saude.pptx`. 15 páginas: 11 modelos de slide para preencher, 3 páginas de tutorial de edição e 1 de divulgação. Anos de exemplo na linha do tempo vão até 2019; sem data de publicação nem parceiros citados.

## O que ensina

**Sequência de slides proposta** (`kit-de-modelos-de-pagina`, p1-11). O template não traz um roteiro de demanda; oferece um kit de modelos de página na ordem em que costumam aparecer:

1. Capa (p1): título da apresentação, subtítulo, espaço para o logo.
2. Agenda (p2): cinco itens numerados, cada um com uma linha.
3. Comparação (p3): título, dois blocos de texto separados por um X, cada um sob uma metade de cápsula.
4. Linha do tempo em dois slides (p4-5): oito marcos anuais (2012 a 2019), quatro por slide; o ano em destaque e uma frase por marco. A linha sai pela borda da p4 e entra pela borda da p5.
5. Texto com destaque (p6): título, parágrafo longo e legenda curta ao lado de uma foto de objeto.
6. Gráfico de colunas (p7): três categorias, três séries, valores escritos no topo de cada coluna, legenda.
7. Tabela (p8): sete linhas e seis colunas (categoria, números, porcentagem, valor em reais), uma linha destacada e nota de rodapé.
8. Três tópicos numerados (p9): números grandes, uma chave que agrupa e texto curto.
9. Lista longa (p10): até 16 tópicos em duas colunas, com legenda num hexágono.
10. Contato (p11): telefone, celular, e-mail e site.

Em todos os slides internos o título segue a mesma fórmula: uma linha fina em caixa alta ("Seu título com") e uma palavra em negrito itálico grande ("destaque"). O template ensina, na prática, a ter um título de duas camadas: contexto pequeno e palavra-chave grande.

**Motivo visual do setor** (`motivo-visual-do-setor`, p1-11). A identidade vem de dois recursos: um padrão de hexágonos em linha branca (lembra estrutura molecular) nas bordas e objetos do universo da saúde fotografados e recortados (cápsula, comprimidos, frasco de vacina, microscópio, coração anatômico, garfo com brócolis, tênis e anilha de academia, prancheta com lápis). Os objetos não são só enfeite: em três páginas viram parte da informação, a cápsula aberta como os dois lados da comparação (p3), os comprimidos como marcos da linha do tempo (p4-5), o lápis como eixo do gráfico (p7).

**Tabela com destaque** (`design-de-informacao`, p8): tabela sem grades verticais, só fios horizontais, com uma linha numa faixa mais escura e em negrito para conduzir a fala ao item que importa.

**Tutorial de edição** (`editar-template-no-powerpoint`, p12-14):
- Todos os elementos gráficos foram desenhados no próprio PowerPoint, então podem ser alterados, reposicionados e adaptados sem distorção nem perda de qualidade (p13-14).
- Alterar a cor de preenchimento: Ferramentas de Desenho, Formatar, Preenchimento da Forma. Usar as cores pré-definidas, "Mais cores de preenchimento" para as cores da marca, ou o Conta-gotas para copiar uma cor de imagem (p13).
- Alterar a cor de contorno: Formatar, Contorno da Forma; também muda espessura e tipo de traço (p13).
- Redimensionar imagem proporcionalmente: arrastar a bolinha do canto segurando Shift (p14).
- Cortar imagem: Ferramentas de Imagem, Formatar, Cortar; arrastar as marcas pretas da borda e soltar. O corte não descarta nada da imagem, cria uma "máscara de corte"; para voltar ao original, selecionar corte e arrastar as arestas (p14).

Divulgação dos treinamentos SOAP na p15.

## Frases-chave

- "Todos os elementos gráficos foram desenvolvidos diretamente no Power Point, o que possibilita a edição sem distorções" (p13)
- "Esta ação não descarta nada da imagem original, apenas cria uma 'máscara de corte'" (p14)
- "Seu título com destaque" (p3, fórmula de título repetida nos slides internos)

## Linguagem visual do deck

- Paleta: azul médio dominante #4D70A6, azul-escuro #3B5680 para faixas e hexágonos de legenda, azul-claro #8EC5E6 e bege #E8D5C0 nas séries do gráfico, branco no texto. Tutorial em preto #101010 com destaque amarelo-alaranjado; divulgação em laranja #F93F03.
- Tipografia: sem serifa humanista; títulos com linha fina em caixa alta mais palavra grande em negrito itálico (parece Ubuntu ou similar).
- Modelos que se repetem: fundo azul chapado, padrão de hexágonos em linha nas bordas, hexágonos soltos e traços diagonais brancos como enfeite, objeto recortado com sombra suave, fio fino ligando legenda ao objeto.
- Marcante: os objetos do setor viram estrutura do dado (cápsula, comprimido, lápis).
- Falhas de exportação: nenhuma visível; fontes e imagens parecem íntegras.

## Ficha do deck

```json
{"titulo":"Template Área da Saúde em azul com hexágonos",
 "resumo":"Template corporativo para a área da saúde em azul chapado, com padrão de hexágonos e objetos médicos recortados que entram na própria informação (cápsula, comprimidos, lápis).",
 "ideia":"Escolha objetos do setor e faça deles parte do dado: metade de cápsula como lado da comparação, comprimido como marco da linha do tempo, lápis como eixo do gráfico.",
 "como_funciona":"Um fundo único e um padrão gráfico discreto dão unidade; cada slide traz um objeto fotografado que identifica o tema sem texto, e a fórmula de título em duas camadas mantém a hierarquia igual em todo o deck.",
 "intencoes":["ABRIR","COMPARAR","SEQUENCIAR"],
 "tecnicas":["metafora-visual","objeto-como-suporte","similaridade","hierarquia-de-leitura"],
 "movimento":["estatico"],
 "estetica":["corporativo","fotografico","monocromatico"],
 "tom":["tecnico","acolhedor"],
 "forca":3,
 "bom_para":["apresentação de clínica ou hospital","relatório de indicadores de saúde","palestra sobre bem-estar"],
 "capa":3}
```

## Repetições

- Tutorial de edição (p13-14): mesmo texto e desenho quase igual de `template-rh` p2-3; mesmo conteúdo, com outro desenho, em `template-integracao` p14 e nas telas de instrução de `template-bancos`.
- Página de divulgação (p15): mesma lista de seis cursos de `template-bancos` p38 e `template-lancamento-de-produto` p13; `template-rh` p25 traz uma lista ampliada.
- Linha do tempo dividida em dois slides (p4-5): mesma solução de `template-clean-e-moderno` p8-9 e da instrução de `template-bancos` p19.

## Ids de conceito usados

- `kit-de-modelos-de-pagina`: o conjunto de modelos de slide que um template oferece (capa, agenda, comparação, linha do tempo, gráfico, tabela, tópicos, lista, contato) e a fórmula comum de título.
- `motivo-visual-do-setor`: construir a identidade do template com um padrão gráfico e objetos fotografados do setor, que passam a fazer parte da informação.
- `design-de-informacao`: id da Perestroika; aqui, tabela e gráfico com destaque de uma linha ou série.
- `editar-template-no-powerpoint`: tutorial que acompanha o template (cor de preenchimento e contorno, redimensionar e cortar imagem).

## Páginas puladas ou duvidosas

- Nenhuma ilegível. p15 é divulgação. As páginas sem texto extraível (p12 só com a palavra TUTORIAL e p15 com texto parcialmente na imagem) foram lidas pela imagem.
