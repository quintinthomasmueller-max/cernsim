// Build des Stellwerk-Widgets: ES-Module (cern/app/src/) → ein IIFE-Bundle.
// Siehe docs/MIGRATION.md (Phase 1). Aufruf: `npm run build`.
import { build } from 'esbuild';
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const APP = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(APP, '..', '..');

// Datenblob (cern/app/data.js, von gen_constants gepflegt) ESM-fähig spiegeln,
// OHNE den ~37-KB-Blob manuell anzufassen: `const CERN_REAL` → `export const CERN_REAL`.
function genData() {
  const src = readFileSync(resolve(APP, 'data.js'), 'utf8');
  const esm = src.replace(/(^|\n)\s*const\s+CERN_REAL/, '$1export const CERN_REAL');
  writeFileSync(resolve(APP, 'src', 'data.gen.js'), esm);
}

genData();

await build({
  entryPoints: [resolve(APP, 'src', 'main.js')],
  bundle: true,
  format: 'iife',
  outfile: resolve(ROOT, 'build', 'app.bundle.js'),
  target: 'es2020',
  legalComments: 'none',
  logLevel: 'info',
});

console.log('esbuild OK → build/app.bundle.js');
