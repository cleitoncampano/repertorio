#!/bin/sh
set -eu
REPERTORIO_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if curl --silent --fail http://127.0.0.1:8766/api/health >/dev/null; then
  open http://127.0.0.1:8766
  exit 0
fi
(sleep 2; open http://127.0.0.1:8766) &
exec "$REPERTORIO_DIR/run.sh" serve
