// ═══════════════════════════════════════════════════════════════════════════
// HISTOGRAM / MASSENSPEKTRUM  — DETEKTOR-GETRIEBEN
// ═══════════════════════════════════════════════════════════════════════════
// Grundsatz: Das angezeigte Massenspektrum hängt AUSSCHLIESSLICH vom gewählten
// Detektor (selDet) ab — jeder Detektor misst physikalisch andere Kanäle.
// Presets setzen nur Maschinenparameter + wählen den passenden Detektor; das
// Spektrum folgt konsequent. Jeder Detektor akkumuliert sein eigenes Spektrum
// (massStore[selDet]) und seine eigene Signifikanz (collStore[selDet]).
//
// Daten: echte CMS-Open-Data (CERN_REAL); LHCb-B-Physik = kalibrierte Simulation
// (CMS-Dimuon-Set enthält keine B-Mesonen).
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

const G=(v,m,s)=>Math.exp(-0.5*((v-m)/s)**2);

// ── ZENTRALE DETEKTOR-SPEKTRUM-TABELLE ──────────────────────────────────────
// Fit-Modelle wurden an die ECHTE Datenform angepasst (Peak-Lage stimmt mit den
// CERN_REAL-Verteilungen überein → Fit-Kurve liegt auf den Daten).
const DETSPEC = {
 ATLAS: {                                  // Allzweck: Präzisions-EW, Z⁰→μμ
  pool:()=>CERN_REAL.pp,  range:[50,150], bins:60, channel:"2mu",
  minE:1.0, target:200,   col:"#58a6ff", fc:"rgba(88,166,255,0.38)",
  markers:[[91.19,"Z⁰"]],
  fit:(v)=> Math.exp(-(v-50)/30)*0.12 + G(v,91.19,3.0),
  title:"ATLAS · Z⁰→μ⁺μ⁻ · Präzisions-Kalibrierkanal (echte CMS-Daten)",
  sub:"Standardmodell-EW · Z⁰-Resonanz bei 91 GeV",
  disco:"🌟 5σ: Z⁰-Resonanz präzise vermessen!"
 },
 CMS: {                                    // Allzweck: Higgs-Goldkanal H→ZZ*→4ℓ
  pool:()=>CERN_REAL.higgs4l, range:[80,200], bins:60, channel:"4l",
  minE:4.0, target:600,   col:"#2ea44f", fc:"rgba(46,164,79,0.38)",
  markers:[[91.19,"Z⁰"],[125.09,"H 125"]],
  // Fallendes ZZ*-Kontinuum + Higgs-Bump bei 124 (in 2-GeV-Bins knapp der höchste Peak)
  fit:(v)=> Math.exp(-(v-80)/46) + 0.66*G(v,124,2.8),
  title:"CMS · H→ZZ*→4ℓ · Goldkanal (Higgs bei 125 GeV)",
  sub:"Kleines Signal auf großem ZZ*-Untergrund · braucht ≥ 4 TeV",
  disco:"🌟 5σ: Higgs-Boson entdeckt!"
 },
 ALICE: {                                  // Schwerionen: Quarkonia (QGP)
  pool:()=>CERN_REAL.ion, range:[1,12], bins:55, channel:"2mu",
  minE:1.0, target:300,   col:"#e377c2", fc:"rgba(227,119,194,0.38)",
  markers:[[3.097,"J/ψ"],[9.46,"Υ"]],
  fit:(v)=> 0.27 + G(v,3.097,0.18)*0.73 + G(v,9.6,0.7)*0.16,
  title:"ALICE · J/ψ + Υ → μ⁺μ⁻ · Quarkonia (echte CMS-Daten)",
  sub:"Quark-Gluon-Plasma: Unterdrückung der Quarkonia-Zustände",
  disco:"🌟 5σ: Quarkonia-Unterdrückung (QGP) nachgewiesen!"
 },
 LHCB: {                                   // B-Physik: CP-Verletzung
  pool:()=>lhcbPool(), range:[4.6,6.0], bins:50, channel:"B",
  minE:1.0, target:400,   col:"#ff7f0e", fc:"rgba(255,127,14,0.38)",
  markers:[[5.279,"B⁰"]],
  fit:(v)=> 0.25 + G(v,5.279,0.07)*0.75,
  title:"LHCb · B⁰ → h⁺h⁻ · CP-Verletzung (kalibrierte Simulation)",
  sub:"Materie-Antimaterie-Asymmetrie im B-Mesonen-Zerfall",
  disco:"🌟 5σ: CP-Verletzung etabliert!"
 }
};
function spec(){ return DETSPEC[selDet] || DETSPEC.ATLAS; }

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

function sampleEvent(){
 const sp=spec();
 let m=sp.pool()[(Math.random()*sp.pool().length)|0];
 if(sp.channel==="4l"){
  // Higgs-Goldkanal: 4-Lepton-Topologie (2 Z→ℓℓ-Paare)
  let leptons=[]; for(let i=0;i<4;i++) leptons.push({pt:8+Math.random()*40,
    eta:(Math.random()-.5)*4, phi:Math.random()*6.283, q:i%2?1:-1, lep:Math.random()<.5?"e":"μ"});
  let isSig=Math.abs(m-125)<5; if(isSig) higgsCands++;
  return {M:m, name:isSig?"Higgs":null, channel:"4l", leptons:leptons, signal:isSig};
 }
 // Dimuon (ATLAS/ALICE) bzw. B-Vertex (LHCb) → 2-Spur-Topologie
 let name=classify(m);
 return {M:m, name:name, channel:sp.channel, leptons:pickTopo(name), signal:!!name};
}

