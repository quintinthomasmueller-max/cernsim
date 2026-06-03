// ═══════════════════════════════════════════════════════════════════════════
// ENGINE — Physik-/Animations-Kern: Injektion, Fluss, Ramp, Squeeze, LHC-Loop,
// Kollisionen, Readouts. Querschnitt über App.state / App.els / App.g (core.js).
// DOM-/SVG-Refs werden bei Boot via main.js#initDom in App.els/App.g befüllt;
// Listener attachen passiert in wireEngine() (nach initDom).
// ═══════════════════════════════════════════════════════════════════════════
import { App, NEEDED, SVG_NS, sleep, $ } from './core.js';

const s = App.state, E = App.els, g = App.g;

// ── Canvas High-DPI backing store ──────────────────────────────────────────
function resizeCanvases(){
 const rEv = E.cvEv.getBoundingClientRect();
 s.evW = rEv.width || 340; s.evH = rEv.height || 180;
 E.cvEv.width = s.evW * s.dpr; E.cvEv.height = s.evH * s.dpr;
 E.cvEv.style.width = s.evW + "px"; E.cvEv.style.height = s.evH + "px";
 E.ctxEv.resetTransform ? E.ctxEv.resetTransform() : null;
 E.ctxEv.scale(s.dpr, s.dpr);

 const rHist = E.cvHist.getBoundingClientRect();
 s.histW = rHist.width || 340; s.histH = rHist.height || 130;
 E.cvHist.width = s.histW * s.dpr; E.cvHist.height = s.histH * s.dpr;
 E.cvHist.style.width = s.histW + "px"; E.cvHist.style.height = s.histH + "px";
 E.ctxHist.resetTransform ? E.ctxHist.resetTransform() : null;
 E.ctxHist.scale(s.dpr, s.dpr);
}

function setMode(ion){
 if(s.isIon===ion && s.b1Count===0 && s.b2Count===0) return;
 s.isIon=ion;
 s.activePhysicsMode = ion ? "QGP" : "HIGGS"; // Injektorwahl setzt Default-Modus (Presets überschreiben)
 E.selP.className="cv4-sel-tab"+(ion?"":" act-p");
 E.selI.className="cv4-sel-tab"+(ion?" act-i":"");
 E.vT.innerText=ion?"Pb⁸²⁺":"Proton";
 E.vT.style.color=ion?"#e377c2":"#58a6ff";
 E.trInj.innerText=ion?"LEIR":"PSB";
 E.b1bar.className="cv4-fill-bar-inner "+(ion?"b1i":"b1");
 E.b2bar.className="cv4-fill-bar-inner "+(ion?"b2i":"b2");
 if(ion){
  document.querySelectorAll(".cv4-dtab").forEach(t=>t.classList.remove("act"));
  $("dt-alice").classList.add("act"); s.selDet="ALICE";
 }
 resetLHC();
 App.drawDetBg(); App.drawHist();
}

