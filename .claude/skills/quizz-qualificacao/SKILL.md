---
name: quizz-qualificacao
description: Adiciona um quizz de diagnóstico/qualificação em uma página ou site, que substitui o link direto de WhatsApp e entrega o lead já qualificado. Use quando o usuário pedir "quizz", "quiz de diagnóstico", "quiz de qualificação", "formulário de qualificação", "captura antes do WhatsApp", "qualificar lead na página", ou quiser que a pessoa responda perguntas antes de cair no atendimento.
---

# Quizz de qualificação embutido na página

Adiciona um quizz de 4 perguntas que substitui o link direto de WhatsApp: a pessoa
clica no CTA, responde, vê um resultado útil na hora, e só então o WhatsApp abre
com as respostas já preenchidas na mensagem.

O ganho é duplo — a pessoa recebe uma resposta concreta antes de falar com alguém,
e o atendente recebe um lead já qualificado em vez de "oi, tudo bem?".

## Antes de começar

Descubra, na conversa ou lendo a página:

- **Negócio**: o que vende e para quem
- **Número de WhatsApp**: formato `55DDNNNNNNNNN`
- **O que o cliente precisa saber antes de comprar**: faixa de preço? prazo? se
  o caso dele é atendido?
- **O que o dono precisa saber antes de atender**: orçamento, urgência, tipo de
  problema, tamanho da operação?

Se a página já existe, leia o arquivo inteiro antes de editar — as variáveis de
cor, as fontes e o espaçamento dela são o que o quizz precisa herdar. Se faltar
só o número de WhatsApp, use um placeholder visível e avise no fim; não trave a
entrega por isso. Se faltar o essencial (o que o negócio vende), pergunte.

## Regras de conteúdo

1. As 4 perguntas devem qualificar de verdade — cada resposta precisa mudar algo
   no resultado ou na prioridade do lead. Nada de pergunta decorativa.
   Ordem que funciona: **contexto → problema/sintoma → urgência ou histórico → nome**.
2. Use o vocabulário real do negócio nas perguntas e nas opções, não termos de
   marketing. Quem lê tem que se reconhecer na alternativa. "Dá corda mas não
   acumula" vale mais que "problema no mecanismo".
3. A última pergunta é o nome, em campo de texto. Não peça e-mail nem telefone:
   o WhatsApp já entrega o contato, e cada campo a mais derruba a conclusão.
4. O resultado **não** é uma nota nem um "perfil". É uma resposta concreta e útil:
   causa provável, faixa de valor, prazo estimado, próximo passo. Derive isso das
   respostas — se a mesma tela aparece para todo mundo, o quizz não vale nada.
5. Seja honesto na estimativa. Diga que é faixa e o que fecha o valor real. Se
   alguma resposta indicar um serviço maior, diga isso sem empurrar.
6. Mensagem do WhatsApp: uma linha por resposta, em texto limpo, para o atendente
   bater o olho e já saber com quem está falando.

## Regras de design

7. Herde a identidade da página: mesmas variáveis de cor, mesmas fontes, mesmo
   tratamento de borda e espaçamento. O quizz não pode parecer um widget colado.
   Não use gradiente roxo, verde-limão nem emoji se isso não estiver na página.
8. Overlay em tela cheia, uma pergunta por vez, indicador de progresso com 4
   marcas. Nada de rolagem dentro da pergunta.
9. Opções são botões grandes (altura mínima 60px), clicáveis inteiros, com marcador
   discreto A/B/C/D. Botão "Voltar" a partir da 2ª pergunta.
10. O resultado usa layout de ficha técnica: rótulo à esquerda, valor à direita,
    com os dois campos mais importantes destacados na cor de acento.

## Regras técnicas

11. Tudo em um único arquivo: HTML, CSS e JS embutidos. Sem framework, sem
    dependência externa, sem `localStorage`.
12. Todos os CTAs da página passam a abrir o quizz (hero, seção final, botão
    flutuante). Nenhum link direto de WhatsApp deve sobrar.
13. Acessibilidade: `role="dialog"` + `aria-modal`, fecha no Esc e no clique fora,
    foco vai para a primeira opção ao trocar de pergunta e volta para o botão de
    origem ao fechar, foco visível, trava o scroll do `body` enquanto aberto.
14. Respeite `prefers-reduced-motion` e mantenha tudo funcional em 375px.

## Adaptação por segmento

| Segmento | As 4 perguntas | O resultado entrega |
|---|---|---|
| Serviço técnico (conserto, manutenção, reforma) | tipo do item → sintoma → tempo sem manutenção → nome | causa provável + faixa de valor + prazo |
| Consultoria / agência | segmento → faturamento ou tamanho → principal gargalo → nome | diagnóstico do gargalo + o que atacar primeiro |
| Saúde / estética | queixa → há quanto tempo → já tratou antes → nome | o que costuma estar por trás + tipo de avaliação indicada |
| Educação / curso | nível atual → objetivo → tempo por semana → nome | trilha recomendada + prazo realista |
| Imobiliária | comprar ou alugar → faixa de valor → região → nome | quantos imóveis batem com o perfil + próximo passo |

Em saúde, evite superlativo e promessa de resultado (restrição CFM/CRO): o
resultado sugere o **tipo de avaliação**, nunca o diagnóstico fechado.

## Estrutura do JS

Modelo mental — não copie literalmente, adapte ao vocabulário do negócio:

```js
var perguntas = [
  { chave:'contexto', titulo:'...', dica:'...', opcoes:['A','B','C','D'] },
  { chave:'problema', titulo:'...', dica:'...', opcoes:[...] },
  { chave:'urgencia', titulo:'...', dica:'...', opcoes:[...] },
  { chave:'nome',     titulo:'Como podemos te chamar?', dica:'Última pergunta', campo:'Seu nome' }
];

// mapeia a resposta que mais pesa → o conteúdo do resultado
var resultados = {
  'resposta A': { causa:'...', faixa:'R$ X a R$ Y', prazo:'N dias' },
  // ...
};
```

Estado: `passo` e `respostas`. Uma função `desenhar()` que renderiza a pergunta
atual, e uma `resultado()` que monta a ficha e o link `wa.me`. Monte a mensagem
com `encodeURIComponent` e `\n` entre as linhas.

## Entrega

Edite o arquivo existente, não crie um novo. Se o site estiver publicado, ofereça
republicar. Feche dizendo, em uma linha por pergunta, o que cada uma está
qualificando e por quê — é isso que permite ao dono ajustar depois.

## Os três erros que matam o quizz

1. **Pedir dados antes de entregar valor.** Nome só na última pergunta, e-mail nunca.
2. **Resultado genérico.** Se a tela final não muda conforme as respostas, a pessoa
   percebe que foi formulário disfarçado e não clica no WhatsApp.
3. **Mais de 5 perguntas.** A cada pergunta extra a conclusão cai. Quatro é o ponto
   onde ainda qualifica e quase todo mundo termina.
