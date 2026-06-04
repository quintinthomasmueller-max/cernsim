// Phase-0-Sonde: beweist, dass das gebündelte Widget headless bootet und seine
// Interaktionen verdrahtet sind — genau die Klasse Fehler ("Regler gehen, Buttons
// nicht"), die uns in der Vorsession >10 Min gekostet hat, ist hier in ms prüfbar.
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { bootWidget, $ } from './helpers/boot.mjs';

describe('Widget bootet headless & verdrahtet Interaktionen', () => {
  let booted;
  beforeEach(() => { booted = bootWidget().booted; });

  it('bootet (Init lief durch, Listener attached)', () => {
    expect(booted).toBe(true);
  });

  it('Modus-Umschaltung: Didaktik ⟷ Reale Ansicht', () => {
    expect($('schematic').style.display).toBe('');
    expect($('geo-layer').style.display).toBe('none');
    $('btn-toggle-geo').click();
    expect($('schematic').style.display).toBe('none');
    expect($('geo-layer').style.display).toBe('');
    $('btn-toggle-geo').click();
    expect($('schematic').style.display).toBe('');
  });

  it('Preset QGP setzt die reale Pb-Pb-Energie (2.70 TeV/u)', () => {
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
