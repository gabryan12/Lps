"""Transcrição palavra a palavra com Whisper local (faster-whisper, grátis, roda em CPU).

python transcrever.py SLUG [--arquivo base.mp4] [--modelo small]
Gera palavras.json no formato de legenda do Remotion (ms, texto com espaço na frente).
"""
import argparse

from comum import projeto, salvar


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--arquivo", default="audio.wav")
    ap.add_argument("--saida", default="palavras.json")
    ap.add_argument("--modelo", default="small", help="tiny/base/small/medium; small é o melhor custo-benefício em CPU")
    a = ap.parse_args()
    p = projeto(a.slug)

    from faster_whisper import WhisperModel

    modelo = WhisperModel(a.modelo, device="auto", compute_type="int8")
    roteiro = p / "roteiro.txt"
    dica = roteiro.read_text(encoding="utf-8")[:800] if roteiro.exists() else None
    segmentos, _ = modelo.transcribe(str(p / a.arquivo), language="pt", word_timestamps=True,
                                     initial_prompt=dica, vad_filter=False)
    palavras = []
    for seg in segmentos:
        for w in seg.words:
            ini, fim = round(w.start * 1000), round(w.end * 1000)
            palavras.append({"text": " " + w.word.strip(), "startMs": ini, "endMs": fim,
                             "timestampMs": (ini + fim) // 2, "confidence": round(w.probability, 3)})
    salvar(p / a.saida, palavras)
    print(f"ok: {len(palavras)} palavras em {p / a.saida}")


if __name__ == "__main__":
    main()
