import {describe,it,expect} from 'vitest';
import {sourceCredit,sourcePage} from './motionSource';

describe('fonte da referência',()=>{
 it('cita o Prompt Motion só nos vídeos reunidos lá',()=>{
  const video={collection:'prompt-motion',page:'https://prompt-motion.com/x',author:'Ana',handle:'ana',posted:'2026-05-02',title_original:'Launch'};
  expect(sourceCredit(video)).toBe('Criado por Ana (@ana), publicado em 02/05/2026, reunido no Prompt Motion. Título original: “Launch”.');
  expect(sourcePage(video)).toEqual({href:'https://prompt-motion.com/x',label:'Prompt Motion'});
 });
 it('slide de PDF não vira link nem cita o Prompt Motion',()=>{
  const slide={collection:'soap',file:'soap/ebook.pdf',page:12};
  expect(sourceCredit(slide)).toBe('');
  expect(sourcePage(slide)).toBeNull();
 });
 it('vídeo de outra coleção abre a página da fonte',()=>{
  const course={collection:'perestroika',page:'https://perestroika.com.br/cursos/chora-ppt/',author:'Perestroika'};
  expect(sourceCredit(course)).toBe('Criado por Perestroika.');
  expect(sourcePage(course)).toEqual({href:'https://perestroika.com.br/cursos/chora-ppt/',label:'Página da fonte'});
 });
});
