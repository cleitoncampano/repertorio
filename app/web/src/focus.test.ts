import {describe,it,expect} from 'vitest';
import {graphFocus} from './focus';
import {layoutGraph} from './layout';
import {colors,type GraphData,type Reference} from './types';
const data:GraphData={vocabulary:{operacoes:{itens:[{id:'previsao',def:'',nome:'Previsão'},{id:'diferenciacao',def:'',nome:'Diferenciação'}]},pistas:{itens:[{id:'semantica',def:'',nome:'Semântica'}]},tecnicas:{itens:[{id:'metafora',def:'',operacao:'previsao',pista:'semantica'},{id:'contraste',def:'',operacao:'diferenciacao',pista:'semantica'}]}},items:Array.from({length:90},(_,i)=>({id:'r'+i,title:'Ref '+i,techniques:i<80?['metafora','contraste']:['contraste'],strength:1+i%5} as Reference))};
describe('seleção por conexões',()=>{
 it('acende o eixo inteiro, além dos 48 resultados de uma página',()=>{
  const focus=graphFocus(data,{selected:null,technique:'',operation:'previsao',matches:null})!;
  expect(focus.references.size).toBe(80);expect([...focus.techniques]).toEqual(['metafora']);
  expect([...focus.operations]).toEqual(['previsao']);expect([...focus.cues]).toEqual(['cue:previsao:semantica']);
 });
 it('uma peça acende suas técnicas e operações, sem acender outras peças',()=>{
  const focus=graphFocus(data,{selected:'r0',technique:'',operation:'',matches:null})!;
  expect([...focus.references]).toEqual(['r0']);expect(focus.techniques.size).toBe(2);expect(focus.operations.size).toBe(2);
 });
 it('combina busca com eixo sem incluir conexões não relacionadas',()=>{
  expect([...graphFocus(data,{selected:null,technique:'',operation:'previsao',matches:['r0','r89']})!.references]).toEqual(['r0']);
 });
 it('preserva a cor da técnica em cada linha da mesma referência',()=>{
  const graph=layoutGraph(data);
  expect(graph.find(e=>e.data.id==='e:r0:metafora')!.data.color).toBe(colors.previsao);
  expect(graph.find(e=>e.data.id==='e:r0:contraste')!.data.color).toBe(colors.diferenciacao);
 });
 it('distribui tamanhos por força e mantém espaço para proporções diferentes',()=>{
  const refs=layoutGraph(data).filter(e=>e.data.type==='reference');
  expect(new Set(refs.map(r=>r.data.size)).size).toBe(5);
  for(let i=0;i<refs.length;i++)for(let j=i+1;j<refs.length;j++){
   const a=refs[i],b=refs[j],distance=(a.data.size+b.data.size)/2;
   expect(Math.abs(a.position!.x-b.position!.x)>=distance||Math.abs(a.position!.y-b.position!.y)>=distance).toBe(true);
  }
 });
});
