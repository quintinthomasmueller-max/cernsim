// ═══════════════════════════════════════════════════════════════════════════
// ENGINE — Physik-/Animations-Kern: Injektion, Fluss, Ramp, Squeeze, LHC-Loop,
// Kollisionen, Readouts. Querschnitt über App.state / App.els / App.g (core.js).
// DOM-/SVG-Refs werden bei Boot via main.js#initDom in App.els/App.g befüllt;
// Listener attachen passiert in wireEngine() (nach initDom).
// ═══════════════════════════════════════════════════════════════════════════
import { App, FILL, REAL_SPS_CYCLE_S, SIM_SCALE, DT_SCALE, BEAM_LIFETIME_H, DUMP_FRAC, STAT_RATE, SVG_NS, sleep, $ } from './core.js';

const s = App.state, E = App.els, g = App.g;

// ── Geo-Zwillinge: jeder wandernde/kreisende Schema-Punkt bekommt einen Punkt in der
// Realansicht (#geo-layer), der mit DEMSELBEN Fortschritt p / Winkel entlang der Geo-
// Geometrie laeuft (App.geoRails/App.geoRings aus geo.ts) → beide Ansichten sind per
// Konstruktion synchron. CSS-Display zeigt je Modus den richtigen; die Punktgroesse
// trennt Injektor-Zoom (klein, im Vollbild unsichtbar) von SPS/LHC-Vollbild (gross,
// im Zoom ausserhalb des Fensters). Fehlt die Geo-Ebene → keine Zwillinge (Schema
// unveraendert; jsdom-Tests fuellen nicht → getPointAtLength wird nie aufgerufen).
function geoLen(el){ try { return el.__glen || (el.__glen = el.getTotalLength()); } catch(e){ return 0; } }
function mkTwin(beam, rPx){
 if(!E.geoLayer || !App.geoRails) return null;
 const t=document.createElementNS(SVG_NS,"circle");
 t.setAttribute("class","geo-twin"); t.setAttribute("r",rPx);
 // NUR Fill, KEINE Stroke: eine Default-Stroke (1 User-Unit) wuerde im ~53x-Injektor-
 // Zoom zu einem riesigen Blob (~53 px) skalieren. Groesse = r (mit der Zoomstufe).
 t.setAttribute("fill",beamColor(beam)); t.setAttribute("stroke","none");
 (t as any).style.pointerEvents="none"; E.geoLayer.appendChild(t); return t;
}
function twinR(el, rPx){ if(el) el.setAttribute("r", rPx); }
function placeTwinPath(el, railEl, frac){
 if(!el || !railEl) return; const L=geoLen(railEl); if(!L) return;
 try { const pt=railEl.getPointAtLength(Math.max(0,Math.min(1,frac))*L); el.setAttribute("cx",pt.x); el.setAttribute("cy",pt.y); } catch(e){}
}
function placeTwinRing(el, ring, a){ if(!el || !ring) return; el.setAttribute("cx",ring.cx+ring.r*Math.cos(a)); el.setAttribute("cy",ring.cy+ring.r*Math.sin(a)); }
function endDot(el){ if(!el) return; if(el.__geo){ el.__geo.remove(); el.__geo=null; } el.remove(); }
// velKey (+ Strahl/Ion) → Geo-Rail des aktuellen Schritts. r = Geo-Punktgroesse.
// entryA/exitA: vorberechnete Geo-Ring-Winkel aus App.geoRails (geo.ts#buildGeoRails)
// fuer lueckenlose Twin-Uebergaenge zwischen Linac→Ring→Transfer→Ring→TI.
function geoRailFor(velKey, beam){
 const R=App.geoRails||{}, RG=App.geoRings||{}, ion=s.isIon, ps=RG.ps;
 switch(velKey){
  case 'linac':   return { kind:'path', el: ion?R.linac3:R.linac4, r:0.18 };
  case 'ring1':   { const rg=ion?RG.leir:RG.psb;
    return { kind:'ring', ring:rg, r:0.18,
      entryA: ion?(R.leirEntryA??Math.PI):(R.psbEntryA??Math.PI),
      exitA:  ion?(R.leirExitA??0):(R.psbExitA??0) }; }
  case 'trToPs':  return { kind:'path', el: ion?R.leirPs:R.psbPs, r:0.18 };
  case 'ps':      return { kind:'ring', ring:ps, r:0.20,
    entryA: ion?(R.psEntryFromLeirA??Math.PI):(R.psEntryFromPsbA??Math.PI),
    exitA:  R.psExitA??0 };
  case 'trToSps': return { kind:'path', el: R.psSps, r:0.22 };
  case 'sps':     return { kind:'ring', ring:RG.sps, r:2.4,
    entryA: R.spsEntryA??Math.PI,
    exitA:  beam===1?(R.spsExitB1A??0):(R.spsExitB2A??0) };
  case 'ti':      return { kind:'path', el: beam===1?R.ti2:R.ti8, r:2.4 };
 }
 return null;
}

// Aktuelle Füll-Konfig (Protonen vs. Pb-Ionen) + abgeleitete Batch-/Zug-Zahlen.
const fc = () => s.isIon ? FILL.ion : FILL.proton;
const totalBatches = () => Math.round(fc().total / fc().psBatch);          // PS-Batches/Strahl
const trainsTotal = () => Math.ceil(totalBatches() / fc().batchesPerTrain); // umlaufende Züge
// Füllstand-Text in ECHTEN Bunches (geparkte/umlaufende Batches × psBatch / Soll).
const fillLabel = (batches) => `${(batches * fc().psBatch).toLocaleString("de-DE")} / ${fc().total.toLocaleString("de-DE")}`;
// Zeitraffer: reale Sekunden je Darstellungssekunde + SPS-Zug-Abstand (25 s / Faktor).
const simScale = () => s.isFastMode ? SIM_SCALE.fast : SIM_SCALE.slow;
const trainCadenceMs = () => REAL_SPS_CYCLE_S * 1000 / simScale();

