import {describe,it,expect} from 'vitest';
import {buildSkillRequest,searchSkills,skills} from './skillCatalog';

describe('descoberta de skills',()=>{
 it('encontra um objetivo sem depender de acentos ou capitalização',()=>{
  expect(searchSkills('CONVERSOES')[0].id).toBe('landing-page-design');
  expect(searchSkills('ilustracao original').map(skill=>skill.id)).toContain('imagegen');
 });
 it('combina as palavras da busca com a categoria escolhida',()=>{
  expect(searchSkills('visual','Vídeo').map(skill=>skill.id)).toEqual(['hyperframes-creative']);
  expect(searchSkills('impeccable','Imagens')).toEqual([]);
  expect(searchSkills('   ','Design')).toHaveLength(3);
 });
 it('inclui somente o espaço indicado no pedido e respeita a revisão',()=>{
  const skill=skills.find(item=>item.id==='frontend-design')!;
  const request=buildSkillRequest(skill,'  Crie um painel de CX.  ',{id:'growmate-id',name:'GrowMate'});
  expect(request).toContain('skill frontend-design');
  expect(request).toContain('\n\nCrie um painel de CX.\n\n');
  expect(request).toContain('apenas as referências do espaço "GrowMate"');
  expect(request).toContain('workspace_id: growmate-id');
  expect(request).toContain('referências aprovadas');
  expect(request).not.toContain('PP Treta');
 });
 it('pede o espaço quando nenhum foi escolhido',()=>{
  const request=buildSkillRequest(skills[0],'Melhore a interface.');
  expect(request).toContain('me pergunte qual espaço');
  expect(request).not.toContain('workspace_id:');
 });
});
