# Rotina · Pauta do dia

**Onde:** Claude Code › Rotinas › Nova rotina · **Quando:** todo dia, 6h30
**Antes de rodar:** troque as 3 primeiras linhas (negócio, público, tom) pelas suas. Clique em
*Executar agora* na primeira vez e aprove o que ele pedir: as próximas rodam sozinhas.

```
Faça minha pauta de conteúdo do dia.

MEU NEGÓCIO: clínica de estética facial / harmonização
MEU PÚBLICO: mulheres de 30 a 50 anos no Rio de Janeiro
MEU TOM: próxima, segura, sem promessa milagrosa

1. PESQUISE DE VERDADE na web notícias das últimas 72h (no máximo 7 dias) sobre o meu nicho no Brasil: famosos, polêmicas, casos de polícia, regras novas, estudos. Priorize grandes portais (g1, O Globo, Folha, UOL). Descarte press release e publieditorial.
2. ESCOLHA as 3 notícias com mais chance de gerar conversa com o meu público — de preferência uma de famoso, uma de segurança/alerta e uma que eu possa explicar como especialista.
3. PARA CADA UMA, ENTREGUE PRONTO PRA GRAVAR:
   - Foto: a foto principal da própria matéria (a imagem de destaque da página, a og:image, ou a foto do corpo do texto que mais tem a ver com o assunto)
   - Gancho: a primeira frase exata do vídeo/capa (máx. 12 palavras)
   - Roteiro em 3 linhas: abertura, virada, chamada pra ação
   - Legenda pronta, com pergunta no final e até 5 hashtags
   - Formato: Reels ou carrossel, e por quê
   - Fonte: título, veículo, data e link clicável
   - Por que vai performar com o meu público (1 frase)
   - Cuidado ao gravar: o que NÃO dizer (ex.: não citar nome de investigado que não foi indiciado, não comentar o rosto de famoso, não prometer resultado)
4. REGRAS: nada inventado. Todo fato, número e nome precisa estar no link citado. Se não achar 3 notícias boas da semana, entregue menos e diga isso. Não faça promessa de resultado nem diagnóstico. NUNCA use notícia que envolva morte — nem como alerta de segurança. O alerta tem que ser um caso sem vítima fatal (produto falsificado, apreensão, regra nova etc.); se não houver, entregue menos e diga isso.
5. ENTREGUE como um painel de uma página, bonito e legível no celular, com a data de hoje no topo e um card por ideia (a melhor primeiro). A foto vai no topo de cada card, largura cheia, com legenda de crédito embaixo: "Foto publicada na matéria de <veículo>. Só para referência, não reutilize no post." Cada legenda e cada gancho com botão "copiar".
   COMO COLOCAR AS FOTOS (obrigatório, senão elas não aparecem): o artefato bloqueia imagem puxada de outro site, então NÃO use o link da foto direto no <img>. Baixe cada foto, reduza para no máximo 1000 px de largura em JPEG (no Mac: sips -Z 1000 -s format jpeg -s formatOptions 75; no Windows: use Python com Pillow), e publique junto com a página pelo parâmetro `files` do Artifact (ex.: "img/noticia1.jpg"), usando caminho relativo no <img>. Se uma foto não baixar, deixe o card sem foto e diga isso no fim.
   PUBLIQUE esse painel como ARTEFATO do claude.ai (privado), com o título "Pauta do dia". Atualize SEMPRE o mesmo artefato, procurando na sua lista de artefatos um com o título "Pauta do dia" (se existir, leia e republique por cima; troque as fotos antigas pelas novas e remova com null as que não forem mais usadas). Só crie um novo se não existir. No fim, me diga o link do artefato.
```
