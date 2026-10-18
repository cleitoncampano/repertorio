# Ferramentas e continuidade

Instalação em 17/10/2026. Objetivo: mais trabalho correto por uso da assinatura, com contexto consultado conforme a tarefa.

## Instalação

| Ferramenta | Versão | Integração |
|---|---|---|
| RTK OSS | 1.0.1 | Binário `~/.local/bin/rtk`; hook nativo no perfil Codex `expresso` |
| Engram | 3.4.0 | Binário `~/.local/bin/engram`; consultas e registros pelo terminal |

Os arquivos vieram dos releases oficiais de `rtk-ai/rtk` e `Gentleman-Programming/engram`. As somas SHA-256 foram conferidas com os metadados e arquivos de checksum dos releases. Manifesto local: `~/.local/share/agent-efficiency/install.json`.

RTK OSS inclui os filtros de comandos. Sua telemetria permanece desligada por padrão. A memória usa o SQLite local do Engram em `~/.engram/`. A instalação não adicionou sincronização em nuvem, um observador de IA ou servidores MCP. Modelo, esforço e permissões do Codex não foram alterados.

O perfil ativo recebe a integração em todos os projetos que abrir. Outros perfis e outros agentes não foram configurados. Reinicie o Codex para carregar o hook. Executors que não acionam o hook devem usar o prefixo `rtk` explicitamente.

## Uso

Na raiz do projeto, consulte o checkpoint existente antes de uma exploração ampla. Use a memória somente quando uma decisão anterior afetar a tarefa:

```sh
engram context
engram search "termos da decisão" --limit 3
engram save "Título da decisão" "O quê; por quê; arquivos; pendências; próxima ação" --type decision
```

Use `--project NOME` quando a detecção da pasta não representar o projeto desejado. A memória deste repositório usa `--project repertorio`. Confira o estado real dos arquivos antes de confiar em uma memória. Registre decisões relevantes, não transcrições ou saídas brutas.

Exemplos de filtragem:

```sh
rtk git status
rtk git log -n 20
rtk git diff --stat
rtk gain
```

Para testes, preserve o interpretador ou ambiente já estabelecido pelo projeto, sem instalar dependências redundantes. Consulte `rtk test --help` para o executor genérico. Para recuperar um resultado ilegível ou insuficiente, consulte a recuperação indicada na saída ou `rtk bypass <comando>`.

O sandbox atual pode impedir gravações nos diretórios de dados globais. Isso foi observado ao abrir o histórico do RTK. Os testes com persistência usaram a autorização normal do executor; a instalação não ampliou diretórios graváveis. Nessa situação, mantenha o checkpoint local e use a autorização necessária para atualizar a memória ou as métricas.

## Validação observada

- `engram test reliability --quick --json`: aprovado, incluindo gravação/busca/contexto e escritas concorrentes.
- Processos independentes de Engram: gravação, busca e contexto aprovados; consulta de outro projeto não recebeu a memória do primeiro. Dados de teste ficaram em uma pasta temporária.
- Hook RTK: reescreveu `git status`, preservou o campo de timeout e deixou um evento incompleto seguir sem alteração.
- Uma execução fora de um repositório preservou o código de erro do Git e a mensagem de diagnóstico.
- Comandos reais, antes das mudanças de documentação desta instalação:

| Comando | Saída original | Saída RTK | Redução em bytes |
|---|---:|---:|---:|
| `git status` | 839 | 468 | 44,2% |
| `git log -n 20` | 3.782 | 2.362 | 37,5% |
| `git diff --stat` | 256 | 256 | 0% |

Essas medidas representam a saída dos comandos, não a economia total da assinatura. Não foi iniciada uma sessão paga de modelo para testar a integração automática. A comparação de consumo e qualidade em tarefas completas permanece como próxima medição útil.

## Recuperação

As instruções anteriores à instalação estão em `~/.local/share/agent-efficiency/backups/20261018T022513Z/`. O manifesto local registra os binários e seus hashes.

Para retirar o hook, use `rtk init --global --codex --uninstall` no mesmo perfil. O bloco próprio de continuidade está delimitado por `efficiency:start` e `efficiency:end` no `AGENTS.md` global e pode ser removido ou ajustado sem afetar o restante. Preserve a memória ao trocar ou remover os binários.

O manual integral anterior do projeto foi preservado em `biblioteca/manual-agentes.md`. O bloco MCP gerado pelo Repertório não foi alterado.
