# Escalonado

`escalonado`

Entradas em sequência, uma após a outra.

**Em HTML:** animation-delay calc(var(--i) * 90ms).

## Receita com o motor

```html
<div class="card" data-passo="1" data-entra="sobe">...</div>
<div class="card" data-passo="1" data-entra="sobe">...</div>
<div class="card" data-passo="1" data-entra="sobe">...</div>
```

- Itens com o mesmo número de passo entram juntos com 90 ms de diferença (ajuste com `style="--i:3"`).
- `data-passo="0"` faz a cascata começar sozinha ao entrar no slide.

## Arquivos que usam (44)

- **041-reel-03-06** (Figurinhas Jogadores, força 4): Apresente cada item como algo que sai de dentro de uma embalagem: os pacotes descem para a borda e o conteúdo sobe de trás deles, um de cada vez, com o texto ao lado do que acabou de sair.  
  `_catalogo/pranchas/041-reel-03-06.jpg`
- **080-reel-08-07** (Cérebro 3D, força 4): Quando o dado é surpreendente, deixe só o número gigante, a unidade numa cor e fonte de contraste e uma legenda de uma linha, ao lado do objeto do tema em 3D; corte tópicos e diagramas.  
  `_catalogo/pranchas/080-reel-08-07.jpg`
- **114-reel-15-08** (Cidades Brasileiras, força 4): Comece com colunas de cor fechadas, uma por item, e abra uma por vez puxando a cor para cima como uma persiana: no fim, a mesma grade virou um painel completo de fotos e textos.  
  `_catalogo/pranchas/114-reel-15-08.jpg`
- **149-reel-20-08-graficos-e-esquemas-redbull** (RedBull, força 4): Use o objeto do tema como barra do gráfico: mostre-o primeiro apagado, como desenho sem cor, e encha cada um com a versão colorida de baixo para cima até a altura do valor, com uma linha e o número no topo.  
  `_catalogo/pranchas/149-reel-20-08-graficos-e-esquemas-redbull.jpg`
- **199-reel-27-09** (Peixe impactante, força 4): Faça um objeto recortado atravessar a tela passando entre o título cheio e uma cópia só em contorno: ele parece nadar por dentro das letras, e cada parada do percurso traz um novo fato.  
  `_catalogo/pranchas/199-reel-27-09.jpg`
- **208-reel-28-08-padroes-caixas-neon** (Caixas Neon, força 4): Apresente os itens como cartões escuros que acendem um de cada vez, cada um com um disco de cor viva atrás; os discos se sobrepõem e somam cores, como luzes de palco acendendo em sequência.  
  `_catalogo/pranchas/208-reel-28-08-padroes-caixas-neon.jpg`
- **236-reel-astecas-itens** (Astecas, força 4): Troque a lista de bullets por uma foto de clima em tela cheia: primeiro só a pergunta grande, depois ela encolhe e os tópicos entram em colunas com ícone, como legendas sobre a imagem.  
  `_catalogo/pranchas/236-reel-astecas-itens.jpg`
- **248-reel-beans** (Beans, força 4): Transforme o título numa palavra gigante e espalhe o objeto do tema ao redor dela em várias profundidades, um nítido atrás e outro enorme e desfocado na frente; depois faça os tópicos entrarem um por vez como blocos curtos com ícone.  
  `_catalogo/pranchas/248-reel-beans.jpg`
- **289-reel-coliseu-bullets** (Coliseu, força 4): Transforme a lista de bullets em duas cenas: primeiro a imagem em tela cheia com só o título, depois a imagem recolhe para uma faixa e os tópicos entram em colunas com ícone, separadas por filetes.  
  `_catalogo/pranchas/289-reel-coliseu-bullets.jpg`
- **295-reel-cortinas-abrindo** (Cortinas Abrindo, força 4): Encene a revelação como no palco: um slide de suspense com a cortina fechada e o anúncio curto, e a cortina se abre para mostrar o nome ou o resultado sobre um fundo vivo.  
  `_catalogo/pranchas/295-reel-cortinas-abrindo.jpg`

Mais: `python3 -I ferramentas/buscar.py -m escalonado --doc arquivo --prancha`
