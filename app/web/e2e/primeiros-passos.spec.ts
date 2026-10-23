import {test,expect} from '@playwright/test';

const evidence='/tmp/repertorio-primeiros-passos-qa';
// PNG de 4 x 4 pixels: o suficiente para o processamento gerar prévia e miniatura.
const png=Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAQAAAAECAIAAAAmkwkpAAAAE0lEQVR4nGNcZRzKAANMcBZeDgA9HQE65eCXkQAAAABJRU5ErkJggg==','base64');

test('adiciona arquivos pelo app num espaço vazio e a referência entra no mapa',async({page,request})=>{
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 const space=await (await request.post('/api/workspaces',{data:{name:'Primeiros passos QA'}})).json();
 await page.goto('/?workspace='+space.id);
 await expect(page.getByRole('heading',{name:'O repertório começa aqui.'})).toBeVisible();
 await page.screenshot({path:evidence+'/espaco-vazio.png'});
 const chooser=page.waitForEvent('filechooser');
 await page.locator('.empty').getByRole('button',{name:'Adicionar arquivos'}).click();
 await (await chooser).setFiles({name:'capa-da-campanha.png',mimeType:'image/png',buffer:png});
 await expect(page.locator('.toast')).toContainText('Arquivo enviado');
 await expect.poll(async()=>(await (await request.get('/api/graph?workspace_id='+space.id)).json()).items.length,{timeout:15000}).toBe(1);
 await expect(page.locator('.library-status')).toContainText('1 referência',{timeout:10000});
 const [item]=(await (await request.get('/api/graph?workspace_id='+space.id)).json()).items;
 expect(item.title).toBe('capa da campanha');
 expect(item.idea).toContain('Peça ao seu agente');
 // Arquivo corrompido: o processamento falha e o app avisa, apontando a Atividade.
 const again=page.waitForEvent('filechooser');
 await page.getByRole('button',{name:'Adicionar arquivos',exact:true}).click();
 await (await again).setFiles({name:'quebrada.png',mimeType:'image/png',buffer:Buffer.from('não é imagem')});
 await expect(page.locator('.toast.error')).toContainText('Não consegui processar um material',{timeout:15000});
 await expect(page.locator('.toast.error')).toContainText('Em Atividade');
 await page.screenshot({path:evidence+'/falha-no-processamento.png'});
 // Formato não aceito chega com explicação em português.
 const refused=await request.post('/api/workspaces/'+space.id+'/upload',{multipart:{files:{name:'notas.txt',mimeType:'text/plain',buffer:Buffer.from('texto')}}});
 expect(refused.status()).toBe(422);
 expect((await refused.json()).detail).toContain('Envie imagens, PDF, PowerPoint ou vídeo');
 expect(errors).toEqual([]);
});

test('serviço fora do ar mostra aviso e erros em português',async({page})=>{
 await page.route('**/api/events**',route=>route.abort());
 await page.route('**/api/references/**',route=>route.abort());
 await page.goto('/?workspace=referencias&ref=deck');
 await expect(page.getByText('Não consegui falar com o serviço do Repertório',{exact:false}).first()).toBeVisible();
 await expect(page.locator('.service-banner')).toContainText('não está respondendo',{timeout:8000});
 await page.screenshot({path:evidence+'/servico-fora.png'});
});

test('conectar agentes mostra comandos com o caminho completo e um por agente',async({page})=>{
 await page.goto('/?workspace=referencias');
 await page.getByRole('button',{name:'Conectar agentes',exact:true}).click();
 const dialog=page.getByRole('dialog');
 await expect(dialog).toContainText('/app/run.sh" connect "/caminho/do/projeto" --write-instructions');
 await expect(dialog.locator('pre').first()).toHaveText(/^"\/.+\/app\/run\.sh" connect/);
 await expect(dialog).toContainText('claude mcp add --transport http -s user repertorio http://127.0.0.1:8767/mcp');
 await page.screenshot({path:evidence+'/conectar-claude-code.png'});
 await dialog.getByRole('button',{name:'Cursor',exact:true}).click();
 await expect(dialog).toContainText('"mcpServers"');
 await dialog.getByRole('button',{name:'Claude Desktop',exact:true}).click();
 await expect(dialog).toContainText('mcp-remote');
 await expect(dialog).toContainText('Node.js');
 await dialog.getByRole('button',{name:'Codex',exact:true}).click();
 await expect(dialog).toContainText('codex mcp add repertorio --url http://127.0.0.1:8767/mcp');
 await page.setViewportSize({width:390,height:844});
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBeTruthy();
});

test('primeira visita com a biblioteca vazia abre o guia uma única vez',async({page})=>{
 await page.route('**/api/workspaces',route=>route.fulfill({json:[{id:'vazio',name:'Meu repertório',revision:1,deleted:null,references_count:0}]}));
 await page.goto('/');
 await expect(page.getByRole('heading',{name:'Suas referências, prontas para orientar a criação.'})).toBeVisible();
 expect(new URL(page.url()).searchParams.get('view')).toBe('guide');
 await page.goto('/');
 await expect(page.locator('.workspace-bar')).toBeVisible();
 expect(new URL(page.url()).searchParams.get('view')).toBeNull();
 await expect(page.getByRole('heading',{name:'Suas referências, prontas para orientar a criação.'})).toHaveCount(0);
});
