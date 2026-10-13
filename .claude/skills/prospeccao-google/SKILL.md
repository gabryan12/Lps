---
name: prospeccao-google
description: Use quando o usuário quiser encontrar clientes locais para vender site ou presença digital — "prospectar [nicho] em [cidade]", "buscar clientes", "achar dentistas/clínicas/salões/pizzarias pra vender meu serviço", "quero leads de [nicho] em [cidade]", "preciso de clientes pra minha agência".
---

# Prospecção no Google

Acha negócios locais que **não têm site de verdade** e escreve a primeira mensagem pra cada um.

Uma chamada ao Google Maps. Nenhum site é aberto. **Uns 3 minutos** (quase tudo esperando o Maps).

## Antes de começar

Precisa da Apify conectada. Ela pode aparecer com dois nomes, conforme o jeito que foi ligada — **os dois servem, use o que existir**: `mcp__Apify__call-actor` (extensão do app) ou `mcp__apify__call-actor` (conexão pelo Claude Code). O mesmo vale pro `get-dataset-items` e pro `get-actor-run`.

Se **nenhum dos dois** existir nesta sessão, **pare** e diga ao usuário, em português: *"A Apify não está ligada. No menu da esquerda, abra Personalizar › Conectores › Descobrir, busque apify, instale a Apify e autorize na janela do navegador. Depois abra uma conversa nova e peça de novo."* Não tente conectar por comando: esse caminho cria a conexão com outro nome e o usuário veio pelo `INSTALAR.md`, que promete que ele só conversa em português.

Pergunte **nicho** e **cidade** se o usuário não disse. Nada mais. Avise que vai levar uns minutos antes de começar.

## Passo 1 — Puxar

Existe `bases/{nicho}-{cidade}.json`? Reutilize e avise a data — repetir a busca cobra de novo.

```
actor: compass/crawler-google-places
input: {
  "searchStringsArray": ["{nicho}"],
  "locationQuery": "{cidade}, Brazil",
  "maxCrawledPlacesPerSearch": 60,
  "language": "pt-BR",
  "skipClosedPlaces": true,
  "scrapeContacts": true
}
callOptions: {"maxTotalChargeUsd": 0.6}
```

⛔ **Não mexa neste input.** Não suba `maxCrawledPlacesPerSearch`, não ligue outro parâmetro, não repita a busca "pra ver se vem mais". Cada um desses gasta o crédito do usuário sem avisar. Se ele quiser mais resultados, **pergunte antes** e diga quanto custa.

⏳ **A busca leva uns 3 minutos e a chamada só espera 45 segundos** — ela volta com status `RUNNING` e um `runId`. Isso é normal, **não chame o actor de novo** (cobraria duas vezes). Chame `get-actor-run` com esse `runId` e `waitSecs: 45`, quantas vezes precisar, até vir `SUCCEEDED`. Entre uma e outra, diga ao usuário em uma linha quantos negócios já vieram.

Projete no `get-dataset-items` — **só estes campos**:

```
title, categoryName, website, domain, emails, phone, totalScore, reviewsCount, placeId, url, neighborhood
```

Salve esses mesmos campos em `bases/{nicho}-{cidade}.json` (data no nome dos arquivos sempre `AAAA-MM-DD`).

## Passo 2 — As seis regras

Aplique nesta ordem e **conte quantos caem em cada uma** — o funil é parte da entrega.

**1. É do nicho?** Olhe `categoryName` **e o título juntos**. Descarte só quando os **dois** apontam para outro ramo.
> O Google mistura: numa busca por estética entrou uma *loja de produtos de beleza*; em fisioterapia, uma *clínica veterinária* com 856 avaliações. Mas categoria irmã **fica** — "Delivery de Pizza" e "Restaurante" com pizza no nome são pizzaria.

**2. Tem 20 avaliações?** Menos que isso, o negócio ainda não se provou. Descarte.
> Não filtre por nota: em três nichos ela reprovou **zero**. E se quase ninguém cair nesta regra, seu nicho é de alto volume (alimentação, por exemplo) — narre o zero e siga.

