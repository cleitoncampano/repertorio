# Repertório

Biblioteca visual local organizada em espaços e compartilhada entre seus projetos e agentes. O mapa mantém as operações do olhar, técnicas e referências do PPTRETA; o serviço central persiste curadoria, buscas, seleções e novas criações.

## Abrir

Dois cliques em **Abrir Repertório.command**, ou na raiz do acervo:

```sh
./repertorio/run.sh serve
```

Abra **http://127.0.0.1:8766**. Deixe o processo em execução enquanto os agentes consultam a biblioteca. Use Ctrl+C para encerrar. Não é necessário login; o serviço só escuta no computador local.

### App no Dock e sempre ligado

Neste computador o Repertório é um aplicativo: **Repertório**, com o ícone psicodélico do olho, fixado no Dock. Clicar abre o acervo numa janela própria (sem navegador). Fechar a janela não desliga nada; ⌘Q encerra só o app, e o serviço continua no ar para os agentes.

- `~/Applications/Repertório.app` é nativo (Swift + WebKit). O código está em `repertorio/mac/main.swift`; o ícone em `repertorio/mac/icone.png` (desenhado por `icone.py`). Para gerar de novo: `./repertorio/mac/build.sh /caminho/Repertório.app`, depois encerre o app e troque o arquivo.
- O app confere o serviço a cada 30 segundos e o religa se cair. Downloads perguntam onde salvar; links externos abrem no navegador.
- `~/Library/LaunchAgents/local.repertorio.plist` abre o app sem janela ao entrar no Mac e confere a cada 5 minutos se ele está aberto.
- O macOS impede que serviços em segundo plano leiam a pasta Documentos; por isso quem liga o serviço é o app, que recebeu essa permissão. Se o app for recompilado, o Mac pede a permissão de novo.
- Registro em `~/Library/Logs/repertorio.log`. Para reiniciar com código novo do servidor, basta encerrar o processo do serviço: o app o religa em segundos.
- Para desligar de vez: `launchctl bootout gui/$(id -u)/local.repertorio`, encerre o app e apague o app e o arquivo do LaunchAgents.

No Claude Code o MCP está registrado para todos os projetos com `claude mcp add --transport http -s user repertorio http://127.0.0.1:8766/mcp`.

Primeira instalação em outro ambiente, com Python 3.12, uv, Node.js >=22.12 e pnpm 11 disponíveis:

```sh
./repertorio/setup.sh
```

O frontend compilado é servido pelo FastAPI. Os originais e o protótipo continuam nos locais anteriores. O banco e as novas criações ficam em `repertorio/.runtime/`, fora do versionamento.

## Espaços de trabalho

O seletor **Espaços**, no canto esquerdo, permite criar, entrar, renomear, excluir e restaurar espaços. O nome atual aparece no cabeçalho. Novos espaços começam vazios; todo o acervo anterior ficou em **PP Treta**, cujo ID é `pp-treta`.

Uma referência pode aparecer em vários espaços sem duplicar a ficha nem os arquivos. Alterar título, descrição ou classificação atualiza todos os espaços. Publicação e lixeira são independentes: excluir de A preserva a referência em B. Pelo painel da referência, use **Adicionar ao espaço** ou **Mover para o espaço**. Mover retira apenas do espaço de origem. Apresentações levam seus slides.

Espaços excluídos ficam disponíveis para restauração no seletor. Os arquivos e as referências dos demais espaços são preservados. Vocabulário, princípios criativos e fontes continuam compartilhados.

Os agentes precisam receber os espaços explicitamente. Exemplo: “Use os espaços GrowMate e PP Treta como inspiração”. Se você não indicar, o agente deve perguntar. O espaço aberto no app não muda o contexto do agente. Ao incorporar o resultado, indique também os espaços de destino.

## Como usar

- Explore o mapa com arraste e zoom. Clique nas operações, técnicas ou imagens para investigar suas relações.
- Busque por palavras e refine por intenção, origem, movimento, formato e estética. A lista oferece navegação por teclado.
- O painel mostra princípio criativo, prévias, slides, relações, condições de uso conhecidas e o contexto disponibilizado ao agente.
- **Excluir deste espaço** envia à Lixeira daquele espaço, com Desfazer. A remoção de uma apresentação também a retira das buscas de seus slides; os originais e mídias compartilhadas não são apagados.
- **Entradas** contém sugestões espontâneas. Pedidos explícitos de incorporação são publicados depois do processamento.
- **Escolhas** mostra as referências que o agente separou para cada pedido. Aprove, corte e comente: o agente lê a revisão com `get_pack` antes de criar.
- **Atividade** registra alterações e consultas por demanda. Trabalhos interrompidos podem ser tentados novamente.

## Conectar projetos e agentes

Cadastre cada pasta uma vez. Este comando apenas registra a pasta; `--write-instructions` acrescenta um bloco delimitado ao AGENTS.md, preservando o restante:

```sh
./repertorio/run.sh connect /caminho/growmate-marketing --write-instructions
./repertorio/run.sh connect /caminho/growmate-comercial --write-instructions
```