// ── Canvas High-DPI backing store ──────────────────────────────────────────
// WICHTIG: Die ANZEIGEGRÖSSE bleibt komplett CSS-gesteuert (width:100% etc.).
// Wir setzen NUR den Backing-Store (canvas.width/height = Anzeigegröße·dpr) und
// NIE canvas.style.width/height. Frühere Versionen schrieben die gemessene
// Pixelgröße als Inline-Style zurück — lief das beim Boot (document "loading",
// Layout noch 0 breit), fror es eine falsche Größe ein und überschrieb das
// responsive CSS dauerhaft (Event-Display/Histogramm verzerrt/überdimensioniert).
// clientWidth/Height = aktuelle, per CSS bestimmte Box → Quelle der Wahrheit.
function fitCanvas(cv, ctx, fbW, fbH){
 const w = cv.clientWidth || fbW, h = cv.clientHeight || fbH;
 const bw = Math.round(w * s.dpr), bh = Math.round(h * s.dpr);
 if(cv.width !== bw)  cv.width  = bw;   // setzt Backing-Store (löscht Canvas)
 if(cv.height !== bh) cv.height = bh;
 ctx.resetTransform ? ctx.resetTransform() : ctx.setTransform(1,0,0,1,0,0);
 ctx.scale(s.dpr, s.dpr);
 return {w, h};
}
function resizeCanvases(){
 const ev = fitCanvas(E.cvEv, E.ctxEv, 340, 180);   s.evW = ev.w;   s.evH = ev.h;
 const hi = fitCanvas(E.cvHist, E.ctxHist, 340, 130); s.histW = hi.w; s.histH = hi.h;
}

// Deutsche Zahlformatierung (Komma als Dezimaltrennzeichen) — einheitlich für
// alle physikalischen Anzeigewerte (Energie, Feld, Fokus, Intensität).
const de = (v, d) => v.toLocaleString("de-DE", { minimumFractionDigits: d, maximumFractionDigits: d });
App.de = de;
// Energie-Label mit modusabhängiger Einheit (Ionen: pro Nukleon, NICHT /u — u ist
// nur näherungsweise die Nukleonmasse).
function fmtEnergy(v){ return de(v, 2) + (s.isIon ? " TeV/Nukleon" : " TeV"); }
// Bunch-Intensität: Protonen ~10¹¹/Bunch, Blei-Ionen ~10⁸/Bunch (anderer Maßstab).
function fmtIntensity(v){ return de(v, 2) + (s.isIon ? "·10⁸ Ionen" : "·10¹¹ p"); }
App.fmtEnergy = fmtEnergy;
App.fmtIntensity = fmtIntensity;

function setMode(ion){
 if(s.isIon===ion && s.b1Count===0 && s.b2Count===0) return;
 s.isIon=ion;
 E.vT.innerText=ion?"Pb⁸²⁺":"Proton";
 E.vT.style.color=ion?"#e377c2":"#58a6ff";
 E.trInj.innerText=ion?"LEIR":"PSB";
 E.b1bar.className="cv4-fill-bar-inner "+(ion?"b1i":"b1");
 E.b2bar.className="cv4-fill-bar-inner "+(ion?"b2i":"b2");
 // Pb-Ionen: max. Steifigkeit der Dipole entspricht 2,76 TeV/u (= 6,8 TeV·Z/A bei
 // gleicher Magnetfeldstärke) — Ziel-Energie physikalisch klemmen.
 if(ion && s.paramEnergy > 2.76){ s.paramEnergy = 2.76; }
 E.lblEnergy.innerText = fmtEnergy(s.paramEnergy);
 if(ion){
  document.querySelectorAll(".cv4-dtab").forEach(t=>t.classList.remove("act"));
  $("dt-alice").classList.add("act"); s.selDet="ALICE";
 }
 resetLHC();
 App.drawDetBg(); App.drawHist();
}

// keepData=true (Strahl-Dump): Strahl/Beschleuniger zurücksetzen, aber die
// AKKUMULIERTEN Physikdaten (Spektrum/Signifikanz) BEHALTEN → mehrere Fills
// summieren sich zur Entdeckung (real). Default (Moduswechsel/Quench/Preset): alles.
function resetLHC(keepData=false){
 s.resetFlag = true;
 // Generationen-Token: noch fliegende Batches/Züge älterer Füll-Läufe brechen ab,
 // AUCH wenn ein sofort gestarteter neuer Lauf resetFlag wieder auf false setzt
 // (sonst zählten unsichtbare Zombie-Batches im neuen Lauf doppelt — Race).
 s.fillGen = (s.fillGen || 0) + 1;
 s.dumping = false;
 stopAutoCollide();
 document.querySelectorAll(".traveling-dot").forEach(d=>d.remove());
 document.querySelectorAll(".geo-twin").forEach(d=>d.remove());   // Geo-Zwillinge mit aufraeumen
 E.btnAuto.classList.remove("off");
 s.filling = false; clearIllum();
 s.lhcDots.b1.forEach(d=>d.el.remove()); s.lhcDots.b2.forEach(d=>d.el.remove());
 s.spsRunning=false; s.spsDots.b1.forEach(d=>d.el.remove()); s.spsDots.b2.forEach(d=>d.el.remove()); s.spsDots={b1:[],b2:[]};
 s.lhcDots={b1:[],b2:[]}; s.b1Count=0; s.b2Count=0; s.b1Batches=0; s.b2Batches=0;
 if(!keepData){ s.collisions=0; App.resetSpectrumData(); E.spInfo.innerText=`Kandidaten (${s.selDet}): 0`; }
 s.dtElapsed=0; s.intensityNow=0; E.lblIntensity.innerText=fmtIntensity(s.paramIntensity);   // Intensitäts-Anzeige zurück auf Sollwert
 s.ramped=false; s.squeezed=false; s.squeezing=false;
 s.lhcEnergy=s.isIon?177:450; s.lhcSpeed=s.isIon?0.0050:0.0078;
 s.paramBetaStar=1.5;
 E.b1c.innerText=fillLabel(0); E.b2c.innerText=fillLabel(0); E.b1bar.style.width="0%"; E.b2bar.style.width="0%";
 E.rbar.style.width="0%";
 E.btnRamp.classList.add("off"); E.btnSqueeze.classList.add("off"); E.btnColl.classList.add("off");
 E.btnAutoColl.classList.add("off");
 E.lblBeta.innerText = de(1.5,2) + " m";   // β*-Anzeige zurück auf unsqueezed (live)
 updateReadouts();
 Object.values(g.paths).forEach((p:any)=>{p.classList.remove("lit","lit-i","lit-b2")});
 Object.values(g.nodes).forEach((n:any)=>{n.classList.remove("glow","glow-i","flash")});
 g.paths.lhc.classList.remove("lit","lit-i");
 setStatus("BEREIT","on");
}

