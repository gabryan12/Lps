---
name: nanobanana
description: Gera fotos com a IA de imagem do Google (Gemini "nano banana") a partir de uma descrição, salvando em PNG na proporção pedida. Use quando o usuário pedir "/nanobanana", "gera uma foto", "cria uma imagem com IA", "foto pro carrossel", "imagem de fundo", ou quando a /carrossel-viral-arte precisar de foto em algum slide. Nunca use para desenhar texto — texto é sempre feito em código.
---

# /nanobanana — fotos com a IA do Google

Gera **foto sem texto** (fundo de slide, ilustração, cena). Letras e números são sempre
desenhados em código pela `/carrossel-viral-arte`, nunca pela IA de imagem.

## Antes de usar: a chave

Precisa de `GEMINI_API_KEY` num arquivo `.env` na pasta de trabalho (ou como variável de
ambiente):

```
GEMINI_API_KEY=cole_sua_chave_aqui
```

Se não existir, explique ao usuário (sem pedir para colar a chave no chat):
1. Abrir **aistudio.google.com/apikey** e entrar com a conta Google.
2. **Criar chave de API** — é grátis e não precisa de cartão para criar.
3. Colar a chave no arquivo `.env` ele mesmo. **Chave é senha:** não colar no chat, não
   mandar por WhatsApp, não deixar em print. Se vazar, apagar no AI Studio e criar outra.
4. Gerar imagem **tem custo**: precisa ativar cobrança no Google (~US$ 0,07 por foto). Sem
   cobrança ativa a geração falha — e o carrossel sai só com texto, nada quebra.

Confira se o `.env` está no `.gitignore` antes de qualquer commit.

## Como gerar

1. Escreva a descrição em português, concreta: assunto, enquadramento, luz, clima, cores
   da marca. Ex.: *"Close de mãos de profissional de estética segurando seringa, luz suave
   de janela, fundo desfocado em tons de azul-marinho, fotografia realista."*
2. Rode:

```bash
python .claude/skills/nanobanana/scripts/gerar.py "<descrição>" carrossel/img/foto1.png 4:5
```

Proporções: `4:5` (carrossel, padrão), `1:1`, `9:16` (stories/reels), `16:9`, `3:4`.

3. Mostre a imagem ao usuário. Se ele pedir ajuste, gere de novo com a descrição revisada
   (avise que cada foto tem custo).

## Regras

- Nunca gerar rosto de pessoa real/famosa, nem "antes e depois" de procedimento.
- Nunca pedir texto, logo ou marca dentro da imagem (o script já reforça isso).
- Se der erro de cobrança/cota, pare e diga — não fique tentando de novo.
