// ═══════════════════════════════════════════════════════════════════════════
// DOM REFERENCES
// ═══════════════════════════════════════════════════════════════════════════
const $=id=>document.getElementById(id);
const sdot=$("sdot"),stxt=$("stxt");
const btnRamp=$("btn-ramp"),btnColl=$("btn-coll"),btnAuto=$("btn-auto"),btnSqueeze=$("btn-squeeze");
const btnAutoColl=$("btn-autocoll"),btnSpeedToggle=$("btn-speed-toggle");
const b1c=$("b1c"),b2c=$("b2c"),b1bar=$("b1bar"),b2bar=$("b2bar"),rbar=$("rbar");
const vE=$("v-e"),vB=$("v-b"),vG=$("v-g"),vT=$("v-t");
const spInfo=$("sp-info");
const sliEnergy=$("sli-energy"), sliIntensity=$("sli-intensity"), sliBeta=$("sli-beta"), sliRampSpeed=$("sli-rampspeed");
const lblEnergy=$("lbl-energy"), lblIntensity=$("lbl-intensity"), lblBeta=$("lbl-beta"), lblRampSpeed=$("lbl-rampspeed");
const trSteps=["tr-src","tr-inj","tr-ps","tr-sps","tr-lhc"].map($);
const trInj=$("tr-inj");
const selP=$("sel-p"),selI=$("sel-i");

const btnToggleGeo=$("btn-toggle-geo");
const btnPreHiggs=$("btn-pre-higgs"),btnPreQgp=$("btn-pre-qgp"),btnPreLhcb=$("btn-pre-lhcb"),btnPrePilot=$("btn-pre-pilot");
const btnZoomOut=$("btn-zoom-out");
const grpAtlas=$("grp-atlas"),grpCms=$("grp-cms"),grpAlice=$("grp-alice"),grpLhcb=$("grp-lhcb");

// SVG path elements
const paths={
 linac4:$("p-linac4"), psb:$("p-psb"), psbPs:$("p-psb-ps"),
 linac3:$("p-linac3"), leir:$("p-leir"), leirPs:$("p-leir-ps"),
 ps:$("p-ps"), psSps:$("p-ps-sps"), sps:$("p-sps"),
 ti2:$("p-ti2"), ti8:$("p-ti8"), lhc:$("p-lhc")
};
const nodes={
 linac4:$("n-linac4"), psb:$("n-psb"), linac3:$("n-linac3"), leir:$("n-leir"),
 ps:$("n-ps"), sps:$("n-sps"),
 atlas:$("d-atlas"), cms:$("d-cms"), alice:$("d-alice"), lhcb:$("d-lhcb")
};

// Canvas references
const cvEv=$("cv-ev"), ctxEv=cvEv.getContext("2d");
const cvHist=$("cv-hist"), ctxHist=cvHist.getContext("2d");

// High-DPI Resolution backing store setup for super crisp Retinas
let dpr = window.devicePixelRatio || 1;
let evW = 340, evH = 180, histW = 340, histH = 130;

function resizeCanvases(){
 // Resize Event Display
 const rEv = cvEv.getBoundingClientRect();
 evW = rEv.width || 340;
 evH = rEv.height || 180;
 cvEv.width = evW * dpr;
 cvEv.height = evH * dpr;
 cvEv.style.width = evW + "px";
 cvEv.style.height = evH + "px";
 ctxEv.resetTransform ? ctxEv.resetTransform() : null;
 ctxEv.scale(dpr, dpr);
 
 // Resize Histogram
 const rHist = cvHist.getBoundingClientRect();
 histW = rHist.width || 340;
 histH = rHist.height || 130;
 cvHist.width = histW * dpr;
 cvHist.height = histH * dpr;
 cvHist.style.width = histW + "px";
 cvHist.style.height = histH + "px";
 ctxHist.resetTransform ? ctxHist.resetTransform() : null;
 ctxHist.scale(dpr, dpr);
}

// Detektor-Tab-Klicks werden zentral in handlers.js (selectDetector) gebunden.

selP.addEventListener("click",()=>{ if(filling)return; setMode(false); });
selI.addEventListener("click",()=>{ if(filling)return; setMode(true); });

