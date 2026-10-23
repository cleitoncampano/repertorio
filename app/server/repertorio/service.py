import hashlib
import json
import re
import uuid
from pathlib import Path
from sqlalchemy import text
from .db import dumps, now
from .importer import index_text
from .schemas import Search
from .workspaces import Workspaces, Problem


class Library(Workspaces):
    def __init__(self, db):
        self.db = db
        self.settings = db.settings

    def meta(self, key, default=None):
        row = self.db.one('SELECT value FROM meta WHERE key=:key',key=key)
        return json.loads(row['value']) if row else default

    def stats(self, workspace_id):
        params={}
        clauses=self.filters(Search(workspace_ids=[workspace_id]),params)
        rows = self.db.query(f"SELECT kind,COUNT(*) AS total FROM refs r WHERE {' AND '.join(clauses)} GROUP BY kind",**params)
        return dict(counts={r['kind']:r['total'] for r in rows}, report=self.meta('import_report',{}),
                    pending=self.search(Search(workspace_ids=[workspace_id],state='pending',limit=1),log=False)['total'],
                    projects=self.db.one('SELECT COUNT(*) AS n FROM projects')['n'])

    def context(self, cid):
        row = self.db.one('SELECT c.*,p.name AS project_name,p.root FROM contexts c JOIN projects p ON c.project_id=p.id WHERE c.id=:id',id=cid)
        if not row:
            raise Problem(404,'Contexto não encontrado. Inicie uma demanda com start_context.')
        row['workspaces']=self.db.query('SELECT w.id,w.name,w.deleted FROM workspaces w JOIN context_workspaces cw ON cw.workspace_id=w.id WHERE cw.context_id=:id ORDER BY w.name_key',id=cid)
        row['workspace_ids']=[w['id'] for w in row['workspaces']]
        return row

    def project(self, data):
        root = Path(data.root).expanduser().resolve()
        if not root.is_dir():
            raise Problem(422,'A pasta do projeto não existe.')
        old = self.db.one('SELECT * FROM projects WHERE root=:r',r=str(root))
        if old:
            return old
        pid = re.sub(r'[^a-z0-9]+','-',data.name.lower()).strip('-') or 'projeto'
        pid += '-' + hashlib.sha256(str(root).encode()).hexdigest()[:6]
        row = dict(id=pid,name=data.name,root=str(root),created=now())
        with self.db.engine.begin() as conn:
            conn.execute(text('INSERT INTO projects VALUES(:id,:name,:root,:created)'),row)
            self.db.log(conn,'project_connected',project_id=pid,name=data.name)
        return row

    def start(self, data):
        ids=self.scope(data.workspace_ids)
        if not self.db.one('SELECT id FROM projects WHERE id=:id',id=data.project_id):
            raise Problem(404,'Cadastre esta pasta primeiro com repertorio connect.')
        row=dict(id=str(uuid.uuid4()),project_id=data.project_id,demand=data.demand,created=now())
        with self.db.engine.begin() as conn:
            conn.execute(text('INSERT INTO contexts VALUES(:id,:project_id,:demand,:created)'),row)
            for wid in ids:
                conn.execute(text('INSERT INTO context_workspaces VALUES(:c,:w)'),dict(c=row['id'],w=wid))
            self.db.log(conn,'context_started',context_id=row['id'],demand=data.demand)
        return {**self.context(row['id']),'instructions':'História primeiro. Consulte somente os espaços desta demanda. Na incorporação, informe os espaços de destino. Examine imagens e adapte a ideia à identidade do projeto. Não copie. Publique apenas quando o usuário solicitar; sugestões ficam pendentes.',
                'vocabulary':self.meta('vocabulary',{}),'principles_available':['narrativa','direcao-de-arte']}

    def summary(self, row):
        d=json.loads(row['payload'])
        out={k:row[k] for k in ['id','kind','title','origin','state','revision','ready','parent_id','updated','hidden']}
        out.update({k:d.get(k) for k in ['description','idea','techniques','intentions','movements','aesthetics','strength','reusable','unclassified','format','number']})
        aid=row.get('thumbnail')
        if aid:
            out['thumbnail']=f'/api/assets/{aid}'
        if d.get('motion') is not None:
            # Coleção de motion: o mapa toca o loop curto, o player toca o vídeo completo e o espaço se organiza
            # por formato de tela e tipo de vídeo.
            out['motion']={**{k:f'/api/assets/{v}' for k,v in d['motion'].items()},**(d.get('video') or {}),'aspect':d.get('aspect') or '','genres':d.get('genres') or []}
        out['url']=self.settings.url+'/?ref='+__import__('urllib.parse',fromlist=['quote']).quote(row['id'],safe='')
        return out

    def filters(self, args, params):
        """Condições estritas compartilhadas pela busca do mapa e pela busca dos agentes."""
        ids=self.scope(args.workspace_ids,args.context_id)
        params.update(min_strength=args.min_strength)
        clauses=[self.membership_clause(ids,params,args.state)]
        if args.state == 'published':
            clauses += ['r.ready=1','r.hidden=0']
        for field, column in [('kind','r.kind'),('origin','r.origin')]:
            value=getattr(args,field)
            if value:
                values=value.split(',')
                keys=[]
                for i,v in enumerate(values):
                    key=field+str(i);params[key]=v;keys.append(':'+key)
                clauses.append(column+' IN ('+','.join(keys)+')')
        for field, jsonfield in [('intention','intentions'),('technique','techniques'),('movement','movements'),('aesthetic','aesthetics')]:
            if getattr(args,field):
                params[field]=getattr(args,field)
                clauses.append(f"EXISTS(SELECT 1 FROM json_each(r.payload,'$.{jsonfield}') WHERE value=:{field})")
        if args.operation:
            ids=[t['id'] for t in self.meta('vocabulary',{}).get('tecnicas',{}).get('itens',[]) if t.get('operacao')==args.operation]
            params['op_techniques']=dumps(ids)
            clauses.append("EXISTS(SELECT 1 FROM json_each(r.payload,'$.techniques') WHERE value IN (SELECT value FROM json_each(:op_techniques)))")
        clauses.append("COALESCE(json_extract(r.payload,'$.strength'),3)>=:min_strength")
        if args.reusable:
            clauses.append("json_extract(r.payload,'$.reusable')=1")
        if args.format:
            clauses.append("json_extract(r.payload,'$.format')=:format")
            params['format']=args.format
        return clauses

    def search(self, args: Search, log=True):
        ids=self.scope(args.workspace_ids,args.context_id)
        params={'limit':args.limit,'offset':args.offset}
        clauses=self.filters(args,params)
        words=re.findall(r'\w+',args.query,flags=re.UNICODE)
        words=[w for w in words if len(w)>1 and w.lower() not in {'de','da','do','para','com','uma','um','as','os','em'}][:30]
        rank='0.0 AS rank'
        join=''
        if words:
            params['match']=' OR '.join('"'+w+'"*' for w in words)
            join=' JOIN ref_search ON ref_search.id=r.id '
            clauses.append('ref_search MATCH :match')
            rank='bm25(ref_search,0,5,1) AS rank'
        where=' AND '.join(clauses)
        total=self.db.one(f'SELECT COUNT(*) AS n FROM refs r {join} WHERE {where}',**params)['n']
        rows=self.db.query(f'''SELECT r.*, {rank},
            (SELECT a.id FROM assets a WHERE a.ref_id=r.id AND a.missing=0 AND a.role IN ('thumbnail','preview') ORDER BY CASE a.role WHEN 'thumbnail' THEN 0 ELSE 1 END,a.id LIMIT 1) AS thumbnail
            FROM refs r {join} WHERE {where} ORDER BY rank ASC,COALESCE(json_extract(r.payload,'$.strength'),3) DESC,r.id LIMIT :limit OFFSET :offset''',**params)
        results=[]
        for s in self.scoped_summaries(rows,ids,state=args.state):
            s['matched_by']=[f'{k}: {getattr(args,k)}' for k in ['intention','technique','operation','movement','aesthetic','origin','format'] if getattr(args,k)]
            if words: s['matched_by'].insert(0,'Texto da ficha ou do slide')
            results.append(s)
        if log and args.context_id:
            with self.db.engine.begin() as conn:
                self.db.log(conn,'references_searched',context_id=args.context_id,query=args.query,total=total)
        return dict(items=results,total=total,offset=args.offset,limit=args.limit)

    def get(self,rid,include_children=True,workspace_ids=None,context_id=None):
        ids=self.scope(workspace_ids,context_id)
        row=self.db.one('SELECT * FROM refs WHERE id=:id',id=rid)
        if not row: raise Problem(404,'Referência não encontrada.')
        data=json.loads(row['payload'])
        out={**{k:v for k,v in data.items() if k!='legacy'},**self.scoped_summary(row,ids)}
        out['workspaces']=self.memberships(rid)
        out['assets']=[{**a,'url':f"/api/assets/{a['id']}"} for a in self.db.query('SELECT id,role,mime,missing FROM assets WHERE ref_id=:id ORDER BY role,path,id',id=rid)]
        if row['parent_id']:
            parent=self.db.one('SELECT hidden,ready FROM refs WHERE id=:id',id=row['parent_id'])
            out['unavailable_by_parent']=not bool(parent and not parent['hidden'] and parent['ready'] and any(m['state']=='published' and m['workspace_id'] in out['workspace_ids'] for m in self.memberships(row['parent_id'],ids)))
        if include_children:
            params={'id':rid}
            clause=self.membership_clause(ids,params,'published')
            children=self.db.query(f"SELECT r.* FROM refs r WHERE r.parent_id=:id AND r.hidden=0 AND r.ready=1 AND {clause} ORDER BY CAST(json_extract(r.payload,'$.number') AS INTEGER)",**params)
            out['children']=[self.scoped_summary(c,ids) for c in children]
            for child in out['children']:
                a=self.db.one("SELECT id FROM assets WHERE ref_id=:id AND role='preview' AND missing=0 LIMIT 1",id=child['id'])
                child['thumbnail']=f"/api/assets/{a['id']}" if a else None
        out['transitions']=self.meta('transitions:'+rid,[])
        related=[]
        for technique in (out.get('techniques') or [])[:3]:
            related.extend(self.search(Search(workspace_ids=ids,technique=technique,kind='arquivo,referencia,criacao',limit=8),log=False)['items'])
        out['related']=list({r['id']:r for r in related if r['id']!=rid}.values())[:6]
        return out

    def validate_data(self,data,workspace_ids=None):
        vocab=self.meta('vocabulary',{})
        for field,key in [('techniques','tecnicas'),('intentions','intencoes'),('movements','movimentos'),('aesthetics','esteticas')]:
            allowed={i['id'] if isinstance(i,dict) else i for i in vocab.get(key,{}).get('itens',[])}
            bad=set(getattr(data,field))-allowed
            if bad: raise Problem(422,f'Valores fora do vocabulário em {field}: {sorted(bad)}')
        for rid in data.source_reference_ids:
            self.get(rid,False,workspace_ids=workspace_ids)

    def update(self,rid,req):
        ids=self.scope(context_id=req.context_id)
        self.get(rid,False,workspace_ids=ids)
        self.validate_data(req.data,ids)
        with self.db.engine.begin() as conn:
            row=conn.execute(text('SELECT * FROM refs WHERE id=:id'),dict(id=rid)).mappings().first()
            if not row: raise Problem(404,'Referência não encontrada.')
            d={**json.loads(row['payload']),**req.data.model_dump()}
            changed=conn.execute(text('UPDATE refs SET title=:title,payload=:p,search_text=:s,curated=1,revision=revision+1,updated=:t WHERE id=:id AND revision=:rev'),
                                 dict(title=d['title'],p=dumps(d),s=index_text(d),t=now(),id=rid,rev=req.expected_revision))
            if changed.rowcount!=1: raise Problem(409,'A referência mudou. Leia a revisão atual antes de atualizar.')
            conn.execute(text('INSERT INTO revisions VALUES(:id,:r,:p)'),dict(id=rid,r=row['revision'],p=dumps(dict(row))))
            self.db.log(conn,'reference_updated',rid,req.context_id,revision=row['revision']+1,workspace_ids=[m['workspace_id'] for m in self.memberships(rid)])
        return self.get(rid,workspace_ids=ids)

    def state(self,rid,req,from_ui=False):
        ids=self.scope([req.workspace_id],req.context_id)
        if not from_ui and not req.context_id: raise Problem(422,'Informe o contexto da alteração.')
        if not from_ui and req.state in ('published','trashed') and not req.user_requested:
            raise Problem(422,'Publicação e exclusão pelo agente exigem pedido explícito do usuário.')
        with self.db.engine.begin() as conn:
            row=conn.execute(text('SELECT * FROM workspace_references WHERE ref_id=:id AND workspace_id=:w AND detached=0'),dict(id=rid,w=req.workspace_id)).mappings().first()
            if not row: raise Problem(404,'Referência não encontrada.')
            changed=conn.execute(text('UPDATE workspace_references SET state=:state,revision=revision+1,updated=:t WHERE ref_id=:id AND workspace_id=:w AND revision=:rev'),
                                 dict(state=req.state,t=now(),id=rid,w=req.workspace_id,rev=req.expected_membership_revision))
            if changed.rowcount!=1: raise Problem(409,'A referência mudou. Atualize antes de tentar novamente.')
            self.db.log(conn,'reference_'+req.state,rid,req.context_id,workspace_ids=ids,previous_state=row['state'],user_requested=req.user_requested or from_ui)
        return self.get(rid,workspace_ids=ids)

    def pack(self,req):
        ids=self.scope(context_id=req.context_id)
        snapshots=[]
        for rid in dict.fromkeys(req.reference_ids):
            ref=self.get(rid,False,workspace_ids=ids)
            if ref['state']!='published' or not ref['ready'] or ref.get('hidden') or ref.get('unavailable_by_parent'):
                raise Problem(409,'Uma referência selecionada não está disponível.')
            snapshots.append({k:ref.get(k) for k in ['id','revision','title','description','idea','techniques','intentions','movements','aesthetics','reusable','usage_notes','assets','url','workspace_ids']})
        pid=str(uuid.uuid4())
        payload=dict(references=snapshots,rationale=req.rationale)
        with self.db.engine.begin() as conn:
            conn.execute(text('INSERT INTO packs VALUES(:id,:c,:t,:p,:d)'),dict(id=pid,c=req.context_id,t=req.title,p=dumps(payload),d=now()))
            self.db.log(conn,'pack_created',context_id=req.context_id,pack_id=pid,title=req.title)
        return dict(id=pid,context_id=req.context_id,workspace_ids=ids,title=req.title,review_url=f'{self.settings.url}/?workspace={ids[0]}&escolha={pid}',**payload)

    def demands(self,workspace_id):
        self.workspace(workspace_id)
        """Pedidos com seleções guardadas, do mais recente ao mais antigo, com o andamento da revisão."""
        packs=self.db.query('''SELECT k.id,k.context_id,k.title,k.created,json_array_length(k.payload,'$.references') AS total,
            (SELECT COUNT(*) FROM pack_reviews v WHERE v.pack_id=k.id AND v.verdict='approved') AS approved,
            (SELECT COUNT(*) FROM pack_reviews v WHERE v.pack_id=k.id AND v.verdict='cut') AS cut
            FROM packs k ORDER BY k.created DESC''')
        rows=self.db.query('SELECT c.id,c.demand,c.created,p.name AS project_name FROM contexts c JOIN projects p ON p.id=c.project_id WHERE EXISTS(SELECT 1 FROM packs k WHERE k.context_id=c.id)')
        for row in rows:
            row['workspaces']=self.context(row['id'])['workspaces']
            row['packs']=[k for k in packs if k['context_id']==row['id']]
            row['updated']=row['packs'][0]['created']
        return sorted([r for r in rows if workspace_id in [w['id'] for w in r['workspaces']]],key=lambda r:r['updated'],reverse=True)

    def pack_detail(self,pid):
        """Seleção guardada com a imagem atual de cada referência e o que o usuário decidiu sobre ela."""
        row=self.db.one('SELECT k.*,c.demand,p.name AS project_name FROM packs k JOIN contexts c ON c.id=k.context_id JOIN projects p ON p.id=c.project_id WHERE k.id=:id',id=pid)
        if not row:raise Problem(404,'Seleção não encontrada.')
        spaces=self.context(row['context_id'])['workspaces']
        ids=[w['id'] for w in spaces if not w['deleted']]
        payload=json.loads(row['payload'])
        reviews={r['ref_id']:{k:r[k] for k in ('verdict','note','updated')} for r in self.db.query('SELECT * FROM pack_reviews WHERE pack_id=:id',id=pid)}
        references=[]
        for snap in payload['references']:
            now=self.db.one('''SELECT r.state,r.hidden,r.kind,(SELECT a.id FROM assets a WHERE a.ref_id=r.id AND a.missing=0 AND a.role IN ('thumbnail','preview') ORDER BY CASE a.role WHEN 'thumbnail' THEN 0 ELSE 1 END,a.id LIMIT 1) AS thumbnail
                FROM refs r WHERE r.id=:id''',id=snap['id'])
            current=None
            if ids:
                try:current=self.get(snap['id'],False,workspace_ids=ids)
                except Problem:pass
            references.append({**snap,'kind':now['kind'] if now else None,'thumbnail':f"/api/assets/{now['thumbnail']}" if now and now['thumbnail'] else None,
                               'available':bool(current and current['state']=='published' and current['ready'] and not current['hidden'] and not current.get('unavailable_by_parent')),
                               'workspace_ids':current['workspace_ids'] if current else [],'review':reviews.get(snap['id'])})
        return dict(id=pid,context_id=row['context_id'],demand=row['demand'],project_name=row['project_name'],title=row['title'],created=row['created'],
                    workspaces=spaces,workspace_ids=[w['id'] for w in spaces],rationale=payload.get('rationale',''),references=references,payload=payload)

    def review(self,pid,req):
        pack=self.db.one('SELECT context_id,title,payload FROM packs WHERE id=:id',id=pid)
        if not pack:raise Problem(404,'Seleção não encontrada.')
        if req.reference_id not in {r['id'] for r in json.loads(pack['payload'])['references']}:
            raise Problem(422,'Esta referência não faz parte da seleção.')
        with self.db.engine.begin() as conn:
            if req.verdict:
                conn.execute(text('''INSERT INTO pack_reviews(pack_id,ref_id,verdict,note,updated) VALUES(:p,:r,:v,:n,:t)
                    ON CONFLICT(pack_id,ref_id) DO UPDATE SET verdict=excluded.verdict,note=excluded.note,updated=excluded.updated'''),
                             dict(p=pid,r=req.reference_id,v=req.verdict,n=req.note,t=now()))
            else:
                conn.execute(text('DELETE FROM pack_reviews WHERE pack_id=:p AND ref_id=:r'),dict(p=pid,r=req.reference_id))
            self.db.log(conn,'pack_reviewed',req.reference_id,pack['context_id'],pack_id=pid,title=pack['title'],verdict=req.verdict)
        return self.pack_detail(pid)

    def events(self,after=0,workspace_id=None):
        if workspace_id:self.workspace(workspace_id)
        rows=self.db.query('''SELECT e.*,p.name AS project_name FROM events e LEFT JOIN contexts c ON c.id=e.context_id LEFT JOIN projects p ON p.id=c.project_id
            WHERE e.id>:after AND (:w IS NULL OR EXISTS(SELECT 1 FROM event_workspaces ew WHERE ew.event_id=e.id AND ew.workspace_id=:w)
            OR NOT EXISTS(SELECT 1 FROM event_workspaces ew WHERE ew.event_id=e.id)) ORDER BY e.id DESC LIMIT 100''',after=after,w=workspace_id)
        for r in rows:r['payload']=json.loads(r['payload'])
        return rows

    def operation(self,oid):
        row=self.db.one('SELECT * FROM operations WHERE id=:id',id=oid)
        if not row: raise Problem(404,'Operação não encontrada.')
        return {**{k:v for k,v in row.items() if k!='payload'},'target_workspace_ids':[w['workspace_id'] for w in self.db.query('SELECT workspace_id FROM operation_workspaces WHERE operation_id=:id',id=oid)]}
