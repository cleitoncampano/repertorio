# Como escrever o pedido de um vídeo de motion

Guia para transformar um pedido de vídeo num prompt que o agente consiga executar no HyperFrames sem cair no genérico.
Use quando o usuário mandar uma linha e houver marca, produto ou dado real: expanda para os blocos abaixo antes de construir.

## Na galeria

- 230 vídeos com prompt e 2 modelos do site. Mediana de 151 caracteres; 188 prompts (82%) cabem em até 300 caracteres e duas linhas. Só 17 são estruturados (blocos, listas ou 6 linhas ou mais).
- Força média 3,73 e 20 vídeos com força 5 (8,7%). Prompt curto: média 3,70, 6% com força 5 e 36% com 3 ou menos. Estruturado: média 4,18, 29% com força 5 e 12% com 3.
- Os 12 vídeos que usam os blocos do site (direction, structure, build, start) têm 4 de força 5 e 8 de força 4: média 4,33, nenhum abaixo de 4. Todos trazem lista de proibidos e conferência de quadros.
- Tamanho sozinho não explica: de 200 a 400 caracteres, só 3% chegam a 5; acima de 1500, 38%. O salto vem dos blocos, não das palavras a mais.
- Rodadas declaradas em 97 vídeos: 90 numa tentativa só (média 3,76), 6 com poucas rodadas (3,67), 1 com muitas (3). Ferramenta citada em 58 (média 3,88, contra 3,68 sem citar).

## Uma linha ou estruturado

- Uma linha funciona quando a tarefa é autocontida: mostrar talento sem marca, sem fatos e sem interface real. O pedido de showreel "para o currículo" gerou 61 vídeos, média 3,85 e 7 de força 5. Funciona também quando o assunto já traz a estrutura: "mostre o que acontece dentro de um data center de IA" virou um tour do prédio ao chip ([Tour 3D explicativo por dentro de um data center, do prédio ao chip](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-sayan-shanky-f850d8)).
- Uma linha falha quando há produto: 84 lançamentos com prompt curto e nenhum de força 5 (37 ficaram em 3). Os 16 lançamentos com prompt estruturado têm 5 de força 5. Sem direção, o agente inventa telas, números e estética.
- Ênfase não substitui direção: os 85 prompts com "go all out" têm média 3,76, a mesma da galeria.
- Estrutura sem direção vira modelo pronto: "cinco cenas, dor, oferta, passos, prova, nome, transições suaves, minhas cores" deu força 2 ([Explicador de negócio em cinco cenas: dor, oferta, passos, prova, nome](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-alex-prompter-1ea044)).
- Prompt longo também erra quando não decide o essencial: 8 mil caracteres imitando a marca de outra empresa, com interface pequena dentro de um palco, deram força 3 ([Filme de app de música com player fixo ligando todas as cenas](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-brainextends-e19ac3)).

## Ferramenta e rodadas

- Por família: HTML ou WebGL capturado pelo Playwright, 4,43 (7 vídeos, 3 de força 5); HyperFrames, 4,1 (10, nove de força 4); HTML e JavaScript puros, 3,94 (17); 3D na web, 3,67 (6); Remotion, 3,54 (13, sete em força 3).
- A ferramenta não decide. Os de cima têm em comum cada quadro calculado pelo tempo, captura determinística e quadros conferidos antes do render; os 14 prompts que pedem tudo "em função do tempo" têm média 4,21. Os Remotion fracos são explicadores genéricos de software, não falhas da ferramenta.
- Rodadas não consertam pedido fraco. Os 10 vídeos de força 5 que declaram rodadas foram feitos numa tentativa só; o único com muitas rodadas ficou em força 3. Ponha a revisão dentro do prompt em vez de corrigir depois.

## Os dois modelos do site

[Modelo de prompt para showreel de 15 s em transformação contínua](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-template-showreel):
- Direção: 15 s; o agente escolhe o conceito e o nomeia em uma linha antes de começar; cada plano nasce do anterior, sem corte nem fusão; uma fonte, até três cores mais preto e branco, uma linguagem de câmera; cinco momentos com tempo igual (tipografia cinética, morph, passagem de 2D para 3D, dado ou interface, título final); lista de proibidos.
- Estrutura: 120 BPM, algo em toda batida; gancho no primeiro compasso, uma técnica por compasso, o auge no último compasso cheio, título no meio compasso final e último quadro igual ao primeiro.
- Construção: um HTML 1920x1080 calculado pelo tempo; molas e easing exponencial como funções; desfoque que segue a velocidade; trilha feita em código; render a 60 fps com subquadros para motion blur; um quadro por batida conferido antes do render completo.
- Começo: apresentar o conceito e um storyboard por batida, construir sem perguntar e entregar o MP4.

