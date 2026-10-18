# Retomada do projeto

Atualizado em 18/10/2026 (America/Sao_Paulo).

## Objetivo atual

Retomar a apresentação da palestra “Você compraria de você mesmo?”. O usuário pediu primeiro o diagnóstico do que falta para finalizar, sem alterar a apresentação nesta etapa.

## Retomada da palestra

- Contexto e conversa anterior recuperados. O pedido original era melhorar apenas o visual, preservando texto, falas e storytelling da primeira parte.
- Base recomendada: `_saida/palestra-cx-ia-editorial/palestra.html`, com oito imagens geradas e todos os 185 trechos e 24 falas preservados. A sessão anterior parou na conferência visual.
- Pendências confirmadas: corrigir texto sobreposto e cortado no slide 7; concluir revisão dos 24 slides e dos cliques/transições; ensaiar tempo; gerar HTML único offline e PDF da editorial; consolidar a entrega.
- O roteiro existente é só a primeira parte. A palestra inteira ainda precisa dos blocos de IA, conexão com CX, prática, cases e conclusão.
- A visual-v2 contém acréscimos e mudanças de conteúdo, portanto não substitui automaticamente a editorial. Detalhes, evidências e próxima ação: `docs/RETOMADA-PALESTRA-CX-IA.md`.

## Entregue

- Incorporados pelo MCP 32 carrosséis, pastas 18 a 49, nas versões atuais: 429 lâminas e 229 arquivos de imagem em assets. A contagem inclui variantes e repetições entre produções.
- As 32 fichas e uma ficha de componentes estão publicadas, prontas e pesquisáveis. A ficha de componentes separa a paleta e 73 ícones SVG das fotografias de terceiros.
- Catálogo e estudos: `_referencias/growmate-livros/README.md`. Cada ficha explica a metáfora, a narrativa, as cores, os tipos e a ideia transferível, com links para o app.
- Originais, PNGs, recortes, fotos, fontes WOFF2, créditos e kit compartilhado: `_originais/growmate-livros/`, fora do Git. O projeto de origem não foi modificado.
- HTMLs autocontidos dos 32 carrosséis anexados ao app junto das lâminas e imagens-fonte. CSS, fontes, SVG e fotografias estão incorporados; os HTMLs originais e suas dependências também foram preservados localmente.
- Verificado: processamento de 33 fichas, busca, ausência de assets marcados como faltantes, download, hashes de 1.019 arquivos copiados e abertura dos 32 HTMLs sem dependências externas. Capas e miolos de quatro carrosséis idênticos entre fonte e cópia em comparação de capturas; interface local conferida.
- Manifesto com arquivos, hashes, IDs e resultados: `docs/REPERTORIO-GROWMATE-LIVROS.json`. Rotina retomável: `ferramentas/incorporar_growmate_livros.py`; renderização: `ferramentas/incorporar-growmate-render.cjs`.
- Corrigida a localização no grafo após o usuário relatar que não enxergava o conjunto: os 33 registros já estavam nos dados, mas as capas ficavam minúsculas no mapa geral. A busca agora enquadra os resultados na área livre e aceita links com `q`. Link direto: http://127.0.0.1:8766/?q=Growmate. Interface compilada; carregar a versão nova com ⌘R no app aberto.
- Correção do grafo validada com 7 testes unitários, 10 testes Playwright em biblioteca temporária e conferência visual dos 33 registros reais; capas e conexões carregadas, sem erros JavaScript. Evidências em `_saida/repertorio-qa/growmate-grafo/`.

## Base de eficiência preservada

- RTK OSS 1.0.1 e Engram 3.4.0 instalados em `~/.local/bin`, com os downloads oficiais verificados por SHA-256.
- RTK registrado no perfil Codex ativo, `expresso`. Novas sessões carregam o hook; nesta sessão, usar `rtk` explicitamente nos comandos compatíveis.
- Engram usado pelo terminal sob demanda, com dados locais e separados por projeto. Não foi adicionado um catálogo MCP ou observador de IA.
- Instruções globais de continuidade registradas no perfil ativo. O manual completo deste projeto está em `biblioteca/manual-agentes.md`; o `AGENTS.md` ficou menor.
- Gravação e recuperação da memória em processos diferentes, isolamento por projeto e teste interno de confiabilidade aprovados. Detalhes em `docs/EFICIENCIA.md`.

## Contexto útil

Repertório é o app de busca e curadoria do acervo PPTRETA. A criação segue roteiro, referências, revisão do usuário e conferência visual. A biblioteca real não recebe dados de demonstração.

Há versões da palestra “Você compraria de você mesmo?”, com 24 slides. Existem alterações anteriores em `_saida/palestra-cx-ia-visual/`, variantes `palestra-cx-ia-visual-v2/` e `palestra-cx-ia-editorial/`, além de duas pastas externas de gateway. Preservar esse trabalho; ele não pertence à instalação das ferramentas.

## Próxima ação

Para a palestra, seguir `docs/RETOMADA-PALESTRA-CX-IA.md`: retomar a editorial pela correção do slide 7 e concluir a revisão visual da primeira parte, sem reescrever a fala. Os blocos restantes exigem a continuação do conteúdo e a definição dos cases e duração total.

O repertório Growmate está incorporado e visível no grafo. Para novos materiais, consultar o catálogo e ler a revisão em Escolhas; preservar os créditos. O funcionamento automático do hook RTK em um Codex reiniciado e a economia total da assinatura ainda não foram medidos.
