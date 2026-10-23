# Plano: Perestroika como repertório acionável para modelos

Criado em 22/10/2026, a pedido do Cleiton. Objetivo: transformar a pasta `perestroika/` em material que agentes de IA consultam e aplicam ao criar, como foi feito com o acervo de apresentações, indo além do visual. Funciona junto com os outros espaços e também sozinho.

## O que tem na pasta

24 PDFs (cerca de 760 páginas), 1 vídeo, 10 imagens e um infográfico. O valor está em duas camadas:

1. **Método** (o mais valioso para um modelo):
   - **Experience Learning** (8 volumes): 23 pontos em 4 grupos. Conteúdo: autoralidade, tese, entrega mínima, fator dia seguinte, ignite, mapa conectivo. Forma: não é palestra é aula, design de informação, tagline, treco, fluxo TTT. Emocional: check-in e check-out, hosting, aula inaugural, happy hour e festa final, ambiente criativo, empoderamento criativo. Estrutural: arco, framework de curso, framework de aula, checkpoint, módulo vivencial, projetos, banca e go pro. Os volumes 01, 07 e 08 dão contexto e história.
   - **Mapa do Storytelling**: 8 cartas para montar uma narrativa (Catraca, Tenho dados, Didatismo na veia, Sou foda, Poder de escuta, Quebra-gelo, Vulnerabilidade, Fator surpresa), cada uma com a pergunta que o autor responde sobre o próprio tema. É um modelo pronto para preencher.
   - **Checklist Apresentações Poderosas**: planejamento (formato, tempo, público, tese), estrutura em início, meio e fim ("se não prender em 30 segundos, esquece") e design (menos é mais, cor com função, um protagonista por slide, alinhamento, fontes, imagens, animações discretas), com exemplos de antes e depois.
   - **Cursos** (Tetris, Swag, Liga os Pontos, Mood, Branding, Print Me, Yakuza, Sputnik, Scholé e o catálogo in company): métodos de criatividade, inovação, pesquisa de tendências, marca e educação corporativa.
2. **Visual**: os próprios slides têm estética editorial forte (cor chapada, títulos condensados, palavra grande sobre foto, numeração "#8"). Servem de referência visual como os de Referências.

Limites encontrados:
- Cerca de metade das páginas tem o texto só dentro da imagem: a extração precisa de leitura visual, não só de texto.
- `ChoraPPT_Curso_Completo_SP.pdf` é o folheto de venda do curso (programa, datas, preço), com pouco conteúdo de método.
- As "pranchetas" são retratos de professores, não pranchas de tipografia como diz o índice. Ficam fora do espaço visual.
- Os links do `INDICE_MATERIAIS.md` apontam para a pasta do projeto.
- É material de terceiros: a pasta continua no `.gitignore`, fora de pacotes e demonstrações. O acervo guarda as ideias reescritas com a fonte (arquivo e página), nunca cópias de slides ou textos longos.

## Recomendação: uma fonte, três portas

O conhecimento é escrito uma vez, em arquivos `.md` dentro do Repertório, e chega aos modelos por três caminhos:

| porta | quem usa | para quê |
|---|---|---|
| MCP (`get_guide`) | qualquer agente: Claude, Codex, Gemini | consultar o método no meio de qualquer criação |
| Skills | Claude Code, em qualquer projeto (inclusive o Growmate Marketing) | disparar o método sozinho quando o pedido combina |
| Espaço visual no app | busca e mapa | achar slides da Perestroika por técnica, intenção e estética, junto com Referências e Inspiração |

Agentes (subagentes) entram em um papel só: o **revisor**, que lê a peça pronta sem ter participado da criação e aponta o que falha no método. Para criar, skill e guia bastam; um agente a mais só duplicaria o trabalho.

**Junto com os outros espaços:** a tese, as 8 cartas e o checklist passam a valer em toda criação (história antes do visual, revisão no fim), e os slides entram na mesma busca de Referências e Inspiração.
**Com vida própria:** a Perestroika é o único material do acervo sobre **experiências de aprendizagem**: aula, workshop, treinamento, curso, onboarding, evento. Vira um tipo novo de entrega, com roteiro de encontro, framework, dinâmicas e slides.

## Fases

### Fase 1: leitura completa
Ler as 760 páginas (texto e imagem), página por página, em lotes paralelos. Saída: transcrição por página com o que cada slide diz e mostra, em pasta de trabalho fora do Git (`perestroika/_trabalho/`).
Pronto quando: todas as páginas lidas, páginas puladas listadas com o motivo.

### Fase 2: métodos em `.md`
Pasta `biblioteca/metodos/perestroika/`, uma ficha por conceito (cerca de 45). Cada ficha traz: o que é em duas linhas; quando usar; como aplicar em passos; perguntas que o modelo faz a si mesmo ou ao usuário; sinal de que deu certo; erro comum; exemplo da Perestroika reescrito; como vira slide, carrossel, vídeo ou aula; fonte com arquivo e página; ligação com as técnicas e guias que já existem (ex.: tese com `principios/narrativa.md`, "um protagonista por slide" com `isolamento` e `hierarquia-de-leitura`, treco com `impacto-e-destaque`, check-out e fator dia seguinte com `fechamento`).
Mais os **modelos para preencher**, a parte mais acionável para um modelo: ficha de tese (curso, tema, aula, tese, tagline, treco), as 8 cartas do storytelling, framework de curso, framework de aula com blocos e horários, perguntas de entrega mínima e fator dia seguinte.
Um `LEIA-ME.md` diz qual ficha abrir em cada situação.
Pronto quando: toda ficha com fonte; sem travessão; links válidos; um teste às cegas ("monte uma aula de 2 horas sobre X" usando só as fichas) aplica tese, treco e framework sem ajuda.

