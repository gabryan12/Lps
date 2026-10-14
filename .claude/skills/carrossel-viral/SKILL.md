---
name: carrossel-viral
description: Transforma uma tendência ou pesquisa em texto de carrossel para Instagram no tom do usuário — 5 opções de gancho de capa, slides que puxam o próximo, legenda e checagem de cada fato. Use quando o usuário pedir "/carrossel-viral", "escreve o carrossel", "copy do carrossel", "texto do post", "transforma essa pesquisa em conteúdo", ou quando for a segunda etapa do time de conteúdo (depois de /tendencias e antes de /carrossel-viral-arte).
---

# /carrossel-viral — copy do carrossel

Segunda peça do time de conteúdo. Recebe o que a pesquisa (`/tendencias`) encontrou e
escreve o carrossel. Só texto: a arte é da próxima etapa (`/carrossel-viral-arte`).

Esta skill junta o melhor de várias práticas de copy para conteúdo (gancho com tensão,
um slide = uma ideia, curiosidade aberta até o fim, CTA único, prova antes de opinião).

## 1. Entrada

Procure na conversa, nesta ordem:
1. Um bloco `TENDÊNCIA ESCOLHIDA` (vindo de `/tendencias`).
2. Uma pesquisa, notícia ou link que o usuário colou.
3. Se não houver nada, pergunte: "Sobre o quê? Cole a pesquisa ou rode /tendencias antes."

Descubra também (pergunte só o que faltar, uma de cada vez):
- **Tom** do perfil (ex.: próxima, segura, sem promessa milagrosa). Se houver um arquivo
  `tom.md` ou `marca.md` na pasta de trabalho, leia e use.
- **@ do perfil** e **objetivo** do post (salvar, comentar, chamar no direct).

## 2. Escreva

### Capa — 5 opções de gancho
Cada uma com no máximo **12 palavras**, usando um mecanismo diferente:
1. Contradição ("Não é o botox que envelhece seu rosto")
2. Número específico ("3 sinais de que o produto é falsificado")
3. Notícia + consequência ("A Anvisa proibiu X. O que muda pra você")
4. Pergunta que dói ("Você sabe o que estão aplicando em você?")
5. Erro comum ("O erro que 8 em cada 10 pessoas cometem antes de…")

Marque a recomendada com ⭐ e diga o porquê em 1 frase.

### Slides (6 a 9 no total, contando capa e CTA)
- **Uma ideia por slide**, no máximo ~30 palavras.
- Cada slide termina puxando o próximo (pergunta, "mas…", lista incompleta).
- Ordem: capa → contexto (o fato, com fonte) → por que importa → o que fazer (passos) →
  virada/insight de especialista → CTA.
- **Números**: no máximo **um** número em destaque gigante no carrossel inteiro; marque-o
  como `NÚMERO EM DESTAQUE`. Os outros números ficam dentro da frase.
- CTA único e concreto (salvar, comentar uma palavra, mandar direct).

### Legenda
- Primeira linha = gancho (diferente da capa).
- 3 a 6 linhas curtas, termina com **pergunta** para comentário.
- Até 5 hashtags do nicho.

### Checagem de fatos
Tabela: **afirmação → fonte (link) → ✅ confirmado / ⚠️ ajustei / ❌ removi**. Todo fato,
número e nome precisa estar no link. O que não tiver fonte sai do texto.

## 3. Formato de saída

Entregue num bloco que a próxima etapa consegue ler:

```
CARROSSEL PRONTO
Gancho escolhido: ...
Slide 1 (capa): ...
Slide 2: ...
...
Slide N (CTA): ...
NÚMERO EM DESTAQUE: <número> — slide <n> (ou "nenhum")
Legenda: ...
Hashtags: ...
```

Depois a checagem de fatos e a pergunta: *"Quer que eu passe para o design
(/carrossel-viral-arte)?"*

## Regras

- Nada de promessa de resultado, diagnóstico ou "antes e depois".
- Nunca comente o rosto/corpo de alguém nem cite investigado não indiciado.
- Português do Brasil, frases curtas, sem jargão de marketing.
