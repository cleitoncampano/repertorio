#!/usr/bin/env python3
"""Lê os .pptx de _originais/pptx e gera os dados de máquina em dados/:

  decks.jsonl        um registro por arquivo (paleta, fontes, proporção, contagens)
  slides.jsonl       um registro por slide (textos, cores, objetos, transição, animações)
  transicoes.jsonl   cada passagem de slide com transição; Morph vem analisado objeto a objeto
  midia.jsonl        cada mídia única de dentro dos arquivos (imagem, svg, vídeo, 3D)

Também grava prévias pequenas das imagens e vídeos em acervo/previas/ e os SVG em acervo/svg/.
Uso, da raiz do projeto:  python3 -I ferramentas/construir/extrair.py
"""
import collections
import hashlib
import io
import json
import math
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from concurrent.futures import ProcessPoolExecutor, as_completed

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PPTX = os.path.join(RAIZ, '_originais', 'pptx')
DADOS = os.path.join(RAIZ, 'dados')
PREVIAS = os.path.join(RAIZ, 'acervo', 'previas')
SVG = os.path.join(RAIZ, 'acervo', 'svg')
TAM_PREVIA = 360

P = '{http://schemas.openxmlformats.org/presentationml/2006/main}'
A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
MC = '{http://schemas.openxmlformats.org/markup-compatibility/2006}'
PR = '{http://schemas.openxmlformats.org/package/2006/relationships}'
ASVG = '{http://schemas.microsoft.com/office/drawing/2016/SVG/main}'

LOREM = set('lorem ipsum dolor sit amet consectetur consectetuer adipiscing adipisicing elit sed do eiusmod tempor incididunt ut '
            'labore et dolore magna aliqua enim ad minim veniam quis nostrud exercitation ullamco laboris nisi aliquip ex ea commodo '
            'consequat duis aute irure in reprehenderit voluptate velit esse cillum fugiat nulla pariatur excepteur sint occaecat '
            'cupidatat non proident sunt culpa qui officia deserunt mollit anim id est laborum maecenas porttitor congue massa fusce '
            'posuere pulvinar ultricies purus lectus malesuada libero commodo eros urna nunc viverra imperdiet nec'.split())


def e_lorem(t):
    baixo = (t or '').lower().strip()
    if baixo.startswith(('lorem', 'ipsum')):
        return True
    palavras = re.findall(r'[a-z]+', baixo)
    return bool(palavras) and sum(p in LOREM for p in palavras) >= 0.6 * len(palavras)


def num(x):
    return ('%.1f' % x).replace('.', ',')
IMAGEM = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.tif', '.tiff'}
VIDEO = {'.mp4', '.mov', '.m4v', '.avi', '.wmv'}
NOMES_ANIM = {('entr', 1): 'aparecer', ('entr', 2): 'voar para dentro', ('entr', 10): 'esmaecer', ('entr', 22): 'revelar',
              ('exit', 1): 'desaparecer', ('exit', 2): 'voar para fora', ('exit', 10): 'esmaecer saída', ('exit', 22): 'revelar saída'}


def nfc(s):
    return unicodedata.normalize('NFC', s)


def local(tag):
    return tag.rsplit('}', 1)[-1]


def ler_rels(z, parte):
    caminho = posixpath.join(posixpath.dirname(parte), '_rels', posixpath.basename(parte) + '.rels')
    out = {}
    try:
        raiz = ET.fromstring(z.read(caminho))
    except (KeyError, ET.ParseError):
        return out
    for e in raiz.iter(PR + 'Relationship'):
        alvo = e.get('Target', '')
        if e.get('TargetMode') == 'External':
            out[e.get('Id')] = (e.get('Type', ''), None)
        else:
            alvo = alvo.lstrip('/') if alvo.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(parte), alvo))
            out[e.get('Id')] = (e.get('Type', ''), alvo)
    return out


def xml(z, parte):
    try:
        return ET.fromstring(z.read(parte))
    except (KeyError, ET.ParseError):
        return None


def hexcor(v):
    return '#' + v.upper() if v and re.fullmatch(r'[0-9A-Fa-f]{6}', v) else None


