import hashlib
import json
import re
import uuid
from pathlib import Path
from sqlalchemy import text
from .db import dumps, now
from .importer import index_text
from .schemas import Search


class Problem(Exception):
    def __init__(self, status, message):
        self.status, self.message = status, message


class Library:
    def __init__(self, db):
        self.db = db
        self.settings = db.settings

    def meta(self, key, default=None):
        row = self.db.one('SELECT value FROM meta WHERE key=:key',key=key)
        return json.loads(row['value']) if row else default

    def stats(self):
        rows = self.db.query("SELECT kind,COUNT(*) AS total FROM refs r WHERE state='published' AND ready=1 AND hidden=0 AND NOT EXISTS(SELECT 1 FROM refs p WHERE p.id=r.parent_id AND (p.state!='published' OR p.hidden=1)) GROUP BY kind")
        return dict(counts={r['kind']:r['total'] for r in rows}, report=self.meta('import_report',{}),
                    pending=self.db.one("SELECT COUNT(*) AS n FROM refs WHERE state='pending'")['n'],
                    projects=self.db.one('SELECT COUNT(*) AS n FROM projects')['n'])

    def context(self, cid):
        row = self.db.one('SELECT c.*,p.name AS project_name,p.root FROM contexts c JOIN projects p ON c.project_id=p.id WHERE c.id=:id',id=cid)
        if not row:
            raise Problem(404,'Contexto não encontrado. Inicie uma demanda com start_context.')
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
        if not self.db.one('SELECT id FROM projects WHERE id=:id',id=data.project_id):
            raise Problem(404,'Cadastre esta pasta primeiro com repertorio connect.')
        row=dict(id=str(uuid.uuid4()),project_id=data.project_id,demand=data.demand,created=now())
        with self.db.engine.begin() as conn:
            conn.execute(text('INSERT INTO contexts VALUES(:id,:project_id,:demand,:created)'),row)
            self.db.log(conn,'context_started',context_id=row['id'],demand=data.demand)
        return {**row,'instructions':'História primeiro. Busque referências, examine imagens e adapte a ideia à identidade do projeto. Não copie. Publique apenas quando o usuário solicitar; sugestões ficam pendentes.',
                'vocabulary':self.meta('vocabulary',{}),'principles_available':['narrativa','direcao-de-arte']}

    def summary(self, row):
        d=json.loads(row['payload'])
        out={k:row[k] for k in ['id','kind','title','origin','state','revision','ready','parent_id','updated','hidden']}
        out.update({k:d.get(k) for k in ['description','idea','techniques','intentions','movements','aesthetics','strength','reusable','unclassified','format','number']})
        aid=row.get('thumbnail')
        if aid:
            out['thumbnail']=f'/api/assets/{aid}'
        out['url']=self.settings.url+'/?ref='+__import__('urllib.parse',fromlist=['quote']).quote(row['id'],safe='')
        return out

    def filters(self, args, params):
        """Condições estritas compartilhadas pela busca do mapa e pela busca dos agentes."""
        params.update(state=args.state,min_strength=args.min_strength)
        clauses=['r.state=:state']
        if args.state == 'published':
            clauses += ['r.ready=1','r.hidden=0',"NOT EXISTS(SELECT 1 FROM refs p WHERE p.id=r.parent_id AND (p.state!='published' OR p.ready=0 OR p.hidden=1))"]
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
        if args.context_id:
            self.context(args.context_id)
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
        for r in rows:
            s=self.summary(r)
            s['matched_by']=[f'{k}: {getattr(args,k)}' for k in ['intention','technique','operation','movement','aesthetic','origin','format'] if getattr(args,k)]
            if words: s['matched_by'].insert(0,'Texto da ficha ou do slide')
            results.append(s)
        if log and args.context_id:
            with self.db.engine.begin() as conn:
                self.db.log(conn,'references_searched',context_id=args.context_id,query=args.query,total=total)
        return dict(items=results,total=total,offset=args.offset,limit=args.limit)

    def get(self,rid,include_children=True):
        row=self.db.one('SELECT * FROM refs WHERE id=:id',id=rid)
        if not row: raise Problem(404,'Referência não encontrada.')
        data=json.loads(row['payload'])
        out={**self.summary(row),**{k:v for k,v in data.items() if k!='legacy'}}
        out['assets']=[{**a,'url':f"/api/assets/{a['id']}"} for a in self.db.query('SELECT id,role,mime,missing FROM assets WHERE ref_id=:id ORDER BY role,path,id',id=rid)]
        if row['parent_id']:
            parent=self.db.one('SELECT state,hidden FROM refs WHERE id=:id',id=row['parent_id'])
            out['unavailable_by_parent']=bool(parent and (parent['state']!='published' or parent['hidden']))
        if include_children:
            children=self.db.query("SELECT * FROM refs WHERE parent_id=:id AND state='published' AND hidden=0 ORDER BY CAST(json_extract(payload,'$.number') AS INTEGER)",id=rid)
            out['children']=[self.summary(c) for c in children]
            for child in out['children']:
                a=self.db.one("SELECT id FROM assets WHERE ref_id=:id AND role='preview' AND missing=0 LIMIT 1",id=child['id'])
                child['thumbnail']=f"/api/assets/{a['id']}" if a else None
        out['transitions']=self.meta('transitions:'+rid,[])
        related=[]
        for technique in out.get('techniques',[])[:3]:
            related.extend(self.search(Search(technique=technique,kind='arquivo,referencia,criacao',limit=8),log=False)['items'])
        out['related']=list({r['id']:r for r in related if r['id']!=rid}.values())[:6]
        return out

    def validate_data(self,data):
        vocab=self.meta('vocabulary',{})
        for field,key in [('techniques','tecnicas'),('intentions','intencoes'),('movements','movimentos'),('aesthetics','esteticas')]:
            allowed={i['id'] if isinstance(i,dict) else i for i in vocab.get(key,{}).get('itens',[])}
            bad=set(getattr(data,field))-allowed
            if bad: raise Problem(422,f'Valores fora do vocabulário em {field}: {sorted(bad)}')
        for rid in data.source_reference_ids:
            if not self.db.one('SELECT id FROM refs WHERE id=:id',id=rid):
                raise Problem(422,f'Referência de origem não encontrada: {rid}')

    def update(self,rid,req):
        self.context(req.context_id); self.validate_data(req.data)
        with self.db.engine.begin() as conn:
            row=conn.execute(text('SELECT * FROM refs WHERE id=:id'),dict(id=rid)).mappings().first()
            if not row: raise Problem(404,'Referência não encontrada.')
            d={**json.loads(row['payload']),**req.data.model_dump()}
            changed=conn.execute(text('UPDATE refs SET title=:title,payload=:p,search_text=:s,curated=1,revision=revision+1,updated=:t WHERE id=:id AND revision=:rev'),
                                 dict(title=d['title'],p=dumps(d),s=index_text(d),t=now(),id=rid,rev=req.expected_revision))
            if changed.rowcount!=1: raise Problem(409,'A referência mudou. Leia a revisão atual antes de atualizar.')
            conn.execute(text('INSERT INTO revisions VALUES(:id,:r,:p)'),dict(id=rid,r=row['revision'],p=dumps(dict(row))))
            self.db.log(conn,'reference_updated',rid,req.context_id,revision=row['revision']+1)
        return self.get(rid)

    def state(self,rid,req,from_ui=False):
        if req.context_id: self.context(req.context_id)
        if not from_ui and not req.context_id: raise Problem(422,'Informe o contexto da alteração.')
        if not from_ui and req.state in ('published','trashed') and not req.user_requested:
            raise Problem(422,'Publicação e exclusão pelo agente exigem pedido explícito do usuário.')
        with self.db.engine.begin() as conn:
            row=conn.execute(text('SELECT * FROM refs WHERE id=:id'),dict(id=rid)).mappings().first()
            if not row: raise Problem(404,'Referência não encontrada.')
            changed=conn.execute(text('UPDATE refs SET state=:state,curated=1,revision=revision+1,updated=:t WHERE id=:id AND revision=:rev'),
                                 dict(state=req.state,t=now(),id=rid,rev=req.expected_revision))
            if changed.rowcount!=1: raise Problem(409,'A referência mudou. Atualize antes de tentar novamente.')
            conn.execute(text('INSERT INTO revisions VALUES(:id,:r,:p)'),dict(id=rid,r=row['revision'],p=dumps(dict(row))))
            self.db.log(conn,'reference_'+req.state,rid,req.context_id,previous_state=row['state'],user_requested=req.user_requested or from_ui)
        return self.get(rid)

    def pack(self,req):
        self.context(req.context_id)
        snapshots=[]
        for rid in dict.fromkeys(req.reference_ids):
            ref=self.get(rid,False)
            if ref['state']!='published' or not ref['ready'] or ref.get('hidden') or ref.get('unavailable_by_parent'):
                raise Problem(409,'Uma referência selecionada não está disponível.')
            snapshots.append({k:ref.get(k) for k in ['id','revision','title','description','idea','techniques','intentions','movements','aesthetics','reusable','usage_notes','assets','url']})
        pid=str(uuid.uuid4())
        payload=dict(references=snapshots,rationale=req.rationale)
        with self.db.engine.begin() as conn:
            conn.execute(text('INSERT INTO packs VALUES(:id,:c,:t,:p,:d)'),dict(id=pid,c=req.context_id,t=req.title,p=dumps(payload),d=now()))
            self.db.log(conn,'pack_created',context_id=req.context_id,pack_id=pid,title=req.title)
        return dict(id=pid,context_id=req.context_id,title=req.title,**payload)

    def events(self,after=0):
        rows=self.db.query('SELECT e.*,p.name AS project_name FROM events e LEFT JOIN contexts c ON c.id=e.context_id LEFT JOIN projects p ON p.id=c.project_id WHERE e.id>:after ORDER BY e.id DESC LIMIT 100',after=after)
        for r in rows:r['payload']=json.loads(r['payload'])
        return rows

    def operation(self,oid):
        row=self.db.one('SELECT * FROM operations WHERE id=:id',id=oid)
        if not row: raise Problem(404,'Operação não encontrada.')
        return {k:v for k,v in row.items() if k!='payload'}
