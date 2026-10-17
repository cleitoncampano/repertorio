import {test,expect} from '@playwright/test';

test('explora, exclui e restaura sem editar arquivos',async({page})=>{
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/');
 await expect(page.getByRole('link',{name:'Repertório, início'})).toBeVisible();
 const canvas=await page.locator('.map-stage').boundingBox();
 const viewport=page.viewportSize()!;
 expect(canvas!.width*canvas!.height/(viewport.width*viewport.height)).toBeGreaterThan(.95);
 expect((await page.locator('.workspace-bar').boundingBox())!.height).toBeLessThanOrEqual(48);
 await expect(page.locator('canvas').first()).toBeVisible();
 await page.getByRole('textbox',{name:'Buscar inspiração'}).fill('Abertura');
 await page.getByRole('button',{name:'Explorar',exact:true}).click();
 await page.locator('.result-row').filter({hasText:'Abertura criativa'}).click();
 await expect(page.locator('.detail-body h2')).toHaveText('Abertura criativa');
 await page.getByRole('button',{name:'Excluir referência'}).click();
 await expect(page.getByRole('status',{name:'Notificação'})).toContainText('lixeira');
 await page.getByRole('button',{name:'Lixeira',exact:true}).click();
 await page.locator('.reference-card').filter({hasText:'Abertura criativa'}).click();
 await page.getByRole('button',{name:'Restaurar referência'}).click();
 await expect(page.getByRole('status',{name:'Notificação'})).toContainText('disponível');
 await page.getByRole('button',{name:'Mapa',exact:true}).click();
 await page.getByRole('button',{name:'Ver lista'}).click();
 await expect(page.locator('.reference-card').filter({hasText:'Abertura criativa'})).toBeVisible();
 expect(errors).toEqual([]);
});

test('agentes paralelos consultam e incorporam uma criação',async({request,page})=>{
 const projects=await (await request.get('/api/projects')).json();
 const sessions=await Promise.all(projects.map(async(p:any)=>(await (await request.post('/api/contexts',{data:{project_id:p.id,demand:'Demanda de '+p.name}})).json())));
 expect(sessions[0].id).not.toBe(sessions[1].id);
 const searches=await Promise.all(sessions.map(async(c:any)=>(await (await request.post('/api/search',{data:{query:'Abertura',context_id:c.id}})).json())));
 expect(searches.every(x=>x.total>0)).toBeTruthy();
 const marketing=sessions.find((c:any)=>projects.find((p:any)=>p.id===c.project_id)?.name==='Marketing');
 const op=await (await request.post('/api/references',{data:{context_id:marketing.id,request_key:'approved-e2e',user_requested:true,files:['carrossel.png'],data:{title:'Criação aprovada E2E',description:'Um novo carrossel',idea:'Conectar contraste e narrativa',techniques:['contraste'],intentions:['ABRIR'],source_reference_ids:['deck']}}})).json();
 await expect.poll(async()=>(await (await request.get('/api/operations/'+op.id)).json()).state).toBe('completed');
 await page.goto('/?ref='+op.ref_id);
 await expect(page.locator('.detail-body h2')).toHaveText('Criação aprovada E2E');
 await expect(page.locator('.detail-preview img')).toBeVisible();
 const pack=await (await request.post('/api/packs',{data:{context_id:sessions[0].id,title:'Nova inspiração',reference_ids:[op.ref_id]}})).json();
 expect(pack.references[0].id).toBe(op.ref_id);
});

test('sugestão aguarda revisão e configuração é acessível por teclado',async({request,page})=>{
 const project=(await (await request.get('/api/projects')).json()).find((p:any)=>p.name==='Marketing');
 const context=await (await request.post('/api/contexts',{data:{project_id:project.id,demand:'Sugerir nova referência'}})).json();
 const op=await (await request.post('/api/references',{data:{context_id:context.id,request_key:'pending-e2e',files:['carrossel.png'],data:{title:'Sugestão para revisar',description:'Uma ideia possível',idea:'Explorar outra leitura'}}})).json();
 await expect.poll(async()=>(await (await request.get('/api/operations/'+op.id)).json()).state).toBe('completed');
 await page.goto('/');
 await page.getByRole('button',{name:'Entradas',exact:true}).click();
 await page.locator('.reference-card').filter({hasText:'Sugestão para revisar'}).click();
 await page.getByRole('button',{name:'Publicar na biblioteca'}).click();
 await expect(page.getByRole('status',{name:'Notificação'})).toContainText('disponível');
 await page.getByRole('button',{name:'Conectar agentes',exact:true}).focus();
 await page.keyboard.press('Enter');
 await expect(page.getByRole('dialog')).toBeVisible();
 await page.keyboard.press('Escape');
 await expect(page.getByRole('dialog')).not.toBeVisible();
});

test('mobile sem transbordamento e navegação por link',async({page})=>{
 await page.setViewportSize({width:390,height:844});
 await page.emulateMedia({reducedMotion:'reduce'});
 await page.goto('/?ref=deck');
 await expect(page.locator('.detail-body h2')).toHaveText('Abertura criativa');
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBeTruthy();
 await page.getByRole('button',{name:'Fechar detalhes'}).click();
 await expect(page.locator('canvas').first()).toBeVisible();
 await page.getByRole('textbox',{name:'Buscar inspiração'}).fill('Abertura');
 await page.getByRole('button',{name:'Explorar',exact:true}).click();
 await expect(page.locator('.result-row').first()).toBeVisible();
 await page.getByRole('button',{name:'Limpar filtros',exact:true}).click();
 await expect(page.locator('.results-panel')).not.toBeVisible();
 await page.getByRole('button',{name:'Legenda',exact:true}).click();
 await expect(page.getByRole('button',{name:'Diferenciação',exact:true})).toBeVisible();
});