// abort(): bricht die Animation SOFORT ab (statt das Segment auf einem bereits
// aus dem DOM entfernten Punkt zu Ende zu rechnen — verschenkte rAF-Frames).
async function moveAlongPath(dot, pathEl, vpx, abort, geo?){
 return new Promise<void>(res=>{
  // Pfadlängen sind statisch → einmal messen und am Element cachen
  const len = pathEl.__len || (pathEl.__len = pathEl.getTotalLength());
  const dur=Math.max(1, len/vpx);   // Dauer = ECHTE Pfadlänge / Geschwindigkeit (kohärentes Tempo)
  let t0=null;
  function step(ts){
   if(abort && abort()){ res(); return; }
   if(!t0) t0=ts;
   let p=Math.min((ts-t0)/dur,1);
   let pt=pathEl.getPointAtLength(p*len);
   dot.setAttribute("cx",pt.x); dot.setAttribute("cy",pt.y);
   if(geo && geo.kind==='path') placeTwinPath(dot.__geo, geo.el, p);   // Geo-Zwilling am selben Fortschritt
   p<1 ? requestAnimationFrame(step) : res();
  }
  requestAnimationFrame(step);
 });
}

async function orbitRing(dot, ring, entryA, exitA, orbits, vpx, abort, geo?){
  let partial=((exitA-entryA)%(2*Math.PI)+2*Math.PI)%(2*Math.PI);
  let totalA=orbits*2*Math.PI+partial;
  const dur=Math.max(1, (ring.r*totalA)/vpx);   // Dauer = Bogenlänge / Geschwindigkeit
  const gEntry = geo && geo.entryA!=null ? geo.entryA : 0;
  // Eigener Geo-Schwenkwinkel: falls geo.exitA gesetzt, landet der Twin am echten
  // Geo-Ausstiegspunkt (unabhaengig vom Schema-Winkel), sonst gleicher Schwenk wie Schema.
  const gExit = geo && geo.exitA!=null ? geo.exitA : null;
  const gPartial = gExit!=null ? ((gExit-gEntry)%(2*Math.PI)+2*Math.PI)%(2*Math.PI) : partial;
  const gTotalA = orbits*2*Math.PI+gPartial;
  return new Promise<void>(res=>{
   let t0=null;
   function step(ts){
    if(abort && abort()){ res(); return; }
    if(!t0) t0=ts;
    let p=Math.min((ts-t0)/dur,1);
    let a=entryA+p*totalA;
    dot.setAttribute("cx",ring.cx+ring.r*Math.cos(a));
    dot.setAttribute("cy",ring.cy+ring.r*Math.sin(a));
    if(geo && geo.kind==='ring') placeTwinRing(dot.__geo, geo.ring, gEntry+p*gTotalA);
    p<1 ? requestAnimationFrame(step) : res();
   }
   requestAnimationFrame(step);
  });
}

// ── Einheitlicher Zeit-Faktor: an SIM_SCALE gekoppelt (Zeitraffer = Basis 1,0) ──
// Bahntempo, Ramp und Squeeze skalieren beim Moduswechsel im SELBEN Verhältnis
// (40/15) wie die Füll-Kadenz — vorher zwei leicht abweichende Faktoren (2,6 vs. 2,67).
function timeScale(){ return SIM_SCALE.fast / simScale(); }

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
 Object.values(g.paths).forEach((p:any)=>{ if(p) p.classList.remove("lit","lit-i","lit-b2"); });
 Object.values(g.nodes).forEach((n:any)=>{ if(n) n.classList.remove("glow","glow-i"); });
 g.trSteps.forEach(st=>st.classList.remove("cur","cur-i","done"));
}

// Lauf-Abbruch: globales resetFlag ODER der Batch gehört zu einer älteren
// Füll-Generation (Reset + sofortiger Neustart → fillGen weitergezählt).
function runAborted(gen){ return s.resetFlag || gen !== s.fillGen; }

// Ein Fluss-Schritt: Stufe betreten -> animieren -> verlassen; bricht bei Abbruch sauber & bilanziert ab.
async function flowStep(dot, pathEl, nodeEl, stageIdx, velKey, ringArgs, gen, beam?){
 if(runAborted(gen)) return false;
 const abort = ()=>runAborted(gen);
 const geo = geoRailFor(velKey, beam);
 if(geo && dot.__geo) twinR(dot.__geo, geo.r);
 if(stageIdx!=null) stageEnter(stageIdx);
 if(nodeEl) enterNode(nodeEl);
 enterPath(pathEl);
 if(ringArgs) await orbitRing(dot, ringArgs[0], ringArgs[1], ringArgs[2], ringArgs[3], App.getStageVel(velKey), abort, geo);
 else         await moveAlongPath(dot, pathEl, App.getStageVel(velKey), abort, geo);
 leavePath(pathEl);
 if(nodeEl) leaveNode(nodeEl);
 if(stageIdx!=null) stageLeave(stageIdx);
 return !runAborted(gen);
}

