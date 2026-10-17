@AGENTS.md

## Só para o Claude Code

- O MCP do Repertório está registrado no escopo do usuário (`claude mcp add --transport http -s user repertorio http://127.0.0.1:8766/mcp`). As ferramentas aparecem como `mcp__repertorio__*`. Se não aparecerem, a sessão começou com o serviço fora do ar: reconecte com `/mcp` ou use o plano B do bloco do Repertório.
- A prancha de `search_references` e a imagem de `get_reference(include_image=true)` chegam direto na conversa. Pranchas do `buscar.py`, do `run.sh search --prancha` e capturas do `ver.py` são arquivos: abra com a ferramenta de leitura de arquivos.
- O hook de travessão desta conta recusa o caractere e também o escape `\u2014` escrito no comando. Em código, gere com `chr(0x2014)`.
- Para capturas da interface com Playwright, use o Chromium já instalado em `~/Library/Caches/ms-playwright/chromium-*/` (passe em `executablePath` ou `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`).
- Comandos que apagam pastas inteiras costumam ser recusados pela permissão desta conta: prefira nomes novos ou mover para a pasta temporária da sessão.
