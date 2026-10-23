@echo off
rem Dois cliques: na primeira vez, prepara o Repertorio; depois liga o servico e abre o navegador.
rem Se o servico ja estiver ligado, so abre a pagina. Feche esta janela para desligar.
if not exist "%~dp0.venv\Scripts\python.exe" (
  echo Primeira vez: preparando o Repertorio. Leva alguns minutos e precisa de internet.
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup.ps1"
  if errorlevel 1 (
    echo.
    echo A preparacao nao terminou. Leia a mensagem acima.
    pause
    exit /b 1
  )
)
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run.ps1" serve --abrir
pause
