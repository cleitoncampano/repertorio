# Foco

`foco`

Holofote: desfoca ou escurece o resto para destacar um item.

**Em HTML:** Classe .foco no alvo e .fora nos irmãos (blur/opacity).

## Receita com o motor

```html
<div class="card" data-foco="pilares" data-foco-em="1">Pilar 1</div>
<div class="card" data-foco="pilares" data-foco-em="2">Pilar 2</div>
<div class="card" data-foco="pilares" data-foco-em="3">Pilar 3</div>
```

- A cada clique um item acende e os outros apagam (classe `.focado-fora`). A plateia sabe exatamente de qual item você está falando.
- Para diagrama: deixe o esquema parado e acenda uma parte por vez.

## Arquivos que usam (57)

- **037-reel-02-12** (Stranger Things, força 4): Comece com a foto do grupo inteiro e depois apresente cada pessoa desfocando o grupo e acendendo só ela num recorte nítido no lugar onde está: o contexto fica, mas o foco é de um por vez.  
  `_catalogo/pranchas/037-reel-02-12.jpg`
- **047-reel-03-12** (Top Tênis, força 4): Mostre os itens numa grade 2x2 de cards coloridos e, a cada slide, alargue um card que ganha cor, texto e logo, enquanto os outros encolhem e escurecem: a grade vira um carrossel de foco sem sair do lugar.  
  `_catalogo/pranchas/047-reel-03-12.jpg`
- **105-reel-13-11** (Tremembé, força 4): Para apresentar várias pessoas de uma mesma foto, deixe a imagem parada e mova só um holofote: um véu escuro com um buraco circular que vai de rosto em rosto, com o nome de cada um trocando de texto ao lado.  
  `_catalogo/pranchas/105-reel-13-11.jpg`
- **112-reel-15-05** (Pringles Desfoque, força 4): Alinhe as variações lado a lado e, a cada slide, deixe só uma nítida e à frente, com as outras desfocadas como fora de foco de câmera; o texto ao lado troca junto e a plateia sente a lente mudando de foco.  
  `_catalogo/pranchas/112-reel-15-05.jpg`
- **119-reel-16-04** (Artemis II, força 4): Apresente cada integrante acendendo só o rosto dele numa foto de grupo escurecida, com cantoneiras de visor de câmera; no último avanço, abra a janela até a tela inteira para devolver o grupo completo.  
  `_catalogo/pranchas/119-reel-16-04.jpg`
- **125-reel-16-11** (Prós e Contras (Lanterna), força 4): Para comparar dois lados, use um foco de luz literal: escureça tudo menos o lado que está em discussão e gire a fonte de luz para iluminar o outro lado na hora de virar o argumento.  
  `_catalogo/pranchas/125-reel-16-11.jpg`
- **131-reel-17-08** (Palavras vazadas - título, força 4): Esconda o título numa tela preta com as letras vazadas e passe por trás uma luz colorida desfocada; a palavra aparece aos pedaços, só onde a luz está, como um holofote procurando o texto.  
  `_catalogo/pranchas/131-reel-17-08.jpg`
- **171-reel-24-04** (Jogadores, força 4): Apresente um grupo como uma sanfona de fotos verticais: a pessoa da vez abre a sua faixa e ganha cor e nome, as outras se encolhem sem sair de cena, e no fim todas ficam lado a lado em pé de igualdade.  
  `_catalogo/pranchas/171-reel-24-04.jpg`
- **187-reel-26-06** (Foco com forma - Seleção, força 4): Numa foto em que várias pessoas aparecem juntas, apresente uma de cada vez com um holofote: o resto escurece, o círculo de luz anda até a pessoa e o nome dela aparece colado ao corpo, sem trocar de foto.  
  `_catalogo/pranchas/187-reel-26-06.jpg`
- **195-reel-27-05** (Jogadores Copa, força 4): Deixe todos os itens em preto e branco e dê cor só ao que está sendo apresentado, alargando a coluna dele; a cor vira o holofote, e acender todos juntos no fim fecha o grupo.  
  `_catalogo/pranchas/195-reel-27-05.jpg`

Mais: `python3 -I ferramentas/buscar.py -m foco --doc arquivo --prancha`
