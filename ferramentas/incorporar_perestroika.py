#!/usr/bin/env python3
"""Espaço Perestroika: monta as fichas visuais a partir da leitura página por página dos PDFs.

Leitura (feita por agentes, instruções em perestroika/_trabalho/INSTRUCOES-LEITURA.md):
  perestroika/_trabalho/leitura/<slug>.jsonl  uma linha por página, com a ficha das páginas selecionadas
  perestroika/_trabalho/leitura/<slug>.md     resumo do PDF, com a ficha do deck em JSON

Montar: app/.venv/bin/python -I ferramentas/incorporar_perestroika.py montar
  grava dados/perestroika/decks.jsonl (PDF = apresentação, página selecionada = slide), copia as páginas para
  _originais/perestroika/paginas/, prepara o vídeo do Chora PPT em dados/perestroika/motion/ e os estudos em
  _referencias/perestroika/.
Conferir: app/.venv/bin/python -I ferramentas/incorporar_perestroika.py pranchas  (pranchas em app/.runtime/qa/perestroika/)
Importar: ./app/run.sh import-decks --workspace ID --folder dados/perestroika
          ./app/run.sh import-motion --workspace ID --folder dados/perestroika/motion

Material de terceiros: entra com reusable=false, só como referência; a pasta perestroika/ fica fora do Git e dos pacotes.
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'perestroika/_trabalho'
OUT = ROOT / 'dados/perestroika'
MEDIA = ROOT / '_originais/perestroika'
STUDIES = ROOT / '_referencias/perestroika'
VIDEO = 'perestroika/chora_ppt_e_storytelling/ChoraPPT_Hero_Video_Slides.mp4'
COURSE = 'https://perestroika.com.br/cursos/chora-ppt/'
DASHES = (chr(0x2014), chr(0x2013))
# Nome da apresentação no mapa; o título que a leitura deu ao deck fica na descrição.
TITLES = {
    '01-contextualizacao': 'Experience Learning 1 · Contextualização', '02-experience-learning': 'Experience Learning 2 · O método',
    '03-conteudo': 'Experience Learning 3 · Metodologia de Conteúdo', '04-forma': 'Experience Learning 4 · Metodologia de Forma',
    '05-emocional': 'Experience Learning 5 · Metodologia Emocional', '06-estrutural': 'Experience Learning 6 · Metodologia Estrutural',
    '07-como-surgiu': 'Experience Learning 7 · Como surgiu', '08-contexto-mundial': 'Experience Learning 8 · Contexto mundial',
    'checklist-completo-apresentacoes-poderosas': 'Checklist Apresentações Poderosas', 'mapa-do-storytelling': 'Mapa do Storytelling em 8 cartas',
    'chorappt-curso-completo-sp': 'Chora PPT · Programa do curso', 'chorappt-edicao-historica-2012': 'Chora PPT · Edição de 2012',
    'liga-os-pontos-rio': 'Liga os Pontos · Antropologia do consumo', 'mood-pesquisa-tendencias-rio': 'Mood · Pesquisa de tendências',
    'swag-criatividade-poa': 'Swag · Curso de skate para meninas', 'tetris-inovacao-e-solucoes-bsb': 'Tetris · Pesquisa e comportamento',
    'yakuza-rio': 'Yakuza · Processos e referências criativas', 'sputnik-educacao-corporativa': 'Sputnik · Educação corporativa',
    'schole-aprendizagem': 'Scholé · Nova educação', 'branding-cwb': 'Branding · Curso com a Farm (Curitiba)',
    'print-me-bh': 'Print.me · Estamparia (Belo Horizonte)', 'print-me-design-grafico-poa': 'Print.me · Estamparia e portfólio (Porto Alegre)', 'perestroika-catalogo-cursos-incompany': 'Peres In Company · Catálogo de cursos',
}


def clean(value):
    if isinstance(value, str):
        for dash in DASHES:
            value = value.replace(dash, ',' if dash == DASHES[0] else '-')
        return re.sub(r'\s+', ' ', value).strip()
    if isinstance(value, list):
        return [clean(v) for v in value]
    return value


def sources():
    """slug -> caminho do PDF, pelo mesmo nome usado na renderização das páginas."""
    import unicodedata
    found = {}
    for p in sorted((ROOT / 'perestroika').rglob('*.pdf')):
        if '_trabalho' in p.parts:
            continue
        s = unicodedata.normalize('NFD', p.stem).encode('ascii', 'ignore').decode().lower()
        found[re.sub(r'[^a-z0-9]+', '-', s).strip('-')] = p.relative_to(ROOT)
    return found


def vocabulary():
    v = json.loads((ROOT / 'dados/vocabulario.json').read_text())
    ids = lambda k: {i['id'] if isinstance(i, dict) else i for i in v[k]['itens']}
    return dict(intencoes=ids('intencoes'), tecnicas=ids('tecnicas'), movimento=ids('movimentos'),
                estetica=ids('esteticas'), tom=ids('tons'))


def deck_card(md):
    """A ficha do deck é o bloco JSON com `capa` no resumo do PDF."""
    for block in re.findall(r'```(?:json)?\s*(\{.*?\})\s*```', md, re.S) + re.findall(r'(\{[^{}]*"capa"[^{}]*\})', md, re.S):
        try:
            card = json.loads(block)
        except json.JSONDecodeError:
            continue
        if 'capa' in card and 'titulo' in card:
            return card
    raise ValueError('ficha do deck não encontrada')


def concepts(items):
    return sorted({c.split(':', 1)[-1] for c in items or [] if c})


def card(f, vocab, problems, where):
    out = {}
    for key, field, limit in (('intencoes', 'intentions', 3), ('tecnicas', 'techniques', 5), ('movimento', 'movements', 2),
                              ('estetica', 'aesthetics', 5), ('tom', 'tone', 3)):
        values = [x for x in f.get(key) or [] if x in vocab[key]]
        problems += [f'{where}: {key} desconhecido {x}' for x in f.get(key) or [] if x not in vocab[key]]
        out[field] = values[:limit]
    out['movements'] = out['movements'] or ['estatico']
    return dict(title=clean(f['titulo']), description=clean(f.get('resumo', '')), idea=clean(f.get('ideia', '')),
                how=clean(f.get('como_funciona', '')), good_for=clean(f.get('bom_para') or []),
                strength=max(1, min(5, int(f.get('forca') or 3))), **out)


def montar():
    vocab, pdfs, problems = vocabulary(), sources(), []
    decks, slides = [], []
    for jl in sorted((WORK / 'leitura').glob('*.jsonl')):
        slug = jl.stem
        pages = [json.loads(line) for line in jl.read_text().splitlines() if line.strip()]
        md = (WORK / 'leitura' / f'{slug}.md').read_text()
        total = len(list((WORK / 'paginas' / slug).glob('p[0-9][0-9][0-9].jpg')))
        if len(pages) != total:
            problems.append(f'{slug}: {len(pages)} linhas para {total} páginas')
        STUDIES.mkdir(parents=True, exist_ok=True)
        (STUDIES / f'{slug}.md').write_text(md)
        deck_id = f'perestroika-{slug}'
        chosen = [p for p in pages if p.get('selecionar') and p.get('ficha')]
        if not chosen:
            # Cópia de outro deck (Mood SP) ou só divulgação: fica no estudo, fora do mapa.
            problems.append(f'{slug}: nenhuma página escolhida, fica fora do espaço')
            continue
        meta = deck_card(md)
        cover = int(meta.get('capa') or (chosen[0]['pagina'] if chosen else 1))
        dest = MEDIA / 'paginas' / slug
        dest.mkdir(parents=True, exist_ok=True)
        for n in {cover, *(p['pagina'] for p in chosen)}:
            src = WORK / 'paginas' / slug / f'p{n:03d}.jpg'
            if not (dest / src.name).exists():
                shutil.copy2(src, dest / src.name)
        rel = lambda n: str((dest / f'p{n:03d}.jpg').relative_to(ROOT))
        base = dict(collection='perestroika', file=str(pdfs[slug]))
        deck = dict(base, doc='arquivo', id=deck_id, preview=rel(cover), original=str(pdfs[slug]), pages=len(pages),
                    concepts=concepts(c for p in pages for c in p.get('conceitos') or []),
                    keywords=f'perestroika {slug.replace("-", " ")}', **card(meta, vocab, problems, slug))
        deck['description'] = clean(f"{deck['title']}. {deck['description']} PDF da Perestroika com {len(pages)} páginas; {len(chosen)} estão no espaço como slides.")
        deck['title'] = 'Perestroika · ' + TITLES.get(slug, deck['title'])
        decks.append(deck)
        for p in chosen:
            n = p['pagina']
            slides.append(dict(base, doc='slide', id=f'{deck_id}#{n}', deck=deck_id, n=n, page=n, preview=rel(n),
                               text=clean(p.get('texto', '')), concepts=concepts(p.get('conceitos')),
                               keywords='perestroika', **card(p['ficha'], vocab, problems, f'{slug} p{n}')))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'decks.jsonl').write_text(''.join(json.dumps(d, ensure_ascii=False) + '\n' for d in decks + slides))
    video()
    print(json.dumps(dict(apresentacoes=len(decks), slides=len(slides), avisos=len(problems)), ensure_ascii=False))
    for line in problems:
        print('aviso:', line)


def video():
    """O vídeo do curso Chora PPT entra como os do Motion: capa, prancha de oito quadros, loop curto e vídeo."""
    sys.path.insert(0, str(ROOT / 'app/server'))
    from repertorio.motion import frame, loop_clip, probe, storyboard
    dest = MEDIA / 'video'
    dest.mkdir(parents=True, exist_ok=True)
    info = probe(ROOT / VIDEO)
    if not (dest / 'quadros.jpg').exists():
        storyboard(ROOT / VIDEO, dest / 'quadros.jpg', info['duration'])
        frame(ROOT / VIDEO, info['duration'] * .92, 1280).save(dest / 'capa.jpg', quality=88)
        loop_clip(ROOT / VIDEO, dest / 'loop.mp4', info['duration'])
    rel = lambda p: str(p.relative_to(ROOT))
    record = dict(
        id='perestroika-chora-ppt-video', slug='chora-ppt-video', collection='perestroika',
        title='Chora PPT: apresentador e tipografia cinética',
        description='Vídeo de abertura do curso Chora PPT, com 13,6 s. O professor fala em fundo branco enquanto corações, '
                    'balões de conversa e um botão de play entram ao redor dele; a cena vira fundo grafite com rabiscos coral '
                    'e fecha em tipografia condensada gigante: "Oceano de estímulos" e "batalha pela atenção".',
        idea='Alterne a pessoa falando com cartelas de uma palavra gigante na mesma cor de acento, para a frase-chave ficar na memória.',
        how='0 a 3 s: apresentador em fundo branco com grafismos coral que pipocam em volta (corações, balões, play). '
            '5 a 8 s: fundo grafite, rabiscos animados e "OCEANO DE ESTÍMULOS" em caixa alta condensada. '
            '9 a 11 s: volta ao apresentador. 12 a 13,6 s: "batalha pela ATENÇÃO" com a palavra final ocupando a tela.',
        techniques=['tipografia-como-imagem', 'contraste-de-cor', 'contraste-de-escala', 'rosto-que-encara'],
        intentions=['ABRIR', 'IMPACTAR', 'DESTACAR'], movements=['texto', 'troca'],
        aesthetics=['editorial', 'alto-contraste', 'escuro', 'claro'], tone=['energetico', 'divertido'], strength=4,
        cautions='Material de divulgação de curso da Perestroika. Use como referência de ritmo e linguagem, sem copiar.',
        author='Perestroika', page=COURSE, stack='Vídeo editado', content_tags=['kinetic-type'],
        good_for=['abertura de curso ou palestra em vídeo', 'vídeo de professor com cartelas de palavra-chave'],
        media=dict(poster=rel(dest / 'capa.jpg'), storyboard=rel(dest / 'quadros.jpg'), loop=rel(dest / 'loop.mp4'), video=VIDEO),
        genres=['tipografia', 'explicativo'], aspect='horizontal', **{k: info[k] for k in ('width', 'height', 'duration', 'fps', 'audio')})
    (OUT / 'motion').mkdir(parents=True, exist_ok=True)
    (OUT / 'motion/chora-ppt.jsonl').write_text(json.dumps(record, ensure_ascii=False) + '\n')


def pranchas():
    """Uma prancha por apresentação com as páginas escolhidas e o título de cada ficha, para conferir antes de importar."""
    from PIL import Image, ImageDraw, ImageFont
    out = ROOT / 'app/.runtime/qa/perestroika'
    out.mkdir(parents=True, exist_ok=True)
    rows = [json.loads(line) for line in (OUT / 'decks.jsonl').read_text().splitlines()]
    try:
        face = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 15)
    except OSError:
        face = ImageFont.load_default()
    for deck in [r for r in rows if r['doc'] == 'arquivo']:
        items = [deck] + [r for r in rows if r.get('deck') == deck['id']]
        cols, w, h, cap = 4, 400, 260, 44
        sheet = Image.new('RGB', (cols * w, -(-len(items) // cols) * (h + cap)), (20, 20, 20))
        draw = ImageDraw.Draw(sheet)
        for i, r in enumerate(items):
            im = Image.open(ROOT / r['preview']).convert('RGB')
            im.thumbnail((w - 8, h - 8))
            x, y = (i % cols) * w, (i // cols) * (h + cap)
            sheet.paste(im, (x + 4, y + 4))
            label = ('CAPA ' if r['doc'] == 'arquivo' else f"p{r['n']} ") + r['title']
            draw.text((x + 6, y + h + 2), label[:52], font=face, fill=(240, 240, 240))
            draw.text((x + 6, y + h + 22), ' '.join(r['techniques'][:3])[:52], font=face, fill=(255, 150, 120))
        sheet.save(out / f"{deck['id']}.jpg", quality=82)
    print(out)


if __name__ == '__main__':
    {'montar': montar, 'pranchas': pranchas}[sys.argv[1]]()
