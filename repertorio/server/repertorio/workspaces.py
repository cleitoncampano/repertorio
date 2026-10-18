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

    def workspaces(self, deleted=False):
        return self.db.query("""SELECT w.*,(SELECT COUNT(*) FROM workspace_references m JOIN refs r ON r.id=m.ref_id
            WHERE m.workspace_id=w.id AND m.detached=0 AND m.state='published' AND r.ready=1 AND r.hidden=0
            AND r.kind IN ('arquivo','referencia','criacao')) AS references_count
            FROM workspaces w WHERE (w.deleted IS NOT NULL)=:deleted ORDER BY w.name_key,w.id""", deleted=deleted)

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
        try:
            with self.db.engine.begin() as conn:
                row = conn.execute(text('SELECT * FROM workspaces WHERE id=:id'), dict(id=wid)).mappings().first()
                if not row:
                    raise Problem(404, 'Espaço não encontrado.')
                changed = conn.execute(text('UPDATE workspaces SET deleted=:d,revision=revision+1,updated=:t WHERE id=:id AND revision=:v'),
                                       dict(d=now() if req.deleted else None,t=now(),id=wid,v=req.expected_revision))
                if changed.rowcount != 1:
                    raise Problem(409, 'O espaço mudou. Atualize antes de tentar novamente.')
                self.db.log(conn,'workspace_deleted' if req.deleted else 'workspace_restored',workspace_ids=[wid],title=row['name'])
        except IntegrityError:
            raise Problem(409, 'Renomeie o espaço ativo com o mesmo nome antes de restaurar este.')
        return self.workspace(wid, active=False)

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

    def scoped_summary(self, row, ids, state=None):
        out = self.summary(row)
        memberships = self.memberships(row['id'], ids)
        if not memberships:
            raise Problem(404, 'Referência não encontrada neste espaço.')
        candidates=[m for m in memberships if state is None or m['state']==state]
        published=[m for m in candidates if m['state']=='published']
        if row['parent_id']:
            parent=self.db.one('SELECT ready,hidden FROM refs WHERE id=:id',id=row['parent_id'])
            available={m['workspace_id'] for m in self.memberships(row['parent_id'],ids) if m['state']=='published'} if parent and parent['ready'] and not parent['hidden'] else set()
            published=[m for m in published if m['workspace_id'] in available]
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
        return dict(items=[self.scoped_summary(r,[workspace_id]) for r in rows],vocabulary=self.meta('vocabulary',{}))

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

    def operations(self, workspace_id):
        self.workspace(workspace_id)
        return self.db.query('''SELECT o.id,o.ref_id,o.state,o.progress,o.error,o.updated FROM operations o
            WHERE EXISTS(SELECT 1 FROM operation_workspaces ow WHERE ow.operation_id=o.id AND ow.workspace_id=:w)
            ORDER BY o.created DESC LIMIT 100''',w=workspace_id)
