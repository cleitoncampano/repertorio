# Repertório

Para conhecer o produto e instalar em Mac ou Windows, comece pelo [guia do produto](../docs/produto/PRODUTO.md) e pela [instalação](../docs/produto/INSTALACAO.md). Este arquivo documenta a manutenção da instalação de desenvolvimento. Novas instalações usam `init`, sem importar o acervo particular; o modo `demo` cria exemplos originais em dados separados.

Biblioteca visual local organizada em espaços e compartilhada entre seus projetos e agentes. O mapa liga as referências pelo momento da história, pelo recurso visual ou pelo formato de tela; o serviço central persiste curadoria, buscas, seleções e novas criações.

## Abrir

Dois cliques em **Abrir Repertório.command**, ou na raiz do acervo:

```sh
./app/run.sh serve
```

Abra **http://127.0.0.1:8766**. Deixe o processo em execução enquanto os agentes consultam a biblioteca. Use Ctrl+C para encerrar. Não é necessário login; o serviço só escuta no computador local.

### App no Dock e sempre ligado

Neste computador o Repertório é um aplicativo: **Repertório**, com o ícone psicodélico do olho, fixado no Dock. Clicar abre o acervo numa janela própria (sem navegador). Fechar a janela não desliga nada; ⌘Q encerra só o app, e o serviço continua no ar para os agentes.

- `~/Applications/Repertório.app` é nativo (Swift + WebKit). O código está em `app/mac/main.swift`; o ícone em `app/mac/icone.png` (desenhado por `icone.py`). Para gerar de novo: `./app/mac/build.sh /caminho/Repertório.app`, depois encerre o app e troque o arquivo.
- O app confere o serviço a cada 30 segundos e o religa se cair. Downloads perguntam onde salvar; links externos abrem no navegador.
- `~/Library/LaunchAgents/local.repertorio.plist` abre o app sem janela ao entrar no Mac e confere a cada 5 minutos se ele está aberto.
- O macOS impede que serviços em segundo plano leiam a pasta Documentos; por isso quem liga o serviço é o app, que recebeu essa permissão. Se o app for recompilado, o Mac pede a permissão de novo.
- Registro em `~/Library/Logs/repertorio.log`. Para reiniciar com código novo do servidor, basta encerrar o processo do serviço: o app o religa em segundos.
- Para desligar de vez: `launchctl bootout gui/$(id -u)/local.repertorio`, encerre o app e apague o app e o arquivo do LaunchAgents.

No Claude Code o MCP está registrado para todos os projetos com `claude mcp add --transport http -s user repertorio http://127.0.0.1:8766/mcp`.

Primeira instalação em outro ambiente, com Python 3.12, uv, Node.js >=22.12 e pnpm 11 disponíveis:

```sh
./app/setup.sh
```

O frontend compilado é servido pelo FastAPI. Os originais e o protótipo continuam nos locais anteriores. O banco e as novas criações ficam em `app/.runtime/`, fora do versionamento.

## Espaços de trabalho

O seletor **Espaços**, no canto esquerdo, permite criar, entrar, renomear e excluir espaços. O nome atual aparece no cabeçalho. Novos espaços começam vazios; todo o acervo anterior ficou em **PP Treta**, cujo ID é `pp-treta`.

Uma referência pode aparecer em vários espaços sem duplicar a ficha nem os arquivos. Alterar título, descrição ou classificação atualiza todos os espaços. Publicação e lixeira são independentes: excluir de A preserva a referência em B. Pelo painel da referência, use **Adicionar ao espaço** ou **Mover para o espaço**. Mover retira apenas do espaço de origem. Apresentações levam seus slides.

Excluir um espaço remove-o imediatamente, sem opção de restauração. Seus vínculos são removidos; os arquivos e as referências dos demais espaços são preservados. Vocabulário, princípios criativos e fontes continuam compartilhados.

Os agentes precisam receber os espaços explicitamente. Exemplo: “Use os espaços GrowMate e PP Treta como inspiração”. Se você não indicar, o agente deve perguntar. O espaço aberto no app não muda o contexto do agente. Ao incorporar o resultado, indique também os espaços de destino.

