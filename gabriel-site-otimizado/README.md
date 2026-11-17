# Site gabrieldiniztrafego.com.br: versão otimizada

## O que mudou nesta versão (velocidade)

- **Fontes dentro do site.** O Inter e o Inter Tight agora vêm de `dist/assets/fonts/` (arquivos `.woff2`, só o conjunto latino) e são pré-carregados. O site não pede mais nada ao Google Fonts, o que tirava cerca de meio segundo do primeiro carregamento.
- **Globo mais leve.** No computador, de 75 para 38 quadros (de 2,7 MB para 1,4 MB). O giro continua na mesma velocidade, e a mistura entre quadros mantém o visual (diferença média de 1,2 em 255 por pixel). No celular já eram 38. A pasta do computador mudou de `assets/globo` para `assets/globo-d` de propósito: os arquivos de `assets/` ficam 1 ano no cache do navegador, e o nome novo evita misturar quadros antigos com novos para quem já visitou o site.
- **Abertura mais rápida.** A tela de abertura é liberada quando os primeiros quadros chegam (12 no computador, 10 no celular). O resto carrega em segundo plano.
- **CSS e JavaScript menores.** O `build.py` agora minifica os dois com o esbuild (precisa do Node.js). CSS de 43,8 para 37,6 KB e JavaScript de 24,7 para 15,5 KB. Sem Node, ele copia os arquivos como estão.
- **Acessibilidade.** Os três painéis de serviços usavam `<article role="tabpanel">`, combinação que o padrão ARIA não permite. Viraram `<div role="tabpanel">`, sem mudar o visual.

Como publicar esta versão: dentro da pasta `gabriel-site-otimizado`, rode `npx wrangler deploy` (mesmo Worker `gabriel-site`, ele só atualiza os arquivos).

Atenção: se um dia trocar uma imagem do globo mantendo o mesmo nome, quem já visitou continua vendo a antiga por até 1 ano. Mude o nome do arquivo ou da pasta.

---


Este pacote tem o site institucional pronto. A pasta `dist/` é o que vai ao ar. Não é preciso programar: o Claude Code faz os comandos e você só autoriza o acesso à sua conta Cloudflare no navegador.

## O que tem aqui

- `dist/`: o site pronto (página inicial, blog, privacidade, termos, imagens do globo, robots.txt e sitemap.xml).
- `wrangler.jsonc`: configuração da Cloudflare (publica a pasta `dist/` e liga o domínio).
- `src/`: o código-fonte, só para quando você quiser mudar textos ou o visual e gerar a `dist/` de novo.

## Antes de começar

1. Ter o Node.js instalado (versão LTS, em nodejs.org). Se o Claude Code já roda no seu computador, o Node já está lá.
2. Ter o domínio `gabrieldiniztrafego.com.br` ativo na sua conta Cloudflare, com a nuvem laranja (proxy) ligada nos registros de DNS. Se o domínio já serve a página `/forms`, isso já está pronto.
3. Nunca envie senhas a ninguém, nem ao Claude. O acesso é feito pelo navegador, no passo 3.

## Publicar (o jeito mais fácil: pelo Claude Code)

1. Descompacte o zip e abra a pasta `gabriel-site` no Claude Code.
2. Cole este pedido:

   > Leia o README.md desta pasta e publique o site na Cloudflare com o wrangler, seguindo o passo a passo. Antes de publicar, confira na documentação atual da Cloudflare se a sintaxe do wrangler.jsonc (assets e routes) está correta. Não mexa na rota /forms: ela já pertence a outro Worker e precisa continuar funcionando.

3. Quando o Claude Code rodar `npx wrangler login`, o navegador abre uma página da Cloudflare. Clique em "Allow" (Permitir) para autorizar.
4. O Claude Code roda `npx wrangler deploy`. Ele vai mostrar um endereço de teste terminado em `.workers.dev`. Abra e confira o site.

## Publicar (sem o Claude Code)

No terminal, dentro da pasta `gabriel-site`:

    npx wrangler login
    npx wrangler deploy

## IMPORTANTE: a página /forms continua intacta

O briefing (`gabrieldiniztrafego.com.br/forms`) é outro Worker, que já responde em `/forms` e `/forms/*`. Este site responde no resto do domínio. Como a Cloudflare usa a rota mais específica, `/forms` continua sendo atendido pelo Worker do briefing.

Depois de publicar, teste os dois endereços:

- `https://gabrieldiniztrafego.com.br/` deve abrir o site novo.
- `https://gabrieldiniztrafego.com.br/forms/` deve abrir o briefing, como antes.

Se `/forms` parar de funcionar, no painel da Cloudflare vá em Workers & Pages, Settings, Domains & Routes do Worker do briefing e confira se as rotas `gabrieldiniztrafego.com.br/forms` e `gabrieldiniztrafego.com.br/forms/*` ainda estão lá. Se o problema continuar, apague a rota `/*` deste site e fale com o Claude Code antes de seguir.

## Conferir depois de publicar

1. Abra o site no celular e no computador. A abertura mostra o globo girando e o contador, depois o texto.
2. Clique nos botões de WhatsApp: devem abrir a conversa com o número (21) 98922-7990.
3. Abra `/privacidade/`, `/termos/` e `/blog/`.
4. Abra `/robots.txt` e `/sitemap.xml`.
5. No Google Search Console, adicione o domínio e envie o sitemap (`https://gabrieldiniztrafego.com.br/sitemap.xml`).

## Como mudar textos e dados (sem refazer o visual)

O arquivo `src/js/content.js` guarda os dados que mudam com frequência:

- `empresa.razao` e `empresa.cnpj`: aparecem no rodapé quando preenchidos.
- `gtmId`: o ID do Google Tag Manager (por exemplo `GTM-XXXXXXX`). Só carrega depois que a pessoa clica em "Aceitar" no aviso de cookies. Configure o GA4 e o Pixel da Meta dentro do GTM.
- `provas`: números, depoimentos e casos. A seção "Resultados de quem já trabalhou comigo" fica escondida até você preencher. Só use dados reais, com autorização do cliente e com período e origem do número.
- `posts`: artigos do blog. A seção do blog também só aparece quando houver artigo.

Depois de editar qualquer arquivo em `src/`, gere a `dist/` de novo e publique:

    python3 src/build.py prod
    npx wrangler deploy

(O comando só atualiza as páginas, o CSS, o JS e as imagens. Os arquivos `robots.txt`, `sitemap.xml`, `_headers` e `404.html` dentro de `dist/` não são apagados.)

## O que ainda precisa de você

- Razão social e CNPJ (rodapé e páginas legais).
- ID do Google Tag Manager.
- Provas reais (depoimentos, números e casos) para a seção de resultados.
- Revisão das páginas de Privacidade e Termos por um advogado antes de divulgar o site em anúncios.
- Primeiro artigo do blog. Enquanto não houver artigo, a página do blog fica com `noindex` (não aparece no Google). Quando tiver conteúdo, peça para remover esse `noindex` e incluir o blog no sitemap.

## Se algo der errado

- `npx wrangler tail` mostra os erros do Worker em tempo real.
- Erro de login: rode `npx wrangler logout` e depois `npx wrangler login`.
- O site novo não aparece no domínio: no painel da Cloudflare, confira se o registro de DNS do domínio está com a nuvem laranja (proxied) e se as rotas deste Worker estão listadas em Domains & Routes.
- As fontes (Inter e Inter Tight) vêm do Google Fonts. Se não carregarem, o site usa uma fonte do sistema.