function resetSpectrumData(){
 massStore={ATLAS:[], CMS:[], ALICE:[], LHCB:[]};
 collStore={ATLAS:0, CMS:0, ALICE:0, LHCB:0};
 higgsCands=0;
}

function generateMassData(){
 const sp=spec();
 // Datenrate ∝ Intensität² / β* (4ℓ-Goldkanal seltener → kleinerer Faktor)
 let rateFactor = Math.pow(paramIntensity, 2) / Math.max(0.3, paramBetaStar);
 let n = Math.max(1, Math.round(rateFactor * (sp.channel==="4l"?1.5:5)));
 const store = massStore[selDet];
 for(let i=0;i<n;i++) store.push(sp.pool()[(Math.random()*sp.pool().length)|0]);
 collStore[selDet] += 1;
 lastEvent = sampleEvent();
 store.push(lastEvent.M);   // das angezeigte Event landet immer im Spektrum des Detektors
 return lastEvent;
}

function getSignificance() {
  const sp=spec(), n=collStore[selDet];
  if (n === 0) return 0;
  if (paramEnergy < sp.minE) return 0;            // Energie zu gering (z. B. Pilot-Strahl)
  return 5.0 * Math.sqrt(n / sp.target);
}

function drawHist(){
  const sp=spec();
  let w=histW,h=histH;
  ctxHist.clearRect(0,0,w,h);
  ctxHist.strokeStyle="#30363d";ctxHist.lineWidth=1;
  ctxHist.beginPath();ctxHist.moveTo(30,8);ctxHist.lineTo(30,h-16);ctxHist.lineTo(w-8,h-16);ctxHist.stroke();
  ctxHist.fillStyle="#8b949e";ctxHist.font="7.5px sans-serif";
  let [mn,mx]=sp.range;
  ctxHist.fillText(mn+" GeV",30,h-5);ctxHist.fillText(mx+" GeV",w-40,h-5);

  let sig = getSignificance();
  const lowE = paramEnergy < sp.minE;
  $("lbl-sig").innerText = sig.toFixed(2) + " σ";

  let sigBar = $("sig-bar"), sigStatus = $("lbl-sig-status");
  sigBar.style.width = (lowE ? 0 : Math.min(100,(sig/5.0)*100)) + "%";

  if (sig === 0) {
    sigStatus.innerText = lowE ? "Inbetriebnahme · Energie zu gering" : "Rauschen (Kein Signal)";
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

  const activeData = massStore[selDet];
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
  // Resonanz-Marker (gestrichelt) bei den PDG-Massen des Detektors
  {ctxHist.save(); ctxHist.setLineDash([3,3]); ctxHist.lineWidth=0.9;
   sp.markers.forEach(([m,lbl])=>{ if(m<mn||m>mx) return;
    const xm=30+(m-mn)/(mx-mn)*(w-40);
    ctxHist.strokeStyle="rgba(255,255,255,0.30)"; ctxHist.beginPath(); ctxHist.moveTo(xm,h-16); ctxHist.lineTo(xm,10); ctxHist.stroke();
    ctxHist.fillStyle="rgba(255,255,255,0.45)"; ctxHist.font="6.5px sans-serif";
    ctxHist.fillText(lbl, xm+2, 16); });
   ctxHist.restore(); }

  // Fit-Kurve (an die echte Datenform angepasst → liegt auf den Balken)
  if (sig > 0.5 && !lowE) {
    let alpha = Math.min(1.0, Math.max(0, (sig - 0.5) / 3.5));
    ctxHist.save(); ctxHist.globalAlpha = alpha;
    let ys=[], ymax=1e-9;
    for(let xp=30;xp<w-8;xp++){
      let v=mn+(xp-30)/(w-38)*(mx-mn), yv=sp.fit(v);
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
      ctxHist.fillText("Higgs-Fenster (120–130 GeV): "+higgsCands+" 4ℓ-Kandidaten", 36, 47); }
    ctxHist.restore();
  }

  // Status-Hinweise unter der Achse
  if (sig < 5.0) {
    ctxHist.fillStyle="rgba(255,255,255,0.45)"; ctxHist.font="8px monospace";
    if (lowE) {
      ctxHist.fillText("⚠️ Strahlenergie zu gering ("+paramEnergy.toFixed(2)+" < "+sp.minE.toFixed(1)+" TeV) — keine Entdeckung möglich.", 36, h-26);
    } else if (sig === 0) {
      ctxHist.fillText("Keine Kollisionen in "+selDet+". Starte Kollisionen!", 36, h-26);
    } else {
      ctxHist.fillText("Sammle Statistik (Signifikanz: " + sig.toFixed(1) + "σ / 5.0σ)", 36, h-26);
    }
  }
}
