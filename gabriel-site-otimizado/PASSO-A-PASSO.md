# Passo a passo: site e blog de gabrieldiniztrafego.com.br

Este guia é para quem não programa. Nada daqui foi publicado: você aprova primeiro.

## O que tem nesta pasta

| Item | Para que serve |
|---|---|
| `previa/` | Cópia **privada** do site, com o artigo de exemplo (rascunho) visível. É a que você aprova. |
| `dist/` | O site **como vai ao ar** (sem rascunhos). É a pasta que a Cloudflare publica. |
| `conteudo/` | Tudo que você edita: `site.yml` (telefone, links), `autor.yml` (caixa do autor) e `blog/` (os artigos). |
| `src/` | O "motor" do site (modelos, estilo, scripts). Só mexa se souber o que está fazendo. |
| `ABRIR-PREVIA.bat` | Dois cliques: abre a prévia no navegador. |
| `ABRIR-SITE-COMO-VAI-AO-AR.bat` | Dois cliques: abre o site final (`dist`) no navegador. |
| `.github/workflows/publicar.yml` | Faz a publicação automática quando você salva um artigo no painel. |

## 1. Ver a prévia (privada, só no seu computador)

1. Tenha o Node.js instalado (você já tem).
2. Dê dois cliques em `ABRIR-PREVIA.bat`. O navegador abre em `http://localhost:5000`.
3. Confira, no computador e no celular (tecla `F12` e o ícone de celular):
   - o **globo** na abertura;
   - a seção **Sobre** (menu → Sobre);
   - o **Blog** e o artigo de exemplo (marcado como rascunho);
   - o botão **Agendar conversa** e o botão lateral no artigo.
4. A faixa amarela embaixo ("PRÉVIA PRIVADA") só existe na prévia.

## 2. Publicar do jeito que você já faz (manual)

Só depois de aprovar a prévia. No terminal, dentro da pasta `gabriel-site` (a que tem o `wrangler.jsonc`):

```
npx wrangler deploy
```

O terminal deve mostrar `Uploaded gabriel-site` e as duas rotas. Depois confira, numa aba anônima:
`https://gabrieldiniztrafego.com.br/`, `/blog/` e **`/forms/`** (o briefing deve continuar abrindo).

> Enquanto não houver **nenhum artigo publicado**, o blog fica com `noindex` (o Google não indexa a página vazia). O `noindex` sai sozinho quando você publicar o primeiro artigo.

## 3. Publicar artigos sem código (painel + GitHub)

Isto deixa você escrever num formulário. Você faz a configuração **uma vez**.

### 3.1 Colocar o projeto no GitHub (uma vez)

1. Entre no GitHub com a conta **gabryan12**.
2. Crie um repositório **privado** chamado `gabriel-site` (vazio).
3. Envie esta pasta inteira para ele (o jeito mais fácil é o **GitHub Desktop**: *File → Add local repository*, escolher a pasta `gabriel-site`, *Publish repository*). Não envie a pasta `node_modules`, se existir.
4. Se o repositório tiver outro nome, abra `src/static/admin/config.yml` e troque `gabryan12/gabriel-site` pelo nome certo.

### 3.2 Liberar a publicação automática (uma vez)

No repositório: **Settings → Secrets and variables → Actions → New repository secret**. Crie dois:

- `CLOUDFLARE_API_TOKEN`: um token da Cloudflare (Account API tokens → Create token → personalizado) com **Workers Scripts: Edit**, **Workers Routes: Edit** (no domínio `gabrieldiniztrafego.com.br`) e **Account Settings: Read**. Dê validade (por exemplo 1 ano).
- `CLOUDFLARE_ACCOUNT_ID`: o ID da sua conta (aparece no painel da Cloudflare, na página inicial da conta).

Nunca cole esses valores em conversas. Eles ficam só no GitHub.

### 3.3 Entrar no painel (uma vez por computador)

1. Crie um **token do GitHub** só para o painel: GitHub → seu perfil → **Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token**. Escolha **apenas o repositório `gabriel-site`** e a permissão **Contents: Read and write**. Copie o token.
2. Abra `https://gabrieldiniztrafego.com.br/admin/` (depois de publicado).
3. Escolha entrar com **token de acesso pessoal** (Personal Access Token) e cole o token.

> O painel (Sveltia CMS 0.269.0) foi incluído e a configuração foi validada, mas **eu não consegui testar o login real com a sua conta do GitHub**. Se o painel não abrir como descrito, me mande uma captura.

### 3.4 Escrever e publicar um artigo

