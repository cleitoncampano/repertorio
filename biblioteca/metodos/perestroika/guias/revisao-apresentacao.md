# Revisão de apresentação

Conferir uma peça pronta (deck, carrossel, roteiro de vídeo ou de aula) antes de entregar ou apresentar. Escolha este guia quando já existe material e a pergunta é "o que melhorar?". A revisão devolve correções em ordem de prioridade, não uma nota.

Base: Checklist Apresentações Poderosas e o curso Chora PPT (escola Perestroika), mais tese e tagline do Experience Learning. Fichas em `get_guide("perestroika/<ficha>")`.

## Como revisar

Olhe a peça como a plateia vai ver: capturas de cada slide em tamanho real, todos os passos de animação, o roteiro de fala se houver. Revise em quatro camadas, da que mais derruba para a que menos derruba; não passe para a próxima com problema grave aberto na anterior.

1. **História** (`perestroika/tese`, `perestroika/tagline`, `perestroika/mapa-do-storytelling`)
   - Dá para escrever a tese numa frase? Ela aparece na peça?
   - Existe uma tagline que alguém repetiria no dia seguinte? Volta no fim?
   - As 8 cartas: objetivo claro (catraca), dados a serviço da história, explicação simples, credibilidade de quem fala, escuta do público, quebra de emoção, um momento humano, uma surpresa. Quais faltam?
2. **Estrutura** (`perestroika/inicio-meio-fim`, `perestroika/planejamento-da-apresentacao`)
   - Os primeiros 30 segundos prendem (dado, pergunta ou problema)? "Se não prender em 30 segundos, esquece."
   - O meio é coeso, um assunto puxando o outro? O fim conclui e diz o que fazer?
   - Cabe no tempo previsto? Combina com o formato (presencial, online) e com o que o público já sabe?
3. **Design** (`perestroika/design-de-slide`)
   - Um protagonista por slide; o resto é elenco de apoio. Com cinco elementos ou mais num slide, repense.
   - Cor com função (paleta curta, a cor marca o que importa); fontes legíveis; tudo alinhado.
   - Gráfico: título com destaque, legenda discreta, nada de informação repetida nem distorção, fundo que não disputa atenção.
   - Imagens que contam a história e ícones que resumem; slide é gratuito, divida quando apertar.
4. **Movimento e acabamento** (`perestroika/design-de-slide`, `perestroika/ensaio-e-finalizacao`)
   - Animações discretas, que não ofuscam a fala.
   - Ensaio em voz alta: tempo, passagem dos slides, pontos em que a fala trava.

Use `perestroika/checklist-apresentacao` como lista completa.

Só há roteiro, sem slides? Revise história e estrutura por inteiro. Em design e acabamento, comente o que a descrição de cada slide já permite (número de elementos, onde está o protagonista, se o gráfico tem um só dado) e liste o que precisa ser conferido nas capturas quando os slides existirem.

## Formato da entrega

```markdown
# Revisão: <nome da peça>
Tese que entendi: "..."   Tagline: "..." (ou: não encontrei)
## Corrigir primeiro (derruba a peça)
1. Slide N: problema. Por quê. Como corrigir.
## Depois (melhora muito)
## Se der tempo (acabamento)
## O que já funciona (manter)
```

Cada item aponta o slide, o problema visto, a regra do checklist e a correção concreta (texto novo, o que cortar, para onde mover). Máximo de 10 itens nas duas primeiras seções.

## Erros da revisão

- Revisar só o visual quando a tese não existe: polir um deck sem história.
- Lista genérica ("melhore o contraste") sem slide, motivo e correção.
- Pedir mais coisas: a revisão da Perestroika quase sempre corta.
- Julgar pela miniatura: abra em tamanho real e veja os passos.

## Prompt base

> Revise <peça> seguindo o guia `revisao-apresentacao` do Repertório. Olhe cada slide em tamanho real. Diga a tese e a tagline que você entendeu; depois liste as correções em ordem de prioridade (história, estrutura, design, acabamento), cada uma com slide, problema, regra e correção concreta. No fim, diga o que já funciona e deve ser mantido.

## Referências para abrir primeiro

- [Antes e depois de gráfico com chamadas](http://127.0.0.1:8766/?workspace=0cbf5669-0d0a-4745-844e-0745357c0419&ref=perestroika-checklist-completo-apresentacoes-poderosas%2312): os erros de gráfico, um por um.
- [Sem contraste e com contraste em grade](http://127.0.0.1:8766/?workspace=0cbf5669-0d0a-4745-844e-0745357c0419&ref=perestroika-checklist-completo-apresentacoes-poderosas%2318): um protagonista por slide.
- [Três iniciais gigantes: início, meio, fim](http://127.0.0.1:8766/?workspace=0cbf5669-0d0a-4745-844e-0745357c0419&ref=perestroika-checklist-completo-apresentacoes-poderosas%237).
- [Mapa do Storytelling em 8 cartas](http://127.0.0.1:8766/?workspace=0cbf5669-0d0a-4745-844e-0745357c0419&ref=perestroika-mapa-do-storytelling).
