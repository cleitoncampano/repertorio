#!/usr/bin/env python3
"""Incorpora o recorte 18 a 49 da Growmate, sem modificar o projeto de origem.

Preparar: app/.venv/bin/python ferramentas/incorporar_growmate_livros.py prepare
Renderizar: node ferramentas/incorporar-growmate-render.cjs
Registrar: app/.venv/bin/python ferramentas/incorporar_growmate_livros.py register
Conferir: app/.venv/bin/python ferramentas/incorporar_growmate_livros.py verify

As mutações do acervo passam pelo MCP; não há escrita direta no SQLite.
"""
import argparse
import asyncio
import hashlib
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path('/Users/cleiton/Documents/Desenvolvimento/growmate/growmate-marketing')
DEST = ROOT / '_originais/growmate-livros'
STUDIES = ROOT / '_referencias/growmate-livros'
MANIFEST = ROOT / 'docs/REPERTORIO-GROWMATE-LIVROS.json'
PROJECT = 'repert-rio-87e17c'
URL = 'http://127.0.0.1:8766'
# Os carrosséis ficam só no espaço Growmate; Inspiração guarda apenas referências externas.
WORKSPACES = ['ff1be998-6589-4e3d-a1f2-e7682406e853']
COLORS = {
    'base': '#0A0A0A', 'papel': '#F5F2EB', 'texto-claro': '#EFEDE6',
    'coral': '#FF4D2E', 'coral-sobre-claro': '#C8321C', 'amarelo-gradiente': '#FFE66B',
}
MOTIFS = [
    ('Círculo Dourado', 'Organizar uma explicação do centro para fora: causa, prática e entrega.'),
    ('Casa, pilares e jornada', 'Fazer uma seta de resultado virar a estrutura dos pilares nas lâminas seguintes.'),
    ('Linha da receita que se divide', 'Dividir uma mesma linha em dois destinos para comparar efeitos de curto e longo prazo.'),
    ('Ciclo e dois laços', 'Usar voltas pequenas e grandes para explicar resposta individual e mudança sistêmica.'),
    ('Caneta vermelha e revisão', 'Mostrar uma política sendo corrigida no próprio documento, com riscos, círculos e anotações.'),
    ('Feed público e conversa', 'Encenar uma conversa para ensinar a resposta, em vez de listar recomendações abstratas.'),
    ('Estrada com lombadas', 'Converter um dado em terreno percorrível; a dificuldade da estrada expressa o esforço.'),
    ('Bumerangue e protocolos', 'Fazer o caminho voltar ao mesmo ponto para tornar o recontato visível.'),
    ('Roteiro revisado e fita métrica', 'Comparar falas riscadas e reescritas e usar uma régua contínua para representar esforço.'),
    ('Voo e rota de avião', 'Estruturar uma história de transformação como decolagem, voo e pouso.'),
    ('Pirâmide que gira', 'Girar a mesma estrutura ao longo das divisas para tornar uma mudança de poder visível.'),
    ('Montanha-russa e quatro elementos', 'Fazer o traçado variar para marcar momentos de elevação, orgulho, conexão e descoberta.'),
    ('Curva de emoção, pico e fim', 'Organizar a sequência pela intensidade e pelo desfecho, usando uma curva contínua.'),
    ('Mapa dobrado em sanfona', 'Tratar cada lâmina como uma dobra de um mapa maior, mantendo rotas e vínculos.'),
    ('Blueprint, palco e bastidor', 'Separar o que a pessoa vê do trabalho interno por uma linha de visibilidade.'),
    ('Estrada e milk-shake', 'Seguir uma história concreta com um objeto recorrente antes de apresentar a teoria.'),
    ('Preto e branco que ganha cor', 'Fazer a cor entrar no momento da mudança da história, dando função narrativa à paleta.'),
    ('Régua de 95% e 5%', 'Usar a própria largura do conjunto para representar uma proporção, com uma quebra final deliberada.'),
    ('Escada de prioridades', 'Organizar públicos em degraus para mostrar a ordem das decisões.'),
    ('Jogo de desempate e prioridades', 'Criar rodadas de decisão que ensinam uma regra de prioridade pela consequência.'),
    ('Chamada e fio de telefone', 'Manter uma chamada em andamento para questionar indicadores de duração do atendimento.'),
    ('Corrente e elos', 'Dar a cada relação causal um elo, tornando visível a dependência entre equipe, cliente e resultado.'),
    ('Contrato e lupa', 'Ampliar trechos de letras miúdas para examinar a experiência produzida por uma regra.'),
    ('Duas linhas que se afastam e cartas', 'Representar a relação pela distância entre linhas e aproximá-las com decisões sucessivas.'),
    ('Prontuário e eletrocardiograma', 'Tratar sinais de retenção como um diagnóstico com ritmo, exames e conduta.'),
    ('Calendário de 100 dias', 'Distribuir pontos de contato no tempo e mostrar os vazios de uma jornada.'),
    ('Pontos e curva de valor', 'Transformar uma fila de pontos iguais em distribuição para explicar diferenças de valor.'),
    ('Placar e diagnóstico', 'Fazer perguntas acumularem um resultado que conduz a uma decisão prática.'),
    ('Escada do café e palco', 'Subir a mesma oferta por níveis de valor e transformar a escada em palco.'),
    ('Terreno e camadas', 'Aprofundar a explicação por estratos e destacar uma camada de cada vez.'),
    ('Iceberg, mergulho e linha de água', 'Mover a linha de água para conduzir uma descida ao problema oculto e uma volta à ação.'),
    ('Estante, lombadas e prateleiras', 'Organizar um acervo por problema do leitor e usar o suporte físico para unir as páginas.'),
]


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def sha(path):
    return hashlib.file_digest(path.open('rb'), 'sha256').hexdigest()


