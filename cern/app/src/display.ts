// ═══════════════════════════════════════════════════════════════════════════
// DETEKTOR-GEOMETRIE & TEILCHEN-SIGNATUREN  (didaktisches Event-Display)
// Lerninhalt: Detektoren sind ZWIEBELSCHALEN aus Materialschichten — jede
// Teilchenart bleibt in „ihrer" Schicht stecken (Signatur). Gefüllte Bänder +
// Klartext-Callouts + Maßstab (Mensch) + klickbare Schichten + Signaturen-Tour.
// Querschnitt über App.state (s) / App.els (E.ctxEv). Refs werden bei Boot befüllt.
// ═══════════════════════════════════════════════════════════════════════════
import { App } from './core.js';

const s = App.state, E = App.els;

const DETKONFIG: Record<string, DetConfig> = {
 // bend = visuelle Krümmungsstärke (skaliert mit B-Feld: CMS 3.8T > ATLAS 2T > ALICE 0.5T)
 // realRmu = echter Außenradius (m) der Myonlage → Maßstab (Mensch/Meterleiste)
 // r = AUSSENradius je Schicht (Modell-Einheiten; Außen=86=realRmu bleibt maßstäblicher
 //     Anker für Mensch/Meterleiste). Die Schicht-DICKEN sind bewusst KEIN Innen-Maßstab:
 //     alle ~gleich dick, nur moduliert mit der echten relativen Dicke und gekappt auf
 //     [1/1,5 … 1,5]× der Gleichverteilung — jede Schale bleibt lesbar, dicker/dünner
 //     bleibt erkennbar. (Dicken→r via clamp(echteDicke/Mittel,1/1,5,1,5), Spanne 5→86.)
 ATLAS: { typ:'barrel', farbe:'#58a6ff', rolle:'Allzweck-Detektor · 2 T Solenoid + Toroid-Myonsystem', bend:0.80,
   realRmu:12.5, fakt:'46 m lang · Ø 25 m · 7 000 t',
   lagen:[ {r:16.4,name:'Spurdetektor',kind:'track',job:'Spuren geladener Teilchen',infoKey:'L_TRACK'},
           {r:27.8,name:'EM-Kalorimeter',kind:'em',job:'stoppt e⁻ & Photonen',infoKey:'L_EM'},
           {r:43.2,name:'Hadron-Kalorimeter',kind:'had',job:'stoppt Protonen & Co.',infoKey:'L_HAD'},
           {r:68.9,name:'Toroid-Magnet',kind:'coil',job:'krümmt die Bahnen',infoKey:'L_COIL'},
           {r:86,name:'Myonkammern',kind:'muon',job:'nur Myonen kommen an',infoKey:'L_MUON'} ] },
 CMS: { typ:'barrel', farbe:'#f85149', rolle:'Allzweck-Detektor · 3,8 T Solenoid · Kristall-Kalorimeter', bend:1.40,
   realRmu:7.4, fakt:'21 m lang · Ø 15 m · 14 000 t (schwerer als der Eiffelturm)',
   lagen:[ {r:19.4,name:'Silizium-Tracker',kind:'track',job:'Spuren geladener Teilchen',infoKey:'L_TRACK'},
           {r:31.6,name:'ECAL (Kristalle)',kind:'em',job:'stoppt e⁻ & Photonen',infoKey:'L_EM'},
           {r:46.2,name:'HCAL (Messing)',kind:'had',job:'stoppt Protonen & Co.',infoKey:'L_HAD'},
           {r:58.5,name:'Solenoid-Magnet',kind:'coil',job:'krümmt die Bahnen · 3,8 T',infoKey:'L_COIL'},
           {r:86,name:'Myonkammern im Joch',kind:'muon',job:'nur Myonen kommen an',infoKey:'L_MUON'} ] },
 ALICE: { typ:'barrel', farbe:'#e377c2', rolle:'Schwerionen · TPC · hohe Spurdichte · 0,5 T', bend:0.60,
   realRmu:8.0, fakt:'26 m lang · Ø 16 m · 10 000 t',
   lagen:[ {r:18.5,name:'ITS (Silizium-Pixel)',kind:'track',job:'Spur-Ursprung & Vertices',infoKey:'L_TRACK'},
           {r:42.2,name:'TPC (Gas-Kammer)',kind:'track',job:'3D-Spuren, bis zu 20 000',infoKey:'L_TPC'},
           {r:55.7,name:'TOF (Stoppuhr)',kind:'em',job:'identifiziert Teilchensorte',infoKey:'L_TOF'},
           {r:86,name:'Außenlagen',kind:'muon',job:'Myonen & Restsignale',infoKey:'L_MUON'} ] },
 LHCB: { typ:'forward', farbe:'#ff7f0e', rolle:'Vorwärts-Spektrometer · Sekundärvertex',
   realLen:21, fakt:'21 m lang · 5 600 t · misst nur den Vorwärtskegel',
   stationen:[ {x:34,name:'VELO',kind:'vtx',w:8,infoKey:'L_VTX'}, {x:80,name:'RICH1',kind:'rich',w:12,infoKey:'L_RICH'},
               {x:120,name:'TT',kind:'track',w:6,infoKey:'L_TRACK'},
               {x:160,name:'Dipol',kind:'magnet',w:18,infoKey:'L_MAGNET'}, {x:210,name:'RICH2',kind:'rich',w:14,infoKey:'L_RICH'},
               {x:250,name:'ECAL',kind:'em',w:10,infoKey:'L_EM'}, {x:285,name:'HCAL',kind:'had',w:12,infoKey:'L_HAD'},
               {x:315,name:'Myon',kind:'muon',w:16,infoKey:'L_MUON'} ] }
};
// Farbsystem je Schicht-Art: RGB + Basis-Alpha (Band-Füllung), Strich, Text.
const KIND_RGB = { track:[88,166,255], em:[46,164,79], had:[255,127,14], coil:[150,162,176],
                   muon:[248,81,73], vtx:[255,255,255], rich:[88,166,255], magnet:[241,224,90] };
