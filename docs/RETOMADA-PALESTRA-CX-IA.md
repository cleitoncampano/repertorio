# Retomada da palestra: Você compraria de você mesmo?

Atualizado em 18/10/2026. Após a recuperação do contexto, o usuário autorizou acrescentar recursos visuais dos carrosséis e finalizar. A primeira parte de 24 slides foi consolidada em `_saida/palestra-cx-ia-codex/`.

## Entrega oficial

- `_saida/palestra-cx-ia-codex/palestra-arquivo-unico.html`: arquivo independente, com imagens, fontes, falas e motor incorporados.
- `_saida/palestra-cx-ia-codex/palestra.pdf`: 24 páginas, com todas as revelações visíveis.
- `_saida/palestra-cx-ia-codex/palestra.html`: versão editável com dependências locais.
- `LEIA-ME.md`, `REFERENCIAS.md` e `VALIDACAO.json` na mesma pasta: operação, procedência visual, resultados e hashes.

Recursos acrescentados: linha contínua de jornada, estações com ícones, cartões dos três momentos, seis caminhos de descoberta, círculos e lupa, sinais para os setores e cartões de perguntas. Paleta coral, papel e preto do kit Growmate, mantendo a tipografia e as oito imagens ilustrativas da editorial. Não foram acrescentados textos ou fotografias de terceiros dos carrosséis.

O usuário delegou a seleção visual ao pedir os elementos que fizessem sentido. Seleção registrada em `ee7c76be-312c-4896-a618-e256fed3555f`, contexto `ca3449a4-fc0e-431b-9dac-9709490c6888`. Referências Simon Sinek, Hug Your Haters, Mapeamento de Experiências, Would You Do That to Your Mother? e kit de componentes. A revisão antiga continua respeitada, incluindo o corte de Vogue.

## Contexto recuperado

- A sessão de 17/10/2026 no perfil local `azship` registra o pedido de melhorar apenas o visual da primeira parte: preservar texto, conteúdo, falas, ordem e storytelling, com liberdade para imagens pertinentes.
- O usuário autorizou continuar depois de revisar a seleção `ef822873-7346-4272-8e0e-d434f48cb738`. A revisão atual no Repertório confirma Magic Masks, Nike e Table top aprovados; Vogue cortada.
- A sessão terminou durante a conferência visual, depois de montar `_saida/palestra-cx-ia-editorial/`. Não foi encontrada uma entrega final dessa versão.
- O roteiro original está em `_saida/palestra-cx-ia/palestra.html`. São 24 slides, da abertura até “Então, o que impede?”. A última fala termina com “(Continua.)”.

## Base usada nesta finalização

`_saida/palestra-cx-ia-editorial/palestra.html`.

É a versão que contém as oito imagens geradas pela ferramenta integrada, com prompts registrados em `imagens.json`: reflexo, acolhimento, atendimento, academia, cotidiano, consumo, mudança e comércio. Os arquivos estão em `img/`.

Direção: fotografias ilustrativas em preto e branco, marfim, preto e ponto laranja como elemento recorrente. Os personagens, estabelecimentos e cenas são fictícios; não representam Cleiton, o evento ou uma academia específica de Araguari.

## Verificação da versão final

- Os 185 trechos visíveis, 24 falas, passos de revelação e grupos de foco da versão final são idênticos ao original.
- Os 24 slides e 53 estados de clique foram capturados e conferidos em 1920 × 1080. Nenhum texto fora da tela ou menor que o limite da verificação; nenhum erro JavaScript ou recurso faltante.
- As 23 transições foram exercitadas em velocidade normal e capturadas. Nenhuma falha de View Transitions.
- Home, End, PageDown, tecla F para entrar e sair da tela cheia e P com falas foram verificados.
- O slide 7 foi corrigido com posicionamento específico para o título e a legenda, eliminando o conflito do seletor `last-of-type` anterior.
- O HTML único foi aberto sozinho numa pasta temporária com requisições externas bloqueadas. Carregou todas as imagens, fontes, motor e falas, com zero dependências externas. Os slides 7, 9, 18, 19 e 22 produziram capturas idênticas às da versão editável.
- O PDF tem 24 páginas de 1440 × 810 pontos. Todas foram renderizadas com Poppler e revisadas visualmente. Na impressão, as três perguntas do slide 22 aparecem legíveis ao mesmo tempo.
- Rotinas: `ferramentas/finalizar_palestra_cx_ia.py`, `ferramentas/conferir_palestra_cx_ia.cjs` e `ferramentas/exportar_palestra_cx_ia.cjs`. Capturas em `_saida/palestra-cx-ia-codex/_ver/`, fora do Git.

## Uso e ensaio

Abrir o HTML único em Chrome ou Edge. F abre a tela cheia; P abre as falas e o cronômetro; setas, espaço e PageDown respeitam cada revelação antes de avançar o slide. O PDF serve para consulta e compartilhamento.

A revisão visual, os cliques e a exportação estão concluídos. A duração ainda depende de um ensaio da fala do apresentador. A agenda prevê 10 minutos para a parte de experiência do cliente.

## Outras versões

- `_saida/palestra-cx-ia-visual/`: preserva os 185 trechos e as 24 falas, com mudanças nos passos de alguns slides.
- `_saida/palestra-cx-ia-visual-v2/`: ainda tem 24 slides, mas contém 331 trechos visíveis; altera textos em vários slides e a fala do slide 17. Não adotar como base fiel ao pedido anterior sem uma decisão nova sobre essas mudanças.
- Os quatro PDFs encontrados nas pastas visual e visual-v2 são binariamente iguais, apesar de os HTMLs serem diferentes. Não usá-los para concluir qual visual é o mais recente.

## Para concluir a palestra inteira

A agenda do slide 4 anuncia cinco blocos. O material disponível desenvolve apenas o primeiro, experiência do cliente e a jornada de descoberta da academia.

Ainda precisam de roteiro e slides: inteligência artificial; encontro entre CX e IA; como fazer na prática; cases; conclusão da palestra. O slide 24 é uma passagem para a continuação, não o encerramento final.

Para desenvolver esses blocos, recuperar ou receber a continuação da fala e definir os cases e a duração total. O usuário pode fornecer ideias soltas ou transcrição; não pedir uma estrutura pronta.

## Próxima ação

Usar a pasta final para apresentar a primeira parte. Para criar os blocos restantes, recuperar ou receber a continuação da fala, os cases e a duração total. Preservar as versões anteriores e a fala já revisada.
