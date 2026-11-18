#!/usr/bin/env python3
"""Gera o site gabrieldiniztrafego.com.br a partir de conteudo/ (dados e artigos) e src/ (modelos, CSS, JS, imagens).

Uso:
  python3 src/build.py                 -> gera dist/ (o que vai ao ar; sem rascunhos)
  python3 src/build.py --previa        -> gera previa/ (com rascunhos, tudo noindex, com faixa "PRÉVIA")
Opcoes: --conteudo PASTA  (outra pasta de conteudo, usada nos testes)   --saida PASTA   --sem-minificar

Precisa de: Python 3.10+, pyyaml, markdown, pillow  (pip install -r requirements.txt). O Node.js e opcional (minifica CSS/JS).
O build FALHA (codigo 1) se faltar resumo, resposta direta, data de atualizacao ou alt da imagem em artigo publicado,
ou se o endereco (slug) se repetir. Problemas menores aparecem como AVISO.
"""
import argparse, datetime as dt, hashlib, html, json, os, re, shutil, subprocess, sys
from collections import OrderedDict

import markdown
import yaml
from PIL import Image

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)

ap = argparse.ArgumentParser()
ap.add_argument("--conteudo", default=os.path.join(ROOT, "conteudo"))
ap.add_argument("--saida", default=None)
ap.add_argument("--previa", action="store_true")
ap.add_argument("--sem-minificar", action="store_true")
ARGS = ap.parse_args()
for _f in (sys.stdout, sys.stderr):        # evita erro de acento no terminal do Windows
    try: _f.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
PREVIA = ARGS.previa
CONT = ARGS.conteudo
OUT = ARGS.saida or os.path.join(ROOT, "previa" if PREVIA else "dist")

ERROS, AVISOS = [], []
def erro(m): ERROS.append(m)
def aviso(m): AVISOS.append(m)

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
def esc(t): return html.escape(str(t), quote=True)
def br(d): return d.strftime("%d/%m/%Y")
def longa(d): return "%d de %s de %d" % (d.day, MESES[d.month - 1], d.year)
def to_date(v):
    if isinstance(v, dt.datetime): return v.date()
    if isinstance(v, dt.date): return v
    if isinstance(v, str):
        try: return dt.date.fromisoformat(v.strip()[:10])
        except ValueError: return None
    return None
def cortar(t, n):
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) <= n: return t
    return t[: n - 1].rsplit(" ", 1)[0].rstrip(",;:.- ") + "…"
def plain(h): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h))).strip()
def lerf(*p):
    with open(os.path.join(*p), encoding="utf-8") as f: return f.read()
def yml(p):
    with open(p, encoding="utf-8") as f: return yaml.safe_load(f) or {}

# ---------------------------------------------------------------- dados
SITE_CFG = yml(os.path.join(CONT, "site.yml"))
AUTOR = yml(os.path.join(CONT, "autor.yml"))
S = SITE_CFG["site"]
URL = S["url"].rstrip("/")
assert "www." not in URL, "O endereco oficial nao pode ter www"
CATS = [dict(c) for c in SITE_CFG["categorias"]]
CAT_POR_NOME = {c["nome"].lower(): c for c in CATS}
CAT_POR_SLUG = {c["slug"]: c for c in CATS}
ORG_ID = URL + "/#organizacao"
PERSON_ID = URL + "/#gabriel"
PERPAGE = 12

# ---------------------------------------------------------------- saida
if os.path.isdir(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)
def write(rel, text, binary=False):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb" if binary else "w", encoding=None if binary else "utf-8", newline=None if binary else "\n") as f: f.write(text)

# ---------------------------------------------------------------- CSS / JS com nome versionado
def minificar(texto, loader):
    if ARGS.sem_minificar or not shutil.which("npx"): return texto
    try:
        r = subprocess.run(["npx", "--yes", "esbuild@0.25.0", "--minify", "--legal-comments=none", "--loader=" + loader],
                           input=texto, capture_output=True, text=True, encoding="utf-8", check=True, shell=(os.name == "nt"), timeout=120)
        return r.stdout
    except Exception as e:
        aviso("não consegui minificar (%s): %s" % (loader, str(e)[:80])); return texto
def emitir(pasta, nome, ext, texto, loader):
    corpo = minificar(texto, loader)
    h = hashlib.sha1(corpo.encode("utf-8")).hexdigest()[:8]
    rel = "%s/%s.%s.%s" % (pasta, nome, h, ext)
    write(rel, corpo)
    return "/" + rel

def conteudo_js():
    c = {"whatsapp": S["whatsapp"], "telefone": S["telefone"], "email": S["email"],
         "empresa": S.get("empresa") or {}, "gtmId": S.get("gtm_id") or "", "links": S["links"],
         "provas": SITE_CFG.get("provas") or {"numeros": [], "depoimentos": [], "casos": []}}
    return "window.SITE_CONTENT = " + json.dumps(c, ensure_ascii=False) + ";\n"

CSS_URL = emitir("css", "site", "css", lerf(SRC, "css", "site.css"), "css")
CONTENT_URL = emitir("js", "content", "js", conteudo_js(), "js")
SITE_JS_URL = emitir("js", "site", "js", lerf(SRC, "js", "site.js"), "js")

