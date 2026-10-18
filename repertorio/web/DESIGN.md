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

- Ao lado do tema, um menu compacto com prévias oferece Mapa livre (organização original), Por grupos (conjuntos por operação) e Hierárquico (operações, pistas, técnicas e referências da esquerda para a direita).
- Mudar a organização reposiciona o mesmo grafo e preserva seleção, busca, filtros, cores e miniaturas. A preferência é global no navegador; as câmeras são independentes por organização e espaço. O menu aparece no mapa; a alternância para lista continua na barra de busca.
- Uma referência com várias técnicas ocupa um único lugar, na operação com mais relações. As conexões cruzadas continuam presentes, discretas na visão geral e realçadas quando selecionadas.
- Hierarquia usa blocos de miniaturas com várias colunas e compacta técnicas sem referências diretas, para equilibrar bibliotecas pequenas e grandes. Nenhum modo altera a curadoria ou os vínculos dos espaços.
- Menu com seleção indicada, navegação por setas, Home/End e Escape. Fechar o menu por Escape preserva a ficha e devolve o foco ao botão. No celular, busca e controles reservam espaço uns para os outros.