const KIND_FILL_A = { track:0.10, em:0.13, had:0.11, coil:0.26, muon:0.09, vtx:0.20, rich:0.10, magnet:0.28 };
const KIND_TXT = { track:'#79c0ff', em:'#3fb950', had:'#ffa657', coil:'#aeb8c2', muon:'#ff7b72',
                   vtx:'#f0f6fc', rich:'#79c0ff', magnet:'#f1e05a' };
function kindFill(kind, mode){ const c=KIND_RGB[kind]||[139,148,158]; let a=KIND_FILL_A[kind]||0.10;
 if(mode==='hi') a=Math.min(0.42, a*2.6); else if(mode==='lo') a*=0.35;
 return `rgba(${c[0]},${c[1]},${c[2]},${a.toFixed(3)})`; }
function layerColor(k){ return ({track:'rgba(88,166,255,0.32)',em:'rgba(46,164,79,0.34)',had:'rgba(255,127,14,0.30)',
  coil:'rgba(139,148,158,0.42)',muon:'rgba(248,81,73,0.34)',vtx:'rgba(255,255,255,0.45)',rich:'rgba(88,166,255,0.18)',
  magnet:'rgba(241,224,90,0.5)'})[k] || 'rgba(139,148,158,0.25)'; }

// Layout: Barrel-Querschnitt links, rechts eine Klartext-Spalte (Callouts) —
// Lehrbuch-Stil statt 6px-Kürzel auf den Ringen. lblX/lblW = Spaltengeometrie.
const R_PIPE = 5;   // Strahlrohr-Innenradius (Modell-Einheiten, wie lagen.r)
function detGeo(){
 const evW=s.evW, evH=s.evH, D=DETKONFIG[s.selDet]||DETKONFIG.ATLAS;
 if(D.typ!=='barrel'){ const cy=evH/2; return {D,cx:evW/2,cy,Rmax:Math.min(evW,evH)/2-6,sc:1,lblX:0,lblW:0}; }
 const lblW=Math.max(92, Math.min(150, evW*0.30));
 const Rmax=Math.min(evH/2-22, (evW-lblW-26)/2);
 return {D, cx:(evW-lblW-10)/2, cy:evH/2, Rmax, sc:Rmax/86, lblX:(evW-lblW-10)/2+Rmax+12, lblW};
}
// Ehrliche Datenherkunft des Event-Displays (strahl-/kanalabhängig): Dimuon-
// Signal- UND Untergrundspuren stammen aus echter CMS-μμ-Kinematik; 4ℓ (CMS-pp)
// und B-Vertex (LHCb) sind kalibrierte Simulation; Pb-Pb-Multiplizität ist
// didaktisch reduziert (real mehrere Tausend Spuren).
function evProvenance(){
 const ion=s.isIon;
 if(s.selDet==='CMS' && !ion) return "4ℓ-Kinematik und -Masse: echte CMS-Open-Data (Record 5200)";
 if(s.selDet==='LHCB')        return "Vertex und Spuren: illustrativ · B-Masse: Simulation";
 return "Signal- und Untergrund-μμ: echte CMS-Kinematik" + (ion ? " · Multipl. didakt. reduziert" : "");
}
function rKind(D,kind,last?){ let r=null; (D.lagen||[]).forEach(l=>{ if(l.kind===kind && (last||r===null)) r=l.r; }); return r; }
function radii(D,sc){ const trk=(rKind(D,'track',true)||30), em=(rKind(D,'em')||trk+10),
  had=(rKind(D,'had')||em+10), mu=(rKind(D,'muon')||had+20);
  return {Rtrk:trk*sc, Rem:em*sc, Rhad:had*sc, Rmu:mu*sc}; }

