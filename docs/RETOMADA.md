# Retomada do projeto

## Pendências dos métodos resolvidas em 23/10/2026

A pedido do Cleiton, depois do ajuste da busca: (1) `biblioteca/processo.md`, `LEIA-PRIMEIRO.md` e o manual mandam escolher referências pelo MCP; `buscar.py` e `roteiro.py` ficaram só para consulta offline e vocabulário. (2) O bloco do Repertório no `AGENTS.md` do Growmate Marketing foi regravado com `connect --write-instructions` e cita os dois métodos (o arquivo não é versionado lá). (3) Regra para dado público lembrado pelo agente no guia `provar-com-dados` e no `pitch-e-proposta`. (4) `get_reference` resume slides e parecidos em uma linha (a lista de parecidos era 80% da resposta). (5) `get_guide` diz de qual espaço é cada referência e, com `context_id` ou `workspace_ids`, marca as dos espaços não escolhidos. (6) Os 7 slides do template de gráficos do SOAP com texto sobreposto foram para a lixeira do espaço e saíram da importação (`SOAP_SKIP` em `ferramentas/incorporar_colecao.py`); o PowerPoint seguiu falhando com erro -50 nesse arquivo. Espaço SOAP: 75 apresentações e 500 slides.

Continua pendente, decisão do Cleiton: os 4.797 slides de Referências não têm `como funciona` nem `serve para` próprios (herdam a ideia da apresentação). Próxima ação: usar as skills de pitch e de fala numa demanda real da Growmate.

## Ícone do Mac em 23/10/2026

A pedido do Cleiton, o olho psicodélico foi substituído pelo R branco em três fragmentos sobre fundo preto, escolhido na versão pequena do canto inferior direito da segunda proposta. Fonte em `app/mac/icone.png` (1024 × 1024, com transparência externa), conceito e prompt em `app/mac/ICONE.md`; o gerador antigo `icone.py` foi removido. `build.sh` mantém os dez tamanhos do macOS. O app foi compilado, instalado em `~/Applications/Repertório.app` e reaberto; assinatura e ícone lido pelo macOS conferidos, serviço respondendo normalmente. Cópia do app anterior e evidências em `app/.runtime/qa/icone-mac-20261023/`. O usuário foi avisado sobre a possível nova permissão de Documentos. Alterações de outras tarefas foram preservadas.

## Busca dos agentes em 23/10/2026

A pedido do Cleiton, a busca dos agentes (`search_references`, `run.sh search`) foi ajustada para pedidos descritivos, com medição antes e depois. Três mudanças: (1) o texto de busca de cada ficha passou a incluir o "como funciona" e o "serve para" (migração `0005`, aplicada ao reiniciar o serviço); (2) palavra solta e comum do vocabulário ("tela", "ligação", "abertura") vale pouco como item e também é buscada no texto; (3) a pontuação conta quantas partes do pedido a ficha atende, e a força da ficha só desempata. Pesos em `app/server/repertorio/agent.py` (`COVER_WEIGHT` e vizinhos). O mapa do app não usa essa busca e não mudou.

Medição: 35 pedidos reais (testes às cegas da Perestroika e do SOAP, buscas registradas de carrosséis e pedidos que já funcionavam), 1.062 resultados com nota dada por agentes sem ver a posição. nDCG@8 (1 = os melhores itens no topo) foi de 0,38 para 0,52; o item certo entre os 3 primeiros, de 18 para 25 pedidos; entre os 8, de 21 para 27. Pioraram "próximos passos com pedido de decisão" (a apresentação inteira passa à frente do seu slide de próximos passos) e "ponto fraco e o plano contra ele" (não há slide exato no acervo). Não ajudaram e ficaram de fora: penalizar a apresentação inteira e cortar terminações das palavras. Pedidos longos levam cerca de 0,45 s em vez de 0,3 s. Para mexer de novo: `ferramentas/medir_busca.py` (`candidatos` para dar nota ao que aparecer de novo, `medir --comparar`). Backup antes: `repertorio-2026-10-23-070656`.

