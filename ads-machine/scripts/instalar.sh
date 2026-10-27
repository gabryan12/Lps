#!/usr/bin/env bash
# Instala tudo que o Ads Machine precisa. Só ferramentas gratuitas.
set -euo pipefail
cd "$(dirname "$0")/.."

command -v ffmpeg >/dev/null || { echo "Instale o ffmpeg (https://ffmpeg.org/download.html)"; exit 1; }
command -v node >/dev/null || { echo "Instale o Node.js 20+ (https://nodejs.org)"; exit 1; }

[ -d .venv ] || python3 -m venv .venv
.venv/bin/pip install -q -r scripts/requirements.txt
(cd template && npm install --no-audit --no-fund)
echo "Ads Machine pronto."