# ---------------------------------------------------------------- imagens (WebP, com largura e altura)
IMG_CACHE = {}
def imagem(caminho_md, largura_max, sufixo):
    """caminho_md: caminho gravado pelo painel (ex.: /conteudo/imagens/capa.jpg). Devolve dict(url, w, h) ou None."""
    rel = re.sub(r"^/?(conteudo/)?imagens/", "", caminho_md.lstrip("/")) if caminho_md.lstrip("/").startswith(("conteudo/imagens/", "imagens/")) else None
    if rel is None: return None
    fonte = os.path.join(CONT, "imagens", rel)
    if not os.path.isfile(fonte): return None
    chave = (fonte, largura_max, sufixo)
    if chave in IMG_CACHE: return IMG_CACHE[chave]
    im = Image.open(fonte)
    tem_alfa = im.mode in ("RGBA", "LA", "P")
    im = im.convert("RGBA" if tem_alfa else "RGB")
    im.thumbnail((largura_max, largura_max * 3), Image.LANCZOS)
    stem = re.sub(r"[^a-z0-9]+", "-", os.path.splitext(os.path.basename(rel))[0].lower()).strip("-") or "imagem"
    dados = hashlib.sha1(open(fonte, "rb").read() + sufixo.encode()).hexdigest()[:8]
    nome = "assets/blog/%s%s.%s.webp" % (stem, sufixo, dados)
    p = os.path.join(OUT, nome); os.makedirs(os.path.dirname(p), exist_ok=True)
    im.save(p, "WEBP", quality=82, method=6)
    r = {"url": "/" + nome, "w": im.width, "h": im.height}
    IMG_CACHE[chave] = r
    return r

# ---------------------------------------------------------------- artigos
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
def validar_titulos_md(corpo, nome):
    """H1 no corpo é erro; os níveis devem descer de um em um, começando em H2."""
    em_codigo, ultimo = False, 1
    for ln in corpo.splitlines():
        if ln.strip().startswith("```"): em_codigo = not em_codigo; continue
        if em_codigo: continue
        m = re.match(r"^(#{1,6})\s+\S", ln)
        if not m: continue
        n = len(m.group(1))
        if n == 1: erro("%s: o texto tem um título de nível 1 (#). Use ## e ###; o título do artigo já é o H1." % nome)
        elif n > ultimo + 1: aviso("%s: títulos fora de ordem (de H%d direto para H%d): %s" % (nome, ultimo, n, ln.strip()[:50]))
        ultimo = max(2, n) if n > 1 else ultimo

def ler_artigo(caminho):
    nome = os.path.basename(caminho)
    raw = lerf(caminho)
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", raw, re.S)
    if not m: erro("%s: faltam os campos do topo (entre ---)." % nome); return None
    try: f = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e: erro("%s: campos do topo inválidos (%s)" % (nome, str(e)[:80])); return None
    a = OrderedDict()
    a["arquivo"] = nome
    a["slug"] = str(f.get("slug") or os.path.splitext(nome)[0]).strip().lower()
    a["rascunho"] = bool(f.get("rascunho", False))
    a["titulo"] = str(f.get("titulo") or "").strip()
    a["titulo_seo"] = str(f.get("titulo_seo") or "").strip()
    a["resumo"] = re.sub(r"\s+", " ", str(f.get("resumo") or "")).strip()
    cat = str(f.get("categoria") or "").strip()
    a["categoria"] = CAT_POR_NOME.get(cat.lower()) or CAT_POR_SLUG.get(cat.lower())
    a["publicado"] = to_date(f.get("publicado")); a["atualizado"] = to_date(f.get("atualizado"))
    a["capa"] = str(f.get("capa") or "").strip(); a["capa_alt"] = str(f.get("capa_alt") or "").strip()
    a["resposta"] = re.sub(r"\s+", " ", str(f.get("resposta_direta") or "")).strip()
    a["faq"] = [{"p": str(x.get("pergunta", "")).strip(), "r": str(x.get("resposta", "")).strip()} for x in (f.get("faq") or []) if isinstance(x, dict)]
    a["fontes"] = [{"t": str(x.get("titulo", "")).strip(), "u": str(x.get("url", "")).strip()} for x in (f.get("fontes") or []) if isinstance(x, dict)]
    a["rel"] = [str(x).strip() for x in (f.get("relacionados") or [])]
    a["antigos"] = [str(x).strip().strip("/") for x in (f.get("slugs_antigos") or [])]
    a["corpo"] = m.group(2).strip()
    pub = not a["rascunho"]
    falha = erro if pub else aviso   # rascunho só avisa
    q = nome + (" (rascunho)" if a["rascunho"] else "")
    if not a["titulo"]: falha("%s: falta o título." % q)
    if not SLUG_RE.match(a["slug"]): falha("%s: endereço (slug) inválido: use só letras minúsculas, números e hífen." % q)
    if not a["resumo"]: falha("%s: falta o resumo (1 frase)." % q)
    if not a["resposta"]: falha("%s: falta a resposta direta (40 a 60 palavras)." % q)
    if not a["atualizado"]: falha("%s: falta a data de atualização." % q)
    if not a["publicado"]: falha("%s: falta a data de publicação." % q)
    if a["publicado"] and a["atualizado"] and a["atualizado"] < a["publicado"]: falha("%s: a data de atualização é anterior à de publicação." % q)
    if not a["categoria"]: falha("%s: categoria inválida ('%s')." % (q, cat))
    if a["capa"] and not a["capa_alt"]: falha("%s: a imagem de capa precisa de texto alternativo." % q)
    if not a["capa"]: aviso("%s: sem imagem de capa (vai usar a imagem padrão de compartilhamento)." % q)
    if a["capa"] and not os.path.isfile(os.path.join(CONT, "imagens", re.sub(r"^/?(conteudo/)?imagens/", "", a["capa"].lstrip("/")))):
        falha("%s: a imagem de capa não foi encontrada (%s)." % (q, a["capa"]))
    if not a["corpo"]: falha("%s: o texto do artigo está vazio." % q)
    n_resp = len(a["resposta"].split())
    if a["resposta"] and not 40 <= n_resp <= 60: aviso("%s: a resposta direta tem %d palavras (o ideal é de 40 a 60)." % (q, n_resp))
    if not 3 <= len(a["faq"]) <= 5: aviso("%s: %d perguntas frequentes (o ideal é de 3 a 5)." % (q, len(a["faq"])))
    if any(not x["p"] or not x["r"] for x in a["faq"]): falha("%s: pergunta frequente sem pergunta ou sem resposta." % q)
    if not a["fontes"]: aviso("%s: sem fontes." % q)
    for x in a["fontes"]:
        if not re.match(r"^https?://", x["u"]): falha("%s: fonte com endereço inválido (%s)." % (q, x["u"]))
    if a["titulo"] and len(a["titulo"]) > 60 and not a["titulo_seo"]: aviso("%s: o título tem %d caracteres; o do Google corta em ~60 (use o campo título para buscadores)." % (q, len(a["titulo"])))
    if len(a["resumo"]) > 160: aviso("%s: o resumo tem %d caracteres; a descrição do Google corta em 160." % (q, len(a["resumo"])))
    validar_titulos_md(a["corpo"], q)
    a["url"] = "/blog/%s/" % a["slug"]
    return a

