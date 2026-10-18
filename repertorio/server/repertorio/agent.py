"""Busca para agentes: lê frases comuns pelo vocabulário, evita repetir a mesma apresentação e monta a prancha."""
import io
import json
import re
import unicodedata
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
from .db import dumps

STOP=set('a o e de da do das dos em no na nos nas um uma uns umas para pra por com sem que se ao aos as os ou mais muito bem tipo algo coisa quero preciso queria gostaria fazer criar montar slide slides apresentacao apresentacoes palestra deck referencia referencias ideia ideias sobre estilo jeito forma visual bonito legal cima baixo the of and'.split())
# IDs do vocabulário genéricos demais para valer sozinhos (o nome completo continua valendo)
SKIP={('movements','texto')}
KINDS='arquivo,slide,referencia,criacao'
KIND_ORDER={'slide':0,'arquivo':1,'referencia':2,'criacao':3,'midia':4}
KIND_NAMES={'arquivo':'apresentação','slide':'slide','referencia':'referência externa','criacao':'criação','midia':'mídia'}
# campo da ficha, chave no vocabulário, rótulo, peso na pontuação
FIELDS=[('intentions','intencoes','intenção',3.0),('techniques','tecnicas','técnica',2.5),('movements','movimentos','movimento',2.0),('aesthetics','esteticas','estética',1.5)]
# Jeitos comuns de pedir cada item. Os nomes e IDs do vocabulário já entram sozinhos.
EXTRA={
 'intentions':{
  'ABRIR':['abertura','capa','comeco','inicio','primeiro slide','primeira tela','titulo da palestra','gancho'],
  'SITUAR':['agenda','sumario','pauta','indice','contexto','onde estamos'],
  'DIVIDIR':['divisor','capitulo','secao','separador','mudanca de assunto'],
  'IMPACTAR':['impacto','impactante','uau','wow','virada','surpresa','efeito uau','efeito wow'],
  'DESTACAR':['destaque','enfase','frase de efeito','palavra chave','mensagem principal','ideia central'],
  'CITAR':['citacao','depoimento','manifesto','aspas','pergunta retorica','testemunho'],
  'APRESENTAR':['equipe','time','palestrante','quem somos','sobre nos','sobre a empresa','bio','perfil','fundador','socio'],
  'EXPLICAR':['explicacao','conceito','esquema','diagrama','como funciona','metodo','metodologia','framework'],
  'SEQUENCIAR':['processo','passo','passo a passo','etapa','linha do tempo','timeline','jornada','cronologia','evolucao','trajetoria','roadmap','historia da empresa'],
  'AGRUPAR':['lista','card','categoria','pilar','grade','servico','topico','beneficio','funcionalidade'],
  'COMPARAR':['comparacao','comparativo','antes e depois','versus','vs','pros e contras','diferenca','tabela comparativa','concorrente'],
  'PROVAR':['numero','numero grande','dado','grafico','resultado','kpi','metrica','indicador','pesquisa','prova social','estatistica','percentual','porcentagem','crescimento','case'],
  'MOSTRAR':['produto','tela','mockup','galeria','portfolio','demonstracao','demo','aplicativo','app','site','interface','celular'],
  'LOCALIZAR':['mapa','lugar','cidade','pais','regiao','geografia','presenca','unidade','localizacao','endereco'],
  'FECHAR':['fechamento','conclusao','encerramento','final','cta','chamada para acao','contato','obrigado','agradecimento','proximo passo'],
 },
 'techniques':{
  'contraste-de-cor':['cor de destaque','uma cor so'],
  'contraste-de-escala':['titulo gigante','texto gigante','letra gigante','palavra gigante','tipografia gigante'],
  'destaque-tipografico':['marca texto','palavra destacada','grifo'],
  'isolamento':['espaco vazio','respiro','vazio'],
  'foco-seletivo':['holofote','desfoque','escurecer o resto'],
  'sangria-total':['tela cheia','foto inteira','imagem inteira','foto de fundo','imagem de fundo','full bleed','texto por cima','texto sobre a foto','texto sobre foto'],
  'corte-radical':['corte','enquadramento'],
  'textura-e-materia':['textura','grao','materia'],
  'tipografia-como-imagem':['tipografia','letra recortada','texto vazado','letreiro'],
  'palavra-fantasma':['palavra escondida'],
  'eco-tipografico':['palavra repetida','repeticao de palavra'],
  'mascara-de-forma':['mascara','foto dentro da letra','foto dentro de forma','recorte em forma'],
  'profundidade-em-camadas':['camada','profundidade','texto atras'],
  'dado-como-heroi':['numero grande','numero gigante','dado gigante','kpi'],
  'cor-por-capitulo':['cor por secao'],
  'regiao-comum':['caixa','card','cartao','bloco'],
  'conexao':['seta','conector','ligacao','fluxograma'],
  'grade-modular':['grid','mosaico','bento','galeria'],
  'sanfona':['acordeao','acordeon'],
  'simetria-e-eixo':['simetria','espelhado','centralizado'],
  'fechamento':['forma incompleta'],
  'hierarquia-de-leitura':['hierarquia'],
  'numeracao':['numerado','lista numerada'],
  'linha-guia':['linha do tempo','timeline','trilha','caminho'],
  'direcao-de-leitura':['diagonal','leitura em z'],
  'olhar-que-guia':['pessoa olhando','olhar'],
  'revelacao-progressiva':['um por um','um a um','aos poucos','aparecer em sequencia'],
  'camera-continua':['plano sequencia','camera viajando','cenario unico'],
  'sumario-navegavel':['sumario interativo','mapa de navegacao'],
  'progressao-de-escala':['escada','degrau','crescente'],
  'padrao-e-quebra':['quebra de padrao'],
  'metafora-visual':['metafora','analogia'],
  'dupla-exposicao':['silhueta'],
  'trompe-loeil':['rasgo','papel rasgado','fita adesiva','dobra','etiqueta'],
  'transformacao':['antes e depois','metamorfose'],
  'escala-impossivel':['gigante','miniatura','perspectiva forcada'],
  'pergunta-aberta':['pergunta','provocacao'],
  'emprestimo-de-codigo':['passaporte','recibo','manchete','cartaz','ingresso','jornal'],
  'interface-imitada':['notificacao','whatsapp','netflix','chat','busca do google'],
  'referencia-cultural':['homenagem','parodia','meme'],
  'rosto-que-encara':['rosto','retrato','close'],
  'quebra-de-moldura':['sair do quadro','fora da moldura'],
  'inversao-figura-fundo':['figura e fundo','negativo'],
  'objeto-como-suporte':['escrito em','embalagem'],
 },
 'movements':{
  'zoom-mergulho':['zoom','mergulho','aproximar','aproximacao','zoom in'],
  'zoom-recuo':['recuo','afastar','afastamento','zoom out'],
  'panorama':['deslizar','rolagem','travelling'],
  'voo':['voar','entrar voando'],
  'reorganizar':['rearranjar','trocar de lugar'],
  'transformacao':['transformar','morph','metamorfose'],
  'texto':['texto animado','texto em movimento','palavra mudando'],
  'giro':['girar','rotacao','rodar'],
  'revelacao':['revelar','cortina','wipe'],
  'troca':['corte seco','fade','esmaecer'],
  'escalonado':['cascata','um apos o outro','um por um'],
  'foco':['holofote'],
  'loop':['continuo','video de fundo','fundo animado'],
  'contagem':['contador','numero subindo','grafico crescendo'],
  'estatico':['sem animacao','parado'],
 },
 'aesthetics':{
  'minimalista':['minimal','minimalismo','clean','limpo','simples'],
  'corporativo':['empresarial','institucional','executivo'],
  'tecnologico':['tecnologia','tech','digital','inteligencia artificial','ia'],
  'futurista':['futuro','sci fi'],
  'ludico':['brincalhao','divertido'],
  'luxo':['luxuoso','premium','sofisticado','elegante'],
  'vidro':['glass','glassmorphism','vidro fosco'],
  '3d':['tridimensional'],
  'fotografico':['foto','fotografia'],
  'preto-e-branco':['pb'],
  'ilustrado':['ilustracao'],
  'escuro':['fundo escuro','fundo preto','dark','preto'],
  'claro':['fundo claro','fundo branco','branco'],
  'gradiente':['degrade'],
  'cinematografico':['cinema','cinematica'],
  'esportivo':['esporte'],
  'gastronomico':['comida','gastronomia','restaurante'],
  'cientifico':['ciencia'],
 },
}


