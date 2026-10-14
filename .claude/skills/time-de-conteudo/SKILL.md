---
name: time-de-conteudo
description: Skill orquestradora do time de conteúdo — recebe só o tema e conduz sozinha pesquisa (/tendencias), copy (/carrossel-viral) e design (/carrossel-viral-arte), devolvendo o carrossel pronto para postar e o que cada etapa produziu. Use quando o usuário pedir "/time-de-conteudo", "faz um post completo sobre X", "conteúdo pronto sobre X", "roda o time de conteúdo", "do tema ao carrossel", ou passar só um tema esperando o post pronto.
---

# /time-de-conteudo — orquestradora

Você é o coordenador. Não pesquise, não escreva e não desenhe por conta própria: **chame
cada skill na ordem**, passe o resultado de uma para a outra e só intervenha se uma etapa
falhar.

```
tema → /tendencias → TENDÊNCIA ESCOLHIDA → /carrossel-viral → CARROSSEL PRONTO → /carrossel-viral-arte → PNGs
```

## 0. Entrada

Precisa só do **tema**. Se o usuário já tiver um `marca.md` (cor, fonte, @, tom, público)
na pasta de trabalho, leia e use em todas as etapas. Se não tiver, pergunte **uma vez, no
começo, tudo junto**: público, tom, cor da marca, @ do perfil. Depois não interrompa mais.
Ofereça salvar as respostas em `marca.md` para as próximas rodadas.

## 1. Pesquisa — use a skill `tendencias`

- Passe o tema, o público e a janela (padrão: 7 dias). Não deixe a skill perguntar de novo
  o que você já sabe.
- Escolha você mesmo a tendência mais forte (a "aposta" da skill) e monte o bloco
  `TENDÊNCIA ESCOLHIDA` com fato, data, links e cuidados.
- Se a pesquisa não achar nada com fonte: **pare** e diga isso. Nunca siga com tema
  inventado.

## 2. Copy — use a skill `carrossel-viral`

- Entrada: o bloco `TENDÊNCIA ESCOLHIDA` + tom.
- Use o gancho marcado com ⭐.
- Confira a checagem de fatos: se algum item estiver ❌, ele precisa ter saído do texto.

## 3. Design — use a skill `carrossel-viral-arte`

- Entrada: o bloco `CARROSSEL PRONTO` + marca.
- Só texto, a menos que o usuário tenha pedido foto (aí a `carrossel-viral-arte` chama a
  `nanobanana`).
- Se o Playwright falhar: instale (`pip install playwright && python -m playwright install
  chromium`) e tente de novo. **Nunca refaça o texto por erro de imagem.**

## 4. Entrega

1. Envie as imagens (`carrossel/slide-01.png`…).
2. Legenda + hashtags prontas para copiar.
3. Um resumo **"o que cada etapa produziu"**:
   - Pesquisa: quantas tendências achou, qual escolheu e por quê (com link).
   - Copy: os 5 ganchos, qual foi usado, quantos fatos checados.
   - Design: quantos slides, cor/fonte usadas, com ou sem foto.
4. O que ficou pendente (fonte que não abriu, foto que falhou etc.).

## Modo passo a passo

Se o usuário pedir para ver cada etapa antes de seguir ("me mostra antes"), pause depois
da pesquisa e depois da copy, esperando o "pode seguir".
