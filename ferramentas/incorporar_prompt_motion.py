#!/usr/bin/env python3
"""Traz a galeria do Prompt Motion (prompt-motion.com) para o espaço Motion do Repertório.

Coletar páginas e prompts:  app/.venv/bin/python ferramentas/incorporar_prompt_motion.py coletar
Baixar capas e vídeos:      app/.venv/bin/python ferramentas/incorporar_prompt_motion.py baixar
Gerar quadros e medidas:    app/.venv/bin/python ferramentas/incorporar_prompt_motion.py quadros
Separar lotes para fichas:  app/.venv/bin/python ferramentas/incorporar_prompt_motion.py lotes
Montar as fichas:           app/.venv/bin/python ferramentas/incorporar_prompt_motion.py montar
Importar no app:            ./app/run.sh import-motion --workspace ID_DO_ESPACO

Vídeos, capas e páginas ficam em _originais/prompt-motion/, fora do Git. A classificação criativa
fica em dados/motion/_trabalho/ e as fichas prontas em dados/motion/prompt-motion.jsonl.
Os vídeos pertencem aos autores: entram como referência de terceiros, sem reutilização da mídia.
"""
import argparse
import json
import re
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://prompt-motion.com'
DEST = ROOT / '_originais/prompt-motion'
PAGES = DEST / '_paginas'
CATALOG = DEST / 'catalogo.json'
WORK = ROOT / 'dados/motion/_trabalho'
OUT = ROOT / 'dados/motion/prompt-motion.jsonl'
AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36 Repertorio/0.2'
TEMPLATES = ['showreel', 'realtime']


def fetch(url, tries=4):
    for n in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': AGENT}), timeout=60) as r:
                return r.read()
        except Exception:
            if n == tries - 1:
                raise
            time.sleep(2 * (n + 1))


def flight(html):
    """Junta o conteúdo que o Next.js envia em self.__next_f e devolve o texto decodificado."""
    chunks = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', html, re.S)
    return ''.join(json.loads('"' + c + '"') for c in chunks)


