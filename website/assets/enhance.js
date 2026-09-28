/* enhance.js — progressive interaction layer for atuliwale.com
   Runs after the prerendered React pages have hydrated. Everything here is
   additive: if this file fails to load, every page still works as before. */
(function () {
  'use strict';

  var doc = document;
  var root = doc.documentElement;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var isMac = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent);

  var PAGES = [
    { t: 'Home', d: 'Data & AI for construction', h: 'index.html', k: 'start overview' },
    { t: 'Approach', d: 'How I work across AEC decisions', h: 'approach.html', k: 'method process ba pm' },
    { t: 'Projects', d: 'All 15 projects, filterable', h: 'projects.html', k: 'portfolio work ml' },
    { t: 'Experience', d: 'Career, ERP modules, education & tools', h: 'experience.html', k: 'cv resume career skills' },
    { t: 'Digital transformation', d: 'Six representative ERP engagements', h: 'digital-transformation.html', k: 'erp case studies' },
    { t: 'Insights', d: 'Field notes on process, data and AI', h: 'blog.html', k: 'blog articles writing' },
    { t: 'Books', d: 'The AEC knowledge series', h: 'ebooks.html', k: 'ebooks guides' },
    { t: 'Contact', d: 'Start a conversation', h: 'contact.html', k: 'email hire message' }
  ];
  var SECTIONS = [
    { t: 'How I help', d: 'Home · four capabilities', h: 'index.html#how-i-help' },
    { t: 'How everything connects', d: 'Home · interactive decision flow', h: 'index.html#decision-flow' },
    { t: 'Selected work', d: 'Home · six highlighted projects', h: 'index.html#selected-work' },
    { t: 'Why ERP adoption fails on site', d: 'Insight · digital adoption', h: 'insight-erp-adoption.html' },
    { t: 'Turning procurement data into project intelligence', d: 'Insight · procurement', h: 'insight-procurement-data.html' },
    { t: 'Where AI genuinely helps in AEC operations', d: 'Insight · AI & automation', h: 'insight-aec-ai.html' }
  ];
  var GH = 'https://github.com/AtulIwale/Portfolio/tree/main/projects/';
  var LIVE = 'https://atuliwale.github.io/Portfolio/projects/';
  var PROJECTS = [
    ['14-construction-safety-intelligence', 'Construction Safety Intelligence', 'Real data · ML + LLM on 19,021 OSHA reports', 1],
    ['15-nyc-permit-approval-forecast', 'NYC Permit Approval Forecast', 'Real data · survival analysis on 29,123 filings', 1],
    ['13-cost-plan-estimation', 'Cost Plan Estimation (ML)', 'Flagship · 6.6% error at feasibility stage', 1],
    ['05-contract-lifecycle-intelligence', 'Contract Lifecycle Intelligence', 'Flagship · catches 95% of high-risk clauses', 1],
    ['03-site-progress-schedule-control', 'Site Progress & Schedule Control', 'Flagship · SPI/CPI and submittal ageing', 1],
    ['01-cost-margin-intelligence', 'Project Cost & Margin Intelligence', 'Flagship · XGBoost cost forecast, 2.8% error', 1],
    ['04-construction-payroll', 'Construction Payroll', 'Flagship · anomaly detection on site payroll', 1],
    ['02-erp-intelligence-copilot', 'Construction ERP Intelligence Copilot', 'Flagship · AI assistant, 94.8% correct', 1],
    ['06-procurement-subcontracting', 'Procurement & Subcontracting', 'Coverage · documented on GitHub', 0],
    ['07-accounts-receivable-payable', 'Accounts Receivable & Payable', 'Coverage · documented on GitHub', 0],
    ['08-inventory-warehouse-management', 'Inventory & Warehouse Management', 'Coverage · documented on GitHub', 0],
    ['09-construction-assets', 'Construction Assets (Fixed & Movable)', 'Coverage · ML app', 0],
    ['11-real-estate-sales', 'Real Estate Sales', 'Coverage · ML app', 0],
    ['10-construction-hr', 'Construction HR', 'Coverage · documented on GitHub', 0],
    ['12-production-planning-rcc', 'Production Planning (RCC)', 'Coverage · documented on GitHub', 0]
  ];
  var EMAIL = 'hello@atuliwale.com';

  function el(tag, attrs, html) {
    var n = doc.createElement(tag);
    if (attrs) for (var k in attrs) n.setAttribute(k, attrs[k]);
    if (html != null) n.innerHTML = html;
    return n;
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) return navigator.clipboard.writeText(text);
    return new Promise(function (res, rej) {
      var ta = el('textarea'); ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
      doc.body.appendChild(ta); ta.select();
      try { doc.execCommand('copy') ? res() : rej(); } catch (e) { rej(e); }
      ta.remove();
    });
  }

  /* ---------- toast ---------- */
  var toastEl, toastTimer;
  function toast(msg) {
    if (!toastEl) { toastEl = el('div', { class: 'enh-toast', role: 'status', 'aria-live': 'polite' }); doc.body.appendChild(toastEl); }
    toastEl.textContent = msg;
    toastEl.classList.add('is-on');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove('is-on'); }, 2200);
  }

  /* ---------- 1. scroll progress + back to top ---------- */
  function initScrollUi() {
    var bar = el('div', { class: 'enh-progress', 'aria-hidden': 'true' });
    var top = el('button', { class: 'enh-top', type: 'button', 'aria-label': 'Back to top' },
      '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg>');
    doc.body.appendChild(bar);
    doc.body.appendChild(top);
    top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' }); });
    var ticking = false;
    function update() {
      ticking = false;
      var max = root.scrollHeight - window.innerHeight;
      var p = max > 0 ? Math.min(1, window.scrollY / max) : 0;
      bar.style.transform = 'scaleX(' + p + ')';
      top.classList.toggle('is-on', window.scrollY > window.innerHeight * 0.9);
    }
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    window.addEventListener('resize', update);
    update();
  }

  /* ---------- 2. reveal on scroll ---------- */
  function initReveal() {
    if (reduceMotion || !('IntersectionObserver' in window)) return;
    var sel = [
      'main .editorial-heading', 'main h2:not(.visually-hidden)', '.help-card', '.selected-work-card',
      '.work-with-me-grid > *', '.audience-selector-card', '.home-proof-grid > div', '.decision-flow-host',
      '.insight-card', '.book-card', '.exp-career-card', '.exp-stage-card', '.exp-stats > *',
      '.projects-stats > *', '.case-study', '.insight-article section', '.pp-capability', '.contact-compose',
      '.site-bottom-cta-inner'
    ].join(',');
    var items = Array.prototype.slice.call(doc.querySelectorAll(sel)).filter(function (n) {
      return !n.closest('.site-header, .site-menu, .inner-title-band, .lake-hero-copy');
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    var vh = window.innerHeight;
    items.forEach(function (n) {
      var r = n.getBoundingClientRect();
      if (r.top < vh * 0.95) return;            // already on screen: leave it alone
      var sib = n.parentElement ? Array.prototype.indexOf.call(n.parentElement.children, n) : 0;
      n.style.setProperty('--enh-delay', Math.min(sib, 5) * 70 + 'ms');
      n.classList.add('enh-reveal');
      io.observe(n);
    });
  }

  /* ---------- 3. count-up numbers ---------- */
  function initCountUp() {
    if (reduceMotion || !('IntersectionObserver' in window)) return;
    var cands = doc.querySelectorAll('.home-proof-grid dt, .exp-stats *, .projects-stats *');
    var nums = [];
    Array.prototype.forEach.call(cands, function (n) {
      if (n.children.length) return;
      var m = /^(\d{1,4})(\+?)$/.exec(n.textContent.trim());
      if (m && parseFloat(getComputedStyle(n).fontSize) >= 26) nums.push({ n: n, v: +m[1], s: m[2] });
    });
    if (!nums.length) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        io.unobserve(e.target);
        var item = nums.filter(function (x) { return x.n === e.target; })[0];
        var start = performance.now(), dur = 1100 + Math.min(item.v, 300) * 2;
        (function step(now) {
          var t = Math.min(1, (now - start) / dur), eased = 1 - Math.pow(1 - t, 3);
          item.n.textContent = Math.round(item.v * eased) + item.s;
          if (t < 1) requestAnimationFrame(step);
        })(start);
      });
    }, { threshold: 0.6 });
    nums.forEach(function (x) {
      x.n.style.minWidth = x.n.getBoundingClientRect().width + 'px';
      x.n.textContent = '0' + x.s;
      io.observe(x.n);
    });
  }

  /* ---------- 4. pointer spotlight + book tilt ---------- */
  function initPointerFx() {
    if (!finePointer || reduceMotion) return;
    var glowSel = '.capability-card, .insight-card, .exp-career-card, .exp-stage-card, .audience-selector-card, .contact-compose';
    doc.addEventListener('pointermove', function (e) {
      var card = e.target.closest && e.target.closest(glowSel);
      if (card) {
        var r = card.getBoundingClientRect();
        card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        card.style.setProperty('--my', (e.clientY - r.top) + 'px');
        card.classList.add('enh-glow');
      }
      var cover = e.target.closest && e.target.closest('.book-cover');
      if (cover) {
        var b = cover.getBoundingClientRect();
        var x = (e.clientX - b.left) / b.width - 0.5, y = (e.clientY - b.top) / b.height - 0.5;
        cover.style.transform = 'perspective(900px) rotateY(' + (x * 10).toFixed(2) + 'deg) rotateX(' + (-y * 8).toFixed(2) + 'deg) translateY(-4px)';
      }
    }, { passive: true });
    doc.addEventListener('pointerout', function (e) {
      var cover = e.target.closest && e.target.closest('.book-cover');
      if (cover && !cover.contains(e.relatedTarget)) cover.style.transform = '';
    });
  }

  /* ---------- 5. reading time on insight articles ---------- */
  function initReadingTime() {
    var article = doc.querySelector('.insight-article');
    var band = doc.querySelector('.inner-title-band .container');
    if (!article || !band) return;
    var words = article.textContent.trim().split(/\s+/).length;
    var mins = Math.max(1, Math.round(words / 220));
    var sections = article.querySelectorAll('section').length;
    band.appendChild(el('p', { class: 'enh-meta' }, '<span>' + mins + ' min read</span><span>' + sections + ' principles</span><span>Field note</span>'));
  }

  /* ---------- 6. copy email on contact ---------- */
  function initCopyEmail() {
    var target = doc.querySelector('.contact-direct .email-large');
    if (!target) return;
    var btn = el('button', { class: 'enh-copy', type: 'button' },
      '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg><span>Copy email</span>');
    target.insertAdjacentElement('afterend', btn);
    btn.addEventListener('click', function () {
      copyText(EMAIL).then(function () {
        btn.classList.add('is-done'); btn.lastChild.textContent = 'Copied';
        setTimeout(function () { btn.classList.remove('is-done'); btn.lastChild.textContent = 'Copy email'; }, 2000);
      }, function () { toast('Copy failed. The address is ' + EMAIL); });
    });
  }

  /* ---------- 7. command palette ---------- */
  function initPalette() {
    var items = [];
    PAGES.forEach(function (p) { items.push({ g: 'Pages', t: p.t, d: p.d, h: p.h, k: p.k || '' }); });
    SECTIONS.forEach(function (p) { items.push({ g: 'Sections & notes', t: p.t, d: p.d, h: p.h, k: '' }); });
    PROJECTS.forEach(function (p) {
      items.push({ g: 'Projects', t: p[1], d: p[2], h: p[3] ? LIVE + p[0] + '/' : GH + p[0], ext: true, k: p[0] });
    });
    items.push({ g: 'Actions', t: 'Copy email address', d: EMAIL, act: 'copy', k: 'mail contact' });
    items.push({ g: 'Actions', t: 'Open LinkedIn', d: 'linkedin.com/in/atul-i-972066140', h: 'https://www.linkedin.com/in/atul-i-972066140/', ext: true, k: 'social' });
    items.push({ g: 'Actions', t: 'Browse code on GitHub', d: 'github.com/AtulIwale/Portfolio', h: 'https://github.com/AtulIwale/Portfolio', ext: true, k: 'source repo' });

    var key = isMac ? '⌘K' : 'Ctrl K';
    var fab = el('button', { class: 'enh-fab', type: 'button', 'aria-haspopup': 'dialog', 'aria-label': 'Search pages and projects (' + key + ')' },
      '<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><span class="enh-fab-label">Jump to…</span><kbd>' + key + '</kbd>');
    doc.body.appendChild(fab);

    var dlg = el('dialog', { class: 'enh-palette', 'aria-label': 'Search pages and projects' },
      '<div class="enh-pal-head"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>' +
      '<input id="enh-pal-input" type="text" autocomplete="off" spellcheck="false" placeholder="Search pages, projects, notes…" role="combobox" aria-expanded="true" aria-controls="enh-pal-list" aria-autocomplete="list">' +
      '<kbd>Esc</kbd></div><ul id="enh-pal-list" class="enh-pal-list" role="listbox"></ul>' +
      '<div class="enh-pal-foot"><span><kbd>↑</kbd><kbd>↓</kbd> move</span><span><kbd>↵</kbd> open</span><span>' + PROJECTS.length + ' projects · ' + PAGES.length + ' pages</span></div>');
    doc.body.appendChild(dlg);
    var input = dlg.querySelector('input'), list = dlg.querySelector('ul');
    var shown = [], active = 0;

    function score(it, q) {
      if (!q) return 1;
      var hay = (it.t + ' ' + it.d + ' ' + it.k + ' ' + it.g).toLowerCase();
      var terms = q.toLowerCase().split(/\s+/).filter(Boolean), s = 0;
      for (var i = 0; i < terms.length; i++) {
        var idx = hay.indexOf(terms[i]);
        if (idx < 0) return 0;
        s += it.t.toLowerCase().indexOf(terms[i]) === 0 ? 3 : it.t.toLowerCase().indexOf(terms[i]) > -1 ? 2 : 1;
      }
      return s;
    }
    function render() {
      var q = input.value.trim();
      shown = items.map(function (it) { return { it: it, s: score(it, q) }; })
        .filter(function (x) { return x.s > 0; })
        .sort(function (a, b) { return q ? b.s - a.s : 0; })
        .map(function (x) { return x.it; });
      if (active >= shown.length) active = 0;
      var html = '', lastG = '';
      if (!shown.length) html = '<li class="enh-pal-empty">No match for “' + esc(q) + '”. Try “cost”, “safety” or “contact”.</li>';
      shown.forEach(function (it, i) {
        if (!q && it.g !== lastG) { html += '<li class="enh-pal-group" role="presentation">' + esc(it.g) + '</li>'; lastG = it.g; }
        html += '<li role="option" id="enh-opt-' + i + '" data-i="' + i + '" aria-selected="' + (i === active) + '">' +
          '<span class="enh-pal-t">' + esc(it.t) + '</span><span class="enh-pal-d">' + esc(it.d) + '</span>' +
          (it.ext ? '<span class="enh-pal-x" aria-hidden="true">↗</span>' : '') + '</li>';
      });
      list.innerHTML = html;
      input.setAttribute('aria-activedescendant', shown.length ? 'enh-opt-' + active : '');
    }
    function move(d) {
      if (!shown.length) return;
      active = (active + d + shown.length) % shown.length;
      Array.prototype.forEach.call(list.querySelectorAll('[role=option]'), function (o) { o.setAttribute('aria-selected', +o.dataset.i === active); });
      input.setAttribute('aria-activedescendant', 'enh-opt-' + active);
      var cur = list.querySelector('[data-i="' + active + '"]');
      if (cur) cur.scrollIntoView({ block: 'nearest' });
    }
    function choose(i) {
      var it = shown[i]; if (!it) return;
      if (it.act === 'copy') {
        close();
        copyText(EMAIL).then(function () { toast('Email copied: ' + EMAIL); }, function () { toast('Copy failed. The address is ' + EMAIL); });
        return;
      }
      close();
      if (it.ext) window.open(it.h, '_blank', 'noopener'); else window.location.href = it.h;
    }
    function open() {
      if (dlg.open) return;
      input.value = ''; active = 0; render();
      dlg.showModal(); root.classList.add('enh-pal-open');
      setTimeout(function () { input.focus(); }, 0);
    }
    function close() { if (dlg.open) dlg.close(); }
    dlg.addEventListener('close', function () { root.classList.remove('enh-pal-open'); fab.focus({ preventScroll: true }); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) close(); });
    input.addEventListener('input', function () { active = 0; render(); });
    input.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') { e.preventDefault(); move(1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); move(-1); }
      else if (e.key === 'Enter') { e.preventDefault(); choose(active); }
    });
    list.addEventListener('click', function (e) { var o = e.target.closest('[role=option]'); if (o) choose(+o.dataset.i); });
    list.addEventListener('pointermove', function (e) {
      var o = e.target.closest('[role=option]'); if (o && +o.dataset.i !== active) { active = +o.dataset.i; move(0); }
    });
    fab.addEventListener('click', open);
    doc.addEventListener('keydown', function (e) {
      var typing = /INPUT|TEXTAREA|SELECT/.test((e.target && e.target.tagName) || '') || (e.target && e.target.isContentEditable);
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); dlg.open ? close() : open(); }
      else if (e.key === '/' && !typing && !dlg.open) { e.preventDefault(); open(); }
    });
  }

  function boot() {
    root.classList.add('enh');
    var steps = [initScrollUi, initPalette, initReveal, initCountUp, initPointerFx, initReadingTime, initCopyEmail];
    steps.forEach(function (fn) { try { fn(); } catch (err) { if (window.console) console.warn('[enhance]', fn.name, err); } });
  }
  // Wait for the page to finish loading so React hydration has completed before we touch the DOM.
  function schedule() { (window.requestIdleCallback || setTimeout)(boot, { timeout: 400 }); }
  if (doc.readyState === 'complete') schedule(); else window.addEventListener('load', schedule);
})();