**3. Ele tem site próprio?** Olhe `domain`. **Se `domain` vier vazio mas `website` estiver preenchido, tire o domínio do `website` na mão** — só é "não tem nada" quando os dois estão vazios.

Aí faça **uma** pergunta:

> **O domínio é o nome do negócio, ou é o nome de outra empresa?**

| O que você vê | Situação | Temperatura |
|---|---|---|
| `website` e `domain` vazios | **Não tem nada** | 🔥 mais quente |
| `instagram.com` · `facebook.com` · `wa.me` · `linktr.ee` · `bit.ly` | **Mora na casa dos outros** | 🔥 quente |
| plataforma que ele usa pra operar (`anota.ai` · `cardapioweb` · `saipos` · `booksy` · `trinks` · `doctoralia`) ou construtor pronto (`wixsite.com` · `lovable.app` · `sites.google.com`) | **Página emprestada** | ⚡ morno |
| o nome do negócio (`clinicaarthys.com`) | **Tem site** | fora da lista |

Os exemplos são só exemplos — plataforma nova aparece toda semana. **Se o domínio não é do negócio, use isto pra escolher entre os dois blocos do meio:** rede social ou encurtador de link → *casa dos outros*; sistema que ele usa pra atender, agendar, receber pedido ou montar página → *página emprestada*.

**Não conseguiu decidir? Escreva `NÃO SEI`.** Esse lead vai para uma lista separada de *Conferir na mão*, com o link, e **não recebe mensagem nenhuma**. Chutar aqui faz você afirmar um fato falso pra um estranho — é o pior erro possível.

**4. Junte quem é a mesma pessoa.** Mesmo `placeId` = duplicata, apague. Mesmo `domain` ou mesma marca no título (*"Royal Face Barra"* e *"Royal Face Ilha"*) = **mesmo dono**: mostre junto, conte como **uma** conversa. Se as unidades caírem em blocos diferentes, a conversa vai para o bloco **mais frio** — se uma unidade já tem site, o dono já tem site.

> Daqui pra frente você tem **dois números**: quantos registros vieram e quantas conversas sobraram. Narre os dois no funil e ordene pelas conversas.

**5. Ordene por `reviewsCount`**, do maior pro menor, dentro de cada bloco. Mais avaliação = negócio maior = paga mais.

**6. Escreva mensagem só pros 3 primeiros** de cada bloco. O resto vai na tabela.

## Passo 3 — A mensagem

Leia `~/workspace/perfil/profissional.md`. Se não existir — **ou existir sem um número que prove** — pergunte só o que falta, uma vez (seu nome · o que você faz · um número que prove), e salve. Sem esse número a parte 2 sai como *"trabalho com presença digital"*, que não convence ninguém.

Rode `date "+%H"`: 5-11h "Bom dia" · 12-17h "Boa tarde" · resto "Boa noite".

**Quatro partes:**

1. **Saudação com o nome** — *"Boa tarde, Dra. Andressa, tudo bem?"*
2. **Quem é você** — *"aqui é o Thales, eu faço site pra clínica"*
3. **O que você viu** — o número real, como fato, nunca como elogio
4. **Oferta com prazo e risco seu + o pedido** — *"monto em 7 dias e você só paga se aprovar. Posso te mandar a primeira tela?"*

| ❌ Nunca | ✅ Sempre |
|---|---|
| *"Estava navegando e vi..."* | clichê nº 1 do spam — comece pelo nome |
| *"Que reputação incrível!"* | *"vi que vocês têm 237 avaliações"* |
| *"Nós da nossa equipe..."* | *"eu faço", "posso te mostrar"* — quem manda é uma pessoa |
| *"Faço site"* | *"monto em 7 dias e você só paga se aprovar"* |
| *"Quantos clientes você perde?"* | *"posso te mandar a primeira tela?"* |
| áudio, "SEO", "responsivo", "imperdível" | texto; "aparecer no Google"; "abrir bem no celular" |

