// Phase-3-Physik-Logik (headless, ohne DOM/Browser): importiert die ES-Module
// direkt und prüft die auf `App` registrierten reinen Funktionen. Deckt die
// didaktischen Kernzusammenhänge ab (Signifikanz ∝ √N, Rate ∝ Intensität²/β*,
// Klassifikation trifft PDG-Fenster) — deterministisch, in Millisekunden.
import { describe, it, expect, beforeEach } from 'vitest';
import { App, STAT_RATE, DT_SCALE, BEAM_LIFETIME_H, DUMP_FRAC } from '../cern/app/src/core.js';
import '../cern/app/src/state.js';     // füllt App.state
import '../cern/app/src/spectrum.js';  // registriert getSignificance/classify/generateMassData/…
import { CERN_REAL } from '../cern/app/src/data.gen.js';   // generierter Echtdaten-Blob

const s = App.state;

beforeEach(() => {
  App.resetSpectrumData();
  s.selDet = 'ATLAS';        // Z⁰-Schwelle 0.9 TeV, target = 200, channel = 2mu (Faktor 5)
  s.isIon = false;
  s.paramEnergy = 6.8;       // Arbeitspunkt weit über allen Schwellen → prodVis = 1
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
    s.collStore.ATLAS = 300;             // = target → exakt 5σ
    expect(App.getSignificance()).toBeCloseTo(5.0, 6);
  });
  it('= 0 bei Energie unter Erzeugungs-Schwelle', () => {
    s.collStore.ATLAS = 300; s.paramEnergy = 0.5;  // < Z⁰-Schwelle 0.9 TeV → nicht erzeugbar
    expect(App.getSignificance()).toBe(0);
  });
  it('= 0 ohne Kollisionen', () => {
    expect(App.getSignificance()).toBe(0);
  });
});

