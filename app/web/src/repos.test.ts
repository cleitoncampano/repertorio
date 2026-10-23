import {describe,it,expect} from 'vitest';
import {searchRepos,type Repo} from './repoCatalog';
import catalog from '../../server/repertorio/catalogo_padrao.json';

const repos=catalog.repos as Repo[];

describe('catálogo de repositórios',()=>{
 it('cada repositório aponta para o GitHub',()=>{
  for(const repo of repos)expect(repo.url).toMatch(/^https:\/\/github\.com\/[\w.-]+\/[\w.-]+$/);
  expect(new Set(repos.map(repo=>repo.id)).size).toBe(repos.length);
 });
 it('encontra pelo objetivo sem depender de acentos',()=>{
  expect(searchRepos(repos,'MEMORIA').map(repo=>repo.id)).toEqual(['engram']);
  expect(searchRepos(repos,'video mp4').map(repo=>repo.id)).toEqual(['hyperframes']);
  expect(searchRepos(repos,'   ')).toHaveLength(repos.length);
 });
});