function drawLegend(){
 const ctxEv=E.ctxEv, evW=s.evW, evH=s.evH;
 // Legende mit Kurzinfo: was jede Farbe/Signatur bedeutet
 const items=[
  ['μ (alle Schichten)','#2ea44f'],
  ['e⁻ → EM-Kal.','#58a6ff'],
  ['γ → EM, keine Spur','#f1e05a'],
  ['Hadron → Had-Kal.','#ff7f0e'],
  ['ν (fehlende Energie)','#8b949e']
 ];
 const gap=Math.min(62,(evW-8)/items.length), y=evH-5;
 ctxEv.save(); ctxEv.font='6px sans-serif'; ctxEv.textAlign='left';
 items.forEach((it,i)=>{ const x=4+i*gap;
  ctxEv.fillStyle=it[1]; ctxEv.beginPath(); ctxEv.arc(x+2,y-2,2.3,0,2*Math.PI); ctxEv.fill();
  ctxEv.fillStyle='rgba(205,215,230,0.85)'; ctxEv.fillText(it[0], x+7, y); });
 ctxEv.restore(); }

// Strichmännchen in ECHTER Größe (1,8 m im Detektor-Maßstab) — DIE Brücke
// zwischen abstraktem Kreis und realem Bauwerk.
function drawHuman(x, fy, h){
 const ctxEv=E.ctxEv;
 ctxEv.save(); ctxEv.strokeStyle='rgba(240,246,252,0.9)'; ctxEv.fillStyle='rgba(240,246,252,0.9)';
 ctxEv.lineWidth=Math.max(1, h*0.07);
 ctxEv.beginPath(); ctxEv.arc(x, fy-h+h*0.14, Math.max(1.4,h*0.14), 0, 2*Math.PI); ctxEv.fill();
 ctxEv.beginPath(); ctxEv.moveTo(x, fy-h*0.70); ctxEv.lineTo(x, fy-h*0.34);            // Rumpf
 ctxEv.moveTo(x-h*0.18, fy-h*0.55); ctxEv.lineTo(x+h*0.18, fy-h*0.55);                 // Arme
 ctxEv.moveTo(x, fy-h*0.34); ctxEv.lineTo(x-h*0.15, fy);                               // Beine
 ctxEv.moveTo(x, fy-h*0.34); ctxEv.lineTo(x+h*0.15, fy); ctxEv.stroke();
 // Label-x clampen: am linken Canvas-Rand nicht abschneiden (zentrierter Text)
 const lx=Math.max(x,19);
 ctxEv.font='6px sans-serif'; ctxEv.textAlign='center'; ctxEv.fillStyle='rgba(205,215,230,0.75)';
 ctxEv.fillText('Mensch', lx, fy-h-9); ctxEv.fillText('1,8 m', lx, fy-h-2);
 ctxEv.restore();
}
function drawScaleBar(pxm, meters){
 const ctxEv=E.ctxEv, x0=8, y=26, len=meters*pxm;
 ctxEv.save(); ctxEv.strokeStyle='rgba(205,215,230,0.6)'; ctxEv.lineWidth=1;
 ctxEv.beginPath(); ctxEv.moveTo(x0,y); ctxEv.lineTo(x0+len,y);
 ctxEv.moveTo(x0,y-3); ctxEv.lineTo(x0,y+3); ctxEv.moveTo(x0+len,y-3); ctxEv.lineTo(x0+len,y+3); ctxEv.stroke();
 ctxEv.font='7px sans-serif'; ctxEv.textAlign='left'; ctxEv.fillStyle='rgba(205,215,230,0.75)';
 ctxEv.fillText(meters+' m', x0+len+5, y+2); ctxEv.restore();
}

function emCluster(cx,cy,ang,r0,r1,col){ const ctxEv=E.ctxEv; ctxEv.save(); ctxEv.globalAlpha=0.6; ctxEv.fillStyle=col; ctxEv.beginPath();
 ctxEv.moveTo(cx+r0*Math.cos(ang-0.14),cy+r0*Math.sin(ang-0.14));
 ctxEv.lineTo(cx+r1*Math.cos(ang-0.22),cy+r1*Math.sin(ang-0.22));
 ctxEv.lineTo(cx+r1*Math.cos(ang+0.22),cy+r1*Math.sin(ang+0.22));
 ctxEv.lineTo(cx+r0*Math.cos(ang+0.14),cy+r0*Math.sin(ang+0.14));
 ctxEv.closePath(); ctxEv.fill(); ctxEv.restore(); }
function hadShower(cx,cy,ang,r0,r1){ const ctxEv=E.ctxEv; ctxEv.strokeStyle='rgba(255,127,14,0.85)'; ctxEv.lineWidth=1;
 for(let k=0;k<5;k++){ let a=ang+(Math.random()-.5)*0.55; ctxEv.beginPath();
  ctxEv.moveTo(cx+r0*Math.cos(ang),cy+r0*Math.sin(ang)); ctxEv.lineTo(cx+r1*Math.cos(a),cy+r1*Math.sin(a)); ctxEv.stroke(); } }
