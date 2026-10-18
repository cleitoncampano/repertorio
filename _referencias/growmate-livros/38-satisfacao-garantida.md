# Satisfação Garantida · Que meta pune quem resolve?

#Livros, post 21. Pasta de origem: `38-satisfacao-garantida`.

## Ideia transferível

Manter uma chamada em andamento para questionar indicadores de duração do atendimento.

## Como foi construído

- **Estrutura:** a ligação que não acaba. O carrossel é uma chamada em andamento: começa em 00:00:01 na capa, passa pelo painel que pune quem resolve, pelo que a Zappos desligou e ligou, pelo caso da pizza (com a espera de dois minutos) e chega aos recordes. Termina em 00:00:00, "a próxima ligação já está tocando", que reencontra a capa.
- **Fio:** uma onda de voz (barras arredondadas) atravessa todas as lâminas na mesma linha de base (y 1200). É gerada por senos com períodos inteiros sobre a largura total, por isso o fim da última lâmina emenda no começo da capa. Cor por fundo com `clipPath` (coral no escuro, preto no claro, no coral e no gradiente). Um cursor de reprodução com o tempo da chamada marca cada lâmina. Na espera do caso da pizza, a onda fica plana e pontilhada da lâmina 07 para a 08 e volta a se mexer quando a atendente retorna.
- **Capa:** Tony Hsieh recortado, sentado, erguendo o celular da Zappos, com os tênis sobre a onda de voz. Gancho: "Que meta pune quem resolve?". Cronômetro 00:00:01.
- **Fotos:** duas fotografias originais diferentes (capa: Delivering Happiness Book, 2009; lâmina 05: Randy Stewart, SXSW 2009). Créditos em `fontes.md`.

## Especificação

12 lâminas de 2160 × 2700 px. Base de composição: 1080 × 1350 px, exportação 2x.

Paleta: `#0A0A0A`, `#F5F2EB`, `#EFEDE6`, `#FF4D2E`, `#C8321C`, `#FFE66B`. Fontes: Inter Tight, Fraunces itálico e JetBrains Mono.

## Roteiro da fonte

1. Capa: Hsieh recortado sobre a onda; "Que meta pune quem resolve?"; cronômetro 00:00:01; livro e crédito.
2. Exemplo, o painel de sempre: ligação de 4 min dentro da meta (cliente volta amanhã) e de 19 min fora da meta (problema resolvido). Tempo médio de atendimento.
3. Coral: visor sem leitura "--:--:--". "A Zappos não media o tempo de ligação."
4. Painel de chaves: desligado (meta de tempo, roteiro, venda empurrada); ligado (ir além por cada cliente, conexão emocional pessoal, PEC).
5. "Cada ligação é marca, não custo." 5% das vendas pelo telefone; todo cliente liga ao menos uma vez. Foto de Hsieh no SXSW 2009.
6. Produto em falta: três janelas de concorrentes, a terceira tem. Sem roteiro, julgamento de quem atende.
7. Caso da pizza (1): madrugada em Santa Monica, o desafio, a ligação em espera. A onda fica plana.
8. Caso da pizza (2), gradiente: 5 pizzarias em 2 minutos; cliente para a vida toda. A onda volta.
9. O relógio não conta. O que conta? No livro: ir além por cada cliente. Fora do livro: cerca de metade da avaliação ligada aos 10 valores (Workforce Management, 2009).
10. Os recordes: quase 6 h (livro), 10 h 29 min (2012), 10 h 43 min (2016). "Ninguém precisa de ligação de dez horas": quem decide quando a conversa acaba.
11. Leve para a reunião: ficha "Essa meta pune quem resolve?" com tempo médio, fila, roteiro e venda por ligação, caixas sim e não, e o que medir no lugar.
12. Fechamento: 00:00:00, nova chamada; salvar e enviar; próximo post, #Livros 22.

## Arquivos preservados

Originais e dependências: `_originais/growmate-livros/carrosseis/38-satisfacao-garantida/`. Arte em `carrossel.html`, lâminas em `out/`, assets em `assets/`, créditos em `fontes.md`. A cópia `repertorio-autocontido.html` incorpora as dependências visuais para download no app.

## Reutilização

Estudo da construção, sem aprovação automática para copiar a peça. O conjunto mistura criação da Growmate e fotografias de terceiros. As condições registradas na produção foram preservadas em `fontes.md`; recortar uma fotografia não altera sua origem. As referências externas não foram revalidadas nesta incorporação.

Ficha no app: [Satisfação Garantida · Que meta pune quem resolve?](http://127.0.0.1:8766/?ref=criacao-bef90665-b647-436b-84cf-cf0899ef0b3a).
