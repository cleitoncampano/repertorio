/* Motor de apresentação do Repertório.
   Estrutura: <div class="palco"> com várias <section class="slide">.
   - data-m="nome": elementos com o mesmo nome em slides seguidos se transformam um no outro (Morph).
   - data-trans no slide de destino: morph (padrão), corte, esmaecer, empurrar, subir, zoom, cortina, circulo.
   - data-dur no slide (ms) muda a duração da passagem.
   - data-passo="1..n": revela no ritmo da fala; data-passo="0" anima sozinho ao entrar. data-entra escolhe o jeito.
   - data-foco="grupo" + data-foco-em="n": no passo n este item acende e os outros do grupo apagam.
   - data-conta="87" (data-casas="1"): número sobe de 0 até o valor. data-barra / data-barra-v com style="--v:.8": barra cresce.
   Teclas: setas, espaço, PageUp/PageDown, Home/End, F (tela cheia), P (janela do apresentador). Clique avança. #5 na URL abre o slide 5; <a href="#5"> leva até ele.
   API: window.motor.ir(n), .avancar(), .voltar(), .total, .atual */
(() => {
  const palco = document.querySelector('.palco');
  if (!palco) return;
  const slides = [...palco.querySelectorAll(':scope > .slide')];
  const raiz = document.documentElement;
  const reduz = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let idx = 0, passo = 0, ocupado = false;

  const dims = () => {
    const cs = getComputedStyle(document.body);
    return [parseFloat(cs.getPropertyValue('--larg')) || 1920, parseFloat(cs.getPropertyValue('--alt')) || 1080];
  };
  const escalar = () => {
    const [w, h] = dims();
    palco.style.setProperty('--k', Math.min(innerWidth / w, innerHeight / h));
  };
  const [W, H] = dims();
  const pagina = document.createElement('style');
  pagina.textContent = `@page { size: ${W}px ${H}px; margin: 0 }`;
  document.head.append(pagina);

  // índice de escalonamento automático (--i) entre itens do mesmo passo
  slides.forEach((s) => {
    const cont = {};
    s.querySelectorAll('[data-passo]').forEach((e) => {
      const p = e.dataset.passo;
      cont[p] = (cont[p] || 0);
      if (!e.style.getPropertyValue('--i')) e.style.setProperty('--i', cont[p]);
      cont[p]++;
    });
    const nomes = [...s.querySelectorAll('[data-m]')].map((e) => e.dataset.m);
    const rep = nomes.filter((n, i) => nomes.indexOf(n) !== i);
    if (rep.length) console.warn('Slide', slides.indexOf(s) + 1, 'tem data-m repetido:', rep);
  });

  const passos = (s) => [...new Set([
    ...[...s.querySelectorAll('[data-passo]')].map((e) => +e.dataset.passo),
    ...[...s.querySelectorAll('[data-foco-em]')].map((e) => +e.dataset.focoEm),
  ].filter((n) => n > 0))].sort((a, b) => a - b);

  const fmt = (v, casas) => v.toLocaleString('pt-BR', { minimumFractionDigits: casas, maximumFractionDigits: casas });
  const contar = (e) => {
    const alvo = parseFloat(e.dataset.conta), casas = +(e.dataset.casas || 0), t0 = performance.now(), dur = +(e.dataset.durConta || 1400);
    if (reduz) { e.textContent = fmt(alvo, casas); return; }
    const tic = (t) => {
      const x = Math.min(1, (t - t0) / dur), ease = 1 - Math.pow(1 - x, 3);
      e.textContent = fmt(alvo * ease, casas);
      if (x < 1) requestAnimationFrame(tic);
    };
    requestAnimationFrame(tic);
  };
  const disparar = (e) => {
    if (e.matches('[data-conta]')) contar(e);
    e.querySelectorAll('[data-conta]').forEach(contar);
    e.querySelectorAll('[data-barra],[data-barra-v]').forEach((b) => b.classList.add('visto'));
  };

  const aplicarPasso = (s, p) => {
    s.querySelectorAll('[data-passo]').forEach((e) => {
      const n = +e.dataset.passo;
      if (n === 0) return;
      const antes = e.classList.contains('visto');
      e.classList.toggle('visto', n <= p);
      if (!antes && n <= p) disparar(e);
    });
    const grupos = {};
    s.querySelectorAll('[data-foco]').forEach((e) => (grupos[e.dataset.foco] ||= []).push(e));
    Object.values(grupos).forEach((itens) => {
      const ativos = itens.filter((e) => +e.dataset.focoEm <= p);
      const atual = ativos.sort((a, b) => +b.dataset.focoEm - +a.dataset.focoEm)[0];
      itens.forEach((e) => e.classList.toggle('focado-fora', !!atual && e !== atual));
    });
  };

  const aoEntrar = (s) => {
    s.querySelectorAll('[data-passo="0"]').forEach((e) => { e.classList.add('visto'); disparar(e); });
    s.querySelectorAll('[data-conta]').forEach((e) => { if (!e.closest('[data-passo]')) contar(e); });
    s.querySelectorAll('[data-barra],[data-barra-v]').forEach((e) => { if (!e.closest('[data-passo]')) requestAnimationFrame(() => e.classList.add('visto')); });
  };
  const aoSair = (s) => {
    s.querySelectorAll('.visto').forEach((e) => e.classList.remove('visto'));
    s.querySelectorAll('.focado-fora').forEach((e) => e.classList.remove('focado-fora'));
  };

  const nomear = (s, sim) => s.querySelectorAll('[data-m]').forEach((e) => {
    e.style.viewTransitionName = sim ? 'm-' + e.dataset.m.replace(/[^a-zA-Z0-9_-]/g, '_') : '';
  });

  const contador = document.createElement('div');
  contador.className = 'mt-contador';
  contador.hidden = document.body.dataset.contador === 'nao';
  document.body.append(contador);
  // janela do apresentador (tecla P): anotações do slide, próximo slide e cronômetro
  let janela = null, inicio = 0;
  const apresentador = () => {
    if (!janela || janela.closed) return;
    const s = slides[idx], prox = slides[idx + 1], ps = passos(s), doc = janela.document;
    const titulo = (el) => (el && (el.querySelector('h1,h2,.display') || el).textContent.replace(/\s+/g, ' ').trim().slice(0, 90)) || '';
    doc.getElementById('n').textContent = `slide ${idx + 1} de ${slides.length}` + (ps.length ? ` · clique ${ps.filter((x) => x <= passo).length} de ${ps.length}` : '');
    doc.getElementById('notas').innerHTML = (s.querySelector('.notas') || {}).innerHTML || '<i>sem anotações</i>';
    doc.getElementById('prox').textContent = prox ? 'Próximo: ' + titulo(prox) : 'Último slide';
  };
  const abrirApresentador = () => {
    janela = window.open('', 'apresentador', 'width=960,height=640');
    if (!janela) return;
    janela.document.open();
    janela.document.write('<!doctype html><meta charset="utf-8"><title>Apresentador</title><body style="margin:0;background:#111;color:#eee;font:30px/1.5 system-ui,sans-serif;padding:36px">' +
      '<div style="display:flex;justify-content:space-between;color:#999;font-size:22px"><span id="n"></span><span id="relogio">00:00</span></div>' +
      '<div id="notas" style="margin-top:26px"></div><div id="prox" style="margin-top:34px;color:#8a8a8a;font-size:22px"></div></body>');
    janela.document.close();
    inicio = Date.now();
    janela.addEventListener('keydown', teclas);
    apresentador();
  };
  setInterval(() => {
    if (!janela || janela.closed) return;
    const t = Math.floor((Date.now() - inicio) / 1000);
    janela.document.getElementById('relogio').textContent = String(Math.floor(t / 60)).padStart(2, '0') + ':' + String(t % 60).padStart(2, '0');
  }, 1000);

  const atualizar = () => {
    contador.textContent = `${idx + 1} / ${slides.length}`;
    history.replaceState(null, '', '#' + (idx + 1));
    apresentador();
  };

  async function ir(n, volta = false) {
    if (n < 0 || n >= slides.length || n === idx || ocupado) return;
    const de = slides[idx], para = slides[n];
    const trans = para.dataset.trans || document.body.dataset.trans || 'morph';
    const dur = para.dataset.dur || document.body.dataset.dur;
    if (dur) raiz.style.setProperty('--dur', dur + 'ms'); else raiz.style.removeProperty('--dur');
    raiz.dataset.trans = trans;
    if (volta) raiz.dataset.volta = ''; else delete raiz.dataset.volta;
    const morph = trans === 'morph';
    const trocar = () => {
      nomear(de, false);
      de.classList.remove('ativo');
      aoSair(de);
      para.classList.add('ativo');
      if (morph) nomear(para, true);
      idx = n;
      const ps = passos(para);
      passo = volta && ps.length ? ps[ps.length - 1] : 0;
      aplicarPasso(para, passo);
      atualizar();
    };
    if (!document.startViewTransition || reduz || trans === 'corte') {
      trocar(); nomear(para, false); aoEntrar(para); return;
    }
    ocupado = true;
    if (morph) nomear(de, true);
    try {
      const vt = document.startViewTransition(trocar);
      await vt.finished;
    } catch (e) { /* transição interrompida: segue */ }
    nomear(para, false);
    ocupado = false;
    aoEntrar(para);
  }

  function avancar() {
    const ps = passos(slides[idx]);
    const prox = ps.find((p) => p > passo);
    if (prox !== undefined) { passo = prox; aplicarPasso(slides[idx], passo); apresentador(); }
    else ir(idx + 1);
  }
  function voltar() {
    const ps = passos(slides[idx]).filter((p) => p < passo);
    if (passo > 0) { passo = ps.length ? ps[ps.length - 1] : 0; aplicarPasso(slides[idx], passo); apresentador(); }
    else ir(idx - 1, true);
  }

  function teclas(e) {
    if (e.target.closest && e.target.closest('input,textarea,[contenteditable]')) return;
    if (['ArrowRight', 'ArrowDown', 'PageDown', ' ', 'Enter'].includes(e.key)) { e.preventDefault(); avancar(); }
    else if (['ArrowLeft', 'ArrowUp', 'PageUp', 'Backspace'].includes(e.key)) { e.preventDefault(); voltar(); }
    else if (e.key === 'Home') ir(0, true);
    else if (e.key === 'End') ir(slides.length - 1);
    else if (e.key === 'f' || e.key === 'F') document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen();
    else if (e.key === 'p' || e.key === 'P') abrirApresentador();
  }
  addEventListener('keydown', teclas);
  addEventListener('click', (e) => { if (!e.target.closest('a,button,input,video,model-viewer')) avancar(); });
  let x0 = null;
  addEventListener('touchstart', (e) => { x0 = e.touches[0].clientX; }, { passive: true });
  addEventListener('touchend', (e) => {
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0; x0 = null;
    if (Math.abs(dx) > 40) dx < 0 ? avancar() : voltar();
  });
  addEventListener('resize', escalar);
  // links internos: <a href="#7"> leva ao slide 7 (sumário navegável, botões de menu)
  addEventListener('hashchange', () => {
    const n = parseInt(location.hash.slice(1), 10);
    if (n >= 1 && n <= slides.length && n - 1 !== idx) ir(n - 1, n - 1 < idx);
  });

  escalar();
  const ini = Math.min(slides.length, Math.max(1, parseInt(location.hash.slice(1), 10) || 1)) - 1;
  idx = ini;
  slides[idx].classList.add('ativo');
  aplicarPasso(slides[idx], 0);
  atualizar();
  requestAnimationFrame(() => aoEntrar(slides[idx]));

  window.motor = {
    ir: (n) => ir(n - 1, n - 1 < idx), avancar, voltar,
    get total() { return slides.length; }, get atual() { return idx + 1; }, get passo() { return passo; },
    get passos() { return passos(slides[idx]); },
    revelarTudo() { slides.forEach((s) => { s.querySelectorAll('[data-passo],[data-barra],[data-barra-v]').forEach((e) => e.classList.add('visto')); }); },
  };
})();