ARTIGOS = []
pasta_blog = os.path.join(CONT, "blog")
if os.path.isdir(pasta_blog):
    for fn in sorted(os.listdir(pasta_blog)):
        if fn.endswith(".md") and not fn.startswith("_"):
            a = ler_artigo(os.path.join(pasta_blog, fn))
            if a: ARTIGOS.append(a)
vistos = {}
for a in ARTIGOS:
    if a["slug"] in vistos: erro("endereço (slug) repetido: '%s' em %s e %s." % (a["slug"], vistos[a["slug"]], a["arquivo"]))
    vistos[a["slug"]] = a["arquivo"]
PUBLICADOS = [a for a in ARTIGOS if (not a["rascunho"]) or PREVIA]
PUBLICADOS.sort(key=lambda a: (a["publicado"] or dt.date.min, a["slug"]), reverse=True)
POR_SLUG = {a["slug"]: a for a in PUBLICADOS}
TEM_ARTIGO = any(not a["rascunho"] for a in ARTIGOS)       # noindex do blog só some com artigo publicado de verdade
for a in ARTIGOS:
    for s in a["rel"]:
        if s not in {x["slug"] for x in ARTIGOS}: aviso("%s: artigo relacionado inexistente (%s)." % (a["arquivo"], s))
if ERROS:
    print("\nERROS (o site NÃO foi gerado):"); [print("  -", e) for e in ERROS]; [print("  aviso:", w) for w in AVISOS]; sys.exit(1)

# ---------------------------------------------------------------- modelos
HEAD, FOOT = lerf(SRC, "partials", "head.html"), lerf(SRC, "partials", "foot.html")
def tel_href(): return "tel:+" + S["whatsapp"]
LINKS = S["links"]
def empresa_p():
    e = S.get("empresa") or {}
    return '<p data-empresa>%s · CNPJ <span class="mono">%s</span></p>' % (esc(e["razao"]), esc(e["cnpj"])) if e.get("razao") and e.get("cnpj") else ""
COMUM = {
    "base": "/", "home": "/", "blog": "/blog/", "priv": "/privacidade/", "termos": "/termos/",
    "css": CSS_URL, "content_js": CONTENT_URL, "site_js": SITE_JS_URL,
    "tel_href": tel_href(), "tel_text": esc(S["telefone"]), "email": esc(S["email"]),
    "link_instagram": esc(LINKS["instagram"]), "link_linkedin": esc(LINKS["linkedin"]), "link_gmn": esc(LINKS["gmn"]),
    "empresa_p": empresa_p(), "site_nome": esc(S["nome"]),
    "previa_banner": '<div class="previa-faixa" role="note">PRÉVIA PRIVADA: esta cópia mostra os rascunhos e não é indexada pelo Google.</div>' if PREVIA else "",
}
def jsonld(objs):
    g = {"@context": "https://schema.org", "@graph": objs}
    return '<script type="application/ld+json">' + json.dumps(g, ensure_ascii=False).replace("</", "<\\/") + "</script>"
