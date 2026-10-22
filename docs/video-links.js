// Created by Mikhail Zhirnov on 22.10.2026.
(() => {
  // On iPhone/iPad, use the browser's media document: the same playback path
  // as opening the MP4 directly. A normal link preserves the user's gesture.
  const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent)
    || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  if (!isIOS) return;

  for (const video of document.querySelectorAll('.release-spotlight-card video')) {
    const fallback = video.querySelector('a[href]');
    const link = document.createElement('a');
    link.className = 'native-video-link';
    link.href = video.src;
    link.setAttribute('aria-label', fallback?.textContent.trim()
      || video.getAttribute('aria-label'));

    const poster = document.createElement('img');
    poster.src = video.poster;
    poster.alt = '';
    poster.width = video.width;
    poster.height = video.height;
    poster.decoding = 'async';

    const play = document.createElement('span');
    play.className = 'native-video-link-play';
    play.setAttribute('aria-hidden', 'true');
    play.innerHTML = '<svg viewBox="0 0 24 24" focusable="false"><path d="M8 5v14l11-7z"/></svg>';
    link.append(poster, play);
    video.replaceWith(link);
  }
})();
