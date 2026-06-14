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
//   • Protonen: 2808 Bunches/Strahl in 10 Zügen (max 288 = 4×72; real ~12 Injektionen).
//   • Pb-Ionen: nur 592 Bunches/Strahl (größerer Abstand) in 8 Zügen.
// Batch-Hierarchie (real, als Label): PSB bündelt+spaltet zu 72-Bunch-PS-Batches,
// das SPS fügt bis 4 Batches zu einem Zug (288 B), ~10 Züge füllen den LHC.
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
// BEWUSST GEMÄSSIGT (war 1800/5400): ein Fill dauert jetzt ~63 s (langsam) /
// ~28 s (schnell) bis zum Dump → die Signifikanz klettert SICHTBAR der √-Kurve
// entlang, statt in 1–2 s auf 5σ zu springen.
export const DT_SCALE = { slow: 900, fast: 2000 };    // 1 s ≈ 15 min / 33 min real
export const BEAM_LIFETIME_H = 15;                     // Intensitäts-Lebensdauer τ
export const DUMP_FRAC = 0.35;                         // Dump-Schwelle (N/N₀)
// Kandidaten-Akkumulation der Datennahme ∝ integrierte Luminosität (∫L·dt). Die
// Signifikanz ist 5·√(Kandidaten/target) → wächst damit ∝ √(∫L·dt): STEIL am
// Anfang, dann zunehmend FLACHER (echtes √-Gesetz), zusätzlich durch den Burn-off
// (L ∝ N² fällt) gedämpft. So kalibriert, dass EIN guter Fill den schwersten
// Kanal (CMS-Higgs: target 90 bei rate 0.12) knapp vor dem Dump auf 5σ bringt;
// leichtere Kanäle (Z⁰) früher. Slider skalieren die Rate zusätzlich ∝ N²/β*
// (engine.js#startAutoCollide, normiert auf den Preset-Arbeitspunkt).
// collStore wird KONTINUIERLICH (float) erhöht → glatte Kurve, keine
// Integer-Sprünge. Bleibt über Dumps erhalten (mehrere Fills summieren sich, real).
export const STAT_RATE = 0.04;

// Shapes: cern/app/src/types.d.ts. AppNamespace hat eine Index-Signatur → die von
// den Modulen dynamisch registrierten Funktionen (App.setStatus/drawHist/…) sind `any`.
export const App: AppNamespace = {
  state: {} as AppState,   // mutable Querschnitt (state.ts füllt via Object.assign)
  els: {},     // DOM-Referenzen (main.ts#initDom befüllt sie bei Boot)
  g: {},       // SVG-Geometrie: { R, J, paths, nodes, svg } (geometry.ts + boot)
};

export const $ = (id: string): any => document.getElementById(id);  // Element-Shape Pilot-lenient

export const SVG_NS = "http://www.w3.org/2000/svg";
export const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