function muonHit(p,ang){ const ctxEv=E.ctxEv; const px=Math.cos(ang+Math.PI/2), py=Math.sin(ang+Math.PI/2);
 ctxEv.strokeStyle='#2ea44f'; ctxEv.lineWidth=3; ctxEv.beginPath();
 ctxEv.moveTo(p[0]-4*px,p[1]-4*py); ctxEv.lineTo(p[0]+4*px,p[1]+4*py); ctxEv.stroke();
 ctxEv.fillStyle='#2ea44f'; ctxEv.beginPath(); ctxEv.arc(p[0],p[1],2.3,0,2*Math.PI); ctxEv.fill(); }
function metArrow(cx,cy,ang,len){ const ctxEv=E.ctxEv; ctxEv.save(); ctxEv.setLineDash([4,3]); ctxEv.strokeStyle='#8b949e'; ctxEv.lineWidth=1.8;
 const tx=cx+len*Math.cos(ang), ty=cy+len*Math.sin(ang);
 ctxEv.beginPath(); ctxEv.moveTo(cx,cy); ctxEv.lineTo(tx,ty); ctxEv.stroke(); ctxEv.setLineDash([]);
 ctxEv.fillStyle='#8b949e'; ctxEv.beginPath(); ctxEv.moveTo(tx,ty);
 ctxEv.lineTo(tx-7*Math.cos(ang-0.4),ty-7*Math.sin(ang-0.4)); ctxEv.lineTo(tx-7*Math.cos(ang+0.4),ty-7*Math.sin(ang+0.4));
 ctxEv.closePath(); ctxEv.fill();
 // Label: fehlende Transversalenergie
 ctxEv.font='5.5px monospace'; ctxEv.fillStyle='rgba(139,148,158,0.8)';
 ctxEv.fillText('E_T^miss',tx+4*Math.cos(ang+Math.PI/2),ty+4*Math.sin(ang+Math.PI/2));
 ctxEv.restore(); }

function drawParticleBarrel(cx,cy,ang,typ,pt,q,D,sc){
 const ctxEv=E.ctxEv;
 const R=radii(D,sc);
 // Krümmung ∝ q·B/p (Lorentzkraft): höheres pT → weniger Ablenkung
 // Faktor 22 statt 16 → stärkere Sichtbarkeit bei didaktischen pT-Werten
 const curv=q*(D.bend||0.6)*Math.min(0.75,22/Math.max(4,pt));
 if(typ==='bg'){
  // Untergrund: Spuren enden an TPC-/Tracker-Außenkante (nicht random gestutzt)
  const bgLen = s.isIon ? R.Rtrk : R.Rtrk*(0.85+Math.random()*0.3);
  drawTrack(cx,cy,ang,bgLen,curv,
    s.isIon?'rgba(227,119,194,0.38)':'rgba(120,140,170,0.38)',0.7); return; }
 if(typ==='mu'){
  // Myon: durchquert ALLE Lagen (MIP = minimal ionisierendes Teilchen)
  let p=drawTrack(cx,cy,ang,R.Rmu,curv,'#2ea44f',2.2); muonHit(p,ang);
  // Kleine Markierung zeigt B-Feld-Ablenkung
  const bx=cx+(R.Rtrk*1.1)*Math.cos(ang), by=cy+(R.Rtrk*1.1)*Math.sin(ang);
  ctxEv.save(); ctxEv.fillStyle='rgba(46,164,79,0.55)'; ctxEv.font='5.5px monospace';
  ctxEv.fillText('B↺',bx+3,by-2); ctxEv.restore(); }
 else if(typ==='e'){ drawTrack(cx,cy,ang,R.Rtrk,curv,'#58a6ff',2.0); emCluster(cx,cy,ang,R.Rtrk,R.Rem,'#58a6ff'); }
 else if(typ==='gamma'){ emCluster(cx,cy,ang,R.Rtrk,R.Rem,'#f1e05a'); }
 else if(typ==='had'){ drawTrack(cx,cy,ang,R.Rem,curv,'rgba(255,127,14,0.9)',1.4); hadShower(cx,cy,ang,R.Rem,R.Rhad); }
 else if(typ==='nu'){ metArrow(cx,cy,ang,R.Rtrk*1.6); }
}
function lhcbX(st){ const xs=s.evW-12; return 18+st/330*(xs-18); }
function drawParticleForward(vx,vy,slope,typ,pt,q,bg){
 const ctxEv=E.ctxEv;
 const xDip=lhcbX(160), xEm=lhcbX(250), xMu=lhcbX(315);
 const col = bg?'rgba(255,127,14,0.40)' : typ==='mu'?'#2ea44f':typ==='e'?'#58a6ff':typ==='gamma'?'#f1e05a':'rgba(255,127,14,0.9)';
 const yDip=vy+slope*(xDip-vx); const slope2=slope+q*Math.min(0.35,26/Math.max(4,pt))/100;
 if(typ==='gamma'){ const y=vy+slope*(xEm-vx); ctxEv.save(); ctxEv.globalAlpha=.6; ctxEv.fillStyle=col;
   ctxEv.fillRect(xEm-3,y-5,7,10); ctxEv.restore(); return; }
 const xEnd = typ==='mu'?xMu : xEm; const yEnd=yDip+slope2*(xEnd-xDip);
 ctxEv.strokeStyle=col; ctxEv.lineWidth=bg?0.8:2;
 ctxEv.beginPath(); ctxEv.moveTo(vx,vy); ctxEv.lineTo(xDip,yDip); ctxEv.lineTo(xEnd,yEnd); ctxEv.stroke();
 if(!bg && typ==='mu'){ ctxEv.fillStyle=col; ctxEv.beginPath(); ctxEv.arc(xMu,yEnd,2.3,0,2*Math.PI); ctxEv.fill(); }
 if(!bg && typ==='e'){ ctxEv.save(); ctxEv.globalAlpha=.6; ctxEv.fillStyle=col; ctxEv.fillRect(xEm-3,yEnd-5,7,10); ctxEv.restore(); }
}

