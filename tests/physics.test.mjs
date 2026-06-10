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
