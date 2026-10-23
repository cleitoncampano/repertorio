"""Inclui "como funciona" e "serve para" no texto de busca das fichas que usam o índice padrão."""
import json
from alembic import op
from sqlalchemy import text

revision='0005'
down_revision='0004'
branch_labels=None
depends_on=None

OLD=('title','description','idea','techniques','intentions','movements','aesthetics','text','usage_notes','keywords')
NEW=('title','description','idea','how','good_for','techniques','intentions','movements','aesthetics','text','usage_notes','keywords')


def join(data,fields):
    return ' '.join(' '.join(map(str,data[k])) if isinstance(data.get(k),list) else str(data.get(k) or '') for k in fields)


def upgrade():
    conn=op.get_bind()
    changes=[]
    for row in conn.execute(text("SELECT id,payload,search_text FROM refs WHERE search_text<>''")).mappings():
        data=json.loads(row['payload'] or '{}')
        # só refaz o texto montado pelo índice padrão; fichas com texto próprio ficam como estão
        if isinstance(data,dict) and row['search_text'].strip()==join(data,OLD).strip() and (data.get('how') or data.get('good_for')):
            changes.append(dict(id=row['id'],s=join(data,NEW)))
    for change in changes:
        conn.execute(text('UPDATE refs SET search_text=:s WHERE id=:id'),change)


def downgrade():
    raise RuntimeError('Restaure um backup para reverter.')
