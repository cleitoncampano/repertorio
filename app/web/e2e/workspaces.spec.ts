import {test,expect} from '@playwright/test';

const evidence='/tmp/repertorio-workspaces-qa';

test('cria, renomeia, compartilha, exclui com confirmação e restaura espaços',async({page,request})=>{
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/?workspace=referencias');
 await page.getByRole('button',{name:'Espaços',exact:true}).click();
 await page.getByRole('textbox',{name:'Nome do novo espaço'}).fill('GrowMate QA');
 await page.getByRole('button',{name:'Criar espaço',exact:true}).click();
 await expect(page.getByRole('heading',{name:'O repertório começa aqui.'})).toBeVisible();
 const grow=new URL(page.url()).searchParams.get('workspace')!;
 expect((await (await request.get('/api/graph?workspace_id='+grow)).json()).items).toEqual([]);
 await page.screenshot({path:evidence+'/espaco-vazio.png'});
 await page.getByRole('button',{name:'Espaços',exact:true}).click();
 await page.getByRole('button',{name:'Renomear GrowMate QA',exact:true}).click();
 await page.getByRole('textbox',{name:'Novo nome do espaço'}).fill('GrowMate QA novo');
 await page.getByRole('button',{name:'Salvar nome',exact:true}).click();
 await expect(page.getByRole('button',{name:'Renomear GrowMate QA novo',exact:true})).toBeVisible();
 await page.screenshot({path:evidence+'/seletor-escuro.png'});
 await page.locator('.space-enter').filter({hasText:/^Referências/}).click();
 await page.goto('/?workspace=referencias&ref=deck');
 await expect(page.locator('.detail-body h2')).toHaveText('Abertura criativa');
 await page.getByRole('combobox',{name:'Espaço de destino'}).selectOption(grow);
 await page.getByRole('button',{name:'Adicionar ao espaço',exact:true}).click();
 await expect(page.locator('.reference-spaces p').first()).toContainText('GrowMate QA novo');
 await page.goto('/?workspace='+grow+'&ref=deck');
 await expect(page.locator('.detail-body h2')).toHaveText('Abertura criativa');
 await page.screenshot({path:evidence+'/referencia-compartilhada.png'});
 await page.getByRole('button',{name:'Excluir deste espaço',exact:true}).click();
 expect((await (await request.get('/api/references/deck?workspace_id=referencias')).json()).state).toBe('published');
  await page.getByRole('button',{name:'Lixeira',exact:true}).click();
  await expect(page.locator('.reference-card').filter({hasText:'Abertura criativa'})).toBeVisible();
 await page.getByRole('button',{name:'Espaços',exact:true}).click();
 const active=page.locator('.space-list').first().locator('.space-enter').filter({hasText:'GrowMate QA novo'});
 // Excluir pede confirmação; Cancelar mantém o espaço.
 await page.getByRole('button',{name:'Excluir espaço GrowMate QA novo',exact:true}).click();
 await expect(page.getByRole('group',{name:'Confirmar exclusão de GrowMate QA novo'})).toContainText('Excluir o espaço GrowMate QA novo? O que também está em outros espaços continua lá');
 await page.screenshot({path:evidence+'/confirmar-exclusao.png'});
 await page.getByRole('group',{name:'Confirmar exclusão de GrowMate QA novo'}).getByRole('button',{name:'Cancelar',exact:true}).click();
 await expect(active).toHaveCount(1);
 // Desfazer logo depois traz o espaço de volta, com a referência.
 await page.getByRole('button',{name:'Excluir espaço GrowMate QA novo',exact:true}).click();
 await page.getByRole('button',{name:'Excluir espaço',exact:true}).click();
 await expect(active).toHaveCount(0);
 await page.getByRole('status').getByRole('button',{name:'Desfazer',exact:true}).click();
 await expect(active).toHaveCount(1);
 expect((await (await request.get('/api/references/deck?workspace_id='+grow)).json()).state).toBe('trashed');
 // Mesmo sem usar o Desfazer, o espaço fica em Excluídos para restaurar.
 await page.getByRole('button',{name:'Excluir espaço GrowMate QA novo',exact:true}).click();
 await page.getByRole('button',{name:'Excluir espaço',exact:true}).click();
 await expect(active).toHaveCount(0);
 await expect(page.getByRole('region',{name:'Espaços excluídos'})).toContainText('GrowMate QA novo');
 await page.screenshot({path:evidence+'/espacos-excluidos.png'});
 await page.getByRole('button',{name:'Restaurar GrowMate QA novo',exact:true}).click();
 await expect(active).toHaveCount(1);
 await expect(page.getByRole('region',{name:'Espaços excluídos'})).toHaveCount(0);
  await page.locator('.space-enter').filter({hasText:/^Referências/}).click();
 await page.reload();
  expect(new URL(page.url()).searchParams.get('workspace')).toBe('referencias');
 await page.setViewportSize({width:390,height:844});
 await page.getByRole('button',{name:'Ativar modo claro',exact:true}).click();
 await page.getByRole('button',{name:'Espaços',exact:true}).click();
 await page.screenshot({path:evidence+'/seletor-mobile-claro.png'});
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBeTruthy();
 expect(errors).toEqual([]);
});

