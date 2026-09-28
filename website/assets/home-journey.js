/* Optional homepage enhancement: complete reading order works without this file or GSAP. */
(() => {
  'use strict';
  if (window.AtulJourney) { window.AtulJourney.mount(); return; }
  let cleanup = () => {};
  let libraries;
  function script(src) {
    return new Promise((resolve, reject) => {
      const tag = document.createElement('script');
      const timeout = setTimeout(() => reject(new Error('Animation CDN unavailable')), 8000);
      tag.src = src; tag.async = true;
      tag.onload = () => { clearTimeout(timeout); resolve(); };
      tag.onerror = () => { clearTimeout(timeout); reject(new Error('Animation CDN unavailable')); };
      document.head.appendChild(tag);
    });
  }
  function loadLibraries() {
    if (window.gsap && window.ScrollTrigger) return Promise.resolve();
    if (!libraries) libraries = (async () => {
      if (!window.gsap) await script('https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js');
      if (!window.ScrollTrigger) await script('https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/ScrollTrigger.min.js');
      window.gsap.registerPlugin(window.ScrollTrigger);
    })().catch(error => { libraries = null; throw error; });
    return libraries;
  }
  function mount() {
    cleanup();
    const root = document.getElementById('home-journey');
    if (!root) return;
    const stage = root.querySelector('.journey-stage');
    const phases = [...root.querySelectorAll('.journey-phase')];
    const images = phases.map(phase => phase.querySelector('img'));
    const indexLinks = [...root.querySelectorAll('[data-phase-index]')];
    const reading = root.querySelector('[data-reading-mode]');
    const motion = matchMedia('(prefers-reduced-motion: reduce)');
    const saving = navigator.connection?.saveData;
    let disposed = false, context, observer, resizeTimer, timeline, entrance, active = -1;
    let readAll = false, pinned = false;
    let setupVersion = 0;
    const unbind = [];
    const on = (target, event, handler, options) => {
      target.addEventListener(event, handler, options);
      unbind.push(() => target.removeEventListener(event, handler, options));
    };
    function warmImages(index) {
      // Only the current and adjacent still need early loading; never request video.
      [index, ...(saving ? [] : [index + 1])].forEach(i => {
        if (images[i]) images[i].loading = 'eager';
      });
    }
    function select(index) {
      if (active === index) return;
      entrance?.cancel(); entrance = null;
      active = index;
      phases.forEach((phase, i) => {
        if (pinned) phase.setAttribute('aria-hidden', String(i !== index));
        if (i === index) indexLinks[i].setAttribute('aria-current', 'step');
        else indexLinks[i].removeAttribute('aria-current');
      });
      if (index >= 0) warmImages(index);
    }
    indexLinks.forEach((link, index) => on(link, 'click', event => {
      if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      const trigger = timeline?.scrollTrigger;
      if (pinned && trigger) {
        // Go to an exact chapter without waiting for a wheel gesture or snap.
        window.scrollTo({ top: trigger.start + (trigger.end - trigger.start) * index / 6, behavior: 'instant' });
        timeline.progress(index / 6);
        window.ScrollTrigger.update();
        select(index);
        if (!motion.matches && !document.hidden && phases[index].animate) {
          entrance?.cancel();
          entrance = phases[index].animate([{ opacity: .65, transform: 'translateY(6px)' }, { opacity: 1, transform: 'translateY(0)' }], { duration: 240, easing: 'ease-out' });
        }
      } else {
        phases[index].scrollIntoView({ behavior: motion.matches ? 'instant' : 'smooth', block: 'start' });
        const heading = phases[index].querySelector('h2');
        heading.tabIndex = -1; heading.focus({ preventScroll: true });
        select(index);
      }
    }));
    function reset() {
      observer?.disconnect(); observer = null;
      entrance?.cancel(); entrance = null;
      context?.revert(); context = null; timeline = null;
      pinned = false; active = -1;
      root.classList.remove('is-pinned');
      phases.forEach(phase => phase.removeAttribute('aria-hidden'));
      indexLinks.forEach(link => link.removeAttribute('aria-current'));
    }
    function staticMode() {
      if (!('IntersectionObserver' in window)) return;
      const visible = new Map();
      observer = new IntersectionObserver(entries => {
        entries.forEach(entry => visible.set(phases.indexOf(entry.target), entry.isIntersecting ? entry.intersectionRatio : 0));
        let best = -1, ratio = 0;
        visible.forEach((value, index) => { if (value > ratio) { ratio = value; best = index; } });
        select(best);
      }, { threshold: [0, .25, .5, .75, 1] });
      phases.forEach(phase => observer.observe(phase));
    }
    async function setup() {
      const version = ++setupVersion;
      reset();
      reading.hidden = motion.matches;
      if (motion.matches || readAll) { staticMode(); return; }
      try { if (!window.gsap || !window.ScrollTrigger) await loadLibraries(); } catch (_) { if (!disposed && version === setupVersion) { reading.hidden = true; staticMode(); } return; }
      if (disposed || version !== setupVersion || !root.isConnected) return;
      const header = document.querySelector('.site-header').getBoundingClientRect().height;
      const available = window.innerHeight - header;
      const tallest = Math.max(...phases.map(phase => phase.scrollHeight));
      const chrome = root.querySelector('.journey-toolbar').offsetHeight + root.querySelector('.journey-index').offsetHeight;
      // At short heights / enlarged text, prefer full readable content over clipped pinned panels.
      const fits = tallest + chrome <= available;
      const gsap = window.gsap;
      function fadeHero() {
        const hero = document.querySelector('.journey-hero');
        if (hero) gsap.to(hero.querySelector('.journey-hero-inner'), {
          opacity: 0, y: -24, ease: 'none',
          scrollTrigger: { trigger: hero, start: 'top ' + header, end: 'bottom ' + (header + available * .35), scrub: true }
        });
      }
      if (!fits) {
        reading.hidden = true;
        context = gsap.context(fadeHero, root.parentElement);
        staticMode(); return;
      }
      root.style.setProperty('--journey-height', available + 'px');
      root.classList.add('is-pinned'); pinned = true;
      context = gsap.context(() => {
        gsap.set(phases, { autoAlpha: 0 });
        gsap.set(phases[0], { autoAlpha: 1 });
        timeline = gsap.timeline({
          defaults: { ease: 'none' },
          scrollTrigger: {
            trigger: root, pin: stage, start: () => 'top ' + header,
            // A quarter of the former distance: roughly one short gesture per phase.
            end: () => '+=' + Math.round(window.innerHeight * 1.5),
            scrub: true, anticipatePin: 1, invalidateOnRefresh: true,
            // Finish a small gesture at the next readable phase in its direction.
            // Disable projected momentum so a gentle scroll cannot fling ahead.
            snap: { snapTo: 1 / 6, directional: true, inertia: false,
              delay: .1, duration: { min: .12, max: .28 }, ease: 'power1.inOut' }
          },
          onUpdate: () => { if (timeline) select(Math.min(5, Math.floor(timeline.time() + .125))); }
        });
        timeline.to({}, { duration: 6 }, 0);
        phases.slice(1).forEach((phase, offset) => {
          const i = offset + 1;
          timeline.to(phases[i - 1], { autoAlpha: 0, xPercent: -1.5, duration: .25 }, i - .25)
            .fromTo(phase, { autoAlpha: 0, xPercent: 1.5 }, { autoAlpha: 1, xPercent: 0, duration: .25 }, i - .25);
        });
        fadeHero();
      }, root.parentElement);
      select(0);
      window.ScrollTrigger.refresh();
    }
    on(reading, 'click', () => {
      readAll = !readAll; reading.textContent = readAll ? 'Scroll journey' : 'Read all phases';
      reading.setAttribute('aria-pressed', String(readAll)); setup();
    });
    on(document, 'visibilitychange', () => { if (document.hidden) { entrance?.cancel(); entrance = null; } });
    on(motion, 'change', setup);
    let lastWidth = innerWidth, lastHeight = innerHeight;
    on(window, 'resize', () => {
      // Ignore small mobile browser-chrome changes; still remeasure orientation, zoom and desktop resize.
      if (innerWidth === lastWidth && Math.abs(innerHeight - lastHeight) < 100) return;
      lastWidth = innerWidth; lastHeight = innerHeight;
      clearTimeout(resizeTimer); resizeTimer = setTimeout(setup, 160);
    }, { passive: true });
    cleanup = () => {
      disposed = true; ++setupVersion; clearTimeout(resizeTimer); reset();
      unbind.forEach(fn => fn()); root.style.removeProperty('--journey-height');
    };
    setup();
    document.fonts?.ready.then(() => { if (!disposed) setup(); });
  }
  window.AtulJourney = { mount, unmount: () => cleanup() };
  mount();
})();