def org():
    return {"@type": "ProfessionalService", "@id": ORG_ID, "name": S["nome"], "url": URL + "/",
            "telephone": "+" + S["whatsapp"][:2] + " " + S["whatsapp"][2:4] + " " + S["whatsapp"][4:9] + "-" + S["whatsapp"][9:],
            "email": S["email"], "areaServed": "BR",
            "address": {"@type": "PostalAddress", "addressLocality": S["cidade"], "addressRegion": S["estado"], "addressCountry": "BR"},
            "sameAs": [LINKS["instagram"], LINKS["linkedin"], LINKS["gmn"]]}
def person():
    return {"@type": "Person", "@id": PERSON_ID, "name": AUTOR["nome"], "jobTitle": AUTOR["funcao"],
            "url": URL + "/#sobre", "description": AUTOR["frase"],
            "worksFor": {"@id": ORG_ID}, "sameAs": [LINKS["instagram"], LINKS["linkedin"]]}

OG_PADRAO = "/assets/og/og-padrao.jpg"
PAGINAS = []        # (url, lastmod) para o sitemap
def pagina(rel_dir, template, titulo, desc, canonical_path, corpo_ctx, noindex=False, og_image=None, og_w=1200, og_h=630,
           og_alt=None, og_type="website", head_extra="", schema=None, loading=False, no_sitemap=False, lastmod=None):
    titulo, desc = titulo.strip(), re.sub(r"\s+", " ", desc).strip()
    if len(titulo) > 60: erro("título da página passa de 60 caracteres (%d): %s" % (len(titulo), titulo))
    if len(desc) > 160: erro("descrição da página passa de 160 caracteres (%d): %s" % (len(desc), titulo))
    canon = URL + canonical_path
    ctx = dict(COMUM)
    ctx.update({
        "title": esc(titulo), "desc": esc(desc), "og_title": esc(titulo), "canonical_url": esc(canon), "og_type": og_type,
        "og_image": esc(URL + (og_image or OG_PADRAO)), "og_image_w": str(og_w), "og_image_h": str(og_h),
        "og_image_alt": esc(og_alt or S["nome"]),
        "robots": '<meta name="robots" content="noindex, follow">' if (noindex or PREVIA) else "",
        "head_extra": head_extra, "jsonld": jsonld(schema or [org()]),
        "loading_script": '<script>document.documentElement.className+=" loading";setTimeout(function(){document.documentElement.classList.remove("loading")},9000)</script>' if loading else "",
        "globo_script": "", "globo_poster": "", "globo_w": "", "globo_h": "",
    })
    ctx.update(corpo_ctx.get("ctx", {}))
    corpo = corpo_ctx["body"] if "body" in corpo_ctx else lerf(SRC, "pages", template + ".html")
    out = HEAD + corpo + FOOT
    for k, v in ctx.items(): out = out.replace("{{" + k + "}}", v)
    resto = re.findall(r"\{\{(\w+)\}\}", out)
    assert not resto, (rel_dir, resto)
    write(os.path.join(rel_dir, "index.html") if rel_dir else "index.html", out)
    if not (noindex or PREVIA or no_sitemap): PAGINAS.append((canonical_path, lastmod))

# ---------------------------------------------------------------- páginas fixas
D = SITE_CFG["datas"]
man = json.load(open(os.path.join(SRC, "assets", "globo-m2", "manifest.json"), encoding="utf-8"))
gdir = "/assets/globo-m2/"
home_ctx = {
    "globo_poster": gdir + man["poster"], "globo_w": str(man["largura"]), "globo_h": str(man["altura"]),
    "head_extra": '<link rel="preload" as="image" type="image/webp" href="%s" fetchpriority="high" media="(max-width: 900px)">' % (gdir + man["poster"]),
    "globo_script": "<script>window.GLOBO_M=" + json.dumps({"dir": gdir, "f": man["quadros"]}) + ";</script>",
}
def sobre_html():
    return lerf(SRC, "pages", "_sobre.html")
home_body = lerf(SRC, "pages", "index.html").replace("{{sobre}}", sobre_html())
pagina("", None, "Gabriel Diniz | Tráfego & IA: anúncios, sites e IA",
       "Gestor de tráfego e IA no Rio de Janeiro. Anúncios, sites e projetos de IA para vender mais. Atendimento on-line em todo o Brasil.",
       "/", {"body": home_body, "ctx": {k: v for k, v in home_ctx.items() if k not in ("head_extra",)}}, loading=True,
       head_extra=home_ctx["head_extra"], schema=[org(), person()], lastmod=D["home"])
for nome, titulo, desc in (
    ("privacidade", "Política de Privacidade | Gabriel Diniz Tráfego & IA", "Como o site gabrieldiniztrafego.com.br trata os dados pessoais, os cookies e os seus direitos."),
    ("termos", "Termos de Uso | Gabriel Diniz Tráfego & IA", "Regras de uso do site gabrieldiniztrafego.com.br.")):
    pagina(nome, nome, titulo, desc, "/%s/" % nome, {"ctx": {"draft": ""}}, lastmod=D[nome])