// ── Füllen mit Batch-Fan-in (real) ──────────────────────────────────────────
// 1 wandernder Punkt = 1 PS-Batch (psBatch Bunches). Mehrere Batches laufen
// einzeln durch den gemeinsamen Injektorkomplex (LINAC→PSB/LEIR→PS) zum SPS,
// AKKUMULIEREN dort und werden zu EINEM Zug ZUSAMMENGEFÜHRT, der über TI 2 (B1) /
// TI 8 (B2) in den LHC läuft. So wird die echte Hierarchie sichtbar. Didaktische
// Abstraktion: real bleiben die 4 Batches im Zug getrennte 72-Bunch-Gruppen (mit
// Lücken) und werden gemeinsam extrahiert — wir zeigen sie als EINEN Zug-Punkt.
function beamColor(beam){ const ion=s.isIon; return beam===1 ? (ion?"#e377c2":"#58a6ff") : (ion?"#c77dff":"#ff7f0e"); }
function newDot(beam, r){
 const dot=document.createElementNS(SVG_NS,"circle");
 dot.setAttribute("class","traveling-dot"); dot.setAttribute("r",r);
 const c=beamColor(beam); dot.setAttribute("fill",c); dot.setAttribute("stroke",c);
 (E.schematic||E.svg).appendChild(dot);
 dot.__geo = mkTwin(beam, 0.18);   // Geo-Zwilling (Injektor-Groesse; SPS/LHC setzen groesser)
 return dot;
}
function pulseNode(n){ if(!n) return; n.classList.add("flash"); setTimeout(()=>n.classList.remove("flash"),200); }
// Füllstands-Balken = was im LHC ANGEKOMMEN ist (Aufruf erst bei Zug-Ankunft in
// fuseTrain, n = Batches des Zugs). Vorher zählte jeder Batch schon bei SPS-Ankunft
// — der „LHC-Füllstand" stieg, während die Bunches noch im SPS kreisten.
function countBatch(beam, n){
 const tot=totalBatches();
 if(beam===1){ s.b1Batches+=n; E.b1c.innerText=fillLabel(s.b1Batches); E.b1bar.style.width=(Math.min(1,s.b1Batches/tot)*100)+"%"; }
 else        { s.b2Batches+=n; E.b2c.innerText=fillLabel(s.b2Batches); E.b2bar.style.width=(Math.min(1,s.b2Batches/tot)*100)+"%"; }
}

// Ein PS-Batch läuft bis zum SPS und PARKT dort (Cluster am Injektionspunkt).
async function injectBatch(beam, parked, gen){
 const ion=s.isIon, R=g.R, J=g.J, paths=g.paths, nodes=g.nodes;
 // Startet KLEIN: vor dem PS gibt es die 72er-Bunch-Struktur noch nicht
 // (LINAC-Puls bzw. wenige PSB/LEIR-Pakete) — sie entsteht erst durch das
 // Bunch-Splitting im PS, dort „wächst" der Punkt (s. u.).
 const dot=newDot(beam, "2.4");
 const fin=()=>{ endDot(dot); };
 const lp=ion?paths.linac3:paths.linac4, ln=ion?nodes.linac3:nodes.linac4;
 if(!await flowStep(dot, lp, ln, 0, 'linac', null, gen, beam)) return fin();
 const r1=ion?R.LEIR:R.PSB, r1p=ion?paths.leir:paths.psb, r1n=ion?nodes.leir:nodes.psb;
 const r1e=ion?J.LEIR_ENTRY:J.PSB_ENTRY, r1x=ion?J.LEIR_EXIT:J.PSB_EXIT;
 if(!await flowStep(dot, r1p, r1n, 1, 'ring1', [r1, r1e, r1x, 3], gen, beam)) return fin();
 if(!await flowStep(dot, ion?paths.leirPs:paths.psbPs, null, null, 'trToPs', null, gen, beam)) return fin();
 const psE=ion?J.PS_FROM_LEIR:J.PS_FROM_PSB;
 if(!await flowStep(dot, paths.ps, nodes.ps, 2, 'ps', [R.PS, psE, J.PS_EXIT, 3], gen, beam)) return fin();
 // Bunch-Splitting: erst HIER wird das Paket zum 72-Bunch-Batch (25-ns-Struktur).
 pulseNode(nodes.ps); dot.setAttribute("r","3.2");
 if(!await flowStep(dot, paths.psSps, null, null, 'trToSps', null, gen, beam)) return fin();
 if(runAborted(gen)) return fin();
 // Am SPS angekommen → tritt in den SPS-Umlauf ein (akkumuliert kreisend, NICHT
 // statisch geparkt → kein Stau am Eingang) + als Bunches zählen.
 const key=beam===1?"b1":"b2";
 const rec={ el:dot, off:s.spsDots[key].length*0.7 };
 twinR(dot.__geo, 2.4);   // im SPS angekommen → Geo-Zwilling auf Vollbild-Groesse
 s.spsDots[key].push(rec); parked.push(rec);
 stageEnter(3); enterNode(nodes.sps); pulseNode(nodes.sps);   // SPS leuchtet, solange Batches umlaufen
 startSpsLoop();
}

// Zusammenführungs-Animation: die akkumulierten Batches rücken — WÄHREND sie
// weiter im SPS umlaufen — winkelmäßig auf ihren gemeinsamen Schwerpunkt zusammen
// (off → Mittelwert). Liefert diesen Schwerpunkt-Offset zurück, sodass der Zug
// danach NAHTLOS an genau dieser Stelle übernimmt (kein Verschwinden/Teleport).
function mergeBatches(parked, gen){
 return new Promise<number>(res=>{
  if(parked.length<=1){ res(parked.length?parked[0].off:0); return; }
  const dur = 0.7 * (trainCadenceMs()/fc().batchesPerTrain);   // < Batch-Abstand → kein Überlapp mit dem nächsten Zug
  const starts = parked.map(r=>r.off);
  const target = starts.reduce((a,b)=>a+b,0)/starts.length;     // Schwerpunkt
  let t0=null;
  function step(ts){
   if(runAborted(gen)){ res(target); return; }
   if(!t0) t0=ts;
   const p=Math.min((ts-t0)/dur,1);
   const e=1-Math.pow(1-p,3);                                   // easeOut: schnell zusammen, sanft schließen
   parked.forEach((r,i)=>{ r.off = starts[i] + (target-starts[i])*e; });
   p<1 ? requestAnimationFrame(step) : res(target);
  }
  requestAnimationFrame(step);
 });
}

