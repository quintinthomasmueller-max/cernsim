import os

file_path = "/Users/andreasmuller/experiments/cernsim/CERN_Visualisierung/scripts/create_notebook.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Define the new, complete and ultra-premium HTML + CSS + JS block
overhauled_html = r"""<div id="cern-v4">
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
</style>

<div class="cv4-hdr">
 <div><span class="cv4-logo">⚛️ CERN CCC</span><span class="cv4-badge">Schaltzentrale v5 - Real Map</span></div>
 <div class="cv4-status"><span class="cv4-dot" id="sdot"></span><span id="stxt">OFFLINE</span></div>
</div>

<div class="cv4-sel">
 <div class="cv4-sel-tab act-p" id="sel-p">🔵 Protonen (LINAC4 → PSB → PS → SPS → LHC)</div>
 <div class="cv4-sel-tab" id="sel-i">🟣 Blei-Ionen (LINAC3 → LEIR → PS → SPS → LHC)</div>
</div>

<div class="cv4-grid">
 <div class="cv4-svg-wrap">
  <svg id="svg" width="700" height="480" viewBox="0 0 700 480" style="background:#090d13">
   <!-- Architectural Grid for tech style -->
   <defs>
    <pattern id="arch-grid" width="30" height="30" patternUnits="userSpaceOnUse">
     <path d="M 30 0 L 0 0 0 30" fill="none" stroke="rgba(255,255,255,0.015)" stroke-width="0.5"/>
    </pattern>
   </defs>
   <rect width="100%" height="100%" fill="url(#arch-grid)" />

   <!-- GEOGRAPHICAL FEATURES -->
   <!-- Geneva Lake (Lac Léman) in top-right -->
   <path d="M 520,0 Q 560,50 620,60 T 700,75 L 700,0 Z" fill="rgba(88,166,255,0.05)" stroke="rgba(88,166,255,0.15)" stroke-width="1.5" />
   <text x="610" y="30" fill="rgba(88,166,255,0.25)" font-size="8px" font-family="monospace">LAC LÉMAN (GENFER SEE)</text>

   <!-- French-Swiss Border (dashed line cutting diagonally) -->
   <path d="M 0,220 L 700,120" stroke="rgba(255,255,255,0.06)" stroke-width="1" stroke-dasharray="6,6" />
   <text x="80" y="200" fill="rgba(255,255,255,0.15)" font-size="7.5px" font-family="monospace" transform="rotate(-8, 80, 200)">STAATSGRENZE SCHWEIZ (CH) - FRANKREICH (FR)</text>

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

   <!-- LHC tunnel (massive ring cx=350 cy=240 r=180) -->
   <circle id="p-lhc" cx="350" cy="240" r="180" class="svg-path svg-lhc"/>

   <!-- STYLISH ACCELERATOR DETECTORS & DETAILS -->
   <!-- RF Cavities on the LHC ring (Point 4) represented as small bright rects -->
   <rect x="340" y="415" width="20" height="10" fill="rgba(255,127,14,0.3)" stroke="#ff7f0e" stroke-width="1" />
   <rect x="340" y="55" width="20" height="10" fill="rgba(255,127,14,0.3)" stroke="#ff7f0e" stroke-width="1" />
   <text x="350" y="435" fill="rgba(255,127,14,0.5)" font-size="6px" font-family="monospace">400 MHz RF</text>

   <!-- Quadrupole focusing triplets near the detectors -->
   <path d="M 330,420 L 370,420" stroke="#2ea44f" stroke-width="3" opacity="0.4" />
   <path d="M 330,60 L 370,60" stroke="#2ea44f" stroke-width="3" opacity="0.4" />
   <path d="M 170,220 L 170,260" stroke="#2ea44f" stroke-width="3" opacity="0.4" />
   <path d="M 530,220 L 530,260" stroke="#2ea44f" stroke-width="3" opacity="0.4" />

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
   <text x="350" y="448" class="svg-lbl" style="fill:#e6edf3;font-weight:bold">ATLAS (IP1)</text>
   <circle id="d-cms" cx="350" cy="60" r="14" class="svg-node"/>
   <text x="350" y="42" class="svg-lbl" style="fill:#e6edf3;font-weight:bold">CMS (IP5)</text>
   <circle id="d-alice" cx="170" cy="240" r="12" class="svg-node"/>
   <text x="134" y="240" class="svg-lbl" style="fill:#e6edf3;font-weight:bold">ALICE (IP2)</text>
   <circle id="d-lhcb" cx="530" cy="240" r="12" class="svg-node"/>
   <text x="567" y="240" class="svg-lbl" style="fill:#e6edf3;font-weight:bold">LHCb (IP8)</text>

   <!-- TI labels -->
   <text x="248" y="186" class="svg-lbl" style="font-size:8px">TI 2</text>
   <text x="485" y="205" class="svg-lbl" style="font-size:8px">TI 8</text>
  </svg>
 </div>

 <div class="cv4-panel">
  <div>
   <div class="cv4-ptitle">🔬 EXPERIMENT-PRESETS (SCHNELLWAHL)</div>
   <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:8px">
    <button class="cv4-btn" id="btn-pre-higgs" style="background:rgba(88,166,255,.12);border-color:#58a6ff;color:#58a6ff;font-size:9.5px;padding:6px 2px">Higgs-Suche (ATLAS/CMS)</button>
    <button class="cv4-btn" id="btn-pre-qgp" style="background:rgba(227,119,194,.12);border-color:#e377c2;color:#e377c2;font-size:9.5px;padding:6px 2px">QGP-Erzeugung (ALICE)</button>
    <button class="cv4-btn" id="btn-pre-lhcb" style="background:rgba(255,127,14,.12);border-color:#ff7f0e;color:#ff7f0e;font-size:9.5px;padding:6px 2px">CP-Verletzung (LHCb)</button>
    <button class="cv4-btn" id="btn-pre-pilot" style="background:rgba(23,190,207,.12);border-color:#17becf;color:#17becf;font-size:9.5px;padding:6px 2px">Pilot-Strahl (Testrun)</button>
   </div>
  </div>

  <div>
   <div class="cv4-ptitle">📡 INJEKTION</div>
   <div style="display:flex;flex-direction:column;gap:6px">
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
</div>"""

