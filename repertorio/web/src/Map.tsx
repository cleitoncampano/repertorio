import {useEffect,useRef,useState,type CSSProperties} from 'react';
import cytoscape,{type Core,type NodeSingular} from 'cytoscape';
import {Plus,Minus,Maximize,LocateFixed} from 'lucide-react';
import {kindName,type GraphData,type Reference} from './types';
import {layoutGraph} from './layout';
import {graphFocus} from './focus';
import {api,sized} from './api';
import {cameraKey,type GraphView} from './graphViewOptions';
import {graphColors,graphSkin,readableInk} from './graphSkins';

// Resoluções do mapa: cada miniatura usa a menor que cobre o tamanho real na tela e melhora ao aproximar.
const LEVELS=[128,256,512,1024];

type Props={workspaceId:string;view:GraphView;data:GraphData;selected:string|null;matches:string[]|null;technique:string;operation:string;theme:'dark'|'light';onSelect:(id:string)=>void;onTerm:(type:string,id:string)=>void;onClear:()=>void};
export function Map({workspaceId,view,data,selected,matches,technique,operation,theme,onSelect,onTerm,onClear}:Props){
 const container=useRef<HTMLDivElement>(null),cy=useRef<Core|null>(null);
 const viewRef=useRef(view);viewRef.current=view;
 const skin=graphSkin(view,theme),skinRef=useRef(skin);skinRef.current=skin;
 const paletteRef=useRef(graphColors(view,theme));paletteRef.current=graphColors(view,theme);
 const applyView=useRef<((next:GraphView)=>void)|null>(null);
 const focusRef=useRef({selected,matches,technique,operation});focusRef.current={selected,matches,technique,operation};
 const panelInset=useRef(0);
 const framedMatches=useRef('');
 const callbacks=useRef({onSelect,onTerm,onClear});callbacks.current={onSelect,onTerm,onClear};
 const [zoom,setZoom]=useState(1);
 const [hover,setHover]=useState<{item:Reference;x:number;y:number}|null>(null);
 // Cores do tema lidas na hora do estilo: trocar o tema reestiliza só os nós que mudam, nunca as milhares de linhas.
 const themeRef=useRef(theme);themeRef.current=theme;
 const ink=()=>skinRef.current?{text:skinRef.current.ink,background:skinRef.current.background,operation:skinRef.current.surface,reference:skinRef.current.surface}:themeRef.current==='light'?{text:'#282520',background:'#f7f5f0',operation:'#fffdfa',reference:'#e0dcd4'}:{text:'#ECE8E1',background:'#121212',operation:'#161616',reference:'#2a2a2a'};
 const paint=(node:NodeSingular)=>skinRef.current?(paletteRef.current[node.data('operation')]||skinRef.current.ink):node.data('color');
 useEffect(()=>{
  if(!container.current)return;
  const reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // Zoom usado nos estilos: linhas e nomes ficam com espessura constante na tela.
  const scale={z:1};
  const measurement=document.createElement('canvas').getContext('2d');
  if(measurement)measurement.font='11px sans-serif';
  let currentView=viewRef.current;
  const instance=cytoscape({container:container.current,elements:layoutGraph(data,currentView),layout:{name:'preset'},minZoom:.045,maxZoom:4,autoungrabify:true,boxSelectionEnabled:false,
   style:[
    {selector:'node',style:{'background-color':paint,'overlay-opacity':0,'border-width':0,'font-family':()=>skinRef.current?.font||'Avenir Next, sans-serif'}},
    {selector:'node[type="operation"]',style:{width:(node:NodeSingular)=>viewRef.current==='prism'?Math.max(skinRef.current!.operationWidth,(String(node.data('label')).length*8+36)/scale.z):skinRef.current?.operationWidth||(viewRef.current==='hierarchy'?700:250),height:()=>viewRef.current==='prism'?Math.max(skinRef.current!.operationHeight,30/scale.z):skinRef.current?.operationHeight||(viewRef.current==='hierarchy'?180:250),shape:()=>skinRef.current?.operationShape||(viewRef.current==='hierarchy'?'roundrectangle':'ellipse'),'background-color':(node:NodeSingular)=>viewRef.current==='prism'?paint(node):ink().operation,'border-color':paint,'border-width':()=>3/scale.z,'border-opacity':1,label:'data(label)',color:(node:NodeSingular)=>viewRef.current==='prism'?readableInk(paint(node)):ink().text,'font-weight':600,'font-size':()=>(skinRef.current||viewRef.current==='hierarchy'?12:Math.max(9,Math.min(16,125*scale.z*.3)))/scale.z,'text-valign':'center'}},
    {selector:'node[type="cue"]',style:{width:28,height:28,label:'data(label)','text-opacity':0,'text-valign':'center','border-color':paint,color:()=>ink().text,'font-size':()=>11/scale.z}},
    {selector:'node[type="technique"]',style:{width:18,height:18,shape:()=>skinRef.current?.techniqueShape||'ellipse','background-color':(node:NodeSingular)=>viewRef.current==='metro'?ink().operation:paint(node),'border-color':paint,'border-width':()=>viewRef.current==='metro'?2/scale.z:0,label:'data(label)',color:()=>ink().text,'font-size':()=>12/scale.z,'text-opacity':0,'text-valign':'center','text-halign':(node:NodeSingular)=>node.data('labelSide') as 'left'|'right','text-rotation':(node:NodeSingular)=>Number(node.data('rotation')),'text-margin-x':(node:NodeSingular)=>node.data('labelSide')==='left'?-16:16,'text-background-color':()=>ink().background,'text-background-opacity':.85,'text-background-padding':'3px'}},
    {selector:'node[type="reference"]',style:{width:(node:NodeSingular)=>skinRef.current?.referenceRatio?node.data('size'):node.data('width'),height:(node:NodeSingular)=>skinRef.current?.referenceRatio?node.data('size')/skinRef.current.referenceRatio:node.data('height'),shape:()=>skinRef.current?.referenceShape||'rectangle','background-color':()=>ink().reference,'background-image':'data(image)','background-fit':()=>skinRef.current?.referenceRatio?'cover':'contain','background-image-containment':'inside','border-color':(node:NodeSingular)=>skinRef.current?paint(node):ink().text,'border-width':()=>skinRef.current?5:0}},
    {selector:'node[?external]',style:{'border-width':3,'border-opacity':.55}},
    {selector:'edge',style:{width:()=>(skinRef.current?.edgeWidth||1.1)/scale.z,'line-color':edge=>skinRef.current?(paletteRef.current[edge.data('operation')]||ink().text):edge.data('color'),opacity:()=>skinRef.current?.edgeOpacity||.13,'curve-style':()=>skinRef.current?.curve||'unbundled-bezier','line-style':()=>skinRef.current?.line||'solid','taxi-direction':'auto','taxi-turn':'50%','control-point-distances':'data(distance)','control-point-weights':'data(weight)','edge-distances':'node-position'}},
    {selector:'edge[?structure]',style:{'line-color':edge=>skinRef.current?(paletteRef.current[edge.data('operation')]||ink().text):'#8f8a82',opacity:()=>skinRef.current?.curve==='taxi'?.55:.28,'curve-style':()=>skinRef.current?.curve||'straight'}},
    {selector:'edge[?cross]',style:{opacity:()=>viewRef.current==='hierarchy'||skinRef.current?.curve==='taxi'?.025:.04}},
    {selector:'node.dim',style:{opacity:.1}},
    {selector:'node[type="operation"].dim',style:{opacity:.25}},
    {selector:'edge.dim',style:{opacity:.018}},
    {selector:'node.lit',style:{opacity:1}},
    {selector:'edge.lit',style:{width:()=>1.8/scale.z,opacity:.85}},
    {selector:'edge[?structure].lit',style:{'line-color':edge=>skinRef.current?(paletteRef.current[edge.data('operation')]||ink().text):edge.data('color'),opacity:.65}},
    {selector:'node[type="technique"].lit',style:{width:26,height:26,'text-opacity':1,'font-weight':600}},
    {selector:'node[type="cue"].lit',style:{shape:'roundrectangle',width:(node:NodeSingular)=>((measurement?.measureText(node.data('label')).width||node.data('label').length*7)+12)/scale.z,height:()=>18/scale.z,padding:'0px','background-color':()=>ink().background,'border-width':()=>1/scale.z,'text-opacity':1}},
    {selector:'node.show-label',style:{'text-opacity':1}},
    {selector:'node.active',style:{'border-color':()=>ink().text,'border-width':12,'border-opacity':1}},
    {selector:'node[type="reference"].hovered',style:{'border-width':8,'border-color':()=>ink().text,'border-opacity':1}},
   ]});
  cy.current=instance;panelInset.current=0;framedMatches.current='';
  let cameraTimer=0;
  const saveCamera=()=>{clearTimeout(cameraTimer);try{sessionStorage.setItem(cameraKey(workspaceId,currentView),JSON.stringify({zoom:instance.zoom(),pan:{x:instance.pan().x+panelInset.current,y:instance.pan().y}}));}catch{/* A câmera continua utilizável sem armazenamento. */}};
  const restoreCamera=()=>{try{const saved=sessionStorage.getItem(cameraKey(workspaceId,currentView));if(saved){const camera=JSON.parse(saved);if(Number.isFinite(camera.zoom)&&camera.zoom>0&&Number.isFinite(camera.pan?.x)&&Number.isFinite(camera.pan?.y)){instance.viewport({zoom:Math.max(instance.minZoom(),Math.min(instance.maxZoom(),camera.zoom)),pan:{x:camera.pan.x-panelInset.current,y:camera.pan.y}});return true;}}}catch{/* Usa o enquadramento inicial. */}return false;};
  instance.fit(undefined,instance.width()<760?30:72);
  restoreCamera();
  setZoom(instance.zoom());
  let frame=0,lastZoom=0,settle=0;
  // Recalcular o estilo de tudo a cada passo de zoom travava o mapa. Agora só linhas e nomes são
  // recalculados, uma vez, quando o zoom para (e se mudou mais de 15%); durante o gesto eles acompanham a escala.
  const rescale=()=>{
   const z=instance.zoom();
   if(instance.destroyed()||Math.abs(Math.log(z/scale.z))<Math.log(1.15))return;
   scale.z=z;instance.batch(()=>instance.elements('edge, node[type!="reference"]').toggleClass('escala'));
  };
  rescale();
  const images=new globalThis.Map<string,HTMLImageElement>(),requested=new globalThis.Map<string,number>(),shown=new globalThis.Map<string,number>();
  const referenceNodes=instance.nodes('[type="reference"]'),techniqueNodes=instance.nodes('[type="technique"]');
  let bundled=false; // até o pacote inicial chegar, nenhuma miniatura é pedida sozinha
  const updateViewport=()=>{
   const z=instance.zoom(),extent=instance.extent(),density=window.devicePixelRatio||1;
   if(Math.abs(z-lastZoom)>.0001){
    lastZoom=z;
    const threshold=currentView==='hierarchy'?.24:skinRef.current&&!['cosmos','circuit'].includes(currentView)?.6:.34;
    techniqueNodes.toggleClass('show-label',z>threshold);
    clearTimeout(settle);settle=window.setTimeout(rescale,140);
   }
   if(!bundled)return;
   referenceNodes.forEach(node=>{
    const p=node.position(),src=node.data('preview'),id=node.id();
    if(!src||p.x<extent.x1-150||p.x>extent.x2+150||p.y<extent.y1-150||p.y>extent.y2+150)return;
    const level=LEVELS.find(l=>l>=node.data('size')*z*density)??LEVELS[LEVELS.length-1];
    if((requested.get(id)??0)>=level)return;
    requested.set(id,level);
    const url=sized(src,level)!,img=new Image();images.set(id,img);
    img.crossOrigin='anonymous'; // o mesmo modo do Cytoscape: a imagem baixa uma vez só e vem do cache
    img.onload=()=>{
     if(instance.destroyed()||(shown.get(id)??0)>level)return;
     shown.set(id,level);
     const ratio=img.naturalWidth/img.naturalHeight,size=node.data('size');
     node.data({image:url,width:ratio>=1?size:size*ratio,height:ratio>=1?size/ratio:size});
    };
    img.src=url;
   });
  };
  updateViewport();
  // As miniaturas de 128 px chegam todas num pedido só; resoluções maiores vêm uma a uma ao aproximar.
  api<Record<string,{src:string;width:number;height:number}>>('/previews?workspace_id='+encodeURIComponent(workspaceId)+'&w='+LEVELS[0]).then(previews=>{
   if(instance.destroyed())return;
   instance.batch(()=>referenceNodes.forEach(node=>{
    const preview=previews[node.data('preview')];if(!preview)return;
    requested.set(node.id(),LEVELS[0]);shown.set(node.id(),LEVELS[0]);
    const ratio=preview.width/preview.height,size=node.data('size');
    node.data({image:preview.src,width:ratio>=1?size:size*ratio,height:ratio>=1?size/ratio:size});
   }));
  }).catch(()=>{/* sem o pacote, cada miniatura é pedida sozinha */}).finally(()=>{bundled=true;if(!instance.destroyed())updateViewport();});
  instance.on('tap','node',e=>{setHover(null);const d=e.target.data();if(d.type==='reference')callbacks.current.onSelect(d.entity);else callbacks.current.onTerm(d.type==='cue'?'operation':d.type,d.entity);});
  instance.on('tap',e=>{if(e.target===instance)callbacks.current.onClear();});
  const items=new globalThis.Map(data.items.map(item=>[item.id,item]));
  instance.on('mouseover','node',e=>{
   e.target.addClass('hovered');if(container.current)container.current.style.cursor='pointer';
   const item=items.get(e.target.data('entity'));
   if(item&&window.matchMedia('(hover: hover)').matches){const p=e.target.renderedPosition();setHover({item,x:Math.max(12,Math.min(p.x+22,instance.width()-260)),y:Math.max(64,Math.min(p.y+18,instance.height()-270))});}
  });
  instance.on('mouseout','node',e=>{setHover(null);e.target.removeClass('hovered');if(container.current)container.current.style.cursor='grab';});
  instance.on('viewport',()=>{
   clearTimeout(cameraTimer);cameraTimer=window.setTimeout(saveCamera,160);
   if(frame)return;
   frame=requestAnimationFrame(()=>{frame=0;setHover(null);setZoom(instance.zoom());updateViewport();});
  });
  window.addEventListener('pagehide',saveCamera);
  const resize=new ResizeObserver(()=>instance.resize());resize.observe(container.current);
  applyView.current=next=>{
   if(currentView===next)return;
   saveCamera();currentView=next;lastZoom=0;setHover(null);framedMatches.current='';
   instance.batch(()=>{
    for(const element of layoutGraph(data,next)){
     const target=instance.getElementById(element.data.id!);
     if(element.position){target.position(element.position);target.data('operation',element.data.operation||'');if(element.data.type==='technique')target.data({rotation:element.data.rotation,labelSide:element.data.labelSide});}
     else target.data({distance:element.data.distance,weight:element.data.weight,cross:!!element.data.cross});
    }
   instance.elements().toggleClass('layout-changed');
   });
   const focused=focusRef.current.selected&&instance.getElementById('ref:'+focusRef.current.selected);
   if(focused&&focused.length){
    const point=focused.position(),level=Math.min(1.3,instance.maxZoom());
    instance.viewport({zoom:level,pan:{x:(instance.width()-panelInset.current*2)/2-point.x*level,y:instance.height()/2-point.y*level}});
   }else if(!restoreCamera()){
    instance.fit(undefined,instance.width()<760?30:72);instance.panBy({x:-panelInset.current,y:0});
   }
   rescale();updateViewport();
  };
  if(!reduced)container.current.animate([{opacity:.5},{opacity:1}],{duration:400});
  return()=>{saveCamera();window.removeEventListener('pagehide',saveCamera);applyView.current=null;cancelAnimationFrame(frame);clearTimeout(settle);resize.disconnect();for(const img of images.values())img.onload=null;instance.destroy();cy.current=null;};
 },[data,workspaceId]);
 useEffect(()=>{applyView.current?.(view);},[view,data,workspaceId]);
 const panelOpen=!!(selected||technique||operation||matches);
 useEffect(()=>{
  const c=cy.current;if(!c)return;
  const position=()=>{const next=panelOpen&&c.width()>760?(c.width()>1100?220:180):0;const shift=panelInset.current-next;panelInset.current=next;c.panBy({x:shift,y:0});};
  position();window.addEventListener('resize',position);return()=>window.removeEventListener('resize',position);
 },[panelOpen,data]);
 useEffect(()=>{
  const c=cy.current;if(!c)return;
  // A classe só serve para reestilizar quem tem cor de tema visível; as miniaturas cobrem o fundo das referências.
  (skinRef.current?c.elements():c.nodes('[type!="reference"], .active, .hovered')).toggleClass('light',theme==='light');
 },[theme,data]);
 useEffect(()=>{
  const instance=cy.current;if(!instance)return;
  const focus=graphFocus(data,{selected,technique,operation,matches});
  instance.batch(()=>{
   instance.elements().removeClass('dim lit active');
   if(!focus)return;
   instance.elements().addClass('dim');
   const show=(id:string)=>instance.getElementById(id).removeClass('dim').addClass('lit');
   focus.references.forEach(id=>show('ref:'+id));focus.techniques.forEach(id=>show('tech:'+id));focus.operations.forEach(id=>show('op:'+id));focus.cues.forEach(show);
   instance.edges().forEach(edge=>{if(edge.source().hasClass('lit')&&edge.target().hasClass('lit'))edge.removeClass('dim').addClass('lit');});
   if(selected)instance.getElementById('ref:'+selected).addClass('active');
  });
 },[selected,matches,technique,operation,data]);
 useEffect(()=>{
  const c=cy.current;
  if(!c||!skinRef.current||selected||!(operation||technique)||c.width()<=760)return;
  const nodes=c.nodes('.lit');if(!nodes.length)return;
  const bounds=nodes.boundingBox({includeLabels:true,includeOverlays:false}),width=c.width()-panelInset.current*2,height=c.height()-200;
  const level=Math.max(c.minZoom(),Math.min(.9,(width-192)/Math.max(1,bounds.w),height/Math.max(1,bounds.h)));
  c.viewport({zoom:level,pan:{x:width/2-(bounds.x1+bounds.x2)/2*level,y:112+height/2-(bounds.y1+bounds.y2)/2*level}});
 },[selected,matches,technique,operation,data,view]);
 useEffect(()=>{
  if(!matches){framedMatches.current='';return;}
  const c=cy.current;if(!c||selected||!matches.length)return;
  const key=view+JSON.stringify([...matches].sort());
  if(framedMatches.current===key)return;
  const ids=new Set(matches),nodes=c.nodes('[type="reference"]').filter(node=>ids.has(node.data('entity')));
  if(!nodes.length)return;
  // A busca enquadra as capas na área livre, sem deixá-las sob o painel de resultados.
  const bounds=nodes.boundingBox({includeLabels:false}),padding=c.width()<760?48:96;
  const width=c.width()-panelInset.current*2;
  const level=Math.max(c.minZoom(),Math.min(1.3,(width-padding*2)/bounds.w,(c.height()-padding*2)/bounds.h));
  c.viewport({zoom:level,pan:{x:width/2-(bounds.x1+bounds.x2)/2*level,y:c.height()/2-(bounds.y1+bounds.y2)/2*level}});
  framedMatches.current=key;
 },[matches,selected,data,view]);
 const adjust=(factor:number)=>{const c=cy.current;if(c)c.zoom({level:c.zoom()*factor,renderedPosition:{x:c.width()/2,y:c.height()/2}});};
 return <div className={'map-stage'+(skin?' graph-skin graph-skin-'+view:'')} data-view={view} style={skin?{'--graph-background':skin.background,'--graph-ink':skin.ink,'--graph-surface':skin.surface,'--graph-accent':skin.palette[0]} as CSSProperties:undefined}><div className="map-surface" ref={container} role="img" aria-label="Mapa de referências conectadas às técnicas. Use a busca ou a lista para navegar com teclado."/>
  {hover&&<div className="map-hover" style={{left:hover.x,top:hover.y}}>{hover.item.thumbnail&&<img src={sized(hover.item.thumbnail,512)} alt=""/>}<div><small>{kindName[hover.item.kind]||'Referência'} · Clique para explorar</small><strong>{hover.item.title}</strong></div></div>}
  <span className="map-help">Arraste para explorar · Role para aproximar</span>
  <div className="map-controls"><button title="Aproximar" aria-label="Aproximar" onClick={()=>adjust(1.25)}><Plus size={17}/></button><span>{Math.round(zoom*100)}%</span><button title="Afastar" aria-label="Afastar" onClick={()=>adjust(.8)}><Minus size={17}/></button><i/><button title="Ver todo o mapa" aria-label="Ver todo o mapa" onClick={()=>{const c=cy.current;if(c){c.fit(undefined,c.width()<760?30:72);c.panBy({x:-panelInset.current,y:0});}}}><Maximize size={16}/></button>{selected&&<button title="Localizar seleção" aria-label="Localizar seleção" onClick={()=>{const c=cy.current;if(c){c.fit(c.getElementById('ref:'+selected),200);c.zoom(Math.min(c.zoom(),1.3));}}}><LocateFixed size={17}/></button>}</div>
 </div>;
}