def tema_cores(z, parte_tema):
    raiz = xml(z, parte_tema)
    cores = {}
    if raiz is None:
        return cores
    esquema = raiz.find('.//' + A + 'clrScheme')
    if esquema is None:
        return cores
    for el in esquema:
        nome = local(el.tag)
        for c in el:
            if local(c.tag) == 'srgbClr':
                cores[nome] = hexcor(c.get('val'))
            elif local(c.tag) == 'sysClr':
                cores[nome] = hexcor(c.get('lastClr'))
    for a_, b_ in (('bg1', 'lt1'), ('tx1', 'dk1'), ('bg2', 'lt2'), ('tx2', 'dk2')):
        if b_ in cores:
            cores[a_] = cores[b_]
    return cores


def cor_de(el, tema):
    """Cor de um a:solidFill / a:gs (primeiro filho de cor)."""
    for c in el:
        n = local(c.tag)
        if n == 'srgbClr':
            return hexcor(c.get('val'))
        if n == 'schemeClr':
            return tema.get(c.get('val'))
        if n == 'sysClr':
            return hexcor(c.get('lastClr'))
        if n == 'prstClr':
            return {'black': '#000000', 'white': '#FFFFFF'}.get(c.get('val'))
    return None


def xfrm_de(item):
    n = local(item.tag)
    if n == 'grpSp':
        x = item.find(P + 'grpSpPr/' + A + 'xfrm')
    elif n == 'graphicFrame':
        x = item.find(P + 'xfrm')
    else:
        x = item.find(P + 'spPr/' + A + 'xfrm')
    if x is None:
        return None
    off, ext = x.find(A + 'off'), x.find(A + 'ext')
    if off is None or ext is None:
        return None
    try:
        return {'x': int(off.get('x')), 'y': int(off.get('y')), 'w': int(ext.get('cx')), 'h': int(ext.get('cy')),
                'rot': int(x.get('rot', 0)) / 60000.0}
    except (TypeError, ValueError):
        return None


def itens_da_arvore(arvore):
    """Objetos de primeiro nível de um spTree (abre mc:AlternateContent)."""
    out = []
    for c in list(arvore):
        n = local(c.tag)
        if n in ('sp', 'pic', 'cxnSp', 'graphicFrame', 'grpSp', 'contentPart'):
            out.append(c)
        elif n == 'AlternateContent':
            esc = c.find(MC + 'Choice')
            if esc is None:
                esc = c.find(MC + 'Fallback')
            if esc is not None:
                out.extend(x for x in esc if local(x.tag) in ('sp', 'pic', 'cxnSp', 'graphicFrame', 'grpSp'))
    return out


def placeholders(z, parte):
    """Mapa de posições dos placeholders de um layout ou master."""
    raiz = xml(z, parte)
    mapa = {}
    if raiz is None:
        return mapa
    arvore = raiz.find('.//' + P + 'spTree')
    if arvore is None:
        return mapa
    for it in itens_da_arvore(arvore):
        ph = it.find('./*/' + P + 'nvPr/' + P + 'ph')
        xf = xfrm_de(it)
        if ph is None or xf is None:
            continue
        tipo = ph.get('type', 'body')
        if ph.get('idx'):
            mapa.setdefault(('idx', ph.get('idx')), xf)
        mapa.setdefault(('type', tipo), xf)
    return mapa


