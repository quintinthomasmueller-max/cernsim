// ═══════════════════════════════════════════════════════════════════════════
// HISTOGRAM / MASSENSPEKTRUM  — STRAHLKONFIGURATIONS-GETRIEBEN
// ═══════════════════════════════════════════════════════════════════════════
// Das Spektrum ist eine Funktion von ZWEI Achsen, nicht nur des Detektors:
//   1) WAS GEMESSEN wird — der gewählte Detektor (s.selDet) liefert seinen
//      charakteristischen Kanal (ATLAS=Z⁰, CMS=Higgs-4ℓ, ALICE=Quarkonia, LHCb=B).
//   2) WAS DA IST — die Strahl-Konfiguration entscheidet, welche Resonanzen
//      überhaupt erzeugt werden und wie hoch ihr Peak steht:
//        • Energie (s.paramEnergy, TeV/Strahl): jede Resonanz hat eine
//          Erzeugungs-Schwelle `thr`. Darunter → NUR Untergrund-Kontinuum, kein
//          Peak; beim Hochrampen wächst der Peak ein (prodVis 0→1). Energie formt
//          also die FORM des Spektrums, nicht nur die Signifikanz.
//        • Strahlart (s.isIon): im Pb-Pb-Modus schmelzen Quarkonia im QGP →
//          J/ψ-/Υ-Peak in ALICE wird unterdrückt (drawVis = prodVis · Suppr.).
//        • Intensität²/β*: Kollisionsrate = Statistik (∝ Signifikanz-Zuwachs).
// Presets sind nur Shortcuts, die diese Parameter + den Detektor setzen — die
// Logik oben ergibt sich daraus von selbst. Daten + Fit teilen EIN Modell
// (Untergrund + Σ Resonanz·drawVis) → die Fit-Kurve liegt immer auf den Balken.
//
// Daten: echte CMS-Open-Data (CERN_REAL); LHCb-B-Physik = kalibrierte Simulation
// (CMS-Dimuon-Set enthält keine B-Mesonen).
import { App, $ } from './core.js';
import { CERN_REAL } from './data.gen.js';

const s = App.state, E = App.els;

let _lhcbPool=null;
function lhcbPool(){
 if(_lhcbPool) return _lhcbPool;
 _lhcbPool=[]; for(let i=0;i<1400;i++){
  _lhcbPool.push(Math.random()<0.45
    ? 5.279+(Math.random()+Math.random()+Math.random()-1.5)*0.06   // B⁰ bei 5.279 GeV
    : 4.6+Math.random()*1.4);                                        // komb. Untergrund
 }
 return _lhcbPool;
}

const G=(v,m,sg)=>Math.exp(-0.5*((v-m)/sg)**2);

