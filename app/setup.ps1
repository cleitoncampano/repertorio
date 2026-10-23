$ErrorActionPreference = 'Stop'
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host 'Falta o uv, que prepara o Python do Repertorio.'
    Write-Host 'Instale pelo guia oficial: https://docs.astral.sh/uv/getting-started/installation/'
    Write-Host 'Depois, feche esta janela e abra de novo.'
    exit 1
}
$repertorioPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
Push-Location $PSScriptRoot
try {
    if (-not (Test-Path $repertorioPython)) {
        & uv venv .venv --python 3.12
        if ($LASTEXITCODE -ne 0) { throw 'Nao foi possivel preparar o Python.' }
    }
    $repertorioLock = 'requirements.lock'
    if (Test-Path (Join-Path $PSScriptRoot '..\.git')) { $repertorioLock = 'requirements-dev.lock' }
    & uv pip sync --python $repertorioPython $repertorioLock
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
    Write-Host 'Pronto. Para abrir, de dois cliques em app\Iniciar Repertorio.cmd.'
} finally { Pop-Location }
