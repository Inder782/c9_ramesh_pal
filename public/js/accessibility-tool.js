/*!
 * ============================================================================
 *  Accessibility Tool  —  v1.0.0
 *  A free, self-contained web accessibility toolbar.  Built in India.
 *  Licence: MIT — free to use, modify, rebrand and redistribute.
 * ============================================================================
 *
 * ONE file. No dependencies. Drop it on any website:
 *
 *   <script src="accessibility-tool.js" defer><\/script>
 *
 * It injects its own button, panel, CSS and behaviour. All settings persist
 * per-visitor in localStorage and re-apply on every page.
 *
 * Optional config — set BEFORE the script loads, or via data-* on the tag:
 *   <script src="accessibility-tool.js" data-accent="#1a237e" data-position="left" defer><\/script>
 *
 *   accent    Brand colour of the launcher + accents.   Default #1a237e
 *   position  'left' or 'right' bottom corner.           Default 'left'
 *   hide      true = no floating button (drive it via window.AccessibilityTool.open()).
 *
 * Public API:  window.AccessibilityTool.open() / .close() / .toggle() / .reset()
 */
(function () {
  'use strict';

  var BRAND = { name: 'Accessibility Tool', version: '1.0.0', origin: 'Built in India' };

  if (window.__a11yToolLoaded) return;      // guard against double-inclusion
  window.__a11yToolLoaded = true;

  var doc = document;
  var root = doc.documentElement;

  /* ---- read config (global object OR data-* on this script) --------------- */
  var cfg = window.ACCESSIBILITY_TOOL || window.RPJ_A11Y || window.NAVKAR_A11Y || {}; // legacy names accepted
  var me = doc.currentScript;
  if (me) {
    if (me.getAttribute('data-accent'))   cfg.accent = me.getAttribute('data-accent');
    if (me.getAttribute('data-position')) cfg.position = me.getAttribute('data-position');
    if (me.getAttribute('data-hide') === 'true') cfg.hide = true;
  }
  var ACCENT   = cfg.accent || '#1a237e';
  var POSITION = cfg.position === 'right' ? 'right' : 'left';
  var HIDE_FAB = !!cfg.hide;

  var STEP_KEY = 'a11y-tool-font';
  var FLAG_KEY = 'a11y-tool-flags';
  var MIN = -2, MAX = 4, PCT = 6;   // font step range and % per step

  /* ---------------------------- inline icons ------------------------------- */
  var I = {
    access: '<circle cx="12" cy="4" r="2"/><path d="M12 6v6m0 0 4 8m-4-8-4 8m-4-11h16"/>',
    close:  '<path d="M6 6l12 12M18 6L6 18"/>',
    contrast:'<circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 0 0 18z" fill="currentColor" stroke="none"/>',
    eyeoff: '<path d="M3 3l18 18M10.6 10.6a2 2 0 0 0 2.8 2.8M9.4 5.2A9.8 9.8 0 0 1 12 5c5 0 9 4.5 9 7a12 12 0 0 1-2.2 3M6.1 6.1C3.7 7.5 2 9.8 2 12c0 2.5 4 7 10 7a10 10 0 0 0 3.9-.8"/>',
    invert: '<circle cx="12" cy="12" r="9"/><path d="M12 3v18a9 9 0 0 0 0-18z" fill="currentColor" stroke="none"/>',
    link:   '<path d="M9 15l6-6M10.5 6.5l1.4-1.4a4 4 0 0 1 5.6 5.6l-1.4 1.4M13.5 17.5l-1.4 1.4a4 4 0 0 1-5.6-5.6l1.4-1.4"/>',
    text:   '<path d="M4 6h16M4 6V5m0 1v1M9 6v13M9 19H7m2 0h2M14 12h6m-6 0v-1m0 1v1m3-1v7m0 0h-2m2 0h2"/>',
    cursor: '<path d="M5 3l5 16 2.5-6.5L19 10 5 3z"/>',
    target: '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/>',
    ruler:  '<rect x="2" y="8" width="20" height="8" rx="1"/><path d="M6 8v3m4-3v4m4-4v3m4-3v4"/>',
    refresh:'<path d="M3 12a9 9 0 0 1 15-6.7L21 8M21 3v5h-5M21 12a9 9 0 0 1-15 6.7L3 16m0 5v-5h5"/>'
  };
  function svg(name, size) {
    return '<svg width="' + size + '" height="' + size + '" viewBox="0 0 24 24" fill="none" ' +
      'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" ' +
      'aria-hidden="true">' + I[name] + '</svg>';
  }

  /* ------------------------------ toggles ---------------------------------- */
  var TOGGLES = [
    { key: 'contrast',        icon: 'contrast', label: 'High contrast' },
    { key: 'grayscale',       icon: 'eyeoff',   label: 'Desaturate' },
    { key: 'invert',          icon: 'invert',   label: 'Invert colours' },
    { key: 'highlight-links', icon: 'link',     label: 'Highlight links' },
    { key: 'readable',        icon: 'text',     label: 'Readable font' },
    { key: 'big-cursor',      icon: 'cursor',   label: 'Big cursor' },
    { key: 'focus-highlight', icon: 'target',   label: 'Focus highlight' },
    { key: 'reading-guide',   icon: 'ruler',    label: 'Reading guide' }
  ];

  /* ------------------------------- state ----------------------------------- */
  var step = parseInt(localStorage.getItem(STEP_KEY) || '0', 10) || 0;
  var flags = {};
  try { flags = JSON.parse(localStorage.getItem(FLAG_KEY) || '{}') || {}; } catch (e) { flags = {}; }
  var guide = null;

  function save() {
    localStorage.setItem(STEP_KEY, String(step));
    localStorage.setItem(FLAG_KEY, JSON.stringify(flags));
  }

  function applyFont() {
    root.style.setProperty('font-size', (100 + step * PCT) + '%', 'important');
    var v = doc.querySelector('[data-at-fontval]');
    if (v) v.textContent = (100 + step * PCT) + '%';
  }
  function applyFlags() {
    root.classList.toggle('at-hc', !!flags['contrast']);
    root.classList.toggle('at-links', !!flags['highlight-links']);
    root.classList.toggle('at-readable', !!flags['readable']);
    root.classList.toggle('at-bigcursor', !!flags['big-cursor']);
    root.classList.toggle('at-focus', !!flags['focus-highlight']);
    root.classList.toggle('at-guide', !!flags['reading-guide']);
    var f = [];
    if (flags['grayscale']) f.push('grayscale(1)');
    if (flags['invert']) f.push('invert(1)');
    root.style.filter = f.join(' ');
    syncUI();
    ensureGuide();
  }
  function syncUI() {
    doc.querySelectorAll('[data-at-flag]').forEach(function (b) {
      b.setAttribute('aria-checked', flags[b.getAttribute('data-at-flag')] ? 'true' : 'false');
    });
  }
  function setStep(s) { step = Math.max(MIN, Math.min(MAX, s)); applyFont(); save(); }
  function toggleFlag(k) { flags[k] = !flags[k]; applyFlags(); save(); }
  function resetAll() { step = 0; flags = {}; applyFont(); applyFlags(); save(); }

  function moveGuide(e) { if (guide) guide.style.top = e.clientY + 'px'; }
  function ensureGuide() {
    if (flags['reading-guide'] && !guide) {
      guide = doc.createElement('div');
      guide.className = 'at-guidebar';
      doc.body.appendChild(guide);
      doc.addEventListener('mousemove', moveGuide, { passive: true });
    } else if (!flags['reading-guide'] && guide) {
      doc.removeEventListener('mousemove', moveGuide);
      guide.remove(); guide = null;
    }
  }

  /* ------------------------------- styles ---------------------------------- */
  var CSS =
  '.at-aw{position:fixed;' + POSITION + ':20px;bottom:20px;z-index:2147483000;' +
    'font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}' +
  '.at-fab{width:52px;height:52px;border-radius:50%;display:grid;place-items:center;' +
    'background:ACCENT;color:#fff;border:2px solid #fff;box-shadow:0 6px 20px rgba(0,0,0,.28);' +
    'cursor:pointer;transition:transform .2s}' +
  '.at-fab:hover,.at-fab:focus-visible{transform:scale(1.08);outline:none}' +
  '.at-panel{position:absolute;' + POSITION + ':0;bottom:calc(100% + 12px);width:min(20rem,calc(100vw - 40px));' +
    'max-height:min(35rem,calc(100vh - 96px));overflow-y:auto;background:#fff;color:#1a1a1a;' +
    'border:1px solid #e2e2e2;border-radius:14px;box-shadow:0 12px 40px rgba(0,0,0,.22);padding:16px}' +
  '.at-panel[hidden]{display:none}' +
  '.at-head{display:flex;align-items:center;justify-content:space-between;gap:8px;' +
    'padding-bottom:12px;border-bottom:1px solid #eee;margin-bottom:12px}' +
  '.at-head h2{display:flex;align-items:center;gap:7px;font-size:1.05rem;margin:0;color:ACCENT;font-weight:700}' +
  '.at-x{display:grid;place-items:center;width:32px;height:32px;border-radius:8px;background:#f4f4f6;' +
    'color:#333;border:1px solid #e2e2e2;cursor:pointer}' +
  '.at-x:hover{background:ACCENT;color:#fff}' +
  '.at-sec{font-size:.7rem;text-transform:uppercase;letter-spacing:.08em;color:#888;' +
    'font-weight:700;margin:14px 0 8px}.at-sec:first-child{margin-top:0}' +
  '.at-size{display:flex;align-items:center;gap:6px}' +
  '.at-size button{flex:1;min-height:40px;border:1px solid #e2e2e2;background:#f7f7f9;border-radius:8px;' +
    'font-weight:700;color:ACCENT;cursor:pointer;font-size:.95rem}' +
  '.at-size button:hover{background:ACCENT;color:#fff}' +
  '.at-size .at-reset-s{font-size:.78rem;flex:1.2}' +
  '.at-size .at-val{flex:1.2;text-align:center;font-weight:700;font-size:.9rem;color:#1a1a1a}' +
  '.at-tog{width:100%;display:flex;align-items:center;justify-content:space-between;gap:8px;' +
    'padding:9px 10px;margin-bottom:6px;border:1px solid #e2e2e2;border-radius:8px;background:#fff;' +
    'color:#1a1a1a;cursor:pointer;text-align:left;font-size:.92rem}' +
  '.at-tog:hover{border-color:ACCENT;background:#fafafa}' +
  '.at-tog .at-lbl{display:inline-flex;align-items:center;gap:8px;font-weight:500}' +
  '.at-tog .at-lbl svg{color:ACCENT;flex:none}' +
  '.at-sw{position:relative;flex:none;width:38px;height:22px;border-radius:999px;background:#ccc;transition:background .2s}' +
  '.at-sw::after{content:"";position:absolute;top:2px;left:2px;width:18px;height:18px;border-radius:50%;' +
    'background:#fff;transition:transform .2s;box-shadow:0 1px 3px rgba(0,0,0,.3)}' +
  '.at-tog[aria-checked="true"] .at-sw{background:#12b76a}' +
  '.at-tog[aria-checked="true"] .at-sw::after{transform:translateX(16px)}' +
  '.at-tog[aria-checked="true"]{border-color:#12b76a;background:#ecfdf3}' +
  '.at-resetall{width:100%;margin-top:8px;display:inline-flex;align-items:center;justify-content:center;gap:7px;' +
    'padding:10px;border-radius:8px;border:1px solid #d92d20;background:#fff5f5;color:#d92d20;font-weight:700;cursor:pointer}' +
  '.at-resetall:hover{background:#d92d20;color:#fff}' +
  '.at-foot{margin-top:12px;padding-top:10px;border-top:1px solid #eee;text-align:center;' +
    'font-size:.7rem;line-height:1.5;color:#9a9a9a}' +
  '.at-foot b{color:#666;font-weight:700}' +
  /* ---- the actual page adjustments ---- */
  'html.at-hc{filter:contrast(1.15)}html.at-hc body{background:#fff!important;color:#000!important}' +
  'html.at-hc a{color:#00309e!important;text-decoration:underline!important}' +
  'html.at-links a{text-decoration:underline!important;text-underline-offset:2px;outline:2px solid #ffbf00;' +
    'outline-offset:1px;background:#fffbe6!important;color:#1a237e!important}' +
  'html.at-readable,html.at-readable body{font-family:Verdana,Tahoma,"Segoe UI",Arial,sans-serif!important}' +
  'html.at-readable p,html.at-readable li,html.at-readable a,html.at-readable span,html.at-readable dd,' +
    'html.at-readable dt,html.at-readable label{letter-spacing:.02em!important;word-spacing:.08em!important;line-height:1.85!important}' +
  'html.at-bigcursor,html.at-bigcursor *{cursor:url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'48\' height=\'48\' viewBox=\'0 0 48 48\'%3E%3Cpath d=\'M8 4 8 40 18 30 25 45 31 42 24 27 38 27 8 4Z\' fill=\'%23000\' stroke=\'%23fff\' stroke-width=\'2\' stroke-linejoin=\'round\'/%3E%3C/svg%3E") 6 4,auto!important}' +
  'html.at-focus :focus{outline:4px solid #ff6a00!important;outline-offset:3px!important;border-radius:3px}' +
  '.at-guidebar{position:fixed;left:0;right:0;height:0;border-top:3px solid #ffbf00;' +
    'box-shadow:0 0 0 9999px rgba(17,22,79,.04);pointer-events:none;z-index:2147482000;display:none}' +
  'html.at-guide .at-guidebar{display:block}' +
  '@media (prefers-reduced-motion:reduce){.at-fab,.at-sw,.at-sw::after{transition:none}}';
  CSS = CSS.split('ACCENT').join(ACCENT);

  /* ------------------------------- build ----------------------------------- */
  function build() {
    var styleEl = doc.createElement('style');
    styleEl.id = 'at-style';
    styleEl.textContent = CSS;
    doc.head.appendChild(styleEl);

    var togHTML = TOGGLES.map(function (t) {
      return '<button class="at-tog" type="button" role="switch" aria-checked="false" data-at-flag="' + t.key + '">' +
        '<span class="at-lbl">' + svg(t.icon, 17) + ' ' + t.label + '</span>' +
        '<span class="at-sw" aria-hidden="true"></span></button>';
    }).join('');

    var wrap = doc.createElement('div');
    wrap.className = 'at-aw';
    wrap.setAttribute('data-at', '');
    wrap.innerHTML =
      (HIDE_FAB ? '' :
        '<button class="at-fab" type="button" aria-expanded="false" aria-controls="at-panel" ' +
        'aria-label="Open accessibility options" data-at-fab>' + svg('access', 28) + '</button>') +
      '<div class="at-panel" id="at-panel" role="dialog" aria-modal="true" aria-labelledby="at-title" hidden>' +
        '<div class="at-head"><h2 id="at-title">' + svg('access', 20) + ' Accessibility</h2>' +
          '<button class="at-x" type="button" aria-label="Close" data-at-close>' + svg('close', 18) + '</button></div>' +
        '<p class="at-sec">Text size</p>' +
        '<div class="at-size" role="group" aria-label="Text size">' +
          '<button type="button" data-at-font="dec" aria-label="Decrease text size">A&#8722;</button>' +
          '<span class="at-val" data-at-fontval aria-live="polite">100%</span>' +
          '<button type="button" data-at-font="inc" aria-label="Increase text size">A+</button>' +
          '<button type="button" class="at-reset-s" data-at-font="reset">Reset</button>' +
        '</div>' +
        '<p class="at-sec">Adjustments</p>' + togHTML +
        '<button class="at-resetall" type="button" data-at-resetall>' + svg('refresh', 16) + ' Reset all settings</button>' +
        '<div class="at-foot"><b>' + BRAND.name + '</b> &#183; v' + BRAND.version + '<br>' + BRAND.origin + ' &#127470;&#127475;</div>' +
      '</div>';
    doc.body.appendChild(wrap);

    var panel = wrap.querySelector('#at-panel');
    var fab = wrap.querySelector('[data-at-fab]');
    var lastFocus = null;

    function focusables() {
      return panel.querySelectorAll('button,[href],input,select,[tabindex]:not([tabindex="-1"])');
    }
    function onKey(e) {
      if (e.key === 'Escape') { close(); if (fab) fab.focus(); return; }
      if (e.key !== 'Tab') return;
      var f = focusables(); if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && doc.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && doc.activeElement === last) { e.preventDefault(); first.focus(); }
    }
    function onOutside(e) { if (!wrap.contains(e.target)) close(); }
    function open() {
      lastFocus = doc.activeElement;
      panel.hidden = false;
      if (fab) fab.setAttribute('aria-expanded', 'true');
      var f = focusables(); if (f.length) f[0].focus();
      doc.addEventListener('keydown', onKey);
      doc.addEventListener('click', onOutside, true);
    }
    function close() {
      panel.hidden = true;
      if (fab) fab.setAttribute('aria-expanded', 'false');
      doc.removeEventListener('keydown', onKey);
      doc.removeEventListener('click', onOutside, true);
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    if (fab) fab.addEventListener('click', function () { panel.hidden ? open() : close(); });
    wrap.querySelector('[data-at-close]').addEventListener('click', function () { close(); if (fab) fab.focus(); });
    wrap.querySelectorAll('[data-at-font]').forEach(function (b) {
      b.addEventListener('click', function () {
        var a = b.getAttribute('data-at-font');
        if (a === 'inc') setStep(step + 1); else if (a === 'dec') setStep(step - 1); else setStep(0);
      });
    });
    wrap.querySelectorAll('[data-at-flag]').forEach(function (b) {
      b.addEventListener('click', function () { toggleFlag(b.getAttribute('data-at-flag')); });
    });
    wrap.querySelector('[data-at-resetall]').addEventListener('click', resetAll);

    // public API (AccessibilityTool, plus legacy aliases)
    var api = {
      open: open, close: close,
      toggle: function () { panel.hidden ? open() : close(); },
      reset: resetAll,
      brand: BRAND
    };
    window.AccessibilityTool = api;
    window.RpjA11y = api;      // legacy aliases (safe to ignore)
    window.NavkarA11y = api;

    applyFont();
    applyFlags();
  }

  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', build);
  else build();
})();