// ── ZENTRALE DETEKTOR-SPEKTRUM-TABELLE ──────────────────────────────────────
// Pro Detektor: `beam` = STRAHL-PROGRAMM, unter dem dieser Detektor seine
// Entdeckung macht ("pp" = Protonen, "PbPb" = Blei-Ionen) + Untergrund `bg(v)` +
// Liste `reson` der messbaren Resonanzen. Jede Resonanz trägt m (Masse),
// hw (Klassifikations-Halbfenster), sg (Fit-/Sampling-Sigma), thr (Energie-
// Schwelle TeV/Strahl), amp (relative Peak-Höhe), label, optional `pp:true`
// (Erzeugung nur mit Protonen → in Ionen-Läufen kein Peak) und `qgp:true`
// (im Ionen-Modus durch QGP unterdrückt). `primary` = Resonanz, deren
// Erzeugbarkeit über die Signifikanz entscheidet.
//   ⇒ Das Spektrum hängt logisch von BEIDEM ab: dem Strahl-Programm/Preset
//     (beam + Energie) UND dem betrachteten Detektor. Higgs ist also nur im
//     pp-Programm bei voller Energie entdeckbar — im QGP-Lauf (Pb-Pb) zeigt CMS
//     nur das ZZ*-Kontinuum, keine Higgs-Entdeckung.
const DETSPEC = {
 ATLAS: {                                  // Z⁰ = QGP-blinde „Standardkerze" → in pp UND Pb-Pb messbar
  pool:()=>CERN_REAL.pp,  range:[50,150], bins:60, channel:"2mu", discoBeam:"any",
  target:200, col:"#58a6ff", fc:"rgba(88,166,255,0.38)",
  bg:(v)=> Math.exp(-(v-50)/30)*0.12,
  // Z⁰ ist elektroschwach (koppelt nicht ans QGP) → KEIN pp-Flag: entsteht in pp und Pb-Pb.
  reson:[{key:"Z0", m:91.19, hw:6.0, sg:3.0, thr:0.9, amp:1.00, label:"Z⁰"}],
  primary:"Z0",
  title:"ATLAS · Z⁰→μ⁺μ⁻ · Präzisions-Kalibrierkanal (echte CMS-Daten)",
  sub:"Standardmodell-EW · Z⁰-Resonanz bei 91 GeV (QGP-blinde Standardkerze)",
  disco:"🌟 5σ: Z⁰-Resonanz präzise vermessen!"
 },
 CMS: {                                    // pp-Programm: Higgs-Goldkanal H→ZZ*→4ℓ
  pool:()=>CERN_REAL.higgs4l, range:[80,200], bins:60, channel:"4l", discoBeam:"pp",
  target:600, col:"#2ea44f", fc:"rgba(46,164,79,0.38)",
  bg:(v)=> Math.exp(-(v-80)/46),
  // Higgs braucht Protonen UND nahezu volle LHC-Energie (thr 5.5 TeV) — der
  // Goldkanal-Bump taucht erst beim Hochrampen auf, darunter nur ZZ*-Kontinuum.
  reson:[{key:"H", m:124, hw:5.0, sg:2.8, thr:5.5, amp:0.66, label:"H 125", pp:true}],
  primary:"H",
  title:"CMS · H→ZZ*→4ℓ · Goldkanal (Higgs bei 125 GeV)",
  sub:"Kleines Signal auf großem ZZ*-Untergrund · braucht Protonen + volle Energie",
  disco:"🌟 5σ: Higgs-Boson entdeckt!"
 },
 ALICE: {                                  // Schwerionen-Programm: Quarkonia (QGP)
  pool:()=>CERN_REAL.ion, range:[1,12], bins:55, channel:"2mu", discoBeam:"PbPb",
  target:300, col:"#e377c2", fc:"rgba(227,119,194,0.38)",
  bg:(v)=> 0.27,
  // Quarkonia entstehen in pp UND Pb-Pb (kein pp-Flag): in pp = volle Referenz,
  // in Pb-Pb durch QGP unterdrückt (qgp). Die QGP-Entdeckung selbst braucht Pb-Pb.
  reson:[{key:"Jpsi", m:3.097, hw:0.5, sg:0.18, thr:0.4, amp:0.73, label:"J/ψ", qgp:true},
         {key:"Ups",  m:9.60,  hw:0.9, sg:0.70, thr:0.6, amp:0.16, label:"Υ",   qgp:true}],
  primary:"Jpsi",
  title:"ALICE · J/ψ + Υ → μ⁺μ⁻ · Quarkonia (echte CMS-Daten)",
  sub:"Quark-Gluon-Plasma: Unterdrückung der Quarkonia-Zustände",
  disco:"🌟 5σ: Quarkonia-Unterdrückung (QGP) nachgewiesen!"
 },
 LHCB: {                                   // pp-Programm: B-Physik / CP-Verletzung
  pool:()=>lhcbPool(), range:[4.6,6.0], bins:50, channel:"B", discoBeam:"pp",
  target:400, col:"#ff7f0e", fc:"rgba(255,127,14,0.38)",
  bg:(v)=> 0.25,
  reson:[{key:"B0", m:5.279, hw:0.18, sg:0.07, thr:0.45, amp:0.75, label:"B⁰", pp:true}],
  primary:"B0",
  title:"LHCb · B⁰ → h⁺h⁻ · CP-Verletzung (kalibrierte Simulation)",
  sub:"Materie-Antimaterie-Asymmetrie im B-Mesonen-Zerfall",
  disco:"🌟 5σ: CP-Verletzung etabliert!"
 }
};
function spec(){ return DETSPEC[s.selDet] || DETSPEC.ATLAS; }
const beamLabel = (b)=> b==="PbPb" ? "Blei-Ionen" : "Protonen";
const curBeam = ()=> s.isIon ? "PbPb" : "pp";
// Entdeckung möglich? discoBeam "any" (Z⁰-Standardkerze) immer; sonst muss das
// Programm-Strahl == aktueller Strahl sein (Higgs/CP nur pp, QGP nur Pb-Pb).
function discoBeamOK(sp){ return sp.discoBeam === "any" || sp.discoBeam === curBeam(); }
// Text, warum die Entdeckung am Strahltyp scheitert (für ALICE in pp = Referenz, kein Fehler).
function wrongBeamShort(sp){ return sp.discoBeam==="PbPb" ? "p-p-Referenz · QGP nur in Pb-Pb"
                                                         : "Falsches Strahl-Programm · braucht "+beamLabel(sp.discoBeam); }
