import json, os, re, zipfile, collections, struct, sys, time, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fontnames_lib import names_at
ROOT = sys.argv[1]; CAT = os.path.join(ROOT, '_catalogo'); S = os.path.dirname(os.path.abspath(__file__))
def sanitize(t):
    t = re.sub(r'[\\/*?:"<>|]', "_", t).strip(); return re.sub(r"\s+", "_", t)
GRUPO = {3: '3D', 4: 'Capas', 5: 'Diversos', 6: 'Efeito WOW', 7: 'Gráficos e esquemas', 8: 'Instagram', 9: 'Mapas',
         10: 'Organograma', 11: 'Padrões', 12: 'Pessoal', 13: 'Produto', 14: 'Templates temáticos', 15: 'Linha do tempo', 17: 'Grátis'}
def grupo(mi): return GRUPO.get(mi, 'Templates completos' if mi >= 18 else 'Outros')
def titulo(p):
    if p['moduleIndex'] >= 18:
        t = re.sub(r'^Templ[a-z]+\s+', '', p['moduleName']); t = re.sub(r'\s*\(Animado\)?\s*$', '', t); return t.strip()
    return p['pageName'].strip()
# fontes disponiveis (sistema, usuario e as que o PowerPoint traz)
avail = set()
for d in ['/System/Library/Fonts', '/Library/Fonts', os.path.expanduser('~/Library/Fonts'),
          '/Applications/Microsoft PowerPoint.app/Contents/Resources/DFonts',
          os.path.expanduser('~/Library/Group Containers/UBF8T346G9.Office/FontCache')]:
    for r, _, fs in os.walk(d):
        for f in fs:
            p = os.path.join(r, f)
            try:
                data = open(p, 'rb').read()
                if data[:4] == b'ttcf':
                    n = struct.unpack('>I', data[8:12])[0]; offs = struct.unpack('>%dI' % n, data[12:12 + 4 * n])
                elif data[:4] in (b'\x00\x01\x00\x00', b'OTTO', b'true'): offs = [0]
                else: continue
                for o in offs:
                    nm = names_at(data, o)
                    for k in (1, 4, 6, 16):
                        if nm.get(k): avail.add(nm[k].strip().lower())
            except Exception: pass
cat = json.load(open(os.path.join(ROOT, '_originais', 'curso', 'catalogo-curso.json')))
PPTX = os.path.join(ROOT, '_originais', 'pptx')
files = sorted(unicodedata.normalize('NFC', f) for f in os.listdir(PPTX) if f.lower().endswith('.pptx'))
ids = {unicodedata.normalize('NFC', k): v for k, v in json.load(open(os.path.join(CAT, 'miniaturas', 'ids.json'))).items()}
fmap = collections.defaultdict(list)
for p in cat:
    for a in p['attachments']:
        o = unicodedata.normalize('NFC', a['fileName']); b, e = os.path.splitext(o)
        alt = unicodedata.normalize('NFC', '%s__%s%s' % (b, sanitize(p['moduleName'] + '-' + p['pageName']), e))
        for cand in (alt, o):
            if cand in files and os.path.getsize(os.path.join(PPTX, cand)) == a['fileSize']:
                fmap[cand].append(p); break
