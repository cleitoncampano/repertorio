import {test,expect} from '@playwright/test';

test('guia explica o fluxo, copia o pedido e abre os recursos reais',async({page,context})=>{
 await context.grantPermissions(['clipboard-read','clipboard-write']);
 const errors:string[]=[];page.on('pageerror',error=>errors.push(error.message));
 await page.goto('/?workspace=pp-treta&view=guide');
 await expect(page.getByRole('heading',{name:'Suas referências, prontas para orientar a criação.'})).toBeVisible();
 await page.getByRole('button',{name:'Copiar exemplo de pedido',exact:true}).click();
 const copied=await page.evaluate(()=>navigator.clipboard.readText());
 expect(copied).toContain('workspace_id: pp-treta');
 expect(copied).toContain('Espere minha revisão antes de criar.');
 expect(copied).toContain('no projeto desta produção');
 await page.getByRole('button',{name:'Conectar meu agente',exact:true}).click();
 await expect(page.getByRole('dialog')).toContainText('Cadastre a pasta do projeto');
 await page.keyboard.press('Escape');
 await page.getByRole('button',{name:'Contraste de tamanho',exact:true}).click();
 await expect(page.getByRole('textbox',{name:'Buscar inspiração'})).toHaveValue('escala');
 await page.goBack();
 await expect(page.getByRole('heading',{name:'Suas referências, prontas para orientar a criação.'})).toBeVisible();
 await page.getByRole('button',{name:'Já sabe o que quer criar?',exact:false}).click();
 await expect(page.getByRole('heading',{name:'O que vamos criar?'})).toBeVisible();
 expect(errors).toEqual([]);
});

test('guia sem espaço no celular, tema claro e conexão Windows',async({page})=>{
 let graphRequests=0;page.on('request',request=>{if(request.url().includes('/api/graph'))graphRequests++;});
 await page.route('**/api/health',route=>route.fulfill({json:{status:'ok',platform:'win32',demo:false}}));
 await page.setViewportSize({width:390,height:844});
 await page.goto('/?workspace=&view=guide');
 await page.getByRole('button',{name:'Ativar modo claro',exact:true}).click();
 await expect(page.locator('.spaces-home')).toHaveCount(0);
 expect(graphRequests).toBe(0);
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth&&document.querySelector('.product-page')!.scrollWidth<=innerWidth)).toBeTruthy();
 await page.screenshot({path:'/tmp/repertorio-produto-qa/guia-mobile-claro.png'});
 await page.locator('summary').filter({hasText:'Como uso no Mac e no Windows?'}).click();
 await expect(page.locator('details[open]')).toContainText('mesma biblioteca local');
 await page.getByRole('button',{name:'Conectar meu agente',exact:true}).scrollIntoViewIfNeeded();
 await page.getByRole('button',{name:'Conectar meu agente',exact:true}).click();
 await expect(page.getByRole('dialog')).toContainText('powershell -NoProfile');
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBeTruthy();
});
