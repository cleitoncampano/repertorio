$ErrorActionPreference = 'Stop'
Get-Command uv -ErrorAction Stop | Out-Null
$repertorioPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
Push-Location $PSScriptRoot
try {
    if (-not (Test-Path $repertorioPython)) {
        & uv venv .venv --python 3.12
        if ($LASTEXITCODE -ne 0) { throw 'Nao foi possivel preparar o Python.' }
    }
    & uv pip sync --python $repertorioPython requirements.lock
    if ($LASTEXITCODE -ne 0) { throw 'Nao foi possivel instalar as dependencias.' }
    if (-not (Test-Path 'web\dist\index.html')) {
        Get-Command pnpm.cmd -ErrorAction Stop | Out-Null
        Push-Location web
        $repertorioPreviousCI = $env:CI
        try {
            $env:CI = 'true'
            & pnpm.cmd install --frozen-lockfile
            if ($LASTEXITCODE -ne 0) { throw 'Nao foi possivel instalar a interface.' }
            & pnpm.cmd build
            if ($LASTEXITCODE -ne 0) { throw 'Nao foi possivel compilar a interface.' }
        } finally {
            $env:CI = $repertorioPreviousCI
            Pop-Location
        }
    }
    & (Join-Path $PSScriptRoot 'run.ps1') init
    if ($LASTEXITCODE -ne 0) { throw 'Nao foi possivel preparar a biblioteca.' }
    Write-Host 'Pronto. Execute app\run.ps1 serve e abra http://127.0.0.1:8766.'
} finally { Pop-Location }
