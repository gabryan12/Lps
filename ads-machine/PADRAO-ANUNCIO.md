# Padrão do anúncio (o que o Revisor confere)

Toda etapa trabalha para passar neste checklist. `scripts/revisar.py` confere automaticamente
os itens marcados com ⚙️; o agente revisor confere o resto olhando os frames.
Para mudar o padrão da sua marca, edite este arquivo **e** os limites `P` em `scripts/revisar.py`.

## Formato
- ⚙️ 1080x1920 (9:16), H.264, 30 fps, áudio AAC
- ⚙️ Duração entre 10 e 60 s (ideal: 20 a 40 s)
- Área segura: nada importante a menos de 180 px do topo ou 380 px da base (botões do Reels/TikTok)

## Áudio
- ⚙️ Loudness integrado entre -16 e -12 LUFS (alvo -14), pico ≤ -1 dBFS
- ⚙️ Nenhum silêncio > 0,6 s fora do CTA final
- Sem estalos nos cortes (fade de 30 ms em toda emenda)
- Trilha (se houver) pelo menos 15 dB abaixo da voz

## Corte
- Nunca cortar no meio de palavra; padding de 50 ms antes / 80 ms depois
- Sem vícios ("hum", "ééé"), sem repetição de frase, sem tomada errada
- Ritmo: pausas acima de 0,3 s viram corte

## Inserts
- ⚙️ Gancho visual nos 2 primeiros segundos (texto destacado, zoom ou b-roll)
- ⚙️ Mudança visual (corte, zoom ou insert) no máximo a cada 4 s
- ⚙️ CTA (insert `cta`) terminando no último frame, começando nos últimos 8 s
- ⚙️ Inserts do mesmo tipo não se sobrepõem
- Texto na tela com no máximo 6 palavras; o insert reforça o que está sendo falado naquele momento
- B-roll só de fonte gratuita com licença comercial (Pexels, Pixabay, Remotion, material do cliente)

## Legenda
- ⚙️ Presente do início ao fim, dentro da duração, nenhuma palavra presa > 1,5 s
- ⚙️ Palavras de baixa confiança do Whisper conferidas com o roteiro (nome da marca, preços, termos)
- Blocos de até 3 palavras, caixa alta, contorno preto, palavra falada na cor da marca
- Legenda é a ÚLTIMA camada: nenhum insert pode cobrir a legenda
- Ortografia igual ao roteiro (acentos, nome da marca, números)

## Mensagem
- O vídeo segue o roteiro do pedido e o comando (tom, público, oferta)
- Promessa, preço e CTA batem exatamente com o pedido
- Nada de promessa que o cliente não autorizou
