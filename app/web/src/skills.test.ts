import {describe,it,expect} from 'vitest';
import {buildSkillRequest,searchSkills,skillCategories,type Skill} from './skillCatalog';
import catalog from '../../server/repertorio/catalogo_padrao.json';

// Catálogo padrão do pacote: o mesmo que uma instalação nova recebe.
const skills=catalog.skills as Skill[];

describe('descoberta de skills',()=>{
 it('o pacote sugere só skills públicas, com o repositório para instalar',()=>{
  expect(skills.length).toBeGreaterThan(0);
  expect(skills.filter(skill=>/perestroika|soap/.test(skill.id))).toEqual([]);
  for(const skill of skills)expect(skill.source).toMatch(/^https:\/\/github\.com\/[\w.-]+\/[\w.-]+$/);
  expect(new Set(skills.map(skill=>skill.id)).size).toBe(skills.length);
 });
 it('encontra um objetivo sem depender de acentos ou capitalização',()=>{
  expect(searchSkills(skills,'TRAVANDO').map(skill=>skill.id)).toEqual(['animation-performance']);
  expect(searchSkills(skills,'animacao').length).toBeGreaterThan(1);
 });
 it('combina as palavras da busca com a categoria escolhida e lista as categorias do catálogo',()=>{
  expect(searchSkills(skills,'hyperframes')).toEqual([]);
  expect(searchSkills(skills,'impeccable','Animação')).toEqual([]);
  expect(searchSkills(skills,'   ','Design')).toHaveLength(skills.filter(skill=>skill.category==='Design').length);
  expect(searchSkills(skills,'travando','Animação').map(skill=>skill.id)).toEqual(['animation-performance']);
  expect(skillCategories(skills)).toEqual(['Todas','Design','Animação','Código']);
 });
 it('abre com o comando as skills que só rodam quando chamadas',()=>{
  const manual=skills.find(item=>item.id==='prototype')!;
  expect(buildSkillRequest(manual,'Crie três versões.').startsWith('/prototype\n\nUse a skill prototype')).toBe(true);
  expect(buildSkillRequest(skills.find(item=>item.id==='animate')!,'Anime o menu.').startsWith('Use a skill animate')).toBe(true);
 });
 it('inclui somente o espaço indicado no pedido e pede as referências com os links',()=>{
  const skill=skills.find(item=>item.id==='frontend-design')!;
  const request=buildSkillRequest(skill,'  Crie um painel de CX.  ',{id:'cliente-id',name:'Cliente'});
  expect(request).toContain('skill frontend-design');
  expect(request).toContain('\n\nCrie um painel de CX.\n\n');
  expect(request).toContain('apenas as referências do espaço "Cliente"');
  expect(request).toContain('workspace_id: cliente-id');
  expect(request).toContain('quais referências vai usar e por quê, com os links');
  expect(request).not.toContain('Referências');
 });
 it('pede o espaço quando nenhum foi escolhido',()=>{
  const request=buildSkillRequest(skills[0],'Melhore a interface.');
  expect(request).toContain('me pergunte qual espaço');
  expect(request).not.toContain('workspace_id:');
 });
});
