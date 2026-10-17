import os, sys, re, json, subprocess, time, unicodedata, glob
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from slim import build
ROOT, OUT, TMP = sys.argv[1], sys.argv[2], sys.argv[3]
only = sys.argv[4].split(',') if len(sys.argv) > 4 else None
SIZE = 800
def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')[:60]
decks = sorted(f for f in os.listdir(ROOT) if f.lower().endswith('.pptx'))
ids = {f: '%03d-%s' % (i + 1, slug(os.path.splitext(f)[0])) for i, f in enumerate(decks)}
json.dump(ids, open(os.path.join(OUT, 'ids.json'), 'w'), ensure_ascii=False, indent=0)
def work(f):
    did = ids[f]; dest = os.path.join(OUT, did); os.makedirs(dest, exist_ok=True)
    tmp = os.path.join(TMP, did); os.makedirs(tmp, exist_ok=True)
    t0 = time.time()
    made = build(os.path.join(ROOT, f), tmp, did)
    if not os.environ.get('REFAZER') and len(glob.glob(os.path.join(dest, '*.jpg'))) >= len(made) and made:
        for p in made: os.remove(p)
        return f, len(made), len(made), 0
    try: subprocess.run(['qlmanage', '-t', '-s', str(SIZE), '-o', tmp] + made, capture_output=True, timeout=90)
    except subprocess.TimeoutExpired: pass
    for p in made:
        if not os.path.exists(p + '.png'):
            try: subprocess.run(['qlmanage', '-t', '-s', str(SIZE), '-o', tmp, p], capture_output=True, timeout=25)
            except subprocess.TimeoutExpired: pass
    ok = 0
    for p in made:
        n = int(re.search(r'__s(\d+)\.pptx$', p).group(1))
        png = p + '.png'
        if os.path.exists(png):
            subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '65', png, '--out', os.path.join(dest, '%02d.jpg' % n)], capture_output=True)
            os.remove(png); ok += 1
        os.remove(p)
    return f, len(made), ok, round(time.time() - t0, 1)
todo = [f for f in decks if not only or f in only]
log = open(os.path.join(TMP, 'progress.log'), 'a')
res = {}
with ThreadPoolExecutor(5) as ex:
    futs = {ex.submit(work, f): f for f in todo}
    for i, fu in enumerate(as_completed(futs)):
        try: f, n, ok, dt = fu.result()
        except Exception as e: f, n, ok, dt = futs[fu], -1, 0, str(e)
        res[f] = {'slides': n, 'ok': ok}
        log.write('%d/%d %s slides=%s ok=%s t=%s\n' % (i + 1, len(todo), f, n, ok, dt)); log.flush()
json.dump(res, open(os.path.join(TMP, 'result_%d.json' % int(time.time())), 'w'), ensure_ascii=False, indent=0)
print('feito', len(res), 'falhas', [k for k, v in res.items() if v['ok'] != v['slides']])
