const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const source = fs.readFileSync(
  path.join(__dirname, '..', 'docs', 'back-to-top.js'), 'utf8'
);
const docs = path.join(__dirname, '..', 'docs');

function render({ locale = 'en', scrollHeight = 2000, innerHeight = 800 } = {}) {
  const buttonListeners = {};
  const windowListeners = {};
  const classes = new Set();
  const properties = new Map();
  const button = {
    attributes: {},
    classList: {
      toggle(name, enabled) {
        if (enabled) classes.add(name);
        else classes.delete(name);
      }
    },
    style: { setProperty(name, value) { properties.set(name, value); } },
    setAttribute(name, value) { this.attributes[name] = value; },
    addEventListener(name, handler) { buttonListeners[name] = handler; },
    blur() { this.blurred = true; }
  };
  const document = {
    documentElement: { lang: locale, scrollHeight },
    createElement() { return button; },
    body: { append() {} }
  };
  const window = {
    innerHeight,
    scrollY: 0,
    addEventListener(name, handler) { windowListeners[name] = handler; },
    matchMedia() { return { matches: false }; },
    scrollTo(options) { this.lastScrollTo = options; }
  };

  vm.runInNewContext(source, { document, window });
  return { button, buttonListeners, classes, document, properties, window, windowListeners };
}

const page = render();
assert.equal(page.properties.get('--scroll-progress'), '0.00%');
assert.equal(page.classes.has('is-visible'), false);
assert.equal(page.button.tabIndex, -1);

page.window.scrollY = 600;
page.windowListeners.scroll();
assert.equal(page.properties.get('--scroll-progress'), '50.00%');
assert.equal(page.classes.has('is-visible'), true);
assert.equal(page.button.tabIndex, 0);

page.window.scrollY = 1200;
page.windowListeners.scroll();
assert.equal(page.properties.get('--scroll-progress'), '100.00%');

page.window.scrollY = 2000;
page.windowListeners.scroll();
assert.equal(page.properties.get('--scroll-progress'), '100.00%');

page.buttonListeners.click();
assert.equal(page.window.lastScrollTo.top, 0);
assert.equal(page.window.lastScrollTo.behavior, 'smooth');

page.window.matchMedia = () => ({ matches: true });
page.buttonListeners.click();
assert.equal(page.window.lastScrollTo.behavior, 'instant');

const shortPage = render({ scrollHeight: 850, innerHeight: 800 });
shortPage.window.scrollY = 50;
shortPage.windowListeners.scroll();
assert.equal(shortPage.classes.has('is-visible'), false);
assert.equal(shortPage.properties.get('--scroll-progress'), '100.00%');

for (const [locale, label] of Object.entries({
  ar: 'العودة إلى الأعلى',
  nl: 'Terug naar boven',
  'pt-BR': 'Voltar ao topo',
  'zh-Hant': '返回頁首'
})) {
  assert.equal(render({ locale }).button.attributes['aria-label'], label);
}

function htmlFiles(directory) {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap(entry => {
    const name = path.join(directory, entry.name);
    return entry.isDirectory() ? htmlFiles(name) : entry.name.endsWith('.html') ? [name] : [];
  });
}

for (const file of htmlFiles(docs)) {
  const html = fs.readFileSync(file, 'utf8');
  assert.match(html, /back-to-top\.css\?v=20261008-scroll-progress/, file);
  assert.match(html, /back-to-top\.js\?v=20261008-scroll-progress/, file);
}

const css = fs.readFileSync(path.join(docs, 'back-to-top.css'), 'utf8');
assert.match(css, /conic-gradient\(from -90deg/);
assert.match(css, /var\(--scroll-progress\)/);

console.log('Back-to-top progress and locale checks passed.');
