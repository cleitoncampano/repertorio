export type Skill={
 id:string;
 name:string;
 category:string;
 description:string;
 when:string;
 example:string;
 // A skill só roda quando chamada pelo comando, não pelo pedido em texto.
 manual?:boolean;
 // Repositório para instalar a skill no agente.
 source?:string;
 // Nome do ícone do Lucide no cartão.
 icon?:string;
};

// O catálogo vem do servidor (/api/catalog): o da pasta de dados do usuário, o da biblioteca ou o padrão do pacote.
export const normalize=(text:string)=>text.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase('pt-BR');
// Categorias na ordem em que aparecem no catálogo.
export const skillCategories=(skills:readonly Skill[])=>['Todas',...new Set(skills.map(skill=>skill.category))];

export function searchSkills(skills:readonly Skill[],query:string,category='Todas'){
 const words=normalize(query).trim().split(/\s+/).filter(Boolean);
 return skills.filter(skill=>(category==='Todas'||skill.category===category)&&words.every(word=>normalize([skill.id,skill.name,skill.category,skill.description,skill.when,skill.example].join(' ')).includes(word)));
}

export function buildSkillRequest(skill:Skill,goal:string,workspace?:{id:string;name:string}){
 return [
  ...(skill.manual?[`/${skill.id}`]:[]),
  `Use a skill ${skill.id} (${skill.name}) para esta demanda:`,
  goal.trim(),
  workspace
   ?`Use como inspiração apenas as referências do espaço ${JSON.stringify(workspace.name)} no Repertório (workspace_id: ${workspace.id}).`
   :'Antes de buscar referências, me pergunte qual espaço do Repertório deve servir de inspiração.',
  'Antes de criar, consulte o Repertório (e o guia do momento ou do tipo de peça, se a biblioteca tiver) e me diga quais referências vai usar e por quê, com os links. Siga a identidade do projeto.',
  'Crie e salve rascunhos, imagens, prévias e arquivos finais no projeto desta produção, fora do Repertório.',
 ].join('\n\n');
}
