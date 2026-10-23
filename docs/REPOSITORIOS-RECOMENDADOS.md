# Repositórios recomendados

Ferramentas que o setup do Cleiton usa junto com o Repertório. O Repertório funciona sem elas; cada uma melhora uma parte do trabalho dos agentes. A aba **Repositórios** do app mostra a mesma lista.

**Para o agente:** confira primeiro o que já está instalado (comando de verificação de cada item). Instale só o que faltar, sempre pela fonte oficial indicada, e conte ao usuário o que instalou e o resultado da verificação. Não copie instalações de outro computador: binários e clones dependem do sistema.

## HyperFrames: vídeos a partir de HTML

- Repositório: https://github.com/heygen-com/hyperframes
- Para que serve: monta e renderiza em MP4 os vídeos do kit de motion (`kit/motion/`). Os agentes usam as skills `hyperframes` e `hyperframes-creative` antes de construir um vídeo.
- Requisito: Node.js 22 ou superior.
- Instalar as skills (Claude Code e Codex): `npx skills add heygen-com/hyperframes -g`
- Instalar a ferramenta, na versão testada no kit: `npm install -g hyperframes@0.8.186` (ou usar `npx hyperframes` sob demanda)
- Verificar: `hyperframes --version` deve mostrar `0.8.186`; `ls ~/.agents/skills | grep hyperframes` deve listar as skills.

## Engram: memória dos agentes

- Repositório: https://github.com/Gentleman-Programming/engram
- Para que serve: guarda decisões, pendências e próximos passos entre uma conversa e outra, num banco local (`~/.engram/`). A memória do Cleiton não vai junto: cada pessoa começa a sua.
- Versão no setup: 3.4.0.
- Instalar: baixe o binário do release oficial para o seu sistema, confira o SHA-256 com o arquivo de checksums do mesmo release e coloque em `~/.local/bin/engram` (essa pasta precisa estar no PATH).
- Uso no setup do Cleiton: pelo terminal (`engram search`, `engram save`), sem servidor MCP. Integração opcional com um agente: `engram setup claude-code` ou `engram setup codex`.
- Verificar: `engram --version`.

## RTK: economia de contexto no terminal

- Repositório: https://github.com/rtk-ai/rtk
- Para que serve: filtra o que os comandos do terminal devolvem ao agente, para gastar menos contexto. A telemetria fica desligada por padrão.
- Versão no setup: 1.0.1.
- Instalar: binário do release oficial, com o SHA-256 conferido no arquivo de checksums, em `~/.local/bin/rtk`.
- Ligar no agente: `rtk init -g` (Claude Code) ou `rtk init -g --codex` (Codex). Para desfazer, repita com `--uninstall`.
- Verificar: `rtk --version`.

## Skills de terceiros do catálogo

As skills da aba **Skills** vêm destes repositórios. Instale com `npx skills add <repositório> -g`, que grava em `~/.agents/skills` (Codex) e `~/.claude/skills` (Claude Code).

| Repositório | Skills |
| --- | --- |
| https://github.com/emilkowalski/skills | `emil-design-eng`, `apple-design`, `prototype`, `break-ui`, `mobile-native`, `animate`, `animate-expo`, `review-animations`, `improve-animations`, `find-animation-opportunities`, `animation-performance`, `animation-vocabulary`, `pick-ui-library`, `ask-sonner`, `write-swift` |
| https://github.com/Leonxlnx/taste-skill | `design-taste-frontend` |
| https://github.com/pbakaus/impeccable | `impeccable` |
| https://github.com/anthropics/skills | `frontend-design` |

Depois de instalar `design-taste-frontend`, confira se `~/.claude/skills/design-taste-frontend` abre a pasta da skill; se o atalho estiver quebrado, refaça como `ln -s ../../.agents/skills/design-taste-frontend ~/.claude/skills/design-taste-frontend`.

`imagegen` e `presentations` vêm com o Codex e não precisam de instalação. As demais skills do catálogo (`landing-page-design` e as dos métodos) não têm repositório público: são copiadas com o setup.

Para atualizar todas as skills instaladas por `npx skills`: `npx skills update`.