## Como usar

- Explore o mapa com arraste e zoom. Clique nos grupos do centro e nos nomes em volta para investigar suas relações. Clicar numa imagem ou vídeo abre a tela grande com a ficha ao lado. Numa imagem, as setas sobre a peça, ← →, dois dedos no trackpad e o deslize no celular passam pelas imagens do material (slides da apresentação), em roda: depois da última volta à primeira; os botões ‹ › do canto direito, ↑ ↓, N e P trocam de material. Material de uma imagem só: ← → e o deslize já trocam de material. Num vídeo, as setas e ← → trocam de vídeo. T alterna o modo teatro e F a tela cheia. **Excluir deste espaço** manda a peça para a lixeira do espaço e passa ao próximo material, com Desfazer no aviso; vale para imagens e vídeos. **Ficha completa** abre o painel lateral.
- Na legenda, **História / Recurso visual / Formato** troca a organização do mapa, e a escolha fica salva por espaço. **História** (padrão das imagens) mostra seis momentos de uma apresentação na ordem: Abrir, Conduzir, Explicar, Provar, Marcar e Fechar, com os papéis em volta. **Recurso visual** reúne as 48 técnicas em sete famílias: Cor e contraste, Tipografia, Imagem e foto, Composição e grade, Percurso e revelação, Ideia e surpresa, Dados e interface. **Formato** (padrão dos vídeos) mostra onde a peça vai passar, com o papel na história ou o tipo de vídeo em volta.
- Ao lado do botão de tema, **Visualização do grafo** oferece nove opções com prévias. **Mapa livre**, **Por grupos** e **Hierárquico** mantêm a linguagem original; **Cosmos**, **Metrô**, **Circuito**, **Jardim**, **Editorial** e **Prisma** têm organizações, paletas e formatos próprios, adaptados aos temas claro e escuro. São as mesmas referências e conexões do espaço aberto. A preferência fica salva no navegador; a câmera de cada organização é independente por espaço. Busca, filtros e ficha aberta permanecem durante a troca. **Mapa livre** permite voltar à organização original.
- Arraste as opções de visualização para mudar sua ordem, como cards de um kanban. No celular, use a alça de pontos à esquerda; o restante do card permite rolar a lista. Pelo teclado, use **Alt + ↑/↓** na opção focada. A ordem fica salva neste navegador e vale em todos os espaços. Reordenar preserva a visualização aberta; clique para trocar. **Escape** cancela o arraste.
- Busque por palavras e refine por intenção, origem, movimento, formato e estética. A lista oferece navegação por teclado.
- O painel mostra princípio criativo, prévias, slides, relações, condições de uso conhecidas e o contexto disponibilizado ao agente.
- **Excluir deste espaço** envia à Lixeira daquele espaço, com Desfazer. A remoção de uma apresentação também a retira das buscas de seus slides; os originais e mídias compartilhadas não são apagados.
- **Skills** reúne somente as habilidades escolhidas pelo usuário: Impeccable, Frontend Design, Landing Page Design, ImageGen, Presentations, HyperFrames e HyperFrames Creative. Busque por objetivo ou categoria e use **Montar pedido** para copiar uma solicitação com a skill, sua ideia e o espaço de inspiração. Cole na conversa com o agente para iniciar o trabalho. O catálogo é global, acessível também sem espaço aberto; novas instalações não entram automaticamente. A lista é mantida em `web/src/skillCatalog.ts`, e `/?view=skills` abre a tela diretamente.
- **Escolhas** mostra as referências que o agente separou para cada pedido. Aprove, corte e comente: o agente lê a revisão com `get_pack` antes de criar.
- Quando há sugestões espontâneas, **Escolhas** também oferece **Sugestões para o acervo**. Abra a ficha e use **Publicar no espaço** ou **Excluir deste espaço**. Pedidos explícitos de incorporação continuam publicados depois do processamento.
- **Atividade** registra alterações e consultas por demanda. Trabalhos interrompidos podem ser tentados novamente.
- **Vídeos de motion** (espaço Motion): o mapa se organiza por formato de tela no centro (Horizontal 16:9 para YouTube e sites, Vertical 9:16 para Reels e TikTok, Quadrado e 4:5 para feed, Prompts-modelo) e, em volta, pelo tipo de vídeo (lançamento, showreel, explicativo, dados, tipografia, histórias, arte abstrata e 3D, vinheta). **Por grupos** mostra os formatos lado a lado. As capas tocam o vídeo no próprio mapa ao aproximar, até 12 por vez, só as visíveis e grandes o bastante; com "reduzir movimento" ligado no sistema, ficam paradas. Passar o mouse mostra o loop; a lista toca os cartões visíveis. Clicar num vídeo abre o player em tela grande, como no YouTube: modo padrão com detalhes e "A seguir" ao lado, modo teatro (T) e tela cheia (F); espaço ou K pausa, M tira o som, ← → (ou as setas na tela, ou dois dedos para o lado no trackpad, ou o deslize no celular) trocam de vídeo, Shift + ← → avançam 5 s, J e L 10 s. **Ficha completa** abre a ficha lateral, com a decupagem cena a cena, o prompt original para copiar, a ferramenta usada, os créditos do autor e **Ver quadros**, a prancha com oito momentos do vídeo, que é a imagem que o agente recebe.

