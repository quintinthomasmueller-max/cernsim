# -*- coding: utf-8 -*-
"""
Generates the fully physics-coherent CERN accelerator complex notebook.
Key principle: the SAME particle bunch travels the entire chain from source to LHC.
The LHC fills up with multiple bunches before collision is possible.
All SVG paths connect at exact geometric junction points.
"""
import json, os

script_dir = os.path.dirname(os.path.abspath(__file__))
cern_root = os.path.abspath(os.path.join(script_dir, ".."))

NB_PATH = os.path.join(cern_root, "notebooks", "CERN_Beschleuniger_Schaltzentrale.ipynb")

import math
def generate_pipe_path(sign, delta=5.5):
    cx, cy, r_base = 350, 240, 180
    pts = []
    for i in range(181):
        a = i * math.pi / 90.0
        r = r_base + sign * delta * math.sin(a * 2)
        x = cx + r * math.cos(a)
        y = cy + r * math.sin(a)
        pts.append(f"{'M' if i==0 else 'L'} {x:.2f},{y:.2f}")
    return " ".join(pts)

pipe1_path = generate_pipe_path(1)
pipe2_path = generate_pipe_path(-1)


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
"3. **LHC auffüllen**: Der LHC braucht mindestens **6 Bunches pro Strahl** (Beam 1 im Uhrzeigersinn über TI 2, Beam 2 gegen den Uhrzeigersinn über TI 8).",
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
"1. Wähle **Protonen** oder **Blei-Ionen** (oder nutze eines der **Experiment-Presets**)",
"2. Klicke **Füllprotokoll (Autopilot)** für eine automatische, symmetrische Injektion beider Strahlen",
"3. Alternativ: Injiziere manuelle Bunches für **Beam 1** (über TI 2) und **Beam 2** (über TI 8)",
"4. Starte das **Ramping** und führe nach dem **Beam Squeeze** Kollisionen aus!",
]))

