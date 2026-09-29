/* redesign/insight.js — research notes: contents highlight, reading progress,
   and topic filters on the index. Menu and reveals come from home.js. */
(function () {
  'use strict';
  var doc = document;

  function initToc() {
    var links = Array.prototype.slice.call(doc.querySelectorAll('.ins-toc a[href^="#"]'));
    if (!links.length) return;
    var heads = links.map(function (a) { return doc.getElementById(a.getAttribute('href').slice(1)); });
    var ticking = false;
    /* the active section is the last heading that has passed 30% of the viewport */
    function update() {
      var line = window.innerHeight * 0.3, active = -1;
      heads.forEach(function (h, i) { if (h && h.getBoundingClientRect().top <= line) active = i; });
      links.forEach(function (a, i) { a.classList.toggle('is-active', i === active); });
      ticking = false;
    }
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    update();
  }

  function initProgress() {
    var article = doc.querySelector('.ins-prose');
    if (!article) return;
    var bar = doc.createElement('div');
    bar.className = 'ins-progress';
    bar.setAttribute('aria-hidden', 'true');
    doc.body.appendChild(bar);
    var ticking = false;
    function update() {
      var r = article.getBoundingClientRect();
      var total = r.height - window.innerHeight * 0.6;
      var p = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 0;
      bar.style.setProperty('--p', p.toFixed(4));
      ticking = false;
    }
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    update();
  }

  function initFilters() {
    var bar = doc.querySelector('.ins-filters');
    if (!bar) return;
    var buttons = Array.prototype.slice.call(bar.querySelectorAll('button'));
    var cards = Array.prototype.slice.call(doc.querySelectorAll('.ins-card'));
    var count = doc.querySelector('[data-ins-count]');
    buttons.forEach(function (b) {
      b.addEventListener('click', function () {
        var topic = b.getAttribute('data-topic');
        buttons.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        var shown = 0;
        cards.forEach(function (c) {
          var match = topic === 'all' || (' ' + c.getAttribute('data-topics') + ' ').indexOf(' ' + topic + ' ') > -1;
          c.hidden = !match;
          if (match) { shown++; c.classList.add('is-in'); }
        });
        if (count) count.textContent = shown + (shown === 1 ? ' note' : ' notes');
      });
    });
  }

  function boot() { initToc(); initProgress(); initFilters(); }
  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', boot); else boot();
})();
