"""Escopo explícito e vínculos de referências, sem duplicação de arquivos."""
import uuid
from urllib.parse import urlencode

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from .db import dumps, now


class Problem(Exception):
    def __init__(self, status, message):
        self.status, self.message = status, message
        super().__init__(message)


class Workspaces:
    def workspace(self, wid, active=True):
        row = self.db.one('SELECT * FROM workspaces WHERE id=:id', id=wid)
        if not row or (active and row['deleted']):
            raise Problem(404, 'Espaço não encontrado ou excluído.')
        return row

    def workspaces(self):
        return self.db.query("""SELECT w.*,(SELECT COUNT(*) FROM workspace_references m JOIN refs r ON r.id=m.ref_id
            WHERE m.workspace_id=w.id AND m.detached=0 AND m.state='published' AND r.ready=1 AND r.hidden=0
            AND r.kind IN ('arquivo','referencia','criacao')) AS references_count
            FROM workspaces w WHERE w.deleted IS NULL ORDER BY w.name_key,w.id""")

    def save_workspace(self, req, wid=None):
        name = req.name.strip()
        if not name:
            raise Problem(422, 'Informe um nome para o espaço.')
        stamp = now()
        try:
            with self.db.engine.begin() as conn:
                if wid:
                    changed = conn.execute(text('''UPDATE workspaces SET name=:n,name_key=:k,revision=revision+1,updated=:t
                        WHERE id=:id AND revision=:v AND deleted IS NULL'''),
                        dict(n=name,k=name.casefold(),t=stamp,id=wid,v=req.expected_revision))
                    if changed.rowcount != 1:
                        raise Problem(409, 'O espaço mudou. Atualize antes de tentar novamente.')
                else:
                    wid = str(uuid.uuid4())
                    conn.execute(text('INSERT INTO workspaces(id,name,name_key,created,updated) VALUES(:id,:n,:k,:t,:t)'),
                                 dict(id=wid,n=name,k=name.casefold(),t=stamp))
                self.db.log(conn, 'workspace_renamed' if hasattr(req,'expected_revision') else 'workspace_created', workspace_ids=[wid], title=name)
        except IntegrityError:
            raise Problem(409, 'Já existe um espaço ativo com esse nome.')
        return self.workspace(wid)

    def workspace_state(self, wid, req):
        if req.deleted is not True:
            raise Problem(422, 'A exclusão de espaços é definitiva.')
        with self.db.engine.begin() as conn:
            row = conn.execute(text('SELECT * FROM workspaces WHERE id=:id AND deleted IS NULL'), dict(id=wid)).mappings().first()
            if not row:
                raise Problem(404, 'Espaço não encontrado.')
            changed = conn.execute(text('UPDATE workspaces SET deleted=:t,revision=revision+1,updated=:t WHERE id=:id AND revision=:v AND deleted IS NULL'),
                                   dict(t=now(),id=wid,v=req.expected_revision))
            if changed.rowcount != 1:
                raise Problem(409, 'O espaço mudou. Atualize antes de tentar novamente.')
            # O registro do espaço continua somente para procedência de demandas e operações.
            # Seus vínculos são removidos; referências e arquivos compartilhados permanecem intactos.
            conn.execute(text('DELETE FROM workspace_references WHERE workspace_id=:id'),dict(id=wid))
            self.db.log(conn,'workspace_deleted',workspace_ids=[wid],title=row['name'])
        return dict(id=wid,deleted=True)

    def scope(self, workspace_ids=None, context_id=None, active=True):
        ids = list(dict.fromkeys(workspace_ids or []))
        if context_id:
            context = self.context(context_id)
            allowed = context['workspace_ids']
            if ids and not set(ids).issubset(allowed):
                raise Problem(422, 'Esses espaços não pertencem à demanda. Inicie outro contexto para alterar o repertório.')
            ids = ids or allowed
        if not ids:
            raise Problem(422, 'Informe os espaços do repertório. Pergunte ao usuário qual espaço deseja usar e consulte list_workspaces.')
        for wid in ids:
            self.workspace(wid, active=active)
        return ids

    def membership_clause(self, ids, params, state=None, alias='r', prefix='scope'):
        params[prefix] = dumps(ids)
        if state:
            params[prefix+'_state'] = state
        parent = ''
        if state == 'published':
            parent = f'''AND ({alias}.parent_id IS NULL OR EXISTS(SELECT 1 FROM workspace_references pm JOIN refs p ON p.id=pm.ref_id
                WHERE pm.workspace_id=m.workspace_id AND pm.ref_id={alias}.parent_id AND pm.detached=0 AND pm.state='published' AND p.ready=1 AND p.hidden=0))'''
        return f'''EXISTS(SELECT 1 FROM workspace_references m JOIN workspaces w ON w.id=m.workspace_id
            WHERE m.ref_id={alias}.id AND m.workspace_id IN (SELECT value FROM json_each(:{prefix}))
            AND m.detached=0 AND w.deleted IS NULL {'AND m.state=:'+prefix+'_state' if state else ''} {parent})'''

    def memberships(self, rid, ids=None):
        return self.db.query('''SELECT m.workspace_id,w.name,m.state,m.revision AS membership_revision FROM workspace_references m
            JOIN workspaces w ON w.id=m.workspace_id WHERE m.ref_id=:rid AND m.detached=0 AND w.deleted IS NULL
            AND (:ids IS NULL OR m.workspace_id IN (SELECT value FROM json_each(:ids)))
            ORDER BY CASE m.state WHEN 'published' THEN 0 WHEN 'pending' THEN 1 ELSE 2 END,w.name_key''',
            rid=rid,ids=dumps(ids) if ids is not None else None)

    def scoped_summaries(self, rows, ids, state=None):
        """Carrega os vínculos da página e dos pais de uma vez, sem consultas por referência."""
        if not rows:
            return []
        refs=list(dict.fromkeys([r['id'] for r in rows]+[r['parent_id'] for r in rows if r['parent_id']]))
        memberships,available={},{}
        for item in self.db.query('''SELECT m.ref_id,r.ready,r.hidden,m.workspace_id,w.name,m.state,m.revision AS membership_revision
            FROM workspace_references m JOIN workspaces w ON w.id=m.workspace_id JOIN refs r ON r.id=m.ref_id
            WHERE m.ref_id IN (SELECT value FROM json_each(:refs)) AND m.detached=0 AND w.deleted IS NULL
            AND m.workspace_id IN (SELECT value FROM json_each(:ids))
            ORDER BY CASE m.state WHEN 'published' THEN 0 WHEN 'pending' THEN 1 ELSE 2 END,w.name_key''',refs=dumps(refs),ids=dumps(ids)):
            rid,ready,hidden=item.pop('ref_id'),item.pop('ready'),item.pop('hidden')
            memberships.setdefault(rid,[]).append(item)
            if ready and not hidden and item['state']=='published':
                available.setdefault(rid,set()).add(item['workspace_id'])
        return [self.scoped_summary(row,ids,state,memberships=memberships.get(row['id'],[]),parent_available=available.get(row['parent_id'],set())) for row in rows]

    def scoped_summary(self, row, ids, state=None, *, memberships=None, parent_available=None):
        out = self.summary(row)
        if memberships is None:
            memberships = self.memberships(row['id'], ids)
        if not memberships:
            raise Problem(404, 'Referência não encontrada neste espaço.')
        candidates=[m for m in memberships if state is None or m['state']==state]
        published=[m for m in candidates if m['state']=='published']
        if row['parent_id']:
            if parent_available is None:
                parent=self.db.one('SELECT ready,hidden FROM refs WHERE id=:id',id=row['parent_id'])
                parent_available={m['workspace_id'] for m in self.memberships(row['parent_id'],ids) if m['state']=='published'} if parent and parent['ready'] and not parent['hidden'] else set()
            published=[m for m in published if m['workspace_id'] in parent_available]
        selected=(published or candidates or memberships)[0]
        matching=published if published and selected['state']=='published' else [m for m in memberships if m['state']==selected['state']]
        out.update(state=selected['state'],membership_revision=selected['membership_revision'],workspace_id=selected['workspace_id'],
                   workspace_ids=[m['workspace_id'] for m in matching],memberships=memberships,
                   url=self.settings.url+'/?'+urlencode({'workspace':selected['workspace_id'],'ref':row['id']}))
        return out

    def graph(self, workspace_id):
        from .schemas import Search
        args = Search(workspace_ids=[workspace_id],kind='arquivo,referencia,criacao')
        params = {}
        clauses = self.filters(args, params)
        rows = self.db.query(f'''SELECT r.*,(SELECT a.id FROM assets a WHERE a.ref_id=r.id AND a.missing=0 AND a.role IN ('thumbnail','preview')
            ORDER BY CASE a.role WHEN 'thumbnail' THEN 0 ELSE 1 END,a.id LIMIT 1) AS thumbnail
            FROM refs r WHERE {' AND '.join(clauses)} ORDER BY r.id''', **params)
        return dict(items=self.scoped_summaries(rows,[workspace_id]),vocabulary=self.meta('vocabulary',{}))

    def reference_workspaces(self, rid, req, from_ui=False):
        ids = self.scope([req.source_workspace_id], req.context_id)
        targets = self.scope(req.target_workspace_ids)
        if req.move and (len(targets) != 1 or req.source_workspace_id in targets):
            raise Problem(422, 'Escolha um único espaço diferente para mover a referência.')
        if not from_ui and (not req.context_id or not req.user_requested):
            raise Problem(422, 'Vincular ou mover referências exige contexto e pedido explícito do usuário.')
        ref = self.get(rid, False, workspace_ids=ids)
        root = ref['parent_id'] or rid
        with self.db.engine.begin() as conn:
            source = conn.execute(text('SELECT * FROM workspace_references WHERE workspace_id=:w AND ref_id=:r AND detached=0'),dict(w=ids[0],r=rid)).mappings().first()
            if not source or source['revision'] != req.expected_membership_revision:
                raise Problem(409, 'O vínculo mudou. Atualize antes de tentar novamente.')
            family = conn.execute(text('SELECT id FROM refs WHERE id=:id OR parent_id=:id'),dict(id=root)).scalars().all()
            for target in targets:
                if target == ids[0]:
                    continue
                for child in family:
                    src = conn.execute(text('SELECT state FROM workspace_references WHERE workspace_id=:w AND ref_id=:r AND detached=0'),dict(w=ids[0],r=child)).mappings().first()
                    if not src:
                        continue
                    conn.execute(text('''INSERT INTO workspace_references(workspace_id,ref_id,state,created,updated) VALUES(:w,:r,:s,:t,:t)
                        ON CONFLICT(workspace_id,ref_id) DO UPDATE SET detached=0,state=excluded.state,revision=workspace_references.revision+1,updated=excluded.updated
                        WHERE workspace_references.detached=1 OR workspace_references.state='trashed' '''),dict(w=target,r=child,s=src['state'],t=now()))
            if req.move:
                conn.execute(text('UPDATE workspace_references SET detached=1,revision=revision+1,updated=:t WHERE workspace_id=:w AND ref_id IN (SELECT value FROM json_each(:family))'),
                             dict(t=now(),w=ids[0],family=dumps(family)))
            self.db.log(conn,'reference_moved' if req.move else 'reference_linked',rid,req.context_id,workspace_ids=list(dict.fromkeys(ids+targets)),title=ref['title'])
        return dict(reference_id=root,workspace_ids=[m['workspace_id'] for m in self.memberships(root)])

    def join_workspaces(self, target, sources):
        """Liga ao espaço tudo o que está publicado nos espaços de origem, sem copiar arquivos. Pode rodar de novo: traz só
        o que é novo e respeita o que o espaço reunido já mandou para a lixeira ou excluiu de vez."""
        self.workspace(target)
        sources = [w for w in dict.fromkeys(sources) if w != target]
        if not sources:
            raise Problem(422, 'Informe ao menos um espaço de origem diferente do destino.')
        names = [self.workspace(w)['name'] for w in sources]
        with self.db.engine.begin() as conn:
            added = conn.execute(text('''INSERT OR IGNORE INTO workspace_references(workspace_id,ref_id,state,created,updated)
                SELECT DISTINCT :w,m.ref_id,'published',:t,:t FROM workspace_references m
                WHERE m.workspace_id IN (SELECT value FROM json_each(:sources)) AND m.detached=0 AND m.state='published' '''),
                dict(w=target,t=now(),sources=dumps(sources))).rowcount
            if added:
                self.db.log(conn,'workspace_joined',workspace_ids=[target]+sources,title=', '.join(names),added=added)
        return dict(workspace_id=target,sources=sources,added=added)

    def purge_trash(self, workspace_id, req):
        """Exclui de vez o que está na lixeira do espaço. O vínculo fica desligado (uma nova importação não traz a peça de
        volta); se nenhum outro espaço usa a peça, a ficha vira um registro vazio e saem os arquivos que o próprio app guardou.
        Originais fora da pasta do app nunca são apagados."""
        from pathlib import Path
        self.workspace(workspace_id)
        removed_assets = []
        with self.db.engine.begin() as conn:
            trashed = set(conn.execute(text("SELECT ref_id FROM workspace_references WHERE workspace_id=:w AND state='trashed' AND detached=0"),
                                       dict(w=workspace_id)).scalars().all())
            targets = (trashed if req.all else set(req.ids)) - set(req.keep)
            if not targets:
                raise Problem(422, 'Escolha ao menos uma referência da lixeira.')
            if targets - trashed:
                raise Problem(409, 'Algumas referências não estão mais na lixeira. Atualize a página.')
            family = sorted(set(conn.execute(text('SELECT id FROM refs WHERE id IN (SELECT value FROM json_each(:ids)) OR parent_id IN (SELECT value FROM json_each(:ids))'),
                                             dict(ids=dumps(sorted(targets)))).scalars().all()))
            stamp = now()
            conn.execute(text('UPDATE workspace_references SET detached=1,revision=revision+1,updated=:t WHERE workspace_id=:w AND detached=0 AND ref_id IN (SELECT value FROM json_each(:ids))'),
                         dict(t=stamp, w=workspace_id, ids=dumps(family)))
            titles = dict(conn.execute(text('SELECT id,title FROM refs WHERE id IN (SELECT value FROM json_each(:ids))'), dict(ids=dumps(sorted(targets)))).all())
            for rid in sorted(targets):
                self.db.log(conn, 'reference_purged', rid, None, workspace_ids=[workspace_id], title=titles.get(rid, rid))
            orphans = conn.execute(text('''SELECT id FROM refs WHERE id IN (SELECT value FROM json_each(:ids))
                AND NOT EXISTS(SELECT 1 FROM workspace_references m WHERE m.ref_id=refs.id AND m.detached=0)'''), dict(ids=dumps(family))).scalars().all()
            if orphans:
                params = dict(ids=dumps(orphans))
                removed_assets = conn.execute(text('SELECT id,path FROM assets WHERE ref_id IN (SELECT value FROM json_each(:ids))'), params).all()
                conn.execute(text('DELETE FROM assets WHERE ref_id IN (SELECT value FROM json_each(:ids))'), params)
                conn.execute(text('DELETE FROM revisions WHERE ref_id IN (SELECT value FROM json_each(:ids))'), params)
                conn.execute(text("DELETE FROM meta WHERE key IN (SELECT 'transitions:'||value FROM json_each(:ids))"), params)
                for rid in orphans:
                    conn.execute(text("UPDATE refs SET title=:id,payload=:p,search_text='',hidden=1,curated=1,revision=revision+1,updated=:t WHERE id=:id"),
                                 dict(id=rid, p=dumps({'title': rid, 'purged': stamp}), t=stamp))
        home = Path(self.settings.home).resolve()
        files = 0
        for aid, path in removed_assets:
            for thumb in (home / 'miniaturas').glob(f'{aid}-*.webp'):
                thumb.unlink(missing_ok=True)
            target = Path(path).resolve()
            if home not in target.parents or self.db.one('SELECT 1 AS n FROM assets WHERE path=:p', p=path):
                continue
            if target.is_file():
                target.unlink()
                files += 1
            if target.parent != home and not any(target.parent.iterdir()):
                target.parent.rmdir()
        return dict(purged=len(targets), files_removed=files)

    def operations(self, workspace_id):
        self.workspace(workspace_id)
        return self.db.query('''SELECT o.id,o.ref_id,o.state,o.progress,o.error,o.updated FROM operations o
            WHERE EXISTS(SELECT 1 FROM operation_workspaces ow WHERE ow.operation_id=o.id AND ow.workspace_id=:w)
            ORDER BY o.created DESC LIMIT 100''',w=workspace_id)
