@echo off
rem Dois cliques: prepara o Repertorio (Python e dependencias). Depois, use "Iniciar Repertorio".
echo Preparando o Repertorio. Leva alguns minutos e precisa de internet.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup.ps1"
if errorlevel 1 (
  echo.
  echo A preparacao nao terminou. Leia a mensagem acima.
  pause
  exit /b 1
)
echo.
echo Pronto. Para abrir, de dois cliques em "Iniciar Repertorio".
pause
