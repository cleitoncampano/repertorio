# Você compraria de você mesmo?

Versão final visual dos 24 slides da primeira parte, concluída em 18/10/2026.

## Para apresentar

Abra `palestra-arquivo-unico.html` no Chrome ou Edge. O arquivo contém imagens, fontes e motor, funciona offline e pode ser copiado sozinho para outro computador.

- Setas, espaço, clique ou PageDown: próximo passo ou slide.
- Seta à esquerda ou PageUp: voltar.
- F: entrar ou sair da tela cheia.
- P: abrir as falas e o cronômetro em outra janela.
- Home e End: primeiro e último slide.
- Acrescente `#7` ao endereço para abrir diretamente o slide 7.

O `palestra.pdf` contém uma página por slide, com todas as revelações visíveis. Ele serve para consulta e compartilhamento. A sequência com cliques, foco e transições está no HTML.

## Direção visual

Fotografias ilustrativas em preto e branco, papel claro, preto e coral. Os recursos dos carrosséis foram reconstruídos para esta fala: percurso contínuo, estações com ícones, cartões de momentos, círculos de descoberta e marcadores de foco. A procedência e as aplicações estão em `REFERENCIAS.md`.

Os 185 trechos, as 24 falas, a ordem, os passos e os grupos de foco são iguais aos da apresentação original. O título e a legenda do slide 7 foram reposicionados para eliminar a sobreposição. As oito imagens geradas anteriormente foram mantidas; os prompts estão em `imagens.json`. São cenas fictícias e ilustrativas.

## Arquivos de trabalho

- `palestra.html`: versão editável, com dependências locais.
- `recursos.css`: camada visual acrescentada nesta finalização.
- `visual.css`, `motor.css`, `motor.js` e `fontes/`: direção editorial e motor existentes.
- `img/`: imagens locais, fora do Git. O HTML único e o PDF já as incorporam.
- `VALIDACAO.json`: resultados e hashes dos arquivos finais.
- `_ver/`: capturas locais de slides, cliques, transições e páginas do PDF, fora do Git.

As versões anteriores foram preservadas nas suas pastas.

## Escopo

Esta entrega finaliza a primeira parte existente: abertura, experiência do cliente e descoberta da academia. O slide 24 mantém a passagem “Então, o que impede?”. Os blocos anunciados na agenda sobre IA, encontro de CX com IA, prática, cases e conclusão ainda precisam de continuação do roteiro. A duração da fala exige um ensaio do apresentador; o cronômetro está na janela P.

## Verificações

Conferidos os 24 slides, 53 estados de clique, 23 transições em velocidade normal, falas, teclado, tela cheia e janela do apresentador. Nenhum corte de texto ou erro JavaScript foi encontrado. O HTML único foi aberto numa pasta temporária, com requisições externas bloqueadas. O PDF foi renderizado com Poppler e suas 24 páginas foram revisadas visualmente.

As rotinas ficam em `ferramentas/conferir_palestra_cx_ia.cjs` e `ferramentas/exportar_palestra_cx_ia.cjs`, na raiz do projeto. A segunda aceita `--pdf` para exportar, `--offline` para conferir apenas a cópia independente, ou nenhum argumento para conferir transições e offline.
