@AGENTS.md

## Só para o Claude Code

- Na manutenção de performance, preserve o visual aprovado e consulte `docs/REPERTORIO-DESEMPENHO.md` e o checkpoint em `docs/RETOMADA.md`. As regras de espaços, Skills, organização do mapa, tela grande e reordenação dos nove templates estão em `AGENTS.md`; use os testes de consultas em lote, persistência da câmera e sobreposição de capas para evitar regressões.

- O MCP do Repertório está registrado no escopo do usuário (`claude mcp add --transport http -s user repertorio http://127.0.0.1:8766/mcp`). As ferramentas aparecem como `mcp__repertorio__*`. Se não aparecerem, a sessão começou com o serviço fora do ar: reconecte com `/mcp` ou use o plano B do bloco do Repertório.
- A prancha de `search_references` e a imagem de `get_reference(include_image=true)` chegam direto na conversa. Pranchas do `buscar.py`, do `run.sh search --prancha` e capturas do `ver.py` são arquivos: abra com a ferramenta de leitura de arquivos.
- O hook de travessão desta conta recusa o caractere e também o escape `\u2014` escrito no comando. Em código, gere com `chr(0x2014)`.
- Para capturas da interface com Playwright, use o Chromium já instalado em `~/Library/Caches/ms-playwright/chromium-*/` (passe em `executablePath` ou `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`).
- Comandos que apagam pastas inteiras costumam ser recusados pela permissão desta conta: prefira nomes novos ou mover para a pasta temporária da sessão.
- Para vídeo, carregue a skill `hyperframes` antes de construir e use `npx hyperframes` (versão 0.8.186 testada no kit). Para ver um MP4 como o agente vê, gere a prancha com `repertorio.motion.storyboard` (`PYTHONPATH=app/server`) e abra a imagem com a ferramenta de leitura.
- O Chromium do Playwright toca H.264; o WebKit instalado fica em `~/Library/Caches/ms-playwright/webkit-2359/pw_run.sh` (passe em `executablePath`) e serve para conferir o comportamento do app do Mac.
- No app do Mac, a tela cheia do navegador pode estar desligada no WebKit (não foi conferido dentro do app); nesse caso, o F do player cobre a janela inteira. Liberar exige recompilar o app com a preferência de tela cheia do WKWebView, e recompilar pede de novo a permissão de Documentos: avise o usuário antes.
- Guias novos por agentes: as instruções estão em `dados/_trabalho/INSTRUCOES-GUIAS-IMAGEM.md` (imagens) e `dados/motion/_trabalho/guias/INSTRUCOES-GUIAS.md` (vídeos); os dados de cada grupo saem de `ferramentas/incorporar_prompt_motion.py guias` e do banco. Valide traços e links antes de salvar.