def clean(text):
    return text.replace(chr(0x2014), ',').replace(chr(0x2013), '-')


def section(text, name):
    match = re.search(r'^## ' + name + r'[^\n]*\n(.*?)(?=^## |\Z)', text, re.S | re.M)
    return clean(match.group(1).strip()) if match else ''


def prepare():
    if MANIFEST.exists():
        raise SystemExit('Manifesto já existe. Preserve os IDs; use register ou verify para retomar.')
    from PIL import Image
    folders = sorted(p for p in (SOURCE / 'carrosseis').iterdir()
                     if p.is_dir() and p.name[:2].isdigit() and 18 <= int(p.name[:2]) <= 49)
    assert len(folders) == 32
    kit_source = SOURCE / 'series/livros-kit'
    kit_dest = DEST / 'series/livros-kit'
    for p in kit_source.rglob('*'):
        if p.is_file() and 'bin' not in p.relative_to(kit_source).parts:
            target = kit_dest / p.relative_to(kit_source)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)
    for name in ['livros.md', 'livros-direcao-v2.md']:
        shutil.copy2(SOURCE / 'series' / name, DEST / 'series' / name)
    manifest = dict(created=datetime.now().astimezone().isoformat(), source=str(SOURCE),
                    destination=str(DEST.relative_to(ROOT)), project_id=PROJECT, colors=COLORS,
                    fonts=['Inter Tight', 'Fraunces itálico', 'JetBrains Mono'], entries=[])
    for d, (motif, transfer) in zip(folders, MOTIFS):
        target = DEST / 'carrosseis' / d.name
        inputs = []
        for p in sorted(d.rglob('*')):
            rel = p.relative_to(d)
            if not p.is_file() or any(x in rel.parts for x in ['versoes', 'linkedin', 'tools']):
                continue
            keep = rel.parts[0] == 'assets' or (rel.parts[0] == 'out' and p.suffix in ['.png', '.pdf'])
            keep |= len(rel.parts) == 1 and p.name in {
                'carrossel.html', 'index.html', 'project.md', 'fontes.md', 'legenda.md', 'legenda.txt',
                'texto-alternativo.txt', 'previa.png', 'panorama.png', 'emenda.png', 'export.mjs', 'qa.json',
            }
            if not keep:
                continue
            q = target / rel
            q.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, q)
            inputs.append(dict(path=str(q.relative_to(ROOT)), source=str(p.relative_to(SOURCE)),
                               sha256=sha(q), bytes=q.stat().st_size))
        text = (target / 'project.md').read_text()
        title = clean(text.splitlines()[0].lstrip('# ').replace(' · carrossel Growmate', ''))
        slides = sorted((target / 'out').glob('*.png'))
        assert slides
        with Image.open(slides[0]) as im:
            dimensions = list(im.size)
        concept = section(text, 'Conceito')
        if not concept:
            concept = ('Diagrama central com três níveis, hierarquia tipográfica em sans e itálico, '
                       'fotografias diferentes do autor, linha coral contínua e alternância de fundos.'
                       if d.name.startswith('18') else
                       'Painel de 17 lâminas. A seta de lucro vira telhado dos pilares; a jornada '
                       'continua entre duas lâminas e o símbolo de infinito conecta o fim à capa.')
        raw = sorted(p for p in (target / 'assets').rglob('*')
                     if p.is_file() and p.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp'])
        # A pasta 49 também contém 32 versões redimensionadas dos mesmos recortes.
        originals = [p for p in raw if 'estante' not in p.relative_to(target / 'assets').parts]
        entry = dict(folder=d.name, post=int(d.name[:2]) - 17, title=title,
                     motif=motif, transferable=transfer, concept=concept,
                     narrative=section(text, 'Roteiro'), slides=len(slides), dimensions=dimensions,
                     assets=len(raw), inputs=inputs, path=str(target.relative_to(ROOT)),
                     files=[str(p.relative_to(ROOT)) for p in slides + originals],
                     previews=[str((target / n).relative_to(ROOT))
                               for n in ['previa.png', 'panorama.png', 'emenda.png'] if (target / n).exists()])
        source = (target / 'carrossel.html').read_text()
        entry['source_colors'] = sorted(set(x.upper() for x in re.findall(r'#[0-9a-fA-F]{6}\b', source)))
        study = STUDIES / (d.name + '.md')
        study.parent.mkdir(parents=True, exist_ok=True)
        study.write_text(clean(
            f'# {title}\n\n#Livros, post {entry["post"]:02d}. Pasta de origem: `{d.name}`.\n\n'
            f'## Ideia transferível\n\n{transfer}\n\n## Como foi construído\n\n{concept}\n\n'
            f'## Especificação\n\n{len(slides)} lâminas de {dimensions[0]} × {dimensions[1]} px. '
            f'Base de composição: 1080 × 1350 px, exportação 2x.\n\n'
            'Paleta: `#0A0A0A`, `#F5F2EB`, `#EFEDE6`, `#FF4D2E`, `#C8321C`, `#FFE66B`. '
            'Fontes: Inter Tight, Fraunces itálico e JetBrains Mono.\n\n'
            f'## Roteiro da fonte\n\n{entry["narrative"]}\n\n'
            f'## Arquivos preservados\n\nOriginais e dependências: `{entry["path"]}/`. '
            'Arte em `carrossel.html`, lâminas em `out/`, assets em `assets/`, créditos em `fontes.md`. '
            'A cópia `repertorio-autocontido.html` incorpora as dependências visuais para download no app.\n\n'
            '## Reutilização\n\nEstudo da construção, sem aprovação automática para copiar a peça. '
            'O conjunto mistura criação da Growmate e fotografias de terceiros. '
            'As condições registradas na produção foram preservadas em `fontes.md`; '
            'recortar uma fotografia não altera sua origem. As referências externas não foram revalidadas nesta incorporação.\n'
        ))
        manifest['entries'].append(entry)
    # Ícones independentes extraídos do kit, sem fotografias de autores.
    js = (kit_dest / 'base.js').read_text()
    block = js.split('const icons={', 1)[1].split('\n};', 1)[0]
    icons = dict(re.findall(r"^\s*(\w+):'([^']*)',?\s*$", block, re.M))
    assert len(icons) >= 40
    icon_dir = kit_dest / 'icones'
    icon_dir.mkdir(exist_ok=True)
    for name, markup in icons.items():
        (icon_dir / (name + '.svg')).write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
            'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
            + markup + '</svg>\n')
    manifest['icons'] = len(icons)
    # Consulta visual de componentes existentes; nenhuma peça de marketing nova.
    swatches = ''.join(f'<div class="swatch" style="background:{v};color:{"#0A0A0A" if k in ["papel","texto-claro","amarelo-gradiente"] else "#EFEDE6"}">{k}<br><b>{v}</b></div>' for k, v in COLORS.items())
    gallery = ''.join(f'<div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">{m}</svg><span>{n}</span></div>' for n, m in icons.items())
    (kit_dest / 'repertorio-componentes.html').write_text(
        '<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Growmate: identidade e componentes</title>'
        '<style>*{box-sizing:border-box}body{margin:0;padding:56px;background:#F5F2EB;color:#0A0A0A;font:20px/1.5 system-ui}h1{font-size:48px;letter-spacing:-.04em}h2{margin-top:42px}.colors{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.swatch{padding:28px;border-radius:12px}.icons{display:grid;grid-template-columns:repeat(8,1fr);gap:24px}.icon{display:grid;justify-items:center;font-size:13px;color:#C8321C}.icon svg{width:46px;height:46px}.gradient{height:120px;background:linear-gradient(135deg,#FF4D2E,#FFE66B 60%,#FF4D2E);border-radius:12px}p{max-width:1000px}</style>'
        '<h1>Growmate · #Livros</h1><p>Paleta e ícones extraídos das produções 18 a 49. Identidade fixa, construções próprias por história.</p>'
        '<div class="colors">' + swatches + '</div><h2>Gradiente de destaque</h2><div class="gradient"></div>'
        '<h2>Tipografia da série</h2><p>Inter Tight: títulos e corpo. Fraunces itálico: ênfase editorial. JetBrains Mono: rótulos, numeração e créditos. Arquivos WOFF2 preservados no kit local.</p>'
        '<h2>Ícones do kit</h2><div class="icons">' + gallery + '</div></html>')
    save(MANIFEST, manifest)
    print(json.dumps(dict(carrosseis=len(folders), slides=sum(x['slides'] for x in manifest['entries']),
                          assets=sum(x['assets'] for x in manifest['entries']), icons=len(icons),
                          copied_files=sum(len(x['inputs']) for x in manifest['entries'])), ensure_ascii=False))


