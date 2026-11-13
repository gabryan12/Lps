import { EmailMessage } from "cloudflare:email";

const FROM = "briefing@gabrieldiniztrafego.com.br";
const TO = "sagatrafego@gmail.com";
const FROM_NAME = "Gabriel Diniz Tráfego";
const API = "/forms/api/";

const MIN_FILL_MS = 30 * 1000; // tempo mínimo desde o início do briefing
const MAX_BODY = { briefing: 150000, inicio: 8000, progresso: 2000 };
const MAX_TOTAL = 60000; // soma dos textos das respostas
const MAX_ITEMS = 200;
const DRAFT_TTL = 60 * 60 * 24 * 60; // rascunhos expiram em 60 dias

const EMAIL_RE = /^[^\s@<>"',;:]+@[^\s@<>"',;:]+\.[^\s@<>"',;:]+$/;
const ID_RE = /^[A-Za-z0-9-]{8,64}$/;

const json = (obj, status = 200, headers = {}) =>
  new Response(JSON.stringify(obj), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
      "x-robots-tag": "noindex, nofollow",
      ...headers,
    },
  });

// Remove quebras de linha e caracteres de controle (evita injeção de cabeçalhos)
const CTRL = new RegExp("[\\r\\n\\u0000-\\u001f\\u007f\\u2028\\u2029]+", "g");
const oneLine = (s) => String(s ?? "").replace(CTRL, " ").trim();
const clip = (s, n) => String(s ?? "").slice(0, n);
const short = (s, n) => clip(oneLine(s), n);

function b64utf8(str) {
  const bytes = new TextEncoder().encode(str);
  let bin = "";
  for (let i = 0; i < bytes.length; i += 0x8000) {
    bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
  }
  return btoa(bin);
}

// Cabeçalho em "encoded-words" (RFC 2047), respeitando o limite de 75 caracteres
function encodeHeader(str) {
  const enc = new TextEncoder();
  const chunks = [];
  let cur = "";
  let curBytes = 0;
  for (const ch of str) {
    const n = enc.encode(ch).length;
    if (curBytes + n > 45) {
      chunks.push(cur);
      cur = "";
      curBytes = 0;
    }
    cur += ch;
    curBytes += n;
  }
  if (cur) chunks.push(cur);
  return chunks.map((c) => `=?UTF-8?B?${b64utf8(c)}?=`).join("\r\n ");
}

const fold76 = (s) => (s.match(/.{1,76}/g) || []).join("\r\n");

function buildRaw(subject, text, replyTo) {
  const headers = [
    `From: ${encodeHeader(FROM_NAME)} <${FROM}>`,
    `To: <${TO}>`,
    `Subject: ${encodeHeader(subject)}`,
    `Date: ${new Date().toUTCString()}`,
    `Message-ID: <${crypto.randomUUID()}@gabrieldiniztrafego.com.br>`,
    "MIME-Version: 1.0",
    "Content-Type: text/plain; charset=UTF-8",
    "Content-Transfer-Encoding: base64",
  ];
  if (replyTo) headers.splice(3, 0, `Reply-To: <${replyTo}>`);
  return headers.join("\r\n") + "\r\n\r\n" + fold76(b64utf8(text)) + "\r\n";
}

async function sendMail(env, subject, text, replyTo) {
  const raw = buildRaw(subject, text, replyTo);
  if (!env.EMAIL) {
    console.log("[DEV] E-mail montado (sem binding, não enviado):\n" + raw);
    return;
  }
  await env.EMAIL.send(new EmailMessage(FROM, TO, raw));
}

/* ---------- KV (opcional em dev) ---------- */
async function kvGet(env, key) {
  if (!env.BRIEFINGS) return null;
  try {
    return await env.BRIEFINGS.get(key, "json");
  } catch (e) {
    console.error("KV get falhou:", e && e.message);
    return null;
  }
}
async function kvPut(env, key, value, opts) {
  if (!env.BRIEFINGS) return false;
  try {
    await env.BRIEFINGS.put(key, JSON.stringify(value), opts);
    return true;
  } catch (e) {
    console.error("KV put falhou:", e && e.message);
    return false;
  }
}

