# Contagem

`contagem`

Números e gráficos que crescem até o valor final.

**Em HTML:** Contador com requestAnimationFrame; barras com transform: scaleX de 0 a 1.

## Receita com o motor

```html
<div style="font-size:300px;font-weight:900"><span data-conta="87">0</span>%</div>
<div data-barra style="--v:.87;width:1600px;height:48px;background:var(--acento)"></div>
<div data-barra-v style="--v:.6;width:120px;height:600px;background:var(--acento)"></div>
```

- O número sobe até o valor ao aparecer (`data-casas="1"` para decimais). Barras crescem até `--v`.
- Um número por slide, gigante (`dado-como-heroi`). Contexto em uma linha ao lado.

## Arquivos que usam (28)

- **585-reels-nestle-grafico** (Páscoa Nestlé, força 5): Use o próprio produto como topo de cada coluna do gráfico, com a coluna na cor da embalagem; depois abra cada coluna num card da mesma cor para contar a história de um item por vez.  
  `_catalogo/pranchas/585-reels-nestle-grafico.jpg`
- **101-reel-13-05** (Gráfico Circular, força 4): Desenhe o indicador como anéis concêntricos gigantes que nascem fora da tela e só mostram um quarto de volta; no avanço, os arcos coloridos giram para dentro e param no valor de cada anel, com o rótulo na ponta.  
  `_catalogo/pranchas/101-reel-13-05.jpg`
- **148-reel-20-08** (Números giratórios, força 4): Mostre cada resultado como um contador mecânico: colunas de 0 a 9 que rolam até parar no valor, com o rótulo e a unidade fixos ao lado; o giro dá peso ao número antes de ele ser lido.  
  `_catalogo/pranchas/148-reel-20-08.jpg`
- **149-reel-20-08-graficos-e-esquemas-redbull** (RedBull, força 4): Use o objeto do tema como barra do gráfico: mostre-o primeiro apagado, como desenho sem cor, e encha cada um com a versão colorida de baixo para cima até a altura do valor, com uma linha e o número no topo.  
  `_catalogo/pranchas/149-reel-20-08-graficos-e-esquemas-redbull.jpg`
- **304-reel-dash-kraftheinz** (Kraft Heinz, força 4): Monte um painel fixo e troque só o recorte de dados: a cada item, as barras assumem a cor dele e os novos valores, o item cresce e gira no cartão de destaque e o menu lateral mostra qual está selecionado.  
  `_catalogo/pranchas/304-reel-dash-kraftheinz.jpg`
- **365-reel-grafico-dinamico** (Gráfico Dinâmico, força 4): Monte cada número como uma fita vertical de dígitos de 0 a 9 escondida atrás de uma janela; ao trocar de slide, as fitas correm até o novo valor enquanto a barra cresce ou encolhe, como um placar mecânico.  
  `_catalogo/pranchas/365-reel-grafico-dinamico.jpg`
- **366-reel-grafico-gptw** (Great Place to Work, força 4): Troque o gráfico de pizza por uma grade de quadrados contornados e encha-os de cor de baixo para cima até a porcentagem; a pessoa recortada entre o título e a grade dá rosto ao número.  
  `_catalogo/pranchas/366-reel-grafico-gptw.jpg`
- **368-reel-grafico-moderno** (Gráfico Minimalista Moderno, força 4): Apresente os valores primeiro como bolas alinhadas no chão e depois faça cada uma subir até a sua altura, deixando um rastro translúcido da mesma cor que vira a coluna.  
  `_catalogo/pranchas/368-reel-grafico-moderno.jpg`
- **373-reel-graficos-mascara** (Gráfico com foto em máscara, força 4): Recorte uma janela fixa numa moldura do tamanho do slide e faça as fotos passarem por trás dela de baixo para cima a cada tema; a janela parada dá continuidade e só o conteúdo troca.  
  `_catalogo/pranchas/373-reel-graficos-mascara.jpg`
- **418-reel-medalhas-bra** (Tabela de Medalhas, força 4): Transforme uma tabela de poucos números em objetos: cada número fica numa etiqueta pendurada sob a imagem do item que ele conta, pintada com a cor desse item.  
  `_catalogo/pranchas/418-reel-medalhas-bra.jpg`

Mais: `python3 -I ferramentas/buscar.py -m contagem --doc arquivo --prancha`
