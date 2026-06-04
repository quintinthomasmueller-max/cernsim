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
  s.selDet = 'ATLAS';        // Z⁰-Schwelle 0.9 TeV, target = 200, channel = 2mu (Faktor 5)
  s.isIon = false;
  s.paramEnergy = 6.8;       // weit über allen Schwellen → prodVis = 1
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
  it('= 0 bei Energie unter Erzeugungs-Schwelle', () => {
    s.collStore.ATLAS = 200; s.paramEnergy = 0.5;  // < Z⁰-Schwelle 0.9 TeV → nicht erzeugbar
    expect(App.getSignificance()).toBe(0);
  });
  it('= 0 ohne Kollisionen', () => {
    expect(App.getSignificance()).toBe(0);
  });
});

describe('Energie formt das Spektrum (Erzeugungs-Schwellen)', () => {
  it('CMS-Higgs braucht nahezu volle Energie (Schwelle 5.5 TeV)', () => {
    s.selDet = 'CMS'; s.collStore.CMS = 600;     // = target
    s.paramEnergy = 2.5; expect(App.getSignificance()).toBe(0);            // unter Schwelle → kein Higgs
    s.paramEnergy = 6.8; expect(App.getSignificance()).toBeGreaterThan(4); // voll erzeugbar
  });
  it('Signifikanz steigt monoton mit der Energie über der Schwelle', () => {
    s.selDet = 'ATLAS'; s.collStore.ATLAS = 200;
    s.paramEnergy = 0.9; const a = App.getSignificance();   // genau an der Schwelle → 0
    s.paramEnergy = 1.1; const b = App.getSignificance();
    s.paramEnergy = 2.0; const c = App.getSignificance();
    expect(a).toBe(0);
    expect(b).toBeGreaterThan(0);
    expect(c).toBeGreaterThan(b);
  });
});

describe('Entdeckung hängt vom Strahl-Programm ab (Preset × Detektor)', () => {
  it('CMS-Higgs ist im Pb-Pb-Lauf (QGP-Preset) NICHT entdeckbar — auch bei voller Energie/Statistik', () => {
    s.selDet = 'CMS'; s.collStore.CMS = 600; s.paramEnergy = 6.8;
    s.isIon = true;  expect(App.getSignificance()).toBe(0);             // Pb-Pb-Lauf → kein Higgs
    s.isIon = false; expect(App.getSignificance()).toBeGreaterThan(4);  // pp-Lauf → entdeckbar
  });
  it('ALICE-QGP braucht Blei-Ionen — in p-p nur Referenz, keine Entdeckung', () => {
    s.selDet = 'ALICE'; s.collStore.ALICE = 300; s.paramEnergy = 2.5;
    s.isIon = false; expect(App.getSignificance()).toBe(0);             // p-p → keine QGP-Entdeckung
    s.isIon = true;  expect(App.getSignificance()).toBeGreaterThan(4);  // Pb-Pb → entdeckbar
  });
  it('ATLAS-Z⁰ ist die QGP-blinde Standardkerze — in pp UND Pb-Pb messbar', () => {
    s.selDet = 'ATLAS'; s.collStore.ATLAS = 200; s.paramEnergy = 6.8;
    s.isIon = false; expect(App.getSignificance()).toBeCloseTo(5.0, 6);
    s.isIon = true;  expect(App.getSignificance()).toBeCloseTo(5.0, 6);  // Z⁰ koppelt nicht ans QGP
  });
  it('LHCb-CP (B⁰) ist nur im pp-Lauf entdeckbar, nicht in Pb-Pb', () => {
    s.selDet = 'LHCB'; s.collStore.LHCB = 400; s.paramEnergy = 6.5;
    s.isIon = false; expect(App.getSignificance()).toBeGreaterThan(4);
    s.isIon = true;  expect(App.getSignificance()).toBe(0);
  });
});

describe('QGP: Quarkonia-Unterdrückung im Ionen-Modus', () => {
  // Anteil der J/ψ-Fenster-Events am ALICE-Spektrum (statistisch, große N).
  function jpsiFraction(ion) {
    App.resetSpectrumData();
    s.selDet = 'ALICE'; s.isIon = ion; s.paramEnergy = 2.5;   // J/ψ erzeugbar (Schwelle 0.4)
    s.paramIntensity = 2.0; s.paramBetaStar = 0.3;            // viele Events pro Kollision
    for (let i = 0; i < 250; i++) App.generateMassData();
    const data = s.massStore.ALICE;
    const inJ = data.filter(m => Math.abs(m - 3.097) <= 0.5).length;
    return inJ / data.length;
  }
  it('Pb-Pb unterdrückt den J/ψ-Peak gegenüber p-p', () => {
    const pp  = jpsiFraction(false);
    const PbPb = jpsiFraction(true);
    expect(pp).toBeGreaterThan(0.1);          // p-p: klarer J/ψ-Peak
    expect(PbPb).toBeLessThan(pp * 0.85);     // Pb-Pb: deutlich unterdrückt (QGP-Schmelzen)
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