# ── CELL 4: The Interactive Dashboard ─────────────────────────────────────────
html = r"""<div id="cern-v4">
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
.cv4-svg-wrap{background:#090d13;border-radius:12px;border:1px solid #21262d;height:500px;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden}
.cv4-panel{background:#161b22;border-radius:12px;border:1px solid #30363d;padding:14px;display:flex;flex-direction:column;gap:14px}
.cv4-ptitle{font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#8b949e;border-bottom:1px solid #30363d;padding-bottom:6px;margin-bottom:6px;font-weight:700}
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
.cv4-grid{display:grid;grid-template-columns:1fr 310px;gap:20px}
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
.svg-lhc{stroke:rgba(88,166,255,.08);stroke-width:4;fill:none}
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
.cv4-sli-lbl{display:flex;justify-content:space-between;font-size:10px;color:#8b949e;margin-top:4px}
.cv4-sli{width:100%;background:#21262d;border-radius:3px;height:4px;outline:none;-webkit-appearance:none;margin-top:2px}
.cv4-sli::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:12px;height:12px;border-radius:50%;background:#58a6ff;cursor:pointer;border:1px solid #30363d}
.cv4-sli::-moz-range-thumb{width:12px;height:12px;border-radius:50%;background:#58a6ff;cursor:pointer;border:1px solid #30363d}
.cv4-quench{background:rgba(248,81,73,.15);border:1px solid #f85149;color:#f85149;padding:10px;border-radius:6px;font-size:12px;font-weight:bold;text-align:center;animation:cv4blink 1s infinite}
@keyframes cv4blink{0%,100%{opacity:.5}50%{opacity:1}}
.geo-element{transition:opacity 0.3s ease, fill-opacity 0.3s ease;}
</style>

<div class="cv4-hdr">
 <div><span class="cv4-logo">⚛️ CERN CCC</span><span class="cv4-badge">Schaltzentrale v5 - Real Map</span></div>
 <div style="display:flex;align-items:center;gap:12px">
  <button class="cv4-btn act" id="btn-toggle-geo" style="padding:4px 8px;font-size:10.5px">🌐 Geo-Overlay</button>
  <div class="cv4-status"><span class="cv4-dot" id="sdot"></span><span id="stxt">OFFLINE</span></div>
 </div>
</div>

<div class="cv4-sel">
  <div class="cv4-sel-tab act-p" id="sel-p">🔵 Protonen (LINAC4 → PSB → PS → SPS → LHC)</div>
  <div class="cv4-sel-tab" id="sel-i">🟣 Blei-Ionen (LINAC3 → LEIR → PS → SPS → LHC)</div>
</div>

<div class="cv4-grid">
 <div class="cv4-svg-wrap">
  <!-- Interactive Absolute Overlay Reset Zoom Button -->
  <button class="cv4-btn off" id="btn-zoom-out" style="position:absolute;top:12px;left:12px;padding:5px 10px;font-size:10px;background:rgba(22,27,34,0.85);border-color:#30363d;z-index:10;transition:all 0.2s">🔍 Ansicht zurücksetzen</button>

  <svg id="svg" width="700" height="480" viewBox="0 0 700 480" style="background:#090d13">
   <!-- Architectural Grid for tech style -->
   <defs>
    <pattern id="arch-grid" width="30" height="30" patternUnits="userSpaceOnUse">
     <path d="M 30 0 L 0 0 0 30" fill="none" stroke="rgba(255,255,255,0.012)" stroke-width="0.5"/>
    </pattern>
   </defs>
   <rect width="100%" height="100%" fill="url(#arch-grid)" />

   <!-- GEOGRAPHICAL FEATURES (Toggleable via .geo-element) -->
   <!-- Geneva Lake (Lac Léman) in top-right -->
   <path class="geo-element" d="M 520,0 Q 560,50 620,60 T 700,75 L 700,0 Z" fill="rgba(88,166,255,0.04)" stroke="rgba(88,166,255,0.12)" stroke-width="1.5" />
   <text class="geo-element" x="610" y="30" fill="rgba(88,166,255,0.22)" font-size="8px" font-family="monospace">LAC LÉMAN (GENFER SEE)</text>

   <!-- French-Swiss Border (dashed line cutting diagonally) -->
   <path class="geo-element" d="M 0,220 L 700,120" stroke="rgba(255,255,255,0.06)" stroke-width="1.2" stroke-dasharray="6,6" />
   <text class="geo-element" x="80" y="200" fill="rgba(255,255,255,0.12)" font-size="7.5px" font-family="monospace" transform="rotate(-8, 80, 200)">STAATSGRENZE SCHWEIZ (CH) - FRANKREICH (FR)</text>

   <!-- Jura Mountain Ridge in the top-left -->
   <path class="geo-element" d="M 0,50 Q 80,80 150,50 T 250,20" stroke="rgba(255,255,255,0.04)" stroke-width="1.5" stroke-dasharray="3,6" fill="none" />
   <text class="geo-element" x="60" y="40" fill="rgba(255,255,255,0.10)" font-size="7px" font-family="monospace">JURA-GEBIRGE (FR)</text>

   <!-- Geographic Town/Site Markers -->
   <text class="geo-element" x="142" y="430" fill="rgba(255,255,255,0.18)" font-size="7.5px" font-family="monospace" text-anchor="middle">CERN Meyrin Campus (CH)</text>
   <text class="geo-element" x="430" y="90" fill="rgba(255,255,255,0.18)" font-size="7.5px" font-family="monospace" text-anchor="middle">CERN Prévessin Campus (FR)</text>
   <text class="geo-element" x="100" y="225" fill="rgba(255,255,255,0.18)" font-size="7.5px" font-family="monospace">St. Genis-Pouilly (FR)</text>
   <text class="geo-element" x="350" y="25" fill="rgba(255,255,255,0.18)" font-size="7.5px" font-family="monospace" text-anchor="middle">Ferney-Voltaire (FR)</text>
   <path class="geo-element" d="M 590,320 L 670,290" stroke="rgba(255,255,255,0.08)" stroke-width="3" />
   <text class="geo-element" x="630" y="332" fill="rgba(255,255,255,0.15)" font-size="7.5px" font-family="monospace" text-anchor="middle">Flughafen Genf (GVA)</text>

   <!-- REAL CERN TOP-VIEW ACCELERATOR STRUCTURE -->
   <!-- LINAC4: straight line injecting into PSB (cx=142, cy=385) -->
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

   <!-- SPS ring: medium ring located SOUTH-EAST inside the LHC, near ALICE. cx=400 cy=148 r=65 -->
   <circle id="p-sps" cx="400" cy="148" r="65" class="svg-path"/>

   <!-- TI 2: SPS → LHC injection near ALICE (Point 2, left) -->
   <path id="p-ti2" d="M 339.5,173.7 Q 255,195 170,240" class="svg-path"/>
   <!-- TI 8: SPS → LHC injection near LHCb (Point 8, right) -->
   <path id="p-ti8" d="M 453.4,187.1 Q 495,215 530,240" class="svg-path"/>

   <!-- Modulated crossover beam vacuum tubes inside the LHC arcs (Double-bore design) -->
    <!-- Beam 1 tube: starts outer at 45°, crosses in detectors -->
    <path id="lhc-pipe1" class="geo-element" d="PLACEHOLDER_PIPE1" stroke="rgba(88,166,255,0.22)" stroke-width="1.2" fill="none" stroke-dasharray="3,3" style="transition: opacity 0.3s;" />
    <!-- Beam 2 tube: starts inner at 45°, crosses in detectors -->
    <path id="lhc-pipe2" class="geo-element" d="PLACEHOLDER_PIPE2" stroke="rgba(255,127,14,0.22)" stroke-width="1.2" fill="none" stroke-dasharray="3,3" style="transition: opacity 0.3s;" />

   <!-- LHC tunnel (massive average ring cx=350 cy=240 r=180) -->
   <circle id="p-lhc" cx="350" cy="240" r="180" class="svg-path svg-lhc"/>

   <!-- STYLISH ACCELERATOR DETECTORS & DETAILS -->
   <!-- RF Cavities on the LHC ring (Point 4) represented as small bright rects -->
   <rect x="340" y="415" width="20" height="10" fill="rgba(255,127,14,0.2)" stroke="#ff7f0e" stroke-width="1" />
   <rect x="340" y="55" width="20" height="10" fill="rgba(255,127,14,0.2)" stroke="#ff7f0e" stroke-width="1" />
   <text x="350" y="435" fill="rgba(255,127,14,0.5)" font-size="6px" font-family="monospace" text-anchor="middle">400 MHz RF</text>

   <!-- Quadrupole focusing triplets near the detectors -->
   <path d="M 330,420 L 370,420" stroke="#2ea44f" stroke-width="3" opacity="0.3" />
   <path d="M 330,60 L 370,60" stroke="#2ea44f" stroke-width="3" opacity="0.3" />
   <path d="M 170,220 L 170,260" stroke="#2ea44f" stroke-width="3" opacity="0.3" />
   <path d="M 530,220 L 530,260" stroke="#2ea44f" stroke-width="3" opacity="0.3" />

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

   <!-- LHC Detector Groups for interactive zoom -->
   <g id="grp-atlas" style="cursor:pointer">
    <circle id="d-atlas" cx="350" cy="420" r="14" class="svg-node"/>
    <text x="350" y="448" class="svg-lbl" style="fill:#e6edf3;font-weight:bold">ATLAS (IP1)</text>
   </g>
   <g id="grp-cms" style="cursor:pointer">
    <circle id="d-cms" cx="350" cy="60" r="14" class="svg-node"/>
    <text x="350" y="42" class="svg-lbl" style="fill:#e6edf3;font-weight:bold">CMS (IP5)</text>
   </g>
   <g id="grp-alice" style="cursor:pointer">
    <circle id="d-alice" cx="170" cy="240" r="12" class="svg-node"/>
    <text x="134" y="240" class="svg-lbl" style="fill:#e6edf3;font-weight:bold">ALICE (IP2)</text>
   </g>
   <g id="grp-lhcb" style="cursor:pointer">
    <circle id="d-lhcb" cx="530" cy="240" r="12" class="svg-node"/>
    <text x="567" y="240" class="svg-lbl" style="fill:#e6edf3;font-weight:bold">LHCb (IP8)</text>
   </g>

   <!-- TI labels -->
   <text x="248" y="186" class="svg-lbl" style="font-size:8px">TI 2</text>
   <text x="485" y="205" class="svg-lbl" style="font-size:8px">TI 8</text>
  </svg>
 </div>

 <div class="cv4-panel">
  <div>
   <div class="cv4-ptitle">🔬 EXPERIMENT-PRESETS (SCHNELLWAHL)</div>
   <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:8px">
    <button class="cv4-btn" id="btn-pre-higgs" style="background:rgba(88,166,255,.10);border-color:#58a6ff;color:#58a6ff;font-size:9.5px;padding:6px 2px">Higgs-Suche (ATLAS/CMS)</button>
    <button class="cv4-btn" id="btn-pre-qgp" style="background:rgba(227,119,194,.10);border-color:#e377c2;color:#e377c2;font-size:9.5px;padding:6px 2px">QGP-Erzeugung (ALICE)</button>
    <button class="cv4-btn" id="btn-pre-lhcb" style="background:rgba(255,127,14,.10);border-color:#ff7f0e;color:#ff7f0e;font-size:9.5px;padding:6px 2px">CP-Verletzung (LHCb)</button>
    <button class="cv4-btn" id="btn-pre-pilot" style="background:rgba(23,190,207,.10);border-color:#17becf;color:#17becf;font-size:9.5px;padding:6px 2px">Pilot-Strahl (Testrun)</button>
   </div>
  </div>

  <div>
   <div class="cv4-ptitle">📡 INJEKTION</div>
   <div style="display:flex;flex-direction:column;gap:6px">
    <button class="cv4-btn" id="btn-speed-toggle" style="background:rgba(88,166,255,.08);border-color:rgba(88,166,255,.3);color:#58a6ff;font-size:10.5px;padding:6px 4px;margin-bottom:2px">⏱️ Modus: Zeitraffer (Schnell)</button>
    <button class="cv4-btn" id="btn-auto" style="background:rgba(46,164,79,.15);border-color:#2ea44f;color:#2ea44f">⚙️ Füllprotokoll (Autopilot)</button>
    <div style="display:flex;gap:4px">
     <button class="cv4-btn" id="btn-b1" style="flex:1;padding:6px;font-size:10px">📥 Manuell B1</button>
     <button class="cv4-btn" id="btn-b2" style="flex:1;padding:6px;font-size:10px">📥 Manuell B2</button>
    </div>
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
   <div class="cv4-fill-row"><span style="width:50px">B1 <span id="b1c">0</span>/6</span><div class="cv4-fill-bar"><div class="cv4-fill-bar-inner b1" id="b1bar" style="width:0%"></div></div></div>
   <div class="cv4-fill-row" style="margin-top:4px"><span style="width:50px">B2 <span id="b2c">0</span>/6</span><div class="cv4-fill-bar"><div class="cv4-fill-bar-inner b2" id="b2bar" style="width:0%"></div></div></div>
  </div>

  <div>
   <div class="cv4-ptitle">🎛️ CCC BETRIEBSPARAMETER</div>
   <div class="cv4-sli-lbl"><span>Ziel-Energie:</span><span id="lbl-energy">6.8 TeV</span></div>
   <input type="range" class="cv4-sli" id="sli-energy" min="1.0" max="7.0" step="0.2" value="6.8">

   <div class="cv4-sli-lbl" style="margin-top:8px"><span>Bunch-Intensität:</span><span id="lbl-intensity">1.15e11 p</span></div>
   <input type="range" class="cv4-sli" id="sli-intensity" min="0.1" max="1.8" step="0.05" value="1.15">

   <div class="cv4-sli-lbl" style="margin-top:8px"><span>Strahl-Fokus β* (Squeeze):</span><span id="lbl-beta">1.50 m</span></div>
   <input type="range" class="cv4-sli" id="sli-beta" min="0.3" max="1.5" step="0.1" value="1.5" disabled>

   <div class="cv4-sli-lbl" style="margin-top:8px"><span>Ramp-Rate dB/dt:</span><span id="lbl-rampspeed" style="color:#58a6ff">0.05 T/s (Sicher)</span></div>
   <input type="range" class="cv4-sli" id="sli-rampspeed" min="0.02" max="0.15" step="0.01" value="0.05">
  </div>

  <div>
   <div class="cv4-ptitle">⚡ LHC BETRIEB</div>
   <div style="display:flex;flex-direction:column;gap:6px">
    <button class="cv4-btn off" id="btn-ramp">🚀 Energie-Ramping starten</button>
    <div class="cv4-fill-row"><span style="width:50px;font-size:10px">Ramp</span><div class="cv4-fill-bar"><div class="cv4-fill-bar-inner b1" id="rbar" style="width:0%"></div></div></div>
    <button class="cv4-btn off" id="btn-squeeze" style="background:rgba(23,190,207,.15);border-color:#17becf;color:#17becf">🗜️ Beam Squeeze starten (β*)</button>
    <div style="display:flex;gap:4px">
     <button class="cv4-btn danger off" id="btn-coll" style="flex:1;font-size:10.5px;padding:9px 2px">💥 Kollision (manuell)</button>
     <button class="cv4-btn off" id="btn-autocoll" style="flex:1.2;background:rgba(248,81,73,.08);border-color:rgba(248,81,73,.4);color:#f85149;font-size:10.5px;padding:9px 2px">▶️ Auto-Datennahme</button>
    </div>
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
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px;font-size:10px;padding:0 4px">
   <span>Signifikanz: <strong id="lbl-sig" style="font-family:monospace;color:#8b949e">0.00 σ</strong></span>
   <span id="lbl-sig-status" style="font-weight:bold;color:#8b949e;font-size:9.5px">Rauschen (Kein Signal)</span>
  </div>
  <div class="cv4-fill-bar" style="height:4px;margin-bottom:6px;background:#21262d;border-radius:2px;overflow:hidden">
   <div class="cv4-fill-bar-inner" id="sig-bar" style="width:0%;background:#8b949e;height:100%;transition:all 0.2s"></div>
  </div>
  <div class="cv4-histwrap"><canvas id="cv-hist" style="width:100%;height:100%"></canvas></div>
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
const NEEDED=6;
let lhcDots={b1:[],b2:[]};
let lhcSpeed=0.0030; // rad/ms at injection energy (Proton default)
let lhcAngle=0, lhcRunning=false, lhcLastT=null;
let lhcEnergy=450; // GeV
let massData=[];
let selDet="ATLAS";
let isFastMode=true; // Toggleable speed mode

function getDurations() {
  if (isFastMode) {
    return {
      linac: isIon ? 350 : 200,
      ring1: isIon ? 900 : 500,
      trToPs: isIon ? 150 : 100,
      ps: isIon ? 1000 : 600,
      trToSps: isIon ? 200 : 100,
      sps: isIon ? 800 : 500,
      ti: isIon ? 250 : 150,
      autoDelay: 150
    };
  } else {
    return {
      linac: isIon ? 1200 : 600,
      ring1: isIon ? 3400 : 1900,
      trToPs: isIon ? 300 : 150,
      ps: isIon ? 3600 : 2000,
      trToSps: isIon ? 400 : 200,
      sps: isIon ? 2700 : 1600,
      ti: isIon ? 500 : 250,
      autoDelay: 800
    };
  }
}

// CCC OPERATOR STATES
let paramEnergy = 6.8;      // Target Energy (TeV)
let paramIntensity = 1.15;  // Bunch Intensity (10^11 protons)
let paramBetaStar = 1.5;    // Beam size at IP (meters)
let paramRampSpeed = 0.05;  // Magnetic field ramp rate (T/s)
let squeezing = false;      // Squeeze in progress
let squeezed = false;       // Squeeze complete
let cryoRecovery = false;   // Cryogenic recovery active
let autoCollInterval = null; // Auto Collide loop

// ═══════════════════════════════════════════════════════════════════════════
// DOM REFERENCES
// ═══════════════════════════════════════════════════════════════════════════
const $=id=>document.getElementById(id);
const sdot=$("sdot"),stxt=$("stxt");
const btnB1=$("btn-b1"),btnB2=$("btn-b2"),btnRamp=$("btn-ramp"),btnColl=$("btn-coll"),btnAuto=$("btn-auto"),btnSqueeze=$("btn-squeeze");
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

["atlas","cms","alice","lhcb"].forEach(d=>{
 $("dt-"+d).addEventListener("click",()=>{
  document.querySelectorAll(".cv4-dtab").forEach(t=>t.classList.remove("act"));
  $("dt-"+d).classList.add("act");
  selDet=d.toUpperCase();
  drawDetBg();
 });
});

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
 resetFlag = true;
 autopilotActive = false;
 stopAutoCollide();
 document.querySelectorAll(".traveling-dot").forEach(d=>d.remove());
 btnB1.classList.remove("off"); btnB2.classList.remove("off"); btnAuto.classList.remove("off");
 injecting = false;
 lhcDots.b1.forEach(d=>d.el.remove()); lhcDots.b2.forEach(d=>d.el.remove());
 lhcDots={b1:[],b2:[]}; b1Count=0; b2Count=0; collisions=0; massData=[];
 ramped=false; squeezed=false; squeezing=false;
 lhcEnergy=isIon?177:450; lhcSpeed=isIon?0.0019:0.0030;
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

async function injectBunch(beam){
 if(injecting) return;
 injecting=true;
 resetFlag = false;
 btnB1.classList.add("off"); btnB2.classList.add("off");

 const ion=isIon;
 const litCls=ion?"lit-i":"lit";
 const glowCls=ion?"glow-i":"glow";
 const dotColor=ion?"#e377c2":"#58a6ff";
 const dotColorB2=ion?"#c77dff":"#ff7f0e";
 const color=beam===1?dotColor:dotColorB2;

 const dot=document.createElementNS(SVG_NS,"circle");
 dot.setAttribute("class", "traveling-dot");
 dot.setAttribute("r","4");
 dot.setAttribute("fill",color);
 dot.style.filter="drop-shadow(0 0 4px "+color+")";
 svg.appendChild(dot);

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

 setTracker(0);
 const linacPath=ion?paths.linac3:paths.linac4;
 const linacNode=ion?nodes.linac3:nodes.linac4;
 lightNode(linacNode); lightPath(linacPath);
 setStatus(ion?"LINAC 3 FEUERT":"LINAC 4 FEUERT","on");
 await moveAlongPath(dot, linacPath, getDurations().linac);
 if (resetFlag) { dot.remove(); return; }
 dimNode(linacNode);

 setTracker(1);
 const ring1=ion?R.LEIR:R.PSB;
 const ring1Path=ion?paths.leir:paths.psb;
 const ring1Node=ion?nodes.leir:nodes.psb;
 const ring1Entry=ion?J.LEIR_ENTRY:J.PSB_ENTRY;
 const ring1Exit=ion?J.LEIR_EXIT:J.PSB_EXIT;
 lightPath(ring1Path); lightNode(ring1Node);
 setStatus(ion?"LEIR: Beschleunigung auf 72 MeV/u":"PSB: Beschleunigung auf 2 GeV","on");
 await orbitRing(dot, ring1, ring1Entry, ring1Exit, 3, getDurations().ring1);
 if (resetFlag) { dot.remove(); return; }
 dimPath(ring1Path); dimPath(linacPath);

 const trToPs=ion?paths.leirPs:paths.psbPs;
 lightPath(trToPs);
 await moveAlongPath(dot, trToPs, getDurations().trToPs);
 if (resetFlag) { dot.remove(); return; }
 dimPath(trToPs); dimNode(ring1Node);

 setTracker(2);
 const psEntry=ion?J.PS_FROM_LEIR:J.PS_FROM_PSB;
 lightPath(paths.ps); lightNode(nodes.ps);
 setStatus(ion?"PS: Beschleunigung auf 5.9 GeV/u":"PS: Beschleunigung auf 26 GeV","on");
 await orbitRing(dot, R.PS, psEntry, J.PS_EXIT, 3, getDurations().ps);
 if (resetFlag) { dot.remove(); return; }
 dimPath(paths.ps);

 lightPath(paths.psSps);
 await moveAlongPath(dot, paths.psSps, getDurations().trToSps);
 if (resetFlag) { dot.remove(); return; }
 dimPath(paths.psSps); dimNode(nodes.ps);

 setTracker(3);
 lightPath(paths.sps); lightNode(nodes.sps);
 const spsExit=beam===1?J.SPS_TI2:J.SPS_TI8;
 setStatus(ion?"SPS: Beschleunigung auf 177 GeV/u":"SPS: Beschleunigung auf 450 GeV","on");
 await orbitRing(dot, R.SPS, J.SPS_ENTRY, spsExit, 2, getDurations().sps);
 if (resetFlag) { dot.remove(); return; }
 dimPath(paths.sps);

 const tiPath=beam===1?paths.ti2:paths.ti8;
 lightPath(tiPath);
 setStatus(beam===1?"Transfer via TI 2 zum LHC":"Transfer via TI 8 zum LHC","on");
 await moveAlongPath(dot, tiPath, getDurations().ti);
 if (resetFlag) { dot.remove(); return; }
 dimPath(tiPath); dimNode(nodes.sps);

 setTracker(4);
 dot.remove();
 addPermanentDot(beam);
 if(beam===1){ b1Count++; b1c.innerText=b1Count; b1bar.style.width=(b1Count/NEEDED*100)+"%"; }
 else { b2Count++; b2c.innerText=b2Count; b2bar.style.width=(b2Count/NEEDED*100)+"%"; }
 paths.lhc.classList.add(ion?"lit-i":"lit");
 if(b1Count>=NEEDED && b2Count>=NEEDED && !ramped){
  btnRamp.classList.remove("off");
  setStatus("LHC GEFÜLLT — Ramping möglich!","on");
 } else {
  setStatus("LHC B1:"+b1Count+"/"+NEEDED+" B2:"+b2Count+"/"+NEEDED,"on");
 }
 injecting=false;
 btnB1.classList.remove("off"); btnB2.classList.remove("off");
 trSteps.forEach(s=>s.classList.remove("cur","cur-i","done"));
}

btnRamp.addEventListener("click",async()=>{
 if(ramped||injecting||cryoRecovery) return;
 btnRamp.classList.add("off"); btnB1.classList.add("off"); btnB2.classList.add("off"); btnAuto.classList.add("off");
 sliEnergy.disabled = true; sliIntensity.disabled = true; sliRampSpeed.disabled = true;
 setStatus("RAMPING MAGNETFELD & ENERGIE...","on");
 const startE=isIon?177:450;
 const targetE=paramEnergy*1000;
 const startSpeed=isIon?0.0019:0.0030;
 const targetSpeed=(isIon?0.0042:0.0070)*(paramEnergy/(isIon?2.5:6.8));
 const dur = 200 / paramRampSpeed;
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
  lhcAngle+=lhcSpeed*dt;
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
 drawCollisionEvent(); generateMassData(); drawHist();
});

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
  drawCollisionEvent(); generateMassData(); drawHist();
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
 let B=lhcEnergy/(0.299792458*2803.95); vB.innerText=B.toFixed(3)+" T";
 let g=lhcEnergy/(isIon?193.7:0.938272); vG.innerText=Math.round(g).toLocaleString("de-DE");
}

function setStatus(txt,cls){stxt.innerText=txt;sdot.className="cv4-dot "+cls;}

function drawDetBg(){
  let w=evW,h=evH,cx=w/2,cy=h/2;
  ctxEv.clearRect(0,0,w,h);
  ctxEv.strokeStyle="#1a1f27"; ctxEv.lineWidth=1; ctxEv.strokeRect(0,0,w,h);
  ctxEv.fillStyle="#8b949e"; ctxEv.font="9px monospace"; ctxEv.fillText(selDet + " | " + (isIon?"Pb-Pb":"p-p"), 8, 16);
  if (selDet === "ATLAS") {
    ctxEv.strokeStyle="rgba(88,166,255,0.06)";
    [20, 45, 70].forEach(r=>{ ctxEv.beginPath(); ctxEv.arc(cx,cy,r,0,2*Math.PI); ctxEv.stroke(); });
    ctxEv.strokeStyle="rgba(88,166,255,0.2)"; ctxEv.lineWidth = 4;
    for(let i=0; i<8; i++) { let a = i * Math.PI / 4; ctxEv.beginPath(); ctxEv.moveTo(cx + 65*Math.cos(a), cy + 65*Math.sin(a)); ctxEv.lineTo(cx + 85*Math.cos(a), cy + 85*Math.sin(a)); ctxEv.stroke(); }
    ctxEv.lineWidth = 1; ctxEv.fillStyle="rgba(88,166,255,0.3)"; ctxEv.font="7px monospace"; ctxEv.fillText("TOROID-MAGNETE", cx - 30, cy + 82);
  } else if (selDet === "CMS") {
    ctxEv.strokeStyle="rgba(248,81,73,0.06)";
    [20, 40, 80].forEach(r=>{ ctxEv.beginPath(); ctxEv.arc(cx,cy,r,0,2*Math.PI); ctxEv.stroke(); });
    ctxEv.strokeStyle="rgba(248,81,73,0.2)"; ctxEv.lineWidth = 6;
    ctxEv.beginPath(); ctxEv.arc(cx, cy, 55, 0, 2*Math.PI); ctxEv.stroke();
    ctxEv.lineWidth = 1; ctxEv.fillStyle="rgba(248,81,73,0.3)"; ctxEv.font="7px monospace"; ctxEv.fillText("SOLENOID-SPULE", cx - 30, cy + 64);
  } else if (selDet === "ALICE") {
    ctxEv.strokeStyle="rgba(227,119,194,0.08)";
    ctxEv.beginPath(); ctxEv.arc(cx,cy,35,0,2*Math.PI); ctxEv.stroke(); ctxEv.beginPath(); ctxEv.arc(cx,cy,15,0,2*Math.PI); ctxEv.stroke();
    ctxEv.strokeStyle="rgba(227,119,194,0.2)"; ctxEv.beginPath();
    for (let i = 0; i <= 8; i++) { let a = i * Math.PI / 4; let x = cx + 80 * Math.cos(a); let y = cy + 80 * Math.sin(a); if (i === 0) ctxEv.moveTo(x, y); else ctxEv.lineTo(x, y); }
    ctxEv.stroke(); ctxEv.fillStyle="rgba(227,119,194,0.3)"; ctxEv.font="7px monospace"; ctxEv.fillText("TPC ZYLINDER", cx - 25, cy - 40); ctxEv.fillText("L3 MAGNET", cx - 20, cy + 76);
  } else if (selDet === "LHCB") {
    ctxEv.strokeStyle="rgba(255,127,14,0.12)"; ctxEv.beginPath(); ctxEv.moveTo(0, cy); ctxEv.lineTo(w, cy); ctxEv.stroke();
    let stations = [{x: 40, label: "IP"},{x: 80, label: "RICH1"},{x: 130, label: "MAGNET"},{x: 180, label: "RICH2"},{x: 230, label: "ECAL"},{x: 290, label: "MUON"}];
    stations.forEach(st => {
      ctxEv.strokeStyle = st.label === "MAGNET" ? "rgba(255,127,14,0.4)" : "rgba(255,127,14,0.15)";
      ctxEv.lineWidth = st.label === "MAGNET" ? 3 : 1;
      ctxEv.beginPath(); ctxEv.moveTo(st.x, 25); ctxEv.lineTo(st.x, h - 15); ctxEv.stroke();
      ctxEv.fillStyle = "rgba(255,127,14,0.4)"; ctxEv.font = "6.5px monospace"; ctxEv.fillText(st.label, st.x - 12, 22);
    });
    ctxEv.lineWidth = 1;
  }
}

function drawCollisionEvent(){
  drawDetBg();
  let w=evW,h=evH,cx=w/2,cy=h/2;
  if (selDet === "ATLAS") {
    for(let i=0; i<12; i++) {
      let a = Math.random()*2*Math.PI; let len = 35 + Math.random()*30;
      ctxEv.strokeStyle = Math.random() > 0.5 ? "#58a6ff" : "#ff7f0e";
      ctxEv.lineWidth = 0.8; ctxEv.beginPath(); ctxEv.moveTo(cx, cy); ctxEv.lineTo(cx+len*Math.cos(a), cy+len*Math.sin(a)); ctxEv.stroke();
    }
    for (let i = 0; i < 2; i++) {
      let a = (i === 0 ? 0.35 : 3.4) + (Math.random() - 0.5) * 0.1;
      ctxEv.strokeStyle = "#2ea44f"; ctxEv.lineWidth = 2;
      ctxEv.beginPath(); ctxEv.moveTo(cx, cy); ctxEv.lineTo(cx + 88*Math.cos(a), cy + 88*Math.sin(a)); ctxEv.stroke();
      ctxEv.fillStyle = "#2ea44f"; ctxEv.beginPath(); ctxEv.arc(cx + 88*Math.cos(a), cy + 88*Math.sin(a), 3.5, 0, 2*Math.PI); ctxEv.fill();
    }
    ctxEv.fillStyle = "#2ea44f"; ctxEv.font = "8px sans-serif"; ctxEv.fillText("Müon-Spur (μ)", cx + 45, cy + 30);
  } else if (selDet === "CMS") {
    [1.1, 4.3].forEach(ja => {
      for (let i = 0; i < 8; i++) {
        let a = ja + (Math.random() - 0.5) * 0.18; let len = 40 + Math.random() * 38;
        ctxEv.strokeStyle = "#ff7f0e"; ctxEv.lineWidth = 0.9;
        ctxEv.beginPath(); ctxEv.moveTo(cx, cy); ctxEv.lineTo(cx + len*Math.cos(a), cy + len*Math.sin(a)); ctxEv.stroke();
      }
    });
    let ea = 2.7; ctxEv.strokeStyle = "#58a6ff"; ctxEv.lineWidth = 1.8; ctxEv.beginPath();
    ctxEv.moveTo(cx, cy); ctxEv.quadraticCurveTo(cx + 40*Math.cos(ea+0.4), cy + 40*Math.sin(ea+0.4), cx + 78*Math.cos(ea), cy + 78*Math.sin(ea));
    ctxEv.stroke(); ctxEv.fillStyle = "#58a6ff"; ctxEv.beginPath(); ctxEv.arc(cx + 78*Math.cos(ea), cy + 78*Math.sin(ea), 3, 0, 2*Math.PI); ctxEv.fill();
    ctxEv.fillStyle = "#ff7f0e"; ctxEv.font = "8px sans-serif"; ctxEv.fillText("Hadron-Jets", cx + 32, cy - 25);
  } else if (selDet === "ALICE") {
    let nTracks = isIon ? 120 : 40;
    for(let i=0; i<nTracks; i++) {
      let a = Math.random()*2*Math.PI;
      let len = 15 + Math.random()*58;
      let curve = a + (Math.random() > 0.5 ? 0.22 : -0.22) * (len/70);
      let tx = cx + len*Math.cos(a), ty = cy + len*Math.sin(a);
      let cpx = cx + (len/2)*Math.cos(curve), cpy = cy + (len/2)*Math.sin(curve);
      ctxEv.strokeStyle = isIon ? "rgba(227,119,194,0.6)" : "rgba(88,166,255,0.6)";
      ctxEv.lineWidth = 0.7;
      ctxEv.beginPath(); ctxEv.moveTo(cx, cy); ctxEv.quadraticCurveTo(cpx, cpy, tx, ty); ctxEv.stroke();
    }
    ctxEv.fillStyle = "rgba(227,119,194,0.8)"; ctxEv.font = "8px sans-serif";
    ctxEv.fillText("TPC-Spuren: n = " + nTracks, cx - 40, cy - 4);
  } else if (selDet === "LHCB") {
    let ipx = 40, ipy = cy;
    let nTracks = 16;
    for (let i = 0; i < nTracks; i++) {
      let a = (Math.random() - 0.5) * 0.65;
      let len = 150 + Math.random() * 120;
      let curve = a + (Math.random() > 0.5 ? 0.08 : -0.08);
      let tx = ipx + len * Math.cos(a);
      let ty = ipy + len * Math.sin(a);
      let cpx = ipx + (len/2) * Math.cos(curve);
      let cpy = ipy + (len/2) * Math.sin(curve);
      let isMu = Math.random() > 0.85;
      ctxEv.strokeStyle = isMu ? "#2ea44f" : "#ff7f0e";
      ctxEv.lineWidth = isMu ? 1.5 : 0.8;
      ctxEv.beginPath(); ctxEv.moveTo(ipx, ipy); ctxEv.quadraticCurveTo(cpx, cpy, tx, ty); ctxEv.stroke();
      if (isMu && tx < w) {
        ctxEv.fillStyle = "#2ea44f";
        ctxEv.beginPath(); ctxEv.arc(tx, ty, 2.5, 0, 2*Math.PI); ctxEv.fill();
      }
    }
    ctxEv.fillStyle = "#ff7f0e"; ctxEv.font = "8px sans-serif";
    ctxEv.fillText("Forward-B-Zerfall", ipx + 90, ipy - 35);
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// HISTOGRAM
// ═══════════════════════════════════════════════════════════════════════════
function generateMassData(){
 // Skalierungsfaktor basierend auf Intensität (quadratisch) und Squeeze (antiproportional)
 let rateFactor = Math.pow(paramIntensity, 2) / paramBetaStar;
 let nPointsMultiplier = Math.max(1, Math.round(rateFactor * 4));
 
 if(!isIon){
  // Background (5x weniger pro Kollision, da wir 5x mehr Kollisionen sammeln)
  let bgCount = Math.max(1, Math.round(4 * nPointsMultiplier));
  for(let i=0; i<bgCount; i++){
   let m=50+Math.exp(Math.random()*4.6)*1.5;
   if(m>50&&m<150)massData.push(m);
  }
  // Z0 Peak (immer vorhanden)
  let zCount = Math.max(1, Math.round(1.6 * nPointsMultiplier));
  for(let i=0; i<zCount; i++) {
   massData.push(91.2+(Math.random()-.5)*4+(Math.random()-.5)*2);
  }
  // Higgs Peak (Schwellenenergie-Kopplung! Wenn Energie < 4.0 TeV, wird kein Higgs erzeugt)
  if(paramEnergy >= 4.0) {
   let hCount = Math.max(1, Math.round(0.6 * nPointsMultiplier));
   for(let i=0; i<hCount; i++){
    let m=125+(Math.random()-.5)*2.8+(Math.random()-.5)*1.2;
    if(m>50&&m<150)massData.push(m);
   }
  }
 }else{
  // Heavy Ion: ALICE Quark-Gluon-Plasma Spektrum (5x weniger pro Kollision)
  let bgCount = Math.max(1, Math.round(6 * nPointsMultiplier));
  for(let i=0; i<bgCount; i++) massData.push(1+Math.random()*11);
  
  let jpsiCount = Math.max(1, Math.round(2.4 * nPointsMultiplier));
  for(let i=0; i<jpsiCount; i++) massData.push(3.1+(Math.random()-.5)*.4+(Math.random()-.5)*.2);
  
  let upsilonCount = Math.max(1, Math.round(0.8 * nPointsMultiplier));
  for(let i=0; i<upsilonCount; i++) massData.push(9.46+(Math.random()-.5)*.6+(Math.random()-.5)*.3);
 }
}

function getTargetDiscover() {
  if (isIon) return 300;
  if (selDet === "LHCB") return 400;
  return 500;
}

function getSignificance() {
  if (collisions === 0) return 0;
  if (!isIon && selDet !== "LHCB" && paramEnergy < 4.0) return 0;
  let target = getTargetDiscover();
  return 5.0 * Math.sqrt(collisions / target);
}

function drawHist(){
  let w=histW,h=histH;
  ctxHist.clearRect(0,0,w,h);
  ctxHist.strokeStyle="#30363d";ctxHist.lineWidth=1;
  ctxHist.beginPath();ctxHist.moveTo(30,8);ctxHist.lineTo(30,h-16);ctxHist.lineTo(w-8,h-16);ctxHist.stroke();
  ctxHist.fillStyle="#8b949e";ctxHist.font="7.5px sans-serif";
  let mn=isIon?1:50, mx=isIon?12:150;
  ctxHist.fillText(mn+" GeV",30,h-5);ctxHist.fillText(mx+" GeV",w-40,h-5);
  
  let sig = getSignificance();
  $("lbl-sig").innerText = sig.toFixed(2) + " σ";
  
  let sigBar = $("sig-bar");
  let sigStatus = $("lbl-sig-status");
  let target = getTargetDiscover();
  let progressPct = (paramEnergy < 4.0 && !isIon && selDet !== "LHCB") ? 0 : (collisions / target) * 100;
  let pct = Math.min(100, progressPct);
  sigBar.style.width = pct + "%";
  
  if (sig === 0) {
    sigStatus.innerText = "Rauschen (Kein Signal)";
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
    sigStatus.innerText = "🌟 5σ ENTDECKUNG (Discovery!)";
    sigStatus.style.color = "#2ea44f";
    sigBar.style.background = "#2ea44f";
  }
  
  if(!massData.length){
    ctxHist.fillStyle="#8b949e";
    ctxHist.font="10px monospace";
    ctxHist.fillText("WARTEN AUF KOLLISIONSDATEN...",w/2-90,h/2);
    return;
  }
  
  let nb=40,bins=Array(nb).fill(0);
  massData.forEach(v=>{if(v>=mn&&v<mx){let i=Math.floor((v-mn)/(mx-mn)*nb);if(i>=0&&i<nb)bins[i]++;}});
  let maxB=Math.max(...bins,1),bw=(w-40)/nb;
  let fc=isIon?"rgba(227,119,194,0.4)":"rgba(88,166,255,0.4)";
  let tc=isIon?"#e377c2":"#58a6ff";
  for(let i=0;i<nb;i++){
    let bh=bins[i]/maxB*(h-30);let x=30+i*bw,y=h-16-bh;
    ctxHist.fillStyle=fc;ctxHist.fillRect(x,y,bw-1,bh);ctxHist.fillStyle=tc;ctxHist.fillRect(x,y,bw-1,1.5);
  }
  
  if (sig > 0) {
    let alpha = Math.min(1.0, collisions / target);
    ctxHist.save();
    ctxHist.globalAlpha = alpha;
    
    ctxHist.strokeStyle="rgba(248,81,73,1)";
    ctxHist.lineWidth=1.5;
    ctxHist.beginPath();
    for(let xp=30;xp<w-8;xp++){
      let v=mn+(xp-30)/(w-38)*(mx-mn),yv=0;
      if(!isIon){yv=Math.exp(-(v-50)/25)*18+(1/((v-91.2)**2+2.5**2))*300+(1/((v-125)**2+1.6**2))*10;}
      else{yv=4.2+(1/((v-3.1)**2+.15**2))*1.4+(1/((v-9.46)**2+.3**2))*.35;}
      let sc=isIon?6.5:20,yp=h-16-yv/sc*(h-35);yp=Math.max(8,Math.min(h-16,yp));
      xp===30?ctxHist.moveTo(xp,yp):ctxHist.lineTo(xp,yp);
    }
    ctxHist.stroke();
    
    ctxHist.fillStyle="#f0f6fc";
    ctxHist.font="8.5px sans-serif";
    if(!isIon){
      ctxHist.fillText("Z⁰ Boson (91 GeV)",w*.35,22);
      if(selDet === "LHCB") {
        ctxHist.fillText("B-Meson-Physik & CP-Asymmetrie (LHCb)!",w*.58,38);
      } else {
        if(paramEnergy >= 4.0) {
          ctxHist.fillText("Higgs-Boson (125 GeV) - 5σ Entdeckung!",w*.58,38);
        } else {
          ctxHist.fillStyle="rgba(248,81,73,0.6)";
          ctxHist.fillText("Higgs unterdrückt (E < 4 TeV)",w*.58,38);
        }
      }
    } else {
      ctxHist.fillText("J/Ψ (3.1 GeV) - Quark-Gluon-Plasma",w*.15,20);
      ctxHist.fillText("Υ (9.46 GeV)",w*.68,45);
    }
    ctxHist.restore();
  }
  
  if (sig < 5.0) {
    ctxHist.fillStyle="rgba(255,255,255,0.45)";
    ctxHist.font="8.5px monospace";
    if (sig === 0) {
      if (paramEnergy < 4.0 && !isIon && selDet !== "LHCB") {
        ctxHist.fillText("⚠️ Strahlenergie zu gering für Higgs-Produktion (< 4.0 TeV)!", w/2 - 145, 12);
      } else {
        ctxHist.fillText("Keine Kollisionen akkumuliert. Starte Kollisionen!", w/2 - 120, 12);
      }
    } else {
      ctxHist.fillText("Sammle Statistik für Entdeckung (Signifikanz: " + sig.toFixed(1) + "σ / 5.0σ)", w/2 - 140, 12);
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// BUTTON HANDLERS
// ═══════════════════════════════════════════════════════════════════════════
btnB1.addEventListener("click",()=>injectBunch(1));
btnB2.addEventListener("click",()=>injectBunch(2));

btnSpeedToggle.addEventListener("click",()=>{
  isFastMode = !isFastMode;
  if(isFastMode) {
    btnSpeedToggle.innerText = "⏱️ Modus: Zeitraffer (Schnell)";
    btnSpeedToggle.style.background = "rgba(88,166,255,.08)";
    btnSpeedToggle.style.borderColor = "rgba(88,166,255,.3)";
    btnSpeedToggle.style.color = "#58a6ff";
  } else {
    btnSpeedToggle.innerText = "⏱️ Modus: Echtzeit (Didaktisch)";
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
 document.querySelectorAll(".cv4-dtab").forEach(t=>t.classList.remove("act"));
 $("dt-lhcb").classList.add("act"); selDet="LHCB";
 updateReadouts(); drawDetBg(); drawHist();
 setStatus("PRESET GELADEN: CP-Verletzung & Schönheit (B-Physik p-p Kollision bei 13 TeV in LHCb)", "on");
});

btnPrePilot.addEventListener("click",()=>{
 setMode(false); // Protonen
 resetLHC();
 sliEnergy.value = 0.4; paramEnergy = 0.4; lblEnergy.innerText = "0.4 TeV";
 sliIntensity.value = 0.10; paramIntensity = 0.10; lblIntensity.innerText = "0.10e11 p";
 sliBeta.value = 1.5; paramBetaStar = 1.5; lblBeta.innerText = "1.50 m";
 sliRampSpeed.value = 0.02; paramRampSpeed = 0.02; lblRampSpeed.innerText = "0.02 T/s (Sicher)"; lblRampSpeed.style.color = "#58a6ff";
 updateReadouts(); drawDetBg(); drawHist();
 setStatus("PRESET GELADEN: Pilot-Strahl (Inbetriebnahme des LHC auf Injektionsniveau)", "on");
});

btnAutoColl.addEventListener("click", toggleAutoCollide);

btnAuto.addEventListener("click",async()=>{
 if(injecting||ramped||b1Count>=NEEDED||b2Count>=NEEDED||cryoRecovery) return;
 btnAuto.classList.add("off");
 btnB1.classList.add("off");
 btnB2.classList.add("off");
 sliEnergy.disabled = true; // Sperre Parameter während Injektion
 
 // Realistischer Beladungsprozess: Zuerst Beam 1 komplett füllen, danach erst Beam 2!
 setStatus("FÜLLPROTOKOLL GESTARTET: Fülle zuerst Beam 1 (im Uhrzeigersinn)...","on");
 
 for(let i=b1Count; i<NEEDED; i++){
  setStatus(`PROTOKOLL: Fülle LHC Beam 1 (Clockwise) - Bunch ${i+1}/${NEEDED}...`,"on");
  await injectBunch(1);
  if(i < NEEDED - 1) {
    await new Promise(r=>setTimeout(r, getDurations().autoDelay));
  }
 }
 
 await new Promise(r=>setTimeout(r, getDurations().autoDelay * 2));
 setStatus("PROTOKOLL: Beam 1 stabil! Fülle nun Beam 2 (gegen den Uhrzeigersinn)...","on");
 
 for(let i=b2Count; i<NEEDED; i++){
  setStatus(`PROTOKOLL: Fülle LHC Beam 2 (Counter-Clockwise) - Bunch ${i+1}/${NEEDED}...`,"on");
  await injectBunch(2);
  if(i < NEEDED - 1) {
    await new Promise(r=>setTimeout(r, getDurations().autoDelay));
  }
 }
 
 setStatus("FÜLLSCHEMA BEENDET: Beide Strahlen unabhängig gefüllt und stabil! Ramping bereit.","on");
 btnAuto.classList.remove("off");
});

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
</script>"""

