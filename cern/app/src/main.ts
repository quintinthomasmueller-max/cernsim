// ═══════════════════════════════════════════════════════════════════════════
// MAIN — Entry-Point der Stellwerk-App (App-First-Migration, Phase 1).
//
// Ersetzt das alte __cernInit/Bootstrap-Konstrukt: bootet idempotent bei
// DOM-Ready, grabbt ALLE DOM-/SVG-Refs in App.els/App.g (initDom) und verdrahtet
// erst DANN die Listener (wireEngine/wireHandlers). Das löst die Jupyter-Race
// (Script lief oft vor dem Widget-DOM → getElementById === null) sauber auf.
//
// Reihenfolge der Imports = Lade-/Registrier-Reihenfolge der Module:
//   geometry → setzt App.g.R/J | state → füllt App.state
//   engine/display/spectrum/info/handlers → registrieren App.* + export wireX()
// ═══════════════════════════════════════════════════════════════════════════
import { App, $ } from './core.js';
import './geometry.js';
import './state.js';
import { wireEngine } from './engine.js';
import './display.js';
import './spectrum.js';
import './info.js';
import './geo.js';
import { wireHandlers } from './handlers.js';

// Alle DOM-/SVG-/Canvas-Refs EINMALIG bei Boot grabben (nicht beim Modul-Laden).
function initDom(){
 const E = App.els, g = App.g, s = App.state;

 E.sdot=$("sdot"); E.stxt=$("stxt");
 E.btnRamp=$("btn-ramp"); E.btnColl=$("btn-coll"); E.btnAuto=$("btn-auto"); E.btnSqueeze=$("btn-squeeze");
 E.btnAutoColl=$("btn-autocoll"); E.btnSpeedToggle=$("btn-speed-toggle");
 E.b1c=$("b1c"); E.b2c=$("b2c"); E.b1bar=$("b1bar"); E.b2bar=$("b2bar"); E.rbar=$("rbar");
 E.vE=$("v-e"); E.vB=$("v-b"); E.vG=$("v-g"); E.vT=$("v-t");
 E.spInfo=$("sp-info");
 // Strahl-Parameter sind jetzt reine ANZEIGEN (Preset-gesteuert), keine Slider mehr.
 E.lblEnergy=$("lbl-energy"); E.lblIntensity=$("lbl-intensity"); E.lblBeta=$("lbl-beta"); E.lblRampSpeed=$("lbl-rampspeed");
 E.trInj=$("tr-inj");
 E.btnToggleGeo=$("btn-toggle-geo");
 E.btnPrePp=$("btn-pre-pp"); E.btnPreQgp=$("btn-pre-qgp"); E.btnPrePilot=$("btn-pre-pilot");
 E.btnZoomOut=$("btn-zoom-out"); E.btnZoomMeyrin=$("btn-zoom-meyrin"); E.btnDiagramFull=$("btn-diagram-full");
 E.btnEvTour=$("btn-ev-tour");
 E.root=$("cern-v4");
 E.grpAtlas=$("grp-atlas"); E.grpCms=$("grp-cms"); E.grpAlice=$("grp-alice"); E.grpLhcb=$("grp-lhcb");
 E.svg=$("svg");
 E.geoLayer=$("geo-layer");
 E.schematic=$("schematic");   // Didaktik-Gruppe (im Real-Modus ausgeblendet)

 // SVG-Pfade & Knoten + Stufen-Tracker → App.g
 g.trSteps=["tr-src","tr-inj","tr-ps","tr-sps","tr-lhc"].map($);
 g.paths={
  linac4:$("p-linac4"), psb:$("p-psb"), psbPs:$("p-psb-ps"),
  linac3:$("p-linac3"), leir:$("p-leir"), leirPs:$("p-leir-ps"),
  ps:$("p-ps"), psSps:$("p-ps-sps"), sps:$("p-sps"),
  ti2:$("p-ti2"), ti8:$("p-ti8"), lhc:$("p-lhc")
 };
 g.nodes={
  linac4:$("n-linac4"), psb:$("n-psb"), linac3:$("n-linac3"), leir:$("n-leir"),
  ps:$("n-ps"), sps:$("n-sps"),
  atlas:$("d-atlas"), cms:$("d-cms"), alice:$("d-alice"), lhcb:$("d-lhcb")
 };

 // Canvas + 2D-Kontexte
 E.cvEv=$("cv-ev"); E.ctxEv=E.cvEv.getContext("2d");
 E.cvHist=$("cv-hist"); E.ctxHist=E.cvHist.getContext("2d");
 s.dpr = window.devicePixelRatio || 1;
}

function start(){
 initDom();
 wireEngine();
 wireHandlers();
 App.drawGeo();          // baut #geo-layer (reale Ansicht) auf
 App.setViewMode(false); // Start im Didaktik-Modus (Schema sichtbar, Geo aus)
 App.resizeCanvases();
 App.updateReadouts(); App.drawDetBg(); App.drawHist();
 App.setStatus("BEREIT — Wähle Teilchenart und starte Injektion","on");
 // Backing-Store an die per-CSS bestimmte Anzeigegröße koppeln. ResizeObserver
 // feuert initial UND bei jeder Layout-Änderung (Grid-Reflow @860px, iframe-
 // Resize in Jupyter, verzögerter Stylesheet-Load) → eine evtl. vor dem Layout
 // gemessene Boot-Größe korrigiert sich selbst. Kein Inline-Style-Lock mehr.
 // Nach Resize das LETZTE Event wieder zeichnen (drawDetBg allein würde die
 // Spuren der letzten Kollision verwerfen, bis das nächste Event eintrifft).
 const redraw = ()=>{ App.resizeCanvases();
  if(App.state.tourStep) App.evTourDraw();   // Tour-Standbild in neuer Größe neu zeichnen
  else App.state.lastEvent ? App.drawCollisionEvent(App.state.lastEvent) : App.drawDetBg();
  App.drawHist(); };
 if(typeof ResizeObserver !== "undefined"){
  const ro = new ResizeObserver(redraw);
  ro.observe(App.els.cvEv); ro.observe(App.els.cvHist);
 } else {
  window.addEventListener("resize", redraw);
 }
}

// ── Bootstrap (robust gegen Jupyter-Timing, idempotent pro Widget-Root) ──────
function ready(){
 return document.getElementById("cern-v4")
     && document.getElementById("svg")
     && document.getElementById("btn-auto");
}
function boot(){
 const root = document.getElementById("cern-v4") as any;  // __cernBooted = Custom-Boot-Flag
 if(!root || root.__cernBooted || !ready()) return !!(root && root.__cernBooted);
 root.__cernBooted = true;
 try { start(); }
 catch(e){ try { console.error("[CERN-Widget] Init fehlgeschlagen:", e); } catch(_){} }
 return true;
}
if(!boot()){
 let n = 0;
 const iv = setInterval(()=>{ if(boot() || ++n > 200) clearInterval(iv); }, 25);
 if(document.readyState === "loading"){
  document.addEventListener("DOMContentLoaded", boot);
 }
}
