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
                'vocabulary':self.meta('vocabulary',{}),'principles_available':['narrativa','direcao-de-arte'],'guides_available':self.guides()}

    def guide_files(self):
        """Guias de criação: por papel na história (slides, carrosséis e peças de imagem), por tipo de vídeo,
        formatos, como pedir o vídeo e os dois kits (movimentos do HyperFrames e motor de apresentação em HTML)."""
        root=self.settings.root;found={}
        for folder in (root/'biblioteca/guias',root/'biblioteca/motion/guias'):
            if folder.is_dir():found.update({p.stem:p for p in sorted(folder.glob('*.md')) if p.stem!='LEIA-ME'})
        for name,path in (('kit',root/'kit/motion/LEIA-ME.md'),('kit-apresentacao',root/'kit/LEIA-ME.md')):
            if path.is_file():found[name]=path
        return found

    def guides(self):
        return list(self.guide_files())

    def guide(self,name):
        files=self.guide_files()
        if name not in files:
            raise Problem(404,'Guia não encontrado. Disponíveis: '+', '.join(files))
        return files[name].read_text()

    def summary(self, row):
        d=json.loads(row['payload'])
        out={k:row[k] for k in ['id','kind','title','origin','state','revision','ready','parent_id','updated','hidden']}
        out.update({k:d.get(k) for k in ['description','idea','techniques','intentions','movements','aesthetics','strength','reusable','unclassified','format','number','aspect']})
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
        from .motion import GENRES
        bad=set(data.genres)-set(GENRES)
        if bad: raise Problem(422,f'Tipos de vídeo desconhecidos: {sorted(bad)}. Use {sorted(GENRES)}.')
        for rid in data.source_reference_ids:
            self.get(rid,False,workspace_ids=workspace_ids)

    def update(self,rid,req):
        ids=self.scope(context_id=req.context_id)
        self.get(rid,False,workspace_ids=ids)
        self.validate_data(req.data,ids)
        with self.db.engine.begin() as conn:
            row=conn.execute(text('SELECT * FROM refs WHERE id=:id'),dict(id=rid)).mappings().first()
            if not row: raise Problem(404,'Referência não encontrada.')
            # Tipos e prompt só mudam quando a atualização os informa: o resto da ficha segue como antes.
            changes={k:v for k,v in req.data.model_dump().items() if k not in ('genres','prompt') or k in req.data.model_fields_set}
            d={**json.loads(row['payload']),**changes}
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
