import {Fragment,type ReactNode} from 'react';

// Markdown das skills em elementos React, sem HTML cru: títulos, listas, tabelas, citações, blocos de código e
// marcações de linha. Links para arquivos da própria skill abrem dentro da leitura.
type Item={depth:number;ordered:boolean;text:string};
export type Block=
 |{kind:'heading';level:number;text:string}
 |{kind:'code';text:string}
 |{kind:'list';items:Item[]}
 |{kind:'table';head:string[];rows:string[][]}
 |{kind:'quote';text:string}
 |{kind:'rule'}
 |{kind:'paragraph';text:string};

const FENCE=/^\s*(```|~~~)/,HEADING=/^(#{1,6})\s+(.*?)\s*#*\s*$/,RULE=/^\s*([-*_])(\s*\1){2,}\s*$/,ITEM=/^(\s*)([-*+]|\d+[.)])\s+(.*)$/;
const SEPARATOR=/^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$/;
const cells=(line:string)=>line.trim().replace(/^\|/,'').replace(/\|$/,'').split('|').map(cell=>cell.trim());

export function parseMarkdown(source:string):Block[]{
 const lines=source.replace(/\r\n?/g,'\n').split('\n'),blocks:Block[]=[];
 const tableAt=(i:number)=>lines[i].includes('|')&&i+1<lines.length&&SEPARATOR.test(lines[i+1]);
 let i=0;
 while(i<lines.length){
  const line=lines[i];
  if(!line.trim()){i++;continue;}
  const fence=line.match(FENCE);
  if(fence){const body:string[]=[];i++;while(i<lines.length&&!lines[i].trim().startsWith(fence[1]))body.push(lines[i++]);i++;blocks.push({kind:'code',text:body.join('\n')});continue;}
  const heading=line.match(HEADING);
  if(heading){blocks.push({kind:'heading',level:heading[1].length,text:heading[2]});i++;continue;}
  if(RULE.test(line)){blocks.push({kind:'rule'});i++;continue;}
  if(tableAt(i)){
   const head=cells(line),rows:string[][]=[];i+=2;
   while(i<lines.length&&lines[i].trim()&&lines[i].includes('|'))rows.push(cells(lines[i++]));
   blocks.push({kind:'table',head,rows});continue;
  }
  if(/^\s*>/.test(line)){const body:string[]=[];while(i<lines.length&&/^\s*>/.test(lines[i]))body.push(lines[i++].replace(/^\s*>\s?/,''));blocks.push({kind:'quote',text:body.join(' ')});continue;}
  if(ITEM.test(line)){
   const items:Item[]=[];
   while(i<lines.length){
    const item=lines[i].match(ITEM),kind=(marker:string)=>/\d/.test(marker);
    // Outro tipo de marcador no primeiro nível começa outra lista.
    if(item&&items.length&&!item[1]&&kind(item[2])!==items[0].ordered)break;
    if(item){items.push({depth:Math.floor(item[1].replace(/\t/g,'  ').length/2),ordered:/\d/.test(item[2]),text:item[3]});i++;continue;}
    // Continuação do item na linha de baixo, com recuo.
    if(items.length&&lines[i].trim()&&/^\s{2,}/.test(lines[i])&&!FENCE.test(lines[i])){items[items.length-1].text+=' '+lines[i].trim();i++;continue;}
    // Linha em branco entre itens da mesma lista.
    const next=i+1<lines.length?lines[i+1].match(ITEM):null;
    if(!lines[i].trim()&&next&&(next[1]||kind(next[2])===items[0].ordered)){i++;continue;}
    break;
   }
   blocks.push({kind:'list',items});continue;
  }
  const body=[line.trim()];i++;
  while(i<lines.length&&lines[i].trim()&&!FENCE.test(lines[i])&&!HEADING.test(lines[i])&&!/^\s*>/.test(lines[i])&&!ITEM.test(lines[i])&&!tableAt(i))body.push(lines[i++].trim());
  blocks.push({kind:'paragraph',text:body.join(' ')});
 }
 return blocks;
}

// Caminho de um link relativo a partir do arquivo aberto (sem âncora); null quando sai da pasta da skill.
export function resolveLink(from:string,href:string){
 const parts=from.split('/').slice(0,-1);
 for(const part of href.split('#')[0].split('/')){
  if(!part||part==='.')continue;
  if(part==='..'){if(!parts.length)return null;parts.pop();}else parts.push(part);
 }
 return parts.join('/')||null;
}

const INLINE=/(`[^`]+`)|(\*\*[^*]+\*\*|__[^_]+__)|(\[([^\]]+)\]\(([^)\s]+)(?:\s+"[^"]*")?\))|(\*[^*\s][^*]*\*|(?<!\w)_[^_\s][^_]*_(?!\w))|(<(https?:\/\/[^>\s]+)>)/g;

type Links={file:string;files:string[];onOpen:(file:string)=>void};

function inline(text:string,links:Links):ReactNode[]{
 const out:ReactNode[]=[];let last=0,key=0;
 for(const m of text.matchAll(INLINE)){
  if(m.index>last)out.push(text.slice(last,m.index));
  if(m[1])out.push(<code key={key++}>{m[1].slice(1,-1)}</code>);
  else if(m[2])out.push(<strong key={key++}>{inline(m[2].slice(2,-2),links)}</strong>);
  else if(m[3])out.push(link(m[4],m[5],links,key++));
  else if(m[6])out.push(<em key={key++}>{inline(m[6].slice(1,-1),links)}</em>);
  else out.push(link(m[8],m[8],links,key++));
  last=m.index+m[0].length;
 }
 if(last<text.length)out.push(text.slice(last));
 return out;
}

function link(label:string,href:string,links:Links,key:number){
 if(/^https?:\/\//.test(href))return <a key={key} href={href} target="_blank" rel="noreferrer">{inline(label,links)}</a>;
 const target=resolveLink(links.file,href);
 if(target&&(target==='SKILL.md'||links.files.includes(target)))return <button key={key} type="button" className="skill-link" onClick={()=>links.onOpen(target)}>{inline(label,links)}</button>;
 return <span key={key}>{inline(label,links)}</span>;
}

// Itens com recuo viram listas dentro do item anterior.
type Node={item:Item;children:Node[]};
function tree(items:Item[]){
 const root:Node[]=[],stack:{depth:number;children:Node[]}[]=[{depth:-1,children:root}];
 for(const item of items){
  while(stack.length>1&&stack[stack.length-1].depth>=item.depth)stack.pop();
  const node={item,children:[]};stack[stack.length-1].children.push(node);stack.push({depth:item.depth,children:node.children});
 }
 return root;
}

function list(nodes:Node[],links:Links):ReactNode{
 const items=nodes.map((node,i)=>{
  const check=node.item.text.match(/^\[( |x|X)\]\s+(.*)$/);
  return <li key={i}>{check?<>{check[1]===' '?'☐ ':'☑ '}{inline(check[2],links)}</>:inline(node.item.text,links)}{node.children.length>0&&list(node.children,links)}</li>;
 });
 return nodes[0]?.item.ordered?<ol>{items}</ol>:<ul>{items}</ul>;
}

export function SkillMarkdown({text,...links}:{text:string}&Links){
 return <>{parseMarkdown(text).map((block,i)=>{
  switch(block.kind){
   case 'heading':{const Tag=(['h3','h4','h5','h6','h6','h6'] as const)[block.level-1];return <Tag key={i} className={'md-h'+block.level}>{inline(block.text,links)}</Tag>;}
   case 'code':return <pre key={i}><code>{block.text}</code></pre>;
   case 'list':return <Fragment key={i}>{list(tree(block.items),links)}</Fragment>;
   case 'table':return <div key={i} className="md-table"><table><thead><tr>{block.head.map((cell,j)=><th key={j}>{inline(cell,links)}</th>)}</tr></thead><tbody>{block.rows.map((row,r)=><tr key={r}>{block.head.map((_,j)=><td key={j}>{inline(row[j]||'',links)}</td>)}</tr>)}</tbody></table></div>;
   case 'quote':return <blockquote key={i}>{inline(block.text,links)}</blockquote>;
   case 'rule':return <hr key={i}/>;
   default:return <p key={i}>{inline(block.text,links)}</p>;
  }
 })}</>;
}
