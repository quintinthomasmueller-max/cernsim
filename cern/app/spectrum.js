// ═══════════════════════════════════════════════════════════════════════════
// HISTOGRAM
// ═══════════════════════════════════════════════════════════════════════════
// ── Physik-gekoppeltes Sampling aus ECHTEN CMS-Open-Data (CERN_REAL) ──
// Eine Kollision liefert EIN physikalisches Event, dessen invariante Masse
// sowohl das Event-Display (Topologie) als auch das Histogramm speist.
let _lhcbPool=null;
function lhcbPool(){
 if(_lhcbPool) return _lhcbPool;
 // CMS-Dimuon-Set enthält keine B-Mesonen -> kalibrierte Simulation:
 // B⁰ bei 5.279 GeV (CPT-konform) auf flachem kombinatorischem Untergrund.
 _lhcbPool=[]; for(let i=0;i<1400;i++){
  _lhcbPool.push(Math.random()<0.45
    ? 5.279+(Math.random()+Math.random()+Math.random()-1.5)*0.06
    : 4.6+Math.random()*1.4);
 }
 return _lhcbPool;
}
function currentPool(){
 switch(activePhysicsMode){
  case "QGP":   return CERN_REAL.ion;   // Pb-Pb-äquiv.: J/ψ, Υ
  case "PILOT": return CERN_REAL.low;   // Tiefmasse: ρ/ω, φ
  case "LHCB":  return lhcbPool();      // B-Physik (kalibriert)
  default:      return CERN_REAL.pp;    // HIGGS: Z⁰-Region
 }
}
function getModeRange(){
 switch(activePhysicsMode){
  case "QGP":   return [1,12];
  case "LHCB":  return [4.6,6.0];
  case "PILOT": return [0.4,2.0];
  default:      return [50,150];        // HIGGS
 }
}

