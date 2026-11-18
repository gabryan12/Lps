@echo off
setlocal
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"
title Previa do site (nao publica nada)
echo.
echo  ============================================================
echo   PREVIA PRIVADA (inclui rascunhos). So voce ve, neste computador.
echo   Nada e publicado.
echo  ============================================================
if not exist wrangler.jsonc (
  echo.
  echo  ERRO: este arquivo precisa ficar dentro da pasta gabriel-site, junto do wrangler.jsonc.
  goto :fim
)

rem ---------- 1. Python
set "PY="
py -3 --version >nul 2>&1 && set "PY=py -3"
if not defined PY (
  python --version >nul 2>&1 && set "PY=python"
)
if not defined PY goto :sempython
rem ---------- 2. Node
node --version >nul 2>&1
if errorlevel 1 goto :semnode
rem ---------- 3. Dependencias do build (so na primeira vez demora)
%PY% -m pip install -q -r requirements.txt
if errorlevel 1 goto :errodeps

echo.
echo  Gerando a previa...
%PY% src\build.py --previa
if errorlevel 1 goto :errobuild
echo.
echo  Abrindo o navegador em http://localhost:5000/blog/
echo  Para ENCERRAR a previa, feche esta janela.
start "" http://localhost:5000/blog/
call npx --yes serve previa -l 5000 --no-clipboard
goto :fim

:errobuild
echo.
echo  ERRO: a previa NAO foi gerada. Leia acima a linha "ERROS" (diz o arquivo e o campo) e corrija.
goto :fim

:sempython
echo.
echo  ERRO: o Python nao esta instalado neste computador (precisa so para gerar o site).
echo  Instale assim: abra https://www.python.org/downloads/ , baixe o Python 3.12 ou mais novo,
echo  e na primeira tela MARQUE "Add python.exe to PATH". Depois feche esta janela e rode de novo.
goto :fim
:semnode
echo.
echo  ERRO: o Node.js nao esta instalado. Instale em https://nodejs.org (versao LTS) e rode de novo.
goto :fim
:errodeps
echo.
echo  ERRO: nao consegui instalar as dependencias do build. Confira se ha internet e rode de novo.
goto :fim

:fim
echo.
pause
endlocal
