import {test,expect} from '@playwright/test';

test('imagens abrem em tela grande, trocam de referência e o mapa se organiza por história, recurso ou formato',async({page})=>{
 await page.goto('/?workspace=referencias');
 await expect(page.locator('.map-surface')).toBeVisible();
 await page.evaluate(()=>(document.querySelector('.map-surface') as any)._cyreg.cy.getElementById('ref:deck').emit('tap'));
 const cinema=page.locator('.cinema');
 await expect(cinema.locator('.cinema-picture')).toBeVisible();
 await expect(cinema.locator('.cinema-info h2')).toHaveText('Abertura criativa');
 await expect(cinema.locator('.cinema-meta')).toContainText('Apresentação');
 await expect(cinema.getByRole('heading',{name:'Ideia transferível'})).toBeVisible();
 await expect(page.locator('.detail-panel')).toHaveCount(0);
 await page.keyboard.press('t');
 await expect(cinema).toHaveClass(/theater/);
 await page.keyboard.press('t');
 await page.keyboard.press('Escape');
 await expect(cinema).toHaveCount(0);
 // Na lista, as setas passam de uma referência para a próxima sem fechar.
 await page.getByRole('button',{name:'Ver lista',exact:true}).click();
 await page.locator('.reference-card').filter({hasText:'Abertura criativa'}).first().click();
 await expect(cinema.locator('.cinema-info h2')).toHaveText('Abertura criativa');
 const first=await cinema.locator('.cinema-count').textContent();
 await page.keyboard.press('ArrowRight');
 await expect(cinema.locator('.cinema-count')).not.toHaveText(first||'');
 await expect(cinema.locator('.cinema-info h2')).not.toHaveText('Abertura criativa');
 await page.keyboard.press('Escape');
 await page.getByRole('button',{name:'Ver mapa',exact:true}).click();
 // Três organizações, guardadas por espaço: história (padrão das imagens), recurso visual e formato.
 const legend=page.locator('#map-legend');
 await expect(legend.getByRole('button',{name:'História',exact:true})).toHaveAttribute('aria-pressed','true');
 await expect(legend.getByRole('button',{name:'Abrir',exact:true})).toBeVisible();
 await legend.getByRole('button',{name:'Recurso visual',exact:true}).click();
 await expect(legend.getByRole('button',{name:'Cor e contraste'})).toBeVisible();
 await legend.getByRole('button',{name:'Formato',exact:true}).click();
 await expect(legend.getByRole('button',{name:'Horizontal 16:9'})).toBeVisible();
 await expect.poll(()=>page.evaluate(()=>!!(document.querySelector('.map-surface') as any)._cyreg.cy.getElementById('op:horizontal').length)).toBe(true);
 await page.reload();
 await expect(page.locator('#map-legend').getByRole('button',{name:'Horizontal 16:9'})).toBeVisible();
 await page.locator('#map-legend').getByRole('button',{name:'História',exact:true}).click();
 await page.locator('#map-legend').getByRole('button',{name:'Abrir',exact:true}).click();
 const moment=page.getByRole('complementary',{name:'Detalhes do momento'});
 await expect(moment).toContainText('MOMENTO DA HISTÓRIA');
 await moment.locator('.technique-index button').first().click();
 await expect(page.getByRole('complementary',{name:'Detalhes do papel'}).locator('.result-row').filter({hasText:'Abertura criativa'})).toBeVisible();
});
