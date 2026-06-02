// Phase-1-Sonde: beweist, dass das esbuild-Bundle (ES-Module → IIFE) headless
// bootet und dieselben Interaktionen verdrahtet wie das Legacy-Bundle. Spiegelt
// widget-boot.test.mjs, lädt aber build/app.bundle.js statt build/widget_bundle.html.
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { bootApp, $ } from './helpers/boot-app.mjs';

describe('esbuild-App bootet headless & verdrahtet Interaktionen', () => {
  let booted;
  beforeEach(() => { booted = bootApp().booted; });

  it('bootet (Init lief durch, Listener attached)', () => {
    expect(booted).toBe(true);
  });

  it('Geo-Overlay-Button graut aus und wieder zurück', () => {
    const svg = $('svg');
    $('btn-toggle-geo').click();
    expect(svg.classList.contains('geo-dimmed')).toBe(true);
    $('btn-toggle-geo').click();
    expect(svg.classList.contains('geo-dimmed')).toBe(false);
  });

  it('Preset QGP setzt die Ziel-Energie (2.5 TeV)', () => {
    $('btn-pre-qgp').click();
    expect($('lbl-energy').textContent).toMatch(/2[.,]5\s*TeV/);
  });

  it('Detektor-Tab (LHCb) wird aktiv', () => {
    $('dt-lhcb').click();
    expect($('dt-lhcb').classList.contains('act')).toBe(true);
  });

  it('Füll-Button startet das Protokoll (Button wird deaktiviert)', () => {
    vi.useFakeTimers();
    try {
      $('btn-auto').click();
      expect($('btn-auto').classList.contains('off')).toBe(true);
    } finally {
      vi.clearAllTimers();
      vi.useRealTimers();
    }
  });
});