1. No painel: **Artigos do blog → Novo artigo**.
2. Preencha os campos (todos têm uma dica embaixo):
   - **Rascunho**: deixe marcado enquanto escreve. **Desmarque para publicar.**
   - **Título (H1)**: ideal até 60 caracteres.
   - **Endereço (slug)**: só letras minúsculas, números e hífen. Vira `/blog/<slug>/`.
   - **Resumo**: uma frase, até 160 caracteres.
   - **Categoria**: Tráfego, IA, Sites e SEO ou Google Meu Negócio.
   - **Data de publicação** e **Data de atualização**. A de atualização é **sua**: só mude quando revisar o artigo de verdade. O site nunca muda essa data sozinho.
   - **Imagem de capa** + **texto alternativo** (obrigatório se houver capa).
   - **Resposta direta**: 40 a 60 palavras, respondendo logo a pergunta do título.
   - **Perguntas frequentes**: 3 a 5.
   - **Fontes**: título e endereço (`https://...`).
   - **Artigos relacionados**: 2 a 4.
   - **Texto do artigo**: use `##` para títulos e `###` para subtítulos. **Não use `#`** (o título já é o H1). Tabelas e listas funcionam.
3. Clique em **Salvar** (ou **Publicar**). Em cerca de 2 a 3 minutos o GitHub gera o site e publica na Cloudflare. Acompanhe na aba **Actions** do repositório.
4. **Se faltar algo obrigatório** (resumo, resposta direta, data de atualização, texto alternativo da capa, ou slug repetido), a publicação **falha** e o site no ar **não muda**. A mensagem aparece em português na aba Actions.

### 3.5 Mudar o endereço (slug) de um artigo

Se precisar mudar, anote o endereço antigo no campo **Endereços antigos**. O site cria um redirecionamento 301 do antigo para o novo.

### 3.6 Texto da caixa do autor

Painel → **Configurações → Caixa do autor**. O texto é um só: muda em todos os artigos e no Google (schema).

## 4. O que o site faz sozinho (SEO, AEO e GEO)

- Endereço oficial **sem www**: canonical, `og:url` e schema usam `https://gabrieldiniztrafego.com.br`. Não há redirecionamento de www na Cloudflare, como combinado.
- **Blog em HTML estático**: lista, categorias e artigos funcionam sem JavaScript. Paginação real (`/blog/pagina/2/`), 12 artigos por página. "Carregar mais" e busca são só reforço.
- **Schema**: `ProfessionalService` em todas as páginas; `Person` (Gabriel) só na página inicial; `BlogPosting`, `BreadcrumbList` e `FAQPage` nos artigos.
- **Sitemap** gerado a cada publicação: início, privacidade, termos, blog, categorias e artigos (com a data de atualização real). Não inclui `/forms/`, rascunhos nem páginas com `noindex`.
- **Cabeçalhos** (`_headers`): `robots.txt` em UTF-8, cache longo para arquivos versionados e curto para HTML, `noindex` no painel.

## 4b. Google Tag Manager e cookies

- O contêiner **GTM-KCSP6484** (com a tag do GA4 dentro) só carrega **depois** que a pessoa clica em **Aceitar**. Antes disso, e se ela clicar em **Recusar** ou ignorar o aviso, o site não pede nada ao Google.
- A escolha fica gravada no navegador da pessoa. Quem aceitou tem o GTM carregado logo no início das próximas visitas; quem recusou não vê o aviso de novo.
- Rodapé: o link **Preferências de cookies** deixa a pessoa mudar de ideia (apaga a escolha e mostra o aviso de novo).
- Cada clique em **Agendar conversa** (e nos botões de WhatsApp) manda ao `dataLayer`, só com consentimento: `cta_agendar_conversa` com `cta_location`, `page_path` e `article_title`. Nenhum dado pessoal.
- Para trocar o contêiner, mude `gtm_id` em `conteudo/site.yml`.
- No GTM você precisa de um **gatilho de evento personalizado** com o nome `cta_agendar_conversa` e variáveis do dataLayer para os 3 campos, ligados a uma tag de evento do GA4.

## 5. Depois de publicar: conferir

1. **Search Console**: adicione `https://gabrieldiniztrafego.com.br` e envie `https://gabrieldiniztrafego.com.br/sitemap.xml`.
2. **Rich Results Test** (https://search.google.com/test/rich-results): cole o endereço de um artigo e confira *Artigo de blog*, *Perguntas frequentes* e *Trilha de navegação*.
3. **Validador de schema** (https://validator.schema.org): cole o endereço da página inicial e de um artigo.
4. **PageSpeed** (https://pagespeed.web.dev): celular e computador.
5. Abra `https://gabrieldiniztrafego.com.br/robots.txt` (os acentos devem aparecer certos) e `.../forms/` (o briefing deve abrir).

## 6. Fazer o build no seu computador (opcional)

Só se quiser gerar o site sem o GitHub. Precisa de Python 3.10+:

```
pip install -r requirements.txt
python src/build.py            (gera a pasta dist)
python src/build.py --previa   (gera a pasta previa, com rascunhos)
```