describe('Energie formt das Spektrum (Erzeugungs-Schwellen)', () => {
  it('CMS-Higgs: Raten-Schwelle 3.5 TeV/Strahl (2012 bei 4 TeV/Strahl entdeckt!)', () => {
    s.selDet = 'CMS'; s.collStore.CMS = 600;     // viel Statistik
    s.paramEnergy = 2.5; expect(App.getSignificance()).toBe(0);            // unter Schwelle → kein Higgs
    s.paramEnergy = 4.0; const e2012 = App.getSignificance();
    expect(e2012).toBeGreaterThan(0);            // historisch ehrlich: bei √s=8 TeV produzierbar
    s.paramEnergy = 6.8; expect(App.getSignificance()).toBeGreaterThan(e2012); // volle Rate Run 3
  });
  it('Signifikanz hängt am Arbeitspunkt, nicht an der Momentan-Energie (Mehr-Fill-Entdeckung überlebt den Strahl-Dump)', () => {
    // Arbeitspunkt pp = paramEnergy 6,8 TeV; während der Datennahme gilt lhcEnergy = 6800.
    s.selDet = 'ATLAS'; s.collStore.ATLAS = 400; s.paramEnergy = 6.8;
    s.lhcEnergy = 6800; const taking = App.getSignificance();
    expect(taking).toBeGreaterThan(4);
    // Strahl-Dump zwischen zwei Füllungen: lhcEnergy fällt auf Injektion (450), die DATEN
    // bleiben erhalten (resetLHC keepData). Die erreichte Signifikanz darf NICHT auf 0
    // zurückfallen — sonst zerstörte ein momentaner Energie-Bezug die Mehr-Fill-Entdeckung.
    s.lhcEnergy = 450;
    expect(App.getSignificance()).toBeCloseTo(taking, 6);
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

describe('Physik-Matrix: jeder Detektor misst, was im AKTUELLEN Strahl real möglich ist', () => {
  it('ATLAS-Z⁰ ist die QGP-blinde Standardkerze — entdeckbar in pp UND Pb-Pb', () => {
    s.selDet = 'ATLAS'; s.collStore.ATLAS = 400; s.paramEnergy = 6.8;
    s.isIon = false; expect(App.getSignificance()).toBeGreaterThan(4);   // pp
    s.isIon = true;  expect(App.getSignificance()).toBeGreaterThan(4);   // Pb-Pb (EW-blind fürs QGP)
  });
  it('CMS misst in pp den Higgs (Raten-Schwelle 3.5 TeV), in Pb-Pb dagegen die Υ-Unterdrückung (Schwelle ~0.6 TeV)', () => {
    s.selDet = 'CMS'; s.collStore.CMS = 300;
    // pp = Higgs-Goldkanal: Rate steigt steil mit der Energie
    s.isIon = false; s.paramEnergy = 3.0; expect(App.getSignificance()).toBe(0);            // < 3.5 TeV → Rate ~0
    s.isIon = false; s.paramEnergy = 6.8; expect(App.getSignificance()).toBeGreaterThan(4); // Higgs erzeugbar
    // Pb-Pb = Υ-Sequenzunterdrückung: schon bei Schwerionen-Energie messbar
    s.isIon = true;  s.paramEnergy = 2.7; expect(App.getSignificance()).toBeGreaterThan(4);
  });
  it('ALICE p-p ist Referenz (misst, bleibt aber < 5σ); Pb-Pb erreicht die QGP-Entdeckung', () => {
    s.selDet = 'ALICE'; s.paramEnergy = 2.7; s.collStore.ALICE = 2000;   // viel Statistik
    s.isIon = false; const ref = App.getSignificance();
    expect(ref).toBeGreaterThan(0);    // misst das Vakuum-Referenzspektrum
    expect(ref).toBeLessThan(5);       // aber KEINE Entdeckung (gedeckelt — QGP braucht Pb-Pb)
    s.isIon = true;  expect(App.getSignificance()).toBeGreaterThanOrEqual(5);  // Pb-Pb → QGP-Entdeckung
  });
  it('LHCb: CP-Verletzung nur im pp-Lauf; im Pb-Pb-Lauf spezialisiert → keine Standard-Entdeckung (0σ)', () => {
    s.selDet = 'LHCB'; s.collStore.LHCB = 400; s.paramEnergy = 6.5;
    s.isIon = false; expect(App.getSignificance()).toBeGreaterThan(4);
    s.isIon = true;  expect(App.getSignificance()).toBe(0);              // disco:false (Vorwärts/SMOG)
  });
});

describe('Gleichzeitige Datennahme: alle Experimente nehmen denselben Fill auf', () => {
  it('liveDetectors() liefert alle vier Detektoren', () => {
    expect(App.liveDetectors().sort()).toEqual(['ALICE', 'ATLAS', 'CMS', 'LHCB']);
  });
  it('seltener Kanal (Higgs) akkumuliert deutlich langsamer als häufiger (Z⁰)', () => {
    s.isIon = false;
    expect(App.detRate('CMS')).toBeLessThan(App.detRate('ATLAS'));   // Higgs selten
    expect(App.detRate('ALICE')).toBeGreaterThan(App.detRate('CMS'));
  });
  it('ein Tick erhöht ALLE Detektoren-Kandidaten gleichzeitig (parallel)', () => {
    App.resetSpectrumData(); s.isIon = false;
    const dCand = (d) => STAT_RATE * 1.0 * 100 * App.detRate(d);   // L=1, dReal=100
    App.liveDetectors().forEach(d => { s.collStore[d] += dCand(d); });
    for (const d of ['ATLAS', 'CMS', 'ALICE', 'LHCB']) expect(s.collStore[d]).toBeGreaterThan(0);
    expect(s.collStore.ATLAS).toBeGreaterThan(s.collStore.CMS);     // Z⁰ häufiger als Higgs
  });
});

describe('Strahlwahl formt die Balken (nicht nur Text)', () => {
  // füllt massStore[det] für (Strahl, Energie) und liefert den Peak-Anteil im Fenster
  function peakFrac(det, ion, energyTeV, center, hw) {
    App.resetSpectrumData();
    s.selDet = det; s.isIon = ion; s.paramEnergy = energyTeV;
    s.paramIntensity = 1.5; s.paramBetaStar = 0.5;
    for (let i = 0; i < 3000; i++) App.accumulateStatsFor(det, 1);
    const data = s.massStore[det];
    return data.filter(m => Math.abs(m - center) <= hw).length / Math.max(1, data.length);
  }
  it('ATLAS-Z⁰ ist die Standardkerze: pp und Pb-Pb zeigen DENSELBEN Peak (EW-blind, gewollt)', () => {
    const pp = peakFrac('ATLAS', false, 6.8, 91.19, 6);
    const pb = peakFrac('ATLAS', true, 2.7, 91.19, 6);
    expect(pp).toBeGreaterThan(0.5);            // klarer Z⁰-Peak
    expect(pb / pp).toBeGreaterThan(0.9);       // in Pb-Pb unverändert (Standardkerze)
    expect(pb / pp).toBeLessThan(1.1);
  });
  it('LHCb zeigt den B⁰-Peak NUR in pp; im Pb-Pb-Lauf (spezialisiert) bleibt nur Untergrund', () => {
    const pp = peakFrac('LHCB', false, 6.8, 5.279, 0.18);
    const pb = peakFrac('LHCB', true, 2.7, 5.279, 0.18);
    expect(pp).toBeGreaterThan(0.5);            // pp: klarer B⁰-Peak
    expect(pb).toBeLessThan(0.35);              // Pb-Pb: flacher Untergrund (kein Peak)
    expect(pp).toBeGreaterThan(pb * 1.7);       // sichtbar unterschiedliche Balken
  });
});

describe('QGP: Quarkonia-Unterdrückung im Ionen-Modus', () => {
  // R_AA-Metrik: PEAK-zu-KONTINUUM-Verhältnis (das Rejection-Sampling hält das
  // Kontinuum fest und senkt nur die Peak-Ausbeute — wie die echte Messung).
  function jpsiToCont(ion) {
    App.resetSpectrumData();
    s.selDet = 'ALICE'; s.isIon = ion; s.paramEnergy = 2.5;   // J/ψ erzeugbar (Schwelle 0.4)
    s.paramIntensity = 2.0; s.paramBetaStar = 0.3;            // viele Events pro Kollision
    for (let i = 0; i < 250; i++) App.generateMassData();
    const data = s.massStore.ALICE;
    const peak = data.filter(m => Math.abs(m - 3.097) <= 0.35).length;
    const cont = data.filter(m => (m > 1.5 && m < 2.5) || (m > 4.2 && m < 8.5)).length;
    return peak / Math.max(1, cont);
  }
  it('Pb-Pb unterdrückt den J/ψ-Peak relativ zum Kontinuum (R_AA < 1)', () => {
    const pp   = jpsiToCont(false);
    const PbPb = jpsiToCont(true);
    expect(pp).toBeGreaterThan(0.2);          // p-p: klarer J/ψ-Peak über dem Kontinuum
    expect(PbPb).toBeLessThan(pp * 0.8);      // Pb-Pb: R_AA = 0.6 modelliert (± Statistik)
  });
});

describe('Spektrum-Kurve passt zu den echten Daten (χ²-Formvergleich)', () => {
  // Gewichtetes POOL-Histogramm (Gewicht = Überlebens-W'keit je Event) gegen die
  // gezeichnete Kurve App.fitValFor — exakt das, was drawHist malt. Fehler aus
  // Pool-Zählung (gewichtetes Poisson). Vor der Daten-Kalibrierung: χ²/ndf 14–157.
  function chi2ndf(det, ion, E, pool, range, bins, windows) {
    s.selDet = det; s.isIon = ion; s.paramEnergy = E;
    const [mn, mx] = range;
    const wOf = m => { for (const [c, hw, w] of windows) if (Math.abs(m - c) <= hw) return w; return 1; };
    const binsD = Array(bins).fill(0), binsW2 = Array(bins).fill(0), model = Array(bins).fill(0);
    pool.forEach(m => {
      if (m < mn || m >= mx) return;
      const i = Math.floor((m - mn) / (mx - mn) * bins);
      const w = wOf(m); binsD[i] += w; binsW2[i] += w * w;
    });
    for (let i = 0; i < bins; i++) model[i] = App.fitValFor(det, mn + (i + 0.5) / bins * (mx - mn));
    const sumD = binsD.reduce((a, b) => a + b, 0), sumM = model.reduce((a, b) => a + b, 0);
    let chi2 = 0, ndf = 0;
    for (let i = 0; i < bins; i++) {
      const mi = model[i] / sumM * sumD;
      if (mi < 1.5 && binsD[i] < 1.5) continue;
      chi2 += (binsD[i] - mi) ** 2 / Math.max(binsW2[i], mi, 0.5); ndf++;
    }
    return chi2 / Math.max(1, ndf);
  }
  it('ATLAS p-p (Z⁰): Kurve folgt den echten μμ-Daten', () => {
    expect(chi2ndf('ATLAS', false, 6.8, CERN_REAL.pp, [50, 150], 60, [])).toBeLessThan(3);
  });
  it('CMS p-p (4ℓ): Kurve folgt den echten 4ℓ-Kandidaten inkl. ZZ-Schulter', () => {
    expect(chi2ndf('CMS', false, 6.8, CERN_REAL.higgs4l, [80, 200], 60, [])).toBeLessThan(3);
  });
  it('CMS Pb-Pb (Υ): Kurve folgt den R_AA-gewichteten Daten', () => {
    const win = [[9.46, 0.40, 0.45], [10.02, 0.28, 0.12], [10.36, 0.26, 0.02]];
    expect(chi2ndf('CMS', true, 2.7, CERN_REAL.ion, [7, 12], 50, win)).toBeLessThan(3);
  });
});

describe('Nullhypothese-Overlay (Erwartung ohne Signal)', () => {
  it('CMS p-p: „ohne Higgs" liegt im 125-Fenster UNTER dem Modell, außerhalb identisch', () => {
    s.selDet = 'CMS'; s.isIon = false; s.paramEnergy = 6.8;
    expect(App.nullValFor('CMS', 125)).toBeLessThan(App.fitValFor('CMS', 125) * 0.5);
    expect(App.nullValFor('CMS', 160)).toBeCloseTo(App.fitValFor('CMS', 160), 9);
  });
  it('CMS Pb-Pb: „ohne QGP" zeigt den VOLLEN Υ-Peak über dem unterdrückten Modell', () => {
    s.selDet = 'CMS'; s.isIon = true; s.paramEnergy = 2.7;
    expect(App.nullValFor('CMS', 9.46)).toBeGreaterThan(App.fitValFor('CMS', 9.46) * 1.5);
  });
});

describe('Energie-Gating: unterdrückte Events bleiben ECHTES Kontinuum', () => {
  it('Pilot (0,45 TeV): ATLAS-Spektrum fällt (kein Uniform-Plateau aus Re-Smear)', () => {
    s.selDet = 'ATLAS'; s.isIon = false; s.paramEnergy = 0.45;
    s.paramIntensity = 2.0; s.paramBetaStar = 0.3;
    for (let i = 0; i < 200; i++) App.generateMassData();
    const d = s.massStore.ATLAS;
    const lo = d.filter(m => m >= 50 && m < 100).length;
    const hi = d.filter(m => m >= 100 && m < 150).length;
    expect(lo).toBeGreaterThan(2 * hi);   // echtes Kontinuum fällt steil
  });
  it('Pilot: auch Z→4ℓ ist im sichtbaren 4ℓ-Event gegatet (nicht nur das H-Fenster)', () => {
    s.selDet = 'CMS'; s.isIon = false; s.paramEnergy = 0.45;
    let zWin = 0;
    for (let i = 0; i < 2000; i++) { const ev = App.sampleEvent(); if (Math.abs(ev.M - 91.19) <= 6) zWin++; }
    expect(zWin / 2000).toBeLessThan(0.02);   // Pool-Anteil wäre ~13 %
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

describe('Datennahme: Signifikanz wächst √-förmig (steil→flach), nicht zu schnell', () => {
  // Bildet die Akkumulations-Mathematik aus engine.js#startAutoCollide nach
  // (collStore += STAT_RATE·L·lumiF·dReal, L = e^{-2t/τ}) und prüft Form/Tempo.
  // lumiF = (I/I_ref)²·(β*_ref/β*) — normiert auf den Preset-Arbeitspunkt des
  // Strahls (pp: 1.40e11/0.30 m · Pb-Pb: 0.90e11/0.50 m); Defaults = Preset → 1.
  function simulateFill(det, { ion = false, energy = 6.8, I = null, beta = null } = {}) {
    App.resetSpectrumData();
    s.selDet = det; s.isIon = ion; s.paramEnergy = energy;
    const ref = ion ? { I: 0.90, b: 0.50 } : { I: 1.40, b: 0.30 };
    const lumiF = Math.pow((I ?? ref.I) / ref.I, 2) * (ref.b / Math.max(0.05, beta ?? ref.b));
    const dtScale = DT_SCALE.slow, tau = BEAM_LIFETIME_H * 3600;
    let dtElapsed = 0, ticks = 0, t5 = null;
    const sigs = [];
    for (let guard = 0; guard < 100000; guard++) {
      const dReal = 0.125 * dtScale; dtElapsed += dReal;
      const frac = Math.exp(-dtElapsed / tau), L = frac * frac;
      s.collStore[det] += STAT_RATE * L * lumiF * dReal * App.detRate(det);   // wie Engine
      const sig = App.getSignificance();
      sigs.push(sig); ticks++;
      if (t5 === null && sig >= 5) t5 = ticks * 0.125;   // Darstellungssekunden
      if (frac <= DUMP_FRAC) break;
    }
    return { sigs, t5, fillSecs: ticks * 0.125 };
  }

  it('springt NICHT in 1–2 Ticks auf 5σ (war der „zu schnell"-Bug)', () => {
    const { sigs } = simulateFill('ATLAS');
    expect(sigs[0]).toBeLessThan(1.5);   // erster Tick weit unter Entdeckung
    expect(sigs[1]).toBeLessThan(2.5);
  });
  it('Z⁰ (ATLAS) erreicht 5σ in watchbarer Zeit (~4–16 s), nicht sofort', () => {
    const { t5 } = simulateFill('ATLAS');
    expect(t5).toBeGreaterThan(4);
    expect(t5).toBeLessThan(16);
  });
  it('Signifikanz-Kurve ist konkav (√-Form): Zuwachs pro Tick nimmt ab', () => {
    const { sigs } = simulateFill('ATLAS');
    const d = []; for (let i = 1; i < 40; i++) d.push(sigs[i] - sigs[i - 1]);
    // jeder spätere Zuwachs ≤ ein früherer (monoton fallende Steigung = konkav)
    for (let i = 1; i < d.length; i++) expect(d[i]).toBeLessThanOrEqual(d[i - 1] + 1e-9);
  });
  it('schwerer Kanal (CMS-Higgs) braucht länger als der leichte (Z⁰) — ein guter Fill', () => {
    const atlas = simulateFill('ATLAS').t5;
    const cms = simulateFill('CMS').t5;
    expect(cms).toBeGreaterThan(atlas);
    expect(cms).toBeLessThan(simulateFill('CMS').fillSecs + 1);  // innerhalb eines Fills erreichbar
  });
  it('ein Fill dauert bis zum Dump deutlich länger als die alte 1–2-s-Entdeckung', () => {
    expect(simulateFill('ATLAS').fillSecs).toBeGreaterThan(30);
    s.isIon = false;
  });
  it('Auto-Datennahme koppelt an Intensität²/β* (A6): schwächerer Strahl → später 5σ', () => {
    const preset = simulateFill('ATLAS').t5;                                 // Arbeitspunkt (lumiF=1)
    const weakI  = simulateFill('ATLAS', { I: 1.0 }).t5;                     // (1.0/1.4)² ≈ 0.51
    expect(weakI).toBeGreaterThan(preset);
    // Ohne Squeeze (β* = 1.5 m → lumiF 0.2) reicht EIN Fill nicht zur Entdeckung —
    // der Squeeze-Schritt hat damit sichtbaren Physik-Payoff (L ∝ 1/β*).
    expect(simulateFill('ATLAS', { beta: 1.5 }).t5).toBe(null);
  });
});

describe('Tempo-Modell: Bahngeschwindigkeit steigt monoton (kein Stau)', () => {
  // getStageVel braucht App.timeScale() (sonst in engine.js registriert) → hier stubben.
  const order = ['linac', 'ring1', 'trToPs', 'ps', 'trToSps', 'sps', 'ti'];
  it('Geschwindigkeit nimmt durch die Kette LINAC→…→SPS→TI monoton zu', () => {
    App.timeScale = () => 1.0; s.isIon = false;
    const v = order.map(k => App.getStageVel(k));
    for (let i = 1; i < v.length; i++) expect(v[i]).toBeGreaterThan(v[i - 1]);
  });
  it('PS→SPS-Transfer ist NICHT langsamer als der PS-Umlauf (behebt den „Stau")', () => {
    App.timeScale = () => 1.0; s.isIon = false;
    expect(App.getStageVel('trToSps')).toBeGreaterThan(App.getStageVel('ps'));
  });
  it('slow-Modus (timeScale 2.6) ist langsamer als Zeitraffer', () => {
    s.isIon = false;
    App.timeScale = () => 1.0; const fast = App.getStageVel('sps');
    App.timeScale = () => 2.6; const slow = App.getStageVel('sps');
    expect(slow).toBeLessThan(fast);
  });
  it('Ionen laufen langsamer als Protonen', () => {
    App.timeScale = () => 1.0;
    s.isIon = false; const pp = App.getStageVel('ps');
    s.isIon = true;  const pb = App.getStageVel('ps');
    expect(pb).toBeLessThan(pp);
    s.isIon = false;
  });
});

describe('Echtdaten-Provenienz (CERN_REAL aus CMS-Open-Data)', () => {
  it('meta deklariert Quelle, √s=7 TeV und ehrliche Flags', () => {
    expect(CERN_REAL.meta.source).toMatch(/CMS Open Data/);
    expect(CERN_REAL.meta.sqrt_s_TeV).toBe(7);
    expect(CERN_REAL.meta.higgs4l_sim).toBe(false);    // 4ℓ jetzt ECHTE CMS-Daten (Record 5200)
    expect(CERN_REAL.meta.higgs4l_source).toMatch(/5200/);
    expect(CERN_REAL.meta.pbpb_real).toBe(false);      // kein echtes Pb-Pb → QGP modelliert
  });
  it('Higgs-4ℓ sind ECHTE Kandidaten mit Z→4ℓ-Peak (91) UND Higgs-Bump (125)', () => {
    expect(CERN_REAL.higgs4l.length).toBeGreaterThan(200);     // ~278 echte Kandidaten
    const inWin = (lo, hi) => CERN_REAL.higgs4l.filter(m => m >= lo && m <= hi).length;
    expect(inWin(88, 94)).toBeGreaterThan(0);    // Z→4ℓ
    expect(inWin(120, 130)).toBeGreaterThan(0);  // Higgs
    expect(CERN_REAL.topo.h4l.length).toBe(CERN_REAL.higgs4l.length);   // Masse↔Kinematik gepaart
    expect(CERN_REAL.topo.h4l[0].length).toBe(20);                      // 4 Leptonen × [pt,eta,phi,q,flavor]
  });
  it('sampleH4l() liefert ein echtes 4-Lepton-Ereignis (Masse + 4 Spuren)', () => {
    const ev = App.sampleH4l();
    expect(ev).toBeTruthy();
    expect(ev.leptons.length).toBe(4);
    expect(typeof ev.M).toBe('number');
    expect(['e', 'μ']).toContain(ev.leptons[0].lep);
  });
  it('Massen-Pools sind nichtleere ECHTE Arrays im erwarteten Bereich', () => {
    expect(CERN_REAL.pp.length).toBeGreaterThan(200);
    expect(Math.min(...CERN_REAL.pp)).toBeGreaterThanOrEqual(50);
    expect(Math.max(...CERN_REAL.pp)).toBeLessThanOrEqual(150);
    expect(CERN_REAL.ion.length).toBeGreaterThan(200);
    expect(Math.max(...CERN_REAL.ion)).toBeLessThanOrEqual(12);
  });
  it('Quarkonia-Substruktur ist in den Echtdaten vorhanden (ψ(2S) + Υ-Familie)', () => {
    const inWin = (lo, hi) => CERN_REAL.ion.filter(m => m >= lo && m <= hi).length;
    expect(inWin(3.0, 3.2)).toBeGreaterThan(0);     // J/ψ
    expect(inWin(3.5, 3.9)).toBeGreaterThan(0);     // ψ(2S)
    expect(inWin(9.0, 10.6)).toBeGreaterThan(0);    // Υ(1S/2S/3S)
  });
  it('Event-Display-Untergrund nutzt ECHTE Kinematik (topo.bg nichtleer)', () => {
    expect(CERN_REAL.topo.bg.length).toBeGreaterThan(0);
    expect(CERN_REAL.topo.Z0.length).toBeGreaterThan(0);
    const t = App.sampleBgTrack();
    expect(typeof t.pt).toBe('number'); expect(typeof t.phi).toBe('number');
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
