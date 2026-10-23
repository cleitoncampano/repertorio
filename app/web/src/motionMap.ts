import type {GraphData,Term} from './types';

// Espaços de vídeo se organizam pelo que importa para quem vai criar: onde o vídeo vai passar
// (formato de tela) e que tipo de vídeo ele é. Os eixos do olhar continuam nos espaços de imagem.
export const MOTION_FORMATS:Term[]=[
 {id:'horizontal',nome:'Horizontal 16:9',def:'YouTube, sites, apresentações e telas largas. É onde está a maior parte da galeria: lançamentos, explicativos e showreels.'},
 {id:'vertical',nome:'Vertical 9:16',def:'Reels, TikTok, Shorts e Stories, para ver com o celular em pé. Texto grande, ação no centro e começo forte.'},
 {id:'quadrado',nome:'Quadrado e 4:5',def:'Feed do Instagram e do LinkedIn: ocupa bem a tela do celular sem virar vertical.'},
 {id:'modelo',nome:'Prompts-modelo',def:'Prompts reescritos pelo Prompt Motion para servir de ponto de partida. Não têm vídeo próprio.'},
];
export const MOTION_TYPES:Record<string,{nome:string;def:string}>={
 lancamento:{nome:'Lançamento de produto',def:'Apresenta um app, site, SaaS ou produto: o problema, as telas reais e a chamada final.'},
 showreel:{nome:'Showreel de motion',def:'Mostra o domínio de técnicas de motion em sequência, como um portfólio em movimento.'},
 explicativo:{nome:'Explicativo',def:'Ensina um conceito ou processo passo a passo, com diagramas, quadro branco ou analogias.'},
 dados:{nome:'Dados e números',def:'Conta a história com números, contadores e gráficos que se constroem na tela.'},
 tipografia:{nome:'Tipografia e mensagem',def:'A palavra é a protagonista: frases, manifestos, letras de música e tipografia cinética.'},
 historia:{nome:'Histórias e personagens',def:'Curtas com personagens, cenas e começo, meio e fim.'},
 abstrato:{nome:'Arte abstrata e 3D',def:'Formas, partículas, 3D e arte generativa, em geral no ritmo da música.'},
 vinheta:{nome:'Marca e vinheta',def:'Aberturas, revelações de logo e peças curtas de identidade de marca.'},
 modelo:{nome:'Prompt-modelo',def:'Prompt completo para copiar e adaptar ao seu tema.'},
};
// Nomes do painel do mapa quando o espaço é de vídeo.
export const MOTION_LABELS={operation:'FORMATO DE TELA',technique:'TIPO DE VÍDEO',techniques:(n:number)=>`${n} tipos de vídeo neste formato`,references:'Vídeos deste tipo',count:'vídeos no mapa',legend:'Formatos de tela',operationPanel:'Detalhes do formato de tela',techniquePanel:'Detalhes do tipo de vídeo'};

export const isMotionSpace=(graph:GraphData)=>graph.items.length>0&&graph.items.every(item=>item.motion);

// Mesmo grafo, com formatos no lugar dos eixos e "formato:tipo" no lugar das técnicas.
// Cada vídeo liga ao tipo dentro do seu formato, então as nove visualizações funcionam sem mudança.
export function motionMap(graph:GraphData):GraphData{
 const formatOf=(item:GraphData['items'][number])=>item.motion?.aspect||'horizontal';
 const used=new Map<string,Set<string>>();
 const items=graph.items.map(item=>{
  const format=formatOf(item),types=item.motion?.genres?.length?item.motion.genres:['lancamento'];
  types.forEach(type=>used.set(format,(used.get(format)||new Set()).add(type)));
  return {...item,techniques:types.map(type=>format+':'+type)};
 });
 const order=Object.keys(MOTION_TYPES);
 const tecnicas=MOTION_FORMATS.filter(f=>used.has(f.id)).flatMap(f=>[...used.get(f.id)!].sort((a,b)=>order.indexOf(a)-order.indexOf(b))
  .map(type=>({id:f.id+':'+type,nome:MOTION_TYPES[type]?.nome||type,def:MOTION_TYPES[type]?.def||'',operacao:f.id})));
 return {items,vocabulary:{...graph.vocabulary,operacoes:{itens:MOTION_FORMATS.filter(f=>used.has(f.id))},pistas:{itens:[]},tecnicas:{itens:tecnicas}}};
}
