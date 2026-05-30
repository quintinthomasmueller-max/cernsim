// ═══════════════════════════════════════════════════════════════════════════
// DETEKTOR-GEOMETRIE & TEILCHEN-SIGNATUREN  (didaktisches Event-Display)
// Lerninhalt: jede Teilchenart hinterlässt in den Detektorlagen eine andere Signatur.
// ═══════════════════════════════════════════════════════════════════════════
const DETKONFIG = {
 ATLAS: { typ:'barrel', farbe:'#58a6ff', rolle:'Allzweck · großes Toroid-Myon-System', bend:0.55,
   lagen:[ {r:26,name:'Spur',kind:'track'}, {r:38,name:'EM',kind:'em'},
           {r:52,name:'HAD',kind:'had'}, {r:62,name:'Toroid',kind:'coil'},
           {r:86,name:'μ-Kammer',kind:'muon'} ] },
 CMS: { typ:'barrel', farbe:'#f85149', rolle:'kompakt · 3.8 T Solenoid · Kristall-ECAL', bend:1.0,
   lagen:[ {r:30,name:'Tracker',kind:'track'}, {r:40,name:'ECAL',kind:'em'},
           {r:52,name:'HCAL',kind:'had'}, {r:60,name:'Solenoid',kind:'coil'},
           {r:86,name:'μ-Joch',kind:'muon'} ] },
 ALICE: { typ:'barrel', farbe:'#e377c2', rolle:'Schwerionen · TPC · hohe Multiplizität', bend:0.35,
   lagen:[ {r:14,name:'ITS',kind:'track'}, {r:58,name:'TPC',kind:'track'},
           {r:70,name:'TOF',kind:'em'}, {r:86,name:'Außen',kind:'muon'} ] },
 LHCB: { typ:'forward', farbe:'#ff7f0e', rolle:'Vorwärtsspektrometer · Sekundärvertex',
   stationen:[ {x:34,name:'VELO',kind:'vtx'}, {x:80,name:'RICH1',kind:'rich'}, {x:120,name:'TT',kind:'track'},
               {x:160,name:'Dipol',kind:'magnet'}, {x:210,name:'RICH2',kind:'rich'},
               {x:250,name:'ECAL',kind:'em'}, {x:285,name:'HCAL',kind:'had'}, {x:315,name:'Myon',kind:'muon'} ] }
};
function layerColor(k){ return ({track:'rgba(88,166,255,0.32)',em:'rgba(46,164,79,0.34)',had:'rgba(255,127,14,0.30)',
  coil:'rgba(139,148,158,0.42)',muon:'rgba(248,81,73,0.34)',vtx:'rgba(255,255,255,0.45)',rich:'rgba(88,166,255,0.18)',
  magnet:'rgba(241,224,90,0.5)'})[k] || 'rgba(139,148,158,0.25)'; }
function detGeo(){ const cx=evW/2, cy=evH/2, Rmax=Math.min(cx,cy)-6, D=DETKONFIG[selDet]||DETKONFIG.ATLAS; return {D,cx,cy,Rmax,sc:Rmax/86}; }
function rKind(D,kind,last){ let r=null; D.lagen.forEach(l=>{ if(l.kind===kind && (last||r===null)) r=l.r; }); return r; }
function radii(D,sc){ const trk=(rKind(D,'track',true)||30), em=(rKind(D,'em')||trk+10),
  had=(rKind(D,'had')||em+10), mu=(rKind(D,'muon')||had+20);
  return {Rtrk:trk*sc, Rem:em*sc, Rhad:had*sc, Rmu:mu*sc}; }

function drawLegend(){ const items=[['μ','#2ea44f'],['e','#58a6ff'],['γ','#f1e05a'],['Had','#ff7f0e'],['ν','#8b949e']];
 const gap=Math.min(30,(evW-14)/items.length), y=evH-5;
 ctxEv.save(); ctxEv.font='7px sans-serif'; ctxEv.textAlign='left';
 items.forEach((it,i)=>{ const x=8+i*gap;
  ctxEv.fillStyle=it[1]; ctxEv.beginPath(); ctxEv.arc(x+2,y-2,2.3,0,2*Math.PI); ctxEv.fill();
  ctxEv.fillStyle='rgba(225,230,238,0.92)'; ctxEv.fillText(it[0], x+7, y); });
 ctxEv.restore(); }