// Die akkumulierten Batches werden zu EINEM Zug zusammengeführt → orbitet SPS → TI → LHC.
async function fuseTrain(beam, parked, gen){
 const R=g.R, J=g.J, paths=g.paths, nodes=g.nodes, key=beam===1?"b1":"b2";
 const nB=parked.length;   // Batches dieses Zugs — gezählt wird erst bei LHC-Ankunft
 const phase = beam===1 ? 0 : Math.PI;
 pulseNode(nodes.sps);
 // 1) Sichtbares Zusammenrücken der Batches (statt abruptem Verschwinden).
 const target = await mergeBatches(parked, gen);
 // 2) Übergabe AM ORT des nun gestapelten Clusters (s.spsAngle + Phase + Schwerpunkt)
 //    → der Zug entsteht genau dort, wo die Batches stehen (nahtlos, kein Teleport).
 const startA = s.spsAngle + phase + target;
 parked.forEach(rec=>{ endDot(rec.el); stageLeave(3); leaveNode(nodes.sps); const i=s.spsDots[key].indexOf(rec); if(i>=0) s.spsDots[key].splice(i,1); });
 parked.length=0;
 if(runAborted(gen)) return;
 const train=newDot(beam, "4.2");
 twinR(train.__geo, 2.4);   // Zug = Vollbild-Groesse (SPS→TI→LHC)
 train.setAttribute("cx", R.SPS.cx + R.SPS.r*Math.cos(startA));
 train.setAttribute("cy", R.SPS.cy + R.SPS.r*Math.sin(startA));
 const spsExit=beam===1?J.SPS_TI2:J.SPS_TI8;
 // Orbit vom aktuellen Cluster-Winkel aus (1 voller Umlauf = SPS-Beschleunigung) bis zum TI-Ausgang.
 if(!await flowStep(train, paths.sps, nodes.sps, 3, 'sps', [R.SPS, startA, spsExit, 1], gen, beam)){ endDot(train); return; }
 if(!await flowStep(train, beam===1?paths.ti2:paths.ti8, null, null, 'ti', null, gen, beam)){ endDot(train); return; }
 endDot(train);
 addPermanentDot(beam);
 if(beam===1) s.b1Count++; else s.b2Count++;
 countBatch(beam, nB);
 paths.lhc.classList.add(s.isIon?"lit-i":"lit");
 renderTracker();
}

// Ein kompletter SPS-Zug = nBatches einzelne PS-Batches → Zusammenführung → LHC.
// gen = Füll-Generation des aufrufenden Laufs (handlers#fuellProtokoll).
async function injectTrain(beam, nBatches, gen){
 if(gen == null) gen = s.fillGen;
 if(runAborted(gen)) return;
 const parked=[], proms=[], sub=trainCadenceMs()/fc().batchesPerTrain;
 for(let i=0;i<nBatches;i++){
  if(runAborted(gen)) break;
  proms.push(injectBatch(beam, parked, gen));
  if(i<nBatches-1) await sleep(sub);
 }
 await Promise.all(proms);
 if(runAborted(gen)){ parked.forEach(rec=>endDot(rec.el)); return; }
 await fuseTrain(beam, parked, gen);
}

async function doRamp(){
 if(s.ramped||s.filling||s.cryoRecovery||s.isPilot) return;
 E.btnRamp.classList.add("off"); E.btnAuto.classList.add("off");
 setStatus(`HOCHFAHREN (1 s ≈ ${simScale()} s real): Magnetfeld und Energie steigen …`,"on");
 const startE=s.isIon?177:450;
 const maxE=s.isIon?2760:7000;   // Ionen: 7 TeV·(82/208) ≈ 2,76 TeV/u (gleiche Dipol-Steifigkeit)
 const targetE=Math.max(s.paramEnergy*1000, startE);   // nie unter Injektionsenergie -> Ramping BESCHLEUNIGT immer
 const startSpeed=s.isIon?0.0050:0.0078;
 const fullSpeed =s.isIon?0.0095:0.0150;                // Geschwindigkeit bei Maximalenergie
 const eFrac=Math.max(0, Math.min(1,(targetE-startE)/(maxE-startE)));
 const targetSpeed=startSpeed+eFrac*(fullSpeed-startSpeed);  // monoton: targetSpeed >= startSpeed
 // EHRLICHE Ramp-Dauer: Feldhub ΔB ÷ Ramp-Rate, dargestellt im Füll-Zeitmaßstab
 // (1 s ≈ simScale() s real). B ∝ E wie in updateReadouts (Pb: Faktor A/Z).
 // Vorher Konstante 200 → die Dauer war energieUNabhängig (Rampe auf 1 TeV dauerte
 // so lange wie auf 6,8 TeV); volle pp-Rampe blieb fast gleich (~10 s im Didaktik-Modus).
 const dB=(s.isIon?208/82:1)*(targetE-startE)/(0.299792458*2803.95);   // Tesla
 const dur=Math.max(800, (dB/s.paramRampSpeed)*1000/simScale());
 // PROBABILISTISCHES Quench-Risiko (statt deterministisch bei 40 %): oberhalb
 // 0,10 T/s steigt die Wahrscheinlichkeit steil (~30 % bei 0,11 → ~95 % bei
 // 0,15 T/s); der Zeitpunkt liegt zufällig in der Rampe — wie ein echtes Risiko.
 const risk = s.paramRampSpeed > 0.10 ? Math.min(0.95, (s.paramRampSpeed - 0.10) * 16 + 0.14) : 0;
 const quenchAt = (risk > 0 && Math.random() < risk) ? (0.25 + Math.random() * 0.65) : Infinity;
 let t0=null;
 let quenched = false;
 await new Promise<void>(res=>{
  function step(ts){
   if(!t0) t0=ts;
   let p=Math.min((ts-t0)/dur,1);
   if(p > quenchAt) { quenched = true; res(); return; }
   s.lhcEnergy=startE+p*(targetE-startE); s.lhcSpeed=startSpeed+p*(targetSpeed-startSpeed);
   E.rbar.style.width=(p*100)+"%"; updateReadouts();
   p<1 ? requestAnimationFrame(step) : res();
  }
  requestAnimationFrame(step);
 });
 if(quenched) { triggerQuench(); return; }
 s.ramped=true; E.btnSqueeze.classList.remove("off");
 setStatus("HOCHFAHREN ABGESCHLOSSEN. Weiter mit dem Beam Squeeze.","on");
}

