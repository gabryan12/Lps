# Operação Claude Code · Dia 2 — de ferramenta a time

Ontem você usou. Hoje você constrói: suas próprias skills, rotinas que rodam sozinhas e um
time de conteúdo (pesquisa → copy → design) comandado por uma skill orquestradora.

## Skills do Dia 2 neste repositório (`.claude/skills/`)

| Skill | Origem | Para quê |
|---|---|---|
| `skill-creator` | anthropics/skills (oficial, igual ao `skill-creator.skill` da aula) | Diagnostica e cria skills com você: entrevista, escreve e testa |
| `tendencias` | `tendencias.skill` da aula (original) | **Pesquisa**: Google Trends, YouTube, TikTok/Instagram, Reddit, imprensa e Amazon, com mapa de cruzamento, diagnóstico e nota. Salva em `~/pesquisas/` |
| `carrossel-viral` | `carrossel-viral.skill` da aula (original) | **Copy**: 5 ganchos, slides com cliffhanger, legenda e checagem. Salva `carrossel.json` em `~/carrosseis/` e confere com `conferir.py` |
| `carrossel-viral-arte` | `carrossel-viral-arte.skill` da aula (original) | **Design**: PNGs 1080×1350 com a cor da marca, texto em código, checagem de estouro/letra/contraste |
| `nanobanana` | `nanobanana.skill` da aula (original) | Fotos com a IA de imagem do Google (opcional, precisa de chave + cobrança) |
| `time-de-conteudo` | orquestradora escrita aqui, a partir do prompt da aula | Recebe só o tema e roda pesquisa → copy → design sozinha |

Única alteração nas originais: os comandos que apontavam para `~/.claude/skills/...` agora
apontam para `.claude/skills/...`, porque aqui elas moram dentro do projeto. Rode o Claude
Code a partir da pasta do projeto.

**Testado aqui:** o `conferir.py` da copy e o `render.py` do design rodaram e geraram os
slides (APROVADO). A pesquisa e a nanobanana dependem do Firecrawl e da chave do Gemini, que
só existem no seu computador.

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
- [ ] **Firecrawl** (a `/tendencias` usa em quase toda busca): crie a conta grátis em firecrawl.dev,
      pegue a chave e peça: *"instale e configure o Firecrawl pra mim"*. Sem ele a skill roda com menos fontes.
- [ ] **Playwright** (para a `/carrossel-viral-arte` no seu computador), na primeira vez peça:
      *"instala o Playwright e o Chromium e gera as imagens de novo"*.
- [ ] **Chave do Gemini** (opcional, só para fotos com a `nanobanana`): aistudio.google.com/apikey ›
      Criar chave de API › salve num arquivo `.env` na pasta de trabalho como `GEMINI_API_KEY=...`.
      Gerar imagem exige cobrança ativa (~US$ 0,07 por foto). **Chave é senha:** não cole no chat.
      O `.env` já está no `.gitignore`. (A nanobanana original diz "cole aqui" — não cole: use o `.env`.)
- [ ] **yt-dlp** (opcional, para a `/tendencias` ler comentários do YouTube): peça *"instala o yt-dlp"*.
- [ ] **Apify** (opcional, para a `/carrossel-viral` ler a voz de um @ do Instagram): conector do Dia 1.
- [ ] **Criar as 3 rotinas** no app (acima).

## A pergunta que fica

Você tem o operário. Quais são os próximos três processos da sua operação que merecem virar skill?
