/* Conteúdo editável do site.
   Provas e artigos começam vazios: as seções só aparecem quando houver conteúdo aqui. */
window.SITE_CONTENT = {
  whatsapp: "5521989227990",
  telefone: "(21) 98922-7990",
  email: "sagatrafego@gmail.com",
  empresa: { razao: "", cnpj: "" },   // preencha: razão social e CNPJ aparecem no rodapé
  gtmId: "",                          // exemplo: "GTM-XXXXXXX" (só carrega depois do "Aceitar")
  links: {
    gmn: "https://maps.app.goo.gl/dZPaRz95yG16iqbj6",
    instagram: "https://www.instagram.com/gabrieldiniztrafego/",
    linkedin: "https://www.linkedin.com/in/gabriel-diniz-trafego-pago-a0abb8259/"
  },
  provas: {
    // numeros: [{ valor: "", legenda: "" }]  (legenda com período e origem do dado)
    numeros: [],
    // depoimentos: [{ texto: "", autor: "" }]  (só com autorização do cliente)
    depoimentos: [],
    // casos: [{ titulo: "", situacao: "", feito: "", resultado: "" }]
    casos: []
  },
  // posts: [{ slug, titulo, resumo, categoria, data, imagem }]  (o painel do blog preenche isto)
  posts: []
};
