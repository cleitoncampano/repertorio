import type {GraphData} from './types';
import {colors,terms} from './types';
import type {ElementDefinition} from 'cytoscape';
import type {GraphView} from './graphViewOptions';
import {isExperimental} from './graphSkins';
import {arrangeAlternate} from './alternateLayouts';

// Capas com o dobro do tamanho original, em imagens e vídeos. O espaçamento entre as capas cresce na mesma
// proporção em todas as visualizações, para nada se sobrepor.
export const COVER_SCALE=2;

// The prototype's radial grammar: operation → cue → technique → reference.
// Seeded placement feels organic without moving the library on every refresh.
function freeLayout(graph:GraphData):ElementDefinition[]{
 const nodes:ElementDefinition[]=[],edges:ElementDefinition[]=[];
 const ops=terms(graph.vocabulary,'operacoes'),tech=terms(graph.vocabulary,'tecnicas');
 const cues=terms(graph.vocabulary,'pistas');
 const positions=new Map<string,{x:number;y:number;a:number}>();
 const angles:Record<string,number>={diferenciacao:-Math.PI/2,agrupamento:0,sequencia:Math.PI/2,previsao:Math.PI};
 const colorFor=(id:string)=>colors[tech.find(t=>t.id===id)?.operacao||'']||'#8f8a82';
 ops.forEach((op,i)=>{
  const angle=angles[op.id]??(-Math.PI/2+i*2*Math.PI/Math.max(ops.length,1));
  nodes.push({data:{id:'op:'+op.id,entity:op.id,type:'operation',operation:op.id,label:op.nome||op.id,color:colors[op.id]},position:{x:Math.cos(angle)*300,y:Math.sin(angle)*300}});
  const ts=tech.filter(t=>t.operacao===op.id).sort((a,b)=>cues.findIndex(c=>c.id===a.pista)-cues.findIndex(c=>c.id===b.pista)||(a.nome||a.id).localeCompare(b.nome||b.id));
  const groups=new Map<string,number[]>();
  ts.forEach((t,j)=>{
   const a=angle-Math.PI/4+.09+(j+.5)*(Math.PI/2-.18)/ts.length;
   const p={x:Math.cos(a)*780,y:Math.sin(a)*780,a};positions.set(t.id,p);
   const cue=cues.find(c=>c.id===t.pista);
   if(cue)groups.set(cue.id,[...(groups.get(cue.id)||[]),a]);
   nodes.push({data:{id:'tech:'+t.id,entity:t.id,type:'technique',operation:op.id,cue:cue?.id,label:t.nome||t.id,color:colors[op.id],rotation:Math.cos(a)>=0?a:a+Math.PI,labelSide:Math.cos(a)>=0?'right':'left'},position:p});
   edges.push({data:{id:'e-structure:'+t.id,source:cue?'cue:'+op.id+':'+cue.id:'op:'+op.id,target:'tech:'+t.id,operation:op.id,structure:true,distance:0,weight:.5,color:colors[op.id]}});
  });
  groups.forEach((as,id)=>{
   const a=as.reduce((s,x)=>s+x,0)/as.length;
   nodes.push({data:{id:'cue:'+op.id+':'+id,entity:op.id,type:'cue',operation:op.id,label:cues.find(c=>c.id===id)?.nome||id,color:colors[op.id]},position:{x:Math.cos(a)*540,y:Math.sin(a)*540}});
   edges.push({data:{id:'e-cue:'+op.id+':'+id,source:'op:'+op.id,target:'cue:'+op.id+':'+id,operation:op.id,structure:true,distance:0,weight:.5,color:colors[op.id]}});
  });
 });
 let seed=7;
 const random=()=> (seed=(seed*16807)%2147483647)/2147483647;
 const placements=graph.items.slice().sort((a,b)=>a.id.localeCompare(b.id)).map(item=>{
  let x=0,y=0;for(const t of item.techniques){const p=positions.get(t);if(p){x+=Math.cos(p.a);y+=Math.sin(p.a);}}
  return {item,target:(x||y)?Math.atan2(y,x):random()*Math.PI*2-Math.PI,angle:0};
 });
 placements.sort((a,b)=>a.target-b.target).forEach((p,i)=>{
  const spread=-Math.PI+2*Math.PI*(i+.5)/placements.length;
  const difference=Math.atan2(Math.sin(spread-p.target),Math.cos(spread-p.target));
  p.angle=p.target+.7*difference;
 });
 const S=COVER_SCALE,occupied=new Set<string>(),cell=108*S;
 const bands:Record<number,[number,number]>={5:[1080,1300],4:[1160,1780],3:[1450,2260],2:[2000,2420],1:[2150,2550]};
 placements.sort((a,b)=>(b.item.strength||3)-(a.item.strength||3));
 for(const {item,angle} of placements){
  const strength=Math.max(1,Math.min(5,item.strength||3));
  const [r0,r1]=bands[strength],r=r0+random()*(r1-r0);
  const gx0=Math.round(Math.cos(angle)*r/cell),gy0=Math.round(Math.sin(angle)*r/cell);
  let point:{x:number;y:number}|undefined;
  for(let ring=0;!point;ring++){
   for(let dx=-ring;dx<=ring&&!point;dx++)for(let dy=-ring;dy<=ring&&!point;dy++){
    if(Math.max(Math.abs(dx),Math.abs(dy))!==ring)continue;
    const gx=gx0+dx,gy=gy0+dy,key=gx+':'+gy;
    if(occupied.has(key)||Math.hypot(gx*cell,gy*cell)<1040)continue;
    occupied.add(key);point={x:gx*cell+(random()-.5)*16*S,y:gy*cell+(random()-.5)*16*S};
   }
  }
  const size=({5:90,4:74,3:62,2:50,1:42}[strength]||62)*COVER_SCALE;
  nodes.push({data:{id:'ref:'+item.id,entity:item.id,type:'reference',operation:tech.find(t=>t.id===item.techniques[0])?.operacao||'',label:item.title,image:'none',preview:item.thumbnail||'',color:item.techniques.length?colorFor(item.techniques[0]):'#8f8a82',size,width:size,height:size*9/16,external:item.origin==='externa'},position:point});
  for(const tid of item.techniques){
   const target=positions.get(tid);if(!target)continue;
   // The same inward quadratic control point as the prototype, represented
   // in Cytoscape's source/target coordinate system.
   const dx=target.x-point.x,dy=target.y-point.y,length=Math.hypot(dx,dy)||1;
   const cx=(point.x+target.x)*.36,cy=(point.y+target.y)*.36;
   const weight=((cx-point.x)*dx+(cy-point.y)*dy)/(length*length);
   const distance=((cx-point.x)*-dy+(cy-point.y)*dx)/length;
   edges.push({data:{id:'e:'+item.id+':'+tid,source:'ref:'+item.id,target:'tech:'+tid,operation:tech.find(t=>t.id===tid)?.operacao||'',color:colorFor(tid),weight,distance}});
  }
 }
 return [...nodes,...edges];
}

