import {normalize} from './skillCatalog';

export type Repo={
 id:string;
 name:string;
 category:string;
 description:string;
 use:string;
 url:string;
 icon?:string;
};

export function searchRepos(repos:readonly Repo[],query:string){
 const words=normalize(query).trim().split(/\s+/).filter(Boolean);
 return repos.filter(repo=>words.every(word=>normalize([repo.id,repo.name,repo.category,repo.description,repo.use,repo.url].join(' ')).includes(word)));
}
