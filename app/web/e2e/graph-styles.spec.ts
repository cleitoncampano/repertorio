import {test,expect} from '@playwright/test';

const options=[['cosmos','Cosmos'],['metro','Metrô'],['circuit','Circuito'],['garden','Jardim'],['editorial','Editorial'],['prism','Prisma']];
const choose=async(page:any,name:string)=>{await page.getByRole('button',{name:'Visualização do grafo',exact:true}).click();await page.getByRole('menuitemradio',{name,exact:true}).click();};
const state=async(page:any)=>page.evaluate(()=>{
 const c=(document.querySelector('.map-surface') as any)._cyreg.cy,node=c.getElementById('ref:deck'),op=c.getElementById('op:diferenciacao');
 return {ids:c.elements().map((item:any)=>item.id()).sort(),marker:c.scratch('qa-style'),shape:node.style('shape'),width:node.width(),height:node.height(),image:node.data('image'),opColor:op.style('border-color'),operationBounds:op.renderedBoundingBox(),active:node.hasClass('active'),background:getComputedStyle(document.querySelector('.map-stage')!).backgroundColor,texture:getComputedStyle(document.querySelector('.map-stage')!).backgroundImage};
});

test('seis linguagens visuais preservam o grafo, as imagens e a seleção nos dois temas',async({page})=>{
 const errors:string[]=[];page.on('pageerror',error=>errors.push(error.message));
 await page.goto('/?workspace=pp-treta&ref=deck');
 await expect(page.locator('.detail-body h2')).toHaveText('Abertura criativa');
 await expect.poll(async()=>(await state(page)).image).not.toBe('none');
 await page.evaluate(()=>{(document.querySelector('.map-surface') as any)._cyreg.cy.scratch('qa-style','same-instance');});
 const original=await state(page),bounds=await page.locator('.map-stage').boundingBox();
 for(const theme of ['dark','light']){
  if(theme==='light')await page.getByRole('button',{name:'Ativar modo claro',exact:true}).click();
  const backgrounds=new Set<string>(),opColors=new Set<string>(),shapes=new Set<string>();
  for(const [id,label] of options){
   await choose(page,label);
   await expect(page.locator('.map-stage')).toHaveAttribute('data-view',id);
   const next=await state(page);
   expect(next.ids).toEqual(original.ids);expect(next.marker).toBe('same-instance');expect(next.active).toBe(true);
   expect(next.image).not.toBe('none');expect(next.texture).not.toBe('none');
   backgrounds.add(next.background);opColors.add(next.opColor);shapes.add(next.shape);
   await expect(page.locator('.detail-body h2')).toHaveText('Abertura criativa');
   expect(await page.locator('.map-stage').boundingBox()).toEqual(bounds);
   const legend=page.getByRole('button',{name:'Diferenciação',exact:true}).locator('i');
   expect((await legend.evaluate(element=>getComputedStyle(element).backgroundColor)).replace(/\s/g,'')).toBe(next.opColor.replace(/\s/g,''));
  }
  expect(backgrounds.size).toBe(6);expect(opColors.size).toBe(6);expect(shapes.size).toBeGreaterThanOrEqual(4);
 }
 await page.evaluate(()=>{(document.querySelector('.map-surface') as any)._cyreg.cy.zoom(.09);});
 await expect.poll(()=>page.evaluate(()=>(document.querySelector('.map-surface') as any)._cyreg.cy.getElementById('op:diferenciacao').renderedWidth())).toBeGreaterThan(100);
 await choose(page,'Mapa livre');
 await expect(page.locator('.map-stage')).toHaveCSS('background-color','rgb(247, 245, 240)');
 const restored=await state(page);
 expect(restored.shape).toBe('rectangle');expect(restored.opColor.replace(/\s/g,'')).toBe('rgb(255,90,60)');expect(restored.texture).toBe('none');
 expect(restored.active).toBe(true);expect(restored.marker).toBe('same-instance');
 await page.getByRole('button',{name:'Fechar detalhes',exact:true}).click();
 await page.getByRole('button',{name:'Diferenciação',exact:true}).click();
 for(const name of ['Circuito','Editorial','Jardim']){
  await choose(page,name);
  await expect.poll(async()=>(await state(page)).operationBounds.x1).toBeGreaterThan(72);
  await expect.poll(async()=>(await state(page)).operationBounds.y1).toBeGreaterThan(80);
  const panel=(await page.getByRole('complementary',{name:'Detalhes do eixo'}).boundingBox())!;
  expect((await state(page)).operationBounds.x2).toBeLessThan(panel.x);
 }
 expect(errors).toEqual([]);
});

test('as nove prévias cabem no menu e o último estilo é acessível no celular e no teclado',async({page})=>{
 await page.setViewportSize({width:320,height:740});await page.emulateMedia({reducedMotion:'reduce'});
 await page.goto('/?workspace=pp-treta');await expect(page.locator('canvas').first()).toBeVisible();
 const button=page.getByRole('button',{name:'Visualização do grafo',exact:true});await button.click();
 const menu=page.getByRole('menu',{name:'Visualização do grafo'});
 await expect(menu.getByRole('menuitemradio')).toHaveCount(9);
 await page.keyboard.press('End');await expect(page.getByRole('menuitemradio',{name:'Prisma',exact:true})).toBeFocused();
 const rect=(await menu.boundingBox())!;expect(rect.x).toBeGreaterThanOrEqual(0);expect(rect.x+rect.width).toBeLessThanOrEqual(320);expect(rect.y+rect.height).toBeLessThanOrEqual(740);
 await page.keyboard.press('Enter');await expect(page.locator('.map-stage')).toHaveAttribute('data-view','prism');
 await page.reload();await expect(page.locator('.map-stage')).toHaveAttribute('data-view','prism');
 await button.click();await expect(page.getByRole('menuitemradio',{name:'Prisma',exact:true})).toHaveAttribute('aria-checked','true');
 await page.keyboard.press('Tab');await expect(menu).toBeHidden();await expect(page.locator('.workspace-current')).toBeFocused();
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
});
