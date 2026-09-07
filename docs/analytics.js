/* Website analytics only; no app, match, player, or Health data is sent. */
(() => {
  "use strict";

  const root = "/TennisScoreWizard/";
  if (location.hostname !== "zhirnoff.github.io" ||
      !location.pathname.startsWith(root) || window.goatcounter) return;

  // Keep query strings and section anchors out of page names, and group
  // /folder/ with /folder/index.html. Local and preview hosts never load it.
  const page = location.pathname.endsWith("/")
    ? `${location.pathname}index.html`
    : location.pathname;
  const locale = document.documentElement.lang || "en";
  window.goatcounter = {path: page};

  const apps = {
    "6782709004": "Standalone",
    "6789285015": "Companion",
  };
  document.querySelectorAll('a[href]').forEach((link) => {
    // GoatCounter reads the opt-out fragment at startup, not on hash changes.
    if (link.getAttribute("href") === "#toggle-goatcounter") {
      link.addEventListener("click", (event) => {
        event.preventDefault();
        location.hash = "toggle-goatcounter";
        location.reload();
      });
      return;
    }
    let url;
    try { url = new URL(link.href, location.href); } catch { return; }
    if (url.hostname !== "apps.apple.com") return;
    const id = url.pathname.match(/\/id(\d+)(?:\/|$)/)?.[1];
    const app = apps[id];
    if (!app) return;
    link.setAttribute("data-goatcounter-click", `app-store-${app.toLowerCase()}:${page}`);
    link.setAttribute("data-goatcounter-title", `App Store · ${app} · ${locale}`);
  });

  const script = document.createElement("script");
  script.src = "https://gc.zgo.at/count.js";
  script.async = true;
  script.dataset.goatcounter = "https://tennisscorewizard.goatcounter.com/count";
  script.addEventListener("load", () => {
    // A later refresh must not undo the browser preference just selected.
    if (location.hash === "#toggle-goatcounter") {
      history.replaceState(history.state, "", location.pathname + location.search);
    }
  });
  document.head.appendChild(script);
})();
