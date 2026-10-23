# Vídeos de motion: por onde começar

Tudo o que o agente precisa para criar um vídeo de motion a partir do espaço Motion do Repertório.

1. **Tipo de vídeo.** Escolha o tipo e leia o guia (pelo MCP: `get_guide` com o nome). Cada guia traz números da galeria,
   estrutura cena a cena por duração, ritmo, visual, o que os melhores fazem, erros, um prompt base e as referências para abrir primeiro.

   | tipo | guia |
   |---|---|
   | Lançamento de produto | `guias/lancamento.md` |
   | Showreel de motion | `guias/showreel.md` |
   | Explicativo | `guias/explicativo.md` |
   | Dados e números | `guias/dados.md` |
   | Tipografia e mensagem | `guias/tipografia.md` |
   | Histórias e personagens | `guias/historia.md` |
   | Arte abstrata e 3D | `guias/abstrato.md` |
   | Marca e vinheta | `guias/vinheta.md` |

2. **Formato de tela.** `guias/formatos.md`: o que muda entre horizontal 16:9 (YouTube e sites), vertical 9:16 (Reels, TikTok e Shorts) e quadrado ou 4:5 (feed).
3. **O pedido.** `guias/prompt.md`: como escrever o prompt do vídeo, o que proibir e como conferir os quadros antes de renderizar.
4. **Referências.** `search_references` no espaço Motion (`format="mp4"` traz só vídeos) e `get_reference(include_image=true)` para ver a prancha de quadros. Diga ao usuário quais vídeos vai usar e por quê, com o link de cada ficha, antes de criar.
5. **Construção.** `kit/motion/LEIA-ME.md`: blocos do HyperFrames para cada movimento e o projeto inicial testado em `kit/motion/inicio/`.
6. **Acervo.** Se o usuário pedir para guardar o vídeo, `register_reference` com o MP4, `data.genres` e `data.prompt`.

Os vídeos da galeria são de terceiros: estude o movimento, o ritmo e o prompt e recrie a ideia com o tema e a identidade do projeto, sem usar a mídia.
Os guias foram escritos a partir das fichas e das pranchas da galeria (`dados/motion/`); para refazê-los com novos vídeos, as instruções estão em `dados/motion/_trabalho/guias/INSTRUCOES-GUIAS.md`.
