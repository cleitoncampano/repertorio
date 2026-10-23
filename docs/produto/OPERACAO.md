# Operar a biblioteca local

## Iniciar e conferir

No Mac, use `./app/run.sh serve` ou o aplicativo opcional. No Windows, use `app\Iniciar Repertorio.cmd` ou PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\app\run.ps1 serve
```

Abra http://127.0.0.1:8766. Os comandos `stop`, `doctor`, `backup`, `restore` e `connect` também podem ser passados ao mesmo iniciador, no lugar de `serve`. `stop` encerra o serviço; no Mac, feche antes o aplicativo, que religa o serviço enquanto estiver aberto. Atualizar e desinstalar: [guia de instalação](INSTALACAO.md#atualizar-para-uma-versão-nova).

## Backup e restauração

No Mac:

```sh
./app/run.sh doctor
./app/run.sh backup /pasta-de-backups/repertorio.zip
```

No Windows:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\app\run.ps1 doctor
powershell -NoProfile -ExecutionPolicy Bypass -File .\app\run.ps1 backup C:\Backups\repertorio.zip
```

O backup copia o banco e os arquivos gerenciados. Originais externos continuam nos respectivos caminhos e precisam de cópias próprias. Guarde os backups fora da pasta de dados. O serviço também oferece cópia semanal; o destino pode ser configurado por `REPERTORIO_BACKUP_DIR`.

Para restaurar, feche o aplicativo do Mac e encerre o serviço com `stop`. Use `restore` seguido do caminho do ZIP. A restauração verifica integridade e preserva a pasta de dados anterior. Confirme os originais externos antes de continuar.

## Projetos e dados

A biblioteca fica na pasta de dados do usuário (`~/Library/Application Support/Repertorio` no Mac, `%LOCALAPPDATA%\Repertorio` no Windows); `doctor` mostra o caminho. `REPERTORIO_HOME` define outra pasta, `REPERTORIO_PORT` define a porta e `REPERTORIO_BACKUP_DIR` define a pasta de backup. Os projetos de produção guardam seus próprios rascunhos, imagens e entregas.

Para cadastrar um projeto, use `connect /caminho/do/projeto --write-instructions`, com o iniciador do seu sistema. Depois, conecte o agente pelo MCP conforme o diálogo **Conectar agentes** no app. O serviço aceita conexões locais; a exposição pública pela internet não faz parte desta instalação.

## Demonstração

Use `demo --home app/.demo --serve` para uma biblioteca de exemplos na porta 8768. Esse modo não importa o acervo da instalação principal, não inicia processamento de materiais e não faz backups automáticos. [Roteiro e comandos](DEMONSTRACAO.md).
