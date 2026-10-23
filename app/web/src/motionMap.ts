import type {GraphData,Term,Vocabulary} from './types';
import {terms} from './types';

// Duas organizações do mesmo mapa: pelos eixos do olhar (técnicas visuais, feitas para slides) ou pelo formato de tela.
// No formato, o centro mostra onde a peça vai passar; em volta, o papel na história (imagens) ou o tipo de vídeo.
export type Organization='eixos'|'formato';
export const MOTION_FORMATS:Term[]=[
 {id:'horizontal',nome:'Horizontal 16:9',def:'Slides, YouTube, sites e apresentações: telas largas. É onde está a maior parte do acervo.'},
 {id:'vertical',nome:'Vertical 9:16',def:'Stories, Reels, TikTok e Shorts, para ver com o celular em pé. Texto grande, ação no centro e começo forte.'},
 {id:'quadrado',nome:'Quadrado e 4:5',def:'Feed e carrossel do Instagram e do LinkedIn: ocupa bem a tela do celular sem virar vertical.'},
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
type Labels={operation:string;technique:string;techniques:(n:number)=>string;references:string;count:string;legend:string;operationPanel:string;techniquePanel:string};
// Nomes do painel do mapa e da legenda na organização por formato.
export const MOTION_LABELS:Labels={operation:'FORMATO DE TELA',technique:'TIPO DE VÍDEO',techniques:n=>`${n} tipos de vídeo neste formato`,references:'Vídeos deste tipo',count:'vídeos no mapa',legend:'Formatos de tela',operationPanel:'Detalhes do formato de tela',techniquePanel:'Detalhes do tipo de vídeo'};
export const FORMAT_LABELS:Labels={operation:'FORMATO DE TELA',technique:'PAPEL NA HISTÓRIA',techniques:n=>`${n} papéis na história neste formato`,references:'Peças com este papel',count:'referências no mapa',legend:'Formatos de tela',operationPanel:'Detalhes do formato de tela',techniquePanel:'Detalhes do papel na história'};

export const isMotionSpace=(graph:GraphData)=>graph.items.length>0&&graph.items.every(item=>item.motion);
export const formatLabels=(graph:GraphData)=>isMotionSpace(graph)?MOTION_LABELS:FORMAT_LABELS;
// Vídeo abre organizado por formato; imagem, pelos eixos do olhar. A escolha fica salva por espaço.
export const defaultOrganization=(graph:GraphData):Organization=>isMotionSpace(graph)?'formato':'eixos';

// Mesmo grafo, com formatos no lugar dos eixos e "formato:tipo" (ou "formato:papel") no lugar das técnicas.
// As nove visualizações desenham o resultado sem mudança.
export function formatMap(graph:GraphData):GraphData{
 const intentions=new Map(terms(graph.vocabulary,'intencoes').map(t=>[t.id,t]));
 const used=new Map<string,Set<string>>();
 const items=graph.items.map(item=>{
  const format=item.motion?.aspect||item.aspect||'horizontal';
  const groups=item.motion?(item.motion.genres?.length?item.motion.genres:['outros']):(item.intentions?.length?item.intentions.slice(0,2):['outros']);
  groups.forEach(group=>used.set(format,(used.get(format)||new Set()).add(group)));
  return {...item,techniques:groups.map(group=>format+':'+group)};
 });
 const order=[...Object.keys(MOTION_TYPES),...intentions.keys(),'outros'];
 const name=(group:string)=>MOTION_TYPES[group]?.nome||intentions.get(group)?.nome||(group==='outros'?'Sem classificação':group);
 const def=(group:string)=>MOTION_TYPES[group]?.def||intentions.get(group)?.def||'';
 const tecnicas=MOTION_FORMATS.filter(f=>used.has(f.id)).flatMap(f=>[...used.get(f.id)!].sort((a,b)=>order.indexOf(a)-order.indexOf(b))
  .map(group=>({id:f.id+':'+group,nome:name(group),def:def(group),operacao:f.id})));
 const vocabulary:Vocabulary={...graph.vocabulary,operacoes:{itens:MOTION_FORMATS.filter(f=>used.has(f.id))},pistas:{itens:[]},tecnicas:{itens:tecnicas}};
 return {items,vocabulary};
}
export const motionMap=formatMap;
