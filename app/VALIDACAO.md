# Validação da primeira versão

## Nova organização do mapa das imagens em 22/10/2026

- Os quatro eixos do olhar saíram da tela. A legenda passa a oferecer **História**, **Recurso visual** e **Formato**, salvos por espaço (escolhas antigas de eixos viram recurso visual).
- **História**, padrão das imagens: seis momentos na ordem de uma apresentação, Abrir (abrir, situar, apresentar), Conduzir (dividir, sequenciar), Explicar (explicar, agrupar, comparar), Provar (provar, mostrar, localizar), Marcar (impactar, destacar, citar) e Fechar, com os papéis em volta. Os mesmos grupos dos guias. Peças sem papel ficam em "Sem papel". Selecionar um papel filtra a lista pela intenção correspondente.
- **Recurso visual**: as 48 técnicas em sete famílias, cada técnica numa só, com as mesmas conexões de antes: Cor e contraste, Tipografia, Imagem e foto, Composição e grade, Percurso e revelação, Ideia e surpresa, Dados e interface.
- **Formato** sem mudança; segue como padrão dos vídeos.
- O vocabulário e a busca dos agentes não mudaram. Com mais de quatro grupos, o anel central abre e as fatias das técnicas encolhem para não invadir o vizinho; com até quatro, posições idênticas às de antes. Nomes de grupo com mais de uma palavra quebram dentro do círculo; a legenda fica numa linha e rola nas telas médias.
- 47 testes do servidor, 60 da interface (incluindo uma técnica por família e o desenho dos momentos nas nove visualizações) e 30 de navegador aprovados; testes antigos dos eixos passaram para os momentos. Capturas em 1440, 1180 e 390 px, sem erros nem transbordamento, em `app/.runtime/qa/organizacao/`.

## Melhorias dos vídeos levadas às imagens em 22/10/2026

- Tela grande para todas as referências: clicar numa imagem no mapa, na lista, no painel do eixo ou em Escolhas abre a peça grande com a ficha ao lado (ideia, como funciona, como fazer em HTML, conexões, papel na história e parecidos). Numa apresentação, a faixa de slides embaixo e ↑ ↓ passam pelos slides. ← →, N e P, as setas na tela, dois dedos no trackpad e o deslize no celular trocam de referência, na ordem da busca, da lista ou do espaço. Modo teatro (T) e tela cheia (F) como no player. **Ficha completa** abre o painel lateral, que continua com curadoria, espaços e o que o agente recebe. Links com `?ref=` seguem abrindo o painel.
- Capas com o dobro do tamanho em todos os espaços e nas nove visualizações, com espaçamento dobrado; prévia ao passar o mouse com 496 px. Sem sobreposição nos testes das nove visualizações.
- Organizar por formato: botão **Eixos do olhar / Formato** na legenda, guardado por espaço. No formato, o centro mostra Horizontal 16:9, Vertical 9:16, Quadrado e 4:5 (e Prompts-modelo); em volta, o papel na história (imagens) ou o tipo de vídeo. Vídeo começa por formato; imagem, pelos eixos. O formato de cada peça é gravado na ficha (importação, processamento e preenchimento na partida do serviço), sem consulta extra no mapa: grafo do PP Treta em 107 a 118 ms, como antes. Acervo real: 1.103 horizontais, 123 quadradas ou 4:5, 30 verticais. O 4:5 passou a contar como feed (dois vídeos do Motion mudaram de vertical para quadrado e 4:5).
- Guias por papel na história em `biblioteca/guias/`: abertura, agenda e divisores, impacto e destaque, apresentar pessoas, explicar e sequenciar, agrupar e comparar, provar com dados, mostrar e localizar, fechamento, e formatos e carrossel (1.125 linhas, 536 links conferidos contra o acervo, sem traços longos). Tirados das fichas e das prévias das peças mais fortes e mais fracas de cada momento. `get_guide` lista também esses guias e o motor HTML (`kit-apresentacao`); `start_context` informa `guides_available`.
- 47 testes do servidor, 58 da interface e 30 de navegador aprovados, incluindo o novo das imagens; três testes antigos passaram a abrir a ficha pela tela grande. Capturas em `app/.runtime/qa/imagens/`.

## Vídeos de motion no espaço Motion em 22/10/2026