pagina("_404", "404", "Página não encontrada | Gabriel Diniz", "O endereço não existe ou mudou de lugar.", "/404.html", {"ctx": {}}, noindex=True)
os.replace(os.path.join(OUT, "_404", "index.html"), os.path.join(OUT, "404.html")); os.rmdir(os.path.join(OUT, "_404"))

# ---------------------------------------------------------------- blog: cartões e listas
def thumb(a):
    if a["capa"]:
        r = imagem(a["capa"], 480, "-mini")
        if r: return '<img src="%s" width="%d" height="%d" alt="" loading="lazy" decoding="async">' % (r["url"], r["w"], r["h"])
    return ""
COR = {c["slug"]: "c%d" % (i + 1) for i, c in enumerate(CATS)}
def cartao(a, nivel=2):
    marca = ' <span class="rasc">(rascunho)</span>' if a["rascunho"] else ""
    return ('<article class="post"><a href="%s"><div class="post-th %s">%s</div><div class="post-meta">%s · <time datetime="%s">%s</time></div>'
            '<h%d>%s%s</h%d><p>%s</p><span class="more">Ler artigo</span></a></article>') % (
        a["url"], COR.get(a["categoria"]["slug"], "c2"), thumb(a), esc(a["categoria"]["nome"]), a["publicado"].isoformat(), longa(a["publicado"]),
        nivel, esc(a["titulo"]), marca, nivel, esc(a["resumo"]))
