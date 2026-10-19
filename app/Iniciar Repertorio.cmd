@echo off
echo Repertorio local. Acesse http://127.0.0.1:8766 no navegador.
echo Mantenha esta janela aberta durante o uso.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run.ps1" serve
pause