function emCluster(cx,cy,ang,r0,r1,col){ ctxEv.save(); ctxEv.globalAlpha=0.6; ctxEv.fillStyle=col; ctxEv.beginPath();
 ctxEv.moveTo(cx+r0*Math.cos(ang-0.14),cy+r0*Math.sin(ang-0.14));
 ctxEv.lineTo(cx+r1*Math.cos(ang-0.22),cy+r1*Math.sin(ang-0.22));
 ctxEv.lineTo(cx+r1*Math.cos(ang+0.22),cy+r1*Math.sin(ang+0.22));
 ctxEv.lineTo(cx+r0*Math.cos(ang+0.14),cy+r0*Math.sin(ang+0.14));
 ctxEv.closePath(); ctxEv.fill(); ctxEv.restore(); }
function hadShower(cx,cy,ang,r0,r1){ ctxEv.strokeStyle='rgba(255,127,14,0.85)'; ctxEv.lineWidth=1;
 for(let k=0;k<5;k++){ let a=ang+(Math.random()-.5)*0.55; ctxEv.beginPath();
  ctxEv.moveTo(cx+r0*Math.cos(ang),cy+r0*Math.sin(ang)); ctxEv.lineTo(cx+r1*Math.cos(a),cy+r1*Math.sin(a)); ctxEv.stroke(); } }
function muonHit(p,ang){ const px=Math.cos(ang+Math.PI/2), py=Math.sin(ang+Math.PI/2);
 ctxEv.strokeStyle='#2ea44f'; ctxEv.lineWidth=3; ctxEv.beginPath();
 ctxEv.moveTo(p[0]-4*px,p[1]-4*py); ctxEv.lineTo(p[0]+4*px,p[1]+4*py); ctxEv.stroke();
 ctxEv.fillStyle='#2ea44f'; ctxEv.beginPath(); ctxEv.arc(p[0],p[1],2.3,0,2*Math.PI); ctxEv.fill(); }
function metArrow(cx,cy,ang,len){ ctxEv.save(); ctxEv.setLineDash([4,3]); ctxEv.strokeStyle='#8b949e'; ctxEv.lineWidth=1.5;
 const tx=cx+len*Math.cos(ang), ty=cy+len*Math.sin(ang);
 ctxEv.beginPath(); ctxEv.moveTo(cx,cy); ctxEv.lineTo(tx,ty); ctxEv.stroke(); ctxEv.setLineDash([]);
 ctxEv.fillStyle='#8b949e'; ctxEv.beginPath(); ctxEv.moveTo(tx,ty);
 ctxEv.lineTo(tx-6*Math.cos(ang-0.4),ty-6*Math.sin(ang-0.4)); ctxEv.lineTo(tx-6*Math.cos(ang+0.4),ty-6*Math.sin(ang+0.4));
 ctxEv.closePath(); ctxEv.fill(); ctxEv.restore(); }

