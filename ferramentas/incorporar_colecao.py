#!/usr/bin/env python3
"""Coleções de PDFs de terceiros (Perestroika, SOAP): páginas para leitura, fichas visuais do espaço e conferência do método.

Uso: app/.venv/bin/python -I ferramentas/incorporar_colecao.py <coleção> <comando>

  paginas   renderiza cada PDF em <origem>/_trabalho/: páginas (1600 px no lado maior), texto por página e folhas de
            contato com 6 páginas numeradas; grava também o vocabulário e o inventário para os leitores.
  conferir  [slug...] confere a leitura dos agentes antes de montar.
  montar    lê a leitura dos agentes (<origem>/_trabalho/leitura/<slug>.jsonl e .md) e grava dados/<coleção>/decks.jsonl
            (PDF = apresentação, página selecionada = slide), copia as páginas para _originais/<coleção>/paginas/ e os
            estudos para _referencias/<coleção>/.
  pranchas  uma prancha por apresentação em app/.runtime/qa/<coleção>/, para conferir antes de importar.
  validar   fichas e guias do método em biblioteca/metodos/<coleção>/.

Importar: ./app/run.sh import-decks --workspace ID --folder dados/<coleção>.
Material de terceiros: entra com reusable=false, só como referência; as pastas de origem ficam fora do Git e dos pacotes.
"""
import json
import re
import shutil
import sqlite3
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DASHES = (chr(0x2014), chr(0x2013))

