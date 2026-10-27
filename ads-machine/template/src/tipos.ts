// Contrato entre os agentes e o Remotion. Cada agente escreve só a sua parte
// do props.json; o template não precisa ser editado para cada anúncio.

export type Palavra = {
  text: string; // com espaço na frente: " palavra"
  startMs: number;
  endMs: number;
  timestampMs: number | null;
  confidence: number | null;
};

type Janela = { inicioMs: number; fimMs: number };

export type Insert = Janela &
  (
    | { tipo: "texto"; texto: string; posicao?: "topo" | "centro"; destaque?: boolean }
    | { tipo: "zoom"; escala?: number }
    | { tipo: "broll"; src: string; modo?: "tela-cheia" | "janela"; video?: boolean }
    | { tipo: "emoji"; emoji: string }
    | { tipo: "numero"; de: number; ate: number; prefixo?: string; sufixo?: string }
    | { tipo: "cta"; texto: string; subtexto?: string }
  );

export type Estilo = {
  corPrimaria: string;
  corTexto: string;
  corFundo: string[]; // gradiente do modo sem vídeo
  fonte: string;
  legendaPosicao: "baixo" | "meio";
  palavrasPorBloco: number;
};

export type AnuncioProps = {
  video: string | null; // caminho em public/ (ex.: "meu-anuncio/cortado.mp4") ou null = fundo animado
  audio: string | null; // usado só quando video é null ou mudo
  duracaoMs: number;
  fps: number;
  largura: number;
  altura: number;
  estilo: Estilo;
  inserts: Insert[];
  legendas: Palavra[];
};

export const PROPS_PADRAO: AnuncioProps = {
  video: null,
  audio: null,
  duracaoMs: 6000,
  fps: 30,
  largura: 1080,
  altura: 1920,
  estilo: {
    corPrimaria: "#FFD400",
    corTexto: "#FFFFFF",
    corFundo: ["#0B0B0F", "#1C1240"],
    fonte: "Montserrat, Arial Black, sans-serif",
    legendaPosicao: "meio",
    palavrasPorBloco: 3,
  },
  inserts: [
    { tipo: "texto", inicioMs: 0, fimMs: 2200, texto: "PAROU DE PERDER CLIENTE", posicao: "topo", destaque: true },
    { tipo: "emoji", inicioMs: 2200, fimMs: 3600, emoji: "⚡" },
    { tipo: "cta", inicioMs: 3600, fimMs: 6000, texto: "Fale com a gente", subtexto: "Clique no botão abaixo" },
  ],
  legendas: [
    { text: " Exemplo", startMs: 0, endMs: 700, timestampMs: 350, confidence: 1 },
    { text: " de", startMs: 700, endMs: 900, timestampMs: 800, confidence: 1 },
    { text: " legenda", startMs: 900, endMs: 1600, timestampMs: 1250, confidence: 1 },
    { text: " animada", startMs: 1600, endMs: 2400, timestampMs: 2000, confidence: 1 },
  ],
};
