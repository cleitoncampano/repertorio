# Fechamento

O último momento da fala: conclusão, chamada para ação e contato.
Escolha quando a tarefa é deixar uma frase na memória e dizer à plateia o que fazer agora; não é o slide de "dúvidas?" nem a capa repetida com ícones de rede.

## Na biblioteca

- 75 peças marcadas para fechar (2 de força 5, 54 de força 4, 15 de força 3, 4 de força 2): 35 apresentações, 32 carrosséis Growmate #Livros e 8 referências externas. Mais 208 slides avulsos: 8 de força 5, 70 de força 4 e 130 de força 3.
- Nas 24 fortes fora os carrosséis: câmera contínua em 42%, profundidade em camadas em 33%, tipografia como imagem e contraste de escala em 29%, empréstimo de código (interface, cartão, créditos) em 25%. Movimento: voo 38%, mergulho 33%, giro 29%. Nas 19 fracas: isolamento e contraste de cor em 42%, estética minimalista 47% e clara 42%, quase sempre sem movimento que ligue o fim ao começo.
- O fim fraco é o mais comum: 92 dos 130 slides de força 3 são o slide 20 de um modelo pronto, 56 só repetem a capa e 95 se apoiam em ícones de redes e contatos. Entre os 78 fortes, 21 voltam à abertura por movimento (recuo, loop, palavra que encolhe) e 21 terminam na marca sozinha.
- Os 32 carrosséis terminam com o fio (estrada, linha, régua, batimento) na mesma altura em que ele começa na capa, para a última lâmina emendar na primeira.

## Composições que funcionam

