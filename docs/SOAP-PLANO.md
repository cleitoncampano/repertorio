# Plano: SOAP como repertório acionável para modelos

Criado em 23/10/2026, a pedido do Cleiton.

## Contexto

Na sessão de 22 e 23/10/2026, o material da escola Perestroika virou três portas para os agentes de IA: método em fichas `.md` servidas por `get_guide`, skills e um espaço visual no app. O Cleiton quer o mesmo para a pasta `soap/` (material da agência SOAP). Este plano diz o que já existe, o que reaproveitar, a ordem das fases e as lições do trabalho com a Perestroika.

Resultado esperado: (1) fichas de método do SOAP em `biblioteca/metodos/soap/`, com índice `metodo-soap` e guias de entrada; (2) skills só onde o SOAP cobre um trabalho que as skills da Perestroika não cobrem; (3) espaço SOAP no app com os PDFs e os templates como apresentações com slides; (4) tudo testado às cegas e salvo no Git.

## O que tem na pasta `soap/` (469 MB, fora do Git pela regra `/soap/`)

- `ebooks_e_guias/`: 55 PDFs e um zip, cerca de 1.400 páginas, quase todos 16:9. Dois grupos:
  - **Apresentações e fala** (o centro): roteiro vencedor, 11 passos de conteúdo, 9 recursos de narrativa, 12 formas de diagramação, 10 formas de ilustrar, linguagem visual de destaque (102 p), referências visuais, 15 erros, 10 sinais de apresentação chata, mitos, 10 mandamentos, ensaio (9 dicas), segurança ao apresentar, linguagem corporal (dicas e erros), anatomia do palestrante, como se destacar (63 p), falta de tempo, audiência, arquétipos de Jung, apresentação institucional, para investidores (com Endeavor), concorrência, venda, elevator pitch, convenções, evento no estado da arte, tendências 2018 e 2020, Dicas SOAP 2018 e 2019, SOAP Insights, guia básico do PowerPoint 2013.
  - **Comunicação, liderança e RH**: guia completo do RH (4 partes), papel do RH em 2020, comunicação interna, atrair e reter talentos, credibilidade do líder, por que a equipe não conta a verdade, feedback, 5 pecados da facilitação, avaliação de treinamentos, neuromarketing, SWOT/TOSW, prospecção remota, comunicação para crianças, capítulo do livro DETONE.
  - `Kit_express_para_desenvolvimento_de_projeto.zip`: uma planilha `.xls` e um template `.ppt` de aprovação de projeto.
- `checklists_e_infograficos/`: 3 PDFs (checklist de qualidade, apresentação impactante, projeto importante).
- `templates/`: 12 `.pptx` (301 slides) e 4 `.ppt` antigos: presentes SOAP 2014 a 2017, gráficos, saúde, bancos, clean e moderno, currículo, integração de funcionários, lançamento de produto, RH, Copa do Mundo, venda de soluções, conquistar recursos, educação.
- Cerca de 470 páginas não têm texto extraível (ex.: linguagem visual de destaque, como se destacar, Dicas 2018, SOAP Insights, os três checklists): exigem leitura visual. Total estimado com os templates: 1.800 páginas.

## O que já existe e deve ser reaproveitado

