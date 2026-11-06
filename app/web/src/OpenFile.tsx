import {useState} from 'react';
import {ExternalLink} from 'lucide-react';
import {api} from './api';
import type {Detail} from './types';

// Abre o arquivo no programa do computador. O slide abre a apresentação de origem inteira.
// Fica nas duas telas da ficha: a tela grande, que é a que abre ao clicar, e o painel da Ficha completa.
export function OpenFile({detail}:{detail:Detail}){
 const file=detail.presentation_file,[error,setError]=useState('');
 if(!file)return null;
 const label=file.mime==='application/pdf'?'Abrir PDF':'Abrir no PowerPoint';
 const open=async()=>{setError('');try{await api('/assets/'+file.id+'/open',{});}catch(e){setError((e as Error).message);}};
 return <><button onClick={open} title={detail.parent_id?'Abre a apresentação completa':undefined}><ExternalLink size={14}/> {label}</button>{error&&<p className="open-file-error" role="alert">{error}</p>}</>;
}
