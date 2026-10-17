# Kit: motor de apresentação em HTML

Reproduz no navegador o que faz o PPTRETA no PowerPoint: Morph entre slides, entradas no ritmo da fala, contagens, máscaras.
Arquivos: `motor.css`, `motor.js`, `modelo.html` (ponto de partida em branco), `demo.html` (todos os recursos em 9 slides).

## Estrutura mínima

```html
<link rel="stylesheet" href="motor.css">
<body data-formato="16:9">            <!-- 16:9 (padrão), 9:16, 1:1, 4:5 -->
<div class="palco">
  <section class="slide"> ... </section>
  <section class="slide" data-trans="empurrar" data-dur="1200"> ... </section>
</div>
<script src="motor.js"></script>
```

Cada slide é desenhado em pixels fixos de 1920x1080 (ou 1080x1920 no 9:16). Posicione com `position:absolute` e medidas em px.
O palco escala sozinho para qualquer tela. Para entregar um arquivo único, rode `python3 -I ferramentas/embutir.py sua.html`.

## Morph: `data-m`

Dê o mesmo `data-m` a um elemento em dois slides seguidos e mude o que quiser (posição, tamanho, cor, forma, texto):
o motor anima a passagem, como o Morph do PowerPoint. Nomes únicos dentro de cada slide.

| quero | faça |
|---|---|
| zoom mergulho | elemento pequeno no slide A, `inset:0;width:100%;height:100%` no B |
| zoom recuo | o inverso |
| voo (entrar de fora) | no slide A, o elemento fica fora da área com a classe `fora-esq`, `fora-dir`, `fora-cima` ou `fora-baixo` |
| reorganizar | mesmos `data-m` em posições novas |
| destacar um item | o item cresce e os outros encolhem para uma coluna |
| texto em movimento | uma palavra por elemento (`<span data-m="w1">`), mudando lugar, tamanho e cor |
| câmera parada, conteúdo troca | o fundo e a moldura com o mesmo `data-m`; só o conteúdo muda |

Passagem do slide inteiro, no slide de destino: `data-trans="morph"` (padrão: o que tem `data-m` se transforma e o resto dissolve), `esmaecer` (dissolve tudo, sem Morph), `corte` (seco), `empurrar`, `subir`, `zoom`, `cortina`, `circulo`.
Duração: `data-dur="1200"` (ms) no slide ou no `<body>`.

## Revelação no ritmo da fala: `data-passo`

- `data-passo="1"`, `"2"`... aparece a cada clique, antes de ir para o próximo slide. Itens com o mesmo número entram juntos, escalonados.
- `data-passo="0"` entra sozinho logo que o slide aparece.
- Jeito de entrar: `data-entra="sobe | desce | esquerda | direita | escala | desfoque | mascara | mascara-cima | circulo"` (sem nada = esmaece).
- Foco: `data-foco="grupo" data-foco-em="2"` no passo 2 este item acende e os outros do mesmo grupo apagam.

## Dados

- `<span data-conta="87" data-casas="0">0</span>` conta de 0 até 87 ao aparecer.
- Barra horizontal: `<div data-barra style="--v:.8; width:1200px; height:40px; background:..."></div>` cresce até 80%. Vertical: `data-barra-v`.

## Fontes sem depender de internet

Baixe as fontes do Google para a pasta da apresentação e use o CSS gerado:
`python3 -I ferramentas/fontes_google.py "Bricolage Grotesque" "Inter" --pasta <pasta-da-apresentacao>/fontes`
e no HTML: `<link rel="stylesheet" href="fontes/fontes.css">`. O `embutir.py --imagens` coloca as fontes dentro do arquivo único.
Fontes condensadas ou muito pesadas em tamanho grande pedem letter-spacing perto de zero (ou levemente negativo, -0,02em); confira com `ver.py`.

## Medidas

O palco tem 1920x1080 px fixos: use px. Se uma ficha ou receita falar em vw, 1vw = 19,2 px.

## Conteúdo provisório

O que o usuário precisa trocar (número sem fonte, foto de exemplo, nome do evento) recebe `class="provisorio"`
(com `data-provisorio="trocar o número"` se quiser outra etiqueta): contorno tracejado e etiqueta laranja.
Para a versão final, `<body data-final>` esconde as marcas.

## Utilitários prontos

`.sangria` (imagem tela cheia), `.recorte` (sombra para PNG recortado), `.texto-foto` (texto preenchido por foto: use com `background-image`),
`.contorno` (texto vazado), `.vidro` (vidro fosco), `.grao` (granulado por cima do slide), `.notas` (anotação do apresentador, não aparece).

## Navegação e entrega

Setas, espaço, PageUp/PageDown (passadores de slide funcionam), Home/End, F para tela cheia, clique avança, `#5` na URL abre o slide 5.
Tecla **P**: abre a janela do apresentador (anotações do slide, próximo slide, clique atual e cronômetro); as setas funcionam nas duas janelas. Ponha a janela no notebook e a apresentação no telão.
Links internos: `<a href="#7">` leva ao slide 7 com a transição normal. Serve para sumário navegável (slide-mapa com um card por capítulo) e botões de menu.
PDF: Imprimir, Salvar como PDF (um slide por página, tudo revelado). Conferir visualmente: `python3 -I ferramentas/ver.py sua.html`.

## Limites honestos

- O Morph usa View Transitions: Chrome, Edge, Safari 18+ e Firefox recentes. Em navegador antigo vira troca simples, sem quebrar.
- Na passagem, o navegador anima uma "foto" de cada elemento: texto que muda muito de tamanho pode ficar levemente borrado durante a animação (como no PowerPoint).
- Formas que mudam de contorno (círculo virando retângulo) fazem fusão entre as duas formas, não uma deformação contínua.
