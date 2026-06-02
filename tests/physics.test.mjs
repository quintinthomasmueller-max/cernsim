// Phase-3-Physik-Logik (headless, ohne DOM/Browser): importiert die ES-Module
// direkt und prüft die auf `App` registrierten reinen Funktionen. Deckt die
// didaktischen Kernzusammenhänge ab (Signifikanz ∝ √N, Rate ∝ Intensität²/β*,
// Klassifikation trifft PDG-Fenster) — deterministisch, in Millisekunden.
import { describe, it, expect, beforeEach } from 'vitest';
import { App } from '../cern/app/src/core.js';
import '../cern/app/src/state.js';     // füllt App.state
import '../cern/app/src/spectrum.js';  // registriert getSignificance/classify/generateMassData/…

const s = App.state;

beforeEach(() => {
  App.resetSpectrumData();
  s.selDet = 'ATLAS';        // minE = 1.0 TeV, target = 200, channel = 2mu (Faktor 5)
  s.paramEnergy = 6.8;
  s.paramIntensity = 1.0;
  s.paramBetaStar = 1.0;
});

describe('Signifikanz ∝ √N', () => {
  it('verdoppelt sich bei 4× Statistik', () => {
    s.collStore.ATLAS = 50;  const a = App.getSignificance();
    s.collStore.ATLAS = 200; const b = App.getSignificance();
    expect(a).toBeGreaterThan(0);
    expect(b / a).toBeCloseTo(2, 5);
  });
  it('folgt 5·√(N/target)', () => {
    s.collStore.ATLAS = 200;             // = target → exakt 5σ
    expect(App.getSignificance()).toBeCloseTo(5.0, 6);
  });
  it('= 0 bei Energie unter Detektor-Schwelle', () => {
    s.collStore.ATLAS = 200; s.paramEnergy = 0.5;  // < minE 1.0
    expect(App.getSignificance()).toBe(0);
  });
  it('= 0 ohne Kollisionen', () => {
    expect(App.getSignificance()).toBe(0);
  });
});

describe('Datenrate ∝ Intensität² / β*', () => {
  // generateMassData pusht n = max(1, round(I²/max(0.3,β*) · 5)) Pool-Events
  // + 1 angezeigtes Event in massStore[selDet]; der Zuwachs ist deterministisch.
  function grow(intensity, beta) {
    App.resetSpectrumData();
    s.paramIntensity = intensity; s.paramBetaStar = beta;
    const before = s.massStore.ATLAS.length;
    App.generateMassData();
    return s.massStore.ATLAS.length - before;
  }
  it('skaliert quadratisch mit der Intensität', () => {
    expect(grow(1.0, 1.0)).toBe(6);   // n=round(1·5)=5  (+1)
    expect(grow(2.0, 1.0)).toBe(21);  // n=round(4·5)=20 (+1)
  });
  it('steigt bei kleinerem β* (stärkere Fokussierung)', () => {
    const tight = grow(1.0, 0.5);     // rate 2  → n=10 (+1)=11
    const wide  = grow(1.0, 1.5);     // rate .67 → n=3  (+1)=4
    expect(tight).toBeGreaterThan(wide);
  });
});

describe('Klassifikation trifft PDG-Fenster', () => {
  it('Z⁰ bei 91.19 GeV', () => expect(App.classify(91.19)).toBe('Z0'));
  it('J/ψ bei 3.097 GeV', () => expect(App.classify(3.097)).toBe('J/psi'));
  it('Υ bei 9.46 GeV', () => expect(App.classify(9.46)).toBe('Upsilon'));
  it('Untergrund (45 GeV, kein Peak) → null', () => expect(App.classify(45)).toBe(null));
  it('Higgs-Kanal (4ℓ) wird NICHT als Dimuon-Resonanz klassifiziert', () =>
    expect(App.classify(125.0)).toBe(null));
});
