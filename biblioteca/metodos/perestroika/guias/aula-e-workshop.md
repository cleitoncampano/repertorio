# Aula e workshop

Um encontro com começo, meio e fim que alguém conduz ao vivo (presencial ou online): aula, workshop, treinamento de equipe, palestra com dinâmica, onboarding. Escolha este guia quando a entrega não é só um deck, e sim um encontro em que as pessoas fazem algo e saem diferentes. Para vários encontros em sequência, use também `curso-e-programa`; para um evento único com público grande, `encontro-e-evento`.

Base: Experience Learning, a metodologia da escola Perestroika (23 pontos em 4 grupos). Fichas em `get_guide("perestroika/<ficha>")`.

## No método

- **Não é palestra, é aula.** Quem conduz tem compromisso com o que o grupo aprende: roteiro, preparação e um plano, mesmo que mude no caminho (`perestroika/nao-e-palestra-e-aula`).
- **Tudo serve a uma tese.** O encontro defende uma ideia própria de quem conduz, resumida numa tagline curta e sonora e reforçada por um treco, a experiência intensa que ninguém esquece (`perestroika/tese`, `perestroika/tagline`, `perestroika/treco`, `perestroika/fluxo-ttt`).
- **Fator dia seguinte.** O participante sai sabendo fazer algo que não sabia, e isso tem nome: o instrumento que leva (`perestroika/fator-dia-seguinte`, `perestroika/entrega-minima`).
- **Blocos curtos e estímulos que mudam.** A aula de 2h30 da Perestroika tem dez blocos: expositivo, perguntas, treco, processamento. Se um bloco falha, os outros compensam (`perestroika/framework-de-aula`).
- **Vínculo é parte do conteúdo.** Check-in no começo, check-out no fim, postura de anfitrião (`perestroika/check-in-check-out`, `perestroika/hosting`).

## Passo a passo

1. **Tese e entrega.** Preencha `perestroika/ficha-de-tese` (tese, tagline, treco) e responda: "no dia seguinte, sentado no computador, o que a pessoa vai saber fazer?". Se não houver resposta concreta, a tese ainda está abstrata.
2. **Perguntas que o encontro responde.** De 3 a 5 perguntas, na ordem em que serão respondidas (`perestroika/entrega-minima-e-dia-seguinte`). Elas viram os blocos de conteúdo.
3. **Blocos com horário.** Monte a grade com o modelo `perestroika/grade-de-aula` (conceito em `perestroika/framework-de-aula`): abertura (check-in curto, retomada, apresentação), conteúdo expositivo em partes de até 45 minutos, perguntas, intervalo, treco com instruções e execução, processamento (o que aconteceu e o que isso tem a ver com a tese), finalização com a tagline e o check-out. Troque de estímulo pelo menos a cada 30 a 45 minutos: expor, fazer, discutir.
4. **O treco.** Escolha uma experiência intensa que prove a tagline no corpo, não só na fala (aula de trás para a frente, invasão surpresa, jogo em grupo, simulação). Ela precisa de instruções claras e de um momento de processamento depois.
5. **Materiais.** Slides só para o expositivo e para as instruções do treco; o instrumento do dia seguinte (checklist, ficha, modelo) como arquivo que a pessoa leva.
6. **Deck.** Para os slides, siga o fluxo normal do Repertório: guias por momento (`abertura`, `explicar-e-sequenciar`, `fechamento`) e referências do espaço escolhido. A tagline volta no último slide.

## Formato da entrega

```markdown
# <Nome do encontro> · <duração> · <formato: presencial/online>
Tese: ...           Tagline: "..."            Treco: ...
Dia seguinte: o participante sai sabendo ... e leva <instrumento>.
Perguntas que o encontro responde: 1. ... 2. ... 3. ...

| bloco | começa | termina | o que acontece | estímulo | material |
|---|---|---|---|---|---|
| Check-in | 09:00 | 09:15 | ... | conversa | ... |
...
Check-out: pergunta de saída e como registrar o que mudou.
Riscos e plano B: o que fazer se o treco não couber no tempo ou se o grupo for menor.
```

## Erros que derrubam

- Encontro sem tese: vira "ciclo de palestras" ou bate-papo ("perguntem aí que eu vou respondendo"), postura que o material rejeita.
- Bloco expositivo de 90 minutos seguidos. A grade da Perestroika não passa de 45.
- Treco sem ligação com a tagline: diverte, mas ninguém lembra para quê. E treco sem processamento depois.
- Dia seguinte genérico ("entender melhor X"). Precisa ser um fazer verificável.
- Check-out cortado porque o tempo acabou. Reserve o tempo dele desde a grade.

## Prompt base

> Desenhe um <workshop/aula/treinamento> de <duração> para <público> sobre <tema>, seguindo o guia `aula-e-workshop` do Repertório. Antes da grade, preencha a ficha de tese (tese, tagline, treco) e diga o que o participante vai saber fazer no dia seguinte. Monte a grade em blocos com horário, trocando de estímulo a cada 30 a 45 minutos, com check-in, treco com processamento e check-out. Depois, proponha os slides só para os blocos que precisam deles.

## Fichas para abrir, nesta ordem

`perestroika/tese`, `perestroika/ficha-de-tese`, `perestroika/fator-dia-seguinte`, `perestroika/framework-de-aula`, `perestroika/grade-de-aula`, `perestroika/treco`, `perestroika/check-in-check-out`. Se o encontro for parte de um curso: `perestroika/arco`, `perestroika/mapa-conectivo`.

## Referências para abrir primeiro

- [Equação ilustrada do fluxo TTT](http://127.0.0.1:8766/?workspace=0cbf5669-0d0a-4745-844e-0745357c0419&ref=perestroika-04-forma%2341): conteúdo, olhar do professor, tese, tagline e treco numa linha só.
- [Roteiro de aula em tabela com horários](http://127.0.0.1:8766/?workspace=0cbf5669-0d0a-4745-844e-0745357c0419&ref=perestroika-06-estrutural%2321): os dez blocos da aula de 2h30.
- [Ficha TTT preenchida: Perestropoly](http://127.0.0.1:8766/?workspace=0cbf5669-0d0a-4745-844e-0745357c0419&ref=perestroika-04-forma%2343) e [registro do treco em fotos](http://127.0.0.1:8766/?workspace=0cbf5669-0d0a-4745-844e-0745357c0419&ref=perestroika-04-forma%2344): do papel à sala.
- [Frase com lacuna para completar](http://127.0.0.1:8766/?workspace=0cbf5669-0d0a-4745-844e-0745357c0419&ref=perestroika-04-forma%2316): o teste da tagline.
- [Mapa do método em quatro quadrantes](http://127.0.0.1:8766/?workspace=0cbf5669-0d0a-4745-844e-0745357c0419&ref=perestroika-02-experience-learning%2319): os 23 pontos de uma vez.