def reference_data(entry):
    concept = re.sub(r'\s+', ' ', entry['concept']).replace('**', '')
    return dict(
        title=f'Growmate #Livros {entry["post"]:02d} · {entry["title"]}'[:240],
        description=clean(f'Carrossel de referência da série #Livros. {entry["slides"]} lâminas, '
                          f'{entry["dimensions"][0]} × {entry["dimensions"][1]} px. '
                          f'Construção: {entry["motif"]}. {concept[:3200]} '
                          'Paleta: preto #0A0A0A, papel #F5F2EB, texto #EFEDE6, coral #FF4D2E, '
                          'coral escuro #C8321C e gradiente amarelo #FFE66B. '
                          'Tipografia: Inter Tight, Fraunces itálico e JetBrains Mono.'),
        idea=clean(entry['transferable']),
        techniques=['contraste-de-cor', 'hierarquia-de-leitura', 'conexao', 'linha-guia',
                    'metafora-visual', 'camera-continua', 'profundidade-em-camadas'],
        intentions=['ABRIR', 'EXPLICAR', 'SEQUENCIAR', 'FECHAR'], movements=['panorama'],
        aesthetics=['editorial', 'alto-contraste', 'colagem'], strength=4, reusable=False,
        source_reference_ids=[],
        usage_notes=clean('Pedido explícito de Cleiton em 17/10/2026. Incorporado como repertório de '
                         'construção, sem aprovar uma reprodução futura. A criação Growmate convive '
                         'com fotografias e recortes de terceiros; conservar os créditos e as condições '
                         f'originais de {entry["path"]}/fontes.md. '
                         f'Estudo: _referencias/growmate-livros/{entry["folder"]}.md. '
                         'As prévias começam nas lâminas em ordem; depois mostram assets e pranchas. '
                         'HTML autocontido, PNGs e imagens-fonte estão anexados como originais. '
                         'Ícones, fontes locais e edição original também foram preservados no kit local. '
                         'Em futuras criações, dizer ao usuário quais referências vai usar e por quê.'),
    )


