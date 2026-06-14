// build_pages.mjs — baut die selbstständige Simulator-Seite für GitHub Pages.
//
// Node-only (kein Python/pandas nötig: data.gen.js/geo.gen.js/sat.gen.js sind
// versioniert). Spiegelt build_share() aus scripts/sync_widget.py, schreibt aber
// statt ins Notebook eine fertige _site/index.html (CSS+JS inline, self-contained).
//
// Aufruf: `node scripts/build_pages.mjs`  →  _site/index.html
import { build } from 'esbuild';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(HERE, '..');
const APP = resolve(ROOT, 'cern', 'app');
const OUT = resolve(ROOT, '_site');

// 1) ES-Module → ein IIFE-Bundle (in-memory, kein Schreiben nach build/).
const result = await build({
  entryPoints: [resolve(APP, 'src', 'main.ts')],
  bundle: true,
  format: 'iife',
  target: 'es2020',
  legalComments: 'none',
  write: false,
  logLevel: 'info',
});
const js = result.outputFiles[0].text;

// 2) Shell + CSS inline (self-contained, wie build_inner()).
const shell = readFileSync(resolve(APP, 'shell.html'), 'utf8');
const css = readFileSync(resolve(APP, 'styles.css'), 'utf8');
const inner = shell
  .replace('{{STYLES}}', '<style>' + css + '</style>')
  .replace('{{SCRIPT}}', '<script>' + js + '</script>');

// 3) Mobil-/Web-taugliches Dokument (Notch, Theme-Color, „Zum Startbildschirm",
//    Emoji-Favicon ohne externe Datei) — identisch zu sync_widget.build_share().
const icon =
  "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' " +
  "viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%E2%9A%9B%EF%B8%8F%3C/text%3E%3C/svg%3E";
const html =
  '<!doctype html><html lang="de"><head><meta charset="utf-8">' +
  '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">' +
  '<meta name="theme-color" content="#131a24">' +
  '<meta name="description" content="Interaktives Modell des CERN-Beschleunigerkomplexes — ' +
  'Füllen, Rampen, Squeeze, Kollidieren mit echten CMS-Open-Data.">' +
  '<meta name="apple-mobile-web-app-capable" content="yes">' +
  '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">' +
  '<meta name="apple-mobile-web-app-title" content="CERN-Schaltzentrale">' +
  '<link rel="icon" href="' + icon + '">' +
  '<title>CERN-Schaltzentrale — interaktives Modell</title>' +
  '<style>html,body{margin:0;background:#131a24}</style></head><body>' +
  inner +
  '</body></html>';

mkdirSync(OUT, { recursive: true });
writeFileSync(resolve(OUT, 'index.html'), html);
// .nojekyll: GitHub Pages soll die Datei roh ausliefern (kein Jekyll-Processing).
writeFileSync(resolve(OUT, '.nojekyll'), '');

console.log('build_pages OK → _site/index.html (' + html.length.toLocaleString() + ' B)');
