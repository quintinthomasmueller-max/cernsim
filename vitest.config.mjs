import { defineConfig } from 'vitest/config';

// Headless-Verifikation des Widgets in jsdom (kein Browser).
// Siehe docs/MIGRATION.md — Phase 0/3.
export default defineConfig({
  test: {
    environment: 'jsdom',
    include: ['tests/**/*.test.mjs'],
    watch: false,
  },
  resolve: {
    // vitest/Vite an esbuild angleichen: esbuild löst `import './x.js'` automatisch
    // auf x.ts auf, Vite NICHT. Nach der schrittweisen .js→.ts-Migration (Schritt 3)
    // scheitern sonst Tests, die Quelle direkt importieren. Fix: bei RELATIVEN
    // Importen die `.js`-Endung strippen → Vites Extension-Resolution findet .ts
    // (vorhandene .js bleiben .js). So funktionieren künftige Konversionen in BEIDEN
    // Toolchains, ohne ein einziges Import-Statement zu ändern.
    alias: [{ find: /^(\.{1,2}\/.*)\.js$/, replacement: '$1' }],
  },
});
