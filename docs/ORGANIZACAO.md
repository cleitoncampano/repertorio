# Organização do Repertório

O projeto se chama **Repertório**. **PPT Treta** é um espaço de referências dentro dele, assim como **Growmate**. O curso PPTRETA continua identificado como origem dos materiais correspondentes.

A pasta principal é `/Users/cleiton/Documents/Desenvolvimento/repertorio`. Abra essa pasta no editor para trabalhar no projeto.

| Pasta | Conteúdo |
| --- | --- |
| `app/` | Aplicativo: servidor Python, interface web, app do Mac e testes |
| `app/.runtime/` | Banco SQLite, arquivos incorporados ao acervo, cache de buscas e evidências de manutenção, fora do Git |
| `biblioteca/` | Método de criação, princípios e manual dos agentes |
| `dados/` | Fontes de importação do catálogo; o banco mantém a curadoria atual |
| `_originais/` | Materiais originais e mídias locais, fora do Git |
| `_referencias/` | Estudos e documentação das referências |
| `kit/` | Motor das apresentações HTML |
| `ferramentas/` | Automação e utilitários do projeto |
| `docs/` | Decisões, operação e checkpoints de continuidade |

## Acervo e produção separados em 19/10/2026

O Repertório mantém o acervo, a curadoria, os métodos, o kit reutilizável e o aplicativo. As produções ficam nos projetos de destino, com seus rascunhos, imagens, prévias, arquivos finais e checkpoints. A incorporação de uma criação ao acervo depende de pedido do usuário e de espaços de destino explícitos.

Projeto Growmate Marketing: `/Users/cleiton/Documents/Desenvolvimento/growmate/growmate-marketing`. A palestra foi organizada em `apresentacoes/palestra-cx-ia/`, com `original/`, `final/`, `ferramentas/`, `historico/` e `project.md`. A transferência preserva as duas versões mantidas pelo usuário e inclui o material local fora do Git. `TRANSFERENCIA.json` registra os arquivos e os hashes. As variantes já excluídas pelo usuário não são restauradas.

Não use `_saida/` desta biblioteca para novas entregas. Pranchas temporárias de busca ficam em `app/.runtime/search-previews/`; evidências da manutenção do aplicativo ficam em `app/.runtime/qa/` ou em pasta temporária. O utilitário `roteiro.py` exige `--saida` explícita no projeto de destino. Os caminhos `_saida/repertorio-qa/` citados nas validações anteriores são históricos.

O projeto de destino é cadastrado pelo comando `connect --write-instructions`, que preserva as instruções existentes e acrescenta o fluxo de consulta pelo MCP. Os contextos e as escolhas anteriores da palestra permanecem no banco, sem reimportar referências ou mover arquivos do acervo.

## Mudança de 19/10/2026

A raiz `pptreta/` passou a `repertorio/`. A subpasta que também se chamava `repertorio/` passou a `app/`, evitando a repetição `repertorio/repertorio`.

Os caminhos do banco foram atualizados em transação, com backup anterior e verificação dos arquivos. Os identificadores de referências, arquivos, projetos, espaços, contextos e escolhas foram preservados. Nenhum acervo foi reimportado. O backup anterior está em `_saida/repertorio-qa/organizacao/antes-da-organizacao.sqlite3`, junto das evidências locais de conferência. O projeto continua com o ID `repert-rio-87e17c`; o espaço PPT Treta continua com o ID `pp-treta`.

Os comandos atuais são:

```sh
./app/run.sh doctor
./app/run.sh serve
pnpm --dir app/web build
```

O app instalado em `~/Applications/Repertório.app` usa a nova raiz. O endereço local continua http://127.0.0.1:8766. O início automático pelo Mac continua usando o mesmo aplicativo.

Dois links locais de compatibilidade mantêm sessões e atalhos antigos funcionando: `pptreta` aponta para a nova raiz e `repertorio/repertorio` aponta para `app`. Eles ficam ocultos no Finder. O link interno não é versionado; os caminhos documentados e os comandos atuais usam apenas a nova organização.

## Mover novamente

Encerre o app do Mac e o serviço antes de mover a pasta. Depois de mover, use a nova raiz e um destino de backup fora dos dados do aplicativo:

```sh
./app/run.sh relocate /caminho/anterior --backup /caminho/externo/antes-da-mudanca.sqlite3
```

O comando recusa um serviço ativo, cria um backup consistente, atualiza os caminhos e verifica contagens, identificadores, vínculos e existência dos arquivos. Se a verificação falhar, a transação é desfeita. A renomeação histórica da subpasta `repertorio` para `app` também é reconhecida.

Confira `doctor`, atualize os caminhos dos ambientes Python e Node quando necessário e gere o app do Mac novamente pela nova raiz. A recompilação pode fazer o macOS solicitar acesso a Documentos. O backup do banco não substitui uma cópia dos originais e das mídias.
