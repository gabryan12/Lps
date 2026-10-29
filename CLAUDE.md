# Regras do projeto

## Vídeo

Sempre que o usuário mencionar "vídeo" (criar, editar, renderizar, animar etc.), invoque **as duas** skills via Skill, antes de qualquer outra coisa, e use-as em conjunto:

- `video-use`: edição do material gravado (transcrição, cortes, color grade, legendas, remoção de pausas).
- `remotion-best-practices`: composição programática (inserts, animações, títulos, lower thirds, overlays, motion graphics, renderização final).

Divisão de trabalho:

1. `video-use` faz o corte base do material bruto e entrega o vídeo editado.
2. Remotion usa esse vídeo como camada base e adiciona os inserts e animações por cima (`<OffthreadVideo>` / `<Sequence>`), com legendas e overlays quando fizer sentido.
3. Renderização final pelo Remotion, a menos que o usuário peça outra saída.

Se o pedido for só de um lado (ex.: só cortar, ou só criar animação do zero), use a skill correspondente, mas ainda carregue as duas.
