import {useState} from 'react';
import {ArrowUpRight,Brain,Film,FolderGit2,Gauge,Search,Sparkles,X} from 'lucide-react';
import {searchRepos} from './repoCatalog';
import {useCatalog} from './catalog';

const icons:Record<string,typeof FolderGit2>={Brain,Gauge,Film};

export function Repositories(){
 const catalog=useCatalog(),repos=catalog.data?.repos||[];
 const [query,setQuery]=useState('');
 const matches=searchRepos(repos,query);
 return <section className="collection-page skills-page" aria-label="Catálogo de repositórios">
  <div className="skills-intro"><div><span className="eyebrow"><FolderGit2 size={14}/> REPOSITÓRIOS</span><h1>Ferramentas que trabalham junto.</h1><p className="page-intro">Projetos abertos que funcionam bem com o Repertório. Abra o repositório para ver instalação, novidades e documentação.</p></div><span className="skills-curated">{catalog.isSuccess&&(repos.length===1?'1 repositório':repos.length+' repositórios')+(catalog.data.personal?(repos.length===1?' escolhido por você':' escolhidos por você'):(repos.length===1?' sugerido':' sugeridos'))}</span></div>
  <div className="skills-tools"><label className="skills-search"><Search size={17}/><input aria-label="Buscar repositórios" placeholder="O que você procura?" value={query} onChange={e=>setQuery(e.target.value)}/>{query&&<button aria-label="Limpar busca de repositórios" onClick={()=>setQuery('')}><X size={15}/></button>}</label></div>
  <div className="skills-context"><Sparkles size={15}/><span>Repositórios que trazem só uma skill ficam na aba Skills.</span></div>
  <div className="skills-grid">{matches.map(repo=>{const Icon=icons[repo.icon||'']||FolderGit2;return <article key={repo.id} className="skill-card" aria-labelledby={'repo-'+repo.id}>
   <div className="skill-card-top"><Icon size={22} strokeWidth={1.5}/><span>{repo.category}</span></div><h2 id={'repo-'+repo.id}>{repo.name}</h2><p>{repo.description}</p><div className="skill-when"><span>NO REPERTÓRIO</span><p>{repo.use}</p></div><a href={repo.url} target="_blank" rel="noreferrer"><span>{repo.url.replace('https://','')}</span><ArrowUpRight size={16}/></a>
  </article>;})}</div>
  {catalog.isError&&<div className="skills-empty" role="alert"><Search size={24}/><h2>Não consegui carregar os repositórios.</h2><p>Confira se o serviço do Repertório está ligado e recarregue a página.</p></div>}
  {catalog.isSuccess&&!matches.length&&<div className="skills-empty"><Search size={24}/><h2>Nenhum repositório encontrado.</h2><p>Tente outra palavra.</p><button onClick={()=>setQuery('')}>Ver todos os repositórios</button></div>}
 </section>;
}