[Modelo de prompt para peça 3D em tempo real com plano-assinatura](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-template-realtime):
- Direção: o assunto vira um espaço 3D; um plano-assinatura para o qual tudo converge; câmera de cinema com um movimento nomeado por plano (dolly, grua, órbita, aproximação, troca de foco); luz de três pontos, neblina, materiais físicos; objetos que reagem uns aos outros; lista de proibidos.
- Estrutura: seis planos de cerca de 3 s, descritos um a um, até o logotipo. Construção: three.js sem build, 60 fps num notebook, modo de render com aleatoriedade semeada, um quadro por plano conferido.
- Bloco extra de armadilhas (sombra listrada, cintilação ao longe, render diferente da prévia) e começo com o plano-assinatura e a lista de planos em poucas linhas.

O que os dois ensinam: decidir o conceito antes do código, limitar fonte, cor e câmera, proibir o clichê pelo nome, amarrar cada cena a um tempo e conferir quadros. O próprio site avisa que, sem revisar os quadros por batida, o resultado volta ao clichê. Os prompts de usuários que chegaram a força 5 somam dois blocos (entradas e armadilhas) e trocam "construa sem perguntar" por "peça as entradas e mostre o mapa de batidas ou alguns quadros antes do filme".

## Estrutura recomendada

- `<entradas>`, quando houver marca ou produto: o que pedir (nome, logo, frase-promessa, 3 a 6 telas ou fotos reais, cor de destaque, música com licença) e o padrão se o usuário pular algo.
- `<direção>`: duração, formato em px e fps, o conceito em uma frase, o elemento-fio que atravessa as cenas, uma fonte, até três cores com função, uma linguagem de câmera, como as cenas passam de uma para outra e a lista de proibidos.
- `<estrutura>`: BPM e número de compassos ou planos; cena a cena com tempo ou batida, dizendo o que entra, o que sai e de onde nasce a próxima; gancho no primeiro compasso, auge no último cheio, fecho com título, logo ou loop.
- `<construção>`: HTML calculado pelo tempo, sem timers nem estado entre quadros, aleatoriedade com semente; molas como funções; cada som posicionado pelo pico; textos e números só do material real; a conferência de quadros.
- `<armadilhas>`, opcional: defeitos conhecidos do efeito escolhido (texto que troca dentro de forma que se transforma pede entrada e saída próprias; cor que inunda a tela precisa passar dos cantos em cerca de 0,3 s).
- `<começo>`: o que o agente mostra antes de construir (conceito em uma linha, mapa de batidas, quatro quadros-chave) e se espera aprovação ou segue sozinho. Com marca real, espere; em peça livre, siga e confira sozinho.

## O que proibir explicitamente

Nos 14 prompts com linha de proibidos, os mais citados: brilho (11), cara de modelo pronto (8), explosão de partículas (8), pausa longa ou tempo morto (7), fusão (6), easing com quique (5), degradê genérico (4), material de banco (4).

1. Brilhos, lens flare, separação RGB e tremor de câmera: a assinatura do motion genérico.
2. Explosões de partículas e confete como enfeite; só valem se forem o próprio dado.
3. Fusões, blur-in e cortes sem motivo: a cena seguinte nasce de um objeto da anterior.
4. Easing com quique e movimento linear: molas com no máximo um leve excesso.
5. Pausas acima de 0,5 a 1 s e quadros congelados, salvo uma pausa escolhida.
6. Degradês genéricos, vidro em tudo, cartões 3D girando sem motivo, zoom constante.
7. Banco de imagens e kits de interface quando existe material real.
8. Números, resultados, clientes, funções e slogans inventados ou parafraseados.
9. Logotipo redesenhado ou dentro de caixa, e a marca de outra empresa.
10. Jargão de animador, timecode e moldura de editor na tela, salvo quando são o conceito.
11. Aleatório sem semente e animação CSS solta: o render deixa de bater com a prévia.
12. "Qualquer coisa com cara de modelo pronto": os melhores escrevem isso com todas as letras.

