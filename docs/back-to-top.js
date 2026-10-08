(() => {
  const labels = {
    ar: 'العودة إلى الأعلى',
    de: 'Nach oben',
    en: 'Back to top',
    es: 'Volver arriba',
    fr: 'Retour en haut',
    it: 'Torna su',
    ja: 'ページの先頭へ',
    ko: '맨 위로',
    nl: 'Terug naar boven',
    'pt-br': 'Voltar ao topo',
    ru: 'Наверх',
    tr: 'Yukarı dön',
    zh: '返回顶部',
    'zh-hant': '返回頁首'
  };
  const locale = document.documentElement.lang.toLowerCase();
  const label = labels[locale] || labels[locale.split('-')[0]] || labels.en;
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'back-to-top';
  button.setAttribute('aria-label', label);
  button.title = label;
  button.innerHTML = '<svg class="back-to-top-ring" viewBox="0 0 56 56" fill="none" aria-hidden="true"><defs><linearGradient id="back-to-top-ring-gradient" x1="4" y1="4" x2="52" y2="52" gradientUnits="userSpaceOnUse"><stop stop-color="#c8ff86"/><stop offset="1" stop-color="#28ff5f"/></linearGradient></defs><circle class="back-to-top-ring-track" cx="28" cy="28" r="25"/><circle class="back-to-top-ring-value" cx="28" cy="28" r="25" pathLength="100"/></svg><svg class="back-to-top-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.15" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6.5 15 5.5-5.5 5.5 5.5"/></svg>';
  document.body.append(button);

  const update = () => {
    const maxScroll = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);
    const progress = maxScroll ? Math.min(1, Math.max(0, window.scrollY / maxScroll)) : 0;
    button.style.setProperty('--scroll-progress', `${(progress * 100).toFixed(2)}%`);
    button.style.setProperty('--scroll-progress-offset', (100 - progress * 100).toFixed(2));
    const canScroll = maxScroll > 120;
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
