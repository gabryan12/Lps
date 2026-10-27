import { AbsoluteFill, interpolate, OffthreadVideo, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { AnuncioProps } from "../tipos";

// Vídeo cortado (com zooms de ênfase) ou, sem vídeo, um fundo animado "faceless"
export const Base: React.FC<AnuncioProps> = ({ video, inserts, estilo }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const agoraMs = (frame / fps) * 1000;

  const zoom = inserts.find((i) => i.tipo === "zoom" && agoraMs >= i.inicioMs && agoraMs < i.fimMs);
  let escala = 1;
  if (zoom && zoom.tipo === "zoom") {
    const entrada = spring({ frame: frame - Math.round((zoom.inicioMs / 1000) * fps), fps, config: { damping: 200 }, durationInFrames: 8 });
    escala = interpolate(entrada, [0, 1], [1, zoom.escala ?? 1.15]);
  }

  if (video) {
    return (
      <AbsoluteFill style={{ transform: `scale(${escala})` }}>
        <OffthreadVideo src={staticFile(video)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      </AbsoluteFill>
    );
  }

  const [c1, c2] = estilo.corFundo;
  const angulo = interpolate(frame, [0, fps * 20], [135, 225]);
  const pulso = 1 + Math.sin(frame / 20) * 0.04;
  return (
    <AbsoluteFill style={{ background: `linear-gradient(${angulo}deg, ${c1}, ${c2})`, transform: `scale(${escala})` }}>
      <div
        style={{
          position: "absolute",
          width: 900,
          height: 900,
          left: 90,
          top: 500,
          borderRadius: "50%",
          background: `radial-gradient(circle, ${estilo.corPrimaria}33, transparent 70%)`,
          transform: `scale(${pulso})`,
        }}
      />
    </AbsoluteFill>
  );
};
