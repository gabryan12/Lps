# Operação Claude Code · Dia 1 — configuração

## Skills já instaladas neste repositório (`.claude/skills/`)

Carregam automaticamente em qualquer sessão do Claude Code aberta neste repositório.

| Skill | Origem | Para quê |
|---|---|---|
| `find-skills` | vercel-labs/skills | Buscar e instalar outras skills do skills.sh |
| `remotion-best-practices` | remotion-dev/skills | Vídeo a partir de texto (Reels, manchete, gerador "saas") |
| `video-use` | browser-use/video-use | Editar vídeo gravado (precisa de chave da ElevenLabs, paga) |
| `frontend-design` | anthropics/skills | Páginas sem "cara de IA" |
| `prospeccao-google` | skill-prospeccao.zip (aula) | `prospectar [nicho] em [cidade]`: precisa do conector Apify |
| `deploy-cloudflare` | deploy-cloudflare.skill (aula) | `publica essa página no ar`: precisa do conector Cloudflare |
| `quizz-qualificacao` | quizz-qualificacao.skill (aula) | Quizz de 4 perguntas que abre o WhatsApp com as respostas |
| `skill-creator` | anthropics/claude-plugins-official (Dia 2) | Criar e diagnosticar suas próprias skills (P21, P22) |

Versões registradas em `skills-lock.json`. Para atualizar: `npx skills update -p`.

## Ainda falta (só você consegue fazer)

### Skills em arquivo (.zip / .skill) da página da aula
Os links de download não vieram no texto copiado e o site da aula não abre daqui.
Baixe e suba em **Personalizar › Habilidades › Adicionar › Fazer upload de habilidade**,
ou envie os arquivos aqui que eu coloco em `.claude/skills/`:

- [x] `skill-prospeccao.zip`: instalada como `prospeccao-google`
- [x] `deploy-cloudflare.skill`: instalada
- [x] `quizz-qualificacao.skill`: instalada

### Conectores
Ficam na sua conta, em **Personalizar › Conectores**:

- [ ] **Apify**: crie a conta em apify.com e depois vá em Descobrir › "apify" (Apify Technologies, Extensão para desktop). Ligue por aqui, não pedindo ao Claude.
- [ ] **Meta Ads**: vá em Descobrir › Meta, ou adicione o conector personalizado `https://mcp.facebook.com/ads`
- [ ] **Google Workspace**: vá em Descobrir › Google (Gmail, Drive, Agenda)
- [ ] **Cloudflare**: crie a conta em dash.cloudflare.com/sign-up e adicione o conector personalizado `https://mcp.cloudflare.com/mcp`
- [ ] **Higgsfield** (bônus): adicione o conector personalizado `https://mcp.higgsfield.ai/mcp`

### Plugins (opcional, depois da aula)
- [ ] Vá em **Personalizar › Plugins › Adicionar › Adicionar marketplace** e informe `github.com/anthropics/claude-code`

## Comandos rápidos da aula

- Vídeo: `Use a skill remotion-best-practices. Crie um vídeo vertical 1080x1920...`
- Prospecção: `prospectar [dentistas] em [Belo Horizonte]` (precisa da skill-prospeccao + Apify)
- Página: `Use a skill frontend-design. Crie um site de uma página para [NEGÓCIO]...`
- Publicar: `publica essa página no ar` (precisa de deploy-cloudflare + conector Cloudflare)
- Quizz: `Cria um quizz de diagnóstico de 4 perguntas nesta página para [NEGÓCIO]...`
- CRM: cole o prompt do CRM usando o modo **Planejar**.

---

# Dia 2: situação nesta sessão na nuvem

## Instalado
- [x] `skill-creator`: baixada do GitHub oficial da Anthropic e colocada em `.claude/skills/`
- [x] Dependências Python das skills do Dia 2 (só nesta sessão; o container é descartado depois):
  `pip install "playwright==1.56.0" pillow yt-dlp google-genai`. A versão 1.56.0 casa com o Chromium
  pré-instalado em `/opt/pw-browsers`. `ffmpeg` e `jq` já vêm no container.
  Em sessão nova, peça "instala as dependências Python do AULA-DIA1.md".

## Bloqueado: arquivos .skill do site da aula
A política de rede do ambiente nega `skills.escoladeautomacao.com.br` (erro 403). Faltam:
- [ ] `tendencias.skill`
- [ ] `carrossel-viral.skill`
- [ ] `carrossel-viral-arte.skill`
- [ ] `nanobanana.skill` (opcional; precisa da `GEMINI_API_KEY`)

Duas saídas: liberar o domínio em **Network access › Allowed domains** do ambiente
(https://code.claude.com/docs/en/cloud-environments#network-access) e pedir de novo,
ou enviar os arquivos .skill nesta conversa.

## Conectores (estado verificado nesta sessão)
- [x] Cloudflare (Developer Platform e cloudflare-api): conectado
- [ ] Google Drive: instalado, mas **não autenticado**
- [ ] Gmail, Google Agenda, Firecrawl: não instalados (estão no catálogo)
- [ ] Meta Ads, Apify, Higgsfield: não aparecem no catálogo daqui; adicione como conector personalizado
  (`https://mcp.facebook.com/ads`, `https://mcp.higgsfield.ai/mcp`; Apify pela conta em apify.com)

Ligue em https://claude.ai/customize/connectors e **abra uma sessão nova**: os conectores são lidos quando a sessão começa.