// ── Detektor-Hintergrund (Zwiebelschalen) ───────────────────────────────────
// Liefert den kind-Wert zur infoKey eines Layers (für Ausgrau-Effekt).
function kindForKey(key){
 const D=DETKONFIG[s.selDet]||DETKONFIG.ATLAS;
 const src=(D.lagen||[]).concat(D.stationen||[]);
 const f=src.find(x=>x.infoKey===key); return f?f.kind:null;
}

// hl = optionale Liste hervorzuhebender Schicht-Arten (Signaturen-Tour oder
// Einzelschicht-Klick). Ohne hl: s.activeLayerKey bestimmt die Hervorhebung.
function drawBg(hl?){
 const ctxEv=E.ctxEv, evW=s.evW, evH=s.evH;
 const {D,cx,cy,Rmax,sc,lblX}=detGeo();
 ctxEv.clearRect(0,0,evW,evH); ctxEv.textAlign='left';
 ctxEv.strokeStyle="#2d3845"; ctxEv.lineWidth=1; ctxEv.strokeRect(0,0,evW,evH);
 ctxEv.fillStyle=D.farbe; ctxEv.font="bold 9px monospace"; ctxEv.fillText(s.selDet+" · "+(s.isIon?"Pb-Pb":"p-p"), 6, 12);
 // Rolle + Realgröße + Datenherkunft als HTML unter dem Canvas (nicht über die Spuren).
 const cap=document.getElementById('ev-caption');
 if(cap) cap.textContent = D.rolle + " · " + D.fakt + " · Daten: " + evProvenance();
 if(!hl && s.activeLayerKey){ const ak=kindForKey(s.activeLayerKey); if(ak) hl=[ak]; }
 const mode=(k)=> hl ? (hl.indexOf(k)>=0?'hi':'lo') : null;

 if(D.typ==='barrel'){
  // Gefüllte Schichten („Zwiebelschalen"): jedes Band = eine Materialschicht.
  let rIn=R_PIPE;
  D.lagen.forEach(l=>{ const Ro=l.r*sc, Ri=rIn*sc;
   ctxEv.fillStyle=kindFill(l.kind, mode(l.kind));
   ctxEv.beginPath(); ctxEv.arc(cx,cy,Ro,0,2*Math.PI); ctxEv.arc(cx,cy,Ri,0,2*Math.PI,true); ctxEv.fill();
   ctxEv.strokeStyle=layerColor(l.kind); ctxEv.lineWidth=(l.kind==='muon'||l.kind==='coil')?1.5:1;
   ctxEv.beginPath(); ctxEv.arc(cx,cy,Ro,0,2*Math.PI); ctxEv.stroke();
   rIn=l.r; });
  // Klartext-Spalte rechts: Name + Aufgabe je Schicht, Leader-Linie zum Band
  // (Zeilen von außen nach innen → Leader kreuzen sich nicht).
  const rows=[...D.lagen].sort((a,b)=>b.r-a.r), n=rows.length;
  const rowH=Math.min(26,(evH-36)/n); let rInM={}; let prev=R_PIPE;
  D.lagen.forEach(l=>{ rInM[l.name]=prev; prev=l.r; });
  ctxEv.save();
  rows.forEach((l,i)=>{ const y=cy+(i-(n-1)/2)*rowH, dim=hl && mode(l.kind)!=='hi';
   const Rmid=((rInM[l.name]+l.r)/2)*sc;
   const cdy=Math.max(-(Rmid-2), Math.min(Rmid-2, y-cy));
   const ax=cx+Math.sqrt(Math.max(0,Rmid*Rmid-cdy*cdy)), ay=cy+cdy;
   ctxEv.strokeStyle='rgba(139,148,158,'+(dim?0.2:0.45)+')'; ctxEv.lineWidth=0.8;
   ctxEv.beginPath(); ctxEv.moveTo(ax,ay); ctxEv.lineTo(lblX-5,y); ctxEv.stroke();
   ctxEv.fillStyle=layerColor(l.kind); ctxEv.beginPath(); ctxEv.arc(ax,ay,1.6,0,2*Math.PI); ctxEv.fill();
   ctxEv.globalAlpha=dim?0.35:1;
   ctxEv.fillStyle=KIND_TXT[l.kind]||'#cdd6e4'; ctxEv.font='bold 8px sans-serif';
   ctxEv.fillText(l.name, lblX, y-1.5);
   ctxEv.fillStyle='rgba(205,215,230,0.75)'; ctxEv.font='7px sans-serif';
   ctxEv.fillText(l.job, lblX, y+7);
   ctxEv.globalAlpha=1; });
  ctxEv.restore();
  // Kollisionspunkt + Maßstab: Meterleiste oben links, Mensch (1,8 m) am „Boden"
  ctxEv.fillStyle="#fff"; ctxEv.beginPath(); ctxEv.arc(cx,cy,1.6,0,2*Math.PI); ctxEv.fill();
  const Rmu=86*sc, pxm=Rmu/D.realRmu, fy=cy+Rmu;
  drawScaleBar(pxm, 5);
  ctxEv.strokeStyle='rgba(139,148,158,0.35)'; ctxEv.lineWidth=1;
  ctxEv.beginPath(); ctxEv.moveTo(cx-Rmu-18,fy); ctxEv.lineTo(cx,fy); ctxEv.stroke();
  drawHuman(cx-Rmu-9, fy, 1.8*pxm);
 } else {
  // LHCb: Stationen als gefüllte Platten + Flugrichtung; Mensch in Realgröße
  // (vertikaler Maßstab: Plattenhöhe ≈ 10 m Detektorhöhe).
  ctxEv.strokeStyle="rgba(255,127,14,0.30)"; ctxEv.lineWidth=1;
  ctxEv.beginPath(); ctxEv.moveTo(6,cy); ctxEv.lineTo(evW-10,cy); ctxEv.stroke();
  ctxEv.fillStyle="rgba(255,127,14,0.55)"; ctxEv.beginPath();
  ctxEv.moveTo(evW-10,cy); ctxEv.lineTo(evW-17,cy-3.5); ctxEv.lineTo(evW-17,cy+3.5); ctxEv.closePath(); ctxEv.fill();
  ctxEv.font='6.5px sans-serif'; ctxEv.fillStyle='rgba(205,215,230,0.7)'; ctxEv.textAlign='right';
  ctxEv.fillText('Teilchen fliegen →', evW-6, cy-7); ctxEv.textAlign='left';
  const yTop=28, yBot=evH-18;
  D.stationen.forEach(st=>{ const x=lhcbX(st.x), w=st.w||8;
   ctxEv.fillStyle=kindFill(st.kind, mode(st.kind));
   ctxEv.fillRect(x-w/2, yTop, w, yBot-yTop);
   ctxEv.strokeStyle=layerColor(st.kind); ctxEv.lineWidth=st.kind==='magnet'?2:1;
   ctxEv.strokeRect(x-w/2, yTop, w, yBot-yTop);
   ctxEv.save(); ctxEv.translate(x,26); ctxEv.rotate(-Math.PI/2);
   ctxEv.fillStyle="rgba(205,214,228,0.6)"; ctxEv.font="5.5px monospace"; ctxEv.fillText(st.name,0,2); ctxEv.restore(); });
  drawHuman(10, yBot, 1.8*(yBot-yTop)/10);
 }
 drawLegend();
}

