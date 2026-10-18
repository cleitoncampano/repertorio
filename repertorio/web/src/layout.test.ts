import {describe,it,expect} from 'vitest';
import {layoutGraph} from './layout';
import type {GraphData,Reference} from './types';
import {graphViews} from './graphViewOptions';
describe('mapa',()=>{
 const graph:GraphData={vocabulary:{operacoes:{itens:[{id:'diferenciacao',def:'',nome:'Diferenciação'}]},tecnicas:{itens:[{id:'contraste',def:'',operacao:'diferenciacao'}]}},items:Array.from({length:100},(_,i)=>({id:'ref'+i,title:'Referência '+i,techniques:['contraste'],strength:4} as Reference))};
 it.each(graphViews)('$name mantém posições estáveis e não sobrepõe as referências',({id})=>{
  const first=layoutGraph(graph,id),second=layoutGraph(graph,id);
  expect(first).toEqual(second);
  const refs=first.filter(e=>e.data.type==='reference');
  expect(new Set(refs.map(e=>JSON.stringify(e.position))).size).toBe(100);
  for(let i=0;i<refs.length;i++)for(let j=i+1;j<refs.length;j++){
   const a=refs[i].position!,b=refs[j].position!;
   expect(Math.abs(a.x-b.x)>=90||Math.abs(a.y-b.y)>=90).toBe(true);
  }
 });
 it.each(graphViews)('$name mantém todas as conexões apontando para nós existentes',({id})=>{
  const elements=layoutGraph(graph,id);const ids=new Set(elements.filter(e=>e.position).map(e=>e.data.id));
  for(const e of elements.filter(e=>e.data.source)){expect(ids.has(e.data.source)).toBe(true);expect(ids.has(e.data.target)).toBe(true);}
 });
 const mixed:GraphData={vocabulary:{operacoes:{itens:[{id:'diferenciacao',def:''},{id:'agrupamento',def:''}]},pistas:{itens:[{id:'cor',def:''}]},tecnicas:{itens:[{id:'contraste',operacao:'diferenciacao',pista:'cor',def:''},{id:'semelhanca',operacao:'agrupamento',def:''},{id:'proximidade',operacao:'agrupamento',def:''}]}},items:[{id:'mista',techniques:['contraste','semelhanca','proximidade'],strength:5},{id:'sem-tecnica',techniques:[],strength:5},{id:'desconhecida',techniques:['nao-existe'],strength:5}] as Reference[]};
 it('agrupa pela operação com mais conexões, mantendo também as relações cruzadas e peças sem classificação',()=>{
  const original=layoutGraph(mixed),grouped=layoutGraph(mixed,'grouped');
  expect(grouped.map(element=>element.data.id).sort()).toEqual(original.map(element=>element.data.id).sort());
  const point=(id:string)=>grouped.find(element=>element.data.id===id)!.position!;
  const ref=point('ref:mista'),blue=point('op:agrupamento'),red=point('op:diferenciacao');
  expect(Math.hypot(ref.x-blue.x,ref.y-blue.y)).toBeLessThan(Math.hypot(ref.x-red.x,ref.y-red.y));
  for(const id of ['ref:sem-tecnica','ref:desconhecida'])expect(point(id)).not.toEqual(original.find(element=>element.data.id===id)!.position);
  expect(grouped.filter(element=>element.data.source==='ref:mista')).toHaveLength(3);
 });
 it('organiza as camadas da esquerda para a direita e trata espaços sem vocabulário',()=>{
  const elements=layoutGraph(mixed,'hierarchy');
  const x=(id:string)=>elements.find(element=>element.data.id===id)!.position!.x;
  expect(x('op:diferenciacao')).toBeLessThan(x('cue:diferenciacao:cor'));
  expect(x('cue:diferenciacao:cor')).toBeLessThan(x('tech:contraste'));
  expect(x('tech:contraste')).toBeLessThan(x('ref:mista'));
  for(const {id} of graphViews){
   expect(layoutGraph({items:[],vocabulary:{}},id)).toEqual([]);
   for(const element of layoutGraph({items:mixed.items,vocabulary:{}},id)){
    if(element.position){expect(Number.isFinite(element.position.x)).toBe(true);expect(Number.isFinite(element.position.y)).toBe(true);}
   }
  }
 });
 it('distribui uma biblioteca grande em uma área equilibrada na hierarquia',()=>{
  const ops=['diferenciacao','agrupamento','sequencia','previsao'];
  const graph:GraphData={vocabulary:{operacoes:{itens:ops.map(id=>({id,def:''}))},tecnicas:{itens:Array.from({length:48},(_,i)=>({id:'t'+i,def:'',operacao:ops[i%4]}))}},items:Array.from({length:1021},(_,i)=>({id:'r'+i,techniques:['t'+i%48],strength:5} as Reference))};
  const positions=layoutGraph(graph,'hierarchy').filter(element=>element.position).map(element=>element.position!);
  const width=Math.max(...positions.map(p=>p.x))-Math.min(...positions.map(p=>p.x));
  const height=Math.max(...positions.map(p=>p.y))-Math.min(...positions.map(p=>p.y));
  expect(width/height).toBeGreaterThan(.5);
  expect(width/height).toBeLessThan(3);
 });
});
