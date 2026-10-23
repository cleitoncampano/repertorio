"""Primeiro uso com vocabulário próprio, sem importar o acervo de desenvolvimento."""
from sqlalchemy import text
from .db import Database, dumps


VOCABULARY = {
    'operacoes': {'itens': [
        {'id': 'diferenciacao', 'nome': 'Diferenciar', 'def': 'Dar destaque ao que precisa ser percebido.'},
        {'id': 'agrupamento', 'nome': 'Agrupar', 'def': 'Mostrar quais elementos pertencem à mesma ideia.'},
        {'id': 'sequencia', 'nome': 'Sequenciar', 'def': 'Organizar a ordem em que uma história é entendida.'},
        {'id': 'previsao', 'nome': 'Antecipar', 'def': 'Criar uma expectativa e mostrar sua continuação.'},
    ]},
    'tecnicas': {'itens': [
        {'id': 'escala', 'nome': 'Contraste de tamanho', 'operacao': 'diferenciacao', 'def': 'Uma mudança de tamanho estabelece a prioridade.'},
        {'id': 'comparacao', 'nome': 'Comparação', 'operacao': 'diferenciacao', 'def': 'Duas situações lado a lado tornam a diferença visível.'},
        {'id': 'grupos', 'nome': 'Grupos visuais', 'operacao': 'agrupamento', 'def': 'Proximidade e alinhamento ligam partes de uma ideia.'},
        {'id': 'percurso', 'nome': 'Percurso', 'operacao': 'sequencia', 'def': 'Etapas conectadas ajudam a acompanhar uma mudança.'},
        {'id': 'numero-contexto', 'nome': 'Número com contexto', 'operacao': 'diferenciacao', 'def': 'Um número é acompanhado de sua consequência.'},
        {'id': 'continuidade', 'nome': 'Continuidade', 'operacao': 'previsao', 'def': 'Um elemento conhecido reaparece para ligar momentos.'},
    ]},
    'intencoes': {'itens': [{'id': key, 'def': label} for key, label in [
        ('ABRIR', 'Apresentar a pergunta central.'), ('EXPLICAR', 'Tornar uma ideia compreensível.'),
        ('PROVAR', 'Sustentar uma afirmação.'), ('FECHAR', 'Indicar o próximo passo.'),
    ]]},
    'movimentos': {'itens': [{'id': 'corte', 'nome': 'Corte', 'def': 'Troca direta de momento.'},
                            {'id': 'continuidade', 'nome': 'Continuidade', 'def': 'Um elemento atravessa a passagem.'}]},
    'esteticas': {'itens': ['claro', 'escuro', 'editorial']},
}


def initialize(settings):
    fresh = not settings.db.exists()
    db = Database(settings)
    try:
        db.migrate()
        if fresh:
            with db.engine.begin() as conn:
                conn.execute(text("UPDATE workspaces SET name='Meu repertório',name_key='meu repertório' WHERE id='referencias'"))
                conn.execute(text('INSERT INTO meta(key,value) VALUES(:key,:value)'),
                             {'key': 'vocabulary', 'value': dumps(VOCABULARY)})
        return {'initialized': fresh, 'preserved_existing_library': not fresh, 'home': str(settings.home)}
    finally:
        db.engine.dispose()