- Galeria completa do Prompt Motion importada no novo espaço **Motion** (`81287ed7-121b-4249-88f2-bff35d60e1cb`): 234 vídeos e 2 modelos de prompt reescritos pelo site, 236 referências externas com `reusable=false`. Mídia baixada para `_originais/prompt-motion/` (704 arquivos, 2,5 GB, sem falhas), fora do Git e do backup, como os demais originais. A fonte permite uso como referência (`Content-Signal: use=reference`, sem treino).
- Cada ficha foi escrita em português por seis agentes a partir de uma prancha com oito momentos do vídeo: descrição, ideia transferível, decupagem com tempos, como recriar em código, técnicas, intenções, movimentos, estéticas, tons, usos e cuidados. Força: 22 com 5, 135 com 4, 75 com 3 e 4 com 2. Vídeos com dados aparentemente inventados, marca de terceiros ou trilha de terceiros têm o alerta nos cuidados.
- Agente: `search_references` aceita `format="mp4"` e mostra a duração na prancha; `get_reference(include_image=true)` devolve prompt original, decupagem, procedência e a prancha de quadros no lugar da capa. Novas frases comuns de movimento (tipografia cinética, push in, pull back, morphing, órbita, gráfico animado, explainer).
- Interface: o mapa toca até 12 vídeos visíveis com pelo menos 72 px, por cima das capas, recortados no formato de cada visualização; espaços sem vídeo não criam a camada e "reduzir movimento" desliga a reprodução. Passar o mouse mostra o loop, a lista toca os cartões visíveis e a ficha tem player com som, decupagem, prompt para copiar, créditos e **Ver quadros**.
- Medição na cópia do acervo, Chromium sem limite de quadros, 3 rodadas arrastando o mapa: 1.066 a 1.099 quadros/s sem vídeos e 450 a 490 com 12 vídeos, cerca de 1,2 ms a mais por quadro; pior quadro igual nos dois casos (21 a 24 ms). Grafo do Motion em 57 ms; PP Treta inalterado (1.021 referências, sem vídeos).
- Corrigido defeito anterior da lista em todos os espaços: com muitos cartões, a grade espremia as linhas na altura da tela (56 px) e os cartões se sobrepunham, no Chromium e no WebKit. A versão anterior compilada à parte mostrou o mesmo defeito. `grid-auto-rows:max-content` restaura a rolagem; conferido em Motion e PP Treta.
- Importação ensaiada numa cópia do banco (236 em 0,7 s; reimportação preserva tudo em 0,03 s; integridade e chaves estrangeiras válidas) antes do acervo real, com backup prévio no iCloud (`repertorio-2026-10-22-201440`). Acervo real: 15.898 referências e 27.173 arquivos, nenhum ausente, integridade `ok`.
- Ajuste pedido no mesmo dia: capas de vídeo com o dobro do tamanho no mapa, nas nove visualizações, e espaçamento das capas dobrado em espaços com vídeo para não sobrepor; prévia ao passar o mouse com o dobro do tamanho (496 px). Comparação com a versão anterior sobre os grafos reais: PP Treta e Growmate com posições idênticas nas nove visualizações; Motion com todas as capas dobradas e nenhuma sobreposição. 46 testes da interface e 28 de navegador aprovados. Capturas em `app/.runtime/qa/motion/dobro/`.
- Player em tela grande, a pedido: clicar num vídeo no mapa ou na lista abre o vídeo cobrindo o app, com som, em vez da ficha lateral. Modos do YouTube: padrão (vídeo grande com detalhes, prompt e "A seguir" ao lado), teatro (vídeo na largura toda, detalhes abaixo) e tela cheia do sistema, com a janela inteira como alternativa quando o navegador não permite. Atalhos espaço ou K, F, T, M, N, setas, J, L e 0 a 9; controles somem após 2,5 s parados e, no toque, o primeiro toque mostra os controles. **Ficha completa** volta à ficha lateral, que ganhou **Assistir em tela grande**. Conferido no Chromium e no WebKit, nos temas escuro e claro e a 390 px: reprodução com som, tela cheia do sistema nos dois motores, sem erros nem transbordamento. Capturas em `app/.runtime/qa/motion/player/`.
- Trocar de vídeo sem sair do player, como no Prompt Motion: setas nas laterais do vídeo, botões ‹ › com contador ("2 de 234") no canto da coluna, teclas ← → (Shift + ← → avança 5 s), N e P, dois dedos para o lado no trackpad (um gesto troca um vídeo só, mesmo com a inércia) e deslize do dedo no celular, com entrada deslizando na direção escolhida (desligada com "reduzir movimento"). A ordem segue a busca ou a lista abertas; sem elas, o espaço inteiro dos mais fortes para os mais fracos. Os atalhos passaram a valer na página inteira enquanto o player está aberto: em tela cheia o F às vezes não chegava ao player (teste falhava em 2 de 4 rodadas; após a mudança, 4 de 4). Conferido no Chromium e no WebKit, desktop e 390 px. Capturas em `app/.runtime/qa/motion/passar/`.
- Nova organização dos espaços de vídeo, a pedido: os quatro eixos do olhar (feitos para slides) saíram do mapa do Motion. No centro ficam os formatos de tela, onde o vídeo vai passar: Horizontal 16:9 (YouTube, sites e apresentações, 201 vídeos), Vertical 9:16 (Reels, TikTok e Shorts, 19), Quadrado e 4:5 (feed, 14) e Prompts-modelo (2). Em volta de cada formato, o tipo de vídeo: lançamento de produto, showreel, explicativo, dados e números, tipografia e mensagem, histórias e personagens, arte abstrata e 3D, marca e vinheta. Tipos revisados à mão em `dados/motion/generos.json` a partir das fichas (cerca de 45 correções sobre a sugestão automática). Legenda, painel do eixo e as nove visualizações usam a nova organização; "Por grupos" separa os formatos lado a lado. As técnicas criativas continuam em cada ficha e na busca. Espaços de imagem e espaços mistos mantêm os eixos do olhar. Formato e tipo também chegam ao agente (`aspect`, `genres`) e à busca por palavras (vertical, Reels, TikTok, YouTube, feed, explicativo). Reimportação real: 236 atualizadas, nenhum arquivo ausente, backup prévio `repertorio-2026-10-22-210045`. Capturas em `app/.runtime/qa/motion/formatos/`.
- Vídeos criados voltam ao acervo como os da galeria: ao incorporar um MP4, MOV ou WEBM, o processamento gera prancha de oito quadros, loop curto de 4 s sem som, capa, medidas e formato de tela, e o vídeo ganha player, loop no mapa e Escolhas. `register_reference` aceita `genres` (tipos de vídeo, validados) e `prompt`; atualizar a ficha sem informá-los preserva os dois. A tela Escolhas toca os vídeos visíveis e abre o player grande; o player passou a valer em todas as telas. A ferramenta da galeria usa as mesmas funções de vídeo do app. Testes: 46 do servidor (vídeo vertical criado, busca pelo prompt e por "tiktok", tipo inválido recusado, atualização preservando tipo e prompt), 57 da interface e 29 de navegador.
- Guias por tipo de vídeo em `biblioteca/motion/guias/`: lançamento, showreel, explicativo, dados, tipografia, histórias, abstrato e vinheta, mais formatos de tela e como escrever o prompt. Cada um tirado das fichas e das pranchas da galeria, com números, estrutura cena a cena por duração, ritmo, visual, padrões dos de força 5 e 4 com links, erros, prompt base, referências para abrir primeiro e os blocos do kit indicados para o tipo. Agentes leem pelo MCP com `get_guide` (sem nome, lista os disponíveis); `start_context` informa `video_guides_available`. O nome do guia é conferido contra a lista.
- Kit de motion em `kit/motion/`: mapa de 15 movimentos da galeria para 59 blocos do registro do HyperFrames (todos conferidos no catálogo da versão 0.8.186), em `LEIA-ME.md` e `movimentos.json`, e o projeto inicial `inicio/` (título palavra por palavra, cartões em cascata, número que conta e marca, 13,2 s) com identidade em variáveis. `npx hyperframes check` sem erros, contraste 16 de 16 e render de 1920x1080 em 14 s; aviso de primeiro quadro vazio documentado. Artefatos do HyperFrames fora do Git. Render e prancha em `app/.runtime/qa/motion/kit/`. 47 testes do servidor aprovados.
- 45 testes do servidor, 37 da interface e 28 de navegador aprovados, incluindo os novos de importação, curadoria preservada, vídeo por partes (Range), imagem do agente e reprodução no mapa, ficha e lista. Capturas em 1440 e 390 px sem erros JavaScript nem transbordamento. Evidências em `app/.runtime/qa/motion/`.

