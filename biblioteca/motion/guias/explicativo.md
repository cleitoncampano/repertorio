# Explicativo

Vídeo que ensina como algo funciona: um conceito, um processo, uma receita, um sistema ou um produto por dentro.
Escolha quando o público precisa sair entendendo o mecanismo, não só lembrando de uma marca.

## Na galeria
- 34 vídeos, 22 de força 4 ou 5. 11 também são explicador de produto (lançamento), e só 4 desses estão entre os fortes.
- Duração mediana de 54 s, de 15 a 457 s: 7 até 20 s, 9 de 24 a 40 s, 11 de 53 a 98 s e 7 de 2,8 a 7,6 min. Fortes: mediana de 30 s. Fracos: 57 s.
- 32 horizontais e 2 quadrados (uma receita e um token bucket). Nenhum vertical.
- Som em 26 de 34 (17 dos 22 fortes). As aulas acima de 2 min usam narração com legenda fixa embaixo.
- Ferramentas citadas: HTML (5) e uma vez cada HyperFrames com GSAP, Remotion, Canvas, JavaScript e Manim com edge-tts. Nas fichas de construção, SVG com stroke-dashoffset aparece em 15, GSAP em 13, three.js nos 4 em 3D.

## Estrutura que funciona
Os fortes não empilham "Passo 1, 2, 3" em cards. Escolhem uma de três formas de dividir o conceito e penduram os passos nela:
- **Objeto fixo que muda a cada passo.** O copo fica no centro e cada ingrediente acontece nele. Um card diz a ação e a quantidade, a trilha de etapas no rodapé ganha visto.
- **Viagem de escala em capítulos.** Do todo até a menor peça e de volta, um capítulo por parada, "1 de 11" no canto.
- **Roteiro de detetive.** A falha, a solução óbvia que também falha, a ideia certa, os passos numerados, o caso extremo em forma de pergunta e a comparação honesta das opções.

**15 s** (uma ideia nova a cada 1,5 a 2 s):
- 0 a 2 s: o objeto ou o problema entra em cena (a bola cai e quica, o evento chega, a pergunta aparece).
- 2 a 5 s: o mecanismo, nomeado por nota à mão e seta sobre o que se vê.
- 5 a 9 s: virada com troca dura de claro para escuro e a frase principal em tipografia gigante.
- 9 a 12 s: a prova visual: o gráfico ou a demonstração funcionando.
- 12 a 15 s: volta ao objeto do começo e fecha com o nome.

**30 a 45 s** (um passo a cada 4 a 5 s):
- 0 a 3 s: o problema mostrado, não dito (um terminal que responde demais, uma máquina marcada "DOWN").
- 3 a 6 s: o objeto fixo e o mapa (trilha de etapas, contador "01/07" no topo).
- 6 a 25 s: os passos, todos sobre o mesmo objeto. O card troca a ação, o número cresce junto do nível, o passo anterior ganha visto.
- 25 a 30 s: o resultado inteiro e a síntese (a proporção 1:1:1, a comparação lado a lado).
- Até 45 s: acrescente o caso extremo em forma de pergunta antes da síntese.

**Longo, 1,5 a 5 min** (capítulos de 8 a 15 s; o data center faz 11 capítulos em 98 s):
- 0 a 10 s: o todo visto de longe, com "capítulo 1 de N" e um parágrafo curto no canto.
- Cada capítulo: sobretítulo numerado, título curto, uma frase e uma peça demonstrada com etiquetas.
- Desça de escala e suba de volta. O retorno amarra os capítulos.
- Fim: o todo recolhido numa tela (o fio vira linha do tempo, o quadro-resumo em cinco linhas numeradas escritas uma a uma).
- Acima de 2 min, narração é obrigatória. Sem ela, capítulos parecidos cansam no meio.

## Ritmo, câmera e transições
- O tempo de leitura manda no corte. Com 3 s por ideia, a plateia só lê o título. Com menos de 2 s por cena e sem narração, quem não conhece o tema perde a ligação entre etapas.
- Em 15 s cabe uma nota por cena, curta e grande. Várias notas pequenas viram ruído.
- Ligue as cenas por algo que persiste: a bola com rastro que atravessa tudo, o fio vermelho, o copo parado, as peças que mudam de lugar entre cenas como num Morph.
- Mergulho para dentro de uma tela ou peça desce um nível; o recuo sobe. Aparece em 7 fortes e em 1 fraco.
- 3D só com câmera de cinema em trilhos entre poses salvas por capítulo, nunca órbita livre. Uma única cena 3D serve a todos os capítulos.
- Receita, simulação e mecanismo pedem tela única, sem cortes: a mudança acontece no objeto.
- Som: um efeito curto em cada passo (pop, rabisco de caneta, whoosh) e a bateria entrando na virada para o escuro. Nos longos, o traço acompanha a narração.