html_replaced = html.replace("PLACEHOLDER_PIPE1", pipe1_path).replace("PLACEHOLDER_PIPE2", pipe2_path)
cells.append(code([
    "display(HTML(r'''" + html_replaced.replace("'''","\\'\\'\\'") + "'''))"
]))

# ── CELL 5: Analysis intro ───────────────────────────────────────────────────
cells.append(md([
"## 📈 Post-Kollisions-Analyse",
"",
"Nach zahlreichen Kollisionen analysieren wir das akkumulierte Massenspektrum.",
"Setze `heavy_ion_analysis = True` für Blei-Ionen (J/ψ, Υ) oder `False` für Protonen (Higgs, Z0).",
"",
"> [!TIP]",
"> **Didaktischer Hinweis zur Entdeckung & Statistik**:",
"> Im realen LHC ist das Signal-zu-Rausch-Verhältnis (Signal-to-Background Ratio) für das Higgs-Boson extrem winzig (z.B. ca. 1 zu 1000 im Zerfallskanal H → ZZ* → 4l). Um die Entdeckung in unserem Schul-Bedienfeld innerhalb weniger Sekunden erlebbar zu machen, wurde die statistische Higgs-Kopplungsstärke didaktisch vergrößert. Die Notwendigkeit, eine signifikante Anzahl an Kollisionen (Statistik) zu sammeln, um das Signal über das Rauschen (Fluktuationen) zu heben, bleibt jedoch vollkommen identisch!",
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

os.makedirs(os.path.dirname(NB_PATH), exist_ok=True)
with open(NB_PATH, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

print(f"🎉 Notebook generiert:\n  {NB_PATH}")
