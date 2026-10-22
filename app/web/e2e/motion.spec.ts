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
 // Clicar num vídeo abre o player em tela grande, não a ficha ao lado.
 const cinema=page.locator('.cinema');
 await expect(cinema).toBeVisible();
 await expect(page.locator('.detail-panel')).toHaveCount(0);
 const player=cinema.locator('.cinema-stage video');
 await expect(player).toHaveAttribute('src',/\/api\/assets\//);
 await expect.poll(()=>player.evaluate(v=>!(v as HTMLVideoElement).paused)).toBe(true);
 await expect(cinema.getByRole('heading',{name:'Prompt original'})).toBeVisible();
 await expect(cinema.locator('pre')).toContainText('logo sting');
 await expect(cinema.getByRole('heading',{name:'Decupagem'})).toBeVisible();
 // Atalhos do YouTube: K pausa, T alterna o modo teatro, F tela cheia (ou janela inteira) e de volta.
 await page.keyboard.press('k');
 await expect.poll(()=>player.evaluate(v=>(v as HTMLVideoElement).paused)).toBe(true);
 await page.keyboard.press('t');
 await expect(cinema).toHaveClass(/theater/);
 await expect(cinema.getByRole('button',{name:'Modo padrão'})).toBeVisible();
 await page.keyboard.press('t');
 await expect(cinema).not.toHaveClass(/theater/);
 await page.keyboard.press('f');
 await expect.poll(()=>page.evaluate(()=>!!document.fullscreenElement||!!document.querySelector('.cinema.filled'))).toBe(true);
 await page.keyboard.press('f');
 await expect.poll(()=>page.evaluate(()=>!!document.fullscreenElement||!!document.querySelector('.cinema.filled'))).toBe(false);
 // A ficha completa continua disponível.
 await cinema.getByRole('button',{name:'Ficha completa'}).click();
 await expect(cinema).toHaveCount(0);
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
 await panel.getByRole('button',{name:'Assistir em tela grande'}).click();
 await expect(cinema).toBeVisible();
 await page.keyboard.press('Escape');
 await expect(cinema).toHaveCount(0);
 await expect(page.locator('.detail-panel')).toHaveCount(0);
 // Na lista, o cartão do vídeo também toca.
 await page.getByRole('button',{name:'Ver lista',exact:true}).click();
 const card=page.locator('.reference-card').filter({hasText:'Logo que gira'});
 await expect(card.locator('.card-image span')).toHaveText('Vídeo');
 await expect.poll(()=>card.locator('video').evaluate(v=>!(v as HTMLVideoElement).paused)).toBe(true);
});