function triggerQuench(){
 s.cryoRecovery = true; stopAutoCollide();
 setStatus("QUENCH! Ein Magnet hat seine Supraleitung verloren, der Strahl wurde notabgeworfen.", "danger");
 E.sdot.className = "cv4-dot flash";
 E.svg.style.transition = "filter 0.5s";
 E.svg.style.filter = "sepia(1) saturate(3) hue-rotate(320deg)";
 let secLeft = 5;
 function cryoTick(){
  if(secLeft > 0){ setStatus(`QUENCH: Helium-Kühlung fährt die Magnete wieder herunter … (${secLeft} s)`, "danger"); secLeft--; setTimeout(cryoTick, 1000); }
  else { E.svg.style.filter = "none"; s.cryoRecovery = false; resetLHC(); setStatus("KÜHLUNG ABGESCHLOSSEN. LHC wieder bereit", "on"); }
 }
 cryoTick();
}

async function doSqueeze(){
 if(!s.ramped||s.squeezed||s.squeezing||s.cryoRecovery) return;
 s.squeezing = true; E.btnSqueeze.classList.add("off");
 setStatus("BEAM SQUEEZE: Die Strahlen werden an den Kollisionspunkten gebündelt. (stark gerafft; real dauert das einige Minuten)","on");
 // Bewusste Raffung über den Füll-Maßstab hinaus (real ~10–15 min wären 40–60 s
 // Darstellung — didaktisch tot). Skaliert aber mit dem Tempo-Modus mit.
 // Ziel-β* kommt jetzt aus dem Preset (s.targetBetaStar), nicht mehr aus einem Slider.
 let t0 = null; const dur = 2000 * timeScale(); const targetBeta = s.targetBetaStar;
 await new Promise<void>(res=>{
  function step(ts){
   if(!t0) t0=ts;
   let p=Math.min((ts-t0)/dur,1);
   s.paramBetaStar = 1.5 - p * (1.5 - targetBeta);
   E.lblBeta.innerText = de(s.paramBetaStar,2) + " m";
   p<1 ? requestAnimationFrame(step) : res();
  }
  requestAnimationFrame(step);
 });
 s.squeezing = false; s.squeezed = true; E.btnColl.classList.remove("off"); E.btnAutoColl.classList.remove("off");
 [g.nodes.atlas,g.nodes.cms,g.nodes.alice,g.nodes.lhcb].forEach(n=>n.classList.add("glow"));
 g.paths.lhc.classList.add(s.isIon?"lit-i":"lit");
 setStatus("STABLE BEAMS: Strahlen gebündelt, bereit für Kollisionen.","on");
}

function addPermanentDot(beam){
 const key=beam===1?"b1":"b2";
 const existing=s.lhcDots[key].length;
 const angleOffset=existing*(2*Math.PI/trainsTotal());
 const dot=document.createElementNS(SVG_NS,"circle");
 dot.setAttribute("class","lhc-bunch"); dot.setAttribute("r","3.5");
 let c=beam===1?(s.isIon?"#e377c2":"#58a6ff"):(s.isIon?"#c77dff":"#ff7f0e");
 // KEIN drop-shadow-Filter (Perf): die 12 Bunches kreisen jeden Frame.
 dot.setAttribute("fill",c); dot.setAttribute("stroke",c);
 (E.schematic||E.svg).appendChild(dot);
 dot.__geo = mkTwin(beam, 2.6);   // umlaufender LHC-Bunch im Geo-Vollbild
 s.lhcDots[key].push({el:dot,off:angleOffset});
 if(!s.lhcRunning) startLHCLoop();
}

// SPS-Akkumulations-Umlauf: ankommende Batches KREISEN im SPS (verteilt, beide
// Strahlen gleichläufig — ein Synchrotron hat EINE Umlaufrichtung) statt statisch
// am Eingang zu stauen → sieht aus wie ein sich füllender Strahl. Wird bei der
// Zusammenführung (fuseTrain) wieder geleert.
function startSpsLoop(){
 if(s.spsRunning) return;
 s.spsRunning=true; s.spsLastT=null;
 const R=g.R;
 function frame(ts){
  if(!s.spsLastT) s.spsLastT=ts;
  let dt=ts-s.spsLastT; s.spsLastT=ts;
  // Winkelgeschwindigkeit aus DERSELBEN Geschwindigkeits-Leiter: ω = v_tangential / r
  // → ankommende Batches kreisen mit SPS-Bahntempo (kein Tempo-Sprung beim Eintritt).
  s.spsAngle += (App.getStageVel('sps')/R.SPS.r)*dt;
  // Beide Strahlen GLEICHLÄUFIG (ein Synchrotron = eine Umlaufrichtung). Die
  // Gegenläufigkeit beginnt erst im LHC (TI 2 vs. TI 8). B2 nur um π phasen-
  // versetzt, damit die Punkte sichtbar getrennt sind — NICHT gegenläufig.
  const gsps = App.geoRings && App.geoRings.sps;
  const place=(arr,phase)=>arr.forEach(d=>{ const a=s.spsAngle+phase+d.off; d.el.setAttribute("cx",R.SPS.cx+R.SPS.r*Math.cos(a)); d.el.setAttribute("cy",R.SPS.cy+R.SPS.r*Math.sin(a)); if(d.el.__geo) placeTwinRing(d.el.__geo, gsps, a); });
  place(s.spsDots.b1, 0); place(s.spsDots.b2, Math.PI);
  if(s.spsRunning && (s.spsDots.b1.length || s.spsDots.b2.length)) requestAnimationFrame(frame);
  else s.spsRunning=false;
 }
 requestAnimationFrame(frame);
}