## Aba Repositórios em 23/10/2026

A pedido do Cleiton, a barra lateral do app ganhou **Repositórios**, logo abaixo de Skills (`?view=repos`). Cartões no formato das skills, com o link do GitHub, para ferramentas usadas junto com o Repertório: Engram (memória dos agentes), RTK (economia de contexto no terminal) e HyperFrames (vídeos do kit de motion). Curadoria em `app/web/src/repoCatalog.ts`; repositório que traz só uma skill fica no catálogo de Skills. Na sequência, a pedido do Cleiton, HyperFrames e HyperFrames Creative saíram da aba Skills (e com eles a categoria Vídeo), porque o HyperFrames é mais que uma skill e já está em Repositórios; as duas skills continuam instaladas e os agentes seguem usando nos vídeos. Em celulares de até 360 px os ícones da barra ficam um pouco mais estreitos para caber com Sugestões. Testes: 63 da interface e 32 de navegador aprovados; interface compilada, atualizar com ⌘R.

## SOAP acionável para modelos em 23/10/2026

A pedido do Cleiton, o material de `soap/` (55 e-books e guias, 3 checklists e 17 templates de PowerPoint, 1.755 páginas) foi lido página por página e virou três portas para os agentes, como a Perestroika. (1) Método: 62 fichas e modelos em `biblioteca/metodos/soap/`, servidos por `get_guide`: índice `metodo-soap`, guias `apresentar-ao-vivo`, `pitch-e-proposta`, `comunicacao-na-empresa` e fichas como `soap/<ficha>`; o checklist SOAP é camada extra do guia `revisao-apresentacao`. (2) Skills `soap-fala` (Apresentar ao vivo) e `soap-pitch` (Pitch e proposta) em `~/.agents/skills/` (ligadas em `~/.claude/skills`), no catálogo de Skills do app; a `perestroika-revisao` passou a usar o checklist SOAP. (3) Espaço SOAP no app (`7f53adaa-6bc5-496c-815e-f6159e2baec9`): 75 apresentações e 507 slides, `reusable=false`. Plano, resultado e pendências em `docs/SOAP-PLANO.md`; manutenção em `biblioteca/metodos/soap/LEIA-ME.md`.

Novos: `ferramentas/incorporar_colecao.py` (Perestroika e SOAP; `incorporar_perestroika.py` virou atalho) e `ferramentas/mcp_leitura.py` (MCP só leitura, para testes). Testes: 48 do servidor, 61 da interface e 29 de navegador aprovados; interface compilada (atualizar com ⌘R); serviço reiniciado. Backup antes da importação no iCloud (`repertorio-2026-10-23-013219`). Dois testes às cegas (pitch para investidores e institucional com revisão) guiaram as correções; materiais em `app/.runtime/qa/soap/testes/materiais-do-teste.html`. Próxima ação: o Cleiton usar `soap-pitch` e `soap-fala` numa demanda real.

## Skills do Emil Kowalski em 23/10/2026

A pedido do Cleiton, as 15 skills de `github.com/emilkowalski/skills` (MIT, commit `2d22863`) foram instaladas com `npx skills add emilkowalski/skills -g` para Claude Code (`~/.claude/skills`) e Codex (`~/.agents/skills`); atualizar com `npx skills update`. No catálogo do app entraram 5 em Design, 7 na nova categoria Animação (movimento de sites e apps, diferente de Vídeo) e 3 na nova categoria Código, somando 25 skills. `prototype`, `review-animations` e `pick-ui-library` só rodam quando chamadas pelo comando: o pedido montado no app começa com `/<skill>` (campo `manual` em `skillCatalog.ts`). Testes da interface (61) e de navegador da aba Skills (2) aprovados; interface compilada, atualizar com ⌘R.

