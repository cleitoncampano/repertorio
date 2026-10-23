import {test,expect} from '@playwright/test';

test('imagens abrem em tela grande, trocam de referência e o mapa se organiza por formato',async({page})=>{
 await page.goto('/?workspace=pp-treta');
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
 // Organizar por formato troca os eixos pelos formatos de tela e fica guardado no espaço.
 const legend=page.locator('#map-legend');
 await expect(legend.getByRole('button',{name:'Diferenciação'})).toBeVisible();
 await legend.getByRole('button',{name:'Formato',exact:true}).click();
 await expect(legend.getByRole('button',{name:'Horizontal 16:9'})).toBeVisible();
 await expect.poll(()=>page.evaluate(()=>!!(document.querySelector('.map-surface') as any)._cyreg.cy.getElementById('op:horizontal').length)).toBe(true);
 await page.reload();
 await expect(page.locator('#map-legend').getByRole('button',{name:'Horizontal 16:9'})).toBeVisible();
 await page.locator('#map-legend').getByRole('button',{name:'Eixos do olhar'}).click();
 await expect(page.locator('#map-legend').getByRole('button',{name:'Diferenciação'})).toBeVisible();
});