## Produto, demonstração e instalação local em 19/10/2026

- Nova entrada **Conheça o Repertório**, em `/?view=guide`: proposta do produto, fluxo, papéis, exemplo de pedido e ações funcionais para copiar, explorar, abrir Skills e conectar um agente. Navegador local em Mac e Windows, aplicativo opcional no Mac. Visual do mapa e nove visualizações preservados.
- 43 testes do servidor, 34 da interface e 27 de navegador aprovados localmente. Após o ajuste final de texto, os três testes do guia e da revisão passaram novamente. Build da interface aprovado; não foi recompilado ou substituído o aplicativo nativo instalado.
- Validação remota do código `56105e0`: 43 testes em cada sistema, Mac e Windows, mais preparação da instalação e execução do iniciador de demonstração por shell e PowerShell. [Execução aprovada no GitHub](https://github.com/cleitoncampano/repertorio/actions/runs/39272717798). Essa execução usa macOS e Windows Server hospedados; não equivale a homologação de um instalador comercial assinado.
- Portabilidade: bloqueio por `fcntl` em Unix e `msvcrt` no Windows, dependências universais com os marcadores de plataforma, arquivos ZIP com caminhos POSIX e fechamento explícito das conexões SQLite antes da limpeza ou renomeação de arquivos. O teste real do Windows detectou as dependências condicionais e os arquivos abertos do backup; corrigidos e revalidados.
- Inicialização `init` preserva bibliotecas existentes e começa vazia em novas instalações. `demo` exige dados separados do acervo real e outra porta, com seis exemplos originais, dois espaços e uma seleção. Sem processamento ou backup automático na demonstração.
- Guia conferido visualmente em 1440, 390 e 320 pixels, em temas claro e escuro, sem transbordamento. Capturas compartilháveis da documentação usam somente os exemplos originais. Evidências em `app/.runtime/qa/produto/`.
- Pacote de avaliação: 51 arquivos, 1.125.468 bytes, inventário e hashes válidos, links internos conferidos. Extraído em pasta com espaços, iniciou biblioteca vazia e demonstração na porta 8769, servindo interface e prévias. O ambiente Python foi reutilizado nesse teste; a instalação limpa das dependências foi validada separadamente pelos runners Mac e Windows.
- Pacote salvo em `growmate-marketing/produtos/repertorio/avaliacao-20261019/`, fora desta biblioteca, commit privado `5e1e213`. O empacotador exclui banco, originais, materiais de cursos e projetos de clientes por uma lista explícita de arquivos permitidos.
- Preservação conferida: 15.662 referências e 26.235 arquivos no acervo real; 36 arquivos Perestroika e 75 SOAP, com nomes, tamanhos e datas de modificação inalterados. Nenhum pedido de exclusão ou importação desses materiais foi executado.
- Preparação comercial e limites documentados em `docs/produto/COMERCIALIZACAO.md`: oferta e licença a definir, PyMuPDF com opções AGPL/comercial, e distribuição assinada do app do Mac ainda não preparada. Repositório permanece privado e o pacote é de avaliação interna.

## Produção externa e transferência em 19/10/2026

- Produções mantidas transferidas para `growmate-marketing/apresentacoes/palestra-cx-ia/`: 298 arquivos de origem inventariados, 301 arquivos preparados e conferidos no destino. HTMLs, PDFs, fontes e imagens preservados por SHA-256. Cópias da origem removidas apenas depois da conferência e do push privado da produção (`9f3ab50`).
- Biblioteca preservada: 15.662 referências, 26.235 arquivos, nenhum vínculo de arquivo apontando para `_saida/`. Apenas o cadastro real do Growmate Marketing foi acrescentado aos projetos, mantendo contextos e escolhas anteriores.
- 37 testes Python aprovados. CLI conferida em diretório temporário: preserva instruções existentes, salva pranchas no runtime respeitando `REPERTORIO_HOME` e exige destino explícito no roteiro.
- Oito aberturas no Chromium, comparando os quatro HTMLs antes/depois: 24 slides e 24 falas em cada arquivo, imagens decodificadas, sem erros JavaScript, recursos faltantes ou requisições externas. Capas da versão final idênticas em pixels. Original com cinco ou seis pixels de suavização diferentes, variação máxima de um nível por canal, sem mudança de layout.
- Pranchas existentes movidas para `app/.runtime/search-previews/`; `_saida/` retirada. Evidências desta mudança em `app/.runtime/qa/producao-externa/`, fora do Git. Nenhuma alteração visual, recompilação ou reinício do aplicativo.

## Organização do projeto em 19/10/2026

Raiz renomeada para `repertorio/`, software movido para `app/` e espaço existente renomeado para PPT Treta. Caminhos do banco atualizados com backup, sem reimportar o acervo. Preservados todos os IDs e vínculos, 15.662 referências e 26.235 arquivos; nenhum arquivo ausente. Comando `relocate` recusa serviço ativo e desfaz a transação quando o destino está incompleto. A importação reutiliza os IDs dos arquivos já cadastrados após a mudança.

Aprovados 37 testes do servidor, 34 da interface, 25 de navegador e build. Testes Python e compilação repetidos pela raiz definitiva. Aplicativo Swift compilado e instalado, inicialização do serviço pelo app conferida na nova raiz, integridade SQLite e chaves estrangeiras válidas. Mapas reais de PPT Treta e Growmate preservam contagens e conexões; miniaturas respondem HTTP 200, sem erros JavaScript. Evidências locais e backup anterior em `_saida/repertorio-qa/organizacao/`. Organização documentada em `docs/ORGANIZACAO.md`.


Executada em 17/10/2026 no computador de desenvolvimento.

## Dados reais

- 15.629 registros importados; 712 apresentações, 4.797 slides, 277 referências externas e 9.843 mídias.
- 989 referências de nível principal no mapa.
- 4.399 slides visíveis por padrão; versões comparativas e slides ocultos permanecem fora da busca.
- Nenhum caminho de arquivo ausente na importação.
- Reimportação preservou os 15.629 registros sem duplicação.

## Testes automatizados

- 14 testes Python: migração, filtros, exclusão/restauração, revisão concorrente, isolamento de contextos, snapshot de seleção, publicação explícita, entrada pendente, arquivos gerenciados, validação de caminhos, backup/restauração, retomada de tarefas e protocolo MCP com imagem.
- 2 testes de mapa: posições determinísticas sem sobreposição e integridade das conexões.
- 4 testes Playwright: explorar/excluir/restaurar; agentes paralelos e incorporação de criação; revisão de sugestão e teclado; mobile com movimento reduzido.
- Build de produção com TypeScript e Vite aprovado.

## Integrações

- CLI real do OpenCode confirmou `repertorio connected` usando configuração isolada e temporária.
- CLI real do Codex reconheceu a configuração Streamable HTTP por URL usando override temporário.
- O protocolo MCP foi exercitado por HTTP nos testes, incluindo retorno de imagem. Não foram iniciadas sessões de geração com modelos pagos.
- A configuração global dos harnesses não foi alterada. O projeto local foi cadastrado e o AGENTS.md recebeu instruções de consulta; a ativação do MCP em cada harness está documentada no manual e na aplicação.

## Medições locais

- 30 buscas HTTP no acervo completo: mediana 29,26 ms; percentil 95 de 60,93 ms.
- Mapa disponível no navegador em 1,01 segundo.
- Nenhum erro ou aviso de JavaScript nas verificações finais.
- Tela de 390 × 844 sem transbordamento horizontal.

Essas medições são do computador de desenvolvimento, não uma garantia para qualquer hardware. Relatório bruto e capturas: `_saida/repertorio-qa/`.

## Limites conhecidos

- A busca usa texto e vocabulário; não há embeddings ou modelo de IA embutido.
- HTML exige prévia fornecida pelo agente; PPTX depende de miniatura incorporada ou prévias enviadas. Vídeo depende de ffmpeg ou prévias enviadas.
- As condições de reutilização são metadados de curadoria, não certificação de licença.
- O backup contém banco e criações gerenciadas. Os originais permanecem externos e precisam acompanhar uma migração de computador.
- O validador Python emite um aviso de depreciação do adaptador de testes Starlette/httpx; os testes passam.

## Redesenho com foco no mapa

- Aplicadas as skills Impeccable (distill) e Frontend Design.
- Removidos o cabeçalho de apresentação, título e faixa de busca em largura total. Controles reunidos em uma barra flutuante de 44 px.
- Canvas em toda a janela, navegação compacta, filtros e detalhes sobrepostos, legenda interativa e prévia de referências ao passar o mouse.
- Build TypeScript/Vite, 2 testes de distribuição e 5 testes Playwright aprovados.
- As verificações de navegador incluem área do mapa, altura da barra, estabilidade ao abrir filtros, atalho de busca, limpeza dos resultados no celular e legenda acessível.
- Nenhuma mudança no backend, importação ou arquivos do acervo.
- Capturas e relatório desta revisão: `_saida/repertorio-qa/mapa-primeiro/`.

## Cores e interação do protótipo, temas claro e escuro

- Paleta dos quatro eixos e fundo #121212 recuperados de `_catalogo/mapa/index.html`.
- Linhas curvas por técnica, pistas intermediárias, seleção do eixo completo e tamanhos variados conforme força e proporção da imagem.
- Painel de operação com definições e técnicas; painel de técnica com orientação HTML e referências; curadoria preservada.
- Alternância claro/escuro no canto superior direito com preferência persistida. Tokens de cor aplicados também aos painéis, filtros, listas, diálogos e mensagens.
- 7 testes unitários e 7 testes Playwright aprovados, além do build de produção.
- No acervo real, Previsão destacou 454 referências, 14 técnicas e 647 ligações, todas na cor #B455FF. A seleção não fica limitada à primeira página de resultados.
- Captura final sem erros ou avisos JavaScript, sem miniaturas pendentes e sem transbordamento horizontal em 390 × 844.
- Evidências: `_saida/repertorio-qa/prototipo-vivo/`, incluindo capturas nos dois temas e relatório JSON.

## Busca para agentes, prancha e serviço sempre ligado

- `search_references` (MCP), `POST /api/agent/search` e `run.sh search` leem o pedido em português comum: frases conhecidas viram intenção, técnica, movimento ou estética, e `understood` mostra a leitura. "abertura com impacto" passou de slides que só tinham a palavra no título para peças de força 5 com ABRIR e IMPACTAR.
- Sem `kind`, mídias soltas ficam de fora. `per_group` evita que a mesma apresentação ocupe vários lugares (arquivo e seus slides contam juntos).
- Prancha numerada (JPEG, até 24 peças) no retorno do MCP, em `POST /api/sheet` e em `run.sh search --prancha`. Apresentações usam o primeiro slide visível em vez da miniatura pequena do mapa.
- Busca do mapa e interface sem mudança de comportamento. 17 testes Python (3 novos) e 7 testes Playwright aprovados.
- Buscas no acervo completo entre 85 e 250 ms.
- Serviço mantido pelo app nativo `~/Applications/Repertório.app` (janela própria, fixado no Dock, confere a cada 30 s) e aberto sem janela no login por `~/Library/LaunchAgents/local.repertorio.plist`. Teste: processo encerrado à força voltou em 10 s.

## Troca de tema mais rápida

- A troca claro/escuro deixou de reestilizar o mapa inteiro (cerca de 5 mil elementos, incluindo as linhas). As cores de tema são lidas na hora do estilo e só os nós de operação, pista e técnica, além da peça ativa, são recalculados; as miniaturas cobrem o fundo das referências.
- Chromium, 1440 × 900 a 2x: de 150-175 ms com uma tarefa longa de 135-160 ms para 38-52 ms sem tarefas longas. Cores conferidas por captura nos dois temas. Testes unitários e 7 testes Playwright aprovados.

## Primeira abertura mais leve

- Antes: 1.976 pedidos de imagem (cada miniatura baixava duas vezes, porque o Cytoscape e o medidor de proporção usavam modos de carregamento diferentes) e 292 MB de originais, alguns com quase 10 MB, para nós de poucos milímetros. Imagens prontas em 5,2 s.
- Agora: cópias em WebP no tamanho de exibição (`?w=128|256|512|1024|2048`, cache em `.runtime/miniaturas/`, preparadas ao iniciar o serviço) e um único pedido `/api/previews?w=128` com todas as miniaturas iniciais. 8 pedidos e cerca de 3,5 MB na abertura; mapa completo em menos de 1 s.
- Qualidade: o mapa troca cada miniatura pela menor resolução que cobre o tamanho real na tela (128, 256, 512 ou 1024 px; o maior nó no zoom máximo de 400% em tela Retina ocupa 720 px). A ficha usa 2048 px, as listas 256 a 1024 px. O botão Original continua entregando o arquivo intacto.
- 18 testes Python, 7 testes unitários e 7 testes Playwright aprovados. Conferido por captura a 1 s da abertura e com zoom de 117%.

## Ver em destaque

- No painel "Olhar de perto", a prévia ganhou "Ampliar": abre a peça em tela cheia (`web/src/Viewer.tsx`). Numa apresentação, a visão geral vem primeiro e cada slide em seguida, com a numeração original; setas, teclado (← →) e fita de miniaturas. Zoom de visualizador, sem lupa: clique simples não faz nada; rodinha do mouse aproxima 20% por clique, pinça aproxima de forma contínua, sempre no ponto do cursor; dois dedos no trackpad e arrastar movem a imagem aproximada; duplo clique alterna; botões − / porcentagem / + e teclas + − 0. Limite de 4 vezes, ou até 12 quando o original tem pixels para isso. Esc ou o X fecham e devolvem ao painel, que continua aberto e com o foco na prévia.
- Mostra a versão de 2048 px na hora e troca pelo original quando ele chega. Slides do curso têm prévias de 800 px, então aproximar muito neles perde nitidez; referências externas mantêm o detalhe.
- 8 testes Playwright aprovados (1 novo), além de capturas com a apresentação "Cérebro".

## Mapa fluido no zoom

- Antes, cada passo de zoom recalculava o estilo dos cerca de 5 mil elementos para manter linhas e nomes com espessura constante: 7 quadros por segundo e 22 s travados em 60 movimentos de rodinha (Chromium, tela 2x).
- Agora a espessura é lida na hora do estilo e só linhas e nomes são recalculados, uma vez, quando o zoom para e mudou mais de 15%. Mesmo teste: 44 a 48 quadros por segundo e cerca de 0,2 s travados. Arrastar continua a 56 quadros por segundo.

## Escolhas

- Nova tela **Escolhas** (`web/src/Choices.tsx`): cada pedido com as seleções que o agente guardou, a justificativa e as referências em cartões. O usuário aprova, corta e comenta; clicar na imagem abre o painel de detalhes. Contador de itens sem resposta na navegação e link direto `/?escolha=ID`.
- Servidor: tabela `pack_reviews` (migração 0003, só acrescenta), `GET /api/demands`, `GET /api/packs/{id}` com a imagem atual e a revisão de cada referência, `POST /api/packs/{id}/reviews`. `build_inspiration_pack` devolve `review_url`; nova ferramenta MCP `get_pack` para o agente ler a revisão antes de criar.
- 20 testes Python (1 novo) e 9 testes Playwright (1 novo) aprovados. Conferido por captura nos temas escuro e claro, numa cópia temporária do banco para não criar pedidos de exemplo no acervo.

## Localizar os carrosséis Growmate no grafo

- Diagnóstico em 17/10/2026: os 32 carrosséis e a ficha de componentes já estavam em `/api/graph`, com miniaturas, mas a câmera mantinha a visão geral. Mesmo após buscar, as 33 capas ocupavam só 209 × 151 px no mapa de 1440 × 1000 px.
- A busca agora enquadra as referências encontradas na área livre à esquerda do painel. O enquadramento acontece quando o conjunto muda; digitar no campo ou explorar o mapa manualmente não dispara uma nova centralização. O restante do acervo permanece no mapa, escurecido como antes.
- Links com `q` abrem uma busca pronta e preservam a consulta ao recarregar ou navegar pelo histórico. `/?q=Growmate` isola os 33 registros; `Growmate #Livros` também encontra referências que só mencionam livros, pois a busca existente usa OR entre palavras.
- Conferido no acervo real: 33 referências iluminadas e com miniaturas carregadas, zoom de 69% e conjunto ocupando 796 × 576 px, inteiro antes do painel lateral. Sem erros JavaScript.
- Build de produção, 7 testes unitários e 10 testes Playwright aprovados. O novo teste cobre link de busca, enquadramento após uma câmera salva fora da área visível, histórico, recarga, limpeza e exploração manual. Testes de navegador usam biblioteca temporária, sem criar referências de demonstração no acervo real.
- Capturas antes e depois e relatório: `_saida/repertorio-qa/growmate-grafo/`. A interface local já foi compilada; o app aberto carrega a nova versão com ⌘R.

## Catálogo curado de Skills

- Em 18/10/2026, **Skills** substituiu **Entradas** na navegação. Os sete cartões autorizados pelo usuário são Impeccable, Frontend Design, Landing Page Design, ImageGen, Presentations, HyperFrames e HyperFrames Creative. A lista explícita fica em `web/src/skillCatalog.ts`; nenhuma instalação é descoberta ou incluída automaticamente.
- Busca por objetivo tolerante a acentos, filtros por categoria, descrição e indicação de quando usar. **Montar pedido** permite editar a demanda e copiar uma solicitação com o nome da skill, o nome e o ID do espaço aberto e a revisão das referências em Escolhas. A execução ocorre quando o usuário cola o pedido na conversa com seu agente. Falha da área de transferência oferece seleção para cópia manual.
- Catálogo global, disponível sem espaço aberto. Nesse caso o pedido instrui o agente a perguntar qual espaço consultar. Trocar de espaço mantém a tela Skills e atualiza os próximos pedidos. Link `/?view=skills`, recarga e histórico preservam a navegação. O grafo não é carregado ao abrir diretamente o catálogo.
- Sugestões espontâneas foram movidas para **Escolhas > Sugestões para o acervo**, visível quando há pendências. Contagem na navegação inclui seleções sem resposta e sugestões; publicação e descarte permanecem restritos ao espaço. Links de revisão e restauração de referências da lixeira continuam funcionando.
- Build de produção, 11 testes unitários e 16 testes Playwright aprovados. Cobertura inclui somente os sete cartões, busca, categoria, pedido editável, cópia real, espaço correto, troca de espaço, acesso global, recarga, histórico, retorno de foco, celular sem transbordamento e publicação de sugestões em Escolhas. Testes usaram biblioteca temporária na porta 8767.
- Catálogo e pedido conferidos visualmente em desktop escuro e celular claro. Capturas locais em `/tmp/repertorio-skills-qa/`. Atualizar a interface do app aberto com ⌘R; serviço nativo e banco não exigem reinício ou migração.

## Três visualizações do grafo

- Em 18/10/2026, incluído **Visualização do grafo** ao lado da troca de tema. Menu com prévias e opções **Mapa livre**, **Por grupos** e **Hierárquico**, sem reduzir a área do canvas. Mapa livre preserva o arranjo anterior.
- A troca reposiciona o mesmo objeto Cytoscape e conserva miniaturas, seleção, busca, filtros e ficha aberta. Organização salva em `repertorio-graph-view`; câmeras por espaço e modo, preservando a chave anterior do mapa original. Novas organizações também funcionam em espaços vazios e sem técnicas reconhecidas.
- Grupos usam a operação com mais relações de cada referência; todas as conexões permanecem. Relações cruzadas ficam mais discretas na visão geral e voltam a ser realçadas na seleção. Hierarquia segue operações, pistas, técnicas e referências, com miniaturas em blocos de várias colunas e técnicas vazias compactadas para evitar uma coluna excessivamente alta.
- Build de produção, 18 testes unitários e 19 testes Playwright aprovados. Cobertura de estabilidade e espaçamento nos três modos, integridade das conexões, classificação mista e desconhecida, biblioteca com 1.021 referências, manutenção da instância e das imagens, preservação de seleção/busca/filtros, câmeras independentes, persistência, espaços vazios, teclado, tema claro, movimento reduzido e telas de 390 e 320 px. Os testes de escrita continuam isolados na biblioteca temporária da porta 8767.
- Conferência visual no acervo real: Growmate conserva 33 referências, 48 técnicas e 292 conexões; PP Treta conserva 1.021 referências no mapa, 48 técnicas e 4.182 conexões em todos os modos. Todas as miniaturas carregadas; nenhum erro JavaScript. Hierarquia ajustada após a primeira inspeção para ocupar uma área equilibrada; contador afastado dos novos controles.
- Capturas de desktop escuro e celular claro, seis vistas dos espaços reais e medições em `_saida/repertorio-qa/grafos/`. A interface está compilada; atualizar o app com ⌘R. Mudança restrita à interface, sem migração, reinício do serviço ou alteração da curadoria.

## Seis linguagens visuais adicionais do grafo

- Em 18/10/2026, acrescentadas **Cosmos**, **Metrô**, **Circuito**, **Jardim**, **Editorial** e **Prisma**, totalizando nove opções. Cada uma combina uma organização própria com cores, formas, conexões, tipografia e fundo, incluindo variantes clara e escura. As três opções anteriores continuam disponíveis.
- Cosmos organiza círculos em órbitas; Metrô cria linhas e estações; Circuito usa chips e trilhas ortogonais verdes; Jardim combina copas elípticas, folhas e ramos; Editorial usa colunas, índices verticais e serifas sobre papel; Prisma organiza losangos numa malha isométrica com hexágonos coloridos. Mídias e dados de curadoria permanecem intactos.
- Menu com uma única coluna em todas as telas, rolagem quando necessário, nove prévias próprias e foco visível na opção atual. Teclado alcança a última opção, Tab segue para a interface e a escolha persiste após recarregar. Ajuste para coluna única recompilado e conferido visualmente no desktop escuro e celular claro; os cinco testes de navegador de `graph-views` e `graph-styles` passaram.
- Paletas acompanham o tema, a legenda e o painel do eixo. Referências usam a cor da operação predominante nas seis novas propostas; todas as relações continuam presentes. Prisma escolhe tinta de contraste adequado e conserva títulos legíveis no afastamento. Rótulos radiais, inclinados e laterais evitam sobreposição com miniaturas. Ao selecionar um eixo ou técnica no desktop, as novas vistas enquadram os nós realçados na área disponível ao lado do painel.
- Implementação em `web/src/graphSkins.ts`, `alternateLayouts.ts`, `GraphPreview.tsx` e integração no mapa existente. A instância e as imagens permanecem durante a troca; voltar ao Mapa livre restaura o fundo, as cores e as formas originais. Preferência e câmeras continuam separadas por organização e espaço.
- Build, 31 testes unitários e 21 testes Playwright aprovados. Cobertura ampliada para geometria e integridade dos nove modos, seis paletas e formatos nos dois temas, legenda coerente, seleção e imagens preservadas, restauração do original, títulos legíveis com zoom de 9%, enquadramento com painel e acesso às nove opções no celular de 320 px. Testes com escrita continuam isolados na porta 8767.
- Acervo real conferido em 24 combinações: seis propostas, dois temas e dois espaços. Growmate conserva 33 referências e 292 conexões; PP Treta conserva 1.021 referências no mapa e 4.182 conexões. Todas as miniaturas carregadas, sem erros JavaScript. Seis capturas adicionais conferem operações selecionadas e duas registram o menu.
- Evidências, medições e capturas em `_saida/repertorio-qa/estilos-grafo/`. Atualizar a interface com ⌘R. Sem migração de dados ou reinício do serviço nativo.

## Reordenação das visualizações por arraste

- Em 18/10/2026, menu com ordem personalizada por arraste do card no mouse ou pela alça no toque. Card suspenso e espaço reservado acompanham o gesto; as bordas rolam a lista automaticamente. Soltar mantém o card visível na nova posição. Reordenar preserva o grafo e a ficha; clique continua trocando a visualização. Escape e soltura fora do menu cancelam. Alt + ↑/↓ permite reordenar pelo teclado, com foco e anúncio de posição.
- A ordem é global neste navegador, persiste entre visitas e espaços em `repertorio-graph-view-order` e aceita opções futuras sem apagar preferências válidas. Preferências inválidas ou duplicadas não removem visualizações do catálogo. A curadoria e os arquivos do acervo não mudam.
- Build, 34 testes unitários e oito testes de navegador das visualizações aprovados. Casos novos cobrem arraste real, persistência após recarga e troca de espaço, clique após arraste, cancelamento, teclado, toque com rolagem normal e automática, manutenção da seleção e visibilidade do card após soltar no fim. Conferidas capturas no desktop escuro e no celular nos dois temas. Evidências em `_saida/repertorio-qa/ordem-grafos/`. Testes com escrita usam biblioteca temporária na porta 8767. Interface compilada; atualizar com ⌘R.

## Revisão de desempenho sem mudança visual

- Em 18/10/2026, grafo e busca passaram a resolver vínculos e disponibilidade dos pais em lote. Na cópia do acervo real, a construção do grafo PP Treta caiu de 227,37 para 111,67 ms e de 1.024 para quatro consultas SQL. A página de busca caiu de 179 para cinco consultas; nela, o ganho de tempo foi menor. Respostas completas idênticas, incluindo escopo, revisão e estado dos vínculos.
- O viewport agrupa atualizações por quadro e reutiliza coleções de nós. Na simulação com 480 eventos por amostra, a câmera passou de 480 gravações durante o movimento para uma gravação final, preservando a posição em recarga imediata, saída da página e troca de visualização. Capturas do mapa antes e depois com pixels idênticos.
- Build, 34 testes Python, 34 testes unitários da interface e 25 testes Playwright aprovados. Medições, limites e arquivos envolvidos em `docs/REPERTORIO-DESEMPENHO.md`; scripts, amostras e capturas em `_saida/repertorio-qa/performance/`. Acervo real preservado; testes com escrita em biblioteca temporária. Instruções AGENTS, Claude e Gemini atualizadas.
