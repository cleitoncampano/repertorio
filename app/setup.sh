#!/bin/sh
set -eu
REPERTORIO_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$REPERTORIO_DIR"
command -v uv >/dev/null 2>&1 || { echo 'Instale uv antes de continuar: https://docs.astral.sh/uv/'; exit 1; }
command -v pnpm >/dev/null 2>&1 || { echo 'Instale pnpm e Node.js 22.12 ou superior antes de continuar.'; exit 1; }
if [ ! -x .venv/bin/python ]; then uv venv .venv --python 3.12; fi
uv pip sync --python .venv/bin/python requirements.lock
(cd web && CI=true pnpm install --frozen-lockfile && pnpm build)
./run.sh import
echo 'Repertório pronto. Execute ./app/run.sh serve a partir da raiz e abra http://127.0.0.1:8766.'
