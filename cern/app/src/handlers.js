// ═══════════════════════════════════════════════════════════════════════════
// BUTTON HANDLERS — Listener-Verdrahtung + Preset-Logik + Füllprotokoll.
// Manuelles Einzel-Füllen entfernt – Füllen ausschließlich über das Füllprotokoll.
// wireHandlers() wird von main.js NACH initDom() aufgerufen.
// ═══════════════════════════════════════════════════════════════════════════
import { App, FILL, SIM_SCALE, sleep, $ } from './core.js';

// Aktuelle Füll-Konfig (Protonen vs. Pb-Ionen) + abgeleitete Zahlen.
const fc = () => App.state.isIon ? FILL.ion : FILL.proton;
const totalBatches = () => Math.round(fc().total / fc().psBatch);   // PS-Batches/Strahl
function fmtBunch(beam){ const b = beam===1 ? App.state.b1Batches : App.state.b2Batches; return (b * fc().psBatch).toLocaleString("de-DE"); }
function totalStr(){ return fc().total.toLocaleString("de-DE"); }

const s = App.state, E = App.els;

// Handler-lokaler View-Zustand (nur hier verwendet)
let realMode = false;   // false = Didaktik (Schema), true = Reale Ansicht (Geo)
let currentVB = {x:0, y:0, w:700, h:480};
let zoomTarget = null; // "ATLAS", "CMS", "ALICE", "LHCB" or null

function animateViewBox(tx, ty, tw, th, dur=500){
 const startX = currentVB.x, startY = currentVB.y, startW = currentVB.w, startH = currentVB.h;
 let t0 = null;
 function step(ts){
  if(!t0) t0 = ts;
  let p = Math.min((ts-t0)/dur, 1);
  let ep = p*p*(3-2*p); // Custom cubic ease-in-out
  currentVB.x = startX + ep*(tx-startX);
  currentVB.y = startY + ep*(ty-startY);
  currentVB.w = startW + ep*(tw-startW);
  currentVB.h = startH + ep*(th-startH);
  E.svg.setAttribute("viewBox", `${currentVB.x} ${currentVB.y} ${currentVB.w} ${currentVB.h}`);
  if(p<1) requestAnimationFrame(step);
 }
 requestAnimationFrame(step);
}

// Detektorwahl ZENTRAL: setzt selDet, Tab-Highlight, Event-Display UND Spektrum.
// Damit zeigt jeder Detektorwechsel (Tab, SVG, Preset) konsequent das passende Spektrum.
function selectDetector(name){
 document.querySelectorAll(".cv4-dtab").forEach(t=>t.classList.remove("act"));
 const tab=$("dt-"+name.toLowerCase()); if(tab) tab.classList.add("act");
 s.selDet=name;
 // Kandidaten-Zähler auf den NEU gewählten Detektor umstellen (sonst zeigte er
 // den Stand des vorigen Detektors bis zur nächsten Kollision/zum Reset).
 if(E.spInfo) E.spInfo.innerText = `Kandidaten (${name}): ${Math.round(s.collStore[name]||0).toLocaleString("de-DE")}`;
 App.drawDetBg(); App.drawHist();
}

function zoomToDetector(name){
 if(zoomTarget === name){
  resetView();   // Zoom out (Detektor-Auswahl bleibt erhalten)
 } else {
  zoomTarget = name;
  E.svg.classList.remove("inj-zoom");
  E.btnZoomMeyrin.style.display = "none";
  E.btnZoomOut.classList.remove("off");
  let tx, ty, tw=160, th=120;   // Box auf die Schema-Detektorpositionen (Kardinalpunkte)
  if(name === "ATLAS") { tx = 270; ty = 360; }
  else if(name === "CMS") { tx = 270; ty = 0; }
  else if(name === "ALICE") { tx = 90; ty = 180; }
  else if(name === "LHCB") { tx = 450; ty = 180; }
  animateViewBox(tx, ty, tw, th);
  selectDetector(name);
 }
}

