import { createTikTokStyleCaptions } from "@remotion/captions";
import { useMemo } from "react";
import { AbsoluteFill, interpolate, Sequence, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Estilo, Palavra } from "../tipos";

// Legenda estilo TikTok: blocos curtos, palavra falada destacada na cor primária
export const Legendas: React.FC<{ legendas: Palavra[]; estilo: Estilo }> = ({ legendas, estilo }) => {
  const { fps } = useVideoConfig();
  const { pages } = useMemo(
    () => createTikTokStyleCaptions({ captions: legendas, combineTokensWithinMilliseconds: estilo.palavrasPorBloco * 380 }),
    [legendas, estilo.palavrasPorBloco],
  );

  return (
    <AbsoluteFill>
      {pages.map((pagina, i) => {
        const proxima = pages[i + 1]?.startMs ?? pagina.startMs + pagina.durationMs;
        const de = Math.round((pagina.startMs / 1000) * fps);
        const ate = Math.round((proxima / 1000) * fps);
        if (ate <= de) return null;
        return (
          <Sequence key={i} from={de} durationInFrames={ate - de} layout="none">
            <Bloco tokens={pagina.tokens} inicioMs={pagina.startMs} estilo={estilo} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};

const Bloco: React.FC<{ tokens: { text: string; fromMs: number; toMs: number }[]; inicioMs: number; estilo: Estilo }> = ({ tokens, inicioMs, estilo }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const agoraMs = inicioMs + (frame / fps) * 1000;
  const entrada = spring({ frame, fps, config: { damping: 200 }, durationInFrames: 5 });

  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: estilo.legendaPosicao === "meio" ? "center" : "flex-end", paddingBottom: 420, paddingTop: 300 }}>
      <div
        style={{
          maxWidth: 960,
          textAlign: "center",
          fontSize: 88,
          fontWeight: 900,
          textTransform: "uppercase",
          lineHeight: 1.1,
          whiteSpace: "pre-wrap",
          WebkitTextStroke: "14px #000",
          paintOrder: "stroke",
          transform: `scale(${interpolate(entrada, [0, 1], [0.85, 1])})`,
        }}
      >
        {tokens.map((t, i) => {
          const ativo = agoraMs >= t.fromMs && agoraMs < t.toMs;
          return (
            <span key={i} style={{ color: ativo ? estilo.corPrimaria : estilo.corTexto }}>
              {t.text}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
