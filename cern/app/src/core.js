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

export const NEEDED = 6;

export const App = {
  state: {},   // mutable Querschnittsvariablen (state.js füllt via Object.assign)
  els: {},     // DOM-Referenzen (main.js#initDom befüllt sie bei Boot)
  g: {},       // SVG-Geometrie: { R, J, paths, nodes, svg } (geometry.js + boot)
  // öffentliche Funktionen registrieren die Module hier (App.setStatus, App.drawHist, …)
};

export const $ = (id) => document.getElementById(id);