async def mcp_work(mode):
    import httpx
    from mcp import ClientSession
    from mcp.client.streamable_http import streamable_http_client
    manifest = json.loads(MANIFEST.read_text())

    async with streamable_http_client(URL + '/mcp') as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            async def call(name, args):
                result = await session.call_tool(name, args)
                if result.isError:
                    raise RuntimeError(str(result.content)[:1800])
                if result.structuredContent:
                    return result.structuredContent
                return json.loads(next(x.text for x in result.content if x.type == 'text'))

            if mode == 'register':
                if not manifest.get('context_id'):
                    context = await call('start_context', dict(project_id=PROJECT, workspace_ids=WORKSPACES, demand=
                        'Incorporar por pedido explícito do usuário os 32 carrosséis Growmate da pasta '
                        '18 (Simon Sinek) à 49, com lâminas, assets, cores, tipografia, créditos e '
                        'construção narrativa para servir de repertório neste projeto.'))
                    manifest['context_id'] = context['id']
                    save(MANIFEST, manifest)
                for entry in manifest['entries']:
                    html = str(Path(entry['path']) / 'repertorio-autocontido.html')
                    assert (ROOT / html).is_file()
                    files = [html] + entry['files']
                    assert len(files) <= 60
                    op = await call('register_reference', dict(request=dict(
                        context_id=manifest['context_id'], target_workspace_ids=WORKSPACES, request_key='growmate-livros-20261017-' + entry['folder'],
                        user_requested=True, files=files, previews=entry['previews'], data=reference_data(entry))))
                    entry['operation_id'] = op['id']
                    entry['reference_id'] = op['ref_id']
                    entry['url'] = URL + '/?workspace=' + WORKSPACES[0] + '&ref=' + op['ref_id']
                    save(MANIFEST, manifest)
                    print(entry['folder'], op['state'], flush=True)
                kit_path = DEST / 'series/livros-kit'
                kit_data = dict(
                    title='Growmate #Livros · Paleta, ícones e construção',
                    description=f'Componentes gráficos da Growmate sem fotografias: seis cores, gradiente '
                                f'coral-amarelo e {manifest["icons"]} ícones em SVG. '
                                'Base 1080 × 1350 px e saída 2160 × 2700. Inter Tight para títulos e corpo, '
                                'Fraunces itálico para destaque e JetBrains Mono para rótulos. '
                                'As fontes e o código do motor foram preservados no kit local. '
                                'Cores: #0A0A0A, #F5F2EB, #EFEDE6, #FF4D2E, #C8321C e #FFE66B.',
                    idea='Manter identidade de cores e tipos, deixando cada história definir a metáfora, '
                         'a estrutura e o número de lâminas. Usar um panorama e um fio próprio para conectar as partes.',
                    techniques=['contraste-de-cor', 'hierarquia-de-leitura', 'conexao', 'linha-guia', 'metafora-visual'],
                    intentions=['EXPLICAR', 'AGRUPAR'], movements=['estatico'],
                    aesthetics=['editorial', 'alto-contraste'], strength=4, reusable=True,
                    source_reference_ids=[],
                    usage_notes='Componentes gráficos internos Growmate, incorporados a pedido do titular do '
                                'projeto para uso neste trabalho. Esta ficha não inclui fotos de autores. '
                                'Ícones vetoriais individuais e CSS original em '
                                '_originais/growmate-livros/series/livros-kit/. '
                                'A indicação de reutilização vale para os componentes gráficos desta ficha; '
                                'não concede licença sobre as fotografias dos outros carrosséis. '
                                'Fontes WOFF2 guardadas como dependência da produção, sem nova auditoria de licença.',
                )
                kit = await call('register_reference', dict(request=dict(
                    context_id=manifest['context_id'], target_workspace_ids=WORKSPACES, request_key='growmate-livros-20261017-componentes',
                    user_requested=True, data=kit_data,
                    files=[str((kit_path / 'repertorio-componentes.html').relative_to(ROOT))],
                    previews=[str((kit_path / 'repertorio-componentes.png').relative_to(ROOT))])))
                manifest['kit'] = dict(reference_id=kit['ref_id'], operation_id=kit['id'], url=URL + '/?workspace=' + WORKSPACES[0] + '&ref=' + kit['ref_id'])
                save(MANIFEST, manifest)
            else:
                entries = manifest['entries'] + [manifest['kit']]
                report = []
                for entry in entries:
                    op = await call('get_operation', dict(operation_id=entry['operation_id']))
                    for _ in range(200):
                        if op['state'] not in ['queued', 'running']:
                            break
                        await asyncio.sleep(3)
                        op = await call('get_operation', dict(operation_id=entry['operation_id']))
                    ref = await call('get_reference', dict(reference_id=entry['reference_id'], include_image=False, workspace_ids=WORKSPACES))
                    assert op['state'] == 'completed', (entry.get('folder'), op)
                    assert ref['ready'] and ref['state'] == 'published'
                    assert not any(a['missing'] for a in ref['assets'])
                    report.append(dict(reference_id=ref['id'], title=ref['title'], state=op['state'],
                                       originals=sum(a['role'] == 'original' for a in ref['assets']),
                                       previews=sum(a['role'] == 'preview' for a in ref['assets'])))
                    print('Conferido:', ref['title'], flush=True)
                async with httpx.AsyncClient(base_url=URL) as client:
                    r = await client.post('/api/search', json=dict(query='Growmate #Livros', limit=100))
                    r.raise_for_status()
                    found = {x['id'] for x in r.json()['items']}
                    assert {x['reference_id'] for x in entries} <= found
                    original = next(a for a in ref['assets'] if a['role'] == 'original')
                    download = await client.get(original['url'])
                    download.raise_for_status()
                    assert len(download.content) > 1000
                # Conferência completa da cópia, inclusive imagens que não entraram no app.
                for e in manifest['entries']:
                    for item in e['inputs']:
                        assert sha(ROOT / item['path']) == item['sha256'], item['path']
                manifest['verification'] = dict(timestamp=datetime.now().astimezone().isoformat(),
                    complete=True, references=report, source_hashes_verified=True, searchable=True)
                save(MANIFEST, manifest)
                write_index(manifest)
                print(json.dumps(dict(references=len(report), published=len(report),
                    slides=sum(x['slides'] for x in manifest['entries']), search='ok', hashes='ok'), ensure_ascii=False))


