# Retomada do projeto

Atualizado em 17/10/2026 (America/Sao_Paulo).

## Objetivo atual

Fazer a assinatura do Codex render mais em todos os projetos, reduzindo leituras repetidas e preservando decisões entre sessões. O usuário autorizou instalar as ferramentas escolhidas.

## Entregue

- RTK OSS 1.0.1 e Engram 3.4.0 instalados em `~/.local/bin`, com os downloads oficiais verificados por SHA-256.
- RTK registrado no perfil Codex ativo, `expresso`. Novas sessões carregam o hook; nesta sessão, usar `rtk` explicitamente nos comandos compatíveis.
- Engram usado pelo terminal sob demanda, com dados locais e separados por projeto. Não foi adicionado um catálogo MCP ou observador de IA.
- Instruções globais de continuidade registradas no perfil ativo. O manual completo deste projeto está em `biblioteca/manual-agentes.md`; o `AGENTS.md` ficou menor.
- Gravação e recuperação da memória em processos diferentes, isolamento por projeto e teste interno de confiabilidade aprovados. Detalhes em `docs/EFICIENCIA.md`.

## Contexto útil

Repertório é o app de busca e curadoria do acervo PPTRETA. A criação segue roteiro, referências, revisão do usuário e conferência visual. A biblioteca real não recebe dados de demonstração.

Há versões da palestra “Você compraria de você mesmo?”, com 24 slides. Existem alterações anteriores em `_saida/palestra-cx-ia-visual/`, variantes `palestra-cx-ia-visual-v2/` e `palestra-cx-ia-editorial/`, além de duas pastas externas de gateway. Preservar esse trabalho; ele não pertence à instalação das ferramentas.

## Próxima ação

A próxima demanda de produto ou apresentação ainda será definida pelo usuário. Começar por este checkpoint e pelo Git; consultar os manuais pertinentes e a memória somente quando o histórico ajudar. O funcionamento automático do hook em um Codex reiniciado e a economia total da assinatura ainda não foram medidos.
