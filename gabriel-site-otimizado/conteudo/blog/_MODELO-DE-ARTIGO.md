---
# ============================================================================
# MODELO DE ARTIGO
# COMO USAR: 1) copie este arquivo (Ctrl+C, Ctrl+V) aqui nesta mesma pasta;
#            2) troque o nome da copia, ex.: como-escolher-gestor-de-trafego.md
#               (sem acento, sem espaco, termina em .md);
#            3) preencha os campos abaixo e o texto no final;
#            4) rode previa.bat para ver o artigo. Quando estiver bom,
#               troque "rascunho: true" por "rascunho: false" e rode publicar.bat.
# Este arquivo (que comeca com "_") nunca vai para o site.
# Tudo depois de "#" e comentario: pode apagar. Mantenha os dois-pontos e os tracos "---".
# ============================================================================

# RASCUNHO: true = so aparece na previa (seu computador). false = vai ao ar no proximo publicar.bat.
rascunho: true

# TITULO (vira o H1 da pagina): escreva como uma PERGUNTA que a pessoa faria no Google.
# Ate 60 caracteres. Ex.: "Quanto custa anunciar no Google para uma clinica?"
titulo: Escreva aqui o titulo em forma de pergunta?

# ENDERECO do artigo: so letras minusculas, numeros e hifen. Vira /blog/<endereco>/. Nao mude depois de publicar.
slug: escreva-o-endereco-do-artigo

# DESCRICAO (resumo): 1 frase, ate 160 caracteres. Aparece no Google e na lista do blog.
resumo: Uma frase dizendo o que a pessoa vai entender ao ler este artigo.

# CATEGORIA: escolha UMA destas, escrita exatamente assim:
# Tráfego | IA | Sites e SEO | Google Meu Negócio
categoria: Tráfego

# DATA DE PUBLICACAO: ano-mes-dia. Dia em que o artigo sai pela primeira vez.
publicado: 2026-01-01

# DATA DE ATUALIZACAO: ano-mes-dia. No primeiro dia, igual a de publicacao.
# So mude quando voce REVISAR o artigo de verdade (o site nunca muda isso sozinho).
atualizado: 2026-01-01

# CAPA (opcional): coloque a imagem na pasta conteudo\imagens e escreva o caminho abaixo.
# Se usar capa, o texto alternativo e obrigatorio (descreva a imagem em uma frase).
# Para usar, apague o "#" no comeco das duas linhas:
# capa: /conteudo/imagens/nome-da-imagem.jpg
# capa_alt: Descreva a imagem em uma frase

# RESPOSTA DIRETA: responda a pergunta do titulo em 40 a 60 palavras, sem enrolar.
# E o trecho que o Google e as IAs costumam citar. Escreva em uma linha so, sem aspas se possivel.
resposta_direta: Escreva aqui a resposta curta e completa para a pergunta do titulo, entre 40 e 60 palavras, em linguagem simples, sem prometer resultado.

# PERGUNTAS FREQUENTES: de 3 a 5. Cada uma com "pergunta" e "resposta" (resposta curta, 1 a 3 frases).
faq:
  - pergunta: Primeira duvida que as pessoas costumam ter?
    resposta: Resposta curta e honesta.
  - pergunta: Segunda duvida?
    resposta: Resposta curta e honesta.
  - pergunta: Terceira duvida?
    resposta: Resposta curta e honesta.

# FONTES: de onde veio a informacao (site oficial, lei, documentacao). O endereco comeca com https://
fontes:
  - titulo: Nome da fonte
    url: https://exemplo.com.br/pagina

# ARTIGOS RELACIONADOS: de 2 a 4 enderecos (slug) de OUTROS artigos ja publicados.
# Ex.: relacionados: [outro-artigo, mais-um-artigo]. Se ainda nao houver, deixe []
relacionados: []

# ENDERECOS ANTIGOS: so use se mudar o "slug" de um artigo ja publicado (cria redirecionamento).
# Ex.: slugs_antigos: [endereco-antigo]. Normalmente deixe []
slugs_antigos: []
---

<!-- CORPO DO ARTIGO. Estes comentarios nao aparecem no site.
     Escreva em secoes: use "##" para titulo de secao e "###" para subtitulo.
     NAO use "#" sozinho (o titulo do artigo ja e o H1). Nao repita o titulo aqui. -->

Abertura: 2 ou 3 frases dizendo o problema da pessoa e o que este artigo resolve.

## Primeira secao (uma ideia por secao)

Explique a primeira ideia em paragrafos curtos. Frases diretas, sem prometer numeros nem resultados.

- Listas ajudam: uma ideia por item.
- Use quando houver passos ou itens para conferir.

## Segunda secao

Continue a explicacao. Se precisar de um subtitulo dentro da secao, use tres "###".

### Um exemplo pratico

Mostre um exemplo real e simples.

## Terceira secao: como aplicar no seu negocio

Feche com o que a pessoa pode fazer agora. Se fizer sentido, convide para conversar (o botao de WhatsApp ja aparece no fim do artigo).

<!-- Tabela (opcional). Apague se nao usar:
| Item | Pergunta | Esta pronto quando |
| --- | --- | --- |
| Exemplo | Pergunta de conferencia? | Criterio claro |
-->
