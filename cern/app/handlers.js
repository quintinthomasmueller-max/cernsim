// ═══════════════════════════════════════════════════════════════════════════
// BUTTON HANDLERS
// ═══════════════════════════════════════════════════════════════════════════
// Manuelles Einzel-Füllen entfernt – Füllen ausschließlich über das Füllprotokoll.

btnSpeedToggle.addEventListener("click",()=>{
  isFastMode = !isFastMode;
  if(isFastMode) {
    btnSpeedToggle.innerText = "⏱️ Tempo: Zeitraffer (schnell)";
    btnSpeedToggle.style.background = "rgba(88,166,255,.08)";
    btnSpeedToggle.style.borderColor = "rgba(88,166,255,.3)";
    btnSpeedToggle.style.color = "#58a6ff";
  } else {
    btnSpeedToggle.innerText = "⏱️ Tempo: Didaktisch (langsam)";
    btnSpeedToggle.style.background = "rgba(227,119,194,.08)";
    btnSpeedToggle.style.borderColor = "rgba(227,119,194,.3)";
    btnSpeedToggle.style.color = "#e377c2";
  }
});

// GEO OVERLAY TOGGLE
let geoVisible = true;
btnToggleGeo.addEventListener("click",()=>{
 geoVisible = !geoVisible;
 document.querySelectorAll(".geo-element").forEach(el=>{
  el.style.opacity = geoVisible ? "1" : "0";
  el.style.pointerEvents = geoVisible ? "auto" : "none";
 });
 btnToggleGeo.classList.toggle("act", geoVisible);
});

// INTERACTIVE SVG CAMERA ZOOM LOGIC
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
  svg.setAttribute("viewBox", `${currentVB.x} ${currentVB.y} ${currentVB.w} ${currentVB.h}`);
  if(p<1) requestAnimationFrame(step);
 }
 requestAnimationFrame(step);
}

function zoomToDetector(name){
 if(zoomTarget === name){
  // Zoom out
  zoomTarget = null;
  btnZoomOut.classList.add("off");
  animateViewBox(0, 0, 700, 480);
 } else {
  zoomTarget = name;
  btnZoomOut.classList.remove("off");
  let tx, ty, tw=160, th=120;
  if(name === "ATLAS") { tx = 270; ty = 360; }
  else if(name === "CMS") { tx = 270; ty = 0; }
  else if(name === "ALICE") { tx = 90; ty = 180; }
  else if(name === "LHCB") { tx = 450; ty = 180; }
  animateViewBox(tx, ty, tw, th);
  
  // Update event display tabs too
  document.querySelectorAll(".cv4-dtab").forEach(t=>t.classList.remove("act"));
  $("dt-"+name.toLowerCase()).classList.add("act");
  selDet=name;
  drawDetBg();
 }
}

btnZoomOut.addEventListener("click", () => {
 zoomTarget = null;
 btnZoomOut.classList.add("off");
 animateViewBox(0, 0, 700, 480);
});

grpAtlas.addEventListener("click", () => zoomToDetector("ATLAS"));
grpCms.addEventListener("click", () => zoomToDetector("CMS"));
grpAlice.addEventListener("click", () => zoomToDetector("ALICE"));
grpLhcb.addEventListener("click", () => zoomToDetector("LHCB"));

// PRESETS CLICK LISTENERS
btnPreHiggs.addEventListener("click",()=>{
 setMode(false); // Protonen
 resetLHC();
 sliEnergy.value = 6.8; paramEnergy = 6.8; lblEnergy.innerText = "6.8 TeV";
 sliIntensity.value = 1.20; paramIntensity = 1.20; lblIntensity.innerText = "1.20e11 p";
 sliBeta.value = 0.3; paramBetaStar = 0.3; lblBeta.innerText = "0.30 m";
 sliRampSpeed.value = 0.05; paramRampSpeed = 0.05; lblRampSpeed.innerText = "0.05 T/s (Sicher)"; lblRampSpeed.style.color = "#58a6ff";
 activePhysicsMode="HIGGS";
 document.querySelectorAll(".cv4-dtab").forEach(t=>t.classList.remove("act"));
 $("dt-atlas").classList.add("act"); selDet="ATLAS";
 updateReadouts(); drawDetBg(); drawHist();
 setStatus("PRESET GELADEN: Higgs-Boson-Suche (Standardmodell p-p Kollision bei 13.6 TeV)", "on");
});

btnPreQgp.addEventListener("click",()=>{
 setMode(true); // Blei-Ionen
 resetLHC();
 sliEnergy.value = 2.5; paramEnergy = 2.5; lblEnergy.innerText = "2.5 TeV";
 sliIntensity.value = 0.90; paramIntensity = 0.90; lblIntensity.innerText = "0.90e11 p";
 sliBeta.value = 0.4; paramBetaStar = 0.4; lblBeta.innerText = "0.40 m";
 sliRampSpeed.value = 0.05; paramRampSpeed = 0.05; lblRampSpeed.innerText = "0.05 T/s (Sicher)"; lblRampSpeed.style.color = "#58a6ff";
 activePhysicsMode="QGP";
 document.querySelectorAll(".cv4-dtab").forEach(t=>t.classList.remove("act"));
 $("dt-alice").classList.add("act"); selDet="ALICE";
 updateReadouts(); drawDetBg(); drawHist();
 setStatus("PRESET GELADEN: Blei-Ionen-Kollision zur Erzeugung des Quark-Gluon-Plasmas in ALICE", "on");
});

