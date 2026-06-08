// ═══════════════════════════════════════════════════════════════════════════
// CORE — geteilter Namespace des Stellwerk-Widgets (App-First-Migration, Phase 1).
//
// Statt einer geteilten IIFE-Closure (alt) gibt es EIN importiertes `App`-Objekt.
// Querschnitt (state/els/g) wird als Objekt-Properties gelesen UND mutiert —
// dadurch umgehen wir die ESM-Regel „importierte Bindungen sind schreibgeschützt"
// (wir reassignen nie ein Import, sondern mutieren Properties).
//
// Konventionen für die Modul-Konvertierung:
//   import { App } from './core.js';
//   const s = App.state;            // veränderliche Querschnittsvariablen
//   s.filling = true;               // mutieren ist erlaubt (Property-Write)
//   App.els.btnAuto.classList…      // DOM-Refs (erst bei Boot via initDom befüllt)
//   App.g.R, App.g.J, App.g.paths…  // SVG-Geometrie (bei Boot befüllt)
//   function foo(){…}  App.foo = foo // öffentliche Funktionen registrieren
//   App.bar()                        // modulübergreifend aufrufen
// ═══════════════════════════════════════════════════════════════════════════

// Füll-Modell: 1 umlaufender Punkt = 1 SPS-Zug (eine Injektion in den LHC).
// MODUSABHÄNGIGE reale Zahlen (Protonen 25-ns-Standard vs. Pb⁸²⁺-Ionen):
//   • Protonen: 2808 Bunches/Strahl in ~12 SPS-Schüssen (je ⌀234, max 288 = 4×72).
//   • Pb-Ionen: nur 592 Bunches/Strahl (größerer Abstand) in ~8 Schüssen.
// Batch-Hierarchie (real, als Label): PSB bündelt+spaltet zu 72-Bunch-PS-Batches,
// das SPS fügt bis 4 Batches zu einem Zug (288 B), ~12 Züge füllen den LHC.
// psBatch = Bunches je PS-Batch (= 1 wandernder Punkt), batchesPerTrain = wie viele
// Batches das SPS zu EINEM Zug fusioniert. Daraus abgeleitet: Batches/Strahl =
// total/psBatch, Züge = ⌈Batches/batchesPerTrain⌉.
//   Protonen: 2808/72 = 39 Batches → 10 Züge (9×4 + 1×3).
//   Pb-Ionen: 592/37 = 16 Batches → 8 Züge (je 2 Batches).
export const FILL = {
  proton: { total: 2808, psBatch: 72, batchesPerTrain: 4 },
  ion:    { total: 592,  psBatch: 37, batchesPerTrain: 2 },
};
// Zeit-Maßstab des Lade-Prozesses: real schießt das SPS ~alle 25 s einen Zug;
// SIM_SCALE = reale Sekunden pro Darstellungssekunde (langsam 15× / schnell 40×).
// → volle Füllung real ~10 min, gezeigt in ~40 s (langsam) bzw. ~15 s (schnell).
export const REAL_SPS_CYCLE_S = 25;
export const SIM_SCALE = { slow: 15, fast: 40 };

// Datennahme (Stable Beams): EIGENE, viel größere Zeitstauchung als das Füllen,
// weil ein Physik-Fill real ~15 h läuft (vs. ~10 min Füllen). Während der
// Kollisionen zerfällt die Strahl-INTENSITÄT N (Burn-off, ~15 h Lebensdauer);
// die Luminosität L ∝ N² und damit die Kollisionsrate sinken. Bei N < 35 % →
// Strahl-Dump (Refill nötig). DT_SCALE = reale Sekunden je Darstellungssekunde.
export const DT_SCALE = { slow: 1800, fast: 5400 };   // 1 s ≈ 30 min / 90 min real
export const BEAM_LIFETIME_H = 15;                     // Intensitäts-Lebensdauer τ
export const DUMP_FRAC = 0.35;                         // Dump-Schwelle (N/N₀)
// Statistik-Akkumulation der Datennahme ∝ integrierte Luminosität (∫L·dt im
// Datennahme-Maßstab). So gekoppelt, dass EIN Fill ~⌀950 Kollisionen liefert →
// 5σ-Entdeckung (größtes target=600) wird vor dem Dump erreicht; bleibt über
// Dumps erhalten (mehrere Fills summieren sich, real). Tempo-gekoppelt via dtScale.
export const STAT_RATE = 0.04;

export const App = {
  state: {},   // mutable Querschnittsvariablen (state.js füllt via Object.assign)
  els: {},     // DOM-Referenzen (main.js#initDom befüllt sie bei Boot)
  g: {},       // SVG-Geometrie: { R, J, paths, nodes, svg } (geometry.js + boot)
  // öffentliche Funktionen registrieren die Module hier (App.setStatus, App.drawHist, …)
};

export const $ = (id) => document.getElementById(id);

export const SVG_NS = "http://www.w3.org/2000/svg";
export const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
