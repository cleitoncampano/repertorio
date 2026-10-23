# template-conquistar-recursos: Template Conquistar Recursos (SOAP)

## O que é

Template de PowerPoint da SOAP, em formato 4:3, para pedir verba ou investimento para uma ideia ou projeto, exportado para PDF a partir de `soap/templates/Template_Conquistar_Recursos.ppt`. 7 páginas: capa, cinco slides de roteiro e a página de contato da SOAP (Brasil, Estados Unidos e Portugal). Sem data; pelo logo antigo e pelo formato 4:3, é dos templates mais antigos do lote.

## O que ensina

**Roteiro para conquistar recursos** (`roteiro-conquistar-recursos`, p1-6). A sequência de títulos é o método:

1. Capa (p1): nome do tema ("Conquistar recursos"), título, nome do apresentador, data e espaço para o logo.
2. A ideia (p2): o que é a proposta.
3. Por que investir (p3): a justificativa, o problema ou a oportunidade.
4. Quanto investir (p4): o valor pedido.
5. ROI (p5): o retorno sobre o investimento.
6. Onde investir (p6): onde o dinheiro será aplicado.

Cada slide traz o mesmo modelo: título em duas linhas em caixa alta, fio verde e até cinco tópicos, ao lado de uma imagem. O texto de exemplo não é Lorem ipsum: são regras de slide (`design-de-slide`), repetidas em todos os slides do roteiro (p2-6):
- Nunca use mais de 6 bullet-points por slide.
- Passe uma mensagem por slide.
- A audiência lerá seu slide, não você.
- Use animações para conduzir seu raciocínio.
- Use linguagem visual para ajudar o entendimento.

**Metáfora condutora** (`metafora-condutora`, p1-6): um mesmo símbolo, o balão de ar quente, atravessa todo o deck e conta a história em paralelo ao texto. Na capa ele é só um desenho a lápis subindo entre prédios (p1); na ideia vira lâmpada desenhada (p2); em "por que investir" é um esboço cercado de pontos de interrogação e setas (p3); em "quanto investir" aparece o primeiro balão colorido e real entre esboços (p4); no ROI o balão colorido está no centro e os esboços ganham cifrões (p5); em "onde investir" o balão desenhado está murcho no chão, à espera de ser inflado (p6). A passagem do esboço em preto e branco para a cor é a narrativa visual do pedido: a ideia que sai do papel.

Página de contato da SOAP na p7.

## Frases-chave

- "Nunca use mais de 6 bullet-points por slide" (p2)
- "Passe uma mensagem por slide" (p2)
- "A audiência lerá seu slide, não você" (p2)
- "Use animações para conduzir seu raciocínio" (p2)
- "Use linguagem visual para ajudar o entendimento" (p2)

## Linguagem visual do deck

- Paleta: preto #000000 nos painéis e faixas, fotos em tons de cinza, verde-limão #8CC63F nos fios sob o título, e o balão colorido (vermelho, laranja, amarelo, verde, azul) como único ponto de cor.
- Tipografia: Century Gothic (ou muito parecida), títulos em caixa alta negrito, tópicos em branco com marcador quadrado.
- Modelos que se repetem: painel preto lateral com título e tópicos, imagem em preto e branco com listras diagonais claras, desenhos a lápis sobre foto, quadrado branco de logo no canto inferior direito.
- Marcante: a mistura de desenho a lápis e foto real, e a cor guardada para o momento do retorno.
- Falhas de exportação: nenhuma visível. O quadrado branco no canto inferior direito de p2-6 é o espaço vazio para o logo, não uma imagem faltando.

## Ficha do deck

```json
{"titulo":"Conquistar Recursos: balão do esboço à cor",
 "resumo":"Template 4:3 para pedir investimento com roteiro de seis slides (ideia, por que, quanto, ROI, onde) e um balão de ar quente que passa de desenho a lápis a balão colorido real ao longo do deck.",
 "ideia":"Escolha um símbolo para a sua ideia e faça-o passar de esboço em preto e branco a objeto colorido à medida que o pedido avança.",
 "como_funciona":"O texto segue a lógica do investidor (o quê, por quê, quanto, retorno, onde) e a imagem conta a mesma história em paralelo; a cor aparece só quando chega o retorno e marca o clímax.",
 "intencoes":["ABRIR","PROVAR","IMPACTAR"],
 "tecnicas":["metafora-visual","padrao-e-quebra","contraste-de-cor"],
 "movimento":["estatico"],
 "estetica":["preto-e-branco","ilustrado","corporativo"],
 "tom":["inspirador","serio"],
 "forca":4,
 "bom_para":["pedido de verba interna","pitch de projeto para diretoria","proposta de investimento"],
 "capa":5}
```

## Repetições

- As cinco regras de slide aparecem iguais em todos os slides p2-6 do próprio template.
- A sequência "por que, quanto, retorno" reaparece no roteiro de `template-aprovacao-de-projeto`, que é a versão completa com análise de viabilidade (ver o `.md` dele).

## Ids de conceito usados

- `roteiro-conquistar-recursos`: sequência de slides para pedir investimento (a ideia, por que investir, quanto investir, ROI, onde investir).
- `metafora-condutora`: um mesmo símbolo atravessa o deck e se transforma junto com a história.
- `design-de-slide`: id da Perestroika; as cinco regras de slide usadas como texto de exemplo.

## Páginas puladas ou duvidosas

- Nenhuma ilegível. p7 é a página de contato da SOAP (divulgação).
