#!/usr/bin/env python3
"""Gera a imagem padrao de compartilhamento (Open Graph, 1200 x 630) em src/assets/og/og-padrao.jpg.
Precisa de: pillow, fonttools, brotli. Uso: python3 src/tools/gerar-og-padrao.py"""
import os, tempfile
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

AQUI = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.dirname(AQUI)
fonte_woff2 = os.path.join(SRC, "assets", "fonts", "inter-tight-latin-wght-normal.woff2")
globo = os.path.join(SRC, "assets", "globo-d", "000.webp")
saida = os.path.join(SRC, "assets", "og"); os.makedirs(saida, exist_ok=True)

tmp = os.path.join(tempfile.mkdtemp(), "inter-tight.ttf")
f = TTFont(fonte_woff2); f.flavor = None; f.save(tmp)
def fonte(px, peso):
    ft = ImageFont.truetype(tmp, px)
    try: ft.set_variation_by_axes([peso])
    except Exception: pass
    return ft

W, H = 1200, 630
im = Image.new("RGB", (W, H), (7, 8, 13))
g = Image.open(globo).convert("RGB"); g = g.resize((int(H * 1.12 * g.width / g.height), int(H * 1.12)))
# mesma máscara circular do site (opaco até 62% do raio, some em 90%)
mask = Image.new("L", g.size, 0); mp = mask.load(); cx, cy = g.width / 2, g.height / 2; R = min(cx, cy)
for y in range(g.height):
    for x in range(g.width):
        r = (((x - cx) ** 2 + (y - cy) ** 2) ** 0.5) / R
        mp[x, y] = 255 if r <= 0.62 else (0 if r >= 0.9 else int(255 * (1 - (r - 0.62) / 0.28)))
im.paste(g, (W - g.width + 110, (H - g.height) // 2), mask)
d = ImageDraw.Draw(im)
d.text((72, 190), "Gabriel Diniz", font=fonte(104, 800), fill=(238, 241, 251))
d.text((72, 312), "Tráfego & IA", font=fonte(104, 800), fill=(108, 130, 255))
d.text((76, 470), "Anúncios, sites e projetos de IA", font=fonte(38, 500), fill=(167, 174, 200))
d.text((76, 520), "gabrieldiniztrafego.com.br", font=fonte(32, 500), fill=(167, 174, 200))
im.save(os.path.join(saida, "og-padrao.jpg"), quality=84, optimize=True)
print("ok", os.path.getsize(os.path.join(saida, "og-padrao.jpg")) // 1024, "KB")
