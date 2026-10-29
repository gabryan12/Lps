# Padrão de anúncio em vídeo

Critérios que o `ads-revisor` usa para aprovar ou reprovar o `final.mp4`.
Edite este arquivo para ajustar o padrão. Os valores abaixo são um ponto de partida.

## Formato
- Vertical 1080x1920 (9:16), 30 fps, H.264 + AAC, `yuv420p`.
- Duração entre 15 e 45 s, salvo se o pedido disser outra.

## Estrutura
- Gancho nos primeiros 3 s: texto na tela e fala já começam no frame 0.
- Um único CTA claro nos últimos 3 s, dito e escrito.
- Mudança visual (corte, zoom, b-roll ou texto) a cada 2 a 4 s; nenhum plano parado por mais de 4 s.

## Áudio
- Sem silêncio maior que 0,3 s, sem "hum", sem repetições nem tomadas erradas.
- Nenhum corte no meio de palavra.
- Volume em torno de -14 LUFS, sem estourar (pico máximo -1 dBTP).

## Legenda
- Estilo TikTok: 2 a 4 palavras por vez, palavra falada em destaque.
- Dentro da área segura: sem tocar as bordas, longe dos ~250 px inferiores e dos ~150 px superiores.
- Texto correto: nomes de marca, preços e números conferidos com o script.

## Inserts
- Cada insert (gancho, zoom, b-roll, emoji, número animado, CTA) entra sincronizado com a fala que ele ilustra.
- Nada cobre o rosto nem a legenda.

## Entrega
- Arquivo `final.mp4` na pasta do vídeo, abrindo e tocando até o fim.