Na mesma data entrou `design-taste-frontend`, de `github.com/Leonxlnx/taste-skill` (MIT, commit `6010f91`), como "Direção de arte para sites" em Design: 26 skills no catálogo. Ela roda programas próprios (Node 22+ e Chrome em segundo plano) e busca fotos livres em acervos públicos; guarda histórico em `~/.taste-skill/`. O instalador gravou o atalho do Claude Code quebrado por causa de `~/.claude-accounts/cvortex/skills`; o atalho foi refeito como `../../.agents/skills/design-taste-frontend`. Confira isso em instalações futuras com `npx skills`. A skill recomenda meia-risca em intervalos; a regra do projeto (sem travessão nem meia-risca) prevalece.

## Inspiração sem carrosséis Growmate em 22/10/2026

A pedido do Cleiton, os carrosséis e o kit da Growmate saíram do espaço Inspiração: as 33 criações foram para a lixeira de Inspiração (recuperáveis pela lixeira do espaço) e seguem publicadas no espaço Growmate. Inspiração ficou só com as 277 referências externas. Nada saiu do acervo nem de Growmate; cópia do banco antes da alteração. `ferramentas/incorporar_growmate_livros.py` agora usa só Growmate. Detalhes em `app/VALIDACAO.md`.

## Nome antigo do acervo removido em 22/10/2026

O espaço Referências tem o ID `referencias` e a origem das apresentações se chama `acervo`. Não reintroduza o nome antigo em textos, código ou dados. Detalhes em `app/VALIDACAO.md`.

## Perestroika acionável para modelos em 23/10/2026

A pedido do Cleiton, o material de `perestroika/` (24 PDFs, cerca de 760 páginas, e um vídeo) foi lido página por página e virou três portas para os agentes. (1) Método: 53 fichas e modelos em `biblioteca/metodos/perestroika/` (Experience Learning, Chora PPT, Mapa do Storytelling, checklist, educação corporativa), servidos por `get_guide`: índice `metodo-perestroika`, guias `aula-e-workshop`, `curso-e-programa`, `encontro-e-evento`, `revisao-apresentacao` e fichas como `perestroika/<ficha>`. (2) Skills `perestroika-tese`, `perestroika-experiencia` e `perestroika-revisao` em `~/.agents/skills/` (ligadas em `~/.claude/skills`), também no catálogo de Skills do app, categoria Método. (3) Espaço Perestroika no app: 23 apresentações, 191 slides fichados e o vídeo do Chora PPT, com `reusable=false`. Plano e decisões em `docs/PERESTROIKA-PLANO.md`; manutenção em `biblioteca/metodos/perestroika/LEIA-ME.md`.

Novos no app: `import-decks` (PDF como apresentação com slides) e `get_guide` lendo `biblioteca/metodos/`. Testes: 47 do servidor, 60 da interface e 29 de navegador aprovados; interface compilada (atualizar com ⌘R); serviço reiniciado com o código novo. Dois testes às cegas (workshop de 3 horas e palestra de 15 minutos) guiaram as correções: exemplos variados, ficha de processamento, modelo de instrumento do dia seguinte, tabela das 8 cartas com os guias. Backup antes da importação no iCloud (`repertorio-2026-10-22-235524`). Próxima ação: o Cleiton usar as skills numa demanda real; melhorias da busca apontadas pelos testes estão no plano, em Pendências.

## Espaço Inspiração em 22/10/2026

Referências guarda só apresentações e material do acervo. Referências externas e criações (carrosséis Growmate) estão em **Inspiração**; as criações seguem também em Growmate. Para slides e carrosséis, consulte Referências e Inspiração juntos. Detalhes em `app/VALIDACAO.md`.

## Sem Escolhas e momentos da história revistos em 22/10/2026

A tela Escolhas saiu: o agente diz na conversa quais referências vai usar e por quê, com o link de cada ficha (`url`, já com o espaço). Sugestões espontâneas ficam em **Sugestões**, visível só com pendências. Na organização História, Fechar virou papel dentro de Marcar, porque quase nenhuma peça tem fechamento como papel principal; são cinco momentos. Detalhes em `app/VALIDACAO.md`.

