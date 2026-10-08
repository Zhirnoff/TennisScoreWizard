const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const docs = path.join(__dirname, '..', 'docs');
const homepages = [
  path.join(docs, 'index.html'),
  ...fs.readdirSync(docs, { withFileTypes: true })
    .filter(entry => entry.isDirectory() && fs.existsSync(path.join(docs, entry.name, 'index.html')))
    .map(entry => path.join(docs, entry.name, 'index.html'))
];

assert.equal(homepages.length, 14);
for (const file of homepages) {
  const html = fs.readFileSync(file, 'utf8');
  const prefix = file === path.join(docs, 'index.html') ? '' : '../';
  assert.equal(html.split(`${prefix}section-menu.css?v=20261008-glass-menu`).length - 1, 1, file);
  assert.equal(html.split(`${prefix}section-menu.js?v=20261008-glass-menu-2`).length - 1, 1, file);
  for (const id of ['versions', 'companion-benefits', 'standalone', 'comparison', 'stats-guide', 'help']) {
    assert.match(html, new RegExp(`id="${id}"`), `${file}: missing ${id}`);
  }
  assert.doesNotMatch(html, /site-experience\.(css|js)/, `${file}: abandoned scene included`);
}

const js = fs.readFileSync(path.join(docs, 'section-menu.js'), 'utf8');
const css = fs.readFileSync(path.join(docs, 'section-menu.css'), 'utf8');
new Function(js);
assert.match(js, /aria-expanded/);
assert.match(js, /aria-current/);
assert.match(js, /event\.key === 'Escape'/);
assert.match(js, /event\.preventDefault\(\)/);
assert.match(js, /history\.replaceState/);
assert.match(js, /section\.element\.scrollIntoView/);
assert.match(css, /section-menu-panel\[hidden\]/);
assert.match(css, /prefers-reduced-motion: reduce/);
assert.match(css, /width: 44px/);

console.log('Compact section menu and localization checks passed.');