- `app/server/repertorio/decks.py` e `./app/run.sh import-decks --workspace ID --folder dados/<coleção>`: importa PDFs como apresentação com slides; já é genérico (campo `collection`, ids livres). Vídeos: `import-motion --folder`.
- `app/server/repertorio/service.py` (`guide_files`, `method_files`): já serve qualquer `biblioteca/metodos/<coleção>/guias/*.md` como guia e `conceitos/` e `modelos/` como `<coleção>/<ficha>`. Atenção: guias de coleções diferentes compartilham o mesmo espaço de nomes; um guia SOAP com o mesmo nome de um da Perestroika substitui o outro em silêncio.
- `app/server/repertorio/cli.py`: o bloco de instruções já cita qualquer `metodo-*.md` encontrado.
- `ferramentas/incorporar_perestroika.py` (`montar`, `pranchas`, `validar`): específico da Perestroika nas constantes (pastas, títulos, prefixo, vídeo). O script que renderizou as páginas ficou só na pasta temporária da sessão anterior e precisa ser refeito (pymupdf, 1600 px no lado maior, folhas de contato de 6 páginas com o número no canto, texto extraído por página).
- Instruções de agentes: `dados/_trabalho/INSTRUCOES-PERESTROIKA-LEITURA.md` e `INSTRUCOES-PERESTROIKA-METODOS.md`.
- Guias e skills de referência de formato: `biblioteca/metodos/perestroika/` (índice, guias, fichas, `LEIA-ME.md`) e `~/.agents/skills/perestroika-*` (ligadas em `~/.claude/skills`).
- Catálogo de Skills do app: `app/web/src/skillCatalog.ts`, ícones em `app/web/src/Skills.tsx`, e o teste `app/web/e2e/skills.spec.ts` (lista de nomes e contagem de cartões).

## Fases

### Fase 0: ferramenta e instruções (antes de ler)

1. Este plano é salvo em `docs/SOAP-PLANO.md` e vai para o Git; a execução parte dele e da `docs/RETOMADA.md`.
2. Generalizar `ferramentas/incorporar_perestroika.py` em `ferramentas/incorporar_colecao.py <coleção> <comando>`, com um dicionário de configuração por coleção (pasta de origem, pasta de trabalho, prefixo de id, títulos dos decks, vídeo opcional) e os comandos `paginas` (novo: renderiza páginas, texto e folhas de contato), `montar`, `pranchas` e `validar`. Manter `incorporar_perestroika.py` como atalho ou remover depois de provar a equivalência: rodar `montar perestroika` e conferir que `dados/perestroika/decks.jsonl` sai idêntico.
3. `validar` passa a conferir também: nomes de guia repetidos entre `biblioteca/guias`, `biblioteca/motion/guias` e `biblioteca/metodos/*/guias`; links de slide com `%23` (com `#` o app abre o deck, não o slide).
4. Templates `.ppt` e `.pptx` (16 mais o do zip): exportar para PDF pelo Keynote ou PowerPoint (osascript; o macOS pode pedir permissão de automação, avisar o usuário), em `soap/_trabalho/pdf-templates/`, e seguir como PDF.
5. Escrever `dados/_trabalho/INSTRUCOES-SOAP-LEITURA.md` e `INSTRUCOES-SOAP-METODOS.md` a partir das da Perestroika, já com as lições (seção abaixo). A lista de conceitos conhecidos começa vazia: os leitores criam ids e o redator unifica.
6. Criar `ferramentas/mcp_leitura.py`: chamada só de leitura ao MCP (`get_guide`, `search_references`, `get_reference`, `list_workspaces`), salvando imagens numa pasta; serve aos testes às cegas sem gravar contexto no acervo.

### Fase 1: leitura completa

- `incorporar_colecao.py soap paginas`, depois 9 a 10 agentes em paralelo, de 150 a 200 páginas cada, agrupados por assunto (apresentação e roteiro; design e visual; fala e performance; pitch, venda e eventos; comunicação, liderança e RH; checklists, dicas e tendências; templates). Saída em `soap/_trabalho/leitura/<slug>.jsonl` e `.md`, uma linha por página, com ficha visual para as páginas escolhidas.
- Duplicatas prováveis: Dicas 2018 e 2019, tendências 2018 e 2020, presentes SOAP de anos diferentes, partes do guia de RH. O leitor aponta o que se repete; deck sem página escolhida fica fora do mapa.
- Pronto quando: todas as páginas lidas, `.jsonl` com uma linha por página, JSON válido, só ids do vocabulário.

### Fase 2: espaço visual SOAP

