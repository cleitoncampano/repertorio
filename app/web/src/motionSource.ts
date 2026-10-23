import type {MotionSource} from './types';

// Crédito da fonte em uma frase. Só os vídeos reunidos no Prompt Motion citam o site.
export function sourceCredit(s:MotionSource){
 const posted=s.posted&&`publicado em ${new Date(s.posted+'T12:00:00').toLocaleDateString('pt-BR')}`;
 const text=[s.author&&`Criado por ${s.author}${s.handle?` (@${s.handle})`:''}`,posted,s.collection==='prompt-motion'&&'reunido no Prompt Motion'].filter(Boolean).join(', ');
 const credit=text?text[0].toUpperCase()+text.slice(1)+'.':'';
 return [credit,s.title_original&&`Título original: “${s.title_original}”.`].filter(Boolean).join(' ');
}

// Slides de PDF guardam o número da página em `page`; só endereço vira link.
export function sourcePage(s:MotionSource){
 if(typeof s.page!=='string'||!/^https?:\/\//.test(s.page))return null;
 return {href:s.page,label:s.collection==='prompt-motion'?'Prompt Motion':'Página da fonte'};
}