## Conectar projetos e agentes

Cadastre cada pasta uma vez. Este comando apenas registra a pasta; `--write-instructions` acrescenta um bloco delimitado ao AGENTS.md, preservando o restante:

```sh
./app/run.sh connect /caminho/growmate-marketing --write-instructions
./app/run.sh connect /caminho/growmate-comercial --write-instructions
```

A saída inclui o `project_id` e os exemplos de configuração. Rascunhos, imagens, prévias e arquivos finais ficam no projeto cadastrado. O Repertório mantém a biblioteca e sua curadoria; a incorporação de uma criação é uma decisão explícita do usuário. Não mova projetos ou conversas para esta aplicação.

No Codex:

```sh
codex mcp add repertorio --url http://127.0.0.1:8766/mcp
```

No arquivo de configuração do OpenCode, mescle esta entrada sem substituir outras configurações:

```json
{
  "mcp": {
    "repertorio": {
      "type": "remote",
      "url": "http://127.0.0.1:8766/mcp",
      "oauth": false,
      "enabled": true
    }
  }
}
```

Depois, abra uma nova sessão e peça: **“Busque no Repertório referências para esta demanda.”** O MCP fornece ferramentas; o bloco de instruções orienta quando consultá-las. A aplicação não intercepta sessões ou credenciais, nem configura globalmente os harnesses sem que você execute esses comandos.

### Ferramentas MCP

| Ferramenta | Uso |
|---|---|
| `start_context` | Recebe `project_id`, `demand` e `workspace_ids`; retorna um `id` de contexto independente |
| `search_references` | Recebe `request` com `query` em português comum, `context_id` e filtros opcionais. Frases conhecidas viram intenção, técnica, movimento ou estética (`understood`); o resto é buscado no texto. Sem `kind`, deixa mídias soltas de fora. `per_group` (padrão 1) limita peças da mesma apresentação. Devolve também uma prancha numerada (`contact_sheet`, padrão ligado) |
| `get_reference` | Recebe `reference_id` e `context_id` ou `workspace_ids`; `include_image: true` inclui imagem raster no resultado MCP (em vídeos, a prancha de oito quadros) |
| `get_guide` | Guias de criação de vídeo: sem `name`, lista os disponíveis; com `name` (`lancamento`, `formatos`, `prompt`, `kit`...), devolve o texto |
| `build_inspiration_pack` | Recebe `request` com contexto, título, IDs e justificativa; guarda versões selecionadas e devolve `review_url` para a tela Escolhas |
| `get_pack` | Recebe `pack_id`; devolve a seleção com a revisão do usuário em cada referência (`approved`, `cut` ou sem resposta, e comentário) |
| `register_reference` | Recebe `request` com arquivos, ficha, `target_workspace_ids` e intenção de publicação; retorna uma operação |
| `update_reference` | Recebe ID e `request` com contexto, `expected_revision` e ficha completa |
| `set_reference_state` | Recebe ID e `request` com revisão e espaço e `expected_membership_revision`, com estado `published`, `pending` ou `trashed` |
| `get_operation` | Recebe `operation_id`; `retry: true` tenta novamente um processamento com falha |

