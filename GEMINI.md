@./AGENTS.md

## Só para o Gemini CLI

- Na manutenção de performance, preserve o visual aprovado e consulte `docs/REPERTORIO-DESEMPENHO.md` e o checkpoint em `docs/RETOMADA.md`. As regras de espaços, Skills e reordenação dos nove templates estão em `AGENTS.md`; use os testes de consultas em lote e persistência da câmera para evitar regressões.

- O MCP do Repertório já está registrado no escopo do usuário (`~/.gemini/settings.json`), feito com:

  ```sh
  gemini mcp add -s user -t http repertorio http://127.0.0.1:8766/mcp
  ```

  `gemini mcp list` confere a conexão e `/mcp`, dentro da sessão, lista as ferramentas (`start_context`, `search_references`, `get_reference`, `build_inspiration_pack`, `get_pack`...).
- Se aparecer desconectado, o serviço estava fora do ar quando a sessão começou: o app do Repertório o religa em até 30 s; abra uma nova sessão. Enquanto isso, use o plano B (`./app/run.sh search "pedido" --workspace ID_DO_ESPACO --prancha` e abra a imagem indicada em Prancha) e avise o usuário.