// Öffentliches drawDetBg: beendet eine evtl. laufende Tour (externe Redraws —
// Detektorwechsel, Reset — sollen die App nie in einem Tour-Standbild lassen).
function drawDetBg(){ if(s.tourStep) evTourEnd(); else drawBg(); }

// ── Klickbare Schichten: Punkt (Canvas-Koordinaten) → INFO_DB-Schlüssel ─────
function evLayerHit(x,y){
 const {D,cx,cy,sc,lblX}=detGeo();
 if(D.typ==='barrel'){
  // Klick in die Klartext-Spalte trifft die Zeile, Klick ins Bild den Ring.
  if(lblX && x>=lblX-6){ const rows=[...D.lagen].sort((a,b)=>b.r-a.r), n=rows.length;
   const rowH=Math.min(26,(s.evH-36)/n), i=Math.round((y-cy)/rowH+(n-1)/2);
   return (i>=0 && i<n) ? rows[i].infoKey : null; }
  const d=Math.hypot(x-cx,y-cy);
  if(d<=R_PIPE*sc) return D.lagen[0].infoKey;   // Strahlrohr-Mitte → innerste Schicht
  let rIn=R_PIPE;
  for(const l of D.lagen){ if(d>rIn*sc && d<=l.r*sc+2) return l.infoKey; rIn=l.r; }
  return null;
 }
 for(const st of D.stationen){ const X=lhcbX(st.x);
  if(Math.abs(x-X)<=(st.w||8)/2+4 && y>20 && y<s.evH-10) return st.infoKey; }
 return null;
}