function primaryReson(sp){ return sp.reson.find(r=>r.key===sp.primary) || sp.reson[0]; }

// ── Strahl-Konfiguration → Sichtbarkeit einer Resonanz ──────────────────────
// energyVis: 0 unter der Erzeugungs-Schwelle, weicher Anstieg auf 1 darüber.
// prodVis:  Erzeugbarkeit = Energie × Strahlart (pp-Resonanzen: 0 im Ionen-Lauf).
// drawVis:  tatsächlich sichtbare Peak-Höhe = prodVis · QGP-Suppression (Ionen).
function energyVis(thr){
 const span = 0.15*thr + 0.30;                  // Übergangsbreite ~½·Schwelle
 return Math.max(0, Math.min(1, (s.paramEnergy - thr)/span));
}
function prodVis(r){ return energyVis(r.thr) * (r.pp && s.isIon ? 0 : 1); }  // EW/B nur mit Protonen
function drawVis(r){ return prodVis(r) * (r.qgp && s.isIon ? 0.45 : 1); }    // QGP schmilzt Quarkonia
function classifyReson(sp, m){ for(const r of sp.reson){ if(Math.abs(m-r.m) <= r.hw) return r; } return null; }
function fitVal(sp, v){ let y=sp.bg(v); for(const r of sp.reson) y += drawVis(r)*r.amp*G(v,r.m,r.sg); return y; }
function resoName(key){ return key==="Jpsi" ? "J/psi" : key==="Ups" ? "Upsilon(1S)" : key; }

function classify(m){
 // ordnet eine reale Masse der nächstgelegenen Resonanz zu (sonst Untergrund)
 let best=null, bd=1e9;
 for(const k in CERN_REAL.reso){
  if(k==="Higgs") continue;                  // anderer Kanal (4ℓ)
  let mm=CERN_REAL.reso[k][0], br=CERN_REAL.reso[k][1];
  let tol=Math.max(0.15, br*1.5+0.035*mm);
  let d=Math.abs(m-mm);
  if(d<tol && d<bd){ bd=d; best=k; }
 }
 return best;
}

function pickTopo(name){
 // echte CMS-Myon-Paar-Kinematik [pt1,eta1,phi1,q1, pt2,eta2,phi2,q2]
 let key = name==="Z0"?"Z0" : name==="J/psi"?"Jpsi" : (name&&name.indexOf("Upsilon")===0)?"Ups" : null;
 let arr = key ? CERN_REAL.topo[key] : null;
 if(arr && arr.length){ let t=arr[(Math.random()*arr.length)|0];
  return [{pt:t[0],eta:t[1],phi:t[2],q:t[3],lep:"μ"},{pt:t[4],eta:t[5],phi:t[6],q:t[7],lep:"μ"}]; }
 let pt=5+Math.random()*20, a=Math.random()*6.283;
 return [{pt:pt,eta:(Math.random()-.5)*3,phi:a,q:1,lep:"μ"},
         {pt:pt*(0.6+Math.random()*0.6),eta:(Math.random()-.5)*3,phi:a+Math.PI,q:-1,lep:"μ"}];
}

// Zieht eine Masse aus dem echten Datenpool, gewichtet mit der Strahl-Konfig:
// Untergrund-Events sind immer zulässig; ein SIGNAL-Event (in einem Resonanz-
// Fenster) wird nur akzeptiert, soweit die Resonanz erzeugbar/sichtbar ist
// (drawVis). Sonst neu ziehen → unter der Schwelle bleibt nur das Kontinuum.
function sampleMass(sp){
 const pool=sp.pool();
 for(let tries=0; tries<8; tries++){
  let m=pool[(Math.random()*pool.length)|0];
  let r=classifyReson(sp, m);
  if(!r) return m;                           // Untergrund: immer zulässig
  if(Math.random() < drawVis(r)) return m;   // Signal: nur soweit erzeugt/sichtbar
 }
 // Energie zu gering (oder Quarkonia voll unterdrückt) → Untergrund-Kontinuum
 return sp.range[0] + Math.random()*(sp.range[1]-sp.range[0]);
}

