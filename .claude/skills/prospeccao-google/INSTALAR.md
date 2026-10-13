# Como instalar

Você vai **conversar** com o Claude em português. Ele faz o trabalho técnico sozinho.

São três passos. **Uns 10 minutos** contando criar a conta da Apify — a busca em si leva uns 3.

> **Skill** é uma habilidade nova que você ensina pro Claude. Depois de instalada, ele sabe fazer uma coisa que antes não sabia.

---

## O que isso faz

Você pede *"prospectar pizzaria em Curitiba"* e recebe uma lista de negócios da cidade que **não têm site**, do maior pro menor, com uma mensagem pronta pra mandar em cada um.

---

## Antes de tudo

**1. Você precisa do app do Claude aberto, na aba Code.** É o mesmo programa da aula — você não vai instalar nada novo aqui.

⚠️ **Não é o Claude do navegador.** O Claude do site conversa, mas não mexe nos seus arquivos, e por isso **não serve** pra esta skill. Se você colar os pedidos abaixo no site, ele vai responder bonitinho e não vai instalar nada.

**2. Ele vai pedir permissão — e você clica pra deixar.** Vai aparecer, algumas vezes, um aviso do tipo *"posso criar esse arquivo?"* com botões embaixo.

> **Pode permitir tudo durante a instalação.** Ele cria arquivos novos, não apaga os seus.

**3. Descompacte o arquivo baixado.** Você baixou algo como `skill-prospeccao.zip`:

- **Mac:** clique duas vezes. Aparece uma pasta `skill-prospeccao` do lado.
- **Windows:** clique com o botão direito → **Extrair tudo** → Extrair. Dois cliques no Windows só espiam dentro do zip, não extraem — e aí o Claude não encontra nada.

---

## Passo 1 — instalar a skill

Você já baixou e descompactou o `skill-prospeccao.zip` (link no material da aula) — a pasta `skill-prospeccao` está aí em algum lugar. **Não precisa movê-la.**

Cole isto no Claude e aperte Enter:

```
Instale a skill que está na pasta skill-prospeccao. Ela está em Downloads ou na minha Área de Trabalho. Ache a pasta, crie o lugar certo se não existir, e me confirme quando estiver instalada.
```

Ele procura nos dois lugares, cria o destino certo e te avisa. Se disser que não encontrou, responda em português contando onde você salvou — ele acha.

> **Por que assim:** a pasta onde as skills moram é escondida — nem o Finder do Mac nem o Explorador do Windows mostram ela. Quem tenta arrastar na mão quase sempre erra o lugar e a skill nunca aparece.

Depois que ele confirmar, **abra uma conversa nova** — é nela que você vai usar a skill.

---

## Passo 2 — conectar o Google Maps

A skill busca os negócios através de um serviço chamado **Apify**. Você precisa de uma conta lá.

**Primeiro, crie a conta:** digite **apify.com** na barra de endereço do navegador e clique em **Sign up** (é "cadastrar" em inglês). Confirme o e-mail que eles mandam.

> **Não vai pedir cartão.** A conta gratuita não aceita nem pede cartão — não existe como te cobrarem.

**Agora ligue a Apify no app do Claude:**

No menu da esquerda, clique em **Personalizar** → aba **Conectores** → **Descobrir** → busque **apify** → clique na **Apify** (a da *Apify Technologies*, marcada como *Extensão para desktop*) → instale e autorize com a conta que você acabou de criar.

Vai abrir uma janela no navegador pedindo pra autorizar: **essa janela é esperada, não é golpe.** Clique em autorizar e volte pro app.

> **Faça por aqui, não pedindo pro Claude.** Se você pedir *"liga a minha Apify"* numa conversa, ele liga por outro caminho que a skill não reconhece.

---

## Passo 3 — usar

Na conversa nova, peça:

```
prospectar pizzaria em Curitiba
```

Troque pelo que você quiser: *"prospectar clínica de estética no Rio de Janeiro"*, *"prospectar salão de beleza em Salvador"*.

**Demora uns 3 minutos.** Boa parte é tela parada esperando o Google Maps responder — você vai ver o Claude escrevendo de vez em quando e depois parando de novo. **Isso é normal, não feche.** Se passar de 10 minutos, pergunte: *"o que está acontecendo?"*

No fim ele entrega dois arquivos: a **lista com as mensagens escritas** e o **painel visual**.

Eles ficam guardados junto com a skill, numa pasta que o computador não mostra — então **não saia procurando**. Peça pra ele:

```
abre o resultado pra mim
```

E pra guardar num lugar que você enxerga, peça também:

```
copia os dois arquivos pra minha Área de Trabalho
```

---

## Deu errado?

**O Claude ignora quando você pede pra prospectar**
Você está numa conversa nova, aberta depois de instalar? Se já está, peça: *"liste as skills que você tem instaladas"* — a `prospeccao-google` tem que aparecer.

**Ele não achou a pasta**
Provavelmente o arquivo ainda está zipado, ou está em outra pasta. Responda pra ele dizendo onde você salvou — ele procura.

**Ele diz que a Apify não está conectada**
Abra **Personalizar › Conectores › Meus** e confira se a **Apify** aparece instalada e ligada. Se não, refaça o Passo 2 e confirme que clicou em autorizar na janela do navegador. Depois abra uma conversa nova.

**Travou numa tela parada**
Espere até 10 minutos — o Google Maps às vezes é lento. Passou disso, pergunte: *"o que está acontecendo com a busca?"*

**"Insufficient credit" / "sem crédito"**
Os créditos grátis do mês acabaram. Veja em console.apify.com/billing quando renovam.

**Veio pouca gente na lista**
Normal em cidade pequena ou nicho muito específico. Tente a cidade maior mais perto, ou um termo mais amplo (*"salão"* no lugar de *"salão de alongamento de unhas"*).
