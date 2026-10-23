import {test,expect,type Page} from '@playwright/test';

const initial=['free','grouped','hierarchy','cosmos','metro','circuit','garden','editorial','prism'];
const toggle=(page:Page)=>page.getByRole('button',{name:'Visualização do grafo',exact:true});
const menu=(page:Page)=>page.getByRole('menu',{name:'Visualização do grafo'});
const row=(page:Page,id:string)=>menu(page).locator('[data-graph-view="'+id+'"]');
const order=(page:Page)=>menu(page).getByRole('menuitemradio').evaluateAll(elements=>elements.map(element=>(element as HTMLElement).dataset.graphView));

test('arrastar reordena sem trocar o grafo e salva a ordem entre visitas e espaços',async({page,request})=>{
 const errors:string[]=[];page.on('pageerror',error=>errors.push(error.message));
 await page.goto('/?workspace=referencias&ref=deck');
 await expect(page.locator('.detail-body h2')).toHaveText('Abertura criativa');
 await toggle(page).click();
 const source=(await row(page,'free').boundingBox())!,destination=(await row(page,'cosmos').boundingBox())!;
 await page.mouse.move(source.x+120,source.y+source.height/2);await page.mouse.down();
 await page.mouse.move(destination.x+120,destination.y+destination.height-8,{steps:12});
 await expect(page.locator('.graph-view-drag-preview')).toBeVisible();
 await expect(row(page,'metro')).toHaveAttribute('data-drop-before','true');
 await expect(page.locator('.map-stage')).toHaveAttribute('data-view','free');
 await page.screenshot({path:'/tmp/repertorio-graph-order-qa/arrastando-desktop.png',animations:'disabled'});
 await page.mouse.up();
 const expected=['grouped','hierarchy','cosmos','free','metro','circuit','garden','editorial','prism'];
 await expect.poll(()=>order(page)).toEqual(expected);
 await expect(menu(page)).toBeVisible();await expect(page.locator('.graph-view-drag-preview')).toHaveCount(0);
 await expect(page.locator('.map-stage')).toHaveAttribute('data-view','free');
 await expect(page.locator('.detail-body h2')).toHaveText('Abertura criativa');
 expect(await page.evaluate(()=>JSON.parse(localStorage.getItem('repertorio-graph-view-order')!))).toEqual(expected);
 await page.keyboard.press('Escape');await toggle(page).click();await expect.poll(()=>order(page)).toEqual(expected);
 await page.reload();await toggle(page).click();await expect.poll(()=>order(page)).toEqual(expected);
 await row(page,'cosmos').click();await expect(menu(page)).toBeHidden();await expect(page.locator('.map-stage')).toHaveAttribute('data-view','cosmos');
 const workspace=await (await request.post('/api/workspaces',{data:{name:'Ordem das visualizações QA'}})).json();
 await page.goto('/?workspace='+workspace.id);await toggle(page).click();await expect.poll(()=>order(page)).toEqual(expected);
 await page.screenshot({path:'/tmp/repertorio-graph-order-qa/ordem-salva-desktop.png',animations:'disabled'});
 expect(errors).toEqual([]);
});

