#!/bin/sh
# Dois cliques no Finder: na primeira vez, prepara o Repertório; depois liga o serviço e abre o navegador.
# Se o serviço já estiver ligado, só abre a página.
set -eu
REPERTORIO_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if [ ! -x "$REPERTORIO_DIR/.venv/bin/python" ]; then
  echo 'Primeira vez: preparando o Repertório. Leva alguns minutos e precisa de internet.'
  "$REPERTORIO_DIR/setup.sh"
fi
exec "$REPERTORIO_DIR/run.sh" serve --abrir
