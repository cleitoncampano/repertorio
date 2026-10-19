export type SkillCategory='Design'|'Imagens'|'Apresentações'|'Vídeo';
export type Skill={
 id:string;
 name:string;
 category:SkillCategory;
 description:string;
 when:string;
 example:string;
};

// Curadoria explícita do usuário. Instalar uma skill não a inclui no catálogo.
export const skills:readonly Skill[]=[
 {id:'impeccable',name:'Impeccable',category:'Design',
  description:'Revisa e refina interfaces: hierarquia, tipografia, cores, acessibilidade e acabamento.',
  when:'Quero melhorar uma interface que já existe.',
  example:'Revise esta interface e melhore a hierarquia visual, a legibilidade e o acabamento.'},
 {id:'frontend-design',name:'Frontend Design',category:'Design',
  description:'Cria páginas e componentes em código, com identidade visual e atenção aos detalhes.',
  when:'Quero construir uma interface com personalidade.',
  example:'Crie uma página inicial responsiva, com uma direção visual própria e componentes funcionais.'},
 {id:'landing-page-design',name:'Landing Page Design',category:'Design',
  description:'Organiza páginas de conversão com abertura clara, prova social e chamadas para ação.',
  when:'Quero apresentar uma oferta e gerar conversões.',
  example:'Desenhe uma landing page para apresentar nossa solução e incentivar o agendamento de uma conversa.'},
 {id:'imagegen',name:'ImageGen',category:'Imagens',
  description:'Gera e edita imagens, ilustrações e composições a partir de uma ideia ou referência.',
  when:'Preciso de uma imagem original para uma peça.',
  example:'Crie uma ilustração original para a abertura de uma apresentação sobre conexão com o cliente.'},
 {id:'presentations:Presentations',name:'Presentations',category:'Apresentações',
  description:'Cria e edita apresentações em PowerPoint ou Google Slides, com narrativa e composição visual.',
  when:'Quero transformar uma história em um deck de slides.',
  example:'Crie uma apresentação em PowerPoint para contar a história da nossa solução, do problema à proposta.'},
 {id:'hyperframes',name:'HyperFrames',category:'Vídeo',
  description:'Conduz a criação de vídeos e animações, do briefing à prévia e à renderização final.',
  when:'Quero produzir um vídeo ou uma animação.',
  example:'Crie um vídeo de 30 segundos para apresentar nossa solução, com uma abertura forte e um fechamento claro.'},
 {id:'hyperframes-creative',name:'HyperFrames Creative',category:'Vídeo',
  description:'Define a direção criativa de vídeos: estilo, paleta, tipografia, narração e sequência de cenas.',
  when:'Preciso definir o conceito visual antes de produzir.',
  example:'Defina a direção criativa de um vídeo institucional: conceito, paleta, tipografia e sequência de cenas.'},
];

const normalize=(text:string)=>text.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase('pt-BR');
export function searchSkills(query:string,category:SkillCategory|'Todas'='Todas'){
 const words=normalize(query).trim().split(/\s+/).filter(Boolean);
 return skills.filter(skill=>(category==='Todas'||skill.category===category)&&words.every(word=>normalize([skill.id,skill.name,skill.category,skill.description,skill.when,skill.example].join(' ')).includes(word)));
}

export function buildSkillRequest(skill:Skill,goal:string,workspace?:{id:string;name:string}){
 return [
  `Use a skill ${skill.id} (${skill.name}) para esta demanda:`,
  goal.trim(),
  workspace
   ?`Use como inspiração apenas as referências do espaço ${JSON.stringify(workspace.name)} no Repertório (workspace_id: ${workspace.id}).`
   :'Antes de buscar referências, me pergunte qual espaço do Repertório deve servir de inspiração.',
  'Antes de criar, consulte o Repertório, registre a seleção de referências e me mostre a revisão em Escolhas. Use as referências aprovadas, respeite meus comentários e siga a identidade do projeto.',
  'Crie e salve rascunhos, imagens, prévias e arquivos finais no projeto desta produção, fora do Repertório.',
 ].join('\n\n');
}