function startLHCLoop(){
 s.lhcRunning=true; s.lhcLastT=null;
 const R=g.R;
 function frame(ts){
  if(!s.lhcLastT) s.lhcLastT=ts;
  let dt=ts-s.lhcLastT; s.lhcLastT=ts;
  s.lhcAngle += (s.lhcSpeed/timeScale())*dt;
  const glhc = App.geoRails && App.geoRails.lhc;
  const frac = (a)=>((a/(2*Math.PI))%1+1)%1;   // Winkel → Bahnanteil auf dem Geo-LHC-Rail
  s.lhcDots.b1.forEach(d=>{
   let a=s.lhcAngle+d.off;
   let r=180 + 5.5 * Math.sin(a * 2);
   d.el.setAttribute("cx",R.LHC.cx+r*Math.cos(a)); d.el.setAttribute("cy",R.LHC.cy+r*Math.sin(a));
   if(d.el.__geo) placeTwinPath(d.el.__geo, glhc, frac(a));         // B1 vorwaerts
  });
  s.lhcDots.b2.forEach(d=>{
   let a=-s.lhcAngle+d.off;
   let r=180 - 5.5 * Math.sin(a * 2);
   d.el.setAttribute("cx",R.LHC.cx+r*Math.cos(a)); d.el.setAttribute("cy",R.LHC.cy+r*Math.sin(a));
   if(d.el.__geo) placeTwinPath(d.el.__geo, glhc, frac(a));         // B2 gegenlaeufig (a faellt)
  });
  if(s.lhcRunning) requestAnimationFrame(frame);
 }
 requestAnimationFrame(frame);
}

function doCollide(){
 if(!s.ramped||!s.squeezed||s.cryoRecovery||s.dumping) return;
 let detNode=g.nodes[s.selDet.toLowerCase()];
 if(detNode){detNode.classList.add("flash");setTimeout(()=>detNode.classList.remove("flash"),350);}
 App.drawCollisionEvent(App.generateMassData()); App.drawHist();
 // Anzeige aus collStore (generateMassData zählt dort) — vorher zeigte s.collisions
 // nach einem Detektor-Wechsel den Stand des VORHERIGEN Detektors + 1.
 s.collisions = s.collStore[s.selDet];
 E.spInfo.innerText=`Kandidaten (${s.selDet}): ${Math.round(s.collisions).toLocaleString("de-DE")}`;
}

function toggleAutoCollide(){
 if(s.autoCollInterval) stopAutoCollide(); else startAutoCollide();
}

// Datennahme-Zeitmaßstab (reale Sekunden je Darstellungssekunde) + Label, modusabhängig.
const dtScale = () => s.isFastMode ? DT_SCALE.fast : DT_SCALE.slow;
const dtLabel = () => s.isFastMode ? "33 min" : "15 min";

function startAutoCollide(){
 if(!s.ramped || !s.squeezed || s.cryoRecovery || s.dumping) return;
 E.btnAutoColl.innerText = "Datennahme stoppen"; E.btnAutoColl.classList.add("act");
 E.btnColl.classList.add("off");
 // Burn-off-Uhr läuft PRO FILL: nur beim ersten Start nach dem Füllen auf null
 // (Pause/Weiter verjüngt den Strahl NICHT — sonst „Unendlich-Fill"-Exploit).
 if(s.dtElapsed === 0) s.intensity0 = s.paramIntensity;   // Stable Beams: N₀ = Intensität bei Fill-Start
 setStatus(`DATENNAHME (1 s ≈ ${dtLabel()} real): Der Strahl verbraucht sich langsam …`, "on");
 const tau = BEAM_LIFETIME_H * 3600;                    // Intensitäts-Lebensdauer in s
 let lastTick = performance.now();
 s.autoCollInterval = setInterval(()=>{
  if(s.cryoRecovery) { stopAutoCollide(); return; }
  // ECHTE verstrichene Darstellungszeit statt fester 125-ms-Annahme: setInterval
  // driftet und wird in Hintergrund-Tabs auf ≥1 s gedrosselt — der Maßstab
  // „1 s ≈ X real" stimmt nur mit gemessener Zeit. Geklemmt auf 0,5 s/Tick,
  // damit eine Rückkehr aus dem Hintergrund keinen Zeitsprung auslöst.
  const now = performance.now();
  const dDisp = Math.min(0.5, (now - lastTick) / 1000); lastTick = now;
  const dReal = dDisp * dtScale();                      // reale Sekunden dieses Ticks
  s.dtElapsed += dReal;
  const frac = Math.exp(-s.dtElapsed / tau);            // N/N₀
  const L = frac * frac;                                // relative Luminosität (Burn-off)
  s.intensityNow = s.intensity0 * frac;
  E.lblIntensity.innerText = fmtIntensity(s.intensityNow);
  // Bunches verblassen (Intensitätsverlust pro Bunch, NICHT Anzahl): opacity ∝ N.
  const op = (0.2 + 0.8 * frac).toFixed(3);
  s.lhcDots.b1.forEach(d=>d.el.setAttribute("opacity", op));
  s.lhcDots.b2.forEach(d=>d.el.setAttribute("opacity", op));
  // SLIDER-PHYSIK in der Datenrate: L ∝ N²/β* (wie die Info-Texte lehren und der
  // manuelle Modus es tut). Normiert auf den Preset-Arbeitspunkt des aktuellen
  // Strahls (pp: 1,40e11/0,30 m · Pb-Pb: 0,90e11/0,50 m) → dort Faktor 1, die
  // Fill-Kalibrierung („ein guter Fill ≈ 5σ im schwersten Kanal") bleibt erhalten.
  // Ohne Squeeze (β* = 1,5 m) sammelt man sichtbar langsamer — echte Physik.
  const ref = s.isIon ? { I: 0.90, b: 0.50 } : { I: 1.40, b: 0.30 };
  const lumiF = Math.pow((s.intensity0 || ref.I) / ref.I, 2) * (ref.b / Math.max(0.05, s.paramBetaStar));
  // GLEICHZEITIGE Datennahme: real nehmen ALLE Experimente denselben Fill auf.
  // Jeder Detektor akkumuliert Kandidaten mit SEINER eigenen Rate (Higgs selten,
  // Z⁰/Quarkonia häufig) → collStore KONTINUIERLICH (float) je Detektor, Signifikanz
  // 5·√(collStore/target) wächst GLATT der √-Kurve entlang (steil→flach), vom Burn-off
  // gedämpft. Tab-Wechsel zeigt den parallel gewachsenen Stand jedes Detektors.
  let dCandSel = 0;
  App.liveDetectors().forEach(d=>{
   const dCand = STAT_RATE * L * lumiF * dReal * App.detRate(d);
   if(d === s.selDet) dCandSel = dCand;
   s.collStore[d] += dCand;
   s.histAcc[d]   += dCand;
   const whole = Math.floor(s.histAcc[d]);
   if(whole > 0){ s.histAcc[d] -= whole; App.accumulateStatsFor(d, whole); }
  });
  s.collisions = s.collStore[s.selDet];   // Anzeige folgt dem gewählten Detektor
  // Sichtbares Einzel-Event des GEWÄHLTEN Detektors in watchbarer Rate ∝ seiner
  // ECHTEN Kandidaten-Rate (L × Lumi-Faktor × Kanal-Rate), gedeckelt auf ~7 Hz.
  // Vorher nur ∝ L (Burn-off): der Pilot-Strahl (lumiF ≈ 0,001) blinkte so oft
  // wie der Vollbetrieb. Jetzt: Vollbetrieb ~jeden Tick, Pilot ~alle 3–4 s.
  if(Math.random() < Math.min(0.85, 8 * dCandSel)){
   let detNode=g.nodes[s.selDet.toLowerCase()];
   if(detNode){ detNode.classList.add("flash"); setTimeout(()=>detNode.classList.remove("flash"), 75); }
   s.lastEvent = App.sampleEvent(); App.drawCollisionEvent(s.lastEvent);   // s.lastEvent → Golden-Event-Freeze
  }
  App.drawHist();
  E.spInfo.innerText = `Kandidaten (${s.selDet}): ${Math.round(s.collStore[s.selDet]).toLocaleString("de-DE")} · L ${Math.round(L*100)} %`;
  setStatus(`DATENNAHME (1 s ≈ ${dtLabel()} real): N ${fmtIntensity(s.intensityNow)} (${Math.round(frac*100)} %) · L ${Math.round(L*100)} %`, "on");
  if(frac <= DUMP_FRAC) beamDump();
 }, 125);
}