def write_index(m):
    lines = ['# Repertório Growmate: série #Livros', '',
             'Incorporado a pedido de Cleiton em 17/10/2026. Origem: '
             '`growmate/growmate-marketing/carrosseis/18-comece-pelo-porque/` '
             'até `49-biblioteca-do-gerente-de-cx/`. Versões atuais; históricos de `versoes/` ficaram de fora.', '',
             f'**32 carrosséis, {sum(x["slides"] for x in m["entries"])} lâminas, '
             f'{sum(x["assets"] for x in m["entries"])} arquivos de imagem em assets e {m["icons"]} ícones SVG.** '
             'A contagem de assets inclui variantes, recortes, logos e fotografias repetidas entre produções.', '',
             f'[Abrir os 33 registros no grafo]({URL}/?q=Growmate). A busca aproxima e enquadra o conjunto; '
             'se o app já estava aberto antes desta atualização, recarregar com ⌘R.', '',
             f'[Abrir paleta e componentes no Repertório]({m["kit"]["url"]}).', '',
             '## Identidade preservada', '',
             '| Papel | Cor |', '|---|---|']
    lines.extend(f'| {k} | `{v}` |' for k, v in COLORS.items())
    lines += ['', 'Inter Tight: títulos e corpo. Fraunces itálico: destaque editorial. '
              'JetBrains Mono: rótulos, numeração e créditos. Gradiente: '
              '`linear-gradient(135deg,#FF4D2E 0%,#FFE66B 60%,#FF4D2E 100%)`.', '',
              '## Como reconstruir as ideias', '',
              'O kit fixa a identidade. Cada história define uma estrutura e um objeto contínuo próprio. '
              'A produção usa um panorama HTML de largura `N * 1080` e altura `1350`; cada lâmina '
              'ocupa um trecho do panorama. CSS posiciona o texto; SVG desenha diagramas, trilhas e '
              'metáforas; PNG com transparência sobrepõe autores e elementos. `bridge`, `over` e '
              '`frente` separam as camadas. `clipPath` adapta a cor das linhas ao fundo de cada lâmina.', '',
              'Nos posts da direção v2, a última divisa deve encaixar na primeira. O kit registra '
              'margens x 72 a 1008, conteúdo y 150 a 1262, corpo mínimo de 26 px e rodapé em y 1290. '
              'Essas são especificações da produção de origem, não um molde obrigatório para novos materiais.', '',
              'Inspire-se na função da metáfora e na sequência, recriando-as para a nova história. '
              'Antes de criar com o acervo, dizer ao usuário quais referências vai usar e por quê.', '',
              '## Catálogo', '', '| Post | Carrossel e ficha no app | Construção | Estudo local |', '|---|---|---|---|']
    for e in m['entries']:
        lines.append(f'| {e["post"]:02d} | [{e["title"]}]({e["url"]}) | {e["motif"]} '
                     f'({e["slides"]} lâminas) | [Como foi feito]({e["folder"]}.md) |')
        p = STUDIES / (e['folder'] + '.md')
        text = p.read_text()
        if '\nFicha no app:' not in text:
            p.write_text(text + f'\nFicha no app: [{e["title"]}]({e["url"]}).\n')
    lines += ['', '## Arquivos e direitos de uso', '',
              'Originais e dependências: `_originais/growmate-livros/`. Kit compartilhado: '
              '`_originais/growmate-livros/series/livros-kit/`; os SVGs individuais estão em `icones/`. '
              'O manifesto `docs/REPERTORIO-GROWMATE-LIVROS.json` registra caminhos, SHA-256, '
              'contagens, IDs e resultado da conferência. Os originais binários seguem fora do Git.', '',
              'Cada ficha do app tem as lâminas em ordem, os assets de imagem anexados, '
              'as pranchas de origem e uma cópia HTML autocontida com CSS, fontes, SVG e imagens. '
              'A cópia editável original e o kit também estão preservados localmente. '
              'As 32 variantes reduzidas da estante do post 32 estão no HTML e na cópia local; '
              'o app recebe seus recortes-fonte para respeitar o limite de 60 arquivos por envio.', '',
              'Os carrosséis completos estão marcados como referência com mídia de terceiros. '
              'A ficha de componentes está separada e não inclui fotografias. '
              'Créditos e condições declaradas na produção estão nos `fontes.md` preservados; '
              'não houve nova verificação das licenças ou das afirmações dos livros. '
              'Não transportar fotos de terceiros para um novo material apenas porque estão neste acervo.', '',
              'O pedido foi de incorporação ao repertório. Não foi criada nova peça de marketing '
              'nem feita qualquer publicação social.', '']
    (STUDIES / 'README.md').write_text(clean('\n'.join(lines)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['prepare', 'register', 'verify'])
    mode = parser.parse_args().mode
    if mode == 'prepare':
        prepare()
    else:
        asyncio.run(mcp_work(mode))
