"""Alinhamento forçado aproximado (fallback quando o Whisper não baixa).

python alinhar_roteiro.py SLUG [--arquivo base.wav]
Mede os silêncios do áudio real (ffmpeg silencedetect), casa cada fronteira de cláusula do roteiro com o
silêncio mais próximo (em fração de caracteres) e distribui as palavras de cada cláusula proporcionalmente
aos caracteres, só dentro do tempo de fala. Sincronia por palavra é APROXIMADA. Gera palavras.json.
"""
import argparse
import re

from comum import duracao, projeto, rodar, salvar


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--arquivo", default="base.wav")
    ap.add_argument("--min", type=float, default=0.12, help="silêncio mínimo (s)")
    a = ap.parse_args()
    p = projeto(a.slug)
    arq = p / a.arquivo
    total = duracao(arq)
    out = rodar(["ffmpeg", "-i", str(arq), "-af", f"silencedetect=n=-40dB:d={a.min}", "-f", "null", "-"])
    ini = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    fim = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    sil = list(zip(ini, fim[: len(ini)]))
    if len(fim) < len(ini):
        sil.append((ini[-1], total))
    # intervalos de fala
    falas, t = [], 0.0
    for s, e in sil:
        if s - t > 0.03:
            falas.append((t, s))
        t = e
    if total - t > 0.03:
        falas.append((t, total))
    # cláusulas do roteiro
    txt = (p / "roteiro.txt").read_text(encoding="utf-8")
    clausulas = [c.split() for c in re.findall(r"[^.,:;?!\n]+[.,:;?!]?", txt) if c.split()]
    # Só pontuação forte/média separa trechos de fala; vírgula tem pausa curta e é tratada como fronteira candidata
    nchar = [sum(len(re.sub(r"\W", "", w)) for w in c) for c in clausulas]
    tot_c = sum(nchar)
    dur_fala = sum(e - s for s, e in falas)
    # fala acumulada no início de cada silêncio (fronteira candidata entre falas)
    acum, c = [], 0.0
    for s, e in falas[:-1]:
        c += e - s
        acum.append(c)
    # fronteiras de cláusula (fração de fala), casadas de forma monotônica com os silêncios
    fronteiras, cum = [], 0
    for n in nchar[:-1]:
        cum += n
        fronteiras.append(cum / tot_c * dur_fala)
    usados, ult = [], -1
    for f in fronteiras:
        cand = [(abs(acum[i] - f), i) for i in range(ult + 1, len(acum))]
        if not cand:
            usados.append(None)
            continue
        d, i = min(cand)
        if d < 0.6:  # tolerância: ~0,6 s de fala
            usados.append(i)
            ult = i
        else:
            usados.append(None)
    # tempo de fala -> tempo real
    def real(tf):
        c = 0.0
        for s, e in falas:
            if tf <= c + (e - s) + 1e-9:
                return s + (tf - c)
            c += e - s
        return falas[-1][1]

    # limites (em tempo de fala) de cada cláusula: silêncio casado ou proporcional
    lim = [0.0]
    for k, u in enumerate(usados):
        lim.append(acum[u] if u is not None else fronteiras[k])
    lim.append(dur_fala)
    palavras, rel = [], []
    for k, c in enumerate(clausulas):
        pesos = [max(1, len(re.sub(r"\W", "", w))) for w in c]
        span = lim[k + 1] - lim[k]
        x = lim[k]
        for w, pw in zip(c, pesos):
            d = span * pw / sum(pesos)
            s_ms, e_ms = round(real(x) * 1000), round(real(x + d - 1e-6) * 1000)
            palavras.append({"text": " " + w, "startMs": s_ms, "endMs": max(e_ms, s_ms + 1),
                             "timestampMs": (s_ms + e_ms) // 2, "confidence": 1.0, "alinhamento": "aproximado"})
            x += d
    salvar(p / "palavras.json", palavras)
    print(f"ok: {len(palavras)} palavras, {len(falas)} trechos de fala, {sum(u is not None for u in usados)}/{len(usados)} fronteiras casadas com silêncio")
    for k, u in enumerate(usados):
        print(" ".join(clausulas[k][-2:]), "->", f"{real(acum[u]):.2f}s" if u is not None else "sem silêncio (proporcional)")


if __name__ == "__main__":
    main()