function sampleEvent(){
 const sp=spec();
 let m=sampleMass(sp);
 if(sp.channel==="4l"){
  // Higgs-Goldkanal: 4-Lepton-Topologie (2 Z→ℓℓ-Paare)
  let leptons=[]; for(let i=0;i<4;i++) leptons.push({pt:8+Math.random()*40,
    eta:(Math.random()-.5)*4, phi:Math.random()*6.283, q:i%2?1:-1, lep:Math.random()<.5?"e":"μ"});
  const H=primaryReson(sp);
  let isSig=Math.abs(m-H.m)<H.hw; if(isSig) s.higgsCands++;   // m liegt nur bei H, wenn Higgs erzeugbar
  return {M:m, name:isSig?"Higgs":null, channel:"4l", leptons:leptons, signal:isSig};
 }
 // Dimuon (ATLAS/ALICE) bzw. B-Vertex (LHCb) → 2-Spur-Topologie
 let r=classifyReson(sp, m);
 let name=r?resoName(r.key):null;
 return {M:m, name:name, channel:sp.channel, leptons:pickTopo(name), signal:!!name};
}

function resetSpectrumData(){
 s.massStore={ATLAS:[], CMS:[], ALICE:[], LHCB:[]};
 s.collStore={ATLAS:0, CMS:0, ALICE:0, LHCB:0};
 s.higgsCands=0;
}

// Bulk-Statistik (Datennahme): 'units' Kollisionen auf einmal in den AKTUELLEN
// Detektor akkumulieren (collStore zählt voll für die Signifikanz; das Histogramm
// wird mit Massen befüllt, aber gedeckelt, damit es nicht ins Unendliche wächst).
const HIST_CAP = 6000;
function accumulateStats(units){
 units = Math.floor(units); if(units<=0) return;
 const sp=spec(), store=s.massStore[s.selDet];
 const rateFactor=Math.pow(s.paramIntensity,2)/Math.max(0.3,s.paramBetaStar);
 const per=Math.max(1, Math.round(rateFactor*(sp.channel==="4l"?1.5:5)));
 for(let k=0;k<units && store.length<HIST_CAP;k++){ for(let i=0;i<per && store.length<HIST_CAP;i++) store.push(sampleMass(sp)); }
 s.collStore[s.selDet]+=units;
}

function generateMassData(){
 const sp=spec();
 // Datenrate ∝ Intensität² / β* (4ℓ-Goldkanal seltener → kleinerer Faktor)
 let rateFactor = Math.pow(s.paramIntensity, 2) / Math.max(0.3, s.paramBetaStar);
 let n = Math.max(1, Math.round(rateFactor * (sp.channel==="4l"?1.5:5)));
 const store = s.massStore[s.selDet];
 for(let i=0;i<n;i++) store.push(sampleMass(sp));   // energie-/strahlgewichtet (Peak nur, wenn erzeugbar)
 s.collStore[s.selDet] += 1;
 s.lastEvent = sampleEvent();
 store.push(s.lastEvent.M);   // das angezeigte Event landet immer im Spektrum des Detektors
 return s.lastEvent;
}

function getSignificance() {
  const sp=spec(), n=s.collStore[s.selDet];
  if (n === 0) return 0;
  // Entdeckung braucht das RICHTIGE Strahl-Programm: CMS-Higgs/LHCb-CP nur in pp,
  // ALICE-QGP nur in Pb-Pb. ATLAS-Z⁰ ist die QGP-blinde Standardkerze (discoBeam
  // "any") → in beidem messbar. Zusätzlich muss die Primär-Resonanz bei dieser
  // Energie erzeugbar sein (kontinuierlich ∝ prodVis statt binärer Schwelle).
  if (!discoBeamOK(sp)) return 0;
  const pv = prodVis(primaryReson(sp));
  if (pv <= 0) return 0;
  return 5.0 * Math.sqrt(n / sp.target) * pv;
}