## Imagens com tela grande, capas maiores e organização por formato em 22/10/2026

As melhorias feitas para os vídeos valem também para as imagens: clicar em qualquer referência abre a tela grande com a ficha ao lado e troca lateral; capas com o dobro do tamanho em todos os espaços; legenda com **História / Recurso visual / Formato** em cada espaço: história (seis momentos da apresentação com seus papéis) é o padrão das imagens, recurso visual reúne as 48 técnicas em sete famílias e formato segue como padrão dos vídeos. Os quatro eixos do olhar saíram da tela; o vocabulário dos agentes continua o mesmo. Guias por papel na história para slides e carrosséis em `biblioteca/guias/`, lidos pelo agente com `get_guide`. Detalhes em `app/VALIDACAO.md`. Interface compilada; atualizar com ⌘R.

## Vídeos de motion no espaço Motion em 22/10/2026

A pedido do Cleiton, o Repertório passou a conectar vídeos. Novo espaço **Motion** com toda a galeria do Prompt Motion (prompt-motion.com): 234 vídeos feitos com Claude e os 2 modelos de prompt reescritos pelo site. Cada vídeo é uma referência externa ligada às mesmas técnicas, intenções e movimentos do mapa, com prompt original, decupagem em português, ferramenta usada, créditos e prancha de oito quadros. O agente encontra pelo MCP (`format="mp4"` filtra vídeos) e vê o movimento pela prancha. Mídia de terceiros: só referência.

O mapa do Motion se organiza por formato de tela (Horizontal 16:9, Vertical 9:16, Quadrado e 4:5, Prompts-modelo) e tipo de vídeo, no lugar dos eixos do olhar; tipos em `dados/motion/generos.json`. No app, as capas tocam o vídeo ao aproximar o mapa (até 12 por vez), o mouse mostra o loop e a lista toca os cartões visíveis. Clicar num vídeo abre o player em tela grande com os modos do YouTube (padrão, teatro e tela cheia) e atalhos de teclado; a ficha lateral continua em **Ficha completa**, com prompt e **Ver quadros**. Capas de vídeo e prévia do mouse com o dobro do tamanho, a pedido; espaços só com imagens mantêm as mesmas posições. Corrigido também um defeito anterior da lista que sobrepunha cartões em todos os espaços. Interface compilada; atualizar com ⌘R. Serviço reiniciado com o código novo. App nativo não recompilado.

Para criar vídeos: guias por tipo em `biblioteca/motion/guias/` (MCP `get_guide`) e kit de movimentos do HyperFrames em `kit/motion/`, com projeto inicial testado. Vídeos criados e incorporados ganham player, loop, quadros, formato, tipo e prompt. Rotina e manutenção: `ferramentas/incorporar_prompt_motion.py` (coletar, baixar, quadros, lotes, montar) e `./app/run.sh import-motion --workspace ID`. Vídeos em `_originais/prompt-motion/` (2,5 GB, fora do Git e do backup); fichas em `dados/motion/`. Validação e medições em `app/VALIDACAO.md`. Próxima ação: o Cleiton explorar o espaço Motion e pedir criações usando-o como inspiração; novas galerias de vídeo podem seguir o mesmo formato de ficha.

## Preparação do produto para apresentação e venda em 19/10/2026

O Cleiton quer comercializar o Repertório e que novos usuários entendam sua função. Modelo confirmado: uso local no navegador em Mac e Windows, com aplicativo opcional no Mac acessando a mesma biblioteca. A frase principal é “Suas referências, prontas para orientar a criação.” Definição, instalação, demonstração, operação e preparação comercial em `docs/produto/`. README e LEIA-ME passam a explicar o produto antes dos detalhes técnicos.

