/* Congela a arte já existente em HTML sem dependências externas.
   Executa somente os carrosséis copiados, nunca altera a origem. */
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL, fileURLToPath} = require('node:url');
const {chromium} = require('../app/web/node_modules/@playwright/test');
const root = path.resolve(__dirname, '..');
const manifestPath = path.join(root, 'docs/REPERTORIO-GROWMATE-LIVROS.json');
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const mime = {'.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.webp':'image/webp','.woff2':'font/woff2','.svg':'image/svg+xml'};
const cache = new Map();
function uri(file) {
  if (!cache.has(file)) cache.set(file, `data:${mime[path.extname(file)] || 'application/octet-stream'};base64,${fs.readFileSync(file).toString('base64')}`);
  return cache.get(file);
}
function inlineCSS(css, base) {
  return css.replace(/url\((["']?)([^)"']+)\1\)/g, (all, quote, url) => {
    if (/^(data:|#)/.test(url)) return all;
    if (/^https?:/.test(url)) throw new Error('Dependência remota em CSS: ' + url);
    const file = url.startsWith('file:') ? fileURLToPath(url) : path.resolve(base, url);
    return `url("${uri(file)}")`;
  });
}
(async () => {
  const browser = await chromium.launch({headless:true,
    ...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ? {executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH} : {})});
  const page = await browser.newPage({viewport:{width:1440,height:1100},deviceScaleFactor:1});
  const report = [];
  for (const entry of manifest.entries) {
    const folder = path.join(root,entry.path), source = path.join(folder,'carrossel.html');
    const errors = [];
    const onError = e => errors.push(e.message);
    page.on('pageerror',onError);
    await page.goto(pathToFileURL(source).href);
    await page.evaluate(() => document.fonts.ready);
    const initial = await page.evaluate(() => ({
      count:document.querySelectorAll('.sl').length,
      images:[...document.images].map(x => ({src:x.src,loaded:x.complete&&x.naturalWidth>0})),
      fonts:['Inter Tight','Fraunces','JetBrains Mono'].map(x=>({name:x,loaded:document.fonts.check(`20px "${x}"`)}))
    }));
    if (errors.length || initial.count!==entry.slides || initial.images.some(x=>!x.loaded))
      throw new Error(entry.folder + ': ' + JSON.stringify({errors,...initial}));
    const styles = await page.evaluate(() => [...document.querySelectorAll('style,link[rel="stylesheet"]')].map(x=>({
      tag:x.tagName,text:x.textContent,href:x.href||''
    })));
    const inlinedStyles = styles.map(x => x.tag==='LINK'
      ? inlineCSS(fs.readFileSync(fileURLToPath(x.href),'utf8'),path.dirname(fileURLToPath(x.href)))
      : inlineCSS(x.text,folder));
    const replacements = Object.fromEntries(initial.images.map(x=>[x.src,uri(fileURLToPath(x.src))]));
    await page.evaluate(({inlinedStyles,replacements})=>{
      [...document.querySelectorAll('style,link[rel="stylesheet"]')].forEach((x,i)=>{
        const s=document.createElement('style');s.textContent=inlinedStyles[i];x.replaceWith(s);
      });
      [...document.images].forEach(x=>{x.src=replacements[x.src];x.removeAttribute('srcset')});
      document.querySelectorAll('script,base').forEach(x=>x.remove());
    },{inlinedStyles,replacements});
    const out=path.join(folder,'repertorio-autocontido.html');
    fs.writeFileSync(out,'<!doctype html>\n'+await page.evaluate(()=>document.documentElement.outerHTML));
    // Sem acesso à rede ou às dependências de arquivo: o documento tem que se bastar.
    await page.route('**/*', route=>route.request().isNavigationRequest()?route.continue():route.abort());
    await page.goto(pathToFileURL(out).href);
    await page.evaluate(()=>document.fonts.ready);
    const frozen=await page.evaluate(()=>({
      count:document.querySelectorAll('.sl').length,
      images:[...document.images].every(x=>x.complete&&x.naturalWidth>0&&x.src.startsWith('data:')),
      fonts:document.fonts.size,
      external:document.querySelectorAll('script,link[rel="stylesheet"]').length
    }));
    if(frozen.count!==entry.slides||!frozen.images||frozen.external||frozen.fonts<3)
      throw new Error('HTML autocontido inválido: '+entry.folder+JSON.stringify(frozen));
    await page.unroute('**/*');
    page.off('pageerror',onError);
    report.push({folder:entry.folder,source:initial,frozen,bytes:fs.statSync(out).size});
    console.log(entry.folder,entry.slides+' lâminas',Math.round(fs.statSync(out).size/1024)+' KB');
  }
  const kit=path.join(root,manifest.destination,'series/livros-kit/repertorio-componentes.html');
  await page.setViewportSize({width:1400,height:1800});
  await page.goto(pathToFileURL(kit).href);
  await page.screenshot({path:kit.replace('.html','.png'),fullPage:true});
  fs.writeFileSync(path.join(root,manifest.destination,'verificacao-html.json'),JSON.stringify(report,null,2)+'\n');
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
