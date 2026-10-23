#!/usr/bin/env python3
"""Consulta o MCP do Repertório só para leitura: nada é gravado no acervo (sem contexto, sem demanda, sem escolhas).

Serve aos testes às cegas e a agentes sem o MCP conectado. As imagens (prancha da busca, prévia da ficha) são salvas
numa pasta e o caminho sai na resposta: abra com a ferramenta de leitura de arquivos.

  app/.venv/bin/python -I ferramentas/mcp_leitura.py list_workspaces
  app/.venv/bin/python -I ferramentas/mcp_leitura.py get_guide                      (lista os guias)
  app/.venv/bin/python -I ferramentas/mcp_leitura.py get_guide '{"name":"metodo-soap"}'
  app/.venv/bin/python -I ferramentas/mcp_leitura.py search_references '{"query":"abertura com impacto","workspace_ids":["ID"]}'
  app/.venv/bin/python -I ferramentas/mcp_leitura.py get_reference '{"reference_id":"ID","include_image":true,"workspace_ids":["ID"]}'

Opções: --imagens PASTA (padrão: pasta temporária do sistema) e --url (padrão: http://127.0.0.1:8766/mcp).
"""
import argparse
import asyncio
import base64
import json
import tempfile
import time
from pathlib import Path

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

TOOLS = ('list_workspaces', 'get_guide', 'search_references', 'get_reference')


async def call(url, tool, args):
    async with streamablehttp_client(url) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            return await session.call_tool(tool, args)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('tool', choices=TOOLS)
    parser.add_argument('args', nargs='?', default='{}')
    parser.add_argument('--imagens', default=str(Path(tempfile.gettempdir()) / 'repertorio-mcp-leitura'))
    parser.add_argument('--url', default='http://127.0.0.1:8766/mcp')
    opts = parser.parse_args()
    args = json.loads(opts.args)
    # Leitura pura: context_id registraria a demanda no acervo.
    args.pop('context_id', None)
    if opts.tool == 'search_references':
        request = args.get('request', args)
        request.pop('context_id', None)
        args = {'request': request}
    result = asyncio.run(call(opts.url, opts.tool, args))
    folder = Path(opts.imagens)
    stamp = time.strftime('%H%M%S')
    texts = []
    for item in result.content:
        if item.type == 'text':
            try:
                texts.append(json.loads(item.text))
            except json.JSONDecodeError:
                texts.append(item.text)
    # Uma lista chega como um texto por item: junta de volta.
    for text in ([texts] if len(texts) > 1 else texts):
        print(text if isinstance(text, str) else json.dumps(text, ensure_ascii=False, indent=1))
    for i, item in enumerate(result.content):
        if item.type == 'image':
            folder.mkdir(parents=True, exist_ok=True)
            path = folder / f'{opts.tool}-{stamp}-{i}.jpg'
            path.write_bytes(base64.b64decode(item.data))
            print(f'imagem: {path}')
    if result.isError:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
