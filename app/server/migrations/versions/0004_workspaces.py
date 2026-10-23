"""Espaços, vínculos independentes e procedência de demandas e operações."""
from alembic import op

revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None


def upgrade():
    statements = [
        "CREATE TABLE workspaces(id TEXT PRIMARY KEY, name TEXT NOT NULL, name_key TEXT NOT NULL, revision INTEGER NOT NULL DEFAULT 1, deleted TEXT, created TEXT NOT NULL, updated TEXT NOT NULL)",
        "CREATE UNIQUE INDEX workspace_names ON workspaces(name_key) WHERE deleted IS NULL",
        "INSERT INTO workspaces(id,name,name_key,created,updated) VALUES('referencias','Referências','referências',strftime('%Y-%m-%dT%H:%M:%fZ','now'),strftime('%Y-%m-%dT%H:%M:%fZ','now'))",
        """CREATE TABLE workspace_references(workspace_id TEXT NOT NULL REFERENCES workspaces(id), ref_id TEXT NOT NULL REFERENCES refs(id),
            state TEXT NOT NULL CHECK(state IN ('published','pending','trashed')), revision INTEGER NOT NULL DEFAULT 1,
            detached INTEGER NOT NULL DEFAULT 0, created TEXT NOT NULL, updated TEXT NOT NULL, PRIMARY KEY(workspace_id,ref_id))""",
        "CREATE INDEX workspace_refs_lookup ON workspace_references(ref_id,workspace_id,state,detached)",
        "CREATE INDEX workspace_refs_state ON workspace_references(workspace_id,state,detached)",
        "INSERT INTO workspace_references(workspace_id,ref_id,state,created,updated) SELECT 'referencias',id,state,created,updated FROM refs",
        "CREATE TABLE context_workspaces(context_id TEXT NOT NULL REFERENCES contexts(id), workspace_id TEXT NOT NULL REFERENCES workspaces(id), PRIMARY KEY(context_id,workspace_id))",
        "INSERT INTO context_workspaces SELECT id,'referencias' FROM contexts",
        "CREATE TABLE operation_workspaces(operation_id TEXT NOT NULL REFERENCES operations(id), workspace_id TEXT NOT NULL REFERENCES workspaces(id), PRIMARY KEY(operation_id,workspace_id))",
        "INSERT INTO operation_workspaces SELECT id,'referencias' FROM operations",
        "CREATE TABLE event_workspaces(event_id INTEGER NOT NULL REFERENCES events(id), workspace_id TEXT NOT NULL REFERENCES workspaces(id), PRIMARY KEY(event_id,workspace_id))",
        "CREATE INDEX event_workspaces_scope ON event_workspaces(workspace_id,event_id)",
        "INSERT INTO event_workspaces SELECT id,'referencias' FROM events",
    ]
    for statement in statements:
        op.execute(statement)


def downgrade():
    raise RuntimeError('Restaure o backup anterior à migração.')
