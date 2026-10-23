"""Demonstração original e isolada, sem ler o acervo do proprietário."""
import hashlib
import json
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from sqlalchemy import text
from .config import Settings
from .db import Database, dumps, now
from .importer import asset, index_text
from .schemas import Project, StartContext, Workspace, WorkspaceUpdate
from .service import Library
from .starter import initialize


EXAMPLES = [
    ('Uma ideia que ocupa a tela', 'escala', 'ABRIR', 'claro',
     'Dê mais espaço à pergunta principal e deixe o contexto em um segundo nível.',
     'Use uma pergunta curta em tamanho grande. Coloque a explicação em um bloco menor, com respiro.'),
    ('Do problema à proposta', 'percurso', 'EXPLICAR', 'escuro',
     'Mostre a transformação como um percurso de três etapas.',
     'Conecte situação atual, descoberta e próximo passo. Mantenha a ordem de leitura evidente.'),
    ('Antes e depois, lado a lado', 'comparacao', 'PROVAR', 'claro',
     'Compare situações com a mesma escala e destaque a diferença que interessa.',
     'Alinhe os dois estados e use um único acento para apontar a mudança.'),
    ('Três partes de uma mesma ideia', 'grupos', 'EXPLICAR', 'editorial',
     'Agrupe os detalhes por assunto para tornar uma ideia maior compreensível.',
     'Use proximidade e alinhamento. Nomeie cada grupo com uma frase curta.'),
    ('O número e o que ele muda', 'numero-contexto', 'PROVAR', 'escuro',
     'Mostre a consequência de um número, além de sua dimensão.',
     'Escreva o número em destaque e a consequência em linguagem comum. Use dados reais na produção.'),
    ('O elemento que continua', 'continuidade', 'FECHAR', 'editorial',
     'Faça um elemento reaparecer para ligar o começo ao próximo passo.',
     'Repita uma forma simples em funções diferentes, preservando a identidade da produção.'),
]


def preview(path, number, title):
    image = Image.new('RGB', (1200, 675), '#F5F2EB' if number % 2 else '#202225')
    draw = ImageDraw.Draw(image)
    ink = '#202225' if number % 2 else '#F5F2EB'
    draw.text((65, 50), 'REPERTORIO / EXEMPLO ORIGINAL', font=ImageFont.load_default(size=22), fill=ink)
    draw.text((65, 150), f'{number:02d}', font=ImageFont.load_default(size=95), fill='#F25C40')
    draw.multiline_text((65, 290), '\n'.join(textwrap.wrap(title, 26)),
                        font=ImageFont.load_default(size=54), fill=ink, spacing=16)
    draw.rectangle((65, 595, 1135, 599), fill='#F25C40')
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def prepare_demo(base, home, port=8768):
    home = Path(home).expanduser().resolve()
    if home == base.home or home.is_relative_to(base.home) or base.home.is_relative_to(home):
        raise ValueError('Use uma pasta de demonstração separada dos dados do acervo real.')
    if port == base.port:
        raise ValueError('Use uma porta diferente da biblioteca principal.')
    settings = Settings(base.root, home, port)
    marker = home / 'demo.json'
    if home.exists():
        if marker.is_file() and settings.db.is_file() and json.loads(marker.read_text()).get('kind') == 'repertorio-demo-v1':
            return settings
        raise ValueError('A pasta já existe. Escolha uma pasta nova; nenhum conteúdo será sobrescrito.')
    initialize(settings)
    db = Database(settings)
    lib = Library(db)
    try:
        primary = lib.save_workspace(WorkspaceUpdate(name='Estúdio Aurora', expected_revision=1), 'referencias')
        secondary = lib.save_workspace(Workspace(name='Marca Horizonte'))
        project_root = home / 'projeto-exemplo'
        project_root.mkdir()
        project = lib.project(Project(name='Projeto demonstrativo', root=str(project_root)))
        stamp = now()
        with db.engine.begin() as conn:
            conn.execute(text('INSERT INTO meta(key,value) VALUES(:key,:value)'), {'key': 'demo', 'value': 'true'})
            for n, (title, technique, intention, aesthetic, idea, how) in enumerate(EXAMPLES, 1):
                rid = f'demo-{n:02d}'
                image = home / 'assets/demo' / f'{rid}.png'
                preview(image, n, title)
                payload = dict(title=title, description='Exemplo original criado para demonstrar o Repertório.',
                               idea=idea, how=how, techniques=[technique], intentions=[intention],
                               movements=['continuidade' if n == 6 else 'corte'], aesthetics=[aesthetic],
                               strength=4, reusable=True, usage_notes='Material demonstrativo original, sem dados de clientes.',
                               text=title, good_for=['Apresentações', 'Posts', 'Páginas'], format='png')
                conn.execute(text('''INSERT INTO refs(id,kind,title,origin,source_hash,payload,search_text,created,updated)
                    VALUES(:id,'referencia',:title,'criacao',:hash,:payload,:search,:stamp,:stamp)'''),
                             dict(id=rid, title=title, hash=hashlib.sha256(dumps(payload).encode()).hexdigest(),
                                  payload=dumps(payload), search=index_text(payload), stamp=stamp))
                wid = primary['id'] if n <= 3 else secondary['id']
                conn.execute(text('''INSERT INTO workspace_references(workspace_id,ref_id,state,created,updated)
                    VALUES(:w,:r,'published',:t,:t)'''), dict(w=wid, r=rid, t=stamp))
                asset(conn, settings, rid, image, 'preview')
                asset(conn, settings, rid, image, 'original')
        lib.start(StartContext(project_id=project['id'], workspace_ids=[primary['id']],
                               demand='Criar uma apresentação para explicar uma nova ideia com clareza.'))
        marker.write_text(dumps({'kind': 'repertorio-demo-v1', 'workspace_ids': [primary['id'], secondary['id']],
                                 'references': len(EXAMPLES)}), encoding='utf-8')
        return settings
    finally:
        db.engine.dispose()