function drawParticleBarrel(cx,cy,ang,typ,pt,q,D,sc){
 const R=radii(D,sc); const curv=q*(D.bend||0.6)*Math.min(0.95,16/Math.max(4,pt));
 if(typ==='bg'){ drawTrack(cx,cy,ang,R.Rtrk*(0.7+Math.random()*0.5),curv,
    isIon?'rgba(227,119,194,0.42)':'rgba(120,140,170,0.40)',0.7); return; }
 if(typ==='mu'){ let p=drawTrack(cx,cy,ang,R.Rmu,curv,'#2ea44f',2.0); muonHit(p,ang); }
 else if(typ==='e'){ drawTrack(cx,cy,ang,R.Rtrk,curv,'#58a6ff',2.0); emCluster(cx,cy,ang,R.Rtrk,R.Rem,'#58a6ff'); }
 else if(typ==='gamma'){ emCluster(cx,cy,ang,R.Rtrk,R.Rem,'#f1e05a'); }
 else if(typ==='had'){ drawTrack(cx,cy,ang,R.Rem,curv,'rgba(255,127,14,0.9)',1.4); hadShower(cx,cy,ang,R.Rem,R.Rhad); }
 else if(typ==='nu'){ metArrow(cx,cy,ang,R.Rtrk*1.3); }
}
function lhcbX(st){ const xs=evW-12; return 18+st/330*(xs-18); }
function drawParticleForward(vx,vy,slope,typ,pt,q,bg){
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

function drawDetBg(){
 const {D,cx,cy,Rmax,sc}=detGeo();
 ctxEv.clearRect(0,0,evW,evH); ctxEv.textAlign='left';
 ctxEv.strokeStyle="#1a1f27"; ctxEv.lineWidth=1; ctxEv.strokeRect(0,0,evW,evH);
 ctxEv.fillStyle=D.farbe; ctxEv.font="9px monospace"; ctxEv.fillText(selDet+" | "+(isIon?"Pb-Pb":"p-p"), 6, 11);
 ctxEv.fillStyle="rgba(160,170,185,0.7)"; ctxEv.font="6px monospace"; ctxEv.fillText(D.rolle, 6, 20);
 if(D.typ==='barrel'){
  D.lagen.forEach(l=>{ const R=l.r*sc;
   ctxEv.strokeStyle=layerColor(l.kind); ctxEv.lineWidth=(l.kind==='muon'||l.kind==='coil')?1.5:1;
   ctxEv.beginPath(); ctxEv.arc(cx,cy,R,0,2*Math.PI); ctxEv.stroke();
   ctxEv.fillStyle="rgba(205,214,228,0.5)"; ctxEv.font="6px monospace";
   ctxEv.fillText(l.name, cx+(R-2)*Math.cos(-0.5)+1, cy+(R-2)*Math.sin(-0.5)); });
  ctxEv.fillStyle="#fff"; ctxEv.beginPath(); ctxEv.arc(cx,cy,1.6,0,2*Math.PI); ctxEv.fill();
 } else {
  ctxEv.strokeStyle="rgba(255,127,14,0.18)"; ctxEv.beginPath(); ctxEv.moveTo(0,cy); ctxEv.lineTo(evW,cy); ctxEv.stroke();
  D.stationen.forEach(st=>{ const x=lhcbX(st.x);
   ctxEv.strokeStyle=layerColor(st.kind); ctxEv.lineWidth=st.kind==='magnet'?3:1;
   ctxEv.beginPath(); ctxEv.moveTo(x,28); ctxEv.lineTo(x,evH-18); ctxEv.stroke();
   ctxEv.save(); ctxEv.translate(x,26); ctxEv.rotate(-Math.PI/2);
   ctxEv.fillStyle="rgba(205,214,228,0.6)"; ctxEv.font="5.5px monospace"; ctxEv.fillText(st.name,0,2); ctxEv.restore(); });
 }
 drawLegend();
}

function drawTrack(x0,y0,ang,len,curv,color,lw){
  let mx=x0+(len/2)*Math.cos(ang)+curv*Math.cos(ang+Math.PI/2)*(len/2);
  let my=y0+(len/2)*Math.sin(ang)+curv*Math.sin(ang+Math.PI/2)*(len/2);
  let tx=x0+len*Math.cos(ang)+curv*Math.cos(ang+Math.PI/2)*len;
  let ty=y0+len*Math.sin(ang)+curv*Math.sin(ang+Math.PI/2)*len;
  ctxEv.strokeStyle=color; ctxEv.lineWidth=lw;
  ctxEv.beginPath(); ctxEv.moveTo(x0,y0); ctxEv.quadraticCurveTo(mx,my,tx,ty); ctxEv.stroke();
  return [tx,ty];
}

// Physik-gekoppeltes Event-Display: zeichnet die zum gesampelten Event (ev)
// gehörende reale Zerfalls-Topologie – dasselbe Event landet im Histogramm.
function drawCollisionEvent(ev){
 drawDetBg();
 const {D,cx,cy,Rmax,sc}=detGeo();
 const evd = goldenEvent || ev || lastEvent;

 if(D.typ==='forward'){
  const pvx=lhcbX(34), pvy=cy, svx=pvx+24, svy=cy+(Math.random()-.5)*8;
  let nbg=Math.round(11*Math.min(2,Math.max(.4,paramIntensity)));
  for(let i=0;i<nbg;i++) drawParticleForward(pvx,pvy,(Math.random()-.5)*0.55,'had',5+Math.random()*15,Math.random()<.5?1:-1,true);
  ctxEv.strokeStyle='rgba(255,255,255,0.55)'; ctxEv.lineWidth=1; ctxEv.beginPath(); ctxEv.moveTo(pvx,pvy); ctxEv.lineTo(svx,svy); ctxEv.stroke();
  ctxEv.fillStyle='#fff'; ctxEv.beginPath(); ctxEv.arc(pvx,pvy,2,0,7); ctxEv.fill();
  if(evd && evd.leptons){ evd.leptons.forEach((L,i)=>{
    drawParticleForward(svx,svy,((i?1:-1)*0.10)+(Math.random()-.5)*0.05, L.lep==='e'?'e':'mu', L.pt||10, L.q||(i?1:-1), false); });
   ctxEv.fillStyle='#f1e05a'; ctxEv.beginPath(); ctxEv.arc(svx,svy,2.3,0,7); ctxEv.fill();
   ctxEv.fillStyle='rgba(241,224,90,0.9)'; ctxEv.font='6px sans-serif'; ctxEv.fillText('Sek.-Vertex (B)', svx+4, svy-5); }
 } else {
  let nbg=Math.round((isIon?64:11)*Math.min(2.2,Math.max(.3,paramIntensity)));
  for(let i=0;i<nbg;i++) drawParticleBarrel(cx,cy,Math.random()*2*Math.PI,'bg',4+Math.random()*9,Math.random()<.5?1:-1,D,sc);
  if(!isIon){ drawParticleBarrel(cx,cy,1.1+Math.random(),'gamma',20,0,D,sc);
              drawParticleBarrel(cx,cy,3.6+Math.random(),'had',26,1,D,sc);
              drawParticleBarrel(cx,cy,5.2+Math.random()*0.6,'nu',0,0,D,sc); }
  if(evd && evd.leptons) evd.leptons.forEach(L=>{
   drawParticleBarrel(cx,cy, L.phi!=null?L.phi:Math.random()*2*Math.PI, L.lep==='e'?'e':'mu', L.pt||10, L.q||1, D, sc); });
 }

 // Kandidaten-Beschriftung (mit Hintergrund) – kohärent mit dem Histogramm-Peak.
 if(evd){
  let lbl = evd.name ? (evd.name+" → "+(evd.channel==="4l"?"ZZ*→4ℓ":"μ⁺μ⁻")+"  M="+(+evd.M).toFixed(1)+" GeV")
                     : ("Untergrund  M="+(+evd.M).toFixed(1)+" GeV");
  ctxEv.font="8px sans-serif"; ctxEv.textAlign='left';
  ctxEv.fillStyle='rgba(13,17,23,0.78)'; ctxEv.fillRect(4,evH-30,evW-8,12);
  ctxEv.fillStyle = evd.signal ? "#f0f6fc" : "rgba(240,246,252,0.6)";
  ctxEv.fillText(lbl, 8, evH-21);
 }
 if(goldenEvent){ ctxEv.fillStyle="#f1e05a"; ctxEv.font="8px sans-serif"; ctxEv.textAlign='right';
  ctxEv.fillText("★ GOLDEN", evW-6, 11); ctxEv.textAlign='left'; }
}

