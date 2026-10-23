# Instalar e começar

O Repertório roda no computador. Em Mac e Windows, você pode acessar pelo navegador. O aplicativo do Mac é uma opção adicional e usa a mesma biblioteca local.

## Antes de instalar

Escolha uma pasta permanente para o programa, como Documentos. Sua biblioteca fica em outra pasta, só sua (veja [Dados e cópias](#dados-e-cópias)).

A primeira preparação usa internet e precisa do **uv**, um programa gratuito que instala o Python do Repertório: siga o [guia oficial do uv](https://docs.astral.sh/uv/getting-started/installation/). Depois de instalar o uv, feche e abra de novo o Terminal (Mac) ou a janela do iniciador (Windows).

Se o pacote já contém `app/web/dist/index.html`, a interface está compilada. Para trabalhar a partir do código-fonte, instale também [Node.js](https://nodejs.org/en/download) 22.12 ou superior e [pnpm](https://pnpm.io/installation) 11.

## Mac

Dê dois cliques em `app/Abrir Repertório.command`. Na primeira vez, ele prepara o Repertório, o que leva alguns minutos; depois, liga o serviço e abre o navegador. Mantenha a janela do Terminal aberta durante o uso: fechar a janela desliga o serviço. Se o serviço já estiver ligado, os dois cliques só abrem a página.

Se o macOS disser que não pode abrir o arquivo porque ele veio da internet, clique no arquivo com o botão direito, escolha **Abrir** e confirme. Nas versões mais novas do macOS, depois do aviso, abra **Ajustes do Sistema**, **Privacidade e Segurança**, e clique em **Abrir Mesmo Assim**. Só é preciso na primeira vez.

Pelo Terminal, dentro da pasta do produto, o resultado é o mesmo:

```sh
./app/setup.sh
./app/run.sh serve --abrir
```

A preparação cria o espaço “Meu repertório”; repeti-la preserva o que já existe. Com a biblioteca vazia, a primeira abertura mostra o guia **Conheça o Repertório**.

## Mac, com o aplicativo opcional

Depois da preparação, gere o aplicativo na própria instalação, usando as ferramentas de linha de comando do Xcode (se faltarem, o macOS oferece instalar; ou rode `xcode-select --install`):

```sh
./app/mac/build.sh "$HOME/Applications/Repertório.app"
```

Abra `Repertório.app`. Ele mostra a mesma interface em uma janela própria e mantém o serviço em execução. Você também pode usar o navegador ao mesmo tempo. O build usa a arquitetura do Mac em que é executado, com macOS 13 ou superior. Para usar outra porta, defina `REPERTORIO_PORT` ao gerar o aplicativo.

Ao gerar ou substituir o aplicativo, o macOS pode pedir novamente acesso à pasta Documentos. O aplicativo gerado localmente não é um instalador comercial assinado e notarizado. Essa etapa de distribuição permanece em preparação.

## Windows

1. Dê dois cliques em `app\Instalar Repertorio.cmd`. Ele prepara o Repertório, o que leva alguns minutos e usa internet.
2. Para abrir, dê dois cliques em `app\Iniciar Repertorio.cmd`. Ele liga o serviço e abre o navegador. Mantenha a janela aberta durante o uso: fechar a janela desliga o serviço.

Se você pular o passo 1, o `Iniciar Repertorio.cmd` faz a preparação na primeira vez. Se o Windows mostrar “O Windows protegeu o computador”, clique em **Mais informações** e em **Executar assim mesmo**. Arquivos tirados de um zip baixado também podem ser liberados assim: botão direito, **Propriedades**, marque **Desbloquear**.

Pelo PowerShell, na pasta do produto:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\app\setup.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\app\run.ps1 serve --abrir
```

Os iniciadores e esses comandos liberam a execução de scripts somente naquele processo do PowerShell. Eles não mudam a configuração permanente da máquina. Políticas administrativas de uma organização podem prevalecer; consulte a [documentação da Microsoft](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.5).

Se algo não funcionar, veja [Quando algo não funciona](PROBLEMAS.md).

## Sua primeira referência

1. Abra **Conheça o Repertório** para entender o fluxo e **Espaços** para organizar seus temas.
2. No mapa, use **Adicionar arquivos** para enviar imagens, PDFs, apresentações ou vídeos próprios ou autorizados. Cada arquivo vira uma referência do espaço aberto.
3. Em **Conectar agentes**, copie o comando que cadastra a pasta do seu projeto e o que conecta o seu agente: Claude Code, Codex, Cursor, Claude Desktop ou OpenCode.
4. No projeto, peça ao agente que complete as fichas novas, com a ideia de cada referência e como aplicá-la. Ele também pode cadastrar arquivos do projeto no espaço escolhido.
5. Para uma criação, peça referências, confira as que o agente indicar e continue no projeto de destino.

O catálogo de Skills ajuda a preparar pedidos. As habilidades e contas dos serviços de IA são instaladas ou configuradas separadamente.

## Dados e cópias

A biblioteca fica numa pasta do seu usuário, separada da pasta do programa:

- Mac: `~/Library/Application Support/Repertorio`
- Windows: `%LOCALAPPDATA%\Repertorio`

Assim, atualizar ou apagar a pasta do programa não apaga suas referências. Para usar outra pasta, configure `REPERTORIO_HOME`. Instalações anteriores, com os dados em `app/.runtime/`, continuam usando essa pasta. Originais externos continuam nos respectivos caminhos: mantenha também uma cópia desses arquivos. As criações ficam nos projetos de destino.

O serviço faz uma cópia semanal da biblioteca na pasta `Repertorio Backups`, ao lado da pasta de dados, e outra sempre que uma versão nova precisa atualizar o banco. Nada vai para a nuvem sem você escolher: para guardar as cópias em outro disco, no iCloud Drive ou no OneDrive, configure `REPERTORIO_BACKUP_DIR`. Quem já tinha cópias no iCloud Drive continua com elas lá.

Use `doctor` para ver onde estão os dados e as cópias. Para backup e restauração, consulte o [guia de operação](OPERACAO.md).

## Encerrar o serviço

No terminal em que o serviço está aberto, use Ctrl+C. De qualquer outro terminal, na pasta do produto, use `./app/run.sh stop` (Mac) ou `powershell -NoProfile -ExecutionPolicy Bypass -File .\app\run.ps1 stop` (Windows). Se usa o aplicativo do Mac, feche o aplicativo antes: ele religa o serviço enquanto estiver aberto.

## Atualizar para uma versão nova

1. Encerre o serviço, como acima.
2. Descompacte a versão nova numa pasta nova, ou substitua a pasta do programa. Sua biblioteca não fica nessa pasta.
3. Rode a preparação de novo (`./app/setup.sh` no Mac ou `setup.ps1` no Windows) e inicie o serviço. Se o banco precisar de atualização, o serviço faz uma cópia antes, em `Repertorio Backups`.
4. Se usa o aplicativo do Mac, gere-o de novo a partir da pasta nova, com `./app/mac/build.sh "$HOME/Applications/Repertório.app"`.

Se a sua biblioteca ainda está em `app/.runtime/`, dentro da pasta do programa, faça um backup antes de trocar a pasta (`backup /caminho/repertorio.zip`). Na versão nova, use `restore /caminho/repertorio.zip`: a biblioteca passa para a pasta de dados do usuário.

## Desinstalar

1. Encerre o serviço e feche o aplicativo do Mac.
2. Apague a pasta do programa e, no Mac, `Repertório.app` em Aplicativos.
3. A biblioteca e as cópias continuam guardadas para uma instalação futura. Para apagar também, use `doctor` antes de apagar a pasta do programa para ver os caminhos, e apague a pasta de dados e a pasta `Repertorio Backups`.
4. No Mac, o registro do aplicativo fica em `~/Library/Logs/repertorio.log` e também pode ser apagado.
