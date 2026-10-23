# Quando algo não funciona

Cada item diz o que aparece na tela e o que fazer. Os comandos ficam na pasta do produto: no Mac, `./app/run.sh`; no Windows, `powershell -NoProfile -ExecutionPolicy Bypass -File .\app\run.ps1`, seguidos do nome do comando.

## “O serviço do Repertório não está respondendo”

O serviço local está desligado ou parou. No Mac, dê dois cliques em `app/Abrir Repertório.command` ou abra o aplicativo; no Windows, dê dois cliques em `app\Iniciar Repertorio.cmd`. A página reconecta sozinha quando o serviço volta.

Se fechou a janela do Terminal ou do iniciador, o serviço também foi desligado: abra de novo pelo iniciador.

## “A porta 8766 está ocupada por outro programa”

Outro programa usa o mesmo endereço. Feche esse programa ou escolha outra porta: defina `REPERTORIO_PORT` (por exemplo, 8770) antes de ligar o serviço e abra o endereço com a porta nova. Se usa o aplicativo do Mac, gere o aplicativo de novo com a mesma variável.

## “O Repertório já está ligado para esta biblioteca”

O serviço já está funcionando, em outra janela ou pelo aplicativo do Mac. Abra http://127.0.0.1:8766 no navegador. Para desligar, use o comando `stop`; no Mac, feche antes o aplicativo, que religa o serviço enquanto estiver aberto.

## “Falta o uv”

A preparação precisa do uv para instalar o Python do Repertório. Instale pelo [guia oficial](https://docs.astral.sh/uv/getting-started/installation/), feche o Terminal ou a janela do iniciador e abra de novo.

## O Windows bloqueou o iniciador

Na tela “O Windows protegeu o computador”, clique em **Mais informações** e em **Executar assim mesmo**. Se o arquivo veio de um zip baixado, clique nele com o botão direito, **Propriedades**, marque **Desbloquear** e confirme. Os iniciadores liberam scripts só para o Repertório; regras de uma empresa podem impedir mesmo assim, e nesse caso fale com quem cuida dos computadores.

## O Mac não abre o arquivo `.command`

Clique no arquivo com o botão direito, escolha **Abrir** e confirme. Nas versões mais novas do macOS, abra **Ajustes do Sistema**, **Privacidade e Segurança**, e clique em **Abrir Mesmo Assim**.

## O Mac pede acesso à pasta Documentos

O aviso aparece quando o aplicativo do Mac é gerado de novo e o produto está em Documentos. Permita o acesso: o serviço precisa ler os arquivos do produto.

## A página aparece em branco ou com “Algo deu errado”

Recarregue a página (⌘R no Mac, F5 no Windows). Se continuar, use **Limpar preferências e recarregar**: isso apaga só o tema, o espaço aberto e a câmera do mapa guardados no navegador, não a biblioteca.

## Um arquivo enviado não apareceu no mapa

Cada arquivo é processado em segundo plano. Se o processamento falhar, o app avisa e o item aparece em **Atividade**, com o motivo e **Tentar novamente**. Arquivos corrompidos ou PDFs com senha não geram prévia: envie outra cópia. Vídeos precisam do ffmpeg instalado no computador para gerar a prévia.

## O agente não encontra o Repertório

Confira se o serviço está ligado e repita os passos de **Conectar agentes** no app: o cadastro da pasta do projeto e o comando ou a configuração do seu agente. Depois, abra uma nova sessão do agente.

## Informações para o suporte

O comando `doctor` mostra a versão, as pastas de dados e de cópias, o estado do serviço e a integridade da biblioteca. Copie o resultado ao pedir ajuda. No Mac, o registro do aplicativo fica em `~/Library/Logs/repertorio.log`.
