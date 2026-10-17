import json
from datetime import datetime, timezone
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, event, text


def now():
    return datetime.now(timezone.utc).isoformat()


def dumps(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))


class Database:
    def __init__(self, settings):
        self.settings = settings
        settings.home.mkdir(parents=True, exist_ok=True)
        self.engine = create_engine(f'sqlite:///{settings.db}', connect_args={'timeout': 20})

        @event.listens_for(self.engine, 'connect')
        def configure(dbapi, _):
            dbapi.execute('PRAGMA journal_mode=WAL')
            dbapi.execute('PRAGMA foreign_keys=ON')
            dbapi.execute('PRAGMA busy_timeout=20000')

    def migrate(self):
        config = Config(str(Path(__file__).resolve().parents[1] / 'alembic.ini'))
        with self.engine.connect() as conn:
            config.attributes['connection'] = conn
            command.upgrade(config, 'head')

    def query(self, sql, **params):
        with self.engine.connect() as conn:
            return [dict(r) for r in conn.execute(text(sql), params).mappings()]

    def one(self, sql, **params):
        rows = self.query(sql, **params)
        return rows[0] if rows else None

    @staticmethod
    def log(conn, action, ref_id=None, context_id=None, **payload):
        conn.execute(text('INSERT INTO events(action,ref_id,context_id,payload,created) VALUES(:a,:r,:c,:p,:t)'),
                     dict(a=action, r=ref_id, c=context_id, p=dumps(payload), t=now()))