- `montar` e `pranchas`; conferir as pranchas em `app/.runtime/qa/soap/`.
- `./app/run.sh backup-now`, `create-workspace SOAP`, `import-decks --workspace ID --folder dados/soap`.
- Direitos: material de terceiros, `reusable=false`. Se algum template trouxer licença de uso explícita (os "presentes SOAP" foram distribuídos como brinde), registrar no `usage_notes` e perguntar ao Cleiton antes de marcar como reutilizável.
- Pronto quando: contagem conferida, busca por um recurso visual traz slides do SOAP, mapa abre com o visual e o desempenho atuais (capturas com o Chromium em `~/Library/Caches/ms-playwright/chromium-1243/`).

### Fase 3: fichas de método

- 3 a 4 redatores em paralelo por grupo de assunto, seguindo `INSTRUCOES-SOAP-METODOS.md`, em `biblioteca/metodos/soap/conceitos/` e `modelos/`.
- Onde o SOAP e a Perestroika tratam do mesmo assunto (checklist, roteiro, erros, ensaio, eventos), a ficha SOAP traz o que é próprio do SOAP e liga para a ficha `perestroika/<ficha>`, sem repetir.
- Guias de entrada escritos à mão sobre as fichas, com nomes que não colidam com os existentes. Candidatos, a confirmar pela leitura: `metodo-soap` (índice), `apresentar-ao-vivo` (fala, corpo, segurança, ensaio, falta de tempo), `pitch-e-proposta` (investidores, concorrência, venda, elevator pitch, institucional), `comunicacao-na-empresa` (comunicação interna, feedback, liderança, RH).
- Pronto quando: `validar soap` com zero problemas, todo exemplo aplicado com tema próprio, índice citando todas as fichas.

### Fase 4: portas de entrada

- `app/server/repertorio/mcp_server.py`: uma frase no `get_guide` sobre o índice `metodo-soap` e as fichas `soap/<ficha>`; testes em `app/tests/test_decks.py` se o serviço mudar.
- Skills em `~/.agents/skills/` com link em `~/.claude/skills/`, só para trabalhos sem skill hoje. Candidatas: apresentar ao vivo e pitch ou proposta. A revisão de apresentação ganha o checklist SOAP como camada extra na skill e no guia que já existem, em vez de outra skill de revisão.
- Catálogo do app (categoria Método), `pnpm --dir app/web build`, atualizar `skills.spec.ts` (nomes e contagem).
- `AGENTS.md` (linha do SOAP em "Acervo e produção", item em "Estado atual", linha em "Onde consultar"), `biblioteca/manual-agentes.md`, `biblioteca/metodos/soap/LEIA-ME.md`, `docs/RETOMADA.md`.
- Mudou código do servidor: reiniciar o serviço encerrando o processo que escuta na 8766 (o app religa em segundos) e conferir `get_guide` pelo MCP.

### Fase 5: teste às cegas e ajustes

- Dois agentes sem contexto, com `ferramentas/mcp_leitura.py` e as skills: um usando só o espaço SOAP (ex.: pitch de 10 minutos para investidores); outro combinando Referências, Inspiração, Perestroika e SOAP (ex.: apresentação institucional com revisão). Temas fora de atendimento ao cliente com IA.
- Cada um entrega a peça e um relato (o que abriu, o que ajudou, o que faltou, contradições). Corrigir o que falhar e montar a página de leitura dos materiais para o Cleiton, como em `app/.runtime/qa/perestroika/testes/`.

## Lições da Perestroika (aplicar desde o começo)

