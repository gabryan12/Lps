---
name: carrossel-viral-arte
description: Transforma o texto de um carrossel em imagens prontas para postar no Instagram (1080×1350, PNG) com a cor da marca, desenhando o texto em código — nunca pela IA — para não sair letra errada. Use quando o usuário pedir "/carrossel-viral-arte", "faz a arte do carrossel", "gera as imagens do carrossel", "design do post", "transforma esse texto em carrossel", ou quando for a terceira etapa do time de conteúdo (depois de /carrossel-viral).
---

# /carrossel-viral-arte — design do carrossel

Terceira peça do time de conteúdo. Recebe o texto pronto (bloco `CARROSSEL PRONTO` da
`/carrossel-viral`) e entrega os PNGs. **Não reescreva o texto** — se algo estiver errado,
volte para a copy.

## 1. Entrada

- Texto: bloco `CARROSSEL PRONTO` na conversa, ou texto colado pelo usuário.
- Marca (pergunte só o que faltar; se houver `marca.md` na pasta, leia):
  - **cor principal** (hex — se o usuário der um nome, converta: "azul marinho" → `#1f3a5f`)
  - **fundo** dos slides internos (padrão `#f6f3ee`) e **cor do texto** (padrão `#161616`)
  - **fonte** do Google Fonts (padrão `Inter`)
  - **@ do perfil**
- **Fotos?** Pergunte só se o usuário não disse. Padrão: carrossel só com texto.

## 2. Monte o JSON

Crie `carrossel/carrossel.json` na pasta de trabalho:

```json
{
  "marca": { "cor": "#1f3a5f", "fundo": "#f6f3ee", "texto": "#161616",
             "fonte": "Inter", "handle": "@seuperfil" },
  "slides": [
    { "tipo": "capa",   "tag": "alerta", "titulo": "Gancho escolhido aqui" },
    { "tipo": "texto",  "titulo": "Título curto", "texto": "Uma ideia por slide." },
    { "tipo": "numero", "numero": "73%", "texto": "frase que explica o número" },
    { "tipo": "cta",    "titulo": "Salva esse post", "texto": "e manda pra quem precisa ver." }
  ]
}
```

Tipos: `capa` (fundo na cor da marca), `texto`, `numero`, `cta` (fundo na cor da marca).
Qualquer slide aceita `"imagem": "img/foto1.jpg"` (caminho relativo ao JSON) — vira foto de
fundo com degradê escuro e o texto continua desenhado por cima, em código.

**Regra de números:** no máximo **um** slide `numero` (o `NÚMERO EM DESTAQUE` da copy). Os
outros números ficam dentro da frase. O script recusa o JSON se houver mais de um.

## 3. Gere as imagens

```bash
python .claude/skills/carrossel-viral-arte/scripts/render.py carrossel/carrossel.json carrossel/
```

Saída: `carrossel/slide-01.png`, `slide-02.png`… Mostre as imagens ao usuário (envie os
arquivos) e liste o que cada slide contém.

### Deu erro ao gerar?
O script usa o **Playwright** para "fotografar" cada slide. Se faltar:

```bash
pip install playwright && python -m playwright install chromium
```

Se o Chromium já estiver instalado em outro lugar, rode com
`CHROMIUM_PATH=/caminho/do/chromium`. Travou de novo? Repita ou abra uma conversa nova — é
o computador, não o carrossel: **nunca refaça o texto por causa disso**.

## 4. Fotos com IA (opcional)

Só se o usuário pedir foto em algum slide:
1. Use a skill **nanobanana** para gerar a foto (sem texto dentro da imagem) e salve em
   `carrossel/img/`.
2. Coloque `"imagem"` nesses slides e rode o render de novo.

Se a nanobanana falhar (sem chave, sem cobrança ativa no Google), entregue o carrossel só
com texto e diga isso — nada quebra.

## Regras

- Texto sempre desenhado pelo HTML/CSS do script — nunca peça para a IA de imagem escrever.
- Máximo ~30 palavras por slide; se não couber, avise e devolva para a copy.
- Verifique o contraste: texto claro sobre cor escura e vice-versa (o script já escolhe).
