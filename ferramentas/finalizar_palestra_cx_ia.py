#!/usr/bin/env python3
"""Monta a entrega visual dos 24 slides sem reescrever conteúdo ou falas."""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / '_saida/palestra-cx-ia-editorial'
DEST = ROOT / '_saida/palestra-cx-ia-codex'
KIT = ROOT / '_originais/growmate-livros/series/livros-kit'


def icon(name, cls='icone', style=''):
    # Pictogramas específicos reconstruídos com o traço do kit para os setores da fala.
    specific = {
        'car': '<path d="M3 15V9l2-5h14l2 5v6M3 9h18M3 15h18M6 12h2M16 12h2M5 15v4M19 15v4"/>',
        'cup': '<path d="M4 9h12v6a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5zM16 10h2a3 3 0 0 1 0 6h-2M3 22h16M8 2v3M12 2v3"/>',
        'tooth': '<path d="M12 5c-3-2-8-3-8 3 0 5 2 13 5 13 2 0 1-7 3-7s1 7 3 7c3 0 5-8 5-13 0-6-5-5-8-3z"/>',
        'scissors': '<circle cx="5" cy="6" r="3"/><circle cx="5" cy="18" r="3"/><path d="M7.5 7.5L21 21M7.5 16.5L21 3M14 10l-3 4"/>',
        'wash': '<path d="M3 16v-4l2-4h14l2 4v4M3 12h18M3 16h18M5 16v3M19 16v3M8 2v3M12 1v4M16 2v3"/>',
    }
    if name in specific:
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
               'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
               + specific[name] + '</svg>')
    else:
        svg = (KIT / 'icones' / (name + '.svg')).read_text().strip()
    return svg.replace('<svg ', f'<svg class="{cls}" aria-hidden="true" focusable="false" style="{style}" ', 1)


def art(markup, cls='', morph=''):
    data = f' data-m="{morph}"' if morph else ''
    return (f'<svg class="recurso {cls}" aria-hidden="true" focusable="false" '
            f'width="1920" height="1080" viewBox="0 0 1920 1080"{data} '
            'xmlns="http://www.w3.org/2000/svg">' + markup + '</svg>')


def stamp_icon(name, x, y, size=64):
    svg = icon(name)
    return (f'<g transform="translate({x} {y})"><svg class="icone" width="{size}" height="{size}" '
            'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round">'
            + svg.split('>', 1)[1].rsplit('</svg>', 1)[0] + '</svg></g>')