// Strahl-Dump: Luminosität zu gering → Fill beenden (Strahl weg), Refill nötig.
function beamDump(){
 s.dumping = true;   // Gate: bis zum Reset KEINE manuellen Kollisionen / kein Neustart
 stopAutoCollide();  // (der Strahl ist weg — ramped/squeezed sind nur noch Restzustand)
 setStatus(`STRAHL-DUMP: N < ${Math.round(DUMP_FRAC*100)} % (L < ${Math.round(DUMP_FRAC*DUMP_FRAC*100)} %): Strahl verbraucht, neue Füllung nötig.`, "danger");
 // keepData=true: Spektrum/Signifikanz BLEIBEN (mehrere Füllungen summieren sich zur Entdeckung).
 setTimeout(()=>{ if(!s.cryoRecovery){ resetLHC(true); setStatus("STRAHL ABGEWORFEN. Daten bleiben erhalten; starte das Füllprotokoll für die nächste Füllung.", "on"); } }, 1600);
}

function stopAutoCollide(){
 const had = !!s.autoCollInterval;
 if(had) { clearInterval(s.autoCollInterval); s.autoCollInterval = null; }
 E.btnAutoColl.innerText = "Auto-Datennahme"; E.btnAutoColl.classList.remove("act");
 if(had && !s.dumping) setStatus("DATENNAHME PAUSIERT. Die Verbrauchs-Uhr läuft beim Fortsetzen weiter.", "on");
 // Manuelle Kollisionen nur freigeben, wenn der Strahl noch existiert (kein Dump).
 if(s.ramped && s.squeezed && !s.cryoRecovery && !s.dumping) E.btnColl.classList.remove("off");
}

function updateReadouts(){
 E.vE.innerText=fmtEnergy(s.lhcEnergy/1000);
 // Dipolfeld: für Pb-Ionen Ladungs-zu-Massenzahl-Verhältnis (Z/A=82/208) berücksichtigen
 let rig=0.299792458*2803.95;
 let B=(s.isIon?(208/82):1)*s.lhcEnergy/rig; E.vB.innerText=de(B,3)+" T";
 // Lorentz-γ PRO NUKLEON: E_Nukleon / m_Nukleon (Ion: 0.9315 GeV, Proton: 0.938272 GeV)
 let gam=s.lhcEnergy/(s.isIon?0.9315:0.938272); E.vG.innerText=Math.round(gam).toLocaleString("de-DE");
}

function setStatus(txt,cls){ E.stxt.innerText=txt; E.sdot.className="cv4-dot "+cls; }

// ── Registrierung der öffentlichen API ──────────────────────────────────────
App.resizeCanvases = resizeCanvases;
App.setMode = setMode;
App.resetLHC = resetLHC;
App.timeScale = timeScale;
App.injectTrain = injectTrain;
App.trainCadenceMs = trainCadenceMs;
App.toggleAutoCollide = toggleAutoCollide;
App.stopAutoCollide = stopAutoCollide;
App.updateReadouts = updateReadouts;
App.setStatus = setStatus;

// ── Listener (nach initDom in main.js aufgerufen) ───────────────────────────
export function wireEngine(){
 // Teilchenart-Wahl: versteckter Toggle auf dem „Teilchen"-Messwert (ersetzt die
 // früheren Auswahl-Tabs). Klick wechselt Protonen ⟷ Blei-Ionen (nicht beim Füllen).
 const roT = $("ro-teilchen");
 if(roT) roT.addEventListener("click",()=>{ if(s.filling) return; setMode(!s.isIon); });
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