def descrever_item(it, tema, rels, ph_layout, ph_master):
    n = local(it.tag)
    nv = it[0] if len(it) else None
    cnv = nv.find(P + 'cNvPr') if nv is not None else None
    nome = cnv.get('name', '') if cnv is not None else ''
    ph = it.find('./*/' + P + 'nvPr/' + P + 'ph')
    xf = xfrm_de(it)
    if xf is None and ph is not None:
        tipo = ph.get('type', 'body')
        for mapa in (ph_layout, ph_master):
            xf = mapa.get(('idx', ph.get('idx'))) if ph.get('idx') else None
            xf = xf or mapa.get(('type', tipo)) or (mapa.get(('type', 'title')) if tipo == 'ctrTitle' else None)
            if xf:
                break
    textos, tamanhos = [], []
    for p_ in it.iter(A + 'p'):
        t = ''.join(x.text or '' for x in p_.iter(A + 't')).strip()
        if t:
            textos.append(t)
    for r_ in it.iter():
        if local(r_.tag) in ('rPr', 'defRPr', 'endParaRPr') and r_.get('sz'):
            try:
                tamanhos.append(int(r_.get('sz')) / 100.0)
            except ValueError:
                pass
    tipo = {'sp': 'forma', 'pic': 'imagem', 'cxnSp': 'linha', 'grpSp': 'grupo', 'graphicFrame': 'quadro', 'contentPart': 'tinta'}[n]
    if n == 'graphicFrame':
        gd = it.find('.//' + A + 'graphicData')
        uri = gd.get('uri', '') if gd is not None else ''
        tipo = 'tabela' if 'table' in uri else 'grafico' if 'chart' in uri else '3d' if 'model3d' in uri else 'smartart' if 'diagram' in uri else 'quadro'
    if n == 'pic' and (it.find('.//' + A + 'videoFile') is not None or any(local(e.tag) == 'media' for e in it.iter())):
        tipo = 'video'
    if n == 'sp' and textos and not it.find(P + 'spPr/' + A + 'prstGeom') is not None:
        tipo = 'texto'
    elif n == 'sp' and textos:
        tipo = 'texto' if (it.find(P + 'nvSpPr/' + P + 'cNvSpPr') is not None and it.find(P + 'nvSpPr/' + P + 'cNvSpPr').get('txBox') == '1') or ph is not None else 'forma'
    blips = []
    for b in it.iter(A + 'blip'):
        rid = b.get(R + 'embed')
        svg = b.find('.//' + ASVG + 'svgBlip')
        blips.append((rid, svg.get(R + 'embed') if svg is not None else None))
    cor = None
    sppr = it.find(P + 'spPr')
    if sppr is not None:
        sf = sppr.find(A + 'solidFill')
        if sf is not None:
            cor = cor_de(sf, tema)
    geom = None
    if sppr is not None:
        pg = sppr.find(A + 'prstGeom')
        geom = pg.get('prst') if pg is not None else ('livre' if sppr.find(A + 'custGeom') is not None else None)
    mascara = n == 'sp' and sppr is not None and sppr.find(A + 'blipFill') is not None
    if n == 'pic' and geom and geom != 'rect':
        mascara = True
    return {'nome': nome, 'tipo': tipo, 'xf': xf, 'texto': ' / '.join(textos)[:200], 'tam': max(tamanhos) if tamanhos else None,
            'blips': blips, 'cor': cor, 'geom': geom, 'mascara': mascara, 'ph': ph.get('type', 'body') if ph is not None else None}


def transicao_de(raiz):
    trans = None
    for ac in raiz.findall(MC + 'AlternateContent'):
        ch = ac.find(MC + 'Choice')
        if ch is not None and ch.find(P + 'transition') is not None:
            trans = ch.find(P + 'transition')
            break
    if trans is None:
        trans = raiz.find(P + 'transition')
    if trans is None:
        return None
    filhos = [c for c in trans if local(c.tag) not in ('sndAc', 'extLst')]
    dur = None
    for k, v in trans.attrib.items():
        if local(k) == 'dur':
            dur = int(v)
    if dur is None and trans.get('spd'):
        dur = {'slow': 1000, 'med': 750, 'fast': 500}.get(trans.get('spd'))
    out = {'tipo': local(filhos[0].tag) if filhos else 'fade', 'dur_ms': dur}
    if filhos:
        f = filhos[0]
        attrs = {local(k): v for k, v in f.attrib.items()}
        if attrs:
            out['opcoes'] = attrs
    if trans.get('advTm'):
        out['auto_ms'] = int(trans.get('advTm'))
    return out


def animacoes_de(raiz):
    cont = collections.Counter()
    tm = raiz.find(P + 'timing')
    if tm is None:
        return []
    for ctn in tm.iter(P + 'cTn'):
        cls = ctn.get('presetClass')
        if cls:
            pid = int(ctn.get('presetID', 0))
            cont[NOMES_ANIM.get((cls, pid), '%s#%d' % (cls, pid))] += 1
    return [{'efeito': k, 'vezes': v} for k, v in cont.most_common()]


# ---------- análise do Morph ----------

def centro(xf, W, H):
    return ((xf['x'] + xf['w'] / 2) / W, (xf['y'] + xf['h'] / 2) / H)


def area(xf, W, H):
    return max(xf['w'], 1) * max(xf['h'], 1) / float(W * H)


def fora(xf, W, H):
    cx, cy = centro(xf, W, H)
    if xf['x'] + xf['w'] <= 0:
        return 'esquerda'
    if xf['x'] >= W:
        return 'direita'
    if xf['y'] + xf['h'] <= 0:
        return 'cima'
    if xf['y'] >= H:
        return 'baixo'
    return None