def paginar(lista, base_url):
    n = max(1, -(-len(lista) // PERPAGE))
    return [(i, base_url if i == 1 else base_url + "pagina/%d/" % i, lista[(i - 1) * PERPAGE: i * PERPAGE]) for i in range(1, n + 1)], n
def pager_html(i, n, base_url):
    if n <= 1: return ""
    url = lambda k: base_url if k == 1 else base_url + "pagina/%d/" % k
    partes = []
    if i > 1: partes.append('<a rel="prev" href="%s">Anterior</a>' % url(i - 1))
    for k in range(1, n + 1):
        partes.append('<span aria-current="page">%d</span>' % k if k == i else '<a href="%s">%d</a>' % (url(k), k))
    if i < n: partes.append('<a rel="next" href="%s">Próxima</a>' % url(i + 1))
    return '<nav class="pager" id="pager" aria-label="Paginação do blog">%s</nav>' % " ".join(partes)
def cats_nav(atual):
    com = [c for c in CATS if any(a["categoria"]["slug"] == c["slug"] for a in PUBLICADOS)]
    if not com: return ""
    itens = ['<a class="chip" href="/blog/"%s>Todos</a>' % (' aria-current="page"' if atual is None else "")]
    for c in com: itens.append('<a class="chip" href="/blog/categoria/%s/"%s>%s</a>' % (c["slug"], ' aria-current="page"' if atual == c["slug"] else "", esc(c["nome"])))
    return '<nav class="cats" aria-label="Categorias do blog">%s</nav>' % "".join(itens)
CTA_FIM = ('<div class="blog-cta"><h2>Quer resolver isso no seu negócio?</h2><a class="btn btn-cobalt btn-lg" href="/#contato" '
           'data-wa="Olá, Gabriel! Vim pelo blog e quero agendar uma conversa." data-local="blog-fim">Agendar conversa</a></div>')
def topicos():
    com = [c for c in CATS if any(a["categoria"]["slug"] == c["slug"] for a in PUBLICADOS)]
    frases = {"trafego": "Quero vender mais com anúncios", "ia": "Quero usar IA no meu negócio", "sites-e-seo": "Quero um site que gere contatos", "google-meu-negocio": "Quero aparecer no Google"}
    if not com: return ""
    busca = ('<form class="busca" id="blog-busca" role="search" hidden><label for="blog-q">Buscar artigos por palavra</label>'
             '<input id="blog-q" type="search" placeholder="Digite um assunto" autocomplete="off"><div id="busca-res" aria-live="polite"></div></form>')
    lis = "".join('<a href="/blog/categoria/%s/">%s</a>' % (c["slug"], esc(frases.get(c["slug"], c["nome"]))) for c in com)
    return '<div class="topics"><h2>Busque por assunto</h2>%s<div class="topic-list">%s</div></div>' % (busca, lis)
VAZIO = ('<div class="empty" id="blog-empty"><h2>Os primeiros artigos chegam em breve.</h2>'
         '<p>Enquanto isso, se você quer resolver algo no seu negócio, a conversa pode começar agora.</p>'
         '<a class="btn btn-cobalt" href="/#contato" data-wa="Olá, Gabriel! Vim pelo blog e quero conversar sobre o meu negócio." data-local="blog-vazio">Agendar conversa</a></div>')

def lista(rel, base_url, titulo_h1, lead, posts, atual_cat, titulo_pag, desc, canon_base):
    pags, n = paginar(posts, base_url)
    for i, url, itens in pags:
        extra = []
        if i > 1: extra.append('<link rel="prev" href="%s">' % esc(URL + (base_url if i == 2 else base_url + "pagina/%d/" % (i - 1))))
        if i < n: extra.append('<link rel="next" href="%s">' % esc(URL + base_url + "pagina/%d/" % (i + 1)))
        h1 = titulo_h1 if i == 1 else "%s, página %d" % (titulo_h1, i)
        corpo = ('<main id="conteudo"><section class="sec" style="padding-bottom: clamp(40px, 6vw, 80px)"><div class="wrap">'
                 '<div class="blog-head"><h1>%s</h1><p class="lead" style="margin-top:16px">%s</p></div>%s%s%s%s%s</div></section></main>') % (
            esc(h1), esc(lead), cats_nav(atual_cat),
            ('<div class="posts" id="posts">%s</div>' % "".join(cartao(a) for a in itens)) if itens else VAZIO,
            pager_html(i, n, base_url), topicos() if i == 1 else "", CTA_FIM)
        t = titulo_pag if i == 1 else "%s, página %d | Gabriel Diniz" % (titulo_h1, i)
        pagina(os.path.join(rel, "pagina", str(i)) if i > 1 else rel, None, t, desc, url, {"body": corpo, "ctx": {}},
               noindex=(not posts and not PREVIA) or False, head_extra="".join(extra), no_sitemap=(i > 1), lastmod=None)

blog_noindex = not TEM_ARTIGO
pags, npg = paginar(PUBLICADOS, "/blog/")
lista("blog", "/blog/", "Blog", "Artigos sobre tráfego, sites e IA para quem quer vender mais.", PUBLICADOS, None,
      "Blog | Gabriel Diniz | Tráfego & IA", "Artigos sobre tráfego pago, sites, SEO, Google Meu Negócio e IA para quem quer vender mais.", "/blog/")
if blog_noindex and not PREVIA:     # a página existe, mas sem artigo ela não entra no Google nem no sitemap
    pass
CATS_COM_ARTIGO = []
for c in CATS:
    posts = [a for a in PUBLICADOS if a["categoria"]["slug"] == c["slug"]]
    if not posts: continue
    CATS_COM_ARTIGO.append(c)
    lista("blog/categoria/%s" % c["slug"], "/blog/categoria/%s/" % c["slug"], c["nome"], c["descricao"], posts, c["slug"],
          "%s | Blog | Gabriel Diniz" % c["nome"], c["descricao"], "")
# /blog/ no sitemap: só com artigo publicado
PAGINAS[:] = [(u, l) for (u, l) in PAGINAS if u != "/blog/"]
if TEM_ARTIGO and not PREVIA:
    PAGINAS.append(("/blog/", max([a["atualizado"] for a in PUBLICADOS])))
# lastmod das categorias = atualização do artigo mais recente
fix = []
for (u, l) in PAGINAS:
    m = re.match(r"^/blog/categoria/([a-z0-9-]+)/$", u)
    if m: l = max(a["atualizado"] for a in PUBLICADOS if a["categoria"]["slug"] == m.group(1))
    fix.append((u, l))
PAGINAS[:] = fix
# índice de busca (só publicados)
write("blog/indice.json", json.dumps([{"t": a["titulo"], "r": a["resumo"], "c": a["categoria"]["nome"], "u": a["url"], "d": longa(a["publicado"])} for a in PUBLICADOS], ensure_ascii=False))

# ---------------------------------------------------------------- blog: artigos
def md_para_html(a):
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "toc"], extension_configs={"toc": {"permalink": False, "toc_depth": "2-3"}})
    h = md.convert(a["corpo"])
    def img(m):
        alt, src = m.group(1), m.group(2)
        r = imagem(src, 1200, "")
        if not alt.strip(): aviso("%s: imagem no texto sem texto alternativo (%s)." % (a["arquivo"], src))
        if r: return '<img src="%s" width="%d" height="%d" alt="%s" loading="lazy" decoding="async">' % (r["url"], r["w"], r["h"], alt)
        aviso("%s: imagem do texto sem largura/altura (arquivo não encontrado ou externa): %s" % (a["arquivo"], src))
        return '<img src="%s" alt="%s" loading="lazy" decoding="async">' % (src, alt)
    h = re.sub(r'<img alt="([^"]*)" src="([^"]+)"\s*/?>', img, h)
    h = h.replace("<table>", '<div class="tbl"><table>').replace("</table>", "</table></div>")
    return h
def caixa_autor(topo, a):
    if topo:
        return ('<div class="autor autor-topo"><b>%s</b><span>%s</span><span class="upd">Atualizado em <time datetime="%s">%s</time></span></div>' %
                (esc(AUTOR["nome"]), esc(AUTOR["funcao"]), a["atualizado"].isoformat(), br(a["atualizado"])))
    return ('<aside class="autor autor-fim" aria-label="Sobre o autor"><h2>%s</h2><p class="role">%s</p><p>%s</p><a href="%s">%s</a></aside>' %
            (esc(AUTOR["nome"]), esc(AUTOR["funcao"]), esc(AUTOR["frase"]), esc(AUTOR["link_url"]), esc(AUTOR["link_texto"])))
