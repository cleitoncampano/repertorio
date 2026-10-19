import {useState} from 'react';
import {useQuery,useQueryClient} from '@tanstack/react-query';
import * as Dialog from '@radix-ui/react-dialog';
import {Layers,Plus,X,Pencil,Trash2,ArrowRight} from 'lucide-react';
import {api} from './api';
import type {Detail,Workspace} from './types';

export function WorkspaceMenu({spaces,current,onSelect,open,onOpenChange}:{spaces:Workspace[];current:string;onSelect:(id:string)=>void;open:boolean;onOpenChange:(open:boolean)=>void}){
 const client=useQueryClient();
 const [name,setName]=useState(''),[editing,setEditing]=useState<Workspace|null>(null),[error,setError]=useState(''),[busy,setBusy]=useState(false);
 const change=async(action:()=>Promise<unknown>)=>{setBusy(true);setError('');try{await action();await client.invalidateQueries({queryKey:['workspaces']});}catch(e){setError((e as Error).message);}finally{setBusy(false);}};
 const enter=(id:string)=>{onSelect(id);onOpenChange(false);};
 return <Dialog.Root open={open} onOpenChange={value=>{if(!busy){onOpenChange(value);setError('');}}}><Dialog.Portal><Dialog.Overlay className="dialog-overlay"/><Dialog.Content className="spaces-dialog">
  <Dialog.Close className="dialog-close" aria-label="Fechar espaços"><X size={20}/></Dialog.Close>
  <Dialog.Title><Layers size={22}/> Espaços</Dialog.Title><Dialog.Description>Escolha o repertório que deseja explorar. Cada espaço tem seu próprio acervo.</Dialog.Description>
  <form className="space-form" onSubmit={e=>{e.preventDefault();void change(async()=>{const saved=await api<Workspace>('/workspaces'+(editing?'/'+editing.id:''),{name,...(editing?{expected_revision:editing.revision}:{})},editing?'PUT':'POST');client.setQueryData<Workspace[]>(['workspaces'],old=>[...(old||[]).filter(w=>w.id!==saved.id),{...saved,references_count:old?.find(w=>w.id===saved.id)?.references_count||0}]);setName('');setEditing(null);if(!editing)enter(saved.id);});}}>
   <input aria-label={editing?'Novo nome do espaço':'Nome do novo espaço'} placeholder="Nome do novo espaço" value={name} onChange={e=>setName(e.target.value)} maxLength={120} required/>
   <button disabled={busy||!name.trim()} type="submit"><Plus size={16}/>{editing?'Salvar nome':'Criar espaço'}</button>{editing&&<button type="button" onClick={()=>{setEditing(null);setName('');}}>Cancelar</button>}
  </form>
  <div className="space-list">{spaces.map(space=><div key={space.id} className={'space-row'+(current===space.id?' current':'')}>
   <button className="space-enter" onClick={()=>enter(space.id)}><Layers size={18}/><span><strong>{space.name}</strong><small>{space.references_count} referências{space.id===current?' · aberto':''}</small></span><ArrowRight size={16}/></button>
   <button aria-label={'Renomear '+space.name} title="Renomear" onClick={()=>{setEditing(space);setName(space.name);}}><Pencil size={16}/></button>
   <button aria-label={'Excluir espaço '+space.name} title="Excluir espaço" disabled={busy} onClick={()=>void change(async()=>{await api('/workspaces/'+space.id+'/state',{deleted:true,expected_revision:space.revision});if(editing?.id===space.id){setEditing(null);setName('');}if(current===space.id)onSelect('');})}><Trash2 size={16}/></button>
  </div>)}</div>
  {error&&<p className="space-error" role="alert">{error}</p>}
 </Dialog.Content></Dialog.Portal></Dialog.Root>;
}

export function ReferenceSpaces({detail,onMoved}:{detail:Detail;onMoved:()=>void}){
 const client=useQueryClient();
 const spaces=useQuery({queryKey:['workspaces'],queryFn:()=>api<Workspace[]>('/workspaces')});
 const [target,setTarget]=useState(''),[error,setError]=useState(''),[busy,setBusy]=useState(false);
 const change=async(move:boolean)=>{setBusy(true);setError('');try{
  await api('/references/'+encodeURIComponent(detail.id)+'/workspaces',{source_workspace_id:detail.workspace_id,target_workspace_ids:[target],expected_membership_revision:detail.membership_revision,move});
  setTarget('');if(move)onMoved();
  await Promise.all(['reference','graph','stats','search','workspaces','activity'].map(key=>client.invalidateQueries({queryKey:[key]})));
 }catch(e){setError((e as Error).message);}finally{setBusy(false);}};
 return <section className="detail-section reference-spaces"><h3>Espaços desta referência</h3><p>{detail.workspaces.map(w=>w.name+(w.state==='trashed'?' (na lixeira)':w.state==='pending'?' (aguardando revisão)':'')).join(', ')}</p>
  <label>Compartilhar ou mover<select aria-label="Espaço de destino" value={target} onChange={e=>setTarget(e.target.value)}><option value="">Escolha um espaço</option>{spaces.data?.filter(w=>w.id!==detail.workspace_id).map(w=><option key={w.id} value={w.id}>{w.name}</option>)}</select></label>
  <div className="space-actions"><button disabled={!target||busy} onClick={()=>void change(false)}>Adicionar ao espaço</button><button disabled={!target||busy} onClick={()=>void change(true)}>Mover para o espaço</button></div><small>Ficha e arquivos são compartilhados. Remover de um espaço preserva os demais.</small>{error&&<p role="alert">{error}</p>}
 </section>;
}