A saída inclui o `project_id` e os exemplos de configuração. Não é preciso mover projetos ou conversas para esta aplicação.

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
| `get_reference` | Recebe `reference_id` e `context_id` ou `workspace_ids`; `include_image: true` inclui imagem raster no resultado MCP |
| `build_inspiration_pack` | Recebe `request` com contexto, título, IDs e justificativa; guarda versões selecionadas e devolve `review_url` para a tela Escolhas |
| `get_pack` | Recebe `pack_id`; devolve a seleção com a revisão do usuário em cada referência (`approved`, `cut` ou sem resposta, e comentário) |
| `register_reference` | Recebe `request` com arquivos, ficha, `target_workspace_ids` e intenção de publicação; retorna uma operação |
| `update_reference` | Recebe ID e `request` com contexto, `expected_revision` e ficha completa |
| `set_reference_state` | Recebe ID e `request` com revisão e espaço e `expected_membership_revision`, com estado `published`, `pending` ou `trashed` |
| `get_operation` | Recebe `operation_id`; `retry: true` tenta novamente um processamento com falha |

Novas ferramentas MCP: `list_workspaces`, `create_workspace`, `rename_workspace`, `set_workspace_state` e `set_reference_workspaces`. Excluir/restaurar um espaço e vincular/mover referências pelo agente exigem `user_requested=true`. Vínculos existentes são compartilhados sem envio de arquivos.

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
./repertorio/run.sh workspaces
./repertorio/run.sh create-workspace "GrowMate"
./repertorio/run.sh search "abertura com impacto" --workspace pp-treta --prancha
./repertorio/run.sh get '284-reel-cerebro-3d' --workspace pp-treta
./repertorio/run.sh context PROJECT_ID "Apresentação comercial" --workspace pp-treta
./repertorio/run.sh register /tmp/envio.json
./repertorio/run.sh operation OPERATION_ID
./repertorio/run.sh doctor
```

A API está documentada em **http://127.0.0.1:8766/docs**. Browser, CLI e MCP usam a mesma camada de serviço. Grafo, contadores, demandas, operações, atividade e prévias recebem `workspace_id`; buscas recebem `workspace_ids` ou `context_id`. A ficha mantém `revision` editorial e o vínculo mantém `membership_revision`. A alteração de estado exige `workspace_id` e `expected_membership_revision`. Chamadas sem repertório explícito retornam 422; links antigos da interface continuam usando PP Treta. Não há busca vetorial nem API de IA paga embutida; o agente do harness interpreta o pedido e escolhe consultas complementares.

## Persistência, importação e recuperação

### Cópia de segurança automática

O serviço faz sozinho, uma vez por semana, uma cópia em **iCloud Drive › Backups › Repertório** (fora do Mac): `repertorio-DATA.zip` com a curadoria (banco e criações) e `pptreta-DATA.bundle` com o histórico do projeto. Guarda as 6 mais recentes e registra "Cópia de segurança salva" em Atividade. `REPERTORIO_BACKUP_DIR` troca a pasta.

```sh
./repertorio/run.sh backup-now     # faz uma cópia agora (com o serviço parado ou rodando)
./repertorio/run.sh doctor         # mostra a última cópia
git clone "…/Backups/Repertório/pptreta-DATA.bundle" pptreta   # recupera o projeto
./repertorio/run.sh restore "…/Backups/Repertório/repertorio-DATA.zip"  # recupera a curadoria (serviço parado)
```

O histórico (git) guarda código, textos, dados e as apresentações de `_saida`. Os 12 GB de `_originais/` e as imagens geradas a partir deles ficam fora (ver `.gitignore`); numa migração, copie `_originais/` à parte.

### Importação e restauração manual

```sh
./repertorio/run.sh import --workspace pp-treta
./repertorio/run.sh backup /caminho/backup-repertorio.zip
# Encerre o serviço antes de restaurar:
./repertorio/run.sh restore /caminho/backup-repertorio.zip
```

- O importador migra os dados existentes, incluindo mídias sem classificação, e preserva IDs, curadoria e exclusões em reimportações.
- O banco é a fonte de verdade da aplicação. Os scripts antigos continuam independentes e não refletem as exclusões feitas no Repertório.
- O backup contém o banco e as criações gerenciadas, com checksums. Os originais de 11 GB não são duplicados: um manifesto registra suas dependências. Para migrar de computador, copie também o acervo original.
- A restauração verifica integridade, ajusta caminhos gerenciados e preserva a pasta anterior com sufixo `before-restore`. Não pode ocorrer enquanto o serviço está ativo.
- Tarefas interrompidas pela parada do serviço voltam à fila ao reiniciar. Edições usam revisão otimista e retornam conflito se outro agente já tiver alterado a ficha.
- `REPERTORIO_ROOT`, `REPERTORIO_HOME` e `REPERTORIO_PORT` permitem separar acervo, dados e porta. O padrão é 8766.

## Desenvolvimento e testes

```sh
./repertorio/.venv/bin/python -m pytest repertorio/tests -q
pnpm --dir repertorio/web test
pnpm --dir repertorio/web build
pnpm --dir repertorio/web dev
```

Testes completos no navegador, em uma biblioteca temporária que não altera o acervo real:

```sh
cd repertorio/web
pnpm exec playwright install chromium
pnpm test:e2e
```

Para usar um Chromium já instalado, informe `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`. As capturas e medições da validação local estão em `_saida/repertorio-qa/` na raiz do acervo.

O frontend de desenvolvimento usa a porta 5173 e encaminha `/api` para 8766. Python usa SQLAlchemy/Alembic, SQLite WAL e FTS5; a interface usa React, TypeScript, Radix, Tailwind, TanStack Query e Cytoscape. As dependências estão fixadas em `requirements.lock` e `web/pnpm-lock.yaml`.

Perestroika, SOAP, captura de páginas, terminal embutido, colaboração remota e autenticação não fazem parte desta primeira versão.