# Nome da apresentação no mapa; o título que a leitura deu ao deck fica na descrição.
PERESTROIKA_TITLES = {
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

# Os nomes dos arquivos da SOAP perderam os acentos ("r_pidos"): cada um ganha um slug legível e o título do mapa.
SOAP_FILES = {
    'Checklist_da_apresentaao_impactante': ('checklist-apresentacao-impactante', 'Checklist da apresentação impactante'),
    'Checklist_de_Qualidade_SOAP': ('checklist-de-qualidade', 'Checklist de qualidade'),
    'Checklist_para_apresentar_um_projeto_importante': ('checklist-projeto-importante', 'Checklist para apresentar um projeto importante'),
    '10_Dicas_Poderosas_de_Linguagem_Corporal': ('linguagem-corporal-dicas', '10 dicas de linguagem corporal'),
    '10_erros_mais_comuns_de_linguagem_corporal_em_apresenta_Apresentacoes': ('linguagem-corporal-erros', '10 erros de linguagem corporal'),
    '10_formas_de_ilustrar_uma_apresenta_o': ('10-formas-de-ilustrar', '10 formas de ilustrar uma apresentação'),
    '10_sinais_de_que_a_sua_apresenta_o_est_chata_ou_foi_ineficiente': ('10-sinais-de-apresentacao-chata', '10 sinais de apresentação chata'),
    '11_passos_r_pidos_e_eficazes_para_criar_conte_do_de_apresenta_Apresentacoes': ('11-passos-de-conteudo', '11 passos para criar o conteúdo'),
    '12_formas_de_impactar_a_audi_ncia_com_a_diagrama_o': ('12-formas-de-diagramacao', '12 formas de impactar com a diagramação'),
    '15_erros_mais_comuns_em_apresenta_Apresentacoes': ('15-erros-em-apresentacoes', '15 erros mais comuns em apresentações'),
    '5_pecados_capitais_da_facilita_o_da_aprendizagem': ('5-pecados-da-facilitacao', '5 pecados capitais da facilitação'),
    '9_dicas_para_ensaiar_para_sua_apresenta_o': ('9-dicas-de-ensaio', '9 dicas para ensaiar'),
    '9_recursos_de_narrativa_para_chamar_a_aten_o_da_audi_ncia': ('9-recursos-de-narrativa', '9 recursos de narrativa'),
    'A_an_lise_SWOT_agora_TOSW': ('swot-tosw', 'Análise SWOT, agora TOSW'),
    'A_anatomia_do_Palestrante': ('anatomia-do-palestrante', 'Anatomia do palestrante'),
    'A_credibilidade_do_l_der_na_constru_o_de_uma_cultura_de_confian_a': ('credibilidade-do-lider', 'Credibilidade do líder e cultura de confiança'),
    'Arquetipos_de_Jung_nas_apresenta_es': ('arquetipos-de-jung', 'Arquétipos de Jung nas apresentações'),
    'Audi_ncia_dicas_para_construir_apresenta_es_com_foco_no_espectador': ('audiencia', 'Audiência: foco no espectador'),
    'Como_aumentar_suas_chances_de_sucesso_em_uma_concorr_ncia': ('concorrencia', 'Como vencer uma concorrência'),
    'Como_fazer_uma_apresenta_o_para_investidores_8211_SOAP_e_Endeavor': ('investidores', 'Apresentação para investidores (com a Endeavor)'),
    'Como_realizar_um_evento_no_estado_da_arte': ('evento-estado-da-arte', 'Evento no estado da arte'),
    'Como_se_destacar_como_apresentador': ('destacar-como-apresentador', 'Como se destacar como apresentador'),
    'Como_ser_mais_seguro_ao_se_apresentar': ('seguranca-ao-apresentar', 'Como ser mais seguro ao apresentar'),
    'Comunica_o_como_aliada_para_atrair_e_reter_talentos': ('atrair-e-reter-talentos', 'Comunicação para atrair e reter talentos'),
    'Comunica_o_interna': ('comunicacao-interna', 'Comunicação interna'),
    'Comunica_o_no_momento_de_venda': ('comunicacao-na-venda', 'Comunicação no momento de venda'),
    'Comunica_o_para_crian_as_e_adolescentes': ('comunicacao-criancas-adolescentes', 'Comunicação para crianças e adolescentes'),
    'Comunicaao_de_sucesso': ('comunicacao-de-sucesso', 'Comunicação de sucesso'),
    'Dicas_SOAP_2018': ('dicas-2018', 'Dicas SOAP 2018'),
    'Dicas_SOAP_2019': ('dicas-2019', 'Dicas SOAP 2019'),
    'E-book_Como_escrever_um_roteiro_vencedor_para_apresenta_es': ('roteiro-vencedor', 'Como escrever um roteiro vencedor'),
    'Feedback_8211_Dicas_para_melhorar_a_comunica_o_e_o_desempenho_da_sua_empresa': ('feedback', 'Feedback na empresa'),
    'Guia_completo_do_RH_8211_Parte_1': ('guia-rh-1', 'Guia completo do RH · Parte 1'),
    'Guia_completo_do_RH_8211_Parte_2': ('guia-rh-2', 'Guia completo do RH · Parte 2'),
    'Guia_completo_do_RH_8211_Parte_3': ('guia-rh-3', 'Guia completo do RH · Parte 3'),
    'Guia_Completo_do_RH_8211_Parte_4': ('guia-rh-4', 'Guia completo do RH · Parte 4'),
    'Guia_SOAP_para_uma_apresenta_o_institucional': ('apresentacao-institucional', 'Apresentação institucional'),
    'Guia_basico_de_ferramentas_do_PowerPoint_2013': ('powerpoint-2013', 'Ferramentas do PowerPoint 2013'),
    'Guia_para_avalia_o_de_resultados_em_treinamentos_corporativos': ('avaliacao-de-treinamentos', 'Avaliação de resultados em treinamentos'),
    'Guia_para_uma_apresenta_o_impactante': ('guia-apresentacao-impactante', 'Guia para uma apresentação impactante'),
    'Kit_SOAP_de_sobreviv_ncia_na_crise_8211_ASOAPCONFIAEMVOCE': ('kit-sobrevivencia-na-crise', 'Kit de sobrevivência na crise'),
    'Linguagem_visual_de_destaque_em_uma_apresenta_o': ('linguagem-visual-de-destaque', 'Linguagem visual de destaque'),
    'MOMENTOS_DECISIVOS_Conven_es': ('convencoes', 'Momentos decisivos: convenções'),
    'Manual_da_falta_de_tempo_em_apresenta_Apresentacoes': ('falta-de-tempo', 'Manual da falta de tempo'),
    'Neuromarketing': ('neuromarketing', 'Neuromarketing'),
    'O_papel_do_RH_em_2020': ('rh-em-2020', 'O papel do RH em 2020'),
    'Os_10_erros_de_elevator_pitch': ('elevator-pitch', '10 erros de elevator pitch'),
    'Os_10_mandamentos_do_apresentador': ('10-mandamentos', '10 mandamentos do apresentador'),
    'Os_Grandes_Mitos_Sobre_Apresenta_Apresentacoes': ('mitos', 'Os grandes mitos sobre apresentações'),
    'Por_que_sua_equipe_nem_sempre_te_conta_a_verdade': ('equipe-e-verdade', 'Por que a equipe não conta a verdade'),
    'Primeiro_cap_tulo_DETONE': ('detone-capitulo-1', 'DETONE · Primeiro capítulo'),
    'Prospec_o_e_Negocia_o_remota': ('prospeccao-remota', 'Prospecção e negociação remota'),
    'Refer_ncias_visuais_para_suas_apresenta_es': ('referencias-visuais', 'Referências visuais para apresentações'),
    'SOAP_Insights': ('insights', 'SOAP Insights'),
    'Tend_ncias_de_apresenta_es_2020': ('tendencias-2020', 'Tendências de apresentações 2020'),
    'Tend_ncias_em_apresenta_es_2018': ('tendencias-2018', 'Tendências de apresentações 2018'),
    'Voce_sabia_15_coisas_que_voce_precisa_saber_sobre_apresenta_Apresentacoes': ('15-coisas-sobre-apresentacoes', '15 coisas que você precisa saber'),
    'Whitepaper_como_sofrer_menos_ao_fazer_sua_apresenta_o': ('sofrer-menos', 'Como sofrer menos ao fazer sua apresentação'),
    'Presente_SOAP_2014': ('presente-2014', 'Presente SOAP 2014'),
    'Presentes_SOAP_2015': ('presente-2015', 'Presente SOAP 2015'),
    'Presente_SOAP_2016': ('presente-2016', 'Presente SOAP 2016'),
    'Presentes_SOAP_2017': ('presente-2017', 'Presente SOAP 2017'),
    'Template_Apresentacoes_com_Graficos': ('template-graficos', 'Template · Apresentações com gráficos'),
    'Template_Area_da_Saude': ('template-saude', 'Template · Área da saúde'),
    'Template_Bancos': ('template-bancos', 'Template · Bancos'),
    'Template_Clean_e_Moderno': ('template-clean-e-moderno', 'Template · Clean e moderno'),
    'Template_Conquistar_Recursos': ('template-conquistar-recursos', 'Template · Conquistar recursos'),
    'Template_Copa_do_Mundo': ('template-copa-do-mundo', 'Template · Copa do Mundo'),
    'Template_Curriculo': ('template-curriculo', 'Template · Currículo'),
    'Template_Educacao': ('template-educacao', 'Template · Educação'),
    'Template_Integracao_Novos_Funcionarios': ('template-integracao', 'Template · Integração de novos funcionários'),
    'Template_Lancamento_de_Produto': ('template-lancamento-de-produto', 'Template · Lançamento de produto'),
    'Template_RH': ('template-rh', 'Template · RH'),
    'Template_Venda_de_Solucoes': ('template-venda-de-solucoes', 'Template · Venda de soluções'),
    'Template_SOAP_aprovacao_de_projeto': ('template-aprovacao-de-projeto', 'Template · Aprovação de projeto'),
    'Analise_de_viabilidade_do_projeto': ('planilha-viabilidade-de-projeto', 'Planilha · Viabilidade de projeto'),
}

# Termos encontrados na leitura dos templates; entram nas observações de uso das fichas (todas seguem reusable=false).
GIFT = ('A SOAP distribuiu este template como presente e libera copiar os elementos para as próprias apresentações '
        '("É só copiar e colar na sua apresentação"), sem licença formal nem permissão de redistribuição; as fotos vêm de '
        'bancos de imagens cujas licenças não acompanham o arquivo. Recrie a ideia em vez de reaproveitar as imagens.')
SOAP_CAUTIONS = {
    **{f'presente-{year}': GIFT for year in (2014, 2015, 2016, 2017)},
    'template-graficos': 'Template editável da SOAP ("fique à vontade para alterar cores, textos e fotos"), sem licença formal; '
                         'usa imagens de terceiros sem crédito (personagem de videogame, efígie de cédula). Recrie a ideia do gráfico.',
}

# Páginas que saíram com texto sobreposto na exportação pelo Keynote (o PowerPoint falha com erro -50 nesse arquivo).
# Ficam fora do espaço; as já importadas foram para a lixeira do espaço SOAP em 23/10/2026, a pedido do Cleiton.
SOAP_SKIP = {'template-graficos': {10, 16, 18, 22, 24, 40, 46}}

COLLECTIONS = {
    'perestroika': dict(label='Perestroika', source='_originais/perestroika', extra=(), what='PDF da Perestroika',
                        slugs={}, titles=PERESTROIKA_TITLES),
    # Templates em PowerPoint e o kit do zip são exportados para PDF em _originais/soap/_trabalho/pdf-templates/ e seguem como PDF.
    'soap': dict(label='SOAP', source='_originais/soap', extra=('_originais/soap/_trabalho/pdf-templates',), what='PDF da SOAP',
                 what_converted='Template da SOAP, exportado para PDF,', slugs={k: v[0] for k, v in SOAP_FILES.items()},
                 titles={v[0]: v[1] for v in SOAP_FILES.values()}, cautions=SOAP_CAUTIONS, skip=SOAP_SKIP),
}


class Collection:
    def __init__(self, name):
        self.name, self.cfg = name, COLLECTIONS[name]
        self.work = ROOT / self.cfg['source'] / '_trabalho'
        self.out = ROOT / 'dados' / name
        self.media = ROOT / '_originais' / name
        self.studies = ROOT / '_referencias' / name
        self.method = ROOT / 'biblioteca/metodos' / name


def clean(value):
    if isinstance(value, str):
        for dash in DASHES:
            value = value.replace(dash, ',' if dash == DASHES[0] else '-')
        return re.sub(r'\s+', ' ', value).strip()
    if isinstance(value, list):
        return [clean(v) for v in value]
    return value


def auto_slug(stem):
    s = unicodedata.normalize('NFD', stem).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def sources(c):
    """slug -> (PDF lido, arquivo de origem). Templates exportados apontam para o .ppt ou .pptx de origem."""
    found = {}
    folders = [(ROOT / c.cfg['source'], True)] + [(ROOT / x, False) for x in c.cfg['extra']]
    for folder, skip_work in folders:
        for p in sorted(folder.rglob('*.pdf')):
            if skip_work and '_trabalho' in p.parts:
                continue
            origin = p
            if not skip_work:
                origin = next((q for q in sorted((ROOT / c.cfg['source']).rglob(p.stem + '.*'))
                               if q.suffix.lower() in ('.ppt', '.pptx', '.xls', '.xlsx') and 'pdf-templates' not in q.parts), p)
            found[c.cfg['slugs'].get(p.stem) or auto_slug(p.stem)] = (p.relative_to(ROOT), origin.relative_to(ROOT))
    return found


def vocabulary():
    v = json.loads((ROOT / 'dados/vocabulario.json').read_text())
    ids = lambda k: {i['id'] if isinstance(i, dict) else i for i in v[k]['itens']}
    return dict(intencoes=ids('intencoes'), tecnicas=ids('tecnicas'), movimento=ids('movimentos'),
                estetica=ids('esteticas'), tom=ids('tons'))


def vocabulary_md():
    """Vocabulário do Repertório para os leitores, no mesmo formato usado na Perestroika."""
    v = json.loads((ROOT / 'dados/vocabulario.json').read_text())
    lines = ['# Vocabulário do Repertório (para as fichas visuais)', '', 'Use somente estes ids.', '']
    for key, field, head in (('intencoes', 'intencoes', '1 a 3, papel do slide na história'), ('tecnicas', 'tecnicas', '1 a 5'),
                             ('movimentos', 'movimento', '0 a 2; em PDF quase sempre `estatico`')):
        lines += [f'## {field} ({head})'] + [f"- `{i['id']}`: {i['def']}" for i in v[key]['itens']] + ['']
    for key, field, head in (('esteticas', 'estetica', '2 a 5'), ('tons', 'tom', '1 a 3')):
        lines += [f'## {field} ({head})', ', '.join(f'`{i}`' for i in v[key]['itens']), '']
    return '\n'.join(lines)


def paginas(c):
    """Páginas em JPG (1600 px no lado maior), texto por página e folhas de contato de 6 páginas numeradas."""
    import pymupdf
    from PIL import Image, ImageDraw, ImageFont
    try:
        face = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 18)
    except OSError:
        face = ImageFont.load_default()
    inventory = []
    for slug, (pdf, origin) in sorted(sources(c).items()):
        doc = pymupdf.open(ROOT / pdf)
        dest = c.work / 'paginas' / slug
        dest.mkdir(parents=True, exist_ok=True)
        texts, empty = [], 0
        for i, page in enumerate(doc, 1):
            text = re.sub(r'\s+', ' ', page.get_text()).strip()
            empty += len(text) < 20
            texts.append(f'=== p{i} ===\n{text}\n')
            jpg = dest / f'p{i:03d}.jpg'
            if not jpg.exists():
                zoom = 1600 / max(page.rect.width, page.rect.height)
                page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False).save(jpg, jpg_quality=86)
        (c.work / 'texto').mkdir(parents=True, exist_ok=True)
        (c.work / 'texto' / f'{slug}.txt').write_text(''.join(texts))
        (c.work / 'folhas').mkdir(parents=True, exist_ok=True)
        for sheet_n, start in enumerate(range(1, doc.page_count + 1, 6), 1):
            sheet = Image.new('RGB', (1920, 1016), (255, 255, 255))
            draw = ImageDraw.Draw(sheet)
            for k, n in enumerate(range(start, min(start + 6, doc.page_count + 1))):
                x, y = (k % 3) * 640, (k // 3) * 508
                im = Image.open(dest / f'p{n:03d}.jpg').convert('RGB')
                im.thumbnail((640, 480))
                sheet.paste(im, (x + (640 - im.width) // 2, y + 28 + (480 - im.height) // 2))
                draw.rectangle((x, y, x + 90, y + 27), fill=(0, 0, 0))
                draw.text((x + 8, y + 4), f'p{n}', font=face, fill=(255, 255, 255))
            sheet.save(c.work / 'folhas' / f'{slug}_{sheet_n:02d}.jpg', quality=82)
        inventory.append(dict(slug=slug, pdf=str(pdf), origem=str(origin), paginas=doc.page_count, sem_texto=empty))
    (c.work / 'VOCABULARIO.md').write_text(vocabulary_md())
    (c.work / 'inventario.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=1))
    print(json.dumps(dict(pdfs=len(inventory), paginas=sum(i['paginas'] for i in inventory),
                          sem_texto=sum(i['sem_texto'] for i in inventory)), ensure_ascii=False))


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


def montar(c):
    vocab, pdfs, problems = vocabulary(), sources(c), []
    decks, slides = [], []
    for jl in sorted((c.work / 'leitura').glob('*.jsonl')):
        slug = jl.stem
        pages = [json.loads(line) for line in jl.read_text().splitlines() if line.strip()]
        md = (c.work / 'leitura' / f'{slug}.md').read_text()
        total = len(list((c.work / 'paginas' / slug).glob('p[0-9][0-9][0-9].jpg')))
        if len(pages) != total:
            problems.append(f'{slug}: {len(pages)} linhas para {total} páginas')
        c.studies.mkdir(parents=True, exist_ok=True)
        (c.studies / f'{slug}.md').write_text(md)
        deck_id = f'{c.name}-{slug}'
        skip = c.cfg.get('skip', {}).get(slug, set())
        chosen = [p for p in pages if p.get('selecionar') and p.get('ficha') and p['pagina'] not in skip]
        if not chosen:
            # Cópia de outro deck ou só divulgação: fica no estudo, fora do mapa.
            problems.append(f'{slug}: nenhuma página escolhida, fica fora do espaço')
            continue
        meta = deck_card(md)
        cover = int(meta.get('capa') or (chosen[0]['pagina'] if chosen else 1))
        dest = c.media / 'paginas' / slug
        dest.mkdir(parents=True, exist_ok=True)
        for n in {cover, *(p['pagina'] for p in chosen)}:
            src = c.work / 'paginas' / slug / f'p{n:03d}.jpg'
            if not (dest / src.name).exists():
                shutil.copy2(src, dest / src.name)
        rel = lambda n: str((dest / f'p{n:03d}.jpg').relative_to(ROOT))
        pdf, origin = pdfs[slug]
        base = dict(collection=c.name, file=str(origin))
        if slug in c.cfg.get('cautions', {}):
            base['cautions'] = c.cfg['cautions'][slug]
        deck = dict(base, doc='arquivo', id=deck_id, preview=rel(cover), original=str(pdf), pages=len(pages),
                    concepts=concepts(x for p in pages for x in p.get('conceitos') or []),
                    keywords=f'{c.name} {slug.replace("-", " ")}', **card(meta, vocab, problems, slug))
        what = c.cfg['what'] if origin == pdf else c.cfg['what_converted']
        deck['description'] = clean(f"{deck['title']}. {deck['description']} {what} com {len(pages)} páginas; {len(chosen)} estão no espaço como slides.")
        deck['title'] = f"{c.cfg['label']} · " + c.cfg['titles'].get(slug, deck['title'])
        decks.append(deck)
        for p in chosen:
            n = p['pagina']
            slides.append(dict(base, doc='slide', id=f'{deck_id}#{n}', deck=deck_id, n=n, page=n, preview=rel(n),
                               text=clean(p.get('texto', '')), concepts=concepts(p.get('conceitos')),
                               keywords=c.name, **card(p['ficha'], vocab, problems, f'{slug} p{n}')))
    c.out.mkdir(parents=True, exist_ok=True)
    (c.out / 'decks.jsonl').write_text(''.join(json.dumps(d, ensure_ascii=False) + '\n' for d in decks + slides))
    print(json.dumps(dict(apresentacoes=len(decks), slides=len(slides), avisos=len(problems)), ensure_ascii=False))
    for line in problems:
        print('aviso:', line)


def pranchas(c):
    """Uma prancha por apresentação com as páginas escolhidas e o título de cada ficha, para conferir antes de importar."""
    from PIL import Image, ImageDraw, ImageFont
    out = ROOT / 'app/.runtime/qa' / c.name
    out.mkdir(parents=True, exist_ok=True)
    rows = [json.loads(line) for line in (c.out / 'decks.jsonl').read_text().splitlines()]
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


def conferir(c, slugs=()):
    """Leitura de um ou mais PDFs (todos, sem slug): uma linha válida por página, ficha completa nas páginas escolhidas,
    só ids do vocabulário, ficha do deck com capa e nenhum travessão."""
    vocab, problems = vocabulary(), []
    for slug in slugs or sorted(p.name for p in (c.work / 'paginas').iterdir() if p.is_dir()):
        total = len(list((c.work / 'paginas' / slug).glob('p[0-9][0-9][0-9].jpg')))
        jl, md = c.work / 'leitura' / f'{slug}.jsonl', c.work / 'leitura' / f'{slug}.md'
        if not jl.exists() or not md.exists():
            problems.append(f'{slug}: falta {jl.name if not jl.exists() else md.name}')
            continue
        lines = [line for line in jl.read_text().splitlines() if line.strip()]
        pages = []
        for i, line in enumerate(lines, 1):
            try:
                pages.append(json.loads(line))
            except json.JSONDecodeError as e:
                problems.append(f'{slug}: linha {i} não é JSON válido ({e.msg})')
        if [p.get('pagina') for p in pages] != list(range(1, total + 1)):
            problems.append(f'{slug}: {len(pages)} linhas para {total} páginas, ou fora de ordem')
        for p in pages:
            if p.get('selecionar'):
                f = p.get('ficha') or {}
                missing = [k for k in ('titulo', 'ideia', 'como_funciona', 'intencoes', 'tecnicas', 'estetica', 'tom', 'forca') if not f.get(k)]
                if missing:
                    problems.append(f'{slug} p{p.get("pagina")}: ficha sem {", ".join(missing)}')
                if f.get('titulo'):
                    card(f, vocab, problems, f'{slug} p{p.get("pagina")}')
            elif not p.get('motivo'):
                problems.append(f'{slug} p{p.get("pagina")}: sem motivo para não selecionar')
        text = jl.read_text() + md.read_text()
        problems += [f'{slug}: travessão ou meia-risca' for dash in DASHES if dash in text]
        try:
            meta = deck_card(md.read_text())
            card(meta, vocab, problems, f'{slug} (deck)')
            if not 1 <= int(meta['capa']) <= total:
                problems.append(f'{slug}: capa {meta["capa"]} fora das páginas')
        except (ValueError, KeyError, TypeError) as e:
            problems.append(f'{slug}: ficha do deck inválida ({e})')
        chosen = sum(1 for p in pages if p.get('selecionar'))
        print(f'{slug}: {len(pages)}/{total} páginas, {chosen} escolhidas')
    print(json.dumps(dict(problemas=len(problems)), ensure_ascii=False))
    for line in problems:
        print('problema:', line)
    return not problems


def known_refs(ids):
    """Ids citados em links que não estão nas fichas das coleções: confere no banco do app, só leitura."""
    db = ROOT / 'app/.runtime/library.sqlite3'
    if not ids or not db.exists():
        return set()
    conn = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
    try:
        return {r[0] for r in conn.execute(f'SELECT id FROM refs WHERE id IN ({",".join("?" * len(ids))})', list(ids))}
    finally:
        conn.close()


def validar(c):
    """Fichas e guias do método: sem travessão, sem nome repetido entre conceitos e modelos nem entre guias de
    coleções diferentes, toda ficha e todo guia citados existem e todo slide citado num link existe, com # escrito %23."""
    metodos = ROOT / 'biblioteca/metodos'
    fichas = {m.name: {p.stem for p in [*m.glob('conceitos/*.md'), *m.glob('modelos/*.md')]} for m in metodos.iterdir() if m.is_dir()}
    names = {}
    for p in [*c.method.glob('conceitos/*.md'), *c.method.glob('modelos/*.md')]:
        names.setdefault(p.stem, []).append(p.parent.name)
    problems = [f'nome repetido: {n} em {", ".join(d)}' for n, d in names.items() if len(d) > 1]
    guides = {}
    for folder in (ROOT / 'biblioteca/guias', ROOT / 'biblioteca/motion/guias', *sorted(metodos.glob('*/guias'))):
        for p in folder.glob('*.md'):
            if p.stem != 'LEIA-ME':
                guides.setdefault(p.stem, []).append(str(folder.relative_to(ROOT)))
    for name in ('kit', 'kit-apresentacao'):
        guides.setdefault(name, []).append('kit')
    problems += [f'guia repetido: {n} em {", ".join(d)}' for n, d in guides.items() if len(d) > 1]
    refs = {json.loads(line)['id'] for m in fichas for f in (ROOT / 'dados' / m).rglob('*.jsonl') for line in f.read_text().splitlines() if line.strip()}
    files = sorted(c.method.rglob('*.md'))
    links = {}
    for p in files:
        text, where = p.read_text(), p.relative_to(ROOT)
        problems += [f'{where}: travessão ou meia-risca' for dash in DASHES if dash in text]
        for coll, n in re.findall(r'`([a-z0-9-]+)/([a-z0-9-]+)`', text):
            if coll in fichas and n not in fichas[coll]:
                problems.append(f'{where}: ficha inexistente {coll}/{n}')
        problems += [f'{where}: caminho de arquivo em vez de {c.name}/{n}' for n in re.findall(r'`(?:conceitos|modelos)/([a-z0-9-]+)\.md`', text)]
        for g in re.findall(r'get_guide\("([a-z0-9/-]+)"\)', text):
            coll, _, n = g.partition('/')
            if g not in guides and not (n and n in fichas.get(coll, ())):
                problems.append(f'{where}: guia inexistente {g}')
        for r in re.findall(r'[?&]ref=([^)\s]+)\)', text):
            if '#' in r:
                problems.append(f'{where}: link de slide com # em vez de %23: {r}')
            links.setdefault(unquote(r).split('&')[0], []).append(where)
    missing = {r for r in links if r not in refs}
    for r in sorted(missing - known_refs(missing)):
        problems += [f'{w}: slide inexistente {r}' for w in links[r]]
    print(json.dumps(dict(fichas=len(names), arquivos=len(files), problemas=len(problems)), ensure_ascii=False))
    for line in problems:
        print('problema:', line)
    return not problems


if __name__ == '__main__':
    commands = {'paginas': paginas, 'conferir': conferir, 'montar': montar, 'pranchas': pranchas, 'validar': validar}
    if len(sys.argv) < 3 or sys.argv[1] not in COLLECTIONS or sys.argv[2] not in commands or (sys.argv[3:] and sys.argv[2] != 'conferir'):
        sys.exit(f'uso: incorporar_colecao.py <{"|".join(COLLECTIONS)}> <{"|".join(commands)}> [slug... só em conferir]')
    c = Collection(sys.argv[1])
    result = conferir(c, sys.argv[3:]) if sys.argv[2] == 'conferir' else commands[sys.argv[2]](c)
    sys.exit(1 if result is False else 0)