function setMode(ion){
 if(isIon===ion && b1Count===0 && b2Count===0) return;
 isIon=ion;
 activePhysicsMode = ion ? "QGP" : "HIGGS"; // Injektorwahl setzt Default-Modus (Presets überschreiben)
 selP.className="cv4-sel-tab"+(ion?"":" act-p");
 selI.className="cv4-sel-tab"+(ion?" act-i":"");
 vT.innerText=ion?"Pb⁸²⁺":"Proton";
 vT.style.color=ion?"#e377c2":"#58a6ff";
 trInj.innerText=ion?"LEIR":"PSB";
 b1bar.className="cv4-fill-bar-inner "+(ion?"b1i":"b1");
 b2bar.className="cv4-fill-bar-inner "+(ion?"b2i":"b2");
 if(ion){
  document.querySelectorAll(".cv4-dtab").forEach(t=>t.classList.remove("act"));
  $("dt-alice").classList.add("act"); selDet="ALICE";
 }
 resetLHC();
 drawDetBg(); drawHist();
}

function resetLHC(){
 resetFlag = true;
 autopilotActive = false;
 stopAutoCollide();
 document.querySelectorAll(".traveling-dot").forEach(d=>d.remove());
 btnAuto.classList.remove("off");
 filling = false; clearIllum();
 lhcDots.b1.forEach(d=>d.el.remove()); lhcDots.b2.forEach(d=>d.el.remove());
 lhcDots={b1:[],b2:[]}; b1Count=0; b2Count=0; collisions=0; resetSpectrumData();
 ramped=false; squeezed=false; squeezing=false;
 lhcEnergy=isIon?177:450; lhcSpeed=isIon?0.0050:0.0078;
 paramBetaStar=1.5;
 b1c.innerText="0"; b2c.innerText="0"; b1bar.style.width="0%"; b2bar.style.width="0%";
 rbar.style.width="0%"; spInfo.innerText="Kollisionen: 0";
 btnRamp.classList.add("off"); btnSqueeze.classList.add("off"); btnColl.classList.add("off");
 btnAutoColl.classList.add("off");
 sliEnergy.disabled = false; sliIntensity.disabled = false; sliBeta.value = 1.5; sliBeta.disabled = true; sliRampSpeed.disabled = false;
 lblBeta.innerText = "1.50 m";
 updateReadouts();
 Object.values(paths).forEach(p=>{p.classList.remove("lit","lit-i","lit-b2")});
 Object.values(nodes).forEach(n=>{n.classList.remove("glow","glow-i","flash")});
 paths.lhc.classList.remove("lit","lit-i");
 setStatus("BEREIT","on");
}

async function moveAlongPath(dot, pathEl, dur){
 return new Promise(res=>{
  const len=pathEl.getTotalLength();
  let t0=null;
  function step(ts){
   if(!t0) t0=ts;
   let p=Math.min((ts-t0)/dur,1);
   let pt=pathEl.getPointAtLength(p*len);
   dot.setAttribute("cx",pt.x); dot.setAttribute("cy",pt.y);
   p<1 ? requestAnimationFrame(step) : res();
  }
  requestAnimationFrame(step);
 });
}

async function orbitRing(dot, ring, entryA, exitA, orbits, dur){
  let partial=((exitA-entryA)%(2*Math.PI)+2*Math.PI)%(2*Math.PI);
  let totalA=orbits*2*Math.PI+partial;
  return new Promise(res=>{
   let t0=null;
   function step(ts){
    if(!t0) t0=ts;
    let p=Math.min((ts-t0)/dur,1);
    let a=entryA+p*totalA;
    dot.setAttribute("cx",ring.cx+ring.r*Math.cos(a));
    dot.setAttribute("cy",ring.cy+ring.r*Math.sin(a));
    p<1 ? requestAnimationFrame(step) : res();
   }
   requestAnimationFrame(step);
  });
}

// ── Einheitlicher Zeit-Faktor: skaliert ALLE Abläufe (Injektion, LHC-Rotation, Ramp) kohärent ──
function timeScale(){ return isFastMode ? 1.0 : 2.6; }
const sleep = ms => new Promise(r=>setTimeout(r, ms));

