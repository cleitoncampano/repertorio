import type {GraphData} from './types';
import {colors,terms} from './types';
import type {ElementDefinition} from 'cytoscape';

// The prototype's radial grammar: operation → cue → technique → reference.
// Seeded placement feels organic without moving the library on every refresh.
export function layoutGraph(graph:GraphData):ElementDefinition[]{
 const nodes:ElementDefinition[]=[],edges:ElementDefinition[]=[];
 const ops=terms(graph.vocabulary,'operacoes'),tech=terms(graph.vocabulary,'tecnicas');
 const cues=terms(graph.vocabulary,'pistas');
 const positions=new Map<string,{x:number;y:number;a:number}>();
 const angles:Record<string,number>={diferenciacao:-Math.PI/2,agrupamento:0,sequencia:Math.PI/2,previsao:Math.PI};
 const colorFor=(id:string)=>colors[tech.find(t=>t.id===id)?.operacao||'']||'#8f8a82';
 ops.forEach((op,i)=>{
  const angle=angles[op.id]??(-Math.PI/2+i*2*Math.PI/Math.max(ops.length,1));
  nodes.push({data:{id:'op:'+op.id,entity:op.id,type:'operation',label:op.nome||op.id,color:colors[op.id]},position:{x:Math.cos(angle)*300,y:Math.sin(angle)*300}});
  const ts=tech.filter(t=>t.operacao===op.id).sort((a,b)=>cues.findIndex(c=>c.id===a.pista)-cues.findIndex(c=>c.id===b.pista)||(a.nome||a.id).localeCompare(b.nome||b.id));
  const groups=new Map<string,number[]>();
  ts.forEach((t,j)=>{
   const a=angle-Math.PI/4+.09+(j+.5)*(Math.PI/2-.18)/ts.length;
   const p={x:Math.cos(a)*780,y:Math.sin(a)*780,a};positions.set(t.id,p);
   const cue=cues.find(c=>c.id===t.pista);
   if(cue)groups.set(cue.id,[...(groups.get(cue.id)||[]),a]);
   nodes.push({data:{id:'tech:'+t.id,entity:t.id,type:'technique',operation:op.id,cue:cue?.id,label:t.nome||t.id,color:colors[op.id],rotation:Math.cos(a)>=0?a:a+Math.PI,labelSide:Math.cos(a)>=0?'right':'left'},position:p});
   edges.push({data:{id:'e-structure:'+t.id,source:cue?'cue:'+op.id+':'+cue.id:'op:'+op.id,target:'tech:'+t.id,structure:true,distance:0,weight:.5,color:colors[op.id]}});
  });
  groups.forEach((as,id)=>{
   const a=as.reduce((s,x)=>s+x,0)/as.length;
   nodes.push({data:{id:'cue:'+op.id+':'+id,entity:op.id,type:'cue',operation:op.id,label:cues.find(c=>c.id===id)?.nome||id,color:colors[op.id]},position:{x:Math.cos(a)*540,y:Math.sin(a)*540}});
   edges.push({data:{id:'e-cue:'+op.id+':'+id,source:'op:'+op.id,target:'cue:'+op.id+':'+id,structure:true,distance:0,weight:.5,color:colors[op.id]}});
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
 const occupied=new Set<string>(),cell=108;
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
    occupied.add(key);point={x:gx*cell+(random()-.5)*16,y:gy*cell+(random()-.5)*16};
   }
  }
  const size=({5:90,4:74,3:62,2:50,1:42}[strength]||62);
  nodes.push({data:{id:'ref:'+item.id,entity:item.id,type:'reference',label:item.title,image:'none',preview:item.thumbnail||'',color:item.techniques.length?colorFor(item.techniques[0]):'#8f8a82',size,width:size,height:size*9/16,external:item.origin==='externa'},position:point});
  for(const tid of item.techniques){
   const target=positions.get(tid);if(!target)continue;
   // The same inward quadratic control point as the prototype, represented
   // in Cytoscape's source/target coordinate system.
   const dx=target.x-point.x,dy=target.y-point.y,length=Math.hypot(dx,dy)||1;
   const cx=(point.x+target.x)*.36,cy=(point.y+target.y)*.36;
   const weight=((cx-point.x)*dx+(cy-point.y)*dy)/(length*length);
   const distance=((cx-point.x)*-dy+(cy-point.y)*dx)/length;
   edges.push({data:{id:'e:'+item.id+':'+tid,source:'ref:'+item.id,target:'tech:'+tid,color:colorFor(tid),weight,distance}});
  }
 }
 return [...nodes,...edges];
}
