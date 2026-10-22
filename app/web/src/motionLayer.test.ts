import {describe,expect,it} from 'vitest';
import {MOTION_LIMIT,motionClip,pickMotion,type MotionBox} from './motionLayer';

const box=(id:string,x:number,y:number,w=120,h=68):MotionBox=>({id,src:'/api/assets/'+id,x,y,w,h});

describe('vídeos no mapa',()=>{
 it('toca só capas visíveis e grandes o bastante, do centro para fora',()=>{
  const picked=pickMotion([box('longe',-200,300),box('pequena',500,300,40,22),box('borda',60,300),box('centro',500,300)],1000,600);
  expect(picked.map(b=>b.id)).toEqual(['centro','borda']);
 });
 it('limita quantos vídeos tocam ao mesmo tempo',()=>{
  const many=Array.from({length:40},(_,i)=>box('v'+i,100+i*20,300));
  expect(pickMotion(many,1000,600)).toHaveLength(MOTION_LIMIT);
 });
 it('recorta o vídeo no formato da capa',()=>{
  expect(motionClip('ellipse',100,100)).toBe('ellipse(50% 50%)');
  expect(motionClip('roundrectangle',100,50)).toBe('inset(0 round 6px)');
  expect(motionClip(undefined,100,50)).toBe('');
 });
});
