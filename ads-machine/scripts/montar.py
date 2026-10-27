"""Junta o trabalho dos agentes no props.json do Remotion e (opcional) renderiza.

python montar.py SLUG             -> só monta (para abrir no Studio)
python montar.py SLUG --render    -> gera projetos/SLUG/final.mp4
"""
import argparse
import os
import shutil
import subprocess

from comum import TEMPLATE, duracao, ler, projeto, salvar

ESTILO_PADRAO = {
    "corPrimaria": "#FFD400",
    "corTexto": "#FFFFFF",
    "corFundo": ["#0B0B0F", "#1C1240"],
    "fonte": "Montserrat, Arial Black, sans-serif",
    "legendaPosicao": "meio",
    "palavrasPorBloco": 3,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--saida", default="final.mp4")
    a = ap.parse_args()
    p = projeto(a.slug)
    pub = TEMPLATE / "public" / a.slug
    if pub.exists():
        shutil.rmtree(pub)
    pub.mkdir(parents=True)

    def publica(nome: str) -> str:
        shutil.copy2(p / nome, pub / os.path.basename(nome))
        return f"{a.slug}/{os.path.basename(nome)}"

    if (p / "cortado.mp4").exists():
        video, audio, base = publica("cortado.mp4"), None, p / "cortado.mp4"
    elif (p / "cortado.wav").exists():
        video, audio, base = None, publica("cortado.wav"), p / "cortado.wav"
    else:
        raise SystemExit("Nada para montar: falta cortado.mp4 ou cortado.wav (etapa de corte)")

    inserts = ler(p / "inserts.json", [])
    for ins in inserts:
        if ins.get("tipo") == "broll":
            ins["src"] = publica(ins["src"])

    props = {
        "video": video,
        "audio": audio,
        "duracaoMs": round(duracao(base) * 1000),
        "fps": 30,
        "largura": 1080,
        "altura": 1920,
        "estilo": {**ESTILO_PADRAO, **ler(p / "estilo.json", {})},
        "inserts": inserts,
        "legendas": ler(p / "legendas.json", []),
    }
    salvar(p / "props.json", props)
    print(f"ok: props.json montado ({props['duracaoMs'] / 1000:.1f}s, {len(inserts)} inserts, {len(props['legendas'])} palavras)")

    if a.render:
        cmd = ["npx", "remotion", "render", "Anuncio", str(p / a.saida), f"--props={p / 'props.json'}",
               "--codec=h264", "--crf=18", "--audio-codec=aac"]
        if os.environ.get("REMOTION_BROWSER"):
            cmd.append(f"--browser-executable={os.environ['REMOTION_BROWSER']}")
        subprocess.run(cmd, cwd=TEMPLATE, check=True)
        print(f"ok: {p / a.saida}")


if __name__ == "__main__":
    main()
