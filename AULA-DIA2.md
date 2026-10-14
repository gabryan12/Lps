# Operação Claude Code · Dia 2 — de ferramenta a time

Ontem você usou. Hoje você constrói: suas próprias skills, rotinas que rodam sozinhas e um
time de conteúdo (pesquisa → copy → design) comandado por uma skill orquestradora.

## Skills do Dia 2 neste repositório (`.claude/skills/`)

| Skill | Origem | Para quê |
|---|---|---|
| `skill-creator` | anthropics/skills (oficial) | Diagnostica e cria skills com você: entrevista, escreve e testa |
| `tendencias` | versão própria, feita a partir do prompt da aula | **Pesquisa**: o que está em alta no nicho, cruzando Google, YouTube, Instagram, TikTok, Reddit e imprensa |
| `carrossel-viral` | versão própria, feita a partir do prompt da aula | **Copy**: 5 ganchos de capa, slides que puxam o próximo, legenda e checagem de fatos |
| `carrossel-viral-arte` | versão própria, feita a partir do prompt da aula | **Design**: PNGs 1080×1350 com a cor da marca; texto desenhado em código (`scripts/render.py`) |
| `nanobanana` | versão própria | Fotos com a IA de imagem do Google (opcional, precisa de chave + cobrança) |
| `time-de-conteudo` | versão própria (orquestradora) | Recebe só o tema e roda pesquisa → copy → design sozinha |

> Os links de download dos `.skill` da aula (`tendencias`, `carrossel-viral`,
> `carrossel-viral-arte`, `nanobanana`) não vieram no texto copiado. Por isso essas são
> versões escritas aqui seguindo os prompts e as regras da página. Se quiser as originais,
> envie os arquivos que eu troco.

## Rotinas (o Claude trabalhando sem você)

Prompts prontos em [`rotinas/`](rotinas/). Para usar: **Claude Code › Rotinas › Nova rotina**,
cole o prompt, escolha o horário e clique em **Executar agora** na primeira vez. Condição: o
computador ligado e o app do Claude aberto.

| Rotina | Horário | Precisa de |
|---|---|---|
| [Pauta do dia](rotinas/pauta-do-dia.md) | todo dia, 6h30 | nada (troque negócio/público/tom) |
| [Seu dia em 60 segundos](rotinas/seu-dia-em-60-segundos.md) | dias úteis, 7h | conector Google (Gmail + Agenda) |
| [Caixa de entrada zerada](rotinas/caixa-de-entrada-zerada.md) | todo dia, 8h e 14h | conector Google (Gmail) |

Cada uma publica um painel como artefato com link fixo, que se atualiza por cima todo dia.

## Como acionar uma skill

| Forma | Como funciona |
|---|---|
| `/slash` | Digite `/nome-da-skill`. O mais confiável. |
| Pelo nome | "usa a skill X pra fazer isso". |
| Sozinha | Fale natural e o Claude reconhece. Depende de a descrição da skill estar boa. |

## Prompts da aula

**A sua primeira skill** (na aba Code):
```
Quero criar uma skill minha.

O que eu faço: [SUA PROFISSÃO / NEGÓCIO]

A tarefa que eu repito e me consome tempo: [DESCREVA EM 2 LINHAS]

Como eu faço isso hoje, passo a passo:
1. [PRIMEIRO PASSO]
2. [SEGUNDO PASSO]
3. [TERCEIRO PASSO]

O que eu considero um resultado bom: [O CRITÉRIO — o que faz você aprovar ou refazer]

O que nunca pode acontecer: [O ERRO QUE VOCÊ MAIS TEME]

Me faça as perguntas que faltarem, uma de cada vez. Depois escreva a skill.
```

**Diagnóstico com o skill-creator:**
```
Use o skill-creator pra avaliar a skill [NOME] que eu acabei de criar. Aponte o que está vago, o que está faltando e o que faria ela ser acionada sozinha nas situações certas. Depois reescreva ela corrigida.
```

**Testando pesquisa + copy juntas (combinação de skills):**
```
Pesquise sobre [TEMA] usando a skill de pesquisa e, com o resultado, escreva o conteúdo usando a skill de copy. Me mostre o que saiu de cada etapa antes de seguir pra próxima.
```

**O time inteiro de uma vez:** `/time-de-conteudo [TEMA]`

## Ainda falta (só você consegue fazer)

- [ ] **Conector Google** (para as rotinas de e-mail/agenda): Personalizar › Conectores › Descobrir › Google › **+**
- [ ] **Firecrawl** (recomendado para a `/tendencias`): crie a conta grátis em firecrawl.dev,
      pegue a chave e peça: *"instale e configure o Firecrawl pra mim"*. Sem ele a skill roda com menos fontes.
- [ ] **Playwright** (para a `/carrossel-viral-arte` no seu computador), na primeira vez peça:
      *"instala o Playwright e o Chromium e gera as imagens de novo"*.
- [ ] **Chave do Gemini** (opcional, só para fotos com a `nanobanana`): aistudio.google.com/apikey ›
      Criar chave de API › salve num arquivo `.env` na pasta de trabalho como `GEMINI_API_KEY=...`.
      Gerar imagem exige cobrança ativa (~US$ 0,07 por foto). **Chave é senha:** não cole no chat.
      O `.env` já está no `.gitignore`.
- [ ] **Criar as 3 rotinas** no app (acima).

## A pergunta que fica

Você tem o operário. Quais são os próximos três processos da sua operação que merecem virar skill?