Novo guia dentro do app: `/?view=guide`, acessível pelo botão “Conheça o Repertório” no cabeçalho. Mostra o fluxo, o papel de cada parte, exemplo de pedido e ações reais para explorar, copiar, abrir Skills e conectar um agente. Mantidos o mapa, as nove visualizações e os contratos de performance. Interface compilada; atualizar com ⌘R. O app nativo instalado não foi recompilado nem substituído.

Instalação nova usa `init`: biblioteca vazia e vocabulário próprio, sem importar o acervo de desenvolvimento. Windows tem `setup.ps1`, `run.ps1` e iniciador CMD; bloqueio do serviço, backup e restauração usam mecanismos compatíveis. Dependências resolvidas para os dois sistemas. Corrigido o fechamento explícito de conexões SQLite após o teste Windows revelar arquivos abertos no backup.

A demonstração `demo --home app/.demo --serve`, na porta 8768, tem dois espaços fictícios, seis referências originais e uma seleção para revisão, sem consultar os dados reais nem executar backup automático. O empacotador `ferramentas/empacotar_produto.py` usa lista explícita de arquivos e inventário com hashes. O candidato de avaliação fica em `growmate-marketing/produtos/repertorio/avaliacao-20261019/`; não contém acervo particular, materiais de cursos ou projetos de clientes.

Perestroika e SOAP permanecem aqui a pedido do usuário para documentação em sessões futuras. Os 111 arquivos foram preservados; não apagar essas pastas nem incluí-las no pacote. Acervo real preservado, com 15.662 referências e 26.235 arquivos. Gateways anteriores continuam fora dos commits desta tarefa.

Verificações locais: 43 testes Python, 34 testes da interface e 27 de navegador aprovados; os três testes do guia e da revisão passaram novamente após o ajuste final de texto. Capturas em desktop e celular, nos dois temas, sem transbordamento até 320 px. Pacote extraído em pasta com espaços, inicialização limpa e demonstração servindo interface e prévias aprovadas. Evidências em `app/.runtime/qa/produto/`. Execução remota aprovada em Mac e Windows: 43 testes do servidor em cada sistema e preparo da instalação pelos iniciadores de shell e PowerShell. Evidência: https://github.com/cleitoncampano/repertorio/actions/runs/39272717798, código `56105e0`. Pacote de avaliação com 51 arquivos e 1.125.468 bytes, registrado no marketing em `5e1e213`.

Pendências de distribuição comercial: definir oferta, suporte e licenciamento. PyMuPDF informa opções AGPL e comercial; a escolha não foi feita. O aplicativo do Mac ainda usa build local, sem instalador comercial assinado e notarizado. O pacote é de avaliação interna. Próxima ação: abrir o guia, apresentar a demonstração e definir a oferta e o conteúdo autorizado que acompanhará a venda.

## Acervo e produção separados em 19/10/2026

A pedido do Cleiton, as duas apresentações mantidas foram transferidas para `/Users/cleiton/Documents/Desenvolvimento/growmate/growmate-marketing/apresentacoes/palestra-cx-ia/`. Organização: `original/`, `final/`, `ferramentas/`, `historico/`, `project.md` e inventário `TRANSFERENCIA.json`. Foram inventariados 298 arquivos de origem e conferidos os 301 arquivos preparados no destino, incluindo as imagens e evidências locais que estavam fora do Git. HTMLs, PDFs, fontes e imagens preservados por SHA-256. As variantes excluídas pelo usuário não foram restauradas. Produção salva no GitHub privado do marketing, commit `9f3ab50`, usando checkout isolado para preservar alterações locais e a fila do agendador.

O projeto Growmate Marketing está conectado ao MCP como `growmate-marketing-15e1a6`, com as instruções anteriores preservadas. As 15.662 referências, os 26.235 arquivos do acervo e os contextos antigos permanecem no Repertório. A pasta `_saida/` foi retirada; as 24 prévias de busca foram levadas para `app/.runtime/search-previews/`. Novas evidências do aplicativo ficam em `app/.runtime/qa/` ou em pasta temporária. O roteiro exige `--saida` explícita no projeto de destino. Instruções e manuais atualizados para produzir fora desta biblioteca.

