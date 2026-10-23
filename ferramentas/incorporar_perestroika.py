#!/usr/bin/env python3
"""Atalho para `ferramentas/incorporar_colecao.py perestroika <comando>` (paginas, montar, pranchas, validar)."""
import runpy
import sys
from pathlib import Path

sys.argv = [sys.argv[0], 'perestroika', *sys.argv[1:]]
runpy.run_path(str(Path(__file__).with_name('incorporar_colecao.py')), run_name='__main__')