def norm(s):
    s=unicodedata.normalize('NFKD',str(s or '')).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+',' ',s).split()


def singular(w):
    if len(w)<=3 or w.endswith('ss'):return w
    for end,rep in (('oes','ao'),('aes','ao'),('ais','al'),('eis','el'),('res','r'),('zes','z')):
        if w.endswith(end):return w[:-len(end)]+rep
    return w[:-1] if w.endswith('s') else w


def phrases(vocab):
    table={}
    def add(text,field,value):
        key=tuple(singular(w) for w in norm(text))
        if key and (field,value) not in table.setdefault(key,[]):table[key].append((field,value))
    for field,key,_,_ in FIELDS:
        known=set()
        for item in vocab.get(key,{}).get('itens',[]):
            value=item['id'] if isinstance(item,dict) else item
            known.add(value)
            if (field,value) not in SKIP:add(value.replace('-',' '),field,value)
            if isinstance(item,dict) and item.get('nome'):add(item['nome'],field,value)
        for value,extra in EXTRA[field].items():
            if value in known:
                for text in extra:add(text,field,value)
    return table


def interpret(query,vocab):
    """Converte o pedido em itens do vocabulário; o que sobra vira busca por texto."""
    table=phrases(vocab);longest=max(map(len,table),default=1)
    words=norm(query);found={f:[] for f,*_ in FIELDS};understood=[];text=[]
    i=0
    while i<len(words):
        for n in range(min(longest,len(words)-i),0,-1):
            key=tuple(singular(w) for w in words[i:i+n])
            if key in table:
                for field,value in table[key]:
                    if value not in found[field]:found[field].append(value)
                labels={f:l for f,_,l,_ in FIELDS}
                understood.append(dict(term=' '.join(words[i:i+n]),meaning=[f'{labels[f]}: {v}' for f,v in table[key]]))
                # estética é sinal fraco e costuma ser também o assunto: continua valendo como texto
                if all(f=='aesthetics' for f,_ in table[key]):text+=[w for w in words[i:i+n] if w not in STOP]
                i+=n;break
        else:
            if words[i] not in STOP and len(words[i])>1:text.append(words[i])
            i+=1
    terms=[]
    for w in text:
        s=singular(w);t=s if w.startswith(s) else w
        if t not in terms:terms.append(t)
    return found,understood,terms[:30]


