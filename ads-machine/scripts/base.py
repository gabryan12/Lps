"""Agente gerador de vídeo: produz a base do anúncio em 1080x1920, 30 fps, áudio normalizado.

Gravação do cliente ou vídeo de avatar:  python base.py SLUG --video entrada/gravacao.mp4
Sem rosto (fundo animado do Remotion):    python base.py SLUG --sem-rosto   (usa audio.wav)
"""
import argparse

from comum import projeto, rodar


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--video")
    ap.add_argument("--sem-rosto", action="store_true")
    ap.add_argument("--audio-separado", action="store_true", help="troca o áudio do vídeo pelo audio.wav (avatar/lip-sync)")
    a = ap.parse_args()
    p = projeto(a.slug)

    if a.sem_rosto:
        rodar(["ffmpeg", "-y", "-i", str(p / "audio.wav"), "-c", "copy", str(p / "base.wav")])
        print(f"ok: {p / 'base.wav'} (modo sem rosto: o Remotion desenha o fundo)")
        return
    if not a.video:
        raise SystemExit("Informe --video ou --sem-rosto")

    src = p / a.video if not a.video.startswith("/") else a.video
    # Preenche a tela vertical (crop central) sem distorcer
    vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p"
    cmd = ["ffmpeg", "-y", "-i", str(src)]
    if a.audio_separado:
        cmd += ["-i", str(p / "audio.wav"), "-map", "0:v:0", "-map", "1:a:0", "-shortest"]
    cmd += ["-vf", vf, "-af", "loudnorm=I=-14:TP=-1.0:LRA=11", "-ar", "48000",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", str(p / "base.mp4")]
    rodar(cmd)
    print(f"ok: {p / 'base.mp4'}")


if __name__ == "__main__":
    main()
