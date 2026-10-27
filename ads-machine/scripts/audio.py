"""Etapa 0 (orquestradora): garante audio.wav normalizado.

Com áudio do cliente:  python audio.py SLUG --arquivo entrada/locucao.m4a
Sem áudio (TTS grátis): python audio.py SLUG --tts --voz pt-BR-AntonioNeural
"""
import argparse
import asyncio

from comum import projeto, rodar


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--arquivo", help="áudio ou vídeo enviado pelo cliente")
    ap.add_argument("--tts", action="store_true", help="gera locução do roteiro.txt com edge-tts (grátis)")
    ap.add_argument("--voz", default="pt-BR-AntonioNeural", help="ex.: pt-BR-FranciscaNeural, pt-BR-ThalitaNeural")
    ap.add_argument("--velocidade", default="+8%", help="ritmo de anúncio costuma ficar entre +5% e +15%")
    a = ap.parse_args()
    p = projeto(a.slug)

    if a.tts:
        import edge_tts

        roteiro = (p / "roteiro.txt").read_text(encoding="utf-8").strip()
        bruto = p / "locucao_tts.mp3"
        asyncio.run(edge_tts.Communicate(roteiro, a.voz, rate=a.velocidade).save(str(bruto)))
        origem = bruto
    elif a.arquivo:
        origem = p / a.arquivo if not a.arquivo.startswith("/") else a.arquivo
    else:
        raise SystemExit("Informe --arquivo ou --tts")

    # Mono 48 kHz e loudness de anúncio (-14 LUFS, pico -1 dB)
    rodar(["ffmpeg", "-y", "-i", str(origem), "-vn", "-ac", "1", "-ar", "48000",
           "-af", "loudnorm=I=-14:TP=-1.0:LRA=11", str(p / "audio.wav")])
    print(f"ok: {p / 'audio.wav'}")


if __name__ == "__main__":
    main()
