@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo.
echo  PREVIA PRIVADA do site (inclui os rascunhos). So voce ve, no seu computador.
echo  O navegador vai abrir em http://localhost:5000
echo  Para parar, feche esta janela.
echo.
start "" http://localhost:5000
npx --yes serve previa -l 5000 --no-clipboard
pause