LOREM = set('lorem ipsum dolor sit amet consectetur consectetuer adipiscing adipisicing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua enim ad minim veniam quis nostrud exercitation ullamco laboris nisi aliquip ex ea commodo consequat duis aute irure in reprehenderit voluptate velit esse cillum fugiat nulla pariatur excepteur sint occaecat cupidatat non proident sunt culpa qui officia deserunt mollit anim id est laborum maecenas porttitor congue massa fusce posuere pulvinar ultricies purus lectus malesuada libero amet commodo eros urna nunc viverra imperdiet nec dolo sita ipsu loremipsum'.split())
decks = []
for f in files:
    z = zipfile.ZipFile(os.path.join(PPTX, f)); names = z.namelist()
    pres = z.read('ppt/presentation.xml').decode('utf8', 'ignore')
    m = re.search(r'<p:sldSz cx="(\d+)" cy="(\d+)"', pres)
    ratio = int(m.group(1)) / int(m.group(2)) if m else 16 / 9
    prels = z.read('ppt/_rels/presentation.xml.rels').decode('utf8', 'ignore')
    tgt = {}
    for e in re.findall(r'<Relationship\b[^>]*/>', prels):
        i_ = re.search(r'Id="([^"]+)"', e); t_ = re.search(r'Target="([^"]+)"', e)
        if i_ and t_: tgt[i_.group(1)] = t_.group(1).lstrip('/') if t_.group(1).startswith('/') else 'ppt/' + t_.group(1)
    lst = re.search(r'<p:sldIdLst>(.*?)</p:sldIdLst>', pres, re.S)
    slides = [tgt[r_] for r_ in re.findall(r'<p:sldId\b[^>]*r:id="([^"]+)"', lst.group(1))] if lst else []
    ocultos = [k + 1 for k, s_ in enumerate(slides) if re.search(r'<p:sld\b[^>]*\sshow="0"', z.read(s_).decode('utf8', 'ignore')[:3000])]
    fonts = collections.Counter(); words = []; seen = set(); morph = anim = 0; table = False
    for s in slides:
        x = z.read(s).decode('utf8', 'ignore')
        if 'p159:morph' in x: morph += 1
        if '<p:timing' in x and '<p:par>' in x: anim += 1
        if '<a:tbl>' in x: table = True
        for t in re.findall(r'<a:latin typeface="([^"]+)"', x):
            if not t.startswith('+'): fonts[t] += 1
        for t in re.findall(r'<a:t>([^<]+)</a:t>', x):
            for w in re.findall(r"[\wÀ-ÿ&'.,%$-]+", t):
                k = w.lower().strip('.,')
                if not k or k in LOREM or k in seen: continue
                seen.add(k); words.append(w)
    th = [n for n in names if re.match(r'ppt/theme/theme\d+\.xml$', n)]
    if th:
        tx = z.read(sorted(th)[0]).decode('utf8', 'ignore')
        for k in ('majorFont', 'minorFont'):
            mm = re.search(r'<a:%s><a:latin typeface="([^"]+)"' % k, tx)
            if mm and mm.group(1) not in fonts: fonts[mm.group(1)] += 0
    ext = collections.Counter(os.path.splitext(n)[1].lower() for n in names if n.startswith('ppt/media/'))
    fl = [k for k, _ in fonts.most_common(6)]
    did = ids[unicodedata.normalize('NFC', f)]; tdir = os.path.join(CAT, 'miniaturas', did)
    thumbs = sorted(int(x[:-4]) for x in os.listdir(tdir) if x.endswith('.jpg')) if os.path.isdir(tdir) else []
    pages = sorted(fmap.get(f, []), key=lambda p: (p['moduleIndex'], p['pageIndex']))
    p0 = pages[0] if pages else None
    decks.append({
        'id': did, 'arq': f, 'titulo': titulo(p0) if p0 else os.path.splitext(f)[0],
        'grupos': sorted(set(grupo(p['moduleIndex']) for p in pages)) or ['Outros'],
        'modulo': p0['moduleName'] if p0 else '', 'ordem': [p0['moduleIndex'], p0['pageIndex']] if p0 else [999, 0],
        'slides': len(slides), 'thumbs': thumbs, 'ocultos': ocultos, 'vertical': ratio < 1, 'quadrado': 0.9 <= ratio <= 1.1,
        'morph': morph, 'anim': anim, 'video': sum(ext[e] for e in ('.mp4', '.mov', '.m4v')) > 0, 'tres_d': ext['.glb'] > 0,
        'grafico': any(re.match(r'ppt/charts/chart\d+\.xml$', n) for n in names), 'tabela': table,
        'fontes': fl, 'faltam': [x for x in fl if x.strip().lower() not in avail],
        'mb': round(os.path.getsize(os.path.join(PPTX, f)) / 1e6, 1),
        'texto': ' '.join(words)[:600],
    })
canva = json.load(open(os.path.join(S, 'canva.json')))
for c in canva:
    c['thumbs'] = sorted(int(x[:-4]) for x in os.listdir(os.path.join(CAT, 'miniaturas', c['id'])) if x.endswith('.jpg'))
data = {'gerado': time.strftime('%d/%m/%Y'), 'decks': decks, 'canva': canva}
open(os.path.join(CAT, 'dados.js'), 'w').write('window.CATALOGO = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
print('decks', len(decks), 'sem aula', [d['arq'] for d in decks if d['grupos'] == ['Outros']],
      'sem miniatura', [d['arq'] for d in decks if len(d['thumbs']) < d['slides']][:10],
      'slides', sum(d['slides'] for d in decks), 'thumbs', sum(len(d['thumbs']) for d in decks))
print(collections.Counter(g for d in decks for g in d['grupos']))
print('com fonte faltando', sum(1 for d in decks if d['faltam']), collections.Counter(x for d in decks for x in d['faltam']).most_common(12))
print('tamanho dados.js', os.path.getsize(os.path.join(CAT, 'dados.js')))
