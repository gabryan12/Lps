import { Composition } from "remotion";
import { Anuncio } from "./Anuncio";
import { AnuncioProps, PROPS_PADRAO } from "./tipos";

export const RemotionRoot: React.FC = () => (
  <Composition
    id="Anuncio"
    component={Anuncio}
    defaultProps={PROPS_PADRAO}
    // Duração, fps e tamanho vêm do props.json do anúncio
    calculateMetadata={({ props }: { props: AnuncioProps }) => ({
      durationInFrames: Math.max(1, Math.ceil((props.duracaoMs / 1000) * props.fps)),
      fps: props.fps,
      width: props.largura,
      height: props.altura,
    })}
    durationInFrames={180}
    fps={30}
    width={1080}
    height={1920}
  />
);
