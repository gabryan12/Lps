#!/usr/bin/env python3
"""Monta o site a partir de src/ (partials + pages).
Uso: python3 build.py preview   -> ../preview  (links relativos, noindex, conteúdo de exemplo)
     python3 build.py prod      -> ../dist     (URLs limpas, indexável, sem exemplos)
"""
import json, os, shutil, subprocess, sys

mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
OUT = os.path.join(ROOT, "preview" if mode == "preview" else "dist")
PREVIEW = mode == "preview"
SITE = "https://gabrieldiniztrafego.com.br"


def read(*p):
    with open(os.path.join(SRC, *p), encoding="utf-8") as f:
        return f.read()


def write(rel, text):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


JSONLD = {
    "@context": "https://schema.org",
    "@type": "ProfessionalService",
    "name": "Gabriel Diniz | Tráfego & IA",
    "url": SITE + "/",
    "telephone": "+5521989227990",
    "email": "sagatrafego@gmail.com",
    "areaServed": "BR",
    "address": {"@type": "PostalAddress", "addressLocality": "Rio de Janeiro", "addressRegion": "RJ", "addressCountry": "BR"},
    "founder": {"@type": "Person", "name": "Gabriel Gomes Diniz", "jobTitle": "Gestor de tráfego e IA"},
    "sameAs": [
        "https://www.instagram.com/gabrieldiniztrafego/",
        "https://www.linkedin.com/in/gabriel-diniz-trafego-pago-a0abb8259/",
    ],
}

PREVIEW_BAR = ('<div class="prev" role="region" aria-label="Controles da prévia"><span id="prev-label">Prévia</span>'
               '<button type="button" id="prev-toggle">Ver sem exemplos</button></div>')
DRAFT = ('<p class="legal-draft">Rascunho para você revisar. Preencha razão social e CNPJ e peça a revisão de um '
         'advogado antes de publicar.</p>')

# (arquivo da página, saída preview, saída prod, profundidade, título, descrição, indexar, jsonld)
PAGES = [
    ("index", "index.html", "index.html", 0,
     "Gabriel Diniz | Tráfego & IA: anúncios, sites e projetos de IA",
     "Gestor de tráfego e IA no Rio de Janeiro. Anúncios, sites e projetos com IA para profissionais e empresas que querem vender mais. Atendimento on-line em todo o Brasil.",
     True, True),
    ("blog", "blog/index.html", "blog/index.html", 1,
     "Blog | Gabriel Diniz Tráfego & IA",
     "Artigos sobre tráfego pago, sites, SEO e IA para quem quer vender mais.",
     False, False),
    ("privacidade", "privacidade.html", "privacidade/index.html", 0,
     "Política de Privacidade | Gabriel Diniz Tráfego & IA",
     "Como o site gabrieldiniztrafego.com.br trata os dados pessoais, os cookies e os seus direitos.",
     True, False),
    ("termos", "termos.html", "termos/index.html", 0,
     "Termos de Uso | Gabriel Diniz Tráfego & IA",
     "Regras de uso do site gabrieldiniztrafego.com.br.",
     True, False),
]
if PREVIEW:
    pass

head, foot = read("partials", "head.html"), read("partials", "foot.html")

for name, out_prev, out_prod, depth, title, desc, index_ok, ld in PAGES:
    if PREVIEW:
        base = "../" * depth
        links = {"home": base + "index.html", "blog": base + "blog/index.html",
                 "priv": base + "privacidade.html", "termos": base + "termos.html"}
        out_rel = out_prev
        robots = '<meta name="robots" content="noindex, nofollow">'
        canonical = ""
        pretty = ""
    else:
        base = "/"
        links = {"home": "/", "blog": "/blog/", "priv": "/privacidade/", "termos": "/termos/"}
        out_rel = out_prod
        robots = "" if index_ok else '<meta name="robots" content="noindex, follow">'  # o blog fica noindex até o 1º artigo
        path = {"index": "/", "blog": "/blog/", "privacidade": "/privacidade/", "termos": "/termos/"}[name]
        canonical = f'<link rel="canonical" href="{SITE}{path}">'
        pretty = "window.SITE_PRETTY=true;"
    body = read("pages", name + ".html")
    html = head + body + foot
    sub = {
        "title": title, "desc": desc, "robots": robots, "canonical": canonical, "base": base,
        "jsonld": ('<script type="application/ld+json">' + json.dumps(JSONLD, ensure_ascii=False) + "</script>") if ld else "",
        "preview_bar": PREVIEW_BAR if PREVIEW else "",
        "preview_js": f'<script src="{base}js/preview-exemplos.js"></script>' if PREVIEW else "",
        "pretty": pretty, "draft": DRAFT if PREVIEW else "",
        **links,
    }
    for k, v in sub.items():
        html = html.replace("{{" + k + "}}", v)
    assert "{{" not in html, (name, html.split("{{")[1][:40])
    write(out_rel, html)

def minify(rel):
    """Gera a versão minificada (menor) com o esbuild, se o Node estiver instalado; senão copia o arquivo como está."""
    src_f, dst_f = os.path.join(SRC, rel), os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(dst_f), exist_ok=True)
    if not PREVIEW and shutil.which("npx"):
        try:
            subprocess.run(["npx", "--yes", "esbuild@0.25.0", src_f, "--minify", "--legal-comments=none", "--outfile=" + dst_f],
                           check=True, capture_output=True, shell=(os.name == "nt"))
            return
        except Exception as e:  # sem rede ou sem Node: segue com o arquivo original
            print("aviso: não consegui minificar", rel, "->", e)
    shutil.copy(src_f, dst_f)

for rel in ("css/site.css", "js/content.js", "js/site.js"):
    minify(rel)
if not PREVIEW:
    assets = os.path.join(OUT, "assets")
    if os.path.exists(assets):
        shutil.rmtree(assets)
    shutil.copytree(os.path.join(SRC, "assets"), assets)
print("ok", mode, "->", OUT)
