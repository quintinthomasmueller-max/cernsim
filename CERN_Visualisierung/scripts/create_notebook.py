# -*- coding: utf-8 -*-
"""
Generates the fully physics-coherent CERN accelerator complex notebook.
Key principle: the SAME particle bunch travels the entire chain from source to LHC.
The LHC fills up with multiple bunches before collision is possible.
All SVG paths connect at exact geometric junction points.
"""
import json, os

NB_PATH = "/Users/quintin/PhytonNotebook/CERN_Visualisierung/notebooks/CERN_Beschleuniger_Schaltzentrale.ipynb"
ROOT_PATH = "/Users/quintin/PhytonNotebook/CERN_Beschleuniger_Schaltzentrale.ipynb"

def md(lines):
    return {"cell_type":"markdown","metadata":{},"source":[l+"\n" for l in lines]}

def code(lines):
    return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[l+"\n" for l in lines]}

cells = []

# ── CELL 1: Introduction ─────────────────────────────────────────────────────
cells.append(md([
"# ⚛️ CERN Beschleuniger-Schaltzentrale",
"",
"## Physikalisch kohärente Teilchenstrahl-Simulation",
"",
"In dieser Simulation durchläuft **dasselbe Teilchenpaket (Bunch)** den gesamten realen Beschleunigerpfad des CERN:",
"",
"### 🔵 Protonenpfad",
"**Quelle** → **LINAC 4** ($160\\text{ MeV}$) → **PSB** ($2\\text{ GeV}$) → **PS** ($26\\text{ GeV}$) → **SPS** ($450\\text{ GeV}$) → **LHC** ($6.8\\text{ TeV}$)",
"",
"### 🟣 Blei-Ionen-Pfad",
"**Quelle** → **LINAC 3** ($4.2\\text{ MeV/u}$) → **LEIR** ($72\\text{ MeV/u}$) → **PS** ($5.9\\text{ GeV/u}$) → **SPS** ($177\\text{ GeV/u}$) → **LHC** ($2.56\\text{ TeV/u}$)",
"",
"### Ablauf",
"1. **Teilchenart wählen** (Protonen oder Blei-Ionen)",
"2. **Bunches injizieren**: Jeder Klick schickt ein Bunch durch die gesamte Kette. Du siehst den Punkt von der Quelle durch jeden Ring wandern.",
"3. **LHC auffüllen**: Der LHC braucht mindestens **5 Bunches pro Strahl** (Beam 1 im Uhrzeigersinn über TI 2, Beam 2 gegen den Uhrzeigersinn über TI 8).",
"4. **Energie rampen**: Alle LHC-Bunches beschleunigen synchron auf Kollisionsenergie.",
"5. **Kollidieren**: Erst wenn beide Strahlen gefüllt und auf Maximalenergie sind, können Kollisionen an den Detektoren (ATLAS, CMS, ALICE, LHCb) ausgelöst werden.",
]))

# ── CELL 2: Python Backend ───────────────────────────────────────────────────
cells.append(code([
"import numpy as np, matplotlib.pyplot as plt, sys, os",
"from IPython.display import display, HTML",
"sys.path.append(os.path.abspath('../scripts'))",
"try:",
"    import cern_utils as cu; print('✅ cern_utils geladen')",
"except: pass",
"print('⚙️ Physik-Engine bereit.')",
]))

# ── CELL 3: Instructions ─────────────────────────────────────────────────────
cells.append(md([
"## 🎛️ Stellwerk starten",
"Führe die nächste Zelle aus. Dann:",
"1. Wähle **Protonen** oder **Blei-Ionen**",
"2. Klicke **Inject Beam 1** – beobachte wie der Bunch von der Quelle durch alle Ringe zum LHC wandert",
"3. Wiederhole für **Beam 2** – der Bunch nimmt den anderen Transferweg (TI 8)",
"4. Fülle beide Strahlen auf (je ≥5 Bunches), dann **Ramp** und **Collide!**",
]))

# ── CELL 4: The Interactive Dashboard ─────────────────────────────────────────
# All SVG coordinates are computed so paths connect at exact junction points.
# Ring layout:
#   LHC: cx=350 cy=240 r=180   |  SPS: cx=400 cy=148 r=65
#   PS:  cx=242 cy=332 r=38    |  PSB: cx=142 cy=385 r=18
#   LEIR: cx=142 cy=275 r=18
# Junction angles computed via atan2 between ring centers.

