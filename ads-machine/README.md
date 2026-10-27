# Ads Machine (versão grátis)

Time de agentes que transforma **script + comando + áudio** em anúncio vertical pronto (1080x1920, MP4).
Uma orquestradora e um agente especializado por etapa, todos no Claude Code, só com ferramentas gratuitas.

Como usar: abra o Claude Code neste repositório e peça
> Faz um anúncio. Script: "…". Comando: anúncio de 30s para clínica de estética, tom direto, cor #E91E63, CTA "Agende pelo WhatsApp". Áudio: segue anexo (ou: sem áudio).

| Etapa | Quem | Arquivo do agente | Entrega |
|---|---|---|---|
| 0. Pedido, roteiro, áudio | Orquestradora | `.claude/skills/ads-machine/SKILL.md` | `audio.wav` |
| 1. Vídeo | `ads-gerador-video` | `.claude/agents/ads-gerador-video.md` | `base.mp4` / `base.wav` |
| 2. Corte | `ads-corte` | `.claude/agents/ads-corte.md` | `cortado.mp4`, `palavras_cortadas.json` |
| 3. Insert | `ads-insert` | `.claude/agents/ads-insert.md` | `inserts.json` |
| 4. Legenda | `ads-legenda` | `.claude/agents/ads-legenda.md` | `legendas.json` |
| 5. Revisão | `ads-revisor` | `.claude/agents/ads-revisor.md` | APROVADO ou falhas por dono |
| 6. Final | Orquestradora | — | `final.mp4` |

- `template/`: projeto Remotion único (composição `Anuncio`). Os agentes só escrevem JSON; o template não muda por anúncio.
- `scripts/`: uma ferramenta por etapa (`audio.py`, `base.py`, `transcrever.py`, `cortar.py`, `legendas.py`, `montar.py`, `revisar.py`).
- `PADRAO-ANUNCIO.md`: o padrão que o revisor cobra. Edite para a sua marca.
- `projetos/<slug>/`: tudo de cada anúncio (fora do git).

Instalação (uma vez): `bash ads-machine/scripts/instalar.sh` (precisa de Python 3, Node 20+ e ffmpeg).
Opcional: `PEXELS_API_KEY` / `PIXABAY_API_KEY` (grátis) para b-roll de banco.

Custos: edge-tts, faster-whisper, ffmpeg, Pexels/Pixabay e Colab são grátis. O Remotion é grátis para pessoa
física e empresas de até 3 pessoas; acima disso exige licença da empresa.