// ── Referenz-gezählte Beleuchtung: Pfad/Knoten leuchtet, solange ≥1 Bunch darauf ist (Pipeline-fähig) ──
const _pathRC = new Map(), _nodeRC = new Map(), _stageRC = [0,0,0,0];
function litClass(){ return isIon ? "lit-i" : "lit"; }
function glowClass(){ return isIon ? "glow-i" : "glow"; }
function enterPath(el){ if(!el) return; _pathRC.set(el,(_pathRC.get(el)||0)+1); el.classList.add(litClass()); }
function leavePath(el){ if(!el) return; const n=(_pathRC.get(el)||0)-1; _pathRC.set(el,Math.max(0,n)); if(n<=0) el.classList.remove("lit","lit-i","lit-b2"); }
function enterNode(el){ if(!el) return; _nodeRC.set(el,(_nodeRC.get(el)||0)+1); el.classList.add(glowClass()); }
function leaveNode(el){ if(!el) return; const n=(_nodeRC.get(el)||0)-1; _nodeRC.set(el,Math.max(0,n)); if(n<=0) el.classList.remove("glow","glow-i"); }
function renderTracker(){
 trSteps.forEach((s,i)=>{
  s.classList.remove("cur","cur-i","done");
  if(i<4 && _stageRC[i]>0) s.classList.add(isIon?"cur-i":"cur");
 });
 if(trSteps[4] && (b1Count>0 || b2Count>0)) trSteps[4].classList.add(isIon?"cur-i":"cur");
}
function stageEnter(i){ _stageRC[i]++; renderTracker(); }
function stageLeave(i){ _stageRC[i]=Math.max(0,_stageRC[i]-1); renderTracker(); }
function clearIllum(){
 _pathRC.clear(); _nodeRC.clear(); for(let i=0;i<4;i++) _stageRC[i]=0;
 Object.values(paths).forEach(p=>{ if(p) p.classList.remove("lit","lit-i","lit-b2"); });
 Object.values(nodes).forEach(n=>{ if(n) n.classList.remove("glow","glow-i"); });
 trSteps.forEach(s=>s.classList.remove("cur","cur-i","done"));
}

// Ein Fluss-Schritt: Stufe betreten -> animieren -> verlassen; bricht bei resetFlag sauber & bilanziert ab.
async function flowStep(dot, pathEl, nodeEl, stageIdx, durKey, ringArgs){
 if(resetFlag) return false;
 if(stageIdx!=null) stageEnter(stageIdx);
 if(nodeEl) enterNode(nodeEl);
 enterPath(pathEl);
 if(ringArgs) await orbitRing(dot, ringArgs[0], ringArgs[1], ringArgs[2], ringArgs[3], getDurations()[durKey]);
 else         await moveAlongPath(dot, pathEl, getDurations()[durKey]);
 leavePath(pathEl);
 if(nodeEl) leaveNode(nodeEl);
 if(stageIdx!=null) stageLeave(stageIdx);
 return !resetFlag;
}

// Ein Bunch durchläuft den GEMEINSAMEN Injektorkomplex und wird erst am SPS nach TI 2 (B1) / TI 8 (B2) abgelenkt.
async function injectBunch(beam){
 const ion=isIon;
 const color = beam===1 ? (ion?"#e377c2":"#58a6ff") : (ion?"#c77dff":"#ff7f0e");
 const dot=document.createElementNS(SVG_NS,"circle");
 dot.setAttribute("class","traveling-dot"); dot.setAttribute("r","4");
 dot.setAttribute("fill",color); dot.style.filter="drop-shadow(0 0 4px "+color+")";
 svg.appendChild(dot);
 const fin=()=>{ dot.remove(); };

 const lp=ion?paths.linac3:paths.linac4, ln=ion?nodes.linac3:nodes.linac4;
 if(!await flowStep(dot, lp, ln, 0, 'linac')) return fin();

 const r1=ion?R.LEIR:R.PSB, r1p=ion?paths.leir:paths.psb, r1n=ion?nodes.leir:nodes.psb;
 const r1e=ion?J.LEIR_ENTRY:J.PSB_ENTRY, r1x=ion?J.LEIR_EXIT:J.PSB_EXIT;
 if(!await flowStep(dot, r1p, r1n, 1, 'ring1', [r1, r1e, r1x, 3])) return fin();
 if(!await flowStep(dot, ion?paths.leirPs:paths.psbPs, null, null, 'trToPs')) return fin();

 const psE=ion?J.PS_FROM_LEIR:J.PS_FROM_PSB;
 if(!await flowStep(dot, paths.ps, nodes.ps, 2, 'ps', [R.PS, psE, J.PS_EXIT, 3])) return fin();
 if(!await flowStep(dot, paths.psSps, null, null, 'trToSps')) return fin();

 const spsExit=beam===1?J.SPS_TI2:J.SPS_TI8;
 if(!await flowStep(dot, paths.sps, nodes.sps, 3, 'sps', [R.SPS, J.SPS_ENTRY, spsExit, 2])) return fin();
 if(!await flowStep(dot, beam===1?paths.ti2:paths.ti8, null, null, 'ti')) return fin();

 dot.remove();
 addPermanentDot(beam);
 if(beam===1){ b1Count++; b1c.innerText=b1Count; b1bar.style.width=(b1Count/NEEDED*100)+"%"; }
 else        { b2Count++; b2c.innerText=b2Count; b2bar.style.width=(b2Count/NEEDED*100)+"%"; }
 paths.lhc.classList.add(ion?"lit-i":"lit");
 renderTracker();
}

