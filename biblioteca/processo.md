# Processo: do pedido à apresentação pronta

Use este roteiro sempre que pedirem uma apresentação (palestra, pitch, aula, proposta), um site ou um vídeo com cara de apresentação.
Cada etapa diz o que ler, o que rodar e o que entregar. A produção fica no projeto de destino, com roteiro, imagens, prévias, validações e arquivos finais. Os comandos abaixo são utilitários da raiz do Repertório: informe caminhos do projeto de destino ou invoque os utilitários pelo caminho absoluto. `<pasta>` sempre representa a pasta daquela produção, fora desta biblioteca.

Referências vêm sempre do MCP do Repertório (`search_references`, `get_reference`, `get_guide`), nos espaços que o usuário escolheu: é a busca que reflete a curadoria do app. Sem o MCP, use `./app/run.sh search "pedido" --workspace ID_DO_ESPACO --prancha` e avise que o MCP estava fora. Os antigos `ferramentas/buscar.py` e `ferramentas/roteiro.py` leem o índice antigo: não use para escolher referências.

## 0. Entenda o pedido (2 minutos)

Anote antes de abrir qualquer referência:
- tema, público, duração ou número de slides, onde vai ser apresentado (palco, reunião, tela, celular; tem internet no local?);
- a estrutura ou o texto que o usuário trouxe e o objetivo: com o que a plateia sai;
- a identidade visual do usuário: cores, fontes, logo, tom. **A identidade é sempre a do usuário.** O acervo dá linguagem, ritmo e efeitos, nunca a marca.
  Se o usuário der liberdade criativa, crie um sistema próprio (passo 2) e diga qual é.
Se faltar identidade e não houver liberdade, pergunte. Se faltar o resto, assuma o sensato e diga o que assumiu.

## 1. História primeiro

Leia `biblioteca/principios/narrativa.md` (seções 1, 2 e 8). Para a tese, o objetivo e a audiência, leia também os índices de método com `get_guide` (`metodo-perestroika`, `metodo-soap`): cada um diz qual ficha abrir. Escolha a estrutura e escreva o roteiro **no formato da seção 8**, uma linha por slide:

```
n | INTENÇÃO | batida (o que a plateia entende) | conector | fala em 1 frase | visual
1 | IMPACTAR | ... | MAS | ... |
```

Regras: um slide, uma ideia. O conector entre linhas é MAS ou PORTANTO. No máximo 1 IMPACTAR por bloco.
Se o usuário trouxe o texto da fala, cada trecho vira uma linha e a fala vai para as anotações do slide (`<aside class="notas">`).
Passe o checklist da seção 9 antes de seguir.

## 2. Escolha a linguagem visual

1. Leia `biblioteca/principios/direcao-de-arte.md` (ordem de trabalho e seções 1 a 3): insight, ideia e onde a peça fica entre sensação visual e solução visual.
2. Procure 2 ou 3 modelos de linguagem parecida com `search_references`, descrevendo o clima e a estética (ex.: `"editorial em preto e branco com acento de cor"`), com `kind: "arquivo"` e `min_strength: 4`.
   Olhe a prancha e leia a `ideia` de cada um. As ideias mais fortes viram regra da apresentação inteira.
3. Escreva o sistema visual em 5 linhas: fundo (e se muda por capítulo), cor de acento e onde ela aparece, tipografia (título, texto, pesos), tratamento de imagem e **um elemento recorrente que viaja entre os slides** com `data-m` (uma forma, um ponto, uma faixa, um objeto). Esse elemento costura tudo.
4. Fontes: `biblioteca/tipografia.md`. Prefira Google Fonts e baixe para a pasta da apresentação (passo 6), para funcionar sem internet.

## 3. Referências para cada slide (uma rodada só)

