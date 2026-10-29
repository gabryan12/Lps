# Regras do projeto

## Vídeo

Sempre que o usuário mencionar "vídeo" (criar, editar, renderizar, animar etc.), invoque **as duas** skills via Skill, antes de qualquer outra coisa, e use-as em conjunto:

- `video-use`: edição do material gravado (transcrição, cortes, color grade, legendas, remoção de pausas).
- `remotion-best-practices`: composição programática (inserts, animações, títulos, lower thirds, overlays, motion graphics, renderização final).

Divisão de trabalho:

1. `video-use` faz o corte base do material bruto e entrega o vídeo editado.
2. Remotion usa esse vídeo como camada base e adiciona os inserts e animações por cima (`<OffthreadVideo>` / `<Sequence>`), com legendas e overlays quando fizer sentido.
3. Renderização final pelo Remotion, a menos que o usuário peça outra saída.

### Organizadora (antes de editar)

Antes de cortar ou renderizar qualquer coisa, monte e apresente ao usuário um plano curto e espere a confirmação:

- objetivo do vídeo, duração e formato alvo (proporção, resolução);
- arquivos de entrada e onde cada saída vai ficar (uma pasta por vídeo, ex.: `videos/<nome>/{bruto,editado,remotion,final}`);
- lista de cortes previstos, inserts/animações (com o ponto de entrada de cada um), estilo de legenda e color grade;
- qual skill cuida de cada etapa.

Só avance para a execução depois que o usuário aprovar o plano.

### Revisora (antes de entregar)

Depois da renderização final, e antes de dizer que terminou, revise o resultado:

- confira duração, resolução e se há áudio (ffprobe);
- extraia frames em pontos-chave (início, cada insert, cortes, fim) e olhe cada um;
- verifique legendas (texto correto, sincronia, sem cortar na borda), cortes (sem palavra picotada) e inserts (entram e saem no ponto planejado);
- compare com o plano da organizadora e liste o que ficou diferente.

Corrija o que estiver errado e revise de novo. Ao entregar, diga o que foi checado e qualquer ponto que não deu para verificar.

Se o pedido for só de um lado (ex.: só cortar, ou só criar animação do zero), use a skill correspondente, mas ainda carregue as duas.
