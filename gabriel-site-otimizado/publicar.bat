@echo off
setlocal
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"
title Publicar o site gabrieldiniztrafego.com.br
echo.
echo  ============================================================
echo   PUBLICAR O SITE  (gera, confere e so depois publica)
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

rem ---------- 4. Gerar o site
echo.
echo  [1/3] Gerando o site...
%PY% src\build.py
if errorlevel 1 goto :errobuild

rem ---------- 5. Conferir o resultado
echo.
echo  [2/3] Conferindo se esta tudo certo...
%PY% src\tools\conferir-dist.py
if errorlevel 1 goto :erroconf

rem ---------- 6. Confirmar e publicar
echo.
echo  [3/3] Tudo conferido. Nada foi publicado ainda.
set "R="
set /p R= Digite S e tecle Enter para PUBLICAR AGORA (so Enter cancela): 
if /i not "%R%"=="S" goto :cancelado
echo.
echo  Publicando...
call npx --yes wrangler deploy
if errorlevel 1 goto :errodeploy
echo.
echo  ============================================================
echo   PRONTO. O site foi publicado.
echo   Confira em aba anonima: https://gabrieldiniztrafego.com.br/blog/
echo   e tambem https://gabrieldiniztrafego.com.br/forms/ (deve abrir normal).
echo  ============================================================
goto :fim

:errobuild
echo.
echo  ERRO: o site NAO foi gerado e NADA foi publicado.
echo  Leia acima a linha "ERROS" (ela diz o arquivo e o campo que falta) e corrija o artigo.
goto :fim
:erroconf
echo.
echo  ERRO: a conferencia encontrou problema. NADA foi publicado. Leia as linhas acima.
goto :fim
:errodeploy
echo.
echo  ERRO: a publicacao falhou. Se pediu login, rode: npx wrangler login   e tente de novo.
goto :fim
:cancelado
echo.
echo  Cancelado. Nada foi publicado.
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