html = r"""
<div id="cern-v4">
<style>
#cern-v4{background:#0d1117;color:#c9d1d9;font-family:-apple-system,'Segoe UI',Roboto,sans-serif;border-radius:16px;padding:20px;border:1px solid #30363d;max-width:1100px;margin:0 auto;user-select:none}
.cv4-hdr{display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #21262d;padding-bottom:10px;margin-bottom:14px}
.cv4-logo{font-size:20px;font-weight:800;color:#58a6ff;letter-spacing:1px}
.cv4-badge{background:rgba(88,166,255,.12);color:#58a6ff;font-size:10px;padding:3px 7px;border-radius:10px;border:1px solid rgba(88,166,255,.25);margin-left:8px}
.cv4-status{font-size:11px;color:#8b949e;display:flex;align-items:center;gap:6px}
.cv4-dot{width:8px;height:8px;border-radius:50%;background:#8b949e;display:inline-block}
.cv4-dot.on{background:#2ea44f;box-shadow:0 0 8px #2ea44f;animation:cv4p 1.5s infinite}
@keyframes cv4p{0%,100%{opacity:.6;transform:scale(.9)}50%{opacity:1;transform:scale(1.2)}}
.cv4-sel{display:flex;gap:6px;margin-bottom:14px}
.cv4-sel-tab{flex:1;padding:8px;font-size:13px;font-weight:700;text-align:center;border-radius:6px;cursor:pointer;border:1px solid #30363d;background:#161b22;transition:all .2s}
.cv4-sel-tab.act-p{background:rgba(88,166,255,.12);border-color:#58a6ff;color:#58a6ff}
.cv4-sel-tab.act-i{background:rgba(227,119,194,.12);border-color:#e377c2;color:#e377c2}
.cv4-grid{display:grid;grid-template-columns:1fr 310px;gap:20px}
@media(max-width:860px){.cv4-grid{grid-template-columns:1fr}}
.cv4-svg-wrap{background:#090d13;border-radius:12px;border:1px solid #21262d;height:500px;display:flex;align-items:center;justify-content:center;position:relative}
.cv4-panel{background:#161b22;border-radius:12px;border:1px solid #30363d;padding:14px;display:flex;flex-direction:column;gap:14px}
.cv4-ptitle{font-size:12px;text-transform:uppercase;letter-spacing:1px;color:#8b949e;border-bottom:1px solid #30363d;padding-bottom:6px;margin-bottom:6px}
.cv4-btn{background:#21262d;color:#c9d1d9;border:1px solid #30363d;padding:9px 14px;border-radius:6px;cursor:pointer;font-size:12px;font-weight:600;transition:all .2s;text-align:center}
.cv4-btn:hover{background:#30363d;border-color:#8b949e}
.cv4-btn.act{background:rgba(88,166,255,.15);border-color:#58a6ff;color:#58a6ff}
.cv4-btn.act-i{background:rgba(227,119,194,.15);border-color:#e377c2;color:#e377c2}
.cv4-btn.danger{background:rgba(248,81,73,.08);border-color:rgba(248,81,73,.4);color:#f85149}
.cv4-btn.danger:hover{background:rgba(248,81,73,.18);box-shadow:0 0 10px rgba(248,81,73,.25)}
.cv4-btn.off{opacity:.3;pointer-events:none}
.cv4-fill-row{display:flex;align-items:center;gap:8px;font-size:11px}
.cv4-fill-bar{flex:1;background:#21262d;border-radius:3px;height:8px;overflow:hidden}
.cv4-fill-bar-inner{height:100%;transition:width .3s;border-radius:3px}
.cv4-fill-bar-inner.b1{background:#58a6ff}
.cv4-fill-bar-inner.b2{background:#ff7f0e}
.cv4-fill-bar-inner.b1i{background:#e377c2}
.cv4-fill-bar-inner.b2i{background:#c77dff}
.cv4-rg{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.cv4-ro{background:#0d1117;border-radius:5px;border:1px solid #21262d;padding:7px 10px}
.cv4-ro-l{font-size:9px;color:#8b949e;text-transform:uppercase}
.cv4-ro-v{font-size:14px;font-weight:700;color:#f0f6fc;font-family:'Courier New',monospace}
.cv4-tracker{display:flex;align-items:center;gap:4px;font-size:10px;color:#8b949e;margin-top:4px}
.cv4-tracker .step{padding:2px 6px;border-radius:3px;border:1px solid #21262d;background:#0d1117}
.cv4-tracker .step.cur{border-color:#58a6ff;color:#58a6ff;background:rgba(88,166,255,.1)}
.cv4-tracker .step.cur-i{border-color:#e377c2;color:#e377c2;background:rgba(227,119,194,.1)}
.cv4-tracker .step.done{border-color:#2ea44f;color:#2ea44f}
.cv4-tracker .arr{color:#30363d}
.svg-path{stroke:#1a1f27;stroke-width:2.5;fill:none}
.svg-path.lit{stroke:#58a6ff;filter:drop-shadow(0 0 5px rgba(88,166,255,.6))}
.svg-path.lit-i{stroke:#e377c2;filter:drop-shadow(0 0 5px rgba(227,119,194,.6))}
.svg-path.lit-b2{stroke:#ff7f0e;filter:drop-shadow(0 0 5px rgba(255,127,14,.6))}
.svg-lhc{stroke:rgba(88,166,255,.08);stroke-width:3.5;fill:none}
.svg-lhc.lit{stroke:rgba(88,166,255,.3)}
.svg-lhc.lit-i{stroke:rgba(227,119,194,.3)}
.svg-node{fill:#0d1117;stroke:#21262d;stroke-width:2}
.svg-node.glow{stroke:#58a6ff;fill:rgba(88,166,255,.12);filter:drop-shadow(0 0 6px rgba(88,166,255,.4))}
.svg-node.glow-i{stroke:#e377c2;fill:rgba(227,119,194,.12);filter:drop-shadow(0 0 6px rgba(227,119,194,.4))}
.svg-node.flash{stroke:#f85149;fill:rgba(248,81,73,.2);filter:drop-shadow(0 0 8px rgba(248,81,73,.6))}
.svg-lbl{font-size:9px;fill:#8b949e;font-family:monospace;text-anchor:middle}
.cv4-bottom{margin-top:20px;display:grid;grid-template-columns:1fr 1fr;gap:16px}
.cv4-evcanvas{background:#090d13;border:1px solid #21262d;border-radius:8px;width:100%;height:180px}
.cv4-histwrap{background:#090d13;border:1px solid #21262d;border-radius:8px;height:130px;padding:6px}
.cv4-dtabs{display:flex;gap:3px;margin-bottom:6px}
.cv4-dtab{flex:1;background:#21262d;border:1px solid #30363d;padding:5px;font-size:10px;color:#8b949e;border-radius:4px;cursor:pointer;text-align:center;font-weight:700}
.cv4-dtab.act{background:rgba(88,166,255,.12);border-color:#58a6ff;color:#58a6ff}
</style>

<div class="cv4-hdr">
 <div><span class="cv4-logo">⚛️ CERN CCC</span><span class="cv4-badge">Schaltzentrale v4</span></div>
 <div class="cv4-status"><span class="cv4-dot" id="sdot"></span><span id="stxt">OFFLINE</span></div>
</div>

<div class="cv4-sel">
 <div class="cv4-sel-tab act-p" id="sel-p">🔵 Protonen (LINAC4 → PSB → PS → SPS → LHC)</div>
 <div class="cv4-sel-tab" id="sel-i">🟣 Blei-Ionen (LINAC3 → LEIR → PS → SPS → LHC)</div>
</div>

<div class="cv4-grid">
 <div class="cv4-svg-wrap">
  <svg id="svg" width="700" height="480" viewBox="0 0 700 480">
   <!-- Paths: all endpoints computed for exact geometric connection -->
   <!-- LINAC4: straight line ending at PSB left edge (124,385) -->
   <path id="p-linac4" d="M 30,385 L 124,385" class="svg-path"/>
   <!-- PSB ring cx=142 cy=385 r=18 -->
   <circle id="p-psb" cx="142" cy="385" r="18" class="svg-path"/>
   <!-- Transfer PSB→PS: starts at PSB exit angle toward PS, ends at PS entry -->
   <path id="p-psb-ps" d="M 157.7,376.2 Q 185,358 206.9,348.6" class="svg-path"/>

   <!-- LINAC3: straight line ending at LEIR left edge (124,275) -->
   <path id="p-linac3" d="M 30,275 L 124,275" class="svg-path"/>
   <!-- LEIR ring cx=142 cy=275 r=18 -->
   <circle id="p-leir" cx="142" cy="275" r="18" class="svg-path"/>
   <!-- Transfer LEIR→PS -->
   <path id="p-leir-ps" d="M 157.7,283.8 Q 185,300 206.9,311.4" class="svg-path"/>

   <!-- PS ring cx=242 cy=332 r=38 -->
   <circle id="p-ps" cx="242" cy="332" r="38" class="svg-path"/>
   <!-- Transfer PS→SPS -->
   <path id="p-ps-sps" d="M 265.2,301.6 Q 312,248 356.8,198.6" class="svg-path"/>

   <!-- SPS ring cx=400 cy=148 r=65 -->
   <circle id="p-sps" cx="400" cy="148" r="65" class="svg-path"/>

   <!-- TI 2: SPS → LHC near ALICE (left) -->
   <path id="p-ti2" d="M 339.5,173.7 Q 255,195 170,240" class="svg-path"/>
   <!-- TI 8: SPS → LHC near LHCb (right) -->
   <path id="p-ti8" d="M 453.4,187.1 Q 495,215 530,240" class="svg-path"/>

   <!-- LHC ring cx=350 cy=240 r=180 -->
   <circle id="p-lhc" cx="350" cy="240" r="180" class="svg-path svg-lhc"/>

   <!-- Nodes / Labels -->
   <circle id="n-linac4" cx="30" cy="385" r="5" class="svg-node"/>
   <text x="30" y="405" class="svg-lbl">LINAC 4</text>
   <circle id="n-psb" cx="142" cy="385" r="7" class="svg-node"/>
   <text x="142" y="415" class="svg-lbl">PSB</text>

   <circle id="n-linac3" cx="30" cy="275" r="5" class="svg-node"/>
   <text x="30" y="258" class="svg-lbl">LINAC 3</text>
   <circle id="n-leir" cx="142" cy="275" r="7" class="svg-node"/>
   <text x="142" y="256" class="svg-lbl">LEIR</text>

   <circle id="n-ps" cx="242" cy="332" r="8" class="svg-node"/>
   <text x="242" y="383" class="svg-lbl">PS</text>
   <circle id="n-sps" cx="400" cy="148" r="10" class="svg-node"/>
   <text x="400" y="230" class="svg-lbl">SPS</text>

   <!-- LHC Detector Nodes -->
   <circle id="d-atlas" cx="350" cy="420" r="14" class="svg-node"/>
   <text x="350" y="448" class="svg-lbl" style="fill:#e6edf3;font-weight:bold">ATLAS</text>
   <circle id="d-cms" cx="350" cy="60" r="14" class="svg-node"/>
   <text x="350" y="42" class="svg-lbl" style="fill:#e6edf3;font-weight:bold">CMS</text>
   <circle id="d-alice" cx="170" cy="240" r="12" class="svg-node"/>
   <text x="134" y="240" class="svg-lbl" style="fill:#e6edf3;font-weight:bold">ALICE</text>
   <circle id="d-lhcb" cx="530" cy="240" r="12" class="svg-node"/>
   <text x="567" y="240" class="svg-lbl" style="fill:#e6edf3;font-weight:bold">LHCb</text>

   <!-- TI labels -->
   <text x="248" y="186" class="svg-lbl" style="font-size:8px">TI 2</text>
   <text x="485" y="205" class="svg-lbl" style="font-size:8px">TI 8</text>
  </svg>
 </div>

 <div class="cv4-panel">
  <div>
   <div class="cv4-ptitle">📡 INJEKTION</div>
   <div style="display:flex;flex-direction:column;gap:6px">
    <button class="cv4-btn" id="btn-b1">📥 Inject Beam 1 (CW, via TI 2)</button>
    <button class="cv4-btn" id="btn-b2">📥 Inject Beam 2 (CCW, via TI 8)</button>
   </div>
   <div class="cv4-tracker" id="tracker">
    <span class="step" id="tr-src">Quelle</span><span class="arr">→</span>
    <span class="step" id="tr-inj">PSB</span><span class="arr">→</span>
    <span class="step" id="tr-ps">PS</span><span class="arr">→</span>
    <span class="step" id="tr-sps">SPS</span><span class="arr">→</span>
    <span class="step" id="tr-lhc">LHC</span>
   </div>
  </div>
  <div>
   <div class="cv4-ptitle">🔋 LHC FÜLLSTAND</div>
   <div class="cv4-fill-row"><span style="width:50px">B1 <span id="b1c">0</span>/5</span><div class="cv4-fill-bar"><div class="cv4-fill-bar-inner b1" id="b1bar" style="width:0%"></div></div></div>
   <div class="cv4-fill-row" style="margin-top:4px"><span style="width:50px">B2 <span id="b2c">0</span>/5</span><div class="cv4-fill-bar"><div class="cv4-fill-bar-inner b2" id="b2bar" style="width:0%"></div></div></div>
  </div>
  <div>
   <div class="cv4-ptitle">⚡ LHC BETRIEB</div>
   <div style="display:flex;flex-direction:column;gap:6px">
    <button class="cv4-btn off" id="btn-ramp">🚀 Energie-Ramping starten</button>
    <div class="cv4-fill-row"><span style="width:50px;font-size:10px">Ramp</span><div class="cv4-fill-bar"><div class="cv4-fill-bar-inner b1" id="rbar" style="width:0%"></div></div></div>
    <button class="cv4-btn danger off" id="btn-coll">💥 Strahlkollision auslösen!</button>
   </div>
  </div>
  <div>
   <div class="cv4-ptitle">📊 MESSWERTE</div>
   <div class="cv4-rg">
    <div class="cv4-ro"><span class="cv4-ro-l">Energie/Beam</span><span class="cv4-ro-v" id="v-e">0.00 TeV</span></div>
    <div class="cv4-ro"><span class="cv4-ro-l">Magnetfeld B</span><span class="cv4-ro-v" id="v-b">0.000 T</span></div>
    <div class="cv4-ro"><span class="cv4-ro-l">Lorentz γ</span><span class="cv4-ro-v" id="v-g">1</span></div>
    <div class="cv4-ro"><span class="cv4-ro-l">Teilchen</span><span class="cv4-ro-v" id="v-t" style="color:#58a6ff">Proton</span></div>
   </div>
  </div>
 </div>
</div>

<div class="cv4-bottom">
 <div>
  <div class="cv4-ptitle">📸 EVENT DISPLAY</div>
  <div class="cv4-dtabs">
   <div class="cv4-dtab act" id="dt-atlas">ATLAS</div>
   <div class="cv4-dtab" id="dt-cms">CMS</div>
   <div class="cv4-dtab" id="dt-alice">ALICE</div>
   <div class="cv4-dtab" id="dt-lhcb">LHCb</div>
  </div>
  <canvas class="cv4-evcanvas" id="cv-ev"></canvas>
 </div>
 <div>
  <div class="cv4-ptitle">📊 MASSENSPEKTRUM <span id="sp-info" style="float:right;font-size:10px;color:#58a6ff">Kollisionen: 0</span></div>
  <div class="cv4-histwrap"><canvas id="cv-hist" style="width:100%;height:100%"></canvas></div>
 </div>
</div>
</div>

<script>
(function(){
const SVG_NS="http://www.w3.org/2000/svg";
const svg=document.getElementById("svg");

// ═══════════════════════════════════════════════════════════════════════════
// GEOMETRY CONFIG — all computed so path endpoints match ring entry/exit pts
// ═══════════════════════════════════════════════════════════════════════════
const R={
 PSB:{cx:142,cy:385,r:18}, LEIR:{cx:142,cy:275,r:18},
 PS:{cx:242,cy:332,r:38}, SPS:{cx:400,cy:148,r:65},
 LHC:{cx:350,cy:240,r:180}
};
// Junction angles (radians, SVG coords: 0=right, positive=CW/downward)
const J={
 PSB_ENTRY: Math.PI,    // from LINAC (left side)
 PSB_EXIT: Math.atan2(R.PS.cy-R.PSB.cy, R.PS.cx-R.PSB.cx),     // toward PS ≈-0.51
 LEIR_ENTRY: Math.PI,
 LEIR_EXIT: Math.atan2(R.PS.cy-R.LEIR.cy, R.PS.cx-R.LEIR.cx),  // toward PS ≈0.51
 PS_FROM_PSB: Math.atan2(R.PSB.cy-R.PS.cy, R.PSB.cx-R.PS.cx),   // from PSB ≈2.63
 PS_FROM_LEIR: Math.atan2(R.LEIR.cy-R.PS.cy, R.LEIR.cx-R.PS.cx),// from LEIR ≈-2.63→3.65
 PS_EXIT: Math.atan2(R.SPS.cy-R.PS.cy, R.SPS.cx-R.PS.cx),       // toward SPS ≈-0.84
 SPS_ENTRY: Math.atan2(R.PS.cy-R.SPS.cy, R.PS.cx-R.SPS.cx),     // from PS ≈2.30
 SPS_TI2: Math.atan2(240-R.SPS.cy, 170-R.SPS.cx),                // toward ALICE ≈2.77
 SPS_TI8: Math.atan2(240-R.SPS.cy, 530-R.SPS.cx),                // toward LHCb ≈0.61
 LHC_ALICE: Math.PI,   // ALICE at 180° (left)
 LHC_LHCB: 0           // LHCb at 0° (right)
};

// ═══════════════════════════════════════════════════════════════════════════
// STATE
// ═══════════════════════════════════════════════════════════════════════════
let isIon=false, injecting=false, ramped=false;
let b1Count=0, b2Count=0, collisions=0;
const NEEDED=5;
let lhcDots={b1:[],b2:[]};
let lhcSpeed=0.0015; // rad/ms at injection energy
let lhcAngle=0, lhcRunning=false, lhcLastT=null;
let lhcEnergy=450; // GeV
let massData=[];
let selDet="ATLAS";

// ═══════════════════════════════════════════════════════════════════════════
// DOM REFERENCES
// ═══════════════════════════════════════════════════════════════════════════
const $=id=>document.getElementById(id);
const sdot=$("sdot"),stxt=$("stxt");
const btnB1=$("btn-b1"),btnB2=$("btn-b2"),btnRamp=$("btn-ramp"),btnColl=$("btn-coll");
const b1c=$("b1c"),b2c=$("b2c"),b1bar=$("b1bar"),b2bar=$("b2bar"),rbar=$("rbar");
const vE=$("v-e"),vB=$("v-b"),vG=$("v-g"),vT=$("v-t");
const spInfo=$("sp-info");
const trSteps=["tr-src","tr-inj","tr-ps","tr-sps","tr-lhc"].map($);
const trInj=$("tr-inj");
const selP=$("sel-p"),selI=$("sel-i");

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

// Canvas
const cvEv=$("cv-ev"), ctxEv=cvEv.getContext("2d");
const cvHist=$("cv-hist"), ctxHist=cvHist.getContext("2d");

// Detector tabs
["atlas","cms","alice","lhcb"].forEach(d=>{
 $("dt-"+d).addEventListener("click",()=>{
  document.querySelectorAll(".cv4-dtab").forEach(t=>t.classList.remove("act"));
  $("dt-"+d).classList.add("act");
  selDet=d.toUpperCase();
  drawDetBg();
 });
});

// ═══════════════════════════════════════════════════════════════════════════
// HADRON SELECTION
// ═══════════════════════════════════════════════════════════════════════════
selP.addEventListener("click",()=>{ if(injecting)return; setMode(false); });
selI.addEventListener("click",()=>{ if(injecting)return; setMode(true); });

function setMode(ion){
 if(isIon===ion && b1Count===0 && b2Count===0) return;
 isIon=ion;
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
 lhcDots.b1.forEach(d=>d.el.remove()); lhcDots.b2.forEach(d=>d.el.remove());
 lhcDots={b1:[],b2:[]}; b1Count=0; b2Count=0; collisions=0; massData=[];
 ramped=false; lhcEnergy=isIon?177:450; lhcSpeed=0.0015;
 b1c.innerText="0"; b2c.innerText="0"; b1bar.style.width="0%"; b2bar.style.width="0%";
 rbar.style.width="0%"; spInfo.innerText="Kollisionen: 0";
 btnRamp.classList.add("off"); btnColl.classList.add("off");
 updateReadouts();
 // Clear path glows
 Object.values(paths).forEach(p=>{p.classList.remove("lit","lit-i","lit-b2")});
 Object.values(nodes).forEach(n=>{n.classList.remove("glow","glow-i","flash")});
 paths.lhc.classList.remove("lit","lit-i");
 setStatus("BEREIT","on");
}

// ═══════════════════════════════════════════════════════════════════════════
// ANIMATION PRIMITIVES
// ═══════════════════════════════════════════════════════════════════════════
function moveAlongPath(dot, pathEl, dur){
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

function orbitRing(dot, ring, entryA, exitA, orbits, dur){
 // Clockwise orbit (angle increases) from entryA to exitA + orbits full turns
 let partial=((exitA-entryA)%(2*Math.PI)+2*Math.PI)%(2*Math.PI);
 let totalA=orbits*2*Math.PI+partial;
 return new Promise(res=>{
  let t0=null;
  function step(ts){
   if(!t0) t0=ts;
   let p=Math.min((ts-t0)/dur,1);
   // Ease: start slow, accelerate (simulating energy ramp in ring)
   let ep=p*p*(3-2*p); // smoothstep
   let a=entryA+ep*totalA;
   dot.setAttribute("cx",ring.cx+ring.r*Math.cos(a));
   dot.setAttribute("cy",ring.cy+ring.r*Math.sin(a));
   p<1 ? requestAnimationFrame(step) : res();
  }
  requestAnimationFrame(step);
 });
}

// ═══════════════════════════════════════════════════════════════════════════
// INJECTION CYCLE — the core physical simulation
// A single bunch traverses: Source → LINAC → Ring1 → PS → SPS → TI → LHC
// ═══════════════════════════════════════════════════════════════════════════
async function injectBunch(beam){
 if(injecting) return;
 injecting=true;
 btnB1.classList.add("off"); btnB2.classList.add("off");

 const ion=isIon;
 const litCls=ion?"lit-i":"lit";
 const glowCls=ion?"glow-i":"glow";
 const dotColor=ion?"#e377c2":"#58a6ff";
 const dotColorB2=ion?"#c77dff":"#ff7f0e";
 const color=beam===1?dotColor:dotColorB2;

 // Create the bunch dot
 const dot=document.createElementNS(SVG_NS,"circle");
 dot.setAttribute("r","4");
 dot.setAttribute("fill",color);
 dot.style.filter="drop-shadow(0 0 4px "+color+")";
 svg.appendChild(dot);

 // Helper to light/unlight paths and track progress
 function lightPath(el){el.classList.add(litCls)}
 function lightNode(el){el.classList.add(glowCls)}
 function dimPath(el){el.classList.remove(litCls,"lit","lit-i","lit-b2")}
 function dimNode(el){el.classList.remove(glowCls,"glow","glow-i")}
 function setTracker(idx){
  trSteps.forEach((s,i)=>{
   s.classList.remove("cur","cur-i","done");
   if(i<idx) s.classList.add("done");
   else if(i===idx) s.classList.add(ion?"cur-i":"cur");
  });
 }

 // ── Phase 1: Source → LINAC ──
 setTracker(0);
 const linacPath=ion?paths.linac3:paths.linac4;
 const linacNode=ion?nodes.linac3:nodes.linac4;
 lightNode(linacNode); lightPath(linacPath);
 setStatus(ion?"LINAC 3 FEUERT":"LINAC 4 FEUERT","on");
 await moveAlongPath(dot, linacPath, 800);
 dimNode(linacNode);

 // ── Phase 2: Orbit in PSB/LEIR ──
 setTracker(1);
 const ring1=ion?R.LEIR:R.PSB;
 const ring1Path=ion?paths.leir:paths.psb;
 const ring1Node=ion?nodes.leir:nodes.psb;
 const ring1Entry=ion?J.LEIR_ENTRY:J.PSB_ENTRY;
 const ring1Exit=ion?J.LEIR_EXIT:J.PSB_EXIT;
 lightPath(ring1Path); lightNode(ring1Node);
 setStatus(ion?"LEIR: Beschleunigung auf 72 MeV/u":"PSB: Beschleunigung auf 2 GeV","on");
 await orbitRing(dot, ring1, ring1Entry, ring1Exit, 3, 1800);
 dimPath(ring1Path); dimPath(linacPath);

 // ── Phase 3: Transfer to PS ──
 const trToPs=ion?paths.leirPs:paths.psbPs;
 lightPath(trToPs);
 await moveAlongPath(dot, trToPs, 400);
 dimPath(trToPs); dimNode(ring1Node);

 // ── Phase 4: Orbit in PS ──
 setTracker(2);
 const psEntry=ion?J.PS_FROM_LEIR:J.PS_FROM_PSB;
 lightPath(paths.ps); lightNode(nodes.ps);
 setStatus(ion?"PS: Beschleunigung auf 5.9 GeV/u":"PS: Beschleunigung auf 26 GeV","on");
 await orbitRing(dot, R.PS, psEntry, J.PS_EXIT, 3, 2000);
 dimPath(paths.ps);

 // ── Phase 5: Transfer to SPS ──
 lightPath(paths.psSps);
 await moveAlongPath(dot, paths.psSps, 500);
 dimPath(paths.psSps); dimNode(nodes.ps);

 // ── Phase 6: Orbit in SPS ──
 setTracker(3);
 lightPath(paths.sps); lightNode(nodes.sps);
 const spsExit=beam===1?J.SPS_TI2:J.SPS_TI8;
 setStatus(ion?"SPS: Beschleunigung auf 177 GeV/u":"SPS: Beschleunigung auf 450 GeV","on");
 await orbitRing(dot, R.SPS, J.SPS_ENTRY, spsExit, 2, 1800);
 dimPath(paths.sps);

 // ── Phase 7: Transfer via TI2 or TI8 to LHC ──
 const tiPath=beam===1?paths.ti2:paths.ti8;
 lightPath(tiPath);
 setStatus(beam===1?"Transfer via TI 2 zum LHC":"Transfer via TI 8 zum LHC","on");
 await moveAlongPath(dot, tiPath, 600);
 dimPath(tiPath); dimNode(nodes.sps);

 // ── Phase 8: Bunch arrives in LHC — becomes permanent ──
 setTracker(4);
 dot.remove(); // remove the traveling dot, create persistent one
 addPermanentDot(beam);

 if(beam===1){ b1Count++; b1c.innerText=b1Count; b1bar.style.width=(b1Count/NEEDED*100)+"%"; }
 else { b2Count++; b2c.innerText=b2Count; b2bar.style.width=(b2Count/NEEDED*100)+"%"; }

 paths.lhc.classList.add(ion?"lit-i":"lit");

 // Check if ready for ramping
 if(b1Count>=NEEDED && b2Count>=NEEDED && !ramped){
  btnRamp.classList.remove("off");
  setStatus("LHC GEFÜLLT — Ramping möglich!","on");
 } else {
  setStatus("LHC B1:"+b1Count+"/"+NEEDED+" B2:"+b2Count+"/"+NEEDED,"on");
 }

 injecting=false;
 btnB1.classList.remove("off"); btnB2.classList.remove("off");
 // Reset tracker
 trSteps.forEach(s=>s.classList.remove("cur","cur-i","done"));
}

// ═══════════════════════════════════════════════════════════════════════════
// LHC PERSISTENT ORBIT SYSTEM
// ═══════════════════════════════════════════════════════════════════════════
function addPermanentDot(beam){
 const key=beam===1?"b1":"b2";
 const existing=lhcDots[key].length;
 const angleOffset=existing*(2*Math.PI/12); // space up to 12 bunches evenly

 const dot=document.createElementNS(SVG_NS,"circle");
 dot.setAttribute("r","3.5");
 let c;
 if(beam===1) c=isIon?"#e377c2":"#58a6ff";
 else c=isIon?"#c77dff":"#ff7f0e";
 dot.setAttribute("fill",c);
 dot.style.filter="drop-shadow(0 0 3px "+c+")";
 svg.appendChild(dot);

 lhcDots[key].push({el:dot,off:angleOffset});
 if(!lhcRunning) startLHCLoop();
}

function startLHCLoop(){
 lhcRunning=true; lhcLastT=null;
 function frame(ts){
  if(!lhcLastT) lhcLastT=ts;
  let dt=ts-lhcLastT; lhcLastT=ts;
  lhcAngle+=lhcSpeed*dt;

  lhcDots.b1.forEach(d=>{
   let a=lhcAngle+d.off;
   d.el.setAttribute("cx",R.LHC.cx+R.LHC.r*Math.cos(a));
   d.el.setAttribute("cy",R.LHC.cy+R.LHC.r*Math.sin(a));
  });
  lhcDots.b2.forEach(d=>{
   let a=-lhcAngle+d.off; // counter-clockwise
   d.el.setAttribute("cx",R.LHC.cx+R.LHC.r*Math.cos(a));
   d.el.setAttribute("cy",R.LHC.cy+R.LHC.r*Math.sin(a));
  });
  if(lhcRunning) requestAnimationFrame(frame);
 }
 requestAnimationFrame(frame);
}

// ═══════════════════════════════════════════════════════════════════════════
// LHC RAMPING
// ═══════════════════════════════════════════════════════════════════════════
btnRamp.addEventListener("click",async()=>{
 if(ramped||injecting) return;
 btnRamp.classList.add("off"); btnB1.classList.add("off"); btnB2.classList.add("off");
 setStatus("RAMPING ENERGY...","on");

 const startE=isIon?177:450;
 const targetE=isIon?2560:6800;
 const startSpeed=0.0015;
 const targetSpeed=0.007;
 const dur=4000;
 let t0=null;

 await new Promise(res=>{
  function step(ts){
   if(!t0) t0=ts;
   let p=Math.min((ts-t0)/dur,1);
   lhcEnergy=startE+p*(targetE-startE);
   lhcSpeed=startSpeed+p*(targetSpeed-startSpeed);
   rbar.style.width=(p*100)+"%";
   updateReadouts();
   p<1 ? requestAnimationFrame(step) : res();
  }
  requestAnimationFrame(step);
 });

 ramped=true;
 // Light up detector nodes
 [nodes.atlas,nodes.cms,nodes.alice,nodes.lhcb].forEach(n=>n.classList.add("glow"));
 btnColl.classList.remove("off");
 setStatus("STABLE BEAMS — "+(lhcEnergy/1000).toFixed(2)+" TeV"+(isIon?"/u":""),"on");
});

// ═══════════════════════════════════════════════════════════════════════════
// COLLISION
// ═══════════════════════════════════════════════════════════════════════════
btnColl.addEventListener("click",()=>{
 if(!ramped) return;
 collisions+=isIon?2:5;
 spInfo.innerText="Kollisionen: "+collisions;

 // Flash selected detector
 let detNode=nodes[selDet.toLowerCase()];
 if(detNode){detNode.classList.add("flash");setTimeout(()=>detNode.classList.remove("flash"),350);}

 drawCollisionEvent();
 generateMassData();
 drawHist();
});

// ═══════════════════════════════════════════════════════════════════════════
// READOUTS
// ═══════════════════════════════════════════════════════════════════════════
function updateReadouts(){
 vE.innerText=(lhcEnergy/1000).toFixed(2)+" TeV"+(isIon?"/u":"");
 let B=lhcEnergy/(0.299792458*2803.95);
 vB.innerText=B.toFixed(3)+" T";
 let g=lhcEnergy/(isIon?193.7:0.938272);
 vG.innerText=Math.round(g).toLocaleString("de-DE");
}

function setStatus(txt,cls){stxt.innerText=txt;sdot.className="cv4-dot "+cls;}

// ═══════════════════════════════════════════════════════════════════════════
// EVENT DISPLAY CANVAS
// ═══════════════════════════════════════════════════════════════════════════
function drawDetBg(){
 let w=cvEv.width,h=cvEv.height,cx=w/2,cy=h/2;
 ctxEv.clearRect(0,0,w,h);
 ctxEv.strokeStyle="#1a1f27";ctxEv.lineWidth=1;
 [18,42,66,88].forEach(r=>{ctxEv.beginPath();ctxEv.arc(cx,cy,r,0,2*Math.PI);ctxEv.stroke();});
 ctxEv.fillStyle="#8b949e";ctxEv.font="9px monospace";
 ctxEv.fillText(selDet+" | "+(isIon?"Pb-Pb":"p-p"),8,16);
}

function drawCollisionEvent(){
 drawDetBg();
 let w=cvEv.width,h=cvEv.height,cx=w/2,cy=h/2;
 let nTracks=isIon?100:14;
 for(let i=0;i<nTracks;i++){
  let a=Math.random()*2*Math.PI;
  let len=isIon?(25+Math.random()*45):(35+Math.random()*55);
  let curve=a+(Math.random()>.5?.18:-.18);
  let tx=cx+len*Math.cos(a),ty=cy+len*Math.sin(a);
  let cpx=cx+(len/2)*Math.cos(curve),cpy=cy+(len/2)*Math.sin(curve);
  ctxEv.beginPath();ctxEv.moveTo(cx,cy);ctxEv.quadraticCurveTo(cpx,cpy,tx,ty);
  if(isIon){
   ctxEv.strokeStyle="rgba(227,119,194,0.4)";ctxEv.lineWidth=.8;ctxEv.stroke();
  }else{
   let mu=Math.random()>.75;
   ctxEv.strokeStyle=mu?"#2ea44f":(Math.random()>.5?"#58a6ff":"#ff7f0e");
   ctxEv.lineWidth=mu?1.8:1;ctxEv.stroke();
   if(mu){ctxEv.fillStyle="#2ea44f";ctxEv.beginPath();ctxEv.arc(cx+88*Math.cos(a),cy+88*Math.sin(a),3,0,2*Math.PI);ctxEv.fill();}
  }
 }
}

// ═══════════════════════════════════════════════════════════════════════════
// HISTOGRAM
// ═══════════════════════════════════════════════════════════════════════════
function generateMassData(){
 if(!isIon){
  for(let i=0;i<35;i++){let m=50+Math.exp(Math.random()*4.6)*1.5;if(m>50&&m<150)massData.push(m);}
  for(let i=0;i<14;i++) massData.push(91.2+(Math.random()-.5)*4+(Math.random()-.5)*2);
  for(let i=0;i<4;i++){let m=125+(Math.random()-.5)*2.8+(Math.random()-.5)*1.2;if(m>50&&m<150)massData.push(m);}
 }else{
  for(let i=0;i<45;i++) massData.push(1+Math.random()*11);
  for(let i=0;i<20;i++) massData.push(3.1+(Math.random()-.5)*.4+(Math.random()-.5)*.2);
  for(let i=0;i<7;i++) massData.push(9.46+(Math.random()-.5)*.6+(Math.random()-.5)*.3);
 }
}

function drawHist(){
 let w=cvHist.width,h=cvHist.height;
 ctxHist.clearRect(0,0,w,h);
 ctxHist.strokeStyle="#30363d";ctxHist.lineWidth=1;
 ctxHist.beginPath();ctxHist.moveTo(30,8);ctxHist.lineTo(30,h-16);ctxHist.lineTo(w-8,h-16);ctxHist.stroke();
 ctxHist.fillStyle="#8b949e";ctxHist.font="7.5px sans-serif";
 let mn=isIon?1:50, mx=isIon?12:150;
 ctxHist.fillText(mn+" GeV",30,h-5);ctxHist.fillText(mx+" GeV",w-40,h-5);
 if(!massData.length){ctxHist.fillStyle="#8b949e";ctxHist.font="10px monospace";ctxHist.fillText("WARTEN AUF KOLLISIONSDATEN...",w/2-90,h/2);return;}
 let nb=40,bins=Array(nb).fill(0);
 massData.forEach(v=>{if(v>=mn&&v<mx){let i=Math.floor((v-mn)/(mx-mn)*nb);if(i>=0&&i<nb)bins[i]++;}});
 let maxB=Math.max(...bins,1),bw=(w-40)/nb;
 let fc=isIon?"rgba(227,119,194,0.4)":"rgba(88,166,255,0.4)";
 let tc=isIon?"#e377c2":"#58a6ff";
 for(let i=0;i<nb;i++){let bh=bins[i]/maxB*(h-30);let x=30+i*bw,y=h-16-bh;
  ctxHist.fillStyle=fc;ctxHist.fillRect(x,y,bw-1,bh);ctxHist.fillStyle=tc;ctxHist.fillRect(x,y,bw-1,1.5);}
 if(collisions>4){
  ctxHist.strokeStyle="rgba(248,81,73,.6)";ctxHist.lineWidth=1.2;ctxHist.beginPath();
  for(let xp=30;xp<w-8;xp++){
   let v=mn+(xp-30)/(w-38)*(mx-mn),yv=0;
   if(!isIon){yv=Math.exp(-(v-50)/25)*18+(1/((v-91.2)**2+2.5**2))*300+(1/((v-125)**2+1.6**2))*10;}
   else{yv=4.2+(1/((v-3.1)**2+.15**2))*1.4+(1/((v-9.46)**2+.3**2))*.35;}
   let sc=isIon?6.5:20,yp=h-16-yv/sc*(h-35);yp=Math.max(8,Math.min(h-16,yp));
   xp===30?ctxHist.moveTo(xp,yp):ctxHist.lineTo(xp,yp);
  }ctxHist.stroke();
  ctxHist.fillStyle="#f0f6fc";ctxHist.font="8px sans-serif";
  if(!isIon){ctxHist.fillText("Z⁰ (91 GeV)",w*.42,22);ctxHist.fillText("Higgs (125 GeV)",w*.7,38);}
  else{ctxHist.fillText("J/Ψ (3.1 GeV)",w*.2,20);ctxHist.fillText("Υ (9.46 GeV)",w*.72,45);}
 }
}

// ═══════════════════════════════════════════════════════════════════════════
// BUTTON HANDLERS
// ═══════════════════════════════════════════════════════════════════════════
btnB1.addEventListener("click",()=>injectBunch(1));
btnB2.addEventListener("click",()=>injectBunch(2));

// ═══════════════════════════════════════════════════════════════════════════
// INIT
// ═══════════════════════════════════════════════════════════════════════════
updateReadouts(); drawDetBg(); drawHist();
setStatus("BEREIT — Wähle Teilchenart und starte Injektion","on");

})();
</script>
"""