// Vollbild wiederherstellen (Zoom zurück): Detail-Labels aus, Meyrin-Button (nur
// in der Realen Ansicht) wieder anbieten.
function resetView(){
 zoomTarget = null;
 E.svg.classList.remove("inj-zoom");
 E.svg.classList.remove("fcc-on");
 E.btnZoomOut.classList.add("off");
 E.btnZoomMeyrin.style.display = realMode ? "" : "none";
 animateViewBox(0, 0, 700, 480);
}

// Easter Egg: den GEPLANTEN Future Circular Collider (FCC) maßstäblich neben
// LHC/SPS zeigen — mit dramatischem Heraus-Zoom. Nur in der Realen Ansicht.
function revealFCC(){
 if(!realMode) return;
 const v = App.geoFccView; if(!v) return;
 zoomTarget = "FCC";
 E.svg.classList.remove("inj-zoom");
 E.svg.classList.add("fcc-on");                 // blendet den FCC-Ring ein (CSS)
 E.btnZoomMeyrin.style.display = "none";
 E.btnZoomOut.classList.remove("off");
 App.setStatus("🔭 FCC — Future Circular Collider: der geplante 91-km-Ring (×3,4 LHC), maßstäblich. „Ansicht zurücksetzen\" kehrt zurück.","on");
 animateViewBox(v.x, v.y, v.w, v.h, 1700);      // langsam = dramatisch
}
App.revealFCC = revealFCC;

// Zoom auf den Injektor-Komplex Meyrin (geo-genaues Fenster aus geo.js).
function zoomMeyrin(){
 const v = App.geoInjectorView; if(!v) return;
 zoomTarget = "MEYRIN";
 E.svg.classList.add("inj-zoom");             // blendet die Detail-Beschriftung ein
 E.btnZoomMeyrin.style.display = "none";
 E.btnZoomOut.classList.remove("off");
 animateViewBox(v.x, v.y, v.w, v.h);
}

async function fuellProtokoll(){
 const totB = totalBatches();
 if(s.filling || s.ramped || s.cryoRecovery || s.dumping || (s.b1Batches>=totB && s.b2Batches>=totB)) return;
 s.filling = true; s.resetFlag = false;
 const gen = s.fillGen;   // Füll-Generation DIESES Laufs (ältere In-Flight-Batches zählen nicht mehr)
 E.btnAuto.classList.add("off");
 E.sliEnergy.disabled = true; E.sliIntensity.disabled = true; E.sliRampSpeed.disabled = true;
 App.setStatus("FÜLLPROTOKOLL: PS-Batches laufen einzeln zum SPS und verschmelzen dort zu Zügen …","on");

 // 1 Punkt = 1 PS-Batch. Pro SPS-Zug fusionieren batchesPerTrain Batches; der letzte
 // Zug ist ggf. kürzer. Abwechselnd B1 (TI 2) / B2 (TI 8), je Zug ein realer SPS-Zyklus.
 const bpt = fc().batchesPerTrain;
 const sizes = []; for(let r=totB; r>0; r-=bpt) sizes.push(Math.min(bpt, r));
 const proms = [];
 for(let t=0; t<sizes.length; t++){
  for(const beam of [1,2]){
   if(s.resetFlag) break;
   proms.push(App.injectTrain(beam, sizes[t], gen));
   App.setStatus(`FÜLLPROTOKOLL: SPS-Züge entstehen …  B1 ${fmtBunch(1)}/${totalStr()}  ·  B2 ${fmtBunch(2)}/${totalStr()} Bunches`,"on");
   await sleep(App.trainCadenceMs()/2);
  }
  if(s.resetFlag) break;
 }
 await Promise.all(proms);
 s.filling = false;
 if(s.resetFlag) return;
 E.btnAuto.classList.remove("off");
 if(s.b1Batches>=totB && s.b2Batches>=totB){
  E.btnRamp.classList.remove("off");
  App.setStatus(`LHC GEFÜLLT — ${totalStr()} Bunches/Strahl (${sizes.length} Züge), beide Strahlen stabil. Ramping möglich!`,"on");
 } else {
  App.setStatus(`Füllung beendet: B1 ${fmtBunch(1)}/${totalStr()}, B2 ${fmtBunch(2)}/${totalStr()} Bunches.`,"on");
 }
}

