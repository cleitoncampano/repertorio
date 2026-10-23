# Kit de motion: movimentos prontos no HyperFrames

Para criar vídeos de motion (HTML renderizado em MP4 pelo HyperFrames) a partir das referências do espaço Motion.
Em vez de escrever cada efeito do zero, comece pelos blocos do registro do HyperFrames que fazem os movimentos mais frequentes da galeria.
Cada bloco vira código editável no projeto: mude cores, textos, tempos e o que for preciso.

## Como usar

1. Leia o guia do tipo de vídeo em `biblioteca/motion/guias/` (estrutura, duração, ritmo, prompt base) e abra as referências que ele indica no espaço Motion.
2. No projeto de destino, copie `kit/motion/inicio/` para a pasta da produção. É um vídeo de 13,2 s já montado e testado: título que sobe palavra por palavra, cartões em cascata, número que conta e a marca no fim.
3. Troque a identidade nas variáveis de `:root` em `index.html` (`--bg`, `--fg`, `--brand`, `--accent`, `--font-display`) e os textos no `data-variable-values` de cada bloco.
4. Para trocar ou acrescentar um movimento, escolha na tabela abaixo e instale com `npx hyperframes add <nome>`. Componentes vão para `compositions/components/`; blocos, para `compositions/`. Os quatro do projeto inicial são montados como cena (`data-composition-src`), com o mesmo id no host e no bloco.
5. Antes de entregar: `npx hyperframes check --json` (zero erros), `npx hyperframes snapshot --at <tempos>` para olhar os quadros e `npx hyperframes render -o renders/video.mp4`.
6. Se o usuário pedir para guardar o vídeo no acervo, use `register_reference` com o MP4, `data.genres` (tipo de vídeo) e `data.prompt`: ele entra com player, loop e prancha de quadros, como os da galeria.

Cuidados aprendidos no teste do projeto inicial:

- O primeiro quadro vira a miniatura nas redes. O projeto inicial começa vazio e o `check` avisa (`first_frame_empty`); para Reels e feed, comece com o título ou a imagem principal já na tela.
- Os blocos usam as variáveis de cor `--brand`, `--accent` e `--accent-2`: a opção `accent` de cada bloco escolhe qual delas (green usa `--brand`, blue usa `--accent`, violet usa `--accent-2`).
- Use `fromTo`, nunca `from`, e não anime `display` nem `visibility` de um `.clip` (regras do HyperFrames).

## Movimentos e blocos

Ordem pela frequência na galeria. Prévias em vídeo abrem no navegador. A versão legível por agentes está em `movimentos.json`.

### Texto em movimento (tipografia cinética)

O movimento mais comum da galeria (156 vídeos).

| bloco | quando usar |
|---|---|
| `per-word-rise` | padrão de chegada: palavras sobem do desfoque, uma a uma, e param |
| `kinetic-type-swap` | uma palavra da frase gira entre opções, como caça-níquel |
| `headline-slam` | título pesado que cai e trava com impacto |
| `text-match-cut` | uma frase vira outra no meio do movimento |
| `focus-blur-resolve` | frase que entra do desfoque para nítida, calma |

### Troca de cena com motivo

114 vídeos. Use de 3 a 5 tipos por filme, cada um causado por algo na tela.

| bloco | quando usar |
|---|---|
| `whip-pan-cut` | chicote lateral com desfoque de movimento |
| `match-cut` | um círculo acelera e casa com o da cena seguinte |
| `iris-reveal` | círculo que abre do ponto clicado para a próxima cena |
| `cut-the-curve` | corte seco no pico de velocidade, mesma direção dos dois lados |
| `fade-through` | passagem calma por uma cor, para momentos de pausa |

### Entrada em cascata

109 vídeos. Itens de lista entram de 40 a 80 ms um do outro.

| bloco | quando usar |
|---|---|
| `grid-card-assemble` | cartões de recurso montam uma grade ou lista |
| `notification-stack` | notificações empilham, a mais nova em cima |
| `logo-wall` | parede de logos de clientes (prova social) |
| `per-word-rise` | também serve para frases em cascata |

### Transformação (uma forma vira outra)

89 vídeos. É o que separa os de força 5: um objeto que muda de forma de cena em cena.

| bloco | quando usar |
|---|---|
| `morph-swap` | A se condensa e vira B no mesmo centro |
| `card-resize` | cartão pequeno se abre em painel de detalhe |
| `icon-morph-beat` | ícone muda de estado e marca a conclusão |
| `modal-morph` | cartão se expande em tela cheia, elemento compartilhado |
| `facet-morph` | massa de triângulos que vira outra silhueta |

