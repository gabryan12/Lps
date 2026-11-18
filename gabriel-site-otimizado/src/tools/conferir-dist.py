# -*- coding: utf-8 -*-
"""Conferencia final da pasta dist/ ANTES de publicar. Sai com codigo 1 se algo estiver errado.
Uso: python src/tools/conferir-dist.py [pasta_dist] [pasta_conteudo]"""
import glob, io, os, re, sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import yaml

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIST = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RAIZ, "dist")
CONT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(RAIZ, "conteudo")
SITE = "https://gabrieldiniztrafego.com.br"
erros, oks = [], []
def ok(m): oks.append(m)
def erro(m): erros.append(m)
def ler(p):
    with io.open(p, encoding="utf-8") as f: return f.read()

for f in ("index.html", "404.html", "sitemap.xml", "robots.txt", "_headers", "blog/index.html", "privacidade/index.html", "termos/index.html"):
    if not os.path.isfile(os.path.join(DIST, f)): erro("falta o arquivo dist/%s" % f)
if erros:
    print("\nERRO: o site gerado esta incompleto:"); [print("  -", e) for e in erros]; sys.exit(1)

# 1. nada de previa no site final
if os.path.isdir(os.path.join(DIST, "previa")): erro("existe uma pasta 'previa' dentro de dist")
for p in glob.glob(os.path.join(DIST, "**", "*"), recursive=True):
    if not os.path.isfile(p) or not p.endswith((".html", ".js")) or os.sep + "admin" + os.sep in p: continue
    try: t = ler(p)
    except Exception: continue
    if "previa-faixa" in t or "PRÉVIA PRIVADA" in t:
        erro("a marca de previa apareceu em %s" % os.path.relpath(p, DIST))
if not erros: ok("sem faixa/marca de PREVIA no site final")

# 2. rascunhos fora do site
rasc, pub = [], []
for p in sorted(glob.glob(os.path.join(CONT, "blog", "*.md"))):
    if os.path.basename(p).startswith("_"): continue
    m = re.match(r"^---\s*\n(.*?)\n---", ler(p), re.S)
    fm = yaml.safe_load(m.group(1)) if m else {}
    slug = str(fm.get("slug") or os.path.splitext(os.path.basename(p))[0]).lower()
    (rasc if fm.get("rascunho", False) else pub).append(slug)
for s in rasc:
    if os.path.exists(os.path.join(DIST, "blog", s)): erro("o rascunho '%s' esta no site final" % s)
for s in pub:
    if not os.path.isfile(os.path.join(DIST, "blog", s, "index.html")): erro("o artigo publicado '%s' nao foi gerado" % s)
ok("%d artigo(s) publicado(s), %d rascunho(s) fora do site" % (len(pub), len(rasc)))

# 3. sitemap e noindex do blog
sm = ler(os.path.join(DIST, "sitemap.xml"))
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
blog = ler(os.path.join(DIST, "blog", "index.html"))
noindex = bool(re.search(r'<meta name="robots" content="[^"]*noindex', blog))
if not pub:
    if not noindex: erro("sem artigos, o /blog/ deveria ter noindex")
    if len(locs) != 3: erro("sem artigos, o sitemap deveria ter 3 enderecos (tem %d)" % len(locs))
    if any("/blog" in l for l in locs): erro("sem artigos, o blog nao deve estar no sitemap")
    ok("sem artigos: /blog/ com noindex e sitemap com 3 enderecos")
else:
    if noindex: erro("ha artigo publicado, mas o /blog/ ainda tem noindex")
    for s in pub:
        if SITE + "/blog/" + s + "/" not in locs: erro("o artigo '%s' nao entrou no sitemap" % s)
    if not re.search(r"<lastmod>\d{4}-\d\d-\d\d</lastmod>", sm): erro("o sitemap esta sem datas (lastmod)")
    ok("com artigos: /blog/ sem noindex, sitemap com %d enderecos" % len(locs))
if any("/forms" in l for l in locs): erro("o sitemap nao pode ter /forms/")

# 4. canonical sem www e artigos com schema
paginas = [p for p in glob.glob(os.path.join(DIST, "**", "*.html"), recursive=True) if os.sep + "admin" + os.sep not in p]
for p in paginas:
    h = ler(p); r = os.path.relpath(p, DIST)
    c = re.findall(r'<link rel="canonical" href="([^"]*)"', h)
    if len(c) != 1 or not c[0].startswith(SITE + "/"): erro("canonical errado em %s: %s" % (r, c))
    if "://www.gabrieldiniztrafego" in h: erro("endereco com www em %s" % r)
    if re.search(r'<script[^>]+src="[^"]*googletagmanager', h): erro("GTM carregando direto no HTML de %s" % r)
for s in pub:
    h = ler(os.path.join(DIST, "blog", s, "index.html"))
    for k in ("BlogPosting", "BreadcrumbList"):
        if k not in h: erro("artigo '%s' sem schema %s" % (s, k))
    if re.search(r'name="robots" content="[^"]*noindex', h): erro("artigo '%s' com noindex" % s)
ok("canonical sem www em %d paginas, GTM fora do HTML" % len(paginas))

if not erros: print("")
for m in oks: print("  ok  ", m)
if erros:
    print("\nERRO: NAO PUBLIQUE. Problemas encontrados:"); [print("  -", e) for e in erros]; sys.exit(1)
print("\nConferencia concluida: tudo certo para publicar.")
