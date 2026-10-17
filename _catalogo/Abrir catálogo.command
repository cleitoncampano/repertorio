#!/bin/zsh
# Dois cliques neste arquivo abrem o catálogo no navegador.
cd "$(dirname "$0")"
if command -v python3 >/dev/null 2>&1; then exec python3 servidor.py; else exec /usr/bin/python3 servidor.py; fi
