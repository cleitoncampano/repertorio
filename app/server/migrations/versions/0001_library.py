"""Biblioteca, curadoria, contextos, trabalhos persistidos e busca."""
from alembic import op

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    statements = [
        """CREATE TABLE refs (
        id TEXT PRIMARY KEY, kind TEXT NOT NULL, title TEXT NOT NULL,
        parent_id TEXT, origin TEXT NOT NULL, state TEXT NOT NULL DEFAULT 'published',
        ready INTEGER NOT NULL DEFAULT 1, hidden INTEGER NOT NULL DEFAULT 0,
        curated INTEGER NOT NULL DEFAULT 0, revision INTEGER NOT NULL DEFAULT 1,
        source_hash TEXT, payload TEXT NOT NULL, search_text TEXT NOT NULL,
        created TEXT NOT NULL, updated TEXT NOT NULL)""",
        "CREATE INDEX refs_parent ON refs(parent_id)",
        "CREATE INDEX refs_state ON refs(state,ready,kind)",
        "CREATE VIRTUAL TABLE ref_search USING fts5(id UNINDEXED, title, search_text, tokenize='unicode61 remove_diacritics 2')",
        """CREATE TRIGGER refs_ai AFTER INSERT ON refs BEGIN
        INSERT INTO ref_search(id,title,search_text) VALUES(new.id,new.title,new.search_text); END""",
        """CREATE TRIGGER refs_au AFTER UPDATE ON refs BEGIN
        DELETE FROM ref_search WHERE id=old.id;
        INSERT INTO ref_search(id,title,search_text) VALUES(new.id,new.title,new.search_text); END""",
        "CREATE TRIGGER refs_ad AFTER DELETE ON refs BEGIN DELETE FROM ref_search WHERE id=old.id; END",
        """CREATE TABLE assets(id TEXT PRIMARY KEY, ref_id TEXT NOT NULL REFERENCES refs(id),
        path TEXT NOT NULL, role TEXT NOT NULL, member TEXT, mime TEXT NOT NULL, missing INTEGER NOT NULL DEFAULT 0)""",
        "CREATE INDEX assets_ref ON assets(ref_id)",
        "CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT NOT NULL)",
        "CREATE TABLE projects(id TEXT PRIMARY KEY, name TEXT NOT NULL, root TEXT NOT NULL UNIQUE, created TEXT NOT NULL)",
        "CREATE TABLE contexts(id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(id), demand TEXT NOT NULL, created TEXT NOT NULL)",
        "CREATE TABLE packs(id TEXT PRIMARY KEY, context_id TEXT NOT NULL REFERENCES contexts(id), title TEXT NOT NULL, payload TEXT NOT NULL, created TEXT NOT NULL)",
        """CREATE TABLE events(id INTEGER PRIMARY KEY AUTOINCREMENT, action TEXT NOT NULL,
        ref_id TEXT, context_id TEXT, payload TEXT NOT NULL, created TEXT NOT NULL)""",
        """CREATE TABLE revisions(ref_id TEXT NOT NULL, revision INTEGER NOT NULL, payload TEXT NOT NULL,
        PRIMARY KEY(ref_id,revision))""",
        """CREATE TABLE operations(id TEXT PRIMARY KEY, context_id TEXT NOT NULL, ref_id TEXT NOT NULL,
        request_key TEXT NOT NULL UNIQUE, state TEXT NOT NULL, progress INTEGER NOT NULL DEFAULT 0,
        payload TEXT NOT NULL, error TEXT, created TEXT NOT NULL, updated TEXT NOT NULL)""",
    ]
    for statement in statements:
        op.execute(statement)


def downgrade():
    raise RuntimeError('Use um backup para reverter a migração sem perder conteúdo.')
