import {graphSkin,isExperimental} from './graphSkins';
import type {GraphView} from './graphViewOptions';

export function GraphPreview({view,theme}:{view:GraphView;theme:'dark'|'light'}){
 if(isExperimental(view)){
  const skin=graphSkin(view,theme)!,p=skin.palette;
  let content;
  if(view==='cosmos')content=<><g fill="none" stroke={p[1]} opacity=".4"><ellipse cx="46" cy="32" rx="20" ry="17"/><ellipse cx="46" cy="32" rx="38" ry="27"/></g>{[[17,15],[76,17],[33,57],[81,47],[9,36],[57,6],[57,46],[27,30],[58,23]].map(([x,y],i)=><circle key={i} cx={x} cy={y} r={i%3===0?3:2} fill={p[i%4]}/>)}<circle cx="46" cy="32" r="6" fill={p[0]}/></>;
  else if(view==='metro')content=<><g fill="none" strokeWidth="3" strokeLinejoin="round"><path d="M8 17H34V45H84" stroke={p[0]}/><path d="M9 49H62V12H84" stroke={p[2]}/><path d="M18 7V31H80" stroke={p[1]}/></g>{[[18,17],[34,31],[62,31],[62,45],[78,45],[18,49]].map(([x,y],i)=><circle key={i} cx={x} cy={y} r="3" fill={skin.surface} stroke={skin.ink} strokeWidth="1"/>)}</>;
  else if(view==='circuit')content=<><g stroke={p[1]} fill="none" strokeWidth="1.3"><path d="M9 11H27V25H42M9 53H31V39H43M82 11H67V26H50M82 52H64V40H49"/><path d="M43 7V19M51 7V19M43 45V57M51 45V57"/></g><rect x="36" y="20" width="22" height="25" rx="2" fill={skin.surface} stroke={p[0]}/>{[[10,11],[9,53],[82,11],[82,52]].map(([x,y],i)=><rect key={i} x={x-2} y={y-2} width="4" height="4" fill={p[0]}/>)}<path d="M42 28h10m-10 7h6" stroke={p[0]}/></>;
  else if(view==='garden')content=<><path d="M46 58V24M46 42L24 24M46 34L67 17M46 51L72 39" fill="none" stroke={p[0]} strokeWidth="2"/>{[[20,21,-35],[40,18,35],[69,15,-30],[73,38,-25],[24,43,25]].map(([x,y,a],i)=><ellipse key={i} cx={x} cy={y} rx="10" ry="6" transform={`rotate(${a} ${x} ${y})`} fill={p[i%4]}/>)}<ellipse cx="46" cy="57" rx="12" ry="3" fill={p[0]}/></>;
  else if(view==='editorial')content=<><path d="M8 12H84" stroke={p[0]} strokeWidth="4"/><path d="M8 20H84M8 57H84" stroke={skin.ink} strokeWidth=".6"/>{[9,35,61].map((x,i)=><g key={x}><rect x={x} y="26" width="21" height={i===1?18:12} fill={i===1?p[0]:skin.ink} opacity={i===1?1:.8}/><path d={`M${x} 48h21m-21 4h15`} stroke={skin.ink} strokeWidth="1"/></g>)}</>;
  else content=<>{Array.from({length:12},(_,i)=>{const col=i%4,row=Math.floor(i/4),x=36+(col-row)*12,y=12+(col+row)*8;return <path key={i} d={`M${x} ${y-6}l10 6-10 6-10-6Z`} fill={p[(col+row)%4]} stroke={skin.background} strokeWidth="1.5"/>;})}</>;
  return <svg className="graph-view-preview" viewBox="0 0 92 64" aria-hidden="true" style={{background:skin.background,color:skin.ink}}>{content}</svg>;
 }
 const points=view==='free'?[[46,32],[23,19],[66,18],[27,46],[69,46],[9,30],[83,32],[44,9],[45,55]]:view==='grouped'?[[23,18],[10,10],[36,9],[11,29],[36,28],[68,45],[56,35],[81,35],[56,55],[82,56]]:[[12,32],[43,16],[43,48],[79,8],[79,24],[79,40],[79,56]];
 const paths=view==='free'?[[0,1],[0,2],[0,3],[0,4],[1,5],[2,6],[1,7],[3,8],[4,6]]:view==='grouped'?[[0,1],[0,2],[0,3],[0,4],[5,6],[5,7],[5,8],[5,9]]:[[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]];
 return <svg className="graph-view-preview" viewBox="0 0 92 64" aria-hidden="true"><g fill="none" stroke="currentColor" strokeWidth="1" opacity=".4">{paths.map(([a,b],i)=><path key={i} d={view==='hierarchy'?`M${points[a][0]},${points[a][1]}H${(points[a][0]+points[b][0])/2}V${points[b][1]}H${points[b][0]}`:`M${points[a].join(',')}L${points[b].join(',')}`}/>)}</g>{points.map(([x,y],i)=>view==='hierarchy'&&i>2?<rect key={i} x={x-4} y={y-3} width={8} height={6} rx={1} fill="currentColor"/>:<circle key={i} cx={x} cy={y} r={i===0||view==='grouped'&&i===5?5:3} fill={i===0?'#FF5A3C':view==='grouped'&&i>=5?'#3E7BFF':'currentColor'} opacity={i===0?1:.8}/>)}</svg>;
}