def lado(dx, dy):
    if abs(dx) >= abs(dy):
        return 'para a direita' if dx > 0 else 'para a esquerda'
    return 'para baixo' if dy > 0 else 'para cima'


def rotulo(o):
    if o['texto'] and e_lorem(o['texto']):
        return 'bloco de texto'
    if o['texto']:
        return '"%s"' % o['texto'][:40]
    return '%s "%s"' % (o['tipo'], o['nome'][:30])


def casar(a, b):
    """Casa os objetos de dois slides como o Morph faz: nome igual, depois mesma imagem, depois mesmo texto."""
    pares, usados_a, usados_b = [], set(), set()
    por_nome = collections.defaultdict(list)
    for j, o in enumerate(b):
        por_nome[o['nome']].append(j)
    for i, o in enumerate(a):
        for j in por_nome.get(o['nome'], []):
            if j not in usados_b and o['tipo'] == b[j]['tipo']:
                pares.append((i, j)); usados_a.add(i); usados_b.add(j); break
    for chave in ('img', 'texto'):
        for i, o in enumerate(a):
            if i in usados_a:
                continue
            k = o['blips'][0][0] if chave == 'img' and o['blips'] else (o['texto'] if chave == 'texto' else None)
            if not k:
                continue
            for j, p_ in enumerate(b):
                if j in usados_b:
                    continue
                kb = p_['blips'][0][0] if chave == 'img' and p_['blips'] else (p_['texto'] if chave == 'texto' else None)
                if kb == k:
                    pares.append((i, j)); usados_a.add(i); usados_b.add(j); break
    return pares, [i for i in range(len(a)) if i not in usados_a], [j for j in range(len(b)) if j not in usados_b]


