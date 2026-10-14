# Rotina · Caixa de entrada zerada

**Onde:** Claude Code › Rotinas › Nova rotina · **Quando:** todo dia, 8h e 14h
**Antes de rodar:** precisa do conector do Google ligado. Só lê: nada é enviado, apagado ou
arquivado. Clique em *Executar agora* na primeira vez e aprove o que ele pedir.

```
Faça a triagem dos meus e-mails novos (desde a última rodada, no máximo 24h) usando o conector do Gmail e me entregue UM painel chamado "Caixa de entrada zerada".

REGRA DE OURO: você só LÊ. Nunca envie, responda, encaminhe, arquive, apague, marque como lido, rotule, mova para spam nem crie rascunho no Gmail. Os rascunhos existem SÓ dentro do painel, para eu copiar e colar se quiser.

1. Separe cada e-mail em 4 grupos:
   - Urgente: dinheiro parado, algo fora do ar, segurança da conta, cliente ou parceiro esperando resposta hoje.
   - Responder esta semana: pessoa real pedindo algo que pode esperar.
   - Só leitura: avisos e relatórios úteis que não pedem ação.
   - Lixo: promoção, newsletter que eu nunca abro, propaganda.
2. No topo, 4 números grandes (um por grupo) e a frase: "Você tinha X e-mails. Precisa olhar só Y." Os 4 números são ABAS clicáveis: ao clicar, o painel mostra só aquele grupo. Abre na aba Urgente.
3. Para cada Urgente: remetente, assunto, UMA linha dizendo por que é urgente, a ação que eu devo tomar, e um RASCUNHO de resposta pronto no meu tom (curto, direto, sem floreio, português do Brasil) com um botão "copiar". Se não há ninguém para responder (é um aviso automático), diga "não precisa responder — só agir" e diga a ação. Cada item urgente tem uma caixinha "feito" para eu marcar.
4. Bloco "Descadastre destes": os remetentes que mais mandaram lixo, com quantos e-mails cada um mandou.
5. Rodapé: "Tempo economizado: ~N minutos" (conte 30 segundos por e-mail lido por você + 2 minutos por rascunho escrito) e a data/hora da triagem.
6. Não mostre dados sensíveis (CPF, CNPJ, número de cartão, valores de clientes, links de login). Na dúvida, resuma. SEM imagens: nada de foto, logo ou anexo dos e-mails.

PUBLIQUE como ARTEFATO do claude.ai (privado), com o título "Caixa de entrada zerada". Atualize SEMPRE o mesmo artefato: antes, liste seus artefatos (action "list") e, se já existir um com esse título, leia (action "read") e republique por cima passando o url dele. Só crie um novo se não existir. No fim, me diga só: quantos urgentes e o link do artefato.
```