btnRamp.addEventListener("click",async()=>{
 if(ramped||filling||cryoRecovery) return;
 btnRamp.classList.add("off"); btnAuto.classList.add("off");
 sliEnergy.disabled = true; sliIntensity.disabled = true; sliRampSpeed.disabled = true;
 setStatus("RAMPING MAGNETFELD & ENERGIE...","on");
 const startE=isIon?177:450;
 const maxE=isIon?2560:7000;
 const targetE=Math.max(paramEnergy*1000, startE);   // nie unter Injektionsenergie -> Ramping BESCHLEUNIGT immer
 const startSpeed=isIon?0.0050:0.0078;
 const fullSpeed =isIon?0.0095:0.0150;                // Geschwindigkeit bei Maximalenergie
 const eFrac=Math.max(0, Math.min(1,(targetE-startE)/(maxE-startE)));
 const targetSpeed=startSpeed+eFrac*(fullSpeed-startSpeed);  // monoton: targetSpeed >= startSpeed
 const dur = (200 / paramRampSpeed) * timeScale();
 let t0=null;
 let quenched = false;
 await new Promise(res=>{
  function step(ts){
   if(!t0) t0=ts;
   let p=Math.min((ts-t0)/dur,1);
   if(paramRampSpeed > 0.10 && p > 0.40) { quenched = true; res(); return; }
   lhcEnergy=startE+p*(targetE-startE); lhcSpeed=startSpeed+p*(targetSpeed-startSpeed);
   rbar.style.width=(p*100)+"%"; updateReadouts();
   p<1 ? requestAnimationFrame(step) : res();
  }
  requestAnimationFrame(step);
 });
 if(quenched) { triggerQuench(); return; }
 ramped=true; btnSqueeze.classList.remove("off"); sliBeta.disabled = false;
 setStatus("RAMPING BEENDET — Squeeze-Phase einleiten!","on");
});

function triggerQuench(){
 cryoRecovery = true; stopAutoCollide();
 setStatus("💥 MAGNET-QUENCH DETEKTIERT! T > 1.9 K - Strahl gedumpt!", "danger");
 sdot.className = "cv4-dot flash";
 svg.style.transition = "filter 0.5s";
 svg.style.filter = "sepia(1) saturate(3) hue-rotate(320deg)";
 let secLeft = 5;
 function cryoTick(){
  if(secLeft > 0){ setStatus(`💥 MAGNET-QUENCH! Helium-Kühlung läuft... (${secLeft}s)`, "danger"); secLeft--; setTimeout(cryoTick, 1000); }
  else { svg.style.filter = "none"; cryoRecovery = false; resetLHC(); setStatus("KÜHLUNG ERFOLGREICH — LHC BEREIT", "on"); }
 }
 cryoTick();
}

btnSqueeze.addEventListener("click",async()=>{
 if(!ramped||squeezed||squeezing||cryoRecovery) return;
 squeezing = true; btnSqueeze.classList.add("off"); sliBeta.disabled = true;
 setStatus("🗜️ BEAM SQUEEZE: Fokussiere Strahlen an den IPs...","on");
 let t0 = null; const dur = 2000; const targetBeta = parseFloat(sliBeta.value);
 await new Promise(res=>{
  function step(ts){
   if(!t0) t0=ts;
   let p=Math.min((ts-t0)/dur,1);
   paramBetaStar = 1.5 - p * (1.5 - targetBeta);
   lblBeta.innerText = paramBetaStar.toFixed(2) + " m";
   p<1 ? requestAnimationFrame(step) : res();
  }
  requestAnimationFrame(step);
 });
 squeezing = false; squeezed = true; btnColl.classList.remove("off"); btnAutoColl.classList.remove("off");
 [nodes.atlas,nodes.cms,nodes.alice,nodes.lhcb].forEach(n=>n.classList.add("glow"));
 paths.lhc.classList.add(isIon?"lit-i":"lit");
 setStatus("STABLE BEAMS — Strahlen fokussiert! Kollisionen bereit.","on");
});