def flat(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        if len(value) == 4 and value[0] == '$' and isinstance(value[3], dict):
            return flat(value[3].get('children'))
        return ''.join(flat(v) for v in value)
    if isinstance(value, dict):
        return flat(value.get('children'))
    return ''


def text_rows(text):
    """Textos longos que o Next.js manda à parte, em linhas ID:T<tamanho em bytes hexa>,texto."""
    raw = text.encode()
    rows = {}
    for m in re.finditer(rb'(?m)^(\w+):T([0-9a-f]+),', raw):
        rows[m.group(1).decode()] = raw[m.end():m.end() + int(m.group(2), 16)].decode('utf-8', 'replace')
    return rows


def value_after(text, marker):
    i = text.find(marker)
    if i < 0:
        return None
    try:
        return json.JSONDecoder().raw_decode(text[i + len(marker):])[0]
    except ValueError:
        return None


def detail(text):
    """Campos de uma página de vídeo: prompt, nota, tradução, autor, post, skill e ficha técnica."""
    out = {}
    rows = text_rows(text)
    for key in ('prompt', 'note', 'translation'):
        v = value_after(text, f'"{key}":')
        if isinstance(v, str) and v.startswith('$') and v[1:] in rows:
            v = rows[v[1:]]
        if isinstance(v, str) and v != '$undefined':
            out[key] = v
    for m in re.finditer(r'\["\$","dt",null,\{"className":"text-muted-foreground","children":"([^"]+)"\}\],\["\$","dd",null,\{"className":"min-w-0","children":', text):
        try:
            v = json.JSONDecoder().raw_decode(text[m.end():])[0]
        except ValueError:
            continue
        out.setdefault('facts', {})[m.group(1)] = flat(v)
    m = re.search(r'"entry-creator".*?"truncate font-medium","children":"([^"]+)"', text, re.S)
    if m:
        out['author'] = m.group(1)
    m = re.search(r'"href":"(https://(?:x|twitter)\.com/[^"]+/status/\d+)"', text)
    if m:
        out['post'] = m.group(1)
    m = re.search(r'"children":"Skill"\}\],\["\$","p",null,\{[^}]*"children":"((?:[^"\\]|\\.)*)"', text)
    if m:
        out['skill'] = {'about': json.loads('"' + m.group(1) + '"')}
        cmd =re.search(r'"text":"((?:[^"\\]|\\.)*)","label":"Copy install command"', text)
        if cmd:
            out['skill']['install'] = json.loads('"' + cmd.group(1) + '"')
        repo = re.search(r'"href":"(https://github\.com/[^"]+)"[^\]]*?"children":\["View repo"', text)
        if repo:
            out['skill']['repo'] = repo.group(1)
    return out


def coletar(args):
    PAGES.mkdir(parents=True, exist_ok=True)
    home = fetch(SITE + '/').decode()
    (PAGES / 'index.html').write_text(home)
    text = flight(home)
    items = json.JSONDecoder().raw_decode(text[text.find('[{"slug":'):])[0]
    print(len(items), 'vídeos na galeria')

    def one(item):
        page = PAGES / f"{item['slug']}.html"
        if not page.exists() or args.refresh:
            page.write_text(fetch(f"{SITE}/{item['slug']}").decode())
            time.sleep(.2)
        return {**item, **detail(flight(page.read_text())), 'page': f"{SITE}/{item['slug']}"}

    with ThreadPoolExecutor(4) as pool:
        entries = list(pool.map(one, items))
    templates = []
    for name in TEMPLATES:
        page = PAGES / f'template-{name}.html'
        if not page.exists() or args.refresh:
            page.write_text(fetch(f'{SITE}/templates/{name}').decode())
        text = flight(page.read_text())
        title = re.search(r'"title","0",\{"children":"([^"]+)"', text)
        desc = re.search(r'"name":"description","content":"((?:[^"\\]|\\.)*)"', text)
        poster = re.search(r'"(https://media\.prompt-motion\.com/[^"]+/poster\.[^"]+)"', text)
        templates.append({'slug': 'template-' + name, 'template': name, 'page': f'{SITE}/templates/{name}',
                          'title': title.group(1).split(' · ')[0] if title else name,
                          'about': json.loads('"' + desc.group(1) + '"') if desc else '',
                          'poster': poster.group(1) if poster else None, 'text': template_text(text)})
    missing = [e['slug'] for e in entries if not e.get('prompt')]
    CATALOG.write_text(json.dumps({'source': SITE, 'collected': time.strftime('%Y-%m-%d'), 'items': entries, 'templates': templates}, ensure_ascii=False, indent=1))
    print('catálogo salvo em', CATALOG.relative_to(ROOT), '| sem prompt:', missing)


def template_text(text):
    """O prompt reescrito da página de modelo."""
    return list(dict.fromkeys(t for t in text_rows(text).values() if '<direction>' in t))


def download(url, path):
    if path.exists() and path.stat().st_size > 0:
        return 'já existe'
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_bytes(fetch(url))
    tmp.replace(path)
    return 'baixado'


def baixar(args):
    data = json.loads(CATALOG.read_text())
    jobs = []
    for e in data['items']:
        folder = DEST / e['slug']
        folder.mkdir(parents=True, exist_ok=True)
        for key, name in (('poster', 'capa.webp'), ('preview', 'loop.mp4'), ('video', 'video.mp4')):
            if e.get(key):
                jobs.append((e[key], folder / name))
    for t in data['templates']:
        if t.get('poster'):
            (DEST / t['slug']).mkdir(parents=True, exist_ok=True)
            jobs.append((t['poster'], DEST / t['slug'] / 'capa.webp'))
    failed = []

    def run(job):
        try:
            return download(*job)
        except Exception as exc:
            failed.append((job[0], str(exc)))
            return 'falhou'

    with ThreadPoolExecutor(args.workers) as pool:
        results = list(pool.map(run, jobs))
    print({k: results.count(k) for k in set(results)}, 'falhas:', failed[:10])
    if failed:
        sys.exit(1)


def probe(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_type,width,height,r_frame_rate',
                        '-of', 'json', str(path)], capture_output=True, text=True, check=True)
    info = json.loads(r.stdout)
    video = next(s for s in info['streams'] if s['codec_type'] == 'video')
    num, den = (video.get('r_frame_rate') or '30/1').split('/')
    return {'duration': round(float(info['format']['duration']), 2), 'width': video['width'], 'height': video['height'],
            'fps': round(int(num) / max(1, int(den)), 2), 'audio': any(s['codec_type'] == 'audio' for s in info['streams'])}