test('link da referência abre no espaço dela e mantém destino explícito',async({page,request})=>{
 const destination=await (await request.post('/api/workspaces',{data:{name:'cVortex QA'}})).json();
 const projects=await (await request.get('/api/projects')).json();
 const context=await (await request.post('/api/contexts',{data:{project_id:projects.find((p:any)=>p.name==='Marketing').id,demand:'Inspiração combinada',workspace_ids:['referencias',destination.id]}})).json();
 const op=await (await request.post('/api/references',{data:{context_id:context.id,target_workspace_ids:[destination.id],request_key:'combined-spaces-e2e',user_requested:true,files:['carrossel.png'],data:{title:'Exclusiva cVortex QA',description:'Só no destino',idea:'Referência exclusiva'}}})).json();
 await expect.poll(async()=>(await (await request.get('/api/operations/'+op.id)).json()).state).toBe('completed');
 expect((await request.get('/api/references/'+op.ref_id+'?workspace_id=referencias')).status()).toBe(404);
 // O link que o agente passa ao usuário leva o espaço da referência, mesmo numa demanda com dois espaços.
 const found=await (await request.post('/api/search',{data:{context_id:context.id,query:'Exclusiva cVortex QA'}})).json();
 const link=new URL(found.items.find((r:any)=>r.id===op.ref_id).url);
 expect(link.searchParams.get('workspace')).toBe(destination.id);
 await page.goto('/'+link.search);
 await expect(page.locator('.workspace-current')).toHaveText('cVortex QA');
 await expect(page.locator('.detail-body h2')).toHaveText('Exclusiva cVortex QA');
 await page.screenshot({path:evidence+'/link-outro-espaco.png'});
 await page.getByRole('button',{name:'Fechar detalhes',exact:true}).click();
 await page.getByRole('button',{name:'Espaços',exact:true}).click();
 await page.locator('.space-enter').filter({hasText:'cVortex QA'}).click();
 await expect(page.getByRole('textbox',{name:'Buscar inspiração'})).toHaveValue('');
 await page.reload();
 await expect(page.locator('.workspace-current')).toHaveText('cVortex QA');
});

test('move pela interface preservando outros vínculos',async({page,request})=>{
 const source=await (await request.post('/api/workspaces',{data:{name:'Origem movimento QA'}})).json();
 const target=await (await request.post('/api/workspaces',{data:{name:'Destino movimento QA'}})).json();
 const deck=await (await request.get('/api/references/deck?workspace_id=referencias')).json();
 expect((await request.post('/api/references/deck/workspaces',{data:{source_workspace_id:'referencias',target_workspace_ids:[source.id],expected_membership_revision:deck.membership_revision}})).ok()).toBeTruthy();
 await page.goto('/?workspace='+source.id+'&ref=deck');
 await expect(page.locator('.detail-body h2')).toHaveText('Abertura criativa');
 await page.getByRole('combobox',{name:'Espaço de destino'}).selectOption(target.id);
 await page.getByRole('button',{name:'Mover para o espaço',exact:true}).click();
 await expect(page.locator('.detail-panel')).toHaveCount(0);
 await expect(page.getByRole('heading',{name:'O repertório começa aqui.'})).toBeVisible();
 expect((await request.get('/api/references/deck?workspace_id='+source.id)).status()).toBe(404);
 expect((await (await request.get('/api/references/deck?workspace_id='+target.id)).json()).state).toBe('published');
 expect((await (await request.get('/api/references/deck?workspace_id=referencias')).json()).state).toBe('published');
});

