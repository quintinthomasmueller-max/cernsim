import { defineConfig } from 'vitest/config';

// Headless-Verifikation des Widgets in jsdom (kein Browser).
// Siehe docs/MIGRATION.md — Phase 0/3.
export default defineConfig({
  test: {
    environment: 'jsdom',
    include: ['tests/**/*.test.mjs'],
    watch: false,
  },
});
