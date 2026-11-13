# Briefing do projeto — Gabriel Diniz Tráfego

Página em **gabrieldiniztrafego.com.br/forms** (e também `www`). O cliente chega por um link que você manda, responde 8 etapas e você recebe tudo por e-mail em `sagatrafego@gmail.com`. Cada briefing também fica guardado num banco da Cloudflare (KV), caso o e-mail falhe.

```
public/forms/index.html   a página inteira (HTML, CSS e JS)
public/_headers           pede ao Google para não indexar /forms
src/worker.js             recebe o briefing, guarda no KV e envia o e-mail
wrangler.jsonc            configuração do Cloudflare
```

A raiz do domínio **não é afetada**: o Worker só responde em `/forms` e `/forms/*`.

## Link personalizado

Mande o link assim para o cliente não precisar digitar o nome:

```
https://gabrieldiniztrafego.com.br/forms?n=Maria%20Souza&ref=indicacao-ana
```

- `n` (ou `nome`): nome da pessoa. A pergunta do nome some e a saudação usa o primeiro nome.
- `ref`: de onde veio o cliente. Aparece nos e-mails.

## O que você precisa antes

- Conta na Cloudflare com o domínio **gabrieldiniztrafego.com.br** adicionado (nameservers apontando para a Cloudflare).
- Node.js instalado (https://nodejs.org, versão LTS).

## Passo a passo

1. **Abra o terminal** na pasta `gabi-briefing`.
2. **Entre na Cloudflare:** `npx wrangler login` (abre o navegador; autorize).
3. **Ative o Email Routing** no domínio: painel da Cloudflare → o domínio → *E-mail* → *Email Routing* → *Enable*. Aceite os registros DNS que ele sugerir.
4. **Verifique o e-mail de destino:** em *Email Routing* → *Destination addresses*, adicione `sagatrafego@gmail.com` e clique no link de confirmação que chegar. Sem isso o envio falha.
5. **Crie o KV (backup dos briefings).** Duas opções:
   - *Automático:* não faça nada. No primeiro `npx wrangler deploy`, o Wrangler cria o KV sozinho.
   - *Manual:* rode `npx wrangler kv namespace create BRIEFINGS`, copie o `id` que ele mostrar e cole em `wrangler.jsonc`: `"kv_namespaces": [{ "binding": "BRIEFINGS", "id": "COLE_O_ID_AQUI" }]`.
6. **DNS (nuvem laranja).** O domínio precisa estar com o proxy da Cloudflare ligado, senão o Worker não recebe o tráfego. Em *DNS* → *Records*:
   - se já existe um registro para `gabrieldiniztrafego.com.br` e para `www`, confira que a nuvem está **laranja** (Proxied);
   - se **não** existe registro para a raiz, crie um registro **A** de fachada: nome `@`, IPv4 `192.0.2.1`, **Proxied** ligado. Faça o mesmo para `www` (tipo A, `192.0.2.1`, Proxied). Esse endereço é só um ponto de apoio: a Cloudflare responde antes de chegar nele. É o jeito padrão e é grátis.
   - A raiz continua livre para o site da agência: quando você tiver o site, aponte o registro para ele. Só `/forms` fica com este Worker.
7. **Publique:** `npx wrangler deploy`
8. **Teste:** abra https://gabrieldiniztrafego.com.br/forms (sem a barra final ele redireciona para `/forms/`), preencha com dados de teste e envie. Você deve receber dois e-mails: "Briefing iniciado — …" (ao concluir nome, WhatsApp e e-mail) e "Novo briefing — …" (no envio final). Confira o spam na primeira vez.
9. **Ver erros:** `npx wrangler tail` mostra o que acontece em tempo real.

> O envio só é aceito 30 segundos depois do início do briefing (antispam). Num teste muito rápido, a página mostra sucesso mas o briefing é descartado de propósito.

## Ler os briefings guardados (KV)

```
npx wrangler kv key list --binding BRIEFINGS --remote
npx wrangler kv key get "briefing:ID_AQUI" --binding BRIEFINGS --remote
```

- `briefing:{id}`: o briefing completo (todas as respostas).
- `rascunho:{id}`: quem começou, última etapa alcançada e se já enviou (expira em 60 dias).

Sem `--remote`, os comandos leem o banco de teste do seu computador.

## Testar no computador (opcional)

`npx wrangler dev` abre em http://localhost:8787/forms/. O e-mail é simulado: o arquivo `.eml` fica em `.wrangler/tmp/email/` e o caminho aparece no terminal. O KV também é local.

## Custos e limites

O plano gratuito do Workers (cerca de 100 mil requisições por dia), o KV e o Email Routing atendem esse uso. Limites e preços mudam: confira os valores atuais na documentação da Cloudflare.

## Observações

- A página tem `noindex, nofollow` no HTML e no cabeçalho (`_headers`).
- Sem Turnstile e sem analytics. O antispam é um campo oculto e o tempo mínimo.
- O destino e o remetente ficam no topo de `src/worker.js` (`TO` e `FROM`). Se mudar o destino, altere também `destination_address` no `wrangler.jsonc` e verifique o novo e-mail no Email Routing.
- O envio recusa mais de ~60 mil caracteres de respostas.