Validação: 37 testes Python aprovados, fluxo da CLI conferido em diretório temporário, oito aberturas dos quatro HTMLs antes/depois sem erros, com 24 slides e 24 falas por arquivo. Capas da versão final idênticas em pixels; capas da original diferem apenas em até seis pixels de suavização, um nível por canal. Evidências em `app/.runtime/qa/producao-externa/`. Próxima ação: abrir o Growmate Marketing para criar; consultar o Repertório pelo MCP e incorporar resultados apenas quando solicitado. Não restaurar `_saida/` nem mover as pastas preexistentes dos gateways nesta tarefa.

## Projeto reorganizado como Repertório em 19/10/2026

Raiz canônica: `/Users/cleiton/Documents/Desenvolvimento/repertorio`. O software saiu da subpasta `repertorio/` para `app/`. Referências é um espaço do acervo, com o mesmo ID `referencias`; Growmate continua independente. O projeto mantém o ID `repert-rio-87e17c`. Links locais ocultos preservam os caminhos antigos, sem duplicar pastas ou arquivos.

Banco atualizado em transação, sem reimportação: 15.662 referências, 26.235 arquivos, IDs, vínculos, contextos e escolhas preservados. Todos os arquivos encontrados. Backup anterior e evidências em `_saida/repertorio-qa/organizacao/`. App do Mac recompilado, instalado e conferido: inicia o serviço pela nova raiz. Documentação e operação em `docs/ORGANIZACAO.md`.

Validação: 37 testes Python, 34 testes unitários da interface, 25 testes de navegador e build aprovados. Dois espaços reais conferidos visualmente, 1.021 referências e 4.182 conexões em Referências, 33 referências e 292 conexões em Growmate; miniaturas e downloads disponíveis, sem erros JavaScript. Próxima ação: abrir a nova pasta no editor e seguir usando o Repertório. Preservar as alterações anteriores da palestra e dos gateways.

## Firefly autônomo e anúncio atualizado em 18/10/2026

Imagem do anúncio no celular do slide 15 gerada e baixada no Adobe Firefly, sem clique do usuário. HTML editável, HTML offline e PDF atualizados em `/Users/cleiton/Documents/Desenvolvimento/growmate/growmate-marketing/apresentacoes/palestra-cx-ia/final/`; recorte e página 15 conferidos. As duas versões HTML produziram capturas idênticas, sem erros. Controle reutilizável em `ferramentas/firefly.py`, operação e correção do foco preso em `docs/FIREFLY.md`. Prompt e procedência salvos na entrega. Próxima ação: usar esse controle para novas imagens quando o usuário pedir.

## Revisão de desempenho concluída em 18/10/2026

Visual e comportamento preservados. Grafo e busca resolvem vínculos em lote; o grafo de Referências passou de 1.024 para quatro consultas e de 227,37 para 111,67 ms na comparação pareada da cópia do acervo. A câmera é atualizada por quadro e gravada após o gesto, com salvamento imediato ao sair, trocar de modo ou desmontar o mapa. Simulação de 480 eventos passou de 480 gravações para uma; capturas antes e depois com pixels idênticos. O ganho de tempo na busca foi menor.

Build, 34 testes Python, 34 testes unitários da interface e 25 testes de navegador aprovados. Respostas completas do servidor idênticas. Detalhes e limites em `docs/REPERTORIO-DESEMPENHO.md`; evidências em `_saida/repertorio-qa/performance/`. AGENTS.md, CLAUDE.md e GEMINI.md atualizados. Servidor atualizado ativado e conferido nos dois espaços reais. Interface compilada, atualizar com ⌘R. Próxima ação: experimentar a fluidez do mapa; uma revisão futura da busca deve medir os planos SQL. Preservar as alterações anteriores da palestra e do checkpoint.

