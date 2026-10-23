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
  expect(searchSkills('workshop','Método').map(skill=>skill.id)).toEqual(['perestroika-experiencia']);
  expect(searchSkills('   ','Design')).toHaveLength(8);
  expect(searchSkills('travando','Animação').map(skill=>skill.id)).toEqual(['animation-performance']);
 });
 it('abre com o comando as skills que só rodam quando chamadas',()=>{
  const manual=skills.find(item=>item.id==='prototype')!;
  expect(buildSkillRequest(manual,'Crie três versões.').startsWith('/prototype\n\nUse a skill prototype')).toBe(true);
  expect(buildSkillRequest(skills.find(item=>item.id==='animate')!,'Anime o menu.').startsWith('Use a skill animate')).toBe(true);
 });
 it('inclui somente o espaço indicado no pedido e pede as referências com os links',()=>{
  const skill=skills.find(item=>item.id==='frontend-design')!;
  const request=buildSkillRequest(skill,'  Crie um painel de CX.  ',{id:'growmate-id',name:'GrowMate'});
  expect(request).toContain('skill frontend-design');
  expect(request).toContain('\n\nCrie um painel de CX.\n\n');
  expect(request).toContain('apenas as referências do espaço "GrowMate"');
  expect(request).toContain('workspace_id: growmate-id');
  expect(request).toContain('quais referências vai usar e por quê, com os links');
  expect(request).not.toContain('Referências');
 });
 it('pede o espaço quando nenhum foi escolhido',()=>{
  const request=buildSkillRequest(skills[0],'Melhore a interface.');
  expect(request).toContain('me pergunte qual espaço');
  expect(request).not.toContain('workspace_id:');
 });
});