/* ---------- validação ---------- */
async function readJson(request, max) {
  const text = await request.text();
  if (text.length > max) return { error: json({ ok: false, error: "too_big" }, 413) };
  try {
    const data = JSON.parse(text);
    if (!data || typeof data !== "object" || Array.isArray(data)) throw new Error("shape");
    return { data };
  } catch {
    return { error: json({ ok: false, error: "invalid_json" }, 400) };
  }
}

function cleanItems(raw) {
  if (!Array.isArray(raw) || raw.length === 0 || raw.length > MAX_ITEMS) return null;
  const items = [];
  let total = 0;
  for (const it of raw) {
    if (!it || typeof it !== "object") return null;
    const sec = short(it.sec, 120);
    const n = short(it.n, 20);
    const q = short(it.q, 400);
    const a = clip(String(it.a ?? "").replace(/\r\n?/g, "\n").trim(), 6000);
    if (!a) continue;
    total += sec.length + n.length + q.length + a.length;
    if (total > MAX_TOTAL) return "too_big";
    items.push({ sec, n, q, a });
  }
  return items.length ? items : null;
}

function buildBriefingText(items, meta) {
  const lines = ["NOVO BRIEFING RECEBIDO", ""];
  if (meta.nome) lines.push(`Nome: ${meta.nome}`);
  if (meta.negocio) lines.push(`Negócio: ${meta.negocio}`);
  if (meta.ref) lines.push(`Origem (ref): ${meta.ref}`);
  lines.push(`ID: ${meta.id}`);
  let lastSec = null;
  for (const it of items) {
    if (it.sec !== lastSec) {
      lines.push("", "==============================", it.sec.toUpperCase(), "==============================", "");
      lastSec = it.sec;
    }
    lines.push(`${it.n}. ${it.q}`);
    lines.push(it.a.split("\n").map((l) => "   " + l).join("\n"));
    lines.push("");
  }
  return lines.join("\n");
}

/* ---------- rotas ---------- */
async function handleBriefing(request, env) {
  const { data, error } = await readJson(request, MAX_BODY.briefing);
  if (error) return error;

  // Honeypot preenchido: finge sucesso e descarta
  if (typeof data.website === "string" && data.website.trim() !== "") return json({ ok: true });

  const id = String(data.id ?? "");
  if (!ID_RE.test(id)) return json({ ok: false, error: "invalid_id" }, 400);

  const items = cleanItems(data.items);
  if (items === "too_big") return json({ ok: false, error: "too_big" }, 413);
  if (!items) return json({ ok: false, error: "invalid_items" }, 400);

  const draft = await kvGet(env, `rascunho:${id}`);
  const started = Number(draft?.startedAt ?? data.started);
  if (!Number.isFinite(started) || Date.now() - started < MIN_FILL_MS) {
    return json({ ok: true }); // rápido demais para ser uma pessoa: descarta em silêncio
  }

  const prior = await kvGet(env, `briefing:${id}`);
  if (prior && prior.emailSent) return json({ ok: true }); // reenvio de algo já entregue

  const meta = {
    id,
    nome: short(data.nome, 80),
    negocio: short(data.negocio, 120),
    ref: short(data.ref, 60),
  };
  const replyTo = EMAIL_RE.test(oneLine(data.email)) ? oneLine(data.email) : null;
  const record = { id, receivedAt: new Date().toISOString(), meta, email: replyTo, items, emailSent: false };

  // 1) backup primeiro: o dado não se perde se o e-mail falhar
  const saved = await kvPut(env, `briefing:${id}`, record);

  // 2) e-mail
  let mailed = false;
  try {
    await sendMail(env, `Novo briefing — ${meta.negocio || meta.nome || "sem nome informado"}`, buildBriefingText(items, meta), replyTo);
    mailed = true;
  } catch (err) {
    console.error("Falha ao enviar e-mail:", err && err.message ? err.message : err);
  }

  if (saved) {
    record.emailSent = mailed;
    await kvPut(env, `briefing:${id}`, record);
    await kvPut(env, `rascunho:${id}`, { ...(draft || {}), id, status: "enviado", updatedAt: Date.now() }, { expirationTtl: DRAFT_TTL });
  }

  if (!saved && !mailed) return json({ ok: false, error: "send_failed" }, 502);
  return json({ ok: true });
}

