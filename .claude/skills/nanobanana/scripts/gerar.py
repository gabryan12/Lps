#!/usr/bin/env python3
"""Gera uma foto com o Gemini (nano banana) e salva como PNG. Sem dependências externas.

Uso:
    python gerar.py "descrição da foto" saida.png [proporcao]

proporcao: 4:5 (padrão, carrossel), 1:1, 9:16, 16:9, 3:4.
A chave vem de GEMINI_API_KEY (variável de ambiente ou arquivo .env na pasta atual).
"""
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

MODELO = os.environ.get("NANOBANANA_MODEL", "gemini-2.5-flash-image")


def chave():
    if os.environ.get("GEMINI_API_KEY"):
        return os.environ["GEMINI_API_KEY"]
    for pasta in [Path.cwd(), *Path.cwd().parents]:
        env = pasta / ".env"
        if env.exists():
            for linha in env.read_text(encoding="utf-8").splitlines():
                if linha.strip().startswith("GEMINI_API_KEY="):
                    return linha.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    descricao, saida = sys.argv[1], Path(sys.argv[2])
    proporcao = sys.argv[3] if len(sys.argv) > 3 else "4:5"

    k = chave()
    if not k:
        print("ERRO: sem GEMINI_API_KEY. Crie em aistudio.google.com/apikey e salve no .env.")
        sys.exit(2)

    corpo = {
        "contents": [{"parts": [{"text": descricao + "\n\nSem nenhum texto, letra, logo ou marca d'água na imagem."}]}],
        "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": proporcao}},
    }
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODELO}:generateContent",
        data=json.dumps(corpo).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": k},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            resposta = json.load(r)
    except urllib.error.HTTPError as e:
        detalhe = e.read().decode(errors="replace")[:500]
        if e.code == 429 or "billing" in detalhe.lower() or "quota" in detalhe.lower():
            print("ERRO: geração de imagem exige cobrança ativa no Google AI Studio (~US$ 0,07 por foto).")
        else:
            print(f"ERRO {e.code}: {detalhe}")
        sys.exit(3)

    for cand in resposta.get("candidates", []):
        for parte in cand.get("content", {}).get("parts", []):
            dados = parte.get("inlineData") or parte.get("inline_data")
            if dados and dados.get("data"):
                saida.parent.mkdir(parents=True, exist_ok=True)
                saida.write_bytes(base64.b64decode(dados["data"]))
                print(f"ok {saida}")
                return
    print("ERRO: a resposta não trouxe imagem (pode ter sido bloqueada pelo filtro de segurança).")
    sys.exit(4)


if __name__ == "__main__":
    main()
