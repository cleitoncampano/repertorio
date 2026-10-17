"""Gera, para cada slide de um .pptx, uma copia enxuta contendo so aquele slide."""
import zipfile, re, os, sys, posixpath
def rels_path(part):
    d, n = posixpath.split(part)
    return posixpath.join(d, '_rels', n + '.rels')
def targets(z, names, part):
    rp = rels_path(part)
    if rp not in names: return []
    x = z.read(rp).decode('utf8', 'ignore')
    out = []
    for m in re.finditer(r'<Relationship\b([^>]*)/?>', x):
        a = m.group(1)
        if 'TargetMode="External"' in a: continue
        t = re.search(r'Target="([^"]+)"', a)
        if not t: continue
        t = t.group(1)
        p = t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(part), t))
        out.append(p)
    return out
def trocar_fontes(data):
    """So para a previa: troca fontes que o Quick Look nao enxerga por equivalentes instaladas."""
    x = data.decode('utf8', 'ignore')
    x = x.replace('typeface="Calibri Light"', 'typeface="Carlito"').replace('typeface="Calibri"', 'typeface="Carlito"')
    x = re.sub(r'typeface="Bricolage Grotesque \d+pt(?: Conden\w*)?( [A-Za-z]+)?"', lambda m: 'typeface="Bricolage Grotesque%s"' % (m.group(1) or ''), x)
    return x.encode('utf8')
def build(src, outdir, base):
    z = zipfile.ZipFile(src); names = set(z.namelist())
    pres = z.read('ppt/presentation.xml').decode('utf8')
    prels = z.read('ppt/_rels/presentation.xml.rels').decode('utf8')
    lst = re.search(r'<p:sldIdLst>(.*?)</p:sldIdLst>', pres, re.S)
    if not lst: return []
    ids = re.findall(r'<p:sldId\b[^>]*/>', lst.group(1))
    rid_of = [re.search(r'r:id="([^"]+)"', s).group(1) for s in ids]
    rel_entries = re.findall(r'<Relationship\b[^>]*/>', prels)
    def rel_target(rid):
        for e in rel_entries:
            if re.search(r'Id="%s"' % re.escape(rid), e):
                t = re.search(r'Target="([^"]+)"', e).group(1)
                return t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.join('ppt', t))
    slide_parts = [rel_target(r) for r in rid_of]
    ct = z.read('[Content_Types].xml').decode('utf8')
    made = []
    for i, (sid, rid) in enumerate(zip(ids, rid_of)):
        newpres = pres[:lst.start(1)] + sid + pres[lst.end(1):]
        newpres = re.sub(r'<p:custShowLst>.*?</p:custShowLst>', '', newpres, flags=re.S)
        newpres = re.sub(r'<p:ext uri="\{521415D9-36F7-43E2-AB2F-B90AF26B5E84\}">.*?</p:ext>', '', newpres, flags=re.S)
        other = set(slide_parts) - {slide_parts[i]}
        keep_rels = [e for e in rel_entries if not (re.search(r'/slide"', e) and re.search(r'Id="([^"]+)"', e).group(1) != rid)]
        newprels = re.sub(r'<Relationship\b[^>]*/>', '', prels)
        newprels = newprels.replace('</Relationships>', ''.join(keep_rels) + '</Relationships>')
        # alcance a partir do pacote
        keep = {'[Content_Types].xml', '_rels/.rels', 'ppt/presentation.xml', 'ppt/_rels/presentation.xml.rels'}
        stack = ['ppt/presentation.xml'] + [p for p in targets(z, names, '') if p in names]
        stack += [t for t in targets(z, names, '_rels/.rels'.replace('_rels/.rels', '')) ]
        for p in re.findall(r'Target="([^"]+)"', z.read('_rels/.rels').decode('utf8','ignore')):
            p = p.lstrip('/')
            if p in names and not p.endswith('thumbnail.jpeg'): stack.append(p)
        pres_targets = []
        for e in keep_rels:
            if 'TargetMode="External"' in e: continue
            t = re.search(r'Target="([^"]+)"', e).group(1)
            pres_targets.append(t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.join('ppt', t)))
        stack += pres_targets
        while stack:
            p = stack.pop()
            if p in keep or p not in names: continue
            if p in other: continue
            if p.startswith('ppt/notesSlides/'): continue
            keep.add(p)
            rp = rels_path(p)
            if rp in names: keep.add(rp)
            stack += targets(z, names, p)
        # remove referencias quebradas nos rels mantidos (ex.: notesSlide)
        out = os.path.join(outdir, '%s__s%03d.pptx' % (base, i + 1))
        with zipfile.ZipFile(out, 'w') as w:
            for n in z.namelist():
                if n not in keep: continue
                if n == 'ppt/presentation.xml': data = newpres.encode('utf8')
                elif n == 'ppt/_rels/presentation.xml.rels': data = newprels.encode('utf8')
                elif n == slide_parts[i]:
                    data = re.sub(r'(<p:sld\b[^>]*?)\s+show="0"', r'\1', z.read(n).decode('utf8'), count=1).encode('utf8')
                else: data = z.read(n)
                if re.match(r'ppt/(slides/slide|slideLayouts/slideLayout|slideMasters/slideMaster|theme/theme)\d+\.xml$', n):
                    data = trocar_fontes(data)
                if n.endswith('.rels') and n != 'ppt/_rels/presentation.xml.rels':
                    x = data.decode('utf8', 'ignore')
                    def ok(m):
                        a = m.group(0)
                        if 'TargetMode="External"' in a: return a
                        t = re.search(r'Target="([^"]+)"', a)
                        if not t: return a
                        t = t.group(1); src_part = n.replace('_rels/', '')[:-5]
                        q = t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(src_part), t))
                        return a if (q in keep or q not in names) else ''
                    data = re.sub(r'<Relationship\b[^>]*/>', ok, x).encode('utf8')
                comp = zipfile.ZIP_STORED if n.startswith('ppt/media/') else zipfile.ZIP_DEFLATED
                w.writestr(zipfile.ZipInfo(n, (2024, 1, 1, 0, 0, 0)), data, compress_type=comp)
        made.append(out)
    return made
if __name__ == '__main__':
    print(len(build(sys.argv[1], sys.argv[2], sys.argv[3])))
