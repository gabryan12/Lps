(function () {
  "use strict";
  var C = window.SITE_CONTENT || {};
  var EX = window.SITE_EXEMPLOS || null;
  var PREVIEW = !!EX;
  var BASE = window.SITE_BASE || "";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var HH = 64;

  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(t) { return String(t == null ? "" : t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function get(k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { window.localStorage.setItem(k, v); } catch (e) { /* sem armazenamento */ } }
  function clamp(v, a, b) { return Math.min(b, Math.max(a, v)); }

  /* Medição: só existe depois do "Aceitar". O consentimento e o carregamento do GTM ficam no script do <head> (window.__consent).
     Sem consentimento, nada é enviado ao dataLayer e nenhum script do Google é pedido. */
  var CONSENT = window.__consent || { get: function () { return null; }, accepted: function () { return false; }, accept: function () {}, decline: function () {}, reset: function () {}, push: function () {} };
  function track(ev, p) {
    var o = { event: ev };
    if (p) { for (var k in p) { if (Object.prototype.hasOwnProperty.call(p, k)) o[k] = p[k]; } }
    CONSENT.push(o);
  }
  function articleTitle(a) {
    var t = a && a.getAttribute("data-artigo");
    if (t) return t;
    var el = $("[data-artigo-titulo]");
    return el ? el.getAttribute("data-artigo-titulo") : "";
  }

  /* WhatsApp, telefone e e-mail */
  function waUrl(msg) { return "https://wa.me/" + C.whatsapp + "?text=" + encodeURIComponent(msg); }
  $$("[data-wa]").forEach(function (a) {
    a.href = waUrl(a.getAttribute("data-wa"));
    a.target = "_blank";
    a.rel = "noopener";
    a.addEventListener("click", function () {
      var loc = a.getAttribute("data-local") || "";
      if (loc === "topo") loc = "hero";
      track("cta_agendar_conversa", { cta_location: loc, page_path: location.pathname, article_title: articleTitle(a) });
    });
  });
  $$("[data-tel]").forEach(function (a) { a.textContent = C.telefone; a.href = "tel:+" + C.whatsapp; });
  $$("[data-email]").forEach(function (a) { a.textContent = C.email; a.href = "mailto:" + C.email; });
  $$("[data-link]").forEach(function (a) { var u = (C.links || {})[a.getAttribute("data-link")]; if (u) { a.href = u; a.target = "_blank"; a.rel = "noopener"; } });
  $$("[data-year]").forEach(function (n) { n.textContent = new Date().getFullYear(); });
  $$("[data-empresa]").forEach(function (n) {
    var e = C.empresa || {};
    if (e.razao && e.cnpj) { n.innerHTML = esc(e.razao) + " · CNPJ <span class=\"mono\">" + esc(e.cnpj) + "</span>"; }
    else if (PREVIEW) { n.innerHTML = "<span class=\"ph\">Razão social e CNPJ entram aqui</span>"; }
    else { n.remove(); }
  });

  /* Menu no celular */
  var mb = $(".menu-btn"), menu = $("#menu");
  if (mb && menu) {
    function setMenu(open) {
      document.documentElement.classList.toggle("menu-open", open);
      menu.classList.toggle("open", open);
      menu.setAttribute("aria-hidden", open ? "false" : "true");
      mb.setAttribute("aria-expanded", open ? "true" : "false");
      mb.setAttribute("aria-label", open ? "Fechar menu" : "Abrir menu");
      if (open) { var f = $("a", menu); if (f) window.setTimeout(function () { f.focus({ preventScroll: true }); }, 350); } else mb.focus({ preventScroll: true });
    }
    mb.addEventListener("click", function () { setMenu(!menu.classList.contains("open")); });
    $$("a", menu).forEach(function (a) { a.addEventListener("click", function () { setMenu(false); }); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && menu.classList.contains("open")) setMenu(false); });
  }

  /* Prévia: ligar e desligar o conteúdo de exemplo */
  function examplesOn() { return PREVIEW && get("exemplos") !== "off"; }
  function paintToggle() {
    var b = $("#prev-toggle"), l = $("#prev-label");
    if (!b || !l) return;
    l.textContent = examplesOn() ? "Prévia: exemplos ligados" : "Prévia: como no lançamento";
    b.textContent = examplesOn() ? "Ver sem exemplos" : "Ver com exemplos";
  }
  var pt = $("#prev-toggle");
  if (pt) {
    pt.addEventListener("click", function () { set("exemplos", examplesOn() ? "off" : "on"); paintToggle(); renderProofs(); });
    paintToggle();
  }

  /* Provas */
  function renderProofs() {
    var sec = $("#provas");
    if (!sec) return;
    var ex = examplesOn();
    var p = ex ? EX.provas : (C.provas || {});
    var n = p.numeros || [], d = p.depoimentos || [], c = p.casos || [];
    if (!n.length && !d.length && !c.length) { sec.hidden = true; return; }
    sec.hidden = false;
    var tag = ex ? "<span class=\"tag-ex\">Exemplo</span>" : "";
    var h = "<div class=\"wrap\"><h2 class=\"h2\">Resultados de quem já trabalhou comigo" + tag + "</h2>";
    if (n.length) {
      h += "<div class=\"pf-grid pf-nums\">" + n.map(function (x) { return "<div class=\"bx pf-num\"><div class=\"pf-big\">" + esc(x.valor) + "</div><p class=\"pf-cap\">" + esc(x.legenda) + "</p></div>"; }).join("") + "</div>";
    }
    if (d.length) {
      h += "<div class=\"pf-grid pf-quotes\">" + d.map(function (x) { var ini = (x.autor || "?").trim().charAt(0).toUpperCase(); return "<blockquote class=\"bx pf-q\"><p>" + esc(x.texto) + "</p><cite><span class=\"pf-av\" aria-hidden=\"true\">" + esc(ini) + "</span>" + esc(x.autor) + "</cite></blockquote>"; }).join("") + "</div>";
    }
    if (c.length) {
      h += "<div class=\"pf-grid pf-cases\">" + c.map(function (x) {
        return "<article class=\"bx pf-case\"><h3>" + esc(x.titulo) + "</h3><dl><div class=\"pf-row\"><dt>Situação</dt><dd>" + esc(x.situacao) + "</dd></div><div class=\"pf-row\"><dt>O que fiz</dt><dd>" + esc(x.feito) + "</dd></div><div class=\"pf-row res\"><dt>Resultado</dt><dd>" + esc(x.resultado) + "</dd></div></dl></article>";
      }).join("") + "</div>";
    }
    sec.innerHTML = h + "</div>";
  }
  renderProofs();
  document.addEventListener("pointermove", function (e) {
    var t = e.target.closest ? e.target.closest(".bx") : null;
    if (!t) return;
    var r = t.getBoundingClientRect();
    t.style.setProperty("--mx", (e.clientX - r.left) + "px"); t.style.setProperty("--my", (e.clientY - r.top) + "px");
  }, { passive: true });

  /* Blog: reforços em JavaScript. A lista, as categorias e a paginação já funcionam sem ele. */
  (function blog() {
    var box = $("#posts"), nav = $("#pager");
    function sem(t) { return String(t || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }
    /* Carregar mais: busca a próxima página e acrescenta os cartões */
    if (box && nav) {
      var nxt = nav.querySelector("a[rel=next]");
      if (nxt) {
        var wrap = document.createElement("div"); wrap.className = "more-wrap";
        var btn = document.createElement("button"); btn.type = "button"; btn.className = "btn btn-ghost"; btn.textContent = "Carregar mais artigos";
        wrap.appendChild(btn); nav.parentNode.insertBefore(wrap, nav); nav.hidden = true;
        var url = nxt.getAttribute("href");
        btn.addEventListener("click", function () {
          btn.disabled = true;
          fetch(url, { credentials: "same-origin" }).then(function (r) { return r.ok ? r.text() : Promise.reject(); }).then(function (t) {
            var d = new DOMParser().parseFromString(t, "text/html");
            $$("#posts > .post", d).forEach(function (c) { box.appendChild(document.importNode(c, true)); });
            var n2 = d.querySelector("#pager a[rel=next]");
            if (n2) { url = n2.getAttribute("href"); btn.disabled = false; } else { wrap.parentNode.removeChild(wrap); }
          }).catch(function () { nav.hidden = false; wrap.parentNode.removeChild(wrap); });
        });
      }
    }
    /* Busca por assunto: usa a lista de todos os artigos (blog/indice.json) */
    var form = $("#blog-busca");
    if (form) {
      form.hidden = false;
      var q = $("#blog-q"), res = $("#busca-res"), idx = null, pend = false;
      function mostrar() {
        var t = sem(q.value).trim();
        if (!t) { res.innerHTML = ""; return; }
        var f = (idx || []).filter(function (p) { return sem(p.t + " " + p.r + " " + p.c).indexOf(t) > -1; }).slice(0, 8);
        res.innerHTML = f.length ? f.map(function (p) { return "<a href=\"" + esc(p.u) + "\"><b>" + esc(p.t) + "</b><span>" + esc(p.c) + " · " + esc(p.d) + "</span></a>"; }).join("") : "<p>Nenhum artigo encontrado. Tente outra palavra.</p>";
      }
      function carregar() {
        if (idx || pend) return; pend = true;
        fetch(BASE + "blog/indice.json", { credentials: "same-origin" }).then(function (r) { return r.json(); }).then(function (j) { idx = j; mostrar(); }).catch(function () { pend = false; });
      }
      q.addEventListener("focus", carregar); q.addEventListener("input", function () { carregar(); mostrar(); });
    }
  })();

  /* Globo: gira sem parar, devagar. Ao rolar a página, gira mais rápido e com mais força. */
  (function globe() {
    var cv = $("#globe");
    if (!cv) return;
    var mobile = window.matchMedia("(max-width: 900px)").matches;
    /* celular: sequência leve (19 quadros, 600 px, nomes versionados) vinda de window.GLOBO_M; computador: 38 quadros, como antes */
    var G = mobile && window.GLOBO_M ? window.GLOBO_M : null;
    var conn = navigator.connection || {};
    var lite = reduce || conn.saveData || /(^|-)2g$/.test(conn.effectiveType || "");   /* movimento reduzido, Save-Data ou conexão lenta: só a imagem parada */
    var N = G ? G.f.length : 38;
    var F = Math.round(N * 0.18);            /* quadros dissolvidos na emenda do ciclo */
    var dir = G ? G.dir : BASE + "assets/globo-d/";
    cv.width = G ? 600 : 960; cv.height = G ? 545 : 872;
    var ctx = cv.getContext("2d");
    var frames = new Array(N);
    var BASE_FPS = G ? 0.9 : 1.8;            /* velocidade parada: um ciclo a cada ~17 s (o celular tem metade dos quadros, então metade do passo) */
    var pos = 0, lastT = 0, lastY = window.scrollY, vel = 0, boost = 0;
    function name(i) { return G ? G.f[i] : ("00" + i).slice(-3) + ".webp"; }
    var got = 0, READY = mobile ? 10 : 12;   /* a abertura libera a tela com poucos quadros; o resto carrega em segundo plano */
    function load(i) {
      return new Promise(function (res) {
        var im = new Image();
        im.onload = function () { frames[i] = im; got++; if (!G) window.__globeProgress = Math.min(1, got / READY); res(); };
        im.onerror = function () { res(); };
        im.src = dir + name(i);
      });
    }
    function at(i) {
      i = clamp(Math.floor(i), 0, N - 1);
      while (i >= 0 && !frames[i]) i--;
      return i >= 0 ? frames[i] : null;
    }
    function blit(img, a) {
      if (!img) return;
      ctx.globalAlpha = a;
      ctx.drawImage(img, 0, 0, cv.width, cv.height);
    }
    function draw() {
      var i = Math.floor(pos), f = pos - i;
      var next = (i + 1 >= N) ? F : i + 1;
      ctx.clearRect(0, 0, cv.width, cv.height);
      /* mistura entre quadros vizinhos para o giro ficar contínuo, sem degraus */
      blit(at(i), 1);
      if (f > 0.01) blit(at(next), f);
      /* emenda do ciclo: dissolve o fim do clipe no começo */
      if (pos > N - F) {
        var k = (pos - (N - F)) / F;
        blit(at(pos - (N - F)), clamp(k, 0, 1));
      }
      ctx.globalAlpha = 1;
    }
    function tick(t) {
      if (!vis) { lastT = 0; window.requestAnimationFrame(tick); return; }   /* fora da tela: não gasta processador */
      var dt = lastT ? Math.min(0.05, (t - lastT) / 1000) : 0.016;
      lastT = t;
      var y = window.scrollY, dy = Math.abs(y - lastY);
      lastY = y;
      /* velocidade da rolagem (suavizada) + quanto já desceu na página */
      vel += (dy / Math.max(dt, 0.001) - vel) * Math.min(1, dt * 8);
      var depth = clamp(y / Math.max(1, window.innerHeight * 1.2), 0, 1);
      var target = clamp(vel / 1800, 0, 1) * 5.5 + depth * 0.9;
      boost += (target - boost) * Math.min(1, dt * (target > boost ? 6 : 1.6));
      var speed = BASE_FPS * (1 + boost * 4.5);
      if (document.documentElement.classList.contains("loading")) speed = BASE_FPS * 2.6;
      pos += speed * dt;
      var c = 0; while (c < N && frames[c]) c++;
      if (c >= N) { if (pos >= N) pos = F + (pos - N); }
      else if (c > 1 && pos >= c - 1) pos = pos % (c - 1);
      else if (c <= 1) pos = 0;
      draw();
      window.requestAnimationFrame(tick);
    }
    var vis = true, onVisible = null;
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) {
        vis = es[0].isIntersecting;
        if (vis && onVisible) { var f = onVisible; onVisible = null; f(); }
      }, { rootMargin: "200px" }).observe(cv);
    }
    function whenVisible(fn) { if (vis) fn(); else onVisible = fn; }
    function whenIdle(fn) {
      function go() { (window.requestIdleCallback || function (f) { window.setTimeout(f, 300); })(fn, { timeout: 2500 }); }
      if (document.readyState === "complete") go(); else window.addEventListener("load", go, { once: true });
    }
    window.__globeProgress = 0;
    if (G) {
      /* CELULAR: a primeira tela é a imagem parada (poster, no HTML). Ela libera a abertura assim que carrega.
         A sequência só começa a baixar depois da primeira renderização e da página carregada, e só se o globo estiver visível. */
      var po = $("#globe-poster"), posterOk = function () { window.__globeProgress = 1; };
      if (!po || (po.complete && po.naturalWidth)) posterOk();
      else { po.addEventListener("load", posterOk); po.addEventListener("error", posterOk); }
      if (lite) return;
      window.requestAnimationFrame(function () { window.requestAnimationFrame(function () {
        whenIdle(function () { whenVisible(function () {
          var live = false;
          function contiguous() { var c = 0; while (c < N && frames[c]) c++; return c; }
          function goLive() {
            if (live) return; live = true;
            pos = 0; draw();
            cv.parentNode.classList.add("live");
            window.requestAnimationFrame(tick);
          }
          load(0).then(function () {              /* o quadro 0 é o próprio poster, já no cache */
            var i = 1;
            function next() {
              if (i >= N) { goLive(); return; }
              var batch = [];
              for (var n = 0; n < 5 && i < N; n++, i++) batch.push(load(i));
              Promise.all(batch).then(function () { if (contiguous() >= 6) goLive(); window.setTimeout(next, 30); });
            }
            next();
          });
        }); });
      }); });
      return;
    }
    /* COMPUTADOR: igual a antes (só a regra de "imagem parada" vale também aqui) */
    load(0).then(function () {
      pos = 0; draw();
      if (lite) return;
      var i = 1;
      function next() {
        if (i >= N) return;
        var batch = [];
        for (var n = 0; n < 80 && i < N; n++, i++) batch.push(load(i));
        Promise.all(batch).then(function () { window.setTimeout(next, 0); });
      }
      window.setTimeout(next, 100);
      window.requestAnimationFrame(tick);
    });
  })();

  /* Serviços: a linha escolhida mostra o painel ao lado */
  (function services() {
    var tabs = $$(".sv"), panels = $$(".sv-p");
    if (!tabs.length) return;
    function pick(id, focus) {
      tabs.forEach(function (b) { var on = b.getAttribute("aria-controls") === id; b.setAttribute("aria-selected", on ? "true" : "false"); b.tabIndex = on ? 0 : -1; if (on && focus) b.focus(); });
      panels.forEach(function (p) { var on = p.id === id; p.hidden = !on; });
      track("servico_escolhido", { servico: id });
    }
    tabs.forEach(function (b, i) {
      b.tabIndex = i === 0 ? 0 : -1;
      b.addEventListener("click", function () { pick(b.getAttribute("aria-controls")); });
      b.addEventListener("mouseenter", function () { if (window.matchMedia("(hover: hover)").matches) pick(b.getAttribute("aria-controls")); });
      b.addEventListener("keydown", function (e) {
        var k = e.key === "ArrowDown" || e.key === "ArrowRight" ? 1 : (e.key === "ArrowUp" || e.key === "ArrowLeft" ? -1 : 0);
        if (!k) return;
        e.preventDefault();
        pick(tabs[(i + k + tabs.length) % tabs.length].getAttribute("aria-controls"), true);
      });
    });
  })();

  /* Para quem: alterna entre "é" e "não é" */
  (function fit() {
    var tabs = $$(".fit-tabs button");
    if (!tabs.length) return;
    tabs.forEach(function (b) {
      b.addEventListener("click", function () {
        tabs.forEach(function (o) {
          var on = o === b;
          o.setAttribute("aria-selected", on ? "true" : "false");
          var pn = document.getElementById(o.getAttribute("aria-controls"));
          if (pn) pn.hidden = !on;
        });
        track("para_quem", { aba: b.textContent.trim() });
      });
    });
  })();

  /* Compromissos: no celular, destaca a linha mais perto do meio da tela */
  (function commits() {
    var rows = $$(".cm");
    if (!rows.length || reduce) return;
    var mq = window.matchMedia("(max-width: 860px)"), tick = false;
    function upd() {
      tick = false;
      var mid = window.innerHeight / 2, best = null, bd = 1e9;
      rows.forEach(function (r) {
        r.classList.remove("on");
        if (!mq.matches) return;
        var b = r.getBoundingClientRect(), d = Math.abs(b.top + b.height / 2 - mid);
        if (b.bottom > 0 && b.top < window.innerHeight && d < bd) { bd = d; best = r; }
      });
      if (best && bd < window.innerHeight * 0.32) best.classList.add("on");
    }
    window.addEventListener("scroll", function () { if (!tick) { tick = true; window.requestAnimationFrame(upd); } }, { passive: true });
    window.addEventListener("resize", upd);
    upd();
  })();

  /* Abertura: frases sobem, cor muda e números correm ao fundo conforme a rolagem */
  (function hero() {
    var h = $(".hero-track");
    if (!h) return;
    var sticky = $(".hero-sticky");
    var cv = $("#nums"), ctx = cv ? cv.getContext("2d") : null;
    var cols = [], cw = 0, ch = 0, dpr = Math.min(2, window.devicePixelRatio || 1), cell = 26, fs = 12;
    var pinned = false, p = 0;
    function size() {
      if (!cv) return;
      var r = cv.getBoundingClientRect();
      cw = r.width; ch = r.height;
      cv.width = Math.round(cw * dpr); cv.height = Math.round(ch * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var small = cw < 700; cell = small ? 40 : 56; fs = small ? 12 : 14;
      var n = Math.ceil(cw / cell) + 1, rows = Math.ceil(ch / cell) + 2;
      cols = [];
      for (var c = 0; c < n; c++) {
        var d = [];
        for (var k = 0; k < rows; k++) d.push(Math.random() < 0.62 ? "" : String(Math.floor(Math.random() * 10)));
        cols.push({ d: d, sp: 9 + Math.random() * 16, off: Math.random() * cell * rows, a: 0.35 + Math.random() * 0.65, big: Math.random() < 0.18 });
      }
    }
    function drawNums(dt) {
      if (!ctx) return;
      ctx.clearRect(0, 0, cw, ch);
      ctx.font = "400 " + fs + "px Outfit, system-ui, sans-serif";
      ctx.textAlign = "center";
      var cx = cw * 0.5, cy = ch * 0.52, R = Math.min(cw, ch * 1.5) * 0.7;
      var rowsN = cols[0] ? cols[0].d.length : 0, H = rowsN * cell;
      for (var c = 0; c < cols.length; c++) {
        var col = cols[c];
        col.off = (col.off + col.sp * dt * (1 + p * 5)) % H;
        var x = c * cell + cell / 2;
        for (var k = 0; k < rowsN; k++) {
          var t = col.d[k]; if (!t) continue;
          var y = ((k * cell - col.off) % H + H) % H - cell;
          var dx = (x - cx) / R, dy = (y - cy) / (R * 0.9), dd = Math.sqrt(dx * dx + dy * dy);
          var a = Math.pow(Math.max(0, 1 - dd), 0.8) * col.a * (0.75 + p * 0.25);
          if (a < 0.03) continue;
          ctx.fillStyle = "rgba(" + (80 + Math.round(90 * (1 - dd))) + "," + (110 + Math.round(70 * (1 - dd))) + ",255," + a.toFixed(3) + ")";
          if (col.big) { ctx.font = "200 " + Math.round(fs * 2.6) + "px Outfit, system-ui, sans-serif"; ctx.fillText(t, x, y); ctx.font = "400 " + fs + "px Outfit, system-ui, sans-serif"; } else ctx.fillText(t, x, y);
        }
        if (Math.random() < 0.02) col.d[Math.floor(Math.random() * rowsN)] = String(Math.floor(Math.random() * 10));
      }
    }
    function update() {
      pinned = window.getComputedStyle(sticky).position === "sticky";
      if (pinned) {
        var total = h.offsetHeight - sticky.offsetHeight;
        var r = h.getBoundingClientRect();
        p = clamp((HH - r.top) / Math.max(1, total), 0, 1);
      } else p = 0;
      var pa = clamp((p - 0.32) / 0.2, 0, 1), b1 = clamp((p - 0.46) / 0.2, 0, 1), b2 = clamp((p - 0.56) / 0.2, 0, 1);
      h.style.setProperty("--p", p.toFixed(3));
      h.style.setProperty("--pa", pa.toFixed(3));
      h.style.setProperty("--b1", reduce ? 1 : b1.toFixed(3));
      h.style.setProperty("--b2", reduce ? 1 : b2.toFixed(3));
    }
    size(); update();
    window.addEventListener("resize", function () { size(); update(); });
    window.addEventListener("scroll", update, { passive: true });
    var root = document.documentElement, globeEl = $(".hero-globe");
    function finish() {
      root.classList.remove("loading");
      h.classList.add("done", "go");
      h.style.removeProperty("--gl");
      window.setTimeout(function () { h.classList.add("settled"); }, 2600);
    }
    if (reduce || window.scrollY > 60) { drawNums(0); finish(); if (reduce) return; }
    else {
      /* Abertura rápida, sem contador: o globo surge em ~0,6 s e o texto entra assim que os primeiros quadros chegam
         (no máximo 2,5 s de espera, mesmo com internet lenta). */
      root.classList.add("loading");
      var t0 = performance.now(), done = false;
      (function wait(now) {
        var el = (now - t0) / 1000;
        var ready = (window.__globeProgress || 0) >= 1;
        var seqM = window.GLOBO_M && window.matchMedia("(max-width: 900px)").matches;   /* celular: o poster já está na tela desde a primeira pintura */
        var T = seqM ? 0.08 : 0.6;
        var k = clamp(el / T, 0, 1);
        if (!seqM) h.style.setProperty("--gl", Math.pow(ready ? k : Math.min(k, 0.25), 0.8).toFixed(3));
        if (!done && ((ready && el >= T) || el > 2.5)) { done = true; finish(); return; }
        window.requestAnimationFrame(wait);
      })(t0);
    }
    var last = 0, acc = 0;
    (function loop(t) {
      var dt = last ? Math.min(0.1, (t - last) / 1000) : 0.016; last = t; acc += dt;
      if (acc > 1 / 30) { drawNums(acc); acc = 0; }
      window.requestAnimationFrame(loop);
    })(0);
  })();

  $$(".opt").forEach(function (a) {
    a.addEventListener("click", function () {
      track("resposta_topo", { resposta: a.textContent.trim() });
      if (window.__spinGlobe) window.__spinGlobe();
    });
  });

  /* Notebook: a página de exemplo rola conforme a seção passa pela tela */
  (function laptop() {
    var scr = $(".lap-screen"), lp = $(".lp");
    if (!scr || !lp) return;
    var dirty = true;
    function upd() {
      dirty = false;
      var r = scr.getBoundingClientRect(), vh = window.innerHeight;
      var p = reduce ? 0 : clamp((vh * 0.9 - r.top) / (vh * 0.9 + r.height * 0.2), 0, 1);
      var max = Math.max(0, lp.offsetHeight - scr.clientHeight);
      lp.style.transform = "translate3d(0," + (-p * max).toFixed(1) + "px,0)";
    }
    function loop() { if (dirty) upd(); window.requestAnimationFrame(loop); }
    window.addEventListener("scroll", function () { dirty = true; }, { passive: true });
    window.addEventListener("resize", function () { dirty = true; });
    window.requestAnimationFrame(loop);
  })();

  /* Formulário */
  var form = $("#form-contato");
  if (form) {
    var msg = $("#form-msg");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (form.website && form.website.value) return;
      var nome = form.nome.value.trim(), tel = form.whats.value.replace(/\D/g, ""), mail = form.email.value.trim(), txt = form.mensagem.value.trim();
      function bad(t) { msg.className = "form-msg err"; msg.textContent = t; }
      if (!nome) return bad("Escreva o seu nome.");
      if (tel.length < 10) return bad("Escreva o WhatsApp com DDD, por exemplo (21) 90000-0000.");
      if (mail && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(mail)) return bad("Confira o e-mail: falta algo, como o @ ou o final .com.");
      if (!txt) return bad("Conte em poucas palavras o que você precisa.");
      track("envio_formulario", {});
      if (C.formEndpoint) {
        msg.className = "form-msg"; msg.textContent = "Enviando...";
        var ctl = new AbortController(); var to = window.setTimeout(function () { ctl.abort(); }, 20000);
        fetch(C.formEndpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ nome: nome, whatsapp: tel, email: mail, mensagem: txt }), signal: ctl.signal })
          .then(function (r) { if (!r.ok) throw new Error("x"); msg.className = "form-msg ok"; msg.textContent = "Recebi sua mensagem. Respondo pelo WhatsApp."; form.reset(); })
          .catch(function () { bad("Não consegui enviar agora. Tente de novo ou chame no WhatsApp."); })
          .then(function () { window.clearTimeout(to); });
      } else {
        msg.className = "form-msg ok";
        msg.textContent = "Prévia: na versão publicada, esta mensagem chega no e-mail do Gabriel.";
      }
    });
  }

  /* Aviso de cookies */
  var ck = $("#cookie");
  if (ck) {
    if (!CONSENT.get()) { ck.hidden = false; }      /* já escolheu (aceitou ou recusou): não mostra de novo */
    $("#ck-ok").addEventListener("click", function () { CONSENT.accept(); ck.hidden = true; });
    $("#ck-no").addEventListener("click", function () { CONSENT.decline(); ck.hidden = true; });
    var pf = $("#ck-prefs");
    if (pf) { pf.addEventListener("click", function () { CONSENT.reset(); ck.hidden = false; $("#ck-ok").focus(); }); }
  }
})();
