# Regras do projeto

## Vídeo

Sempre que o usuário mencionar "vídeo" (criar, gerar, editar, cortar, legendar, anúncio, reels, criativo), invoque a skill `ads-machine` via Skill antes de qualquer outra coisa e siga o pipeline dela. Ela é a orquestradora e chama, em ordem, os agentes de `.claude/agents/`:

1. `ads-gerador-video`: base do vídeo (gravação, avatar ou fundo animado).
2. `ads-corte`: transcrição palavra por palavra, remove silêncios, hesitações e tomadas erradas.
3. `ads-insert`: gancho, zoom, b-roll, emoji, números animados e CTA, sincronizados com a fala (Remotion).
4. `ads-legenda`: legenda estilo TikTok com `@remotion/captions`, corrigindo marca e preço.
5. `ads-revisor`: confere contra `PADRAO-ANUNCIO.md` e aponta qual agente refaz o quê (máximo 3 rodadas).

Também carregue `remotion-best-practices` (estágios 3 e 4) e entregue `videos/<nome>/final.mp4`. Antes de executar, apresente o plano e espere o "ok" do usuário.

As skills `video-use` (exige chave paga da ElevenLabs) e o fluxo antigo "só Remotion" só entram se o usuário pedir explicitamente.
