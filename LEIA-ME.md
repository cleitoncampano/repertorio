# Como usar esta pasta

## Aplicação Repertório

O acervo agora também tem uma aplicação local: **Repertório**, com mapa interativo, busca compartilhada, curadoria, histórico e conexão MCP para agentes de projetos independentes.

- Abra `repertorio/Abrir Repertório.command` ou execute `./repertorio/run.sh serve`.
- Acesse **http://127.0.0.1:8766**.
- Instalação, integração com Codex/OpenCode, cadastro de criações e backup: [manual do Repertório](repertorio/README.md).

O protótipo e os scripts descritos abaixo continuam disponíveis. A curadoria feita na aplicação é persistida no banco do Repertório; os índices antigos permanecem como origem da importação.

## No dia a dia

1. Abra o terminal nesta pasta com o seu harness (Claude Code, Codex, OpenCode, Antigravity).
   Ele lê sozinho o manual (`AGENTS.md`) e já sabe o que existe aqui.
2. Peça do seu jeito, por exemplo:
   > Quero uma apresentação para uma palestra sobre X, para tal público, 20 minutos. A estrutura é esta: ... Minha identidade visual: cores ..., fonte ..., logo em ...
3. O modelo monta a história, busca referências no acervo, escolhe os movimentos e entrega um arquivo HTML que roda no navegador
   (seta para avançar, tecla F para tela cheia) e vira PDF.

Dica: se a sessão não parecer ter lido o manual, diga "leia o AGENTS.md antes de começar".

## Para ver o acervo com os próprios olhos

Dois cliques em `_catalogo/Abrir catálogo.command`: abre o catálogo com todos os 4.709 slides, com busca, e abre o arquivo original no PowerPoint.
Dois cliques em `_catalogo/Abrir mapa.command`: abre o mapa da biblioteca, com as peças ligadas às técnicas do jeito que o modelo enxerga e uma busca que mostra o que ele escolheria.
Para ver o motor de apresentação funcionando, abra `kit/demo.html` no navegador.

## O que tem aqui dentro

- **O acervo do PPTRETA** descrito slide a slide: o que cada um faz na história, a técnica visual, o movimento, a estética e uma nota de força de 1 a 5.
  Os slides "antes" que o curso mostra só para comparar ficam fora das buscas.
- **Referências de fora** (capas de revista, anúncios, ativações, aberturas de filme) ligadas pelas mesmas técnicas.
- **Princípios** resumidos de storytelling e direção de arte, tirados dos estudos da pasta `_referencias`.
- **Um motor de apresentação em HTML** que faz o efeito Morph do PowerPoint.
- **Mais de 9 mil mídias** tiradas dos arquivos (fotos, recortes sem fundo, ícones, vídeos, objetos 3D), etiquetadas e com aviso quando são de marcas ou famosos.

Os arquivos originais do curso estão em `_originais/` e não foram alterados.