btnPreLhcb.addEventListener("click",()=>{
 setMode(false); // Protonen
 resetLHC();
 sliEnergy.value = 6.5; paramEnergy = 6.5; lblEnergy.innerText = "6.5 TeV";
 sliIntensity.value = 1.00; paramIntensity = 1.00; lblIntensity.innerText = "1.00e11 p";
 sliBeta.value = 0.6; paramBetaStar = 0.6; lblBeta.innerText = "0.60 m";
 sliRampSpeed.value = 0.05; paramRampSpeed = 0.05; lblRampSpeed.innerText = "0.05 T/s (Sicher)"; lblRampSpeed.style.color = "#58a6ff";
 activePhysicsMode="LHCB";
 document.querySelectorAll(".cv4-dtab").forEach(t=>t.classList.remove("act"));
 $("dt-lhcb").classList.add("act"); selDet="LHCB";
 updateReadouts(); drawDetBg(); drawHist();
 setStatus("PRESET GELADEN: CP-Verletzung & Schönheit (B-Physik p-p Kollision bei 13 TeV in LHCb)", "on");
});

btnPrePilot.addEventListener("click",()=>{
 setMode(false); // Protonen
 resetLHC();
 sliEnergy.value = 0.45; paramEnergy = 0.45; lblEnergy.innerText = "0.45 TeV (Injektion)";
 sliIntensity.value = 0.10; paramIntensity = 0.10; lblIntensity.innerText = "0.10e11 p";
 sliBeta.value = 1.5; paramBetaStar = 1.5; lblBeta.innerText = "1.50 m";
 sliRampSpeed.value = 0.02; paramRampSpeed = 0.02; lblRampSpeed.innerText = "0.02 T/s (Sicher)"; lblRampSpeed.style.color = "#58a6ff";
 activePhysicsMode="PILOT";
 document.querySelectorAll(".cv4-dtab").forEach(t=>t.classList.remove("act"));
 $("dt-atlas").classList.add("act"); selDet="ATLAS";
 updateReadouts(); drawDetBg(); drawHist();
 setStatus("PRESET GELADEN: Pilot-Strahl (Inbetriebnahme des LHC auf Injektionsniveau)", "on");
});

btnAutoColl.addEventListener("click", toggleAutoCollide);

async function fuellProtokoll(){
 if(filling || ramped || cryoRecovery || (b1Count>=NEEDED && b2Count>=NEEDED)) return;
 filling = true; resetFlag = false;
 btnAuto.classList.add("off");
 sliEnergy.disabled = true; sliIntensity.disabled = true; sliRampSpeed.disabled = true;
 selP.style.pointerEvents = "none"; selI.style.pointerEvents = "none";
 setStatus("FÜLLPROTOKOLL: Injektoren laufen – beide Strahlen werden gepipelinet gefüllt …","on");

 // Gemeinsamer Injektorkomplex; Aufspaltung erst am SPS. Abwechselnd B1 (TI 2) / B2 (TI 8),
 // Kadenz << Kettenlaufzeit -> mehrere Bunches gleichzeitig unterwegs (Pipeline), beide Ringe parallel.
 const queue = [];
 for(let i=0;i<NEEDED;i++){ queue.push(1); queue.push(2); }
 const inflight = [];
 for(const beam of queue){
  if(resetFlag) break;
  inflight.push(injectBunch(beam));
  setStatus(`FÜLLPROTOKOLL: Bunches im Beschleunigerkomplex …  B1 ${b1Count}/${NEEDED}  ·  B2 ${b2Count}/${NEEDED}`,"on");
  await sleep(650 * timeScale());
 }
 await Promise.all(inflight);
 filling = false;
 selP.style.pointerEvents = ""; selI.style.pointerEvents = "";
 if(resetFlag) return;
 btnAuto.classList.remove("off");
 if(b1Count>=NEEDED && b2Count>=NEEDED){
  btnRamp.classList.remove("off");
  setStatus("LHC GEFÜLLT — beide Strahlen stabil. Ramping möglich!","on");
 } else {
  setStatus(`Füllung beendet: B1 ${b1Count}/${NEEDED}, B2 ${b2Count}/${NEEDED}.`,"on");
 }
}
btnAuto.addEventListener("click", fuellProtokoll);

// SLIDERS BINDING
sliEnergy.addEventListener("input",()=>{
 paramEnergy = parseFloat(sliEnergy.value);
 lblEnergy.innerText = paramEnergy.toFixed(1) + " TeV";
 updateReadouts();
});

sliIntensity.addEventListener("input",()=>{
 paramIntensity = parseFloat(sliIntensity.value);
 lblIntensity.innerText = paramIntensity.toFixed(2) + "e11 p";
});

sliBeta.addEventListener("input",()=>{
 lblBeta.innerText = parseFloat(sliBeta.value).toFixed(2) + " m";
});

sliRampSpeed.addEventListener("input",()=>{
 paramRampSpeed = parseFloat(sliRampSpeed.value);
 if(paramRampSpeed > 0.10) {
  lblRampSpeed.innerText = paramRampSpeed.toFixed(2) + " T/s (⚠️ RISIKO)";
  lblRampSpeed.style.color = "#f85149";
 } else {
  lblRampSpeed.innerText = paramRampSpeed.toFixed(2) + " T/s (Sicher)";
  lblRampSpeed.style.color = "#58a6ff";
 }
});

// ═══════════════════════════════════════════════════════════════════════════
// INIT
// ═══════════════════════════════════════════════════════════════════════════
resizeCanvases();
updateReadouts(); drawDetBg(); drawHist();
setStatus("BEREIT — Wähle Teilchenart und starte Injektion","on");

// Handle resize dynamically
window.addEventListener("resize", ()=>{
 resizeCanvases(); drawDetBg(); drawHist();
});

})();