1. **Volta à capa, pelo movimento.** O último slide é a capa de novo, mas a câmera chega lá: recua do conteúdo, a palavra gigante encolhe até caber, o holofote se abre e devolve a foto inteira. A repetição vira conclusão porque a plateia vê o caminho. [Portfolio](http://127.0.0.1:8766/?workspace=pp-treta&ref=462-reel-portfolio), [Tremembé, slide 6](http://127.0.0.1:8766/?workspace=pp-treta&ref=105-reel-13-11#6), [Mapa Mundi - Escolaridade, slide 8](http://127.0.0.1:8766/?workspace=pp-treta&ref=212-reel-29-06#8).
2. **A forma da marca cobre a tela.** A forma que viajou pela apresentação (cartão, retângulo, cor) cresce até 100% da tela e deixa só o logo branco no centro e uma chamada de até 5 palavras embaixo. [Nubank](http://127.0.0.1:8766/?workspace=pp-treta&ref=435-reel-nu), [Nomad, slide 5](http://127.0.0.1:8766/?workspace=pp-treta&ref=434-reel-nomad#5), [iFood, slide 4](http://127.0.0.1:8766/?workspace=pp-treta&ref=379-reel-ifood#4).
3. **Convite curto e assinatura.** Dois slides. No primeiro, uma frase-convite de 3 a 6 palavras em letra larga pesada (120 a 160 px), alinhada à esquerda, sobre fundo escuro. No segundo, o nome em letra larga e o contato pequeno (24 a 28 px) no canto inferior direito, sobre cor clara. [Table Top Zoom, slide 6](http://127.0.0.1:8766/?workspace=pp-treta&ref=562-reel-zoom#6), [Table Top Zoom, slide 7](http://127.0.0.1:8766/?workspace=pp-treta&ref=562-reel-zoom#7).
4. **Obrigado com um acento.** Uma palavra gigante centralizada (200 a 260 px), o ponto final na cor de destaque, um fio curto e, embaixo, nome, e-mail e telefone em 3 linhas com o QR code ao lado. Sem ícones de rede espalhados. [Processo Industrial, slide 8](http://127.0.0.1:8766/?workspace=pp-treta&ref=320-reel-empurrao-completa#8), [Resultados Trimestrais, slide 7](http://127.0.0.1:8766/?workspace=pp-treta&ref=565-reel-zoom-numeros#7).
5. **Próximos passos com prazo.** De 3 a 4 colunas com número gigante, título de até 3 palavras e prazo escrito numa barra na base; a barra cresce um trecho por passo e muda de vermelho para laranja, amarelo e verde. Termina com todos à vista e a barra completa. [Próximos Passos](http://127.0.0.1:8766/?workspace=pp-treta&ref=472-reel-proximos-passos).
6. **Pergunta que fica.** Depois dos dados, volte ao símbolo do problema (mapa, objeto, rosto) e deixe uma pergunta curta sem resposta, sozinha na tela. [Uber, slide 10](http://127.0.0.1:8766/?workspace=pp-treta&ref=544-reel-uber#10).

## Movimento

- Feche o ciclo: o elemento-assinatura da capa reaparece no último slide, no mesmo lugar e tamanho, e o Morph o traz de onde ele estava (gigante, girado, fora da tela). Recuo de 1200 a 1500 ms depois do último conteúdo.
- Esvazie a tela: os elementos saem pelas bordas e sobra uma coisa só, a frase, o logo ou a pergunta com data e hora. [Convite Chá Revelação, slide 3](http://127.0.0.1:8766/?workspace=pp-treta&ref=292-reel-convite-bee#3), [Namorados 2025, slide 9](http://127.0.0.1:8766/?workspace=pp-treta&ref=025-cartao-namorados#9).
- Mergulho de volta: se a fala morou dentro de um objeto (tela de notebook, mesa, quadro), o fim entra de novo nele para o agradecimento. [Etapas](http://127.0.0.1:8766/?workspace=pp-treta&ref=329-reel-etapas-mac).
- Subida em paradas: numa imagem vertical alta, a câmera sobe uma parada por slide e a mensagem final ocupa o vazio do topo. [Mensagem Natal](http://127.0.0.1:8766/?workspace=pp-treta&ref=177-reel-24-12).
- A chamada entra no clique, não junto com o slide; o contato entra por último. Rolagem de créditos ou de texto longo só com poucas linhas e duração medida pela leitura.

## Como fazer no motor HTML

1. Loop com a capa: copie para o último slide o elemento-assinatura da capa com o mesmo `data-m`, mesma posição e tamanho; nos slides do meio ele pode estar com `scale(16)`, girado ou em `fora-dir`. No último, `data-trans="morph"` e `data-dur="1400"`.
2. Forma que cobre a tela: um `div` com `data-m="marca"` em `width:640px; height:400px; border-radius:32px` no penúltimo e `inset:0; width:100%; height:100%; border-radius:0` no último; o logo branco com `data-passo="0"`. Sem forma viajante, use `data-trans="circulo"` a partir do botão ou do logo.
3. Chamada e contato no ritmo da fala: frase com `data-passo="1" data-entra="mascara"`, contatos com `data-passo="2" data-entra="sobe"`. E-mail, telefone, QR e endereço reais ou com `class="provisorio"`.
4. Barra de prazo: um slide por passo com a mesma barra (`data-m="prazo"`) mais longa e de outra cor; o Morph anima largura e cor juntas. As colunas novas entram com `data-passo="1" data-entra="sobe"`.
5. Mesa ou mapa como menu: na capa, um cartão por capítulo com `<a href="#N">`, girado como papel sobre a mesa; no último slide, o mesmo mapa com tudo marcado antes do agradecimento. [Table Top Zoom](http://127.0.0.1:8766/?workspace=pp-treta&ref=562-reel-zoom).
6. Confira o fim com `python3 -I ferramentas/ver.py` e no PDF (que revela todos os passos): chamada, nome e contato legíveis, nenhum texto tapado por logo ou forma, `<body data-final>` só na versão de entrega.

## Em carrossel e story

- Nos 32 carrosséis Growmate (4:5, 2160 x 2700 px; no kit, `data-formato="4:5"`), a última lâmina repete o tom da capa (mesma cor de fundo, a pessoa recortada de novo) com: conclusão em sans muito pesada terminando em serifa itálica; chamada com ícone de marcador e destinatário ("Salve e envie para quem aprova políticas e contratos com você."); o próximo post anunciado; numeração 12 / 12. [Growmate #Livros 23 · Would You Do That to Your Mother? · Você faria isso com a sua mãe?](http://127.0.0.1:8766/?workspace=ff1be998-6589-4e3d-a1f2-e7682406e853&ref=criacao-a8c67c5d-406d-4a89-adff-06c25cac835d).
- O fio sai da última lâmina na mesma altura em px em que entra na capa, e às vezes um objeto da capa volta (o canhoto de protocolo, o anel centrado na divisa, a mão-francesa que se completa). [Growmate #Livros 08 · The Effortless Experience (2/3) · Uma cliente, três protocolos](http://127.0.0.1:8766/?workspace=ff1be998-6589-4e3d-a1f2-e7682406e853&ref=criacao-fab8a88d-57de-4515-b76c-562828f60c64), [Growmate #Livros 32 · A biblioteca do gerente de CX · A estante (v2)](http://127.0.0.1:8766/?workspace=ff1be998-6589-4e3d-a1f2-e7682406e853&ref=criacao-3cd5f79e-1776-4c3f-882c-31f131b7806a).
- A entrega prática (caderno, ata, formulário para preencher) vem uma ou duas lâminas antes; a última fica só para conclusão e chamada. [Growmate #Livros 16 · Muito Além da Sorte · A história do milk-shake (v2)](http://127.0.0.1:8766/?workspace=ff1be998-6589-4e3d-a1f2-e7682406e853&ref=criacao-050831e5-06a1-4c56-adb0-1fd784f13210).
- Em 9:16, a cena sobe e sai pelo alto e fica a marca com o site no terço do meio, em corpo que se leia no celular. [Nike KD14](http://127.0.0.1:8766/?workspace=pp-treta&ref=593-story-reel), [Feliz 2025](http://127.0.0.1:8766/?workspace=pp-treta&ref=154-reel-2025-insta).

## O que os melhores fazem

1. Terminam onde começaram, por um caminho visível: o último quadro responde ao primeiro. [Portfolio](http://127.0.0.1:8766/?workspace=pp-treta&ref=462-reel-portfolio), [Nubank](http://127.0.0.1:8766/?workspace=pp-treta&ref=435-reel-nu)
2. Uma coisa só na última tela: a frase, o logo ou a pergunta, com muito vazio. [Namorados 2025, slide 9](http://127.0.0.1:8766/?workspace=pp-treta&ref=025-cartao-namorados#9)
3. A assinatura é um gesto da própria apresentação, não um slide novo: chaves que se fecham em volta do logo, avião que sobe e devolve o logo ao branco. [XP](http://127.0.0.1:8766/?workspace=pp-treta&ref=560-reel-xp-palavras), [Azul](http://127.0.0.1:8766/?workspace=pp-treta&ref=086-reel-10-02)
4. A chamada tem verbo e destino: "Te espero pra um café", "Salve e envie para quem aprova". [Table Top Zoom, slide 6](http://127.0.0.1:8766/?workspace=pp-treta&ref=562-reel-zoom#6)
5. Os próximos passos têm prazo e estado, e a cor diz o quanto falta. [Próximos Passos](http://127.0.0.1:8766/?workspace=pp-treta&ref=472-reel-proximos-passos)
6. A mensagem sai de dentro de um objeto do tema, que vira a porta para o último slide. [Instax Natal](http://127.0.0.1:8766/?workspace=pp-treta&ref=185-reel-25-12), [Etapas](http://127.0.0.1:8766/?workspace=pp-treta&ref=329-reel-etapas-mac)
7. A pessoa encara e aponta para a lente: o retrato vira chamado. [Dave Dye (anúncios)](http://127.0.0.1:8766/?workspace=62224bbe-f662-4bb4-88af-fcf44b1c1e98&ref=ref-05-18-howard-gossage-01)

## Erros que derrubam

1. Capa repetida com quadrados de redes sociais: 56 slides fracos fazem isso; ninguém lê os ícones e o fim não diz nada novo. [Neon Company, slide 20](http://127.0.0.1:8766/?workspace=pp-treta&ref=003-26-0103-neon-company#20), [Healthy Food, slide 20](http://127.0.0.1:8766/?workspace=pp-treta&ref=016-26-0402-healthy-food#20)
2. Clichê no lugar do resultado: aperto de mãos recortado sobre foto desfocada. [Negócio Fechado](http://127.0.0.1:8766/?workspace=pp-treta&ref=377-reel-handshake)
3. Chamada ou passos ilegíveis: nomes miúdos em laranja escuro sobre preto, título branco sobre amarelo, QR pequeno demais para escanear da plateia. [3 próximos passos](http://127.0.0.1:8766/?workspace=pp-treta&ref=228-reel-3steps), [Mulheres](http://127.0.0.1:8766/?workspace=pp-treta&ref=322-reel-empurrao-mulheres)
4. Lista no lugar da conclusão: sete formas de terminar em duas colunas, fileira de links recomendados; o fim vira índice. [Manifesto Writing](http://127.0.0.1:8766/?workspace=62224bbe-f662-4bb4-88af-fcf44b1c1e98&ref=ref-04-cheatsheet-7-ways-to-end), [Eyecannndy (técnicas de câmera e edição)](http://127.0.0.1:8766/?workspace=62224bbe-f662-4bb4-88af-fcf44b1c1e98&ref=ref-06-08-eyecannndy-page-resources)
5. Créditos ou texto longo rolando mais rápido do que se lê. [Letra de Música](http://127.0.0.1:8766/?workspace=pp-treta&ref=401-reel-letra), [Créditos Filme](http://127.0.0.1:8766/?workspace=pp-treta&ref=223-reel-30-12)
6. Loop que volta a uma capa quase vazia: o ciclo fecha, mas a última tela fica muda, com uma palavra miúda no centro. [Time Brasil](http://127.0.0.1:8766/?workspace=pp-treta&ref=525-reel-timebrasil)

## Prompt base

```
Crie o fechamento de uma apresentação (conclusão, chamada para ação e contato) em HTML com o motor do kit,
na mesma pasta e com o mesmo motor.css e motor.js da apresentação, no projeto de destino.
Tema: [TEMA]. Conclusão em uma frase: [FRASE]. Ação que a plateia deve fazer: [AÇÃO E DESTINO].
Contato: [NOME, E-MAIL, TELEFONE, SITE, QR] ou provisório. Formato: [16:9 | 4:5 | 9:16].

Antes de desenhar: leia a capa e identifique o elemento-assinatura (palavra, logo, forma, objeto, fio).
O fechamento volta a ele. Mostre o plano dos slides antes de construir.

O que mostrar (2 ou 3 slides)
- Slide A: a conclusão em até 8 palavras, sozinha, ou a pergunta que fica, sobre o símbolo do tema.
- Slide B: a chamada com verbo e destino (até 6 palavras). Se houver passos, de 3 a 4 com prazo.
- Slide C: assinatura: o elemento da capa de volta, nome e contato pequenos (24 a 28 px), QR com 160 px ou mais.

Hierarquia
- Uma coisa dominante por slide: a frase em 120 a 180 px, ou a palavra de agradecimento em 200 a 260 px.
  Contato em bloco único de até 3 linhas. Uma cor de destaque, usada no ponto final, na barra ou no verbo.

Técnica (escolha uma)
- volta à capa pelo movimento; forma da marca que cresce até cobrir a tela; convite curto e assinatura;
  próximos passos com barra de prazo; pergunta final sozinha sobre o símbolo do problema.

Movimento
- Mesmo data-m da capa no último slide, data-trans="morph", data-dur de 1200 a 1500.
  Elementos do conteúdo saem pelas bordas (fora-esq, fora-dir) e sobra uma coisa só.
  Chamada com data-passo="1" data-entra="mascara"; contato com data-passo="2" data-entra="sobe".

Proibido
- repetir a capa parada com ícones de redes; "Dúvidas?" ou "Obrigado" sem conclusão antes; aperto de mãos,
  troféu ou foto genérica de banco; lista de tópicos ou de links no último slide; texto branco sobre cor clara;
  créditos rolando rápido; contato, número ou QR inventados sem class="provisorio"; marca de terceiros.

Conferir antes de entregar
- Rode python3 -I ferramentas/ver.py e imprima em PDF: a conclusão se lê de longe (e no celular em 4:5 e 9:16),
  o QR escaneia, o elemento da capa volta ao mesmo lugar sem salto, nada fica tapado pela forma que cobre a tela.
  Entregue a captura do último slide e diga em uma linha a frase que a plateia leva.
```

## Abra primeiro

- [Portfolio](http://127.0.0.1:8766/?workspace=pp-treta&ref=462-reel-portfolio): passeio por dentro das letras e recuo até a palavra caber de novo, igual à capa.
- [Table Top Zoom](http://127.0.0.1:8766/?workspace=pp-treta&ref=562-reel-zoom): mesa como menu, convite curto em fundo escuro e cartão final com nome e contato.
- [Nubank](http://127.0.0.1:8766/?workspace=pp-treta&ref=435-reel-nu): a forma da marca que encolhe no começo e cresce até virar a tela no fim.
- [XP](http://127.0.0.1:8766/?workspace=pp-treta&ref=560-reel-xp-palavras): delimitadores que se abrem para a palavra e se fecham em volta do logo.
- [Próximos Passos](http://127.0.0.1:8766/?workspace=pp-treta&ref=472-reel-proximos-passos): colunas com prazo e barra que vai do vermelho ao verde.
- [Uber](http://127.0.0.1:8766/?workspace=pp-treta&ref=544-reel-uber): dados construídos com o objeto do tema e pergunta final sem resposta sobre o mapa.
- [Etapas](http://127.0.0.1:8766/?workspace=pp-treta&ref=329-reel-etapas-mac): conteúdo dentro de uma tela de notebook e mergulho de volta para o agradecimento.
- [Growmate #Livros 23 · Would You Do That to Your Mother? · Você faria isso com a sua mãe?](http://127.0.0.1:8766/?workspace=ff1be998-6589-4e3d-a1f2-e7682406e853&ref=criacao-a8c67c5d-406d-4a89-adff-06c25cac835d): última lâmina 4:5 com conclusão, chamada para salvar e enviar e fio que emenda na capa.