function classify(m){
 // ordnet eine reale Masse der nächstgelegenen Resonanz zu (sonst Untergrund)
 let best=null, bd=1e9;
 for(const k in CERN_REAL.reso){
  if(k==="Higgs") continue;                  // anderer Kanal (4ℓ), nicht im Dimuon
  let mm=CERN_REAL.reso[k][0], br=CERN_REAL.reso[k][1];
  let tol=Math.max(0.15, br*1.5+0.035*mm);   // Fenster aus nat. Breite + Detektorauflösung
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
 let pt=5+Math.random()*20, a=Math.random()*6.283;          // Fallback: 2 gegensätzliche Spuren
 return [{pt:pt,eta:(Math.random()-.5)*3,phi:a,q:1,lep:"μ"},
         {pt:pt*(0.6+Math.random()*0.6),eta:(Math.random()-.5)*3,phi:a+Math.PI,q:-1,lep:"μ"}];
}

function sampleEvent(){
 // Higgs-Goldkanal: in p-p (kein LHCb) erst ab E>=4 TeV, selten ein H→ZZ*→4ℓ-Kandidat
 if(!isIon && selDet!=="LHCB" && paramEnergy>=4.0 && Math.random()<0.012){
  let m=CERN_REAL.higgs4l[(Math.random()*CERN_REAL.higgs4l.length)|0];
  let leptons=[]; for(let i=0;i<4;i++) leptons.push({pt:8+Math.random()*40,
    eta:(Math.random()-.5)*4, phi:Math.random()*6.283, q:i%2?1:-1, lep:Math.random()<.5?"e":"μ"});
  let isSig=Math.abs(m-125)<5; if(isSig) higgsCands++;
  return {M:m, name:isSig?"Higgs":null, channel:"4l", leptons:leptons, signal:isSig};
 }
 let pool=currentPool();
 let m=pool[(Math.random()*pool.length)|0];
 let name=classify(m);
 return {M:m, name:name, channel:"2mu", leptons:pickTopo(name), signal:!!name};
}

function generateMassData(){
 // Datenrate ∝ Intensität² / β*  →  pro Kollision akkumuliert ein Schwung REALER Massen
 let rateFactor = Math.pow(paramIntensity, 2) / Math.max(0.3, paramBetaStar);
 let nBatch = Math.max(1, Math.round(rateFactor * 5));
 let pool = currentPool();
 for(let i=0;i<nBatch;i++) massData.push(pool[(Math.random()*pool.length)|0]);
 lastEvent = sampleEvent();
 if(lastEvent.channel==="2mu") massData.push(lastEvent.M);  // nur Dimuon ins Spektrum (4ℓ = eigener Kanal)
 return lastEvent;
}

function getTargetDiscover() {
  switch(activePhysicsMode){
   case "QGP":   return 300;   // Quarkonia-Unterdrückung
   case "LHCB":  return 400;   // CP-Asymmetrie
   case "PILOT": return 1e9;   // Inbetriebnahme: praktisch keine Entdeckung
   default:      return 500;   // HIGGS
  }
}

function getSignificance() {
  if (collisions === 0 || activePhysicsMode === "PILOT") return 0;
  if (activePhysicsMode === "HIGGS" && paramEnergy < 4.0) return 0; // Higgs braucht E >= 4 TeV
  return 5.0 * Math.sqrt(collisions / getTargetDiscover());
}

function drawHist(){
  let w=histW,h=histH;
  ctxHist.clearRect(0,0,w,h);
  ctxHist.strokeStyle="#30363d";ctxHist.lineWidth=1;
  ctxHist.beginPath();ctxHist.moveTo(30,8);ctxHist.lineTo(30,h-16);ctxHist.lineTo(w-8,h-16);ctxHist.stroke();
  ctxHist.fillStyle="#8b949e";ctxHist.font="7.5px sans-serif";
  let [mn,mx]=getModeRange();
  ctxHist.fillText(mn+" GeV",30,h-5);ctxHist.fillText(mx+" GeV",w-40,h-5);
  
  let sig = getSignificance();
  $("lbl-sig").innerText = sig.toFixed(2) + " σ";
  
  let sigBar = $("sig-bar");
  let sigStatus = $("lbl-sig-status");
  let target = getTargetDiscover();
  let pct = (activePhysicsMode==="PILOT" || (activePhysicsMode==="HIGGS" && paramEnergy < 4.0)) ? 0 : Math.min(100, (sig/5.0)*100);
  sigBar.style.width = pct + "%" ;
  
  if (sig === 0) {
    sigStatus.innerText = (activePhysicsMode==="PILOT") ? "Inbetriebnahme · Kalibrierung" : "Rauschen (Kein Signal)";
    sigStatus.style.color = "#8b949e";
    sigBar.style.background = "#30363d";
  } else if (sig < 3.0) {
    sigStatus.innerText = "Rauschen (Keine Signifikanz)";
    sigStatus.style.color = "#8b949e";
    sigBar.style.background = "#58a6ff";
  } else if (sig < 5.0) {
    sigStatus.innerText = "⚠️ Signal-Hinweis (Evidence!)";
    sigStatus.style.color = "#ff7f0e";
    sigBar.style.background = "#ff7f0e";
  } else {
    sigStatus.innerText = {HIGGS:"🌟 5σ: Higgs-Boson entdeckt!", QGP:"🌟 5σ: Quarkonia-Unterdrückung (QGP)!", LHCB:"🌟 5σ: CP-Verletzung etabliert!"}[activePhysicsMode] || "🌟 5σ ENTDECKUNG!";
    sigStatus.style.color = "#2ea44f";
    sigBar.style.background = "#2ea44f";
  }
  
  if(!massData.length){
    ctxHist.fillStyle="#8b949e";
    ctxHist.font="10px monospace";
    ctxHist.fillText("WARTEN AUF KOLLISIONSDATEN...",w/2-90,h/2);
    return;
  }
  
  // Bin-Anzahl je Modus (breite Bereiche → mehr Bins)
  let nb = activePhysicsMode==="HIGGS" ? 60 : activePhysicsMode==="QGP" ? 55 : 50;
  let bins=Array(nb).fill(0);
  massData.forEach(v=>{if(v>=mn&&v<mx){let i=Math.floor((v-mn)/(mx-mn)*nb);if(i>=0&&i<nb)bins[i]++;}});
  let maxB=Math.max(...bins,1),bw=(w-40)/nb;
  let fc=isIon?"rgba(227,119,194,0.38)":"rgba(88,166,255,0.38)";
  let tc=isIon?"#e377c2":"#58a6ff";
  // Balken
  for(let i=0;i<nb;i++){
    let bh=bins[i]/maxB*(h-30);let x=30+i*bw,y=h-16-bh;
    ctxHist.fillStyle=fc;ctxHist.fillRect(x,y,bw-1,bh);ctxHist.fillStyle=tc;ctxHist.fillRect(x,y,bw-1,1.5);
  }
  // Fehlerbalken (±√N pro Bin) – Poisson-Statistik
  if(massData.length>20){
    ctxHist.strokeStyle=isIon?"rgba(227,119,194,0.75)":"rgba(88,166,255,0.75)"; ctxHist.lineWidth=0.9;
    for(let i=0;i<nb;i++){
      if(bins[i]<3) continue;
      let bh=bins[i]/maxB*(h-30); let x=30+(i+0.5)*bw, y=h-16-bh;
      let err=Math.sqrt(bins[i])/maxB*(h-30);
      ctxHist.beginPath(); ctxHist.moveTo(x,y-err); ctxHist.lineTo(x,y+err); ctxHist.stroke();
      ctxHist.beginPath(); ctxHist.moveTo(x-2,y-err); ctxHist.lineTo(x+2,y-err); ctxHist.stroke();
      ctxHist.beginPath(); ctxHist.moveTo(x-2,y+err); ctxHist.lineTo(x+2,y+err); ctxHist.stroke();
    }
  }
  // Resonanz-Marker: gestrichelte Linien bei den bekannten PDG-Massen
  {const markers={HIGGS:[[91.19,"Z⁰"]], QGP:[[3.097,"J/ψ"],[9.46,"Υ"]],
                  LHCB:[[5.279,"B⁰"]], PILOT:[[0.78,"ρ/ω"],[1.019,"φ"]]};
   const mm=markers[activePhysicsMode]||[];
   ctxHist.save(); ctxHist.setLineDash([3,3]); ctxHist.lineWidth=0.9;
   mm.forEach(([m,lbl])=>{ if(m<mn||m>mx) return;
    const xm=30+(m-mn)/(mx-mn)*(w-40);
    ctxHist.strokeStyle="rgba(255,255,255,0.30)"; ctxHist.beginPath(); ctxHist.moveTo(xm,h-16); ctxHist.lineTo(xm,10); ctxHist.stroke();
    ctxHist.fillStyle="rgba(255,255,255,0.45)"; ctxHist.font="6.5px sans-serif";
    ctxHist.fillText(lbl, xm+2, 16); });
   ctxHist.restore(); }
  
  if (sig > 0.5) {
    let alpha = Math.min(1.0, Math.max(0, (sig - 0.5) / 3.5));
    ctxHist.save();
    ctxHist.globalAlpha = alpha;
    
        const G=(v,m,s)=>Math.exp(-0.5*((v-m)/s)**2);
    // Analytisches Modell (normiert auf 1 am Peak)
    let ys=[], ymax=1e-9;
    for(let xp=30;xp<w-8;xp++){
      let v=mn+(xp-30)/(w-38)*(mx-mn), yv;
      if(activePhysicsMode==="QGP")        yv=0.30+G(v,3.097,0.12)*1.0+G(v,9.46,0.25)*0.35;
      else if(activePhysicsMode==="LHCB")  yv=0.15+G(v,5.279,0.06)*1.0;
      else if(activePhysicsMode==="PILOT") yv=Math.exp(-(v-0.4)/0.5)*0.5+G(v,0.78,0.10)*1.0+G(v,1.019,0.03)*0.5;
      else                                 yv=Math.exp(-(v-50)/25)*0.30+G(v,91.19,2.6)*1.0;
      ys.push(yv); if(yv>ymax)ymax=yv;
    }
    // Skalierung: Kurven-Peak auf Daten-Peak ausrichten (nicht auf Canvas-Höhe)
    // Dazu Kurven-Integral über alle Pixel berechnen und auf massData.length normieren.
    // Einfacher Ankerpunkt: Kurve trifft maxB am höchsten Datenpunkt.
    let yscale = maxB / ymax;          // 1 Kurven-Peak-Einheit = maxB Bin-Counts
    ctxHist.strokeStyle="rgba(248,81,73,1)"; ctxHist.lineWidth=1.5; ctxHist.beginPath();
    ys.forEach((yv,k)=>{
      let yp=h-16-(yv*yscale/maxB)*(h-30); yp=Math.max(8,Math.min(h-16,yp));
      k===0?ctxHist.moveTo(30+k,yp):ctxHist.lineTo(30+k,yp); });
    ctxHist.stroke();

    ctxHist.fillStyle="#f0f6fc"; ctxHist.font="8.5px sans-serif";
    if(activePhysicsMode==="HIGGS"){
      ctxHist.fillText("Z⁰ → μ⁺μ⁻ (91 GeV) · echte CMS-Daten", w*.28, 22);
      if(paramEnergy>=4.0){ ctxHist.fillStyle="#aec7e8";
        ctxHist.fillText("Higgs→4ℓ-Kandidaten (Goldkanal): "+higgsCands, w*.50, 38); }
      else{ ctxHist.fillStyle="rgba(248,81,73,0.7)";
        ctxHist.fillText("Higgs-Produktion unterdrückt (E < 4 TeV)", w*.48, 38); }
    } else if(activePhysicsMode==="QGP"){
      ctxHist.fillText("J/ψ → μ⁺μ⁻ (3.1 GeV) · echte CMS-Daten", w*.10, 20);
      ctxHist.fillText("Υ(1S,2S,3S) (9.5 GeV)", w*.60, 42);
    } else if(activePhysicsMode==="LHCB"){
      ctxHist.fillText("B⁰ → h⁺h⁻ (5.28 GeV) · kalibrierte Simulation", w*.18, 22);
      ctxHist.fillText("CP-Asymmetrie Materie / Antimaterie", w*.28, 40);
    } else { // PILOT
      ctxHist.fillText("ρ⁰/ω (0.78) · φ (1.02 GeV) · Teststrahl", w*.16, 20);
      ctxHist.fillText("unkalibriert – Detektor-Inbetriebnahme", w*.26, 40);
    }
    ctxHist.restore();
  }
  
  if (sig < 5.0) {
    ctxHist.fillStyle="rgba(255,255,255,0.45)";
    ctxHist.font="8.5px monospace";
    if (sig === 0) {
      if (activePhysicsMode==="PILOT") {
        ctxHist.fillText("Pilot-Strahl: Detektor-Kalibrierung – keine Entdeckung angestrebt.", w/2 - 155, 12);
      } else if (activePhysicsMode==="HIGGS" && paramEnergy < 4.0) {
        ctxHist.fillText("⚠️ Strahlenergie zu gering für Higgs-Produktion (< 4.0 TeV)!", w/2 - 145, 12);
      } else {
        ctxHist.fillText("Keine Kollisionen akkumuliert. Starte Kollisionen!", w/2 - 120, 12);
      }
    } else {
      ctxHist.fillText("Sammle Statistik für Entdeckung (Signifikanz: " + sig.toFixed(1) + "σ / 5.0σ)", w/2 - 140, 12);
    }
  }
}

