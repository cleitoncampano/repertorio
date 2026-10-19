import {test,expect} from '@playwright/test';

test('agrupa gravações da câmera e preserva o último movimento ao recarregar',async({page})=>{
 await page.goto('/?workspace=pp-treta');await expect(page.locator('canvas').first()).toBeVisible();
 const moved=await page.evaluate(()=>{
  const original=Storage.prototype.setItem;
  (window as any).cameraWrites=0;
  Storage.prototype.setItem=function(key,value){if(this===sessionStorage&&key.startsWith('repertorio-camera-'))(window as any).cameraWrites++;return original.call(this,key,value);};
  const c=(document.querySelector('.map-surface') as any)._cyreg.cy;
  c.viewport({zoom:.6,pan:{x:80,y:90}});
  for(let index=0;index<200;index++)c.panBy({x:1,y:0});
  return {zoom:c.zoom(),pan:c.pan(),writes:(window as any).cameraWrites};
 });
 expect(moved.writes).toBe(0);
 await expect.poll(()=>page.evaluate(()=>JSON.parse(sessionStorage.getItem('repertorio-camera-v3:pp-treta')||'null'))).toEqual({zoom:moved.zoom,pan:moved.pan});
 expect(await page.evaluate(()=>(window as any).cameraWrites)).toBe(1);
 await expect(page.locator('.map-controls span')).toHaveText('60%');
 // Recarrega antes do prazo de gravação: pagehide precisa preservar a posição final.
 await page.evaluate(()=>{(document.querySelector('.map-surface') as any)._cyreg.cy.viewport({zoom:.8,pan:{x:350,y:200}});});
 await page.reload();await expect(page.locator('canvas').first()).toBeVisible();
 await expect.poll(()=>page.evaluate(()=>{const c=(document.querySelector('.map-surface') as any)._cyreg.cy;return {zoom:c.zoom(),pan:c.pan()};})).toEqual({zoom:.8,pan:{x:350,y:200}});
});