## Visual
- Claro domina: 13 dos 22 fortes. Papel creme, quadro branco, fundo pontilhado, maquete 3D branca sem textura. O escuro entra para o "antes", o excesso ou a virada.
- Três vozes de texto: condensada pesada nos títulos (Anton nos exemplos), manuscrita só nas notas e desenhada por traço, mono em números, medidas e parâmetros. Aulas editoriais trocam a condensada por serifa.
- Cor com função fixa: uma por fluxo (energia amarela, dados azul, calor vermelho), uma cor de caneta por papel (azul estrutura, vermelho problema, verde resposta), uma cor e uma letra por personagem do sistema.
- Legenda de cores fixa num canto, sempre visível.
- Diagrama que se constrói: setas e linhas desenhadas na hora, caixas ligadas mostrando quem faz o quê, etiquetas finas com linha de chamada, vista explodida para camadas.
- Mapa de onde estamos sempre na tela: trilha de etapas, pilha no topo, régua de tempo, "N de M".
- Nota à mão aparece em 8 fortes e 1 fraco; 3D em 6 fortes e nenhum fraco. Interface real só em tamanho grande.

## O que os melhores fazem
1. Fazem a forma do vídeo imitar o conceito: recursão vira cenas aninhadas, cada nível num gênero visual, com uma pilha fixa no topo mostrando a profundidade. [Explicação de recursão em que cada nível muda de gênero visual](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-emollick-8661a8)
2. Fixam o objeto e deixam cada passo acontecer nele, com card de ação e quantidade e trilha de etapas que ganha visto. [Receita ilustrada passo a passo com copo que enche e etapas marcadas](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-ror-fly-9950f1)
3. Constroem o conceito traço a traço no quadro branco, no ritmo da narração, e terminam com o quadro-resumo em lista numerada. [Aula de física em quadro branco com caneta que desenha e narração](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-tak3sh8-be5012)
4. Anotam a própria demonstração à mão, como professor no quadro: a seta e a nota dizem o porquê do que se vê. [Showreel anotado à mão que explica cada princípio de animação](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-himanshutwtxs-5f4b43)
5. Montam o diagrama como história de detetive, com cada máquina sempre na mesma cor e letra e linhas que ligam quem faz o quê. [Explicador neobrutalista de sistema técnico em passos e caso extremo](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-0xnfrith-5be616)
6. Seguem um fio só pela história inteira, do prédio ao chip e de volta, com cor fixa por fluxo e etiquetas em cada peça. [Tour 3D explicativo por dentro de um data center, do prédio ao chip](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-sayan-shanky-f850d8)
7. Mostram o mecanismo funcionando em vez de ilustrar o marco: o terminal reproduz a conversa, arcos ligam uma palavra às outras, duas barras comparam o erro. [Linha do tempo da IA em capítulos com ano fantasma e mecanismo animado](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-kloss-xyz-fe0c31)
8. Usam uma analogia desenhável que volta em todo passo: um gesto repetido que fica mais forte até a quebra cômica, ou o escuro que vira claro quando a coisa fica entendida. [História da IA em pixel art contada por um bumerangue](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-pluginplay-3d4006) e [Explicador que vai do muro de páginas escuras ao diagrama claro](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-sudo-kiran-b055de)

## Erros que derrubam
- O molde "logo, Passo 1, 2, 3 em cards iguais, bento de recursos, botão". 7 dos 12 fracos são explicadores de produto nessa linha: corretos e esquecíveis. [Explicador de produto em três passos com barra de etapas colorida](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-ajith-io-c52e09)
- Passos com telas parecidas e nada que leve de um ao outro: o miolo fica monótono. [Explicação de fundo gerido por agentes em quatro passos numerados](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-imthatcarlos-e04bfe)
- Corte mais rápido que a leitura, sem narração: cenas de menos de 2 s deixam o leigo sem a ligação entre etapas. [Reel de cobrança por uso: de um evento à fatura final](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-sudeepsd-1a3485)
- Aula longa e uniforme: as de 7 a 8 min ficaram em força 3. Para redes, extraia um passo de 1 a 2 min. [Aula animada de derivada com gráficos que se constroem passo a passo](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-linearuncle-5d2bae)
- Cor ou estilo que muda sem razão: o público perde quem é quem, e troca de gênero que não é o argumento vira colagem confusa.
- Exemplo genérico, número inventado ou fato errado. O diagrama de exemplo precisa ser bom de verdade, peças genéricas ou números inventados tiram a autoridade do 3D, e piada visual não salva data errada. Use só números e datas da fonte do usuário.

