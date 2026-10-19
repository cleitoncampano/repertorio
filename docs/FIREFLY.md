# Firefly no Chrome

Geração e download pela conta já autenticada em uma aba do Adobe Firefly. Não usa API, chaves, cookies exportados ou arquivos de autenticação. O Chrome precisa permitir JavaScript de Eventos da Apple, como já estava configurado nesta sessão.

```sh
python3 ferramentas/firefly.py status
python3 ferramentas/firefly.py generate --prompt-file _saida/palestra-cx-ia-codex/anuncio-firefly-prompt.txt
python3 ferramentas/firefly.py status
python3 ferramentas/firefly.py download --out _saida/meu-trabalho/imagem.png
```

`generate` usa Firefly Image 5, retrato e a opção 2K da interface. Aceita `--resolution 1K` e `--ratio square` ou `--ratio widescreen`. Não envia outra geração enquanto a interface indica processamento. Aguarde a conclusão no `status` antes de baixar. `download` usa o botão normal do Firefly, identifica somente o novo arquivo Firefly em Downloads e copia para o destino; não sobrescreve arquivos existentes. `--index` escolhe outro resultado visível, começando em zero.

O serviço de geração, os créditos e eventuais avisos continuam sendo controlados pelo Firefly. Confira as dimensões do arquivo: nesta primeira geração, o seletor indicava 2K, mas o PNG baixado tinha 896 × 1152 pixels. O tamanho real está registrado em `imagens.json`.

## Correção de foco verificada em 18/10/2026

O comando comum `execute javascript` do Chrome roda em um contexto isolado, sem as propriedades dos componentes da aplicação. O controle usa um comando `javascript:` no contexto da própria página, com retorno restrito a um atributo de diagnóstico.

Um aviso introdutório fechado deixava um `SP-OVERLAY` com `open=false`, `state=closed` e a captura de foco ativa. Isso cancelava os cliques antes do botão Gerar, inclusive os eventos nativos de mouse. O script libera somente essa captura quando o componente pertence a `FIREFLY-INTRO-MODAL-DIALOG` e já está fechado. Não fecha modais abertos nem altera validações, plano, créditos ou autenticação.

Depois da correção, geração e download do anúncio foram concluídos sem clique do usuário. O script é específico para a interface atual do Firefly; quando os componentes mudarem, confira a tela e ajuste os seletores antes de reenviar uma geração.

## Resultado aplicado

`_saida/palestra-cx-ia-codex/img/anuncio-academia-firefly.png`, no celular do slide 15. Cena fictícia em preto e branco, com aluno treinando e orientação de um professor. Prompt em `anuncio-firefly-prompt.txt`, procedência e hash em `imagens.json`. HTML editável, HTML offline e PDF atualizados; capturas de conferência em `_ver/firefly/`.
