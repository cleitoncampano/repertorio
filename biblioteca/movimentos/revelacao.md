# Revelação

`revelacao`

Máscara, cortina ou wipe descobre o conteúdo.

**Em HTML:** clip-path inset()/circle() animado de 0 a 100%.

## Receita com o motor

```html
<img src="foto.jpg" class="sangria" data-passo="1" data-entra="mascara">        <!-- cortina da esquerda para a direita -->
<img src="foto.jpg" class="sangria" data-passo="1" data-entra="circulo">        <!-- abre do centro em círculo -->
<section class="slide" data-trans="cortina">...</section>                       <!-- o slide inteiro entra como cortina -->
```

- Use quando o conteúdo é a resposta de uma pergunta feita antes (`pergunta-aberta`).
- Máscara em forma de letra ou ícone: `mask-image: url(forma.svg)` com `mask-size` animado.

## Arquivos que usam (57)

- **132-reel-17-09** (Tucano - Efeito Raio-X, força 5): Tenha duas versões da mesma imagem, a normal e a de dentro, e passe um quadrado que mostra a de dentro exatamente alinhado: parece uma lente que enxerga através do assunto.  
  `_catalogo/pranchas/132-reel-17-09.jpg`
- **138-reel-18-09-efeito-wow-anatomia-humana** (Anatomia Humana, força 5): Sobreponha à foto uma janela que mostra a camada interna exatamente alinhada com a pessoa, e mova a janela a cada slide para um ponto diferente: cada avanço é um novo corte do mesmo assunto.  
  `_catalogo/pranchas/138-reel-18-09-efeito-wow-anatomia-humana.jpg`
- **035-reel-02-10** (New York City, força 4): Mostre a cena primeiro como rascunho a lápis e revele a foto real no avanço, com o título no mesmo lugar: o desenho que ganha cor vira a metáfora de uma ideia que sai do papel.  
  `_catalogo/pranchas/035-reel-02-10.jpg`
- **038-reel-03-01** (BYD, força 4): Cubra uma grade de quatro fotos com uma forma que só deixa um quarto à mostra e gire essa forma a cada slide: a janela passeia pelos itens como um relógio e o texto ocupa as áreas fechadas.  
  `_catalogo/pranchas/038-reel-03-01.jpg`
- **041-reel-03-06** (Figurinhas Jogadores, força 4): Apresente cada item como algo que sai de dentro de uma embalagem: os pacotes descem para a borda e o conteúdo sobe de trás deles, um de cada vez, com o texto ao lado do que acabou de sair.  
  `_catalogo/pranchas/041-reel-03-06.jpg`
- **061-reel-05-10** (Eleições 2026, força 4): Num duelo entre dois, cubra a tela com uma forma gigante que tenha uma fatia aberta como janela: ela mostra um lado e esconde o outro, e girar a forma meia volta passa a vez ao rival sem trocar de cena.  
  `_catalogo/pranchas/061-reel-05-10.jpg`
- **070-reel-06-11** (Comunicar-se com Impacto, força 4): Deixe a frase incompleta em letra pequena sobre preto e faça a palavra que falta aparecer só quando um vídeo de cor ou movimento passa por trás das letras vazadas; a revelação é a própria palavra.  
  `_catalogo/pranchas/070-reel-06-11.jpg`
- **074-reel-07-07** (Fumaça Preta, força 4): Escreva a palavra-chave na mesma cor do fundo e passe por trás dela um vídeo de algo escuro que entra e sai da tela; a palavra nasce e desaparece com o movimento, sem nenhuma animação de texto.  
  `_catalogo/pranchas/074-reel-07-07.jpg`
- **114-reel-15-08** (Cidades Brasileiras, força 4): Comece com colunas de cor fechadas, uma por item, e abra uma por vez puxando a cor para cima como uma persiana: no fim, a mesma grade virou um painel completo de fotos e textos.  
  `_catalogo/pranchas/114-reel-15-08.jpg`
- **121-reel-16-06** (Impacto Vídeo, força 4): Encha a palavra-chave com um vídeo que começa vazio e vai se espalhando, para as letras surgirem do nada enquanto a plateia olha; o fundo preto esconde tudo que não é letra.  
  `_catalogo/pranchas/121-reel-16-06.jpg`

Mais: `python3 -I ferramentas/buscar.py -m revelacao --doc arquivo --prancha`