def analisar_morph(a, b, W, H):
    a = [o for o in a if o['xf']]
    b = [o for o in b if o['xf']]
    pares, saem, entram = casar(a, b)
    mov = []
    for i, j in pares:
        oa, ob = a[i], b[j]
        ca, cb = centro(oa['xf'], W, H), centro(ob['xf'], W, H)
        dx, dy = cb[0] - ca[0], cb[1] - ca[1]
        esc = math.sqrt(area(ob['xf'], W, H) / area(oa['xf'], W, H))
        asp_a = oa['xf']['w'] / max(oa['xf']['h'], 1)
        asp_b = ob['xf']['w'] / max(ob['xf']['h'], 1)
        m = {'obj': rotulo(ob), 'tipo': ob['tipo'], 'dx': round(dx, 3), 'dy': round(dy, 3), 'escala': round(esc, 2),
             'giro': round(ob['xf']['rot'] - oa['xf']['rot'], 1), 'deforma': round(asp_b / asp_a, 2) if asp_a else 1,
             'area_final': round(area(ob['xf'], W, H), 3)}
        if oa['cor'] != ob['cor'] and oa['cor'] and ob['cor']:
            m['cor'] = [oa['cor'], ob['cor']]
        if oa['texto'] != ob['texto'] and oa['texto'] and ob['texto']:
            m['texto_muda'] = True
        if fora(oa['xf'], W, H) and not fora(ob['xf'], W, H):
            m['entra_de'] = fora(oa['xf'], W, H)
        if fora(ob['xf'], W, H) and not fora(oa['xf'], W, H):
            m['sai_para'] = fora(ob['xf'], W, H)
        parado = abs(dx) < 0.01 and abs(dy) < 0.01 and abs(esc - 1) < 0.03 and abs(m['giro']) < 1 and abs(m['deforma'] - 1) < 0.03 and 'cor' not in m and 'texto_muda' not in m
        m['parado'] = parado
        mov.append(m)
    ativos = [m for m in mov if not m['parado']]
    fam = []
    grandes = [m for m in ativos if m['escala'] >= 1.8 and m['area_final'] >= 0.45]
    if grandes:
        fam.append('zoom-mergulho')
    if ativos and sum(1 for m in ativos if m['escala'] <= 0.6) >= max(1, len(ativos) * 0.5):
        fam.append('zoom-recuo')
    desl = [m for m in ativos if math.hypot(m['dx'], m['dy']) > 0.1 and 0.85 < m['escala'] < 1.18]
    if len(desl) >= 2:
        vs = [(m['dx'], m['dy']) for m in desl]
        mx, my = sum(v[0] for v in vs) / len(vs), sum(v[1] for v in vs) / len(vs)
        if all(math.hypot(v[0] - mx, v[1] - my) < 0.08 for v in vs) and len(desl) >= 0.6 * len(ativos):
            fam.append('panorama')
        elif len(desl) >= 3:
            fam.append('reorganizar')
    if any('entra_de' in m or 'sai_para' in m for m in ativos):
        fam.append('voo')
    if any(abs(m['giro']) >= 15 for m in ativos):
        fam.append('giro')
    if any(abs(m['deforma'] - 1) > 0.35 or 'cor' in m for m in ativos):
        fam.append('transformacao')
    if any(m.get('texto_muda') or (m['tipo'] == 'texto' and (abs(m['escala'] - 1) > 0.2 or math.hypot(m['dx'], m['dy']) > 0.1)) for m in ativos):
        fam.append('texto')
    if len(pares) <= 1 and (len(saem) + len(entram)) >= 3:
        fam.append('troca')
    if not fam and not ativos:
        fam.append('so-entradas' if entram else 'estatico')
    destaques = sorted(ativos, key=lambda m: -(abs(math.log(max(m['escala'], 0.01))) * 2 + math.hypot(m['dx'], m['dy']) + abs(m['giro']) / 90))[:3]
    frases = []
    for m in destaques:
        partes = []
        if m['escala'] >= 1.15:
            partes.append('cresce %sx' % num(m['escala']))
        elif m['escala'] <= 0.87:
            partes.append('encolhe para %d%%' % round(m['escala'] * 100))
        if 'entra_de' in m:
            partes.append('entra vindo de fora (%s)' % m['entra_de'])
        elif 'sai_para' in m:
            partes.append('sai da tela (%s)' % m['sai_para'])
        elif math.hypot(m['dx'], m['dy']) > 0.05:
            partes.append('vai %s' % lado(m['dx'], m['dy']))
        if abs(m['giro']) >= 15:
            partes.append('gira %d°' % round(m['giro']))
        if abs(m['deforma'] - 1) > 0.35:
            partes.append('muda de proporção')
        if 'cor' in m:
            partes.append('troca de cor %s→%s' % tuple(m['cor']))
        if m.get('texto_muda'):
            partes.append('o texto muda')
        if m['area_final'] >= 0.85:
            partes.append('termina ocupando a tela')
        if partes:
            frases.append('%s %s' % (m['obj'], ', '.join(partes)))
    if entram:
        frases.append('%d objeto(s) novo(s) surgem' % len(entram))
    if saem:
        frases.append('%d objeto(s) somem' % len(saem))
    return {'familias': fam, 'casados': len(pares), 'parados': len(mov) - len(ativos), 'entram': len(entram), 'saem': len(saem),
            'resumo': '; '.join(frases) or 'sem mudança visível de posição', 'objetos': ativos[:12]}


# ---------- mídia ----------

def info_imagem(dados, sha, ext):
    from PIL import Image
    out = {}
    try:
        im = Image.open(io.BytesIO(dados))
        out['w'], out['h'] = im.size
        im.draft('RGB', (TAM_PREVIA * 2, TAM_PREVIA * 2))
        im.load()
        tem_alfa = im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info)
        if tem_alfa:
            im = im.convert('RGBA')
            pequeno = im.resize((48, 48))
            alfa = pequeno.getchannel('A').getdata()
            out['transparencia'] = round(sum(1 for v in alfa if v < 16) / float(len(alfa)), 2)
        else:
            im = im.convert('RGB')
        media = im.convert('RGB').resize((1, 1)).getpixel((0, 0))
        out['cor_media'] = '#%02X%02X%02X' % media
        prev = im.copy()
        prev.thumbnail((TAM_PREVIA, TAM_PREVIA))
        if tem_alfa and out.get('transparencia', 0) > 0.02:
            nome = sha + '.png'
            caminho = os.path.join(PREVIAS, nome)
            if not os.path.exists(caminho):
                prev.quantize(256).save(caminho, optimize=True)
        else:
            nome = sha + '.jpg'
            caminho = os.path.join(PREVIAS, nome)
            if not os.path.exists(caminho):
                prev.convert('RGB').save(caminho, quality=72, optimize=True)
        out['previa'] = 'acervo/previas/' + nome
    except Exception as e:
        out['erro'] = str(e)[:80]
    return out


