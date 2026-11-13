import { EmailMessage } from "cloudflare:email";

const FROM = "briefing@gabrieldiniztrafego.com.br";
const TO = "sagatrafego@gmail.com";
const FROM_NAME = "Gabriel Diniz Tráfego";

const MAX_BODY = 150000; // tamanho bruto da requisição
const MAX_TOTAL = 60000; // soma dos textos das respostas
const MAX_ITEMS = 200;

const EMAIL_RE = /^[^\s@<>"',;:]+@[^\s@<>"',;:]+\.[^\s@<>"',;:]+$/;

const json = (obj, status = 200, headers = {}) =>
  new Response(JSON.stringify(obj), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
      ...headers,
    },
  });

// Remove quebras de linha e caracteres de controle (evita injeção de cabeçalhos)
const oneLine = (s) =>
  String(s ?? "")
    .replace(new RegExp("[\\r\\n\\u0000-\\u001f\\u007f\\u2028\\u2029]+", "g"), " ")
    .trim();

const clip = (s, n) => String(s ?? "").slice(0, n);

function b64utf8(str) {
  const bytes = new TextEncoder().encode(str);
  let bin = "";
  for (let i = 0; i < bytes.length; i += 0x8000) {
    bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
  }
  return btoa(bin);
}

// Codifica um cabeçalho em "encoded-words" (RFC 2047), respeitando o limite de 75 caracteres
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

function cleanItems(raw) {
  if (!Array.isArray(raw) || raw.length === 0 || raw.length > MAX_ITEMS) return null;
  const items = [];
  let total = 0;
  for (const it of raw) {
    if (!it || typeof it !== "object") return null;
    const sec = clip(oneLine(it.sec), 120);
    const n = clip(oneLine(it.n), 20);
    const q = clip(oneLine(it.q), 400);
    const a = clip(String(it.a ?? "").replace(/\r\n?/g, "\n").trim(), 6000);
    if (!a) continue;
    total += sec.length + n.length + q.length + a.length;
    if (total > MAX_TOTAL) return "too_big";
    items.push({ sec, n, q, a });
  }
  return items.length ? items : null;
}

function buildText(items) {
  const lines = ["NOVO BRIEFING RECEBIDO", ""];
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

function buildRaw(items, officeName, replyTo) {
  const subject = `Novo briefing — ${officeName || "sem nome informado"}`;
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
  const body = fold76(b64utf8(buildText(items)));
  return headers.join("\r\n") + "\r\n\r\n" + body + "\r\n";
}

async function handleBriefing(request, env) {
  if (request.method !== "POST") {
    return json({ ok: false, error: "method_not_allowed" }, 405, { Allow: "POST" });
  }

  const text = await request.text();
  if (text.length > MAX_BODY) return json({ ok: false, error: "too_big" }, 413);

  let data;
  try {
    data = JSON.parse(text);
  } catch {
    return json({ ok: false, error: "invalid_json" }, 400);
  }
  if (!data || typeof data !== "object") return json({ ok: false, error: "invalid_json" }, 400);

  // Honeypot: robôs preenchem; finge sucesso e descarta
  if (typeof data.website === "string" && data.website.trim() !== "") {
    return json({ ok: true });
  }

  const items = cleanItems(data.items);
  if (items === "too_big") return json({ ok: false, error: "too_big" }, 413);
  if (!items) return json({ ok: false, error: "invalid_items" }, 400);

  const officeName = clip(items.find((i) => i.n === "1")?.a.replace(/\s+/g, " ") ?? "", 80);
  const emailAnswer = oneLine(items.find((i) => i.n === "4")?.a);
  const replyTo = EMAIL_RE.test(emailAnswer) ? emailAnswer : null;

  const raw = buildRaw(items, officeName, replyTo);

  const { hostname } = new URL(request.url);
  const isDev = ["localhost", "127.0.0.1", "[::1]"].includes(hostname);
  if (isDev || !env.EMAIL) {
    console.log("[DEV] E-mail montado (não enviado):\n" + raw);
    return json({ ok: true, dev: true });
  }

  try {
    await env.EMAIL.send(new EmailMessage(FROM, TO, raw));
  } catch (err) {
    console.error("Falha ao enviar e-mail:", err && err.message ? err.message : err);
    return json({ ok: false, error: "send_failed" }, 502);
  }
  return json({ ok: true });
}

export default {
  async fetch(request, env) {
    const { pathname } = new URL(request.url);
    if (pathname === "/api/briefing") return handleBriefing(request, env);
    if (pathname.startsWith("/api/")) return json({ ok: false, error: "not_found" }, 404);
    if (env.ASSETS) return env.ASSETS.fetch(request);
    return new Response("Not found", { status: 404 });
  },
};
