$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$repertorioPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $repertorioPython)) {
    throw 'Execute app\setup.ps1 antes de iniciar o Repertorio.'
}
$repertorioServer = Join-Path $PSScriptRoot 'server'
if ($env:PYTHONPATH) {
    $env:PYTHONPATH = $repertorioServer + [IO.Path]::PathSeparator + $env:PYTHONPATH
} else {
    $env:PYTHONPATH = $repertorioServer
}
$repertorioArguments = @($args)
if ($repertorioArguments.Count -eq 0) { $repertorioArguments = @('serve') }
& $repertorioPython -m repertorio.cli @repertorioArguments
exit $LASTEXITCODE
