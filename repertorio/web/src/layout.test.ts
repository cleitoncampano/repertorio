import {describe,it,expect} from 'vitest';
import {layoutGraph} from './layout';
import type {GraphData,Reference} from './types';
describe('mapa',()=>{
 const graph:GraphData={vocabulary:{operacoes:{itens:[{id:'diferenciacao',def:'',nome:'Diferenciação'}]},tecnicas:{itens:[{id:'contraste',def:'',operacao:'diferenciacao'}]}},items:Array.from({length:100},(_,i)=>({id:'ref'+i,title:'Referência '+i,techniques:['contraste'],strength:4} as Reference))};
 it('mantém posições estáveis e não sobrepõe as referências',()=>{
  const first=layoutGraph(graph),second=layoutGraph(graph);
  expect(first).toEqual(second);
  const refs=first.filter(e=>e.data.type==='reference');
  expect(new Set(refs.map(e=>JSON.stringify(e.position))).size).toBe(100);
 });
 it('todas as conexões apontam para nós existentes',()=>{
  const elements=layoutGraph(graph);const ids=new Set(elements.filter(e=>e.position).map(e=>e.data.id));
  for(const e of elements.filter(e=>e.data.source)){expect(ids.has(e.data.source)).toBe(true);expect(ids.has(e.data.target)).toBe(true);}
 });
});
