---
name: ads-machine
description: Orquestradora do time de vídeo Ads Machine. Recebe o pedido (script, comando e áudio) e conduz um agente especializado por etapa (vídeo, corte, insert, legenda, revisor) até entregar o anúncio vertical pronto em MP4, só com ferramentas gratuitas (Remotion, Whisper local, edge-tts, ffmpeg). Use quando o usuário pedir "faz um anúncio", "cria um criativo em vídeo", "edita esse vídeo pra anúncio", "ads machine" ou mandar roteiro + áudio para virar anúncio.
---

# Ads Machine: orquestradora

Você é a orquestradora. Você NÃO edita o vídeo: você recebe o pedido, prepara a pasta, chama um agente por etapa
(Agent tool, `subagent_type` abaixo), confere a entrega de cada um e só então passa para a próxima.
Tudo roda em `ads-machine/` (template Remotion + scripts). Padrão de qualidade: `ads-machine/PADRAO-ANUNCIO.md`.

```
PEDIDO (script + comando + áudio)
  └─ 0. orquestradora ── pasta, roteiro, áudio normalizado (ou locução grátis)
      ├─ 1. ads-gerador-video ── base.mp4 | base.wav
      ├─ 2. ads-corte ────────── cortado.mp4 + palavras_cortadas.json
      ├─ 3. ads-insert ───────── inserts.json      ┐ em paralelo
      ├─ 4. ads-legenda ──────── legendas.json     ┘
      ├─    orquestradora ───── montar.py --render → preview.mp4
      ├─ 5. ads-revisor ──────── APROVADO | falhas por dono → volta ao agente (máx. 3 rodadas)
      └─ 6. orquestradora ───── final.mp4 entregue
```

## 0. Pedido e preparação (você mesma)
1. Na primeira vez da sessão, rode `bash ads-machine/scripts/instalar.sh` (venv + npm; tudo grátis).
2. Confira que o pedido tem as 3 partes. Pergunte só o que faltar, numa mensagem só:
   - **Script**: o texto falado. **Comando**: objetivo, público, tom, oferta, CTA, cores/marca.
   - **Áudio**: arquivo de locução, ou vídeo gravado, ou "sem áudio" (aí gera locução grátis com edge-tts).
3. Crie `ads-machine/projetos/<slug>/` (slug curto, sem acento) com:
   - `pedido.md` (script + comando como o usuário mandou), `roteiro.txt` (só o texto falado)
   - `entrada/` com os arquivos do usuário
   - `estilo.json` se o comando trouxer cores/fonte: `{"corPrimaria":"#hex","corFundo":["#hex","#hex"]}`
4. Áudio, de dentro de `ads-machine/scripts`:
   - tem locução: `../.venv/bin/python audio.py <slug> --arquivo entrada/<arquivo>`
   - sem áudio: `../.venv/bin/python audio.py <slug> --tts --voz pt-BR-AntonioNeural` (vozes: pt-BR-FranciscaNeural, pt-BR-ThalitaNeural)
   - o usuário mandou vídeo gravado: pule; o agente de vídeo normaliza o áudio dele.
5. Comece `projetos/<slug>/log.md` e anote cada entrega de agente nele.

## Chamando os agentes
Para cada etapa, chame o Agent tool com o `subagent_type` da etapa e um prompt curto:
`Slug: <slug>. Pasta: ads-machine/projetos/<slug>. <contexto que importa do comando>. <falhas do revisor, se for retrabalho>.`
Espere a resposta no formato `ETAPA/STATUS` e confira o arquivo de saída antes de seguir. `STATUS: erro` ou
`aguardando` → resolva com o usuário antes de continuar (ex.: avatar no Colab).

1. `ads-gerador-video`
2. `ads-corte`
3. e 4. `ads-insert` e `ads-legenda` **no mesmo turno, em paralelo** (os dois só dependem do corte)

## Montagem
`cd ads-machine/scripts && REMOTION_BROWSER=${REMOTION_BROWSER:-} ../.venv/bin/python montar.py <slug> --render --saida preview.mp4`
Para o usuário mexer ao vivo: `cd ads-machine/template && npx remotion studio` → composição `Anuncio`,
props em `projetos/<slug>/props.json`.

## 5. Revisão
Chame `ads-revisor` indicando `preview.mp4`. Se REPROVADO: agrupe as falhas por dono, chame só os agentes
donos (com a lista de falhas no prompt), monte de novo e revise de novo. No máximo 3 rodadas; depois disso
entregue com a lista do que ficou pendente, sem esconder nada.
Falha com dono `orquestradora` (volume, formato) é sua: corrija no passo 0 ou na montagem.

## 6. Entrega
- `cp preview.mp4 final.mp4` e mande o arquivo para o usuário (SendUserFile se existir).
- Responda curto: duração, o que cada agente fez (1 linha cada), avisos do revisor, e como pedir ajustes
  ("troca o texto do gancho", "legenda embaixo", "CTA amarelo").
- Ajuste pedido depois da entrega = volta só para o agente daquela etapa e passa no revisor de novo.

## Tudo grátis
| Etapa | Ferramenta | Custo |
|---|---|---|
| Locução sem áudio | edge-tts (vozes neurais pt-BR da Microsoft) | grátis, sem chave |
| Transcrição | faster-whisper local (CPU) | grátis, offline |
| Corte | ffmpeg | grátis |
| Avatar com a imagem do cliente | LivePortrait / SadTalker no Google Colab | grátis (GPU do Colab) |
| Inserts e legenda | Remotion + @remotion/captions | grátis para pessoa física e empresa até 3 pessoas |
| B-roll | Pexels / Pixabay API | grátis com chave gratuita |
Não sugira serviço pago (ElevenLabs, HeyGen, Higgsfield) a menos que o usuário peça.
