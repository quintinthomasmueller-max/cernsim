// Lädt das gebündelte Widget (build/widget_bundle.html) in jsdom und bootet es —
// mit minimalen Headless-Mocks (jsdom kennt weder Canvas-2D noch SVG-Geometrie noch rAF).
// Siehe docs/MIGRATION.md — Phase 0/3.
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..', '..');
const BUNDLE = resolve(ROOT, 'build/widget_bundle.html');

// Universeller, wurf-sicherer 2D-Context-Stub: jeder Property-Zugriff/Aufruf gibt
// denselben aufrufbaren Proxy zurück (Arithmetik → NaN, aber nie ein Throw).
function stubContext() {
  const p = new Proxy(function () { return p; }, {
    get: () => p, apply: () => p, set: () => true,
  });
  return p;
}

export function bootWidget() {
  const html = readFileSync(BUNDLE, 'utf8');
  const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
  if (!scriptMatch) throw new Error('Kein <script> im Bundle gefunden');
  const js = scriptMatch[1];
  const markup = html
    .replace(/^[\s\S]*?<body>/, '')
    .replace(/<\/body>[\s\S]*$/, '')
    .replace(/<script>[\s\S]*?<\/script>/, '');

  document.body.innerHTML = markup;

  // jsdom kennt kein innerText (nur textContent) — das Widget nutzt aber überall
  // element.innerText für Readouts. Mappen, damit Assertions greifen.
  if (!Object.getOwnPropertyDescriptor(window.HTMLElement.prototype, 'innerText')) {
    Object.defineProperty(window.HTMLElement.prototype, 'innerText', {
      get() { return this.textContent; },
      set(v) { this.textContent = v; },
      configurable: true,
    });
  }

  globalThis.requestAnimationFrame = () => 0;
  globalThis.cancelAnimationFrame = () => {};
  window.requestAnimationFrame = globalThis.requestAnimationFrame;
  window.cancelAnimationFrame = globalThis.cancelAnimationFrame;
  if (!window.devicePixelRatio) window.devicePixelRatio = 1;
  HTMLCanvasElement.prototype.getContext = () => stubContext();
  const svgProto = window.SVGElement && window.SVGElement.prototype;
  if (svgProto) {
    svgProto.getTotalLength = () => 100;
    svgProto.getPointAtLength = () => ({ x: 0, y: 0 });
  }

  // new Function => eigener Scope pro Aufruf (kein const-Redeclare zwischen Tests).
  // Der Bootstrap im Bundle ruft __cernInit erst auf, wenn der Widget-DOM da ist.
  new Function(js)();

  const root = document.getElementById('cern-v4');
  return { root, booted: !!(root && root.__cernBooted) };
}

export const $ = (id) => document.getElementById(id);
