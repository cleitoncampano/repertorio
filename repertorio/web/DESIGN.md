# Repertório: o mapa vem primeiro

Superfície: exploração da biblioteca. Modo: Operate, com o acervo visual como foco.

Direção definida pelo usuário: o mapa deve ocupar a tela; marca, busca e navegação devem ser pequenos. Aplicação das skills Impeccable (distill) e Frontend Design à interface existente.

## Hierarquia

- Canvas ocupa toda a janela. Nenhum título promocional, cabeçalho editorial ou rodapé deve reduzir sua área.
- Uma barra flutuante de 44 px reúne marca, busca, filtros e alternância mapa/lista.
- Navegação flutuante com nomes acessíveis e dicas ao passar o mouse ou focar. No celular, fica embaixo.
- Busca pelo atalho `/`; Escape fecha filtros e detalhes. A lista permite explorar referências com teclado.
- Filtros e fichas são sobreposições. Mantêm o tamanho e a posição do mapa.
- A primeira visita enquadra o acervo completo. A câmera fica preservada durante a sessão; o controle de enquadramento restaura a visão geral.
- Miniaturas têm prévia ao passar o mouse. Cores identificam operações do olhar, nunca estados arbitrários.
- No celular, a legenda tem um controle com nome, e resultados começam abaixo do resumo da busca.

## Expressão visual

O protótipo `_catalogo/mapa/index.html` é a autoridade visual. Fundo preto #121212, painéis neutros, texto #ECE8E1. Eixos: diferenciação #FF5A3C, agrupamento #3E7BFF, sequência #F5B400 e previsão #B455FF. Modo claro usa papel #F7F5F0, painel #FFFDFA e texto #282520, preservando as cores das conexões. Tipografia compacta Avenir Next, com fallback Segoe UI e sans-serif. Sem fonte de destaque ou título gigante na superfície de trabalho.

## Verificação

Playwright verifica área do mapa acima de 95% da janela, barra até 48 px, estabilidade do canvas ao abrir filtros, atalhos, acesso à legenda no celular e limpeza de busca com o painel aberto. Fluxos de curadoria e integração continuam cobertos.

## Conexões e temas

- Linhas curvas ligam cada peça à técnica, na cor da operação daquela técnica. O eixo selecionado acende todas as ligações, independentemente da paginação da busca.
- Pistas ficam entre operações e técnicas. Rótulos se revelam ao selecionar; outros caminhos ficam discretos.
- Tamanhos variam conforme a força e a proporção real da miniatura. Distribuição com semente fixa e espaço entre peças evita um mosaico uniforme e mantém a localização estável.
- O painel do eixo explica a operação e suas técnicas. A técnica mostra sua definição, orientação HTML e referências. O painel da peça mantém os dados e ações de curadoria.
- Alternador claro/escuro no canto superior direito, disponível em todas as telas. Preferência local persistida, sem alterar a câmera nem remontar o grafo.

## Visualizações do grafo

- Ao lado do tema, um menu com nove prévias oferece Mapa livre (organização original), Por grupos (conjuntos por operação) e Hierárquico (operações, pistas, técnicas e referências da esquerda para a direita), mais seis linguagens visuais autorizadas pelo usuário: Cosmos, Metrô, Circuito, Jardim, Editorial e Prisma.
- Mudar a organização reposiciona o mesmo grafo e preserva seleção, busca, filtros e miniaturas. As três opções originais preservam a paleta; as seis novas atualizam cores, formas e linhas. A preferência é global no navegador; as câmeras são independentes por organização e espaço. O menu aparece no mapa; a alternância para lista continua na barra de busca.
- Uma referência com várias técnicas ocupa um único lugar, na operação com mais relações. As conexões cruzadas continuam presentes, discretas na visão geral e realçadas quando selecionadas.
- Hierarquia usa blocos de miniaturas com várias colunas e compacta técnicas sem referências diretas, para equilibrar bibliotecas pequenas e grandes. Nenhum modo altera a curadoria ou os vínculos dos espaços.
- Menu com seleção indicada, navegação por setas, Home/End e Escape. Fechar o menu por Escape preserva a ficha e devolve o foco ao botão. No celular, busca e controles reservam espaço uns para os outros.
- Cosmos usa órbitas e círculos em azul/violeta; Metrô usa estações e trajetos ortogonais; Circuito usa chips, portas e trilhas verdes; Jardim usa copas, folhas e ramos; Editorial usa colunas, serifas e linhas de tinta; Prisma usa uma malha isométrica de losangos e hexágonos coloridos. Cada proposta tem uma variante clara e outra escura.
- A legenda e o painel do eixo acompanham a paleta selecionada. Títulos sobre fundos coloridos escolhem tinta de contraste adequado; os do Prisma têm largura mínima legível no afastamento. As mídias originais ficam intactas, com enquadramento visual nas formas e prévia completa ao passar o mouse.
- O menu usa uma única coluna em todas as telas, com rolagem quando necessário. O item selecionado permanece acessível ao abrir; Tab sai do menu sem perder a sequência de foco. Rótulos radiais ou inclinados e índices verticais evitam colisões com miniaturas.
- Nas seis novas propostas, selecionar uma operação ou técnica no desktop enquadra o conjunto realçado na área livre ao lado da ficha, com margem para os controles e os nomes. As três organizações anteriores mantêm o comportamento da câmera.