export function layoutGraph(graph:GraphData,view:GraphView='free'):ElementDefinition[]{
 const elements=freeLayout(graph);
 if(view==='free')return elements;
 const nodes=new Map<string,ElementDefinition>(elements.filter(node=>node.position).map(node=>[node.data.id!,node]));
 const ops=terms(graph.vocabulary,'operacoes'),techniques=terms(graph.vocabulary,'tecnicas');
 const validTechniques=techniques.filter(tech=>nodes.has('tech:'+tech.id));
 const order=new Map(validTechniques.map((tech,index)=>[tech.id,index]));
 const byId=new Map(validTechniques.map(tech=>[tech.id,tech]));
 const primary=new Map<string,string>();
 // Cada peça ocupa um lugar só. Todas as suas conexões continuam visíveis.
 for(const item of graph.items){
  const counts=new Map<string,number>();
  item.techniques.forEach(id=>{const op=byId.get(id)?.operacao;if(op)counts.set(op,(counts.get(op)||0)+1);});
  const op=ops.slice().sort((a,b)=>(counts.get(b.id)||0)-(counts.get(a.id)||0)).find(op=>counts.has(op.id));
  if(!op)continue;
  const first=item.techniques.filter(id=>byId.get(id)?.operacao===op.id).sort((a,b)=>order.get(a)!-order.get(b)!)[0];
  if(first)primary.set(item.id,first);
 }
 const S=COVER_SCALE;
 const place=(id:string,x:number,y:number)=>{const node=nodes.get(id);if(node){node.position={x,y};if(node.data.type==='technique'){node.data.rotation=0;node.data.labelSide='right';}}};
 if(isExperimental(view)){
  graph.items.forEach(item=>{nodes.get('ref:'+item.id)!.data.operation=byId.get(primary.get(item.id)||'')?.operacao||'';});
  arrangeAlternate({graph,nodes,ops,techniques:validTechniques,primary,place,scale:S},view);
 }else if(view==='grouped'){
  const groups=[...ops.map(op=>({id:op.id,items:graph.items.filter(item=>byId.get(primary.get(item.id)||'')?.operacao===op.id)}))];
  const unclassified=graph.items.filter(item=>!primary.has(item.id));
  if(unclassified.length)groups.push({id:'',items:unclassified});
  const layouts=groups.map(group=>{
   const tech=validTechniques.filter(tech=>tech.operacao===group.id),points:{x:number;y:number}[]=[];
   // Une os anéis internos às referências sem sobrepor suas miniaturas.
   const inner=Math.max(500,tech.length*26),cell=116*S;
   for(let ring=0;points.length<group.items.length;ring++){
    for(let x=-ring;x<=ring;x++)for(let y=-ring;y<=ring;y++){
     if(Math.max(Math.abs(x),Math.abs(y))!==ring||Math.hypot(x*cell,y*cell)<inner)continue;
     points.push({x:x*cell,y:y*cell});
    }
   }
   points.sort((a,b)=>Math.hypot(a.x,a.y)-Math.hypot(b.x,b.y)||a.x-b.x||a.y-b.y);
   const chosen=points.slice(0,group.items.length).sort((a,b)=>Math.atan2(a.y,a.x)-Math.atan2(b.y,b.x));
   return {...group,tech,points:chosen,radius:Math.max(inner+80,...chosen.map(point=>Math.hypot(point.x,point.y)+70*S))};
  });
  const columns=Math.max(1,Math.ceil(Math.sqrt(layouts.length))),widths:number[]=[],heights:number[]=[];
  layouts.forEach((group,index)=>{const col=index%columns,row=Math.floor(index/columns);widths[col]=Math.max(widths[col]||0,group.radius*2);heights[row]=Math.max(heights[row]||0,group.radius*2);});
  const start=(sizes:number[],index:number)=>sizes.slice(0,index).reduce((sum,size)=>sum+size+200,0)+sizes[index]/2;
  layouts.forEach((group,index)=>{
   const x=start(widths,index%columns),y=start(heights,Math.floor(index/columns));
   place('op:'+group.id,x,y);
   const cues=Array.from(nodes.values()).filter(node=>node.data.type==='cue'&&node.data.operation===group.id);
   cues.forEach((node,i)=>{const angle=-Math.PI/2+2*Math.PI*i/cues.length;place(node.data.id!,x+Math.cos(angle)*220,y+Math.sin(angle)*220);});
   group.tech.forEach((tech,i)=>{const angle=-Math.PI/2+2*Math.PI*(i+.5)/group.tech.length;place('tech:'+tech.id,x+Math.cos(angle)*360,y+Math.sin(angle)*360);const node=nodes.get('tech:'+tech.id)!;node.data.labelSide=Math.cos(angle)<0?'left':'right';});
   group.items.slice().sort((a,b)=>(order.get(primary.get(a.id)||'')??Infinity)-(order.get(primary.get(b.id)||'')??Infinity)||a.id.localeCompare(b.id)).forEach((item,i)=>place('ref:'+item.id,x+group.points[i].x,y+group.points[i].y));
  });
 }else{
  let top=0;
  const gap=108*S,columns=Math.max(2,Math.min(36,Math.ceil(Math.sqrt(graph.items.length)*1.2)));
  for(const op of ops){
   const start=top;
   const cuePositions=new Map<string,number[]>();
   for(const tech of validTechniques.filter(tech=>tech.operacao===op.id).sort((a,b)=>(a.pista||'').localeCompare(b.pista||'')||(a.nome||a.id).localeCompare(b.nome||b.id))){
    const items=graph.items.filter(item=>primary.get(item.id)===tech.id).sort((a,b)=>a.id.localeCompare(b.id));
    const height=items.length?Math.ceil(items.length/columns)*gap+16:52,middle=top+height/2;
    place('tech:'+tech.id,1200,middle);
    if(tech.pista)cuePositions.set(tech.pista,[...(cuePositions.get(tech.pista)||[]),middle]);
    items.forEach((item,i)=>place('ref:'+item.id,2400+i%columns*124*S,top+height/2-(Math.ceil(items.length/columns)-1)*gap/2+Math.floor(i/columns)*gap));
    top+=height;
   }
   top=Math.max(top,start+200);
   place('op:'+op.id,0,(start+top)/2);
   cuePositions.forEach((ys,cue)=>place('cue:'+op.id+':'+cue,600,ys.reduce((sum,y)=>sum+y,0)/ys.length));
   top+=120;
  }
  graph.items.filter(item=>!primary.has(item.id)).sort((a,b)=>a.id.localeCompare(b.id)).forEach((item,i)=>place('ref:'+item.id,2400+i%columns*124*S,top+Math.floor(i/columns)*gap));
 }
 // Mantém os mesmos nós e relações; apenas reposiciona e simplifica as curvas.
 elements.filter(element=>!element.position).forEach(edge=>{
  edge.data.distance=0;edge.data.weight=.5;
  if(!edge.data.structure)edge.data.cross='tech:'+primary.get(String(edge.data.source).slice(4))!==edge.data.target;
  if(view==='cosmos'||view==='garden'){
   const a=nodes.get(String(edge.data.source))?.position,b=nodes.get(String(edge.data.target))?.position;
   if(a&&b)edge.data.distance=Math.hypot(a.x-b.x,a.y-b.y)*(view==='garden'?.12:.08);
  }
 });
 return elements;
}
