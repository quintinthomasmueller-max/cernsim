// ═══════════════════════════════════════════════════════════════════════════
// STATE — alle veränderlichen Querschnittsvariablen leben in App.state.
// Zugriff in anderen Modulen: const s = App.state;  s.filling = true; …
// ═══════════════════════════════════════════════════════════════════════════
import { App } from './core.js';

Object.assign(App.state, {
  isIon: false, injecting: false, ramped: false, filling: false,
  b1Count: 0, b2Count: 0, collisions: 0,
  lhcDots: { b1: [], b2: [] },
  lhcSpeed: 0.0078,          // rad/ms bei Injektionsenergie (Proton)
  lhcAngle: 0, lhcRunning: false, lhcLastT: null,
  lhcEnergy: 450,            // GeV
  // Per-Detektor-Datenspeicher: jeder Detektor akkumuliert NUR sein eigenes Spektrum.
  massStore: { ATLAS: [], CMS: [], ALICE: [], LHCB: [] },
  collStore: { ATLAS: 0, CMS: 0, ALICE: 0, LHCB: 0 },
  lastEvent: null, goldenEvent: null, higgsCands: 0,
  selDet: 'ATLAS',
  activePhysicsMode: 'HIGGS', // HIGGS|QGP|LHCB|PILOT (entkoppelt vom Detektor-Tab)
  isFastMode: true,
  // CCC-Operator-Parameter
  paramEnergy: 6.8,          // Ziel-Energie (TeV)
  paramIntensity: 1.15,      // Bunch-Intensität (10^11 Protonen)
  paramBetaStar: 1.5,        // Strahlgröße am IP (m)
  paramRampSpeed: 0.05,      // Magnetfeld-Ramp-Rate (T/s)
  squeezing: false, squeezed: false, cryoRecovery: false,
  autoCollInterval: null,
});

// Didaktisches Geschwindigkeitsmodell: visuelle Bahngeschwindigkeit steigt monoton
// durch die Kette (LINAC→PSB→PS→SPS→TI), LHC-Ring ist immer am schnellsten.
// Dauer = Pfadlänge / Geschwindigkeit. Nutzt App.timeScale() (engine.js).
export function getDurations() {
  const s = App.state;
  const V = { linac: 0.52, psb: 0.75, trPs: 0.75, ps: 0.93, trSps: 0.93, sps: 1.12, ti: 1.32 };
  const LEN = { linac: 94, psb: 112 * 3, trPs: 56, ps: 238 * 3, trSps: 138, sps: 408 * 2, ti: 182 };
  const slow = App.timeScale();
  const ion = s.isIon ? 1.6 : 1.0;
  const d = (len, v) => Math.round(len / v * slow * ion);
  return {
    linac: d(LEN.linac, V.linac),
    ring1: d(LEN.psb, V.psb),
    trToPs: d(LEN.trPs, V.trPs),
    ps: d(LEN.ps, V.ps),
    trToSps: d(LEN.trSps, V.trSps),
    sps: d(LEN.sps, V.sps),
    ti: d(LEN.ti, V.ti),
    autoDelay: s.isFastMode ? 150 : 600,
  };
}
App.getDurations = getDurations;