def smart_search(lib,args,log=True):
    ids=lib.scope(args.workspace_ids,args.context_id)
    found,understood,terms=interpret(args.query,lib.meta('vocabulary',{}))
    params={}
    clauses=lib.filters(args.model_copy(update={'kind':args.kind or KINDS}),params)
    soft=[];join='';rank='NULL AS rank'
    for field,*_ in FIELDS:
        if found[field]:
            params['v_'+field]=dumps(found[field])
            soft.append(f"EXISTS(SELECT 1 FROM json_each(r.payload,'$.{field}') WHERE value IN (SELECT value FROM json_each(:v_{field})))")
    if terms:
        params['match']=' OR '.join('"'+w+'"*' for w in terms)
        join=' LEFT JOIN (SELECT id AS sid,bm25(ref_search,0,5,1) AS rank FROM ref_search WHERE ref_search MATCH :match) t ON t.sid=r.id'
        rank='t.rank AS rank';soft.append('t.sid IS NOT NULL')
    if soft:clauses.append('('+' OR '.join(soft)+')')
    rows=lib.db.query(f'''SELECT r.id,r.kind,r.parent_id,{rank},COALESCE(json_extract(r.payload,'$.strength'),3) AS strength,
        json_extract(r.payload,'$.intentions') AS intentions,json_extract(r.payload,'$.techniques') AS techniques,
        json_extract(r.payload,'$.movements') AS movements,json_extract(r.payload,'$.aesthetics') AS aesthetics
        FROM refs r{join} WHERE {' AND '.join(clauses)}''',**params)
    best=min([r['rank'] for r in rows if r['rank'] is not None],default=0)
    scored=[]
    for r in rows:
        score=0.7*r['strength'];hits=[]
        if r['rank'] is not None and best<0:
            score+=3*r['rank']/best;hits.append('texto: '+' '.join(terms))
        for field,_,label,weight in FIELDS:
            common=[v for v in found[field] if v in json.loads(r[field] or '[]')]
            score+=weight*len(common);hits+=[f'{label}: {v}' for v in common]
        scored.append((score,r,hits))
    scored.sort(key=lambda x:(-x[0],KIND_ORDER.get(x[1]['kind'],9),x[1]['id']))
    seen={};kept=[]
    for item in scored:
        key=item[1]['parent_id'] or item[1]['id']
        if seen.get(key,0)<args.per_group:
            seen[key]=seen.get(key,0)+1;kept.append(item)
    page=kept[args.offset:args.offset+args.limit]
    items=[]
    for n,(_,r,hits) in enumerate(page,args.offset+1):
        row=lib.db.one('''SELECT r.*,(SELECT a.id FROM assets a WHERE a.ref_id=r.id AND a.missing=0 AND a.role IN ('thumbnail','preview') ORDER BY CASE a.role WHEN 'thumbnail' THEN 0 ELSE 1 END,a.id LIMIT 1) AS thumbnail
            FROM refs r WHERE r.id=:id''',id=r['id'])
        items.append({'n':n,**lib.scoped_summary(row,ids,state=args.state),'matched_by':hits})
    if log and args.context_id:
        with lib.db.engine.begin() as conn:
            lib.db.log(conn,'references_searched',context_id=args.context_id,query=args.query,total=len(kept))
    return dict(items=items,total=len(kept),offset=args.offset,limit=args.limit,understood=understood,text_terms=terms)