## Prompt base
```
<direção>
Vídeo explicativo de {15 | 30 | 90} s sobre {CONCEITO}, para {PÚBLICO} que não conhece o tema. Formato {1920x1080 | 1080x1080}.
Antes de tudo, escolha UMA forma de dividir o conceito e nomeie em uma linha: objeto fixo que muda a cada passo, viagem de escala em capítulos, ou roteiro de detetive (falha, solução óbvia que falha, ideia, passos, caso extremo, comparação).
Escolha UMA analogia concreta e desenhável e mantenha do começo ao fim. Se o conceito tem forma (aninhado, em ciclo, em fluxo), dê essa forma ao vídeo.
Fundo claro (papel creme, quadro branco ou maquete branca). Cores com papel fixo: {COR_ESTRUTURA}, {COR_PROBLEMA}, {COR_RESPOSTA}. Cada elemento mantém cor e letra até o fim.
Títulos em {FONTE_TITULO} condensada pesada, notas em manuscrita desenhada por traço, números e medidas em mono.
Mapa sempre visível: trilha de etapas, "capítulo N de M" ou régua no rodapé.
Proibido: cards de passos iguais que entram e somem; bento de recursos; mais de uma nota por cena em 15 s; jargão sem tradução na tela; números, percentuais, datas ou nomes de clientes que não estejam em {FONTES}; capturas de tela pequenas; trocar de estilo sem razão.
</direção>

<estrutura>
15 s: 0 a 2 s objeto ou problema; 2 a 5 s mecanismo nomeado com nota à mão; 5 a 9 s virada para o escuro com a frase principal; 9 a 12 s prova visual; 12 a 15 s volta ao objeto e nome.
30 s: 0 a 3 s problema mostrado; 3 a 6 s objeto fixo e mapa; 6 a 25 s um passo a cada 4 a 5 s sobre o mesmo objeto; 25 a 30 s resultado inteiro e síntese.
90 s ou mais: capítulos de 8 a 15 s com sobretítulo numerado, título curto, uma frase e uma peça com etiquetas; desça de escala e volte; feche com o todo numa tela; narração com legenda fixa.
</estrutura>

<construção>
1. HyperFrames: um HTML no tamanho final, timeline GSAP controlada pelo tempo, todo estado inicial definido em t=0, sem timers, animação CSS solta ou aleatório sem semente.
2. Uma lista única de passos (ou uma simulação) no topo do arquivo alimenta objeto, card, trilha e legenda. Nível, barra e número de cada passo usam a mesma curva de tempo.
3. Traços, setas e notas em SVG revelados por stroke-dashoffset. 3D só se a explicação for espacial, com câmera entre poses por capítulo.
4. Efeito sonoro curto em cada passo, mudança de música na virada; nos longos, traço sincronizado à narração.
</construção>

<começo>
Escreva primeiro: a forma escolhida, a analogia, a lista de passos com o tempo de cada um e a origem de cada número da tela. Depois construa sem perguntar.
Antes do render completo, gere um quadro parado no meio de cada passo e confira: o texto se lê no tempo da cena, a trilha marca o passo certo, nenhuma cor trocou de dono, nada corta ou se sobrepõe. Corrija e só então renderize o MP4.
</começo>
```

## Abra primeiro
- [Receita ilustrada passo a passo com copo que enche e etapas marcadas](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-ror-fly-9950f1): o passo a passo mais limpo da galeria, com objeto fixo, card e trilha de etapas.
- [Explicador neobrutalista de sistema técnico em passos e caso extremo](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-0xnfrith-5be616): roteiro de detetive e cor fixa por elemento num diagrama técnico.
- [Aula de física em quadro branco com caneta que desenha e narração](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-tak3sh8-be5012): quadro branco com cor de caneta por papel e quadro-resumo final.
- [Filme de produto em papel com bola que conecta ideias e notas à mão](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-ik-builds-b8bdcf): 15 s com fio condutor, notas à mão, virada claro e escuro e um prompt que proíbe resultado inventado.
- [Tour 3D explicativo por dentro de um data center, do prédio ao chip](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-sayan-shanky-f850d8): viagem de escala em 11 capítulos, cor por fluxo e legenda fixa.
- [Explicação de recursão em que cada nível muda de gênero visual](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-emollick-8661a8): a estrutura do vídeo como argumento, com mapa fixo da profundidade.
- [Linha do tempo da IA em capítulos com ano fantasma e mecanismo animado](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-kloss-xyz-fe0c31): mostrar o mecanismo em vez do marco, com três âncoras fixas por capítulo.
- [Explicador de token bucket com balde, número e gráfico sincronizados](http://127.0.0.1:8766/?workspace=81287ed7-121b-4249-88f2-bff35d60e1cb&ref=motion-parkerrex-1a54fe): três vistas do mesmo estado numa tela só, sem corte, saídas de uma simulação.

## Blocos do kit

Movimentos prontos no HyperFrames para este tipo (detalhes e o projeto inicial testado em `kit/motion/LEIA-ME.md`; instale com `npx hyperframes add <nome>`):

- `whiteboard-ink`: esboço de quadro branco com a caneta seguindo o traço
- `svg-stroke-trace`: desenho de linha que se traça e preenche
- `vox-annotate`: palavra recebe marca-texto à mão, com seta
- `grid-card-assemble`: cartões de recurso montam uma grade ou lista
- `zoom-through-transition`: atravessa um cartão até a cena seguinte
- `pull-back-reveal`: de um detalhe para o título e os cartões em volta
