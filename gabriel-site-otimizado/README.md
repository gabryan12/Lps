# Site gabrieldiniztrafego.com.br (com blog)

Site estático em Cloudflare Workers. A página inicial é uma página só (rolagem). O **blog** é a única parte com páginas separadas.

- **Como usar, publicar e escrever artigos:** leia o [`PASSO-A-PASSO.md`](PASSO-A-PASSO.md).
- **Origem e licença do globo:** [`FONTE-DO-GLOBO.md`](FONTE-DO-GLOBO.md) (precisa ser preenchido).

## Estrutura

```
conteudo/          o que você edita: site.yml, autor.yml, blog/*.md, imagens/, redirecionamentos.txt
src/build.py       gera o site (dist/ e previa/)
src/pages/         modelos das páginas (início, Sobre, 404, privacidade, termos)
src/partials/      cabeçalho e rodapé
src/css, src/js    estilo e scripts
src/assets/        fontes, globo (computador e celular), imagem de compartilhamento
src/static/        robots.txt e o painel de edição (admin/)
src/tools/         geradores de imagens (globo do celular, imagem de compartilhamento)
dist/              site final (o que a Cloudflare publica)
previa/            cópia privada com rascunhos
wrangler.jsonc     configuração da Cloudflare (Worker "gabriel-site", rotas /* e www/*)
```

O Worker `gabriel-site` responde em todo o domínio; o briefing (`/forms/`) é outro Worker (`gabi-briefing`) e continua com a rota mais específica. **Nada neste projeto altera as rotas do `/forms/`.**

## Decisões desta versão

- **Sem redirecionamento de www**: o endereço oficial é `https://gabrieldiniztrafego.com.br`; o `canonical`, o `og:url`, o schema e o sitemap usam esse endereço.
- **robots.txt**: o arquivo é o mesmo de antes (apenas ASCII, sem comentários com acento), servido como `text/plain; charset=utf-8`. Não foi criado outro `robots.txt`.
- **Fontes**: o site usa **Inter** e **Inter Tight** (variáveis, só o conjunto latino, `font-display: swap`), hospedadas no próprio site. A tipografia Bricolage Grotesque e DM Mono é a do briefing `/forms/`, e não foi aplicada aqui para não mudar a identidade do site.
- **CSS e JavaScript com nome versionado** (hash no nome): cache de 1 ano; o HTML tem cache de 5 minutos.
- **Globo no celular**: imagem parada (poster) na primeira tela e sequência de 19 quadros só depois do carregamento. O computador não mudou.
- **Link do Google Meu Negócio**: `https://share.google/5qsY0mw24iTJKilTg` (o antigo `maps.app.goo.gl/...` foi trocado).

## Google Tag Manager e consentimento (resumo técnico)

Contêiner `GTM-KCSP6484` (campo `gtm_id` em `conteudo/site.yml`). Um script curto no `<head>` (gerado no build) guarda a escolha em `localStorage` (`cookies` = `aceito` ou `recusado`, com try/catch) e só injeta o GTM se for `aceito`. Sem `<noscript>` do GTM, sem ID `G-` no código, sem Meta Pixel. Os cliques em "Agendar conversa" vão ao `dataLayer` como `cta_agendar_conversa` (`cta_location`, `page_path`, `article_title`), só com consentimento. O `/forms/` não tem GTM.

## Globo no celular (resumo técnico)

Imagem parada de 15 KB (`width`/`height` definidos, `fetchpriority="high"`, pré-carregada no `<head>`); a sequência (19 quadros, 600 px, nomes com hash, 296 KB) só começa a baixar depois da página carregada, com o navegador ocioso e o globo visível. Com "reduzir movimento", Save-Data ou conexão 2G, fica só a imagem parada. O giro pausa quando o globo sai da tela. Para regerar: `python3 src/tools/gerar-globo-mobile.py 2`.

## Pendências suas

- Razão social (opcional, `conteudo/site.yml`, campo `empresa.razao`). O CNPJ já está no rodapé.
- No Google Tag Manager: criar o gatilho do evento `cta_agendar_conversa` e as variáveis `cta_location`, `page_path` e `article_title`.
- Provas reais (depoimentos, números, casos) em `conteudo/site.yml`, campo `provas`; a seção fica escondida enquanto estiver vazia.
- Revisão das páginas de Privacidade e Termos por um advogado antes de divulgar o site em anúncios.
- Preencher o `FONTE-DO-GLOBO.md` (origem e licença do vídeo do globo).
- Apagar o artigo de exemplo (`conteudo/blog/o-que-preparar-antes-de-anunciar.md`) ou transformá-lo em artigo real.