def info_video(dados, sha, ext):
    out = {}
    with tempfile.TemporaryDirectory() as tmp:
        arq = os.path.join(tmp, 'v' + ext)
        open(arq, 'wb').write(dados)
        try:
            pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height:format=duration',
                                 '-of', 'json', arq], capture_output=True, timeout=60)
            j = json.loads(pr.stdout or b'{}')
            st = (j.get('streams') or [{}])[0]
            out['w'], out['h'] = st.get('width'), st.get('height')
            out['dur_s'] = round(float(j.get('format', {}).get('duration', 0)), 1)
            nome = sha + '.jpg'
            caminho = os.path.join(PREVIAS, nome)
            if not os.path.exists(caminho):
                subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(min(1.0, out['dur_s'] / 3)), '-i', arq, '-frames:v', '1',
                                '-vf', 'scale=%d:-2' % TAM_PREVIA, caminho], capture_output=True, timeout=120)
            if os.path.exists(caminho):
                out['previa'] = 'acervo/previas/' + nome
        except Exception as e:
            out['erro'] = str(e)[:80]
    return out


# ---------- por arquivo ----------

def processar(arq, did):
    z = zipfile.ZipFile(os.path.join(PPTX, arq))
    nomes = set(z.namelist())
    pres = xml(z, 'ppt/presentation.xml')
    sz = pres.find(P + 'sldSz')
    W, H = int(sz.get('cx')), int(sz.get('cy'))
    rels_pres = ler_rels(z, 'ppt/presentation.xml')
    lista = pres.find(P + 'sldIdLst')
    partes = [rels_pres[s.get(R + 'id')][1] for s in (lista if lista is not None else [])]
    temas = sorted(n for n in nomes if re.match(r'ppt/theme/theme\d+\.xml$', n))
    tema = tema_cores(z, temas[0]) if temas else {}
    cache_ph = {}

    def ph(parte):
        if parte not in cache_ph:
            cache_ph[parte] = placeholders(z, parte) if parte else {}
        return cache_ph[parte]

    slides, transicoes, ocorr, svg_fallback = [], [], collections.defaultdict(list), {}
    objetos_por_slide = []
    fontes_deck = collections.Counter()
    cores_deck = collections.Counter()
    fundos = collections.Counter()
    for k, parte in enumerate(partes, 1):
        raiz = xml(z, parte)
        if raiz is None:
            objetos_por_slide.append([]); continue
        rels = ler_rels(z, parte)
        layout = next((t for (tp, t) in rels.values() if tp.endswith('/slideLayout')), None)
        master = next((t for (tp, t) in ler_rels(z, layout).values() if tp.endswith('/slideMaster')), None) if layout else None
        arvore = raiz.find('.//' + P + 'spTree')
        itens = [descrever_item(it, tema, rels, ph(layout), ph(master)) for it in (itens_da_arvore(arvore) if arvore is not None else [])]
        objetos_por_slide.append(itens)
        fontes = collections.Counter(t for t in (e.get('typeface') for e in raiz.iter(A + 'latin')) if t and not t.startswith('+'))
        fontes_deck.update(fontes)
        cores = collections.Counter()
        for sf in raiz.iter(A + 'solidFill'):
            c = cor_de(sf, tema)
            if c:
                cores[c] += 1
        for gs in raiz.iter(A + 'gs'):
            c = cor_de(gs, tema)
            if c:
                cores[c] += 1
        fundo = None
        for fonte_bg in (raiz, xml(z, layout) if layout else None, xml(z, master) if master else None):
            if fonte_bg is None:
                continue
            bg = fonte_bg.find('.//' + P + 'bg')
            if bg is not None:
                sf = bg.find('.//' + A + 'solidFill')
                if bg.find('.//' + A + 'blipFill') is not None:
                    fundo = 'imagem'
                elif sf is not None:
                    fundo = cor_de(sf, tema)
                elif bg.find(P + 'bgRef') is not None:
                    ref = bg.find(P + 'bgRef')
                    fundo = cor_de(ref, tema)
                if fundo:
                    break
        # imagem cobrindo o slide também conta como fundo
        grandes = [o for o in itens if o['blips'] and o['xf'] and area(o['xf'], W, H) >= 0.9]
        if grandes and fundo != 'imagem':
            fundo = 'imagem' if not fundo else fundo + '+imagem'
        fundos[fundo or 'nenhum'] += 1
        cores_deck.update({c: n for c, n in cores.items()})
        if fundo and fundo.startswith('#'):
            cores_deck[fundo[:7]] += 6
        oculto = raiz.get('show') == '0'
        trans = transicao_de(raiz)
        anim = animacoes_de(raiz)
        textos = sorted([o for o in itens if o['texto']], key=lambda o: -(o['tam'] or 0))
        reais = [o for o in textos if not e_lorem(o['texto'])]
        cont = collections.Counter(o['tipo'] for o in itens)
        for o in itens:
            for rid, svgrid in o['blips']:
                alvo = rels.get(rid, (None, None))[1]
                if alvo:
                    papel = 'fundo' if o['xf'] and area(o['xf'], W, H) >= 0.9 else ('mascara' if o['mascara'] else o['tipo'])
                    ocorr[alvo].append({'slide': k, 'papel': papel, 'area': round(area(o['xf'], W, H), 3) if o['xf'] else None})
                if svgrid and rels.get(svgrid, (None, None))[1]:
                    svg_alvo = rels[svgrid][1]
                    ocorr[svg_alvo].append({'slide': k, 'papel': 'icone/vetor', 'area': round(area(o['xf'], W, H), 3) if o['xf'] else None})
                    if alvo:
                        svg_fallback[alvo] = svg_alvo
        for rid, (tp, alvo) in rels.items():
            if alvo and alvo.startswith('ppt/media/') and alvo not in ocorr:
                ocorr[alvo].append({'slide': k, 'papel': 'outro', 'area': None})
            elif alvo and alvo.startswith('ppt/media/') and not any(x['slide'] == k for x in ocorr[alvo]):
                ocorr[alvo].append({'slide': k, 'papel': 'outro', 'area': None})
        slides.append({
            'deck': did, 'n': k, 'oculto': oculto, 'thumb': '_catalogo/miniaturas/%s/%02d.jpg' % (did, k),
            'titulo': (reais[0]['texto'][:120] if reais else None),
            'textos': [o['texto'][:160] for o in reais[:8]],
            'objetos': dict(cont), 'n_objetos': len(itens),
            'fontes': [f for f, _ in fontes.most_common(4)],
            'cores': [c for c, _ in cores.most_common(6)], 'fundo': fundo,
            'transicao': trans, 'animacoes': anim,
        })
        if trans:
            reg = {'deck': did, 'de': k - 1 if k > 1 else None, 'para': k, 'tipo': trans['tipo'], 'dur_ms': trans.get('dur_ms')}
            if trans.get('opcoes'):
                reg['opcoes'] = trans['opcoes']
            if trans['tipo'] == 'morph' and k > 1:
                reg.update(analisar_morph(objetos_por_slide[k - 2], itens, W, H))
            transicoes.append(reg)
    # mídia: hash, dimensões, prévias
    midias = []
    for parte in sorted(n for n in nomes if n.startswith('ppt/media/')):
        dados = z.read(parte)
        ext = os.path.splitext(parte)[1].lower()
        sha = hashlib.sha1(dados).hexdigest()[:16]
        reg = {'id': sha, 'ext': ext, 'bytes': len(dados), 'deck': did, 'parte': parte, 'usos': ocorr.get(parte, [])}
        if parte in svg_fallback:
            reg['fallback_de'] = hashlib.sha1(z.read(svg_fallback[parte])).hexdigest()[:16]
        if ext in IMAGEM:
            reg['tipo'] = 'imagem'
            reg.update(info_imagem(dados, sha, ext))
        elif ext == '.svg':
            reg['tipo'] = 'svg'
            destino = os.path.join(SVG, sha + '.svg')
            if not os.path.exists(destino):
                open(destino, 'wb').write(dados)
            reg['arquivo'] = 'acervo/svg/%s.svg' % sha
            m = re.search(rb'viewBox="([\d.\s-]+)"', dados[:2000])
            if m:
                reg['viewbox'] = m.group(1).decode()
        elif ext in VIDEO:
            reg['tipo'] = 'video'
            reg.update(info_video(dados, sha, ext))
        elif ext == '.glb':
            reg['tipo'] = '3d'
        elif ext in ('.mp3', '.wav', '.m4a'):
            reg['tipo'] = 'audio'
        else:
            reg['tipo'] = 'outro'
        midias.append(reg)
    # paleta do arquivo: junta tons quase iguais
    paleta = []
    for c, n in cores_deck.most_common(40):
        rgb = tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))
        for p_ in paleta:
            if sum((a_ - b_) ** 2 for a_, b_ in zip(rgb, p_['rgb'])) < 24 ** 2:
                p_['peso'] += n; break
        else:
            paleta.append({'hex': c, 'rgb': rgb, 'peso': n})
    total = float(sum(p_['peso'] for p_ in paleta) or 1)
    paleta = [{'hex': p_['hex'], 'peso': round(p_['peso'] / total, 2)} for p_ in sorted(paleta, key=lambda p_: -p_['peso'])[:8]]
    proporcao = W / float(H)
    deck = {'id': did, 'arq': arq, 'largura_emu': W, 'altura_emu': H,
            'proporcao': '16:9' if abs(proporcao - 16 / 9) < 0.05 else '9:16' if abs(proporcao - 9 / 16) < 0.05 else '4:5' if abs(proporcao - 0.8) < 0.03 else '1:1' if abs(proporcao - 1) < 0.05 else '4:3' if abs(proporcao - 4 / 3) < 0.05 else '%.2f' % proporcao,
            'paleta': paleta, 'fundos': dict(fundos.most_common(5)),
            'fontes': [{'nome': f, 'usos': n} for f, n in fontes_deck.most_common(8)],
            'tema': {k: v for k, v in tema.items() if k.startswith(('dk', 'lt', 'accent'))},
            'transicoes': dict(collections.Counter(t['tipo'] for t in transicoes)),
            'familias_morph': dict(collections.Counter(f for t in transicoes for f in t.get('familias', []))),
            'midias': dict(collections.Counter(m['tipo'] for m in midias))}
    return deck, slides, transicoes, midias


