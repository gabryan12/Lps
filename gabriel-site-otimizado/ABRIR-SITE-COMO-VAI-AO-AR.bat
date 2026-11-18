@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo.
echo  SITE COMO VAI AO AR (sem rascunhos). So voce ve, no seu computador.
echo  O navegador vai abrir em http://localhost:5001
echo  Para parar, feche esta janela.
echo.
start "" http://localhost:5001
npx --yes serve dist -l 5001 --no-clipboard
pause
