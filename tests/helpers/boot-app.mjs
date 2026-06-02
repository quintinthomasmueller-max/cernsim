// Lädt das esbuild-Bundle (build/app.bundle.js, Phase-1-Architektur) + shell.html-
// Markup in jsdom und bootet es — mit denselben Headless-Mocks wie boot.mjs
// (jsdom kennt weder Canvas-2D noch SVG-Geometrie noch rAF).
// Siehe docs/MIGRATION.md — Phase 1/3.
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..', '..');
const BUNDLE = resolve(ROOT, 'build/app.bundle.js');
const SHELL = resolve(ROOT, 'cern/app/shell.html');

// Wurf-sicherer 2D-Context-Stub: jeder Zugriff/Aufruf gibt denselben Proxy zurück.
function stubContext() {
  const p = new Proxy(function () { return p; }, {
    get: () => p, apply: () => p, set: () => true,
  });
  return p;
}

export function bootApp() {
  const js = readFileSync(BUNDLE, 'utf8');
  const markup = readFileSync(SHELL, 'utf8')
    .replace('{{STYLES}}', '')
    .replace('{{SCRIPT}}', '');

  document.body.innerHTML = markup;

  // jsdom kennt kein innerText (nur textContent) — das Widget nutzt innerText.
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

  // new Function => eigener Scope pro Aufruf (IIFE-Bundle, bootet selbst bei DOM-Ready).
  new Function(js)();

  const root = document.getElementById('cern-v4');
  return { root, booted: !!(root && root.__cernBooted) };
}

export const $ = (id) => document.getElementById(id);
