/* Confere os estados finais e cada clique usando o motor existente. */
const fs=require('node:fs'),path=require('node:path');
const {pathToFileURL}=require('node:url');
const {chromium}=require('../app/web/node_modules/@playwright/test');
const root=path.resolve(__dirname,'..'),dest=path.join(root,'_saida/palestra-cx-ia-codex');
const output=path.join(dest,'_ver');fs.mkdirSync(output,{recursive:true});
const check=()=>{
 const s=document.querySelector('.slide.ativo'),stage=document.querySelector('.palco').getBoundingClientRect(),warnings=[];
 s.querySelectorAll('*').forEach(el=>{
  if(el.closest('.notas,svg,.recurso'))return;
  const style=getComputedStyle(el);
  if(style.display==='none'||style.visibility==='hidden'||+style.opacity===0||el.closest('[data-passo]:not(.visto)'))return;
  const text=[...el.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent.trim()).join(' ').trim();
  if(!text)return;
  const rect=el.getBoundingClientRect();
  if(rect.left<stage.left-3||rect.top<stage.top-3||rect.right>stage.right+3||rect.bottom>stage.bottom+3)warnings.push({kind:'outside',text:text.slice(0,100)});
  if(parseFloat(style.fontSize)<24)warnings.push({kind:'small',text:text.slice(0,100),size:parseFloat(style.fontSize)});
 });
 const morph=[...s.querySelectorAll('[data-m]')].map(x=>x.dataset.m);
 if(morph.length!==new Set(morph).size)warnings.push({kind:'duplicate-morph'});
 return warnings;
};
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH});
 try{
  const page=await browser.newPage({viewport:{width:1920,height:1080},reducedMotion:'reduce'});
  const errors=[],failed=[];
  page.on('pageerror',e=>errors.push(e.message));
  page.on('requestfailed',r=>failed.push({url:r.url(),error:r.failure()?.errorText}));
  await page.goto(pathToFileURL(path.join(dest,'palestra.html')).href);
  await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(x=>x.decode()))});
  await page.addStyleTag({content:'*,*::before,*::after{animation-duration:1ms!important;animation-delay:0ms!important;transition-duration:1ms!important;transition-delay:0ms!important}'});
  const report={slides:[],steps:[],errors,failed,images:await page.evaluate(()=>[...document.images].every(x=>x.complete&&x.naturalWidth>0))};
  const total=await page.evaluate(()=>motor.total);
  for(let n=1;n<=total;n++){
   await page.evaluate(n=>motor.ir(n),n);
   await page.evaluate(()=>document.fonts.ready);
   const steps=await page.evaluate(()=>motor.passos);
   // Inclui o estado inicial mesmo quando só há revelações automáticas (passo zero).
   await page.waitForTimeout(80);
   if(steps.length||n===7){
    await page.screenshot({path:path.join(output,`passo-${String(n).padStart(2,'0')}-0.png`)});
    report.steps.push({slide:n,step:0,warnings:await page.evaluate(check)});
    for(let k=0;k<steps.length;k++){
     await page.evaluate(()=>motor.avancar());await page.waitForTimeout(80);
     const step=await page.evaluate(()=>motor.passo);
     if(await page.evaluate(()=>motor.atual)!==n)throw new Error('Clique pulou o slide '+n);
     await page.screenshot({path:path.join(output,`passo-${String(n).padStart(2,'0')}-${k+1}.png`)});
     report.steps.push({slide:n,step,warnings:await page.evaluate(check)});
    }
   }
   await page.evaluate(()=>motor.revelarTudo());await page.waitForTimeout(80);
   await page.evaluate(()=>document.fonts.ready);
   await page.screenshot({path:path.join(output,`slide-${String(n).padStart(2,'0')}.png`)});
   report.slides.push({slide:n,warnings:await page.evaluate(check)});
  }
  const [presenter]=await Promise.all([page.waitForEvent('popup'),page.keyboard.press('p')]);
  await presenter.waitForLoadState();
  report.presenter={opened:true,notes:await presenter.locator('#notas').innerText()};
  await presenter.close();
  report.fonts=await page.evaluate(()=>[...document.fonts].filter(x=>x.status==='loaded').map(x=>({family:x.family,style:x.style})));
  fs.writeFileSync(path.join(output,'checagem.json'),JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify({slides:report.slides.length,steps:report.steps.length,images:report.images,errors,failed,warnings:report.slides.filter(x=>x.warnings.length),stepWarnings:report.steps.filter(x=>x.warnings.length),presenter:report.presenter.opened}));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