- Dar aos redatores, já na instrução, um tema diferente por ficha para os exemplos aplicados. Na Perestroika todos escolheram atendimento com IA e os testes copiaram o exemplo.
- Conceito e modelo nunca com o mesmo nome (`framework-de-aula` e `grade-de-aula`); `validar` pega.
- Citar fichas sempre como `` `soap/<ficha>` ``, nunca pelo caminho do arquivo.
- Cada agente usa a própria pasta temporária para scripts; um leitor sobrescreveu o script de outro.
- Não criar contexto nem demanda de teste no acervo real; testes com escrita usam cópia temporária.
- Commits com `git commit -m "..." -- <caminhos>`: outra sessão pode estar trabalhando no mesmo repositório, e um `git commit` sem caminhos leva o que estiver preparado por ela. Não reintroduzir o nome antigo do acervo de apresentações em textos ou código.
- Travessão: o hook recusa o caractere e o escape no comando; em código, `chr(0x2014)`.
- Ler as pranchas antes de importar e capturar o app depois; atualizar com ⌘R no app.

## Verificação

- `app/.venv/bin/python -I ferramentas/incorporar_colecao.py soap validar` (zero problemas) e o mesmo para `perestroika`.
- `dados/perestroika/decks.jsonl` idêntico antes e depois da generalização.
- `app/.venv/bin/python -m pytest app/tests -q`, `pnpm --dir app/web test`, `pnpm --dir app/web test:e2e -- skills.spec.ts` com `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH` apontando para o Chromium 1243.
- Pelo MCP: `get_guide()` lista `metodo-soap` sem perder nenhum guia anterior; `get_guide("soap/<ficha>")` abre; `search_references` no espaço SOAP devolve prancha.
- Capturas do mapa e da tela grande do espaço SOAP; um link de slide de guia abrindo o slide certo.
- Os dois testes às cegas entregam peças que aplicam o método sem copiar exemplos.

## Andamento (atualizado em 23/10/2026, 1h35)

- Fase 0 concluída: `ferramentas/incorporar_colecao.py` (Perestroika idêntica, comandos `paginas`, `conferir`, `montar`, `pranchas`, `validar`), `ferramentas/mcp_leitura.py`, instruções `dados/_trabalho/INSTRUCOES-SOAP-*.md`. Templates em PDF em `soap/_trabalho/pdf-templates/` (PowerPoint; o de gráficos pelo Keynote, com textos sobrepostos em algumas páginas). Planilha do kit em texto: `soap/_trabalho/kit-express/Analise_de_viabilidade_do_projeto.md`. Páginas renderizadas: 75 PDFs, 1.755 páginas.
- Fase 1 concluída (1h40): 10 lotes, 1.755 páginas, `conferir` com zero problemas. Lotes em `soap/_trabalho/relatorios/lotes.md`; conclusões em `soap/_trabalho/relatorios/resultados.md`.
- Fase 2 concluída (1h45): espaço SOAP `7f53adaa-6bc5-496c-815e-f6159e2baec9`, 75 apresentações e 507 slides importados, backup `repertorio-2026-10-23-013219`, capturas em `app/.runtime/qa/soap/app/`.
- Fase 3 concluída (2h40): 62 fichas e modelos em `biblioteca/metodos/soap/`, guias `metodo-soap`, `apresentar-ao-vivo`, `pitch-e-proposta`, `comunicacao-na-empresa`, camada SOAP em `revisao-apresentacao`; `validar` com zero problemas nas duas coleções. Resultados dos redatores em `soap/_trabalho/relatorios/fichas.md`.
- Fase 4 concluída: `get_guide` e bloco de instruções citam o SOAP, teste de duas coleções, skills `soap-fala` e `soap-pitch` (catálogo do app), camada SOAP na `perestroika-revisao`, AGENTS.md e manual; 48 testes do servidor, 61 da interface e 29 de navegador aprovados; serviço reiniciado.
- Fase 5 em andamento: dois testes às cegas (pitch da Composta só com SOAP; institucional da Movi com Referências, Inspiração, Perestroika e SOAP), entregas em `app/.runtime/qa/soap/testes/`. Para retomar: se `pitch.md` ou `institucional.md` faltarem, relançar o teste; depois corrigir o que o relato apontar e montar `materiais-do-teste.html` como o da Perestroika.
