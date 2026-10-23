import {useState} from 'react';
import {ArrowUpRight,Brain,Film,FolderGit2,Gauge,Search,Sparkles,X} from 'lucide-react';
import {repos,searchRepos} from './repoCatalog';

const icons:Record<string,typeof FolderGit2>={engram:Brain,rtk:Gauge,hyperframes:Film};

export function Repositories(){
 const [query,setQuery]=useState('');
 const matches=searchRepos(query);
 return <section className="collection-page skills-page" aria-label="Catálogo de repositórios">
  <div className="skills-intro"><div><span className="eyebrow"><FolderGit2 size={14}/> REPOSITÓRIOS</span><h1>Ferramentas que trabalham junto.</h1><p className="page-intro">Projetos abertos que usamos com o Repertório. Abra o repositório para ver instalação, novidades e documentação.</p></div><span className="skills-curated">{repos.length===1?'1 repositório escolhido por você':repos.length+' repositórios escolhidos por você'}</span></div>
  <div className="skills-tools"><label className="skills-search"><Search size={17}/><input aria-label="Buscar repositórios" placeholder="O que você procura?" value={query} onChange={e=>setQuery(e.target.value)}/>{query&&<button aria-label="Limpar busca de repositórios" onClick={()=>setQuery('')}><X size={15}/></button>}</label></div>
  <div className="skills-context"><Sparkles size={15}/><span>Repositórios que trazem só uma skill ficam na aba Skills.</span></div>
  <div className="skills-grid">{matches.map(repo=>{const Icon=icons[repo.id]||FolderGit2;return <article key={repo.id} className="skill-card" aria-labelledby={'repo-'+repo.id}>
   <div className="skill-card-top"><Icon size={22} strokeWidth={1.5}/><span>{repo.category}</span></div><h2 id={'repo-'+repo.id}>{repo.name}</h2><p>{repo.description}</p><div className="skill-when"><span>NO REPERTÓRIO</span><p>{repo.use}</p></div><a href={repo.url} target="_blank" rel="noreferrer"><span>{repo.url.replace('https://','')}</span><ArrowUpRight size={16}/></a>
  </article>;})}</div>
  {!matches.length&&<div className="skills-empty"><Search size={24}/><h2>Nenhum repositório encontrado.</h2><p>Tente outra palavra.</p><button onClick={()=>setQuery('')}>Ver todos os repositórios</button></div>}
 </section>;
}
