(() => {
  const root = document.querySelector('#versions');
  if (!root) return;

  const sections = [
    ['versions', document.querySelector('.nav a[href="#versions"]')?.textContent],
    ['companion-benefits', 'Pro'],
    ['standalone', 'Standalone'],
    ['comparison', document.querySelector('.nav a[href="#comparison"]')?.textContent],
    ['stats-guide', document.querySelector('.nav a[href="#stats-guide"]')?.textContent],
    ['help', document.querySelector('#help h2')?.textContent]
  ].map(([id, label]) => ({ id, element: document.getElementById(id), label: label?.trim() })).filter(item => item.element && item.label);
  if (!sections.length) return;

  const wrapper = document.createElement('div');
  wrapper.className = 'section-menu';
  const toggle = document.createElement('button');
  toggle.type = 'button';
  toggle.className = 'section-menu-toggle';
  toggle.setAttribute('aria-expanded', 'false');
  toggle.setAttribute('aria-controls', 'section-menu-panel');
  const name = document.querySelector('.nav')?.getAttribute('aria-label') || document.querySelector('#versions h2')?.textContent.trim();
  toggle.setAttribute('aria-label', name);
  toggle.title = name;
  toggle.innerHTML = '<svg class="section-menu-grid" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="4" width="6" height="6" rx="1.6"/><rect x="14" y="4" width="6" height="6" rx="1.6"/><rect x="4" y="14" width="6" height="6" rx="1.6"/><rect x="14" y="14" width="6" height="6" rx="1.6"/></svg><svg class="section-menu-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6 18 18M18 6 6 18"/></svg>';

  const panel = document.createElement('nav');
  panel.id = 'section-menu-panel';
  panel.className = 'section-menu-panel';
  panel.setAttribute('aria-label', name);
  panel.hidden = true;
  for (const [index, section] of sections.entries()) {
    const link = document.createElement('a');
    link.className = 'section-menu-link';
    link.href = `#${section.id}`;
    const number = document.createElement('span');
    number.className = 'section-menu-number';
    number.setAttribute('aria-hidden', 'true');
    number.textContent = String(index + 1).padStart(2, '0');
    const text = document.createElement('span');
    text.className = 'section-menu-link-text';
    text.textContent = section.label;
    link.append(number, text);
    link.addEventListener('click', event => {
      event.preventDefault();
      closeMenu(true);
      if (window.location.hash) {
        window.history.replaceState(window.history.state, '', window.location.pathname + window.location.search);
      }
      section.element.scrollIntoView({
        behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth',
        block: 'start'
      });
    });
    panel.append(link);
  }
  wrapper.append(toggle, panel);
  document.body.append(wrapper);

  function closeMenu(restoreFocus = false) {
    if (panel.hidden) return;
    panel.hidden = true;
    toggle.setAttribute('aria-expanded', 'false');
    if (restoreFocus) toggle.focus({ preventScroll: true });
  }

  toggle.addEventListener('click', () => {
    const opening = panel.hidden;
    panel.hidden = !opening;
    toggle.setAttribute('aria-expanded', String(opening));
  });
  document.addEventListener('pointerdown', event => {
    if (!wrapper.contains(event.target)) closeMenu();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') closeMenu(true);
  });

  let scheduled = false;
  const update = () => {
    const visible = window.scrollY > Math.max(500, window.innerHeight * .7);
    wrapper.classList.toggle('is-visible', visible);
    toggle.tabIndex = visible ? 0 : -1;
    if (!visible) closeMenu();
    const marker = window.scrollY + window.innerHeight * .35;
    let active = sections[0];
    for (const section of sections) {
      if (section.element.getBoundingClientRect().top + window.scrollY <= marker) active = section;
    }
    for (const link of panel.querySelectorAll('a')) {
      if (link.hash === `#${active.id}`) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    }
    scheduled = false;
  };
  window.addEventListener('scroll', () => {
    if (scheduled) return;
    scheduled = true;
    window.requestAnimationFrame(update);
  }, { passive: true });
  window.addEventListener('resize', update);
  window.addEventListener('pageshow', update);
  update();
})();
