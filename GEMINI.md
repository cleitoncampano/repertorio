@./AGENTS.md

## Só para o Gemini CLI

- Para usar o Repertório, registre o MCP uma vez em `~/.gemini/settings.json`, mesclando com o que já existe:

  ```json
  {"mcpServers": {"repertorio": {"httpUrl": "http://127.0.0.1:8766/mcp"}}}
  ```

  Depois, `/mcp` lista as ferramentas (`start_context`, `search_references`, `get_reference`, `build_inspiration_pack`, `get_pack`...).
- Enquanto o MCP não estiver registrado, use o plano B: `./repertorio/run.sh search "pedido" --prancha` e abra a imagem indicada em Prancha. Avise o usuário que está sem o MCP.
