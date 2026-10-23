import {describe,expect,it} from 'vitest';
import {defaultOrganization,formatLabels,formatMap,isMotionSpace,motionMap} from './motionMap';
import {layoutGraph} from './layout';
import {graphViews} from './graphViewOptions';
import type {GraphData,Reference} from './types';

const video=(id:string,aspect:string,genres:string[])=>({id,title:id,techniques:['contraste'],strength:4,motion:{loop:'/l/'+id,video:'/v/'+id,aspect,genres}} as unknown as Reference);
const vocabulary={operacoes:{itens:[{id:'diferenciacao',def:'',nome:'Diferenciação'}]},tecnicas:{itens:[{id:'contraste',def:'',operacao:'diferenciacao'}]}};
const graph:GraphData={vocabulary,items:[video('a','horizontal',['lancamento']),video('b','vertical',['tipografia','lancamento']),video('c','quadrado',['explicativo']),
 {id:'t',title:'modelo',techniques:[],strength:5,motion:{aspect:'modelo',genres:['modelo']}} as unknown as Reference]};

describe('mapa dos espaços de vídeo',()=>{
 it('troca os eixos do olhar por formato de tela e tipo de vídeo',()=>{
  const map=motionMap(graph);
  expect((map.vocabulary.operacoes.itens as {id:string}[]).map(o=>o.id)).toEqual(['horizontal','vertical','quadrado','modelo']);
  expect((map.vocabulary.tecnicas.itens as {id:string;operacao:string}[]).map(t=>t.id)).toEqual(['horizontal:lancamento','vertical:lancamento','vertical:tipografia','quadrado:explicativo','modelo:modelo']);
  expect(map.items.find(i=>i.id==='b')!.techniques).toEqual(['vertical:tipografia','vertical:lancamento']);
  // A ficha original continua com as técnicas criativas.
  expect(graph.items[1].techniques).toEqual(['contraste']);
 });
 it('só vale quando o espaço é todo de vídeo',()=>{
  expect(isMotionSpace(graph)).toBe(true);
  expect(isMotionSpace({...graph,items:[...graph.items,{id:'img',title:'img',techniques:['contraste'],strength:3} as Reference]})).toBe(false);
 });
 it.each(graphViews)('$name organiza os vídeos por formato e tipo, com conexões válidas',({id})=>{
  const elements=layoutGraph(motionMap(graph),id),ids=new Set(elements.filter(e=>e.position).map(e=>e.data.id));
  expect(['op:horizontal','op:vertical','op:quadrado','op:modelo','tech:vertical:tipografia'].every(n=>ids.has(n))).toBe(true);
  for(const e of elements.filter(e=>e.data.source)){expect(ids.has(e.data.source)).toBe(true);expect(ids.has(e.data.target)).toBe(true);}
 });
 it('imagens se organizam por formato e papel na história; o espaço de imagem começa pelos eixos',()=>{
  const images:GraphData={vocabulary:{...vocabulary,intencoes:{itens:[{id:'ABRIR',nome:'Abrir',def:'Capa'},{id:'PROVAR',nome:'Provar',def:'Dados'}]}},
   items:[{id:'capa',title:'Capa',techniques:['contraste'],intentions:['ABRIR','PROVAR'],strength:4,aspect:'quadrado'} as Reference,{id:'slide',title:'Slide',techniques:['contraste'],intentions:[],strength:3} as Reference]};
  const map=formatMap(images);
  expect(map.items.find(i=>i.id==='capa')!.techniques).toEqual(['quadrado:ABRIR','quadrado:PROVAR']);
  expect(map.items.find(i=>i.id==='slide')!.techniques).toEqual(['horizontal:outros']);
  expect((map.vocabulary.tecnicas.itens as {id:string;nome:string}[]).find(t=>t.id==='quadrado:ABRIR')!.nome).toBe('Abrir');
  expect(defaultOrganization(images)).toBe('eixos');expect(defaultOrganization(graph)).toBe('formato');
  expect(formatLabels(images).technique).toBe('PAPEL NA HISTÓRIA');expect(formatLabels(graph).technique).toBe('TIPO DE VÍDEO');
 });
});
