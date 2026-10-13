---
name: "deploy-cloudflare"
description: "Publica ou atualiza um site/página como Cloudflare Worker direto pela API, sem wrangler e sem terminal. Use quando o usuário pedir para publicar, subir, hospedar, colocar no ar, fazer deploy ou atualizar uma página, landing, dashboard ou demo — e também quando pedir para listar ou apagar workers já publicados."
---

# Deploy de site na Cloudflare sem wrangler

Publica HTML/CSS/JS como Cloudflare Worker usando o conector **cloudflare-api** (Code Mode), que expõe `search` e `execute`. O `execute` roda JavaScript com `cloudflare.request()` e uma variável `accountId` já preenchida — não peça o account ID ao usuário.

## Antes de começar

Se o conteúdo do site ainda não existe, escreva ele primeiro. O deploy é o último passo, não o primeiro. Para páginas com identidade visual, use a skill `frontend-design`.

Se o conector não estiver autorizado, o `execute` falha. Nesse caso avise que é preciso autorizar em Conectores no claude.ai — não tente contornar com curl.

## Deploy

Uma única chamada `execute` faz as duas etapas. As duas são obrigatórias: sem a segunda o script existe mas não tem URL pública.

```js
async () => {
  const name = "NOME-DO-WORKER";           // kebab-case
  const html = "...";                       // HTML completo da página

  const worker =
    'const PAGE=' + JSON.stringify(html) + ';\n' +
    'export default { fetch(request){\n' +
    '  return new Response(PAGE,{headers:{"content-type":"text/html; charset=utf-8"}});\n' +
    '} };\n';

  const metadata = { main_module: "worker.js", compatibility_date: "2025-07-01" };
  const b = "----D" + Date.now();
  const form = [
    "--" + b,
    'Content-Disposition: form-data; name="metadata"',
    "Content-Type: application/json",
    "",
    JSON.stringify(metadata),
    "--" + b,
    'Content-Disposition: form-data; name="worker.js"; filename="worker.js"',
    "Content-Type: application/javascript+module",
    "",
    worker,
    "--" + b + "--",
    ""
  ].join("\r\n");

  const up = await cloudflare.request({
    method: "PUT",
    path: "/accounts/" + accountId + "/workers/scripts/" + name,
    body: form,
    contentType: "multipart/form-data; boundary=" + b,
    rawBody: true
  });
  if (!up.success) return { step: "upload", errors: up.errors };

  const sub = await cloudflare.request({
    method: "POST",
    path: "/accounts/" + accountId + "/workers/scripts/" + name + "/subdomain",
    body: { enabled: true }
  });

  const acct = await cloudflare.request({
    method: "GET",
    path: "/accounts/" + accountId + "/workers/subdomain"
  });

  return { upload: up.success, subdomain: sub.success,
           url: "https://" + name + "." + acct.result.subdomain + ".workers.dev",
           errors: [].concat(up.errors, sub.errors) };
}
```

Detalhes que quebram se mudarem: as linhas do multipart juntam com `\r\n`; `rawBody: true` é obrigatório senão o body vira JSON; o content-type da parte do script é `application/javascript+module`.

## Validação

Sempre confirme com curl antes de entregar a URL. Faça retry curto — **não** use um `sleep` fixo longo:

```bash
for i in $(seq 1 10); do
  c=$(curl -s -o /dev/null -w "%{http_code}" https://NOME.SUBDOMINIO.workers.dev)
  [ "$c" = "200" ] && echo "no ar" && break
  sleep 3
done
```

`error code: 1104` no primeiro hit significa DNS ainda não propagado, não deploy quebrado. Some em até ~25s num hostname novo. Em worker já existente a atualização é quase imediata — não espere à toa.

## Página dinâmica

O Worker pode ler `request.cf` e injetar dados reais do visitante: `colo` (PoP), `city`, `country`, `asn`, `asOrganization`, `httpProtocol`, `tlsVersion`, `timezone`. Monte o HTML com marcadores tipo `__COLO__` e substitua com `.split(x).join(y)` dentro do `fetch`.

## Gerenciar

```js
// listar
async () => (await cloudflare.request({ method:"GET",
  path:"/accounts/"+accountId+"/workers/scripts" })).result.map(w=>w.id)

// apagar
async () => cloudflare.request({ method:"DELETE",
  path:"/accounts/"+accountId+"/workers/scripts/NOME" })
```

Confirme com o usuário antes de apagar qualquer coisa.

## Limites — diga antes, não depois

**Pages não funciona por aqui.** `POST /pages/projects/{nome}/deployments` aceita o multipart e responde `success: true`, mas serve conteúdo vazio. O Direct Upload real exige autenticar em `/pages/assets/upload` com um JWT próprio do projeto e um manifest mapeando cada caminho para um hash blake3 — e o Code Executor só assina com o token da conta. Não gaste tentativas nisso; use Worker.

**Assets externos.** Esta via serve o que couber inline no bundle: HTML, CSS, JS, SVG, fontes do Google Fonts por CDN. Imagem binária pesada, fonte local ou build de framework precisam do endpoint `assets-upload-session`, que esbarra no mesmo problema de JWT. Para esses casos, o caminho é wrangler local ou Git + Workers Builds.

## Custo de tempo

O `execute` responde em ~2s. O que demora é escrever a página. Republicar algo que já existe é rápido; criar um site do zero leva o tempo de criar o site. Seja honesto sobre isso em vez de prometer deploy instantâneo.

