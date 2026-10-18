# Retomada do projeto

## Nove propostas visuais de grafo disponíveis em 18/10/2026

Acrescentadas Cosmos, Metrô, Circuito, Jardim, Editorial e Prisma às três opções existentes. As seis novas têm geometria, paleta, formas, linhas e fundo próprios, com versões clara e escura. Menu com nove prévias, duas colunas no desktop e rolagem no celular. Paletas acompanham legenda e painel; selecionar eixo ou técnica enquadra as novas vistas ao lado da ficha. Preferência, busca, filtros, imagens e câmeras continuam preservados.

Build, 31 testes unitários e 21 de navegador aprovados. Conferidas 24 combinações dos espaços reais Growmate e PP Treta nos dois temas, todas as miniaturas e contagens preservadas, sem erros JavaScript. Ajustados rótulos, contraste, títulos no afastamento e enquadramento com o painel aberto. Evidências em `_saida/repertorio-qa/estilos-grafo/`; detalhes em `repertorio/VALIDACAO.md`. Interface compilada, atualizar com ⌘R; sem mudanças no banco ou no serviço. Próxima ação: o usuário experimentar as nove propostas. Preservar as alterações anteriores da palestra e do checkpoint.

## Três visualizações do grafo implementadas em 18/10/2026

Novo botão Visualização do grafo, ao lado do tema, com prévias de Mapa livre (arranjo original), Por grupos e Hierárquico. Mudar o modo reposiciona a mesma instância e preserva imagens, seleção, busca, filtros e ficha. Preferência global no navegador, câmeras independentes por espaço e modo. Novos controles também funcionam no celular; voltar ao Mapa livre pelo mesmo menu.

Build, 18 testes unitários e 19 de navegador aprovados. Conferidos os três modos nos espaços reais Growmate (33 referências, 292 conexões) e PP Treta (1.021 referências no mapa, 4.182 conexões), sem erros JavaScript. Evidências em `_saida/repertorio-qa/grafos/`; detalhes em `repertorio/VALIDACAO.md`. A hierarquia foi equilibrada após inspeção do acervo real. Interface compilada, atualizar com ⌘R; sem mudanças no banco ou no serviço. Próxima ação: o usuário experimentar as organizações e indicar os ajustes que desejar. Preservar as alterações anteriores da palestra.

## Catálogo de Skills implementado em 18/10/2026

Skills substitui Entradas na navegação, com somente as sete habilidades pedidas: Impeccable, Frontend Design, Landing Page Design, ImageGen, Presentations, HyperFrames e HyperFrames Creative. Catálogo global, busca por objetivo, categorias e descrições. Montar pedido permite editar a ideia e copiar para a conversa do agente, incluindo o espaço de inspiração e a revisão em Escolhas. Novas instalações não entram automaticamente; curadoria em `repertorio/web/src/skillCatalog.ts`.

Sugestões espontâneas ficam em Escolhas > Sugestões para o acervo quando há pendências. Build, 11 testes unitários e 16 de navegador aprovados em biblioteca temporária. Capturas conferidas em `/tmp/repertorio-skills-qa/`; detalhes em `repertorio/VALIDACAO.md`. Interface compilada: atualizar o app com ⌘R. Próxima ação: usar o catálogo e acrescentar habilidades somente quando o usuário pedir. Preservar os trabalhos de palestra e demais alterações anteriores.

## Espaços de trabalho implementados em 18/10/2026

O Repertório agora tem espaços com criação, renomeação, exclusão direta e definitiva e troca pela navegação esquerda. O acervo anterior está em PP Treta; novos espaços começam vazios. Fichas e arquivos são compartilhados, com publicação e lixeira independentes por espaço. Agentes recebem os espaços de inspiração e os destinos de incorporação explicitamente.

Validação: 32 testes do servidor, 7 da interface e 14 de navegador aprovados; build e migração numa cópia dos 15.662 registros aprovados. Backup anterior verificado em `_saida/repertorio-qa/espacos/antes-dos-espacos.zip`. Operação, contratos e recuperação: `docs/REPERTORIO-ESPACOS.md`.

Growmate já reúne os 32 carrosséis #Livros incorporados ontem, das pastas 18 (Simon Sinek) a 49, mais a ficha de paleta e 73 ícones SVG (33 referências no total). As mesmas fichas continuam em PP Treta, sem duplicar arquivos. Grafo, busca dos agentes e publicação dos 32 itens verificados. Espaço: `ff1be998-6589-4e3d-a1f2-e7682406e853`; contexto da vinculação: `55be2440-518d-49d6-a55f-b24b4fae5460`. Detalhes em `docs/REPERTORIO-GROWMATE-LIVROS.json`. Próxima ação: usar o espaço Growmate como inspiração quando o usuário indicar. Preservar os trabalhos de palestra descritos abaixo.

Atualizado em 18/10/2026 (America/Sao_Paulo).

## Objetivo atual

Finalização visual da primeira parte da palestra “Você compraria de você mesmo?”, autorizada pelo usuário com liberdade para escolher recursos dos carrosséis. Entrega consolidada em `_saida/palestra-cx-ia-codex/`.

## Retomada da palestra

- Contexto e conversa anterior recuperados. O pedido original era melhorar apenas o visual, preservando texto, falas e storytelling da primeira parte.
- Entrega oficial: `_saida/palestra-cx-ia-codex/palestra-arquivo-unico.html`, independente e offline, e `palestra.pdf`, com 24 páginas. A fonte editável é `palestra.html` na mesma pasta.
- Base editorial preservada, com as oito imagens geradas. Os 185 trechos, as 24 falas, os passos e os grupos de foco continuam idênticos ao roteiro original.
- Aplicados percurso contínuo, estações com ícones, cartões, círculos de descoberta e marcadores de foco derivados dos carrosséis. Corrigido o corte e a sobreposição do slide 7.
- Conferidos os 24 slides, 53 estados de clique, 23 transições, notas, teclado, tela cheia e janela P. HTML único aberto numa pasta isolada sem requisições externas; cinco slides idênticos em comparação de pixels. PDF renderizado com Poppler e 24 páginas revisadas. Evidências locais em `_ver/`; resultados e hashes em `VALIDACAO.json`.
- Seleção atual: `ee7c76be-312c-4896-a618-e256fed3555f`, no contexto existente `ca3449a4-fc0e-431b-9dac-9709490c6888`. O usuário delegou a escolha nesta rodada. A referência Vogue, cortada na revisão anterior, continua descartada.
- O tempo da fala ainda depende de ensaio do apresentador. A janela P inclui cronômetro.
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

Para apresentar a primeira parte, abrir o HTML único em `_saida/palestra-cx-ia-codex/`. A revisão visual e a exportação estão concluídas. Para avançar a palestra completa, receber ou recuperar a continuação da fala e definir os cases e a duração total. Detalhes em `docs/RETOMADA-PALESTRA-CX-IA.md`.

O repertório Growmate está incorporado e visível no grafo. Para novos materiais, consultar o catálogo e ler a revisão em Escolhas; preservar os créditos. O funcionamento automático do hook RTK em um Codex reiniciado e a economia total da assinatura ainda não foram medidos.
