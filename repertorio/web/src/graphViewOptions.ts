export const graphViews=[
 {id:'free',name:'Mapa livre',description:'Explore as conexões no mapa original.'},
 {id:'grouped',name:'Por grupos',description:'Veja conjuntos separados por operação criativa.'},
 {id:'hierarchy',name:'Hierárquico',description:'Siga das operações às técnicas e referências.'},
] as const;
export type GraphView=typeof graphViews[number]['id'];
export function graphView(value:string|null):GraphView{
 return value==='grouped'||value==='hierarchy'?value:'free';
}

// Mantém a câmera original e separa as novas câmeras por espaço e visualização.
export function cameraKey(workspace:string,view:GraphView){
 return 'repertorio-camera-v3:'+workspace+(view==='free'?'':':'+view);
}
