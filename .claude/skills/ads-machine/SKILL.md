---
name: ads-machine
description: Orquestradora de vídeos de anúncio. Use SEMPRE que o usuário mencionar "vídeo" (criar, gerar, editar, cortar, legendar, anúncio, reels, criativo). Monta a pasta, normaliza o áudio e chama em ordem os agentes ads-gerador-video, ads-corte, ads-insert, ads-legenda e ads-revisor, até entregar o final.mp4.
---

# ads-machine (orquestradora)

Você coordena o pipeline. Não edita vídeo você mesma: delega cada estágio ao agente certo (ferramenta Agent, `subagent_type` com o nome do agente) e verifica o arquivo que cada um entrega antes de passar adiante.

Ao começar, carregue também a skill `remotion-best-practices` (os estágios 3 e 4 dependem dela). Se o usuário quiser só um estágio (ex.: "só legenda neste vídeo"), rode apenas o estágio pedido, mais a revisão.

## Entrada esperada
Pedido do usuário, com: script (texto falado), comando/objetivo do anúncio e, opcionalmente, áudio, gravação, foto para avatar, marca/preço/CTA. Se faltar o script ou o objetivo, pergunte antes de começar.

## Passo 0: pasta e áudio
1. Crie `videos/<nome-curto>/` com `script.txt` (script e briefing), e copie ali os arquivos do usuário.
2. Resumo do plano para o usuário (formato, estágios, de onde vem a base do vídeo, inserts previstos) e espere o "ok".
3. Se não veio áudio e o usuário não vai gravar: gere a locução com `edge-tts` a partir do `script.txt` (`pip install edge-tts`; voz `pt-BR-AntonioNeural` ou `pt-BR-FranciscaNeural`) em `audio.mp3`.
4. Normalize o áudio para -14 LUFS: `ffmpeg -i audio.mp3 -af loudnorm=I=-14:TP=-1:LRA=11 audio-norm.wav`.

## Estágios (nesta ordem)
Cada agente recebe o caminho da pasta e o arquivo de entrada, e devolve o arquivo de saída. Confira com `ffprobe` que o arquivo existe e abre.

| # | Agente | Entrada | Saída |
|---|---|---|---|
| 1 | `ads-gerador-video` | script, áudio, gravação/foto | `01-base.mp4` |
| 2 | `ads-corte` | `01-base.mp4` | `02-cortado.mp4` + `transcricao.json` |
| 3 | `ads-insert` | `02-cortado.mp4`, `transcricao.json`, script | `03-insert.mp4` |
| 4 | `ads-legenda` | `03-insert.mp4`, `transcricao.json`, script | `04-legenda.mp4` |
| 5 | `ads-revisor` | `04-legenda.mp4`, `PADRAO-ANUNCIO.md` | `revisao.md` (aprovado ou lista de ajustes por agente) |

## Revisão em loop
- Se o revisor aprovar: copie `04-legenda.mp4` para `final.mp4` e vá ao passo final.
- Se reprovar: chame de novo só os agentes que ele apontou, na ordem do pipeline, e passe adiante a partir do primeiro estágio refeito (os seguintes também rodam de novo).
- No máximo 3 rodadas de revisão. Na terceira reprovação, entregue o melhor `final.mp4` e liste com clareza o que ficou pendente.

## Passo final: entrega
Entregue `videos/<nome>/final.mp4` (envie o arquivo ao usuário) e um resumo curto: o que foi feito em cada estágio, quantas rodadas de revisão, e o que não pôde ser verificado ou ficou pendente.

## Regras
- Padrão de qualidade: `PADRAO-ANUNCIO.md` na raiz do repositório.
- Ferramentas gratuitas primeiro (ffmpeg, faster-whisper, edge-tts, Remotion). B-roll do Pexels/Pixabay só se houver chave de API (`PEXELS_API_KEY` / `PIXABAY_API_KEY`); sem chave, use fundo animado, texto ou imagem gerada no Remotion e avise.
- Se um estágio depender de algo que o ambiente não tem (Chrome, GPU, Colab, chave), diga qual é o bloqueio em vez de fingir que fez.
