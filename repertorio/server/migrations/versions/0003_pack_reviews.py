"""Revisão do usuário nas seleções de inspiração: aprovar ou cortar cada referência, com comentário opcional."""
from alembic import op

revision='0003'
down_revision='0002'
branch_labels=None
depends_on=None


def upgrade():
    op.execute("""CREATE TABLE pack_reviews(pack_id TEXT NOT NULL REFERENCES packs(id), ref_id TEXT NOT NULL,
        verdict TEXT NOT NULL CHECK(verdict IN ('approved','cut')), note TEXT NOT NULL DEFAULT '', updated TEXT NOT NULL,
        PRIMARY KEY(pack_id,ref_id))""")


def downgrade():
    raise RuntimeError('Restaure um backup para reverter.')