cells.append(code([
    "display(HTML(r'''" + html.replace("'''","\\'\\'\\'") + "'''))"
]))

# ── CELL 5: Analysis intro ───────────────────────────────────────────────────
cells.append(md([
"## 📈 Post-Kollisions-Analyse",
"",
"Nach zahlreichen Kollisionen analysieren wir das akkumulierte Massenspektrum.",
"Setze `heavy_ion_analysis = True` für Blei-Ionen (J/ψ, Υ) oder `False` für Protonen (Higgs, Z0).",
]))

# ── CELL 6: Scientific fitting ───────────────────────────────────────────────
cells.append(code([
"import numpy as np, matplotlib.pyplot as plt",
"from scipy.optimize import curve_fit",
"",
"heavy_ion_analysis = False  # True für Pb-Pb, False für p-p",
"",
"try: cu.apply_cern_style()",
"except: plt.style.use('dark_background')",
"fig, ax = plt.subplots(figsize=(12, 7))",
"",
"if not heavy_ion_analysis:",
"    np.random.seed(42)",
"    bg=np.random.exponential(35,14000)+50; bg=bg[bg<160]",
"    zs=np.random.normal(91.18,2.8,5600); zs=zs[(zs>=50)&(zs<=160)]",
"    hs=np.random.normal(125,1.8,400); hs=hs[(hs>=50)&(hs<=160)]",
"    data=np.concatenate([bg,zs,hs])",
"    h,e=np.histogram(data,bins=80,range=(50,160)); c=.5*(e[1:]+e[:-1])",
"    def model(x,a,l,az,mz,gz,ah,mh,sh):",
"        return a*np.exp(-(x-50)/l)+az*(gz/2)**2/((x-mz)**2+(gz/2)**2)+ah*np.exp(-.5*((x-mh)/sh)**2)",
"    p,pc=curve_fit(model,c,h,p0=[500,30,200,91.2,5,20,125,2])",
"    ax.errorbar(c,h,yerr=np.sqrt(h),fmt='o',color='#8b949e',ms=3,label='p-p Daten')",
"    xf=np.linspace(50,160,1000); ax.plot(xf,model(xf,*p),color='#58a6ff',lw=2.5,label='Fit')",
"    ax.set_title('⚛️ Proton-Proton: Higgs & Z⁰',fontsize=14,fontweight='bold',color='#58a6ff')",
"    ax.set_xlabel('Invariante Masse [GeV/c²]'); ax.set_ylabel('Ereignisse'); ax.set_xlim(50,160)",
"    t=f'$M(Z^0) = {p[3]:.2f} \\\\pm {np.sqrt(pc[3,3]):.2f}$ GeV\\n$M(H) = {p[6]:.2f} \\\\pm {np.sqrt(pc[6,6]):.2f}$ GeV'",
"    ax.text(.05,.95,t,transform=ax.transAxes,fontsize=10,va='top',",
"            bbox=dict(boxstyle='round',fc='#161b22',ec='#30363d',alpha=.8),color='#fff')",
"else:",
"    np.random.seed(137)",
"    bg=np.random.uniform(1,12,9750)",
"    jp=np.random.normal(3.1,.18,4050); jp=jp[(jp>=1)&(jp<=12)]",
"    up=np.random.normal(9.46,.32,1200); up=up[(up>=1)&(up<=12)]",
"    data=np.concatenate([bg,jp,up])",
"    h,e=np.histogram(data,bins=70,range=(1,12)); c=.5*(e[1:]+e[:-1])",
"    def model_i(x,bg,aj,mj,sj,au,mu,su):",
"        return bg+aj*np.exp(-.5*((x-mj)/sj)**2)+au*np.exp(-.5*((x-mu)/su)**2)",
"    p,pc=curve_fit(model_i,c,h,p0=[150,200,3.1,.2,50,9.46,.3])",
"    ax.errorbar(c,h,yerr=np.sqrt(h),fmt='o',color='#8b949e',ms=3,label='Pb-Pb Daten (ALICE)')",
"    xf=np.linspace(1,12,1000); ax.plot(xf,model_i(xf,*p),color='#e377c2',lw=2.5,label='Fit')",
"    ax.set_title('⚛️ Pb-Pb: Quark-Gluon-Plasma',fontsize=14,fontweight='bold',color='#e377c2')",
"    ax.set_xlabel('Invariante Masse [GeV/c²]'); ax.set_ylabel('Ereignisse'); ax.set_xlim(1,12)",
"    t=f'$M(J/\\\\psi) = {p[2]:.3f} \\\\pm {np.sqrt(pc[2,2]):.3f}$ GeV\\n$M(\\\\Upsilon) = {p[5]:.3f} \\\\pm {np.sqrt(pc[5,5]):.3f}$ GeV'",
"    ax.text(.05,.95,t,transform=ax.transAxes,fontsize=10,va='top',",
"            bbox=dict(boxstyle='round',fc='#161b22',ec='#30363d',alpha=.8),color='#fff')",
"ax.legend(framealpha=.8,loc='upper right')",
"plt.tight_layout(); plt.show()",
]))

