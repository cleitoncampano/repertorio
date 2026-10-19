import {terms,type GraphData} from './types';
export type MapFocus={selected:string|null;technique:string;operation:string;matches:string[]|null};
export function graphFocus(data:GraphData,focus:MapFocus){
 const {selected,technique,operation,matches}=focus;
 if(!selected&&!technique&&!operation&&!matches)return null;
 const techniques=terms(data.vocabulary,'tecnicas');
 const selectedRef=data.items.find(i=>i.id===selected);
 const ts=new Set(selectedRef?.techniques|| (technique?[technique]:operation?techniques.filter(t=>t.operacao===operation).map(t=>t.id):[]));
 const found=matches?new Set(matches):null;
 const refs=new Set(data.items.filter(item=>selected?item.id===selected:(!found||found.has(item.id))&&(!(technique||operation)||item.techniques.some(t=>ts.has(t)))).map(i=>i.id));
 if(!selected&&!technique&&!operation)for(const item of data.items)if(refs.has(item.id))item.techniques.forEach(t=>ts.add(t));
 const ops=new Set(techniques.filter(t=>ts.has(t.id)).map(t=>t.operacao).filter((s):s is string=>!!s));
 if(operation)ops.add(operation);
 const cues=new Set(techniques.filter(t=>ts.has(t.id)&&t.pista).map(t=>'cue:'+t.operacao+':'+t.pista));
 return {references:refs,techniques:ts,operations:ops,cues};
}
