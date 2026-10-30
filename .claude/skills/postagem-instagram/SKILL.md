---
name: "postagem-instagram"
description: "Cria postagens orgânicas de Instagram completas (carrossel, post único, Reels, stories) com legenda, imagens/vídeo prontos e base em dados do perfil. Use sempre que o usuário pedir postagem, post, carrossel, Reels, story, legenda, conteúdo para Instagram ou calendário editorial."
---

# Postagem orgânica de Instagram

Sempre que o usuário pedir uma postagem, acople TODAS as frentes abaixo, nesta ordem. Não pergunte se quer cada uma: entregue o pacote completo e deixe o usuário cortar o que não quiser.

## 1. Briefing mínimo
Nicho, tema, objetivo (alcance, salvamentos, leads) e tom de voz. Se já foram dados na conversa ou em outro post, reaproveite. Só pergunte o que faltar e bloqueie o trabalho.

## 2. Dados do perfil (Supermetrics)
Antes de escrever, tente puxar o que performa no perfil do usuário:
- `data_source_discovery` e `accounts_discovery` para achar a conta de Instagram.
- `instagram_insights` / `data_query` para posts de melhor alcance, salvamentos e horários.
- Use o resultado para escolher formato, gancho e horário. Cite os números reais; nunca invente métricas.
- Se a conta não estiver conectada, avise com o link de login e siga sem dados, dizendo que a recomendação é genérica.

## 3. Conteúdo
- **Formato:** escolha pelo objetivo e pelos dados (carrossel para salvamento, Reels para alcance, post único para prova social).
- **Carrossel:** 7 a 10 slides. Slide 1 é gancho, o último é CTA. Uma ideia por slide, texto curto.
- **Reels:** roteiro com gancho nos 3 primeiros segundos, cenas, falas e legenda na tela.
- **Legenda:** primeira linha como gancho, corpo escaneável, CTA único, 3 a 5 hashtags relevantes.
- **Entrega extra:** 3 variações de gancho e sugestão de dia e horário.

## 4. Arte
- Carrossel e post único: gere os slides em HTML 1080x1350 (4:5) com a skill `frontend-design`, uma identidade visual consistente e fontes legíveis no celular. Exporte cada slide em PNG com Playwright (Chromium já instalado, `require('playwright')`) e salve no diretório de trabalho para o usuário abrir.
- Stories: mesma abordagem em 1080x1920.

## 5. Vídeo (Reels)
- Se o usuário enviar gravação bruta: edite com `video-use` (cortes, legendas, color grade).
- Se for animação do zero: use `remotion-best-practices`, 1080x1920, até 30 s.

## 6. Publicação
Só publique ou agende com `manage_social_media` se o usuário pedir explicitamente. Publicar é externo e difícil de desfazer: mostre o post final e confirme antes.

## Entrega final
Resumo curto com: formato escolhido e por quê, legenda, caminho dos arquivos gerados, melhor horário e o que foi baseado em dado real versus estimativa.