# Parse the create_notebook.py file and replace the html variable cleanly
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# We want to replace between html = r\"\"\" and the end \"\"\"
# Let's locate 'html = r\"\"\"' and the closing '\"\"\"'
start_marker = 'html = r"""'
end_marker = '"""'

start_pos = text.find(start_marker)
if start_pos != -1:
    print("Found html variable start!")
    # Find the closing triple quotes after start_pos
    end_pos = text.find(end_marker, start_pos + len(start_marker))
    if end_pos != -1:
        print("Found html variable end!")
        
        # Replace the HTML content
        new_text = text[:start_pos + len(start_marker)] + new_html_content + text[end_pos:]
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_text)
        print("Successfully replaced HTML content in create_notebook.py!")
    else:
        print("Could not find closing triple quotes!")
else:
    print("Could not find html = r\"\"\" start!")

# Now, we also need to bind the new DOM elements (the four preset buttons) in the JS listeners
# Let's write a follow-up Python string replacement to inject the DOM references and click listeners for the presets!
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

dom_target = 'const b1c=$("b1c"),b2c=$("b2c"),b1bar=$("b1bar"),b2bar=$("b2bar"),rbar=$("rbar");'
dom_replacement = 'const b1c=$("b1c"),b2c=$("b2c"),b1bar=$("b1bar"),b2bar=$("b2bar"),rbar=$("rbar");\nconst btnPreHiggs=$("btn-pre-higgs"),btnPreQgp=$("btn-pre-qgp"),btnPreLhcb=$("btn-pre-lhcb"),btnPrePilot=$("btn-pre-pilot");'

if dom_target in text:
    text = text.replace(dom_target, dom_replacement)
    print("Injected DOM references for presets!")

listeners_target = 'btnAuto.addEventListener("click",async()=>{'
listeners_replacement = """// PRESETS CLICK LISTENERS
btnPreHiggs.addEventListener("click",()=>{
 setMode(false); // Protonen
 resetLHC();
 sliEnergy.value = 6.8; paramEnergy = 6.8; lblEnergy.innerText = "6.8 TeV";
 sliIntensity.value = 1.20; paramIntensity = 1.20; lblIntensity.innerText = "1.20e11 p";
 sliBeta.value = 0.3; paramBetaStar = 0.3; lblBeta.innerText = "0.30 m";
 sliRampSpeed.value = 0.06; paramRampSpeed = 0.06; lblRampSpeed.innerText = "0.06 T/s (Sicher)"; lblRampSpeed.style.color = "#58a6ff";
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
 sliRampSpeed.value = 0.06; paramRampSpeed = 0.06; lblRampSpeed.innerText = "0.06 T/s (Sicher)"; lblRampSpeed.style.color = "#58a6ff";
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

btnAuto.addEventListener("click",async()=>{"""

if listeners_target in text:
    text = text.replace(listeners_target, listeners_replacement)
    print("Injected click listeners for presets!")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)
print("Finished overhauling script successfully!")
