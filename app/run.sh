#!/bin/sh
set -eu
REPERTORIO_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
export PYTHONPATH="$REPERTORIO_DIR/server${PYTHONPATH:+:$PYTHONPATH}"
if [ ! -x "$REPERTORIO_DIR/.venv/bin/python" ]; then echo "Prepare o Repertório antes: ./app/setup.sh" >&2; exit 1; fi
exec "$REPERTORIO_DIR/.venv/bin/python" -m repertorio.cli "${@:-serve}"
