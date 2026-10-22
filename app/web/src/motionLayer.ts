// Vídeos de motion tocando sobre o mapa. O Cytoscape desenha só imagens paradas; por cima dele fica uma
// camada de <video> alinhada às capas visíveis. Poucos tocam por vez para o mapa continuar leve.
export type MotionBox={id:string;src:string;poster?:string;x:number;y:number;w:number;h:number;clip?:string};

// Até 12 vídeos ao mesmo tempo, só nas capas que já aparecem com pelo menos 72 px no lado maior.
export const MOTION_LIMIT=12,MOTION_MIN=72;

// Os mais próximos do centro da tela ganham a vez; o desempate pelo id evita trocas a cada quadro.
export function pickMotion(boxes:MotionBox[],width:number,height:number,limit=MOTION_LIMIT,min=MOTION_MIN):MotionBox[]{
 const cx=width/2,cy=height/2;
 return boxes.filter(b=>Math.max(b.w,b.h)>=min&&b.x+b.w/2>0&&b.x-b.w/2<width&&b.y+b.h/2>0&&b.y-b.h/2<height)
  .sort((a,b)=>Math.hypot(a.x-cx,a.y-cy)-Math.hypot(b.x-cx,b.y-cy)||a.id.localeCompare(b.id))
  .slice(0,limit);
}

// Recorte do vídeo no mesmo formato da capa em cada visualização do grafo.
export function motionClip(shape:string|undefined,w:number,h:number){
 if(shape==='ellipse')return 'ellipse(50% 50%)';
 if(shape==='diamond')return 'polygon(50% 0,100% 50%,50% 100%,0 50%)';
 if(shape==='roundrectangle')return `inset(0 round ${Math.round(Math.min(w,h)*.12)}px)`;
 return '';
}

export class MotionLayer{
 private videos=new Map<string,HTMLVideoElement>();
 constructor(private root:HTMLElement){}

 sync(boxes:MotionBox[]){
  const keep=new Set(boxes.map(b=>b.id));
  for(const [id,video] of this.videos)if(!keep.has(id))this.drop(id,video);
  for(const b of boxes){
   let video=this.videos.get(b.id);
   if(!video){
    video=document.createElement('video');
    Object.assign(video,{muted:true,loop:true,playsInline:true,autoplay:true,preload:'auto'});
    video.setAttribute('aria-hidden','true');video.tabIndex=-1;video.dataset.ref=b.id;
    if(b.poster)video.poster=b.poster;
    // Aparece só quando já está tocando, sem piscar sobre a capa.
    video.addEventListener('playing',()=>video!.classList.add('playing'),{once:true});
    video.src=b.src;this.root.appendChild(video);this.videos.set(b.id,video);
    video.play().catch(()=>{/* Sem reprodução automática, fica a capa do mapa. */});
   }
   video.style.transform=`translate(${b.x-b.w/2}px,${b.y-b.h/2}px)`;
   video.style.width=b.w+'px';video.style.height=b.h+'px';video.style.clipPath=b.clip||'';
  }
 }

 clear(){for(const [id,video] of this.videos)this.drop(id,video);}

 private drop(id:string,video:HTMLVideoElement){
  // Soltar o arquivo libera o decodificador; só pausar mantém a memória ocupada.
  video.pause();video.removeAttribute('src');video.load();video.remove();this.videos.delete(id);
 }
}
