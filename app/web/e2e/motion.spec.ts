import {test,expect} from '@playwright/test';

test('vídeos de motion tocam no mapa e na ficha, com prompt e quadros',async({page,request})=>{
 const spaces=await (await request.get('/api/workspaces')).json();
 const motion=spaces.find((s:{name:string})=>s.name==='Motion');
 await page.goto('/?workspace='+motion.id);
 await expect(page.locator('.map-surface')).toBeVisible();
 // De longe a capa é pequena e nada toca; ao aproximar, o vídeo aparece sobre ela.
 await page.evaluate(()=>(document.querySelector('.map-surface') as any)._cyreg.cy.zoom(.1));
 await expect(page.locator('.map-motion video')).toHaveCount(0);
 await page.evaluate(()=>{const c=(document.querySelector('.map-surface') as any)._cyreg.cy;c.zoom(2.2);c.center(c.getElementById('ref:motion-giro'));});
 const layer=page.locator('.map-motion video');
 await expect(layer).toHaveCount(1);
 await expect(layer).toHaveAttribute('src',/\/api\/assets\//);
 await expect(layer).toHaveClass(/playing/);
 const box=(await layer.boundingBox())!,node=await page.evaluate(()=>(document.querySelector('.map-surface') as any)._cyreg.cy.getElementById('ref:motion-giro').renderedBoundingBox());
 expect(Math.abs(box.x+box.width/2-(node.x1+node.x2)/2-(await page.locator('.map-surface').boundingBox())!.x)).toBeLessThan(3);
 await page.evaluate(()=>{const c=(document.querySelector('.map-surface') as any)._cyreg.cy;c.getElementById('ref:motion-giro').emit('tap');});
 const panel=page.locator('.detail-panel');
 await expect(panel.locator('video')).toHaveAttribute('src',/\/api\/assets\//);
 await expect(panel.getByRole('heading',{name:'Prompt original'})).toBeVisible();
 await expect(panel.locator('.motion-prompt')).toContainText('logo sting');
 await expect(panel.getByRole('heading',{name:'Decupagem'})).toBeVisible();
 await expect(panel.getByRole('link',{name:'Post do autor'})).toHaveAttribute('href','https://x.com/ana/status/1');
 await expect(panel.locator('.reference-meta')).toContainText('Vídeo · 0:04 · 16:9 · com som');
 await panel.getByRole('button',{name:'Ver quadros'}).click();
 await expect(page.getByRole('dialog')).toContainText('Quadros do vídeo');
 await page.keyboard.press('Escape');
 // Na lista, o cartão do vídeo também toca.
 await page.getByRole('button',{name:'Ver lista',exact:true}).click();
 const card=page.locator('.reference-card').filter({hasText:'Logo que gira'});
 await expect(card.locator('.card-image span')).toHaveText('Vídeo');
 await expect.poll(()=>card.locator('video').evaluate(v=>!(v as HTMLVideoElement).paused)).toBe(true);
});