## Como pedir a conferência de quadros

1. Antes do código: "Mostre o conceito em uma linha, o mapa de batidas com cada tempo e 4 quadros-chave (gancho, produto, auge, fecho). Espere minha aprovação." Na galeria, o pedido de mapa e 4 quadros aparece em [Lançamento de app de fotos em plano único, da tela à moldura na parede](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-twoclipping-221cab); o de quadros em tempos exatos (0; 1,6; 2,5; 5; 6,5; 9,3 e 11 s) em [Voo de câmera 3D sobre uma landing page deitada no chão do estúdio](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-twoclipping-d89be5).
2. Antes do render completo: "Gere um quadro por batida (ou um por cena) e olhe todos. Corrija o que estiver poluído, fora da batida, sobreposto, fora da área segura ou ilegível com o quadro reduzido a 390 px de largura."
3. Depois do rascunho: procurar saltos de um quadro (diferença três vezes maior que a dos vizinhos), conferir a emenda do loop e as passagens rápidas quadro a quadro. Os mais exigentes pedem uma folha de contato com todos os quadros ([Lançamento de modelo de imagem com legendas digitadas e vidro líquido](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-rossaxbt-3085b7)) e um crítico novo, que não construiu a peça, para rever o render ([Promo de galeria feito só com o site real e uma câmera contínua](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-antonio-kodheli-490109)).
4. No HyperFrames: `npx hyperframes check --json` para layout e contraste, `npx hyperframes snapshot --at 0,0.5,1,...` com um tempo por batida, leitura dos PNGs, render `--quality draft` para conferir e `--quality delivery` no fim.

## O que os melhores fazem

- Pedem as entradas reais e dão um padrão para o que o usuário não mandar ([Filme de produto em plano contínuo, do pedido digitado à entrega](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-ultimaxbt-2ddf1e)).
- Nomeiam um elemento-fio e proíbem que ele salte sem caminho ([Sistema de movimento em que um ponto laranja liga todas as cenas](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-ultimaxbt-bbebf5), [Loop de interface escura em que uma bola branca aciona cada componente](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-rossaxbt-94583b)).
- Escrevem a estrutura em batidas, com o estado de cada compasso, e pedem o último quadro igual ao primeiro ([Uma única forma que vira botão, player, slider, gráfico e busca](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-twoclipping-5cba86)).
- Proíbem o que o produto não tem: botão inexistente, número inventado, slogan parafraseado ([Promo de galeria feito só com o site real e uma câmera contínua](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-antonio-kodheli-490109)).
- Dão tempos e medidas exatos quando o movimento é o produto ([Voo de câmera 3D sobre uma landing page deitada no chão do estúdio](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-twoclipping-d89be5)).
- Escrevem regras de texto: nomear o que o produto aprende, nunca a abstração, e nenhum resultado inventado ([Filme de produto em papel com bola que conecta ideias e notas à mão](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-ik-builds-b8bdcf)).
- Quando usam uma linha só, o conceito está dentro dela: "cada explicação de recursão num estilo radicalmente diferente" ([Explicação de recursão em que cada nível muda de gênero visual](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-emollick-8661a8)).

## Erros que derrubam

- Tema amplo sem recorte, duração nem estilo: a história política de um país desde a independência virou 3 min e meio de silhuetas genéricas ([Linha do tempo política com cartões de retrato e cor por partido](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-triglyceee-bd5b08)).
- Pedir algo que não é motion: um jogo de cartas virou gravação de partida, sem roteiro nem cortes ([Partida de jogo de cartas em pixel art gravada como demonstração](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-aisongman-71ffac)).
- Data comemorativa sem dados conferidos: confete de modelo pronto e o ano errado na tela ([Aniversário de 20 anos de marca de receitas com selo e confete](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-deebeeeff-50fcd0)).
- Duração deixada alta: 90 a 100 s de telas calmas perdem o público antes do fim ([Showreel de portfólio com o site real em janelas e chat que responde](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-wani-shola-16ca7a)).
- Lista de proibidos sem conferência: a própria ficha do modelo avisa que a regra de toda cena nascer da anterior só se cumpre revendo quadro por batida ([Modelo de prompt para showreel de 15 s em transformação contínua](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-template-showreel)).