function drawTrack(x0,y0,ang,len,curv,color,lw){
  const ctxEv=E.ctxEv;
  let mx=x0+(len/2)*Math.cos(ang)+curv*Math.cos(ang+Math.PI/2)*(len/2);
  let my=y0+(len/2)*Math.sin(ang)+curv*Math.sin(ang+Math.PI/2)*(len/2);
  let tx=x0+len*Math.cos(ang)+curv*Math.cos(ang+Math.PI/2)*len;
  let ty=y0+len*Math.sin(ang)+curv*Math.sin(ang+Math.PI/2)*len;
  ctxEv.strokeStyle=color; ctxEv.lineWidth=lw;
  ctxEv.beginPath(); ctxEv.moveTo(x0,y0); ctxEv.quadraticCurveTo(mx,my,tx,ty); ctxEv.stroke();
  return [tx,ty];
}

// ── SIGNATUREN-TOUR: „Wie lese ich das Bild?" ───────────────────────────────
// Ein Teilchen pro Schritt, zugehörige Schicht(en) leuchten, Erklärtext unter
// dem Canvas. Schritt 6 = komplette Kollision. Gesteuert über s.tourStep (0=aus).
const TOUR=[
 {typ:'mu', name:'Myon (μ)', col:'#2ea44f', hl:['muon'],
  text:'Ein Myon, ein schwererer Verwandter des Elektrons, durchfliegt alle Schichten und wird als einziges Teilchen ganz außen in den Myonkammern registriert. Vier solche grünen Spuren auf einmal bilden den Goldkanal, mit dem 2012 das Higgs entdeckt wurde.'},
 {typ:'e', name:'Elektron (e⁻)', col:'#58a6ff', hl:['track','em'],
  text:'Das Elektron zieht erst eine vom Magnetfeld gekrümmte Spur durch den Spurdetektor und bleibt dann im EM-Kalorimeter stecken; der blaue Keil ist seine dort deponierte Energie.'},
 {typ:'gamma', name:'Photon (γ)', col:'#f1e05a', hl:['em'],
  text:'Das Photon ist elektrisch neutral und zieht deshalb keine Spur im Spurdetektor. Es erscheint erst als gelbes Energiebündel im EM-Kalorimeter. Dieses fehlende Spursignal ist sein Erkennungsmerkmal.'},
 {typ:'had', name:'Hadron (p, π, …)', col:'#ff7f0e', hl:['had'],
  text:'Hadronen (Protonen, Pionen …) fliegen durch das EM-Kalorimeter fast ungebremst hindurch und zerplatzen erst im Hadron-Kalorimeter zu einem orangen Teilchen-Schauer („Jet").'},
 {typ:'nu', name:'Neutrino (ν)', col:'#8b949e', hl:[],
  text:'Ein Neutrino durchquert den ganzen Detektor, und sogar die Erde, völlig spurlos. Verraten wird es nur durch die Bilanz: Auf einer Seite fehlt Impuls; der gestrichelte Pfeil zeigt, wohin er verschwand.'},
 {typ:'all', name:'Alles zusammen', col:'#f0f6fc', hl:null,
  text:'Eine komplette Kollision: viele Untergrund-Spuren und dazu die Signaturen von eben. Aus diesen Mustern lesen die Physiker ab, welches Teilchen für rund 10⁻²² Sekunden existiert hat. Ein Klick auf eine Schicht zeigt Foto und Details.'}
];
function evTourDraw(){
 const st=TOUR[s.tourStep-1]; if(!st) return;
 const {D,cx,cy,sc}=detGeo();
 if(st.typ==='all'){
  const keep=s.tourStep; s.tourStep=0;          // Bypass des Tour-Freeze
  drawCollisionEvent(s.lastEvent); s.tourStep=keep;
 } else {
  drawBg(st.hl);
  if(D.typ==='forward'){ if(st.typ==='nu'){} else drawParticleForward(lhcbX(34),cy,-0.07,st.typ,30,1,false); }
  else { const ang={mu:-1.0,e:-0.45,gamma:0.5,had:2.35,nu:3.9}[st.typ];
   drawParticleBarrel(cx,cy,ang,st.typ,st.typ==='mu'?45:24,1,D,sc); }
 }
 const cap=document.getElementById('ev-caption');
 if(cap) cap.innerHTML='<b style="color:'+st.col+'">Schritt '+s.tourStep+'/'+TOUR.length+' · '+st.name+':</b> '+st.text;
 if(E.btnEvTour) E.btnEvTour.textContent = s.tourStep<TOUR.length ? ('Weiter '+s.tourStep+'/'+TOUR.length) : 'Tour beenden';
}
function evTourAdvance(){
 const next=(s.tourStep||0)+1;
 if(next>TOUR.length){ evTourEnd(); return; }
 s.tourStep=next; evTourDraw();
}
function evTourEnd(){
 s.tourStep=0;
 if(E.btnEvTour) E.btnEvTour.textContent='Signaturen-Tour';
 s.lastEvent ? drawCollisionEvent(s.lastEvent) : drawBg();
}

