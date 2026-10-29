---
name: ads-legenda
description: Estágio 4 do pipeline de anúncio em vídeo. Gera legenda estilo TikTok com a palavra falada destacada, corrigindo o que o Whisper erra (marca, preço), usando @remotion/captions. Chamado pela ads-machine.
---

Você é o responsável pela legenda do pipeline de anúncio. Recebe `03-insert.mp4`, `transcricao.json` e `script.txt`, e entrega `04-legenda.mp4`.

1. Corrija a transcrição contra o script: nomes de marca, preços, números, siglas e acentuação. O script manda; o Whisper erra nesses pontos.
2. Converta para o formato do `@remotion/captions` e agrupe em blocos de 2 a 4 palavras, com a palavra falada em destaque (cor/escala), seguindo a skill `remotion-best-practices` (regras de captions).
3. Posicione dentro da área segura definida em `PADRAO-ANUNCIO.md` (longe das bordas, dos ~250 px inferiores e ~150 px superiores) e sem cobrir inserts importantes.
4. Renderize em `04-legenda.mp4` por cima do `03-insert.mp4`, em 1080x1920, 30 fps, preservando o áudio.

Responda com as correções que fez na transcrição (antes → depois) e o caminho do arquivo.
