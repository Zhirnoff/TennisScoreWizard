// Created by Mikhail Zhirnov on 22.10.2026.
(() => {
  for (const video of document.querySelectorAll('.release-spotlight-card video')) {
    const player = document.createElement('div');
    player.className = 'inline-video-player';
    const start = document.createElement('button');
    start.type = 'button';
    start.className = 'inline-video-start';
    start.setAttribute('aria-label', video.getAttribute('aria-label'));
    start.innerHTML = '<span aria-hidden="true">▶</span>';
    video.before(player);
    player.append(video, start);
    video.controls = false;
    video.tabIndex = -1;

    let request = 0;
    const showStart = () => {
      start.hidden = false;
      start.removeAttribute('aria-busy');
      video.controls = false;
      video.tabIndex = -1;
    };

    start.addEventListener('click', () => {
      const currentRequest = ++request;
      start.setAttribute('aria-busy', 'true');
      video.controls = true;
      if (video.error) video.load();
      if (video.ended) video.currentTime = 0;
      try {
        // Keep play() in the original tap/keyboard event. Waiting for a load
        // event first loses the user gesture required for sound on iPhone.
        const playback = video.play();
        playback?.catch(() => {
          if (currentRequest === request && video.paused) showStart();
        });
      } catch {
        showStart();
      }
    });

    video.addEventListener('playing', () => {
      const moveFocus = document.activeElement === start;
      start.hidden = true;
      start.removeAttribute('aria-busy');
      video.controls = true;
      video.tabIndex = 0;
      if (moveFocus) video.focus({ preventScroll: true });
    });
    video.addEventListener('ended', showStart);
    video.addEventListener('error', showStart);
  }
})();
