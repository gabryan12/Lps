---
name: time-de-conteudo
description: Skill orquestradora do time de conteúdo — recebe só o tema e conduz sozinha pesquisa (/tendencias), copy (/carrossel-viral) e design (/carrossel-viral-arte), devolvendo o carrossel pronto para postar e o que cada etapa produziu. Use quando o usuário pedir "/time-de-conteudo", "faz um post completo sobre X", "conteúdo pronto sobre X", "roda o time de conteúdo", "do tema ao carrossel", ou passar só um tema esperando o post pronto.
---

# /time-de-conteudo — orquestradora

Você é o coordenador. Não pesquise, não escreva e não desenhe por conta própria: **use cada
skill na ordem**, seguindo o SKILL.md dela, e passe o arquivo que uma salva para a próxima.

```
tema ─▶ /tendencias ─▶ ~/pesquisas/pesquisa-tendencias-<nicho>-<data>.md
     ─▶ /carrossel-viral ─▶ ~/carrosseis/<perfil>/<data>-<assunto>/carrossel.json
     ─▶ /carrossel-viral-arte ─▶ .../design/slide-01.png …
```

## 0. Entrada — pergunte tudo de uma vez

Precisa do **tema**. Numa única mensagem, pergunte só o que faltar:
- **perfil** que vai postar (@ ou "o meu perfil");
- **onde está o público** (Brasil inteiro, ou estado/cidade se for negócio local);
- **cor da marca** (hex, ou um tema: neutro, quente, verde, rosa, mono);
- **quer foto de IA** em alguns slides? (padrão: não — precisa da chave do Gemini).

Se já existir `~/carrosseis/<perfil>/perfil.md`, leia e não pergunte de novo. Depois desta
mensagem, **não interrompa mais** até a entrega, salvo nos pontos de parada abaixo.

## 1. Pesquisa — skill `tendencias`

- Rode com o tema, o público e a janela padrão (semana). Não refaça as perguntas do Passo 1
  dela que já foram respondidas.
- Escolha você a tendência com **✅ Vai** mais forte (prefira 🥇 Lacuna). Se nenhuma for
  ✅ Vai, **pare** e mostre o radar: a decisão é da pessoa.
- Guarde o caminho do relatório salvo em `~/pesquisas/`.

## 2. Copy — skill `carrossel-viral`

- Entrada: o relatório da etapa 1 + o perfil.
- Use a capa marcada como `recomendada`.
- Só siga quando o `conferir.py` dela der **APROVADO**. Reprovou → corte o texto e confira
  de novo (é trabalho da copy, não do design).

## 3. Design — skill `carrossel-viral-arte`

- Entrada: o `carrossel.json` aprovado + a cor da marca.
- Foto só se a pessoa pediu: a etapa usa a `nanobanana` (precisa de `GEMINI_API_KEY` no
  `.env` e cobrança ativa no Google). Falhou → siga só com texto e diga isso.
- Se o Playwright falhar: instale (`pip install playwright pillow && python3 -m playwright
  install chromium`) e gere de novo. **Nunca refaça o texto por erro de imagem.**
- Só entregue com **APROVADO** e depois de abrir a capa, um slide do meio e o CTA.

## 4. Entrega

1. Envie a capa e 2 slides (SendUserFile) e diga a pasta com todos.
2. Legenda + hashtags prontas para copiar.
3. **O que cada etapa produziu:**
   - Pesquisa: quantos candidatos checou, qual escolheu, diagnóstico e nota (com link do relatório).
   - Copy: os 5 ganchos, qual foi usado, quantos itens checados e o resultado do `conferir.py`.
   - Design: quantos slides, cor/fontes, com ou sem foto, resultado do APROVADO.
4. O que ficou de fora (fonte não medida, foto que falhou, item "confirmar com a pessoa").

Termine com uma pergunta: aprova ou quer trocar capa/cor.

## Modo passo a passo

Se a pessoa pedir para ver cada etapa ("me mostra antes de seguir"), pare depois da pesquisa
e depois da copy, esperando o "pode seguir".
