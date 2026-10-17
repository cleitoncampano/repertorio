#!/usr/bin/env python3
"""Serve o catálogo em http://127.0.0.1:8765 e abre os arquivos originais no Mac.

Só aceita pedidos vindos da própria página do catálogo e só abre arquivos
que estão em _originais/pptx e _originais/canva, na pasta dos materiais.
"""
import http.server
import json
import os
import socket
import subprocess
import sys
import threading
import webbrowser

PORTA = 8765
AQUI = os.path.dirname(os.path.abspath(__file__))
MATERIAIS = os.path.dirname(AQUI)
ENDERECO = 'http://127.0.0.1:%d/' % PORTA


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=AQUI, **k)

    def log_message(self, *a):
        pass

    def do_POST(self):
        if self.path != '/abrir' or self.headers.get('X-Catalogo') != '1':
            return self.send_error(403)
        try:
            pedido = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))))
            nome = pedido['arq']
        except (ValueError, KeyError):
            return self.send_error(400)
        pasta = 'canva' if nome.lower().endswith('.pdf') else 'pptx'
        caminho = os.path.join(MATERIAIS, '_originais', pasta, nome)
        if os.path.basename(nome) != nome or not nome.lower().endswith(('.pptx', '.pdf')) or not os.path.isfile(caminho):
            return self.send_error(404)
        subprocess.run(['open', '-R', caminho] if pedido.get('finder') else ['open', caminho])
        self.send_response(204)
        self.end_headers()


def porta_em_uso():
    with socket.socket() as s:
        return s.connect_ex(('127.0.0.1', PORTA)) == 0


if __name__ == '__main__':
    if len(sys.argv) > 1:  # ex.: python3 servidor.py mapa/  abre direto o mapa
        ENDERECO = ENDERECO + sys.argv[1].lstrip('/')
    if porta_em_uso():
        webbrowser.open(ENDERECO)
        sys.exit(0)
    servidor = http.server.ThreadingHTTPServer(('127.0.0.1', PORTA), Handler)
    threading.Timer(0.6, lambda: webbrowser.open(ENDERECO)).start()
    print('Catálogo aberto em %s' % ENDERECO)
    print('Deixe esta janela aberta enquanto usa o catálogo. Para encerrar, feche a janela.')
    servidor.serve_forever()
