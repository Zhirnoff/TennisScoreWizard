(() => {
  const labels = {
    de: 'Nach oben',
    en: 'Back to top',
    es: 'Volver arriba',
    fr: 'Retour en haut',
    it: 'Torna su',
    ja: 'ページの先頭へ',
    ko: '맨 위로',
    ru: 'Наверх',
    tr: 'Yukarı dön',
    zh: '返回顶部'
  };
  const language = document.documentElement.lang.toLowerCase().split('-')[0];
  const label = labels[language] || labels.en;
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'back-to-top';
  button.setAttribute('aria-label', label);
  button.title = label;
  button.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m5 12 7-7 7 7"/><path d="M12 5v14"/></svg>';
  document.body.append(button);

  const update = () => {
    const canScroll = document.documentElement.scrollHeight > window.innerHeight + 120;
    const visible = canScroll && window.scrollY > Math.max(500, window.innerHeight * .7);
    button.classList.toggle('is-visible', visible);
    button.tabIndex = visible ? 0 : -1;
  };

  button.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'
    });
    button.blur();
  });

  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  window.addEventListener('pageshow', update);
  update();
})();
