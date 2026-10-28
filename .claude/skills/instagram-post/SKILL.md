---
name: instagram-post
description: Cria post único de Instagram (imagem de feed 1080x1350 ou story 1080x1920) com legenda, hashtags e calendário de conteúdo. Use quando o usuário pedir "post pro Instagram", "arte pro feed", "post estático", "story", "legenda", "ideias de post", "calendário de conteúdo", "pauta da semana" ou "o que postar". Para posts com vários slides, use a skill instagram-carrossel.
---

# Post de Instagram (feed, story, legenda e pauta)

Cobre quatro pedidos comuns. Identifique qual é e siga só a parte relevante:

| Pedido | Entrega |
|---|---|
| Arte de feed | PNG 1080x1350 + legenda |
| Story | PNG 1080x1920 (1 a 5 telas) |
| Só legenda | Texto pronto para colar |
| Ideias / calendário | Tabela de pautas com formato e gancho |

Se o pedido tem mais de uma ideia em sequência ("5 dicas de…"), é carrossel:
use a skill `instagram-carrossel`.

## Antes de começar

Descubra na conversa ou no repositório: **negócio e público**, **objetivo do post**
(vender, educar, prova social, bastidor, captar lead), **@ do perfil**, **identidade
visual** (cores, fontes, logo — se houver página no repo, leia e herde) e **CTA**.
Se faltar a identidade, escolha uma direção coerente e diga qual foi. Se faltar o
negócio, pergunte.

## Arte de feed (1080x1350)

1. **Uma mensagem só.** Título de até ~10 palavras que se entende em 2 segundos
   rolando o feed. Texto de apoio opcional, máximo 2 linhas.
2. Tipografia grande (título 80–120px), margens de 80px, contraste alto.
3. Tipos que funcionam: frase de impacto, número/resultado, antes e depois,
   depoimento (só real, com permissão — nunca invente), oferta com prazo, pergunta.
4. @ do perfil discreto no rodapé. Sem excesso de emoji ou gradiente genérico;
   use `frontend-design` como referência estética.

## Story (1080x1920)

5. Deixe livres os **250px de cima e 250px de baixo** (barra de progresso, nome do
   perfil, campo de resposta). Conteúdo no centro.
6. Uma ideia por tela, texto ainda maior que no feed. Indique onde entraria a
   figurinha (enquete, caixinha, link) com um espaço reservado e avise o usuário
   — figurinhas são adicionadas no app, não na imagem.

## Renderizar

Salve o HTML em `instagram/<slug>/post.html` com cada arte em um
`<section class="slide">` do tamanho exato e use o script do carrossel:

```bash
node .claude/skills/instagram-carrossel/scripts/render.js instagram/<slug>/post.html instagram/<slug>/png 1080 1350
```

Para story, passe `1080 1920`. Abra o PNG com a ferramenta Read e confira texto
cortado, contraste e fonte antes de entregar.

## Legenda

7. **1ª linha = gancho** (~125 caracteres, aparece antes do "mais").
8. Corpo em parágrafos curtos, tom de conversa, vocabulário do público.
9. **Um CTA** claro no fim (comenta X, salva, link na bio, chama no direct/WhatsApp).
10. 3 a 8 hashtags específicas do nicho e da cidade, se for negócio local
    (ex.: #dentistabh). Nada de #love #instagood.
11. Entregue também 2 variações curtas da 1ª linha para teste e um texto alternativo da imagem.

## Ideias e calendário

12. Tabela com: dia, formato (carrossel / post / reels / story), pilar
    (educar, autoridade, prova social, bastidor, oferta), gancho/título e CTA.
13. Equilibre: no máximo 1 de cada 4 posts é venda direta. Varie formatos.
14. Ganchos específicos do negócio, não genéricos ("Quanto custa um implante em
    BH em 2026" > "Fale sobre implantes").
15. Ofereça produzir na hora qualquer item da pauta (carrossel → `instagram-carrossel`,
    reels → `remotion-best-practices`).

## Entrega

Envie os PNGs (SendUserFile), diga o caminho da pasta e mostre a legenda pronta
para copiar.
