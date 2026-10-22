import type {ElementDefinition} from 'cytoscape';
import type {GraphData,Term} from './types';
import type {ExperimentalView} from './graphSkins';

// scale afasta as capas quando o espaço tem vídeos, que aparecem com o dobro do tamanho.
type Context={graph:GraphData;nodes:Map<string,ElementDefinition>;ops:Term[];techniques:Term[];primary:Map<string,string>;place:(id:string,x:number,y:number)=>void;scale?:number};

export function arrangeAlternate({graph,nodes,ops,techniques,primary,place,scale:S=1}:Context,view:ExperimentalView){
 const refs=graph.items.slice().sort((a,b)=>a.id.localeCompare(b.id));
 const byTech=new Map(techniques.map(tech=>[tech.id,tech]));
 const operation=(id:string)=>byTech.get(primary.get(id)||'')?.operacao||'';
 const groups=ops.map(op=>({id:op.id,items:refs.filter(ref=>operation(ref.id)===op.id),tech:techniques.filter(tech=>tech.operacao===op.id)}));
 const unknown=refs.filter(ref=>!primary.has(ref.id));
 if(unknown.length)groups.push({id:'',items:unknown,tech:[]});
 const cues=(op:string)=>Array.from(nodes.values()).filter(node=>node.data.type==='cue'&&node.data.operation===op);
 const ordered=refs.slice().sort((a,b)=>groups.findIndex(group=>group.id===operation(a.id))-groups.findIndex(group=>group.id===operation(b.id))||(primary.get(a.id)||'').localeCompare(primary.get(b.id)||'')||a.id.localeCompare(b.id));

 if(view==='cosmos'){
  ops.forEach((op,i)=>{const a=-Math.PI/2+i*2*Math.PI/Math.max(1,ops.length);place('op:'+op.id,Math.cos(a)*260,Math.sin(a)*260);});
  groups.forEach((group,index)=>{
   const center=-Math.PI/2+index*2*Math.PI/Math.max(1,groups.length),span=2*Math.PI/Math.max(1,groups.length);
   cues(group.id).forEach((cue,i,list)=>{const a=center-span*.32+(i+.5)*span*.64/list.length;place(cue.data.id!,Math.cos(a)*520,Math.sin(a)*520);});
   group.tech.forEach((tech,i)=>{const a=center-span*.4+(i+.5)*span*.8/group.tech.length;place('tech:'+tech.id,Math.cos(a)*780,Math.sin(a)*780);const node=nodes.get('tech:'+tech.id)!;node.data.labelSide=Math.cos(a)<0?'left':'right';node.data.rotation=Math.cos(a)<0?a+Math.PI:a;});
  });
  let offset=0,ring=0;
  while(offset<ordered.length){
   const radius=1120+ring*164*S,capacity=Math.floor(2*Math.PI*radius/(156*S)),count=Math.min(capacity,ordered.length-offset);
   for(let i=0;i<count;i++){const a=-Math.PI/2+(i+.5*(ring%2))*2*Math.PI/count;place('ref:'+ordered[offset+i].id,Math.cos(a)*radius,Math.sin(a)*radius);}
   offset+=count;ring++;
  }
 }else if(view==='metro'){
  const columns=Math.max(5,Math.ceil(Math.sqrt(refs.length)*1.1));
  let top=0;
  groups.forEach(group=>{
   const rows=Math.ceil(group.items.length/columns),half=Math.ceil(rows/2),middle=top+half*144*S+250;
   place('op:'+group.id,-600,middle);
   cues(group.id).forEach((cue,i)=>place(cue.data.id!,100+i*220,middle));
   group.tech.forEach((tech,i)=>{place('tech:'+tech.id,900+i*230,middle);nodes.get('tech:'+tech.id)!.data.rotation=-Math.PI/4;});
   group.items.forEach((item,i)=>{const row=Math.floor(i/columns),side=row%2?-1:1,band=Math.floor(row/2);place('ref:'+item.id,900+i%columns*148*S,middle+side*(280*S+band*144*S));});
   top=middle+half*144*S+500;
  });
 }else if(view==='circuit'){
  const columns=Math.max(4,Math.ceil(Math.sqrt(refs.length*1.25))),rows=Math.max(1,Math.ceil(refs.length/columns));
  const step=144*S,width=(columns-1)*step,height=Math.max(1500,(rows-1)*step);
  ordered.forEach((item,i)=>place('ref:'+item.id,i%columns*step,Math.floor(i/columns)*step));
  ops.forEach((op,i)=>{
   const right=i%2===1,band=Math.floor(i/2),bands=Math.ceil(ops.length/2),middle=(band+.5)*height/bands;
   place('op:'+op.id,right?width+1100:-1100,middle);
   const ports=techniques.filter(tech=>tech.operacao===op.id);
   ports.forEach((tech,j)=>{place('tech:'+tech.id,right?width+220:-220,(band+(j+.5)/Math.max(1,ports.length))*height/bands);nodes.get('tech:'+tech.id)!.data.labelSide=right?'right':'left';});
   cues(op.id).forEach((cue,j,list)=>place(cue.data.id!,right?width+650:-650,(band+(j+.5)/list.length)*height/bands));
  });
 }else if(view==='garden'){
  const trees=groups.map(group=>{
   const step=144*S,radius=Math.max(330,Math.sqrt(group.items.length*step*step/(Math.PI*1.25*.85))+180),rx=radius*1.25,ry=radius*.85,points:{x:number;y:number}[]=[];
   for(let x=-Math.ceil(rx/step);x<=Math.ceil(rx/step);x++)for(let y=-Math.ceil(ry/step);y<=Math.ceil(ry/step);y++)if((x*step/rx)**2+(y*step/ry)**2<=1)points.push({x:x*step,y:y*step});
   points.sort((a,b)=>Math.hypot(a.x/rx,a.y/ry)-Math.hypot(b.x/rx,b.y/ry)||a.y-b.y||a.x-b.x);
   return {...group,rx,ry,points:points.slice(0,group.items.length).sort((a,b)=>a.y-b.y||a.x-b.x)};
  });
  const columns=Math.max(1,Math.ceil(Math.sqrt(trees.length))),widths:number[]=[],heights:number[]=[];
  trees.forEach((tree,i)=>{const col=i%columns,row=Math.floor(i/columns);widths[col]=Math.max(widths[col]||0,tree.rx*2+300);heights[row]=Math.max(heights[row]||0,tree.ry*2+1100);});
  trees.forEach((tree,i)=>{
   const x=widths.slice(0,i%columns).reduce((a,b)=>a+b,0)+widths[i%columns]/2,y=heights.slice(0,Math.floor(i/columns)).reduce((a,b)=>a+b,0)+tree.ry;
   place('op:'+tree.id,x,y+tree.ry+720);
   tree.tech.forEach((tech,j)=>{place('tech:'+tech.id,x+(j-(tree.tech.length-1)/2)*Math.min(150,tree.rx*2/Math.max(1,tree.tech.length)),y+tree.ry+200+Math.sin(j)*28);nodes.get('tech:'+tech.id)!.data.rotation=-Math.PI/3;});
   cues(tree.id).forEach((cue,j,list)=>place(cue.data.id!,x+(j-(list.length-1)/2)*200,y+tree.ry+470));
   tree.items.forEach((item,j)=>place('ref:'+item.id,x+tree.points[j].x,y+tree.points[j].y));
  });
 }else if(view==='editorial'){
  let left=0;
  groups.forEach(group=>{
   const columns=Math.max(3,Math.min(14,Math.ceil(Math.sqrt(group.items.length*1.1)))),width=Math.max(640,columns*148*S);
   place('op:'+group.id,left+width/2,0);
   cues(group.id).forEach((cue,j)=>place(cue.data.id!,left+160+j*210,260));
   group.tech.forEach((tech,j)=>place('tech:'+tech.id,left+130,420+j*68));
   const start=650+group.tech.length*68;
   group.items.forEach((item,j)=>place('ref:'+item.id,left+90*S+j%columns*148*S,start+Math.floor(j/columns)*144*S));
   left+=width+440;
  });
 }else if(view==='prism'){
  const columns=Math.max(3,Math.ceil(Math.sqrt(refs.length))),rows=Math.max(1,Math.ceil(refs.length/columns));
  ordered.forEach((item,i)=>{const col=i%columns,row=Math.floor(i/columns);place('ref:'+item.id,(col-row)*124*S,(col+row)*96*S);});
  const x=(columns-rows)*62*S,y=(columns+rows-2)*48*S,rx=(columns+rows)*62*S+380,ry=(columns+rows)*48*S+380;
  ops.forEach((op,i)=>{const a=-Math.PI/2+i*2*Math.PI/Math.max(1,ops.length);place('op:'+op.id,x+Math.cos(a)*rx*1.3,y+Math.sin(a)*ry*1.3);});
  groups.forEach((group,index)=>{
   const center=-Math.PI/2+index*2*Math.PI/Math.max(1,groups.length),span=2*Math.PI/Math.max(1,groups.length);
   group.tech.forEach((tech,i)=>{const a=center-span*.36+(i+.5)*span*.72/group.tech.length;place('tech:'+tech.id,x+Math.cos(a)*rx,y+Math.sin(a)*ry);const node=nodes.get('tech:'+tech.id)!;node.data.labelSide=Math.cos(a)<0?'left':'right';node.data.rotation=Math.cos(a)<0?a+Math.PI:a;});
   cues(group.id).forEach((cue,i,list)=>{const a=center-span*.28+(i+.5)*span*.56/list.length;place(cue.data.id!,x+Math.cos(a)*rx*1.15,y+Math.sin(a)*ry*1.15);});
  });
 }
}