test('controles compactos preservam o mapa e a busca por teclado',async({page})=>{
 await page.goto('/');
 await expect(page.locator('canvas').first()).toBeVisible();
 const before=await page.locator('.map-stage').boundingBox();
 await page.keyboard.press('/');
 await expect(page.getByRole('textbox',{name:'Buscar inspiração'})).toBeFocused();
 await page.keyboard.press('Escape');
 await page.getByRole('button',{name:'Filtros',exact:true}).click();
 await expect(page.getByRole('region',{name:'Filtros do mapa'})).toBeVisible();
 expect(await page.locator('.map-stage').boundingBox()).toEqual(before);
 await page.getByLabel('Origem',{exact:true}).selectOption('pptreta');
 await page.getByRole('button',{name:'Ver resultados'}).click();
 await expect(page.getByRole('region',{name:'Filtros do mapa'})).not.toBeVisible();
 await expect(page.locator('.filter-summary')).toBeVisible();
 await page.getByRole('button',{name:'Limpar filtros',exact:true}).click();
 await expect(page.locator('.filter-summary')).not.toBeVisible();
 await page.getByRole('button',{name:'Ver todo o mapa'}).click();
 expect(await page.locator('.map-stage').boundingBox()).toEqual(before);
});

test('eixo abre explicação, técnica e referências conectadas',async({page})=>{
 await page.goto('/');
 await page.getByRole('button',{name:'Diferenciação',exact:true}).click();
 const panel=page.getByRole('complementary',{name:'Detalhes do eixo'});
 await expect(panel.getByRole('heading',{name:'Diferenciação',exact:true})).toBeVisible();
 await panel.locator('.technique-index button').first().click();
 const technique=page.getByRole('complementary',{name:'Detalhes da técnica'});
 await expect(technique).toBeVisible();
 await technique.locator('.result-row').filter({hasText:'Abertura criativa'}).click();
 await expect(page.locator('.detail-body h2')).toHaveText('Abertura criativa');
});

test('tema claro e escuro persistem sem mudar a área do mapa',async({page})=>{
 await page.goto('/');
 await expect(page.locator('canvas').first()).toBeVisible();
 const bounds=await page.locator('.map-stage').boundingBox();
 await page.getByRole('button',{name:'Ativar modo claro',exact:true}).click();
 await expect(page.locator('html')).toHaveAttribute('data-theme','light');
 await expect(page.locator('.map-stage')).toHaveCSS('background-color','rgb(247, 245, 240)');
 expect(await page.locator('.map-stage').boundingBox()).toEqual(bounds);
 await page.reload();
 await expect(page.locator('html')).toHaveAttribute('data-theme','light');
 await page.getByRole('button',{name:'Diferenciação',exact:true}).click();
 await expect(page.locator('.technique-index button').first()).toHaveCSS('color','rgb(40, 37, 32)');
 await page.setViewportSize({width:390,height:844});
 await page.getByRole('button',{name:'Ativar modo escuro',exact:true}).click();
 await expect(page.locator('html')).toHaveAttribute('data-theme','dark');
 await expect(page.locator('.map-stage')).toHaveCSS('background-color','rgb(18, 18, 18)');
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBeTruthy();
});

test('prévia abre em destaque, passa os slides, aproxima e volta ao painel',async({page})=>{
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/?ref=deck');
 await expect(page.locator('.detail-body h2')).toHaveText('Abertura criativa');
 await page.getByRole('button',{name:'Ver em destaque'}).click();
 const viewer=page.getByRole('dialog',{name:'Abertura criativa'});
 await expect(viewer).toBeVisible();
 await expect(viewer.locator('.viewer-bar span')).toHaveText('Visão geral · 1 de 2');
 const percent=viewer.getByRole('button',{name:'Ajustar à tela'});
 const stage=(await viewer.locator('.viewer-stage').boundingBox())!;
 await page.mouse.move(stage.x+stage.width/2,stage.y+stage.height/2);
 await page.mouse.wheel(0,-400);
 await expect(percent).not.toHaveText('100%');
 await page.keyboard.press('ArrowRight');
 await expect(viewer.locator('.viewer-bar span')).toHaveText('Slide 1 · 2 de 2');
 await expect(percent).toHaveText('100%');
 await expect(percent).toHaveText('100%');
 await viewer.locator('.viewer-stage img').click();
 await expect(percent).toHaveText('100%');
 const box=(await viewer.locator('.viewer-stage').boundingBox())!;
 await page.mouse.move(box.x+box.width/2,box.y+box.height/2);
 await page.mouse.wheel(0,-400);
 await expect(percent).not.toHaveText('100%');
 await viewer.locator('.viewer-stage').dblclick();
 await expect(percent).toHaveText('100%');
 await viewer.getByRole('button',{name:'Aumentar zoom'}).click();
 await expect(percent).toHaveText('150%');
 await percent.click();
 await expect(percent).toHaveText('100%');
 await page.keyboard.press('Escape');
 await expect(viewer).toBeHidden();
 await expect(page.locator('.detail-body h2')).toHaveText('Abertura criativa');
 await expect(page.getByRole('button',{name:'Ver em destaque'})).toBeFocused();
 expect(errors).toEqual([]);
});