# ── CELL 7: Conclusion ───────────────────────────────────────────────────────
cells.append(md([
"## 🎓 Zusammenfassung",
"",
"In dieser Simulation hat **dasselbe Teilchenpaket** den gesamten Beschleunigerkomplex durchlaufen:",
"- Vom Injektor (LINAC 4/3) durch die Vorbeschleuniger (PSB/LEIR → PS → SPS) bis zur Einspeisung in den LHC.",
"- Der LHC wurde tatsächlich aufgefüllt: Jeder Injektionszyklus hat ein weiteres Bunch zum Strahl hinzugefügt.",
"- Erst bei ausreichender Füllung beider Strahlen konnte die Energie gerampt und Kollisionen ausgelöst werden.",
"- Die Pfade im Stellwerk sind geometrisch exakt verbunden (Transferlinien TI 2 und TI 8 verbinden SPS mit LHC an den korrekten Einspeisepunkten nahe ALICE und LHCb).",
]))

# ── Build & Write Notebook ────────────────────────────────────────────────────
nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name":"Python 3","language":"python","name":"python3"},
        "language_info": {"name":"python"}
    },
    "nbformat": 4, "nbformat_minor": 2
}

for path in [NB_PATH, ROOT_PATH]:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)

print(f"🎉 Notebook generiert:\n  1. {NB_PATH}\n  2. {ROOT_PATH}")
