# Origem e licença do globo

**ATENÇÃO: este arquivo precisa ser preenchido por você.** O pacote não trouxe o vídeo original nem o link da licença, e eu não inventei esses dados.

## O que existe hoje no pacote

| Pasta | O que é | Tamanho da imagem |
|---|---|---|
| `src/assets/globo-d/` | 38 quadros do globo para o computador (WebP) | 960 x 872 |
| `src/origem/globo-m-38/` | 38 quadros do globo para o celular, a partir dos quais a versão leve é gerada | 600 x 545 |
| `src/assets/globo-m2/` | versão leve do celular, gerada por `src/tools/gerar-globo-mobile.py` (19 quadros, nomes com hash). Não edite à mão | 600 x 545 |

Todos os quadros foram extraídos de um vídeo do globo (a fonte original). Esse vídeo **não está** no pacote.

## Registro da fonte (preencher)

- Nome do arquivo de vídeo original: ______________________
- Onde foi obtido (endereço/link da página de origem): ______________________
- Autor ou plataforma: ______________________
- Licença (nome e link do texto da licença): ______________________
- Data em que foi baixado: ______________________
- Pode ser usado comercialmente? Exige crédito/atribuição? ______________________
- Onde o vídeo original está guardado (pasta/nuvem): ______________________

Guarde também um comprovante da licença (e-mail, recibo ou captura da página). Se a licença exigir crédito, ele precisa aparecer no site.

## Como refazer o globo a partir do vídeo original

1. Extraia os quadros do vídeo (por exemplo, com `ffmpeg`) em WebP, 38 quadros num ciclo: 600 x 545 para o celular e 960 x 872 para o computador.
2. Coloque os do celular em `src/origem/globo-m-38/` e os do computador em `src/assets/globo-d/`, numerados `000.webp`, `001.webp` e assim por diante.
3. Gere o celular: `python3 src/tools/gerar-globo-mobile.py 2` (o `2` pega um quadro a cada dois; precisa do Python).
4. Gere o site: `python3 src/build.py prod`.
5. Se trocar uma imagem do computador mantendo o mesmo nome, quem já visitou continua vendo a antiga por até 1 ano (cache). Troque o nome da pasta `globo-d` (e o caminho em `src/js/site.js`).
