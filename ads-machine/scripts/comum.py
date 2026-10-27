"""Funções compartilhadas pelos scripts do Ads Machine."""
import json
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PROJETOS = RAIZ / "projetos"
TEMPLATE = RAIZ / "template"


def projeto(slug: str) -> Path:
    p = PROJETOS / slug
    p.mkdir(parents=True, exist_ok=True)
    return p


def ler(path: Path, padrao=None):
    if not path.exists():
        return padrao
    return json.loads(path.read_text(encoding="utf-8"))


def salvar(path: Path, dados) -> None:
    path.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")


def rodar(cmd: list[str]) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"Falhou: {' '.join(cmd)}\n{r.stderr[-2000:]}")
    return r.stdout + r.stderr


def sonda(arquivo: Path) -> dict:
    out = rodar(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(arquivo)])
    return json.loads(out[: out.rfind("}") + 1])


def duracao(arquivo: Path) -> float:
    return float(sonda(arquivo)["format"]["duration"])