1. Para cada momento, leia o guia do papel na história com `get_guide` (`abertura`, `provar-com-dados`, `fechamento`...): ele traz estrutura, erros e as referências para abrir primeiro. Use só as referências dos espaços escolhidos.
2. Busque com `search_references` descrevendo o que o slide precisa mostrar, em português comum (ex.: "número gigante com uma linha de explicação", "mapa com vários pontos"). Vêm primeiro as fichas que atendem mais partes do pedido; `understood` mostra como ele foi lido. Para só slides, `kind: "slide"`; para filtrar pela intenção, `intention: "<INTENÇÃO>"` (página em `biblioteca/intencoes/<INTENÇÃO>.md`).
3. Olhe a prancha e abra só as fichas escolhidas com `get_reference(include_image=true)`. Anote as escolhas num `referencias.md` da produção, com o link de cada ficha.
Escolha **a ideia**, não o layout, e anote qual técnica cada slide usa (`biblioteca/tecnicas/<id>.md`).
Inspirar não é copiar: mude pelo menos dois de composição, cor, tipografia, imagem e movimento em relação à referência.
Observação: o acervo tem poucos fechamentos fortes (FECHAR); para o final, use as dicas da página FECHAR e as referências externas.

## 4. Decida o movimento entre slides

Leia o roteiro em pares de slides e decida o que continua de um para o outro. O que continua ganha o mesmo `data-m`.
Receitas prontas em `biblioteca/movimentos/<família>.md`. Exemplos reais: `search_references` com `movement: "<família>"` e `kind: "arquivo"`.
Ritmo: Morph para continuidade, corte seco (`data-trans="corte"`) para virada, mergulho no máximo duas vezes, passos (`data-passo`) no ritmo da fala.

## 5. Imagens e mídia

- Do usuário primeiro. Do acervo, só o que não é de terceiros: `search_references` com `kind: "midia"` e `reusable: true` (ex.: "recorte de pessoa sem fundo"),
  e copie em alta: `python3 -I ferramentas/midia.py <id> <pasta>/img`.
- Ícones SVG soltos em `acervo/svg/` (busque "ícone" com `kind: "midia"`).
- Interfaces (busca, chat, post, notificação) ficam melhores feitas em HTML/CSS do que em imagem: são nítidas, editáveis e animáveis (técnica `interface-imitada`).

## 6. Construa com o kit

1. Crie a pasta da apresentação no projeto de destino e copie `kit/modelo.html`, `kit/motor.css` e `kit/motor.js` para ela. Não use `_saida/` do Repertório.
2. Fontes offline: `python3 -I ferramentas/fontes_google.py "Família 1" "Família 2" --pasta <pasta>/fontes` e use `<link rel="stylesheet" href="fontes/fontes.css">`.
3. Troque os tokens de identidade no topo do modelo. Manual do motor: `kit/LEIA-ME.md`; todos os recursos em `kit/demo.html`.
4. Slides em pixels fixos de 1920x1080 (ou 1080x1920), `position:absolute`, texto real. Se uma ficha falar em vw, 1vw = 19,2 px.
5. O que o usuário precisa trocar (dado sem fonte, foto de exemplo, nome do evento) recebe `class="provisorio"`.

## 7. Confira e corrija

```
python3 -I ferramentas/ver.py <pasta>/apresentacao.html --passos --transicoes
```
Abra `prancha.jpg` (estado final), `prancha-passos.jpg` (cada clique) e `prancha-transicoes.jpg` (o meio de cada passagem) e leia os avisos
(texto menor que 24 px, texto saindo do slide). Revise: hierarquia, legibilidade a 5 metros, contraste, consistência, um impacto por bloco, nada copiado.
Corrija e rode de novo.

## 8. Entregue

- Arquivo único, com fontes e imagens dentro (funciona sem internet): `python3 -I ferramentas/embutir.py <pasta>/apresentacao.html --imagens`
- PDF: `python3 -I ferramentas/ver.py <pasta>/apresentacao.html --pdf`.
- Diga ao usuário, em poucas linhas: a estrutura escolhida, o sistema visual, as referências que inspiraram os momentos fortes (ids) e o que ele precisa trocar (os `provisorio`).

## Para site e vídeo

- **Site:** mesma ordem (história, linguagem, referências). As seções viram "slides"; os Morphs viram transições de rolagem (View Transitions, `position: sticky`, animações por scroll). O vocabulário e a busca são os mesmos.
- **Vídeo:** o roteiro vira cenas; cada cena é um slide 1920x1080 (ou 1080x1920) e o motor grava bem em captura de tela. Movimentos e técnicas valem igual.