def storyboard(video, out, duration, frames=8):
    """Oito momentos do vídeo numa prancha 4x2, com o tempo de cada um. É o que o agente vê do movimento."""
    from PIL import Image, ImageDraw, ImageFont
    times = [duration * (i + .5) / frames for i in range(frames)]
    shots = []
    for t in times:
        r = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-ss', f'{t:.2f}', '-i', str(video), '-frames:v', '1',
                            '-vf', 'scale=480:480:force_original_aspect_ratio=decrease', '-f', 'image2pipe', '-vcodec', 'png', '-'],
                           capture_output=True, check=True, timeout=120)
        import io
        shots.append(Image.open(io.BytesIO(r.stdout)).convert('RGB'))
    w = max(s.width for s in shots)
    h = max(s.height for s in shots)
    gap, label = 8, 26
    sheet = Image.new('RGB', (gap + 4 * (w + gap), gap + 2 * (h + label + gap)), (16, 16, 16))
    draw = ImageDraw.Draw(sheet)
    try:
        face = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 17)
    except OSError:
        face = ImageFont.load_default()
    for i, (shot, t) in enumerate(zip(shots, times)):
        x = gap + (i % 4) * (w + gap)
        y = gap + (i // 4) * (h + label + gap)
        sheet.paste(shot, (x + (w - shot.width) // 2, y + label + (h - shot.height) // 2))
        draw.text((x, y + 3), f'{i + 1} · {t:.1f}s', font=face, fill=(255, 140, 110))
    sheet.save(out, quality=86)


def quadros(args):
    data = json.loads(CATALOG.read_text())

    def one(e):
        folder = DEST / e['slug']
        video = folder / 'video.mp4'
        meta = folder / 'medidas.json'
        if not video.exists():
            return e['slug'], 'sem vídeo'
        if not meta.exists() or args.refresh:
            meta.write_text(json.dumps(probe(video)))
        info = json.loads(meta.read_text())
        board = folder / 'quadros.jpg'
        if not board.exists() or args.refresh:
            storyboard(video, board, info['duration'])
        return e['slug'], 'ok'

    with ThreadPoolExecutor(args.workers) as pool:
        results = list(pool.map(one, data['items']))
    bad = [r for r in results if r[1] != 'ok']
    print(len(results) - len(bad), 'prontos', bad)


KEYS = ('title', 'description', 'idea', 'how', 'html', 'techniques', 'intentions', 'movements', 'aesthetics', 'strength', 'good_for', 'tone', 'cautions')


def lotes(args):
    """Divide a galeria em lotes para a classificação criativa (instruções em dados/motion/_trabalho/)."""
    data = json.loads(CATALOG.read_text())
    entries = []
    for e in data['items']:
        folder = DEST / e['slug']
        meta = json.loads((folder / 'medidas.json').read_text())
        facts = e.get('facts', {})
        entries.append({'slug': e['slug'], 'title_original': e['title'], 'prompt': e.get('prompt') or '', 'prompt_note': e.get('note') or '',
                        'author': e.get('author'), 'content_tags': e.get('contentTags', []), 'stack': facts.get('Stack', ''),
                        'iterations': facts.get('Iterations', ''), 'effort': facts.get('Effort', ''), 'skill': e.get('skill'),
                        **meta, 'quadros': str(folder / 'quadros.jpg')})
    for t in data['templates']:
        entries.append({'slug': t['slug'], 'title_original': t['title'], 'template': True, 'about': t['about'],
                        'prompt': '\n\n'.join(t.get('text') or []), 'quadros': str(DEST / t['slug'] / 'capa.webp')})
    (WORK / 'lotes').mkdir(parents=True, exist_ok=True)
    size = -(-len(entries) // args.lotes)
    for n in range(args.lotes):
        chunk = entries[n * size:(n + 1) * size]
        (WORK / 'lotes' / f'lote-{n + 1:02d}.json').write_text(json.dumps(chunk, ensure_ascii=False, indent=1))
        print(f'lote-{n + 1:02d}', len(chunk))


def aspect(width, height):
    """Formato de tela: horizontal (16:9, YouTube e sites), vertical (9:16, Reels e TikTok) ou quadrado (1:1 e 4:5, feed)."""
    if not width or not height:
        return ''
    ratio = width / height
    return 'horizontal' if ratio > 1.2 else 'vertical' if ratio < .85 else 'quadrado'


def montar(args):
    """Une coleta, medidas e classificação criativa numa ficha por vídeo."""
    data = json.loads(CATALOG.read_text())
    vocab = json.loads((ROOT / 'dados/vocabulario.json').read_text())
    allowed = {k: {i['id'] if isinstance(i, dict) else i for i in vocab[v]['itens']}
               for k, v in [('techniques', 'tecnicas'), ('intentions', 'intencoes'), ('movements', 'movimentos'), ('aesthetics', 'esteticas'), ('tone', 'tons')]}
    genres = json.loads((ROOT / 'dados/motion/generos.json').read_text())['videos']
    fichas = {}
    for f in sorted(WORK.glob('fichas-*.jsonl')):
        for line in f.read_text().splitlines():
            if line.strip():
                d = json.loads(line)
                fichas[d['slug']] = d
    rows, problems = [], []
    for e in data['items']:
        f = fichas.get(e['slug'])
        folder = DEST / e['slug']
        if not f:
            problems.append((e['slug'], 'sem classificação'))
            continue
        for k, ok in allowed.items():
            bad = set(f.get(k) or []) - ok
            if bad:
                problems.append((e['slug'], k, sorted(bad)))
                f[k] = [v for v in f.get(k) or [] if v in ok]
        meta = json.loads((folder / 'medidas.json').read_text()) if (folder / 'medidas.json').exists() else {}
        facts = e.get('facts', {})
        rows.append({
            'id': 'motion-' + e['slug'], 'slug': e['slug'], 'collection': 'prompt-motion',
            **{k: f.get(k) for k in KEYS if f.get(k) is not None},
            'title_original': e['title'],
            'prompt': e.get('prompt', ''), 'prompt_note': e.get('note', ''), 'prompt_translation': e.get('translation', ''),
            'author': e.get('author') or e['handle'], 'handle': e['handle'], 'post': e.get('post'), 'page': e['page'],
            'posted': e['date'], 'model': facts.get('Model', ''), 'iterations': facts.get('Iterations', ''),
            'stack': facts.get('Stack', ''), 'effort': facts.get('Effort', ''),
            'skill': e.get('skill'), 'content_tags': e.get('contentTags', []), 'source_tags': e.get('tags', []),
            'media': {'poster': str((folder / 'capa.webp').relative_to(ROOT)), 'loop': str((folder / 'loop.mp4').relative_to(ROOT)),
                      'video': str((folder / 'video.mp4').relative_to(ROOT)), 'storyboard': str((folder / 'quadros.jpg').relative_to(ROOT))},
            'genres': genres.get(e['slug'], []), 'aspect': aspect(meta.get('width') or e.get('width'), meta.get('height') or e.get('height')),
            'width': meta.get('width') or e.get('width'), 'height': meta.get('height') or e.get('height'),
            'duration': meta.get('duration'), 'fps': meta.get('fps'), 'audio': meta.get('audio'),
        })
    for t in data['templates']:
        f = fichas.get(t['slug'])
        if not f:
            problems.append((t['slug'], 'sem classificação'))
            continue
        rows.append({'id': 'motion-' + t['slug'], 'slug': t['slug'], 'collection': 'prompt-motion', 'template': True,
                     **{k: f.get(k) for k in KEYS if f.get(k) is not None},
                     'title_original': t['title'], 'prompt': f.get('prompt') or '\n\n'.join(t.get('text') or []),
                     'genres': ['modelo'], 'aspect': 'modelo', 'author': 'Prompt Motion', 'handle': 'p4nthera_', 'page': t['page'], 'content_tags': [], 'source_tags': ['template'],
                     'media': {'poster': str((DEST / t['slug'] / 'capa.webp').relative_to(ROOT))}})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows))
    print(len(rows), 'fichas em', OUT.relative_to(ROOT), '| avisos:', problems)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('coletar')
    c.add_argument('--refresh', action='store_true')
    b = sub.add_parser('baixar')
    b.add_argument('--workers', type=int, default=4)
    q = sub.add_parser('quadros')
    q.add_argument('--workers', type=int, default=4)
    q.add_argument('--refresh', action='store_true')
    lt = sub.add_parser('lotes')
    lt.add_argument('--lotes', type=int, default=6)
    sub.add_parser('montar')
    args = p.parse_args()
    {'coletar': coletar, 'baixar': baixar, 'quadros': quadros, 'lotes': lotes, 'montar': montar}[args.cmd](args)


if __name__ == '__main__':
    main()
