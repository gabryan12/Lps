---
name: tendencias
description: Pesquisa o que está em alta num nicho ou assunto e prova cruzando Google, YouTube, Instagram, TikTok, Reddit e imprensa, entregando uma lista de pautas com fonte. Use quando o usuário pedir "/tendencias", "o que está em alta sobre X", "sobre o que eu posto", "pauta de conteúdo", "tendências do meu nicho", "pesquisa de conteúdo", "assunto do momento", ou quando for a primeira etapa do time de conteúdo (antes da copy e do design).
---

# /tendencias — pesquisa de conteúdo

Primeira peça do time de conteúdo (pesquisa → copy → design). O trabalho aqui é um só:
descobrir **sobre o que vale falar agora** e provar com fonte. Não escreva post, não
faça arte — isso é das próximas etapas (`carrossel-viral` e `carrossel-viral-arte`).

## 1. Pergunte o assunto da vez

A skill é genérica: toda vez que rodar, pergunte (uma pergunta de cada vez, só o que
faltar na conversa):

1. **Assunto/nicho** desta rodada (ex.: "harmonização facial", "tráfego pago para clínicas").
2. **Público** (quem vai ler) e **região** (Brasil inteiro? uma cidade?).
3. **Janela de tempo**: padrão = últimos 7 dias; aceite "hoje", "30 dias".

Se o usuário já disse tudo no pedido, não pergunte de novo — siga.

## 2. Escolha a ferramenta de pesquisa

Use o que já existe na sessão, nesta ordem:

1. **Firecrawl** (MCP ou CLI, se estiver configurado): é o que lê as páginas de verdade —
   use para buscar e raspar as fontes abaixo.
2. **WebSearch / WebFetch** do próprio Claude.
3. Se nada funcionar, diga isso e pare. Nunca invente tendência.

Se o Firecrawl não estiver disponível, avise uma vez no fim: "rodei sem o Firecrawl, com
menos fontes — crie a conta grátis em firecrawl.dev e peça: *instale e configure o
Firecrawl pra mim*".

## 3. Cruze as fontes

Para o assunto, procure sinais em cada canal (pule o que não abrir e diga qual pulou):

| Canal | O que procurar |
|---|---|
| Google / Google Trends | buscas em alta, "pessoas também perguntam" |
| Imprensa (g1, O Globo, Folha, UOL, Estadão, veículos do nicho) | notícias da janela de tempo |
| YouTube | vídeos recentes com muita visualização para o tamanho do canal |
| Instagram / TikTok | hashtags, áudios e formatos repetindo no nicho |
| Reddit / fóruns | dúvidas e reclamações reais do público |

Uma tendência só entra na lista se aparecer em **pelo menos 2 canais diferentes**, ou em 1
grande portal com data dentro da janela. Descarte press release, publieditorial e conteúdo
sem data.

## 4. Entregue

Até **7 tendências**, a mais forte primeiro. Para cada uma:

- **Tendência** — em 1 frase.
- **Por que agora** — o que aconteceu (fato + data).
- **Provas** — 2 a 4 links clicáveis com veículo/canal e data.
- **Força** — 🔥🔥🔥 / 🔥🔥 / 🔥, e em quantos canais apareceu.
- **Ângulo para o público** — como o especialista explicaria isso (1 frase).
- **Cuidado** — o que não dizer (nome de investigado não indiciado, promessa de resultado,
  diagnóstico, opinião sobre o corpo/rosto de alguém).

Feche com: **"Minha aposta: #N"** e o porquê em 1 frase, e a pergunta
*"Quer que eu passe essa para a copy (/carrossel-viral)?"*

## Regras

- Nada inventado: todo fato, número e nome precisa estar no link citado.
- Nunca use notícia que envolva morte.
- Se achar menos de 3 tendências boas, entregue menos e diga isso.
- Guarde o resultado na conversa num bloco `TENDÊNCIA ESCOLHIDA` quando o usuário escolher
  uma — é o que a próxima etapa (`carrossel-viral`) lê.
