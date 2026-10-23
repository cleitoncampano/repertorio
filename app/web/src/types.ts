export type Workspace={id:string;name:string;revision:number;deleted:string|null;references_count:number};
export type Membership={workspace_id:string;name:string;state:string;membership_revision:number};
// Vídeo de motion: loop curto para o mapa e as listas, vídeo completo e prancha de quadros para a ficha.
export type Motion={loop?:string;video?:string;storyboard?:string;duration?:number;width?:number;height?:number;fps?:number;audio?:boolean;aspect?:string;genres?:string[]};
export type Reference={workspace_id:string;workspace_ids:string[];membership_revision:number;memberships:Membership[];id:string;kind:string;title:string;origin:string;state:string;revision:number;ready:number;parent_id?:string;updated:string;description:string;idea:string;techniques:string[];intentions:string[];movements:string[];aesthetics:string[];strength:number;reusable:boolean|null;thumbnail?:string;url:string;format?:string;unclassified?:boolean;number?:number|null;matched_by?:string[];motion?:Motion;aspect?:string};
export type Asset={id:string;role:string;mime:string;missing:number;url:string};
export type Detail=Reference & {workspaces:Membership[];assets:Asset[];children:Reference[];related:Reference[];usage_notes:string;how?:string;html?:string;good_for?:string[];project_name?:string;source_reference_ids?:string[];unavailable_by_parent?:boolean;prompt?:string;prompt_note?:string;template?:boolean;source?:MotionSource};
export type MotionSource={collection?:string;page?:string;post?:string;author?:string;handle?:string;posted?:string;model?:string;iterations?:string;stack?:string;effort?:string;title_original?:string;skill?:{about?:string;install?:string;repo?:string}};
export type Term={id:string;nome?:string;def:string;operacao?:string;pista?:string;html?:string};
export type Vocabulary=Record<string,{itens:(Term|string)[]}>;
export type GraphData={items:Reference[];vocabulary:Vocabulary};
export const terms=(v:Vocabulary|undefined,key:string):Term[]=>(v?.[key]?.itens||[]).filter((x):x is Term=>typeof x!=='string');
// Os quatro primeiros são os eixos do olhar; os seguintes, os formatos de tela dos espaços de vídeo.
export const colors:Record<string,string>={diferenciacao:'#FF5A3C',agrupamento:'#3E7BFF',sequencia:'#F5B400',previsao:'#B455FF',horizontal:'#FF5A3C',vertical:'#B455FF',quadrado:'#3E7BFF',modelo:'#F5B400'};
export const kindName:Record<string,string>={arquivo:'Apresentação',slide:'Slide',referencia:'Referência',midia:'Mídia',criacao:'Criação'};
