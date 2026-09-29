/* redesign/home.js — homepage behaviour for the static redesign
   (the old React homepage handled the menu; everything else is progressive). */
(function () {
  'use strict';
  var doc = document;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* mobile menu: same dialog markup and classes as the other pages */
  function initMenu() {
    var trigger = doc.querySelector('.menu-trigger');
    var dlg = doc.getElementById('site-menu');
    if (!trigger || !dlg || typeof dlg.showModal !== 'function') return;
    trigger.addEventListener('click', function () { dlg.showModal(); trigger.setAttribute('aria-expanded', 'true'); });
    var close = dlg.querySelector('.menu-close');
    if (close) close.addEventListener('click', function () { dlg.close(); });
    dlg.addEventListener('close', function () { trigger.setAttribute('aria-expanded', 'false'); trigger.focus(); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
    Array.prototype.forEach.call(dlg.querySelectorAll('a'), function (a) { a.addEventListener('click', function () { dlg.close(); }); });
  }

  /* sections and project columns reveal once, in reading order */
  function initReveal() {
    var items = Array.prototype.slice.call(doc.querySelectorAll('[data-reveal]'));
    if (reduce || !('IntersectionObserver' in window)) { items.forEach(function (n) { n.classList.add('is-in'); }); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.filter(function (e) { return e.isIntersecting; })
        .sort(function (a, b) { return (a.boundingClientRect.top - b.boundingClientRect.top) || (a.boundingClientRect.left - b.boundingClientRect.left); })
        .forEach(function (e, i) {
          e.target.style.setProperty('--d', Math.min(i, 5) * 90 + 'ms');
          e.target.classList.add('is-in');
          io.unobserve(e.target);
          if (e.target.classList.contains('rd-stat')) countUp(e.target);
        });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    items.forEach(function (n) { io.observe(n); });
  }

  /* numbers count once, when the strip is first seen */
  function countUp(stat) {
    var el = stat.querySelector('.rd-count');
    if (!el || reduce || el.dataset.done) return;
    el.dataset.done = '1';
    var target = +el.dataset.count, start = performance.now(), dur = 1100 + Math.min(target, 300);
    el.style.minWidth = el.getBoundingClientRect().width + 'px';
    (function step(now) {
      var t = Math.min(1, (now - start) / dur), eased = 1 - Math.pow(1 - t, 3);
      el.textContent = Math.round(target * eased);
      if (t < 1) requestAnimationFrame(step);
    })(start);
  }

  function boot() { initMenu(); initReveal(); }
  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', boot); else boot();
})();
