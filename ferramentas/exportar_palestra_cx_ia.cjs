/* Exporta o PDF e verifica a entrega offline e as transições do motor. */
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require('../repertorio/web/node_modules/@playwright/test');
const dest = path.resolve(__dirname, '../_saida/palestra-cx-ia-codex');
const output = path.join(dest, '_ver');
const source = pathToFileURL(path.join(dest, 'palestra.html')).href;
const ready = page => page.evaluate(async () => {
  await document.fonts.ready;
  await Promise.all([...document.images].map(image => image.decode()));
});

async function exportPDF(browser) {
  const page = await browser.newPage({viewport: {width: 1920, height: 1080}, reducedMotion: 'reduce'});
  await page.emulateMedia({media: 'print'});
  await page.goto(source);
  await ready(page);
  await page.pdf({path: path.join(dest, 'palestra.pdf'), width: '1920px', height: '1080px',
    printBackground: true, margin: {top: 0, bottom: 0, left: 0, right: 0}});
  console.log('PDF exportado: ' + path.join(dest, 'palestra.pdf'));
  await page.close();
}

async function checkTransitions(browser) {
  const page = await browser.newPage({viewport: {width: 1920, height: 1080}, reducedMotion: 'no-preference'});
  const errors = [], transitions = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto(source);
  await ready(page);
  await page.evaluate(() => {
    window.__transitionErrors = [];
    const start = document.startViewTransition.bind(document);
    document.startViewTransition = callback => {
      const transition = start(callback);
      transition.ready.catch(error => window.__transitionErrors.push(error.message));
      window.__transition = transition;
      return transition;
    };
  });
  for (let n = 2; n <= 24; n++) {
    await page.evaluate(() => motor.revelarTudo());
    await page.waitForTimeout(160);
    await page.evaluate(n => { window.__moving = motor.ir(n); }, n);
    await page.waitForTimeout(350);
    await page.screenshot({path: path.join(output, `trans-${String(n).padStart(2, '0')}.png`)});
    await page.evaluate(() => window.__moving);
    const current = await page.evaluate(() => motor.atual);
    if (current !== n) throw new Error(`Transição ${n}: slide atual ${current}`);
    transitions.push({to: n, type: await page.locator('html').getAttribute('data-trans')});
  }
  await page.keyboard.press('Home');
  await page.waitForFunction(() => motor.atual === 1);
  await page.waitForTimeout(1100);
  await page.keyboard.press('PageDown');
  await page.waitForFunction(() => motor.atual === 2);
  await page.waitForTimeout(1100);
  await page.keyboard.press('End');
  await page.waitForFunction(() => motor.atual === 24);
  await page.waitForTimeout(1100);
  await page.keyboard.press('f');
  await page.waitForFunction(() => Boolean(document.fullscreenElement));
  await page.keyboard.press('f');
  await page.waitForFunction(() => !document.fullscreenElement);
  const report = {transitions, errors, transitionErrors: await page.evaluate(() => window.__transitionErrors),
    keyboard: {home: true, pageDown: true, end: true, fullscreen: true}};
  fs.writeFileSync(path.join(output, 'transicoes.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report));
  await page.close();
}

async function checkOffline(browser) {
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'palestra-offline-'));
  try {
    const isolated = path.join(temporary, 'apresentacao.html');
    fs.copyFileSync(path.join(dest, 'palestra-arquivo-unico.html'), isolated);
    const page = await browser.newPage({viewport: {width: 1920, height: 1080}, reducedMotion: 'reduce'});
    const errors = [], requests = [], failed = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('requestfailed', request => failed.push(request.url()));
    await page.route('**/*', route => {
      const request = route.request();
      if (request.isNavigationRequest() && request.url() === pathToFileURL(isolated).href) return route.continue();
      requests.push(request.url());
      return route.abort();
    });
    await page.goto(pathToFileURL(isolated).href);
    await ready(page);
    await page.addStyleTag({content: '*,*::before,*::after{animation-duration:1ms!important;animation-delay:0ms!important;transition-duration:1ms!important;transition-delay:0ms!important}'});
    const screenshots = [7, 9, 18, 19, 22];
    for (let n = 1; n <= 24; n++) {
      await page.evaluate(n => motor.ir(n), n);
      const steps = await page.evaluate(() => motor.passos.length);
      for (let k = 0; k < steps; k++) await page.evaluate(() => motor.avancar());
      await page.evaluate(() => motor.revelarTudo());
      await page.waitForTimeout(80);
      if (screenshots.includes(n)) await page.screenshot({path: path.join(output, `offline-${n}.png`)});
    }
    const report = await page.evaluate(() => ({slides: motor.total,
      images: [...document.images].every(image => image.complete && image.naturalWidth > 0),
      embeddedImages: [...document.images].every(image => image.src.startsWith('data:')),
      externalDependencies: document.querySelectorAll('link[rel="stylesheet"],script[src]').length}));
    Object.assign(report, {errors, requests, failed});
    const [presenter] = await Promise.all([page.waitForEvent('popup'), page.keyboard.press('p')]);
    await presenter.waitForLoadState();
    report.presenter = Boolean(await presenter.locator('#notas').innerText());
    await presenter.close();
    fs.writeFileSync(path.join(output, 'offline.json'), JSON.stringify(report, null, 2) + '\n');
    console.log(JSON.stringify(report));
    if (errors.length || requests.length || failed.length || !report.images || !report.embeddedImages || report.externalDependencies) {
      throw new Error('A entrega offline não passou pela verificação');
    }
    await page.close();
  } finally { fs.rmSync(temporary, {recursive: true, force: true}); }
}

(async () => {
  fs.mkdirSync(output, {recursive: true});
  const browser = await chromium.launch({executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH});
  try {
    if (process.argv.includes('--pdf')) await exportPDF(browser);
    else if (process.argv.includes('--offline')) await checkOffline(browser);
    else { await checkTransitions(browser); await checkOffline(browser); }
  } finally { await browser.close(); }
})().catch(error => {console.error(error); process.exit(1);});
