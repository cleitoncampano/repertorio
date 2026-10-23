import {describe,it,expect} from 'vitest';
import {repos,searchRepos} from './repoCatalog';

describe('catálogo de repositórios',()=>{
 it('cada repositório aponta para o GitHub',()=>{
  for(const repo of repos)expect(repo.url).toMatch(/^https:\/\/github\.com\/[\w.-]+\/[\w.-]+$/);
  expect(new Set(repos.map(repo=>repo.id)).size).toBe(repos.length);
 });
 it('encontra pelo objetivo sem depender de acentos',()=>{
  expect(searchRepos('MEMORIA').map(repo=>repo.id)).toEqual(['engram']);
  expect(searchRepos('video mp4').map(repo=>repo.id)).toEqual(['hyperframes']);
  expect(searchRepos('   ')).toHaveLength(repos.length);
 });
});