App.selectDetector = selectDetector;
App.zoomToDetector = zoomToDetector;
App.fuellProtokoll = fuellProtokoll;

// ═══════════════════════════════════════════════════════════════════════════
// LISTENER-VERDRAHTUNG (nach initDom in main.js)
// ═══════════════════════════════════════════════════════════════════════════
export function wireHandlers(){
 E.btnSpeedToggle.addEventListener("click",()=>{
   s.isFastMode = !s.isFastMode;
   if(s.isFastMode) {
     E.btnSpeedToggle.innerText = `⏱️ Tempo: Zeitraffer · 1 s ≈ ${SIM_SCALE.fast} s real`;
     E.btnSpeedToggle.style.background = "rgba(88,166,255,.08)";
     E.btnSpeedToggle.style.borderColor = "rgba(88,166,255,.3)";
     E.btnSpeedToggle.style.color = "#58a6ff";
   } else {
     E.btnSpeedToggle.innerText = `⏱️ Tempo: Didaktisch · 1 s ≈ ${SIM_SCALE.slow} s real`;
     E.btnSpeedToggle.style.background = "rgba(227,119,194,.08)";
     E.btnSpeedToggle.style.borderColor = "rgba(227,119,194,.3)";
     E.btnSpeedToggle.style.color = "#e377c2";
   }
 });

 // MODUS-UMSCHALTUNG: Didaktik (Schema, animiert) ⟷ Reale Ansicht (Geo, echte Größen)
 E.btnToggleGeo.addEventListener("click",()=>{
  realMode = !realMode;
  App.setViewMode(realMode);
  E.btnToggleGeo.classList.toggle("act", realMode);
  E.btnToggleGeo.innerText = realMode ? "🎬 Didaktik-Modus" : "🌍 Reale Ansicht";
  resetView();   // Moduswechsel → Vollbild + Meyrin-Button passend ein/aus
  App.setStatus(realMode
    ? "REALE ANSICHT — echte OSM-Geometrie. Tipp: 🔬 Injektor-Komplex zoomt auf Meyrin."
    : "DIDAKTIK-MODUS — schematische, animierte Beschleuniger-Kette", "on");
 });

 // Event-Display-Tabs sind klickbar → wechseln Detektor + Spektrum (ohne Kamera-Zoom)
 ["atlas","cms","alice","lhcb"].forEach(d=>{
  const t=$("dt-"+d); if(t) t.addEventListener("click",()=>selectDetector(d.toUpperCase()));
 });

 // EVENT-DISPLAY interaktiv: Klick auf eine Schicht → Info-Panel mit Foto;
 // während der Signaturen-Tour schaltet jeder Canvas-Klick einen Schritt weiter.
 E.cvEv.addEventListener("click", e=>{
  if(s.tourStep){ App.evTourAdvance(); return; }
  const r=E.cvEv.getBoundingClientRect();
  const x=(e.clientX-r.left)*(s.evW/(r.width||s.evW));
  const y=(e.clientY-r.top)*(s.evH/(r.height||s.evH));
  const k=App.evLayerHit(x,y);
  if(k) App.showInfo(k);
 });
 if(E.btnEvTour) E.btnEvTour.addEventListener("click", e=>{ e.stopPropagation(); App.evTourAdvance(); });

 E.btnZoomOut.addEventListener("click", resetView);
 E.btnZoomMeyrin.addEventListener("click", zoomMeyrin);

 // VOLLBILD-RING (Großansicht am Handy): CSS-Overlay statt Fullscreen-API
 // (iOS-Safari erlaubt requestFullscreen auf Elementen nicht zuverlässig).
 // Der Ring/Bunches skalieren automatisch (alles in SVG-viewBox-Koordinaten).
 if(E.btnDiagramFull){
  const root = E.root || document.getElementById("cern-v4");
  const setFull = (on)=>{ root.classList.toggle("diagram-full", on);
    E.btnDiagramFull.innerHTML = on ? "✕ Schließen" : "⛶ Großansicht"; };
  E.btnDiagramFull.addEventListener("click", ()=> setFull(!root.classList.contains("diagram-full")));
  document.addEventListener("keydown", e=>{ if(e.key==="Escape" && root.classList.contains("diagram-full")) setFull(false); });
 }

 E.grpAtlas.addEventListener("click", () => { App.showInfo("ATLAS"); zoomToDetector("ATLAS"); });
 E.grpCms.addEventListener("click",   () => { App.showInfo("CMS");   zoomToDetector("CMS");   });
 E.grpAlice.addEventListener("click", () => { App.showInfo("ALICE"); zoomToDetector("ALICE"); });
 E.grpLhcb.addEventListener("click",  () => { App.showInfo("LHCB");  zoomToDetector("LHCB");  });

 // INFO PANEL — Beschleuniger-Knoten
 $("hit-linac4").addEventListener("click", () => App.showInfo("LINAC4"));
 $("hit-linac3").addEventListener("click", () => App.showInfo("LINAC3"));
 $("hit-psb").addEventListener("click",    () => App.showInfo("PSB"));
 $("hit-leir").addEventListener("click",   () => App.showInfo("LEIR"));
 $("hit-ps").addEventListener("click",     () => App.showInfo("PS"));
 $("hit-sps").addEventListener("click",    () => App.showInfo("SPS"));
 $("hit-lhc").addEventListener("click",    () => App.showInfo("LHC"));
 $("info-close").addEventListener("click", App.hideInfo);

 // PARAM INFO ACCORDION — ⓘ-Buttons füllen und toggeln Textboxen
 document.querySelectorAll('.cv4-pi-btn').forEach(btn => {
  btn.addEventListener('click', e => {
   e.stopPropagation();
   const key = btn.dataset.pi;
   const box = $('pi-' + key);
   if(!box) return;
   if(!box.dataset.filled){
    if(App.PARAM_INFO[key]) box.textContent = App.PARAM_INFO[key];
    // Optionales Vorbild-Bild (z. B. echte Higgs-Kandidaten 2012 unter „Bild lesen")
    const fig = App.PARAM_INFO_FIG && App.PARAM_INFO_FIG[key];
    if(fig){
     const src = 'https://commons.wikimedia.org/wiki/Special:FilePath/' + encodeURIComponent(fig.img) + '?width=640';
     box.insertAdjacentHTML('beforeend',
      `<img class="cv4-pi-img" src="${src}" alt="" loading="lazy" referrerpolicy="no-referrer" onerror="this.style.display='none'">`
      + `<div class="cv4-pi-cap">${fig.cap}<br>📷 ${fig.cred}</div>`);
    }
    box.dataset.filled = '1';
   }
   const wasOpen = box.classList.contains('open');
   document.querySelectorAll('.cv4-param-info.open').forEach(x => x.classList.remove('open'));
   if(!wasOpen) box.classList.add('open');
  });
 });

 // PRESETS — die 3 realen LHC-Betriebsmodi (pp-Physik / Schwerionen / Pilot).
 // pp-Physik: EIN Proton-Lauf bei voller Energie, auf dem in Wirklichkeit ALLE
 // Experimente gleichzeitig laufen — Higgs (CMS), Z⁰ (ATLAS) UND CP-Verletzung
 // (LHCb). Default-Tab CMS; per Detektor-Tab sind die anderen Entdeckungen direkt da.
 E.btnPrePp.addEventListener("click",()=>{
  App.setMode(false); // Protonen
  App.resetLHC();
  E.sliEnergy.value = 6.8; s.paramEnergy = 6.8; E.lblEnergy.innerText = "6.8 TeV";
  E.sliIntensity.value = 1.40; s.paramIntensity = 1.40; E.lblIntensity.innerText = "1.40e11 p";
  E.sliBeta.value = 0.3; s.paramBetaStar = 0.3; E.lblBeta.innerText = "0.30 m";
  E.sliRampSpeed.value = 0.05; s.paramRampSpeed = 0.05; E.lblRampSpeed.innerText = "0.05 T/s (Sicher)"; E.lblRampSpeed.style.color = "#58a6ff";
  App.updateReadouts(); selectDetector("CMS");   // CMS = Higgs-Goldkanal H→ZZ*→4ℓ
  App.setStatus("PRESET: Protonen-Physik (Run 3 · 13.6 TeV) — Higgs (CMS), Z⁰ (ATLAS) & CP (LHCb) laufen GLEICHZEITIG auf diesem Strahl (Tab wechseln zeigt jeden Stand). Spektren: echte CMS-Open-Data — μμ (Record 545) UND die 278 echten 4ℓ-Higgs-Kandidaten (Record 5200).", "on");
 });

 E.btnPreQgp.addEventListener("click",()=>{
  App.setMode(true); // Blei-Ionen
  App.resetLHC();
  E.sliEnergy.value = 2.7; s.paramEnergy = 2.7; E.lblEnergy.innerText = "2.70 TeV/u";
  E.sliIntensity.value = 0.90; s.paramIntensity = 0.90; E.lblIntensity.innerText = "0.90e11 p";
  E.sliBeta.value = 0.5; s.paramBetaStar = 0.5; E.lblBeta.innerText = "0.50 m";
  E.sliRampSpeed.value = 0.05; s.paramRampSpeed = 0.05; E.lblRampSpeed.innerText = "0.05 T/s (Sicher)"; E.lblRampSpeed.style.color = "#58a6ff";
  App.updateReadouts(); selectDetector("ALICE");
  App.setStatus("PRESET: Schwerionen (Pb-Pb · 2.7 TeV/u, √s_NN=5.36 TeV) → ALICE: J/ψ-QGP-Unterdrückung · CMS: Υ-Sequenzunterdrückung · ATLAS: Z⁰-Standardkerze · LHCb spezialisiert. Massen echt (CMS-p-p), QGP-Unterdrückung modelliert.", "on");
 });

 E.btnPrePilot.addEventListener("click",()=>{
  App.setMode(false); // Protonen
  App.resetLHC();
  E.sliEnergy.value = 0.45; s.paramEnergy = 0.45; E.lblEnergy.innerText = "0.45 TeV (Injektion)";
  E.sliIntensity.value = 0.10; s.paramIntensity = 0.10; E.lblIntensity.innerText = "0.10e11 p";
  E.sliBeta.value = 1.5; s.paramBetaStar = 1.5; E.lblBeta.innerText = "1.50 m";
  E.sliRampSpeed.value = 0.02; s.paramRampSpeed = 0.02; E.lblRampSpeed.innerText = "0.02 T/s (Sicher)"; E.lblRampSpeed.style.color = "#58a6ff";
  App.updateReadouts(); selectDetector("ATLAS");
  App.setStatus("PRESET GELADEN: Pilot-Strahl (Inbetriebnahme · 0.45 TeV — zu wenig Energie für Entdeckungen)", "on");
 });

 E.btnAutoColl.addEventListener("click", App.toggleAutoCollide);
 E.btnAuto.addEventListener("click", fuellProtokoll);

 // SLIDERS
 E.sliEnergy.addEventListener("input",()=>{
  s.paramEnergy = parseFloat(E.sliEnergy.value);
  E.lblEnergy.innerText = App.fmtEnergy(s.paramEnergy);   // Einheit modusabhängig (Ionen: TeV/u)
  App.updateReadouts();
  App.drawHist();   // Energie formt das Spektrum (Erzeugbarkeit/Signifikanz) → sofortiges Feedback
 });
 E.sliIntensity.addEventListener("input",()=>{
  s.paramIntensity = parseFloat(E.sliIntensity.value);
  E.lblIntensity.innerText = s.paramIntensity.toFixed(2) + "e11 p";
 });
 E.sliBeta.addEventListener("input",()=>{
  E.lblBeta.innerText = parseFloat(E.sliBeta.value).toFixed(2) + " m";
 });
 E.sliRampSpeed.addEventListener("input",()=>{
  s.paramRampSpeed = parseFloat(E.sliRampSpeed.value);
  if(s.paramRampSpeed > 0.10) {
   E.lblRampSpeed.innerText = s.paramRampSpeed.toFixed(2) + " T/s (⚠️ RISIKO)";
   E.lblRampSpeed.style.color = "#f85149";
  } else {
   E.lblRampSpeed.innerText = s.paramRampSpeed.toFixed(2) + " T/s (Sicher)";
   E.lblRampSpeed.style.color = "#58a6ff";
  }
 });
}
