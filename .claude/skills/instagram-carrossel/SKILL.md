---
name: instagram-carrossel
description: Cria carrossel de Instagram completo — roteiro dos slides, design e PNGs 1080x1350 prontos para postar, mais legenda e hashtags. Use quando o usuário pedir "carrossel", "carousel", "post em carrossel", "slides pro Instagram", "transforma isso em carrossel", "conteúdo em sequência pro feed", ou mandar um texto/artigo/aula e quiser virar carrossel.
---

# Carrossel de Instagram

Entrega um carrossel pronto: o roteiro slide a slide, os PNGs renderizados no
tamanho certo e a legenda. O objetivo de um carrossel é **fazer a pessoa passar
para o próximo slide** e, no fim, salvar, compartilhar ou chamar no direct. Cada
decisão de texto e de design serve a isso.

## Antes de começar

Descubra, na conversa ou nos arquivos do repositório:

- **Tema e objetivo**: educar, vender, gerar autoridade, captar lead (palavra no direct)?
- **Público**: quem lê e qual problema tem — escreva na língua dele
- **Perfil/marca**: @ do perfil, cores, fontes, logo, foto (se houver página ou
  identidade no repo, leia e herde)
- **CTA final**: o que a pessoa deve fazer — salvar, comentar uma palavra, clicar no link da bio, chamar no WhatsApp

Se faltar só a identidade visual, escolha uma direção coerente com o nicho e diga
qual escolheu. Se faltar o tema, pergunte. Não trave por detalhe.

## Roteiro (texto)

1. **7 a 10 slides** é o padrão. Máximo 20 (limite do Instagram). Menos de 5 raramente vale um carrossel.
2. **Slide 1 = gancho.** Uma frase, até ~12 palavras, que cria tensão: número
   concreto, erro comum, promessa específica ou contradição. Nada de "Dicas sobre X".
   Bom: "3 erros que fazem seu orçamento parecer caro". Ruim: "Dicas de precificação".
3. **Slide 2 = por que importa.** Confirma o problema ou a dor; segura quem ficou curioso.
4. **Miolo = uma ideia por slide.** Título curto + no máximo 2–3 linhas de apoio
   (~30 palavras). Se precisa de mais, vira dois slides.
5. **Penúltimo = síntese** (resumo, checklist ou antes/depois) — é o slide que faz salvar.
6. **Último = CTA único e claro.** Uma ação só. "Comenta CHECKLIST que eu te mando" > "curte, comenta, compartilha e segue".
7. Escreva com o vocabulário real do público, frases curtas, sem jargão de marketing.
   Números e exemplos concretos > adjetivos.
8. Não invente dados, estatísticas ou depoimentos. Se o usuário não deu o número, use exemplo genérico sinalizado ou deixe placeholder visível.

Mostre o roteiro (tabela: nº, título, texto de apoio) **e já siga para o design** —
não pare para pedir aprovação, a não ser que o usuário tenha pedido para revisar antes.

## Design

9. Formato **1080x1350 (4:5)** — ocupa mais tela no feed que o quadrado. Só use
   1080x1080 se o usuário pedir.
10. Um único HTML com todos os slides, cada um um `<section class="slide">` de
    exatamente 1080x1350px, empilhados verticalmente (`display:block`, sem margem
    entre eles). Fontes do Google Fonts via `<link>`; nada de dependência local.
11. **Área segura**: margens internas de pelo menos 80px; nada importante nos 120px
    de baixo do 1º slide (o Instagram sobrepõe ícones/legenda no preview).
12. **Tipografia grande**: título 72–110px, texto de apoio 36–44px. Se lê mal no
    celular em tamanho de miniatura, está pequeno. Máximo 2 famílias de fonte.
13. **Consistência**: mesmo grid, mesmas cores e posição de elementos em todos os
    slides; varie só o conteúdo. O 1º e o último podem ter tratamento especial.
14. **Continuidade visual**: indicador de progresso discreto (ex.: "3/8" ou barra)
    e uma seta/sinal de "arrasta" no 1º slide. Elementos que "vazam" de um slide
    para o próximo reforçam o swipe.
15. Rodapé discreto com o @ do perfil em todos os slides.
16. Contraste alto (texto sobre fundo com contraste AA). Evite gradiente roxo
    genérico, emoji em excesso e cara de template — use a skill `frontend-design`
    como referência de direção estética quando não houver identidade definida.

## Renderizar os PNGs

Salve o HTML em `instagram/<slug-do-tema>/carrossel.html` (crie a pasta) e rode:

```bash
node .claude/skills/instagram-carrossel/scripts/render.js instagram/<slug>/carrossel.html instagram/<slug>/png
```

O script gera `slide-01.png`, `slide-02.png`… e avisa se algum slide não está em
1080x1350. Para quadrado, passe `1080 1080` no fim.

Depois de renderizar, **abra pelo menos o slide 1 e um do miolo com a ferramenta
Read** e confira: texto cortado, sobreposição, contraste, fonte que não carregou.
Corrija e renderize de novo antes de entregar.

## Legenda

Entregue junto, em `instagram/<slug>/legenda.txt`:

- **1ª linha = gancho** (aparece antes do "mais"; ~125 caracteres). Não repita o slide 1 palavra por palavra — complemente.
- Corpo curto: contexto ou bastidor, em parágrafos de 1–2 linhas.
- CTA igual ao do último slide.
- **3 a 8 hashtags** específicas do nicho (não use #love #instagood). Opcional: palavras-chave no texto ajudam a busca do Instagram mais que hashtags.
- Sugestão de **texto alternativo** (acessibilidade) para o 1º slide.

## Entrega

- Envie os PNGs ao usuário (SendUserFile) e diga o caminho da pasta.
- Mostre a legenda pronta para copiar.
- Se o usuário quiser versão animada para Reels, sugira a skill `remotion-best-practices`.
- Pergunte se quer commitar a pasta `instagram/` no repositório só se ele trabalha com git; senão, apenas entregue.