def relacionados(a):
    ok = [POR_SLUG[s] for s in a["rel"] if s in POR_SLUG and s != a["slug"]][:4]
    if len(ok) < 2:
        extra = [x for x in PUBLICADOS if x["slug"] != a["slug"] and x not in ok]
        extra.sort(key=lambda x: (x["categoria"]["slug"] != a["categoria"]["slug"]))
        ok = (ok + extra)[: max(2, len(ok))][:3]
    return ok

for a in PUBLICADOS:
    cat = a["categoria"]
    corpo_html = md_para_html(a)
    capa = imagem(a["capa"], 1200, "") if a["capa"] else None
    tit_seo = a["titulo_seo"] or a["titulo"]
    suf = " | Gabriel Diniz"
    titulo_tag = tit_seo + suf if len(tit_seo + suf) <= 60 else (tit_seo if len(tit_seo) <= 60 else cortar(tit_seo, 60))
    desc = cortar(a["resumo"], 160)
    rel = relacionados(a)
    figura = ('<figure class="capa"><img src="%s" width="%d" height="%d" alt="%s" fetchpriority="high" decoding="async"></figure>' % (capa["url"], capa["w"], capa["h"], esc(a["capa_alt"]))) if capa else ""
    faq_html = ""
    if a["faq"]:
        faq_html = '<section class="faq" aria-labelledby="faq-h"><h2 id="faq-h">Perguntas frequentes</h2>%s</section>' % "".join(
            "<h3>%s</h3><p>%s</p>" % (esc(x["p"]), esc(x["r"])) for x in a["faq"])
    fontes_html = ""
    if a["fontes"]:
        fontes_html = '<section class="fontes" aria-labelledby="fontes-h"><h2 id="fontes-h">Fontes</h2><ul>%s</ul></section>' % "".join(
            '<li><a href="%s" rel="noopener" target="_blank">%s</a></li>' % (esc(x["u"]), esc(x["t"] or x["u"])) for x in a["fontes"])
    rel_html = ""
    if rel:
        rel_html = '<section class="related" aria-labelledby="rel-h"><h2 id="rel-h">Artigos relacionados</h2><div class="posts">%s</div></section>' % "".join(cartao(x, 3) for x in rel)
    msg = "Olá, Gabriel! Li o artigo “%s” e quero agendar uma conversa." % a["titulo"]
    atr = 'data-wa="%s" data-local="artigo" data-artigo="%s"' % (esc(msg), esc(a["titulo"]))
    corpo = ('<main id="conteudo"><article class="sec art-pg"><div class="wrap art1">'
             '<nav class="crumb" aria-label="Você está em"><a href="/">Início</a> › <a href="/blog/">Blog</a> › <a href="/blog/categoria/%s/">%s</a> › <span aria-current="page">%s</span></nav>'
             '<header><div class="art-meta">%s · <time datetime="%s">Publicado em %s</time></div><h1>%s</h1></header>'
             '<section class="resposta" aria-labelledby="resp-h"><h2 id="resp-h">Resposta direta</h2><p>%s</p></section>'
             '%s%s<div class="art-body">%s</div>%s%s%s%s'
             '<div class="art-end"><h2>Quer aplicar isso no seu negócio?</h2><p>A primeira conversa é sem compromisso.</p><a class="btn btn-cobalt btn-lg" href="/#contato" %s>Agendar conversa</a></div>'
             '</div></article></main>'
             '<a class="fab" href="/#contato" %s>Agendar conversa</a>') % (
        cat["slug"], esc(cat["nome"]), esc(a["titulo"]), esc(cat["nome"]), a["publicado"].isoformat(), br(a["publicado"]), esc(a["titulo"]),
        esc(a["resposta"]), caixa_autor(True, a), figura, corpo_html, faq_html, fontes_html, rel_html, caixa_autor(False, a), atr, atr)
    # schema
    url_abs = URL + a["url"]
    crumbs = [("Início", URL + "/"), ("Blog", URL + "/blog/"), (cat["nome"], URL + "/blog/categoria/%s/" % cat["slug"]), (a["titulo"], url_abs)]
    posting = {"@type": "BlogPosting", "@id": url_abs + "#artigo", "headline": cortar(a["titulo"], 110), "description": desc,
               "datePublished": a["publicado"].isoformat(), "dateModified": a["atualizado"].isoformat(), "inLanguage": "pt-BR",
               "image": [URL + (capa["url"] if capa else OG_PADRAO)], "mainEntityOfPage": {"@type": "WebPage", "@id": url_abs},
               "publisher": {"@id": ORG_ID}, "author": {"@type": "Person", "@id": PERSON_ID, "name": AUTOR["nome"], "url": URL + "/#sobre"},
               "articleSection": cat["nome"]}
    objs = [org(), posting,
            {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]}]
    if a["faq"]:
        objs.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": x["p"], "acceptedAnswer": {"@type": "Answer", "text": x["r"]}} for x in a["faq"]]})
    extra = ('<meta property="article:published_time" content="%s"><meta property="article:modified_time" content="%s"><meta property="article:section" content="%s">'
             % (a["publicado"].isoformat(), a["atualizado"].isoformat(), esc(cat["nome"])))
    pagina("blog/%s" % a["slug"], None, titulo_tag, desc, a["url"], {"body": corpo, "ctx": {}},
           noindex=a["rascunho"], og_image=(capa["url"] if capa else None), og_w=(capa["w"] if capa else 1200), og_h=(capa["h"] if capa else 630),
           og_alt=(a["capa_alt"] if capa else None), og_type="article", head_extra=extra, schema=objs, lastmod=a["atualizado"])

