# Como publicar artigos (do seu computador, sem GitHub)

Você só usa 3 coisas: o **modelo**, o **previa.bat** e o **publicar.bat**. Tudo fica dentro da pasta `gabriel-site`.

## Uma vez só (preparação)
- Precisa do **Node.js** (você já tem) e do **Python** (gera o site). Se faltar, o `.bat` avisa e diz como instalar (python.org, marcando "Add python.exe to PATH").
- Na primeira vez, o `.bat` baixa as peças que faltam. Depois fica rápido.

## Escrever e publicar um artigo
1. Abra a pasta `conteudo\blog`. Copie o arquivo **`_MODELO-DE-ARTIGO.md`** (Ctrl+C, Ctrl+V) e renomeie a cópia, por exemplo `quanto-custa-anunciar.md` (sem acento, sem espaço, terminando em `.md`). O arquivo que começa com `_` nunca vai para o site.
2. Abra a cópia no **Bloco de Notas** e preencha os campos (os comentários com `#` explicam cada um). Mantenha `rascunho: true` enquanto escreve. Se usar capa, coloque a imagem em `conteudo\imagens`.
3. **Ver a prévia:** dê dois cliques em **`previa.bat`**. O navegador abre em `http://localhost:5000/blog/` com o seu artigo (rascunhos aparecem só aqui). Mudou algo? Feche a janela preta, salve o arquivo e rode `previa.bat` de novo.
4. **Publicar:** troque `rascunho: true` por `rascunho: false`, salve e dê dois cliques em **`publicar.bat`**. Ele gera o site, confere e, se estiver tudo certo, pede **S + Enter** para publicar. Se algo estiver errado, mostra o erro e **não publica**.
5. **Confirmar que subiu** (aba anônima): `https://gabrieldiniztrafego.com.br/blog/` (o artigo aparece) e `/forms/` (continua abrindo).

## Corrigir um artigo já publicado
1. Abra o arquivo do artigo em `conteudo\blog`, corrija o texto.
2. Mude **`atualizado:`** para a data de hoje (ano-mês-dia). O site nunca muda essa data sozinho; ela vai para a página, para o Google (schema) e para o sitemap (`lastmod`). Só mude em revisão real.
3. Dê dois cliques em `publicar.bat`.
4. **Não mude o `slug`** (endereço). Se precisar mudar, escreva o endereço antigo em `slugs_antigos:` (cria redirecionamento 301).

## Remover um artigo
- **Tirar do ar mas guardar:** troque para `rascunho: true` e rode `publicar.bat`.
- **Apagar de vez:** apague o arquivo `.md` e rode `publicar.bat`. O endereço antigo passa a mostrar a página 404. Para mandar quem entra por ele para outro lugar, acrescente uma linha em `conteudo\redirecionamentos.txt`, por exemplo `/blog/artigo-antigo/  /blog/`.
- Se o Google já indexou, peça a remoção no Search Console (opcional).

## O que acontece sozinho ao publicar o primeiro artigo
- O `noindex` do `/blog/` sai (o blog passa a ser indexável). Enquanto não há artigo publicado, ele fica com `noindex`.
- O sitemap ganha o artigo, a categoria e o `/blog/` com a data real de atualização (`lastmod`). Rascunhos nunca entram.
- O artigo recebe schema (`BlogPosting`, `BreadcrumbList` e `FAQPage`), canonical sem www, botão de WhatsApp e caixa do autor.
- A página da categoria é criada. A paginação (12 por página, `/blog/pagina/2/`) aparece quando houver mais de 12 artigos.

## O painel `/admin/`
Hoje **não serve para nada e pode ser ignorado**. Ele depende do GitHub e esta rotina não usa.