### Número que conta e gráfico que cresce

69 vídeos.

| bloco | quando usar |
|---|---|
| `count-up` | número que acelera, desacelera e trava no valor exato |
| `number-wheel` | dígitos que rolam, como placar |
| `chart-story` | gráfico que se constrói na ordem de leitura e mostra os valores |
| `conic-progress-ring` | anel de progresso com o número no centro |
| [`data-chart`](https://static.heygen.ai/hyperframes-oss/docs/images/catalog/blocks/data-chart.mp4) | bloco de barras e linha com legendas (cena inteira) |

### Câmera que entra (zoom mergulho)

47 vídeos. A câmera vai até um elemento e ele vira a próxima cena.

| bloco | quando usar |
|---|---|
| `zoom-through-transition` | atravessa um cartão até a cena seguinte |
| `parallax-zoom` | cartão central cresce até a tela, vizinhos se afastam |
| `parallax-device-dive` | celular sobe e a câmera mergulha na tela do app |
| `ui-focus-zoom` | a câmera aproxima e passeia pela região da interface |
| `cursor-zoom-follow` | gravação de tela que aproxima a cada clique |

### Câmera que recua (revela o todo)

30 vídeos. Bom para fechar mostrando o conjunto.

| bloco | quando usar |
|---|---|
| `pull-back-reveal` | de um detalhe para o título e os cartões em volta |
| `parallax-unzoom` | cartão em tela cheia encolhe e forma uma grade |

### Câmera que passeia

43 vídeos.

| bloco | quando usar |
|---|---|
| `pan-stations` | travelling lateral por estações de recurso, com parada em cada uma |
| `scroll-camera-story` | rolagem cinematográfica por seções |
| `swipe-rail` | trilho de cartões arrastado com impulso |

### Giro e órbita

65 vídeos.

| bloco | quando usar |
|---|---|
| `locked-nucleus-orbit` | satélites orbitam um centro e formam a marca |
| `split-tilt-cards` | dois cartões abrem como livro, em perspectiva |
| `extruded-logo` | letras 3D viram uma a uma (cena inteira, three.js) |

### Revelação por máscara ou traço

39 vídeos.

| bloco | quando usar |
|---|---|
| `svg-mask-reveal` | imagem aparece só dentro das letras da marca |
| `svg-stroke-trace` | desenho de linha que se traça e preenche |
| `whiteboard-ink` | esboço de quadro branco com a caneta seguindo o traço |
| `colorama-wipe` | título revelado por uma frente colorida e desfocada |

### Voo de elementos

32 vídeos.

| bloco | quando usar |
|---|---|
| `offset-path-traveler` | elemento que percorre um caminho e gira na curva |
| `physical-exit` | saída com impulso: arremesso, queda ou deslize |

### Foco e destaque

17 vídeos.

| bloco | quando usar |
|---|---|
| `focus-rack` | foco passa de um cartão para outro |
| `vox-annotate` | palavra recebe marca-texto à mão, com seta |
| `marker-highlight` | traço de marcador sublinha ou circula |
| `tracing-beam` | luz percorre um caminho e acende cada elemento |

### Interface de produto viva

Lançamentos com tela real (103 vídeos com interface).

| bloco | quando usar |
|---|---|
| `typed-prompt` | pedido sendo digitado com cursor piscando |
| `oversized-cursor` | cursor grande que aponta e clica |
| `press-ripple` | cursor chega, aperta o botão e dispara a ação |
| `agent-cursor` | agente de IA operando a interface passo a passo |
| `code-terminal-run` | terminal rodando um comando |
| `native-notification-pop` | notificação do sistema que cai na tela |

### Marca, vinheta e fechamento

Abertura e assinatura.

| bloco | quando usar |
|---|---|
| `logo-sting` | a marca entra com impacto e fica parada |
| `logo-brand-close` | nome entra letra a letra e trava no centro |
| `cta-close` | frase de chamada com botão no fim |
| `titlecard-lockup` | cartão de título calmo para respiro |

### Ritmo e batida

Corte na batida, mude o layout no compasso.

| bloco | quando usar |
|---|---|
| `beat-accent` | um impacto na batida: clarão e pulso no elemento |
| `beat-freeze-cut` | rampa de velocidade, congelamento e corte (cena inteira) |

## Projeto inicial

`inicio/` foi conferido com `npx hyperframes check` (sem erros; contraste aprovado em 16 de 16 pontos) e renderizado em 1920x1080 a 30 fps em 14 s.
Os blocos são cópias da versão 0.8.186 do registro; para atualizá-los, rode `npx hyperframes add <nome>` dentro da pasta.
