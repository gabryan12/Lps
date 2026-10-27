"""Agente de corte: tira silêncios, vícios de linguagem e trechos marcados, sem cortar dentro de palavra.

python cortar.py SLUG [--entrada base.mp4] [--pausa-max 0.30]
Lê palavras.json (+ cortes_manuais.json opcional: [{"deMs":..,"ateMs":..,"motivo":".."}]).
Gera edl.json, cortado.mp4 (ou cortado.wav no modo sem vídeo) e palavras_cortadas.json.
"""
import argparse
import re
import tempfile
from pathlib import Path

from comum import ler, projeto, rodar, salvar, sonda

VICIOS = {"hum", "hmm", "humm", "ahn", "ãh", "ã", "eh", "éé", "ééé", "aa", "aaa", "eee"}


def limpa(t: str) -> str:
    return re.sub(r"[^\wà-ú]", "", t.lower())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--entrada", default="base.mp4")
    ap.add_argument("--pausa-max", type=float, default=0.30, help="pausas maiores que isso (s) viram corte")
    ap.add_argument("--pad-antes", type=float, default=0.05)
    ap.add_argument("--pad-depois", type=float, default=0.08)
    a = ap.parse_args()
    p = projeto(a.slug)
    entrada = p / a.entrada
    palavras = ler(p / "palavras.json")
    if not palavras:
        raise SystemExit("palavras.json vazio: rode transcrever.py antes")
    manuais = ler(p / "cortes_manuais.json", [])
    tem_video = any(s["codec_type"] == "video" for s in sonda(entrada)["streams"])
    total = float(sonda(entrada)["format"]["duration"])

    def removida(w):
        if limpa(w["text"]) in VICIOS:
            return "vicio"
        for c in manuais:
            if w["startMs"] < c["ateMs"] and w["endMs"] > c["deMs"]:
                return c.get("motivo", "manual")
        return None

    mantidas, removidas = [], []
    for w in palavras:
        motivo = removida(w)
        (removidas if motivo else mantidas).append({**w, "motivo": motivo} if motivo else w)

    # Agrupa palavras mantidas em trechos contínuos (quebra em pausa longa ou palavra removida no meio)
    trechos, atual = [], []
    idx = {id(w): i for i, w in enumerate(palavras)}
    for w in mantidas:
        if atual:
            ant = atual[-1]
            pulou = idx[id(w)] - idx[id(ant)] > 1
            if pulou or (w["startMs"] - ant["endMs"]) / 1000 > a.pausa_max:
                trechos.append(atual)
                atual = []
        atual.append(w)
    if atual:
        trechos.append(atual)

    # Padding sem invadir o trecho vizinho
    segs = []
    for i, t in enumerate(trechos):
        ini = t[0]["startMs"] / 1000 - a.pad_antes
        fim = t[-1]["endMs"] / 1000 + a.pad_depois
        if i > 0:
            ini = max(ini, (trechos[i - 1][-1]["endMs"] / 1000 + t[0]["startMs"] / 1000) / 2)
        if i + 1 < len(trechos):
            fim = min(fim, (t[-1]["endMs"] / 1000 + trechos[i + 1][0]["startMs"] / 1000) / 2)
        segs.append({"inicio": round(max(0, ini), 3), "fim": round(min(total, fim), 3), "palavras": t})

    # Renderiza cada trecho com fade de 30 ms e junta sem reencodar
    ext = "mp4" if tem_video else "wav"
    with tempfile.TemporaryDirectory() as tmp:
        lista = Path(tmp) / "lista.txt"
        linhas = []
        for i, s in enumerate(segs):
            d = s["fim"] - s["inicio"]
            out = Path(tmp) / f"s{i:03d}.{ext}"
            fades = f"afade=t=in:st=0:d=0.03,afade=t=out:st={max(0, d - 0.03):.3f}:d=0.03"
            cmd = ["ffmpeg", "-y", "-ss", f"{s['inicio']:.3f}", "-i", str(entrada), "-t", f"{d:.3f}", "-af", fades]
            if tem_video:
                cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                        "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000"]
            else:
                cmd += ["-vn", "-ac", "1", "-ar", "48000"]
            rodar(cmd + [str(out)])
            linhas.append(f"file '{out}'")
        lista.write_text("\n".join(linhas))
        rodar(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lista), "-c", "copy", str(p / f"cortado.{ext}")])

    # Remapeia as palavras para a linha do tempo nova
    offset, novas, edl = 0.0, [], []
    for s in segs:
        for w in s["palavras"]:
            ini = round((w["startMs"] / 1000 - s["inicio"] + offset) * 1000)
            fim = round((w["endMs"] / 1000 - s["inicio"] + offset) * 1000)
            novas.append({**w, "startMs": ini, "endMs": fim, "timestampMs": (ini + fim) // 2})
        edl.append({"inicio": s["inicio"], "fim": s["fim"], "saida": round(offset, 3),
                    "texto": "".join(w["text"] for w in s["palavras"]).strip()})
        offset += s["fim"] - s["inicio"]

    salvar(p / "palavras_cortadas.json", novas)
    salvar(p / "edl.json", {"entrada": a.entrada, "saida": f"cortado.{ext}", "duracao_original": round(total, 3),
                            "duracao_final": round(offset, 3), "segmentos": edl,
                            "removidas": [{"text": w["text"], "startMs": w["startMs"], "motivo": w["motivo"]} for w in removidas]})
    print(f"ok: {len(segs)} trechos, {total:.1f}s -> {offset:.1f}s, {len(removidas)} palavras removidas")


if __name__ == "__main__":
    main()