# ---------------------------------------------------------------- arquivos estáticos, sitemap, headers, redirecionamentos
def copiar(origem, destino):
    if os.path.isdir(origem): shutil.copytree(origem, destino, dirs_exist_ok=True)
copiar(os.path.join(SRC, "assets"), os.path.join(OUT, "assets"))
if os.path.isdir(os.path.join(OUT, "assets", "globo-m2")):
    pass
copiar(os.path.join(SRC, "static"), OUT)
if PREVIA:
    shutil.rmtree(os.path.join(OUT, "admin"), ignore_errors=True)
# a lista de quadros do celular fica no HTML; o manifest não precisa ir ao ar
mf = os.path.join(OUT, "assets", "globo-m2", "manifest.json")
if os.path.exists(mf): os.remove(mf)

if not PREVIA:
    linhas = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, l in sorted(PAGINAS, key=lambda x: (x[0] != "/", x[0])):
        linhas.append("  <url><loc>%s</loc>%s</url>" % (URL + u, ("<lastmod>%s</lastmod>" % l.isoformat()) if l else ""))
    linhas.append("</urlset>")
    write("sitemap.xml", "\n".join(linhas) + "\n")

HTML_CACHE = "Cache-Control: public, max-age=300, must-revalidate"
hdr = ["/*", "  X-Content-Type-Options: nosniff", "  Referrer-Policy: strict-origin-when-cross-origin", "  X-Frame-Options: SAMEORIGIN", "",
       "/assets/*", "  Cache-Control: public, max-age=31536000, immutable", "",
       "/css/*", "  Cache-Control: public, max-age=31536000, immutable", "",
       "/js/*", "  Cache-Control: public, max-age=31536000, immutable", "",
       "/robots.txt", "  Content-Type: text/plain; charset=utf-8", "  Cache-Control: public, max-age=3600", "",
       "/sitemap.xml", "  Content-Type: application/xml; charset=utf-8", "  Cache-Control: public, max-age=3600", "",
       "/", "  " + HTML_CACHE, "", "/privacidade/*", "  " + HTML_CACHE, "", "/termos/*", "  " + HTML_CACHE, "",
       "/blog/*", "  " + HTML_CACHE] + (["  X-Robots-Tag: noindex, follow"] if (blog_noindex or PREVIA) else []) + [""] + [
       "/blog/indice.json", "  Content-Type: application/json; charset=utf-8", "",
       "# /forms/ e servido por outro Worker (gabi-briefing); esta regra so vale se o endereco cair neste site.",
       "/forms/*", "  X-Robots-Tag: noindex, nofollow", "",
       "/admin/*", "  X-Robots-Tag: noindex, nofollow", "  Cache-Control: no-cache", ""]
if PREVIA: hdr += ["/*", "  X-Robots-Tag: noindex, nofollow", ""]
write("_headers", "\n".join(hdr))

red = []
for a in ARTIGOS:
    if a["rascunho"] and not PREVIA: continue
    for velho in a["antigos"]:
        if velho and velho != a["slug"]:
            red += ["/blog/%s/ %s 301" % (velho, a["url"]), "/blog/%s %s 301" % (velho, a["url"])]
rp = os.path.join(CONT, "redirecionamentos.txt")
if os.path.isfile(rp):
    for ln in lerf(rp).splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"): continue
        partes = ln.split()
        if len(partes) < 2: aviso("redirecionamentos.txt: linha ignorada (%s)." % ln); continue
        if partes[0].startswith("/forms") or partes[1].startswith("/forms"): erro("redirecionamentos.txt: nunca redirecione /forms (%s)." % ln); continue
        red.append("%s %s %s" % (partes[0], partes[1], partes[2] if len(partes) > 2 else "301"))
for r in red:
    if r.startswith("/forms"): erro("redirecionamento de /forms não é permitido: " + r)
if red: write("_redirects", "\n".join(red) + "\n")

if ERROS:
    print("\nERROS (o site NÃO foi gerado):"); [print("  -", e) for e in ERROS]; sys.exit(1)
pub = [a for a in ARTIGOS if not a["rascunho"]]
print("ok -> %s | %d artigo(s) publicado(s), %d rascunho(s) | %d página(s) no sitemap | blog %s" % (
    OUT, len(pub), len(ARTIGOS) - len(pub), len(PAGINAS), "indexável" if TEM_ARTIGO else "com noindex (sem artigos)"))
for w in AVISOS: print("  aviso:", w)
