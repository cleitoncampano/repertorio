import {describe,expect,it} from 'vitest';
import {parseMarkdown,resolveLink} from './skillMarkdown';

describe('leitura das skills',()=>{
 it('separa títulos, listas com recuo, tabelas, citações e código sem ler o que está dentro do bloco',()=>{
  const blocks=parseMarkdown(['# Título','Primeira linha','continua aqui.','','- um','  - dentro','- dois','','1. passo','','| A | B |','|---|:-:|','| x | y |','','> nota','','```js','# não é título','```','','---'].join('\n'));
  expect(blocks.map(b=>b.kind)).toEqual(['heading','paragraph','list','list','table','quote','code','rule']);
  expect(blocks[1]).toEqual({kind:'paragraph',text:'Primeira linha continua aqui.'});
  expect(blocks[2]).toMatchObject({items:[{depth:0,text:'um'},{depth:1,text:'dentro'},{depth:0,text:'dois'}]});
  expect(blocks[3]).toMatchObject({items:[{ordered:true,text:'passo'}]});
  expect(blocks[4]).toEqual({kind:'table',head:['A','B'],rows:[['x','y']]});
  expect(blocks[6]).toEqual({kind:'code',text:'# não é título'});
 });
 it('itens separados por linha em branco seguem na mesma lista e a tabela não engole o parágrafo anterior',()=>{
  expect(parseMarkdown('- a\n\n- b')).toEqual([{kind:'list',items:[{depth:0,ordered:false,text:'a'},{depth:0,ordered:false,text:'b'}]}]);
  expect(parseMarkdown('Antes\n| A |\n|---|\n| 1 |').map(b=>b.kind)).toEqual(['paragraph','table']);
 });
 it('links relativos ficam dentro da pasta da skill',()=>{
  expect(resolveLink('SKILL.md','references/guia.md#parte')).toBe('references/guia.md');
  expect(resolveLink('references/guia.md','./outro.md')).toBe('references/outro.md');
  expect(resolveLink('references/guia.md','../SKILL.md')).toBe('SKILL.md');
  expect(resolveLink('SKILL.md','../fora.md')).toBeNull();
 });
});