## Visualizações reordenáveis em 18/10/2026

Arraste os cards do menu para personalizar a ordem. Mouse arrasta o card; no celular, a alça permite arrastar e o restante permite rolar. Prévia suspensa, espaço de destino, rolagem automática nas bordas, cancelamento por Escape e alternativa por Alt + ↑/↓. A ordem fica salva no navegador e vale em todos os espaços. Reordenar mantém o grafo aberto; clique continua trocando a visualização.

Build, 34 testes unitários e oito testes de navegador das visualizações aprovados. Conferidas capturas no desktop escuro e celular nos dois temas. Evidências em `_saida/repertorio-qa/ordem-grafos/`; detalhes em `app/VALIDACAO.md`. Interface compilada, atualizar com ⌘R; sem mudanças no banco ou no serviço. Próxima ação: experimentar a ordem dos templates. Preservar as alterações anteriores da palestra e do checkpoint.

## Nove propostas visuais de grafo disponíveis em 18/10/2026

Acrescentadas Cosmos, Metrô, Circuito, Jardim, Editorial e Prisma às três opções existentes. As seis novas têm geometria, paleta, formas, linhas e fundo próprios, com versões clara e escura. Menu com nove prévias em uma única coluna em todas as telas, com rolagem quando necessário. Paletas acompanham legenda e painel; selecionar eixo ou técnica enquadra as novas vistas ao lado da ficha. Preferência, busca, filtros, imagens e câmeras continuam preservados.

Build, 31 testes unitários e 21 de navegador aprovados. Conferidas 24 combinações dos espaços reais Growmate e Referências nos dois temas, todas as miniaturas e contagens preservadas, sem erros JavaScript. Ajustados rótulos, contraste, títulos no afastamento e enquadramento com o painel aberto. Evidências em `_saida/repertorio-qa/estilos-grafo/`; detalhes em `app/VALIDACAO.md`. Interface compilada, atualizar com ⌘R; sem mudanças no banco ou no serviço. Próxima ação: o usuário experimentar as nove propostas. Preservar as alterações anteriores da palestra e do checkpoint.

## Três visualizações do grafo implementadas em 18/10/2026

Novo botão Visualização do grafo, ao lado do tema, com prévias de Mapa livre (arranjo original), Por grupos e Hierárquico. Mudar o modo reposiciona a mesma instância e preserva imagens, seleção, busca, filtros e ficha. Preferência global no navegador, câmeras independentes por espaço e modo. Novos controles também funcionam no celular; voltar ao Mapa livre pelo mesmo menu.

Build, 18 testes unitários e 19 de navegador aprovados. Conferidos os três modos nos espaços reais Growmate (33 referências, 292 conexões) e Referências (1.021 referências no mapa, 4.182 conexões), sem erros JavaScript. Evidências em `_saida/repertorio-qa/grafos/`; detalhes em `app/VALIDACAO.md`. A hierarquia foi equilibrada após inspeção do acervo real. Interface compilada, atualizar com ⌘R; sem mudanças no banco ou no serviço. Próxima ação: o usuário experimentar as organizações e indicar os ajustes que desejar. Preservar as alterações anteriores da palestra.

## Catálogo de Skills implementado em 18/10/2026

Skills substitui Entradas na navegação, com somente as sete habilidades pedidas: Impeccable, Frontend Design, Landing Page Design, ImageGen, Presentations, HyperFrames e HyperFrames Creative. Catálogo global, busca por objetivo, categorias e descrições. Montar pedido permite editar a ideia e copiar para a conversa do agente, incluindo o espaço de inspiração e a revisão em Escolhas. Novas instalações não entram automaticamente; curadoria em `app/web/src/skillCatalog.ts`.