function drawHist(){
  const sp=spec();
  const ctxHist=E.ctxHist;
  let w=s.histW,h=s.histH;
  ctxHist.clearRect(0,0,w,h);
  ctxHist.strokeStyle="#30363d";ctxHist.lineWidth=1;
  ctxHist.beginPath();ctxHist.moveTo(30,8);ctxHist.lineTo(30,h-16);ctxHist.lineTo(w-8,h-16);ctxHist.stroke();
  ctxHist.fillStyle="#8b949e";ctxHist.font="7.5px sans-serif";
  let [mn,mx]=sp.range;
  ctxHist.fillText(mn+" GeV",30,h-5);ctxHist.fillText(mx+" GeV",w-40,h-5);

  let sig = getSignificance();
  const prim = primaryReson(sp);
  const wrongBeam = !discoBeamOK(sp);        // Entdeckung im falschen Strahl-Programm (für ALICE/pp = Referenz)
  const notProd = !wrongBeam && prodVis(prim) <= 0;  // Rate bei dieser Energie zu gering (richtiger Strahl)
  $("lbl-sig").innerText = sig.toFixed(2) + " σ";

  let sigBar = $("sig-bar"), sigStatus = $("lbl-sig-status");
  sigBar.style.width = ((wrongBeam||notProd) ? 0 : Math.min(100,(sig/5.0)*100)) + "%";

  if (sig === 0) {
    sigStatus.innerText = wrongBeam ? wrongBeamShort(sp)
                        : notProd  ? "Inbetriebnahme · "+prim.label+"-Rate zu gering"
                        :            "Rauschen (Kein Signal)";
    sigStatus.style.color = "#8b949e"; sigBar.style.background = "#30363d";
  } else if (sig < 3.0) {
    sigStatus.innerText = "Rauschen (Keine Signifikanz)";
    sigStatus.style.color = "#8b949e"; sigBar.style.background = "#58a6ff";
  } else if (sig < 5.0) {
    sigStatus.innerText = "⚠️ Signal-Hinweis (Evidence!)";
    sigStatus.style.color = "#ff7f0e"; sigBar.style.background = "#ff7f0e";
  } else {
    sigStatus.innerText = sp.disco;
    sigStatus.style.color = "#2ea44f"; sigBar.style.background = "#2ea44f";
  }

  const activeData = s.massStore[s.selDet];
  if(!activeData.length){
    ctxHist.fillStyle="#8b949e"; ctxHist.font="10px monospace";
    ctxHist.fillText("WARTEN AUF KOLLISIONSDATEN...",w/2-90,h/2);
    return;
  }

  // Histogramm
  let nb=sp.bins, bins=Array(nb).fill(0);
  activeData.forEach(v=>{if(v>=mn&&v<mx){let i=Math.floor((v-mn)/(mx-mn)*nb);if(i>=0&&i<nb)bins[i]++;}});
  let maxB=Math.max(...bins,1),bw=(w-40)/nb;
  let fc=sp.fc, tc=sp.col;
  for(let i=0;i<nb;i++){
    let bh=bins[i]/maxB*(h-30);let x=30+i*bw,y=h-16-bh;
    ctxHist.fillStyle=fc;ctxHist.fillRect(x,y,bw-1,bh);ctxHist.fillStyle=tc;ctxHist.fillRect(x,y,bw-1,1.5);
  }
  // Fehlerbalken (±√N pro Bin) – Poisson-Statistik
  if(activeData.length>20){
    ctxHist.strokeStyle=sp.col; ctxHist.globalAlpha=0.7; ctxHist.lineWidth=0.9;
    for(let i=0;i<nb;i++){
      if(bins[i]<3) continue;
      let bh=bins[i]/maxB*(h-30); let x=30+(i+0.5)*bw, y=h-16-bh;
      let err=Math.sqrt(bins[i])/maxB*(h-30);
      ctxHist.beginPath(); ctxHist.moveTo(x,y-err); ctxHist.lineTo(x,y+err); ctxHist.stroke();
      ctxHist.beginPath(); ctxHist.moveTo(x-2,y-err); ctxHist.lineTo(x+2,y-err); ctxHist.stroke();
      ctxHist.beginPath(); ctxHist.moveTo(x-2,y+err); ctxHist.lineTo(x+2,y+err); ctxHist.stroke();
    }
    ctxHist.globalAlpha=1;
  }
  // Resonanz-Marker (gestrichelt) bei den PDG-Massen des Detektors. Nicht
  // erzeugbare Resonanzen (Energie unter Schwelle) werden blass markiert —
  // die Linie zeigt, WO der Peak stünde, sobald genug Energie da ist.
  {ctxHist.save(); ctxHist.setLineDash([3,3]); ctxHist.lineWidth=0.9;
   sp.reson.forEach(r=>{ if(r.m<mn||r.m>mx) return;
    const xm=30+(r.m-mn)/(mx-mn)*(w-40);
    const on=prodVis(r)>0;
    ctxHist.strokeStyle=on?"rgba(255,255,255,0.30)":"rgba(255,255,255,0.12)";
    ctxHist.beginPath(); ctxHist.moveTo(xm,h-16); ctxHist.lineTo(xm,10); ctxHist.stroke();
    ctxHist.fillStyle=on?"rgba(255,255,255,0.45)":"rgba(255,255,255,0.22)";
    ctxHist.font="6.5px sans-serif";
    ctxHist.fillText(r.label, xm+2, 16); });
   ctxHist.restore(); }

  // Fit-Kurve aus DEMSELBEN Modell wie die Daten (bg + Σ Resonanz·drawVis) →
  // liegt immer auf den Balken; unter der Schwelle bleibt nur das Kontinuum.
  if (sig > 0.5) {
    let alpha = Math.min(1.0, Math.max(0, (sig - 0.5) / 3.5));
    ctxHist.save(); ctxHist.globalAlpha = alpha;
    let ys=[], ymax=1e-9;
    for(let xp=30;xp<w-8;xp++){
      let v=mn+(xp-30)/(w-38)*(mx-mn), yv=fitVal(sp,v);
      ys.push(yv); if(yv>ymax)ymax=yv;
    }
    ctxHist.strokeStyle=sp.col; ctxHist.lineWidth=1.7; ctxHist.beginPath();
    ys.forEach((yv,k)=>{ let yp=h-16-(yv/ymax)*(h-30); yp=Math.max(8,Math.min(h-16,yp));
      k===0?ctxHist.moveTo(30+k,yp):ctxHist.lineTo(30+k,yp); });
    ctxHist.stroke();
    // Beschriftung
    ctxHist.fillStyle=sp.col; ctxHist.font="8px sans-serif";
    ctxHist.fillText(sp.title, 36, 22);
    ctxHist.fillStyle="rgba(205,214,228,0.75)"; ctxHist.font="7px sans-serif";
    ctxHist.fillText(sp.sub, 36, 35);
    if(sp.channel==="4l"){ ctxHist.fillStyle="#aec7e8"; ctxHist.font="7px sans-serif";
      ctxHist.fillText("Higgs-Fenster (120–130 GeV): "+s.higgsCands+" 4ℓ-Kandidaten", 36, 47); }
    ctxHist.restore();
  }

  // Status-Hinweise unter der Achse
  if (sig < 5.0) {
    ctxHist.fillStyle="rgba(255,255,255,0.45)"; ctxHist.font="8px monospace";
    if (wrongBeam) {
      ctxHist.fillText(sp.discoBeam==="PbPb"
        ? "ℹ️ p-p-Referenz: Quarkonia unverdrängt. QGP-Unterdrückung nur im Pb-Pb-Lauf sichtbar."
        : "⚠️ "+prim.label+"-Entdeckung braucht "+beamLabel(sp.discoBeam)+"-Strahl — aktuell "+beamLabel(curBeam())+". Falsches Preset.", 36, h-26);
    } else if (notProd) {
      ctxHist.fillText("⚠️ "+prim.label+"-Produktionsrate bei "+s.paramEnergy.toFixed(2)+" TeV zu gering für Entdeckung — ≥ "+prim.thr.toFixed(2)+" TeV nötig.", 36, h-26);
    } else if (s.collStore[s.selDet] === 0) {
      ctxHist.fillText("Keine Kollisionen in "+s.selDet+". Starte Kollisionen!", 36, h-26);
    } else if (sp.reson.some(r=>r.qgp) && s.isIon) {
      ctxHist.fillText("Sammle Statistik · QGP unterdrückt "+prim.label+" (Signifikanz: " + sig.toFixed(1) + "σ / 5.0σ)", 36, h-26);
    } else {
      ctxHist.fillText("Sammle Statistik (Signifikanz: " + sig.toFixed(1) + "σ / 5.0σ)", 36, h-26);
    }
  }
}

App.classify = classify;
App.sampleEvent = sampleEvent;
App.resetSpectrumData = resetSpectrumData;
App.generateMassData = generateMassData;
App.accumulateStats = accumulateStats;
App.getSignificance = getSignificance;
App.drawHist = drawHist;
