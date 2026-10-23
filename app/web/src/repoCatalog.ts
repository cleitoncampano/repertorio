import {normalize} from './skillCatalog';

export type Repo={
 id:string;
 name:string;
 category:string;
 description:string;
 use:string;
 url:string;
};

// Curadoria explícita do usuário. Repositórios que trazem só uma skill ficam no catálogo de Skills.
export const repos:readonly Repo[]=[
 {id:'engram',name:'Engram',category:'Memória',
  description:'Memória local para agentes de IA: guarda decisões, pendências e próximos passos entre uma conversa e outra, num banco no próprio computador.',
  use:'Decisões e pendências do Repertório ficam no Engram, consultado pelo terminal no início de cada demanda.',
  url:'https://github.com/Gentleman-Programming/engram'},
 {id:'rtk',name:'RTK',category:'Agentes',
  description:'Filtra o que os comandos do terminal devolvem ao agente, para gastar menos contexto e render mais por uso da assinatura.',
  use:'Instalado junto com o Engram; o Codex usa nos comandos do terminal deste projeto.',
  url:'https://github.com/rtk-ai/rtk'},
 {id:'hyperframes',name:'HyperFrames',category:'Vídeo',
  description:'Motor que transforma páginas HTML em vídeo MP4, com prévia, conferência dos quadros e renderização final.',
  use:'Os vídeos criados com o kit de motion do Repertório são montados e renderizados com ele.',
  url:'https://github.com/heygen-com/hyperframes'},
];

export function searchRepos(query:string){
 const words=normalize(query).trim().split(/\s+/).filter(Boolean);
 return repos.filter(repo=>words.every(word=>normalize([repo.id,repo.name,repo.category,repo.description,repo.use,repo.url].join(' ')).includes(word)));
}
