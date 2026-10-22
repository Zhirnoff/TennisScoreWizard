// Created by Mikhail Zhirnov on 22.10.2026.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const docs = path.join(__dirname, '..', 'docs');
const source = fs.readFileSync(path.join(docs, 'video-player.js'), 'utf8');

function render(playback = () => Promise.resolve()) {
  const elements = [];
  const videoListeners = {};
  const video = {
    controls: true,
    paused: true,
    ended: false,
    error: null,
    calls: [],
    getAttribute() { return 'Localized video description'; },
    before(element) { this.wrapper = element; },
    addEventListener(event, listener) { videoListeners[event] = listener; },
    play() { this.calls.push('play'); return playback(); },
    load() { this.calls.push('load'); },
    focus(options) { this.focusOptions = options; }
  };
  const document = {
    activeElement: null,
    querySelectorAll() { return [video]; },
    createElement(tag) {
      const element = {
        tag,
        hidden: false,
        attributes: {},
        listeners: {},
        setAttribute(name, value) { this.attributes[name] = value; },
        removeAttribute(name) { delete this.attributes[name]; },
        addEventListener(event, listener) { this.listeners[event] = listener; },
        append(...children) { this.children = children; }
      };
      elements.push(element);
      return element;
    }
  };
  vm.runInNewContext(source, { document });
  return { video, videoListeners, document, start: elements[1] };
}

async function check() {
  const page = render();
  assert.deepEqual(page.video.calls, [], 'Do not load or play before a tap');
  assert.equal(page.video.controls, false);
  assert.equal(page.start.attributes['aria-label'], 'Localized video description');
  page.start.listeners.click();
  assert.deepEqual(page.video.calls, ['play'], 'play() must run synchronously in the tap');
  assert.equal(page.start.hidden, false, 'Keep the tap target until playback starts');
  page.document.activeElement = page.start;
  page.video.paused = false;
  page.videoListeners.playing();
  assert.equal(page.start.hidden, true);
  assert.equal(page.video.controls, true, 'Keep native pause, seek, audio and fullscreen');
  assert.equal(page.video.focusOptions.preventScroll, true);
  assert.equal(page.videoListeners.pause, undefined, 'Do not restart native pauses');
  page.videoListeners.ended();
  assert.equal(page.start.hidden, false);
  page.video.ended = true;
  page.start.listeners.click();
  assert.equal(page.video.currentTime, 0, 'Allow another tap to replay');

  const rejected = render(() => Promise.reject(new Error('Playback denied')));
  rejected.start.listeners.click();
  await Promise.resolve();
  assert.equal(rejected.start.hidden, false);
  assert.equal(rejected.video.controls, false);
  assert.equal(rejected.start.attributes['aria-busy'], undefined);
  rejected.start.listeners.click();
  await Promise.resolve();
  assert.deepEqual(rejected.video.calls, ['play', 'play'], 'Allow retry after rejection');

  const failed = render(() => { throw new Error('Media failure'); });
  failed.video.error = { code: 2 };
  failed.start.listeners.click();
  assert.deepEqual(failed.video.calls, ['load', 'play'], 'Retry a failed source in the same tap');
  assert.equal(failed.start.hidden, false);
  assert.equal(failed.start.attributes['aria-busy'], undefined);

  let rejectEarlier;
  const stale = render(() => new Promise((resolve, reject) => { rejectEarlier = reject; }));
  stale.start.listeners.click();
  const firstReject = rejectEarlier;
  stale.start.listeners.click();
  stale.video.paused = false;
  stale.videoListeners.playing();
  firstReject(new Error('Old request cancelled'));
  await Promise.resolve();
  assert.equal(stale.start.hidden, true, 'An old request must not cover a playing video');
  stale.videoListeners.error();
  assert.equal(stale.start.hidden, false);

  for (const locale of ['', 'ar', 'de', 'es', 'fr', 'it', 'ja', 'ko', 'nl',
                        'pt-BR', 'ru', 'tr', 'zh-Hans', 'zh-Hant']) {
    const html = fs.readFileSync(path.join(docs, locale, 'index.html'), 'utf8');
    assert.equal((html.match(/video-player\.js\?v=20261022-video-tap/g) || []).length, 1);
    assert.equal((html.match(/<video controls playsinline preload="none"/g) || []).length, 3);
    assert.doesNotMatch(html, /<video[^>]*\bautoplay\b/);
    assert.match(html, /english-refresh\.css\?v=20261022-video-tap/);
  }
  console.log('Video player: tap, retry, replay, native controls and 14 locales passed.');
}

check().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
