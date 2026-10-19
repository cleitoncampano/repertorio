# Espaços de trabalho no Repertório

Implementado em 18/10/2026. Servidor 0.2.1, migração Alembic 0004.

## Uso

- Abrir o seletor Espaços no topo da navegação esquerda. Criar um espaço sempre começa vazio.
- Todo o acervo anterior permanece em PP Treta (`pp-treta`), inclusive os carrosséis Growmate já incorporados. Nenhum espaço de marca é criado ou abastecido automaticamente.
- Uma ficha e seus arquivos podem aparecer em vários espaços. Edições editoriais se propagam; publicação, lixeira e presença são locais.
- Adicionar ao espaço cria vínculos. Mover retira apenas da origem. Apresentações incluem seus slides.
- Excluir um espaço é imediato e definitivo no app, sem restauração. Os vínculos do espaço são apagados; referências e arquivos dos demais espaços permanecem disponíveis. O registro interno do espaço é mantido apenas para a procedência histórica de demandas e operações.
- Ao produzir, informar os espaços de inspiração. Ao incorporar, informar os destinos. O agente pergunta quando o repertório não foi indicado.

## Interfaces

`start_context` exige `workspace_ids`; buscas usam `context_id` ou `workspace_ids`; `get_reference` recebe um desses escopos. `register_reference` exige `target_workspace_ids` e processa os arquivos uma única vez. A revisão editorial permanece em `revision`; o vínculo usa `membership_revision`, exigida como `expected_membership_revision` nas alterações de estado. Ferramentas de espaços e compartilhamento estão documentadas no README do app e no MCP.

Espaços e fichas têm IDs estáveis. Os vínculos usam chave composta, estado local e marca de retirada para que reimportações não ressuscitem referências movidas. Novos slides herdam os vínculos da apresentação. Contextos guardam os espaços consultados; operações guardam seus destinos. Eventos indicam os espaços afetados. O banco e os arquivos continuam únicos.

## Validação

- 32 testes Python, 7 testes unitários da interface e 14 testes Playwright aprovados. Build TypeScript/Vite aprovado.
- Testes e demonstrações executados em bibliotecas temporárias, sem criar demandas ou referências de teste no acervo real.
- Migração ensaiada numa cópia do banco real: 15.662 registros vinculados, com hashes idênticos para todas as tabelas anteriores, incluindo referências, assets, contextos, seleções, comentários e operações.
- Migração real aplicada: 15.662 vínculos, integridade SQLite e chaves estrangeiras aprovadas; hashes das tabelas anteriores preservados. Serviço 0.2.1 ativo com um único espaço, PP Treta, e 1.021 referências no grafo.
- Integridade SQLite aprovada. Migração medida em 0,149 s; grafo de 1.021 referências em 0,207 s nesse ensaio.
- Conferidos visualmente seletor, espaço vazio, referência compartilhada, escolhas combinadas e interface móvel clara/escura.
- Backup anterior à migração: `_saida/repertorio-qa/espacos/antes-dos-espacos.zip`, 650.391.824 bytes, 1.413 entradas verificadas por SHA-256. Inclui banco e 1.412 arquivos gerenciados; os originais externos continuam nos caminhos existentes.
- Evidências locais: `_saida/repertorio-qa/espacos/`. O banco, o backup e as capturas não entram no Git.

## Operação e recuperação

Atualizar o app aberto com ⌘R. O aplicativo nativo não precisa ser recompilado. O serviço limita o encerramento das conexões abertas a cinco segundos, para que o monitor consiga reiniciá-lo.

Para reverter a migração, encerrar o app e o serviço, recuperar também o código anterior e restaurar o backup com `./app/run.sh restore _saida/repertorio-qa/espacos/antes-dos-espacos.zip`. Reabrir o app somente depois da restauração. Não executar código anterior sobre o banco com a migração nova.

A próxima ação de uso é criar GrowMate pelo seletor e indicar quais referências deseja adicionar ou compartilhar.

## Ajuste solicitado em 18/10/2026

Removidas confirmação adicional e restauração de espaços. O botão Excluir atua diretamente; a API rejeita `deleted=false`, o MCP expõe `delete_workspace` e a CLI usa `delete-workspace`. Excluir referências individualmente continua usando a lixeira do respectivo espaço. A mudança não altera o esquema do banco nem exclui espaços existentes automaticamente.

Validação do ajuste: 15 testes pertinentes do servidor e 14 testes de navegador aprovados, build TypeScript/Vite aprovado e captura móvel conferida. Os testes validam exclusão imediata, rejeição de restauração, preservação de arquivos, referências compartilhadas e histórico, reutilização do nome e exclusão do último espaço.
