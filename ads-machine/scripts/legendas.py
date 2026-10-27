"""Agente de legenda: transforma palavras_cortadas.json em legendas.json para o Remotion.

python legendas.py SLUG
Aplica correcoes.json opcional ({"errado": "certo"}) para nomes de marca e termos que o Whisper erra.
"""
import argparse
import re

from comum import ler, projeto, salvar


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--entrada", default="palavras_cortadas.json")
    ap.add_argument("--sem-pontuacao", action="store_true", default=True)
    a = ap.parse_args()
    p = projeto(a.slug)
    palavras = ler(p / a.entrada)
    correcoes = {k.lower(): v for k, v in ler(p / "correcoes.json", {}).items()}

    edl = ler(p / "edl.json", {})
    limite = round(edl.get("duracao_final", 1e9) * 1000)
    saida = []
    for w in palavras:
        t = w["text"].strip()
        corrigida = t.lower().strip(".,!?;:") in correcoes
        t = correcoes.get(t.lower().strip(".,!?;:"), t)
        if a.sem_pontuacao:
            t = re.sub(r"[.,;:]+$", "", t)
        if not t or w["startMs"] >= limite:
            continue
        saida.append({"text": " " + t, "startMs": w["startMs"], "endMs": min(limite, max(w["endMs"], w["startMs"] + 80)),
                      "timestampMs": w["timestampMs"], "confidence": 1.0 if corrigida else w.get("confidence")})
    # Garante ordem e sem sobreposição
    for i in range(1, len(saida)):
        if saida[i]["startMs"] < saida[i - 1]["endMs"]:
            saida[i - 1]["endMs"] = saida[i]["startMs"]
    salvar(p / "legendas.json", saida)
    duvidosas = [w["text"].strip() for w in saida if (w["confidence"] or 1) < 0.6]
    print(f"ok: {len(saida)} palavras. Conferir (baixa confiança): {duvidosas}")


if __name__ == "__main__":
    main()