async function handleInicio(request, env) {
  const { data, error } = await readJson(request, MAX_BODY.inicio);
  if (error) return error;
  if (typeof data.website === "string" && data.website.trim() !== "") return json({ ok: true });

  const id = String(data.id ?? "");
  if (!ID_RE.test(id)) return json({ ok: false, error: "invalid_id" }, 400);

  const nome = short(data.nome, 80);
  const negocio = short(data.negocio, 120);
  const whatsapp = short(data.whatsapp, 30);
  const email = short(data.email, 120);
  const ref = short(data.ref, 60);
  if (!nome || whatsapp.replace(/\D/g, "").length < 10 || !EMAIL_RE.test(email)) {
    return json({ ok: false, error: "invalid_contact" }, 400);
  }

  const draft = await kvGet(env, `rascunho:${id}`);
  if (draft && draft.inicioSent) return json({ ok: true, dup: true }); // uma vez por sessão

  const startedAt = Number(draft?.startedAt) || Date.now();
  await kvPut(
    env,
    `rascunho:${id}`,
    { id, startedAt, nome, negocio, whatsapp, email, ref, step: draft?.step ?? 0, status: "iniciado", inicioSent: true, updatedAt: Date.now() },
    { expirationTtl: DRAFT_TTL }
  );

  const text = [
    "BRIEFING INICIADO",
    "",
    `Nome: ${nome}`,
    `Negócio: ${negocio || "(ainda não informado)"}`,
    `WhatsApp: ${whatsapp}`,
    `E-mail: ${email}`,
    `Origem (ref): ${ref || "(sem ref)"}`,
    `Iniciado em: ${new Date(startedAt).toUTCString()}`,
    `ID: ${id}`,
    "",
    "A pessoa começou a preencher o briefing e autorizou o uso destes dados.",
  ].join("\n");
  try {
    await sendMail(env, `Briefing iniciado — ${nome}${negocio ? " (" + negocio + ")" : ""}`, text, EMAIL_RE.test(email) ? email : null);
  } catch (err) {
    console.error("Falha ao enviar aviso de início:", err && err.message ? err.message : err);
  }
  return json({ ok: true });
}

async function handleProgresso(request, env) {
  const { data, error } = await readJson(request, MAX_BODY.progresso);
  if (error) return error;
  const id = String(data.id ?? "");
  const step = Math.trunc(Number(data.step));
  const total = Math.trunc(Number(data.total));
  if (!ID_RE.test(id) || !Number.isFinite(step) || step < 0 || step > 50) return json({ ok: false, error: "invalid" }, 400);

  const draft = await kvGet(env, `rascunho:${id}`);
  if (draft && draft.status !== "enviado") {
    await kvPut(
      env,
      `rascunho:${id}`,
      { ...draft, step: Math.max(Number(draft.step) || 0, step), totalSteps: Number.isFinite(total) ? total : draft.totalSteps, updatedAt: Date.now() },
      { expirationTtl: DRAFT_TTL }
    );
  }
  return json({ ok: true });
}

const ROUTES = { briefing: handleBriefing, inicio: handleInicio, progresso: handleProgresso };

export default {
  async fetch(request, env) {
    const { pathname } = new URL(request.url);
    if (!pathname.startsWith(API)) {
      if (env.ASSETS) return env.ASSETS.fetch(request);
      return new Response("Not found", { status: 404 });
    }
    const name = pathname.slice(API.length).replace(/\/$/, "");
    const handler = Object.prototype.hasOwnProperty.call(ROUTES, name) ? ROUTES[name] : null;
    if (!handler) return json({ ok: false, error: "not_found" }, 404);
    if (request.method !== "POST") return json({ ok: false, error: "method_not_allowed" }, 405, { Allow: "POST" });
    try {
      return await handler(request, env);
    } catch (err) {
      console.error("Erro inesperado:", err && err.message ? err.message : err);
      return json({ ok: false, error: "server_error" }, 500);
    }
  },
};