function resetLHC(){
 s.resetFlag = true;
 s.autopilotActive = false;
 stopAutoCollide();
 document.querySelectorAll(".traveling-dot").forEach(d=>d.remove());
 E.btnAuto.classList.remove("off");
 s.filling = false; clearIllum();
 s.lhcDots.b1.forEach(d=>d.el.remove()); s.lhcDots.b2.forEach(d=>d.el.remove());
 s.lhcDots={b1:[],b2:[]}; s.b1Count=0; s.b2Count=0; s.collisions=0; App.resetSpectrumData();
 s.ramped=false; s.squeezed=false; s.squeezing=false;
 s.lhcEnergy=s.isIon?177:450; s.lhcSpeed=s.isIon?0.0050:0.0078;
 s.paramBetaStar=1.5;
 E.b1c.innerText="0"; E.b2c.innerText="0"; E.b1bar.style.width="0%"; E.b2bar.style.width="0%";
 E.rbar.style.width="0%"; E.spInfo.innerText="Kollisionen: 0";
 E.btnRamp.classList.add("off"); E.btnSqueeze.classList.add("off"); E.btnColl.classList.add("off");
 E.btnAutoColl.classList.add("off");
 E.sliEnergy.disabled = false; E.sliIntensity.disabled = false; E.sliBeta.value = 1.5; E.sliBeta.disabled = true; E.sliRampSpeed.disabled = false;
 E.lblBeta.innerText = "1.50 m";
 updateReadouts();
 Object.values(g.paths).forEach(p=>{p.classList.remove("lit","lit-i","lit-b2")});
 Object.values(g.nodes).forEach(n=>{n.classList.remove("glow","glow-i","flash")});
 g.paths.lhc.classList.remove("lit","lit-i");
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
function timeScale(){ return s.isFastMode ? 1.0 : 2.6; }

// ── Referenz-gezählte Beleuchtung: Pfad/Knoten leuchtet, solange ≥1 Bunch darauf ist (Pipeline-fähig) ──
const _pathRC = new Map(), _nodeRC = new Map(), _stageRC = [0,0,0,0];
function litClass(){ return s.isIon ? "lit-i" : "lit"; }
function glowClass(){ return s.isIon ? "glow-i" : "glow"; }
function enterPath(el){ if(!el) return; _pathRC.set(el,(_pathRC.get(el)||0)+1); el.classList.add(litClass()); }
function leavePath(el){ if(!el) return; const n=(_pathRC.get(el)||0)-1; _pathRC.set(el,Math.max(0,n)); if(n<=0) el.classList.remove("lit","lit-i","lit-b2"); }
function enterNode(el){ if(!el) return; _nodeRC.set(el,(_nodeRC.get(el)||0)+1); el.classList.add(glowClass()); }
function leaveNode(el){ if(!el) return; const n=(_nodeRC.get(el)||0)-1; _nodeRC.set(el,Math.max(0,n)); if(n<=0) el.classList.remove("glow","glow-i"); }
function renderTracker(){
 g.trSteps.forEach((st,i)=>{
  st.classList.remove("cur","cur-i","done");
  if(i<4 && _stageRC[i]>0) st.classList.add(s.isIon?"cur-i":"cur");
 });
 if(g.trSteps[4] && (s.b1Count>0 || s.b2Count>0)) g.trSteps[4].classList.add(s.isIon?"cur-i":"cur");
}
function stageEnter(i){ _stageRC[i]++; renderTracker(); }
function stageLeave(i){ _stageRC[i]=Math.max(0,_stageRC[i]-1); renderTracker(); }
function clearIllum(){
 _pathRC.clear(); _nodeRC.clear(); for(let i=0;i<4;i++) _stageRC[i]=0;
 Object.values(g.paths).forEach(p=>{ if(p) p.classList.remove("lit","lit-i","lit-b2"); });
 Object.values(g.nodes).forEach(n=>{ if(n) n.classList.remove("glow","glow-i"); });
 g.trSteps.forEach(st=>st.classList.remove("cur","cur-i","done"));
}

// Ein Fluss-Schritt: Stufe betreten -> animieren -> verlassen; bricht bei resetFlag sauber & bilanziert ab.
async function flowStep(dot, pathEl, nodeEl, stageIdx, durKey, ringArgs){
 if(s.resetFlag) return false;
 if(stageIdx!=null) stageEnter(stageIdx);
 if(nodeEl) enterNode(nodeEl);
 enterPath(pathEl);
 if(ringArgs) await orbitRing(dot, ringArgs[0], ringArgs[1], ringArgs[2], ringArgs[3], App.getDurations()[durKey]);
 else         await moveAlongPath(dot, pathEl, App.getDurations()[durKey]);
 leavePath(pathEl);
 if(nodeEl) leaveNode(nodeEl);
 if(stageIdx!=null) stageLeave(stageIdx);
 return !s.resetFlag;
}

// Ein Bunch durchläuft den GEMEINSAMEN Injektorkomplex und wird erst am SPS nach TI 2 (B1) / TI 8 (B2) abgelenkt.
async function injectBunch(beam){
 const ion=s.isIon;
 const R=g.R, J=g.J, paths=g.paths, nodes=g.nodes;
 const color = beam===1 ? (ion?"#e377c2":"#58a6ff") : (ion?"#c77dff":"#ff7f0e");
 const dot=document.createElementNS(SVG_NS,"circle");
 dot.setAttribute("class","traveling-dot"); dot.setAttribute("r","4");
 // KEIN per-Punkt drop-shadow-Filter: SVG-Filter auf bewegten Elementen rastern
 // jeden Frame neu → Ruckeln. Glow stattdessen billig per Stroke (siehe CSS).
 dot.setAttribute("fill",color); dot.setAttribute("stroke",color);
 (E.schematic||E.svg).appendChild(dot);
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
 if(beam===1){ s.b1Count++; E.b1c.innerText=s.b1Count; E.b1bar.style.width=(s.b1Count/NEEDED*100)+"%"; }
 else        { s.b2Count++; E.b2c.innerText=s.b2Count; E.b2bar.style.width=(s.b2Count/NEEDED*100)+"%"; }
 paths.lhc.classList.add(ion?"lit-i":"lit");
 renderTracker();
}

async function doRamp(){
 if(s.ramped||s.filling||s.cryoRecovery) return;
 E.btnRamp.classList.add("off"); E.btnAuto.classList.add("off");
 E.sliEnergy.disabled = true; E.sliIntensity.disabled = true; E.sliRampSpeed.disabled = true;
 setStatus("RAMPING MAGNETFELD & ENERGIE...","on");
 const startE=s.isIon?177:450;
 const maxE=s.isIon?2560:7000;
 const targetE=Math.max(s.paramEnergy*1000, startE);   // nie unter Injektionsenergie -> Ramping BESCHLEUNIGT immer
 const startSpeed=s.isIon?0.0050:0.0078;
 const fullSpeed =s.isIon?0.0095:0.0150;                // Geschwindigkeit bei Maximalenergie
 const eFrac=Math.max(0, Math.min(1,(targetE-startE)/(maxE-startE)));
 const targetSpeed=startSpeed+eFrac*(fullSpeed-startSpeed);  // monoton: targetSpeed >= startSpeed
 const dur = (200 / s.paramRampSpeed) * timeScale();
 let t0=null;
 let quenched = false;
 await new Promise(res=>{
  function step(ts){
   if(!t0) t0=ts;
   let p=Math.min((ts-t0)/dur,1);
   if(s.paramRampSpeed > 0.10 && p > 0.40) { quenched = true; res(); return; }
   s.lhcEnergy=startE+p*(targetE-startE); s.lhcSpeed=startSpeed+p*(targetSpeed-startSpeed);
   E.rbar.style.width=(p*100)+"%"; updateReadouts();
   p<1 ? requestAnimationFrame(step) : res();
  }
  requestAnimationFrame(step);
 });
 if(quenched) { triggerQuench(); return; }
 s.ramped=true; E.btnSqueeze.classList.remove("off"); E.sliBeta.disabled = false;
 setStatus("RAMPING BEENDET — Squeeze-Phase einleiten!","on");
}

function triggerQuench(){
 s.cryoRecovery = true; stopAutoCollide();
 setStatus("💥 MAGNET-QUENCH DETEKTIERT! T > 1.9 K - Strahl gedumpt!", "danger");
 E.sdot.className = "cv4-dot flash";
 E.svg.style.transition = "filter 0.5s";
 E.svg.style.filter = "sepia(1) saturate(3) hue-rotate(320deg)";
 let secLeft = 5;
 function cryoTick(){
  if(secLeft > 0){ setStatus(`💥 MAGNET-QUENCH! Helium-Kühlung läuft... (${secLeft}s)`, "danger"); secLeft--; setTimeout(cryoTick, 1000); }
  else { E.svg.style.filter = "none"; s.cryoRecovery = false; resetLHC(); setStatus("KÜHLUNG ERFOLGREICH — LHC BEREIT", "on"); }
 }
 cryoTick();
}

async function doSqueeze(){
 if(!s.ramped||s.squeezed||s.squeezing||s.cryoRecovery) return;
 s.squeezing = true; E.btnSqueeze.classList.add("off"); E.sliBeta.disabled = true;
 setStatus("🗜️ BEAM SQUEEZE: Fokussiere Strahlen an den IPs...","on");
 let t0 = null; const dur = 2000; const targetBeta = parseFloat(E.sliBeta.value);
 await new Promise(res=>{
  function step(ts){
   if(!t0) t0=ts;
   let p=Math.min((ts-t0)/dur,1);
   s.paramBetaStar = 1.5 - p * (1.5 - targetBeta);
   E.lblBeta.innerText = s.paramBetaStar.toFixed(2) + " m";
   p<1 ? requestAnimationFrame(step) : res();
  }
  requestAnimationFrame(step);
 });
 s.squeezing = false; s.squeezed = true; E.btnColl.classList.remove("off"); E.btnAutoColl.classList.remove("off");
 [g.nodes.atlas,g.nodes.cms,g.nodes.alice,g.nodes.lhcb].forEach(n=>n.classList.add("glow"));
 g.paths.lhc.classList.add(s.isIon?"lit-i":"lit");
 setStatus("STABLE BEAMS — Strahlen fokussiert! Kollisionen bereit.","on");
}

function addPermanentDot(beam){
 const key=beam===1?"b1":"b2";
 const existing=s.lhcDots[key].length;
 const angleOffset=existing*(2*Math.PI/NEEDED);
 const dot=document.createElementNS(SVG_NS,"circle");
 dot.setAttribute("class","lhc-bunch"); dot.setAttribute("r","3.5");
 let c=beam===1?(s.isIon?"#e377c2":"#58a6ff"):(s.isIon?"#c77dff":"#ff7f0e");
 // KEIN drop-shadow-Filter (Perf): die 12 Bunches kreisen jeden Frame.
 dot.setAttribute("fill",c); dot.setAttribute("stroke",c);
 (E.schematic||E.svg).appendChild(dot);
 s.lhcDots[key].push({el:dot,off:angleOffset});
 if(!s.lhcRunning) startLHCLoop();
}

function startLHCLoop(){
 s.lhcRunning=true; s.lhcLastT=null;
 const R=g.R;
 function frame(ts){
  if(!s.lhcLastT) s.lhcLastT=ts;
  let dt=ts-s.lhcLastT; s.lhcLastT=ts;
  s.lhcAngle += (s.lhcSpeed/timeScale())*dt;
  s.lhcDots.b1.forEach(d=>{
   let a=s.lhcAngle+d.off;
   let r=180 + 5.5 * Math.sin(a * 2);
   d.el.setAttribute("cx",R.LHC.cx+r*Math.cos(a)); d.el.setAttribute("cy",R.LHC.cy+r*Math.sin(a));
  });
  s.lhcDots.b2.forEach(d=>{
   let a=-s.lhcAngle+d.off;
   let r=180 - 5.5 * Math.sin(a * 2);
   d.el.setAttribute("cx",R.LHC.cx+r*Math.cos(a)); d.el.setAttribute("cy",R.LHC.cy+r*Math.sin(a));
  });
  if(s.lhcRunning) requestAnimationFrame(frame);
 }
 requestAnimationFrame(frame);
}

function doCollide(){
 if(!s.ramped||!s.squeezed||s.cryoRecovery) return;
 s.collisions+=1; E.spInfo.innerText="Kollisionen: "+s.collisions;
 let detNode=g.nodes[s.selDet.toLowerCase()];
 if(detNode){detNode.classList.add("flash");setTimeout(()=>detNode.classList.remove("flash"),350);}
 App.drawCollisionEvent(App.generateMassData()); App.drawHist();
}

function toggleAutoCollide(){
 if(s.autoCollInterval) stopAutoCollide(); else startAutoCollide();
}

function startAutoCollide(){
 if(!s.ramped || !s.squeezed || s.cryoRecovery) return;
 E.btnAutoColl.innerText = "⏸️ Datennahme stoppen"; E.btnAutoColl.classList.add("act");
 E.btnColl.classList.add("off");
 setStatus("DATENNAHME GESTARTET: Akkumuliere Kollisionsdaten...", "on");
 s.autoCollInterval = setInterval(()=>{
  if(s.cryoRecovery) { stopAutoCollide(); return; }
  s.collisions += 1;
  E.spInfo.innerText = "Kollisionen: " + s.collisions;
  let detNode=g.nodes[s.selDet.toLowerCase()];
  if(detNode){ detNode.classList.add("flash"); setTimeout(()=>detNode.classList.remove("flash"), 75); }
  App.drawCollisionEvent(App.generateMassData()); App.drawHist();
 }, 125);
}

function stopAutoCollide(){
 if(s.autoCollInterval) { clearInterval(s.autoCollInterval); s.autoCollInterval = null; }
 E.btnAutoColl.innerText = "▶️ Auto-Datennahme"; E.btnAutoColl.classList.remove("act");
 setStatus("DATENNAHME GESTOPPT", "on");
 if(s.ramped && s.squeezed && !s.cryoRecovery) E.btnColl.classList.remove("off");
}

function updateReadouts(){
 E.vE.innerText=(s.lhcEnergy/1000).toFixed(2)+" TeV"+(s.isIon?"/u":"");
 // Dipolfeld: für Pb-Ionen Ladungs-zu-Massenzahl-Verhältnis (Z/A=82/208) berücksichtigen
 let rig=0.299792458*2803.95;
 let B=(s.isIon?(208/82):1)*s.lhcEnergy/rig; E.vB.innerText=B.toFixed(3)+" T";
 // Lorentz-γ PRO NUKLEON: E_Nukleon / m_Nukleon (Ion: 0.9315 GeV, Proton: 0.938272 GeV)
 let gam=s.lhcEnergy/(s.isIon?0.9315:0.938272); E.vG.innerText=Math.round(gam).toLocaleString("de-DE");
}

function setStatus(txt,cls){ E.stxt.innerText=txt; E.sdot.className="cv4-dot "+cls; }

// ── Registrierung der öffentlichen API ──────────────────────────────────────
App.resizeCanvases = resizeCanvases;
App.setMode = setMode;
App.resetLHC = resetLHC;
App.timeScale = timeScale;
App.injectBunch = injectBunch;
App.toggleAutoCollide = toggleAutoCollide;
App.stopAutoCollide = stopAutoCollide;
App.updateReadouts = updateReadouts;
App.setStatus = setStatus;

// ── Listener (nach initDom in main.js aufgerufen) ───────────────────────────
export function wireEngine(){
 E.selP.addEventListener("click",()=>{ if(s.filling)return; setMode(false); });
 E.selI.addEventListener("click",()=>{ if(s.filling)return; setMode(true); });
 E.btnRamp.addEventListener("click", doRamp);
 E.btnSqueeze.addEventListener("click", doSqueeze);
 E.btnColl.addEventListener("click", doCollide);
 // Golden-Event: Klick aufs Display friert ein Signal-Event ein (bzw. löst es wieder).
 E.cvEv.addEventListener("click",()=>{
  if(s.goldenEvent){ s.goldenEvent=null; }
  else if(s.lastEvent && s.lastEvent.signal){ s.goldenEvent=s.lastEvent; }
  App.drawCollisionEvent(s.lastEvent);
 });
 E.cvEv.style.cursor="pointer";
}
