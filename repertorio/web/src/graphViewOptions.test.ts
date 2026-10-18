import {describe,expect,it} from 'vitest';
import {graphViewOrder,graphViews} from './graphViewOptions';

describe('ordem das visualizações',()=>{
 const ids=graphViews.map(view=>view.id);
 it('recupera as opções padrão quando a preferência é inválida',()=>{
  for(const invalid of [null,{},'prism',42])expect(graphViewOrder(invalid)).toEqual(ids);
 });
 it('preserva a preferência sem duplicar nem manter opções removidas',()=>{
  expect(graphViewOrder(['prism','free','prism','removida',null])).toEqual(['prism','free',...ids.filter(id=>id!=='prism'&&id!=='free')]);
 });
 it('acrescenta visualizações novas sem desfazer a ordem salva',()=>{
  expect(graphViewOrder(['cosmos','hierarchy'])).toEqual(['cosmos','hierarchy',...ids.filter(id=>id!=='cosmos'&&id!=='hierarchy')]);
 });
});
