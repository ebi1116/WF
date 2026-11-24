(() => {
  const slider = document.querySelector('[data-hero-slider]');
  if (!slider) return;

  const slides = [...slider.querySelectorAll('[data-slide]')];
  const indicators = [...slider.querySelectorAll('[data-indicator]')];
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let current = 0;
  let timer;
  let touchStart = null;

  const show = (index) => {
    current = (index + slides.length) % slides.length;
    slides.forEach((slide, i) => {
      const active = i === current;
      slide.classList.toggle('is-active', active);
      slide.setAttribute('aria-hidden', String(!active));
    });
    indicators.forEach((indicator, i) => {
      indicator.setAttribute('aria-current', String(i === current));
    });
  };

  const stop = () => window.clearInterval(timer);
  const start = () => {
    stop();
    if (!reduceMotion.matches) {
      timer = window.setInterval(() => show(current + 1), 4000);
    }
  };

  slider.querySelector('[data-prev]').addEventListener('click', () => { show(current - 1); start(); });
  slider.querySelector('[data-next]').addEventListener('click', () => { show(current + 1); start(); });
  indicators.forEach((indicator) => indicator.addEventListener('click', () => {
    show(Number(indicator.dataset.indicator));
    start();
  }));
  slider.addEventListener('mouseenter', stop);
  slider.addEventListener('mouseleave', start);
  slider.addEventListener('focusin', stop);
  slider.addEventListener('focusout', (event) => {
    if (!slider.contains(event.relatedTarget)) start();
  });
  slider.addEventListener('touchstart', (event) => {
    touchStart = event.changedTouches[0].clientX;
  }, { passive: true });
  slider.addEventListener('touchend', (event) => {
    if (touchStart === null) return;
    const delta = event.changedTouches[0].clientX - touchStart;
    if (Math.abs(delta) > 45) show(current + (delta < 0 ? 1 : -1));
    touchStart = null;
    start();
  }, { passive: true });
  reduceMotion.addEventListener?.('change', start);
  start();
})();
