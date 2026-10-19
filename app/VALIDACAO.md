# Validação da primeira versão

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
