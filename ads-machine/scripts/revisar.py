"""Agente revisor: confere o vídeo contra o PADRAO-ANUNCIO.md e diz quem precisa refazer o quê.

python revisar.py SLUG [--arquivo final.mp4]
Gera revisao.json e frames em revisao/ (folha de contato para inspeção visual).
"""
import argparse
import re
import shutil

from comum import ler, projeto, rodar, salvar, sonda

P = {  # limites do padrão (espelham PADRAO-ANUNCIO.md)
    "largura": 1080, "altura": 1920, "fps": 30,
    "dur_min": 10, "dur_max": 60,
    "lufs_min": -16, "lufs_max": -12, "pico_max": -1.0,
    "silencio_max": 0.6, "gancho_ms": 2000, "cta_final_ms": 4000, "sem_mudanca_max_ms": 4000,
    "palavra_max_ms": 1500, "confianca_min": 0.6,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--arquivo", default="final.mp4")
    a = ap.parse_args()
    p = projeto(a.slug)
    arq = p / a.arquivo
    props = ler(p / "props.json", {})
    edl = ler(p / "edl.json", {})
    itens = []

    def item(regra, ok, detalhe, resp, aviso=False):
        itens.append({"regra": regra, "status": "ok" if ok else ("aviso" if aviso else "falha"), "detalhe": detalhe, "responsavel": resp})

    info = sonda(arq)
    v = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    au = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    dur = float(info["format"]["duration"])
    num, den = (v or {}).get("r_frame_rate", "0/1").split("/")
    fps = round(int(num) / int(den)) if v else 0
    item("formato 1080x1920 h264", bool(v) and v["width"] == P["largura"] and v["height"] == P["altura"] and v["codec_name"] == "h264",
         f"{v and v['width']}x{v and v['height']} {v and v['codec_name']}", "finalizacao")
    item("30 fps", fps == P["fps"], f"{fps} fps", "finalizacao")
    item("tem áudio AAC", bool(au) and au["codec_name"] == "aac", au["codec_name"] if au else "sem áudio", "finalizacao")
    item("duração entre 10 e 60 s", P["dur_min"] <= dur <= P["dur_max"], f"{dur:.1f}s", "corte")
    if props:
        item("duração bate com a montagem", abs(dur - props["duracaoMs"] / 1000) < 0.25,
             f"arquivo {dur:.2f}s x props {props['duracaoMs'] / 1000:.2f}s", "finalizacao")

    # Áudio: loudness e silêncios esquecidos
    if au:
        r = rodar(["ffmpeg", "-nostats", "-i", str(arq), "-af", "ebur128=peak=true", "-f", "null", "-"])
        lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1])
        pico = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)[-1])
        item("volume -16 a -12 LUFS", P["lufs_min"] <= lufs <= P["lufs_max"], f"{lufs} LUFS", "orquestradora")
        item("pico abaixo de -1 dBFS", pico <= P["pico_max"], f"{pico} dBFS", "orquestradora", aviso=pico <= 0)
        r = rodar(["ffmpeg", "-nostats", "-i", str(arq), "-af", f"silencedetect=n=-40dB:d={P['silencio_max']}", "-f", "null", "-"])
        sil = [round(float(x), 2) for x in re.findall(r"silence_start: (-?[\d.]+)", r)]
        sil = [s for s in sil if s < dur - P["cta_final_ms"] / 1000]  # silêncio no CTA final é aceitável
        item(f"sem silêncio > {P['silencio_max']}s", not sil, f"silêncios em {sil}s" if sil else "limpo", "corte")

    # Legenda
    leg = props.get("legendas", [])
    item("legenda presente", len(leg) > 0, f"{len(leg)} palavras", "legenda")
    longas = [w["text"].strip() for w in leg if w["endMs"] - w["startMs"] > P["palavra_max_ms"]]
    item("nenhuma palavra presa na tela", not longas, str(longas) if longas else "ok", "legenda")
    duv = [w["text"].strip() for w in leg if (w.get("confidence") or 1) < P["confianca_min"]]
    item("palavras de baixa confiança conferidas", not duv, f"conferir grafia: {duv}" if duv else "ok", "legenda", aviso=True)
    fora = [w["text"] for w in leg if w["endMs"] > dur * 1000 + 50]
    item("legenda dentro da duração", not fora, str(fora) if fora else "ok", "legenda")

    # Inserts: gancho, ritmo e CTA
    ins = props.get("inserts", [])
    fora = [i["tipo"] for i in ins if i["fimMs"] > dur * 1000 + 50 or i["inicioMs"] >= i["fimMs"]]
    item("inserts dentro da duração", not fora, str(fora) if fora else "ok", "insert")
    item("gancho visual nos 2 primeiros segundos", any(i["inicioMs"] <= P["gancho_ms"] and i["tipo"] != "cta" for i in ins),
         "ok" if any(i["inicioMs"] <= P["gancho_ms"] and i["tipo"] != "cta" for i in ins) else "precisa de texto/zoom/b-roll logo no começo", "insert")
    tem_cta = any(i["tipo"] == "cta" and i["fimMs"] >= dur * 1000 - 300 and i["inicioMs"] >= dur * 1000 - 8000 for i in ins)
    item("CTA no final", tem_cta, "ok" if tem_cta else "precisa de insert tipo cta terminando no fim do vídeo", "insert")
    marcos = sorted({0, round(dur * 1000)} | {round(s["saida"] * 1000) for s in edl.get("segmentos", [])}
                    | {i["inicioMs"] for i in ins} | {i["fimMs"] for i in ins})
    buraco = max((b - a for a, b in zip(marcos, marcos[1:])), default=0)
    item(f"mudança visual a cada {P['sem_mudanca_max_ms'] // 1000}s no máximo", buraco <= P["sem_mudanca_max_ms"],
         f"maior trecho parado: {buraco / 1000:.1f}s", "insert")
    tipos = {}
    for i in ins:
        tipos.setdefault(i["tipo"], []).append(i)
    sobre = [t for t, l in tipos.items() for x, y in zip(sorted(l, key=lambda i: i["inicioMs"]), sorted(l, key=lambda i: i["inicioMs"])[1:])
             if y["inicioMs"] < x["fimMs"] and t != "zoom"]
    item("inserts do mesmo tipo não se sobrepõem", not sobre, str(sobre) if sobre else "ok", "insert")

    # Folha de contato para o revisor olhar os frames
    d = p / "revisao"
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir()
    rodar(["ffmpeg", "-y", "-i", str(arq), "-vf", f"fps=1,scale=270:-1,tile=6x{max(1, -(-int(dur) // 6))}:padding=4", "-frames:v", "1", str(d / "folha.jpg")])
    for t in (0.5, dur / 2, max(0, dur - 1)):
        rodar(["ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", str(arq), "-frames:v", "1", "-vf", "scale=540:-1", str(d / f"frame_{t:05.1f}.jpg")])

    falhas = [i for i in itens if i["status"] == "falha"]
    salvar(p / "revisao.json", {"aprovado": not falhas, "itens": itens})
    for i in itens:
        print(f"[{i['status'].upper():5}] {i['regra']}: {i['detalhe']} ({i['responsavel']})")
    print("APROVADO" if not falhas else f"REPROVADO: {len(falhas)} falha(s)")


if __name__ == "__main__":
    main()
