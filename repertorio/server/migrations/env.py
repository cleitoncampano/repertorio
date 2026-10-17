from alembic import context

with context.config.attributes['connection'].begin():
    context.configure(connection=context.config.attributes['connection'])
    with context.begin_transaction():
        context.run_migrations()
