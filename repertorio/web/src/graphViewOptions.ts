export const graphViews=[
 {id:'free',name:'Mapa livre',description:'Explore as conexões no mapa original.'},
 {id:'grouped',name:'Por grupos',description:'Veja conjuntos separados por operação criativa.'},
 {id:'hierarchy',name:'Hierárquico',description:'Siga das operações às técnicas e referências.'},
 {id:'cosmos',name:'Cosmos',description:'Constelações, órbitas e luz em azul e violeta.'},
 {id:'metro',name:'Metrô',description:'Rotas coloridas, estações e encontros de ideias.'},
 {id:'circuit',name:'Circuito',description:'Chips e trilhas verdes em uma placa digital.'},
 {id:'garden',name:'Jardim',description:'Ramos, folhas e ideias em tons naturais.'},
 {id:'editorial',name:'Editorial',description:'Um mural de papel, tipografia e tinta vermelha.'},
 {id:'prism',name:'Prisma',description:'Losangos e cores vibrantes em um mosaico isométrico.'},
] as const;
export type GraphView=typeof graphViews[number]['id'];
export function graphView(value:string|null):GraphView{
 return graphViews.find(view=>view.id===value)?.id||'free';
}

export function graphViewOrder(value:unknown):GraphView[]{
 const ids=graphViews.map(view=>view.id);
 const saved=Array.isArray(value)?value.filter((id):id is GraphView=>ids.includes(id)):[];
 return [...new Set([...saved,...ids])];
}

// Mantém a câmera original e separa as novas câmeras por espaço e visualização.
export function cameraKey(workspace:string,view:GraphView){
 return 'repertorio-camera-v3:'+workspace+(view==='free'?'':':'+view);
}
