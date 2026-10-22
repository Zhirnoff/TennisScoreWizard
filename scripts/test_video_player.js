// Created by Mikhail Zhirnov on 22.10.2026.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const docs = path.join(__dirname, '..', 'docs');
const locales = ['', 'ar', 'de', 'es', 'fr', 'it', 'ja', 'ko', 'nl',
                 'pt-BR', 'ru', 'tr', 'zh-Hans', 'zh-Hant'];

for (const locale of locales) {
  const folder = path.join(docs, locale);
  const html = fs.readFileSync(path.join(folder, 'index.html'), 'utf8');
  const videos = [...html.matchAll(/<video\b([^>]*)>([\s\S]*?)<\/video>/g)];
  assert.equal(videos.length, 3, locale + ': keep all three videos');
  assert.doesNotMatch(html, /video-player\.js|inline-video-start|inline-video-player/);
  assert.match(html, /english-refresh\.css\?v=20261022-native-video/);
  for (const [, attrs, content] of videos) {
    assert.match(attrs, /\bcontrols\b/, 'Use native browser controls');
    assert.match(attrs, /\bplaysinline\b/, 'Keep playback inside the page');
    assert.match(attrs, /\bpreload="none"/, 'Do not download before interaction');
    assert.doesNotMatch(attrs, /\bautoplay\b|\bloading=|\bon[a-z]+=/);
    const source = attrs.match(/\bsrc="([^"]+\.mp4)"/);
    assert.ok(source, 'Give the video its MP4 source directly');
    assert.ok(fs.existsSync(path.resolve(folder, source[1])));
    const poster = attrs.match(/\bposter="([^"]+)"/);
    assert.ok(poster, 'Keep the approved still image');
    assert.ok(fs.existsSync(path.resolve(folder, poster[1])));
    assert.match(attrs, /aria-label="[^"]+"/);
    assert.match(content, /<track[^>]*kind="captions"/);
    assert.doesNotMatch(content, /<source\b/);
  }
}
assert.equal(fs.existsSync(path.join(docs, 'video-player.js')), false);
assert.doesNotMatch(fs.readFileSync(path.join(docs, 'english-refresh.css'), 'utf8'),
                    /inline-video-player|inline-video-start/);
console.log('Native video controls, direct sources, posters and captions: 14 locales passed.');
