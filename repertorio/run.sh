#!/bin/sh
set -eu
REPERTORIO_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
export PYTHONPATH="$REPERTORIO_DIR/server${PYTHONPATH:+:$PYTHONPATH}"
exec "$REPERTORIO_DIR/.venv/bin/python" -m repertorio.cli "${@:-serve}"