def finish():
    DEST.mkdir(exist_ok=True)
    for folder in ['fontes', 'img']:
        shutil.copytree(BASE / folder, DEST / folder, dirs_exist_ok=True)
    for file in ['motor.css', 'motor.js', 'visual.css', 'imagens.json']:
        shutil.copy2(BASE / file, DEST / file)
    shutil.copy2(KIT / 'assets/fonts/jetbrains-mono-latin.woff2', DEST / 'fontes/jetbrains-mono-latin.woff2')
    source = (BASE / 'palestra.html').read_text()
    source = source.replace('</head>', '<link rel="stylesheet" href="recursos.css">\n</head>')
    slides = re.findall(r'<section\b.*?</section>', source, re.S)
    assert len(slides) == 24
    before = list(slides)
    additions = {}

    # Agenda: ícones usam os mesmos cliques das paradas existentes.
    agenda = iter(['heart', 'spark', 'link', 'tool', 'chart'])
    slides[3] = re.sub(r'(<div class="parada"[^>]*>)',
                       lambda m: m[1] + icon(next(agenda), 'agenda-icone'), slides[3])

    # Os pontos espalhados se tornam uma linha contínua e depois três momentos.
    additions[7] = art('<path class="fio-suave" d="M188 818H1763"/>', 'rede-contatos', 'percurso-cx')
    nodes = [200, 417, 634, 851, 1068, 1285, 1502, 1719]
    symbols = ['search', 'users', 'chat', 'store', 'cart', 'heart', 'thumb', 'refresh']
    marks = ''.join(
        f'<path class="fio-fino" d="M{x} 610V660"/>'
        f'<circle cx="{x}" cy="565" r="49" class="estacao"/>'
        + stamp_icon(name, x - 24, 541, 48)
        for x, name in zip(nodes, symbols))
    additions[8] = art(marks, 'estacoes-jornada', 'percurso-cx')
    for step, name in enumerate(['search', 'cart', 'heart'], 1):
        pat = rf'(<div class="t"[^>]*data-passo="{step}"[^>]*>)'
        slides[8], count = re.subn(pat, lambda m: m[1] + icon(name, 'momento-icone'), slides[8], count=1)
        assert count == 1
    additions[9] = art(''.join(
        f'<rect class="regiao-jornada" x="{x}" y="370" width="540" height="590" rx="24"/>'
        for x in [112, 690, 1268]), 'fases-jornada', 'percurso-cx')

    # A viagem é ilustrativa: a trilha não pretende representar um mapa geográfico.
    additions[10] = art('<circle cx="1660" cy="380" r="58" class="halo"/>'
                        '<circle cx="1660" cy="380" r="88" class="halo fino"/>', 'destino')

    # Mapa dos seis caminhos: o pictograma acompanha o clique do próprio cartão.
    cards = iter(['users', 'search', 'star', 'megaphone', 'eye', 'spark'])
    slides[11] = re.sub(r'(<div class="card"[^>]*>)',
                        lambda m: m[1] + icon(next(cards), 'caminho-icone'), slides[11])
    additions[12] = art('<path class="fio-suave" d="M950 450V860M890 450H1010M890 655H1010M890 860H1010"/>', 'convergencia')

    # Conversa, avaliações e IA mantêm as interfaces e todos os textos originais.
    additions[13] = art('<path class="fio-suave" d="M1100 576H1640Q1760 576 1760 620"/>'
                        '<circle class="marcador" cx="1100" cy="576" r="7"/>', 'linha-conversa')
    additions[14] = art('<path class="fio-suave" d="M1080 650V850"/>'
                        '<circle class="marcador" cx="1080" cy="650" r="7"/>'
                        '<circle class="marcador" cx="1080" cy="850" r="7"/>', 'linha-avaliacoes')
    additions[16] = art(stamp_icon('door', 1140, 790, 92)
                        + '<path class="fio-suave" d="M1260 842H1760"/>'
                        '<circle class="marcador" cx="1760" cy="842" r="11"/>', 'porta-ia')
    additions[17] = art('<rect x="142" y="820" width="628" height="188" rx="22" class="faixa-pre"/>', 'regiao-pre')

    # Círculos e lupa: foco no momento da descoberta, sem acrescentar um novo modelo.
    lens = ('<circle cx="1460" cy="466" r="244" class="orbita"/>'
            '<circle cx="1460" cy="466" r="176" class="anel"/>'
            '<circle cx="1460" cy="466" r="118" class="lente"/>'
            '<path d="M1545 551L1642 648" class="cabo-lupa"/>'
            + stamp_icon('search', 1406, 412, 108)
            + '<circle cx="1460" cy="222" r="17" class="marcador"/>'
            '<circle cx="1216" cy="466" r="13" class="marcador"/>'
            '<circle cx="1650" cy="313" r="13" class="marcador"/>')
    additions[18] = art(lens, 'lupa-descoberta')

    # Os símbolos distinguem os setores já presentes na fala.
    sectors = iter(['cup', 'tooth', 'spark', 'scissors', 'car', 'wash'])
    slides[18] = re.sub(r'(<div class="t display apagado"[^>]*>)',
                        lambda m: m[1] + icon(next(sectors), 'setor-icone'), slides[18])

    # A auditoria final tem três sinais que acompanham os grupos de foco existentes.
    questions = iter(['search', 'phone', 'spark'])
    slides[21] = re.sub(r'(<div class="pergunta"[^>]*>)',
                        lambda m: m[1] + icon(next(questions), 'pergunta-icone'), slides[21])
    additions[23] = art(stamp_icon('bookmark', 1600, 770, 126)
                        + '<path class="fio-suave" d="M1600 941H1740"/>', 'levar')
    additions[24] = art('<path class="fio-final" d="M112 970H1330M1490 970H1808"/>'
                        '<path class="barreira" d="M1408 934V1006"/>'
                        '<circle cx="1808" cy="970" r="10" fill="currentColor"/>', 'limite')

    for n, svg in additions.items():
        slides[n-1] = slides[n-1].replace('<aside class="notas">', svg + '\n  <aside class="notas">')
    for a, b in zip(before, slides):
        source = source.replace(a, b, 1)
    (DEST / 'palestra.html').write_text(source)
    (DEST / '.gitignore').write_text('_ver/\nestudo/\nimg/\n')
    study = DEST / 'estudo'
    study.mkdir(exist_ok=True)
    shutil.copy2(BASE / 'estudo/conferir.py', study / 'conferir.py')
    print('Entrega montada:', DEST)
    print('Slides:', len(slides), '| composições gráficas novas:', len(additions))


if __name__ == '__main__':
    finish()
