# Briefing do site — Gabriel Diniz Tráfego

Página de briefing para clientes de qualquer segmento (gabrieldiniztrafego.com.br). O cliente digita o nome logo na abertura, e ele é repetido nas orientações para o projeto parecer exclusivo. O formulário tem 9 etapas e as respostas chegam por e-mail em `sagatrafego@gmail.com`.

```
public/index.html   a página inteira (HTML, CSS e JS)
src/worker.js       recebe o formulário e envia o e-mail
wrangler.jsonc      configuração do Cloudflare
```

## O que você precisa antes

- Conta na Cloudflare com o domínio **gabrieldiniztrafego.com.br** já adicionado (nameservers apontando para a Cloudflare).
- Node.js instalado (https://nodejs.org, versão LTS).

## Passo a passo

1. **Abra o terminal** dentro da pasta `gabi-briefing`.
2. **Entre na Cloudflare:** `npx wrangler login` (abre o navegador; autorize).
3. **Ative o Email Routing** no domínio: painel da Cloudflare → o domínio → *E-mail* → *Email Routing* → *Enable*. Aceite a criação dos registros DNS que ele sugerir.
4. **Verifique o e-mail de destino:** em *Email Routing* → *Destination addresses*, adicione `sagatrafego@gmail.com`, abra o e-mail que a Cloudflare enviar e clique no link de confirmação. Sem isso, o envio falha.
5. **Publique:** `npx wrangler deploy`
6. **Ligue o domínio:** o `wrangler.jsonc` já declara `gabrieldiniztrafego.com.br` e `www` como domínios personalizados, então o deploy tenta criar essa ligação. Se reclamar de registro DNS existente, apague no painel (*DNS*) o registro A/AAAA/CNAME antigo do mesmo nome e rode o deploy de novo. Confira em *Workers & Pages* → `gabi-briefing` → *Settings* → *Domains & Routes*.
7. **Teste:** abra https://gabrieldiniztrafego.com.br, preencha o formulário com dados de teste e envie. O e-mail “Novo briefing — …” deve chegar em alguns segundos (veja também o spam na primeira vez).
8. **Ver erros:** `npx wrangler tail` mostra os registros em tempo real enquanto você testa.

## Testar no computador (opcional)

`npx wrangler dev` abre em http://localhost:8787. O e-mail é simulado: o arquivo `.eml` é salvo em `.wrangler/tmp/email/` e o caminho aparece no terminal.

## Custos e limites

O plano gratuito do Workers e o Email Routing atendem esse uso (o gratuito permite cerca de 100 mil requisições por dia). Limites e preços mudam: confira os valores atuais na documentação da Cloudflare.

## Observações

- A página tem `noindex`: não aparece no Google.
- Respostas ficam salvas no navegador do cliente até o envio; depois do envio são apagadas.
- O destino e o remetente estão no topo de `src/worker.js` (`TO` e `FROM`). Se mudar o destino, altere também `destination_address` no `wrangler.jsonc` e verifique o novo e-mail no Email Routing.
- O envio recusa mais de ~60 mil caracteres e ignora preenchimentos do campo oculto anti-spam.
