#!/usr/bin/env python3
"""Gera a versão leve do globo para o celular.

Entrada : src/origem/globo-m-38/*.webp  (38 quadros, 600 x 545, extraídos do vídeo original)
Saída   : src/assets/globo-m2/g<NN>-<hash>.webp  (1 a cada STRIDE quadros, SEM recomprimir) + manifest.json

- Os nomes levam um hash do conteúdo: se a imagem mudar, o nome muda, então o cache longo (1 ano) nunca serve imagem velha.
- O primeiro quadro é o "poster" (imagem parada da primeira tela).
- Para refazer a partir do vídeo original, gere de novo os quadros em src/origem/ (ver FONTE-DO-GLOBO.md) e rode este script.
Uso: python3 src/tools/gerar-globo-mobile.py [STRIDE]   (padrão 2: 38 -> 19 quadros)
"""
import hashlib, json, os, shutil, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(AQUI)
ORIGEM = os.path.join(SRC, "origem", "globo-m-38")
SAIDA = os.path.join(SRC, "assets", "globo-m2")
STRIDE = int(sys.argv[1]) if len(sys.argv) > 1 else 2

quadros = sorted(f for f in os.listdir(ORIGEM) if f.endswith(".webp"))
escolhidos = quadros[::STRIDE]
if os.path.exists(SAIDA):
    shutil.rmtree(SAIDA)
os.makedirs(SAIDA)
nomes = []
for i, f in enumerate(escolhidos):
    dados = open(os.path.join(ORIGEM, f), "rb").read()
    h = hashlib.sha1(dados).hexdigest()[:8]
    nome = "g%02d-%s.webp" % (i, h)
    open(os.path.join(SAIDA, nome), "wb").write(dados)
    nomes.append(nome)
json.dump({"stride": STRIDE, "largura": 600, "altura": 545, "poster": nomes[0], "quadros": nomes},
          open(os.path.join(SAIDA, "manifest.json"), "w"), indent=1)
total = sum(os.path.getsize(os.path.join(SAIDA, n)) for n in nomes)
print("ok:", len(nomes), "quadros,", total // 1024, "KB; poster:", nomes[0])
