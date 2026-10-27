import { AbsoluteFill, Img, interpolate, OffthreadVideo, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Estilo, Insert } from "../tipos";

const useEntrada = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return spring({ frame, fps, config: { damping: 14, stiffness: 160 } });
};

export const InsertLayer: React.FC<{ insert: Insert; estilo: Estilo }> = ({ insert, estilo }) => {
  const entrada = useEntrada();
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  switch (insert.tipo) {
    case "broll": {
      const src = staticFile(insert.src);
      const janela = insert.modo === "janela";
      const midia = insert.video ? (
        <OffthreadVideo src={src} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      ) : (
        <Img src={src} style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${interpolate(frame, [0, fps * 4], [1, 1.12])})` }} />
      );
      return (
        <AbsoluteFill style={janela ? { alignItems: "center", paddingTop: 180 } : undefined}>
          <div
            style={
              janela
                ? { width: 900, height: 560, borderRadius: 36, overflow: "hidden", boxShadow: "0 20px 60px #0008", transform: `scale(${entrada})` }
                : { width: "100%", height: "100%", opacity: interpolate(frame, [0, 4], [0, 1], { extrapolateRight: "clamp" }) }
            }
          >
            {midia}
          </div>
        </AbsoluteFill>
      );
    }
    case "texto":
      return (
        <AbsoluteFill style={{ alignItems: "center", justifyContent: insert.posicao === "centro" ? "center" : "flex-start", paddingTop: 220 }}>
          <div
            style={{
              maxWidth: 940,
              textAlign: "center",
              fontSize: 92,
              fontWeight: 900,
              lineHeight: 1.05,
              textTransform: "uppercase",
              color: insert.destaque ? "#000" : estilo.corTexto,
              background: insert.destaque ? estilo.corPrimaria : "transparent",
              padding: "18px 34px",
              borderRadius: 20,
              textShadow: insert.destaque ? "none" : "0 6px 24px #000c",
              transform: `scale(${entrada}) rotate(${interpolate(entrada, [0, 1], [-4, 0])}deg)`,
            }}
          >
            {insert.texto}
          </div>
        </AbsoluteFill>
      );
    case "emoji":
      return (
        <AbsoluteFill style={{ alignItems: "flex-end", paddingTop: 300, paddingRight: 80 }}>
          <div style={{ fontSize: 220, transform: `scale(${entrada}) rotate(${Math.sin(frame / 5) * 8}deg)` }}>{insert.emoji}</div>
        </AbsoluteFill>
      );
    case "numero": {
      const valor = Math.round(interpolate(frame, [0, Math.min(durationInFrames, fps)], [insert.de, insert.ate], { extrapolateRight: "clamp" }));
      return (
        <AbsoluteFill style={{ alignItems: "center", paddingTop: 260 }}>
          <div style={{ fontSize: 200, fontWeight: 900, color: estilo.corPrimaria, textShadow: "0 8px 30px #000c", transform: `scale(${entrada})` }}>
            {insert.prefixo ?? ""}
            {valor.toLocaleString("pt-BR")}
            {insert.sufixo ?? ""}
          </div>
        </AbsoluteFill>
      );
    }
    case "cta":
      return (
        <AbsoluteFill style={{ alignItems: "center", justifyContent: "flex-end", paddingBottom: 260 }}>
          <div
            style={{
              background: estilo.corPrimaria,
              color: "#000",
              fontSize: 76,
              fontWeight: 900,
              padding: "34px 60px",
              borderRadius: 999,
              boxShadow: "0 16px 50px #0009",
              transform: `translateY(${interpolate(entrada, [0, 1], [300, 0])}px) scale(${1 + Math.sin(frame / 6) * 0.03})`,
            }}
          >
            {insert.texto}
          </div>
          {insert.subtexto ? (
            <div style={{ marginTop: 26, fontSize: 44, fontWeight: 700, color: estilo.corTexto, textShadow: "0 4px 16px #000c", opacity: entrada }}>{insert.subtexto}</div>
          ) : null}
        </AbsoluteFill>
      );
    default:
      return null;
  }
};
