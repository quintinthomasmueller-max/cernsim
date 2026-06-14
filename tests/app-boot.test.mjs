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

  it('Modus-Umschaltung: Didaktik ⟷ Reale Ansicht', () => {
    // Start = Didaktik: Schema sichtbar, Geo-Layer aus
    expect($('schematic').style.display).toBe('');
    expect($('geo-layer').style.display).toBe('none');
    $('btn-toggle-geo').click();   // → Reale Ansicht
    expect($('schematic').style.display).toBe('none');
    expect($('geo-layer').style.display).toBe('');
    $('btn-toggle-geo').click();   // → zurück zu Didaktik
    expect($('schematic').style.display).toBe('');
    expect($('geo-layer').style.display).toBe('none');
  });

  it('Preset QGP setzt die reale Pb-Pb-Energie (2,70 TeV/Nukleon)', () => {
    $('btn-pre-qgp').click();
    expect($('lbl-energy').textContent).toMatch(/2[.,]7\d*\s*TeV/);
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