**O argumento muda com o bloco:**

- **Não tem nada** → *"quem te indica manda procurar seu nome, e essa pessoa não tem onde cair."*
- **Mora na casa dos outros** → reconheça primeiro (*"o Instagram de vocês é ativo"*) e posicione o site como **complemento**, nunca substituto.
- **Página emprestada** → *"o {plataforma} resolve o pedido, mas o endereço na internet é dele, não seu."* ⚠️ Não diga que a página é feia, lenta ou mal ranqueada — **você não abriu o site**. Fale só do que sabe: o domínio não é dele.

**Tamanho:** até ~380 caracteres. **Tratamento:** copie o que o título do Google usa — se está *"Dra. Elaine"*, trate por *"Dra."*.

**Se for nome de empresa** (não de pessoa), peça o encaminhamento — e **varie a abertura pela posição**, senão saem 9 mensagens idênticas: 1º *"consegue me passar pro responsável?"* · 2º *"quem cuida da parte digital de vocês?"* · 3º *"queria falar com quem decide isso aí no {bairro}"*.

**Varie também o pedido:** 1º *"Posso te mandar a primeira tela?"* · 2º *"Quer ver como ficaria o seu?"* · 3º *"Faz sentido eu te mandar uma prévia?"*

## Passo 4 — Entregar

Salve em `saidas/`: `{nicho}-{cidade}-AAAA-MM-DD.md` e `.html`.

O `.html` preenche `dashboard-template.html` — **não redesenhe, e apague o comentário de instruções do topo** antes de entregar. Todos os leads entram no quadro; só os 3 primeiros de cada bloco têm mensagem escrita no `.md`. O **gancho** de cada linha é uma frase de até 8 palavras dizendo o que aquele lead não tem (*"só Instagram, 162 avaliações"*).

**Narre o funil com número.** Descarte em silêncio parece ferramenta quebrada:

> Puxei 60. Tirei 1 fora do nicho e 13 com menos de 20 avaliações. Sobraram 46:
> **15 não têm nada** · **18 moram na casa dos outros** · **3 em página emprestada** · 10 já têm site · **2 pra conferir na mão**.


## Passo 5 — Rascunho de e-mail (só se tiver e-mail)

Muita rodada volta com **zero** e-mails — é normal, e-mail só aparece pra quem tem site próprio. Se vier zero, **diga isso no `.md` e siga**; não é erro.

⚠️ **Confira de quem é o e-mail antes de usar.** O scraper às vezes devolve o e-mail da *plataforma*, não do negócio (`contato@keepo.bio` num lead cujo link é keepo.bio). Se o domínio do e-mail não é o do negócio, **descarte** — escrever pra plataforma não fala com o dono.

Tendo e-mail: `create_draft`, **sempre rascunho, nunca envio, um por vez**. Antes de criar confira: assunto ≤ 60 caracteres, sem CAIXA ALTA, sem emoji, sem *grátis · promoção · imperdível · desconto · clique aqui · garantido · urgente*; um link só; assinatura com nome e WhatsApp.

Gmail não conectado? **Escreva o e-mail dentro do `.md` e avise** — nunca pule calado.

## Regras invariáveis

- **Nunca invente contato, número, prêmio ou depoimento.** Só o que veio do Google. Na dúvida, `NÃO SEI`.
- **Nunca afirme nada sobre a aparência, a velocidade ou o conteúdo de um site** — esta skill não abre site nenhum.
- **Nunca diga que o site está fora do ar** sem abrir no navegador. Erro de conexão quase sempre é o servidor recusando robô, não site caído — e essa é a pior mensagem pra mandar errado.
- **Sempre rascunho, nunca envio.** Se pedirem disparo em massa, **recuse**: queima o domínio e é o oposto do método.
- Português, sem jargão na mensagem pro cliente.
