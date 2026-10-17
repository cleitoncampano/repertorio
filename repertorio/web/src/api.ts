// Prévia reduzida no maior lado (128, 256, 512, 1024 ou 2048 px); o original segue para download.
export const sized=(url:string|undefined,width:number)=>url&&url+'?w='+width;

export async function api<T>(path:string,body?:unknown,method?:string):Promise<T>{
  const response=await fetch('/api'+path,{method:method||(body?'POST':'GET'),headers:body?{'Content-Type':'application/json'}:undefined,body:body?JSON.stringify(body):undefined});
  if(!response.ok){const error=await response.json().catch(()=>({detail:'Não foi possível acessar o serviço.'}));throw new Error(typeof error.detail==='string'?error.detail:JSON.stringify(error.detail));}
  return response.json();
}
