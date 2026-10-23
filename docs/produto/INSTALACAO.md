# Instalar e começar

O Repertório roda no computador. Em Mac e Windows, você pode acessar pelo navegador. O aplicativo do Mac é uma opção adicional e usa a mesma biblioteca local.

## Antes de instalar

Escolha uma pasta permanente para o produto. A primeira preparação usa internet para instalar o ambiente Python e as dependências. Instale o [uv pelo guia oficial](https://docs.astral.sh/uv/getting-started/installation/). O script prepara Python 3.12, se necessário.

Se o pacote já contém `app/web/dist/index.html`, a interface está compilada. Se estiver trabalhando a partir do código-fonte, instale também [Node.js](https://nodejs.org/en/download) 22.12 ou superior e [pnpm](https://pnpm.io/installation) 11.

## Mac, no navegador

No terminal, dentro da pasta do produto:

```sh
./app/setup.sh
./app/run.sh serve
```

Abra **http://127.0.0.1:8766/?view=guide**. Mantenha o terminal aberto durante o uso. Ctrl+C encerra o serviço iniciado por esse terminal.

O primeiro preparo cria uma biblioteca vazia, com o espaço “Meu repertório”. Repetir a preparação preserva o acervo existente; ela não importa os materiais particulares de desenvolvimento.

## Mac, com o aplicativo opcional

Depois da preparação, gere o aplicativo na própria instalação do cliente, usando as ferramentas de linha de comando do Xcode:

```sh
./app/mac/build.sh "$HOME/Applications/Repertório.app"
```

Abra `Repertório.app`. Ele mostra a mesma interface em uma janela própria e mantém o serviço em execução. Você também pode usar o navegador ao mesmo tempo. O build usa a arquitetura do Mac em que é executado, com macOS 13 ou superior.

Ao gerar ou substituir o aplicativo, o macOS pode pedir novamente acesso à pasta Documentos. O aplicativo gerado localmente não é um instalador comercial assinado e notarizado. Essa etapa de distribuição permanece em preparação.

## Windows, no navegador

Abra PowerShell na pasta do produto:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\app\setup.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\app\run.ps1 serve
```

Abra **http://127.0.0.1:8766/?view=guide**. Depois do primeiro preparo, também pode usar `app\Iniciar Repertorio.cmd` para iniciar o serviço e acessar o endereço no navegador. A janela do serviço permanece aberta durante o uso; Ctrl+C encerra o processo.

Os comandos usam a política de execução somente naquele processo do PowerShell. Eles não mudam a configuração permanente da máquina. Políticas administrativas de uma organização podem prevalecer; consulte a [documentação da Microsoft](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.5).

## Sua primeira referência

1. Abra **Conheça o Repertório** para entender o fluxo e **Espaços** para organizar seus temas.
2. Em **Conectar agentes**, cadastre a pasta do seu projeto e conecte um agente compatível com MCP. Os comandos aparecem no próprio app.
3. No projeto da produção, peça ao agente que cadastre arquivos próprios ou autorizados no espaço escolhido, com uma explicação da ideia e de como aplicar o recurso.
4. Para uma criação, peça referências, confira as que o agente indicar e continue no projeto de destino.

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
