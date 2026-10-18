import {colors} from './types';
import type {GraphView} from './graphViewOptions';

export type ExperimentalView='cosmos'|'metro'|'circuit'|'garden'|'editorial'|'prism';
type Shape='ellipse'|'roundrectangle'|'rectangle'|'hexagon'|'diamond'|'triangle';
export type GraphSkin={
 background:string;ink:string;surface:string;palette:readonly string[];
 operationShape:Shape;referenceShape:Shape;techniqueShape:Shape;
 operationWidth:number;operationHeight:number;referenceRatio:number|null;
 curve:'unbundled-bezier'|'taxi'|'straight';line:'solid'|'dotted';edgeWidth:number;edgeOpacity:number;font:string;
};
const designs:Record<ExperimentalView,Omit<GraphSkin,'background'|'ink'|'surface'|'palette'>>={
 cosmos:{operationShape:'ellipse',referenceShape:'ellipse',techniqueShape:'diamond',operationWidth:290,operationHeight:290,referenceRatio:1,curve:'unbundled-bezier',line:'solid',edgeWidth:1,edgeOpacity:.12,font:'Avenir Next, sans-serif'},
 metro:{operationShape:'roundrectangle',referenceShape:'roundrectangle',techniqueShape:'ellipse',operationWidth:640,operationHeight:200,referenceRatio:null,curve:'taxi',line:'solid',edgeWidth:2.4,edgeOpacity:.18,font:'Avenir Next, sans-serif'},
 circuit:{operationShape:'hexagon',referenceShape:'roundrectangle',techniqueShape:'rectangle',operationWidth:590,operationHeight:240,referenceRatio:1.35,curve:'taxi',line:'solid',edgeWidth:1.2,edgeOpacity:.16,font:'monospace'},
 garden:{operationShape:'ellipse',referenceShape:'ellipse',techniqueShape:'ellipse',operationWidth:560,operationHeight:220,referenceRatio:1.4,curve:'unbundled-bezier',line:'solid',edgeWidth:1.4,edgeOpacity:.14,font:'Georgia, serif'},
 editorial:{operationShape:'rectangle',referenceShape:'rectangle',techniqueShape:'rectangle',operationWidth:900,operationHeight:200,referenceRatio:null,curve:'straight',line:'dotted',edgeWidth:1,edgeOpacity:.11,font:'Georgia, serif'},
 prism:{operationShape:'hexagon',referenceShape:'diamond',techniqueShape:'triangle',operationWidth:440,operationHeight:300,referenceRatio:1,curve:'straight',line:'solid',edgeWidth:1.1,edgeOpacity:.16,font:'Avenir Next, sans-serif'},
};
const palettes:Record<ExperimentalView,{dark:[string,string,string,...string[]];light:[string,string,string,...string[]]}>={
 cosmos:{dark:['#090e26','#e7f6ff','#16203e','#64e8ff','#ad8bfa','#ff83bd','#7cf3cf'],light:['#eaf3ff','#223569','#f8fbff','#006c9a','#7051bc','#b72a76','#087d73']},
 metro:{dark:['#19232d','#f1eee3','#26333c','#ee5b65','#ffc857','#5bd2b0','#80b6f4'],light:['#f5f0df','#29342e','#fffdf3','#d74642','#1f9d83','#cf8a13','#4769bd']},
 circuit:{dark:['#071b16','#b7ffc8','#102c23','#a4ed53','#39ddbb','#d8ec8a','#53b1a5'],light:['#eaf2dc','#193e29','#f8fced','#487326','#097460','#7e8425','#22656b']},
 garden:{dark:['#20281f','#f1edd9','#344231','#d5b67c','#9ebc93','#d693a8','#b2a0d0'],light:['#f5f1e5','#334b35','#fffaf0','#607c45','#a0763f','#a75e77','#776b98']},
 editorial:{dark:['#232221','#f3efe4','#302e2a','#ed6b52','#e6dcc5','#c4bbb1','#b79369'],light:['#f8f3e7','#292824','#fffdf6','#c84432','#333b44','#8b694d','#575f4c']},
 prism:{dark:['#241132','#f9edff','#402149','#ff759c','#65d3e8','#ffc36c','#b795ff'],light:['#f2eafd','#4a2861','#fff7ff','#ca316b','#117f9e','#a15e0e','#7955b5']},
};
export function isExperimental(view:GraphView):view is ExperimentalView{return Object.hasOwn(designs,view);}
export function graphSkin(view:GraphView,theme:'dark'|'light'):GraphSkin|null{
 if(!isExperimental(view))return null;
 const [background,ink,surface,...palette]=palettes[view][theme];
 return {...designs[view],background,ink,surface,palette};
}
export function graphColors(view:GraphView,theme:'dark'|'light'):Record<string,string>{
 const skin=graphSkin(view,theme);
 return skin?Object.fromEntries(Object.keys(colors).map((id,index)=>[id,skin.palette[index%skin.palette.length]])):colors;
}
export function readableInk(color:string){
 const channels=color.slice(1).match(/../g)!.map(value=>{const n=parseInt(value,16)/255;return n<=.04045?n/12.92:((n+.055)/1.055)**2.4;});
 const light=.2126*channels[0]+.7152*channels[1]+.0722*channels[2];
 return (light+.05)/.05>1.05/(light+.05)?'#000000':'#ffffff';
}
