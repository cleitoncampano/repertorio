# Loop

`loop`

Movimento contínuo de ambiente (vídeo de fundo, gif, rotação lenta) ou sequência de slides que se repete (1-2-1-2) para virar vídeo em loop.

**Em HTML:** <video autoplay muted loop playsinline> ou animation infinite lenta.

## Receita com o motor

```html
<video class="sangria" src="fundo.mp4" autoplay muted loop playsinline></video>
<div style="animation: girar 40s linear infinite">...</div>
<style>@keyframes girar { to { rotate: 360deg } }</style>
```

- Movimento de ambiente dá vida a slide de abertura, divisor e encerramento, enquanto você fala.
- Vídeos do acervo: busque com `--doc midia --uso video`.

## Arquivos que usam (86)

- **canva-18** (Canva: Steph Curry, força 5): Coloque o nome da pessoa em duas linhas gigantes atrás do recorte e redesenhe em contorno, por cima do corpo, só a parte das letras que ele cobre, para o nome continuar legível sem esconder a pessoa. Na troca, deslize as duas linhas em sentidos opostos para abrir espaço para o texto, e volte ao nome inteiro para fechar o loop.  
  `_catalogo/pranchas/canva-18.jpg`
- **044-reel-03-09** (Taylor violão, força 4): Recorte a silhueta do objeto que simboliza o tema numa placa da cor do fundo e deixe uma foto deslizar lentamente por trás dela, como se a cena acontecesse dentro do objeto; use um vazio da própria silhueta para ancorar o texto.  
  `_catalogo/pranchas/044-reel-03-09.jpg`
- **046-reel-03-10** (Mistérios da Vida Marinha, força 4): Atravesse o título gigante com uma divisória de borda orgânica e inverta figura e fundo dos dois lados: de um lado letras brancas sobre o vídeo, do outro um painel branco com as letras vazadas deixando o vídeo aparecer.  
  `_catalogo/pranchas/046-reel-03-10.jpg`
- **059-reel-05-08** (Toronto, força 4): Apoie o título gigante, na mesma cor do fundo, sobre a borda de uma faixa lisa para as letras parecerem brotar dela; no avanço, role essa faixa para cima como uma página e traga os cards de conteúdo.  
  `_catalogo/pranchas/059-reel-05-08.jpg`
- **074-reel-07-07** (Fumaça Preta, força 4): Escreva a palavra-chave na mesma cor do fundo e passe por trás dela um vídeo de algo escuro que entra e sai da tela; a palavra nasce e desaparece com o movimento, sem nenhuma animação de texto.  
  `_catalogo/pranchas/074-reel-07-07.jpg`
- **077-reel-07-11** (Lançamento, força 4): Para pôr uma foto na frente do título sem perder a leitura, deixe o título sólido atrás da foto e repita só o contorno das letras, translúcido, por cima dela; o olho completa a palavra.  
  `_catalogo/pranchas/077-reel-07-11.jpg`
- **099-reel-12-11** (Mar, força 4): Recorte um vídeo do tema dentro das letras do título: a palavra vira janela para o movimento, e o fundo preto em volta deixa só a tipografia viva.  
  `_catalogo/pranchas/099-reel-12-11.jpg`
- **103-reel-13-08** (Números vazados, força 4): Recorte o número do passo de dentro da imagem, de modo que ele apareça como um buraco na cor do fundo, gigante e cortado pela borda; a contagem vira a própria imagem do slide.  
  `_catalogo/pranchas/103-reel-13-08.jpg`
- **121-reel-16-06** (Impacto Vídeo, força 4): Encha a palavra-chave com um vídeo que começa vazio e vai se espalhando, para as letras surgirem do nada enquanto a plateia olha; o fundo preto esconde tudo que não é letra.  
  `_catalogo/pranchas/121-reel-16-06.jpg`
- **152-reel-2024** (Ano-novo, força 4): Recorte uma palavra ou número gigante num véu escuro e ponha um vídeo por trás: o movimento só aparece dentro das letras, e a palavra vira janela para a cena.  
  `_catalogo/pranchas/152-reel-2024.jpg`

Mais: `python3 -I ferramentas/buscar.py -m loop --doc arquivo --prancha`