## Prompt base

Adapte os colchetes. Exemplo para Reels; troque formato, tamanhos e área segura conforme `formatos.md`.

```
<entradas>
Peça: nome e logo, uma frase-promessa, 3 a 6 telas ou fotos reais, a cor de destaque e uma música com licença comercial perto de 120 BPM. Se eu pular algo, use [padrões].
</entradas>
<direção>
Vídeo de [15] s, 1080x1920 a 60 fps, para [Reels e TikTok]. Conceito: [uma frase]; diga o conceito em uma linha antes de começar.
Elemento-fio: [um ponto, uma forma, um cartão] atravessa todas as cenas; cada cena nasce dele, sem corte nem fusão.
Uma fonte ([da marca]), até três cores com função (fundo, texto, destaque), uma linguagem de câmera.
Título de 100 a 180 px, nenhum texto abaixo de 44 px, uma frase por tela, título e ação entre y 300 e y 1500. Tudo entendido sem som.
Use só textos, números e telas do material que eu der.
Proibido: brilhos, lens flare, separação RGB, tremor de câmera, explosões de partículas, fusões, blur-in, easing com quique, degradês genéricos, pausas acima de 0,5 s, números ou funções inventados, logo redesenhado, qualquer coisa com cara de modelo pronto.
</direção>
<estrutura>
120 BPM, [8] compassos de 2 s, algo acontece em toda batida.
Compasso 1: gancho de até 5 palavras, legível já no quadro 0.
Compassos 2 a 6: uma ideia por compasso, cada uma nascendo da anterior: [problema], [produto real em ação], [prova], [virada].
Compasso 7: o momento mais forte. Compasso 8: logo e frase final; último quadro igual ao primeiro.
</estrutura>
<construção>
1. HyperFrames em HTML no tamanho acima. Todo estado calculado pelo tempo: sem timers, sem animação CSS solta, sem estado entre quadros, aleatoriedade com semente.
2. Molas e easing exponencial como funções do tempo; desfoque acompanha a velocidade nos movimentos rápidos.
3. Cada efeito sonoro posicionado pelo pico na batida; mixagem em -14 LUFS.
4. Antes do render completo: rode check, gere um quadro por batida e olhe todos. Corrija o que estiver poluído, fora da batida, sobreposto, fora da área segura ou ilegível a 390 px de largura. Procure saltos de um quadro e confira a emenda do loop.
</construção>
<começo>
Peça as entradas, mostre o conceito, o mapa de batidas e 4 quadros-chave (gancho, produto, auge, fecho) e espere minha aprovação. Depois construa sem novas perguntas e entregue o MP4.
</começo>
```

Para peça livre, sem marca: tire `<entradas>` e troque o começo por "apresente o conceito e o storyboard por batida e construa sem me perguntar nada", como no modelo de showreel.

## Abra primeiro

- [Modelo de prompt para showreel de 15 s em transformação contínua](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-template-showreel): os quatro blocos na forma mais curta.
- [Modelo de prompt para peça 3D em tempo real com plano-assinatura](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-template-realtime): plano-assinatura, câmera nomeada e bloco de armadilhas.
- [Uma única forma que vira botão, player, slider, gráfico e busca](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-twoclipping-5cba86): estrutura em batidas; compare com [Uma forma só que vira botão, player, toggle, gráfico e aviso](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-demonugc-4c5753), mesmo prompt e força 4, para ver que o pedido não dispensa a conferência.
- [Lançamento de app de fotos em plano único, da tela à moldura na parede](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-twoclipping-221cab): entradas, mapa de batidas e 4 quadros antes do filme.
- [Promo de galeria feito só com o site real e uma câmera contínua](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-antonio-kodheli-490109): proibir o que não existe e revisar com um crítico novo.
- [Filme de produto em papel com bola que conecta ideias e notas à mão](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-ik-builds-b8bdcf): regras de texto e campos para preencher com o material da marca.
- [Explicação de recursão em que cada nível muda de gênero visual](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-emollick-8661a8): uma linha que funciona porque carrega o conceito.
- [Explicador de negócio em cinco cenas: dor, oferta, passos, prova, nome](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-alex-prompter-1ea044): o contraexemplo da estrutura sem direção.
