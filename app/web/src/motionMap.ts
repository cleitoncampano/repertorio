import type {GraphData,Term,Vocabulary} from './types';
import {terms} from './types';

// Três organizações do mesmo mapa, cada uma responde uma pergunta de quem está criando:
// História: em que momento da apresentação a peça entra (seis momentos, com os papéis em volta).
// Recurso visual: o que faz a peça prender o olho (sete famílias, com as técnicas em volta).
// Formato: onde a peça vai passar (formatos de tela, com o papel na história ou o tipo de vídeo em volta).
export type Organization='historia'|'recurso'|'formato';
export const ORGANIZATIONS:{id:Organization;nome:string}[]=[{id:'historia',nome:'História'},{id:'recurso',nome:'Recurso visual'},{id:'formato',nome:'Formato'}];
// Os papéis seguem a ordem de uma apresentação; o mapa os percorre no sentido do relógio.
export const STORY_PHASES:(Term&{papeis:string[]})[]=[
 {id:'abrir',nome:'Abrir',def:'Capa, contexto e quem fala: o começo que promete o que vem.',papeis:['ABRIR','SITUAR','APRESENTAR']},
 {id:'conduzir',nome:'Conduzir',def:'Agenda, capítulos e passos: o que leva a plateia de uma parte à outra.',papeis:['DIVIDIR','SEQUENCIAR']},
 {id:'explicar',nome:'Explicar',def:'Conceitos, grupos e comparações: onde a ideia fica clara.',papeis:['EXPLICAR','AGRUPAR','COMPARAR']},
 {id:'provar',nome:'Provar',def:'Dados, produto e lugares: o que mostra que é verdade.',papeis:['PROVAR','MOSTRAR','LOCALIZAR']},
 {id:'marcar',nome:'Marcar',def:'Virada, destaque e citação: o momento que fica na memória.',papeis:['IMPACTAR','DESTACAR','CITAR']},
 {id:'fechar',nome:'Fechar',def:'Conclusão, chamada para ação e contato.',papeis:['FECHAR']},
];
// As 48 técnicas do vocabulário em famílias com nomes de ofício; cada técnica fica numa família só.
export const VISUAL_FAMILIES:(Term&{tecnicas:string[]})[]=[
 {id:'cor',nome:'Cor e contraste',def:'Uma diferença de cor, tamanho ou luz faz uma coisa saltar do resto.',tecnicas:['contraste-de-cor','contraste-de-escala','isolamento','foco-seletivo','intruso','cor-por-capitulo','inversao-figura-fundo']},
 {id:'tipografia',nome:'Tipografia',def:'A letra é a imagem: tamanho, peso, recorte e repetição da palavra.',tecnicas:['destaque-tipografico','tipografia-como-imagem','palavra-fantasma','eco-tipografico','hierarquia-de-leitura']},
 {id:'imagem',nome:'Imagem e foto',def:'Foto e recorte fazem o trabalho: sangria, camadas, máscara, rosto e olhar.',tecnicas:['sangria-total','corte-radical','textura-e-materia','mascara-de-forma','profundidade-em-camadas','dupla-exposicao','rosto-que-encara','olhar-que-guia','quebra-de-moldura']},
 {id:'composicao',nome:'Composição e grade',def:'Como os elementos se agrupam e se alinham: grade, cartões, eixo e numeração.',tecnicas:['proximidade','similaridade','regiao-comum','conexao','grade-modular','sanfona','simetria-e-eixo','fechamento','numeracao']},
 {id:'percurso',nome:'Percurso e revelação',def:'O caminho do olho e do tempo: linha que guia, revelação aos poucos, câmera contínua.',tecnicas:['linha-guia','direcao-de-leitura','revelacao-progressiva','camera-continua','sumario-navegavel','progressao-de-escala','padrao-e-quebra']},
 {id:'ideia',nome:'Ideia e surpresa',def:'A sacada: metáfora, ilusão, escala impossível, pergunta que fica no ar.',tecnicas:['metafora-visual','trompe-loeil','transformacao','escala-impossivel','escala-inversa','pergunta-aberta','referencia-cultural','objeto-como-suporte']},
 {id:'informacao',nome:'Dados e interface',def:'Número como protagonista e telas de produto ou de códigos conhecidos.',tecnicas:['dado-como-heroi','interface-imitada','emprestimo-de-codigo']},
];
// Técnica fora da lista segue o eixo antigo para a família mais próxima.
const FAMILY_BY_OPERATION:Record<string,string>={diferenciacao:'cor',agrupamento:'composicao',sequencia:'percurso',previsao:'ideia'};
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
export const STORY_LABELS:Labels={operation:'MOMENTO DA HISTÓRIA',technique:'PAPEL NA HISTÓRIA',techniques:n=>`${n} papéis neste momento`,references:'Peças com este papel',count:'referências no mapa',legend:'Momentos da história',operationPanel:'Detalhes do momento',techniquePanel:'Detalhes do papel'};
export const CRAFT_LABELS:Labels={operation:'RECURSO VISUAL',technique:'TÉCNICA VISUAL',techniques:n=>`${n} técnicas nesta família`,references:'Referências que usam esta técnica',count:'referências no mapa',legend:'Recursos visuais',operationPanel:'Detalhes do recurso',techniquePanel:'Detalhes da técnica'};
// Nomes do painel do mapa e da legenda na organização por formato.
export const MOTION_LABELS:Labels={operation:'FORMATO DE TELA',technique:'TIPO DE VÍDEO',techniques:n=>`${n} tipos de vídeo neste formato`,references:'Vídeos deste tipo',count:'vídeos no mapa',legend:'Formatos de tela',operationPanel:'Detalhes do formato de tela',techniquePanel:'Detalhes do tipo de vídeo'};
export const FORMAT_LABELS:Labels={operation:'FORMATO DE TELA',technique:'PAPEL NA HISTÓRIA',techniques:n=>`${n} papéis na história neste formato`,references:'Peças com este papel',count:'referências no mapa',legend:'Formatos de tela',operationPanel:'Detalhes do formato de tela',techniquePanel:'Detalhes do papel na história'};