Novas ferramentas MCP: `list_workspaces`, `create_workspace`, `rename_workspace`, `delete_workspace` e `set_reference_workspaces`. Excluir um espaço e vincular/mover referências pelo agente exigem `user_requested=true`. Vínculos existentes são compartilhados sem envio de arquivos.

Recursos MCP: `repertorio://workspaces`, `repertorio://projects`, `repertorio://vocabulary`, `repertorio://fonts`, `repertorio://principles/narrativa`, `repertorio://principles/direcao-de-arte`, `repertorio://contexts/{id}` e `repertorio://packs/{id}`.

Para inspeção visual de outros slides, obtenha a ficha do slide pelo ID listado nos filhos. A resposta inicial inclui até 12 filhos e 8 resumos de transição para limitar o contexto; a interface permite explorar todos.

### Incorporar um material aprovado

O agente inicia um contexto e envia uma ficha como esta (os valores de classificação devem existir no vocabulário):

```json
{
  "context_id": "ID_RETORNADO_POR_START_CONTEXT",
  "target_workspace_ids": ["pp-treta"],
  "request_key": "carrossel-christensen-v1",
  "user_requested": true,
  "files": ["saida/carrossel.pdf"],
  "previews": ["saida/capa.png"],
  "data": {
    "title": "Inovação vista por outro ângulo",
    "description": "Carrossel que apresenta uma ideia em etapas.",
    "idea": "Use contraste entre duas situações para revelar a mudança de perspectiva.",
    "techniques": ["contraste-de-escala"],
    "intentions": ["EXPLICAR"],
    "movements": [],
    "aesthetics": [],
    "strength": 4,
    "reusable": null,
    "source_reference_ids": [],
    "usage_notes": "Conferir condições de uso das imagens da peça."
  }
}
```

Os caminhos são relativos à pasta cadastrada, ou absolutos dentro dela. O servidor verifica novamente caminhos e hashes no processamento e copia apenas os arquivos enviados. O limite é 1 GB por arquivo e 60 arquivos por envio. Uma chave repetida devolve a mesma operação; reutilizar a chave com outro conteúdo gera conflito.

Sugestões usam `user_requested: false`. O campo registra a declaração do agente sobre o pedido do usuário, não uma verificação independente da conversa.

Imagens produzem prévias automaticamente. PDFs produzem até 30 páginas de prévia; PPTX usa a miniatura incorporada, quando existente; vídeo usa ffmpeg quando instalado. HTML nunca é executado pelo serviço. Para HTML, PPTX sem miniatura e vídeos sem ffmpeg, forneça `previews`. O original permanece disponível integralmente. Se o processamento falhar por falta de prévia, envie novamente com prévias e uma nova chave; exclua a entrada incompleta se ela não for mais necessária.

HTML e demais originais são entregues como download, não executados no domínio da interface. A classificação `reusable` expressa o que foi informado; não certifica licenciamento.

### CLI e API

```sh
./app/run.sh workspaces
./app/run.sh create-workspace "GrowMate"
./app/run.sh delete-workspace ID_DO_ESPACO --revision REVISAO_ATUAL
./app/run.sh search "abertura com impacto" --workspace pp-treta --prancha
./app/run.sh get '284-reel-cerebro-3d' --workspace pp-treta
./app/run.sh context PROJECT_ID "Apresentação comercial" --workspace pp-treta
./app/run.sh register /tmp/envio.json
./app/run.sh operation OPERATION_ID
./app/run.sh doctor
```

A API está documentada em **http://127.0.0.1:8766/docs**. Browser, CLI e MCP usam a mesma camada de serviço. Grafo, contadores, demandas, operações, atividade e prévias recebem `workspace_id`; buscas recebem `workspace_ids` ou `context_id`. A ficha mantém `revision` editorial e o vínculo mantém `membership_revision`. A alteração de estado exige `workspace_id` e `expected_membership_revision`. Chamadas sem repertório explícito retornam 422; links antigos da interface continuam usando PP Treta. Não há busca vetorial nem API de IA paga embutida; o agente do harness interpreta o pedido e escolhe consultas complementares.