function addPermanentDot(beam){
 const key=beam===1?"b1":"b2";
 const existing=lhcDots[key].length;
 const angleOffset=existing*(2*Math.PI/NEEDED);
 const dot=document.createElementNS(SVG_NS,"circle");
 dot.setAttribute("r","3.5");
 let c=beam===1?(isIon?"#e377c2":"#58a6ff"):(isIon?"#c77dff":"#ff7f0e");
 dot.setAttribute("fill",c); dot.style.filter="drop-shadow(0 0 3px "+c+")";
 svg.appendChild(dot);
 lhcDots[key].push({el:dot,off:angleOffset});
 if(!lhcRunning) startLHCLoop();
}

function startLHCLoop(){
 lhcRunning=true; lhcLastT=null;
 function frame(ts){
  if(!lhcLastT) lhcLastT=ts;
  let dt=ts-lhcLastT; lhcLastT=ts;
  lhcAngle += (lhcSpeed/timeScale())*dt;
  lhcDots.b1.forEach(d=>{
   let a=lhcAngle+d.off;
   let r=180 + 5.5 * Math.sin(a * 2);
   d.el.setAttribute("cx",R.LHC.cx+r*Math.cos(a)); d.el.setAttribute("cy",R.LHC.cy+r*Math.sin(a));
  });
  lhcDots.b2.forEach(d=>{
   let a=-lhcAngle+d.off;
   let r=180 - 5.5 * Math.sin(a * 2);
   d.el.setAttribute("cx",R.LHC.cx+r*Math.cos(a)); d.el.setAttribute("cy",R.LHC.cy+r*Math.sin(a));
  });
  if(lhcRunning) requestAnimationFrame(frame);
 }
 requestAnimationFrame(frame);
}

btnColl.addEventListener("click",()=>{
 if(!ramped||!squeezed||cryoRecovery) return;
 collisions+=1; spInfo.innerText="Kollisionen: "+collisions;
 let detNode=nodes[selDet.toLowerCase()];
 if(detNode){detNode.classList.add("flash");setTimeout(()=>detNode.classList.remove("flash"),350);}
 drawCollisionEvent(generateMassData()); drawHist();
});

// Golden-Event: Klick aufs Display friert ein Signal-Event ein (bzw. löst es wieder).
cvEv.addEventListener("click",()=>{
 if(goldenEvent){ goldenEvent=null; }
 else if(lastEvent && lastEvent.signal){ goldenEvent=lastEvent; }
 drawCollisionEvent(lastEvent);
});
cvEv.style.cursor="pointer";

function toggleAutoCollide(){
 if(autoCollInterval) stopAutoCollide(); else startAutoCollide();
}

function startAutoCollide(){
 if(!ramped || !squeezed || cryoRecovery) return;
 btnAutoColl.innerText = "⏸️ Datennahme stoppen"; btnAutoColl.classList.add("act");
 btnColl.classList.add("off");
 setStatus("DATENNAHME GESTARTET: Akkumuliere Kollisionsdaten...", "on");
 autoCollInterval = setInterval(()=>{
  if(cryoRecovery) { stopAutoCollide(); return; }
  collisions += 1;
  spInfo.innerText = "Kollisionen: " + collisions;
  let detNode=nodes[selDet.toLowerCase()];
  if(detNode){ detNode.classList.add("flash"); setTimeout(()=>detNode.classList.remove("flash"), 75); }
  drawCollisionEvent(generateMassData()); drawHist();
 }, 125);
}

function stopAutoCollide(){
 if(autoCollInterval) { clearInterval(autoCollInterval); autoCollInterval = null; }
 btnAutoColl.innerText = "▶️ Auto-Datennahme"; btnAutoColl.classList.remove("act");
 setStatus("DATENNAHME GESTOPPT", "on");
 if(ramped && squeezed && !cryoRecovery) btnColl.classList.remove("off");
}

function updateReadouts(){
 vE.innerText=(lhcEnergy/1000).toFixed(2)+" TeV"+(isIon?"/u":"");
 // Dipolfeld: für Pb-Ionen Ladungs-zu-Massenzahl-Verhältnis (Z/A=82/208) berücksichtigen
 let rig=0.299792458*2803.95;
 let B=(isIon?(208/82):1)*lhcEnergy/rig; vB.innerText=B.toFixed(3)+" T";
 // Lorentz-γ PRO NUKLEON: E_Nukleon / m_Nukleon (Ion: 0.9315 GeV, Proton: 0.938272 GeV)
 let g=lhcEnergy/(isIon?0.9315:0.938272); vG.innerText=Math.round(g).toLocaleString("de-DE");
}

function setStatus(txt,cls){stxt.innerText=txt;sdot.className="cv4-dot "+cls;}