Sugestões espontâneas ficam em Escolhas > Sugestões para o acervo quando há pendências. Build, 11 testes unitários e 16 de navegador aprovados em biblioteca temporária. Capturas conferidas em `/tmp/repertorio-skills-qa/`; detalhes em `app/VALIDACAO.md`. Interface compilada: atualizar o app com ⌘R. Próxima ação: usar o catálogo e acrescentar habilidades somente quando o usuário pedir. Preservar os trabalhos de palestra e demais alterações anteriores.

## Espaços de trabalho implementados em 18/10/2026

O Repertório agora tem espaços com criação, renomeação, exclusão direta e definitiva e troca pela navegação esquerda. O acervo anterior está em Referências; novos espaços começam vazios. Fichas e arquivos são compartilhados, com publicação e lixeira independentes por espaço. Agentes recebem os espaços de inspiração e os destinos de incorporação explicitamente.

Validação: 32 testes do servidor, 7 da interface e 14 de navegador aprovados; build e migração numa cópia dos 15.662 registros aprovados. Backup anterior verificado em `_saida/repertorio-qa/espacos/antes-dos-espacos.zip`. Operação, contratos e recuperação: `docs/REPERTORIO-ESPACOS.md`.

Growmate já reúne os 32 carrosséis #Livros incorporados ontem, das pastas 18 (Simon Sinek) a 49, mais a ficha de paleta e 73 ícones SVG (33 referências no total). As mesmas fichas continuam em Referências, sem duplicar arquivos. Grafo, busca dos agentes e publicação dos 32 itens verificados. Espaço: `ff1be998-6589-4e3d-a1f2-e7682406e853`; contexto da vinculação: `55be2440-518d-49d6-a55f-b24b4fae5460`. Detalhes em `docs/REPERTORIO-GROWMATE-LIVROS.json`. Próxima ação: usar o espaço Growmate como inspiração quando o usuário indicar. Preservar os trabalhos de palestra descritos abaixo.

Atualizado em 18/10/2026 (America/Sao_Paulo).

## Objetivo atual

Manter o Repertório como biblioteca compartilhada, curadoria e aplicativo. Novas criações e seus arquivos de trabalho ficam no projeto de destino, consultando o acervo pelo MCP.

A palestra “Você compraria de você mesmo?” está no Growmate Marketing, em `apresentacoes/palestra-cx-ia/`. O checkpoint da produção é `project.md` naquela pasta. A primeira parte de 24 slides está pronta; a continuação depende da fala, dos cases e da duração. `docs/RETOMADA-PALESTRA-CX-IA.md` aponta para o novo local.

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

Repertório é o projeto e o app de busca e curadoria de referências. Referências e Growmate são espaços dentro dele. A criação segue roteiro, referências, revisão do usuário e conferência visual. A biblioteca real não recebe dados de demonstração.

As duas versões da palestra mantidas pelo usuário foram transferidas para o Growmate Marketing, com imagens, fontes, histórico e evidências. As demais variantes foram excluídas pelo usuário antes desta organização e não devem ser restauradas. As duas pastas locais de gateway são alterações anteriores e não pertencem a esta transferência; preservá-las.

## Próxima ação

Para novas peças da Growmate, abrir `/Users/cleiton/Documents/Desenvolvimento/growmate/growmate-marketing` e trabalhar na pasta daquela produção. O projeto está cadastrado no MCP como `growmate-marketing-15e1a6`; o espaço de inspiração é informado por demanda, sem inferir o espaço aberto no aplicativo.

Para apresentar ou continuar a palestra, consultar `apresentacoes/palestra-cx-ia/project.md` no Growmate Marketing. A entrega principal está em `final/palestra-arquivo-unico.html` dentro da produção.

Para manter o acervo, usar este projeto. Novas evidências de manutenção ficam em `app/.runtime/qa/` ou em pasta temporária. Preservar as alterações anteriores dos gateways. O funcionamento automático do hook RTK em um Codex reiniciado e a economia total da assinatura ainda não foram medidos.
