// Prévia reduzida no maior lado (128, 256, 512, 1024 ou 2048 px); o original segue para download.
export const sized=(url:string|undefined,width:number)=>url&&url+'?w='+width;

const OFFLINE='Não consegui falar com o serviço do Repertório. Confira se ele está ligado e tente de novo.';

// Erros chegam em português: serviço desligado, falha do serviço ou a mensagem que ele devolveu.
async function request<T>(path:string,init:RequestInit):Promise<T>{
  let response:Response;
  try{response=await fetch('/api'+path,init);}catch(e){if((e as Error).name==='AbortError')throw e;throw new Error(OFFLINE);}
  if(!response.ok){const error=await response.json().catch(()=>({detail:response.status>=500?'O serviço do Repertório teve um problema. Tente de novo.':OFFLINE}));throw new Error(typeof error.detail==='string'?error.detail:'Não consegui concluir o pedido. Recarregue a página e tente de novo.');}
  return response.json();
}

// signal: o React Query cancela o pedido quando uma recarga mais nova toma o lugar.
export function api<T>(path:string,body?:unknown,method?:string,signal?:AbortSignal):Promise<T>{
  return request<T>(path,{method:method||(body?'POST':'GET'),headers:body?{'Content-Type':'application/json'}:undefined,body:body?JSON.stringify(body):undefined,signal});
}

// Arquivos do computador para um espaço: cada um vira uma referência, processada em segundo plano.
export function uploadFiles(workspaceId:string,files:File[]){
  const form=new FormData();for(const file of files)form.append('files',file,file.name);
  return request<{operations:{id:string}[]}>('/workspaces/'+encodeURIComponent(workspaceId)+'/upload',{method:'POST',body:form});
}