// Physik-gekoppeltes Event-Display: zeichnet die zum gesampelten Event (ev)
// gehörende reale Zerfalls-Topologie – dasselbe Event landet im Histogramm.
function drawCollisionEvent(ev){
 if(s.tourStep) return;   // Tour-Standbild nicht von Live-Events übermalen
 const ctxEv=E.ctxEv, evW=s.evW, evH=s.evH;
 drawBg();
 const {D,cx,cy,Rmax,sc}=detGeo();
 const evd = s.goldenEvent || ev || s.lastEvent;

 if(D.typ==='forward'){
  const pvx=lhcbX(34), pvy=cy, svx=pvx+24, svy=cy+(Math.random()-.5)*8;
  let nbg=Math.round(11*Math.min(2,Math.max(.4,s.paramIntensity)));
  for(let i=0;i<nbg;i++) drawParticleForward(pvx,pvy,(Math.random()-.5)*0.55,'had',5+Math.random()*15,Math.random()<.5?1:-1,true);
  ctxEv.strokeStyle='rgba(255,255,255,0.55)'; ctxEv.lineWidth=1; ctxEv.beginPath(); ctxEv.moveTo(pvx,pvy); ctxEv.lineTo(svx,svy); ctxEv.stroke();
  ctxEv.fillStyle='#fff'; ctxEv.beginPath(); ctxEv.arc(pvx,pvy,2,0,7); ctxEv.fill();
  if(evd && evd.leptons){ evd.leptons.forEach((L,i)=>{
    drawParticleForward(svx,svy,((i?1:-1)*0.10)+(Math.random()-.5)*0.05, L.lep==='e'?'e':'mu', L.pt||10, L.q||(i?1:-1), false); });
   ctxEv.fillStyle='#f1e05a'; ctxEv.beginPath(); ctxEv.arc(svx,svy,2.3,0,7); ctxEv.fill();
   ctxEv.fillStyle='rgba(241,224,90,0.9)'; ctxEv.font='6px sans-serif'; ctxEv.fillText('Sek.-Vertex (B)', svx+4, svy-5); }
 } else {
  let nbg=Math.round((s.isIon?64:11)*Math.min(2.2,Math.max(.3,s.paramIntensity)));
  // Untergrundspuren aus ECHTER CMS-Off-Peak-μμ-Kinematik (topo.bg) statt Zufall.
  for(let i=0;i<nbg;i++){ const t=App.sampleBgTrack();
   drawParticleBarrel(cx,cy, t.phi!=null?t.phi:Math.random()*2*Math.PI,'bg', t.pt||(4+Math.random()*9), t.q||(Math.random()<.5?1:-1), D, sc); }
  if(!s.isIon){
   drawParticleBarrel(cx,cy,1.1+Math.random()*0.5,'gamma',20,0,D,sc);
   drawParticleBarrel(cx,cy,3.6+Math.random()*0.5,'had',26,1,D,sc);
   // MET-Pfeil: zeigt entgegen dem vektoriellen pT-Summe der Leptonen (Impulserhaltung)
   let metAng;
   if(evd && evd.leptons && evd.leptons.length){
    let sx=0,sy=0;
    evd.leptons.forEach(L=>{ const phi=L.phi!=null?L.phi:0; sx+=(L.pt||10)*Math.cos(phi); sy+=(L.pt||10)*Math.sin(phi); });
    metAng=Math.atan2(-sy,-sx); // entgegengesetzt = fehlende Energie
   } else { metAng=5.2+Math.random()*0.6; }
   drawParticleBarrel(cx,cy,metAng,'nu',0,0,D,sc);
  }
  if(evd && evd.leptons) evd.leptons.forEach(L=>{
   drawParticleBarrel(cx,cy, L.phi!=null?L.phi:Math.random()*2*Math.PI, L.lep==='e'?'e':'mu', L.pt||10, L.q||1, D, sc); });
 }

 // Kandidaten-Beschriftung (mit Hintergrund) – kohärent mit dem Histogramm-Peak.
 if(evd){
  let lbl = evd.name ? (evd.name+" → "+(evd.channel==="4l"?"ZZ*→4ℓ":"μ⁺μ⁻")+"  M="+App.de(+evd.M,1)+" GeV")
                     : ("Untergrund  M="+App.de(+evd.M,1)+" GeV");
  ctxEv.font="8px sans-serif"; ctxEv.textAlign='left';
  ctxEv.fillStyle='rgba(13,17,23,0.78)'; ctxEv.fillRect(4,evH-30,evW-8,12);
  ctxEv.fillStyle = evd.signal ? "#f0f6fc" : "rgba(240,246,252,0.6)";
  ctxEv.fillText(lbl, 8, evH-21);
 }
 if(s.goldenEvent){ ctxEv.fillStyle="#f1e05a"; ctxEv.font="8px sans-serif"; ctxEv.textAlign='right';
  ctxEv.fillText("GOLDEN", evW-6, 11); ctxEv.textAlign='left'; }
}

function setActiveLayer(key){
 s.activeLayerKey = key || null;
 if(!s.tourStep) drawBg();
}

App.drawDetBg = drawDetBg;
App.drawCollisionEvent = drawCollisionEvent;
App.evLayerHit = evLayerHit;
App.evTourAdvance = evTourAdvance;
App.evTourEnd = evTourEnd;
App.evTourDraw = evTourDraw;
App.setActiveLayer = setActiveLayer;