## Persistência, importação e recuperação

### Cópia de segurança automática

O serviço faz sozinho, uma vez por semana, uma cópia em **iCloud Drive › Backups › Repertório** (fora do Mac): `repertorio-DATA.zip` com a curadoria (banco e criações) e `pptreta-DATA.bundle` com o histórico do projeto. Guarda as 6 mais recentes e registra "Cópia de segurança salva" em Atividade. `REPERTORIO_BACKUP_DIR` troca a pasta.

```sh
./app/run.sh backup-now     # faz uma cópia agora (com o serviço parado ou rodando)
./app/run.sh doctor         # mostra a última cópia
git clone "…/Backups/Repertório/pptreta-DATA.bundle" pptreta   # recupera o projeto
./app/run.sh restore "…/Backups/Repertório/repertorio-DATA.zip"  # recupera a curadoria (serviço parado)
```

O histórico (git) guarda código, textos e dados do acervo. As produções são versionadas e preservadas pelos respectivos projetos de destino. Os 12 GB de `_originais/` e as imagens geradas a partir deles ficam fora (ver `.gitignore`); numa migração, copie `_originais/` à parte.

### Importação e restauração manual

```sh
./app/run.sh import --workspace pp-treta
./app/run.sh import-motion --workspace ID_DO_ESPACO   # vídeos de dados/motion/*.jsonl
./app/run.sh backup /caminho/backup-repertorio.zip
# Encerre o serviço antes de restaurar:
./app/run.sh restore /caminho/backup-repertorio.zip
```

- O importador migra os dados existentes, incluindo mídias sem classificação, e preserva IDs, curadoria e exclusões em reimportações.
- `import-motion` cria uma referência externa por vídeo, ligada às técnicas do vocabulário, com capa, prancha de quadros, loop curto e vídeo completo. Também preserva a curadoria feita no app. As fichas são montadas por `ferramentas/incorporar_prompt_motion.py`; os vídeos ficam em `_originais/prompt-motion/`, fora do Git e do backup, como os demais originais.
- O banco é a fonte de verdade da aplicação. Os scripts antigos continuam independentes e não refletem as exclusões feitas no Repertório.
- O backup contém o banco e as criações gerenciadas, com checksums. Os originais de 11 GB não são duplicados: um manifesto registra suas dependências. Para migrar de computador, copie também o acervo original.
- A restauração verifica integridade, ajusta caminhos gerenciados e preserva a pasta anterior com sufixo `before-restore`. Não pode ocorrer enquanto o serviço está ativo.
- Tarefas interrompidas pela parada do serviço voltam à fila ao reiniciar. Edições usam revisão otimista e retornam conflito se outro agente já tiver alterado a ficha.
- `REPERTORIO_ROOT`, `REPERTORIO_HOME` e `REPERTORIO_PORT` permitem separar acervo, dados e porta. O padrão é 8766.

## Desenvolvimento e testes

```sh
./app/.venv/bin/python -m pytest app/tests -q
pnpm --dir app/web test
pnpm --dir app/web build
pnpm --dir app/web dev
```

Testes completos no navegador, em uma biblioteca temporária que não altera o acervo real:

```sh
cd app/web
pnpm exec playwright install chromium
pnpm test:e2e
```

Para usar um Chromium já instalado, informe `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`. Novas capturas e medições da validação local ficam em `app/.runtime/qa/` ou em uma pasta temporária. Caminhos `_saida/repertorio-qa/` nas validações anteriores são registros históricos.

O frontend de desenvolvimento usa a porta 5173 e encaminha `/api` para 8766. Python usa SQLAlchemy/Alembic, SQLite WAL e FTS5; a interface usa React, TypeScript, Radix, Tailwind, TanStack Query e Cytoscape. As dependências estão fixadas em `requirements.lock` e `web/pnpm-lock.yaml`.

Perestroika, SOAP, captura de páginas, terminal embutido, colaboração remota e autenticação não fazem parte desta primeira versão.
