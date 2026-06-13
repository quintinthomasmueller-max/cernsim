// Build des Stellwerk-Widgets: ES-Module (cern/app/src/) → ein IIFE-Bundle.
// Siehe docs/MIGRATION.md (Phase 1). Aufruf: `npm run build`.
import { build } from 'esbuild';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const APP = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(APP, '..', '..');

// Datenblob: src/data.gen.js ist DIE eine Quelle (ES-Modul, von scripts/build_data.py
// generiert + von gen_constants.py gepflegt) — der frühere const→export-Spiegel
// aus cern/app/data.js ist entfallen.

await build({
  entryPoints: [resolve(APP, 'src', 'main.ts')],
  bundle: true,
  format: 'iife',
  outfile: resolve(ROOT, 'build', 'app.bundle.js'),
  target: 'es2020',
  legalComments: 'none',
  logLevel: 'info',
});

console.log('esbuild OK → build/app.bundle.js');