test('teclado reordena e o arraste pode ser cancelado por Escape ou fora do menu',async({page})=>{
 await page.goto('/?workspace=referencias&ref=deck');await toggle(page).click();
 await page.keyboard.press('Alt+ArrowUp');await expect.poll(()=>order(page)).toEqual(initial);
 await page.keyboard.press('Alt+ArrowDown');
 const expected=['grouped','free',...initial.slice(2)];
 await expect.poll(()=>order(page)).toEqual(expected);await expect(row(page,'free')).toBeFocused();
 await expect(page.getByRole('status')).toContainText('Mapa livre na posição 2 de 9.');
 await page.keyboard.press('End');await page.keyboard.press('Alt+ArrowDown');await expect.poll(()=>order(page)).toEqual(expected);
 await page.keyboard.press('Home');
 const source=(await row(page,'grouped').boundingBox())!,destination=(await row(page,'cosmos').boundingBox())!;
 await page.mouse.move(source.x+130,source.y+40);await page.mouse.down();await page.mouse.move(destination.x+130,destination.y+40,{steps:8});
 await expect(page.locator('.graph-view-drag-preview')).toBeVisible();await page.keyboard.press('Escape');await page.mouse.up();
 await expect(menu(page)).toBeVisible();await expect.poll(()=>order(page)).toEqual(expected);await expect(row(page,'grouped')).toBeFocused();
 await expect(page.locator('.detail-body h2')).toHaveText('Abertura criativa');
 await page.mouse.move(source.x+130,source.y+40);await page.mouse.down();await page.mouse.move(source.x-100,source.y+120,{steps:8});await page.mouse.up();
 await expect.poll(()=>order(page)).toEqual(expected);await expect(menu(page)).toBeVisible();
 await page.mouse.move(source.x+130,source.y+40);await page.mouse.down();await page.mouse.move(destination.x+130,destination.y+40,{steps:8});
 await expect(page.locator('.graph-view-drag-preview')).toBeVisible();await page.keyboard.press('Alt+ArrowDown');await page.mouse.up();
 await expect(page.locator('.graph-view-drag-preview')).toHaveCount(0);await expect.poll(()=>order(page)).toEqual(initial);
 await row(page,'metro').click();await expect(page.locator('.map-stage')).toHaveAttribute('data-view','metro');
});

test.describe('arraste por toque',()=>{
 test.use({hasTouch:true,isMobile:true,viewport:{width:390,height:740}});
 test('permite rolar os cards e arrastar pela alça até o fim com rolagem automática',async({page,context})=>{
  await page.goto('/?workspace=referencias');await toggle(page).tap();
  const session=await context.newCDPSession(page);
  const touch=async(type:'touchStart'|'touchMove'|'touchEnd',x=0,y=0)=>session.send('Input.dispatchTouchEvent',{type,touchPoints:type==='touchEnd'?[]:[{x,y}]});
  const first=(await row(page,'free').boundingBox())!;
  await touch('touchStart',first.x+180,first.y+first.height/2);
  for(let i=1;i<=6;i++)await touch('touchMove',first.x+180,first.y+first.height/2-i*16);
  await touch('touchEnd');
  await expect.poll(()=>menu(page).evaluate(element=>element.scrollTop)).toBeGreaterThan(30);
  await expect.poll(()=>order(page)).toEqual(initial);await expect(page.locator('.graph-view-drag-preview')).toHaveCount(0);
  await menu(page).evaluate(element=>{element.scrollTop=0;});
  const handle=(await row(page,'free').locator('.graph-view-grip').boundingBox())!,bounds=(await menu(page).boundingBox())!;
  await touch('touchStart',handle.x+handle.width/2,handle.y+handle.height/2);
  await touch('touchMove',handle.x+handle.width/2,bounds.y+bounds.height-10);
  await expect(page.locator('.graph-view-drag-preview')).toBeVisible();
  await expect.poll(()=>menu(page).evaluate(element=>element.scrollHeight-element.scrollTop-element.clientHeight)).toBeLessThan(2);
  await expect(row(page,'prism')).toHaveAttribute('data-drop-after','true');
  await page.screenshot({path:'/tmp/repertorio-graph-order-qa/arrastando-celular.png',animations:'disabled'});
  await touch('touchEnd');
  await expect.poll(()=>order(page)).toEqual([...initial.slice(1),'free']);
  await expect(menu(page)).toBeVisible();await expect(page.locator('.map-stage')).toHaveAttribute('data-view','free');
  await expect.poll(async()=>{const moved=(await row(page,'free').boundingBox())!,list=(await menu(page).boundingBox())!;return moved.y>=list.y&&moved.y+moved.height<=list.y+list.height+1;}).toBe(true);
  await page.screenshot({path:'/tmp/repertorio-graph-order-qa/ordem-salva-celular.png',animations:'disabled'});
 });
});
