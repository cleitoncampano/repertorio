#!/usr/bin/env python3
"""Transforma uma apresentação HTML num arquivo único: embute motor.css, motor.js, outras folhas e scripts locais,
e (com --imagens) as imagens, vídeos curtos, fontes locais e fontes do Google Fonts como data URI (funciona sem internet).
Uso: python3 -I ferramentas/embutir.py apresentacao.html [--imagens] [-o saida.html]
"""
import argparse
import base64
import mimetypes
import os
import re


def ler(base, src):
    caminho = os.path.normpath(os.path.join(base, src))
    return caminho if os.path.isfile(caminho) else None


def data_uri(caminho):
    tipo = mimetypes.guess_type(caminho)[0] or 'application/octet-stream'
    return 'data:%s;base64,%s' % (tipo, base64.b64encode(open(caminho, 'rb').read()).decode())


def local(src):
    return not re.match(r'^(https?:|data:|//|#)', src)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('html')
    ap.add_argument('--imagens', action='store_true')
    ap.add_argument('-o')
    a = ap.parse_args()
    base = os.path.dirname(os.path.abspath(a.html))
    s = open(a.html, encoding='utf8').read()

    def css(m):
        href = m.group(1)
        c = ler(base, href) if local(href) else None
        if not c:
            return m.group(0)
        txt = open(c, encoding='utf8').read()
        if a.imagens:
            pasta = os.path.dirname(c)
            txt = re.sub(r'url\((["\']?)([^)"\']+)\1\)', lambda u: 'url(%s)' % (data_uri(ler(pasta, u.group(2))) if local(u.group(2)) and ler(pasta, u.group(2)) else u.group(2)), txt)
        return '<style>\n%s\n</style>' % txt
    def google(m):
        href = m.group(1).replace('&amp;', '&')
        try:
            import urllib.request
            ua = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'}
            txt = urllib.request.urlopen(urllib.request.Request(href, headers=ua), timeout=60).read().decode()
            def fonte(u):
                dado = urllib.request.urlopen(urllib.request.Request(u.group(1), headers=ua), timeout=60).read()
                return 'url(data:font/woff2;base64,%s)' % base64.b64encode(dado).decode()
            return '<style>\n%s\n</style>' % re.sub(r'url\((https://fonts\.gstatic\.com[^)]+)\)', fonte, txt)
        except Exception as ex:
            print('aviso: não consegui embutir', href, ex)
            return m.group(0)
    if a.imagens:
        s = re.sub(r'<link[^>]+href=["\'](https://fonts\.googleapis\.com/css2?[^"\']+)["\'][^>]*>', google, s)
    s = re.sub(r'<link[^>]+rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)["\'][^>]*>', css, s)
    s = re.sub(r'<link[^>]+href=["\']([^"\']+)["\'][^>]*rel=["\']stylesheet["\'][^>]*>', css, s)

    def js(m):
        src = m.group(1)
        c = ler(base, src) if local(src) else None
        return '<script>\n%s\n</script>' % open(c, encoding='utf8').read() if c else m.group(0)
    s = re.sub(r'<script[^>]+src=["\']([^"\']+)["\'][^>]*>\s*</script>', js, s)

    if a.imagens:
        def attr(m):
            src = m.group(2)
            c = ler(base, src) if local(src) else None
            return '%s="%s"' % (m.group(1), data_uri(c)) if c else m.group(0)
        s = re.sub(r'\b(src|poster)="([^"]+)"', attr, s)
        s = re.sub(r'url\((["\']?)([^)"\']+)\1\)', lambda u: 'url(%s)' % (data_uri(ler(base, u.group(2))) if local(u.group(2)) and ler(base, u.group(2)) else u.group(2)), s)

    saida = a.o or re.sub(r'\.html?$', '', a.html) + '.unico.html'
    open(saida, 'w', encoding='utf8').write(s)
    print(saida, '%.1f MB' % (os.path.getsize(saida) / 1e6))


if __name__ == '__main__':
    main()
