#!/usr/bin/env python3
"""Renderiza um carrossel 1080x1350 a partir de um JSON, desenhando o texto em HTML/CSS.

Uso:
    python render.py carrossel.json pasta_de_saida/

O JSON segue o formato descrito no SKILL.md. Cada slide vira slide-01.png, slide-02.png...
Precisa de: pip install playwright && python -m playwright install chromium
"""
import html
import json
import os
import sys
from pathlib import Path

W, H = 1080, 1350


def esc(s):
    return html.escape(str(s or "")).replace("\n", "<br>")


def cor_texto_sobre(hex_cor):
    h = hex_cor.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    luminancia = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return "#111111" if luminancia > 150 else "#ffffff"


def css(marca):
    cor = marca.get("cor", "#1f3a5f")
    fundo = marca.get("fundo", "#f6f3ee")
    texto = marca.get("texto", "#161616")
    fonte = marca.get("fonte", "Inter")
    sobre_cor = cor_texto_sobre(cor)
    fonte_url = fonte.replace(" ", "+")
    return f"""
@import url('https://fonts.googleapis.com/css2?family={fonte_url}:wght@400;600;800&display=swap');
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: {W}px; height: {H}px; }}
body {{ font-family: '{fonte}', system-ui, sans-serif; background: {fundo}; color: {texto};
  display: flex; flex-direction: column; padding: 96px 88px 150px; position: relative; overflow: hidden; }}
body.s-capa, body.s-cta {{ background: {cor}; color: {sobre_cor}; }}
.foto {{ position: absolute; inset: 0; background-size: cover; background-position: center; }}
.foto::after {{ content: ''; position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(0,0,0,.05) 30%, rgba(0,0,0,.78) 100%); }}
body.s-foto {{ color: #fff; }}
.conteudo {{ position: relative; z-index: 1; display: flex; flex-direction: column; flex: 1; }}
.s-capa .conteudo, .s-foto .conteudo {{ justify-content: flex-end; }}
.tag {{ font-size: 30px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase;
  opacity: .75; margin-bottom: 36px; }}
h1 {{ font-size: 96px; line-height: 1.02; font-weight: 800; letter-spacing: -.02em; }}
h2 {{ font-size: 68px; line-height: 1.08; font-weight: 800; letter-spacing: -.015em; margin-bottom: 40px; }}
p {{ font-size: 44px; line-height: 1.32; font-weight: 400; }}
.numero {{ font-size: 300px; line-height: .9; font-weight: 800; color: {cor}; letter-spacing: -.04em;
  margin-bottom: 32px; }}
.s-foto .numero {{ color: #fff; }}
.meio {{ justify-content: center; }}
.rodape {{ position: absolute; left: 88px; right: 88px; bottom: 56px; display: flex;
  justify-content: space-between; font-size: 28px; font-weight: 600; opacity: .6; z-index: 1; }}
.barra {{ width: 96px; height: 10px; background: {cor}; margin-bottom: 40px; }}
.s-capa .barra, .s-cta .barra, .s-foto .barra {{ background: currentColor; }}
"""


def slide_html(slide, i, total, marca, base_dir):
    tipo = slide.get("tipo", "texto")
    classes = [f"s-{tipo}"]
    foto = ""
    if slide.get("imagem"):
        caminho = Path(slide["imagem"])
        if not caminho.is_absolute():
            caminho = (base_dir / caminho).resolve()
        if caminho.exists():
            foto = f'<div class="foto" style="background-image:url(\'{caminho.as_uri()}\')"></div>'
            classes.append("s-foto")

    partes = []
    if slide.get("tag"):
        partes.append(f'<div class="tag">{esc(slide["tag"])}</div>')
    if tipo == "numero" and slide.get("numero"):
        partes.append(f'<div class="numero">{esc(slide["numero"])}</div>')
    if tipo == "capa":
        partes.append('<div class="barra"></div>')
        partes.append(f'<h1>{esc(slide.get("titulo"))}</h1>')
    elif slide.get("titulo"):
        partes.append(f'<h2>{esc(slide["titulo"])}</h2>')
    if slide.get("texto"):
        partes.append(f'<p>{esc(slide["texto"])}</p>')

    meio = "" if tipo == "capa" else " meio"
    handle = esc(marca.get("handle", ""))
    seta = "arraste →" if i < total else ""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{css(marca)}</style></head>
<body class="{' '.join(classes)}">{foto}
<div class="conteudo{meio}">{''.join(partes)}</div>
<div class="rodape"><span>{handle}</span><span>{i}/{total} {seta}</span></div>
</body></html>"""


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    entrada = Path(sys.argv[1]).resolve()
    saida = Path(sys.argv[2]).resolve()
    saida.mkdir(parents=True, exist_ok=True)
    dados = json.loads(entrada.read_text(encoding="utf-8"))
    marca = dados.get("marca", {})
    slides = dados["slides"]

    grandes = sum(1 for s in slides if s.get("tipo") == "numero")
    if grandes > 1:
        print(f"ERRO: {grandes} slides com número gigante. Regra: no máximo 1 por carrossel.")
        sys.exit(2)

    from playwright.sync_api import sync_playwright

    exe = os.environ.get("CHROMIUM_PATH")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        for i, slide in enumerate(slides, 1):
            # uma aba por slide: reaproveitar a aba embaralha as letras no Chromium headless
            page = browser.new_page(viewport={"width": W, "height": H})
            arquivo_html = saida / f"slide-{i:02d}.html"
            arquivo_html.write_text(slide_html(slide, i, len(slides), marca, entrada.parent), encoding="utf-8")
            page.goto(arquivo_html.as_uri())
            page.wait_for_load_state("networkidle")
            page.evaluate("document.fonts.ready.then(() => true)")
            page.wait_for_timeout(150)
            page.screenshot(path=str(saida / f"slide-{i:02d}.png"), full_page=False)
            page.close()
            arquivo_html.unlink()
            print(f"ok slide-{i:02d}.png")
        browser.close()


if __name__ == "__main__":
    main()
