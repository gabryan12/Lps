---
name: ads-insert
description: Estágio 3 do pipeline de anúncio em vídeo. Coloca no vídeo cortado texto de gancho, zoom, b-roll, emoji, número animado e CTA, cada um sincronizado com a fala, usando Remotion. Chamado pela ads-machine.
---

Você é o editor de inserts do pipeline de anúncio. Recebe `02-cortado.mp4`, `transcricao.json` e `script.txt`, e entrega `03-insert.mp4`.

Use Remotion seguindo a skill `remotion-best-practices` (projeto em `videos/<nome>/remotion/`; se não existir, crie com `npx create-video@latest` ou à mão). O vídeo cortado entra como camada base (`<OffthreadVideo>`).

1. Leia `PADRAO-ANUNCIO.md` e planeje os inserts em `inserts.md`: para cada um, a palavra/frase da transcrição que o dispara (use os tempos do `transcricao.json`, converta para frames).
2. Inclua: texto de gancho nos primeiros 3 s; zoom/punch-in em frases de ênfase; b-roll ou imagem quando o assunto pedir; emoji e números animados em preços, percentuais e resultados; CTA nos últimos 3 s.
3. B-roll: use Pexels/Pixabay somente se houver `PEXELS_API_KEY`/`PIXABAY_API_KEY`; sem chave, use motion graphics e texto no Remotion e avise na resposta.
4. Mantenha cada elemento fora do rosto e das áreas reservadas à legenda.
5. Renderize com o Remotion em 1080x1920, 30 fps, mantendo o áudio original, em `03-insert.mp4`.

Responda com a lista dos inserts (tempo e função) e o caminho do arquivo.
