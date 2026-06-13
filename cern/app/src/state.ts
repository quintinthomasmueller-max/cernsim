// ═══════════════════════════════════════════════════════════════════════════
// STATE — alle veränderlichen Querschnittsvariablen leben in App.state.
// Zugriff in anderen Modulen: const s = App.state;  s.filling = true; …
// ═══════════════════════════════════════════════════════════════════════════
import { App } from './core.js';

// `satisfies AppState`: prüft das Init-Objekt an der Quelle gegen den Vertrag —
// fehlende/vertippte/überzählige State-Felder fallen hier beim tsc-Gate auf.
Object.assign(App.state, {
  isIon: false, ramped: false, filling: false,
  b1Count: 0, b2Count: 0,         // umlaufende Züge je Strahl
  b1Batches: 0, b2Batches: 0,     // angekommene PS-Batches je Strahl (→ Bunches-Anzeige)
  collisions: 0,
  dtElapsed: 0, intensity0: 0, intensityNow: 0,   // Datennahme: vergangene reale Zeit + Strahl-Intensität (Burn-off)
  dumping: false,                 // Strahl-Dump läuft (gated Kollisionen/Neustart bis zum Reset)
  fillGen: 0,                     // Füll-Generation (Zombie-Batch-Schutz bei Reset+Neustart)
  spsDots: { b1: [], b2: [] }, spsAngle: 0, spsRunning: false, spsLastT: null,  // im SPS akkumulierende Batches
  lhcDots: { b1: [], b2: [] },
  lhcSpeed: 0.0078,          // rad/ms bei Injektionsenergie (Proton)
  lhcAngle: 0, lhcRunning: false, lhcLastT: null,
  lhcEnergy: 450,            // GeV
  // Per-Detektor-Datenspeicher: jeder Detektor akkumuliert NUR sein eigenes Spektrum.
  massStore: { ATLAS: [], CMS: [], ALICE: [], LHCB: [] },
  collStore: { ATLAS: 0, CMS: 0, ALICE: 0, LHCB: 0 },   // Kandidaten je Detektor (Signifikanz ∝ √)
  histAcc:   { ATLAS: 0, CMS: 0, ALICE: 0, LHCB: 0 },   // Bruchteil-Akku fürs Histogramm je Detektor
  histSeen:  { ATLAS: 0, CMS: 0, ALICE: 0, LHCB: 0 },   // gesehene Einträge (Reservoir-Sampling am HIST_CAP)
  lastEvent: null, goldenEvent: null, higgsCands: 0,
  selDet: 'ATLAS',
  tourStep: 0,               // Signaturen-Tour im Event-Display (0 = aus, 1..6 = Schritt)
  isFastMode: false,
  // CCC-Operator-Parameter
  paramEnergy: 6.8,          // Ziel-Energie (TeV)
  paramIntensity: 1.15,      // Bunch-Intensität (10^11 Protonen)
  paramBetaStar: 1.5,        // AKTUELLES β* am IP (m): 1,5 unsqueezed → Ziel nach Squeeze
  targetBetaStar: 0.3,       // β*-Ziel des Presets (Squeeze fährt paramBetaStar darauf herunter)
  paramRampSpeed: 0.05,      // Magnetfeld-Ramp-Rate (T/s)
  isPilot: false,
  squeezing: false, squeezed: false, cryoRecovery: false,
  autoCollInterval: null,
  // Ablaufsteuerung (vormals implizite Globals im IIFE-Closure)
  resetFlag: false,
  // Canvas-Maße / High-DPI (dpr bei Boot aus window.devicePixelRatio gesetzt)
  dpr: 1, evW: 340, evH: 180, histW: 340, histH: 130,
} satisfies AppState);

// ── Kohärentes Tempo-Modell: EINE Geschwindigkeits-Leiter (Bildschirm-px je ms) ──
// Die visuelle Bahngeschwindigkeit steigt MONOTON durch die Kette
// (LINAC→PSB/LEIR→Transfer→PS→Transfer→SPS→TI), der LHC-Ring (via lhcSpeed) ist
// immer am schnellsten. Frühere Version gab PRO STUFE eine feste DAUER vor —
// entkoppelt von der echten Pfadlänge. Kurze Transferlinien (PS→SPS ≈ 15 px)
// „dauerten" dadurch genauso lang wie ganze Ring-Umläufe → der Punkt KROCH dort
// (vom Nutzer als „Stau zwischen PS und SPS" wahrgenommen). Jetzt gilt überall
// dur = Pfadlänge / Geschwindigkeit (engine.js#moveAlongPath/orbitRing); die
// Geschwindigkeit steigt monoton → kein Tempo-Sprung/Stau an Übergängen. Dieselbe
// Leiter speist auch den SPS-Akkumulations-Umlauf (engine.js#startSpsLoop).
const STAGE_VPX: Record<string, number> = { linac: 0.30, ring1: 0.34, trToPs: 0.40, ps: 0.46, trToSps: 0.54, sps: 0.66, ti: 0.82 };
export function getStageVel(key: string): number {
  const s = App.state;
  const ion = s.isIon ? 0.72 : 1.0;                          // Ionen schwerer → etwas langsamer
  return (STAGE_VPX[key] || 0.5) * ion / App.timeScale!();   // slow-Modus (ts=40/15≈2,67) → langsamer
}
App.getStageVel = getStageVel;
