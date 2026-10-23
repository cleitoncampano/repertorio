#!/bin/sh
set -eu
REPERTORIO_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$REPERTORIO_DIR"
command -v uv >/dev/null 2>&1 || { echo 'Instale uv antes de continuar: https://docs.astral.sh/uv/'; exit 1; }
if [ ! -x .venv/bin/python ]; then uv venv .venv --python 3.12; fi
# Na cópia de desenvolvimento (com Git) entram também testes e ferramentas; o pacote do cliente leva só o necessário.
LOCK=requirements.lock
if [ -d ../.git ]; then LOCK=requirements-dev.lock; fi
uv pip sync --python .venv/bin/python "$LOCK"
if [ ! -f web/dist/index.html ]; then
  command -v pnpm >/dev/null 2>&1 || { echo 'Instale pnpm e Node.js 22.12 ou superior para compilar a interface.'; exit 1; }
  (cd web && CI=true pnpm install --frozen-lockfile && pnpm build)
fi
./run.sh init
echo 'Repertório pronto. Execute ./app/run.sh serve a partir da raiz e abra http://127.0.0.1:8766.'