def main():
    os.makedirs(DADOS, exist_ok=True); os.makedirs(PREVIAS, exist_ok=True); os.makedirs(SVG, exist_ok=True)
    ids = {nfc(k): v for k, v in json.load(open(os.path.join(RAIZ, '_catalogo', 'miniaturas', 'ids.json'))).items()}
    arquivos = sorted(nfc(f) for f in os.listdir(PPTX) if f.lower().endswith('.pptx'))
    so = set(sys.argv[1:])
    if so:
        arquivos = [f for f in arquivos if ids[f] in so or f in so]
    res = {}
    with ProcessPoolExecutor(max(2, (os.cpu_count() or 4) - 2)) as ex:
        futs = {ex.submit(processar, f, ids[f]): f for f in arquivos}
        for i, fu in enumerate(as_completed(futs), 1):
            f = futs[fu]
            try:
                res[f] = fu.result()
            except Exception as e:
                print('ERRO', f, repr(e)[:200], flush=True)
            if i % 50 == 0:
                print('%d/%d' % (i, len(arquivos)), flush=True)
    sufixo = '.parcial' if so else ''
    with open(os.path.join(DADOS, 'decks.jsonl' + sufixo), 'w') as fd, open(os.path.join(DADOS, 'slides.jsonl' + sufixo), 'w') as fs, \
            open(os.path.join(DADOS, 'transicoes.jsonl' + sufixo), 'w') as ft:
        for f in arquivos:
            if f not in res:
                continue
            deck, slides, trans, _ = res[f]
            fd.write(json.dumps(deck, ensure_ascii=False) + '\n')
            for s in slides:
                fs.write(json.dumps(s, ensure_ascii=False) + '\n')
            for t in trans:
                ft.write(json.dumps(t, ensure_ascii=False) + '\n')
    # mídia: um registro por arquivo único, juntando onde aparece
    unicos = collections.OrderedDict()
    for f in arquivos:
        if f not in res:
            continue
        for m in res[f][3]:
            u = unicos.get(m['id'])
            usos = [{'deck': m['deck'], **x} for x in m['usos']] or [{'deck': m['deck'], 'slide': None, 'papel': 'sem uso'}]
            if u is None:
                m = dict(m); m['usos'] = usos; m['origem'] = {'arq': f, 'parte': m.pop('parte')}; m.pop('deck')
                unicos[m['id']] = m
            else:
                u['usos'].extend(usos)
    with open(os.path.join(DADOS, 'midia.jsonl' + sufixo), 'w') as fm:
        for m in unicos.values():
            fm.write(json.dumps(m, ensure_ascii=False) + '\n')
    print('decks', len(res), 'slides', sum(len(r[1]) for r in res.values()), 'transições', sum(len(r[2]) for r in res.values()),
          'mídias únicas', len(unicos))


if __name__ == '__main__':
    main()