test('lixeira seleciona uma, seleciona tudo e exclui de vez só neste espaço',async({page,request})=>{
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 const ws=await (await request.post('/api/workspaces',{data:{name:'Lixeira QA'}})).json();
 for(const id of ['deck','free']){
  const ref=await (await request.get('/api/references/'+id+'?workspace_id=referencias')).json();
  expect((await request.post('/api/references/'+id+'/workspaces',{data:{source_workspace_id:'referencias',target_workspace_ids:[ws.id],expected_membership_revision:ref.membership_revision}})).ok()).toBeTruthy();
  const here=await (await request.get('/api/references/'+id+'?workspace_id='+ws.id)).json();
  expect((await request.post('/api/references/'+id+'/state',{data:{workspace_id:ws.id,expected_membership_revision:here.membership_revision,state:'trashed'}})).ok()).toBeTruthy();
 }
 await page.goto('/?workspace='+ws.id+'&view=trashed');
 await expect(page.locator('.trash-item')).toHaveCount(2);
 const toolbar=page.locator('.trash-toolbar'),purge=toolbar.getByRole('button',{name:'Excluir definitivamente'});
 await expect(purge).toBeDisabled();
 await page.getByRole('checkbox',{name:'Selecionar Abertura criativa'}).check();
 await expect(toolbar).toContainText('1 selecionada');
 await page.getByRole('checkbox',{name:'Selecionar tudo',exact:true}).check();
 await expect(toolbar).toContainText('2 selecionadas');
 await page.getByRole('checkbox',{name:'Selecionar Textura verde'}).uncheck();
 await expect(toolbar).toContainText('1 selecionada');
 await purge.click();
 const dialog=page.getByRole('dialog');
 await expect(dialog).toContainText('Excluir 1 referência definitivamente?');
 await page.screenshot({path:evidence+'/lixeira-confirmar.png'});
 await dialog.getByRole('button',{name:'Excluir definitivamente'}).click();
 await expect(page.getByRole('status',{name:'Notificação'})).toContainText('Referência excluída definitivamente.');
 await expect(page.locator('.trash-item')).toHaveCount(1);
 await expect(page.locator('.trash-item')).toContainText('Textura verde');
 expect((await request.get('/api/references/deck?workspace_id='+ws.id)).status()).toBe(404);
 expect((await (await request.get('/api/references/deck?workspace_id=referencias')).json()).state).toBe('published');
 await page.getByRole('checkbox',{name:'Selecionar tudo',exact:true}).check();
 await toolbar.getByRole('button',{name:'Excluir definitivamente'}).click();
 await page.getByRole('dialog').getByRole('button',{name:'Excluir definitivamente'}).click();
 await expect(page.getByRole('heading',{name:'A lixeira está vazia.'})).toBeVisible();
 await page.screenshot({path:evidence+'/lixeira-vazia.png'});
 expect(errors).toEqual([]);
});

test('excluir todos os espaços permite criar e voltar a trabalhar',async({page,request})=>{
 const spaces=await (await request.get('/api/workspaces')).json();
 for(const space of spaces)expect((await request.post('/api/workspaces/'+space.id+'/state',{data:{deleted:true,expected_revision:space.revision}})).ok()).toBeTruthy();
 await page.goto('/');
 await expect(page.getByRole('heading',{name:'Seu repertório, em espaços.'})).toBeVisible();
 await page.getByRole('button',{name:'Ver espaços',exact:true}).click();
 await page.getByRole('textbox',{name:'Nome do novo espaço'}).fill('Novo começo QA');
 await page.getByRole('button',{name:'Criar espaço',exact:true}).click();
 await expect(page.getByRole('heading',{name:'O repertório começa aqui.'})).toBeVisible();
});
