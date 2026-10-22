// Created by Mikhail Zhirnov on 22.10.2026.
// Opt-in investigation of physical-iPhone playback; never runs on ordinary visits.
(() => {
  if (new URLSearchParams(location.search).get('video-check') !== '1') return;
  const video = document.querySelector('video');
  if (!video) return;

  const originalSource = video.src;
  const started = performance.now();
  const attempts = [];
  let attempt;
  let sampling;
  let mode = 'original';
  const panel = document.createElement('aside');
  panel.lang = 'ru';
  panel.setAttribute('aria-label', 'Проверка воспроизведения');
  panel.style.cssText = 'margin-top:16px;padding:16px;background:#101815;border:1px solid #28ff5f;border-radius:12px;color:white;font:16px/1.5 system-ui;text-align:left;';
  panel.innerHTML = `
    <strong>Проверка видео</strong>
    <p style="color:white;margin:8px 0">Нажмите Play на ролике выше и подождите 10 секунд. Затем скопируйте результат и отправьте его в чат.</p>
    <p role="status" style="color:#28ff5f;margin:8px 0">Ожидание нажатия Play.</p>
    <button type="button" data-action="copy">Скопировать результат</button>
    <details style="margin-top:12px"><summary>Дополнительные проверки</summary>
      <p style="color:white;margin:8px 0">Каждая кнопка меняет один параметр. После неё снова нажмите Play на ролике.</p>
      <button type="button" data-action="fresh">Свежая загрузка файла</button>
      <button type="button" data-action="fullscreen">Полноэкранный режим</button>
    </details>
    <details style="margin-top:12px"><summary>Текст результата</summary>
      <textarea readonly aria-label="Результат проверки" rows="8" style="box-sizing:border-box;width:100%;background:#000;color:#fff;font:12px/1.4 monospace"></textarea>
    </details>
    <small style="display:block;margin-top:8px">Отчёт никуда не отправляется автоматически.</small>`;
  for (const button of panel.querySelectorAll('button')) {
    button.style.cssText = 'display:block;min-height:44px;width:100%;margin-top:8px;padding:8px;border:1px solid #28ff5f;border-radius:8px;background:#163621;color:#fff;font:inherit;';
  }
  video.after(panel);
  const status = panel.querySelector('[role="status"]');
  const output = panel.querySelector('textarea');
  const codes = ['NONE', 'ABORTED', 'NETWORK', 'DECODE', 'SRC_NOT_SUPPORTED'];

  function snapshot() {
    const quality = video.getVideoPlaybackQuality?.();
    return {
      at: Math.round(performance.now() - started),
      time: Number(video.currentTime.toFixed(3)),
      paused: video.paused,
      ready: video.readyState,
      network: video.networkState,
      size: [video.videoWidth, video.videoHeight],
      frames: quality?.totalVideoFrames ?? video.webkitDecodedFrameCount ?? null,
      dropped: quality?.droppedVideoFrames ?? null,
      buffered: Array.from({ length: video.buffered.length }, (_, i) =>
        [video.buffered.start(i), video.buffered.end(i)]),
      error: video.error ? {
        code: codes[video.error.code] || video.error.code,
        message: video.error.message
      } : null
    };
  }

  function report() {
    output.value = JSON.stringify({
      diagnostic: '20261022-1',
      browser: navigator.userAgent,
      page: location.pathname,
      source: originalSource,
      attempts,
      current: snapshot()
    }, null, 2);
  }

  function begin() {
    if (attempt) return;
    attempt = { mode, source: video.src, events: [], samples: [], delivery: [] };
    attempts.push(attempt);
    let ticks = 0;
    sampling = setInterval(() => {
      attempt.samples.push(snapshot());
      report();
      if (++ticks === 10) {
        clearInterval(sampling);
        sampling = null;
        if (!video.error) {
          status.textContent = video.currentTime > 0.5
            ? 'Время видео идёт. Скопируйте результат и напишите, движется ли картинка.'
            : 'Видео не продвинулось. Скопируйте результат.';
        }
      }
    }, 1000);
  }

  async function probeDelivery(target) {
    // Only after a playback failure, never on page load. Fetch a tiny byte range.
    await Promise.all([false, true].map(async fresh => {
      const url = new URL(target.source);
      if (fresh) url.searchParams.set('video-probe', String(Date.now()));
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 8000);
      try {
        const response = await fetch(url, {
          cache: 'no-store', headers: { Range: 'bytes=0-1' }, signal: controller.signal
        });
        const bytes = new Uint8Array(await response.arrayBuffer());
        target.delivery.push({
          fresh, status: response.status,
          type: response.headers.get('content-type'),
          range: response.headers.get('content-range'),
          encoding: response.headers.get('content-encoding'),
          length: bytes.length, firstBytes: Array.from(bytes.slice(0, 16))
        });
      } catch (error) {
        target.delivery.push({ fresh, error: String(error) });
      } finally {
        clearTimeout(timeout);
        report();
      }
    }));
  }

  // Listening does not intercept the native control or call play/load.
  video.addEventListener('pointerdown', begin, { passive: true });
  for (const name of ['loadstart', 'loadedmetadata', 'loadeddata', 'canplay', 'play',
    'playing', 'waiting', 'stalled', 'suspend', 'pause', 'ended', 'error']) {
    video.addEventListener(name, () => {
      begin();
      attempt.events.push({ name, ...snapshot() });
      if (name === 'error') {
        status.textContent = `Ошибка Safari: ${codes[video.error?.code] || 'UNKNOWN'}. Скопируйте результат через 10 секунд.`;
        if (!attempt.probed) {
          attempt.probed = true;
          void probeDelivery(attempt);
        }
      } else if (name === 'play') {
        status.textContent = 'Запуск запрошен. Записываю результат…';
      }
      report();
    });
  }

  let observedSecond = -1;
  video.addEventListener('timeupdate', () => {
    const second = Math.floor(video.currentTime);
    if (second === observedSecond) return;
    observedSecond = second;
    if (video.currentTime > 0.5 && !video.error) {
      status.textContent = 'Время видео идёт. Скопируйте результат и напишите, движется ли картинка.';
    }
    report();
  });

  function reset(nextMode) {
    video.pause();
    clearInterval(sampling);
    attempt = null;
    observedSecond = -1;
    mode = nextMode;
    status.textContent = 'Теперь нажмите Play на ролике выше.';
  }

  panel.querySelector('[data-action="fresh"]').addEventListener('click', () => {
    reset('fresh-url');
    video.setAttribute('playsinline', '');
    const url = new URL(originalSource);
    url.searchParams.set('video-check-file', String(Date.now()));
    video.src = url.href;
    video.load();
    report();
  });
  panel.querySelector('[data-action="fullscreen"]').addEventListener('click', () => {
    reset('fullscreen');
    video.removeAttribute('playsinline');
    video.load();
    report();
  });
  panel.querySelector('[data-action="copy"]').addEventListener('click', async () => {
    report();
    try {
      await navigator.clipboard.writeText(output.value);
      status.textContent = 'Результат скопирован. Вставьте его в чат.';
    } catch {
      output.parentElement.open = true;
      output.focus();
      output.select();
      status.textContent = 'Скопируйте выделенный текст результата вручную.';
    }
  });
  report();
})();
