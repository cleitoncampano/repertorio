import {test,expect} from '@playwright/test';

const evidence='/tmp/repertorio-repos-qa';

test('repositórios abaixo de Skills, com link do GitHub e busca',async({page})=>{
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/');
 const rail=page.getByRole('navigation',{name:'Navegação principal'});
 const labels=await rail.locator('.nav-item').evaluateAll(items=>items.map(item=>item.getAttribute('aria-label')));
 expect(labels.indexOf('Repositórios')).toBe(labels.indexOf('Skills')+1);
 await rail.getByRole('button',{name:'Repositórios',exact:true}).click();
 await expect(rail.getByRole('button',{name:'Repositórios',exact:true})).toHaveAttribute('aria-current','page');
 await expect(page).toHaveURL(/view=repos/);
 await expect(page.locator('.skill-card h2')).toHaveText(['Engram','RTK','HyperFrames']);
 await expect(page.getByRole('link',{name:/github\.com\/Gentleman-Programming\/engram/})).toHaveAttribute('href','https://github.com/Gentleman-Programming/engram');
 await expect(page.getByRole('link',{name:/github\.com\/Gentleman-Programming\/engram/})).toHaveAttribute('target','_blank');
 await page.screenshot({path:evidence+'/repositorios-escuro.png',animations:'disabled'});
 await page.getByRole('textbox',{name:'Buscar repositórios'}).fill('memoria');
 await expect(page.locator('.skill-card h2')).toHaveText(['Engram']);
 await page.getByRole('textbox',{name:'Buscar repositórios'}).fill('termo inexistente');
 await page.getByRole('button',{name:'Ver todos os repositórios',exact:true}).click();
 await expect(page.locator('.skill-card')).toHaveCount(3);
 await page.reload();
 await expect(page.getByRole('heading',{name:'Ferramentas que trabalham junto.'})).toBeVisible();
 expect(errors).toEqual([]);
});

test('repositórios no celular em tema claro sem transbordamento',async({page})=>{
 await page.setViewportSize({width:320,height:740});
 await page.goto('/?workspace=&view=repos');
 await expect(page.locator('.skill-card')).toHaveCount(3);
 await page.getByRole('button',{name:'Ativar modo claro',exact:true}).click();
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBeTruthy();
 await page.screenshot({path:evidence+'/repositorios-mobile-claro.png',animations:'disabled'});
 await page.goto('/?view=pending');
 await expect(page.getByRole('button',{name:'Sugestões',exact:true})).toBeVisible();
 const rail=await page.getByRole('navigation',{name:'Navegação principal'}).boundingBox();
 expect(rail!.x+rail!.width).toBeLessThanOrEqual(320);
});