export const isMotionSpace=(graph:GraphData)=>graph.items.length>0&&graph.items.every(item=>item.motion);
export const formatLabels=(graph:GraphData)=>isMotionSpace(graph)?MOTION_LABELS:FORMAT_LABELS;
// Vídeo abre organizado por formato; imagem, pela história. A escolha fica salva por espaço.
export const defaultOrganization=(graph:GraphData):Organization=>isMotionSpace(graph)?'formato':'historia';
// Escolhas guardadas antes da mudança: os eixos do olhar viraram o recurso visual.
export const savedOrganization=(value:unknown):Organization|undefined=>value==='eixos'?'recurso':value==='historia'||value==='recurso'||value==='formato'?value:undefined;
export const organizationLabels=(graph:GraphData,organization:Organization)=>organization==='historia'?STORY_LABELS:organization==='recurso'?CRAFT_LABELS:formatLabels(graph);
export function organizeMap(graph:GraphData,organization:Organization):GraphData{
 return organization==='historia'?storyMap(graph):organization==='recurso'?craftMap(graph):formatMap(graph);
}

// Papéis da ficha (até três) ligados aos momentos; peças sem papel ficam num grupo próprio.
export function storyMap(graph:GraphData):GraphData{
 const intentions=new Map(terms(graph.vocabulary,'intencoes').map(t=>[t.id,t]));
 const phaseOf=new Map(STORY_PHASES.flatMap(phase=>phase.papeis.map(role=>[role,phase.id] as const)));
 const used=new Set<string>();
 const items=graph.items.map(item=>{
  const roles=(item.intentions||[]).filter(role=>phaseOf.has(role)).slice(0,3);
  const ids=roles.length?roles.map(role=>'papel:'+role):['papel:outros'];
  ids.forEach(id=>used.add(id));
  return {...item,techniques:ids};
 });
 const phases=STORY_PHASES.filter(phase=>phase.papeis.some(role=>used.has('papel:'+role)));
 const tecnicas=phases.flatMap(phase=>phase.papeis.filter(role=>used.has('papel:'+role)).map(role=>({id:'papel:'+role,nome:intentions.get(role)?.nome||role,def:intentions.get(role)?.def||'',operacao:phase.id})));
 const operacoes:Term[]=[...phases];
 if(used.has('papel:outros')){operacoes.push({id:'outros',nome:'Sem papel',def:'Peças ainda sem papel na história.'});tecnicas.push({id:'papel:outros',nome:'Sem papel',def:'Peças ainda sem papel na história.',operacao:'outros'});}
 return {items,vocabulary:{...graph.vocabulary,operacoes:{itens:operacoes},pistas:{itens:[]},tecnicas:{itens:tecnicas}}};
}

// As mesmas técnicas e conexões, agrupadas nas famílias de recurso visual.
export function craftMap(graph:GraphData):GraphData{
 const familyOf=new Map(VISUAL_FAMILIES.flatMap(family=>family.tecnicas.map(id=>[id,family.id] as const)));
 const tecnicas=terms(graph.vocabulary,'tecnicas').map(t=>({...t,operacao:familyOf.get(t.id)||FAMILY_BY_OPERATION[t.operacao||'']||'ideia',pista:undefined}));
 const used=new Set(tecnicas.map(t=>t.operacao));
 return {items:graph.items,vocabulary:{...graph.vocabulary,operacoes:{itens:VISUAL_FAMILIES.filter(f=>used.has(f.id))},pistas:{itens:[]},tecnicas:{itens:tecnicas}}};
}

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
