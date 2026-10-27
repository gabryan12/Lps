import { AbsoluteFill, Audio, Sequence, staticFile, useVideoConfig } from "remotion";
import { AnuncioProps } from "./tipos";
import { Base } from "./componentes/Base";
import { InsertLayer } from "./componentes/Inserts";
import { Legendas } from "./componentes/Legendas";

// Ordem das camadas é regra do padrão: base → b-roll → gráficos → CTA → legenda POR ÚLTIMO
export const Anuncio: React.FC<AnuncioProps> = (props) => {
  const { fps } = useVideoConfig();
  const ms = (v: number) => Math.round((v / 1000) * fps);
  const ordem = ["broll", "texto", "numero", "emoji", "cta"] as const;
  const inserts = props.inserts.filter((i) => i.tipo !== "zoom");
  inserts.sort((a, b) => ordem.indexOf(a.tipo as never) - ordem.indexOf(b.tipo as never));

  return (
    <AbsoluteFill style={{ backgroundColor: "#000", fontFamily: props.estilo.fonte }}>
      <Base {...props} />
      {props.audio ? <Audio src={staticFile(props.audio)} /> : null}
      {inserts.map((ins, i) => (
        <Sequence key={i} from={ms(ins.inicioMs)} durationInFrames={Math.max(1, ms(ins.fimMs - ins.inicioMs))} layout="none">
          <InsertLayer insert={ins} estilo={props.estilo} />
        </Sequence>
      ))}
      <Legendas legendas={props.legendas} estilo={props.estilo} />
    </AbsoluteFill>
  );
};