### Fase 3: portas de entrada
- **MCP:** `get_guide` passa a servir os guias da Perestroika (pequeno ajuste em `guide_files` de `app/server/repertorio/service.py` e no texto da ferramenta em `mcp_server.py`, com teste). Guias novos: `metodo-perestroika` (índice), `aula-e-workshop`, `curso-e-programa`, `encontro-e-evento`, `revisao-apresentacao`. O `start_context` lista o método como disponível.
- **Skills** no escopo do usuário, finas, apontando para as fichas (o conteúdo não é duplicado):
  1. `perestroika-tese`: antes de qualquer apresentação, vídeo ou carrossel, fecha tese, tagline, treco, as 8 cartas e o fator dia seguinte.
  2. `perestroika-experiencia`: desenha aula, workshop, treinamento, curso ou evento, com arco, frameworks, check-in, check-out e checkpoint.
  3. `perestroika-revisao`: passa o checklist numa peça pronta e devolve correções priorizadas.
- **Catálogo de Skills do app** (`app/web/src/skillCatalog.ts`): as três entram com exemplo de pedido.
- `AGENTS.md`, o bloco gerado por `cli.py` e o manual ganham uma linha cada sobre quando usar o método.
Pronto quando: `get_guide` lista os novos guias; as skills disparam com pedidos naturais ("quero montar um workshop", "revisa esse deck"); testes do servidor e da interface passam.

### Fase 4: espaço visual Perestroika
- Cada PDF vira um deck pai e cada página escolhida vira slide filho, como nas apresentações de Referências. Saem folhetos de preço, logos de clientes, retratos e páginas só de texto corrido; estimativa de 250 a 350 slides.
- Fichas com o vocabulário atual (intenções, técnicas, movimento, estética, tom), `ideia` e `como_funciona`, em lotes com prancha para conferência, mais um campo ligando o slide à ficha de método que ele ilustra.
- Importação num espaço novo **Perestroika**, com `reusable=false`. O vídeo do Chora PPT entra com prancha de quadros, como os do Motion.
Pronto quando: contagem conferida, pranchas revisadas, busca como "palavra grande sobre foto" traz slides da Perestroika ao lado de Referências e Inspiração, mapa abre com o visual e o desempenho atuais.

### Fase 5: teste real
Uma criação de verdade usando o espaço sozinho (ex.: um workshop Growmate) e outra combinada (ex.: uma palestra com Referências e Inspiração). Ajustar fichas, guias e skills com o que falhar.

### Fase 6 (opcional)
- Agente revisor em `.claude/agents/`, se a skill de revisão não bastar.
- A pasta `soap/` (checklists, infográficos, ebooks) pode seguir o mesmo caminho.

## Ordem e custo

Fases 1 a 3 entregam o que é mais acionável (método, modelos, skills) e não mexem no mapa. A fase 1 é a mais cara, pela leitura visual de 760 páginas. A fase 4 repete o trabalho de Referências e pode vir depois sem prejuízo das anteriores.

## Resultado (23/10/2026)

As cinco fases foram executadas na ordem 1, 4, 2, 3 e 5: o espaço visual entrou antes das fichas para os guias já apontarem para os slides.

- Leitura: 760 páginas, todas lidas; estudos por PDF em `_referencias/perestroika/`.
- Método: 53 fichas e modelos, 5 guias de entrada, conferidos por `ferramentas/incorporar_perestroika.py validar`.
- Skills: `perestroika-tese`, `perestroika-experiencia`, `perestroika-revisao`, no catálogo do app (categoria Método).
- Espaço Perestroika: 23 apresentações, 191 slides e 1 vídeo. O Mood SP (cópia do Mood RIO) ficou fora. Branding não virou ficha: o material só cita os conceitos.
- Teste às cegas: um workshop de 3 horas (só Perestroika) e uma palestra de 15 minutos (Referências, Inspiração e Perestroika). Os dois aplicaram tese, tagline, treco e dia seguinte. As falhas encontradas foram corrigidas: exemplos repetidos, falta de ficha de processamento e de modelo de instrumento, palestra curta sem rota, regras de tempo ambíguas.

## Pendências fora do escopo do método

Apontadas pelos testes, envolvem a busca e os guias de todos os espaços; ficam para decisão do Cleiton:
- Resolvido em 23/10/2026: a busca lia palavras comuns como filtro ("tela" virava MOSTRAR) e não achava "cronômetro" nem "chat" (ver `docs/RETOMADA.md`, Busca dos agentes). Continua pendente: `get_reference` traz uma lista longa de apresentações relacionadas só por técnica.
- Algumas fichas de slide de Referências herdam a ideia da apresentação e vêm sem `como_funciona`.
- Não há referências de interface de atendimento (chat, ticket, painel) fora do espaço Growmate, e os guias por momento citam o Growmate mesmo quando o usuário não escolheu esse espaço.
- `biblioteca/processo.md` (passo 3) ainda manda usar `roteiro.py` e `buscar.py`, que o AGENTS.md diz não refletirem a curadoria.
- Falta uma regra para dado público lembrado pelo agente (sugerir com fonte, ano e marca provisória).
