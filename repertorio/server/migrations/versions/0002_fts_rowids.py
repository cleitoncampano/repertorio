"""Relaciona rowids para que atualizações FTS não percorram todo o índice."""
from alembic import op

revision='0002'
down_revision='0001'
branch_labels=None
depends_on=None


def upgrade():
    for name in ['refs_ai','refs_au','refs_ad']:op.execute(f'DROP TRIGGER {name}')
    op.execute('DELETE FROM ref_search')
    op.execute('INSERT INTO ref_search(rowid,id,title,search_text) SELECT rowid,id,title,search_text FROM refs')
    op.execute('''CREATE TRIGGER refs_ai AFTER INSERT ON refs BEGIN
    INSERT INTO ref_search(rowid,id,title,search_text) VALUES(new.rowid,new.id,new.title,new.search_text); END''')
    op.execute('''CREATE TRIGGER refs_au AFTER UPDATE ON refs BEGIN
    DELETE FROM ref_search WHERE rowid=old.rowid;
    INSERT INTO ref_search(rowid,id,title,search_text) VALUES(new.rowid,new.id,new.title,new.search_text); END''')
    op.execute('CREATE TRIGGER refs_ad AFTER DELETE ON refs BEGIN DELETE FROM ref_search WHERE rowid=old.rowid; END')


def downgrade():
    raise RuntimeError('Restaure um backup para reverter.')