def sheet_items(lib,ids,workspace_ids=None,context_id=None):
    scope=lib.scope(workspace_ids,context_id)
    rows={r['id']:r for r in lib.db.query('SELECT * FROM refs WHERE id IN (SELECT value FROM json_each(:ids))',ids=dumps(ids))}
    result=[]
    for n,i in enumerate(ids,1):
        if i in rows:
            ref=lib.get(i,False,workspace_ids=scope)
            if ref['state']=='published' and ref['ready'] and not ref['hidden'] and not ref.get('unavailable_by_parent'):
                result.append({'n':n,**ref})
    return result


def font(bold,size):
    for name in (['Arial Bold.ttf'] if bold else ['Arial.ttf']):
        try:return ImageFont.truetype('/System/Library/Fonts/Supplemental/'+name,size)
        except OSError:pass
    try:return ImageFont.load_default(size)
    except TypeError:return ImageFont.load_default()


def fit(draw,text,face,width):
    text=' '.join(str(text or '').split())
    if draw.textlength(text,font=face)<=width:return text
    while text and draw.textlength(text+'...',font=face)>width:text=text[:-1]
    return text.rstrip(' .,;:')+'...'


def picture(lib,item):
    """Apresentação usa o primeiro slide visível: a miniatura do mapa é pequena e a prévia é uma faixa com todos."""
    a=None
    if item.get('kind')=='arquivo':
        params={'id':item['id']}
        clause=lib.membership_clause(item['workspace_ids'],params,'published',alias='c')
        a=lib.db.one(f"""SELECT a.path FROM refs c JOIN assets a ON a.ref_id=c.id AND a.role='preview' AND a.missing=0
            WHERE c.parent_id=:id AND c.hidden=0 AND {clause} ORDER BY CAST(json_extract(c.payload,'$.number') AS INTEGER) LIMIT 1""",**params)
    a=a or lib.db.one("SELECT path FROM assets WHERE ref_id=:id AND missing=0 AND role IN ('thumbnail','preview') ORDER BY CASE role WHEN 'preview' THEN 0 ELSE 1 END,path,id LIMIT 1",id=item['id'])
    return Path(a['path']) if a else None


def contact_sheet(lib,items,cell=380,gap=12):
    """Prancha numerada na mesma ordem dos itens, para o agente ver tudo de uma vez."""
    items=items[:24]
    if not items:return None
    cols=min(4,len(items));ih=round(cell*9/16);caption=56;rows=-(-len(items)//cols)
    sheet=Image.new('RGB',(gap+cols*(cell+gap),gap+rows*(ih+caption+gap)),(18,18,18))
    draw=ImageDraw.Draw(sheet);title=font(True,19);meta=font(False,16);badge=font(True,20)
    for k,item in enumerate(items):
        x=gap+(k%cols)*(cell+gap);y=gap+(k//cols)*(ih+caption+gap)
        frame=Image.new('RGB',(cell,ih),(42,42,42))
        path=picture(lib,item)
        if path and path.suffix.lower() in {'.jpg','.jpeg','.png','.webp','.gif'} and (path.is_relative_to(lib.settings.root) or path.is_relative_to(lib.settings.home)):
            try:
                with Image.open(path) as im:
                    im=ImageOps.contain(im.convert('RGBA'),(cell,ih));frame.paste(im,((cell-im.width)//2,(ih-im.height)//2),im)
            except OSError:path=None
        else:path=None
        sheet.paste(frame,(x,y))
        if not path:draw.text((x+cell//2,y+ih//2),'sem prévia',font=meta,fill=(150,150,150),anchor='mm')
        label=str(item.get('n',k+1));w=draw.textlength(label,font=badge)+16
        draw.rectangle([x,y,x+w,y+28],fill=(255,90,60));draw.text((x+8,y+3),label,font=badge,fill=(255,255,255))
        draw.text((x,y+ih+6),fit(draw,item.get('title'),title,cell),font=title,fill=(236,232,225))
        details=[KIND_NAMES.get(item.get('kind'),item.get('kind')),f"força {item.get('strength') or 3}"]+(item.get('intentions') or [])[:2]
        if item.get('reusable') is False:details.append('mídia de terceiros')
        draw.text((x,y+ih+31),fit(draw,' · '.join(details),meta,cell),font=meta,fill=(160,155,147))
    buf=io.BytesIO();sheet.save(buf,format='JPEG',quality=82);return buf.getvalue()
