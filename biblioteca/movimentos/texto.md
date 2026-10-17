# Texto em movimento

`texto`

Palavras crescem, mudam de lugar ou trocam de conteúdo.

**Em HTML:** data-m por palavra (span) para palavras que continuam; as novas entram com fade.

## Receita com o motor

```html
<section class="slide">
  <span data-m="w1" class="palavra" style="left:120px;top:300px;font-size:150px">Menos</span>
  <span data-m="w2" class="palavra" style="left:120px;top:470px;font-size:150px">slides</span>
</section>
<section class="slide">
  <span data-m="w1" class="palavra" style="left:120px;top:140px;font-size:60px;opacity:.5">Menos</span>
  <span data-m="w2" class="palavra" style="left:100px;top:300px;font-size:420px;color:var(--acento)">slides</span>
  <span class="palavra" data-passo="0" data-entra="sobe" style="left:120px;top:820px;font-size:60px">mais conversa</span>
</section>
```

- Uma palavra por elemento (`.palavra { position:absolute; white-space:nowrap }`). As que continuam ganham `data-m`; as novas entram com passo.
- Ótimo para frase de efeito que se reorganiza, título que vira subtítulo, palavra-chave que cresce.

## Arquivos que usam (184)

- **157-reel-21-08-efeito-wow-rio-de-janeiro** (Rio de Janeiro, força 5): Vaze o nome do lugar numa tela branca para a foto aparecer só dentro das letras, e no avanço mergulhe numa das letras até a foto ocupar tudo: o nome vira a porta de entrada.  
  `_catalogo/pranchas/157-reel-21-08-efeito-wow-rio-de-janeiro.jpg`
- **canva-18** (Canva: Steph Curry, força 5): Coloque o nome da pessoa em duas linhas gigantes atrás do recorte e redesenhe em contorno, por cima do corpo, só a parte das letras que ele cobre, para o nome continuar legível sem esconder a pessoa. Na troca, deslize as duas linhas em sentidos opostos para abrir espaço para o texto, e volte ao nome inteiro para fechar o loop.  
  `_catalogo/pranchas/canva-18.jpg`
- **002-26-0102-cinema** (Cinema, força 4): Escolha um único acento de cor e aplique sempre na palavra-chave de cada título; todo o resto fica em preto, branco e fotos sem cor, e a repetição vira identidade.  
  `_catalogo/pranchas/002-26-0102-cinema.jpg`
- **027-reel-01-01** (Africa, força 4): Ponha a palavra-título gigante atrás do sujeito recortado e repita a mesma palavra só em contorno por cima dele: as letras somem atrás da cabeça, mas o traço continua visível e a leitura não se perde.  
  `_catalogo/pranchas/027-reel-01-01.jpg`
- **038-reel-03-01** (BYD, força 4): Cubra uma grade de quatro fotos com uma forma que só deixa um quarto à mostra e gire essa forma a cada slide: a janela passeia pelos itens como um relógio e o texto ocupa as áreas fechadas.  
  `_catalogo/pranchas/038-reel-03-01.jpg`
- **055-reel-04-10** (Lego players, força 4): Dê a cada item uma faixa de cor própria e alterne entre a visão geral, com todas iguais, e o foco, em que uma faixa engole a tela e o número de ordem vira gigante atrás do item.  
  `_catalogo/pranchas/055-reel-04-10.jpg`
- **057-reel-05-05** (Hamilton x Verstappen, força 4): Para um duelo, ponha os dois rivais de frente um para o outro nas bordas e mantenha o centro como palco do nome: a cada slide só o texto troca de dono e as fotos se acomodam de leve.  
  `_catalogo/pranchas/057-reel-05-05.jpg`
- **060-reel-05-09** (Gusttavo Lima, força 4): Comece com o fundo vazio só com letras gigantes quase da cor dele e, no avanço, faça o retrato subir de baixo enquanto o nome se reorganiza atrás em letras fantasmas, assentando a citação em serifa grande ao lado.  
  `_catalogo/pranchas/060-reel-05-09.jpg`
- **061-reel-05-10** (Eleições 2026, força 4): Num duelo entre dois, cubra a tela com uma forma gigante que tenha uma fatia aberta como janela: ela mostra um lado e esconde o outro, e girar a forma meia volta passa a vez ao rival sem trocar de cena.  
  `_catalogo/pranchas/061-reel-05-10.jpg`
- **067-reel-06-08** (Machu Picchu, força 4): Emoldure a foto do lugar com elementos desfocados em primeiro plano para dar profundidade, e quando entrar o texto, abra um painel com a própria foto desfocada em vez de um bloco de cor: a informação fica dentro da paisagem.  
  `_catalogo/pranchas/067-reel-06-08.jpg`

## Passagens de slide analisadas

- **219-reel-30-07#2**: "swot" cresce 7,2x, vai para a direita, termina ocupando a tela; 1 objeto(s) novo(s) surgem  
  `_catalogo/miniaturas/219-reel-30-07/02.jpg`
- **219-reel-30-07#4**: "swot" vai para a esquerda, termina ocupando a tela; bloco de texto vai para cima, o texto muda  
  `_catalogo/miniaturas/219-reel-30-07/04.jpg`
- **219-reel-30-07#9**: "sw" cresce 1,6x, vai para a esquerda, muda de proporção, o texto muda; "t" encolhe para 64%, vai para a esquerda, muda de proporção, o texto muda; "o" vai para cima, o texto muda, termina ocupando a   
  `_catalogo/miniaturas/219-reel-30-07/09.jpg`
- **283-reel-celula-3d#2**: "E SUAS ESTRUTURAS" sai da tela (esquerda); 3d "Modelo 3D 4" cresce 1,3x, vai para a esquerda; "células" sai da tela (esquerda); 2 objeto(s) novo(s) surgem  
  `_catalogo/miniaturas/283-reel-celula-3d/02.jpg`
- **283-reel-celula-3d#4**: "MITOCÔNDRIA" encolhe para 66%, vai para baixo, muda de proporção, o texto muda; 3d "Modelo 3D 4" cresce 1,2x, vai para cima, termina ocupando a tela; linha "Conector Reto 2" encolhe para 82%, vai par  
  `_catalogo/miniaturas/283-reel-celula-3d/04.jpg`
- **284-reel-cerebro-3d#3**: "CÉREBRO" vai para cima; "CÉREBRO" vai para baixo; "CÉREBRO" vai para a esquerda; 1 objeto(s) somem  
  `_catalogo/miniaturas/284-reel-cerebro-3d/03.jpg`
- **462-reel-portfolio#2**: "Portfolio" cresce 16,2x, vai para a direita, termina ocupando a tela; "NOME DO PROFISSIONAL" sai da tela (baixo); imagem "Imagem 7" entra vindo de fora (direita); 1 objeto(s) novo(s) surgem  
  `_catalogo/miniaturas/462-reel-portfolio/02.jpg`
- **462-reel-portfolio#3**: "Portfolio" vai para a esquerda, termina ocupando a tela; imagem "Imagem 7" sai da tela (esquerda); imagem "Imagem 1" entra vindo de fora (direita); 1 objeto(s) novo(s) surgem; 1 objeto(s) somem  
  `_catalogo/miniaturas/462-reel-portfolio/03.jpg`

Mais: `python3 -I ferramentas/buscar.py -m texto --doc arquivo --prancha`
