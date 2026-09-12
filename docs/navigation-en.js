/* Transient navigation feedback is not a visited-link or scroll-spy state. */
(() => {
  const nav = document.querySelector('.nav .nav-links');
  if (!nav) return;
  let pendingAnchorURL = null;

  const reset = () => {
    pendingAnchorURL = null;
    nav.querySelectorAll('.is-nav-activated').forEach(link => {
      link.classList.remove('is-nav-activated');
    });
    // Browsers may restore the previously tapped link's focus from history.
    if (nav.contains(document.activeElement)) document.activeElement.blur();
  };

  nav.addEventListener('click', event => {
    const link = event.target.closest('a');
    if (!link || !nav.contains(link) || event.defaultPrevented ||
        event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey ||
        event.altKey || link.target === '_blank') return;
    nav.querySelectorAll('.is-nav-activated').forEach(item => {
      item.classList.remove('is-nav-activated');
    });
    link.classList.add('is-nav-activated');
    const target = new URL(link.href);
    pendingAnchorURL = target.origin === location.origin &&
      target.pathname === location.pathname && target.search === location.search
      ? target.href : null;
  });

  window.addEventListener('pagehide', reset);
  window.addEventListener('pageshow', reset);
  window.addEventListener('popstate', () => {
    // A clicked same-page anchor also emits popstate; retain its feedback.
    if (pendingAnchorURL === location.href) {
      pendingAnchorURL = null;
      return;
    }
    reset();
  });
})();
