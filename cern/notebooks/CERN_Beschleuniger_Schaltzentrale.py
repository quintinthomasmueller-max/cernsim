# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.3
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # ⚛️ CERN-Schaltzentrale & Teilchenphysik-Datenanalyse
# ### Ein interaktives Curriculum für den Begabtenkurs
#
# Dieses Notebook führt durch den **echten Arbeitsablauf der experimentellen Teilchenphysik** —
# von der Beschleunigung über die Kollision bis zur Entdeckung — und nutzt dabei durchgehend
# **echte Open Data des CMS-Experiments** am LHC (Run 2011, √s = 7 TeV).
#
# ## 🎯 Lernziele
# Nach diesem Notebook kannst du …
# 1. erklären, **wie ein Teilchenbeschleuniger** Teilchen auf nahezu Lichtgeschwindigkeit bringt und kollidieren lässt;
# 2. aus gemessenen **Impulsen die invariante Masse** eines Teilchens berechnen (relativistische Kinematik);
# 3. ein **Massenspektrum** lesen und die darin verborgene „Teilchen-Leiter" erkennen;
# 4. eine **Resonanz vermessen** (Masse & Breite per Kurvenanpassung) und mit dem Literaturwert (PDG) vergleichen;
# 5. die **statistische Signifikanz** einer Entdeckung berechnen und das **5σ-Kriterium** begründen;
# 6. den Zusammenhang **Strahlenergie ↔ erreichbare Teilchenmasse** quantifizieren.
#
# ## 🗺️ Fahrplan
# | Teil | Thema |
# |------|-------|
# | **1** | Die Maschine — der Beschleunigerkomplex (interaktives Stellwerk) |
# | **2** | Von Rohdaten zur Masse — die invariante Masse aus 4-Vektoren |
# | **3** | Das Massenspektrum — die Teilchen-Leiter |
# | **4** | Eine Resonanz vermessen — Kurvenanpassung & PDG-Vergleich |
# | **5** | Entdeckung & Signifikanz — das 5σ-Kriterium und der Higgs |
# | **6** | Maschinenphysik — Energie, Magnetfeld und die Reichweite |
# | **7** | Zusammenfassung & Übungen |
#
# > **🔎 Datenehrlichkeit:** Wo echte Messdaten verwendet werden, ist die Quelle angegeben.
# > Wo Daten simuliert sind (z. B. der Higgs-Goldkanal H→ZZ\*→4ℓ), steht es ausdrücklich dabei.
# > Eine Simulation wird nie als Messung ausgegeben.

# %% [markdown]
# ---
# ## Teil 1 · Die Maschine
#
# > **Lernziel:** Verstehen, wie der CERN-Beschleunigerkomplex ein Teilchenpaket („Bunch") stufenweise
# > beschleunigt, im LHC speichert und an den Experimenten zur Kollision bringt.
#
# Ein Collider macht zwei Dinge: Er **beschleunigt** geladene Teilchen mit Hochfrequenz-Feldern und **lenkt**
# sie mit supraleitenden Dipolmagneten auf eine Kreisbahn. Je höher die Energie, desto stärker muss das
# Magnetfeld sein, um die Teilchen auf der Bahn zu halten — das ist später (Teil 6) die zentrale Grenze.
#
# Dasselbe **Teilchenpaket** durchläuft den gesamten realen Pfad:
#
# ### 🔵 Protonen
# **Quelle** → **LINAC 4** (160 MeV) → **PSB** (2 GeV) → **PS** (26 GeV) → **SPS** (450 GeV) → **LHC** (bis 6.8 TeV)
#
# ### 🟣 Blei-Ionen
# **Quelle** → **LINAC 3** (4.2 MeV/u) → **LEIR** (72 MeV/u) → **PS** (5.9 GeV/u) → **SPS** (177 GeV/u) → **LHC** (bis 2.56 TeV/u)
#
# Im **Stellwerk** unten erlebst du diesen Ablauf interaktiv: Teilchenart wählen → Bunches injizieren
# (Beam 1 über TI 2, Beam 2 über TI 8) → auf Kollisionsenergie **rampen** → **Beam Squeeze** → **kollidieren**.
# Die vier **Experiment-Presets** (Higgs/ATLAS·CMS, QGP/ALICE, CP/LHCb, Pilot) stellen je einen realistischen
# Betriebspunkt ein.

# %%
import numpy as np, matplotlib.pyplot as plt, sys, os
from IPython.display import display, HTML
sys.path.append(os.path.abspath('../scripts'))
import cern_utils as cu
cu.apply_cern_style()

# ── Echte CMS-Open-Data laden: Dimuon-Ereignisse MIT vollen 4-Vektoren ──
#    Run2011A DoubleMu, √s = 7 TeV. Repo-Subset (offline-fähig); für die volle
#    Statistik in Zelle 1 LADE_VOLLEN_DATENSATZ=True (lädt ~14 MB von opendata.cern.ch).
EV, INFO = cu.lade_dimuon_4vektoren()
print(f'✅ {INFO["n"]:,} Dimuon-Ereignisse geladen')
print(f'   Quelle: {INFO["quelle"]}')
print(f'   Pro Ereignis: E, p⃗=(px,py,pz), Ladung Q für beide Myonen (+ CMS-Massenspalte M).')
print('⚙️ Bereit. Führe als Nächstes das Stellwerk aus.')

# %% [markdown]
# ### 🎛️ Stellwerk
# Führe die nächste Zelle aus und bediene die Schaltzentrale:
# 1. **Protonen** oder **Blei-Ionen** wählen — oder ein **Experiment-Preset** laden.
# 2. **Füllprotokoll (Autopilot)** für eine automatische, symmetrische Injektion beider Strahlen.
# 3. **Ramping** starten (beschleunigt auf Kollisionsenergie) → **Beam Squeeze** → **Kollidieren**.
# 4. Beobachte **Event-Display** und **Massenspektrum**: jede Kollision ist EIN physikalisches Ereignis,
#    das konsistent im Detektorbild *und* im Histogramm erscheint.
#
# > Falls das Widget nicht reagiert: in JupyterLab das Notebook **„Trust"** (Befehlspalette → *Trust Notebook*)
# > und die Zelle neu ausführen — eingebettetes JavaScript läuft nur in vertrauenswürdigen Notebooks.

# %%
display(HTML(r'''<iframe id="cern-v4-frame" title="CERN Stellwerk" scrolling="no" style="width:100%;height:1040px;border:0;display:block;overflow:hidden;background:#131a24" srcdoc="<!doctype html><html><head><meta charset=&quot;utf-8&quot;><style>html,body{margin:0;background:#131a24}</style></head><body><div id=&quot;cern-v4&quot;>
<style>
/* ═══════════════════════════════════════════════════════════════════════════
   THEME — „aufgehelltes&quot; Dark-Theme: vom Pechschwarz abgehoben, höherer Kontrast,
   rundere/cleanere Karten. Eine zentrale Palette (CSS-Variablen) statt verstreuter
   Farb-Literale. Die Physik-Visualisierungen (SVG-Ring, Canvas) bleiben auf einem
   dunklen „Monitor&quot;-Grund — Spuren/Glow lesen sich dort am besten.
   ─────────────────────────────────────────────────────────────────────────── */
#cern-v4{
  --bg:#131a24;          /* Wurzel-/Seitengrund (aus dem Schwarz gehoben)      */
  --panel:#1c2531;       /* Bedien-Panels                                       */
  --card:#27323f;        /* eingebettete Karten/Buttons                         */
  --screen:#0e141d;      /* Anzeigeflächen (SVG-Karte + Canvas) = „Monitor&quot;     */
  --bd:#3c4a5c;          /* sichtbarere Rahmen                                  */
  --bd-soft:#2d3845;     /* dezente Trennlinien                                 */
  --tx:#e6edf5;          /* Primärtext (heller)                                 */
  --tx-dim:#a3b4c6;      /* Sekundärtext — deutlich kontrastreicher als zuvor    */
  --tx-bright:#f4f8fd;   /* Werte/Headlines                                     */
  --blue:#58a6ff; --green:#2ea44f; --pink:#e377c2; --orange:#ff7f0e;
  --red:#f85149; --cyan:#17becf;
  background:var(--bg);color:var(--tx);
  font-family:-apple-system,'Segoe UI',Roboto,sans-serif;
  border-radius:18px;padding:22px;border:1px solid var(--bd);
  max-width:1100px;margin:0 auto;user-select:none;
}
.cv4-hdr{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--bd-soft);padding-bottom:12px;margin-bottom:14px;gap:10px;flex-wrap:wrap}
.cv4-logo{font-size:20px;font-weight:800;color:var(--blue);letter-spacing:.5px}
.cv4-badge{background:rgba(88,166,255,.12);color:var(--blue);font-size:10px;padding:3px 8px;border-radius:10px;border:1px solid rgba(88,166,255,.25);margin-left:8px}
/* Kurz-Untertitel direkt unter dem Logo (didaktischer Einstieg) */
.cv4-tagline{font-size:11.5px;color:var(--tx-dim);margin:4px 0 14px;line-height:1.45;max-width:760px}
.cv4-tagline b{color:var(--tx)}
.cv4-status{font-size:11px;color:var(--tx-dim);display:flex;align-items:center;gap:6px}
.cv4-dot{width:8px;height:8px;border-radius:50%;background:var(--tx-dim);display:inline-block}
.cv4-dot.on{background:var(--green);box-shadow:0 0 8px var(--green);animation:cv4p 1.5s infinite}
.cv4-dot.danger{background:var(--red);box-shadow:0 0 8px var(--red)}
@keyframes cv4p{0%,100%{opacity:.6;transform:scale(.9)}50%{opacity:1;transform:scale(1.2)}}
.cv4-sel{display:flex;gap:8px;margin-bottom:14px}
.cv4-sel-tab{flex:1;padding:9px;font-size:13px;font-weight:700;text-align:center;border-radius:9px;cursor:pointer;border:1px solid var(--bd);background:var(--card);transition:all .2s}
.cv4-sel-tab:hover{border-color:var(--tx-dim)}
.cv4-sel-tab.act-p{background:rgba(88,166,255,.16);border-color:var(--blue);color:var(--blue)}
.cv4-sel-tab.act-i{background:rgba(227,119,194,.16);border-color:var(--pink);color:var(--pink)}
/* Linke Spalte (.cv4-colL) = Beschleuniger-Ansicht + direkt darunter die Live-
   MESSWERTE; rechts das Bedien-Panel. align-items:start = jede Spalte behält ihre
   Inhaltshöhe. Vorher klaffte unter dem Diagramm eine große Lücke neben dem hohen
   Panel — die Messwerte füllen sie jetzt. */
.cv4-grid{display:grid;grid-template-columns:1fr 320px;gap:18px;align-items:start}
.cv4-colL{display:flex;flex-direction:column;gap:14px;min-width:0}
.cv4-svg-wrap{background:var(--screen);border-radius:14px;border:1px solid var(--bd-soft);display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden}
.cv4-readouts{background:var(--panel);border:1px solid var(--bd);border-radius:16px;padding:12px 16px}
.cv4-rg{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
/* SVG fluid: skaliert über die viewBox (Ring am Handy voll sichtbar). Auf dem
   Desktop füllt es die linke Spalte → größeres Diagramm, weniger Leerraum. */
#svg{width:100%;height:auto;display:block;margin:0 auto}
.cv4-panel{background:var(--panel);border-radius:16px;border:1px solid var(--bd);padding:16px;display:flex;flex-direction:column;gap:16px}
.cv4-ptitle{font-size:11px;text-transform:uppercase;letter-spacing:1px;color:var(--tx-dim);border-bottom:1px solid var(--bd-soft);padding-bottom:6px;margin-bottom:8px;font-weight:700}
.cv4-btn{background:var(--card);color:var(--tx);border:1px solid var(--bd);padding:9px 14px;border-radius:9px;cursor:pointer;font-size:12px;font-weight:600;transition:all .2s;text-align:center}
.cv4-btn:hover{background:#33404f;border-color:var(--tx-dim)}
.cv4-btn.act{background:rgba(88,166,255,.18);border-color:var(--blue);color:var(--blue)}
.cv4-btn.act-i{background:rgba(227,119,194,.18);border-color:var(--pink);color:var(--pink)}
.cv4-btn.danger{background:rgba(248,81,73,.10);border-color:rgba(248,81,73,.45);color:var(--red)}
.cv4-btn.danger:hover{background:rgba(248,81,73,.2);box-shadow:0 0 10px rgba(248,81,73,.25)}
.cv4-btn.off{opacity:.32;pointer-events:none}
.cv4-fill-row{display:flex;align-items:center;gap:8px;font-size:11px;color:var(--tx-dim)}
.cv4-fill-bar{flex:1;background:var(--card);border-radius:4px;height:8px;overflow:hidden}
.cv4-fill-bar-inner{height:100%;transition:width .3s;border-radius:4px}
.cv4-fill-bar-inner.b1{background:var(--blue)}
.cv4-fill-bar-inner.b2{background:var(--orange)}
.cv4-fill-bar-inner.b1i{background:var(--pink)}
.cv4-fill-bar-inner.b2i{background:#c77dff}
.cv4-ro{background:var(--bg);border-radius:8px;border:1px solid var(--bd-soft);padding:8px 10px}
.cv4-ro-l{font-size:9px;color:var(--tx-dim);text-transform:uppercase;letter-spacing:.3px}
.cv4-ro-v{font-size:14px;font-weight:700;color:var(--tx-bright);font-family:'Courier New',monospace}
.cv4-tracker{display:flex;align-items:center;gap:4px;font-size:10px;color:var(--tx-dim);margin-top:6px;flex-wrap:wrap}
.cv4-tracker .step{padding:2px 7px;border-radius:5px;border:1px solid var(--bd-soft);background:var(--bg)}
.cv4-tracker .step.cur{border-color:var(--blue);color:var(--blue);background:rgba(88,166,255,.1)}
.cv4-tracker .step.cur-i{border-color:var(--pink);color:var(--pink);background:rgba(227,119,194,.1)}
.cv4-tracker .step.done{border-color:var(--green);color:var(--green)}
.cv4-tracker .arr{color:var(--bd)}
/* Beschleuniger-Schema: un-beleuchtete Bahn etwas sichtbarer (Laien sollen die
   Struktur schon vor der Animation erkennen); aktiv = heller Glow. */
.svg-path{stroke:#33404f;stroke-width:2.5;fill:none}
.svg-path.lit{stroke:var(--blue);filter:drop-shadow(0 0 5px rgba(88,166,255,.6))}
.svg-path.lit-i{stroke:var(--pink);filter:drop-shadow(0 0 5px rgba(227,119,194,.6))}
.svg-path.lit-b2{stroke:var(--orange);filter:drop-shadow(0 0 5px rgba(255,127,14,.6))}
.svg-lhc{stroke:rgba(120,160,210,.20);stroke-width:4;fill:none}
/* Der LHC-Ring ist riesig (Ø ~360px). Im Betrieb laufen 12 Bunches darüber →
   ein drop-shadow-Filter auf dem Ring würde jeden Frame komplett neu gerastert
   (Haupt-Ursache des Ruckelns). Daher KEIN Filter, Glow nur über die Strichfarbe. */
.svg-lhc.lit{stroke:rgba(88,166,255,.5);filter:none}
.svg-lhc.lit-i{stroke:rgba(227,119,194,.5);filter:none}
/* Bewegte Bunches: billiger Glow per Stroke statt drop-shadow-Filter */
.traveling-dot,.lhc-bunch{stroke-width:2;stroke-opacity:.45;paint-order:stroke}
.svg-node{fill:var(--card);stroke:var(--bd);stroke-width:2}
.svg-node.glow{stroke:var(--blue);fill:rgba(88,166,255,.14);filter:drop-shadow(0 0 6px rgba(88,166,255,.45))}
.svg-node.glow-i{stroke:var(--pink);fill:rgba(227,119,194,.14);filter:drop-shadow(0 0 6px rgba(227,119,194,.45))}
.svg-node.flash{stroke:var(--red);fill:rgba(248,81,73,.2);filter:drop-shadow(0 0 8px rgba(248,81,73,.6))}
.svg-lbl{font-size:9px;fill:#b0bdcc;font-family:monospace;text-anchor:middle}
.cv4-bottom{margin-top:20px;display:grid;grid-template-columns:1fr 1fr;gap:18px}
.cv4-evcanvas{background:var(--screen);border:1px solid var(--bd-soft);border-radius:10px;width:100%;height:190px}
.cv4-histwrap{background:var(--screen);border:1px solid var(--bd-soft);border-radius:10px;height:150px;padding:6px}
.cv4-dtabs{display:flex;gap:4px;margin-bottom:8px}
.cv4-dtab{flex:1;background:var(--card);border:1px solid var(--bd);padding:6px;font-size:10px;color:var(--tx-dim);border-radius:8px;cursor:pointer;text-align:center;font-weight:700;transition:all .15s}
.cv4-dtab:hover{border-color:var(--tx-dim)}
.cv4-dtab.act{background:rgba(88,166,255,.16);border-color:var(--blue);color:var(--blue)}
.cv4-sli-lbl{display:flex;justify-content:space-between;font-size:10.5px;color:var(--tx-dim);margin-top:4px}
.cv4-sli{width:100%;background:var(--card);border-radius:3px;height:5px;outline:none;-webkit-appearance:none;margin-top:3px}
.cv4-sli::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:14px;height:14px;border-radius:50%;background:var(--blue);cursor:pointer;border:1px solid var(--bd)}
.cv4-sli::-moz-range-thumb{width:14px;height:14px;border-radius:50%;background:var(--blue);cursor:pointer;border:1px solid var(--bd)}
.cv4-sli:disabled{opacity:.5}
.cv4-quench{background:rgba(248,81,73,.15);border:1px solid var(--red);color:var(--red);padding:10px;border-radius:8px;font-size:12px;font-weight:bold;text-align:center;animation:cv4blink 1s infinite}
@keyframes cv4blink{0%,100%{opacity:.5}50%{opacity:1}}

/* ═══ MASSENSPEKTRUM-Panel: Texte als HTML UM den Graphen (nicht mehr im Canvas) ═══
   Früher malte drawHist Titel/Herkunft/Status DIREKT über die Balken → unleserlich,
   dunkel. Jetzt: klare HTML-Zeilen ober-/unterhalb, der Canvas zeigt nur das Histogramm. */
.cv4-sp-head{margin-bottom:6px}
.cv4-sp-title{font-size:12px;font-weight:700;line-height:1.3}
.cv4-sp-sub{font-size:10px;color:var(--tx-dim);line-height:1.4;margin-top:2px}
.cv4-sig-row{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:4px;font-size:11px;flex-wrap:wrap}
.cv4-sig-row .lbl-sig{font-family:'Courier New',monospace;color:var(--tx-bright);font-weight:700}
.cv4-sig-status{font-weight:700;font-size:10px}
.cv4-sigbar{height:5px;margin-bottom:8px;background:var(--card);border-radius:3px;overflow:hidden}
.cv4-sigbar>div{width:0;height:100%;background:var(--blue);transition:width .25s,background .25s}
.cv4-sp-foot{margin-top:7px;font-size:9.5px;line-height:1.5;color:var(--tx-dim);display:flex;flex-direction:column;gap:3px}
.cv4-sp-real{color:#aec7e8}
.cv4-sp-status{color:var(--tx)}
.cv4-sp-prov{font-size:8.5px;color:var(--tx-dim);opacity:.85}

/* Geo-Layer braucht keine Pointer-Events und soll bewegte Bunches nicht ausbremsen */
#geo-layer{pointer-events:none}
/* Injektor-Komplex Meyrin: Detail-Beschriftung erst beim Zoom (#svg.inj-zoom),
   im Vollbild stattdessen nur der dezente Hinweis-Ring. */
.geo-inj-detail{opacity:0;transition:opacity .3s}
.geo-inj-hint{opacity:1;transition:opacity .3s}
#svg.inj-zoom .geo-inj-detail{opacity:1}
#svg.inj-zoom .geo-inj-hint{opacity:0}
/* Grobe Vollbild-Labels (PS/PSB/SPS-Zentroide) im Zoom ausblenden — sie wären
   ~20× zu groß; die feinen Ersatz-Labels liefert die Detail-Ebene. */
#svg.inj-zoom .geo-far{opacity:0}
/* Easter Egg FCC: Ring standardmäßig versteckt, erscheint beim Heraus-Zoom. */
.geo-fcc{opacity:0;transition:opacity .8s}
#svg.fcc-on .geo-fcc{opacity:1}
/* Versteckter Auslöser (✦ im See) — klickbar trotz #geo-layer{pointer-events:none}. */
.fcc-trigger{pointer-events:auto;cursor:pointer;transition:fill .2s}
.fcc-trigger:hover{fill:rgba(210,120,255,0.95)}
.info-hit{cursor:pointer;transition:fill 0.18s}
.info-hit:hover{fill:rgba(88,166,255,0.09)!important}
.info-hit-ring{cursor:pointer;transition:stroke 0.18s}
.info-hit-ring:hover{stroke:rgba(88,166,255,0.16)!important}
.cv4-info-panel{position:absolute;top:16px;right:16px;width:256px;background:var(--panel);border:1px solid var(--bd);border-radius:12px;z-index:20;display:none;box-shadow:0 12px 40px rgba(0,0,0,0.6);overflow:hidden;animation:cv4infoin 0.18s ease}
@keyframes cv4infoin{from{opacity:0;transform:scale(0.96) translateY(-4px)}to{opacity:1;transform:none}}
.cv4-info-panel.visible{display:block}
.cv4-hdr-photo{position:relative;height:120px;background:linear-gradient(135deg,#101722,#18222f);overflow:hidden}
.cv4-hdr-photo img{width:100%;height:100%;object-fit:cover;display:block}
.cv4-hdr-shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(28,37,49,0) 45%,rgba(28,37,49,0.9) 100%);border-bottom:3px solid var(--accent);pointer-events:none}
.cv4-hdr-cred{position:absolute;right:5px;bottom:5px;max-width:90%;font-size:7px;font-family:monospace;color:rgba(230,237,243,0.72);text-shadow:0 1px 2px #000;text-align:right;line-height:1.3;pointer-events:none}
.cv4-hdr-fbtxt{display:none;position:absolute;inset:0;align-items:center;justify-content:center;font-size:13px;font-weight:800;letter-spacing:1px;color:var(--accent);opacity:0.55;text-transform:uppercase}
.cv4-hdr-noimg{background:linear-gradient(135deg,#0f1d33,#103057)}
.cv4-hdr-noimg .cv4-hdr-fbtxt{display:flex}
.cv4-info-close{position:absolute;top:7px;right:7px;background:rgba(13,17,23,0.82);border:1px solid var(--bd);color:var(--tx-dim);border-radius:6px;cursor:pointer;padding:1px 7px;font-size:11px;z-index:2;line-height:1.7;transition:all .15s}
.cv4-info-close:hover{color:var(--red);border-color:var(--red)}
.cv4-info-body{padding:10px 13px 13px}
.cv4-info-title{font-size:13.5px;font-weight:800;color:var(--tx-bright);margin-bottom:2px}
.cv4-info-sub{font-size:8.5px;margin-bottom:9px;text-transform:uppercase;letter-spacing:0.4px;line-height:1.4}
.cv4-info-stats-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:5px;margin-bottom:9px}
.cv4-info-stat{background:var(--card);border:1px solid var(--bd-soft);border-radius:6px;padding:4px 6px}
.cv4-info-stat-l{display:block;font-size:7.5px;color:var(--tx-dim);text-transform:uppercase;letter-spacing:0.3px}
.cv4-info-stat-v{display:block;font-size:10px;font-weight:700;font-family:'Courier New',monospace}
.cv4-info-text{font-size:10.5px;color:var(--tx-dim);line-height:1.6}
.cv4-pi-btn{background:none;border:1px solid var(--bd);color:var(--blue);border-radius:5px;cursor:pointer;padding:0 6px;font-size:10px;line-height:1.5;vertical-align:middle;margin-left:3px;transition:all .15s}
.cv4-pi-btn:hover{background:rgba(88,166,255,.12);border-color:var(--blue)}
.cv4-param-info{max-height:0;overflow:hidden;transition:max-height 0.28s ease,padding 0.28s ease,margin 0.28s ease;font-size:10px;color:var(--tx-dim);line-height:1.6;padding:0 9px;margin:0;background:rgba(14,20,29,0.75);border-left:2px solid var(--bd);border-radius:0 0 6px 6px}
.cv4-param-info.open{max-height:240px;overflow:auto;padding:8px 9px;margin-top:4px}

/* ═══ Responsive / Mobile (Eltern-QR: EINE Seite, am Handy nutzbar) ═══════════ */
.cv4-preset-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:7px;margin-bottom:8px}
@media(max-width:860px){
 #cern-v4{padding:13px}
 /* Einspaltig: Diagramm + Messwerte (colL), dann Steuerung. */
 .cv4-grid{grid-template-columns:1fr}
 .cv4-rg{grid-template-columns:1fr 1fr}      /* Messwerte 2×2 statt 4er-Reihe */
 .cv4-hdr{flex-wrap:wrap;gap:8px}
 .cv4-bottom{grid-template-columns:1fr}           /* Event-Display + Spektrum untereinander */
 .cv4-preset-grid{grid-template-columns:1fr 1fr}
 .cv4-sel-tab{font-size:11px;padding:8px 4px}
 /* Info-Panel als zentriertes Modal — sonst vom niedrigen SVG-Wrap geclippt */
 .cv4-info-panel{position:fixed;top:50%;left:50%;right:auto;transform:translate(-50%,-50%);width:min(330px,92vw);max-height:82vh;overflow:auto;z-index:9999}
 #btn-diagram-full{display:block!important}        /* „Großansicht&quot; nur am Handy */
}
/* ═══ Vollbild-Ring (Tippen → Großansicht), CSS-Overlay (iOS-Fullscreen-API unsicher) ═══ */
#btn-diagram-full{display:none}
#cern-v4.diagram-full .cv4-svg-wrap{position:fixed;inset:0;z-index:9998;height:100vh;width:100vw;border-radius:0;background:var(--screen)}
#cern-v4.diagram-full .cv4-svg-wrap #svg{max-width:none;width:auto;height:92vh;max-height:100vh}   /* füllt auch Querformat */
.cv4-fs-hint{display:none;position:absolute;bottom:10px;left:50%;transform:translateX(-50%);font-size:11px;color:var(--tx-dim);background:rgba(14,20,29,.8);padding:4px 12px;border-radius:12px;z-index:9999;pointer-events:none;white-space:nowrap}
#cern-v4.diagram-full .cv4-fs-hint{display:block}
</style>

<div class=&quot;cv4-hdr&quot;>
 <div><span class=&quot;cv4-logo&quot;>⚛️ CERN-Schaltzentrale</span><span class=&quot;cv4-badge&quot;>interaktives Modell</span></div>
 <div style=&quot;display:flex;align-items:center;gap:12px&quot;>
  <button class=&quot;cv4-btn&quot; id=&quot;btn-toggle-geo&quot; style=&quot;padding:5px 9px;font-size:10.5px&quot;>🌍 Reale Ansicht</button>
  <div class=&quot;cv4-status&quot;><span class=&quot;cv4-dot&quot; id=&quot;sdot&quot;></span><span id=&quot;stxt&quot;>OFFLINE</span></div>
 </div>
</div>

<div class=&quot;cv4-tagline&quot;>
 <b>Steuere den größten Teilchenbeschleuniger der Welt.</b> Beschleunige Teilchen fast auf Lichtgeschwindigkeit, bring sie zur Kollision und entdecke daraus neue Teilchen — wie im echten Kontrollzentrum (CCC) am CERN bei Genf.
 <span class=&quot;cv4-pi-btn&quot; data-pi=&quot;introCern&quot;>ⓘ Was ist der CERN?</span>
 <span class=&quot;cv4-pi-btn&quot; data-pi=&quot;introUse&quot;>ⓘ Wie bediene ich das?</span>
</div>
<div class=&quot;cv4-param-info&quot; id=&quot;pi-introCern&quot;></div>
<div class=&quot;cv4-param-info&quot; id=&quot;pi-introUse&quot;></div>

<div class=&quot;cv4-sel&quot;>
  <div class=&quot;cv4-sel-tab act-p&quot; id=&quot;sel-p&quot;>🔵 Protonen-Strahl <span style=&quot;opacity:.65;font-weight:400&quot;>· LINAC4→PSB→PS→SPS→LHC</span></div>
  <div class=&quot;cv4-sel-tab&quot; id=&quot;sel-i&quot;>🟣 Blei-Ionen-Strahl <span style=&quot;opacity:.65;font-weight:400&quot;>· LINAC3→LEIR→PS→SPS→LHC</span></div>
</div>

<div class=&quot;cv4-grid&quot;>
 <!-- Linke Spalte: Beschleuniger-Ansicht + direkt darunter die Live-Messwerte. -->
 <div class=&quot;cv4-colL&quot;>
 <div class=&quot;cv4-svg-wrap&quot;>
  <!-- Interactive Absolute Overlay Reset Zoom Button -->
  <button class=&quot;cv4-btn off&quot; id=&quot;btn-zoom-out&quot; style=&quot;position:absolute;top:12px;left:12px;padding:5px 10px;font-size:10px;background:rgba(28,37,49,0.92);border-color:#3c4a5c;z-index:10;transition:all 0.2s&quot;>🔍 Ansicht zurücksetzen</button>
  <!-- Zoom auf den Injektor-Komplex Meyrin (nur in der Realen Ansicht sichtbar) -->
  <button class=&quot;cv4-btn&quot; id=&quot;btn-zoom-meyrin&quot; style=&quot;position:absolute;bottom:12px;left:12px;padding:5px 10px;font-size:10px;background:rgba(28,37,49,0.92);border-color:#2ea44f;color:#a3b4c6;z-index:10;transition:all 0.2s;display:none&quot;>🔬 Injektor-Komplex (Meyrin)</button>
  <!-- Großansicht/Vollbild des Plans (nur am Handy sichtbar, CSS schaltet display) -->
  <button class=&quot;cv4-btn&quot; id=&quot;btn-diagram-full&quot; style=&quot;position:absolute;top:12px;right:12px;padding:5px 10px;font-size:11px;background:rgba(28,37,49,0.92);border-color:#58a6ff;color:#58a6ff;z-index:9999;transition:all 0.2s&quot;>⛶ Großansicht</button>
  <div class=&quot;cv4-fs-hint&quot;>↻ Querformat zeigt mehr Detail · ⛶ schließt</div>

  <!-- INFO PANEL -->
  <div id=&quot;info-panel&quot; class=&quot;cv4-info-panel&quot;>
   <button class=&quot;cv4-info-close&quot; id=&quot;info-close&quot;>✕</button>
   <div id=&quot;info-hdr&quot;></div>
   <div class=&quot;cv4-info-body&quot;>
    <div class=&quot;cv4-info-title&quot; id=&quot;info-title&quot;></div>
    <div class=&quot;cv4-info-sub&quot; id=&quot;info-sub&quot;></div>
    <div class=&quot;cv4-info-stats-grid&quot; id=&quot;info-stats&quot;></div>
    <div class=&quot;cv4-info-text&quot; id=&quot;info-text&quot;></div>
   </div>
  </div>

  <svg id=&quot;svg&quot; width=&quot;700&quot; height=&quot;480&quot; viewBox=&quot;0 0 700 480&quot; style=&quot;background:#0e141d&quot;><!-- = --screen -->
   <!-- Architectural Grid for tech style -->
   <defs>
    <pattern id=&quot;arch-grid&quot; width=&quot;30&quot; height=&quot;30&quot; patternUnits=&quot;userSpaceOnUse&quot;>
     <path d=&quot;M 30 0 L 0 0 0 30&quot; fill=&quot;none&quot; stroke=&quot;rgba(255,255,255,0.025)&quot; stroke-width=&quot;0.5&quot;/>
    </pattern>
   </defs>
   <rect width=&quot;100%&quot; height=&quot;100%&quot; fill=&quot;url(#arch-grid)&quot; />

   <!-- GEO-OVERLAY (geo-genau, generiert): geo.js füllt #geo-layer beim Boot aus
        cern/app/src/geo.gen.js (reale OSM-Geometrie, Web-Mercator, am LHC-Ring
        ausgerichtet). Toggle/Dimmen via .geo-element. Nord = oben.
        © OpenStreetMap-Mitwirkende (ODbL). -->
   <g id=&quot;geo-layer&quot;></g>

   <!-- SCHEMATIK (Didaktik-Modus): stilisierte, animierte Beschleuniger-Kette.
        Wird im Real-Modus komplett ausgeblendet (geo-layer zeigt dann die echte Lage). -->
   <g id=&quot;schematic&quot;>
   <!-- REAL CERN TOP-VIEW ACCELERATOR STRUCTURE -->
   <!-- LINAC4: straight line injecting into PSB (cx=142, cy=385) -->
   <path id=&quot;p-linac4&quot; d=&quot;M 30,385 L 124,385&quot; class=&quot;svg-path&quot;/>
   <!-- PSB ring cx=142 cy=385 r=18 -->
   <circle id=&quot;p-psb&quot; cx=&quot;142&quot; cy=&quot;385&quot; r=&quot;18&quot; class=&quot;svg-path&quot;/>
   <!-- Transfer PSB→PS: starts at PSB exit angle toward PS, ends at PS entry -->
   <path id=&quot;p-psb-ps&quot; d=&quot;M 157.7,376.2 Q 185,358 206.9,348.6&quot; class=&quot;svg-path&quot;/>

   <!-- LINAC3: straight line ending at LEIR left edge (124,275) -->
   <path id=&quot;p-linac3&quot; d=&quot;M 30,275 L 124,275&quot; class=&quot;svg-path&quot;/>
   <!-- LEIR ring cx=142 cy=275 r=18 -->
   <circle id=&quot;p-leir&quot; cx=&quot;142&quot; cy=&quot;275&quot; r=&quot;18&quot; class=&quot;svg-path&quot;/>
   <!-- Transfer LEIR→PS -->
   <path id=&quot;p-leir-ps&quot; d=&quot;M 157.7,283.8 Q 185,300 206.9,311.4&quot; class=&quot;svg-path&quot;/>

   <!-- PS ring cx=242 cy=332 r=38 -->
   <circle id=&quot;p-ps&quot; cx=&quot;242&quot; cy=&quot;332&quot; r=&quot;38&quot; class=&quot;svg-path&quot;/>
   <!-- Transfer PS→SPS (PS-Austritt → SPS-Eintritt) -->
   <path id=&quot;p-ps-sps&quot; d=&quot;M 279.4,338.5 Q 286,341 293.8,341.1&quot; class=&quot;svg-path&quot;/>

   <!-- SPS ring: kleinerer Ring unten-mittig, tangential zum LHC nahe Punkt 1 (ATLAS) — wie reale Geografie. cx=345 cy=350 r=52 -->
   <circle id=&quot;p-sps&quot; cx=&quot;345&quot; cy=&quot;350&quot; r=&quot;52&quot; class=&quot;svg-path&quot;/>

   <!-- TI 2: SPS → LHC Punkt 2 (unten-links). Kurze Strecke, Tunnel AUSSERHALB des Rings (südl. Bogen, meidet PS). -->
   <path id=&quot;p-ti2&quot; d=&quot;M 293.5,343.0 Q 225,425 193.9,329.6&quot; class=&quot;svg-path&quot;/>
   <!-- TI 8: SPS → LHC Punkt 8 (unten-rechts). Kurze Strecke, Tunnel INNERHALB des Rings. -->
   <path id=&quot;p-ti8&quot; d=&quot;M 394.9,364.5 Q 425,360 459.0,383.2&quot; class=&quot;svg-path&quot;/>

   <!-- Modulated crossover beam vacuum tubes inside the LHC arcs (Double-bore design) -->
    <!-- Beam 1 tube: starts outer at 45°, crosses in detectors -->
    <path id=&quot;lhc-pipe1&quot; class=&quot;geo-element&quot; d=&quot;M 530.00,240.00 L 530.27,246.30 L 530.33,252.61 L 530.15,258.93 L 529.75,265.26 L 529.12,271.58 L 528.25,277.89 L 527.16,284.17 L 525.83,290.42 L 524.26,296.62 L 522.47,302.77 L 520.44,308.86 L 518.17,314.88 L 515.68,320.81 L 512.96,326.65 L 510.01,332.38 L 506.84,338.01 L 503.45,343.51 L 499.85,348.88 L 496.05,354.10 L 492.04,359.18 L 487.83,364.10 L 483.44,368.86 L 478.86,373.44 L 474.10,377.83 L 469.18,382.04 L 464.10,386.05 L 458.88,389.85 L 453.51,393.45 L 448.01,396.84 L 442.38,400.01 L 436.65,402.96 L 430.81,405.68 L 424.88,408.17 L 418.86,410.44 L 412.77,412.47 L 406.62,414.26 L 400.42,415.83 L 394.17,417.16 L 387.89,418.25 L 381.58,419.12 L 375.26,419.75 L 368.93,420.15 L 362.61,420.33 L 356.30,420.27 L 350.00,420.00 L 343.73,419.51 L 337.50,418.80 L 331.30,417.88 L 325.16,416.75 L 319.07,415.41 L 313.04,413.88 L 307.08,412.15 L 301.19,410.23 L 295.38,408.12 L 289.65,405.82 L 284.00,403.35 L 278.45,400.70 L 272.99,397.89 L 267.64,394.90 L 262.38,391.76 L 257.23,388.46 L 252.20,385.00 L 247.27,381.39 L 242.47,377.64 L 237.78,373.74 L 233.22,369.70 L 228.78,365.53 L 224.47,361.22 L 220.30,356.78 L 216.26,352.22 L 212.36,347.53 L 208.61,342.73 L 205.00,337.80 L 201.54,332.77 L 198.24,327.62 L 195.10,322.36 L 192.11,317.01 L 189.30,311.55 L 186.65,306.00 L 184.18,300.35 L 181.88,294.62 L 179.77,288.81 L 177.85,282.92 L 176.12,276.96 L 174.59,270.93 L 173.25,264.84 L 172.12,258.70 L 171.20,252.50 L 170.49,246.27 L 170.00,240.00 L 169.73,233.70 L 169.67,227.39 L 169.85,221.07 L 170.25,214.74 L 170.88,208.42 L 171.75,202.11 L 172.84,195.83 L 174.17,189.58 L 175.74,183.38 L 177.53,177.23 L 179.56,171.14 L 181.83,165.12 L 184.32,159.19 L 187.04,153.35 L 189.99,147.62 L 193.16,141.99 L 196.55,136.49 L 200.15,131.12 L 203.95,125.90 L 207.96,120.82 L 212.17,115.90 L 216.56,111.14 L 221.14,106.56 L 225.90,102.17 L 230.82,97.96 L 235.90,93.95 L 241.12,90.15 L 246.49,86.55 L 251.99,83.16 L 257.62,79.99 L 263.35,77.04 L 269.19,74.32 L 275.12,71.83 L 281.14,69.56 L 287.23,67.53 L 293.38,65.74 L 299.58,64.17 L 305.83,62.84 L 312.11,61.75 L 318.42,60.88 L 324.74,60.25 L 331.07,59.85 L 337.39,59.67 L 343.70,59.73 L 350.00,60.00 L 356.27,60.49 L 362.50,61.20 L 368.70,62.12 L 374.84,63.25 L 380.93,64.59 L 386.96,66.12 L 392.92,67.85 L 398.81,69.77 L 404.62,71.88 L 410.35,74.18 L 416.00,76.65 L 421.55,79.30 L 427.01,82.11 L 432.36,85.10 L 437.62,88.24 L 442.77,91.54 L 447.80,95.00 L 452.73,98.61 L 457.53,102.36 L 462.22,106.26 L 466.78,110.30 L 471.22,114.47 L 475.53,118.78 L 479.70,123.22 L 483.74,127.78 L 487.64,132.47 L 491.39,137.27 L 495.00,142.20 L 498.46,147.23 L 501.76,152.38 L 504.90,157.64 L 507.89,162.99 L 510.70,168.45 L 513.35,174.00 L 515.82,179.65 L 518.12,185.38 L 520.23,191.19 L 522.15,197.08 L 523.88,203.04 L 525.41,209.07 L 526.75,215.16 L 527.88,221.30 L 528.80,227.50 L 529.51,233.73 L 530.00,240.00&quot; stroke=&quot;rgba(88,166,255,0.484)&quot; stroke-width=&quot;1.2&quot; fill=&quot;none&quot; stroke-dasharray=&quot;3,3&quot; style=&quot;transition: opacity 0.3s;&quot; />
    <!-- Beam 2 tube: starts inner at 45°, crosses in detectors -->
    <path id=&quot;lhc-pipe2&quot; class=&quot;geo-element&quot; d=&quot;M 530.00,240.00 L 529.51,246.27 L 528.80,252.50 L 527.88,258.70 L 526.75,264.84 L 525.41,270.93 L 523.88,276.96 L 522.15,282.92 L 520.23,288.81 L 518.12,294.62 L 515.82,300.35 L 513.35,306.00 L 510.70,311.55 L 507.89,317.01 L 504.90,322.36 L 501.76,327.62 L 498.46,332.77 L 495.00,337.80 L 491.39,342.73 L 487.64,347.53 L 483.74,352.22 L 479.70,356.78 L 475.53,361.22 L 471.22,365.53 L 466.78,369.70 L 462.22,373.74 L 457.53,377.64 L 452.73,381.39 L 447.80,385.00 L 442.77,388.46 L 437.62,391.76 L 432.36,394.90 L 427.01,397.89 L 421.55,400.70 L 416.00,403.35 L 410.35,405.82 L 404.62,408.12 L 398.81,410.23 L 392.92,412.15 L 386.96,413.88 L 380.93,415.41 L 374.84,416.75 L 368.70,417.88 L 362.50,418.80 L 356.27,419.51 L 350.00,420.00 L 343.70,420.27 L 337.39,420.33 L 331.07,420.15 L 324.74,419.75 L 318.42,419.12 L 312.11,418.25 L 305.83,417.16 L 299.58,415.83 L 293.38,414.26 L 287.23,412.47 L 281.14,410.44 L 275.12,408.17 L 269.19,405.68 L 263.35,402.96 L 257.62,400.01 L 251.99,396.84 L 246.49,393.45 L 241.12,389.85 L 235.90,386.05 L 230.82,382.04 L 225.90,377.83 L 221.14,373.44 L 216.56,368.86 L 212.17,364.10 L 207.96,359.18 L 203.95,354.10 L 200.15,348.88 L 196.55,343.51 L 193.16,338.01 L 189.99,332.38 L 187.04,326.65 L 184.32,320.81 L 181.83,314.88 L 179.56,308.86 L 177.53,302.77 L 175.74,296.62 L 174.17,290.42 L 172.84,284.17 L 171.75,277.89 L 170.88,271.58 L 170.25,265.26 L 169.85,258.93 L 169.67,252.61 L 169.73,246.30 L 170.00,240.00 L 170.49,233.73 L 171.20,227.50 L 172.12,221.30 L 173.25,215.16 L 174.59,209.07 L 176.12,203.04 L 177.85,197.08 L 179.77,191.19 L 181.88,185.38 L 184.18,179.65 L 186.65,174.00 L 189.30,168.45 L 192.11,162.99 L 195.10,157.64 L 198.24,152.38 L 201.54,147.23 L 205.00,142.20 L 208.61,137.27 L 212.36,132.47 L 216.26,127.78 L 220.30,123.22 L 224.47,118.78 L 228.78,114.47 L 233.22,110.30 L 237.78,106.26 L 242.47,102.36 L 247.27,98.61 L 252.20,95.00 L 257.23,91.54 L 262.38,88.24 L 267.64,85.10 L 272.99,82.11 L 278.45,79.30 L 284.00,76.65 L 289.65,74.18 L 295.38,71.88 L 301.19,69.77 L 307.08,67.85 L 313.04,66.12 L 319.07,64.59 L 325.16,63.25 L 331.30,62.12 L 337.50,61.20 L 343.73,60.49 L 350.00,60.00 L 356.30,59.73 L 362.61,59.67 L 368.93,59.85 L 375.26,60.25 L 381.58,60.88 L 387.89,61.75 L 394.17,62.84 L 400.42,64.17 L 406.62,65.74 L 412.77,67.53 L 418.86,69.56 L 424.88,71.83 L 430.81,74.32 L 436.65,77.04 L 442.38,79.99 L 448.01,83.16 L 453.51,86.55 L 458.88,90.15 L 464.10,93.95 L 469.18,97.96 L 474.10,102.17 L 478.86,106.56 L 483.44,111.14 L 487.83,115.90 L 492.04,120.82 L 496.05,125.90 L 499.85,131.12 L 503.45,136.49 L 506.84,141.99 L 510.01,147.62 L 512.96,153.35 L 515.68,159.19 L 518.17,165.12 L 520.44,171.14 L 522.47,177.23 L 524.26,183.38 L 525.83,189.58 L 527.16,195.83 L 528.25,202.11 L 529.12,208.42 L 529.75,214.74 L 530.15,221.07 L 530.33,227.39 L 530.27,233.70 L 530.00,240.00&quot; stroke=&quot;rgba(255,127,14,0.484)&quot; stroke-width=&quot;1.2&quot; fill=&quot;none&quot; stroke-dasharray=&quot;3,3&quot; style=&quot;transition: opacity 0.3s;&quot; />

   <!-- LHC tunnel (massive average ring cx=350 cy=240 r=180) -->
   <circle id=&quot;p-lhc&quot; cx=&quot;350&quot; cy=&quot;240&quot; r=&quot;180&quot; class=&quot;svg-path svg-lhc&quot;/>

   <!-- STYLISH ACCELERATOR DETECTORS &amp; DETAILS -->
   <!-- RF Cavities on the LHC ring (Point 4) represented as small bright rects -->
   <rect x=&quot;340&quot; y=&quot;415&quot; width=&quot;20&quot; height=&quot;10&quot; fill=&quot;rgba(255,127,14,0.2)&quot; stroke=&quot;#ff7f0e&quot; stroke-width=&quot;1&quot; />
   <rect x=&quot;340&quot; y=&quot;55&quot; width=&quot;20&quot; height=&quot;10&quot; fill=&quot;rgba(255,127,14,0.2)&quot; stroke=&quot;#ff7f0e&quot; stroke-width=&quot;1&quot; />
   <text x=&quot;350&quot; y=&quot;435&quot; fill=&quot;rgba(255,127,14,0.5)&quot; font-size=&quot;6px&quot; font-family=&quot;monospace&quot; text-anchor=&quot;middle&quot;>400 MHz RF</text>

   <!-- Quadrupole focusing triplets near the detectors -->
   <path d=&quot;M 330,420 L 370,420&quot; stroke=&quot;#2ea44f&quot; stroke-width=&quot;3&quot; opacity=&quot;0.3&quot; />
   <path d=&quot;M 330,60 L 370,60&quot; stroke=&quot;#2ea44f&quot; stroke-width=&quot;3&quot; opacity=&quot;0.3&quot; />
   <path d=&quot;M 170,220 L 170,260&quot; stroke=&quot;#2ea44f&quot; stroke-width=&quot;3&quot; opacity=&quot;0.3&quot; />
   <path d=&quot;M 530,220 L 530,260&quot; stroke=&quot;#2ea44f&quot; stroke-width=&quot;3&quot; opacity=&quot;0.3&quot; />

   <!-- Nodes / Labels -->
   <circle id=&quot;n-linac4&quot; cx=&quot;30&quot; cy=&quot;385&quot; r=&quot;5&quot; class=&quot;svg-node&quot;/>
   <text x=&quot;30&quot; y=&quot;405&quot; class=&quot;svg-lbl&quot;>LINAC 4</text>
   <circle id=&quot;n-psb&quot; cx=&quot;142&quot; cy=&quot;385&quot; r=&quot;7&quot; class=&quot;svg-node&quot;/>
   <text x=&quot;142&quot; y=&quot;415&quot; class=&quot;svg-lbl&quot;>PSB</text>

   <circle id=&quot;n-linac3&quot; cx=&quot;30&quot; cy=&quot;275&quot; r=&quot;5&quot; class=&quot;svg-node&quot;/>
   <text x=&quot;30&quot; y=&quot;258&quot; class=&quot;svg-lbl&quot;>LINAC 3</text>
   <circle id=&quot;n-leir&quot; cx=&quot;142&quot; cy=&quot;275&quot; r=&quot;7&quot; class=&quot;svg-node&quot;/>
   <text x=&quot;142&quot; y=&quot;256&quot; class=&quot;svg-lbl&quot;>LEIR</text>

   <circle id=&quot;n-ps&quot; cx=&quot;242&quot; cy=&quot;332&quot; r=&quot;8&quot; class=&quot;svg-node&quot;/>
   <text x=&quot;242&quot; y=&quot;383&quot; class=&quot;svg-lbl&quot;>PS</text>
   <circle id=&quot;n-sps&quot; cx=&quot;345&quot; cy=&quot;350&quot; r=&quot;10&quot; class=&quot;svg-node&quot;/>
   <text x=&quot;345&quot; y=&quot;291&quot; class=&quot;svg-lbl&quot; text-anchor=&quot;middle&quot;>SPS</text>

   <!-- LHC Detector Groups (DIDAKTIK): an den Kardinalpunkten = Überkreuzungen der
        Strahlrohre (lhc-pipe1/2). Der Geo-Modus zeichnet die ECHTEN IP-Lagen separat. -->
   <g id=&quot;grp-atlas&quot; style=&quot;cursor:pointer&quot;>
    <circle id=&quot;d-atlas&quot; cx=&quot;350&quot; cy=&quot;420&quot; r=&quot;14&quot; class=&quot;svg-node&quot;/>
    <text x=&quot;350&quot; y=&quot;448&quot; class=&quot;svg-lbl&quot; style=&quot;fill:#e6edf3;font-weight:bold&quot;>ATLAS (IP1)</text>
   </g>
   <g id=&quot;grp-cms&quot; style=&quot;cursor:pointer&quot;>
    <circle id=&quot;d-cms&quot; cx=&quot;350&quot; cy=&quot;60&quot; r=&quot;14&quot; class=&quot;svg-node&quot;/>
    <text x=&quot;350&quot; y=&quot;42&quot; class=&quot;svg-lbl&quot; style=&quot;fill:#e6edf3;font-weight:bold&quot;>CMS (IP5)</text>
   </g>
   <g id=&quot;grp-alice&quot; style=&quot;cursor:pointer&quot;>
    <circle id=&quot;d-alice&quot; cx=&quot;170&quot; cy=&quot;240&quot; r=&quot;12&quot; class=&quot;svg-node&quot;/>
    <text x=&quot;134&quot; y=&quot;240&quot; class=&quot;svg-lbl&quot; style=&quot;fill:#e6edf3;font-weight:bold&quot;>ALICE (IP2)</text>
   </g>
   <g id=&quot;grp-lhcb&quot; style=&quot;cursor:pointer&quot;>
    <circle id=&quot;d-lhcb&quot; cx=&quot;530&quot; cy=&quot;240&quot; r=&quot;12&quot; class=&quot;svg-node&quot;/>
    <text x=&quot;567&quot; y=&quot;240&quot; class=&quot;svg-lbl&quot; style=&quot;fill:#e6edf3;font-weight:bold&quot;>LHCb (IP8)</text>
   </g>

   <!-- TI labels -->
   <text x=&quot;206&quot; y=&quot;392&quot; class=&quot;svg-lbl&quot; style=&quot;font-size:8px&quot;>TI 2</text>
   <text x=&quot;436&quot; y=&quot;356&quot; class=&quot;svg-lbl&quot; style=&quot;font-size:8px&quot;>TI 8</text>

   <!-- INFO HIT TARGETS — transparent click zones; order = innermost last (highest z in SVG) -->
   <circle id=&quot;hit-lhc&quot; cx=&quot;350&quot; cy=&quot;240&quot; r=&quot;180&quot; fill=&quot;none&quot; stroke=&quot;rgba(88,166,255,0.01)&quot; stroke-width=&quot;22&quot; pointer-events=&quot;stroke&quot; class=&quot;info-hit-ring&quot;/>
   <circle id=&quot;hit-sps&quot; cx=&quot;345&quot; cy=&quot;350&quot; r=&quot;58&quot; fill=&quot;rgba(0,0,0,0.01)&quot; class=&quot;info-hit&quot;/>
   <circle id=&quot;hit-ps&quot;  cx=&quot;242&quot; cy=&quot;332&quot; r=&quot;48&quot; fill=&quot;rgba(0,0,0,0.01)&quot; class=&quot;info-hit&quot;/>
   <circle id=&quot;hit-psb&quot; cx=&quot;142&quot; cy=&quot;390&quot; r=&quot;24&quot; fill=&quot;rgba(0,0,0,0.01)&quot; class=&quot;info-hit&quot;/>
   <circle id=&quot;hit-leir&quot; cx=&quot;142&quot; cy=&quot;265&quot; r=&quot;24&quot; fill=&quot;rgba(0,0,0,0.01)&quot; class=&quot;info-hit&quot;/>
   <circle id=&quot;hit-linac4&quot; cx=&quot;55&quot; cy=&quot;385&quot; r=&quot;32&quot; fill=&quot;rgba(0,0,0,0.01)&quot; class=&quot;info-hit&quot;/>
   <circle id=&quot;hit-linac3&quot; cx=&quot;55&quot; cy=&quot;275&quot; r=&quot;32&quot; fill=&quot;rgba(0,0,0,0.01)&quot; class=&quot;info-hit&quot;/>
   </g><!-- /#schematic -->
  </svg>
 </div>

 <!-- MESSWERTE (LIVE): direkt unter dem Diagramm (linke Spalte) — füllt die Lücke
      neben dem hohen Bedien-Panel. IDs unverändert (engine#updateReadouts). -->
 <div class=&quot;cv4-readouts&quot;>
  <div class=&quot;cv4-ptitle&quot;>📊 MESSWERTE (LIVE)</div>
  <div class=&quot;cv4-rg&quot;>
   <div class=&quot;cv4-ro&quot;><span class=&quot;cv4-ro-l&quot;>Energie/Beam</span><span class=&quot;cv4-ro-v&quot; id=&quot;v-e&quot;>0.00 TeV</span></div>
   <div class=&quot;cv4-ro&quot;><span class=&quot;cv4-ro-l&quot;>Magnetfeld B</span><span class=&quot;cv4-ro-v&quot; id=&quot;v-b&quot;>0.000 T</span></div>
   <div class=&quot;cv4-ro&quot;><span class=&quot;cv4-ro-l&quot;>Lorentz γ</span><span class=&quot;cv4-ro-v&quot; id=&quot;v-g&quot;>1</span></div>
   <div class=&quot;cv4-ro&quot;><span class=&quot;cv4-ro-l&quot;>Teilchen</span><span class=&quot;cv4-ro-v&quot; id=&quot;v-t&quot; style=&quot;color:#58a6ff&quot;>Proton</span></div>
  </div>
 </div>
 </div><!-- /.cv4-colL -->

 <div class=&quot;cv4-panel&quot;>
  <div>
   <div class=&quot;cv4-ptitle&quot;>🔬 EXPERIMENT WÄHLEN — SCHNELLSTART</div>
   <!-- Die 3 realen LHC-Betriebsmodi: pp-Physik (Higgs/Z⁰/CP zusammen) · Schwerionen/QGP · Pilot. -->
   <div class=&quot;cv4-preset-grid&quot;>
    <div><button class=&quot;cv4-btn&quot; id=&quot;btn-pre-pp&quot; style=&quot;background:rgba(88,166,255,.12);border-color:#58a6ff;color:#58a6ff;font-size:10.5px;padding:8px 3px;width:100%&quot;>Protonen-Physik<br><span style=&quot;font-size:8.5px;opacity:.8&quot;>13,6 TeV · Higgs/Z⁰/CP</span> <span class=&quot;cv4-pi-btn&quot; data-pi=&quot;prePp&quot;>ⓘ</span></button><div class=&quot;cv4-param-info&quot; id=&quot;pi-prePp&quot;></div></div>
    <div><button class=&quot;cv4-btn&quot; id=&quot;btn-pre-qgp&quot; style=&quot;background:rgba(227,119,194,.12);border-color:#e377c2;color:#e377c2;font-size:10.5px;padding:8px 3px;width:100%&quot;>Schwerionen / QGP<br><span style=&quot;font-size:8.5px;opacity:.8&quot;>Blei-Ionen · ALICE</span> <span class=&quot;cv4-pi-btn&quot; data-pi=&quot;preQgp&quot;>ⓘ</span></button><div class=&quot;cv4-param-info&quot; id=&quot;pi-preQgp&quot;></div></div>
    <div><button class=&quot;cv4-btn&quot; id=&quot;btn-pre-pilot&quot; style=&quot;background:rgba(23,190,207,.12);border-color:#17becf;color:#17becf;font-size:10.5px;padding:8px 3px;width:100%&quot;>Pilot-Strahl<br><span style=&quot;font-size:8.5px;opacity:.8&quot;>Inbetriebnahme · 0,45 TeV</span> <span class=&quot;cv4-pi-btn&quot; data-pi=&quot;prePilot&quot;>ⓘ</span></button><div class=&quot;cv4-param-info&quot; id=&quot;pi-prePilot&quot;></div></div>
   </div>
  </div>

  <div>
   <div class=&quot;cv4-ptitle&quot;>📡 SCHRITT 1 — STRAHL FÜLLEN</div>
   <div style=&quot;display:flex;flex-direction:column;gap:6px&quot;>
    <button class=&quot;cv4-btn&quot; id=&quot;btn-speed-toggle&quot; style=&quot;background:rgba(88,166,255,.08);border-color:rgba(88,166,255,.3);color:#58a6ff;font-size:10.5px;padding:6px 4px;margin-bottom:2px&quot;>⏱️ Tempo: Zeitraffer · 1 s ≈ 40 s real</button>
    <button class=&quot;cv4-btn&quot; id=&quot;btn-auto&quot; style=&quot;background:rgba(46,164,79,.15);border-color:#2ea44f;color:#2ea44f&quot;>⚙️ Füllprotokoll starten</button>
   </div>
   <div class=&quot;cv4-tracker&quot; id=&quot;tracker&quot;>
    <span class=&quot;step&quot; id=&quot;tr-src&quot;>Quelle</span><span class=&quot;arr&quot;>→</span>
    <span class=&quot;step&quot; id=&quot;tr-inj&quot;>PSB</span><span class=&quot;arr&quot;>→</span>
    <span class=&quot;step&quot; id=&quot;tr-ps&quot;>PS</span><span class=&quot;arr&quot;>→</span>
    <span class=&quot;step&quot; id=&quot;tr-sps&quot;>SPS</span><span class=&quot;arr&quot;>→</span>
    <span class=&quot;step&quot; id=&quot;tr-lhc&quot;>LHC</span>
   </div>
  </div>

  <div>
   <div class=&quot;cv4-ptitle&quot;>🔋 LHC-FÜLLSTAND</div>
   <div style=&quot;font-size:8.5px;color:#8b949e;margin:-2px 0 4px;line-height:1.35&quot;>1 Punkt = 1 PS-Batch (72 B). Das SPS bündelt bis 4 Batches zu 1 Zug (288 B) → ~10 Züge füllen den LHC (Pb-Ionen: nur 592 B)</div>
   <div class=&quot;cv4-fill-row&quot;><span style=&quot;width:108px;font-size:9.5px&quot;>B1 <span id=&quot;b1c&quot;>0 / 2.808</span></span><div class=&quot;cv4-fill-bar&quot;><div class=&quot;cv4-fill-bar-inner b1&quot; id=&quot;b1bar&quot; style=&quot;width:0%&quot;></div></div></div>
   <div class=&quot;cv4-fill-row&quot; style=&quot;margin-top:4px&quot;><span style=&quot;width:108px;font-size:9.5px&quot;>B2 <span id=&quot;b2c&quot;>0 / 2.808</span></span><div class=&quot;cv4-fill-bar&quot;><div class=&quot;cv4-fill-bar-inner b2&quot; id=&quot;b2bar&quot; style=&quot;width:0%&quot;></div></div></div>
  </div>

  <div>
   <div class=&quot;cv4-ptitle&quot;>🎛️ BETRIEBSPARAMETER (CCC)</div>

   <div class=&quot;cv4-sli-lbl&quot;><span>Ziel-Energie: <button class=&quot;cv4-pi-btn&quot; data-pi=&quot;energy&quot;>ⓘ</button></span><span id=&quot;lbl-energy&quot;>6.8 TeV</span></div>
   <div class=&quot;cv4-param-info&quot; id=&quot;pi-energy&quot;></div>
   <input type=&quot;range&quot; class=&quot;cv4-sli&quot; id=&quot;sli-energy&quot; min=&quot;0.45&quot; max=&quot;7.0&quot; step=&quot;0.05&quot; value=&quot;6.8&quot;>

   <div class=&quot;cv4-sli-lbl&quot; style=&quot;margin-top:8px&quot;><span>Bunch-Intensität: <button class=&quot;cv4-pi-btn&quot; data-pi=&quot;intensity&quot;>ⓘ</button></span><span id=&quot;lbl-intensity&quot;>1.15e11 p</span></div>
   <div class=&quot;cv4-param-info&quot; id=&quot;pi-intensity&quot;></div>
   <input type=&quot;range&quot; class=&quot;cv4-sli&quot; id=&quot;sli-intensity&quot; min=&quot;0.1&quot; max=&quot;1.8&quot; step=&quot;0.05&quot; value=&quot;1.15&quot;>

   <div class=&quot;cv4-sli-lbl&quot; style=&quot;margin-top:8px&quot;><span>Strahl-Fokus β*: <button class=&quot;cv4-pi-btn&quot; data-pi=&quot;beta&quot;>ⓘ</button></span><span id=&quot;lbl-beta&quot;>1.50 m</span></div>
   <div class=&quot;cv4-param-info&quot; id=&quot;pi-beta&quot;></div>
   <input type=&quot;range&quot; class=&quot;cv4-sli&quot; id=&quot;sli-beta&quot; min=&quot;0.3&quot; max=&quot;1.5&quot; step=&quot;0.1&quot; value=&quot;1.5&quot; disabled>

   <div class=&quot;cv4-sli-lbl&quot; style=&quot;margin-top:8px&quot;><span>Ramp-Rate dB/dt: <button class=&quot;cv4-pi-btn&quot; data-pi=&quot;rampspeed&quot;>ⓘ</button></span><span id=&quot;lbl-rampspeed&quot; style=&quot;color:#58a6ff&quot;>0.05 T/s (Sicher)</span></div>
   <div class=&quot;cv4-param-info&quot; id=&quot;pi-rampspeed&quot;></div>
   <input type=&quot;range&quot; class=&quot;cv4-sli&quot; id=&quot;sli-rampspeed&quot; min=&quot;0.02&quot; max=&quot;0.15&quot; step=&quot;0.01&quot; value=&quot;0.05&quot;>
  </div>

  <div>
   <div class=&quot;cv4-ptitle&quot;>⚡ SCHRITT 2 — BESCHLEUNIGEN &amp; KOLLIDIEREN</div>
   <div style=&quot;display:flex;flex-direction:column;gap:6px&quot;>
    <button class=&quot;cv4-btn off&quot; id=&quot;btn-ramp&quot;>🚀 Energie-Ramping starten</button>
    <div><button class=&quot;cv4-pi-btn&quot; data-pi=&quot;ramp&quot; style=&quot;font-size:9px&quot;>ⓘ Was ist Energie-Ramping?</button><div class=&quot;cv4-param-info&quot; id=&quot;pi-ramp&quot;></div></div>
    <div class=&quot;cv4-fill-row&quot;><span style=&quot;width:50px;font-size:10px&quot;>Ramp</span><div class=&quot;cv4-fill-bar&quot;><div class=&quot;cv4-fill-bar-inner b1&quot; id=&quot;rbar&quot; style=&quot;width:0%&quot;></div></div></div>
    <button class=&quot;cv4-btn off&quot; id=&quot;btn-squeeze&quot; style=&quot;background:rgba(23,190,207,.15);border-color:#17becf;color:#17becf&quot;>🗜️ Beam Squeeze starten (β*)</button>
    <div><button class=&quot;cv4-pi-btn&quot; data-pi=&quot;squeeze&quot; style=&quot;font-size:9px&quot;>ⓘ Was ist der Beam Squeeze?</button><div class=&quot;cv4-param-info&quot; id=&quot;pi-squeeze&quot;></div></div>
    <div style=&quot;display:flex;gap:4px&quot;>
     <button class=&quot;cv4-btn danger off&quot; id=&quot;btn-coll&quot; style=&quot;flex:1;font-size:10.5px;padding:9px 2px&quot;>💥 Kollision (manuell)</button>
     <button class=&quot;cv4-btn off&quot; id=&quot;btn-autocoll&quot; style=&quot;flex:1.2;background:rgba(248,81,73,.08);border-color:rgba(248,81,73,.4);color:#f85149;font-size:10.5px;padding:9px 2px&quot;>▶️ Auto-Datennahme</button>
    </div>
   </div>
  </div>

 </div>
</div>

<div class=&quot;cv4-bottom&quot;>
 <div>
  <div class=&quot;cv4-ptitle&quot;>📸 EVENT-DISPLAY — EINE KOLLISION <span class=&quot;cv4-pi-btn&quot; data-pi=&quot;evRead&quot; style=&quot;float:right&quot;>ⓘ Bild lesen</span></div>
  <div class=&quot;cv4-param-info&quot; id=&quot;pi-evRead&quot;></div>
  <div class=&quot;cv4-dtabs&quot;>
   <div class=&quot;cv4-dtab act&quot; id=&quot;dt-atlas&quot;>ATLAS</div>
   <div class=&quot;cv4-dtab&quot; id=&quot;dt-cms&quot;>CMS</div>
   <div class=&quot;cv4-dtab&quot; id=&quot;dt-alice&quot;>ALICE</div>
   <div class=&quot;cv4-dtab&quot; id=&quot;dt-lhcb&quot;>LHCb</div>
  </div>
  <canvas class=&quot;cv4-evcanvas&quot; id=&quot;cv-ev&quot;></canvas>
  <div class=&quot;cv4-sp-foot&quot;><div id=&quot;ev-caption&quot;></div></div>
 </div>
 <div>
  <div class=&quot;cv4-ptitle&quot;>📊 MASSENSPEKTRUM — TEILCHEN WIEGEN <span class=&quot;cv4-pi-btn&quot; data-pi=&quot;spRead&quot; style=&quot;float:right&quot;>ⓘ Diagramm lesen</span></div>
  <div class=&quot;cv4-param-info&quot; id=&quot;pi-spRead&quot;></div>
  <div class=&quot;cv4-sp-head&quot;>
   <div class=&quot;cv4-sp-title&quot; id=&quot;sp-title&quot;>—</div>
   <div class=&quot;cv4-sp-sub&quot; id=&quot;sp-sub&quot;></div>
  </div>
  <div class=&quot;cv4-sig-row&quot;>
   <span>Signifikanz: <strong class=&quot;lbl-sig&quot; id=&quot;lbl-sig&quot;>0.00 σ</strong></span>
   <span class=&quot;cv4-sig-status&quot; id=&quot;lbl-sig-status&quot;>Sammle Statistik …</span>
  </div>
  <div class=&quot;cv4-sigbar&quot;><div id=&quot;sig-bar&quot;></div></div>
  <div class=&quot;cv4-histwrap&quot;><canvas id=&quot;cv-hist&quot; style=&quot;width:100%;height:100%&quot;></canvas></div>
  <div class=&quot;cv4-sp-foot&quot;>
   <div id=&quot;sp-info&quot;>0 Kandidaten</div>
   <div class=&quot;cv4-sp-status&quot; id=&quot;sp-status&quot;></div>
   <div class=&quot;cv4-sp-real&quot; id=&quot;sp-real&quot;></div>
   <div class=&quot;cv4-sp-prov&quot; id=&quot;sp-prov&quot;></div>
  </div>
 </div>
</div>

<script>(() => {
  // cern/app/src/core.js
  var FILL = {
    proton: { total: 2808, psBatch: 72, batchesPerTrain: 4 },
    ion: { total: 592, psBatch: 37, batchesPerTrain: 2 }
  };
  var REAL_SPS_CYCLE_S = 25;
  var SIM_SCALE = { slow: 15, fast: 40 };
  var DT_SCALE = { slow: 900, fast: 2e3 };
  var BEAM_LIFETIME_H = 15;
  var DUMP_FRAC = 0.35;
  var STAT_RATE = 0.04;
  var App = {
    state: {},
    // mutable Querschnittsvariablen (state.js füllt via Object.assign)
    els: {},
    // DOM-Referenzen (main.js#initDom befüllt sie bei Boot)
    g: {}
    // SVG-Geometrie: { R, J, paths, nodes, svg } (geometry.js + boot)
    // öffentliche Funktionen registrieren die Module hier (App.setStatus, App.drawHist, …)
  };
  var $ = (id) => document.getElementById(id);
  var SVG_NS = &quot;http://www.w3.org/2000/svg&quot;;
  var sleep = (ms) => new Promise((r) => setTimeout(r, ms));

  // cern/app/src/geometry.js
  var R = {
    PSB: { cx: 142, cy: 385, r: 18 },
    LEIR: { cx: 142, cy: 275, r: 18 },
    PS: { cx: 242, cy: 332, r: 38 },
    SPS: { cx: 345, cy: 350, r: 52 },
    LHC: { cx: 350, cy: 240, r: 180 }
  };
  var J = {
    PSB_ENTRY: Math.PI,
    // von LINAC (links)
    PSB_EXIT: Math.atan2(R.PS.cy - R.PSB.cy, R.PS.cx - R.PSB.cx),
    // → PS ≈-0.51
    LEIR_ENTRY: Math.PI,
    LEIR_EXIT: Math.atan2(R.PS.cy - R.LEIR.cy, R.PS.cx - R.LEIR.cx),
    // → PS ≈0.51
    PS_FROM_PSB: Math.atan2(R.PSB.cy - R.PS.cy, R.PSB.cx - R.PS.cx),
    // von PSB ≈2.63
    PS_FROM_LEIR: Math.atan2(R.LEIR.cy - R.PS.cy, R.LEIR.cx - R.PS.cx),
    // von LEIR ≈-2.63→3.65
    PS_EXIT: Math.atan2(R.SPS.cy - R.PS.cy, R.SPS.cx - R.PS.cx),
    // → SPS ≈0.17
    SPS_ENTRY: Math.atan2(R.PS.cy - R.SPS.cy, R.PS.cx - R.SPS.cx),
    // von PS ≈-2.97
    SPS_TI2: Math.atan2(329.6 - R.SPS.cy, 193.9 - R.SPS.cx),
    // → LHC Punkt 2 (unten-links) ≈-3.01
    SPS_TI8: Math.atan2(383.2 - R.SPS.cy, 459 - R.SPS.cx),
    // → LHC Punkt 8 (unten-rechts) ≈0.28
    LHC_ALICE: Math.PI,
    // ALICE bei 180° (links)
    LHC_LHCB: 0
    // LHCb bei 0° (rechts)
  };
  App.g.R = R;
  App.g.J = J;

  // cern/app/src/state.js
  Object.assign(App.state, {
    isIon: false,
    ramped: false,
    filling: false,
    b1Count: 0,
    b2Count: 0,
    // umlaufende Züge je Strahl
    b1Batches: 0,
    b2Batches: 0,
    // angekommene PS-Batches je Strahl (→ Bunches-Anzeige)
    collisions: 0,
    dtElapsed: 0,
    intensity0: 0,
    intensityNow: 0,
    // Datennahme: vergangene reale Zeit + Strahl-Intensität (Burn-off)
    dumping: false,
    // Strahl-Dump läuft (gated Kollisionen/Neustart bis zum Reset)
    fillGen: 0,
    // Füll-Generation (Zombie-Batch-Schutz bei Reset+Neustart)
    spsDots: { b1: [], b2: [] },
    spsAngle: 0,
    spsRunning: false,
    spsLastT: null,
    // im SPS akkumulierende Batches
    lhcDots: { b1: [], b2: [] },
    lhcSpeed: 78e-4,
    // rad/ms bei Injektionsenergie (Proton)
    lhcAngle: 0,
    lhcRunning: false,
    lhcLastT: null,
    lhcEnergy: 450,
    // GeV
    // Per-Detektor-Datenspeicher: jeder Detektor akkumuliert NUR sein eigenes Spektrum.
    massStore: { ATLAS: [], CMS: [], ALICE: [], LHCB: [] },
    collStore: { ATLAS: 0, CMS: 0, ALICE: 0, LHCB: 0 },
    // Kandidaten je Detektor (Signifikanz ∝ √)
    histAcc: { ATLAS: 0, CMS: 0, ALICE: 0, LHCB: 0 },
    // Bruchteil-Akku fürs Histogramm je Detektor
    histSeen: { ATLAS: 0, CMS: 0, ALICE: 0, LHCB: 0 },
    // gesehene Einträge (Reservoir-Sampling am HIST_CAP)
    lastEvent: null,
    goldenEvent: null,
    higgsCands: 0,
    selDet: &quot;ATLAS&quot;,
    isFastMode: true,
    // CCC-Operator-Parameter
    paramEnergy: 6.8,
    // Ziel-Energie (TeV)
    paramIntensity: 1.15,
    // Bunch-Intensität (10^11 Protonen)
    paramBetaStar: 1.5,
    // Strahlgröße am IP (m)
    paramRampSpeed: 0.05,
    // Magnetfeld-Ramp-Rate (T/s)
    squeezing: false,
    squeezed: false,
    cryoRecovery: false,
    autoCollInterval: null,
    // Ablaufsteuerung (vormals implizite Globals im IIFE-Closure)
    resetFlag: false,
    // Canvas-Maße / High-DPI (dpr bei Boot aus window.devicePixelRatio gesetzt)
    dpr: 1,
    evW: 340,
    evH: 180,
    histW: 340,
    histH: 130
  });
  var STAGE_VPX = { linac: 0.3, ring1: 0.34, trToPs: 0.4, ps: 0.46, trToSps: 0.54, sps: 0.66, ti: 0.82 };
  function getStageVel(key) {
    const s5 = App.state;
    const ion = s5.isIon ? 0.72 : 1;
    return (STAGE_VPX[key] || 0.5) * ion / App.timeScale();
  }
  App.getStageVel = getStageVel;

  // cern/app/src/engine.js
  var s = App.state;
  var E = App.els;
  var g = App.g;
  var fc = () => s.isIon ? FILL.ion : FILL.proton;
  var totalBatches = () => Math.round(fc().total / fc().psBatch);
  var trainsTotal = () => Math.ceil(totalBatches() / fc().batchesPerTrain);
  var fillLabel = (batches) => `${(batches * fc().psBatch).toLocaleString(&quot;de-DE&quot;)} / ${fc().total.toLocaleString(&quot;de-DE&quot;)}`;
  var simScale = () => s.isFastMode ? SIM_SCALE.fast : SIM_SCALE.slow;
  var trainCadenceMs = () => REAL_SPS_CYCLE_S * 1e3 / simScale();
  function fitCanvas(cv, ctx, fbW, fbH) {
    const w = cv.clientWidth || fbW, h = cv.clientHeight || fbH;
    const bw = Math.round(w * s.dpr), bh = Math.round(h * s.dpr);
    if (cv.width !== bw) cv.width = bw;
    if (cv.height !== bh) cv.height = bh;
    ctx.resetTransform ? ctx.resetTransform() : ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.scale(s.dpr, s.dpr);
    return { w, h };
  }
  function resizeCanvases() {
    const ev = fitCanvas(E.cvEv, E.ctxEv, 340, 180);
    s.evW = ev.w;
    s.evH = ev.h;
    const hi = fitCanvas(E.cvHist, E.ctxHist, 340, 130);
    s.histW = hi.w;
    s.histH = hi.h;
  }
  function fmtEnergy(v) {
    return v.toFixed(2) + (s.isIon ? &quot; TeV/u&quot; : &quot; TeV&quot;);
  }
  App.fmtEnergy = fmtEnergy;
  function setMode(ion) {
    if (s.isIon === ion &amp;&amp; s.b1Count === 0 &amp;&amp; s.b2Count === 0) return;
    s.isIon = ion;
    E.selP.className = &quot;cv4-sel-tab&quot; + (ion ? &quot;&quot; : &quot; act-p&quot;);
    E.selI.className = &quot;cv4-sel-tab&quot; + (ion ? &quot; act-i&quot; : &quot;&quot;);
    E.vT.innerText = ion ? &quot;Pb\u2078\xB2\u207A&quot; : &quot;Proton&quot;;
    E.vT.style.color = ion ? &quot;#e377c2&quot; : &quot;#58a6ff&quot;;
    E.trInj.innerText = ion ? &quot;LEIR&quot; : &quot;PSB&quot;;
    E.b1bar.className = &quot;cv4-fill-bar-inner &quot; + (ion ? &quot;b1i&quot; : &quot;b1&quot;);
    E.b2bar.className = &quot;cv4-fill-bar-inner &quot; + (ion ? &quot;b2i&quot; : &quot;b2&quot;);
    E.sliEnergy.max = ion ? 2.8 : 7;
    if (ion &amp;&amp; s.paramEnergy > 2.76) {
      s.paramEnergy = 2.76;
      E.sliEnergy.value = 2.76;
    }
    E.lblEnergy.innerText = fmtEnergy(s.paramEnergy);
    if (ion) {
      document.querySelectorAll(&quot;.cv4-dtab&quot;).forEach((t) => t.classList.remove(&quot;act&quot;));
      $(&quot;dt-alice&quot;).classList.add(&quot;act&quot;);
      s.selDet = &quot;ALICE&quot;;
    }
    resetLHC();
    App.drawDetBg();
    App.drawHist();
  }
  function resetLHC(keepData = false) {
    s.resetFlag = true;
    s.fillGen = (s.fillGen || 0) + 1;
    s.dumping = false;
    stopAutoCollide();
    document.querySelectorAll(&quot;.traveling-dot&quot;).forEach((d) => d.remove());
    E.btnAuto.classList.remove(&quot;off&quot;);
    s.filling = false;
    clearIllum();
    s.lhcDots.b1.forEach((d) => d.el.remove());
    s.lhcDots.b2.forEach((d) => d.el.remove());
    s.spsRunning = false;
    s.spsDots.b1.forEach((d) => d.el.remove());
    s.spsDots.b2.forEach((d) => d.el.remove());
    s.spsDots = { b1: [], b2: [] };
    s.lhcDots = { b1: [], b2: [] };
    s.b1Count = 0;
    s.b2Count = 0;
    s.b1Batches = 0;
    s.b2Batches = 0;
    if (!keepData) {
      s.collisions = 0;
      App.resetSpectrumData();
      E.spInfo.innerText = `Kandidaten (${s.selDet}): 0`;
    }
    s.dtElapsed = 0;
    s.intensityNow = 0;
    E.lblIntensity.innerText = s.paramIntensity.toFixed(2) + &quot;e11 p&quot;;
    s.ramped = false;
    s.squeezed = false;
    s.squeezing = false;
    s.lhcEnergy = s.isIon ? 177 : 450;
    s.lhcSpeed = s.isIon ? 5e-3 : 78e-4;
    s.paramBetaStar = 1.5;
    E.b1c.innerText = fillLabel(0);
    E.b2c.innerText = fillLabel(0);
    E.b1bar.style.width = &quot;0%&quot;;
    E.b2bar.style.width = &quot;0%&quot;;
    E.rbar.style.width = &quot;0%&quot;;
    E.btnRamp.classList.add(&quot;off&quot;);
    E.btnSqueeze.classList.add(&quot;off&quot;);
    E.btnColl.classList.add(&quot;off&quot;);
    E.btnAutoColl.classList.add(&quot;off&quot;);
    E.sliEnergy.disabled = false;
    E.sliIntensity.disabled = false;
    E.sliBeta.value = 1.5;
    E.sliBeta.disabled = true;
    E.sliRampSpeed.disabled = false;
    E.lblBeta.innerText = &quot;1.50 m&quot;;
    updateReadouts();
    Object.values(g.paths).forEach((p) => {
      p.classList.remove(&quot;lit&quot;, &quot;lit-i&quot;, &quot;lit-b2&quot;);
    });
    Object.values(g.nodes).forEach((n) => {
      n.classList.remove(&quot;glow&quot;, &quot;glow-i&quot;, &quot;flash&quot;);
    });
    g.paths.lhc.classList.remove(&quot;lit&quot;, &quot;lit-i&quot;);
    setStatus(&quot;BEREIT&quot;, &quot;on&quot;);
  }
  async function moveAlongPath(dot, pathEl, vpx, abort) {
    return new Promise((res) => {
      const len = pathEl.__len || (pathEl.__len = pathEl.getTotalLength());
      const dur = Math.max(1, len / vpx);
      let t0 = null;
      function step(ts) {
        if (abort &amp;&amp; abort()) {
          res();
          return;
        }
        if (!t0) t0 = ts;
        let p = Math.min((ts - t0) / dur, 1);
        let pt = pathEl.getPointAtLength(p * len);
        dot.setAttribute(&quot;cx&quot;, pt.x);
        dot.setAttribute(&quot;cy&quot;, pt.y);
        p < 1 ? requestAnimationFrame(step) : res();
      }
      requestAnimationFrame(step);
    });
  }
  async function orbitRing(dot, ring, entryA, exitA, orbits, vpx, abort) {
    let partial = ((exitA - entryA) % (2 * Math.PI) + 2 * Math.PI) % (2 * Math.PI);
    let totalA = orbits * 2 * Math.PI + partial;
    const dur = Math.max(1, ring.r * totalA / vpx);
    return new Promise((res) => {
      let t0 = null;
      function step(ts) {
        if (abort &amp;&amp; abort()) {
          res();
          return;
        }
        if (!t0) t0 = ts;
        let p = Math.min((ts - t0) / dur, 1);
        let a = entryA + p * totalA;
        dot.setAttribute(&quot;cx&quot;, ring.cx + ring.r * Math.cos(a));
        dot.setAttribute(&quot;cy&quot;, ring.cy + ring.r * Math.sin(a));
        p < 1 ? requestAnimationFrame(step) : res();
      }
      requestAnimationFrame(step);
    });
  }
  function timeScale() {
    return s.isFastMode ? 1 : 2.6;
  }
  var _pathRC = /* @__PURE__ */ new Map();
  var _nodeRC = /* @__PURE__ */ new Map();
  var _stageRC = [0, 0, 0, 0];
  function litClass() {
    return s.isIon ? &quot;lit-i&quot; : &quot;lit&quot;;
  }
  function glowClass() {
    return s.isIon ? &quot;glow-i&quot; : &quot;glow&quot;;
  }
  function enterPath(el) {
    if (!el) return;
    _pathRC.set(el, (_pathRC.get(el) || 0) + 1);
    el.classList.add(litClass());
  }
  function leavePath(el) {
    if (!el) return;
    const n = (_pathRC.get(el) || 0) - 1;
    _pathRC.set(el, Math.max(0, n));
    if (n <= 0) el.classList.remove(&quot;lit&quot;, &quot;lit-i&quot;, &quot;lit-b2&quot;);
  }
  function enterNode(el) {
    if (!el) return;
    _nodeRC.set(el, (_nodeRC.get(el) || 0) + 1);
    el.classList.add(glowClass());
  }
  function leaveNode(el) {
    if (!el) return;
    const n = (_nodeRC.get(el) || 0) - 1;
    _nodeRC.set(el, Math.max(0, n));
    if (n <= 0) el.classList.remove(&quot;glow&quot;, &quot;glow-i&quot;);
  }
  function renderTracker() {
    g.trSteps.forEach((st, i) => {
      st.classList.remove(&quot;cur&quot;, &quot;cur-i&quot;, &quot;done&quot;);
      if (i < 4 &amp;&amp; _stageRC[i] > 0) st.classList.add(s.isIon ? &quot;cur-i&quot; : &quot;cur&quot;);
    });
    if (g.trSteps[4] &amp;&amp; (s.b1Count > 0 || s.b2Count > 0)) g.trSteps[4].classList.add(s.isIon ? &quot;cur-i&quot; : &quot;cur&quot;);
  }
  function stageEnter(i) {
    _stageRC[i]++;
    renderTracker();
  }
  function stageLeave(i) {
    _stageRC[i] = Math.max(0, _stageRC[i] - 1);
    renderTracker();
  }
  function clearIllum() {
    _pathRC.clear();
    _nodeRC.clear();
    for (let i = 0; i < 4; i++) _stageRC[i] = 0;
    Object.values(g.paths).forEach((p) => {
      if (p) p.classList.remove(&quot;lit&quot;, &quot;lit-i&quot;, &quot;lit-b2&quot;);
    });
    Object.values(g.nodes).forEach((n) => {
      if (n) n.classList.remove(&quot;glow&quot;, &quot;glow-i&quot;);
    });
    g.trSteps.forEach((st) => st.classList.remove(&quot;cur&quot;, &quot;cur-i&quot;, &quot;done&quot;));
  }
  function runAborted(gen) {
    return s.resetFlag || gen !== s.fillGen;
  }
  async function flowStep(dot, pathEl, nodeEl, stageIdx, velKey, ringArgs, gen) {
    if (runAborted(gen)) return false;
    const abort = () => runAborted(gen);
    if (stageIdx != null) stageEnter(stageIdx);
    if (nodeEl) enterNode(nodeEl);
    enterPath(pathEl);
    if (ringArgs) await orbitRing(dot, ringArgs[0], ringArgs[1], ringArgs[2], ringArgs[3], App.getStageVel(velKey), abort);
    else await moveAlongPath(dot, pathEl, App.getStageVel(velKey), abort);
    leavePath(pathEl);
    if (nodeEl) leaveNode(nodeEl);
    if (stageIdx != null) stageLeave(stageIdx);
    return !runAborted(gen);
  }
  function beamColor(beam) {
    const ion = s.isIon;
    return beam === 1 ? ion ? &quot;#e377c2&quot; : &quot;#58a6ff&quot; : ion ? &quot;#c77dff&quot; : &quot;#ff7f0e&quot;;
  }
  function newDot(beam, r) {
    const dot = document.createElementNS(SVG_NS, &quot;circle&quot;);
    dot.setAttribute(&quot;class&quot;, &quot;traveling-dot&quot;);
    dot.setAttribute(&quot;r&quot;, r);
    const c = beamColor(beam);
    dot.setAttribute(&quot;fill&quot;, c);
    dot.setAttribute(&quot;stroke&quot;, c);
    (E.schematic || E.svg).appendChild(dot);
    return dot;
  }
  function pulseNode(n) {
    if (!n) return;
    n.classList.add(&quot;flash&quot;);
    setTimeout(() => n.classList.remove(&quot;flash&quot;), 200);
  }
  function countBatch(beam) {
    const tot = totalBatches();
    if (beam === 1) {
      s.b1Batches++;
      E.b1c.innerText = fillLabel(s.b1Batches);
      E.b1bar.style.width = Math.min(1, s.b1Batches / tot) * 100 + &quot;%&quot;;
    } else {
      s.b2Batches++;
      E.b2c.innerText = fillLabel(s.b2Batches);
      E.b2bar.style.width = Math.min(1, s.b2Batches / tot) * 100 + &quot;%&quot;;
    }
  }
  async function injectBatch(beam, parked, gen) {
    const ion = s.isIon, R3 = g.R, J2 = g.J, paths = g.paths, nodes = g.nodes;
    const dot = newDot(beam, &quot;3.2&quot;);
    const fin = () => {
      dot.remove();
    };
    const lp = ion ? paths.linac3 : paths.linac4, ln = ion ? nodes.linac3 : nodes.linac4;
    if (!await flowStep(dot, lp, ln, 0, &quot;linac&quot;, null, gen)) return fin();
    const r1 = ion ? R3.LEIR : R3.PSB, r1p = ion ? paths.leir : paths.psb, r1n = ion ? nodes.leir : nodes.psb;
    const r1e = ion ? J2.LEIR_ENTRY : J2.PSB_ENTRY, r1x = ion ? J2.LEIR_EXIT : J2.PSB_EXIT;
    if (!await flowStep(dot, r1p, r1n, 1, &quot;ring1&quot;, [r1, r1e, r1x, 3], gen)) return fin();
    if (!await flowStep(dot, ion ? paths.leirPs : paths.psbPs, null, null, &quot;trToPs&quot;, null, gen)) return fin();
    const psE = ion ? J2.PS_FROM_LEIR : J2.PS_FROM_PSB;
    if (!await flowStep(dot, paths.ps, nodes.ps, 2, &quot;ps&quot;, [R3.PS, psE, J2.PS_EXIT, 3], gen)) return fin();
    if (!await flowStep(dot, paths.psSps, null, null, &quot;trToSps&quot;, null, gen)) return fin();
    if (runAborted(gen)) return fin();
    const key = beam === 1 ? &quot;b1&quot; : &quot;b2&quot;;
    const rec = { el: dot, off: s.spsDots[key].length * 0.7 };
    s.spsDots[key].push(rec);
    parked.push(rec);
    stageEnter(3);
    enterNode(nodes.sps);
    pulseNode(nodes.sps);
    startSpsLoop();
    countBatch(beam);
  }
  async function fuseTrain(beam, parked, gen) {
    const R3 = g.R, J2 = g.J, paths = g.paths, nodes = g.nodes, key = beam === 1 ? &quot;b1&quot; : &quot;b2&quot;;
    pulseNode(nodes.sps);
    parked.forEach((rec) => {
      rec.el.remove();
      stageLeave(3);
      leaveNode(nodes.sps);
      const i = s.spsDots[key].indexOf(rec);
      if (i >= 0) s.spsDots[key].splice(i, 1);
    });
    parked.length = 0;
    if (runAborted(gen)) return;
    const train = newDot(beam, &quot;4.2&quot;);
    train.setAttribute(&quot;cx&quot;, R3.SPS.cx + R3.SPS.r * Math.cos(J2.SPS_ENTRY));
    train.setAttribute(&quot;cy&quot;, R3.SPS.cy + R3.SPS.r * Math.sin(J2.SPS_ENTRY));
    const spsExit = beam === 1 ? J2.SPS_TI2 : J2.SPS_TI8;
    if (!await flowStep(train, paths.sps, nodes.sps, 3, &quot;sps&quot;, [R3.SPS, J2.SPS_ENTRY, spsExit, 1], gen)) {
      train.remove();
      return;
    }
    if (!await flowStep(train, beam === 1 ? paths.ti2 : paths.ti8, null, null, &quot;ti&quot;, null, gen)) {
      train.remove();
      return;
    }
    train.remove();
    addPermanentDot(beam);
    if (beam === 1) s.b1Count++;
    else s.b2Count++;
    paths.lhc.classList.add(s.isIon ? &quot;lit-i&quot; : &quot;lit&quot;);
    renderTracker();
  }
  async function injectTrain(beam, nBatches, gen) {
    if (gen == null) gen = s.fillGen;
    if (runAborted(gen)) return;
    const parked = [], proms = [], sub = trainCadenceMs() / fc().batchesPerTrain;
    for (let i = 0; i < nBatches; i++) {
      if (runAborted(gen)) break;
      proms.push(injectBatch(beam, parked, gen));
      if (i < nBatches - 1) await sleep(sub);
    }
    await Promise.all(proms);
    if (runAborted(gen)) {
      parked.forEach((rec) => rec.el.remove());
      return;
    }
    await fuseTrain(beam, parked, gen);
  }
  async function doRamp() {
    if (s.ramped || s.filling || s.cryoRecovery) return;
    E.btnRamp.classList.add(&quot;off&quot;);
    E.btnAuto.classList.add(&quot;off&quot;);
    E.sliEnergy.disabled = true;
    E.sliIntensity.disabled = true;
    E.sliRampSpeed.disabled = true;
    setStatus(&quot;RAMPING MAGNETFELD &amp; ENERGIE...&quot;, &quot;on&quot;);
    const startE = s.isIon ? 177 : 450;
    const maxE = s.isIon ? 2760 : 7e3;
    const targetE = Math.max(s.paramEnergy * 1e3, startE);
    const startSpeed = s.isIon ? 5e-3 : 78e-4;
    const fullSpeed = s.isIon ? 95e-4 : 0.015;
    const eFrac = Math.max(0, Math.min(1, (targetE - startE) / (maxE - startE)));
    const targetSpeed = startSpeed + eFrac * (fullSpeed - startSpeed);
    const dur = 200 / s.paramRampSpeed * timeScale();
    const risk = s.paramRampSpeed > 0.1 ? Math.min(0.95, (s.paramRampSpeed - 0.1) * 16 + 0.14) : 0;
    const quenchAt = risk > 0 &amp;&amp; Math.random() < risk ? 0.25 + Math.random() * 0.65 : Infinity;
    let t0 = null;
    let quenched = false;
    await new Promise((res) => {
      function step(ts) {
        if (!t0) t0 = ts;
        let p = Math.min((ts - t0) / dur, 1);
        if (p > quenchAt) {
          quenched = true;
          res();
          return;
        }
        s.lhcEnergy = startE + p * (targetE - startE);
        s.lhcSpeed = startSpeed + p * (targetSpeed - startSpeed);
        E.rbar.style.width = p * 100 + &quot;%&quot;;
        updateReadouts();
        p < 1 ? requestAnimationFrame(step) : res();
      }
      requestAnimationFrame(step);
    });
    if (quenched) {
      triggerQuench();
      return;
    }
    s.ramped = true;
    E.btnSqueeze.classList.remove(&quot;off&quot;);
    E.sliBeta.disabled = false;
    setStatus(&quot;RAMPING BEENDET \u2014 Squeeze-Phase einleiten!&quot;, &quot;on&quot;);
  }
  function triggerQuench() {
    s.cryoRecovery = true;
    stopAutoCollide();
    setStatus(&quot;\u{1F4A5} MAGNET-QUENCH DETEKTIERT! T > 1.9 K - Strahl gedumpt!&quot;, &quot;danger&quot;);
    E.sdot.className = &quot;cv4-dot flash&quot;;
    E.svg.style.transition = &quot;filter 0.5s&quot;;
    E.svg.style.filter = &quot;sepia(1) saturate(3) hue-rotate(320deg)&quot;;
    let secLeft = 5;
    function cryoTick() {
      if (secLeft > 0) {
        setStatus(`\u{1F4A5} MAGNET-QUENCH! Helium-K\xFChlung l\xE4uft... (${secLeft}s)`, &quot;danger&quot;);
        secLeft--;
        setTimeout(cryoTick, 1e3);
      } else {
        E.svg.style.filter = &quot;none&quot;;
        s.cryoRecovery = false;
        resetLHC();
        setStatus(&quot;K\xDCHLUNG ERFOLGREICH \u2014 LHC BEREIT&quot;, &quot;on&quot;);
      }
    }
    cryoTick();
  }
  async function doSqueeze() {
    if (!s.ramped || s.squeezed || s.squeezing || s.cryoRecovery) return;
    s.squeezing = true;
    E.btnSqueeze.classList.add(&quot;off&quot;);
    E.sliBeta.disabled = true;
    setStatus(&quot;\u{1F5DC}\uFE0F BEAM SQUEEZE: Fokussiere Strahlen an den IPs...&quot;, &quot;on&quot;);
    let t0 = null;
    const dur = 2e3;
    const targetBeta = parseFloat(E.sliBeta.value);
    await new Promise((res) => {
      function step(ts) {
        if (!t0) t0 = ts;
        let p = Math.min((ts - t0) / dur, 1);
        s.paramBetaStar = 1.5 - p * (1.5 - targetBeta);
        E.lblBeta.innerText = s.paramBetaStar.toFixed(2) + &quot; m&quot;;
        p < 1 ? requestAnimationFrame(step) : res();
      }
      requestAnimationFrame(step);
    });
    s.squeezing = false;
    s.squeezed = true;
    E.btnColl.classList.remove(&quot;off&quot;);
    E.btnAutoColl.classList.remove(&quot;off&quot;);
    [g.nodes.atlas, g.nodes.cms, g.nodes.alice, g.nodes.lhcb].forEach((n) => n.classList.add(&quot;glow&quot;));
    g.paths.lhc.classList.add(s.isIon ? &quot;lit-i&quot; : &quot;lit&quot;);
    setStatus(&quot;STABLE BEAMS \u2014 Strahlen fokussiert! Kollisionen bereit.&quot;, &quot;on&quot;);
  }
  function addPermanentDot(beam) {
    const key = beam === 1 ? &quot;b1&quot; : &quot;b2&quot;;
    const existing = s.lhcDots[key].length;
    const angleOffset = existing * (2 * Math.PI / trainsTotal());
    const dot = document.createElementNS(SVG_NS, &quot;circle&quot;);
    dot.setAttribute(&quot;class&quot;, &quot;lhc-bunch&quot;);
    dot.setAttribute(&quot;r&quot;, &quot;3.5&quot;);
    let c = beam === 1 ? s.isIon ? &quot;#e377c2&quot; : &quot;#58a6ff&quot; : s.isIon ? &quot;#c77dff&quot; : &quot;#ff7f0e&quot;;
    dot.setAttribute(&quot;fill&quot;, c);
    dot.setAttribute(&quot;stroke&quot;, c);
    (E.schematic || E.svg).appendChild(dot);
    s.lhcDots[key].push({ el: dot, off: angleOffset });
    if (!s.lhcRunning) startLHCLoop();
  }
  function startSpsLoop() {
    if (s.spsRunning) return;
    s.spsRunning = true;
    s.spsLastT = null;
    const R3 = g.R;
    function frame(ts) {
      if (!s.spsLastT) s.spsLastT = ts;
      let dt = ts - s.spsLastT;
      s.spsLastT = ts;
      s.spsAngle += App.getStageVel(&quot;sps&quot;) / R3.SPS.r * dt;
      const place = (arr, dir) => arr.forEach((d) => {
        const a = dir * s.spsAngle + d.off;
        d.el.setAttribute(&quot;cx&quot;, R3.SPS.cx + R3.SPS.r * Math.cos(a));
        d.el.setAttribute(&quot;cy&quot;, R3.SPS.cy + R3.SPS.r * Math.sin(a));
      });
      place(s.spsDots.b1, 1);
      place(s.spsDots.b2, -1);
      if (s.spsRunning &amp;&amp; (s.spsDots.b1.length || s.spsDots.b2.length)) requestAnimationFrame(frame);
      else s.spsRunning = false;
    }
    requestAnimationFrame(frame);
  }
  function startLHCLoop() {
    s.lhcRunning = true;
    s.lhcLastT = null;
    const R3 = g.R;
    function frame(ts) {
      if (!s.lhcLastT) s.lhcLastT = ts;
      let dt = ts - s.lhcLastT;
      s.lhcLastT = ts;
      s.lhcAngle += s.lhcSpeed / timeScale() * dt;
      s.lhcDots.b1.forEach((d) => {
        let a = s.lhcAngle + d.off;
        let r = 180 + 5.5 * Math.sin(a * 2);
        d.el.setAttribute(&quot;cx&quot;, R3.LHC.cx + r * Math.cos(a));
        d.el.setAttribute(&quot;cy&quot;, R3.LHC.cy + r * Math.sin(a));
      });
      s.lhcDots.b2.forEach((d) => {
        let a = -s.lhcAngle + d.off;
        let r = 180 - 5.5 * Math.sin(a * 2);
        d.el.setAttribute(&quot;cx&quot;, R3.LHC.cx + r * Math.cos(a));
        d.el.setAttribute(&quot;cy&quot;, R3.LHC.cy + r * Math.sin(a));
      });
      if (s.lhcRunning) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }
  function doCollide() {
    if (!s.ramped || !s.squeezed || s.cryoRecovery || s.dumping) return;
    s.collisions += 1;
    E.spInfo.innerText = `Kandidaten (${s.selDet}): ${Math.round(s.collisions).toLocaleString(&quot;de-DE&quot;)}`;
    let detNode = g.nodes[s.selDet.toLowerCase()];
    if (detNode) {
      detNode.classList.add(&quot;flash&quot;);
      setTimeout(() => detNode.classList.remove(&quot;flash&quot;), 350);
    }
    App.drawCollisionEvent(App.generateMassData());
    App.drawHist();
  }
  function toggleAutoCollide() {
    if (s.autoCollInterval) stopAutoCollide();
    else startAutoCollide();
  }
  var dtScale = () => s.isFastMode ? DT_SCALE.fast : DT_SCALE.slow;
  var dtLabel = () => s.isFastMode ? &quot;33 min&quot; : &quot;15 min&quot;;
  function startAutoCollide() {
    if (!s.ramped || !s.squeezed || s.cryoRecovery || s.dumping) return;
    E.btnAutoColl.innerText = &quot;\u23F8\uFE0F Datennahme stoppen&quot;;
    E.btnAutoColl.classList.add(&quot;act&quot;);
    E.btnColl.classList.add(&quot;off&quot;);
    if (s.dtElapsed === 0) s.intensity0 = s.paramIntensity;
    setStatus(`DATENNAHME (1 s \u2248 ${dtLabel()} real) \u2014 Burn-off l\xE4uft \u2026`, &quot;on&quot;);
    const tau = BEAM_LIFETIME_H * 3600;
    let lastTick = performance.now();
    s.autoCollInterval = setInterval(() => {
      if (s.cryoRecovery) {
        stopAutoCollide();
        return;
      }
      const now = performance.now();
      const dDisp = Math.min(0.5, (now - lastTick) / 1e3);
      lastTick = now;
      const dReal = dDisp * dtScale();
      s.dtElapsed += dReal;
      const frac = Math.exp(-s.dtElapsed / tau);
      const L = frac * frac;
      s.intensityNow = s.intensity0 * frac;
      E.lblIntensity.innerText = s.intensityNow.toFixed(2) + &quot;e11 p&quot;;
      const op = (0.2 + 0.8 * frac).toFixed(3);
      s.lhcDots.b1.forEach((d) => d.el.setAttribute(&quot;opacity&quot;, op));
      s.lhcDots.b2.forEach((d) => d.el.setAttribute(&quot;opacity&quot;, op));
      const ref = s.isIon ? { I: 0.9, b: 0.5 } : { I: 1.4, b: 0.3 };
      const lumiF = Math.pow((s.intensity0 || ref.I) / ref.I, 2) * (ref.b / Math.max(0.05, s.paramBetaStar));
      App.liveDetectors().forEach((d) => {
        const dCand = STAT_RATE * L * lumiF * dReal * App.detRate(d);
        s.collStore[d] += dCand;
        s.histAcc[d] += dCand;
        const whole = Math.floor(s.histAcc[d]);
        if (whole > 0) {
          s.histAcc[d] -= whole;
          App.accumulateStatsFor(d, whole);
        }
      });
      s.collisions = s.collStore[s.selDet];
      if (Math.random() < L) {
        let detNode = g.nodes[s.selDet.toLowerCase()];
        if (detNode) {
          detNode.classList.add(&quot;flash&quot;);
          setTimeout(() => detNode.classList.remove(&quot;flash&quot;), 75);
        }
        s.lastEvent = App.sampleEvent();
        App.drawCollisionEvent(s.lastEvent);
      }
      App.drawHist();
      E.spInfo.innerText = `Kandidaten (${s.selDet}): ${Math.round(s.collStore[s.selDet]).toLocaleString(&quot;de-DE&quot;)} \xB7 L ${Math.round(L * 100)} %`;
      setStatus(`\u{1F4C9} DATENNAHME (1 s \u2248 ${dtLabel()} real) \u2014 N ${s.intensityNow.toFixed(2)}e11 (${Math.round(frac * 100)} %) \xB7 L ${Math.round(L * 100)} %`, &quot;on&quot;);
      if (frac <= DUMP_FRAC) beamDump();
    }, 125);
  }
  function beamDump() {
    s.dumping = true;
    stopAutoCollide();
    setStatus(`\u{1F4A5} STRAHL-DUMP \u2014 N < ${Math.round(DUMP_FRAC * 100)} % (L < ${Math.round(DUMP_FRAC * DUMP_FRAC * 100)} %): Strahl verbraucht, neuer Fill n\xF6tig.`, &quot;danger&quot;);
    setTimeout(() => {
      if (!s.cryoRecovery) {
        resetLHC(true);
        setStatus(&quot;STRAHL GEDUMPT \u2014 Daten bleiben. F\xFCllprotokoll f\xFCr n\xE4chsten Fill starten.&quot;, &quot;on&quot;);
      }
    }, 1600);
  }
  function stopAutoCollide() {
    const had = !!s.autoCollInterval;
    if (had) {
      clearInterval(s.autoCollInterval);
      s.autoCollInterval = null;
    }
    E.btnAutoColl.innerText = &quot;\u25B6\uFE0F Auto-Datennahme&quot;;
    E.btnAutoColl.classList.remove(&quot;act&quot;);
    if (had &amp;&amp; !s.dumping) setStatus(&quot;DATENNAHME PAUSIERT \u2014 Burn-off-Uhr l\xE4uft beim Fortsetzen weiter&quot;, &quot;on&quot;);
    if (s.ramped &amp;&amp; s.squeezed &amp;&amp; !s.cryoRecovery &amp;&amp; !s.dumping) E.btnColl.classList.remove(&quot;off&quot;);
  }
  function updateReadouts() {
    E.vE.innerText = (s.lhcEnergy / 1e3).toFixed(2) + &quot; TeV&quot; + (s.isIon ? &quot;/u&quot; : &quot;&quot;);
    let rig = 0.299792458 * 2803.95;
    let B = (s.isIon ? 208 / 82 : 1) * s.lhcEnergy / rig;
    E.vB.innerText = B.toFixed(3) + &quot; T&quot;;
    let gam = s.lhcEnergy / (s.isIon ? 0.9315 : 0.938272);
    E.vG.innerText = Math.round(gam).toLocaleString(&quot;de-DE&quot;);
  }
  function setStatus(txt, cls) {
    E.stxt.innerText = txt;
    E.sdot.className = &quot;cv4-dot &quot; + cls;
  }
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
  function wireEngine() {
    E.selP.addEventListener(&quot;click&quot;, () => {
      if (s.filling) return;
      setMode(false);
    });
    E.selI.addEventListener(&quot;click&quot;, () => {
      if (s.filling) return;
      setMode(true);
    });
    E.btnRamp.addEventListener(&quot;click&quot;, doRamp);
    E.btnSqueeze.addEventListener(&quot;click&quot;, doSqueeze);
    E.btnColl.addEventListener(&quot;click&quot;, doCollide);
    E.cvEv.addEventListener(&quot;click&quot;, () => {
      if (s.goldenEvent) {
        s.goldenEvent = null;
      } else if (s.lastEvent &amp;&amp; s.lastEvent.signal) {
        s.goldenEvent = s.lastEvent;
      }
      App.drawCollisionEvent(s.lastEvent);
    });
    E.cvEv.style.cursor = &quot;pointer&quot;;
  }

  // cern/app/src/display.js
  var s2 = App.state;
  var E2 = App.els;
  var DETKONFIG = {
    // bend = visuelle Krümmungsstärke (skaliert mit B-Feld: CMS 3.8T > ATLAS 2T > ALICE 0.5T)
    ATLAS: {
      typ: &quot;barrel&quot;,
      farbe: &quot;#58a6ff&quot;,
      rolle: &quot;Allzweck \xB7 2T Solenoid + Toroid-Myon-System&quot;,
      bend: 0.8,
      lagen: [
        { r: 26, name: &quot;Spur&quot;, kind: &quot;track&quot; },
        { r: 38, name: &quot;EM&quot;, kind: &quot;em&quot; },
        { r: 52, name: &quot;HAD&quot;, kind: &quot;had&quot; },
        { r: 62, name: &quot;Toroid&quot;, kind: &quot;coil&quot; },
        { r: 86, name: &quot;\u03BC-Kammer&quot;, kind: &quot;muon&quot; }
      ]
    },
    CMS: {
      typ: &quot;barrel&quot;,
      farbe: &quot;#f85149&quot;,
      rolle: &quot;kompakt \xB7 3.8 T Solenoid \xB7 Kristall-ECAL&quot;,
      bend: 1.4,
      lagen: [
        { r: 30, name: &quot;Tracker&quot;, kind: &quot;track&quot; },
        { r: 40, name: &quot;ECAL&quot;, kind: &quot;em&quot; },
        { r: 52, name: &quot;HCAL&quot;, kind: &quot;had&quot; },
        { r: 60, name: &quot;Solenoid&quot;, kind: &quot;coil&quot; },
        { r: 86, name: &quot;\u03BC-Joch&quot;, kind: &quot;muon&quot; }
      ]
    },
    ALICE: {
      typ: &quot;barrel&quot;,
      farbe: &quot;#e377c2&quot;,
      rolle: &quot;Schwerionen \xB7 TPC \xB7 hohe Multiplizit\xE4t \xB7 0.5T&quot;,
      bend: 0.6,
      lagen: [
        { r: 14, name: &quot;ITS&quot;, kind: &quot;track&quot; },
        { r: 58, name: &quot;TPC&quot;, kind: &quot;track&quot; },
        { r: 70, name: &quot;TOF&quot;, kind: &quot;em&quot; },
        { r: 86, name: &quot;Au\xDFen&quot;, kind: &quot;muon&quot; }
      ]
    },
    LHCB: {
      typ: &quot;forward&quot;,
      farbe: &quot;#ff7f0e&quot;,
      rolle: &quot;Vorw\xE4rtsspektrometer \xB7 Sekund\xE4rvertex&quot;,
      stationen: [
        { x: 34, name: &quot;VELO&quot;, kind: &quot;vtx&quot; },
        { x: 80, name: &quot;RICH1&quot;, kind: &quot;rich&quot; },
        { x: 120, name: &quot;TT&quot;, kind: &quot;track&quot; },
        { x: 160, name: &quot;Dipol&quot;, kind: &quot;magnet&quot; },
        { x: 210, name: &quot;RICH2&quot;, kind: &quot;rich&quot; },
        { x: 250, name: &quot;ECAL&quot;, kind: &quot;em&quot; },
        { x: 285, name: &quot;HCAL&quot;, kind: &quot;had&quot; },
        { x: 315, name: &quot;Myon&quot;, kind: &quot;muon&quot; }
      ]
    }
  };
  function layerColor(k) {
    return {
      track: &quot;rgba(88,166,255,0.32)&quot;,
      em: &quot;rgba(46,164,79,0.34)&quot;,
      had: &quot;rgba(255,127,14,0.30)&quot;,
      coil: &quot;rgba(139,148,158,0.42)&quot;,
      muon: &quot;rgba(248,81,73,0.34)&quot;,
      vtx: &quot;rgba(255,255,255,0.45)&quot;,
      rich: &quot;rgba(88,166,255,0.18)&quot;,
      magnet: &quot;rgba(241,224,90,0.5)&quot;
    }[k] || &quot;rgba(139,148,158,0.25)&quot;;
  }
  function detGeo() {
    const cx = s2.evW / 2, cy = s2.evH / 2, Rmax = Math.min(cx, cy) - 6, D = DETKONFIG[s2.selDet] || DETKONFIG.ATLAS;
    return { D, cx, cy, Rmax, sc: Rmax / 86 };
  }
  function evProvenance() {
    const ion = s2.isIon;
    if (s2.selDet === &quot;CMS&quot; &amp;&amp; !ion) return &quot;4\u2113-Kinematik &amp; -Masse: ECHTE CMS-Open-Data (Record 5200)&quot;;
    if (s2.selDet === &quot;LHCB&quot;) return &quot;Vertex &amp; Spuren: illustrativ \xB7 B-Masse: SIMULATION&quot;;
    return &quot;Signal- &amp; Untergrund-\u03BC\u03BC: ECHTE CMS-Kinematik&quot; + (ion ? &quot; \xB7 Multipl. didakt. reduziert&quot; : &quot;&quot;);
  }
  function rKind(D, kind, last) {
    let r = null;
    D.lagen.forEach((l) => {
      if (l.kind === kind &amp;&amp; (last || r === null)) r = l.r;
    });
    return r;
  }
  function radii(D, sc) {
    const trk = rKind(D, &quot;track&quot;, true) || 30, em = rKind(D, &quot;em&quot;) || trk + 10, had = rKind(D, &quot;had&quot;) || em + 10, mu = rKind(D, &quot;muon&quot;) || had + 20;
    return { Rtrk: trk * sc, Rem: em * sc, Rhad: had * sc, Rmu: mu * sc };
  }
  function drawLegend() {
    const ctxEv = E2.ctxEv, evW = s2.evW, evH = s2.evH;
    const items = [
      [&quot;\u03BC (alle Lagen)&quot;, &quot;#2ea44f&quot;],
      [&quot;e\u207B (\u2192EM-Kal.)&quot;, &quot;#58a6ff&quot;],
      [&quot;\u03B3 (\u2192EM, kein Track)&quot;, &quot;#f1e05a&quot;],
      [&quot;Had (\u2192HAD-Kal.)&quot;, &quot;#ff7f0e&quot;],
      [&quot;\u03BD: fehl. E_T (MET)&quot;, &quot;#8b949e&quot;]
    ];
    const gap = Math.min(62, (evW - 8) / items.length), y = evH - 5;
    ctxEv.save();
    ctxEv.font = &quot;6px sans-serif&quot;;
    ctxEv.textAlign = &quot;left&quot;;
    items.forEach((it, i) => {
      const x = 4 + i * gap;
      ctxEv.fillStyle = it[1];
      ctxEv.beginPath();
      ctxEv.arc(x + 2, y - 2, 2.3, 0, 2 * Math.PI);
      ctxEv.fill();
      ctxEv.fillStyle = &quot;rgba(205,215,230,0.85)&quot;;
      ctxEv.fillText(it[0], x + 7, y);
    });
    ctxEv.restore();
  }
  function emCluster(cx, cy, ang, r0, r1, col) {
    const ctxEv = E2.ctxEv;
    ctxEv.save();
    ctxEv.globalAlpha = 0.6;
    ctxEv.fillStyle = col;
    ctxEv.beginPath();
    ctxEv.moveTo(cx + r0 * Math.cos(ang - 0.14), cy + r0 * Math.sin(ang - 0.14));
    ctxEv.lineTo(cx + r1 * Math.cos(ang - 0.22), cy + r1 * Math.sin(ang - 0.22));
    ctxEv.lineTo(cx + r1 * Math.cos(ang + 0.22), cy + r1 * Math.sin(ang + 0.22));
    ctxEv.lineTo(cx + r0 * Math.cos(ang + 0.14), cy + r0 * Math.sin(ang + 0.14));
    ctxEv.closePath();
    ctxEv.fill();
    ctxEv.restore();
  }
  function hadShower(cx, cy, ang, r0, r1) {
    const ctxEv = E2.ctxEv;
    ctxEv.strokeStyle = &quot;rgba(255,127,14,0.85)&quot;;
    ctxEv.lineWidth = 1;
    for (let k = 0; k < 5; k++) {
      let a = ang + (Math.random() - 0.5) * 0.55;
      ctxEv.beginPath();
      ctxEv.moveTo(cx + r0 * Math.cos(ang), cy + r0 * Math.sin(ang));
      ctxEv.lineTo(cx + r1 * Math.cos(a), cy + r1 * Math.sin(a));
      ctxEv.stroke();
    }
  }
  function muonHit(p, ang) {
    const ctxEv = E2.ctxEv;
    const px = Math.cos(ang + Math.PI / 2), py = Math.sin(ang + Math.PI / 2);
    ctxEv.strokeStyle = &quot;#2ea44f&quot;;
    ctxEv.lineWidth = 3;
    ctxEv.beginPath();
    ctxEv.moveTo(p[0] - 4 * px, p[1] - 4 * py);
    ctxEv.lineTo(p[0] + 4 * px, p[1] + 4 * py);
    ctxEv.stroke();
    ctxEv.fillStyle = &quot;#2ea44f&quot;;
    ctxEv.beginPath();
    ctxEv.arc(p[0], p[1], 2.3, 0, 2 * Math.PI);
    ctxEv.fill();
  }
  function metArrow(cx, cy, ang, len) {
    const ctxEv = E2.ctxEv;
    ctxEv.save();
    ctxEv.setLineDash([4, 3]);
    ctxEv.strokeStyle = &quot;#8b949e&quot;;
    ctxEv.lineWidth = 1.8;
    const tx = cx + len * Math.cos(ang), ty = cy + len * Math.sin(ang);
    ctxEv.beginPath();
    ctxEv.moveTo(cx, cy);
    ctxEv.lineTo(tx, ty);
    ctxEv.stroke();
    ctxEv.setLineDash([]);
    ctxEv.fillStyle = &quot;#8b949e&quot;;
    ctxEv.beginPath();
    ctxEv.moveTo(tx, ty);
    ctxEv.lineTo(tx - 7 * Math.cos(ang - 0.4), ty - 7 * Math.sin(ang - 0.4));
    ctxEv.lineTo(tx - 7 * Math.cos(ang + 0.4), ty - 7 * Math.sin(ang + 0.4));
    ctxEv.closePath();
    ctxEv.fill();
    ctxEv.font = &quot;5.5px monospace&quot;;
    ctxEv.fillStyle = &quot;rgba(139,148,158,0.8)&quot;;
    ctxEv.fillText(&quot;E_T^miss&quot;, tx + 4 * Math.cos(ang + Math.PI / 2), ty + 4 * Math.sin(ang + Math.PI / 2));
    ctxEv.restore();
  }
  function drawParticleBarrel(cx, cy, ang, typ, pt, q, D, sc) {
    const ctxEv = E2.ctxEv;
    const R3 = radii(D, sc);
    const curv = q * (D.bend || 0.6) * Math.min(0.75, 22 / Math.max(4, pt));
    if (typ === &quot;bg&quot;) {
      const bgLen = s2.isIon ? R3.Rtrk : R3.Rtrk * (0.85 + Math.random() * 0.3);
      drawTrack(
        cx,
        cy,
        ang,
        bgLen,
        curv,
        s2.isIon ? &quot;rgba(227,119,194,0.38)&quot; : &quot;rgba(120,140,170,0.38)&quot;,
        0.7
      );
      return;
    }
    if (typ === &quot;mu&quot;) {
      let p = drawTrack(cx, cy, ang, R3.Rmu, curv, &quot;#2ea44f&quot;, 2.2);
      muonHit(p, ang);
      const bx = cx + R3.Rtrk * 1.1 * Math.cos(ang), by = cy + R3.Rtrk * 1.1 * Math.sin(ang);
      ctxEv.save();
      ctxEv.fillStyle = &quot;rgba(46,164,79,0.55)&quot;;
      ctxEv.font = &quot;5.5px monospace&quot;;
      ctxEv.fillText(&quot;B\u21BA&quot;, bx + 3, by - 2);
      ctxEv.restore();
    } else if (typ === &quot;e&quot;) {
      drawTrack(cx, cy, ang, R3.Rtrk, curv, &quot;#58a6ff&quot;, 2);
      emCluster(cx, cy, ang, R3.Rtrk, R3.Rem, &quot;#58a6ff&quot;);
    } else if (typ === &quot;gamma&quot;) {
      emCluster(cx, cy, ang, R3.Rtrk, R3.Rem, &quot;#f1e05a&quot;);
    } else if (typ === &quot;had&quot;) {
      drawTrack(cx, cy, ang, R3.Rem, curv, &quot;rgba(255,127,14,0.9)&quot;, 1.4);
      hadShower(cx, cy, ang, R3.Rem, R3.Rhad);
    } else if (typ === &quot;nu&quot;) {
      metArrow(cx, cy, ang, R3.Rtrk * 1.6);
    }
  }
  function lhcbX(st) {
    const xs = s2.evW - 12;
    return 18 + st / 330 * (xs - 18);
  }
  function drawParticleForward(vx, vy, slope, typ, pt, q, bg) {
    const ctxEv = E2.ctxEv;
    const xDip = lhcbX(160), xEm = lhcbX(250), xMu = lhcbX(315);
    const col = bg ? &quot;rgba(255,127,14,0.40)&quot; : typ === &quot;mu&quot; ? &quot;#2ea44f&quot; : typ === &quot;e&quot; ? &quot;#58a6ff&quot; : typ === &quot;gamma&quot; ? &quot;#f1e05a&quot; : &quot;rgba(255,127,14,0.9)&quot;;
    const yDip = vy + slope * (xDip - vx);
    const slope2 = slope + q * Math.min(0.35, 26 / Math.max(4, pt)) / 100;
    if (typ === &quot;gamma&quot;) {
      const y = vy + slope * (xEm - vx);
      ctxEv.save();
      ctxEv.globalAlpha = 0.6;
      ctxEv.fillStyle = col;
      ctxEv.fillRect(xEm - 3, y - 5, 7, 10);
      ctxEv.restore();
      return;
    }
    const xEnd = typ === &quot;mu&quot; ? xMu : xEm;
    const yEnd = yDip + slope2 * (xEnd - xDip);
    ctxEv.strokeStyle = col;
    ctxEv.lineWidth = bg ? 0.8 : 2;
    ctxEv.beginPath();
    ctxEv.moveTo(vx, vy);
    ctxEv.lineTo(xDip, yDip);
    ctxEv.lineTo(xEnd, yEnd);
    ctxEv.stroke();
    if (!bg &amp;&amp; typ === &quot;mu&quot;) {
      ctxEv.fillStyle = col;
      ctxEv.beginPath();
      ctxEv.arc(xMu, yEnd, 2.3, 0, 2 * Math.PI);
      ctxEv.fill();
    }
    if (!bg &amp;&amp; typ === &quot;e&quot;) {
      ctxEv.save();
      ctxEv.globalAlpha = 0.6;
      ctxEv.fillStyle = col;
      ctxEv.fillRect(xEm - 3, yEnd - 5, 7, 10);
      ctxEv.restore();
    }
  }
  function drawDetBg() {
    const ctxEv = E2.ctxEv, evW = s2.evW, evH = s2.evH;
    const { D, cx, cy, Rmax, sc } = detGeo();
    ctxEv.clearRect(0, 0, evW, evH);
    ctxEv.textAlign = &quot;left&quot;;
    ctxEv.strokeStyle = &quot;#2d3845&quot;;
    ctxEv.lineWidth = 1;
    ctxEv.strokeRect(0, 0, evW, evH);
    ctxEv.fillStyle = D.farbe;
    ctxEv.font = &quot;bold 9px monospace&quot;;
    ctxEv.fillText(s2.selDet + &quot; \xB7 &quot; + (s2.isIon ? &quot;Pb-Pb&quot; : &quot;p-p&quot;), 6, 12);
    const cap = document.getElementById(&quot;ev-caption&quot;);
    if (cap) cap.textContent = D.rolle + &quot; \xB7 Daten: &quot; + evProvenance();
    if (D.typ === &quot;barrel&quot;) {
      D.lagen.forEach((l) => {
        const R3 = l.r * sc;
        ctxEv.strokeStyle = layerColor(l.kind);
        ctxEv.lineWidth = l.kind === &quot;muon&quot; || l.kind === &quot;coil&quot; ? 1.5 : 1;
        ctxEv.beginPath();
        ctxEv.arc(cx, cy, R3, 0, 2 * Math.PI);
        ctxEv.stroke();
        ctxEv.fillStyle = &quot;rgba(205,214,228,0.5)&quot;;
        ctxEv.font = &quot;6px monospace&quot;;
        ctxEv.fillText(l.name, cx + (R3 - 2) * Math.cos(-0.5) + 1, cy + (R3 - 2) * Math.sin(-0.5));
      });
      ctxEv.fillStyle = &quot;#fff&quot;;
      ctxEv.beginPath();
      ctxEv.arc(cx, cy, 1.6, 0, 2 * Math.PI);
      ctxEv.fill();
    } else {
      ctxEv.strokeStyle = &quot;rgba(255,127,14,0.18)&quot;;
      ctxEv.beginPath();
      ctxEv.moveTo(0, cy);
      ctxEv.lineTo(evW, cy);
      ctxEv.stroke();
      D.stationen.forEach((st) => {
        const x = lhcbX(st.x);
        ctxEv.strokeStyle = layerColor(st.kind);
        ctxEv.lineWidth = st.kind === &quot;magnet&quot; ? 3 : 1;
        ctxEv.beginPath();
        ctxEv.moveTo(x, 28);
        ctxEv.lineTo(x, evH - 18);
        ctxEv.stroke();
        ctxEv.save();
        ctxEv.translate(x, 26);
        ctxEv.rotate(-Math.PI / 2);
        ctxEv.fillStyle = &quot;rgba(205,214,228,0.6)&quot;;
        ctxEv.font = &quot;5.5px monospace&quot;;
        ctxEv.fillText(st.name, 0, 2);
        ctxEv.restore();
      });
    }
    drawLegend();
  }
  function drawTrack(x0, y0, ang, len, curv, color, lw) {
    const ctxEv = E2.ctxEv;
    let mx = x0 + len / 2 * Math.cos(ang) + curv * Math.cos(ang + Math.PI / 2) * (len / 2);
    let my = y0 + len / 2 * Math.sin(ang) + curv * Math.sin(ang + Math.PI / 2) * (len / 2);
    let tx = x0 + len * Math.cos(ang) + curv * Math.cos(ang + Math.PI / 2) * len;
    let ty = y0 + len * Math.sin(ang) + curv * Math.sin(ang + Math.PI / 2) * len;
    ctxEv.strokeStyle = color;
    ctxEv.lineWidth = lw;
    ctxEv.beginPath();
    ctxEv.moveTo(x0, y0);
    ctxEv.quadraticCurveTo(mx, my, tx, ty);
    ctxEv.stroke();
    return [tx, ty];
  }
  function drawCollisionEvent(ev) {
    const ctxEv = E2.ctxEv, evW = s2.evW, evH = s2.evH;
    drawDetBg();
    const { D, cx, cy, Rmax, sc } = detGeo();
    const evd = s2.goldenEvent || ev || s2.lastEvent;
    if (D.typ === &quot;forward&quot;) {
      const pvx = lhcbX(34), pvy = cy, svx = pvx + 24, svy = cy + (Math.random() - 0.5) * 8;
      let nbg = Math.round(11 * Math.min(2, Math.max(0.4, s2.paramIntensity)));
      for (let i = 0; i < nbg; i++) drawParticleForward(pvx, pvy, (Math.random() - 0.5) * 0.55, &quot;had&quot;, 5 + Math.random() * 15, Math.random() < 0.5 ? 1 : -1, true);
      ctxEv.strokeStyle = &quot;rgba(255,255,255,0.55)&quot;;
      ctxEv.lineWidth = 1;
      ctxEv.beginPath();
      ctxEv.moveTo(pvx, pvy);
      ctxEv.lineTo(svx, svy);
      ctxEv.stroke();
      ctxEv.fillStyle = &quot;#fff&quot;;
      ctxEv.beginPath();
      ctxEv.arc(pvx, pvy, 2, 0, 7);
      ctxEv.fill();
      if (evd &amp;&amp; evd.leptons) {
        evd.leptons.forEach((L, i) => {
          drawParticleForward(svx, svy, (i ? 1 : -1) * 0.1 + (Math.random() - 0.5) * 0.05, L.lep === &quot;e&quot; ? &quot;e&quot; : &quot;mu&quot;, L.pt || 10, L.q || (i ? 1 : -1), false);
        });
        ctxEv.fillStyle = &quot;#f1e05a&quot;;
        ctxEv.beginPath();
        ctxEv.arc(svx, svy, 2.3, 0, 7);
        ctxEv.fill();
        ctxEv.fillStyle = &quot;rgba(241,224,90,0.9)&quot;;
        ctxEv.font = &quot;6px sans-serif&quot;;
        ctxEv.fillText(&quot;Sek.-Vertex (B)&quot;, svx + 4, svy - 5);
      }
    } else {
      let nbg = Math.round((s2.isIon ? 64 : 11) * Math.min(2.2, Math.max(0.3, s2.paramIntensity)));
      for (let i = 0; i < nbg; i++) {
        const t = App.sampleBgTrack();
        drawParticleBarrel(cx, cy, t.phi != null ? t.phi : Math.random() * 2 * Math.PI, &quot;bg&quot;, t.pt || 4 + Math.random() * 9, t.q || (Math.random() < 0.5 ? 1 : -1), D, sc);
      }
      if (!s2.isIon) {
        drawParticleBarrel(cx, cy, 1.1 + Math.random() * 0.5, &quot;gamma&quot;, 20, 0, D, sc);
        drawParticleBarrel(cx, cy, 3.6 + Math.random() * 0.5, &quot;had&quot;, 26, 1, D, sc);
        let metAng;
        if (evd &amp;&amp; evd.leptons &amp;&amp; evd.leptons.length) {
          let sx = 0, sy = 0;
          evd.leptons.forEach((L) => {
            const phi = L.phi != null ? L.phi : 0;
            sx += (L.pt || 10) * Math.cos(phi);
            sy += (L.pt || 10) * Math.sin(phi);
          });
          metAng = Math.atan2(-sy, -sx);
        } else {
          metAng = 5.2 + Math.random() * 0.6;
        }
        drawParticleBarrel(cx, cy, metAng, &quot;nu&quot;, 0, 0, D, sc);
      }
      if (evd &amp;&amp; evd.leptons) evd.leptons.forEach((L) => {
        drawParticleBarrel(cx, cy, L.phi != null ? L.phi : Math.random() * 2 * Math.PI, L.lep === &quot;e&quot; ? &quot;e&quot; : &quot;mu&quot;, L.pt || 10, L.q || 1, D, sc);
      });
    }
    if (evd) {
      let lbl = evd.name ? evd.name + &quot; \u2192 &quot; + (evd.channel === &quot;4l&quot; ? &quot;ZZ*\u21924\u2113&quot; : &quot;\u03BC\u207A\u03BC\u207B&quot;) + &quot;  M=&quot; + (+evd.M).toFixed(1) + &quot; GeV&quot; : &quot;Untergrund  M=&quot; + (+evd.M).toFixed(1) + &quot; GeV&quot;;
      ctxEv.font = &quot;8px sans-serif&quot;;
      ctxEv.textAlign = &quot;left&quot;;
      ctxEv.fillStyle = &quot;rgba(13,17,23,0.78)&quot;;
      ctxEv.fillRect(4, evH - 30, evW - 8, 12);
      ctxEv.fillStyle = evd.signal ? &quot;#f0f6fc&quot; : &quot;rgba(240,246,252,0.6)&quot;;
      ctxEv.fillText(lbl, 8, evH - 21);
    }
    if (s2.goldenEvent) {
      ctxEv.fillStyle = &quot;#f1e05a&quot;;
      ctxEv.font = &quot;8px sans-serif&quot;;
      ctxEv.textAlign = &quot;right&quot;;
      ctxEv.fillText(&quot;\u2605 GOLDEN&quot;, evW - 6, 11);
      ctxEv.textAlign = &quot;left&quot;;
    }
  }
  App.drawDetBg = drawDetBg;
  App.drawCollisionEvent = drawCollisionEvent;

  // cern/app/src/data.gen.js
  var CERN_REAL = { &quot;meta&quot;: { &quot;source&quot;: &quot;CMS Open Data \u2014 Run2011A DoubleMu (\u03BC\u03BC) + Record 5200 (4\u2113)&quot;, &quot;record&quot;: &quot;https://opendata.cern.ch/record/545&quot;, &quot;record_4l&quot;: &quot;https://opendata.cern.ch/record/5200&quot;, &quot;sqrt_s_TeV&quot;: 7, &quot;sqrt_s_4l_TeV&quot;: 8, &quot;run&quot;: &quot;2011A DoubleMu&quot;, &quot;channel_real&quot;: &quot;\u03BC\u207A\u03BC\u207B (echte Massen + Kinematik)&quot;, &quot;higgs4l_sim&quot;: false, &quot;higgs4l_source&quot;: &quot;CMS Open Data, Record 5200 (2011+2012, 4\u03BC/4e/2e2\u03BC)&quot;, &quot;higgs4l_n&quot;: 278, &quot;pbpb_real&quot;: false, &quot;n_events&quot;: 12e3 }, &quot;pp&quot;: [53.52, 84.81, 52, 90.21, 90.61, 89.5, 87.37, 92.52, 96.1, 92.66, 59.3, 94.73, 92.06, 91.35, 57.31, 93.02, 89.39, 93.79, 88.69, 90.73, 78.09, 99.76, 51.59, 90.42, 91.81, 90.63, 90.69, 89.08, 102.96, 50.46, 93.83, 88.02, 92.62, 92.62, 94.37, 69.77, 97.94, 88.82, 89.25, 94.69, 92.79, 50.36, 88.54, 55.7, 87.35, 91.19, 91.23, 92.75, 98.01, 79.98, 92.08, 91.58, 94.3, 92.39, 90.34, 59.72, 90.76, 90.45, 67.49, 57.93, 68.65, 90.25, 91.16, 93.43, 71.18, 90.35, 91.41, 87.07, 86.55, 108.27, 85.41, 62.56, 92.59, 84.85, 88.06, 92.41, 92.44, 92.16, 88.95, 56.94, 88.58, 90.3, 108.64, 133.9, 88.22, 62.2, 92.52, 80.48, 90.56, 89.7, 89.12, 93.51, 91.8, 82.58, 88.92, 93.12, 66.84, 87.42, 90.73, 90.28, 89.89, 90.4, 92.31, 67.85, 86.76, 86.19, 89.67, 93.84, 91.11, 82.52, 87.36, 88.18, 90.91, 92.4, 90.84, 94.17, 91.07, 90.51, 87.48, 92.93, 90.83, 82.86, 87.8, 94.9, 89.7, 70.49, 88.66, 60, 89.98, 73.58, 57.16, 83.77, 63.94, 87.47, 93.5, 88.37, 93.63, 82.31, 89.4, 55.15, 91.45, 92.51, 100.4, 82.34, 92.38, 88.7, 56.52, 94.16, 109.16, 90.79, 95.62, 90.82, 89.33, 92, 89.67, 92.13, 99.9, 93.59, 76.73, 91.97, 119.45, 92.44, 88.45, 86.28, 65.28, 91.52, 50.47, 95.02, 93.87, 91.29, 89.63, 87.65, 79.65, 98.02, 91.98, 54.27, 90.14, 90.34, 88.97, 94.79, 93.46, 91.48, 93.16, 88.93, 71.37, 87.44, 106.66, 51.56, 91.15, 88.84, 93.14, 90.25, 92.5, 60.05, 84.73, 69.04, 91, 51.97, 94.64, 88.98, 100.48, 84.99, 92.2, 89.75, 88.09, 92.05, 87.99, 90.85, 60.21, 93.75, 89.43, 53.9, 92.41, 72.35, 90.79, 58.12, 83.71, 51.05, 93.03, 88.78, 90.14, 88.93, 90.84, 62.37, 57.23, 89.43, 98.6, 102.53, 91.99, 81.38, 87.29, 88.69, 102.62, 87.73, 89.91, 89.23, 85.47, 91.21, 62.77, 91.5, 87.19, 93.4, 90.28, 87.93, 76.5, 92.43, 88.26, 92.71, 91.66, 90.9, 94.66, 84.46, 88.45, 90.47, 89.33, 97.55, 90.48, 82.32, 50.6, 91.19, 89.08, 83.73, 67.02, 90.44, 90.45, 91.85, 90.75, 91.47, 54.09, 96.65, 82.4, 90.7, 90.92, 84.69, 93.76, 89.88, 90.06, 80.38, 75.06, 75.48, 61.87, 92.64, 68.87, 85.56, 95.06, 84.95, 76.06, 66.08, 93.38, 74.76, 75.05, 71.66, 90.55, 89.28, 88.5, 85.2, 54.34, 92.42, 83.24, 53.99, 92.4, 72.02, 90.65, 92.13, 89.64, 89.9, 127.73, 89.05, 89.82, 91.88, 72.34, 85.83, 91.09, 92.77, 85.82, 75.15, 89.29, 94.34, 91.63, 86.42, 75.41, 88.44, 91.81, 87.95, 90.83, 92.4, 95.59, 93.95, 90.64, 93.63, 89.16, 61.41, 96.54, 88.05, 90.53, 91.9, 88.91, 89.79, 91.8, 64.22, 86.14, 50.08, 85.35, 88.91, 89.63, 107.52, 73.31, 54.16, 90.86, 55.02, 90.5, 90.38, 100.36, 58.61, 92.97, 94.05, 84.33, 91.69, 88.72, 90.74, 91.69, 57.21, 92.45, 83.45, 83.05, 87.81, 95.02, 89.16, 111.23, 59.3, 91.5, 89.77, 64.2, 90.53, 98.06, 50.85, 66.08, 60.63, 89.84, 83.7, 90.33, 87.48, 50.75, 89.35, 90.11, 88.67, 79.85, 92.78, 87.76, 92.8, 52.15, 59, 89.83, 93.66, 100.35, 88.61, 61.92, 58.28, 70.41, 87.56, 91.57, 91.81, 91.26, 54.42, 91.91, 87.1, 92.3, 88.84, 98.91, 91.17, 92.33, 91.66, 55.63, 88.22, 88.52, 119.5, 93.42, 92.86, 90.03, 89.86, 75.66, 73.42, 92.21, 88.59, 85.38, 90.53, 90.38, 53.89, 92.99, 95.83, 52.52, 89.47, 84.94, 90.32, 85.76, 90.67, 92.35, 94.36, 93.37, 88.41, 93.13, 92.26, 83.44, 92.79, 91.5, 89.53, 91.27, 94.86, 59.84, 94.06, 87.57, 54.56, 88.41, 59.08, 91.56, 81.61, 93.23, 81.65, 55.88, 90.03, 89.67, 93.82, 88.43, 90.98, 92.78, 94.69, 74.95, 56.61, 89.55, 91.32, 94.04, 129.38, 115.23, 93.08, 87.68, 89.29, 53.93, 88.79, 91.33, 87.37, 91.98, 89.57, 90.94, 61.96, 87.95, 91.53, 91.38, 90.03, 99.86, 84.29, 87.98, 89.07, 91.81, 90.85, 89.81, 89.08, 90.87, 51.27, 72.49, 90.77, 92.19, 86.81, 81.87, 82.01, 92.2, 76.19, 91.36, 91.83, 90.35, 91.69, 93.55, 90.79, 144.25, 89.53, 90.91, 88.64, 90.08, 91.56, 89.42, 99.62, 86.89, 62.09, 89.73, 91.27, 96.18, 83.64, 55.09, 87.82, 57.75, 91.97, 86.55, 62.05, 91.19, 92.41, 50.28, 91.01, 96.1, 91.58, 91.07, 75.68, 67.41, 57.61, 91.15, 91.02, 92.65, 92.44, 93.32, 90.33, 88.59, 88.88, 91.4, 90.85, 90.87, 91.51, 92.16, 84.12, 62.28, 93.93, 52.24, 91.91, 88.92, 94.36, 92.37, 89.05, 95.38, 84.77, 87.01, 89.08, 75.07, 90.77, 93.31, 80.84, 94.56, 92.18, 90.58, 91.02, 97.18, 51.65, 91.12, 92.97, 89.91, 89.37, 89.55, 87.95, 91.38, 86.27, 94.26, 63.53, 91.23, 90.66, 61.55, 60.43, 50.52, 95.73, 73.14, 92.25, 53.25, 91.61, 92.26, 88.73, 89.55, 92.57, 86.01, 91.88, 86.91, 105.54, 92.25, 88.56, 92.69, 90.32, 84.32, 79.13, 62.39, 90.72, 51.13, 91.69, 86.19, 91.24, 89.91, 52.86, 78.25, 92.06, 67.71, 89.23, 66.37, 55.14, 93.59, 80.79, 84.3, 94.45, 90.62, 92.5, 59.48, 108.5, 64.1, 70.42, 89.09, 112.63, 77.97, 90.21, 90.61, 50.58, 92.03, 89.73, 86.42, 86.82, 89.49, 90.27, 92.3, 61.75, 90.42, 84.76, 89.34, 89.95, 75.22, 90.78, 97.07, 91.13, 52.58, 99.49, 90.18, 60.85, 83.53, 67.77, 91.57, 87.37, 53.22, 91.25, 89.16, 92.4, 92.79, 85.72, 85.38, 57.38, 91.6, 94.14, 89.52, 89.64, 90.27, 93.56, 92.08, 89.74, 91.07, 82.01, 92.82, 96.51, 90.77, 97.52, 85.91, 89.66, 94.29, 101.18, 102.88, 75.63, 90.24, 96.41, 89.67, 59.55, 91.11, 91.11, 90.6, 91.06, 52.66, 92.17, 90.75, 66.93, 100.34, 92.34, 86.74, 89.7, 89.11, 94.12, 63.38, 88.54, 92.88, 92.48, 95.67, 81.31, 94.47, 91.14, 54.68, 86.55, 91.05, 90.83, 89.23, 87.76, 90.05, 94.5, 88.83, 93.28, 56.81, 91.24, 94.23, 90.13, 86.84, 57.15, 77.69, 91.41, 84.74, 65.27, 88.05, 94.62, 67.19, 84.2, 90.26, 89.74, 54.85, 90.1, 72.83, 88.59, 91.92, 92.44, 96.07, 89.99, 90.77, 91.49, 90.61, 88.99, 51.97, 77.19, 86.32, 91.52, 85.63, 90.21, 94.35, 91.97, 51.86, 90.99, 94.29, 68.27, 90.14, 92.49, 67.66, 91.46, 91.38, 69.29, 91.5, 91.38, 51.79, 90.4, 89.78, 93.19, 59.18, 91.72, 91.59, 92.27, 90.22, 51.18, 91.96, 92, 89.4, 91.12, 90.44, 77.18, 91.18, 82.49, 103.83, 90.06, 92.11, 53.18, 81.6, 51.07, 78.29, 75.02, 92.03, 86.77], &quot;ion&quot;: [9.16, 1.02, 2.03, 1.46, 9.44, 4.58, 8.14, 9.46, 1.42, 1.74, 11.78, 11.88, 2.95, 1.01, 3.09, 2.81, 3.11, 8.74, 2.33, 1.01, 9.37, 9.81, 9.49, 3.13, 5.59, 10.45, 11.69, 2.87, 1.2, 2.01, 2.84, 10.46, 9.38, 10.45, 1.19, 1.28, 9.59, 10.4, 11.27, 6.51, 1.11, 7.81, 9.47, 10.89, 9.38, 10.52, 10.71, 8.43, 2.05, 10.25, 3.24, 1.04, 10.37, 5.39, 2.69, 9.45, 6.33, 4.9, 7.82, 9.52, 2.06, 1.6, 2, 1.93, 1.33, 1.7, 3.09, 1.02, 9.37, 1.31, 3.12, 10.3, 3.21, 11.21, 3.07, 11.15, 10.42, 3.08, 11.13, 7.02, 11.14, 5.77, 11.79, 5.03, 7.68, 9.57, 1.7, 3.66, 2.06, 3.08, 10.64, 1.97, 3.42, 3.12, 2.54, 3.16, 10.78, 1.63, 11.13, 2.57, 11.75, 2.4, 9.35, 10, 1.94, 2.68, 9.46, 3.12, 11.35, 1.83, 1.98, 3.07, 3.08, 11.04, 1.29, 3.71, 11.93, 1.15, 1.04, 1.22, 10.39, 9.53, 11.7, 7.21, 5.78, 6.97, 2.01, 3.09, 3.07, 1.67, 2.05, 1.8, 3.11, 10.29, 7.18, 10.74, 11.64, 10.29, 10.07, 4.7, 3.06, 1.37, 10.16, 1.4, 9, 2.42, 10.7, 10.48, 4.04, 10.14, 2.74, 1.12, 9.42, 2.45, 1.77, 2.73, 3.06, 10.25, 1.52, 1.09, 10.07, 2.86, 9.32, 2.27, 10.8, 5.46, 2.49, 1.51, 9.83, 9.33, 11.61, 8.17, 3.11, 8.3, 11.73, 1, 10.89, 1.44, 7.29, 2.3, 10.43, 9.38, 11.27, 11.2, 3.1, 1.64, 9.19, 9.84, 3.03, 1.03, 10.39, 1.19, 10.37, 9.5, 1.26, 10.51, 8.47, 9.04, 9.23, 5.86, 3.03, 5.28, 9.12, 3.12, 2.46, 3.08, 10.24, 9.78, 2.46, 7.69, 1.58, 1.33, 11.05, 3.35, 10.98, 3.1, 9.44, 3.54, 3.15, 10.92, 9.86, 10.2, 10.07, 11.11, 1.92, 11.06, 3.99, 9.29, 2.87, 11.61, 9.33, 9.47, 3.06, 8.57, 2.4, 4.74, 1.47, 2.16, 3.06, 3.11, 4.5, 1.52, 9.75, 10.29, 2.53, 2.64, 3.13, 3.1, 9.56, 3.09, 8.87, 10.1, 9.22, 11.56, 9.99, 11.37, 10.81, 1.05, 6.09, 10.65, 2, 6.65, 1.1, 7.55, 3.14, 10.37, 11.6, 9.5, 2.32, 10.14, 2.09, 10.88, 10.05, 2, 11.29, 3.15, 6.51, 9.41, 1.04, 9.47, 8.86, 11.03, 6.47, 3.71, 3.07, 10.61, 3.14, 3.08, 4.61, 8.25, 9.22, 1.72, 2.38, 3.34, 9.47, 9.51, 10.47, 10.23, 7.22, 3.68, 9.52, 2.54, 3.07, 10.27, 1.86, 10.12, 9.97, 2.25, 8.98, 11.83, 9.96, 7.51, 2.06, 1.66, 10.06, 1.31, 9.47, 8.75, 1.12, 10.15, 4.33, 3.09, 1.21, 1.38, 9.58, 3.07, 3.1, 8.64, 7.69, 9.4, 10.33, 10.41, 2.23, 8.12, 10.8, 7.41, 3.08, 3.08, 9.37, 9.97, 7.77, 5.42, 10.86, 9.77, 3.09, 1.33, 11.17, 3.05, 9.85, 2.49, 9.52, 3.17, 2.37, 3.09, 2.75, 2.1, 2.33, 1.86, 11.62, 3.05, 11.51, 8.95, 10.37, 3.62, 3.06, 1.42, 2.19, 3.14, 11.39, 8.3, 9.48, 9.4, 3.08, 11.06, 2.02, 3.07, 3.99, 11.65, 3.13, 1.77, 2.3, 3.08, 5.49, 1.01, 11.6, 10.17, 5.53, 11.81, 5.79, 1.14, 3.11, 3.12, 3.09, 10.78, 4.75, 4.51, 10.03, 4.86, 3.09, 9.78, 10.32, 11.19, 9.37, 1.54, 11.96, 1.94, 9.46, 9.49, 11.02, 11.61, 10.09, 4.59, 9.18, 3.12, 6.29, 10.7, 9.86, 10.77, 11.38, 11.95, 9.56, 3.15, 2.04, 3.17, 9.38, 3.03, 10.65, 11.39, 3.15, 7.13, 2.2, 3.13, 11.96, 11.95, 11.88, 4.54, 3.09, 3.06, 1.81, 8.32, 2.48, 4.99, 11.55, 1.2, 9.78, 7.67, 3.05, 3.1, 8.63, 1.21, 3.08, 5.65, 8.56, 2.22, 11.37, 9.41, 1.79, 11.85, 2.82, 9.6, 3.18, 4.74, 7.35, 3.07, 1.27, 9.95, 3.08, 3.16, 10.54, 11.16, 1.23, 9.4, 2.32, 2.99, 10.56, 3.28, 8.27, 2.9, 10, 10.96, 11.1, 3.2, 4.13, 11.88, 2.1, 3.1, 9.48, 4.42, 9.82, 3.08, 8.31, 10.27, 3.08, 1.5, 11.64, 10.69, 2.64, 8.09, 3.04, 1.88, 8.66, 3.08, 2.33, 3.39, 9.61, 10.25, 3.12, 2.39, 2.6, 2.54, 11.69, 11.29, 9.51, 9.55, 11.92, 3.1, 8.94, 11.72, 1.13, 3.03, 3.06, 3.12, 10.92, 7.55, 10.11, 2.38, 3.11, 11.09, 3.06, 9.96, 1.61, 1.99, 7.07, 2.37, 11.36, 4.24, 4.04, 10.36, 3.44, 2.5, 10.19, 10.2, 8.51, 1.94, 3.11, 10.4, 3.08, 11.92, 6.26, 9.36, 9.39, 3.12, 9.56, 11.26, 9.98, 2.23, 9.93, 9.23, 3.01, 1.86, 8.76, 1.77, 10.34, 3.22, 10.98, 5.55, 5.16, 1.06, 8.9, 2.08, 10.08, 2.28, 10.09, 11.15, 7.55, 2.16, 1.22, 3.86, 4.85, 1.9, 9.69, 2.45, 3.13, 2.81, 1.78, 9.42, 9.25, 10.28, 9.88, 3.72, 1.68, 1.67, 4.48, 10.56, 9.48, 3.14, 3.19, 10.73, 11.63, 10.57, 11.68, 7.37, 9.44, 11.84, 2.89, 2.87, 3.69, 3.48, 6.32, 3.21, 2.01, 2.16, 3.32, 9.91, 7.05, 1.18, 11.61, 9.79, 6.11, 3.05, 10.86, 7.05, 4.87, 4.23, 10.13, 2.2, 10.53, 3.1, 9.46, 5.25, 3.12, 10.18, 4.04, 9.91, 2.2, 9.39, 1.5, 2.7, 3.06, 2.23, 3.1, 11.07, 11.8, 1.71, 8.51, 3.56, 11.44, 2.42, 7.23, 3.08, 1.54, 2.97, 1.23, 2.34, 3.08, 3.07, 3.83, 10.81, 1.47, 8.69, 3.17, 3.07, 3.75, 3.01, 11.27, 3.1, 11.21, 3.07, 9.26, 9.65, 9.62, 11.6, 9.46, 1.96, 9.16, 1.35, 2.08, 9.37, 9.42, 2.78, 2.02, 11.25, 1.23, 6.61, 3, 6.93, 11.21, 10.43, 9.36, 9.93, 1.48, 10.84, 3.12, 5.92, 1.2, 2.04, 2.89, 1.49, 7.74, 3.09, 1.91, 1.57, 3.12, 3.08, 10.63, 11.03, 3.06, 11.58, 11.72, 10.93, 11.38, 6.97, 1.57, 3.13, 3.08, 1.05, 9.02, 9.47, 1.81, 10.09, 3.05, 10.95, 11.49, 3.59, 6.05, 2.38, 11.09, 1.77, 11.17, 2.11, 3.11, 5.82, 3.06, 3.26, 3.12, 3.11, 5.04, 3.12, 1.05, 1.79, 10.91, 9.48, 3.07, 1.9, 5.96, 11.42, 1.88, 3.11, 3.24, 1.34, 3.08, 2.03, 10.81, 10.91, 1.03, 2.16, 11.64, 1.19, 3.07, 1.99, 5.62, 3.63, 1.32, 3.05, 3.81, 11.19, 10.4, 1.52, 10.32, 4.05, 3.15, 9.61, 10.73, 3.1, 2.69, 10.54, 3.05, 11.4, 9.86, 1.19, 1.28, 1.48, 1.29, 2.03, 3.11, 1.25, 9.48, 3.08, 9.45, 3.14, 3.1, 1.45, 10.91, 1.27, 9.92, 9.58, 2.61, 10.89, 1.5, 3.02, 3.11, 9.5, 8.37, 1.42, 10.21, 1.08, 2.68, 1.08, 3.09, 11.95, 11.09, 9.16, 11.08, 1.69, 4.01, 8.64, 2.07, 10.16, 5.04, 3.1, 1.83, 10.97, 8.48, 2.71, 3.09, 11.24, 3.65, 10.82, 3.38, 3.11, 3.12, 1.32, 11.89, 5.06, 11.83, 1.73, 1.31, 3.51, 10.71, 9.36, 8.7, 4.49, 3.1, 6.43, 1.67, 11.41, 11.18, 3.08, 11.11, 5.83, 3.04, 10.9, 1.32, 1.59, 3.09, 8.48, 9.58, 3.1, 3.57, 3.12, 10.5, 10.85, 11.76, 11.06, 4.19, 8.87, 9.86, 1.19, 2.73, 10.27, 6.96, 9.92, 1.87, 9.59, 2.39, 1.15, 9.76, 10.17, 2.75, 10.38, 9.43, 9.43, 9.45, 8.13, 10.4, 3.1, 3.1, 9.46, 4.62, 3.07, 2.56, 2.45, 10.39, 2.81, 3.09, 3.14, 3.69, 8.94, 9.45, 3.09, 1.8, 2.68, 9.85, 9.52, 11.94, 3.07, 2.41, 11.81, 2.49, 10.6, 10.19, 8.14, 1.99, 10.8, 2, 2.45, 6.89, 9.36, 3.11, 11.53, 7.57, 10.79, 2.95, 3.57, 11.88, 9.53, 1.51, 10.91, 3.09, 9.38, 8.45, 2.78, 7.32, 9.35, 10.63, 3.01, 3.13, 2.16, 3.65, 1.34, 2.2, 10.41, 7.06, 3.09, 10.46, 10.28, 8.75, 2, 2.62, 3.09, 4.49, 7.27, 11.82, 2.14, 11.69, 10.1, 5.35, 3.08, 4.26, 9.68, 10.36, 2.13, 1.85, 11.85, 1.94, 9.14, 11.73, 8.17, 3.06, 11.68, 2.72, 10.21, 1.87, 3.09, 3.03, 11.86, 7.14, 9.3, 7.93, 11.89, 1.26, 11.35, 11.61, 10.8, 2.27, 11.2, 7.83, 3.05, 9.47, 1.42, 9.69, 3.11, 9.49, 8.38, 10.18, 10.17, 9.83, 1.89, 11.74, 9.98, 10.97, 10.58, 4.71, 10.76, 10.88, 11.68, 6.05, 2.11, 10.76, 2.08, 3.12, 8.59, 6.26, 8.79, 9.97, 3.93, 1.73, 9.34, 10.35, 11.33, 3.15, 6.75, 9.72, 1.49, 3.11, 9.93, 10.32, 11.56, 1.19, 10.32, 9.06, 9.51, 2.98, 10.34, 11.67, 8.78, 10.45, 1.36, 2.22, 11.02, 3.06, 2.47, 11.13, 2.95, 3.07, 9.7, 9.36, 3.08, 10.37, 1.04, 3.09, 11.42, 9.44, 8.45, 2.09, 9.3, 2.54, 11.36, 11.38, 9.53, 9.85, 3.32, 11.57, 10.23, 3.13, 5.79, 10.31, 10.93, 3.74, 11.94, 10.77, 9.43, 2.82, 8.98, 1.75, 1.85, 10.09, 1.03, 10.9, 4.58, 3.55, 8.25, 1.02, 8.95, 1.59, 2.31, 11.35, 9.37, 3.05, 11.87, 9.4, 3.08, 9.06, 3.15, 8.75, 1.43, 10.37, 1.03, 9.94, 3.04, 3.08, 3.22, 2.69, 3.06, 3.1, 9.67, 9.46, 8.8, 11.37, 5.94, 10.57, 1.77, 8.24, 1, 2.55, 9.34, 2.44, 10.84, 3.11, 11.3, 6, 1.08, 3.72, 2.19, 3.09, 3.1, 11.56, 3.1, 3.1, 10.84, 1.93, 2.26, 5.32, 6.75, 8.08, 11.45, 2.28, 1.65, 3.11, 1.02, 1.39, 5.01, 11.29, 3.05, 1.75, 1.06, 10.24, 10.01, 9.48, 2.15, 3.93, 11.73, 7.47, 3.12, 10.24, 10.68, 3.05, 10.23, 2.86, 3.09, 10.74, 1.56, 2.92, 3.1, 2.36, 7.7, 3.51, 1.01, 1.25, 3.12, 3.05, 1.74, 9.57, 8.95, 11.58, 8.75, 10.42, 10.79, 3.41, 3.07, 10.08, 6.52, 8.6, 11.82, 10.83, 11.58, 8.65, 9.49, 11.7, 5.65, 3.38, 9.95, 1.18, 11.08, 3.06, 9.69, 3.09, 2.95, 9.69, 1.56, 3.57, 3.02, 9.49, 10.57, 9.31, 10.18, 2.89, 3.09, 1.7, 10.47, 9.53, 3.11, 2.5, 4.12, 10.21, 6.83, 2.99, 1.49, 8.94, 9.2, 7.72, 11.96, 4.49, 9.44, 3.26, 3.07, 3.53, 9.56, 1.84, 3.09, 2.75, 3.11, 9.45, 1.05, 7.42, 2.42, 3.71, 1.96, 11.91, 2.65, 10.44, 10.26, 1.21, 11.76, 1.3, 3.17, 1.95, 9.47, 2.89, 4.47, 3.07, 9.78, 10.03, 1.47, 11.67, 9.66, 3.92, 2.73, 3.12, 3.06, 2.31, 2.12, 10.73, 3.11, 9.42, 1.44, 8.06, 2.77, 3.11, 3.07, 10.46, 10.29, 9.41, 1.22, 9.28, 2.53, 9.99, 10.04, 3.04, 11.84, 3.07, 2.82, 2.25, 9.89, 3.09, 1.1, 3.11, 10.61, 2.65, 4.39, 3.66, 4.75, 3.94, 4.65, 9.69, 1.92, 8.87, 3.13, 1.92, 11.06, 9.54, 4.22, 10.02, 11.71, 3.08, 6.95, 10.66, 9.39, 11.69, 3.08, 9.58, 8.69, 9.38, 5.89, 9.29, 3.3, 3.03, 9.71, 1.22, 2.27, 11.13, 9.26, 3.11, 9.42, 11.01, 2.21, 1.2, 3.05, 10.78, 1.14, 10.57, 6.44, 11.98, 3.13, 8.54, 9.54, 9.26, 10.63, 8.89, 10.6, 10.58, 3.13, 3.07, 10.98, 10.16, 10.01, 10.06, 7.99, 9.44, 3.07, 9.46, 4.32, 7.77, 10.84, 1.96, 3.08, 1.39, 9.81, 9.86, 7.95, 1.03, 5.48, 1.28, 6.08, 9.37, 2.46, 11.44, 11.98, 10.27, 3.15, 3.66, 8.66, 9.53, 9.49, 11.4, 3.58, 2.1, 1.46, 10.6, 9.65, 11.51, 1.17, 3.12, 3.1, 11.31, 9.61, 9.52, 7.9, 1.95, 1.68, 2.31, 1.64, 10.26, 9.47, 1.24, 9.48, 10.34, 3.96, 11.18, 1.18, 3.13, 1.97, 1.03, 3.11, 3.57, 1.19, 1.6, 3.12, 6.38, 11.29, 9.12, 2.17, 10.75, 9.49, 8.69, 9.16, 9.55, 9.24, 2.76, 1.93, 1.76, 8.27, 2.51, 11.2, 1.12, 1.53, 4.13, 8.1, 7.46, 1.55, 9.99, 10.78, 7.39, 3.13, 3.13, 10.57, 2.27, 2.25, 3.04, 1.44, 10.27, 2.06, 3.02, 2.08, 8.61, 9.94, 3.08, 11.61, 3.14, 11.12, 2.08, 1.48, 9.29, 3.14, 9.39, 7.32, 9.54, 2.14, 2.69, 3.46, 11.95, 1.03, 3.7, 9.65, 11.82, 11.43, 3.12, 9.57, 11.92, 8.96, 3.17, 11.44, 6.35, 11.21, 3.07, 1.48, 9.96, 3.09, 10.25, 8.66, 9.76, 1.98, 7.07, 5.55, 1.06, 9.75, 3.09, 3.54, 2.13, 9.27, 3.1, 1.29, 3.11, 11.73, 5.35, 3.08, 2.02, 2.09, 9.05, 8.82, 10.88, 11.38, 2.54, 4.53, 11.63, 10.06, 4.94, 2.38, 3.09, 7.24, 10.19, 10.35, 1.53, 5.58, 3.11, 3.05, 3.15, 9.83, 4.28, 11.5, 2.6, 11.59, 3.12, 10.3, 2.58, 2.26, 10.61, 3.1, 10.61, 7.62, 11.35, 3.69, 10.46, 3.12, 10.96, 7.33, 11.01, 5.17, 10.09, 9.46, 7.63, 1.31, 11.18, 1.49, 9.6, 9.51, 9.05, 10.2, 11.67, 11.24, 11.48, 2.42, 10.08, 9.49, 11.47, 10.42, 9.24, 1.55, 11.85, 6.48, 3.1, 2.63, 2.57, 11.4, 11.46, 10.67, 11.71, 1.52, 3.1, 9.47, 3.07, 10.38, 1.02, 5.64, 3.09, 3.99, 9.37, 3.08, 1.86, 1.21, 2.84, 3.65, 3.05, 2.37, 2.18, 3.12, 3.71, 3.11, 9.95, 10.91, 9.57, 8.84, 3.12, 2.17, 2.92, 9.55, 2.93, 2.22, 10.89, 2.36], &quot;low&quot;: [1.44, 1.02, 2.03, 2.85, 1.46, 2.71, 3.21, 1.42, 0.48, 1.17, 1.42, 3.07, 0.56, 2.27, 3.01, 0.53, 0.59, 1.02, 3.11, 3.13, 1.83, 0.54, 0.66, 3.09, 2.46, 3.02, 0.7, 3.06, 0.79, 1.81, 1.2, 2.01, 0.83, 2.84, 2.7, 1.28, 0.72, 1.18, 1.11, 1.24, 3.09, 2.29, 3.07, 1.49, 2.87, 1.9, 1.84, 2.05, 3.46, 3.24, 1.04, 1.65, 2.69, 1.11, 3.12, 3.37, 3.06, 0.88, 2.06, 1.54, 3.11, 2, 1.01, 1.33, 3.25, 3.09, 0.74, 0.8, 1.22, 1.31, 3.12, 3.12, 3.12, 3.07, 0.68, 1.38, 0.66, 2.71, 0.98, 2.98, 0.74, 0.97, 3.09, 1.96, 0.73, 1.72, 3.12, 3.07, 1.51, 2.16, 3.06, 3.08, 2.65, 1.97, 3.42, 3.07, 3.08, 3.06, 3.16, 2.03, 3.13, 1.8, 1.94, 2.57, 0.97, 3.15, 2.4, 1.24, 1.94, 2.68, 3.05, 3.12, 0.79, 1.15, 1.83, 1.98, 3.01, 0.95, 3.07, 3.08, 3.08, 2.05, 1.29, 2.34, 0.78, 0.84, 1.15, 3.18, 1.04, 1.22, 0.95, 0.6, 1.33, 0.44, 0.87, 2.01, 3.11, 1, 3.09, 3.13, 1.67, 0.6, 3.03, 1.8, 3.11, 3.04, 1.98, 0.9, 0.41, 0.87, 2.37, 3.16, 1.65, 1.37, 2.12, 1.4, 3.34, 3.11, 3.1, 3.02, 1.6, 0.47, 2.47, 1.12, 2.45, 3.11, 2.73, 3.48, 3.06, 3.12, 0.79, 1.52, 1.09, 2.59, 3.08, 3.11, 2.27, 0.8, 0.61, 0.74, 2.49, 2.72, 3.02, 0.94, 0.77, 3.12, 3.11, 3.11, 0.64, 1.97, 1, 0.99, 2.66, 1.01, 2.3, 3.09, 2.43, 3.1, 1.64, 1.39, 3.08, 3.03, 1.84, 1.03, 3.09, 0.62, 1.26, 2.53, 3.1, 3.07, 3.3, 1.99, 1.88, 0.62, 2.19, 3.12, 0.55, 2.22, 2.46, 0.96, 0.86, 3.09, 0.92, 0.89, 2.46, 3.11, 1.58, 2.72, 1.33, 3.11, 2.36, 0.71, 0.67, 0.83, 3.15, 1.79, 2.07, 2.41, 1.92, 3.13, 3.07, 2.87, 3.06, 0.95, 0.95, 1.82, 2.22, 2.4, 3.08, 1.78, 2.16, 3.12, 2.44, 3.11, 1.52, 3.14, 0.45, 0.58, 2.1, 2.64, 3.02, 0.76, 3.1, 3.09, 3.11, 1.24, 1.8, 1.03, 0.6, 1.05, 0.57, 1.37, 2, 2.56, 1.41, 1.1, 1.94, 0.53, 3.06, 2.94, 2.32, 1.77, 2.09, 1.21, 2.25, 2, 0.88, 2.17, 3.15, 3.12, 1.04, 1.24, 2, 2.93, 3.1, 2.97, 3.07, 1.51, 3.14, 3.07, 0.75, 3.16, 1.08, 3.05, 3.21, 2.48, 2.38, 3.34, 3.1, 3.11, 3.09, 1.55, 2.54, 3.07, 1.86, 1.04, 3.14, 2.25, 3.01, 3.09, 1.23, 2.06, 1.66, 3.29, 1.12, 0.91, 3.11, 1.79, 0.56, 2.95, 0.6, 3.13, 1.21, 2.6, 1.38, 3.12, 3.13, 3.11, 2.54, 3.14, 1.27, 3.09, 2.23, 1.64, 3.07, 3.08, 0.96, 1.92, 1.26, 0.49, 0.85, 3.08, 1.33, 3.06, 3.12, 3.05, 0.53, 2.49, 1.56, 3.17, 0.72, 2.35, 3.09, 2.75, 1.46, 2.33, 3.32, 2.88, 1.3, 3.05, 1.3, 0.44, 2.06, 3.07, 3.06, 1.42, 1.56, 2.3, 0.88, 0.42, 0.42, 3.08, 2.1, 2.02, 0.79, 3.07, 3.14, 0.97, 3.13, 1.77, 2.3, 3.08, 3.11, 1.01, 2.29, 1.48, 3.08, 3.06, 1.14, 3.11, 3.12, 3.09, 1.17, 2.31, 2.45, 2.25, 1.96, 3.09, 3.09, 2.04, 2.93, 0.61, 1.54, 3.14, 0.74, 0.44, 2.56, 0.41, 0.58, 3.06, 2.96, 1.85, 1.89, 3.08, 2.61, 2.15, 1.91, 0.52, 3.08, 2.35, 1.02, 0.76, 3.11, 0.79, 3.15, 0.75, 1.68, 3.17, 2.07, 3.03, 2.51, 2.82, 3.08, 2.07, 3.04, 2.2, 3.13, 2.08, 3.09, 2.38, 0.74, 3.06, 3.06, 2.22, 1.81, 2.1, 3.07, 3.11, 3.11, 3.11, 1.36, 0.5, 3.05, 1.35, 3.1, 2.04, 1.21, 3.06, 3.08, 2.08, 0.65, 0.58, 3.13, 0.97, 0.76, 1.79, 3.07, 3.09, 0.78, 2.95, 3.18, 2.41, 2.55, 3.07, 1.04, 1.27, 0.9, 2.36, 3.04, 3.1, 1.98, 1.36, 0.44, 3.11, 1.23, 1.19, 0.43, 0.99, 2.76, 3.28, 3.11, 3.16, 2.38, 3.2, 1.65, 0.71, 2.28, 3.1, 0.98, 1.02, 3.08, 1.15, 1.08, 1.5, 3.11, 3.04, 3.08, 1.05, 3.12, 1.19, 2.4, 1.04, 3.08, 0.75, 2.6, 2.54, 0.9, 3.1, 3.09, 0.6, 1.03, 3.07, 2.4, 1.02, 3.09, 1.06, 0.77, 2.16, 3.01, 3.06, 1.02, 3.09, 3.15, 1.15, 1.02, 2.86, 1.58, 3.11, 3.11, 3.06, 3.15, 3.02, 0.46, 3.09, 2.37, 1.88, 0.82, 1.91, 3.09, 0.64, 0.77, 0.94, 3.34, 3.05, 1.94, 3.1, 3.09, 0.54, 3.03, 1.11, 3.08, 0.89, 0.53, 0.92, 2.51, 3.02, 2.23, 3.03, 0.93, 0.51, 1.02, 3.1, 2.13, 1.77, 3.22, 1.8, 1.02, 0.93, 3.11, 1.06, 2.98, 2.08, 2.28, 3.09, 0.76, 1.22, 1.68, 3.1, 1.9, 3.1, 3.14, 3.14, 0.46, 3.13, 3.46, 2.81, 1.78, 3.08, 0.64, 2.99, 2.45, 1.68, 1.67, 2.99, 3.09, 3.12, 3.11, 3.09, 0.96, 3.11, 2.89, 0.45, 1.74, 3.48, 3.06, 3.21, 2.92, 1.61, 3.09, 0.72, 0.51, 3.13, 3.32, 3.09, 0.65, 1.18, 0.78, 0.85, 2.22, 3.05, 0.75, 1.02, 3.02, 3.12, 2.2, 3.12, 2.77, 2.26, 0.85, 0.7, 0.71, 0.95, 3.04, 0.89, 3.09, 3.11, 3.09, 3.06, 2.23, 3.1, 1.89, 1.71, 0.44, 0.79, 2.42, 0.97, 1.78, 3.08, 1.65, 2.61, 3.48, 2.97, 1.23, 2.34, 3.08, 3.07, 2.58, 3.11, 1.42, 0.97, 3.1, 3.17, 1.63, 3.08, 2.86, 3.08, 1.1, 1.77, 0.86, 2.87, 2.35, 3.16, 2.3, 2.08, 0.52, 1.67, 2.78, 1.33, 3.1, 1.57, 1.23, 2.56, 1.9, 3, 0.93, 1.8, 2.14, 1.77, 0.67, 1.5, 3.12, 3.1, 2.04, 0.83, 3.07, 3.08, 1.49, 0.45, 3.09, 1.91, 1.57, 0.63, 3.08, 1.01, 0.86, 3.06, 2.25, 2.88, 3.04, 3.11, 0.95, 3.08, 1.57, 3.08, 1.68, 0.49, 3.1, 0.94, 1.81, 2.95, 3.05, 1.04, 3.07, 1.54, 0.84, 1.02, 3.12, 3.12, 2.11, 0.6, 3.09, 3.11, 3.13, 1.34, 3.11, 3.12, 3.11, 3.12, 0.78, 3.03, 1.79, 1.37, 3.07, 1.9, 3.08, 3.22, 3.14, 3.11, 1.34, 3.08, 3.06, 2.03, 2.98, 2.36, 1.03, 0.51, 2.06, 0.68, 1.19, 3.08, 3.06, 1.99, 1.46, 2.3, 1.32, 3.05, 3.1, 2.08, 0.44, 2.27, 1.52, 0.45, 1.69, 2.23, 0.71, 3.1, 2.69, 1.71, 1.1, 3.05, 2.02, 2.8, 3.11, 1.28, 1.48, 2.68, 1.29, 2.48, 3.29, 2.82, 1.25, 3.09, 0.42, 3.14, 2.56, 3.1, 1.36, 3.12, 1.65, 1.56, 1.83, 2.18, 1.5, 2.3, 1.04, 2.3, 3.09, 1.42, 0.73, 2.68, 1.08, 2.48, 0.55, 3.08, 0.75, 0.46, 2.03, 2.09, 0.79, 2.07, 2.86, 3.13, 3.1, 1.83, 2.4, 2.71, 1.24, 2.23, 3.38, 3.11, 1.32, 3.13, 2.62, 1.73, 3.09, 3.11, 0.68, 2.22, 1.24, 3.1, 3.14, 0.48, 1.67, 2.78, 3.08, 3.04, 2.08, 2.45, 0.57, 3.13, 1.59, 3.09, 0.75, 0.77, 0.89, 1.09, 3.08, 0.94, 3.08, 1.44, 3.39, 3.04, 1.19, 2.73, 1.24, 3.15, 1.87, 2.8, 2.39, 0.77, 1.15, 1.91, 3.09, 3.06, 0.82, 3.14, 1.34, 2.78, 1.03, 0.86, 3.26, 2.99, 3.1, 3.12, 1.59, 3.07, 1.47, 0.43, 2, 0.9, 3.07, 2.81, 0.78, 1.14, 3.14, 0.61, 0.43, 2.78, 3.09, 1.8, 2.2, 0.57, 3.2, 1.19, 3.07, 0.69, 2.41, 1.73, 2.49, 2.05, 3.09, 3.17, 0.64, 3.1, 2, 2.45, 3.12, 3.11, 2, 3.14, 2.95, 2.05, 1.51, 0.47, 3.12, 2.85, 1.77, 2.97, 3.1, 3.08, 3.01, 3.06, 3.13, 2.16, 1.34, 1.82, 2.2, 0.51, 0.79, 3.06, 2, 0.47, 0.85, 0.81, 3.09, 2.05, 3.2, 1.82, 0.97, 3.16, 0.47, 3.46, 0.72, 3.09, 0.93, 1.04, 3.12, 1.9, 2.13, 3.09, 3.06, 1.94, 3.11, 3.03, 0.43, 3.06, 3.08, 3.12, 0.44, 3.08, 2.09, 2.07, 3.09, 1.91, 3.07, 0.69, 0.99, 1.17, 1.26, 3.05, 3.09, 1.71, 1.92, 2.27, 3.1, 1.07, 3.05, 1.42, 3.08, 3.05, 3.25, 3.35, 1.11, 2.31, 0.75, 2.51, 0.8, 3, 2.32, 1.68, 0.44, 2.11, 3.08, 0.52, 0.47, 0.78, 3.12, 1.1, 0.5, 3.08, 1.01, 0.92, 1.73, 2.2, 0.99, 3.08, 3.15, 0.78, 1.99, 1.05, 0.57, 1.1, 0.67, 2.16, 1.48, 1.25, 3.09, 0.47, 3.12, 2.98, 1.86, 3.11, 1.24, 1.36, 1.7, 2.22, 3.11, 2.98, 1.67, 0.95, 3.05, 3.07, 3.29, 3.12, 1.96, 3.06, 1.04, 3.09, 1.19, 0.97, 3.1, 3.45, 2.09, 3.06, 3.1, 3.06, 2.6, 1.99, 1.69, 2.15, 3.08, 1.25, 0.73, 0.53, 0.94, 3.06, 2.82, 2.58, 1.14, 3.08, 2.69, 2.01, 2.78, 1.02, 2.48, 1.06, 3.05, 1.94, 1.54, 3.08, 1.69, 3.15, 0.73, 1.43, 2.47, 3.09, 0.91, 3.04, 0.77, 0.52, 0.78, 3.08, 3.22, 2.69, 3.06, 2.3, 3.08, 3.09, 3.14, 3.07, 3.12, 1.73, 1.77, 1.37, 1, 2.55, 3.07, 2.44, 0.58, 2.54, 3.01, 3.11, 0.91, 1.54, 1.08, 3.08, 3.06, 2.19, 2.19, 3.09, 0.42, 3.1, 0.89, 2.55, 1.92, 2.26, 0.41, 3.06, 3.07, 2.28, 3.12, 1.65, 1.36, 3.16, 3.12, 1.39, 1, 1.51, 3.05, 1.83, 1.75, 1.1, 3.12, 1.24, 3.03, 0.77, 2.08, 2.15, 1.69, 3.04, 1.27, 1.32, 3.06, 3.14, 3.09, 2.05, 3.15, 2.92, 3.05, 2.36, 3.03, 3.09, 2.82, 1.25, 2.75, 3.08, 3.05, 1.81, 3.1, 3.05, 0.68, 3.07, 3, 3.41, 3.07, 1.43, 0.88, 3.01, 0.82, 1, 3.38, 1.14, 1.18, 3.04, 3.06, 3.12, 2.95, 1.72, 2.18, 3.02, 2.88, 0.76, 3.02, 3.04, 3.09, 2.89, 3.09, 3.11, 1.59, 3.09, 2.5, 3.08, 3.1, 0.88, 2.99, 3.06, 1.49, 2, 3.05, 0.43, 2.73, 1.28, 3.26, 2.01, 3.07, 0.59, 2.77, 0.58, 3.01, 0.94, 1.84, 1.91, 3.09, 0.86, 1.03, 3.11, 3.16, 0.9, 0.97, 3.15, 1.96, 3.16, 1.1, 3.08, 1.15, 2.15, 1.3, 3.17, 1.95, 3.1, 3.23, 0.98, 3.12, 3.07, 3.06, 1.47, 3.07, 3.08, 3.08, 1.07, 3.16, 3.17, 3.12, 3.08, 2.53, 2.31, 0.57, 3.09, 1.33, 3.11, 3.15, 3.04, 1.78, 3.02, 2.77, 3.11, 3.07, 3.23, 0.72, 1.12, 3.09, 3.11, 1.25, 2.53, 1.19, 0.86, 3.04, 3.09, 3.11, 0.95, 3.09, 2.25, 1.1, 3.12, 3.11, 0.77, 2.05, 2.73, 0.41, 2.21, 1.16, 3.1, 1.92, 1.52, 0.83, 1.22, 1.02, 2.12, 3.08, 2.16, 1.88, 0.83, 3.1, 3.08, 3.1, 3.13, 2.08, 0.77, 1.43, 3.1, 1.18, 1.85, 1.45, 2.27, 2.02, 3.06, 3.11, 3.1, 2.27, 1.86, 1.18, 2.93, 1.2, 0.85, 3.1, 3.05, 1.09, 1.14, 1.37, 1.04, 1, 0.79, 3.11, 0.9, 1.63, 0.88, 3.1, 3.08, 1.6, 0.49, 3.07, 1.03, 2.84, 3.06, 3.11, 3.07, 3.08, 3.12, 1.64, 3.05, 1.03, 1.49, 1.1, 1.28, 2.95, 0.78, 1.5, 0.58, 3.11, 3.36, 2.12, 3.08, 2.55, 2.69, 1.78, 1.46, 0.48, 1.61, 0.62, 0.66, 3.1, 3.1, 1.44, 3.11, 3.3, 0.78, 1.29, 1.95, 0.76, 3.09, 2.31, 2, 0.76, 2.3, 3.12, 3.08, 1.01, 1.76, 1.18, 2.94, 1.5, 0.51, 1.97, 3.11, 1.03, 0.96, 3.09, 1.7, 1.19, 1.6, 1.39, 1.32, 3.14, 2.16, 3.1, 2.65, 1.65, 3.11, 2.76, 1.6, 0.67, 2.37, 0.46, 2.51, 0.43, 1.53, 3.37, 2.31, 3.13, 1.5, 1.28, 3.07, 3.15, 1.83, 1.44, 2.38, 2.06, 3.02, 2.08, 0.49, 3.18, 2.33, 3.08, 3.14, 3.08, 2.08, 3.03, 1.48, 0.54, 2.32, 3.14, 1.95, 1.4, 0.5, 3.04, 1.21, 2.03, 1.02, 1.95, 1.03, 2.4, 0.46, 2.29, 3.12, 3.12, 2.55, 2.78, 0.98, 2.26, 3.07, 1.74, 2.71, 3.09, 1.57, 1.03, 1.98, 0.63, 3.06, 1.06, 3.12, 0.67, 3.09, 3, 2.13, 2.48, 3.1, 3.07, 3.11, 1.58, 0.59, 3.08, 2.14, 2.96, 2.09, 2.4, 3.16, 0.89, 0.5, 0.86, 3.11, 2.86, 3.09, 2.38, 3.12, 1.53, 1.56, 1.26, 3.05, 3.15, 3.43, 0.98, 1.49, 1.1, 1.43, 2.6, 3.12, 3.08, 0.4, 2.26, 1.67, 3.1, 3.13, 2.23, 1.1, 2.54, 3.16, 3.1, 3.14, 1.31, 1.13, 0.47, 2.51, 0.99, 0.94, 0.44, 3.29, 3.05, 3.07, 2.42, 3.14, 2.82, 3.06, 1.55, 1, 0.79, 3.1, 2.63, 2.78, 2.45, 2.03, 1.49, 3.04, 2.05, 1.19, 1.52, 3.1, 3.06, 3.07, 1.25, 3.08, 0.62, 3.09, 3.08, 3.33, 3.06, 3.03, 1.21, 3.07, 0.97, 2.84, 1.91, 2.37, 3.14, 2.18, 1.1, 3.12, 2.1, 3.11, 0.66, 1.14, 2.8, 1.95, 0.96, 3.03, 0.48, 2.92, 2.93, 1.68, 2.22, 2.74], &quot;higgs4l&quot;: [185.69, 314.54, 84.67, 90.24, 188.93, 188.72, 97.49, 244.61, 141.93, 90.01, 193.9, 261.28, 163.11, 235.35, 198.02, 338.79, 96.21, 275.65, 218.02, 147.77, 574.54, 263.2, 229.58, 90.68, 228.24, 148.95, 321.56, 212.44, 147.02, 377.94, 144.29, 175.02, 199.2, 186.73, 588.98, 126.48, 188.22, 180.83, 304.72, 205.79, 227.73, 200.89, 392.91, 87.46, 274.44, 198.18, 277.99, 165.08, 189.82, 128.58, 281.27, 233.77, 246.19, 236.92, 328.31, 211.81, 206.08, 211.38, 390.28, 96.61, 109.82, 157.87, 121.56, 187.28, 194.9, 169.95, 239.76, 160.66, 204.41, 126.29, 289.45, 172.66, 217.12, 185.04, 136.48, 221.32, 272.77, 246.27, 156.12, 96.34, 477.96, 212.61, 89.02, 293.5, 383.02, 214.1, 209.34, 124.63, 235.93, 276.64, 187.41, 210, 269.47, 160.54, 216.24, 598.99, 567.96, 271.04, 297.31, 357.09, 185.88, 182.31, 233.02, 209.54, 253.25, 157.52, 220.24, 258.24, 257.67, 515.34, 208.73, 226.87, 129.91, 479.15, 187.58, 205.8, 680.2, 125.53, 285.96, 186.91, 100.92, 95.43, 138.19, 363.54, 213.5, 89.67, 203.77, 87.15, 95.01, 208.31, 237.72, 249.09, 192.24, 201.2, 227.55, 250.38, 459.05, 232.16, 153.92, 211.48, 161.96, 201.86, 91.7, 317.19, 197.77, 270.88, 511.62, 237.99, 282.08, 177.28, 240.06, 189.59, 193.06, 200.79, 187.41, 275.75, 255.2, 276.26, 320.51, 125.16, 239.93, 89.26, 125.37, 172.23, 154.95, 91.45, 235.88, 79.39, 232.93, 119.29, 92.6, 211.12, 145.66, 86.29, 197.58, 92.16, 220.66, 310.51, 465.2, 120.53, 92.31, 221.68, 93.24, 140.12, 209.54, 305.76, 93, 92.28, 89.39, 461.7, 190.2, 200.39, 206.29, 88.68, 191.83, 287.39, 91.81, 191.05, 214.77, 113.8, 548.47, 180.43, 192.95, 90.02, 86.35, 90.76, 89.81, 243.86, 164.03, 233.47, 197.66, 196.54, 228.6, 177.54, 742.15, 251.98, 357.32, 84.64, 89.4, 86.29, 203.86, 180.99, 125.34, 389.96, 144.45, 199.58, 547.08, 337.73, 270.33, 255.28, 184.11, 262.81, 96.31, 212.39, 92.36, 213.1, 91.31, 122, 183.37, 87.3, 238.69, 95.2, 86.66, 91.69, 435.34, 322.63, 100.87, 253.44, 243.91, 205.71, 242.49, 246.28, 198.43, 90.02, 90.11, 118.8, 89.32, 85.8, 196.8, 279.21, 200.39, 144.32, 109.72, 121.81, 90.76, 182.48, 144.84, 100.18, 446.41, 188.53, 188.51, 232.6, 172.72, 95.88, 316.98, 258.31, 182.86, 214.47], &quot;topo&quot;: { &quot;Z0&quot;: [[44.11, 1.06, 1.95, 1, 45.2, 0.77, -1.24, -1], [49.86, 1.81, -2.82, -1, 39.68, 1.57, 0.21, 1], [51.18, -0.43, -1.57, 1, 46.25, -0.34, 1.25, -1], [28.07, 1.6, -0.34, 1, 32.71, -0.43, 2.68, -1], [40.78, 1.29, -0.69, -1, 26.89, -0.48, 2.82, 1], [35.31, -1.4, -2.74, -1, 37.65, 0.09, 0.65, 1], [37.86, -0.77, -2.06, -1, 38.12, 0.45, 0.91, 1], [43.23, 0.59, -2.75, 1, 45.98, 0.23, 0.42, -1], [37.3, -2.23, 1.67, 1, 45.3, -1.18, -1.45, -1], [46.77, -2.01, 1.18, 1, 42.5, -1.45, -2.07, -1], [43.67, -0.25, -1.39, -1, 41.82, -0.85, 1.98, 1], [33.91, -1.89, 2.68, 1, 50.67, -0.7, 0.18, -1], [41.19, 1.19, -0.15, -1, 39.11, 0.35, 3.1, 1], [48.14, -0.08, -2.67, 1, 45.37, 0.23, -0.07, -1], [38.64, 1.27, 0.41, -1, 53.11, 0.85, -2.42, 1], [45.42, -1.18, 2.41, -1, 40.2, -0.38, -0.76, 1], [41.69, 0.37, 1.27, 1, 48.11, 0.68, -2, -1], [53.04, -1.16, -2.46, -1, 35.91, -0.56, 0.65, 1], [25.35, -1.11, 0.29, -1, 27.79, 1.17, -3.02, 1], [42.87, -1.96, 0.05, 1, 43.45, -2.12, -3.03, -1], [44.23, -1.5, -0.11, 1, 41.94, -1.07, 2.93, -1], [58.54, 0.56, -2.8, -1, 35.84, 0.86, 0.48, 1], [47.76, 1.25, -0.79, -1, 40.24, 1.59, 2.53, 1], [23.18, 1.41, 1.82, 1, 37.4, -0.52, -1.34, -1], [49.79, -0.24, -2.07, -1, 39.66, -0.58, 1.26, 1], [44.04, 0.1, -1.69, 1, 46.19, 0.64, 1.43, -1], [40.75, 1.82, -2.94, -1, 46.78, 1.09, 0.31, 1], [37.44, -0.78, -1.71, -1, 39.71, 0.4, 1.29, 1], [44.76, 0.75, -0.92, -1, 45.68, 0.57, 2.03, 1], [37.78, -1.3, 0.38, 1, 18.54, 0.86, -2.92, -1], [49.82, 2.01, -1.49, -1, 39.41, 1.33, 1.67, 1], [30.38, 0.35, -1.52, 1, 63.96, -0.12, 2.18, -1], [40.41, 2.19, 1.98, -1, 27.44, 0.48, -1.26, 1], [27.8, -0.81, -2.45, 1, 42.13, 0.87, 0.56, -1], [113.96, -2.12, -0.56, 1, 39.46, -0.95, -0.15, -1], [46.67, -1.39, -2.97, 1, 44.46, -1.32, 0, -1], [30.92, 1.54, -0.72, 1, 32.25, -0.24, 2.33, -1], [38.89, -1.12, -1.52, 1, 43.48, -0.25, 1.77, -1], [34.43, 0.34, -1.86, -1, 41.53, -0.9, 1.81, 1], [34.54, -0.08, -2.07, -1, 61.62, -0.81, 2, 1], [39.15, 1.68, -1.59, 1, 27.13, -0.1, 1.82, -1], [29.22, -0.63, -0.47, -1, 92.85, -0.61, 1.79, 1], [45.16, -1.1, 2.11, 1, 41.78, -0.5, -0.96, -1], [49.47, 1.68, 3.05, 1, 13.64, -0.67, -0.34, -1], [28.32, -1.16, 0.48, -1, 42.91, 0.48, -2.29, 1], [26.36, 1.53, 0.55, -1, 81.54, 1.05, -2.07, 1], [29.79, -1.07, 0.59, 1, 25.93, 1.09, -2.54, -1], [38.02, 2.12, -2.59, 1, 33.87, 0.58, 0.7, -1], [46.31, -1.87, 3.08, 1, 42.2, -1.55, 0.36, -1], [36.58, 1.14, -2.37, -1, 41.51, 0.01, 1.02, 1], [51.8, -1.1, -1.16, 1, 43.62, -0.82, 1.65, -1], [18.33, -1.99, 1.41, 1, 20.78, 1.01, -1.98, -1], [36.29, -1.81, 0.29, -1, 44.95, -0.98, -3.05, 1], [43.98, -1.81, -3.02, -1, 45.8, -0.42, -1.62, 1], [23.68, 1.04, -2.2, -1, 40.41, -0.88, 1.1, 1], [43.86, -2.01, 1.57, -1, 48.65, -1.5, -1.31, 1], [26.39, 2.02, 1.18, -1, 50.29, 0.43, -0.91, 1], [34.61, -1.93, 2.24, -1, 28.87, -0.08, -1.15, 1], [66.26, 0.99, -0.35, 1, 51.7, 0.17, 1.14, -1], [44.31, 0.07, -2.78, 1, 48.09, 0.15, 0.36, -1], [21.04, 2.33, 0.79, -1, 29.84, -0.02, -2.7, 1], [31.45, 1.08, -0.66, -1, 38.37, -0.39, 2.36, 1], [27.86, 2.16, -1.91, -1, 32.24, 0.16, 0.91, 1], [46.25, -0.91, 3.05, 1, 42.36, -0.78, -0.05, -1], [26.68, 1.29, 0.86, -1, 37.58, -0.51, -2.79, 1], [45.52, 0.06, -0.55, -1, 45.51, -0.07, 2.62, 1], [37.28, 1.06, 2.35, 1, 33.17, -0.52, -0.94, -1], [41.15, -1.12, 2.15, -1, 40.04, -0.31, -1.05, 1], [44.29, -1.05, -1.67, -1, 43.82, -0.4, 1.61, 1], [42.34, 1.05, 0.03, 1, 43.25, 0.35, -3.1, -1], [35.09, -1.52, 1.99, -1, 38.73, -0.18, -0.88, 1], [44.75, 0.06, -2.98, -1, 43.97, 0.46, 0.12, 1], [63.98, -0.5, -1.95, 1, 26.79, 0.43, 1.6, -1], [47.86, -2.01, -2.19, -1, 35.73, -1.08, 0.9, 1], [43.56, 0.95, 1.67, 1, 45.55, 0.13, -1.48, -1], [37.09, -0.5, -0.87, 1, 55.69, -0.43, 2.33, -1], [51.07, 1.52, -0.16, -1, 29.1, 0.37, 3.12, 1], [43.6, 0.12, -2.48, 1, 40.17, 0.61, 0.42, -1], [40.34, 1.07, 2.7, -1, 32.83, -0.3, -0.6, 1], [37.76, 1.92, -1.54, 1, 41.06, 0.94, 1.68, -1], [49.31, -1.36, -1.57, -1, 41.19, -0.92, 1.58, 1], [46.31, 2.01, -2.81, 1, 54.52, 1.11, -1, -1], [47.34, -0.72, 3.1, -1, 42.02, -0.86, -0.23, 1], [47.85, 0.25, -2.35, -1, 43.18, 0.55, 0.82, 1], [48.57, 1.25, 2.71, -1, 43.74, 1.02, -0.46, 1], [47.86, 1.49, 1.1, 1, 39.71, 1.05, -1.99, -1], [23.44, 1.1, 0.48, 1, 69.2, -0.43, -0.96, -1], [47.13, 0.05, 0.37, 1, 42.05, -0.52, -3.07, -1], [34.33, -1.26, 1.92, 1, 40.42, 0.1, -1.17, -1], [43.78, 2.17, -0.75, 1, 43.75, 1.35, 2.08, -1], [44.76, 1.54, 1.75, 1, 46.54, 0.9, -2.19, -1], [44.87, -0.12, -0.83, -1, 40.31, -0.66, 2.33, 1], [52.52, -0.4, -1.66, -1, 37.71, -0.42, 1.57, 1], [45.96, -1.33, -0.98, 1, 39.06, -0.52, 2.21, -1], [36.19, -1.5, 2.79, -1, 38.4, -0.28, -0.33, 1], [26.66, -0.3, -1.33, -1, 75.87, -0.6, 1.91, 1], [39.36, 1.05, 2.24, 1, 53.67, 0.38, -0.29, -1], [37.72, 0.4, -0.34, -1, 42.11, -0.7, 2.61, 1], [36.87, -2.4, -2.77, -1, 43.53, -1.33, 0.29, 1], [42.7, 1.43, 0.43, 1, 44.17, 1.12, -2.65, -1], [27.39, 1.55, -1.03, -1, 39.44, -0.17, 2.08, 1], [29.88, 1.7, -0.61, 1, 35.12, -0.03, 2.42, -1], [40.42, -1.07, -1.03, -1, 33.5, 0.23, 2.65, 1], [43.06, 0.25, 2.27, 1, 42.56, 0.91, -1.03, -1], [25.04, -1.38, -1.53, -1, 27.96, 0.83, 2.01, 1], [38.85, -1.87, 0.33, 1, 34.4, -0.54, -2.77, -1], [25.03, -1.06, -2.45, -1, 24.12, 1.3, 0.92, 1], [46.94, -1.31, -1.56, -1, 44.66, -1.16, 1.62, 1], [42.8, 1.55, 2.38, 1, 43.85, 1.34, -0.82, -1], [42.63, -0.91, 2.02, 1, 42.13, -0.27, -0.98, -1], [45.59, -0.11, -2.71, 1, 41.74, 0.52, 0.42, -1], [26.37, 2.25, -0.3, -1, 29.86, 0.19, 2.81, 1], [40.55, -1.16, 2, 1, 36.33, 0.01, -1.2, -1], [23.93, 1.48, -0.07, -1, 25.35, -1, 2.97, 1], [43.91, -1.12, -0.82, -1, 16.14, 1.21, 1.36, 1], [46.56, 1.32, -1.28, -1, 47.03, 1.16, 2.14, 1], [38.11, 1.99, 1.51, 1, 44.16, 1.09, -1.71, -1], [33.32, -1.58, -3.02, -1, 37.12, -0.1, 0.2, 1], [142.48, -0.48, -0.97, -1, 45.87, -0.56, 0.25, 1], [68.64, -1.72, 1.13, 1, 33.05, -0.47, -0.46, -1], [16.15, -1.4, 0.14, 1, 25.57, 1.66, -0.94, -1], [34.16, -0.13, -2.22, -1, 59.83, -0.6, 0.53, 1], [44.79, -1.55, 1.68, 1, 39.43, -0.9, -1.77, -1], [28.5, -0.95, 2.81, -1, 48.94, 0.38, -0.57, 1], [31.86, 1.97, 1.41, -1, 37.28, 0.45, -1.78, 1], [27.24, -1.59, -0.03, 1, 18.81, 1.12, -1.66, -1], [43.84, -1.3, 1.79, -1, 44.53, -0.53, -1.55, 1], [41.87, 0.26, -1.58, 1, 47.93, 0.66, 1.64, -1], [36.96, -0.12, -2.51, 1, 51.46, 0.1, 0.71, -1], [40.94, -1.27, -3.12, -1, 37.33, -0.22, -0.21, 1], [49.91, -1.25, -2.78, -1, 43.36, -1.33, 0.68, 1], [32.17, -1.54, -2.07, 1, 13.42, 1.5, -2.42, -1], [37.16, 1.96, 0.95, 1, 40.34, 0.77, -2.33, -1], [74.17, 0.28, 0.76, 1, 25.14, 0.67, -2.36, -1], [31.61, 0.66, 1.57, 1, 38.3, -0.87, -1.42, -1], [38.43, 1.6, 2.35, 1, 39.7, 0.55, -0.85, -1], [44.86, 0.65, -2.33, 1, 43.69, 0.06, 0.97, -1], [38.95, 0.4, -0.54, -1, 48.62, -0.4, 3.05, 1], [39.73, -0.71, -0.31, 1, 48.31, -0.2, 2.97, -1], [33.63, 1.89, 2.75, 1, 31.9, 0.09, -0.18, -1], [37.95, 1.95, 0.18, 1, 20.03, -0.23, 3.13, -1], [43.24, 1.31, 2.37, 1, 43.31, 0.73, -0.89, -1], [15.72, -1.84, 2.77, -1, 19.54, 1.28, -0.58, 1], [46.92, -1.01, -0.66, 1, 43.95, -0.79, 2.56, -1], [36.09, -2.01, -2.17, 1, 39.71, -0.71, 0.85, -1], [30.6, -1.78, -2.68, -1, 33.99, 0.03, 0.98, 1], [40.13, -1.22, 0.17, 1, 51.85, -0.57, -2.96, -1], [43.33, 1.82, -0.66, 1, 46.7, 1.49, 2.58, -1], [40.6, 1.84, -0.94, 1, 34.1, 0.46, 2.1, -1], [36.65, -1.91, 0.82, 1, 39.62, -0.58, -2.55, -1], [22.66, 1.46, -2.24, 1, 38.79, -0.54, 0.2, -1], [43.96, 1.51, -0.85, 1, 43.2, 0.89, 2.5, -1], [43.7, 1.44, -2.47, -1, 19.59, -0.67, 1.34, 1], [67.26, 1.35, -1.66, 1, 45.71, 1.16, 2.69, -1], [32.76, -1.57, 0.85, 1, 33.83, 0.14, -2.32, -1], [51.75, -0.47, -2.52, -1, 43.41, -0.15, 0.87, 1], [38.4, -1.63, -1, 1, 43.3, -0.69, 2.17, -1], [47.79, 1.84, -0.66, -1, 46.89, 1.21, -3.14, 1], [40.44, -1.88, -0.38, 1, 35.04, -0.61, 2.7, -1], [47.37, -2.33, -0.2, -1, 42.13, -1.76, 2.9, 1], [46.11, 1.81, 0, -1, 43.51, 1.6, 2.93, 1], [50.77, -1.38, 2.79, -1, 26.57, 0.67, -2.96, 1], [37.57, 1.72, 1.65, 1, 32.56, 0.19, -1.71, -1], [57.81, 1.3, 1.44, -1, 61.68, 0.67, -0.21, 1], [44.76, -1.98, -1.04, 1, 31.76, -0.67, 2.13, -1], [36.74, -1.31, -0.46, -1, 29.41, 0.34, 2.58, 1], [42.58, 1.54, 0.44, -1, 45.46, 0.94, -2.71, 1], [47.14, 0.64, -1.02, 1, 44.98, 0.76, 2.15, -1], [46.5, 1.2, 0.48, -1, 42.32, 0.82, -2.75, 1], [37.62, -0.97, 1.73, -1, 14.09, 1.66, -1.2, 1], [41.06, 1.56, -2.94, -1, 31.16, 0.15, 0.14, 1], [39.42, -0.06, -1.03, 1, 39.38, 0.96, 2.12, -1], [30.04, 0.11, 2.25, 1, 72.24, -0.88, 0.31, -1], [24.05, 2.22, 1.68, 1, 26.6, -0.16, -0.74, -1], [44.07, -0.32, -2.04, 1, 47.38, -0.05, 0.98, -1], [17.99, -1.09, 1.69, -1, 17.16, 2.01, -1.03, 1], [42.31, -1.42, -2.2, 1, 41.76, -0.64, 1.12, -1], [34.21, 1.42, -0.5, -1, 27.77, -0.44, 2.6, 1], [49.58, -0.77, -2.46, -1, 42.81, -0.38, 0.16, 1], [20.63, 2.18, -1.89, -1, 21.69, -0.6, 1.38, 1], [42.36, 1.48, -1.21, -1, 42.04, 0.68, 1.93, 1], [52.39, -1.21, 0.95, 1, 41.28, -1.35, -2.47, -1], [42.05, -1.43, 3.13, 1, 42.24, -1.03, 0.23, -1], [36.79, 1.18, 2.01, 1, 32.66, -0.47, -1.28, -1], [14.66, -1.95, 1.06, 1, 15.63, 1.58, -2.86, -1], [18.06, -2.1, 1.15, -1, 38.27, 0.23, -2.15, 1], [39.24, -1.52, 1.15, 1, 48.54, -0.81, -1.99, -1], [92.87, -0.15, -0.36, -1, 20.96, 0.34, 2.66, 1], [40.01, 0.58, -2.72, -1, 51.02, -0.05, 0.65, 1], [36.05, -1.54, -0.78, -1, 15.47, 1.21, -2.92, 1], [54.03, 0.91, 0.06, 1, 36.41, 0.37, 2.92, -1], [39.09, -1.68, 2.71, 1, 55.05, -1.25, -1.02, -1], [43.64, 1.31, -2.43, 1, 27.88, -0.26, 0.58, -1], [46.29, -0.93, -0.15, 1, 43.6, -0.89, 3.11, -1], [41.78, 1.64, 0.22, -1, 37.89, 0.57, 2.83, 1], [35.39, 0.74, -0.88, 1, 37.96, -0.69, 2.06, -1], [25.22, -1.37, -1.19, -1, 19.9, 1.31, 1.94, 1], [98.59, -0.57, -1, -1, 28.3, -0.52, 1.08, 1], [54.68, -0.78, -3.06, -1, 34.47, -0.41, 0.3, 1], [30.93, -1.76, -2.45, 1, 49.93, -0.51, 0.8, -1], [18.5, -2.03, -0.71, -1, 23.29, 0.82, 2.17, 1], [50.06, -1.24, 2.91, 1, 41.18, -1.15, -0.49, -1], [35.32, -1.33, 0.5, 1, 32.72, 0.18, -2.85, -1], [37.7, -2.01, 0.55, -1, 24.92, -0.13, -2.72, 1], [43.53, -0.94, -2.59, 1, 39.25, -0.19, 0.51, -1], [44.1, -1.45, -2.54, -1, 43.88, -2.21, 0.18, 1], [35.7, 1.47, 0.89, 1, 35.68, 0.02, -2.31, -1], [26.45, 1.69, -0.49, 1, 28.92, -0.81, -1.21, -1], [36.57, -1.22, 0.65, -1, 38.15, 0.1, -2.57, 1], [27.37, 0.58, -2.43, -1, 80.03, 0.61, 1.25, 1], [32.97, -1.08, -0.78, 1, 35.41, 0.51, 2.34, -1], [46.94, 1.24, -0.62, -1, 42.57, 0.94, 2.66, 1], [85.57, -0.65, -3.11, 1, 25.73, -0.46, -0.47, -1], [83.24, 0.33, 0.18, -1, 26.64, 0.18, 2.81, 1], [32.27, -2.13, 0.08, -1, 12.87, 0.82, -2.78, 1], [24.8, -1.75, -1.24, -1, 24.64, 0.72, 2.33, 1], [36.56, 1.8, 1.34, -1, 38.24, 0.47, -1.8, 1], [46.74, -0.4, 0.74, 1, 43.04, -0.81, -1.95, -1], [22.29, -1.33, 0.55, 1, 20.66, 1.45, -2.52, -1], [44.44, 0.31, -1.87, -1, 47.79, 0.34, 1.19, 1]], &quot;Jpsi&quot;: [[21.24, 1.08, 1.3, -1, 8.77, 0.85, 1.29, 1], [8.17, -0.31, -0.87, 1, 9.32, -0.65, -0.9, -1], [7.65, 0.93, 1.28, 1, 9.34, 1.23, 1.48, -1], [3.21, -1.49, -3.04, -1, 3.32, -2.23, 2.65, 1], [6.67, -1.23, 1.55, 1, 6.91, -0.77, 1.64, -1], [4.11, -2.25, -1.05, -1, 1.11, -1.94, 0.62, 1], [10.72, -0.24, 0.16, -1, 9.54, -0.13, 0.44, 1], [12.67, -0.04, 1.66, 1, 10.16, 0.15, 1.86, -1], [7.38, 0.99, -2.49, 1, 8.75, 1.11, -2.85, -1], [8.79, -0.77, -1.81, -1, 15.5, -0.88, -1.57, 1], [4.37, 0.86, 1.08, -1, 5.68, 0.25, 1.22, 1], [3.12, 1.78, -2.46, 1, 2.84, 2.09, 2.86, -1], [13.77, -0.41, -2.73, 1, 8.93, -0.64, -2.89, -1], [5.56, -1.83, 0.44, 1, 3.06, -2.24, 1.1, -1], [6.08, 0.16, -0.8, 1, 7.48, 0.18, -1.26, -1], [4.36, 0.55, -0.34, 1, 3.49, -0.22, -0.41, -1], [3.8, 2.02, -1.77, 1, 3.33, 2.04, -2.69, -1], [11.61, 0.94, 2.67, -1, 7.28, 0.62, 2.76, 1], [4.97, -0.48, 1.82, -1, 3.87, -0.02, 2.36, 1], [14.74, 1.64, 2.77, -1, 8.07, 1.43, 2.95, 1], [5.86, 1.97, 0.49, 1, 9.49, 2.02, 0.9, -1], [6.64, 0.89, -1.93, 1, 22.42, 0.9, -2.19, -1], [8.15, -0.62, 0.36, 1, 20.94, -0.71, 0.58, -1], [3.24, -1.57, -1.92, 1, 4.43, -2.2, -1.46, -1], [9.67, 0.4, 1.12, 1, 8.71, 0.69, 0.97, -1], [4.74, 1.83, 2.96, -1, 3.2, 2.05, -2.52, 1], [12.01, -0.49, -2.15, 1, 7.02, -0.16, -2.09, -1], [8.43, -0.41, 1.47, 1, 11.98, -0.47, 1.77, -1], [3.82, 2.21, -0.55, 1, 3.89, 1.54, -0.12, -1], [9.47, 1.22, 2.21, 1, 16.93, 0.98, 2.18, -1], [2.63, 1.58, -2.65, -1, 1.63, 2.19, -1.12, 1], [5.15, 0.96, 1.27, 1, 40.18, 0.81, 1.42, -1], [7.76, 1.38, -0.03, -1, 6.61, 1.07, -0.31, 1], [8.6, 0.33, 0.55, 1, 34.47, 0.27, 0.71, -1], [13.24, -0.39, 0.59, 1, 9.83, -0.48, 0.33, -1], [9.11, -0.65, -0.15, 1, 11.33, -0.66, 0.15, -1], [19.52, -0.95, -1.12, -1, 12.33, -0.93, -0.91, 1], [4.63, -2.22, -0.67, 1, 1.89, -2, -1.71, -1], [2.99, 1.55, 1.62, 1, 4.96, 0.73, 1.41, -1], [15.95, -0.89, -0.55, -1, 6.02, -0.78, -0.84, 1], [6.34, -1.41, -2.21, -1, 8.65, -1.02, -2.36, 1], [7.89, 1.03, 0.51, 1, 6.65, 0.79, 0.16, -1], [11.56, -1.25, -3.05, -1, 17.92, -1.06, -3.13, 1], [8.08, -2.1, -0.7, 1, 6.6, -1.81, -1.02, -1], [12.98, 0.51, 1.89, 1, 6.95, 0.2, 1.94, -1], [8.53, 1.43, -1.18, -1, 7.45, 1.08, -1.01, 1], [7.77, 0.38, -0.49, 1, 6.71, -0, -0.31, -1], [8.92, 1.37, 2.58, -1, 6.54, 1.06, 2.84, 1], [6.6, 0.07, -2.83, 1, 8.79, 0.24, 3.07, -1], [8.19, 0.4, -0.17, -1, 11.93, 0.48, -0.47, 1], [6.28, 1.5, 0.17, -1, 4.45, 0.97, -0.03, 1], [10.14, 0.24, -2.65, 1, 10.54, 0.33, -2.37, -1], [6.8, 0.93, -2.73, 1, 10.58, 0.86, -3.08, -1], [6.38, 0.43, 1.77, 1, 10.12, 0.37, 2.15, -1], [4, -1.32, 2.05, -1, 4.13, -0.92, 1.4, 1], [7.32, -0.13, -1.09, -1, 6.01, 0.18, -1.43, 1], [18.91, 0.38, -1.89, -1, 11.91, 0.17, -1.91, 1], [8.34, 0.53, -0.53, -1, 7.63, 0.2, -0.35, 1], [9.81, 0.47, -2.7, 1, 6.63, 0.11, -2.83, -1], [9.69, 0.58, -0.48, -1, 4.96, 0.13, -0.55, 1], [4.28, 0.69, -0.23, 1, 7.69, 0.16, -0.35, -1], [1.68, 2.32, 3.07, 1, 3.06, 1.86, 1.67, -1], [22, 0.72, -0.69, -1, 8.43, 0.84, -0.5, 1], [15.88, 0.13, 0.76, 1, 12.48, -0.03, 0.91, -1], [12.81, 0.79, -0.73, 1, 17.54, 0.59, -0.68, -1], [3.92, -1.42, -1.79, 1, 4.1, -1.09, -2.5, -1], [8.81, -0.12, 1.68, 1, 7.32, -0.06, 1.3, -1], [7.83, -2.2, -1.26, 1, 6.33, -1.95, -0.9, -1], [8.34, 1.24, -2.01, -1, 16.71, 1.05, -2.18, 1], [9.33, -0.41, -2.48, 1, 6.09, -0.56, -2.09, -1], [4.12, -1.02, -2.67, -1, 14.63, -0.62, -2.63, 1], [7.08, 0.57, 2.67, 1, 10.32, 0.21, 2.61, -1], [6.88, 0.72, 0.41, 1, 10.12, 0.61, 0.05, -1], [8.4, 1.24, -0.48, 1, 14.64, 1.16, -0.21, -1], [21.26, 0.57, -1.53, 1, 20.43, 0.47, -1.64, -1], [14.7, 0.59, -3.12, -1, 11.7, 0.6, -2.88, 1], [9.61, 1.73, -1.86, 1, 6.72, 1.83, -1.49, -1], [9.12, -0.39, 1.73, -1, 19.44, -0.16, 1.75, 1], [18.91, -0.93, 2.95, -1, 16.93, -0.76, 2.93, 1], [18.35, -0.76, 2.74, 1, 12.61, -0.56, 2.71, -1], [2.43, 2.03, -2.92, -1, 4.65, 2.05, -1.96, 1], [13.25, 0.02, 1.23, -1, 20.02, 0.21, 1.18, 1], [14.54, -1.26, 1.87, 1, 20.44, -1.11, 1.97, -1], [3.67, -1.68, -1.51, -1, 4.07, -1.35, -2.23, 1], [5.64, 1.15, -0.01, -1, 3.56, 0.75, -0.57, 1], [15.75, 0.46, 0.75, 1, 10.98, 0.25, 0.87, -1], [6.36, -0.64, 2.53, -1, 6.69, -0.36, 2.15, 1], [7, -0.44, 3, -1, 7.56, -0.03, 2.88, 1], [9.79, -0.65, 1.61, 1, 6.99, -0.6, 1.24, -1], [7.11, 1.45, 0.63, 1, 7.15, 1.15, 0.32, -1], [9.17, -0.11, -0.6, 1, 5.96, 0.2, -0.32, -1], [3.89, 1.41, -1.26, 1, 4.66, 0.71, -1.12, -1], [23.84, -0.06, -2.21, 1, 5.22, -0.07, -1.95, -1], [4.77, -0.93, -1.41, 1, 10.95, -0.59, -1.16, -1], [1.81, -2.29, -3.02, -1, 3.41, -2.05, -1.68, 1], [8.68, -0.9, 3.1, 1, 8.63, -1.12, -2.9, -1], [15.23, 0.93, -1.5, 1, 12.14, 0.71, -1.56, -1], [16.61, -0.02, -1.26, 1, 6.23, -0.24, -1.47, -1], [7.9, -1.08, 0.84, 1, 7.08, -0.92, 0.46, -1], [8.41, -2.22, -0.16, -1, 3.45, -2.14, 0.45, 1], [3.81, 1.01, 1.57, -1, 4.2, 0.68, 2.28, 1], [5.39, 1.46, -0.23, 1, 3.82, 0.81, -0.12, -1], [43.57, 0.13, 2.47, 1, 10.15, -0.03, 2.47, -1], [7.07, 0.74, -0.07, -1, 9.66, 0.5, -0.36, 1], [6.27, 1.34, 0.42, -1, 7.01, 0.92, 0.6, 1], [6.05, 0.14, -0.92, -1, 4.02, -0.29, -0.47, 1], [6.61, -0.63, -0.26, 1, 13.23, -0.34, -0.11, -1], [11.78, 0.16, -2.27, -1, 4.15, 0.41, -1.9, 1], [9.01, -1.26, -0.64, 1, 14.83, -1.52, -0.57, -1], [4.22, 2.18, 2.19, 1, 3.99, 1.48, 2.44, -1], [10.48, 0.57, -2.5, 1, 14.74, 0.67, -2.73, -1], [7.63, 0.89, 3.07, -1, 13.71, 0.59, 2.96, 1], [19.3, -0.09, 0.31, 1, 9.04, -0.29, 0.42, -1], [9.55, 0.03, 2.44, 1, 7.64, 0.34, 2.58, -1], [9.78, 0.39, -0.2, 1, 8.38, 0.06, -0.26, -1], [8.38, -1.04, 0.27, -1, 6.66, -0.86, -0.09, 1], [11.49, -0.37, 0.56, 1, 6.12, -0.67, 0.78, -1], [11.75, -1.87, 1.8, -1, 9.8, -1.73, 1.54, 1], [12.13, -0.78, 2.93, 1, 18.14, -0.64, 2.79, -1], [17.04, -1.47, -1.95, 1, 7.64, -1.63, -2.17, -1], [10.16, 0.4, -1.37, 1, 13.16, 0.17, -1.48, -1], [11.23, 1.88, 1.67, -1, 6.67, 1.99, 1.33, 1], [5.63, 0.94, -2.76, -1, 4.68, 1.09, 2.94, 1], [14.37, 1.22, 0.56, -1, 13.42, 1.04, 0.42, 1], [2.04, 2.11, -2.52, -1, 1.78, 2.15, 1.79, 1], [5.84, 1.77, 1.76, -1, 4.15, 1.16, 1.69, 1], [10.96, 0.94, 1.63, -1, 10.2, 0.86, 1.92, 1], [9.24, 0.8, 2.47, -1, 32.08, 0.65, 2.57, 1], [10.52, 0.99, 1.85, -1, 8.9, 1.13, 1.55, 1], [9.38, -0.11, -1.6, -1, 10.2, -0.16, -1.28, 1], [7.08, -0.38, 2.48, 1, 13.64, -0.11, 2.31, -1], [8.46, -0.48, -1.92, 1, 9.31, -0.44, -1.57, -1], [8.07, -1.59, 2.89, -1, 9.43, -1.33, 3.13, 1], [4.86, -0.4, -1.04, 1, 7.26, 0.11, -1.08, -1], [12.95, -0.68, -1.5, -1, 6.07, -0.88, -1.78, 1], [13.61, -0.67, 2.84, 1, 10.55, -0.78, 2.59, -1], [7.15, 2.29, -0.82, 1, 7.67, 1.92, -0.71, -1], [8.97, 0.42, 2.1, 1, 7.62, 0.36, 1.72, -1], [6.17, -0.02, 0.96, -1, 4.1, -0.14, 0.34, 1], [3.41, 1.15, 1.12, 1, 11, 1.1, 0.61, -1], [26.04, -0.42, -1.4, 1, 8.21, -0.26, -1.29, -1], [6.77, 1.21, -1.88, 1, 6.2, 0.75, -1.78, -1], [12.66, -1.49, -0.02, 1, 10.62, -1.27, 0.11, -1], [3.66, 1.41, -1.99, 1, 4.44, 0.73, -1.68, -1], [21.13, 0.73, -2.02, 1, 9.02, 0.79, -1.8, -1], [1.9, -1.83, 0.53, -1, 5.71, -1.97, -0.42, 1], [8.62, -2.01, -0.33, -1, 3.49, -1.52, -0.59, 1], [5.95, 1.17, 0.35, -1, 8.11, 0.91, 0, 1], [6.21, -0.36, -2, -1, 8.06, -0.15, -2.38, 1], [7.45, 1.03, 1.85, 1, 8.61, 0.78, 1.56, -1], [3.7, 1.31, 0.23, 1, 6.79, 1.12, 0.8, -1], [10.86, -1.07, -0.3, 1, 7.21, -0.86, -0.02, -1], [11.91, -1.13, 1.81, 1, 7.94, -0.81, 1.8, -1], [12.25, 1.56, 2.99, -1, 16.89, 1.7, -3.13, 1], [9.39, -1.23, -0.44, -1, 11.26, -1.47, -0.26, 1], [7.06, -1.97, 0.26, 1, 4.62, -1.47, 0.05, -1], [14.27, -1.24, -2.79, 1, 11.76, -1.47, -2.82, -1], [7.93, -1.44, -2.1, 1, 15.19, -1.16, -2.05, -1], [16.69, -0.34, -2.87, -1, 11.57, -0.35, -3.08, 1], [6.6, 1.13, -3.06, 1, 6.61, 0.73, -2.84, -1], [2.63, -1.72, -0.51, -1, 8.17, -1.64, 0.15, 1], [5.36, -0.02, 1.71, 1, 5.83, 0.38, 2.08, -1], [6.97, 1.46, 1.63, 1, 6.81, 1.03, 1.57, -1], [10.13, 0.39, -2.8, 1, 8.56, 0.06, -2.85, -1], [7.09, -0.91, 0.43, 1, 11.1, -0.76, 0.74, -1], [6.81, -0.29, -2.33, 1, 8.41, 0.1, -2.41, -1], [3.99, 0.86, -0.51, -1, 4.33, 0.58, 0.2, 1], [3.33, 1.96, 2.87, -1, 4.09, 1.99, 2, 1], [7.37, -2.08, 1.67, 1, 6.2, -1.7, 1.91, -1], [15.25, 0, -0.72, 1, 9.89, 0.18, -0.55, -1], [3.23, 1.98, -2, 1, 3.3, 1.29, -1.33, -1], [7.12, 0.7, -0.77, 1, 31.12, 0.68, -0.98, -1], [33.24, 0.92, 2.66, -1, 8.53, 0.87, 2.48, 1], [11.64, 0.62, -2.16, 1, 5.34, 0.27, -2.32, -1], [8.2, 0.41, 2.54, 1, 5.21, 0.37, 2.06, -1], [8.75, 0.18, 3.08, -1, 9.06, 0.4, -2.94, 1], [3.22, -1.36, 2.47, -1, 2.46, -1.4, -2.68, 1], [11.55, -0.69, -1.92, 1, 11.94, -0.42, -1.96, -1], [10.45, -0.74, -3.1, -1, 14.69, -0.5, -3.14, 1], [5, -0.78, 0.35, 1, 4.96, -0.47, -0.19, -1], [7.5, 0.43, 0.62, 1, 7.74, 0.57, 0.24, -1], [6.14, -0.11, 0.68, 1, 6.63, -0.12, 1.17, -1], [8, 1.11, 3.1, 1, 4.13, 0.74, -2.79, -1], [8.99, 0.67, -3.11, -1, 13.46, 0.77, 2.92, 1], [6.31, 0.42, 0.87, 1, 6.73, 0.28, 0.41, -1], [13.75, -1.24, -1.13, 1, 10.13, -1, -1.24, -1], [6.37, -0.57, -0.31, 1, 11.2, -0.69, 0.04, -1], [9.28, 0.49, -2.12, 1, 6.12, 0.79, -2.4, -1], [6.37, 0.49, 0.85, 1, 6.13, 0.93, 1.08, -1], [5.15, 1.45, -1.68, -1, 8.72, 1.15, -1.36, 1], [5.31, -0.64, -1.83, 1, 4.22, -0.08, -2.15, -1], [9.31, -0.2, 2.1, 1, 14.79, -0.23, 2.36, -1], [8.28, -2.09, -0.44, -1, 6.32, -2.02, -0.84, 1], [8.11, 0.43, 0.51, 1, 7.09, 0.8, 0.34, -1], [17.35, -1.02, 1.06, 1, 9.31, -0.93, 1.29, -1], [3.06, 2.06, -0.34, 1, 3.24, 1.48, -1.14, -1], [12.73, -0.53, 2.17, 1, 8.24, -0.46, 1.88, -1], [1.91, -2.1, -0.45, 1, 2.85, -1.4, -1.65, -1], [6.71, 1.08, 0.52, -1, 7.07, 0.74, 0.82, 1], [3.65, -1.2, 2.89, -1, 4.86, -0.72, 2.31, 1], [14.18, 0.65, -1.36, 1, 10.27, 0.4, -1.3, -1], [7.69, -0.92, -1.35, 1, 7.65, -0.91, -1.76, -1], [9.36, -1.15, 1.9, 1, 10.23, -1.16, 1.58, -1], [12.55, 1.2, -1.13, -1, 9.09, 0.91, -1.13, 1], [13.49, -1.41, 0.79, -1, 11.63, -1.32, 0.56, 1], [6.22, -1.41, -0.35, -1, 5.44, -1.06, 0.06, 1], [7.15, -0.96, -0.14, 1, 7.31, -0.59, -0.35, -1], [11.9, -1.37, 2.58, 1, 8.02, -1.39, 2.9, -1], [7.75, 0.4, 0.64, 1, 3.49, 0.86, 0.26, -1], [7.58, -1.67, 1.41, -1, 6.35, -1.25, 1.29, 1], [10.27, -1.22, -0.28, 1, 9.67, -1.5, -0.39, -1], [8.77, 1.06, -2.77, 1, 9.22, 0.91, -2.47, -1], [1.82, -1.97, 0.56, -1, 1.55, -2.35, 2.75, 1], [22.19, -0.97, 1.53, 1, 10.02, -0.92, 1.74, -1], [8.98, 1.11, 2.28, -1, 16.62, 1.21, 2.52, 1], [9.24, 1.15, 0.33, -1, 12.86, 0.88, 0.26, 1], [20.43, 1.04, -1.7, -1, 6.35, 0.81, -1.58, 1], [10.29, 1.4, -2.63, 1, 21.97, 1.55, -2.5, -1], [1.72, -2.34, -2.13, -1, 7.42, -1.76, -1.49, 1], [25.68, 0.95, -0.64, 1, 11, 0.92, -0.46, -1]], &quot;psi2S&quot;: [[3.12, 2.24, -0.16, -1, 3.59, 2.25, 1, 1], [6.64, -0.36, -2.11, 1, 6.79, -0.85, -1.87, -1], [2.56, 2.4, -1.73, 1, 3.37, 2.23, -0.33, -1], [11.61, 0.22, -1.23, -1, 6.54, 0.52, -0.94, 1], [3.2, -2.03, 0.31, 1, 1.63, -2.32, 2.13, -1], [12.85, 0.71, 1.62, 1, 14.89, 0.93, 1.47, -1], [14.89, 0.3, 2.93, -1, 10.92, 0.06, 2.81, 1], [3.9, -1.48, -2.83, 1, 5.04, -0.67, -3.04, -1], [12.55, -2.25, -0.73, 1, 6.17, -2.09, -1.12, -1], [5.08, 0.86, 0.94, 1, 6.62, 0.72, 0.29, -1], [18.93, -1.07, -3.13, 1, 7.62, -0.83, 2.97, -1], [14.38, -1.91, -0.6, 1, 2.63, -1.99, -1.19, -1], [10.74, 0.06, 2.47, -1, 15.43, 0.17, 2.21, 1], [6.31, -0.03, -0.05, 1, 6.06, -0.02, 0.56, -1], [1.67, 2.22, 2.54, 1, 3.32, 1.21, -2.47, -1], [7.13, 1.75, -2.52, 1, 13.46, 1.64, -2.88, -1], [14.67, -0.55, 2.83, 1, 25.98, -0.6, 2.65, -1], [8.65, 1.08, 2.94, 1, 10.82, 0.72, 2.81, -1], [13.47, -0.52, -2.31, 1, 15.59, -0.74, -2.45, -1], [16.72, -1.72, -3.12, 1, 1.54, -1.7, 2.44, -1], [1.58, -2.35, 3.06, -1, 3.21, -1.24, -1.92, 1], [1.98, 2.19, 0.82, -1, 3.11, 1.66, -0.77, 1], [13.43, -1.06, 0.77, 1, 9.86, -1.03, 1.08, -1], [4.15, -2.06, 2.48, -1, 3.63, -1.13, 2.54, 1], [8.45, 1.68, 1.75, 1, 1.63, 2.39, 1.1, -1], [2.23, -1.94, 3.08, -1, 2.34, -1.8, 1.11, 1], [9.74, 1.51, -0.72, -1, 17, 1.28, -0.9, 1], [9.09, -0.74, 0.23, -1, 3.56, -0.8, 0.88, 1], [7.73, -1.36, -1.18, -1, 5.96, -1.13, -1.7, 1], [21.03, -0.85, -2.88, 1, 24.11, -0.81, -3.04, -1], [4.62, -2.31, -1.56, 1, 4.11, -1.84, -0.83, -1], [5.9, -1.01, -2.71, -1, 7.41, -0.53, -2.45, 1], [19.06, 1.31, 0.1, 1, 12.36, 1.56, 0.11, -1], [2.11, 2.37, -2.38, 1, 1.7, 2.31, 0.37, -1], [4.4, 0.2, -0.28, 1, 11.23, 0.59, -0.65, -1], [11.13, -1.05, -1.21, 1, 6.81, -1.09, -0.8, -1], [2.97, -2.09, -2.82, 1, 4, -1.62, -1.78, -1], [11.02, -0.44, 2.26, 1, 18.91, -0.5, 2.51, -1], [6.23, 1.13, 0.88, 1, 7.91, 0.73, 1.19, -1], [3.76, -0.99, 3.06, -1, 6.5, -0.6, -2.55, 1], [7.86, -1.56, 0.42, 1, 7.28, -1.54, 0.9, -1], [6.53, -1.52, -0.91, 1, 7.12, -1.26, -1.38, -1], [11.75, -0.02, -2.24, -1, 8.2, -0.18, -1.59, 1], [15.37, -1.64, 2.3, -1, 10.39, -1.49, 2.05, 1], [12.33, -0.78, -1.31, -1, 6.12, -0.46, -1.05, 1], [9.8, -0.87, 0.01, 1, 15.44, -0.97, -0.27, -1], [8.19, -0.18, -2.84, -1, 5.94, -0.7, -2.8, 1], [3.31, -2.21, 0.47, 1, 2.79, -1.58, -0.6, -1], [11.35, 1.65, -1.85, -1, 1.43, 2.4, -1.41, 1], [8.93, 1.16, 2.13, 1, 14.78, 1.12, 2.45, -1], [16.72, 0.66, -0.83, -1, 12.26, 0.87, -0.68, 1], [6.95, -1.04, -0.36, 1, 6.11, -0.97, 0.21, -1], [10.12, -0.92, 2.33, 1, 9.67, -0.72, 2.65, -1], [10.81, 0.48, 2.62, -1, 6.54, 0.66, 3, 1], [8.68, -0.47, -0.17, -1, 6.17, -0.83, 0.17, 1], [13.8, -1.48, 1.89, -1, 15.64, -1.73, 1.88, 1], [5.24, -0.79, 1.73, 1, 4.06, -0.02, 1.61, -1], [16.07, 0.18, -2.27, 1, 9.52, 0.32, -2.53, -1], [8.83, -0.38, 2.13, 1, 16.26, -0.37, 1.83, -1], [3.48, -2.35, -0.53, -1, 1.48, -2.27, 1.39, 1], [9.39, 1.73, -0.8, 1, 2.02, 2.13, -1.52, -1], [1.86, 2.29, 2.88, 1, 2.23, 2.21, 0.41, -1], [2.3, 2.36, 0.3, -1, 7.52, 1.5, 0.28, 1], [9.39, 0.18, 1.19, 1, 17.42, 0.22, 1.49, -1], [5.36, -1.17, -0.82, -1, 5.65, -1.06, -1.49, 1], [28.13, -0.06, -1.19, 1, 10.85, -0.2, -1.04, -1], [17.39, 0.34, -0.46, -1, 18.1, 0.15, -0.54, 1], [15.97, -1.6, 2.03, 1, 2.94, -1.98, 1.62, -1], [6.07, -0.4, -0.38, 1, 7.18, -0.74, -0.8, -1], [6.38, 0.87, 0.22, -1, 8.01, 0.79, -0.3, 1], [2.4, 1.54, 0.88, -1, 3.38, 1.71, 2.32, 1], [4.41, 1.89, 2.36, 1, 4.4, 1.48, 3.08, -1], [10.42, -1.48, 2.41, 1, 14.02, -1.18, 2.35, -1], [16.37, 1.5, -1.55, -1, 8.59, 1.33, -1.3, 1], [21.16, 0.97, -3.09, -1, 17.24, 0.81, 3.09, 1], [4.16, 1.66, 3.06, -1, 5.76, 1.31, -2.55, 1], [9.06, -0.88, 2.69, -1, 7.56, -0.44, 2.69, 1], [9.2, -0.03, 1.48, 1, 14.1, -0.06, 1.79, -1], [3.12, 1.2, 0.45, -1, 7.69, 0.83, -0.19, 1], [14.05, -0.64, -1.24, 1, 20.97, -0.64, -1.46, -1], [3.67, -2.23, 0.81, 1, 2.92, -1.46, -0.05, -1], [19.2, 1.53, 0.15, -1, 10.27, 1.27, 0.16, 1], [14.65, 0, 3.08, -1, 11.42, 0.29, 3.06, 1], [10.29, -0.16, 1.29, 1, 8.71, -0.35, 1.63, -1], [20.4, -1.36, -0.7, -1, 14.89, -1.37, -0.48, 1], [9.07, -0.44, -0.09, 1, 13.99, -0.73, 0.06, -1], [27.76, 0.5, -0.36, 1, 9.31, 0.57, -0.58, -1]], &quot;Ups&quot;: [[4.05, 1.16, -1.62, 1, 4.1, 2.14, 1.49, -1], [4.36, -0.47, 0.5, -1, 5.12, -0.3, -2.83, 1], [7.24, -1.91, -1.22, -1, 10.63, -1.25, -2.06, 1], [4.63, -0.64, 0.2, -1, 7.65, -0.52, 2.28, 1], [4.99, -1.09, -3.08, -1, 4.01, -0.4, 0.12, 1], [12.95, -1.01, 1.01, 1, 9.68, -0.41, 0.28, -1], [2.27, -2.02, -2.71, 1, 11.63, -1.05, -0.54, -1], [9.31, -1.86, -2.53, 1, 7.86, -1.13, 2.92, -1], [4.71, 1.56, 0.62, -1, 4.62, 1.47, -2.59, 1], [4.53, 1.07, 0.71, -1, 4.77, 0.17, -2.34, 1], [6.3, -0.45, -1.1, 1, 4.3, -0.41, 2.01, -1], [4.59, -1.4, 1.26, 1, 4.94, -1.08, -1.6, -1], [4.96, -0.38, 2.82, 1, 4.23, -0.74, -0.3, -1], [5.88, 0.3, -2.43, -1, 4.44, 0.5, 0.97, 1], [6.16, 2, -0.86, 1, 6.78, 1.65, 0.82, -1], [4.12, 0.4, 0.21, -1, 5.51, 0.52, -2.9, 1], [4.71, -1.21, -1.16, 1, 5.16, -1.55, 1.9, -1], [5.38, -1.08, -2.11, 1, 4.56, -0.93, 0.86, -1], [5.45, 1, 0.16, -1, 4.96, 0.99, -2.91, 1], [4.89, 0.37, -2.53, 1, 6.88, 0.52, 1.69, -1], [5, 0.16, -1.7, 1, 4.46, 0.02, 1.68, -1], [5.6, 0.21, 1.14, 1, 4.13, -0.58, -2.16, -1], [5.83, 0.38, -2.9, -1, 4.42, 0.68, -0.01, 1], [4.59, -1.38, -0.4, 1, 4.29, -0.3, 2.62, -1], [5.81, 1.15, -1.17, -1, 4.19, 1.84, 1.84, 1], [4.34, -1.43, 2.56, 1, 5.06, -0.77, -0.52, -1], [5.07, 0.1, 1.71, 1, 4.14, 0.03, -1.22, -1], [4.69, -1.62, 1.15, 1, 5.6, -1.49, -2.01, -1], [4.21, -0.07, -2.92, 1, 4.91, -0.36, 0.13, -1], [3.71, -1.49, 2.91, -1, 4.94, -0.12, 0.36, 1], [4.27, 0.53, 0.72, -1, 5.62, -0.25, -2.23, 1], [4.92, -1.78, -0.71, -1, 3.95, -1.05, 2.7, 1], [4.05, -1.45, -1.79, 1, 4.43, -0.59, 1.27, -1], [5.17, 0.99, -2.89, 1, 3.97, 1.2, 0.1, -1], [4.23, -1.34, 2.41, 1, 4.22, -0.41, -0.44, -1], [4.66, 0.86, -2.05, -1, 4.98, 0.47, 1.08, 1], [16.54, -0.41, -2.57, 1, 15.99, 0.04, -2.18, -1], [4.82, -1.45, -1.91, 1, 4.49, -0.97, 1.36, -1], [5.74, 0.66, 1.08, 1, 4.19, 0.19, -2.34, -1], [6.54, 1.39, 0.62, 1, 7.06, 0.17, 1.04, -1], [12.19, 0.35, -0.04, -1, 13.88, 0.2, 0.69, 1], [4.76, -1.53, 3.05, 1, 4.34, -0.94, -0.25, -1], [5.15, 1.93, 0.78, 1, 4.4, 1.76, -2.57, -1], [4.29, -1.28, -2.99, 1, 4.54, -0.65, 0.37, -1], [15.21, -1.6, 0, 1, 8.99, -0.96, -0.59, -1], [4.67, 1.42, 2.95, 1, 4.38, 2.02, -0, -1], [5.49, 0.54, 0.82, -1, 4.32, 0.09, -2.44, 1], [4.66, 0.59, 2.61, -1, 4.32, -0.41, -0.76, 1], [5.56, -0.03, 1.35, -1, 3.82, 0.53, -2.43, 1], [5.2, -0.23, -1.98, -1, 4.22, -0.41, 1.22, 1], [4.62, 1.37, 0.38, 1, 4.8, 0.7, -2.53, -1], [10.27, 1.33, 2.12, 1, 14.15, 0.53, 2.18, -1], [5.12, -1.59, 1.12, 1, 4.11, -0.77, -2.28, -1], [4.95, 0, 2.41, 1, 4.77, 0.19, -0.77, -1], [3.38, -1.04, -0.43, -1, 2.14, 1.65, -0.68, 1], [4.68, -0.96, -0.47, 1, 5.69, -0.76, 2.54, -1], [5.69, -0.08, 2.23, -1, 4.28, -0.75, -1.01, 1], [4.64, -2.03, 0.34, 1, 5.04, -1.58, -2.51, -1], [3.99, 2, -3.09, -1, 5.32, 1.6, 0.22, 1], [9.48, 1.65, -0.35, -1, 6.12, 0.44, -0.63, 1], [4.22, -1.23, -1.34, -1, 6.58, -1.27, 1.52, 1], [4.45, -0.23, -1.68, -1, 4.58, 0.07, 1.73, 1], [4.75, 0.95, 2.43, -1, 4.71, 0.14, -0.83, 1], [5.04, -0.04, -0.16, -1, 4.52, -0.21, -3.01, 1], [4, 1.34, 2.13, 1, 4.27, -0.05, -0.77, -1], [4.12, 0.17, -1.8, -1, 5.39, 0.19, 1.47, 1], [4.79, 1.21, -2.29, -1, 4.64, 1.11, 1.04, 1], [4.93, 0.52, -1.57, -1, 4.67, 0.37, 1.74, 1], [4.98, 1.22, -0.92, 1, 4.83, 0.91, 2.25, -1], [12.14, -0.58, 1.48, 1, 6.68, 0.41, 1.56, -1], [5.72, 0.25, -2.96, 1, 4.4, 0.24, 0.31, -1], [4.58, -0.47, -2.52, -1, 5.02, -0.29, 0.48, 1], [4.18, 1.05, -2.57, -1, 5.36, 0.31, 0.8, 1], [6.3, -1.38, 0.41, 1, 3.99, -1.51, -2.45, -1], [4.15, -1.18, -2.24, -1, 4.7, -0.71, 0.9, 1], [4.73, 1.52, 3.03, -1, 5.49, 0.99, -0.2, 1], [4.8, 0.21, 2.12, -1, 4.96, 0.82, -0.91, 1], [4.29, -0.89, -2.19, 1, 5.1, -0.54, 1.13, -1], [4.35, -1.9, 0.3, 1, 6.79, -0.93, 2.03, -1], [14.2, -0.11, 0.66, 1, 11.33, -0.66, 1.27, -1], [16.61, -1.28, -3.08, -1, 8.04, -1.41, -2.19, 1], [5.42, -1.31, -0.28, 1, 5.71, -0.57, 1.71, -1], [7.72, -1.44, -0.58, -1, 7.19, -0.6, 0.48, 1], [4.94, -1.56, -0.49, -1, 5.45, -1.6, 2.87, 1], [4.55, -1.13, 1.69, -1, 5.2, -0.5, -1.71, 1], [8.17, 1.14, -0.22, 1, 19.25, 0.48, 0.18, -1], [4.36, 1.06, -1.33, 1, 5.38, 0.31, 1.66, -1], [4.61, 0.74, -0.04, -1, 4.69, 0.39, 3.12, 1], [4.21, -1.18, -2.3, -1, 4.4, -0.28, 0.87, 1], [5.18, -0.36, -1.3, 1, 4.34, -0.47, 1.95, -1], [6.41, -0.31, 3.02, 1, 9.81, -0.84, -2.2, -1], [5.23, -0.12, 2.8, 1, 4.82, -0.1, -0.2, -1], [5.07, 0.68, 1.22, -1, 4.19, -0.3, -2.15, 1], [4.04, 1.32, -0.77, 1, 5.51, 1.15, 2.38, -1], [4.7, 1.47, 1.89, -1, 4.35, 0.86, -1.45, 1], [4.88, -0.04, 1.93, -1, 4.4, 0.36, -1.06, 1], [6.08, -1.75, 3.04, -1, 6.35, -1.55, -1.54, 1], [4.3, -1.59, 2.94, -1, 4.82, -1.45, 0.02, 1], [4.61, 0.22, -2.26, 1, 4.36, 0.5, 0.74, -1], [4.42, -1.12, 0.31, 1, 4.34, -0.37, -3.06, -1], [5.14, -2.12, 2.86, 1, 4.45, -1.97, -0.35, -1], [4.36, -1.98, -1.91, -1, 4.76, -1.93, 1.53, 1], [8.78, 2.14, -1.37, -1, 8.48, 1.44, -2.24, 1], [5.24, 0.51, -2.03, 1, 4.16, -0.02, 0.95, -1], [4.15, 1.55, -0.78, -1, 3.88, 0.37, 2.44, 1], [5.52, 0.46, 0.93, -1, 4.02, -0.15, -2.09, 1], [5.16, 1.25, 1.96, 1, 4.31, 0.37, -1.31, -1], [3.57, -1.48, 2.48, -1, 5.17, -0.7, -0.84, 1], [4.03, -0.65, -2.99, 1, 4.13, 0.82, 0.05, -1], [4.04, -1.2, -2.37, -1, 5.53, -1.06, 0.85, 1], [5.12, -1.87, 1.45, -1, 4.49, -0.98, -1.94, 1], [4.74, 0.29, -1.55, -1, 4.42, 0.1, 1.77, 1], [4.01, -1.87, -2.03, 1, 5.17, -1.72, 0.98, -1], [5.83, 1.66, -1.42, 1, 4.59, 1.59, 1.88, -1], [6.07, 1.3, 1.33, -1, 9.61, 0.52, 2.28, 1], [4.54, 0.4, -2.64, -1, 4.6, 0.91, 0.21, 1], [5.93, -0.1, 2.33, -1, 9.58, 0.81, -3, 1], [4.38, -2.11, -1.2, -1, 3.93, -1.22, 1.9, 1], [4.88, -1.31, 1.54, 1, 5.34, -1.11, -1.53, -1], [6.15, 1.4, -0.14, -1, 6.27, -0.12, -0.2, 1], [5.02, 0.55, -0.77, 1, 4.72, 0.13, 2.19, -1], [5.96, -1.33, 0.67, -1, 4.15, -0.91, -2.47, 1], [5.68, 0.43, 0.63, -1, 4.12, 0.29, -2.26, 1], [5.6, -1.98, 2.01, -1, 3.95, -1.63, -1.27, 1], [1.45, -1.38, 0.74, 1, 4.24, 1.58, 1.46, -1], [6.8, -0.12, 2.35, 1, 3.62, 0.04, -1.09, -1], [13.84, 1.34, 0.55, 1, 10.63, 0.58, 0.26, -1], [5.43, -0.44, -2.5, 1, 4.45, 0.23, 0.46, -1], [4.09, 1.44, -2, 1, 4.55, 0.57, 1.14, -1], [5.44, -1.18, -0.04, 1, 4.49, -0.92, -3.14, -1], [10.26, -1.73, 1.57, -1, 2.53, -2.25, -0.59, 1], [4.62, -0.36, -1.99, 1, 4.84, -0.29, 1.29, -1], [5.34, -1.55, -1.4, 1, 4.06, -0.56, 1.72, -1], [6.82, 1.05, -1.66, -1, 4.01, 0.95, 1.73, 1], [4.92, -1.71, -2.21, -1, 5.36, -1.35, 1.16, 1], [5.6, 0.13, 2.53, -1, 5.75, -0.54, -2.03, 1], [6, -2.33, 2.76, 1, 6.87, -1.15, -2.81, -1], [40.63, 1.85, -0.2, 1, 13.24, 1.45, -0.12, -1], [7.77, -0.58, 1, -1, 8.73, -0.92, -0.14, 1], [12.9, -1.08, -2.95, -1, 13.35, -0.52, -2.43, 1], [8.01, 1.98, 0.89, -1, 15.45, 1.84, 1.75, 1], [4.19, 1.47, -0.14, -1, 5.51, 1.12, -3.12, 1], [4.36, 0.99, -0.11, 1, 6.53, 0.86, -2.49, -1], [4.88, 0.9, 2.96, -1, 4.62, 0.61, 0.09, 1], [4.5, -0.46, -1.22, 1, 4.55, 0.18, 1.85, -1], [4.7, -2.37, 0.92, -1, 4.16, -1.39, -2.44, 1], [4.71, 1.04, -1.94, 1, 4.24, 0.35, 1.47, -1], [4.8, 2.31, 1.33, 1, 4.68, 2, -1.59, -1], [4.32, -0.11, -2.51, -1, 6.23, -0.18, 0.83, 1], [5.53, 0.37, -0.8, -1, 4.04, 0.16, 2.09, 1], [5.03, -1.48, -1.87, 1, 5.47, -1.53, 1.53, -1], [8.37, -0.11, 1.85, -1, 10.61, -0.19, 2.84, 1], [5, 0.98, 2.46, 1, 4.12, 0.97, -0.77, -1], [4.78, 0.42, 1.93, 1, 4.76, -0.32, -1.35, -1], [4.37, -0.99, -2.63, -1, 6.38, -1.11, 0.61, 1], [3.12, 1.84, 1, 1, 5.42, 0.63, -2.89, -1], [5.67, -0.05, -1.35, 1, 4.47, 0.38, 1.7, -1], [4.66, -1.76, -2.17, -1, 5.28, -1.54, 0.84, 1], [4.55, 1.55, -1.58, 1, 4.91, 1.37, 1.44, -1], [4.66, 0.98, 2.81, -1, 4.02, 0.12, -0.24, 1], [11.35, -1.35, 3.05, -1, 3.28, -1.84, 1.19, 1], [4.23, -1.79, 0.43, -1, 5.88, -1.27, -2.62, 1], [4.94, -1.94, -0.83, 1, 4.24, -1.34, 2.37, -1], [4.37, -2.05, -2, -1, 4.13, -0.84, 1.01, 1], [5.48, -0.16, 2.98, -1, 4.09, -0.59, -0.22, 1], [6.72, 0.23, -0.22, -1, 7.99, 0.86, -1.52, 1], [4.88, -0.41, -2.59, -1, 4.11, 0.74, 0.74, 1], [4.69, 1.47, 3.05, 1, 4.36, 0.76, 0.18, -1], [4.63, -1.14, -0.03, -1, 4.53, -1.32, -3.13, 1], [6.1, -0.97, 1.62, -1, 7.45, -0.06, 0.45, 1], [4.21, 1.54, 0.87, 1, 5.08, 1.12, -2.23, -1], [4.29, 0.91, -0.05, -1, 5.87, 0.32, -3.03, 1], [7.09, 0.44, -0.99, 1, 9.02, -0.69, -1.34, -1], [4.26, -1.51, 0.02, -1, 4.95, -0.9, -2.96, 1], [4.7, 1, -0.64, 1, 8.26, 1.34, 2.24, -1], [4.33, -1.29, 3.13, -1, 4.93, -0.49, -0.08, 1], [5.5, 0.43, -0.3, -1, 4.08, 0.65, 2.76, 1], [6.4, -0.85, 2.58, -1, 8.73, -0.92, -2.22, 1], [4.94, -0.63, -0.06, -1, 3.92, 0.58, 2.16, 1], [4.72, 0.9, 2.57, -1, 4.8, 0.7, -0.58, 1], [3.05, 1.85, 2.96, 1, 4.6, -0.1, -1.91, -1], [4.63, 0.95, -0.43, -1, 4.51, 0.56, 2.86, 1], [4.39, 1.36, -1.54, -1, 4.6, 0.82, 1.36, 1], [3.68, -1.14, 1.21, 1, 6.31, -1.09, -1.79, -1], [5.27, -1.75, 0.14, 1, 4.24, -1.24, -2.92, -1], [5.2, 0.14, -1.34, 1, 4.1, 0.8, 1.66, -1], [5.28, 0.75, -1.3, -1, 4.19, 0.74, 2.1, 1], [5.75, -1.47, 2.65, -1, 7.72, -0.46, 1.5, 1], [4.8, 0.34, -1.6, 1, 5.05, 0.63, 1.42, -1], [6.17, -0.93, 2.95, 1, 3.72, -0.17, -0.45, -1], [4.66, 0.5, 2.69, -1, 4.78, 0.07, -0.55, 1], [11.43, -0.21, 0.61, 1, 17.94, -0.85, 0.73, -1], [4.88, 0.9, 1.29, -1, 4.44, 0.54, -1.84, 1], [4.53, 0.32, -0.81, -1, 4.52, -0.66, 2.21, 1], [4.53, 1.29, -2.03, 1, 4.68, 0.77, 1.35, -1], [4.73, 1.11, -1.75, -1, 4.06, 0.49, 1.29, 1], [10.6, -0.73, 0.1, 1, 6.02, 0.36, 0.04, -1], [7.65, 1.5, 1.11, 1, 5.16, 1.12, -0.66, -1], [4.31, 1.33, 0.66, -1, 4.83, 1.57, -2.39, 1], [5.29, -1.42, -2.16, -1, 4.44, -0.8, 0.81, 1], [4.38, -0.63, -2.96, -1, 7.1, -0.35, -0.58, 1], [2.89, -1.72, 2.21, -1, 5.14, -0.43, -0.89, 1], [4.32, -0.83, -0.21, -1, 5.09, -1.79, 2.7, 1], [5.43, -0.84, 1.67, 1, 4.62, -0.86, -1.49, -1], [3.52, 1.06, 0.35, 1, 1.1, -2.21, 0.88, -1], [4.07, 1.53, 2.39, -1, 5.31, 0.7, -0.93, 1], [4.95, 0.56, -1.95, -1, 5.01, 0.53, 1.74, 1], [3.99, 2.04, -1.28, 1, 3.83, 0.56, 1.86, -1], [4.7, 1.13, -2.22, 1, 8.99, -0.21, -2.17, -1], [4.25, -0.9, 0.15, -1, 5.77, -0.87, -2.83, 1], [9.07, 0.26, -2.61, 1, 7.92, -0.32, 2.59, -1], [9.23, 0.5, 1.9, -1, 0.71, -2.16, -1.17, 1], [4.77, 1.31, 1.94, 1, 4.3, 0.91, -0.97, -1], [7.6, 0.07, 1.38, 1, 6.34, -0.52, 2.82, -1], [4.49, -1.32, 2.06, -1, 5.03, -1.2, -1.26, 1], [4.74, -1.54, -0.89, 1, 4.37, -0.97, 2.02, -1], [17.32, 1.42, 2.82, -1, 8.6, 1.77, -2.76, 1], [5.12, -0, -1.73, -1, 4.89, -0.06, 1.22, 1], [5.65, -1.25, 1.28, 1, 4.23, -0.78, -1.84, -1], [5.04, -1.89, 2.74, -1, 4.55, -1.09, -0.22, 1]], &quot;low&quot;: [[6.83, 0.2, -1.45, 1, 7.14, 0.32, -1.51, -1], [46.62, 0.11, -0.27, 1, 16.5, 0.12, -0.29, -1], [6.44, 0.53, 0.26, -1, 6.91, 0.38, 0.22, 1], [9.54, 0.47, -2.62, 1, 6.11, 0.46, -2.49, -1], [5.26, 1.89, -2.8, -1, 5.51, 1.78, -2.83, 1], [32.16, 0.3, -1.39, -1, 15.89, 0.32, -1.36, 1], [4.53, -1.63, 1.32, -1, 20.31, -1.57, 1.37, 1], [8.17, -0.97, -1.01, -1, 3.82, -1.07, -1.09, 1], [3.93, 0.35, -3.06, -1, 9.66, 0.36, 3.09, 1], [12.61, -0.36, -1.36, 1, 13.31, -0.29, -1.33, -1], [9.79, 0.47, -2.74, 1, 15.6, 0.54, -2.68, -1], [3.44, 1.16, -0.57, 1, 3.19, 1.36, -0.79, -1], [6.64, -0.62, 0.05, 1, 26.78, -0.66, 0.08, -1], [2.23, -2, -0.33, 1, 2.83, -2.24, -0.42, -1], [7.02, 1.3, -2.96, -1, 10.62, 1.24, -3.05, 1], [10.18, 1.06, 2.16, 1, 6.7, 1.1, 2.05, -1], [11.78, 0.99, 2.73, -1, 9.17, 1.05, 2.81, 1], [19.26, -1.39, 1.86, 1, 10.11, -1.38, 1.89, -1], [6.12, 1.31, -0.26, 1, 10.08, 1.27, -0.38, -1], [13.99, -0.69, -1.89, 1, 4.25, -0.77, -1.96, -1], [15.94, -1.52, -0.09, -1, 5.18, -1.46, -0.02, 1], [6.99, -0.61, 2.39, -1, 12.58, -0.53, 2.41, 1], [5.78, -0.58, -1.16, -1, 21.25, -0.58, -1.07, 1], [6.62, -1.22, 1.45, 1, 4.69, -1.19, 1.55, -1], [8.35, -0.93, -1.23, 1, 9.21, -0.92, -1.12, -1], [2.9, 1.99, -2.06, -1, 1.92, 2, -1.69, 1], [3.66, 1.45, 0.01, -1, 4.11, 1.3, 0.15, 1], [10.46, 0.1, 0.27, 1, 26.03, 0.16, 0.32, -1], [11.36, 1.04, -2.03, -1, 14.54, 1, -2.08, 1], [8.55, -0.11, 1.18, 1, 6.15, -0.11, 1.29, -1], [9.31, -0.96, 3.1, -1, 10.18, -0.89, 3.14, 1], [2.11, 2.22, -1.67, 1, 5.32, 2.19, -1.49, -1], [9.04, -0.11, 0.52, 1, 23.56, -0.12, 0.57, -1], [19.13, 1.18, 1.36, 1, 16.44, 1.15, 1.36, -1], [10.98, -0.62, -2.13, 1, 7.68, -0.61, -2.02, -1], [10.61, -0.45, 0.01, 1, 10.66, -0.35, 0.04, -1], [4.17, 1.59, 1.51, 1, 6.84, 1.46, 1.41, -1], [9.99, 1.44, 1.74, -1, 14.38, 1.47, 1.7, 1], [11.28, 1.02, 2, 1, 6.85, 0.93, 2.03, -1], [7.79, 1.62, -2.02, -1, 3.72, 1.49, -1.96, 1], [6.26, -1.03, 1.58, -1, 6.31, -1.12, 1.61, 1], [4.53, -1.97, 3.12, -1, 8.95, -2.08, 3.04, 1], [3.6, -1.89, -1.04, 1, 4.13, -1.72, -1.15, -1], [7.8, 1.82, -0.91, -1, 0.99, 1.87, -0.75, 1], [12.56, -0.08, -3.14, -1, 16.84, -0.05, -3.1, 1], [12.69, 1.03, -2.13, 1, 8.71, 1.06, -2.02, -1], [13.62, 0.4, 0.2, 1, 8.14, 0.36, 0.16, -1], [11.56, 0.61, -0.55, 1, 9.48, 0.54, -0.62, -1], [3.26, -1.49, 1.64, 1, 2.85, -1.31, 1.9, -1], [13.2, -0.56, 0.1, 1, 6.66, -0.49, 0.03, -1], [9.13, -0.66, -1.28, -1, 7.14, -0.75, -1.27, 1], [8.69, -0.14, 0.67, -1, 3.71, -0.32, 0.65, 1], [10.71, 0.84, -2.2, 1, 42.45, 0.83, -2.23, -1], [9.14, 0.79, -1.72, 1, 13.2, 0.8, -1.63, -1], [8.23, -0.44, 0.07, 1, 23.42, -0.43, 0.15, -1], [7.13, -1.35, 0.37, 1, 13.59, -1.48, 0.4, -1], [6.16, 0.6, 0.19, 1, 6.89, 0.51, 0.22, -1], [9.89, 0.31, 2.78, -1, 19.7, 0.3, 2.82, 1], [4.22, -1.15, 1.88, 1, 19.64, -1.1, 1.94, -1], [7.85, 0.76, 0.76, 1, 7.64, 0.81, 0.6, -1], [9.89, -1.35, 2.69, 1, 4.47, -1.47, 2.73, -1], [8.09, -1.05, -0.39, 1, 7.9, -0.97, -0.35, -1], [7.08, 1.05, 2.76, -1, 6.64, 0.92, 2.72, 1], [2.53, 2.29, -0.77, 1, 6.38, 2.37, -0.68, -1], [2.41, 1.49, -1.41, -1, 2.71, 1.37, -1.12, 1], [11.56, -1.03, 2.59, 1, 26.86, -1.05, 2.6, -1], [10.66, -0.71, -3.07, 1, 6.76, -0.68, -3.12, -1], [10.59, 0.28, -1.51, -1, 19.04, 0.25, -1.5, 1], [4.19, 0.89, 1.14, 1, 5.04, 0.85, 1.29, -1], [1.94, -2.29, 1.42, 1, 2.14, -2.26, 1.18, -1], [7.38, 1.49, 1.21, -1, 6.35, 1.49, 1.14, 1], [1.85, -2.34, 0.07, 1, 2.26, -2.15, 0.18, -1], [9.58, -1.41, -1.89, -1, 13.85, -1.47, -1.91, 1], [23.76, 0.98, -1.05, 1, 8.31, 1.04, -1.04, -1], [7.64, 0.69, -1.96, -1, 3.67, 0.67, -1.82, 1], [3.25, 2.02, 0.3, -1, 3.1, 1.7, 0.31, 1], [34.6, 1.63, -1.5, 1, 15.27, 1.66, -1.54, -1], [8.41, -1.03, -2.61, -1, 7.48, -0.91, -2.7, 1], [8.31, 0.82, 1.54, 1, 11.86, 0.84, 1.6, -1], [6.03, -1.16, -1.8, 1, 6.41, -1.26, -1.65, -1], [8.52, 0.07, -2.13, 1, 8.4, 0.09, -1.99, -1], [6.61, -0.75, 1.17, -1, 5.36, -0.9, 1.14, 1], [2.92, 1.41, 1.05, -1, 5.69, 1.2, 1.08, 1], [2.62, -1.82, -1.7, 1, 4.22, -2.06, -1.5, -1], [6.07, 0.76, -1.94, 1, 6.4, 0.65, -1.82, -1], [7.41, 0.07, 0.71, 1, 12.6, 0.1, 0.67, -1], [8.46, -0.24, -0.75, 1, 7.14, -0.1, -0.8, -1], [14.1, -0.41, -0.8, -1, 9.54, -0.4, -0.88, 1], [6.32, 1, -2.93, -1, 6.61, 0.88, -2.93, 1], [14.62, 0.28, 0.18, 1, 10.44, 0.25, 0.11, -1], [12.02, 1.14, 1.9, 1, 16.93, 1.2, 1.89, -1], [10.98, -1.15, -2.71, -1, 8.6, -1.13, -2.81, 1], [9.28, -0.34, 2.38, 1, 10.03, -0.3, 2.45, -1], [6.7, 0.8, 1.86, 1, 12.39, 0.73, 1.86, -1], [13.56, -1, -1.5, 1, 6.28, -0.92, -1.6, -1], [6.26, 0.49, 1.2, -1, 7.48, 0.58, 1.23, 1], [2.63, -1.36, 1.65, 1, 3.36, -1.5, 1.29, -1], [3.03, -1.37, 0.91, 1, 4.02, -1.38, 1.15, -1], [12.65, 0.18, -2.5, 1, 14.97, 0.09, -2.5, -1], [5.78, 0.12, -2.52, 1, 6.78, 0.08, -2.42, -1], [6.86, -0.29, -0.24, 1, 31.62, -0.3, -0.29, -1], [9.21, 1.24, -0.86, 1, 3.49, 1.09, -1.01, -1], [1.97, 2.33, 2.48, 1, 3.34, 2, 2.48, -1], [11.42, -0.07, -0.08, 1, 7.11, -0.01, -0.08, -1], [24.5, 1.12, -1.48, -1, 11.31, 1.1, -1.41, 1], [7.85, -1.52, 1.43, 1, 3.59, -1.44, 1.58, -1], [8.02, -0.37, 3.06, -1, 6.51, -0.32, 2.96, 1], [17.2, -0.22, -2.42, 1, 5.36, -0.18, -2.35, -1], [23.67, 1.17, 1.47, 1, 11.75, 1.14, 1.52, -1], [16.97, -0.29, -1.72, -1, 10.36, -0.28, -1.65, 1], [8.9, -0.34, -1.38, 1, 13.36, -0.41, -1.32, -1], [2.31, 1.84, -0.13, 1, 1.78, 2.06, -0.24, -1], [7.97, 1.3, 2.17, 1, 11.89, 1.23, 2.09, -1], [6.14, -1.39, 2.86, 1, 6.14, -1.33, 2.81, -1], [11.41, -1.08, 0.38, 1, 4.75, -1.12, 0.44, -1], [7.49, 0.79, 0.62, 1, 6.66, 0.84, 0.8, -1], [9.74, 1.4, 2.41, -1, 67.78, 1.4, 2.46, 1], [6.87, -1.55, -0.31, 1, 7.02, -1.4, -0.41, -1], [8.49, 1.2, 0.44, -1, 14.96, 1.14, 0.44, 1], [6.69, -0.56, 0.12, 1, 4.71, -0.47, 0.12, -1], [1.4, -2.21, 1.22, 1, 1.18, -2.33, 0.23, -1], [6.62, -1.06, 1.73, -1, 6.02, -0.91, 1.62, 1], [9, 1.06, -0.76, 1, 10.38, 1.09, -0.69, -1], [3.22, -1.37, -2.82, 1, 8.08, -1.2, -2.79, -1], [6.59, 1.14, 0.62, 1, 6.54, 1.05, 0.56, -1], [3.53, -1.73, 1.84, 1, 4.28, -1.55, 2.09, -1], [8.2, 0.23, 0.47, 1, 7.17, 0.27, 0.52, -1], [12.24, -0.66, 1.01, 1, 6.88, -0.62, 1.1, -1], [14.01, -1.17, -2.04, 1, 9.08, -1.13, -2.04, -1], [8.31, 0.73, -0.34, 1, 6.76, 0.84, -0.32, -1], [7.39, -1.28, 0.47, -1, 11.39, -1.35, 0.57, 1], [14.77, 0.76, 1.19, 1, 8.93, 0.8, 1.28, -1], [16.03, -0.5, 2.87, -1, 6.08, -0.44, 2.91, 1], [7.47, 0.24, -1.32, 1, 7.65, 0.35, -1.27, -1], [13.78, 0.42, 0.99, 1, 12.77, 0.44, 1.02, -1], [8.19, -0.05, -1.95, 1, 13.98, -0.13, -1.92, -1], [8.99, 0.54, 2.73, -1, 11.64, 0.48, 2.66, 1], [7.26, -0.79, 1.16, 1, 6.13, -0.64, 1.21, -1], [12.7, -1.24, -1.3, 1, 14, -1.19, -1.33, -1], [11.59, -1.35, -1.91, 1, 6.72, -1.37, -1.98, -1], [15.84, -1.04, -0.02, -1, 9.5, -1.13, -0.08, 1], [3.82, 1.94, -1.47, -1, 3.79, 2.2, -1.6, 1], [16.08, 0.39, -1.32, 1, 12.09, 0.44, -1.35, -1], [8.34, -0.44, 2.09, 1, 16.33, -0.48, 2.11, -1], [5.52, -1.46, 1.66, -1, 4.98, -1.5, 1.46, 1], [23.22, -1.34, 2.78, 1, 8.45, -1.37, 2.73, -1], [16, -0.23, -2.42, 1, 7.86, -0.25, -2.51, -1], [11.08, 0.93, 0.76, 1, 10.83, 0.94, 0.7, -1], [2.23, 1.96, -0.76, 1, 2.15, 1.73, -0.39, -1], [7.99, 0.48, 2.18, 1, 19.09, 0.44, 2.11, -1], [10.65, -1.12, -1.93, 1, 6.21, -1.12, -1.81, -1], [4.19, -2.03, -1.37, 1, 3.55, -2.05, -1.24, -1], [6.72, -0.37, 0.1, 1, 7.42, -0.37, 0.16, -1], [6.9, 0.21, -3.04, -1, 6.65, 0.19, 3.09, 1], [19.52, -0.06, 3.13, -1, 18.9, -0.05, 3.08, 1], [32.78, -0.68, 2.12, 1, 12.65, -0.68, 2.17, -1], [5.55, 0.8, -0.21, -1, 24.49, 0.81, -0.15, 1], [8.96, 1.63, -1.69, -1, 13.88, 1.65, -1.6, 1], [1.92, 2.09, -1.77, 1, 1.64, 1.98, -1.22, -1], [4.2, -1.17, 2.21, -1, 10.99, -1.04, 2.21, 1], [32.43, -0.32, 1.97, 1, 13.88, -0.33, 2.02, -1], [5.28, -0.45, -1.6, -1, 4.44, -0.33, -1.43, 1], [10.48, 0.47, 1.74, 1, 6.84, 0.55, 1.75, -1], [2.25, 2.22, -0.45, -1, 1.71, 2.08, 0.17, 1], [5.59, -0.08, 2.4, 1, 7.92, -0.06, 2.55, -1], [13.04, 1.43, 2.07, 1, 8.34, 1.41, 2.01, -1], [6.94, 0.61, 0.66, 1, 9.1, 0.71, 0.63, -1], [6.81, -1.16, -0.91, -1, 7.81, -1.11, -0.79, 1], [5.41, -0.02, -2.92, -1, 4.24, 0.05, -2.78, 1], [10.02, 1.29, -1.17, 1, 7.42, 1.35, -1.08, -1], [12.58, 0.5, -1.02, 1, 14.9, 0.52, -1.05, -1], [7.21, 0.8, 1.29, -1, 6.22, 0.85, 1.19, 1], [8.84, -0.5, -1.18, 1, 7.93, -0.5, -1.06, -1], [16.96, -0.25, 0.29, 1, 13.15, -0.23, 0.35, -1], [19.38, 1.18, -2.33, 1, 12.98, 1.12, -2.37, -1], [6.51, -0.89, -0.84, -1, 10.02, -0.82, -0.98, 1], [3.39, 1.14, 1.36, 1, 3.08, 1.33, 1.69, -1], [6.41, 0.63, 1.05, 1, 6.2, 0.7, 1.13, -1], [9.11, 0.31, 3.1, -1, 8.23, 0.34, -3.1, 1], [7.25, 1.42, 0.29, 1, 7.12, 1.44, 0.45, -1], [6.42, -0.1, 0.84, 1, 6.76, 0.05, 0.77, -1], [7.24, 0.44, 2.52, 1, 10.35, 0.49, 2.51, -1], [1.41, -2.18, 0.97, 1, 0.92, -2.27, -0.13, -1], [8.57, -2.02, 1, -1, 4.86, -2, 1.13, 1], [10.34, -1.38, 0.21, 1, 9.63, -1.28, 0.2, -1], [9.84, -1.48, 3.08, 1, 8, -1.45, -3.07, -1], [7.56, 1.42, 0.76, -1, 9.32, 1.56, 0.76, 1], [63.68, -0.48, -1.82, -1, 19.12, -0.48, -1.8, 1], [4.79, -1.15, -2.63, 1, 6.42, -1.07, -2.81, -1], [6.57, 1.64, -1.47, 1, 13.36, 1.59, -1.39, -1], [22.66, 0.08, 0.43, -1, 3.95, 0.05, 0.35, 1], [15.69, -1.35, 2.47, 1, 9.95, -1.3, 2.41, -1], [4.04, -0.87, 2.72, -1, 3.53, -0.75, 2.98, 1], [7.97, 0.02, -0.36, 1, 8.29, 0.09, -0.29, -1], [22.43, 1.3, -1.4, -1, 12.99, 1.35, -1.42, 1], [6.03, 0.18, -0.42, -1, 6.75, 0.18, -0.52, 1], [7.92, -1.05, -2.97, -1, 15.87, -1.01, -2.96, 1], [4.21, 1.67, -1.54, -1, 3.33, 1.5, -1.45, 1], [9.57, -0.69, -3.09, -1, 7.46, -0.83, -3.13, 1], [13.06, 0.83, -2.64, -1, 16.86, 0.8, -2.68, 1], [6.4, -0.03, 0.91, 1, 7.09, 0.02, 0.77, -1], [1.6, -2.23, 2.21, 1, 1.41, -2.38, 1.76, -1], [15.08, -1.43, -2.94, -1, 10.24, -1.39, -3.01, 1], [5.47, -1.26, 0.54, 1, 22.01, -1.3, 0.48, -1], [11.88, -0.07, 0.68, -1, 8.43, -0.14, 0.66, 1], [2.24, -2.14, 3.08, -1, 2.02, -2.21, 2.86, 1], [13.66, -0.21, 0.89, 1, 8.93, -0.13, 0.93, -1], [6.22, -1.25, 2.81, -1, 18, -1.17, 2.77, 1], [5.21, -0.21, -0.62, -1, 3.57, -0.44, -0.67, 1], [7.93, -0.62, 1.71, 1, 23.87, -0.61, 1.63, -1], [8.71, 1.84, -0.68, -1, 6.55, 1.76, -0.75, 1], [7.98, -0.7, 2.08, 1, 14.05, -0.6, 2.14, -1], [6.51, 0.43, -0.17, 1, 5.85, 0.34, -0.22, -1], [3.19, -1.77, -2.02, 1, 11.63, -1.6, -2.08, -1], [8.15, -1.02, -0.96, 1, 13.34, -1.01, -0.89, -1], [89.93, -0.48, -3.08, 1, 5.95, -0.52, -3.09, -1], [6.15, 0.89, -0.4, 1, 7.48, 0.75, -0.44, -1], [2.96, 1.95, -1.2, -1, 6.64, 2.14, -1.12, 1], [2.98, -1.5, -2.99, -1, 2.48, -1.46, 3.13, 1], [18.13, -2.25, 0.15, -1, 4.34, -2.25, 0.27, 1]], &quot;bg&quot;: [[14.87, -0.12, -2.64, -1, 8.07, 0.45, 0.46, 1], [8.16, -1.41, 3.06, 1, 6, -1.11, -0.35, -1], [3.85, -1.39, 0.55, -1, 3.08, 1.86, -0.62, 1], [11.63, 1.06, 1.22, 1, 4.59, 0.08, 2.92, -1], [4.67, -1.33, 1.1, -1, 7.15, 1.14, -2.17, 1], [4.97, -0.86, 0.89, -1, 6.39, 0.28, -2.25, 1], [8.51, 0.43, -2.22, -1, 6.57, -0.68, 0.9, 1], [14.86, -0.7, -2.08, -1, 6.84, -0.24, 0.82, 1], [9.35, 1.07, -1.68, -1, 17.89, -0.65, -0.67, 1], [4.05, -1.9, -2.23, -1, 7.27, -0.43, 1.01, 1], [6.43, -0.38, -1.31, -1, 7.1, -0.78, 2.23, 1], [5.64, -1.74, -0.59, 1, 7.2, 1.4, 2.44, -1], [7.8, -1.88, -1.53, -1, 17.22, -1.35, 1.06, 1], [8.01, -1.18, 0.32, 1, 12.16, -0.56, -2.68, -1], [2.69, -1.98, 2.44, 1, 4.25, 1, -1.05, -1], [5.01, -0.79, -2.39, 1, 7.06, 1.4, 0.84, -1], [10.57, 1.76, -0.33, 1, 10.58, -0.04, 2.36, -1], [11.32, -1.23, 2.09, -1, 7.2, -0.39, -0.78, 1], [8.88, -1.58, 1.25, -1, 4.78, 0.41, -2.03, 1], [8.78, -1.2, 2.33, 1, 10.86, 1.54, -0.78, -1], [7.71, 0.94, 1.86, 1, 8.45, 0.46, -1.12, -1], [12.73, -1.1, -0.04, 1, 12.98, 1.92, 0.46, -1], [7.72, 2.13, 2.48, 1, 5.89, 0.55, -0.79, -1], [6.72, 0.85, -2.3, 1, 7.05, -0.84, 0.78, -1], [9.51, 1.93, 2.94, 1, 12.96, 0.51, -0.44, -1], [13.82, -0.79, 2.97, 1, 9.89, -0.95, -0, -1], [6.49, 1.16, -0.11, -1, 5.38, -0.84, -3.09, 1], [5.99, 1.67, -0.1, -1, 7.71, -0.07, 2.93, 1], [9.16, -0.75, -2.57, -1, 14.3, -0.24, 0.76, 1], [6.8, 1, -2.54, -1, 7.39, 0.81, 0.83, 1], [6.3, -1.08, 2.38, -1, 14.27, 0.31, -2.61, 1], [6.69, -1.22, -1.55, -1, 5.3, 0.2, 1.37, 1], [4, 1.3, -0.12, 1, 6.02, -0.29, -3.05, -1], [6.16, 1.08, -3.05, 1, 5.33, -0.63, 0.27, -1], [5.11, 0.45, 2.57, -1, 7.14, -0.69, -0.3, 1], [8.8, -0.14, -1.73, 1, 7.66, -0.27, 1.58, -1], [12.39, -1.15, -3.11, 1, 9.9, -0.24, -0.36, -1], [9.56, 1.45, -0.83, 1, 14.09, 1.08, 2.96, -1], [5.31, 1.2, 1.96, 1, 8.36, 1.31, -1.43, -1], [5.59, -2.1, -1.59, -1, 4.62, 1.34, 1.79, 1], [10.87, -1.68, 1.27, 1, 14.45, -0.7, -1.85, -1], [4.31, -1.26, -1.48, 1, 4.38, 0.97, 1.67, -1], [7.7, 0.7, 0.04, -1, 9.12, 0.63, -3.04, 1], [6.66, 2.2, 0.51, 1, 9, 1.59, -2.59, -1], [10.23, -0.48, 2.03, -1, 1.3, 2.26, 3.07, 1], [6.57, -1.34, 1.11, -1, 6.53, 0.71, -2.05, 1], [11.31, -0.26, -1.36, 1, 6.83, -0.74, 1, -1], [7.26, -1.94, -1.65, 1, 7.31, -1.53, 1.56, -1], [37.45, 1.43, 1.13, 1, 16.73, 0.33, -1.65, -1], [10.45, -1.29, 0.69, -1, 12.82, 0.42, -2.24, 1], [5.23, 2.09, 1.16, 1, 5.79, -0.6, -1.89, -1], [9.67, 1.73, -0.47, 1, 4.99, -0.49, -2.83, -1], [22.77, -1.58, -1.25, 1, 8.28, -1.14, 0.22, -1], [5.37, 1.68, 2.93, -1, 6.07, 0.04, 1.26, 1], [11.63, 1.85, -2.76, 1, 6.39, -0.29, 0.14, -1], [4.44, -2, -1.94, 1, 4.29, 1.26, 1, -1], [12.38, -1.71, -2.41, -1, 10.99, 0.95, -1.27, 1], [6.47, 1.46, 1.52, -1, 7.58, 0.2, -1.36, 1], [5.51, 0.86, -2.2, 1, 5.73, -0.47, 0.85, -1], [6.54, -1.27, 0.06, -1, 6.47, -0.66, 2.76, 1], [5.85, -1.96, -0.74, -1, 4.83, 0.95, 2.74, 1], [16.97, -1.51, -0.45, 1, 9.31, -0.22, 2.46, -1], [11.93, 1.02, 1.92, 1, 5.63, -0.47, -1.45, -1], [6.2, 0.96, 0.21, 1, 5.41, -0.1, -3, -1], [5.95, 1.24, -2.81, -1, 5.2, -0.11, 0.2, 1], [12.76, -1.36, -1.15, -1, 23.2, -1.14, 1.98, 1], [8.62, 1.04, -0.9, -1, 5.98, -0.68, 2.14, 1], [4.22, 1.89, 1.25, -1, 4.91, -0.64, -2.49, 1], [7.14, 1.93, -0.63, -1, 6.53, -0.19, 0.65, 1], [11.27, -1.07, 1.53, -1, 4.25, -0.76, -1.91, 1], [5.21, -1.94, 2.62, 1, 4.36, -0.17, -0.61, -1], [6.37, -1.7, -1.19, -1, 7.86, 1.08, 1.77, 1], [5.03, -1.68, 2.44, -1, 4.05, 0.18, -0.77, 1], [5.39, -2.09, -0.69, -1, 4.89, 0.5, 2.19, 1], [4.48, 2.17, 2.65, -1, 4.45, -0.87, -0.28, 1], [4.61, -1.29, -1.15, 1, 5.19, 0.4, 2.18, -1], [6.23, 1.41, 0.3, -1, 6.3, -0.29, -3.04, 1], [5.36, 1.62, 2.83, -1, 7.06, 0.23, -0.16, 1], [6.9, 2.15, 1, 1, 6.99, 0.89, -1.85, -1], [29.1, -1.89, -2.89, -1, 21.88, -2.04, -0.14, 1], [5.79, 0.46, -1.44, 1, 13.52, -0.47, 1.55, -1], [30.46, -1.31, 1.77, -1, 21.31, -1.09, 2.49, 1], [4.93, -2.32, -0.93, 1, 3.9, 2.01, 1.39, -1], [4.39, -1.18, 3.09, -1, 4.82, 1.46, -0.05, 1], [8.63, -0.26, -1.65, 1, 5.99, -0.37, 1.65, -1], [9.56, -1, 1.6, -1, 6.79, 0.55, -1.6, 1], [6.02, -0.4, -1.78, 1, 11.95, 0.2, 2.43, -1], [11.3, 1.12, -3.03, -1, 8.39, 0.81, 0.17, 1], [7.1, -1.45, -1.77, -1, 15.93, -0.22, 1.37, 1], [4.47, -1.52, -2.21, 1, 5.52, 1.06, 0.77, -1], [11.83, -0.35, -0.06, -1, 16.97, 0.52, -3, 1], [8.72, 1.12, -1.66, -1, 6.24, -0.64, 0.69, 1], [15.7, -0.93, 3.09, -1, 12.31, 1.45, -0.07, 1], [4.67, -1.49, -2.98, 1, 18.93, 0.6, 0.17, -1], [6.3, -1.46, -1.12, -1, 7.01, 0.49, 1.86, 1], [13.15, 1.13, 1.46, 1, 26.84, -0.15, 1.8, -1], [9.06, -1.95, -2.47, -1, 6.27, 0.27, 0.42, 1], [11.95, 2.18, -0.17, 1, 15.2, 0.51, -3.03, -1], [11.99, 1.62, 1.16, -1, 7.24, 1.48, -2.63, 1], [7.99, -1.21, 2.62, -1, 6.56, 0.74, -0.6, 1], [4.36, 1.82, 1.94, 1, 4.14, -0.25, -1.44, -1], [9.95, -1.71, -0.85, -1, 9.96, -0.51, 2.62, 1], [20.37, 1.08, 2.69, -1, 11.83, 0.57, 0.98, 1], [2.85, 1.72, 2.15, 1, 7.02, -0.87, -1.82, -1], [7.92, -0.94, -2.08, 1, 11.76, 0.71, 1.52, -1], [9.03, 1.36, 2.51, -1, 8.41, 0.2, -0.63, 1], [6.72, 1.97, 1.88, -1, 8.76, 0.88, -1.06, 1], [4.22, -1.57, 0.47, 1, 3.35, 2.03, 2.98, -1], [9.61, -0.93, 3.04, -1, 9.03, -0.76, -0.1, 1], [4.73, 1.46, -1.88, -1, 12.71, 0.5, 1.28, 1], [4.28, -1.36, 2.66, 1, 5.2, 1.18, -0.36, -1], [3.46, -2.34, -0.21, -1, 3.02, 1.84, 1.46, 1], [8.44, -2.19, -1.54, -1, 5.56, -1.59, 1.31, 1], [5.94, -1.49, -0.22, -1, 4.24, 1.27, -3.08, 1], [4.68, -2.28, -0.35, 1, 5.32, -0.59, 2.9, -1], [4, -1.11, 0.14, -1, 5.1, 1.15, 3.1, 1], [7.64, -0.3, -1.06, -1, 6.39, -0.69, 2.31, 1], [3.85, 1.95, -2.24, 1, 12.4, -0.99, -0.64, -1], [5.52, 1.65, 3.09, 1, 7.47, -0.72, 0.01, -1], [8.55, -0.36, -1.98, -1, 7.72, 0.78, 1.07, 1], [4.1, -1.63, -2.32, -1, 4.12, 1.48, 0.76, 1], [6.35, 1.71, -3.04, -1, 7.09, 0.51, 0.13, 1], [5.44, -1.48, 2.18, 1, 9.76, 1.23, -1.46, -1], [9.89, 2.05, 1.36, 1, 9.11, 1.07, -1.94, -1], [6.79, -1.41, 0.82, -1, 4.86, 0.1, -2.42, 1], [8.64, 1.14, 0.78, -1, 13.22, -0.62, -2.99, 1], [11.02, -1.85, 0.68, 1, 11.2, 0.67, -2.44, -1], [5.5, 1.54, 2.19, -1, 4.46, -0.27, -0.89, 1], [4.91, -1.47, -2.01, 1, 12.63, 1.42, 1.23, -1], [6.47, 1.13, 0.6, 1, 9.11, -0.01, -2.41, -1], [4.78, 1.35, 2.28, 1, 7.36, -0.61, -1.12, -1], [8.03, 1.1, 0.09, -1, 5.78, 0.37, 3.07, 1], [15.49, -1.98, 1.74, 1, 19.87, -0.11, -0.92, -1], [6.6, 1.88, 0.03, 1, 5.49, 0.93, 3.04, -1], [6.83, -1.35, -2.25, 1, 7.11, 1.27, 1.08, -1], [4.11, 1.96, -0.19, -1, 6.4, -0.02, 2.83, 1], [4.66, 1.19, 0.07, -1, 6.06, -0.45, -2.79, 1], [5.91, -1.91, -2.93, 1, 7.06, 0.15, 0.35, -1], [10.61, 1.24, -2.42, 1, 17.38, -0.68, -1.73, -1], [6.04, -0.48, -2.27, 1, 7.72, -0.45, 1.48, -1], [5.05, -1.95, 1.16, -1, 5.91, -0.67, -2.01, 1], [5.37, 1.81, 0.63, -1, 8.58, 0.77, -2.64, 1], [4.02, 2, 1.23, 1, 5.62, 0.01, -1.83, -1], [10.61, 1.7, 1.12, 1, 10.11, 1.03, -1.7, -1], [13.06, -1.05, -0.39, -1, 8.94, -0.36, -2.98, 1], [7.2, -1.45, 0.11, 1, 5.83, -0.1, -2.86, -1], [5.88, 0.75, -2.45, -1, 6.16, -0.21, 0.76, 1], [5.63, -1.22, -2.71, -1, 5.2, 0.62, 0.31, 1], [4.57, -1.71, -2.28, -1, 5.92, 0.65, 1.01, 1], [9.99, 0.23, 1.77, -1, 18.6, 0.83, -1.21, 1], [6.88, -0.94, -0.65, -1, 7.32, -0.84, 2.41, 1], [7.35, 0.62, 2.82, -1, 9.1, 0.07, -0.44, 1], [6.95, 0.31, -2.31, -1, 5.1, -0.65, 1, 1], [8.33, -1.49, 1.7, -1, 9.29, -0.37, 2.72, 1], [5.01, -1.25, 1.36, 1, 7.51, 0.58, -1.81, -1], [21.86, -0.62, 1.25, -1, 8.28, -0.82, -2.02, 1], [9.91, -0.08, -2.2, 1, 7.25, -0.45, 0.74, -1], [6.56, -1.8, 2.83, -1, 8.09, 0.15, -0.39, 1], [7.86, 1.21, -2.13, -1, 8.02, 0.68, 0.7, 1], [7.16, -1.96, -2.35, 1, 8.37, -1.36, 1.02, -1], [7.61, -1.84, 0.93, 1, 7.69, -0.07, -2.04, -1], [17.3, -1.15, 1.39, -1, 14.73, 0.86, -2.42, 1], [10.88, -1.44, -0.46, -1, 10.68, 1.72, 2.72, 1], [20.36, 0.57, -2.87, 1, 37.33, -0.18, 0.21, -1], [6.3, -1.14, -1.43, -1, 6.57, 0.8, 1.79, 1], [11.4, -0.39, -2.89, -1, 7.39, -0.54, 0.11, 1], [4.25, -0.84, -0.42, -1, 10.14, -1.11, 2.96, 1], [5.89, -1.39, 1.39, 1, 5.93, 1.41, -1.7, -1], [21.95, 0.01, -0.98, 1, 16.15, 0.84, 2.07, -1], [9.36, -0.86, -1.96, -1, 6.22, -0.79, 1.25, 1], [7.5, 1.67, -2.45, -1, 7.69, 0.35, 0.67, 1], [16.37, 1.27, -2.32, 1, 9.33, 0.63, 1.04, -1], [6.63, 0.65, 1.59, 1, 7.55, -0.05, -1.97, -1], [4.51, -1.11, -1.02, 1, 5.59, 1.87, 1.84, -1], [5.1, 2.09, -1.98, 1, 4.96, 0.45, 1.27, -1], [6.32, -1.56, 0.82, 1, 6.36, 0.72, -2.46, -1], [6.27, -1.58, 1.94, -1, 7.04, 0.42, -0.99, 1], [3.4, -2.21, -2.93, -1, 2.84, 2.13, -2.65, 1], [20.95, 1.35, -0.72, 1, 10.37, 0.79, 2.37, -1], [22, -1.08, 2.41, -1, 15.85, -1.1, -1.45, 1], [7.64, 0.94, -2.99, -1, 8.14, 0.93, 0.29, 1], [9.62, -1.02, -0.1, -1, 9.98, -0.62, 2.87, 1], [6.21, -1.22, -0.84, 1, 6.24, 0.08, 2.4, -1], [17.01, 1.1, -1.14, -1, 11.11, 0.57, 2.12, 1], [6.46, -1.23, -0.19, -1, 7.83, 0.1, 2.76, 1], [6.12, -0.45, 0.34, -1, 6.6, 0.42, 2.68, 1], [4.59, -2.04, -1.25, 1, 7.67, 0.56, 1.74, -1], [7.2, 0.02, -2.22, -1, 10.2, 0.86, 0.92, 1], [5.92, 2.07, -0.54, 1, 5.24, 0.54, 2.63, -1], [28.41, -0.59, -0.04, 1, 2.25, 1.84, 2.59, -1], [7.64, 1.08, -0.16, -1, 7.01, 0.38, 2.88, 1], [5.95, 0.71, 0.03, 1, 6.32, -0.84, -3.13, -1], [6.65, -0.2, -1.26, 1, 8.09, 0.01, 1.83, -1], [10, 1.24, 0.52, -1, 9.22, -0.4, -2.12, 1], [14.82, 1.4, -0.71, 1, 9.27, -0.66, 2.57, -1], [4.88, -1.27, -2.53, -1, 5.7, 0.53, 0.32, 1], [11.34, 1.26, 0.64, -1, 12.71, 1.55, -2.6, 1], [6.82, -0.13, 2.41, 1, 9.2, -0.81, -0.78, -1], [9.36, 1.59, 0.69, 1, 10.75, 1.02, -2.21, -1], [21.17, 1.27, 1.03, 1, 16.82, 1, -0.46, -1], [6.49, -0.97, 1.91, -1, 8.35, 0.42, -1.09, 1], [6.29, -1.65, 0.23, -1, 7.25, -0.56, -2.95, 1], [10.69, -2.2, -1.32, -1, 16.84, -0.43, 1.85, 1], [12.9, -1.53, -2.91, -1, 11.64, 0.58, 0.39, 1], [11.44, -1.92, 1.26, -1, 9.64, -0.21, -1.62, 1], [10.09, -0.96, -2.16, -1, 14.86, -1.16, 0.97, 1], [10.33, -1.34, -0.96, -1, 18.07, -0.09, 2.07, 1], [10.73, 1.07, 2.7, 1, 7.42, 0.47, -0.6, -1], [17.22, -1.2, 0.74, 1, 12.48, 0.58, -1.83, -1], [9.06, 0.32, 1.99, 1, 7.88, 0.78, -1.14, -1], [5.58, -1.71, 0.51, -1, 6.59, 1.3, -2.81, 1], [11.44, -1.13, 0.83, -1, 4.86, 0.84, -2.41, 1], [10.9, 1.89, -2.27, 1, 4.78, 0.33, 1.03, -1], [3.39, -1.94, 2.53, 1, 3.74, 1.53, -1.16, -1], [8.63, 0.48, 0.06, -1, 14.5, 0.34, 2.33, 1], [9.49, -0.51, -0.53, -1, 6.33, -2.18, -2.47, 1], [7.46, -1.47, 2.02, 1, 4.53, -0.35, -1.09, -1], [8.69, 1.88, 1.05, 1, 7.12, 0.58, -2.34, -1], [6.13, 0.82, -2.32, 1, 12.43, -0.19, 2.32, -1], [5.18, -2.24, 0.57, -1, 5.98, 0.72, 1.5, 1], [14.51, 1.77, 2.2, -1, 8.3, -0.54, -0.74, 1], [6.5, -1.02, -3.07, 1, 6.05, 1.41, 0.29, -1], [11.11, -1.44, -0.45, 1, 5.19, 1.91, 2.89, -1], [11.26, 1.57, 1.03, -1, 6.74, 0.92, -2.54, 1], [4.54, 1.56, -0.09, 1, 5.74, -0.19, 2.85, -1], [8.02, -0.07, 0.46, -1, 6.34, -0.59, -2.67, 1], [14.71, -1.55, -1.37, -1, 15.15, 0.31, 1.84, 1], [12.89, 1.63, -1.21, -1, 8.04, 0.86, 1.38, 1], [7.14, 1.3, 1.35, 1, 5.22, -0.4, -1.59, -1], [14.22, 0.7, -0.47, 1, 1.21, -1.97, -0.75, -1], [6.18, -1.59, 0.47, -1, 7.98, 0.84, -2.57, 1], [13.23, -1.78, 2.08, 1, 19.16, -0.5, -2.41, -1], [4.74, -1.42, 1.27, 1, 5.01, 1.11, -1.76, -1], [8.14, 1.02, -1.7, 1, 6.37, -0.24, 1.62, -1], [4.51, 0.44, 2.15, -1, 3.93, -2.03, 2.87, 1], [9.05, -0.42, -3.12, -1, 7.55, -0.9, 0.01, 1], [5.01, 1.93, -0.81, 1, 4.38, -0.32, 2.59, -1], [8.41, -1.1, 1.7, -1, 6.93, 0.92, -1.2, 1], [9.88, 1.78, 0.39, -1, 10.59, 0.76, -2.5, 1], [9.09, -1.66, -2.7, -1, 6.57, 0.74, 0.67, 1], [36.01, -1.22, 3.03, 1, 30.88, 0.81, 0.31, -1], [7.75, -1.43, -1.46, 1, 8.33, -0.33, 1.6, -1], [11.22, 1.03, -2.51, 1, 23.31, 0.73, 0.74, -1], [3.33, 2.05, 2.76, -1, 3.66, -0.86, -1.5, 1], [13.12, 1.26, -1.21, 1, 11.11, 0.77, -0.16, -1], [2.18, 1.86, -2.79, 1, 1.72, -1.99, 0.54, -1], [8.05, -0.96, -1.22, -1, 7.61, 1.99, -2.89, 1], [10.16, 0.24, -2.53, 1, 5.04, -0.82, 0.41, -1], [6.47, -0.03, -2.5, 1, 8.03, 0.78, 0.91, -1], [44.47, -1.48, -0.82, -1, 9.82, -0.86, 2.28, 1], [8.94, -0.73, -1.37, -1, 9, -0.14, 1.49, 1], [5.81, -1.66, -1.73, 1, 7.4, -0.05, 1.47, -1], [4.75, -0.99, -0.23, 1, 6.89, 0.34, 2.74, -1], [7.31, -1.75, 1.92, 1, 5.2, 0.03, -1.5, -1], [9.34, 1.76, -1.76, 1, 17.87, 0.35, 1.61, -1], [4.75, 1.48, -2.59, -1, 6.77, -0.45, 0.8, 1], [5.26, 1.43, 1.97, -1, 7.22, -0.1, -1.1, 1], [11.35, -0.44, 0.35, -1, 5.55, -0.41, -2.88, 1], [8.97, 2.3, 1.85, 1, 14.17, 0.58, -1.21, -1], [12.31, -1.02, 2.75, 1, 0.9, 2.37, 2.89, -1], [9.13, 1.15, -0.92, 1, 8.12, -0.41, 1.29, -1], [4.83, -1.25, -0.14, 1, 7.42, 0.52, 2.2, -1], [8.83, 0.01, -3.06, -1, 8.33, -0.68, 0.34, 1], [4.6, 2.07, 1.69, 1, 10.98, -0.75, -2.63, -1], [5.84, -1.52, 2.22, -1, 7.64, -0.53, -0.96, 1], [10.61, 1.59, -0.12, -1, 11.66, 0.05, -1.18, 1], [6.69, -1.1, 2.49, -1, 11.74, 0.22, -0.41, 1], [18.33, -2.04, -1.48, -1, 14.32, -0.91, 1.36, 1], [8.26, 1.92, 1.1, 1, 6.13, 1.04, -2.11, -1], [6.48, -0.99, 2.96, -1, 5.62, 0.62, -0.12, 1], [10.17, -0.67, -2.69, -1, 13.87, 0.31, 1.26, 1], [6.99, -0.51, -2, -1, 6.82, -0.42, 1.06, 1], [8.03, 0.27, -1.45, -1, 13.67, 0.22, 1.91, 1], [11.95, 1.35, -2.47, 1, 13.71, 0.06, -2.42, -1], [5.6, -2.32, 1.03, -1, 2.75, 2.39, 2.37, 1], [5.47, -1.17, 3.06, 1, 4.77, 1.32, 0.15, -1], [9.88, 1.47, 3.06, -1, 6.78, 0.39, -2.04, 1], [4.83, -0.45, 2.6, 1, 6.08, 0.93, -0.52, -1], [6.59, 1.05, -0.61, 1, 6.44, 0.73, 2.24, -1], [9.89, -0.69, 1.54, 1, 7.3, -0.19, -1.7, -1]], &quot;h4l&quot;: [[47.409, -1.112, 0.253, 1, 1, 38.369, -0.293, -2.86, -1, 1, 46.532, -0.294, -2.63, 1, 0, 30.988, -1.594, -0.019, -1, 0], [101.832, -0.11, 0.539, 1, 1, 47.666, -0.467, -0.758, -1, 1, 81.277, -1.335, -2.671, -1, 0, 48.007, -0.437, 2.39, 1, 0], [21.698, 0.365, 1.055, -1, 1, 11.657, -1.072, -1.743, 1, 1, 21.801, -1.049, -1.746, 1, 0, 12.348, 0.378, 1.068, -1, 0], [11.53, -0.6, -0.535, -1, 1, 9.197, -0.788, 2.1, 1, 1, 56.482, 0.127, -2.617, -1, 0, 13.972, 0.399, 0.218, 1, 0], [49.169, 0.794, 0.784, -1, 1, 44.236, 0.425, -2.922, 1, 1, 33.653, 0.075, -1.046, -1, 0, 20.322, 2.347, 2.304, 1, 0], [46.979, 0.439, -2.676, 1, 1, 44.345, 1.129, 1.061, -1, 1, 28.93, -0.257, -2.119, -1, 0, 20.781, 2.229, 0.278, 1, 0], [24.772, -0.419, 3.059, -1, 1, 18.306, 1.121, 0.696, 1, 1, 17.897, 1.19, -2.753, -1, 0, 13.278, 1.611, -1.502, 1, 0], [77.981, -0.369, -2.22, 1, 1, 37.757, -1.002, -0.381, -1, 1, 55.781, -0.879, 0.873, 1, 0, 51.92, 0.166, 2.285, -1, 0], [17.525, -0.017, -2.154, 1, 1, 8.174, -0.477, -0.917, -1, 1, 50.667, 1.137, 1.817, -1, 0, 42.55, 1.386, -0.849, 1, 0], [20.429, 1.848, 2.797, -1, 1, 14.112, 0.57, -0.036, 1, 1, 22.935, 0.582, -0.055, 1, 0, 12.492, 2.323, 3.133, -1, 0], [70.06, -0.229, -0.293, 1, 1, 23.789, -1.109, -3.121, -1, 1, 54.547, -0.34, 3.009, -1, 0, 37.737, 0.114, -0.541, 1, 0], [51.8, -0.119, 0.94, -1, 1, 34.988, -0.88, -2.769, 1, 1, 68.897, -1.818, -2.435, -1, 0, 42.789, -2.034, 0.814, 1, 0], [31.343, -1.187, -2.152, 1, 1, 28.72, -0.317, 0.902, -1, 1, 48.372, -0.293, 0.432, 1, 0, 45.809, -0.445, -2.566, -1, 0], [101.777, -1.056, 1.748, -1, 1, 26.777, 0.554, 2.146, 1, 1, 35.752, -1.654, -1.437, -1, 0, 33.32, 0.121, 0.545, 1, 0], [45.908, 1.644, 2.635, 1, 1, 28.324, -0.026, -2.022, -1, 1, 46.547, -0.366, -0.35, 1, 0, 19.392, 1.004, 1.583, -1, 0], [86.768, 2.421, -0.838, 1, 1, 14.288, 0.304, -1.377, -1, 1, 114.076, 0.481, 2.069, 1, 0, 14.662, 1.562, -1.621, -1, 0], [29.457, 0.084, 2.302, -1, 1, 8.126, 0.973, 2.388, 1, 1, 51.43, 0.448, 2.467, -1, 0, 36.445, -0.017, -2.079, 1, 0], [70.049, -0.344, -3.136, 1, 1, 57.807, -1.271, -2.038, -1, 1, 71.752, -1.024, 1.364, 1, 0, 53.338, -0.178, 0.135, -1, 0], [73.122, 0.483, 1.216, 1, 1, 14.261, -1.326, -0.976, -1, 1, 66.963, 0.736, -2.777, -1, 0, 33.255, 0.16, -0.399, 1, 0], [100.789, 1.409, -1.853, 1, 1, 37.907, 2.239, 2.739, -1, 1, 24.056, 1.367, -0.849, 1, 0, 16.013, 1.447, -3.118, -1, 0], [94.996, 1.252, 2.208, -1, 1, 73.129, 0.208, 2.24, 1, 1, 104.914, -1.318, -0.338, -1, 0, 62.247, -1.311, -1.509, 1, 0], [68.045, 2.181, -0.901, -1, 1, 23.936, 1.551, 2.487, 1, 1, 63.345, 0.415, 1.425, -1, 0, 35.705, 0.319, -2.616, 1, 0], [91.213, 0.854, -1.841, -1, 1, 23.743, 1.395, 2.482, 1, 1, 74.668, 0.816, 1.107, -1, 0, 17.041, -0.625, -1.966, 1, 0], [11.823, 0.034, -1.263, -1, 1, 9.22, -0.394, 0.321, 1, 1, 35.579, -0.453, 0.068, 1, 0, 34.312, -0.434, 2.815, -1, 0], [46.483, 1.924, 1.757, 1, 1, 12.627, -0.549, -0.01, -1, 1, 48.873, 1.104, -1.546, -1, 0, 16.988, -1.347, -0.694, 1, 0], [9.567, -0.728, 1.274, 1, 1, 8.954, 2.135, -3.052, -1, 1, 35.083, -1.291, 0.339, 1, 0, 33.406, -0.204, -2.66, -1, 0], [169.088, 0.407, 2.592, 1, 1, 55.782, 1.114, 3.112, -1, 1, 44.679, 2.285, -1.069, -1, 0, 19.638, 1.222, 0.018, 1, 0], [64.452, -1.31, 0.141, 1, 1, 32.678, -0.73, 2.676, -1, 1, 57.692, -2.314, -2.896, 1, 0, 23.023, -0.988, -0.482, -1, 0], [13.79, -0.745, -2.193, -1, 1, 9.963, 0.16, -3.077, 1, 1, 93.565, -1.871, -1.307, 1, 0, 23.174, -0.593, 0.36, -1, 0], [126.745, -0.171, 0.717, -1, 1, 15.715, -0.615, -2.755, 1, 1, 99.915, 1.63, -2.409, 1, 0, 20.109, -0.151, -1.977, -1, 0], [34.493, -1.195, -0.92, -1, 1, 12.902, 1.479, 3.03, 1, 1, 23.879, -1.341, 1.445, -1, 0, 17.273, -1.228, 2.26, 1, 0], [48.847, 0.062, 2.998, 1, 1, 42.328, 0.449, 0.035, -1, 1, 41.764, 0.386, 0.291, 1, 0, 40.076, 0.339, -2.502, -1, 0], [39.345, 0.278, -2.86, -1, 1, 13.666, -2.387, -1.654, 1, 1, 70.419, -0.666, 0.562, 1, 0, 9.674, 1.314, -2.713, -1, 0], [48.02, -0.197, 1.039, -1, 1, 41.416, 0.144, -2.414, 1, 1, 54.128, -0.119, -0.259, -1, 0, 23.948, -1.395, 2.66, 1, 0], [172.434, 0.397, -0.218, 1, 1, 84.33, -0.074, 0.477, -1, 1, 186.531, 0.959, -3.124, 1, 0, 57.728, 1.905, 3.054, -1, 0], [21.211, 0.021, -1.24, 1, 1, 10.345, -0.354, 2.416, -1, 1, 43.375, -0.852, 1.822, 1, 0, 23.862, -2.021, -1.21, -1, 0], [44.669, -1.448, 2.435, 1, 1, 41.35, -0.725, -0.722, -1, 1, 45.396, -0.817, -2.683, 1, 0, 45.343, -0.49, 0.432, -1, 0], [34.786, -1.106, -2.908, 1, 1, 18.701, 1.637, -0.155, -1, 1, 40.695, -0.119, 2.287, 1, 0, 36.857, 0.116, -1.549, -1, 0], [88.146, 0.501, 2.227, -1, 1, 35.225, -0.654, 1.062, 1, 1, 130.21, 0.765, -1.47, -1, 0, 18.287, -0.155, 0.577, 1, 0], [73.627, 0.504, 0.339, -1, 1, 28.053, 0.201, -2.696, 1, 1, 33.608, 2.221, 1.694, 1, 0, 16.905, -0.28, -1.605, -1, 0], [87.123, 1.436, 1.794, -1, 1, 25.136, 0.758, -0.67, 1, 1, 57.79, 1.509, -2.272, 1, 0, 42.528, 2.13, -0.111, -1, 0], [45.736, 0.981, 1.652, 1, 1, 45.07, 1.069, -1.848, -1, 1, 47.869, -0.254, -0.544, 1, 0, 33.169, 0.96, 2.442, -1, 0], [117.299, 1.287, 2.695, -1, 1, 29.937, -0.139, 2.873, 1, 1, 238.36, 0.919, 0.836, -1, 0, 52.03, 0.673, 0.04, 1, 0], [23.596, -0.538, -2.487, 1, 1, 9.652, -0.1, 2.884, -1, 1, 34.873, -1.25, 3.034, 1, 0, 22.848, -0.218, -0.709, -1, 0], [67.9, 2.222, -0.436, -1, 1, 38.08, 0.998, -1.765, 1, 1, 57.812, 0.34, 2.508, 1, 0, 49.866, 1.494, 1.205, -1, 0], [35.133, -2.262, -3.092, 1, 1, 23.692, -0.192, 0.161, -1, 1, 30.271, 0.473, -0.579, 1, 0, 16.442, -2.208, 2.754, -1, 0], [96.66, -0.503, 3.087, 1, 1, 29.595, -1.214, 1.392, -1, 1, 107.118, -0.344, -0.664, 1, 0, 27.232, -1.36, 0.778, -1, 0], [28.62, 0.057, -0.486, 1, 1, 11.173, -2.172, 1.613, -1, 1, 62.408, -1.449, 2.533, -1, 0, 27.238, -1.667, -0.837, 1, 0], [40.703, 1.632, 0.01, -1, 1, 36.256, 0.269, -2.318, 1, 1, 72.181, 0.901, -2.794, 1, 0, 30.098, 0.997, -0.03, -1, 0], [70.13, -0.894, 1.988, 1, 1, 24.372, -0.134, -2.07, -1, 1, 22.782, 0.326, -2.75, 1, 0, 13.204, -0.122, -2.03, -1, 0], [117.586, -0.228, 1.752, -1, 1, 18.426, 0.595, -0.346, 1, 1, 106.942, -0.498, -1.748, 1, 0, 25.763, 0.17, -0.041, -1, 0], [76.645, 0.031, -1.088, -1, 1, 27.239, -0.388, 1.453, 1, 1, 56.796, 1.476, 1.558, 1, 0, 22.96, -0.023, -1.96, -1, 0], [102.16, 0.671, -0.207, 1, 1, 42.742, -0.175, -1.421, -1, 1, 86.451, 1.107, 1.153, -1, 0, 22.235, 0.171, -1.876, 1, 0], [86.242, -0.617, 1.767, 1, 1, 21.431, 0.285, -2.201, -1, 1, 81.045, 0.557, -0.183, 1, 0, 20.249, -0.616, -2.73, -1, 0], [57.079, -0.817, -1.397, -1, 1, 40.58, -0.921, 1.984, 1, 1, 96.172, 1.045, -2.799, 1, 0, 38.113, 1.057, 1.668, -1, 0], [61.14, -1.296, 1.643, -1, 1, 38.59, -1.638, -0.874, 1, 1, 56.059, -2.127, -2.29, 1, 0, 21.698, -0.097, 2.996, -1, 0], [36.424, -1.617, 1.993, 1, 1, 18.896, 0.63, -1.334, -1, 1, 26.598, 1.51, -1.245, -1, 0, 12.912, -1.475, 1.152, 1, 0], [59.656, -0.348, -1.26, 1, 1, 39.527, -0.379, 1.309, -1, 1, 59.629, -0.792, -2.967, 1, 0, 29.103, -1.762, 0.844, -1, 0], [78.734, 1.459, -1.288, 1, 1, 15.349, -0.269, -1.394, -1, 1, 127.407, -0.888, 2.022, 1, 0, 17.233, 0.206, 0.344, -1, 0], [48.962, -1.223, 0.569, 1, 1, 12.328, -1.444, 2.889, -1, 1, 25.287, -1.716, -2.233, -1, 0, 8.62, -1.539, 3.016, 1, 0], [49.548, -0.736, -0.587, -1, 1, 20.649, -0.501, 1.482, 1, 1, 30.905, -0.546, 1.424, -1, 0, 25.472, 0.181, 0.922, 1, 0], [61.192, 0.563, 2.124, -1, 1, 33.866, 0.345, -0.792, 1, 1, 14.924, -0.851, -0.474, -1, 0, 12.984, -1.501, -2.016, 1, 0], [19.073, -0.307, -2.826, 1, 1, 9.63, -2.261, 1.313, -1, 1, 37.742, -0.403, -1.421, 1, 0, 36.551, -0.338, 0.876, -1, 0], [60.448, 0.806, -2.499, 1, 1, 35.349, 1.412, 0.074, -1, 1, 42.231, 0.328, 0.913, -1, 0, 39.441, 1.187, -1.822, 1, 0], [65.319, 0.746, -1.428, 1, 1, 33.079, 0.536, 1.668, -1, 1, 55.637, 1.058, 2.54, 1, 0, 27.782, -0.115, -0.299, -1, 0], [38.252, 1.395, -2.193, 1, 1, 8.622, 0.309, -0.263, -1, 1, 59.007, -0.321, 1.292, 1, 0, 22.198, 1.115, -1.598, -1, 0], [53.13, -1.887, 2.086, 1, 1, 23.609, -0.056, 3.112, -1, 1, 67.104, -1.566, -0.038, -1, 0, 46.178, -2.347, -1.723, 1, 0], [45.094, 1.977, -2.913, 1, 1, 10.283, -9e-3, -2.073, -1, 1, 114.319, 0.613, -2.189, -1, 0, 54.811, 0.439, -2.157, 1, 0], [59.707, -1.313, -2.041, 1, 1, 34.448, -0.615, 0.655, -1, 1, 55.705, -0.093, 1.756, -1, 0, 27.329, -1.36, -0.727, 1, 0], [24.516, -0.405, 2.847, -1, 1, 18.236, 0.779, 1.72, 1, 1, 78.152, -0.371, 2.263, 1, 0, 13.613, 1.605, 0.548, -1, 0], [56.706, -1.545, 2.96, -1, 1, 27.375, 0.621, 2.175, 1, 1, 61.397, -1.52, -1.146, -1, 0, 49.081, -2.25, 0.533, 1, 0], [22.741, 0.575, 0.087, 1, 1, 13.26, 1.939, -0.141, -1, 1, 112.614, 1.822, 2.226, -1, 0, 24.013, 2.003, -2.06, 1, 0], [43.028, 1.731, -2.068, -1, 1, 40.021, 0.444, 2.179, 1, 1, 72.217, 0.362, -0.451, 1, 0, 32.506, 0.792, 1.997, -1, 0], [82.293, -0.717, 2.961, 1, 1, 30.693, -1.154, -1.299, -1, 1, 60.374, -1.637, 2.075, -1, 0, 30.462, -0.48, -2.454, 1, 0], [66.669, -0.943, -2.742, -1, 1, 15.327, -1.484, -1.441, 1, 1, 61.56, -0.754, 2.233, -1, 0, 51.856, -0.918, -2.678, 1, 0], [27.46, -1.754, 0.483, 1, 1, 10.938, 1.305, -1.38, -1, 1, 56.709, -1.975, -2.457, 1, 0, 40.387, -1.845, 1.04, -1, 0], [48.487, 0.762, 0.89, -1, 1, 31.04, -0.479, -2.369, 1, 1, 61.464, -1.405, -1.732, -1, 0, 24.921, -2.116, 1.331, 1, 0], [61.962, -1.766, 1.32, -1, 1, 41.227, -1.674, -1.093, 1, 1, 63.548, -0.734, 3.086, -1, 0, 36.721, -0.161, -0.911, 1, 0], [18.289, -1.696, -1.687, 1, 1, 12.37, 0.587, 0.615, -1, 1, 56.76, 0.532, 2.979, 1, 0, 24.022, 0.581, 0.615, -1, 0], [17.861, -2.04, -0.918, 1, 1, 16.445, -0.846, -0.157, -1, 1, 27.428, -2.341, 1.926, -1, 0, 19.776, -1.119, -1.678, 1, 0], [48.097, 1.952, -2.05, 1, 1, 44.118, 2.085, -1.723, -1, 1, 106.275, -0.76, 0.84, 1, 0, 21.981, -1.091, -3.031, -1, 0], [72.18, -2.089, 2.77, -1, 1, 31.051, -1.96, -0.857, 1, 1, 64.27, -2.232, -0.186, -1, 0, 43.205, -1.741, 2.6, 1, 0], [14.014, -1.418, -2.3, 1, 1, 9.185, -0.6, 0.667, -1, 1, 35.816, -0.604, 0.66, -1, 0, 24.777, -1.283, -2.334, 1, 0], [71.481, 1.553, 2.971, 1, 1, 50.301, 1.116, -1.656, -1, 1, 89.106, 0.068, 0.556, -1, 0, 33.844, 0.531, -1.232, 1, 0], [75.624, -0.988, -2.729, -1, 1, 35.743, -0.265, -1.802, 1, 1, 94.829, 0.466, 0.519, 1, 0, 61.416, 1.418, 1.079, -1, 0], [69.159, -0.499, 2.633, 1, 1, 30.889, 0.195, -1.5, -1, 1, 70.293, 0.165, -0.54, -1, 0, 33.579, -0.334, 1.71, 1, 0], [64.259, -0.799, 1.281, 1, 1, 35.376, 0.17, -2.977, -1, 1, 81.509, -0.027, -1.034, 1, 0, 8.127, 0.939, -2.865, -1, 0], [28.633, -0.18, -0.71, -1, 1, 14.168, -0.675, 0.172, 1, 1, 50.152, -0.263, -2.198, -1, 0, 37.033, -2e-3, 0.781, 1, 0], [63.155, -0.076, -2.999, -1, 1, 45.401, -0.876, 1.456, 1, 1, 72.191, -0.114, -0.02, -1, 0, 31.638, 0.658, -1.97, 1, 0], [77.835, -0.023, 0.325, 1, 1, 18.12, -1.368, -1.968, -1, 1, 55.338, -2.304, -2.763, -1, 0, 21.476, -0.059, -2.145, 1, 0], [54.705, 0.76, -2.792, -1, 1, 24.89, -0.612, 0.29, 1, 1, 41.256, 0.959, -1.491, -1, 0, 29.924, -0.584, 1.207, 1, 0], [47.881, -0.467, -1.415, -1, 1, 44.893, 0.464, 0.565, 1, 1, 54.671, -0.27, -2.919, -1, 0, 43.337, 0.573, 1.329, 1, 0], [95.776, -0.062, -1.139, -1, 1, 12.507, -1.9, 2.76, 1, 1, 86.314, 0.456, 2.145, 1, 0, 35.812, 0.062, 0.228, -1, 0], [32.89, -1.441, 2.914, -1, 1, 32.071, -0.568, -1.899, 1, 1, 47.683, -1.482, 0.392, -1, 0, 42.255, -0.787, -1.9, 1, 0], [36.666, 1.468, 1.725, -1, 1, 23.432, -1.021, 0.515, 1, 1, 71.791, 0.575, -2.405, -1, 0, 36.091, 0.54, 1.074, 1, 0], [134.222, 0.253, 0.907, -1, 1, 56.042, 0.931, 1.664, 1, 1, 243.606, -1.13, -1.908, -1, 0, 11.049, 0.481, -1.762, 1, 0], [122.405, -0.326, 2.582, -1, 1, 53.451, 0.317, -2.685, 1, 1, 91.317, 2.378, 0.154, 1, 0, 46.851, 1.861, -1.179, -1, 0], [66.332, -1.066, -2.498, 1, 1, 45.508, -0.613, 1.942, -1, 1, 74.19, 0.665, 0.246, -1, 0, 19.99, -0.998, -1.577, 1, 0], [44.37, 1.107, 2.456, 1, 1, 27.992, -0.516, -1.264, -1, 1, 63.354, -1.834, -1.008, 1, 0, 25.539, -0.983, 2.447, -1, 0], [133.45, 0.782, -1.854, 1, 1, 45.041, 0.229, -2.974, -1, 1, 91.886, -0.756, 1.583, -1, 0, 19.915, -1.073, -2.01, 1, 0], [76.435, -0.361, 1.189, -1, 1, 23.863, -0.806, -2.463, 1, 1, 26.889, -2.082, -1.902, -1, 0, 12.578, -2.348, -1.157, 1, 0], [37.436, -1.433, 2.994, 1, 1, 25.229, 0.427, -0.155, -1, 1, 33.056, 0.597, 0.189, -1, 0, 22.749, -1.516, -2.692, 1, 0], [51.461, -0.271, -2.819, -1, 1, 18.874, -2.266, -0.056, 1, 1, 55.591, 0.13, 0.052, 1, 0, 35.679, 0.672, -2.733, -1, 0], [72.797, -0.102, -1.101, 1, 1, 28.318, 0.278, 1.64, -1, 1, 43.359, 1.253, 2.311, -1, 0, 25.909, -0.695, 0.541, 1, 0], [49.848, 1.857, -1.704, 1, 1, 46.596, 1.75, 1.623, -1, 1, 175.055, 1.892, 1.729, -1, 0, 69.372, 1.96, 2.545, 1, 0], [42.201, -1.341, -2.059, 1, 1, 8.507, -0.41, -1.822, -1, 1, 57.886, -0.559, 0.714, 1, 0, 38.215, -1.336, -3.078, -1, 0], [70.537, 0.149, 1.898, 1, 1, 33.513, -0.033, -0.643, -1, 1, 67.785, 0.031, -2.244, 1, 0, 44.111, -0.439, -0.242, -1, 0], [81.186, 1.221, 0.263, 1, 1, 10.885, -0.882, -2.154, -1, 1, 71.666, 1.813, -2.763, -1, 0, 32.734, 0.108, -1.489, 1, 0], [84.171, 0.355, 1.618, -1, 1, 19.271, -0.563, -1.447, 1, 1, 50.288, -0.82, -0.304, -1, 0, 29.961, -2.126, 2.423, 1, 0], [43.616, 0.583, 0.566, 1, 1, 33.01, 1.841, 1.086, -1, 1, 62.004, -2.244, -1.338, 1, 0, 33.96, -2.188, 1.292, -1, 0], [53.374, -0.017, 2.048, -1, 1, 40.98, -0.638, -0.418, 1, 1, 57.798, -1.399, -2.929, 1, 0, 24.648, -0.01, -0.322, -1, 0], [78.781, 0.626, 2.244, -1, 1, 22.882, -0.198, -1.234, 1, 1, 50.032, 0.051, -0.915, 1, 0, 42.744, -0.929, 1.295, -1, 0], [14.036, 0.13, -0.649, -1, 1, 8.114, 2.237, 2.528, 1, 1, 47.014, 1.786, 2.021, -1, 0, 15.547, -0.475, -0.934, 1, 0], [87.362, -0.279, -2.399, 1, 1, 46.7, -1.31, -1.496, -1, 1, 80.12, 1.876, 1.085, -1, 0, 52.625, 0.581, 0.859, 1, 0], [43.166, -1.971, 2.551, 1, 1, 34.498, -0.756, -0.123, -1, 1, 35.575, -2.093, -1.385, -1, 0, 34.298, -0.422, 2.132, 1, 0], [35.756, -1.441, 2.64, -1, 1, 30.683, 0.308, -0.553, 1, 1, 48.346, 0.276, 0.194, 1, 0, 43.565, 0.368, -2.59, -1, 0], [81.345, -2.311, 1.394, -1, 1, 31.567, -0.699, 1.244, 1, 1, 73.967, 1.804, -1.71, 1, 0, 27.628, 0.026, -1.795, -1, 0], [46.28, -0.027, -2.954, 1, 1, 45.847, -0.021, 0.319, -1, 1, 23.947, 0.52, -2.179, 1, 1, 7.281, -0.282, 1.583, -1, 1], [59.008, 2.472, -2.99, -1, 1, 56.369, 1.427, -0.131, 1, 1, 40.398, 2.112, 0.965, 1, 1, 26.169, -0.447, -1.287, -1, 1], [45.147, -0.444, 1.771, -1, 1, 41.225, -1.094, -0.016, -1, 1, 39.767, 0.378, -1.586, 1, 1, 36.42, -0.078, 3.116, 1, 1], [32.074, 1.923, 2.213, 1, 1, 24.078, 0.461, -1.278, -1, 1, 9.651, -0.325, -1.325, 1, 1, 7.321, 1.102, 0.996, -1, 1], [43.328, -1.33, 0.27, 1, 1, 32.094, -0.594, 2.264, -1, 1, 9.442, -0.628, 2.395, 1, 1, 9.076, -1.741, -1.584, -1, 1], [52.679, 0.577, -2.844, -1, 1, 43.673, 0.171, -0.374, 1, 1, 26.453, 0.155, 1.58, 1, 1, 13.599, 0.793, 3.065, -1, 1], [113.417, 1.259, 1.654, -1, 1, 95.839, 0.206, -1.474, -1, 1, 41.008, 0.635, 2.914, 1, 1, 40.116, -0.732, -0.547, 1, 1], [67.087, 1.017, 1.916, 1, 1, 42.665, -1.156, -1.199, 1, 1, 17.384, -0.717, -0.878, -1, 1, 12.803, -0.285, 1.49, -1, 1], [22.236, -0.45, -2.529, 1, 1, 16.381, 1.583, 1.527, -1, 1, 15.649, 0.61, -0.717, -1, 1, 13.546, 1.206, -2.537, 1, 1], [52.968, 1.024, 1.813, 1, 1, 45.658, 1.76, -0.472, -1, 1, 44.555, 2.324, 2.779, 1, 1, 39.981, 1.59, -1.695, -1, 1], [24.782, -0.702, -0.329, -1, 1, 15.856, 1.259, -2.734, 1, 1, 14.24, 0.05, 0.623, 1, 1, 11.686, -0.889, 0.649, -1, 1], [50.07, -1.174, 0.434, 1, 1, 21.336, -1.611, -1.825, 1, 1, 12.835, -2.197, 2.653, -1, 1, 9.52, -2.004, -0.937, -1, 1], [72.608, -0.627, -2.941, 1, 1, 45.088, -0.051, 1.113, 1, 1, 37.684, -0.968, -0.828, -1, 1, 19.526, -2.219, -2.546, -1, 1], [79.209, -0.413, 1.811, -1, 1, 54.438, 0.257, -2.659, 1, 1, 46.351, 0.811, -0.386, -1, 1, 36.134, -0.314, -2.264, 1, 1], [58.559, 1.357, 1.709, 1, 1, 53.462, 0.654, 0.366, -1, 1, 40.77, 2.232, -0.308, -1, 1, 22.044, -0.8, -3.018, 1, 1], [50.236, 0.476, 0.705, 1, 1, 43.986, 0.685, -1.462, -1, 1, 43.718, 0.64, -2.92, -1, 1, 21.268, -1.151, 1.193, 1, 1], [78.375, 1.392, 0.43, 1, 1, 59.299, 0.525, -2.7, 1, 1, 29.982, 0.988, -1.779, -1, 1, 20.567, 1.135, 1.916, -1, 1], [81.62, 0.7, -0.564, 1, 1, 60.394, 1.071, -2.532, 1, 1, 42.005, 1.749, 1.676, -1, 1, 25.391, 1.571, 1.981, -1, 1], [111.31, -0.401, 1.362, 1, 1, 75.427, -0.93, -2.471, -1, 1, 35.746, 0.18, -0.89, 1, 1, 14.004, -0.276, -2.515, -1, 1], [189.421, -0.435, 0.951, -1, 1, 147.528, -1.077, -1.832, 1, 1, 60.849, -1.598, -2.645, -1, 1, 25.383, -0.661, -0.549, 1, 1], [85.168, 0.419, -0.102, -1, 1, 60.466, 0.482, 2.252, 1, 1, 34.892, 0.498, -2.114, 1, 1, 20.32, 2.202, -1.667, -1, 1], [46.205, 0.419, -1.063, -1, 1, 34.293, 0.266, 1.804, 1, 1, 31.268, -1.015, 0.962, -1, 1, 18.056, -0.816, 2.664, 1, 1], [78.846, -0.536, -0.915, 1, 1, 53.129, -0.675, -2.521, -1, 1, 48.48, -1.254, 1.399, 1, 1, 28.458, -9e-3, -1.498, -1, 1], [65.104, -1.594, 2.987, 1, 1, 40.056, -2.259, -0.614, 1, 1, 22.523, -0.529, 1.196, -1, 1, 8.958, -0.627, 1.228, -1, 1], [64.657, 0.784, -1.048, -1, 1, 62.782, 0.18, 2.934, -1, 1, 42.762, 0.747, -1.304, 1, 1, 25.309, 1.413, 1.569, 1, 1], [36.857, 1.219, -1.747, 1, 1, 28.739, 1.632, 2.073, -1, 1, 16.636, 1.278, -0.568, -1, 1, 8.809, 1.323, 1.43, 1, 1], [87.062, -1.209, -0.11, 1, 1, 71.1, -0.234, 2.206, -1, 1, 65.852, -1.532, -1.327, -1, 1, 57.814, -1.285, 3.006, 1, 1], [57.537, -0.554, 1.315, -1, 1, 50.085, -1.025, 1.641, -1, 1, 41.303, -1.679, -2.18, 1, 1, 26.692, -2.023, -1.266, 1, 1], [78.769, 0.925, 2.685, 1, 1, 57.842, 0.124, 0.678, 1, 1, 53.253, -0.516, -0.7, -1, 1, 43.811, -0.089, -2.402, -1, 1], [166.479, -0.062, 1.547, 1, 1, 152.247, 1.66, -1.649, -1, 1, 24.677, 1.923, -0.139, 1, 1, 11.125, -0.665, -2.269, -1, 1], [76.407, -1.533, -1.948, -1, 1, 64.455, -0.576, -1.417, -1, 1, 58.78, 0.405, -2.576, 1, 1, 12.887, 0.683, 0.471, 1, 1], [120.832, 1.345, -1.607, -1, 1, 98.408, 0.958, 1.992, -1, 1, 32.221, 2.381, 1.668, 1, 1, 8.892, 1.165, 1.997, 1, 1], [74.445, 0.403, -2.195, -1, 1, 45.658, 0.387, 0.283, 1, 1, 35.355, -0.156, 1.823, 1, 1, 17.378, 0.451, 0.758, -1, 1], [96.225, -0.09, -1.947, -1, 1, 37.972, -1.742, 0.647, -1, 1, 23.89, 0.586, 1.108, 1, 1, 23.648, 0.231, 0.604, 1, 1], [50.63, 1.8, -1.794, -1, 1, 47.736, 1.361, 2.522, 1, 1, 32.728, 0.199, -0.18, -1, 1, 11.552, -0.576, 1.841, 1, 1], [60.337, -0.59, 2.962, 1, 1, 45.447, -1.744, 2.366, -1, 1, 35.958, -0.994, -1.126, -1, 1, 35.901, -0.6, -0.592, 1, 1], [70.967, -0.27, -2.308, -1, 1, 50.068, -0.592, 2.609, 1, 1, 38.257, -1.41, 0.48, -1, 1, 33.436, -0.257, 1.764, 1, 1], [53.801, 0.992, -0.078, 1, 1, 42.751, -0.159, 3.13, -1, 1, 39.702, 0.641, -2.689, -1, 1, 29.881, 1.127, 0.848, 1, 1], [115.432, 0.224, 2.771, 1, 1, 107.204, 0.283, -2.662, -1, 1, 39.51, -1.529, 2.053, -1, 1, 18.445, 0.368, -0.539, 1, 1], [52.624, 1.89, 0.023, 1, 1, 38.35, 0.963, 0.087, -1, 1, 37.604, 1.487, -2.479, -1, 1, 33.894, -0.808, 1.985, 1, 1], [127.919, -0.635, 0.523, -1, 1, 55.035, -1.565, 3.092, 1, 1, 38.558, 0.102, 2.363, -1, 1, 17.43, -2.299, 0.35, 1, 1], [123.784, -1.291, -1.43, -1, 1, 118.07, -1.16, 2.357, -1, 1, 56.911, -1.044, -2.561, 1, 1, 22.189, 0.401, 2.757, 1, 1], [42.716, -0.435, -0.693, 1, 1, 36.093, -1.684, 2.728, -1, 1, 16.462, -1.767, -0.238, -1, 1, 11.62, -1.032, -2.858, 1, 1], [62.597, -1.298, -2.403, 1, 1, 35.618, -0.809, -0.12, -1, 1, 29.529, 1.307, 1.072, 1, 1, 15.624, 0.835, 2.293, -1, 1], [41.17, 0.344, -0.21, 1, 1, 23.449, -0.247, 2.822, -1, 1, 10.847, -0.121, 1.961, -1, 1, 9.895, -0.43, -2.563, 1, 1], [37.723, 1.115, 1.614, -1, 1, 36.596, 1.189, -1.415, 1, 1, 29.363, 0.722, -2.686, -1, 1, 28.055, 0.62, -2.205, 1, 1], [50.348, 1.853, -0.155, 1, 1, 34.047, 0.687, -3.042, -1, 1, 32.767, 0.244, 1.828, -1, 1, 20.192, 0.299, -0.916, 1, 1], [38.355, -0.423, -0.058, -1, 1, 32.405, 0.408, 2.852, 1, 1, 26.023, 1.558, -1.625, 1, 1, 23.769, 0.046, 2.204, -1, 1], [33.06, -0.419, -0.134, -1, 0, 20.028, 0.918, -2.873, 1, 0, 11.465, 0.972, -2.818, -1, 0, 11.421, 0.113, 1.677, 1, 0], [50.581, 0.307, 2.979, -1, 0, 26.287, -1.667, 0.948, -1, 0, 22.76, 2.049, -1.099, 1, 0, 13.274, 1.464, -1.394, 1, 0], [32.761, 2.306, -1.967, -1, 0, 23.887, 1.709, 1.276, 1, 0, 9.724, 1.32, 1.065, 1, 0, 8.655, 1.716, 2.781, -1, 0], [97.572, -0.505, 2.358, -1, 0, 87.574, -0.13, -0.193, -1, 0, 35.334, -0.727, -2.172, 1, 0, 8.878, -0.45, 1.224, 1, 0], [51.773, -0.317, -2.131, 1, 0, 36.741, 0.408, 0.539, -1, 0, 16.349, 0.684, 1.367, 1, 0, 5.22, 0.768, -0.475, -1, 0], [41.151, 0.747, 1.132, 1, 0, 24.689, 0.434, -2.346, -1, 0, 13.343, 0.703, -1.117, -1, 0, 9.225, 1.532, -1.999, 1, 0], [26.131, 0.531, 0.412, 1, 0, 23.1, 1.859, -2.115, 1, 0, 16.883, -2.341, 2.785, -1, 0, 5.591, 1.811, 2.725, -1, 0], [47.88, -1.216, -0.82, -1, 0, 23.193, 0.577, 2.508, -1, 0, 14.413, 1.157, 3.066, 1, 0, 7.361, -1.492, -2.698, 1, 0], [36.594, -0.755, 2.035, 1, 0, 17.312, 0.319, -0.863, -1, 0, 11.241, 0.242, -3.035, -1, 0, 11.141, 0.355, -0.869, 1, 0], [45.226, 2.031, -1.636, 1, 0, 28.213, 2.34, 0.635, -1, 0, 24.303, -0.146, 1.682, 1, 0, 20.416, -0.022, 2.488, -1, 0], [38.202, -0.013, -1.524, 1, 0, 17.329, -1.056, 2.175, 1, 0, 14.27, -1.021, 2.204, -1, 0, 13.084, -0.886, 1.334, -1, 0], [65.524, 0.232, 0.17, -1, 0, 64.105, 1.327, 2.825, 1, 0, 17.062, 2.207, -1.369, 1, 0, 12.248, -0.892, -1.394, -1, 0], [78.024, 1.441, 1.774, 1, 0, 59.239, -0.774, -1.212, 1, 0, 43.184, 0.121, 3.093, -1, 0, 42.599, 0.06, 1.411, -1, 0], [95.571, -1.988, -1.248, -1, 0, 77.221, 0.98, 2.091, 1, 0, 44.725, 1e-3, 0.998, -1, 0, 14.19, -0.347, 2.912, 1, 0], [59.789, -0.471, 1.711, -1, 0, 34.465, -0.246, -1.564, 1, 0, 5.652, -1.665, -0.769, -1, 0, 5.617, 1.354, -2.521, 1, 0], [44.678, -0.897, -0.608, -1, 0, 29.674, -0.373, 2.427, 1, 0, 13.917, -0.893, -0.608, 1, 0, 5.704, -1.14, 0.971, -1, 0], [69.504, -0.647, -0.722, 1, 0, 64.366, 0.012, 1.418, 1, 0, 53.568, -1.213, -2.218, -1, 0, 7.036, -2.025, 0.509, -1, 0], [27.689, 0.41, -0.422, -1, 0, 21.937, -1.398, 2.281, 1, 0, 9.845, 0.201, 1.862, -1, 0, 7.043, 0.809, -1.214, 1, 0], [56.337, -1.842, -0.144, 1, 0, 54.272, -0.848, 0.851, 1, 0, 50.059, -2.371, 0.497, -1, 0, 9.735, -2.206, -0.94, -1, 0], [73.452, 0.754, 2.42, -1, 0, 56.74, 1.859, -0.985, -1, 0, 27.098, 0.184, -1.021, 1, 0, 12.298, 0.027, 1.229, 1, 0], [101.844, -0.824, -1.37, -1, 0, 61.08, -2.284, 1.835, 1, 0, 36.456, -1.459, -0.188, -1, 0, 8.996, 1.486, -0.011, 1, 0], [37.317, -0.805, 2.639, 1, 0, 20.864, -1.48, -1.025, -1, 0, 12.546, 0.365, 0.065, -1, 0, 7.479, -0.145, -2.069, 1, 0], [41.692, 1.208, -1.979, 1, 0, 22.549, 1.328, 0.431, -1, 0, 20.817, 1.605, 1.146, 1, 0, 8.276, 0.959, 0.138, -1, 0], [22.817, -0.591, 0.456, 1, 0, 22.285, -0.788, -2.76, -1, 0, 15.978, -2.384, 2.703, 1, 0, 10.618, -0.662, 1.187, -1, 0], [90.519, 2.264, 2.326, 1, 0, 65.112, -0.215, -0.349, -1, 0, 43.695, -0.844, -2.15, 1, 0, 24.829, 1.766, -0.09, -1, 0], [42.075, 0.317, -0.064, 1, 0, 40.258, 1.968, 0.894, 1, 0, 37.888, 0.848, -2.462, -1, 0, 35.864, 1.566, -2.647, -1, 0], [63.7, -0.469, 2.9, 1, 0, 52.537, -1.061, -0.838, -1, 0, 38.309, -1.608, 1.735, 1, 0, 27.838, -1.338, -0.472, -1, 0], [54.6, -0.019, -1.401, 1, 0, 50.303, -0.538, 2.038, 1, 0, 25.718, -1.065, 1.844, -1, 0, 25.121, -2.253, 0.218, -1, 0], [51.222, 1.34, -2.316, 1, 0, 23.808, 1.253, -2.913, 1, 0, 22.866, 2.095, 1.895, -1, 0, 13.133, 1.815, -1.831, -1, 0], [63.001, 0.649, 2.387, -1, 0, 53.633, 1.645, -1.473, -1, 0, 33.595, 1.22, 1.088, 1, 0, 23.84, 0.586, -0.482, 1, 0], [90.865, -1.041, 1.348, -1, 0, 90.703, 0.416, -2.074, -1, 0, 27.71, -0.761, -2.588, 1, 0, 20.805, -1.166, -0.6, 1, 0], [38.206, -0.683, 2.109, 1, 0, 28.356, -0.675, -1.204, -1, 0, 15.543, -0.705, -1.22, 1, 0, 6.908, -1.617, 1.671, -1, 0], [60.817, 4e-3, -0.141, -1, 0, 47.104, 1.172, 2.22, -1, 0, 39.798, 0.423, -0.543, 1, 0, 18.053, 1.773, 2.409, 1, 0], [56.441, -0.253, 1.718, -1, 0, 48.733, -0.556, -1.604, -1, 0, 48.575, -0.928, -2.609, 1, 0, 44.313, 0.235, 0.588, 1, 0], [67.363, 0.45, -1.456, -1, 0, 20.143, 1.974, -1.186, 1, 0, 18.828, 0.96, 2.324, 1, 0, 6.198, 0.942, 2.319, -1, 0], [104.934, 1.653, 0.04, -1, 0, 53.702, -0.214, -2.571, 1, 0, 48.569, -1.758, 3.115, -1, 0, 23.082, 2.215, 2.304, 1, 0], [45.917, 0.672, 1.469, -1, 0, 44.454, 1.162, -2.291, 1, 0, 39.271, 2.072, -1.526, 1, 0, 29.172, 1.245, 1.196, -1, 0], [54.567, 0.269, -0, 1, 0, 47.307, -0.616, 2.794, -1, 0, 34.8, 0.655, 0.303, 1, 0, 22.892, -1.192, -2.829, -1, 0], [35.083, -1.978, -1.848, -1, 0, 17.386, -0.925, 1.089, 1, 0, 16.814, -0.884, 1.156, -1, 0, 10.642, -1.691, 1.699, 1, 0], [30.327, -2.19, 2.586, 1, 0, 22.911, -1.748, -0.025, -1, 0, 14.203, -0.711, -1.404, 1, 0, 7.193, -2.204, 2.609, -1, 0], [45.639, 1.11, -1.719, 1, 0, 34.184, 1.162, -0.36, -1, 0, 24.861, -0.09, -1.361, 1, 0, 5.775, 1.95, -1.722, -1, 0], [34.056, -0.283, 0.157, 1, 0, 16.64, -1.463, 3.14, -1, 0, 16.594, -1.269, 3.007, 1, 0, 12.279, -0.948, -1.787, -1, 0], [82.017, 0.918, -0.214, -1, 0, 50.465, 0.266, 2.783, -1, 0, 27.129, -0.988, -0.433, 1, 0, 22.577, 1.764, 2.373, 1, 0], [46.989, -2.027, -2.403, 1, 0, 40.974, -1.907, 1.953, 1, 0, 26.891, -0.231, -0.55, -1, 0, 15.067, -1.604, 0.748, -1, 0], [80.913, 0.482, 2.183, 1, 0, 30.72, -0.203, -2.005, 1, 0, 29.926, 2.229, -2.458, -1, 0, 28.406, -0.43, -1.454, -1, 0], [64.515, -1.859, 1.377, -1, 0, 51.55, -1.334, -3.137, 1, 0, 42.641, -1.734, -1.273, -1, 0, 39.208, -2.233, 1.338, 1, 0], [65.22, 0.193, -2.98, 1, 0, 38.146, 1.587, -0.142, 1, 0, 26.842, 1.258, 1.223, -1, 0, 5.304, -1.982, -0.769, -1, 0], [47.594, 0.356, 2.663, -1, 0, 44.724, 1.324, -1.861, -1, 0, 41.939, 0.646, -0.392, 1, 0, 40.483, 2.338, 1.025, 1, 0], [71.509, 0.715, -0.701, -1, 0, 57.353, 0.814, 2.733, 1, 0, 50.742, 0.494, -1.49, -1, 0, 14.052, 1.24, -0.833, 1, 0], [57.387, 2.366, 0.721, 1, 0, 44.417, -2.162, 2.9, 1, 0, 39.528, -2.051, -0.31, -1, 0, 31.206, 1.637, -2.272, -1, 0], [116.456, 2.117, 0.722, -1, 0, 88.352, 1.654, -2.539, 1, 0, 24.342, 1.97, -1.865, -1, 0, 16.205, 1.496, -2.166, 1, 0], [79.749, 0.557, -0.57, -1, 0, 77.994, -1.515, 1.862, 1, 0, 35.779, -1.704, -2.131, -1, 0, 29.906, 0.385, -2.922, 1, 0], [58.748, -0.535, 0.789, -1, 0, 18.291, -0.89, -1.689, 1, 0, 11.284, -0.351, 2.017, 1, 0, 5.577, -0.862, -1.702, -1, 0], [63.845, -0.291, -3.067, 1, 0, 34.019, -0.118, -2.994, 1, 0, 18.449, -1.291, 1.423, -1, 0, 11.408, -0.955, 2.865, -1, 0], [46.304, -1.439, 0.69, -1, 0, 17.571, -1.329, -2.122, 1, 0, 13.131, -1.394, -2.219, -1, 0, 12.449, -1.148, 1.532, 1, 0], [89.319, -0.622, 1.464, 1, 0, 51.488, -0.351, 2.38, 1, 0, 46.617, -0.942, -1.826, -1, 0, 32.07, -1.17, -2.951, -1, 0], [151.983, 0.394, -1.339, -1, 0, 44.865, 1.266, -2.041, 1, 0, 19.704, 0.496, 2.517, -1, 0, 16.305, 0.512, 2.515, 1, 0], [40.153, -0.146, -2.128, -1, 0, 27.853, -1.332, 1.911, -1, 0, 20.774, -0.766, 0.429, 1, 0, 15.071, 0.575, 1.597, 1, 0], [81.125, 1.988, -0.221, 1, 0, 78.772, -0.537, 3.094, 1, 0, 40.373, -0.198, 1.281, -1, 0, 26.882, 0.919, -2.009, -1, 0], [37.982, 0.306, 0.375, 1, 0, 36.044, -1.101, -2.475, -1, 0, 28.886, 0.152, 1.79, -1, 0, 18.249, -0.618, -1.499, 1, 0], [63.225, 0.733, -3.052, 1, 0, 41.819, 0.675, 1.093, -1, 0, 36.876, 2.06, -0.96, 1, 0, 25.27, 1.82, -0.162, -1, 0], [111.925, -0.918, -1.101, 1, 0, 87.887, 1.687, 2.367, -1, 0, 25.624, 2.093, 0.4, 1, 0, 15.406, -1.977, 2.646, -1, 0], [145.749, 1.434, 1.137, 1, 0, 98.839, 0.725, -2.598, 1, 0, 53.082, 1.255, -1.414, -1, 0, 17.151, 0.182, -0.394, -1, 0], [101.025, 0.888, -0.298, -1, 0, 100.748, 0.933, 2.919, 1, 0, 25.86, 1.684, 0.535, -1, 0, 10.364, -0.977, -2.954, 1, 0], [102.33, -0.474, -0.158, 1, 0, 61.613, -1.724, 1.113, 1, 0, 30.697, -2.313, -2.267, -1, 0, 18.628, -1.137, -2.834, -1, 0], [54.873, 0.953, 2.034, 1, 0, 31.15, 0.204, -1.65, -1, 0, 19.081, -0.578, -1.304, 1, 0, 18.636, -1.611, -0.058, -1, 0], [86.848, -0.153, -0.229, 1, 0, 50.762, 1.05, 3.076, 1, 0, 37.515, -0.053, 2.037, -1, 0, 10.377, -2.381, -1.724, -1, 0], [27.899, 0.651, -1.42, -1, 0, 14.574, -0.133, 1.831, 1, 0, 12.375, -1.891, 1.658, 1, 0, 7.685, -0.827, -1.094, -1, 0], [51.475, 0.677, 1.756, 1, 0, 44.344, 0.906, -1.957, -1, 0, 41.252, 1.93, 0.363, 1, 0, 33.177, -0.088, -1.554, -1, 0], [32.671, 1.822, 0.131, 1, 0, 19.216, 2.067, -1.959, -1, 0, 18.712, 0.843, -3.016, 1, 0, 13.286, 1.556, 2.068, -1, 0], [77.374, 0.935, -1.24, 1, 0, 47.319, 2.236, 1.881, -1, 0, 24.544, 0.721, 2.783, -1, 0, 12.209, -0.462, -2.663, 1, 0], [34.418, 0.488, 2.615, 1, 0, 22.991, 0.352, -0.236, -1, 0, 14.379, -0.182, -0.794, 1, 0, 12.117, 1.344, -0.975, -1, 0], [63.005, 1.359, -2.584, -1, 0, 23.429, 1.016, 0.861, 1, 0, 21.97, 1.096, -0.033, -1, 0, 9.166, 2.2, 1.351, 1, 0], [56.056, 1.875, 1.807, 1, 0, 45.124, 2.363, -2.551, 1, 0, 43.613, 1.929, -0.08, -1, 0, 34.657, 2.274, -1.459, -1, 0], [33.035, 0.047, -2.909, -1, 0, 20.176, -0.111, 0.471, 1, 0, 16.497, 0.754, 1.596, 1, 0, 14.648, 0.07, -1.481, -1, 0], [89.034, 0.213, -0.651, 1, 0, 81.344, -0.073, 2.458, -1, 0, 28.852, 0.904, -2.679, -1, 0, 11.821, 1.826, 0.218, 1, 0], [44.832, -0.926, -2.784, -1, 0, 13.796, -2.235, 0.641, 1, 0, 12.296, -2.265, 0.611, -1, 0, 9.794, -1.182, -0.46, 1, 0], [26.317, -0.468, -1.63, -1, 0, 20.594, 0.765, 1.68, -1, 0, 10.99, 1.224, 2.384, 1, 0, 7.93, 1.507, 0.624, 1, 0], [36.767, 0.882, 1.109, 1, 0, 19.521, 0.53, 0.428, 1, 0, 17.274, 2.159, -2.438, -1, 0, 7.339, 2.332, 0.287, -1, 0], [116.836, -2.24, 0.85, -1, 0, 100.871, -0.569, -1.942, 1, 0, 47.552, 0.194, -3.13, -1, 0, 22.159, -0.532, 0.846, 1, 0], [51.137, 1.152, 2.336, -1, 0, 46.597, -2.384, -0.332, 1, 0, 17.933, -1.16, -2.947, 1, 0, 7.202, -1.022, -0.123, -1, 0], [22.667, -1.11, -2.733, 1, 0, 20.072, 1.19, 0.104, 1, 0, 12.125, 0.799, -1.201, -1, 0, 7.619, -1.104, -2.741, -1, 0], [87.515, -0.156, -1.245, 1, 0, 59.633, 0.955, 1.874, 1, 0, 17.827, 1.621, 2.119, -1, 0, 10.429, -1.918, 1.973, -1, 0], [99.287, 1.111, 0.215, 1, 0, 78.508, 1.652, 2.166, 1, 0, 32.561, 0.992, -2.154, -1, 0, 21.772, 0.414, -2.253, -1, 0], [51.655, 1.406, -0.234, 1, 0, 46.24, 1.061, -2.799, -1, 0, 35.244, 1.397, 2.403, -1, 0, 20.171, -0.869, 0.03, 1, 0], [98.721, 0.75, -2.819, -1, 0, 59.229, 0.646, 0.14, 1, 0, 30.118, -0.758, 2.177, -1, 0, 26.933, 0.463, -0.791, 1, 0], [77.655, -1.381, -2.793, 1, 0, 62.309, -2.055, -0.18, -1, 0, 51.779, -2.31, 1.786, 1, 0, 25.022, -0.766, -0.255, -1, 0], [53.642, 0.366, 1.936, -1, 0, 42.166, -0.799, -1.562, 1, 0, 38.072, 0.844, -1.447, 1, 0, 24.183, 1.037, 1.078, -1, 0], [31.001, 0.873, 0.876, -1, 0, 14.876, -1.204, -2.329, 1, 0, 10.267, 0.581, -2.702, -1, 0, 8.603, 0.318, -1.234, 1, 0], [27.322, -2.32, -2.619, -1, 0, 20.633, -0.359, -0.09, 1, 0, 9.08, -2.104, 1.903, -1, 0, 7.004, -1.468, -0.015, 1, 0], [28.742, -0.662, 2.346, 1, 0, 25.871, 1.209, -0.821, 1, 0, 25.282, -0.031, 2.054, -1, 0, 14.886, 0.046, -2.074, -1, 0], [30.439, -1.684, 2.75, -1, 0, 16.206, -2.365, -0.733, 1, 0, 14.927, -0.991, 0.809, 1, 0, 12.236, -0.49, -0.625, -1, 0], [31.918, -2.037, -1.562, -1, 0, 20.026, -2.064, 2.776, 1, 0, 17.932, -1.152, 1.183, 1, 0, 9.923, -1.35, 1.244, -1, 0], [60.753, -0.604, -2.88, -1, 0, 46.108, 0.29, 0.909, 1, 0, 34.881, -1.011, -1.136, -1, 0, 22.112, 0.737, 0.702, 1, 0], [72.826, 0.74, -1.689, 1, 0, 61.935, -0.92, 1.385, 1, 0, 32.452, -1.045, -1.879, -1, 0, 31.082, 0.898, 1.109, -1, 0], [46.943, 0.372, 0.072, 1, 0, 45.977, -0.856, 1.432, 1, 0, 45.159, 0.389, -2.669, -1, 0, 37.428, 0.14, -2.043, -1, 0], [35.613, -0.837, -1.534, 1, 0, 18.638, 1.49, 1.945, -1, 0, 14.986, -1.884, 1.376, 1, 0, 7.438, -0.83, -1.497, -1, 0], [80.362, 0.414, -2.549, -1, 0, 48.405, 0.429, -1.355, 1, 0, 10.184, 1.238, 1.355, 1, 0, 5.787, 0.611, -0.73, -1, 0], [57.678, 1.214, 2.839, 1, 0, 35.61, 0.6, 0.499, -1, 0, 15.906, 0.344, 0.88, -1, 0, 11.383, -0.101, 3.098, 1, 0], [34.523, -0.551, 1.534, -1, 0, 21.577, -0.834, -0.929, 1, 0, 10.08, -2.396, -2.481, 1, 0, 7.355, -2.043, 0.698, -1, 0], [47.295, 0.417, -2.759, 1, 0, 46.476, -0.667, -0.093, -1, 0, 37, -0.38, 0.77, -1, 0, 30.728, 0.494, 3.104, 1, 0], [47.881, -0.585, -1.99, 1, 0, 38.924, -0.831, 1.743, -1, 0, 21.777, 0.621, -0.165, -1, 0, 7.399, -2.094, 1.751, 1, 0], [28.539, 1.423, 2.33, 1, 0, 24.941, 0.131, -1.241, 1, 0, 16.39, -0.218, -1.279, -1, 0, 8.995, -0.482, -0.456, -1, 0], [104.638, 0.273, 2.402, 1, 0, 103.031, -2.073, -0.066, -1, 0, 38.486, -1.705, -1.686, 1, 0, 26.233, -0.562, -2.208, -1, 0], [49.289, 0.941, -2.581, 1, 0, 43.974, 0.025, 1.515, 1, 0, 42.726, 0.93, 0.28, -1, 0, 40.19, 0.719, -1.82, -1, 0], [43.166, 0.334, 0.684, 1, 0, 26.682, 1.97, -2.966, -1, 0, 23.303, -0.915, -1.688, -1, 0, 12.556, 2.246, 1.249, 1, 0], [64.621, 1.053, 0.703, -1, 0, 61.065, 0.088, -1.717, -1, 0, 34.569, 0.138, 1.931, 1, 0, 20.838, 2.253, -2.967, 1, 0], [62.245, -0.04, -2.747, 1, 0, 33.809, -0.111, 0.369, -1, 0, 32.444, -0.083, 1.559, 1, 0, 31.678, -1.05, -0.405, -1, 0], [47.966, 0.681, 1.832, 1, 0, 25.536, 0.126, -1.487, -1, 0, 15.925, 0.433, -2.475, 1, 0, 5.277, 1.11, -1.23, -1, 0], [124.129, 1.495, 0.201, -1, 0, 66.027, 0.114, -2.492, -1, 0, 57.445, 0.785, 2.573, 1, 0, 19.746, 1.715, -2.24, 1, 0], [117.056, -1.342, -0.729, -1, 0, 87.328, -1.036, 2.633, -1, 0, 21.273, -0.115, -1.284, 1, 0, 14.263, -1e-3, 0.896, 1, 0], [38.493, -1.102, -2.907, 1, 0, 33.621, 0.079, 1.2, -1, 0, 23.268, 1.478, -1.685, 1, 0, 16.118, -1.465, 1.51, -1, 0], [59.443, -0.204, -2.166, -1, 0, 42.147, -0.849, 0.091, 1, 0, 33.597, 1.205, 1.83, 1, 0, 27.623, -0.853, 0.054, -1, 0]] }, &quot;reso&quot;: { &quot;rho/omega&quot;: [0.78, 0.149, &quot;#9467bd&quot;], &quot;phi&quot;: [1.019, 425e-5, &quot;#8c564b&quot;], &quot;J/psi&quot;: [3.097, 93e-6, &quot;#2ca02c&quot;], &quot;Upsilon&quot;: [9.46, 54e-6, &quot;#d62728&quot;], &quot;Z0&quot;: [91.19, 2.495, &quot;#17becf&quot;], &quot;Higgs&quot;: [125, 4e-3, &quot;#aec7e8&quot;] } };

  // cern/app/src/spectrum.js
  var s3 = App.state;
  var E3 = App.els;
  var R2 = CERN_REAL;
  var META = R2.meta || { sqrt_s_TeV: 7, source: &quot;CMS Open Data&quot; };
  var _lhcbPool = null;
  function lhcbPool() {
    if (_lhcbPool) return _lhcbPool;
    _lhcbPool = [];
    for (let i = 0; i < 1400; i++) {
      _lhcbPool.push(Math.random() < 0.45 ? 5.279 + (Math.random() + Math.random() + Math.random() - 1.5) * 0.06 : 4.6 + Math.random() * 1.4);
    }
    return _lhcbPool;
  }
  var G = (v, m, sg) => Math.exp(-0.5 * ((v - m) / sg) ** 2);
  var Z0 = { key: &quot;Z0&quot;, m: 91.19, hw: 6, sg: 3, thr: 0.9, amp: 1, label: &quot;Z\u2070&quot; };
  var JPSI = { key: &quot;Jpsi&quot;, m: 3.097, hw: 0.35, sg: 0.1, thr: 0.4, amp: 0.92, label: &quot;J/\u03C8&quot; };
  var PSI2 = { key: &quot;psi2S&quot;, m: 3.686, hw: 0.22, sg: 0.09, thr: 0.4, amp: 0.18, label: &quot;\u03C8(2S)&quot; };
  var U1 = { key: &quot;Ups&quot;, m: 9.46, hw: 0.4, sg: 0.16, thr: 0.6, amp: 0.36, label: &quot;\u03A5(1S)&quot; };
  var U2 = { key: &quot;Ups2S&quot;, m: 10.02, hw: 0.28, sg: 0.15, thr: 0.6, amp: 0.15, label: &quot;\u03A5(2S)&quot; };
  var U3 = { key: &quot;Ups3S&quot;, m: 10.36, hw: 0.26, sg: 0.15, thr: 0.6, amp: 0.09, label: &quot;\u03A5(3S)&quot; };
  var HIG = { key: &quot;H&quot;, m: 125, hw: 5, sg: 2.8, thr: 3.5, amp: 0.62, label: &quot;H(125)&quot; };
  var Z4L = { key: &quot;Z4l&quot;, m: 91.19, hw: 4, sg: 2.6, thr: 0.9, amp: 0.85, label: &quot;Z\u21924\u2113&quot; };
  var B0 = { key: &quot;B0&quot;, m: 5.279, hw: 0.18, sg: 0.07, thr: 0.45, amp: 0.75, label: &quot;B\u2070&quot; };
  var sup = (r, raa) => ({ ...r, raa });
  var DETSPEC = {
    ATLAS: {
      col: &quot;#58a6ff&quot;,
      fc: &quot;rgba(88,166,255,0.38)&quot;,
      beams: {
        pp: {
          channel: &quot;2mu&quot;,
          pool: () => R2.pp,
          range: [50, 150],
          bins: 60,
          bg: (v) => Math.exp(-(v - 50) / 30) * 0.12,
          reson: [Z0],
          primary: &quot;Z0&quot;,
          disco: true,
          rate: 1,
          target: 300,
          title: &quot;ATLAS \xB7 Z\u2070\u2192\u03BC\u207A\u03BC\u207B (p-p \xB7 echte CMS-Daten)&quot;,
          sub: &quot;EW-Eichkanal \xB7 Z\u2070-Resonanz bei 91 GeV&quot;,
          prov: &quot;Massen: echte CMS-Open-Data (\u03BC\u207A\u03BC\u207B) \xB7 Spuren &amp; Pile-up: illustrativ&quot;,
          real: &quot;Real ~30 Z\u2070\u2192\u03BC\u03BC pro s bei L=2\xB710\xB3\u2074 \u2014 Pr\xE4zisions-Eichkanal&quot;,
          discoMsg: &quot;\u{1F31F} 5\u03C3: Z\u2070-Resonanz pr\xE4zise vermessen!&quot;
        },
        PbPb: {
          channel: &quot;2mu&quot;,
          pool: () => R2.pp,
          range: [50, 150],
          bins: 60,
          bg: (v) => Math.exp(-(v - 50) / 30) * 0.12,
          reson: [Z0],
          primary: &quot;Z0&quot;,
          disco: true,
          rate: 0.6,
          target: 200,
          title: &quot;ATLAS \xB7 Z\u2070\u2192\u03BC\u207A\u03BC\u207B (Pb-Pb \xB7 Standardkerze)&quot;,
          sub: &quot;Z\u2070 ist elektroschwach \u2192 koppelt NICHT ans QGP, bleibt unver\xE4ndert&quot;,
          prov: &quot;Massen: echte CMS-p-p-Z\u2070 (in Pb-Pb identisch, EW) \xB7 Spuren: illustrativ&quot;,
          real: &quot;Z\u2070 als QGP-blinde Standardkerze \u2014 eicht den Pb-Pb-Lauf&quot;,
          discoMsg: &quot;\u{1F31F} 5\u03C3: Z\u2070-Standardkerze in Pb-Pb vermessen!&quot;
        }
      }
    },
    CMS: {
      col: &quot;#2ea44f&quot;,
      fc: &quot;rgba(46,164,79,0.38)&quot;,
      beams: {
        pp: {
          channel: &quot;4l&quot;,
          pool: () => R2.higgs4l,
          range: [80, 200],
          bins: 60,
          bg: (v) => Math.exp(-(v - 80) / 46),
          reson: [HIG, Z4L],
          primary: &quot;H&quot;,
          disco: true,
          rate: 0.12,
          target: 90,
          title: &quot;CMS \xB7 H\u2192ZZ*\u21924\u2113 (p-p \xB7 Goldkanal)&quot;,
          sub: &quot;Z\u21924\u2113-Peak (91) + Higgs-Bump (125) auf ZZ*-Untergrund \xB7 Higgs-Rate steigt steil mit der Energie&quot;,
          prov: &quot;4\u2113-Massen &amp; -Kinematik: ECHTE CMS-Open-Data (Record 5200, 278 Kandidaten 2011/2012)&quot;,
          real: &quot;Real nur ~1 H\u21924\u2113 pro Tag \u2014 die 278 echten Kandidaten zeigen Z\u21924\u2113 UND den Higgs-Bump&quot;,
          discoMsg: &quot;\u{1F31F} 5\u03C3: Higgs-Boson entdeckt!&quot;
        },
        PbPb: {
          channel: &quot;2mu&quot;,
          pool: () => R2.ion,
          range: [7, 12],
          bins: 50,
          bg: (v) => 0.2,
          reson: [sup(U1, 0.45), sup(U2, 0.12), sup(U3, 0.02)],
          primary: &quot;Ups&quot;,
          disco: true,
          rate: 0.5,
          target: 220,
          title: &quot;CMS \xB7 \u03A5\u2192\u03BC\u207A\u03BC\u207B (Pb-Pb \xB7 sequentielle Unterdr\xFCckung)&quot;,
          sub: &quot;Bottomonium-Thermometer: \u03A5(3S)>\u03A5(2S)>\u03A5(1S) zunehmend geschmolzen&quot;,
          prov: &quot;\u03A5-Massen: echte CMS-p-p \xB7 Pb-Pb-Unterdr\xFCckung modelliert (R_AA)&quot;,
          real: &quot;Sequentielle \u03A5-Unterdr\xFCckung misst die QGP-Temperatur (reales CMS-Resultat)&quot;,
          discoMsg: &quot;\u{1F31F} 5\u03C3: sequentielle \u03A5-Unterdr\xFCckung (QGP) nachgewiesen!&quot;,
          supp: true
        }
      }
    },
    ALICE: {
      col: &quot;#e377c2&quot;,
      fc: &quot;rgba(227,119,194,0.38)&quot;,
      beams: {
        pp: {
          channel: &quot;2mu&quot;,
          pool: () => R2.ion,
          range: [1, 12],
          bins: 55,
          bg: (v) => 0.27,
          reson: [JPSI, PSI2, U1, U2, U3],
          primary: &quot;Jpsi&quot;,
          disco: true,
          reference: true,
          rate: 1.2,
          target: 450,
          title: &quot;ALICE \xB7 J/\u03C8 + \u03A5 \u2192 \u03BC\u207A\u03BC\u207B (p-p-Referenz \xB7 echte CMS-Daten)&quot;,
          sub: &quot;Vakuum-Referenz: unverdr\xE4ngte Quarkonia \u2014 KEINE Entdeckung (QGP nur in Pb-Pb)&quot;,
          prov: &quot;Massen: echte CMS-Open-Data (\u03BC\u207A\u03BC\u207B) \xB7 Spuren &amp; Multiplizit\xE4t: illustrativ&quot;,
          real: &quot;Unverdr\xE4ngte Quarkonia \u2014 die p-p-Baseline, gegen die Pb-Pb verglichen wird&quot;,
          discoMsg: &quot;\u{1F31F} 5\u03C3: Quarkonia-Referenzspektrum (Vakuum) etabliert!&quot;
        },
        PbPb: {
          channel: &quot;2mu&quot;,
          pool: () => R2.ion,
          range: [1, 12],
          bins: 55,
          bg: (v) => 0.27,
          reson: [sup(JPSI, 0.6), sup(PSI2, 0.25), sup(U1, 0.45), sup(U2, 0.12), sup(U3, 0.02)],
          primary: &quot;Jpsi&quot;,
          disco: true,
          rate: 0.85,
          target: 380,
          title: &quot;ALICE \xB7 Quarkonia in Pb-Pb (QGP-Unterdr\xFCckung)&quot;,
          sub: &quot;R_AA < 1 vs. p-p-Referenz \xB7 Schmelzen gebundener Zust\xE4nde im Quark-Gluon-Plasma&quot;,
          prov: &quot;Massen: echte CMS-p-p-Quarkonia \xB7 QGP-Unterdr\xFCckung modelliert (R_AA)&quot;,
          real: &quot;J/\u03C8 &amp; \u03A5 im QGP unterdr\xFCckt (R_AA<1) \u2014 vs. der unverdr\xE4ngten p-p-Referenz&quot;,
          discoMsg: &quot;\u{1F31F} 5\u03C3: Quarkonia-Unterdr\xFCckung (QGP) nachgewiesen!&quot;,
          supp: true
        }
      }
    },
    LHCB: {
      col: &quot;#ff7f0e&quot;,
      fc: &quot;rgba(255,127,14,0.38)&quot;,
      beams: {
        pp: {
          channel: &quot;B&quot;,
          pool: () => lhcbPool(),
          range: [4.6, 6],
          bins: 50,
          bg: (v) => 0.25,
          reson: [B0],
          primary: &quot;B0&quot;,
          disco: true,
          rate: 0.7,
          target: 500,
          title: &quot;LHCb \xB7 B\u2070\u2192h\u207Ah\u207B (p-p \xB7 CP-Verletzung)&quot;,
          sub: &quot;Materie-Antimaterie-Asymmetrie im B-Mesonen-Zerfall&quot;,
          prov: &quot;B-Masse: kalibrierte SIMULATION (kein B im Dimuon-Set) \xB7 Vertex: illustrativ&quot;,
          real: &quot;B\u2070\u2192h\u207Ah\u207B \u2014 CP-Asymmetrie baut sich \xFCber viele Fills auf&quot;,
          discoMsg: &quot;\u{1F31F} 5\u03C3: CP-Verletzung etabliert!&quot;
        },
        PbPb: {
          channel: &quot;B&quot;,
          pool: () => lhcbPool(),
          range: [4.6, 6],
          bins: 50,
          bg: (v) => 0.25,
          reson: [B0],
          primary: &quot;B0&quot;,
          disco: false,
          rate: 0.05,
          target: 600,
          title: &quot;LHCb \xB7 spezialisiertes Vorw\xE4rtsprogramm (Pb-Pb)&quot;,
          sub: &quot;kein Standard-Schwerionen-Collider-Detektor&quot;,
          prov: &quot;B-Masse: kalibrierte Simulation \xB7 Vertex: illustrativ&quot;,
          real: &quot;LHCb misst Pb-Pb nur im Vorw\xE4rts-/Fixed-Target-Modus (SMOG) \u2014 geringe Akzeptanz&quot;,
          discoMsg: &quot;&quot;,
          note: &quot;LHCb ist im Pb-Pb-Collider-Lauf nur eingeschr\xE4nkt aktiv (spezialisiertes Vorw\xE4rts-/SMOG-Programm).&quot;
        }
      }
    }
  };
  var DETS = [&quot;ATLAS&quot;, &quot;CMS&quot;, &quot;ALICE&quot;, &quot;LHCB&quot;];
  var curBeam = () => s3.isIon ? &quot;PbPb&quot; : &quot;pp&quot;;
  function profile(det, beam) {
    const d = DETSPEC[det] || DETSPEC.ATLAS;
    return { col: d.col, fc: d.fc, ...d.beams[beam || curBeam()] };
  }
  function spec() {
    return profile(s3.selDet, curBeam());
  }
  function liveDetectors() {
    return DETS.slice();
  }
  App.liveDetectors = liveDetectors;
  function primaryReson(sp) {
    return sp.reson.find((r) => r.key === sp.primary) || sp.reson[0];
  }
  function energyVis(thr) {
    const span = 0.15 * thr + 0.3;
    return Math.max(0, Math.min(1, (s3.paramEnergy - thr) / span));
  }
  function prodVis(r) {
    return energyVis(r.thr);
  }
  function drawVis(r) {
    return prodVis(r) * (r.raa != null ? r.raa : 1);
  }
  function classifyReson(sp, m) {
    for (const r of sp.reson) {
      if (Math.abs(m - r.m) <= r.hw) return r;
    }
    return null;
  }
  function fitVal(sp, v) {
    let y = sp.bg(v);
    for (const r of sp.reson) y += drawVis(r) * r.amp * G(v, r.m, r.sg);
    return y;
  }
  function resoName(key) {
    return { Jpsi: &quot;J/psi&quot;, psi2S: &quot;psi(2S)&quot;, Ups: &quot;Upsilon(1S)&quot;, Ups2S: &quot;Upsilon(2S)&quot;, Ups3S: &quot;Upsilon(3S)&quot;, Z0: &quot;Z0&quot;, Z4l: &quot;Z(4l)&quot;, B0: &quot;B0&quot; }[key] || key;
  }
  function classify(m) {
    let best = null, bd = 1e9;
    for (const k in R2.reso) {
      if (k === &quot;Higgs&quot;) continue;
      let mm = R2.reso[k][0], br = R2.reso[k][1];
      let tol = Math.max(0.15, br * 1.5 + 0.035 * mm);
      let d = Math.abs(m - mm);
      if (d < tol &amp;&amp; d < bd) {
        bd = d;
        best = k;
      }
    }
    return best;
  }
  var _bgTracks = null;
  function bgTracks() {
    if (_bgTracks) return _bgTracks;
    _bgTracks = [];
    const arr = R2.topo &amp;&amp; R2.topo.bg || [];
    arr.forEach((t) => {
      _bgTracks.push({ pt: t[0], eta: t[1], phi: t[2], q: t[3] });
      _bgTracks.push({ pt: t[4], eta: t[5], phi: t[6], q: t[7] });
    });
    return _bgTracks;
  }
  function sampleBgTrack() {
    const a = bgTracks();
    if (a.length) return a[Math.random() * a.length | 0];
    return { pt: 4 + Math.random() * 9, eta: (Math.random() - 0.5) * 3, phi: Math.random() * 6.283, q: Math.random() < 0.5 ? 1 : -1 };
  }
  App.sampleBgTrack = sampleBgTrack;
  var _h4l = null;
  function h4lEvents() {
    if (_h4l) return _h4l;
    const T = R2.topo &amp;&amp; R2.topo.h4l || [], M = R2.higgs4l || [];
    _h4l = T.map((a, k) => ({
      M: M[k],
      leptons: [0, 1, 2, 3].map((i) => ({ pt: a[i * 5], eta: a[i * 5 + 1], phi: a[i * 5 + 2], q: a[i * 5 + 3], lep: a[i * 5 + 4] ? &quot;e&quot; : &quot;\u03BC&quot; }))
    }));
    return _h4l;
  }
  function sampleH4l() {
    const e = h4lEvents();
    return e.length ? e[Math.random() * e.length | 0] : null;
  }
  App.sampleH4l = sampleH4l;
  function pickTopo(name) {
    const map = {
      Z0: &quot;Z0&quot;,
      &quot;J/psi&quot;: &quot;Jpsi&quot;,
      &quot;psi(2S)&quot;: &quot;psi2S&quot;,
      &quot;Upsilon(1S)&quot;: &quot;Ups&quot;,
      &quot;Upsilon(2S)&quot;: &quot;Ups&quot;,
      &quot;Upsilon(3S)&quot;: &quot;Ups&quot;,
      &quot;rho/omega&quot;: &quot;low&quot;,
      &quot;phi&quot;: &quot;low&quot;
    };
    let key = name ? map[name] : &quot;bg&quot;;
    let arr = key &amp;&amp; R2.topo ? R2.topo[key] : null;
    if (arr &amp;&amp; arr.length) {
      let t = arr[Math.random() * arr.length | 0];
      return [{ pt: t[0], eta: t[1], phi: t[2], q: t[3], lep: &quot;\u03BC&quot; }, { pt: t[4], eta: t[5], phi: t[6], q: t[7], lep: &quot;\u03BC&quot; }];
    }
    let pt = 5 + Math.random() * 20, a = Math.random() * 6.283;
    return [
      { pt, eta: (Math.random() - 0.5) * 3, phi: a, q: 1, lep: &quot;\u03BC&quot; },
      { pt: pt * (0.6 + Math.random() * 0.6), eta: (Math.random() - 0.5) * 3, phi: a + Math.PI, q: -1, lep: &quot;\u03BC&quot; }
    ];
  }
  function sampleMass(sp) {
    const pool = sp.pool();
    let m = pool[Math.random() * pool.length | 0];
    let r = classifyReson(sp, m);
    if (!r) return m;
    if (Math.random() < drawVis(r)) return m;
    return sp.range[0] + Math.random() * (sp.range[1] - sp.range[0]);
  }
  function sampleEvent() {
    const sp = spec();
    if (sp.channel === &quot;4l&quot;) {
      const H = primaryReson(sp), ev = sampleH4l();
      if (ev) {
        let m3 = ev.M, suppressed = false;
        if (Math.abs(m3 - H.m) < H.hw &amp;&amp; Math.random() >= drawVis(H)) {
          m3 = sp.range[0] + Math.random() * (sp.range[1] - sp.range[0]);
          suppressed = true;
        }
        let isSig2 = !suppressed &amp;&amp; Math.abs(m3 - H.m) < H.hw;
        if (isSig2) s3.higgsCands++;
        return { M: m3, name: isSig2 ? &quot;Higgs&quot; : null, channel: &quot;4l&quot;, leptons: ev.leptons, signal: isSig2 };
      }
      let m2 = sampleMass(sp), leptons = [];
      for (let i = 0; i < 4; i++) leptons.push({ pt: 8 + Math.random() * 40, eta: (Math.random() - 0.5) * 4, phi: Math.random() * 6.283, q: i % 2 ? 1 : -1, lep: Math.random() < 0.5 ? &quot;e&quot; : &quot;\u03BC&quot; });
      let isSig = drawVis(H) > 0 &amp;&amp; Math.abs(m2 - H.m) < H.hw;
      if (isSig) s3.higgsCands++;
      return { M: m2, name: isSig ? &quot;Higgs&quot; : null, channel: &quot;4l&quot;, leptons, signal: isSig };
    }
    let m = sampleMass(sp);
    let r = classifyReson(sp, m);
    let name = r ? resoName(r.key) : null;
    return { M: m, name, channel: sp.channel, leptons: pickTopo(name), signal: !!name };
  }
  function resetSpectrumData() {
    s3.massStore = { ATLAS: [], CMS: [], ALICE: [], LHCB: [] };
    s3.collStore = { ATLAS: 0, CMS: 0, ALICE: 0, LHCB: 0 };
    s3.histAcc = { ATLAS: 0, CMS: 0, ALICE: 0, LHCB: 0 };
    s3.histSeen = { ATLAS: 0, CMS: 0, ALICE: 0, LHCB: 0 };
    s3.higgsCands = 0;
  }
  var HIST_CAP = 6e3;
  function pushMass(det, m) {
    const store = s3.massStore[det];
    if (!s3.histSeen) s3.histSeen = { ATLAS: 0, CMS: 0, ALICE: 0, LHCB: 0 };
    const seen = ++s3.histSeen[det];
    if (store.length < HIST_CAP) {
      store.push(m);
      return;
    }
    const j = Math.random() * seen | 0;
    if (j < HIST_CAP) store[j] = m;
  }
  function accumulateStatsFor(det, units) {
    units = Math.floor(units);
    if (units <= 0) return;
    const sp = profile(det);
    const rateFactor = Math.pow(s3.paramIntensity, 2) / Math.max(0.3, s3.paramBetaStar);
    const per = Math.max(1, Math.round(rateFactor * (sp.channel === &quot;4l&quot; ? 1 : 2.2)));
    for (let k = 0; k < units; k++)
      for (let i = 0; i < per; i++) pushMass(det, sampleMass(sp));
  }
  App.accumulateStatsFor = accumulateStatsFor;
  function generateMassData() {
    const sp = spec();
    let rateFactor = Math.pow(s3.paramIntensity, 2) / Math.max(0.3, s3.paramBetaStar);
    let n = Math.max(1, Math.round(rateFactor * (sp.channel === &quot;4l&quot; ? 1.5 : 5)));
    for (let i = 0; i < n; i++) pushMass(s3.selDet, sampleMass(sp));
    s3.collStore[s3.selDet] += 1;
    s3.lastEvent = sampleEvent();
    pushMass(s3.selDet, s3.lastEvent.M);
    return s3.lastEvent;
  }
  function sigFor(det) {
    const sp = profile(det), n = s3.collStore[det];
    if (n <= 0) return 0;
    if (!sp.disco) return 0;
    const pv = prodVis(primaryReson(sp));
    if (pv <= 0) return 0;
    let sig = 5 * Math.sqrt(n / sp.target) * pv;
    if (sp.reference) sig = Math.min(sig, 4.6);
    return sig;
  }
  function getSignificance() {
    return sigFor(s3.selDet);
  }
  App.sigFor = sigFor;
  function drawHist() {
    const sp = spec();
    const ctxHist = E3.ctxHist;
    let w = s3.histW, h = s3.histH;
    ctxHist.clearRect(0, 0, w, h);
    ctxHist.strokeStyle = &quot;#3a4656&quot;;
    ctxHist.lineWidth = 1;
    ctxHist.beginPath();
    ctxHist.moveTo(30, 10);
    ctxHist.lineTo(30, h - 16);
    ctxHist.lineTo(w - 8, h - 16);
    ctxHist.stroke();
    ctxHist.fillStyle = &quot;#aab8c7&quot;;
    ctxHist.font = &quot;8px sans-serif&quot;;
    let [mn, mx] = sp.range;
    ctxHist.fillText(mn + &quot; GeV&quot;, 30, h - 4);
    ctxHist.fillText(mx + &quot; GeV&quot;, w - 44, h - 4);
    let sig = getSignificance();
    const prim = primaryReson(sp);
    const specialized = !sp.disco;
    const notProd = !specialized &amp;&amp; prodVis(prim) <= 0;
    $(&quot;lbl-sig&quot;).innerText = sig.toFixed(2) + &quot; \u03C3&quot;;
    const elT = $(&quot;sp-title&quot;);
    if (elT) {
      elT.textContent = sp.title;
      elT.style.color = sp.col;
    }
    const elS = $(&quot;sp-sub&quot;);
    if (elS) elS.textContent = sp.sub;
    let sigBar = $(&quot;sig-bar&quot;), sigStatus = $(&quot;lbl-sig-status&quot;);
    sigBar.style.width = (specialized || notProd ? 0 : Math.min(100, sig / 5 * 100)) + &quot;%&quot;;
    if (sig === 0) {
      sigStatus.innerText = specialized ? &quot;Spezialisiert \xB7 keine Standard-Entdeckung&quot; : notProd ? &quot;Inbetriebnahme \xB7 &quot; + prim.label + &quot;-Rate zu gering&quot; : &quot;Sammle Statistik \u2026&quot;;
      sigStatus.style.color = &quot;#a3b4c6&quot;;
      sigBar.style.background = &quot;#3a4656&quot;;
    } else if (sp.reference) {
      sigStatus.innerText = &quot;p-p-Referenz (Vakuum) \xB7 keine Entdeckung&quot;;
      sigStatus.style.color = &quot;#58a6ff&quot;;
      sigBar.style.background = &quot;#58a6ff&quot;;
    } else if (sig < 3) {
      sigStatus.innerText = &quot;Rauschen (keine Signifikanz)&quot;;
      sigStatus.style.color = &quot;#a3b4c6&quot;;
      sigBar.style.background = &quot;#58a6ff&quot;;
    } else if (sig < 5) {
      sigStatus.innerText = &quot;\u26A0\uFE0F Signal-Hinweis (Evidenz!)&quot;;
      sigStatus.style.color = &quot;#ff7f0e&quot;;
      sigBar.style.background = &quot;#ff7f0e&quot;;
    } else {
      sigStatus.innerText = sp.discoMsg;
      sigStatus.style.color = &quot;#2ea44f&quot;;
      sigBar.style.background = &quot;#2ea44f&quot;;
    }
    let statusTxt;
    if (specialized) statusTxt = &quot;\u2139\uFE0F &quot; + sp.note;
    else if (notProd) statusTxt = &quot;\u26A0\uFE0F &quot; + prim.label + &quot;-Produktionsrate bei &quot; + s3.paramEnergy.toFixed(2) + &quot; TeV/Strahl zu gering f\xFCr eine Messung \u2014 wird ab ~&quot; + prim.thr.toFixed(1) + &quot; TeV/Strahl sichtbar (Raten-Modell).&quot;;
    else if (sp.supp) statusTxt = &quot;QGP-Unterdr\xFCckung (Modell): R_AA \u03A5(1S) \u2248 0,45, sequenziell \xB7 Signifikanz &quot; + sig.toFixed(1) + &quot; \u03C3 / 5 \u03C3.&quot;;
    else if (sp.reference) statusTxt = &quot;p-p-Referenz: unverdr\xE4ngte Quarkonia (Vakuum). Die QGP-Unterdr\xFCckung (R_AA<1) erscheint erst im Pb-Pb-Lauf.&quot;;
    else statusTxt = &quot;Sammle Statistik (Signifikanz &quot; + sig.toFixed(1) + &quot; \u03C3 von 5,0 \u03C3).&quot;;
    const elStat = $(&quot;sp-status&quot;);
    if (elStat) elStat.textContent = statusTxt;
    let realTxt = &quot;\u279C &quot; + sp.real;
    if (sp.channel === &quot;4l&quot;) realTxt += &quot; \xB7 Higgs-Fenster (120\u2013130 GeV): &quot; + s3.higgsCands + &quot; 4\u2113-Kandidaten&quot;;
    const elR = $(&quot;sp-real&quot;);
    if (elR) elR.textContent = realTxt;
    const elP = $(&quot;sp-prov&quot;);
    if (elP) elP.textContent = &quot;\u{1F4CA} &quot; + sp.prov + &quot; \xB7 Ma\xDFstab: Massen aus CMS-Open-Data (\u221As = 7 TeV, energieunabh\xE4ngig), Raten modelliert, Kandidaten statt Roh-Kollisionen.&quot;;
    const activeData = s3.massStore[s3.selDet];
    if (!activeData.length) {
      ctxHist.fillStyle = &quot;#aab8c7&quot;;
      ctxHist.font = &quot;10px monospace&quot;;
      ctxHist.fillText(&quot;WARTEN AUF KOLLISIONSDATEN\u2026&quot;, w / 2 - 92, h / 2);
      return;
    }
    let nb = sp.bins, bins = Array(nb).fill(0);
    activeData.forEach((v) => {
      if (v >= mn &amp;&amp; v < mx) {
        let i = Math.floor((v - mn) / (mx - mn) * nb);
        if (i >= 0 &amp;&amp; i < nb) bins[i]++;
      }
    });
    let maxB = Math.max(...bins, 1), bw = (w - 40) / nb;
    for (let i = 0; i < nb; i++) {
      let bh = bins[i] / maxB * (h - 30);
      let x = 30 + i * bw, y = h - 16 - bh;
      ctxHist.fillStyle = sp.fc;
      ctxHist.fillRect(x, y, bw - 1, bh);
      ctxHist.fillStyle = sp.col;
      ctxHist.fillRect(x, y, bw - 1, 1.5);
    }
    if (activeData.length > 20) {
      ctxHist.strokeStyle = sp.col;
      ctxHist.globalAlpha = 0.7;
      ctxHist.lineWidth = 0.9;
      for (let i = 0; i < nb; i++) {
        if (bins[i] < 3) continue;
        let bh = bins[i] / maxB * (h - 30);
        let x = 30 + (i + 0.5) * bw, y = h - 16 - bh;
        let err = Math.sqrt(bins[i]) / maxB * (h - 30);
        ctxHist.beginPath();
        ctxHist.moveTo(x, y - err);
        ctxHist.lineTo(x, y + err);
        ctxHist.stroke();
        ctxHist.beginPath();
        ctxHist.moveTo(x - 2, y - err);
        ctxHist.lineTo(x + 2, y - err);
        ctxHist.stroke();
        ctxHist.beginPath();
        ctxHist.moveTo(x - 2, y + err);
        ctxHist.lineTo(x + 2, y + err);
        ctxHist.stroke();
      }
      ctxHist.globalAlpha = 1;
    }
    {
      ctxHist.save();
      ctxHist.setLineDash([3, 3]);
      ctxHist.lineWidth = 0.9;
      sp.reson.forEach((r) => {
        if (r.m < mn || r.m > mx) return;
        const xm = 30 + (r.m - mn) / (mx - mn) * (w - 40);
        const on = prodVis(r) > 0, suppd = r.raa != null &amp;&amp; r.raa < 1;
        ctxHist.strokeStyle = on ? &quot;rgba(255,255,255,0.30)&quot; : &quot;rgba(255,255,255,0.12)&quot;;
        ctxHist.beginPath();
        ctxHist.moveTo(xm, h - 16);
        ctxHist.lineTo(xm, 10);
        ctxHist.stroke();
        ctxHist.fillStyle = on ? &quot;rgba(255,255,255,0.5)&quot; : &quot;rgba(255,255,255,0.22)&quot;;
        ctxHist.font = &quot;6.5px sans-serif&quot;;
        ctxHist.fillText(r.label + (suppd ? &quot; \u2193&quot; : &quot;&quot;), xm + 2, 16);
      });
      ctxHist.restore();
    }
    if (sig > 0.5) {
      let alpha = Math.min(1, Math.max(0, (sig - 0.5) / 3.5));
      ctxHist.save();
      ctxHist.globalAlpha = alpha;
      let ys = [], ymax = 1e-9;
      for (let xp = 30; xp <= w - 10; xp++) {
        let v = mn + (xp - 30) / (w - 40) * (mx - mn), yv = fitVal(sp, v);
        ys.push(yv);
        if (yv > ymax) ymax = yv;
      }
      ctxHist.strokeStyle = sp.col;
      ctxHist.lineWidth = 1.7;
      ctxHist.beginPath();
      ys.forEach((yv, k) => {
        let yp = h - 16 - yv / ymax * (h - 30);
        yp = Math.max(8, Math.min(h - 16, yp));
        k === 0 ? ctxHist.moveTo(30 + k, yp) : ctxHist.lineTo(30 + k, yp);
      });
      ctxHist.stroke();
      ctxHist.restore();
    }
  }
  App.detRate = (det) => profile(det).rate || 1;
  App.profileMeta = () => META;
  App.classify = classify;
  App.sampleEvent = sampleEvent;
  App.resetSpectrumData = resetSpectrumData;
  App.generateMassData = generateMassData;
  App.getSignificance = getSignificance;
  App.drawHist = drawHist;

  // cern/app/src/info.js
  var INFO_DB = {
    LINAC4: {
      title: &quot;LINAC 4&quot;,
      sub: &quot;Linearbeschleuniger \xB7 Protonen (H\u207B \u2192 Stripping)&quot;,
      color: &quot;#58a6ff&quot;,
      img: &quot;Linac 4 at CERN.jpg&quot;,
      cred: &quot;M. Brice/CERN \xB7 CC BY-SA 4.0&quot;,
      stats: [[&quot;L\xE4nge&quot;, &quot;86 m&quot;], [&quot;\u03B2-Bereich&quot;, &quot;0 \u2192 52 % c&quot;], [&quot;Seit&quot;, &quot;2020&quot;]],
      text: &quot;LINAC4 ist der erste Schritt im Proton-Injektorkomplex. Er beschleunigt H\u207B-Ionen (Protonen mit zwei Elektronen) mittels Hochfrequenz-Strukturen auf 160 MeV, entsprechend 52 % der Lichtgeschwindigkeit. Beim Transfer zum PSB entfernt eine Stripperfolie die Elektronen. Seit 2020 ersetzt er LINAC2 und verdoppelt die Strahlintensit\xE4t f\xFCr den LHC.&quot;
    },
    LINAC3: {
      title: &quot;LINAC 3&quot;,
      sub: &quot;Linearbeschleuniger \xB7 Blei-Ionen (ECR-Quelle)&quot;,
      color: &quot;#e377c2&quot;,
      img: &quot;Linac 3 at CERN.jpg&quot;,
      cred: &quot;M. Brice/CERN \xB7 CC BY-SA 4.0&quot;,
      stats: [[&quot;L\xE4nge&quot;, &quot;~30 m&quot;], [&quot;\u03B2-Bereich&quot;, &quot;0 \u2192 9 % c&quot;], [&quot;Seit&quot;, &quot;1994&quot;]],
      text: &quot;LINAC3 beschleunigt Blei-Ionen (Pb\xB2\u2079\u207A) aus einer Elektronen-Zyklotron-Resonanz-Quelle (ECR) auf 4,2 MeV pro Nukleon \u2013 nur 9 % der Lichtgeschwindigkeit, da Blei-Kerne (A=208) viel schwerer sind als Protonen. Die Ionen werden danach in LEIR gestapelt und durch Elektronenk\xFChlung komprimiert. LINAC3 ist seit 1994 in Betrieb.&quot;
    },
    PSB: {
      title: &quot;Proton Synchrotron Booster&quot;,
      sub: &quot;Synchrotron \xB7 4 \xFCbereinander gestapelte Ringe&quot;,
      color: &quot;#58a6ff&quot;,
      img: &quot;The Proton Synchrotron Booster in its tunnel.jpg&quot;,
      cred: &quot;Lo\xEFez, Brice/CERN \xB7 CC BY 4.0&quot;,
      stats: [[&quot;Umfang&quot;, &quot;4 \xD7 157 m&quot;], [&quot;\u03B2-Bereich&quot;, &quot;52 \u2192 95 % c&quot;], [&quot;Gebaut&quot;, &quot;1972&quot;]],
      text: &quot;Der PSB besteht aus vier \xFCbereinandergestapelten Synchrotron-Ringen und beschleunigt Protonen von 160 MeV (52 % c) auf 2 GeV (95 % c). Nach dem LHC-Injector-Upgrade (LIU, 2020) liefert er doppelt so hohe Strahlintensit\xE4ten. Die vier Ringe erlauben das gleichzeitige Beschleunigen mehrerer Pakete mit unterschiedlichem Timing.&quot;
    },
    LEIR: {
      title: &quot;Low Energy Ion Ring&quot;,
      sub: &quot;Ionen-Synchrotron \xB7 Elektronenk\xFChlung&quot;,
      color: &quot;#e377c2&quot;,
      img: &quot;Low Energy Ion Ring (LEIR).jpg&quot;,
      cred: &quot;F. Stollberger \xB7 CC BY-SA 4.0&quot;,
      stats: [[&quot;Umfang&quot;, &quot;78 m&quot;], [&quot;\u03B2-Bereich&quot;, &quot;9 \u2192 37 % c&quot;], [&quot;Aus LEAR&quot;, &quot;2005&quot;]],
      text: &quot;LEIR (Low Energy Ion Ring) wurde 2005 aus dem Antiproton-Ring LEAR umgebaut. Er akkumuliert Blei-Ionen von LINAC3 (9 % c) und k\xFChlt sie per Elektronenk\xFChlung: Ein Elektronenstrahl gleicher Mittelsgeschwindigkeit reduziert die Impulsstreuung dramatisch. Danach werden die Ionen auf 72 MeV/u (37 % c) beschleunigt und an den PS \xFCbergeben.&quot;
    },
    PS: {
      title: &quot;Proton Synchrotron&quot;,
      sub: &quot;Synchrotron \xB7 \xC4ltester noch aktiver CERN-Beschleuniger&quot;,
      color: &quot;#2ea44f&quot;,
      img: &quot;Aerial view of PS at CERN in 1965.jpg&quot;,
      cred: &quot;CERN \xB7 CC BY 4.0&quot;,
      stats: [[&quot;Umfang&quot;, &quot;628 m&quot;], [&quot;\u03B2-Bereich&quot;, &quot;95 \u2192 99,94 % c&quot;], [&quot;Seit&quot;, &quot;1959&quot;]],
      text: &quot;Das Proton-Synchrotron (PS) ist seit 1959 ununterbrochen in Betrieb. Es beschleunigt Protonen von 2 GeV (95 % c) auf 26 GeV (99,94 % c) \u2013 ab hier ist der Geschwindigkeitsgewinn minimal, aber der Energiegewinn enorm (Relativit\xE4t!). Hier entsteht die LHC-Bunch-Struktur: aus wenigen Paketen des PSB formt das PS per HF-Gymnastik (Bunch-Splitting) einen Batch von 72 Bunches mit 25 ns Abstand. Das SPS sammelt dann bis zu 4 dieser Batches und f\xFCgt sie zu einem Zug (288 Bunches) zusammen, der als Einheit in den LHC geschossen wird \u2013 ~10 solcher Z\xFCge f\xFCllen einen Strahl (2808 Bunches).&quot;
    },
    SPS: {
      title: &quot;Super Proton Synchrotron&quot;,
      sub: &quot;Synchrotron \xB7 Nobelpreis-Beschleuniger (1984)&quot;,
      color: &quot;#ff7f0e&quot;,
      img: &quot;SPS 2015.JPG&quot;,
      cred: &quot;Nazgul02 \xB7 CC BY-SA 4.0&quot;,
      stats: [[&quot;Umfang&quot;, &quot;6,9 km&quot;], [&quot;\u03B2-Bereich&quot;, &quot;99,94 \u2192 99,9998 % c&quot;], [&quot;Gebaut&quot;, &quot;1976&quot;]],
      text: &quot;Das SPS (1976) beschleunigt auf 450 GeV \u2013 die Geschwindigkeit steigt dabei von 99,94 % auf 99,9998 % c, ein scheinbar kleiner Unterschied mit riesiger Energiewirkung. Ber\xFChmt durch die Entdeckung der W- und Z-Bosonen 1983 (Nobelpreis 1984). Als letzter Vorbeschleuniger liefert es beide LHC-Strahlen \xFCber TI 2 und TI 8.&quot;
    },
    LHC: {
      title: &quot;Large Hadron Collider&quot;,
      sub: &quot;Proton-Proton / Pb-Pb Kollider \xB7 Leistungsst\xE4rkster der Welt&quot;,
      color: &quot;#58a6ff&quot;,
      img: &quot;LHC dipole magnets.jpg&quot;,
      cred: &quot;alpinethread \xB7 CC BY-SA 2.0&quot;,
      stats: [[&quot;Umfang&quot;, &quot;26 659 m&quot;], [&quot;\u03B2 bei 6,8 TeV&quot;, &quot;99,99999 % c&quot;], [&quot;Temp.&quot;, &quot;1,9 K&quot;]],
      text: &quot;Im LHC sind Protonen mit 6,8 TeV nur noch 3 m/s langsamer als Licht (99,99999 % c). 1 232 supraleitende Dipolmagnete (8,33 T, NbTi bei 1,9 K) halten die Strahlen auf Kreisbahn. An vier Interaktionspunkten kollidieren Protonenpakete bei \u221As = 13,6 TeV \u2013 mehr Energie als je zuvor erreicht. 2012 f\xFChrte der LHC zur Entdeckung des Higgs-Bosons.&quot;
    },
    ATLAS: {
      title: &quot;ATLAS Detektor&quot;,
      sub: &quot;A Toroidal LHC Apparatus \xB7 IP1 \xB7 Allzweck-Detektor&quot;,
      color: &quot;#58a6ff&quot;,
      img: &quot;CERN LHC ATLAS Detector.jpg&quot;,
      cred: &quot;S. Waldherr \xB7 CC BY-SA 4.0&quot;,
      stats: [[&quot;Ma\xDFe&quot;, &quot;46 \xD7 25 m&quot;], [&quot;Kollisions-E.&quot;, &quot;\u221As \u2264 14 TeV&quot;], [&quot;Gewicht&quot;, &quot;7 000 t&quot;]],
      text: &quot;ATLAS ist der gr\xF6\xDFte Detektor am LHC. Kollisionen bei bis zu 99,99999 % c erzeugen Teilchenschauer, die alle Schichten durchqueren: Silizium-Pixel-Tracker (innerste Lage ~33 mm vom Strahl), LAr-Kalorimeter, Tile-Kalorimeter und das Toroid-Magnetsystem (8 Spulen je 25 m). 2012 co-Entdecker des Higgs-Bosons bei mH = 125 GeV.&quot;
    },
    CMS: {
      title: &quot;CMS Detektor&quot;,
      sub: &quot;Compact Muon Solenoid \xB7 IP5 \xB7 Allzweck-Detektor&quot;,
      color: &quot;#17becf&quot;,
      img: &quot;CMS detector 2.jpg&quot;,
      cred: &quot;T. Guignard \xB7 CC BY-SA 2.0&quot;,
      stats: [[&quot;Ma\xDFe&quot;, &quot;21 \xD7 15 m&quot;], [&quot;Kollisions-E.&quot;, &quot;\u221As \u2264 14 TeV&quot;], [&quot;Gewicht&quot;, &quot;14 000 t&quot;]],
      text: &quot;CMS ist mit 14 000 t der schwerste Detektor am LHC. Herzst\xFCck ist ein 3,8-Tesla-Solenoid (100 000\xD7 st\xE4rker als das Erdfeld). Teilchen aus 99,99999 % c schnellen Kollisionen werden durch Silizium-Tracker (200 m\xB2 Streifen + 124 Mio. Pixel) und Bleiwolframat-Kristall-Kalorimeter (ECAL) gemessen. 2012 co-Entdecker des Higgs-Bosons.&quot;
    },
    ALICE: {
      title: &quot;ALICE Detektor&quot;,
      sub: &quot;A Large Ion Collider Experiment \xB7 IP2 \xB7 Schwerionen-Physik&quot;,
      color: &quot;#e377c2&quot;,
      img: &quot;ALICE experiment at CERN.jpg&quot;,
      cred: &quot;Andres T \xB7 CC BY-SA 2.0&quot;,
      stats: [[&quot;Ma\xDFe&quot;, &quot;26 \xD7 16 m&quot;], [&quot;Pb-Pb \u221As_NN&quot;, &quot;\u2264 5,5 TeV&quot;], [&quot;Gewicht&quot;, &quot;10 000 t&quot;]],
      text: &quot;ALICE untersucht Pb-Pb-Kollisionen, bei denen Pb-Kerne mit ~99,999 % c aufeinanderprallen. Dabei entsteht Quark-Gluon-Plasma (QGP) \u2013 der Zustand der Materie Mikrosekunden nach dem Urknall. Die TPC (90 m\xB3) identifiziert tausende Teilchen gleichzeitig; der ITS2-Tracker hat 12,5 Mrd. Pixel auf 10 m\xB2 \u2013 h\xF6chste Pixeldichte am LHC.&quot;
    },
    LHCB: {
      title: &quot;LHCb Detektor&quot;,
      sub: &quot;LHC beauty Experiment \xB7 IP8 \xB7 Vorw\xE4rtsspektrometer&quot;,
      color: &quot;#ff7f0e&quot;,
      img: &quot;The LHCb detector. Courtesy of Kathleen Yurkewicz. (10134715223).jpg&quot;,
      cred: &quot;STFC \xB7 CC BY-SA 2.0&quot;,
      stats: [[&quot;L\xE4nge&quot;, &quot;21 m&quot;], [&quot;Kollisions-E.&quot;, &quot;\u221As \u2264 14 TeV&quot;], [&quot;Akzeptanz&quot;, &quot;\u03B7 = 2\u20135&quot;]],
      text: &quot;LHCb misst bei p-p-Kollisionen (99,99999 % c) nur in einem engen Vorw\xE4rtskegel, wo B-Mesonen bevorzugt entstehen. Der VELO-Detektor n\xE4hert sich dem Kollisionspunkt bis auf 5,1 mm. RICH-Detektoren identifizieren Teilchen \xFCber Cherenkov-Strahlung. Ziel: die CP-Verletzung und die Asymmetrie zwischen Materie und Antimaterie im Universum verstehen.&quot;
    }
  };
  var PARAM_INFO = {
    energy: &quot;Die Kollisionsenergie im Schwerpunktsystem betr\xE4gt das Doppelte: 6,8 TeV/Strahl \u2192 \u221As = 13,6 TeV. H\xF6here Energie erm\xF6glicht schwerere Teilchen (E = mc\xB2). Das Limit setzen die supraleitenden Dipolmagnete (max. 8,33 T bei 1,9 K). Die Injektionsenergie vom SPS betr\xE4gt immer 0,45 TeV.&quot;,
    intensity: &quot;Ein Bunch enth\xE4lt ~10\xB9\xB9 Protonen. Im Nominalbetrieb hat der LHC bis zu 2 808 Bunches je Strahl (25 ns Abstand = 7,5 m). Die Luminosit\xE4t w\xE4chst quadratisch mit der Intensit\xE4t (L \u221D N\xB2). Zu hohe Intensit\xE4t verursacht koh\xE4rente Strahldynamik-Instabilit\xE4ten und Raumladungseffekte in den Injektoren.&quot;,
    beta: &quot;\u03B2* ist die Betatronfunktion am Interaktionspunkt \u2013 ein Ma\xDF f\xFCr die Fokussierung in Metern. Kleines \u03B2* = kleiner Strahldurchmesser = hohe Luminosit\xE4t. Bei \u03B2* = 0,30 m betr\xE4gt der Strahldurchmesser am IP nur ~13 \u03BCm \u2013 f\xFCnfmal d\xFCnner als ein Haar. Gesteuert durch supraleitende Quadrupol-Triplets 30 m vom Kollisionspunkt.&quot;,
    rampspeed: &quot;dB/dt bestimmt die Geschwindigkeit des Magnetfeldanstiegs. Zu schnelle Rampen erzeugen Wirbelstr\xF6me in den Magnetkammern (Sextupol-Fehler) und verkleinern die dynamische Apertur. Die reale LHC-Rampe dauert ~22 min (\u2248 0,008 T/s). \u26A0 Werte \xFCber 0,10 T/s simulieren erh\xF6htes Quench-Risiko \u2013 ein Quench (Verlust der Supraleitung) stoppt den Betrieb f\xFCr 2\u201312 Stunden.&quot;,
    ramp: &quot;Beim Ramping steigt der Dipolstrom von 763 A (0,45 TeV) auf ~11 100 A bei 6,8 TeV (Design: 11 850 A f\xFCr 7 TeV). Die 1 232 supraleitenden NbTi-Magnete m\xFCssen dabei bei 1,9 K (unter dem \u03BB-Punkt von \u2074He) bleiben. Gleichzeitig erh\xF6hen die 400-MHz-HF-Hohlraumresonatoren ihre Spannung, um die Bunches per Phasenfokussierung synchron zu halten. Ein Quench erfordert Stunden der Regeneration.&quot;,
    squeeze: &quot;Nach dem Ramping werden die Strahlen am IP durch die innersten Quadrupol-Triplets (30 m vom Kollisionspunkt) von \u03B2* \u2248 11 m auf den Zielwert fokussiert. Bei \u03B2* = 0,3 m schrumpft der Strahldurchmesser von ~80 \u03BCm auf ~13 \u03BCm. Der Squeeze ist ein kritischer, langsamer Prozess: Zu schnelles Fokussieren \xFCberschreitet die dynamische Apertur \u2013 der Strahl geht verloren.&quot;,
    prePp: 'Der Standard-Physiklauf des LHC: Protonen gegen Protonen bei voller Energie (Run 3: 6,8 TeV/Strahl \u2192 13,6 TeV). Auf DIESEM einen Strahl laufen in Wirklichkeit alle Experimente gleichzeitig: ATLAS &amp; CMS suchen das Higgs-Boson (2012 bei 8 TeV entdeckt, Nobelpreis 2013) im \u201EGoldkanal&quot; H\u2192ZZ*\u21924\u2113 und vermessen das Z\u2070 als Kalibrierung; LHCb untersucht parallel die CP-Verletzung an B-Mesonen (warum es mehr Materie als Antimaterie gibt). Higgs und CP-Verletzung brauchen also dieselbe Maschinen-Einstellung \u2013 wechsle einfach den Detektor-Tab. So f\xE4hrt der LHC ~90 % der Zeit. \u2014 Datenbasis im Widget: ECHTE CMS-Open-Data (\u03BC\u207A\u03BC\u207B, \u221As = 7 TeV; Resonanzmassen sind energieunabh\xE4ngig, daher didaktisch auf Run 3 \xFCbertragbar \u2013 Produktionsraten skalieren mit der Energie und sind modelliert). Auch der Higgs-Goldkanal H\u2192ZZ*\u21924\u2113 nutzt jetzt ECHTE CMS-Open-Data: die 278 publizierten 4-Lepton-Higgs-Kandidaten von 2011/2012 (Record 5200) \u2013 darin sieht man den Z\u21924\u2113-Peak (91 GeV) UND den Higgs-Bump (125 GeV). In der Datennahme nehmen alle Detektoren denselben Fill GLEICHZEITIG auf.',
    preQgp: 'Der Schwerionen-Lauf (~1 Monat pro Jahr, meist am Jahresende): Statt Protonen kollidieren ganze Blei-Kerne bei 2,68 TeV/Nukleon (\u221As_NN = 5,36 TeV in Run 3). In der Mini-Explosion entsteht f\xFCr 10\u207B\xB2\xB3 s das Quark-Gluon-Plasma: ein \u201EUr-Zustand&quot; der Materie bei \xFCber 10\xB9\xB2 \xB0C, in dem Quarks und Gluonen frei sind \u2013 wie wenige Millionstelsekunden nach dem Urknall. ALICE l\xF6st die tausenden Teilchen auf und misst die J/\u03C8-Unterdr\xFCckung; CMS misst die sequentielle \u03A5-Unterdr\xFCckung (\u03A5(3S)>\u03A5(2S)>\u03A5(1S)) als QGP-Thermometer; ATLAS/CMS messen das Z\u2070 als \u201EStandardkerze&quot; (es koppelt nicht ans Plasma). \u2014 Datenbasis: die Quarkonia-Massen sind ECHTE CMS-p-p-Daten; die QGP-Unterdr\xFCckung (R_AA<1) ist ein DEKLARIERTES Modell, da kein echtes Pb-Pb-Open-Data vorliegt. Die Spurmultiplizit\xE4t im Event-Display ist didaktisch reduziert (real mehrere Tausend Spuren).',
    prePilot: 'Kein Physik-Experiment, sondern die Inbetriebnahme. Der Strahl l\xE4uft nur mit Injektionsenergie (0,45 TeV, kein Hochfahren) und wenigen Protonen. Bei so geringer Rate entsteht praktisch nichts Neues \u2013 das ist Absicht: Mit einem \u201Eleichten&quot; Strahl pr\xFCfen die Operateure gefahrlos die Strahlf\xFChrung, Optik und Steuerung. Erst wenn alles stabil l\xE4uft, wird auf volle Energie und Intensit\xE4t hochgefahren. So beginnt real jeder LHC-Betriebszyklus. \u2014 Bei 0,45 TeV ist die Produktionsrate f\xFCr schwere Teilchen (Z\u2070, Higgs \u2026) praktisch null \u2192 das Spektrum zeigt nur Untergrund-Kontinuum aus echten CMS-Open-Data.',
    // ── Laien-Einstieg (Elternabend) ────────────────────────────────────────────
    introCern: &quot;Das CERN bei Genf betreibt den gr\xF6\xDFten Teilchenbeschleuniger der Welt, den LHC: einen 27 km langen Ringtunnel 100 m unter der Erde. Darin werden zwei Strahlen winziger Teilchen (Protonen) fast auf Lichtgeschwindigkeit gebracht und an vier Punkten frontal zur Kollision gebracht. Aus der Energie der Kollision entstehen kurzlebig neue Teilchen (E = mc\xB2) \u2013 gro\xDFe Detektoren (ATLAS, CMS, ALICE, LHCb) fotografieren sie. So wurde 2012 das Higgs-Boson entdeckt. Bis ein Strahl Energie hat, durchl\xE4uft er eine Kette von Vorbeschleunigern (LINAC \u2192 PSB/LEIR \u2192 PS \u2192 SPS \u2192 LHC) \u2013 genau diese Kette siehst du oben.&quot;,
    introUse: 'So bedienst du die Schaltzentrale: (1) Strahl w\xE4hlen (Protonen oder Blei-Ionen). (2) Ein Experiment-Preset laden ODER von Hand: F\xFCllprotokoll starten \u2192 Energie-Ramping \u2192 Beam Squeeze. (3) \u201EAuto-Datennahme&quot; sammelt Kollisionen. Unten siehst du links eine einzelne Kollision (Event-Display) und rechts, wie sich daraus das Massenspektrum aufbaut \u2013 findet ein Detektor 5 \u03C3, gilt das Teilchen als entdeckt. Tipp: Auf jeden Ring/Detektor klicken zeigt ein Info-Fenster mit Foto und echten Kennzahlen.',
    evRead: &quot;Jede Linie ist die Spur EINES Teilchens, das aus einer einzigen Kollision im Zentrum nach au\xDFen fliegt. Die Farbe verr\xE4t die Teilchenart (siehe Legende unten): gr\xFCn = Myon (durchquert alle Schichten), blau = Elektron, gelb = Photon, orange = Hadron-Schauer, grau gestrichelt = fehlende Energie (ein Neutrino ist unsichtbar entkommen). Die Kr\xFCmmung der Spur kommt vom Magnetfeld \u2013 je gerader, desto h\xF6her der Impuls. Aus diesen Spuren rekonstruiert man, welches Teilchen zerfallen ist. (Spuren &amp; Untergrund: echte CMS-Open-Data.)&quot;,
    spRead: 'Hier \u201Ewiegen&quot; wir Teilchen: Aus den Spuren jeder Kollision berechnen wir die invariante Masse des zerfallenen Teilchens und tragen sie ins Histogramm ein (x-Achse = Masse in GeV, y-Achse = H\xE4ufigkeit). Ein echtes Teilchen (z. B. das Z\u2070 bei 91 GeV) erscheint als scharfer \u201EBerg&quot; \xFCber dem glatten Untergrund. Die Signifikanz (in \u03C3) misst, wie sicher der Berg echt und kein Zufall ist \u2013 ab 5 \u03C3 spricht man von einer Entdeckung (so wurde 2012 das Higgs gefunden). Je mehr Kollisionen, desto deutlicher der Berg: die Signifikanz w\xE4chst mit der Wurzel der Datenmenge (\u221D \u221AN).'
  };
  function buildPhotoHdr(d) {
    if (!d.img) return d.hdr || &quot;&quot;;
    const src = &quot;https://commons.wikimedia.org/wiki/Special:FilePath/&quot; + encodeURIComponent(d.img) + &quot;?width=640&quot;;
    const fb = &quot;this.style.display='none';this.parentNode.classList.add('cv4-hdr-noimg')&quot;;
    return `<div class=&quot;cv4-hdr-photo&quot; style=&quot;--accent:${d.color}&quot;><img src=&quot;${src}&quot; alt=&quot;${d.title}&quot; loading=&quot;lazy&quot; referrerpolicy=&quot;no-referrer&quot; onerror=&quot;${fb}&quot;><div class=&quot;cv4-hdr-shade&quot;></div><div class=&quot;cv4-hdr-cred&quot;>\u{1F4F7} ${d.cred}</div><div class=&quot;cv4-hdr-fbtxt&quot;>${d.title}</div></div>`;
  }
  function showInfo(key) {
    const d = INFO_DB[key];
    if (!d) return;
    const panel = document.getElementById(&quot;info-panel&quot;);
    document.getElementById(&quot;info-hdr&quot;).innerHTML = buildPhotoHdr(d);
    document.getElementById(&quot;info-title&quot;).textContent = d.title;
    const sub = document.getElementById(&quot;info-sub&quot;);
    sub.textContent = d.sub;
    sub.style.color = d.color;
    document.getElementById(&quot;info-stats&quot;).innerHTML = d.stats.map(
      ([l, v]) => `<div class=&quot;cv4-info-stat&quot;><span class=&quot;cv4-info-stat-l&quot;>${l}</span><span class=&quot;cv4-info-stat-v&quot; style=&quot;color:${d.color}&quot;>${v}</span></div>`
    ).join(&quot;&quot;);
    document.getElementById(&quot;info-text&quot;).textContent = d.text;
    panel.classList.add(&quot;visible&quot;);
  }
  function hideInfo() {
    document.getElementById(&quot;info-panel&quot;).classList.remove(&quot;visible&quot;);
  }
  function toggleParamInfo(id) {
    const el = document.getElementById(&quot;pi-&quot; + id);
    if (!el) return;
    const isOpen = el.classList.contains(&quot;open&quot;);
    document.querySelectorAll(&quot;.cv4-param-info.open&quot;).forEach((x) => x.classList.remove(&quot;open&quot;));
    if (!isOpen) el.classList.add(&quot;open&quot;);
  }
  App.PARAM_INFO = PARAM_INFO;
  App.showInfo = showInfo;
  App.hideInfo = hideInfo;
  App.toggleParamInfo = toggleParamInfo;

  // cern/app/src/geo.gen.js
  var GEO = { &quot;lhc&quot;: [&quot;M 393.0,64.1 L 397.9,65.2 L 401.5,66.0 L 405.1,67.0 L 408.7,68.0 L 412.2,69.1 L 415.8,70.3 L 419.2,71.6 L 422.7,73.0 L 426.1,74.5 L 429.5,76.0 L 432.8,77.7 L 436.1,79.4 L 439.4,81.2 L 442.6,83.1 L 445.8,85.0 L 448.9,87.1 L 451.9,89.2 L 454.9,91.4 L 457.9,93.6 L 460.8,95.9 L 463.6,98.4 L 466.4,100.8 L 469.1,103.4 L 471.8,106.0 L 474.4,108.6 L 476.9,111.4 L 479.3,114.2 L 481.7,117.0 L 484.0,119.9 L 486.3,122.9 L 488.4,125.9 L 490.5,129.0&quot;, &quot;M 525.4,261.6 L 521.0,283.7&quot;, &quot;M 378.8,61.3 L 383.0,62.1 L 385.8,62.6 L 388.8,63.2 L 393.0,64.1&quot;, &quot;M 262.1,81.5 L 265.4,79.5 L 268.8,77.5 L 272.2,75.6 L 275.7,73.8 L 279.3,72.1 L 282.8,70.5 L 286.4,69.0 L 290.1,67.5 L 293.8,66.2 L 297.5,64.9 L 301.2,63.8 L 305.0,62.7 L 308.8,61.8 L 312.6,60.9 L 316.5,60.1 L 320.4,59.5 L 324.2,58.9 L 328.1,58.4 L 332.0,58.0 L 335.9,57.8 L 339.9,57.6 L 343.8,57.5 L 344.2,57.5 L 347.7,57.5 L 351.6,57.7 L 355.5,57.9 L 359.5,58.2 L 363.4,58.6 L 367.2,59.2 L 371.1,59.8 L 375.0,60.5 L 378.8,61.3&quot;, &quot;M 502.9,147.7 L 505.0,150.8 L 506.9,154.0 L 508.8,157.2 L 510.6,160.5 L 512.3,163.8 L 513.9,167.2 L 515.4,170.5 L 516.9,174.0 L 518.3,177.4 L 519.6,180.9 L 520.8,184.4 L 521.9,188.0 L 522.9,191.6 L 523.9,195.2 L 524.7,198.8 L 525.5,202.4 L 526.2,206.1 L 526.8,209.8 L 527.3,213.5 L 527.7,217.2 L 528.0,220.9 L 528.2,224.6 L 528.3,228.3 L 528.4,232.1 L 528.3,235.8 L 528.2,239.5 L 527.9,243.2 L 527.6,246.9 L 527.2,250.6 L 526.7,254.3 L 526.1,258.0 L 525.4,261.6&quot;, &quot;M 490.5,129.0 L 502.9,147.7&quot;, &quot;M 521.0,283.7 L 520.2,287.3 L 519.4,290.9 L 518.4,294.5 L 518.2,295.5 L 517.4,298.1 L 516.3,301.7 L 515.1,305.2 L 513.8,308.7 L 512.4,312.1 L 511.0,315.6 L 509.4,319.0 L 507.8,322.3 L 506.1,325.6 L 504.3,328.9 L 502.4,332.1 L 500.5,335.3 L 498.5,338.4 L 496.4,341.4 L 494.2,344.5 L 491.9,347.4 L 489.6,350.3 L 487.2,353.2 L 484.7,356.0 L 482.2,358.7 L 479.6,361.3 L 476.9,363.9 L 474.2,366.5 L 471.4,368.9 L 468.5,371.3 L 465.6,373.6 L 462.7,375.9 L 459.6,378.0 L 456.6,380.1&quot;, &quot;M 438.0,392.7 L 434.9,394.6 L 431.8,396.5 L 428.7,398.3 L 425.5,400.0 L 422.3,401.7 L 419.1,403.3 L 415.8,404.8 L 412.5,406.2 L 409.1,407.6 L 405.7,408.8 L 402.3,410.0 L 398.9,411.1 L 395.4,412.2 L 391.9,413.1 L 388.4,414.0 L 384.9,414.8 L 381.4,415.5 L 377.8,416.1 L 374.2,416.6 L 370.7,417.1 L 367.1,417.4 L 363.5,417.7 L 359.9,417.9 L 356.2,418.0 L 352.6,418.1 L 349.0,418.0 L 345.4,417.9 L 341.8,417.7 L 338.2,417.4 L 334.6,417.0 L 331.0,416.5 L 327.5,415.9 L 323.9,415.3 L 320.4,414.6&quot;, &quot;M 456.6,380.1 L 450.4,384.5 L 438.0,392.7&quot;, &quot;M 307.7,412.1 L 304.1,411.5 L 300.6,410.7 L 297.0,409.9 L 293.5,409.0 L 289.9,408.0 L 286.4,406.9 L 283.0,405.8 L 279.5,404.5 L 276.1,403.2 L 272.8,401.8 L 269.4,400.3 L 266.1,398.7 L 262.9,397.1 L 259.6,395.4 L 256.4,393.6 L 253.3,391.7 L 250.2,389.7 L 247.2,387.7 L 244.2,385.6 L 241.2,383.5 L 238.3,381.2 L 235.5,378.9 L 232.7,376.5 L 230.0,374.1 L 227.3,371.6 L 224.7,369.0 L 222.2,366.4 L 219.7,363.7 L 217.3,361.0 L 214.9,358.2 L 212.6,355.3 L 210.4,352.4 L 208.3,349.5 L 206.2,346.5&quot;, &quot;M 320.4,414.6 L 313.3,413.3 L 307.7,412.1&quot;, &quot;M 193.8,327.8 L 191.7,324.7 L 189.8,321.5 L 187.9,318.3 L 186.1,315.0 L 184.4,311.7 L 182.7,308.4 L 181.2,305.0 L 179.7,301.5 L 178.3,298.1 L 177.0,294.6 L 175.8,291.1 L 174.7,287.5 L 173.6,283.9 L 172.7,280.3 L 171.8,276.7 L 171.0,273.1 L 170.4,269.4 L 169.8,265.7 L 169.3,262.0 L 168.8,258.3 L 168.5,254.6 L 168.3,250.9 L 168.2,247.2 L 168.1,243.4 L 168.2,239.7 L 168.3,236.0 L 168.5,232.3 L 168.9,228.5 L 169.3,224.8 L 169.8,221.1 L 170.4,217.5&quot;, &quot;M 206.2,346.5 L 200.0,337.1 L 193.8,327.8&quot;, &quot;M 240.1,95.2 L 251.5,88.1 L 262.1,81.5&quot;, &quot;M 175.5,191.8 L 176.3,187.9 L 177.3,184.1 L 178.3,180.2 L 179.4,176.4 L 180.6,172.6 L 181.9,168.9 L 183.3,165.1 L 184.9,161.5 L 186.5,157.8 L 188.2,154.2 L 190.0,150.7 L 191.9,147.2 L 193.9,143.7 L 195.9,140.3 L 198.1,137.0 L 200.4,133.7 L 202.7,130.5 L 205.1,127.4 L 207.6,124.3 L 210.2,121.2 L 212.9,118.3 L 215.6,115.4 L 218.4,112.6 L 221.3,109.9 L 224.3,107.2 L 227.3,104.6 L 230.4,102.1 L 233.6,99.7 L 236.8,97.4 L 240.1,95.2&quot;, &quot;M 170.4,217.5 L 173.0,204.6 L 175.5,191.8&quot;], &quot;lake&quot;: [&quot;M 759.5,366.0 L 759.7,367.9 L 759.6,369.1 L 759.2,370.1 L 759.3,371.6 L 759.6,413.6 L 758.7,415.8 L 758.7,418.2 L 757.7,421.7 L 756.2,425.4 L 756.0,425.9&quot;, &quot;M 756.0,425.9 L 752.5,430.5 L 750.5,433.0 L 749.9,433.6 L 749.4,434.3 L 749.0,435.0 L 735.2,455.1 L 730.6,462.1 L 726.9,466.3 L 727.0,466.5 L 729.3,464.5 L 728.5,467.4 L 717.9,486.6 L 717.3,488.1 L 717.4,488.4 L 706.5,510.2 L 706.1,510.5&quot;, &quot;M 706.1,510.5 L 704.7,510.7 L 703.7,511.1 L 704.5,511.6 L 700.3,512.7 L 698.5,513.6 L 697.5,513.5 L 693.5,513.6 L 693.1,513.5&quot;, &quot;M 693.1,513.5 L 690.4,511.3 L 685.0,508.0 L 684.3,508.5 L 684.6,509.0 L 686.0,509.6 L 689.7,515.9 L 691.7,516.8&quot;, &quot;M 696.1,520.1 L 698.0,523.0 L 698.4,524.1 L 697.5,524.8 L 696.7,525.4&quot;, &quot;M 688.1,529.7 L 678.9,535.7 L 677.8,535.6 L 681.3,530.6 L 681.2,529.4 L 681.5,528.9&quot;, &quot;M 681.5,528.9 L 678.8,525.2 L 676.9,528.2 L 676.1,530.8 L 674.8,532.4 L 672.8,535.0 L 671.8,536.9 L 670.3,538.5 L 669.9,540.0 L 664.3,538.6 L 664.4,538.2&quot;, &quot;M 664.4,538.2 L 664.1,537.7 L 663.5,537.7 L 663.3,538.2 L 660.5,539.1 L 653.1,539.6 L 652.8,539.8 L 653.1,539.9 L 663.5,538.7&quot;, &quot;M 627.2,537.7 L 627.5,537.3 L 631.9,531.6 L 632.6,530.7 L 634.8,530.9 L 633.5,529.4&quot;, &quot;M 633.5,529.4 L 633.6,528.8 L 633.6,528.1 L 633.8,527.4 L 633.6,525.9&quot;, &quot;M 632.8,522.0 L 637.2,521.7 L 638.2,525.3 L 637.9,526.0 L 638.5,525.4 L 637.8,521.7 L 636.7,521.2 L 635.7,520.8 L 632.6,521.3&quot;, &quot;M 620.2,455.2 L 620.6,456.7 L 620.8,457.1 L 622.6,460.7 L 623.8,461.5 L 623.6,461.6 L 623.0,460.8 L 622.9,461.8 L 623.2,462.3 L 626.9,467.0 L 627.4,468.0 L 628.7,472.5 L 631.4,474.4 L 630.1,473.7 L 629.6,474.9 L 630.4,475.0 L 632.4,477.4 L 635.4,482.8 L 634.2,487.4 L 634.0,488.1 L 633.7,489.0 L 633.9,489.5 L 634.2,489.9 L 634.2,490.2 L 633.3,489.0 L 633.4,488.1 L 631.7,490.8 L 631.7,491.1 L 631.4,490.9 L 630.4,497.4 L 630.2,496.9 L 629.1,498.1 L 628.7,500.4&quot;, &quot;M 625.4,432.4 L 625.6,434.7 L 625.8,435.5 L 625.6,435.2 L 625.1,433.1 L 624.4,436.9 L 623.2,440.7 L 622.5,447.1 L 622.7,448.3 L 622.9,450.1 L 623.3,450.8 L 623.2,451.1 L 623.0,450.9 L 623.2,450.7 L 622.9,450.2 L 621.9,449.7 L 622.1,451.2 L 621.9,451.8 L 621.8,452.5 L 621.8,452.9 L 621.8,451.5 L 621.0,452.4 L 620.5,453.5 L 620.2,455.2&quot;, &quot;M 623.5,428.5 L 623.7,428.5 L 626.4,424.5 L 626.2,423.7&quot;, &quot;M 626.3,422.8 L 627.2,424.0 L 626.4,422.6 L 626.2,421.1&quot;, &quot;M 626.2,421.1 L 625.9,420.4 L 625.0,419.5 L 625.1,419.2 L 625.5,419.0&quot;, &quot;M 625.5,419.0 L 626.0,419.5 L 626.7,420.0 L 626.0,419.3 L 625.4,418.2 L 625.5,418.0 L 625.3,416.4 L 624.9,416.5&quot;, &quot;M 624.8,415.6 L 625.3,415.5 L 626.4,417.0 L 625.5,415.9 L 625.1,415.5 L 624.3,414.2&quot;, &quot;M 624.5,413.8 L 626.3,415.1 L 626.2,414.7 L 624.1,412.4&quot;, &quot;M 626.3,404.1 L 627.7,404.6 L 627.0,405.3 L 627.8,404.6 L 626.4,404.0 L 626.3,403.9&quot;, &quot;M 626.4,402.7 L 627.5,402.7 L 627.5,403.4 L 627.6,403.5 L 627.6,402.7 L 626.5,402.2&quot;, &quot;M 627.3,396.4 L 628.0,396.9 L 628.2,397.2 L 627.9,396.5 L 627.4,395.9&quot;, &quot;M 629.1,391.0 L 630.4,392.5 L 630.6,392.0 L 629.6,390.0&quot;, &quot;M 630.7,386.3 L 631.6,386.9 L 631.7,387.5 L 631.6,387.2 L 631.4,386.5 L 630.7,386.2&quot;, &quot;M 630.7,386.2 L 631.6,383.5 L 633.3,380.2 L 633.7,378.8 L 632.0,372.7 L 632.2,372.1&quot;, &quot;M 632.5,371.1 L 634.4,371.5 L 634.1,370.9 L 634.1,368.8 L 634.6,367.4 L 636.3,364.9 L 632.5,359.1 L 629.3,356.4 L 629.1,353.9 L 629.5,354.7 L 628.9,351.4 L 628.2,345.4 L 630.2,345.3 L 628.5,343.6 L 629.0,341.9 L 629.6,342.3 L 628.8,341.7 L 629.0,339.9 L 628.8,339.5 L 629.3,338.9 L 629.7,338.5 L 629.8,338.9 L 629.7,339.2 L 629.9,338.6 L 629.6,337.8 L 631.5,335.9 L 631.8,335.5 L 632.0,335.9 L 631.9,336.1 L 632.0,335.8 L 631.6,335.4 L 631.8,334.4 L 635.4,330.4 L 637.3,331.1 L 638.3,331.2 L 638.2,330.4 L 638.0,330.0 L 638.3,329.4 L 638.6,329.1 L 638.7,328.3 L 639.0,327.2 L 642.2,322.8 L 642.7,322.4 L 644.5,322.5 L 644.9,322.4&quot;, &quot;M 644.9,322.4 L 643.1,321.2 L 643.6,320.6 L 643.5,320.4 L 643.9,320.0 L 644.3,320.8 L 644.4,320.8 L 644.3,319.9 L 645.8,313.8 L 645.9,313.5 L 646.2,313.4 L 646.6,312.8 L 648.0,308.8 L 648.2,308.1 L 648.2,307.8 L 648.5,306.7 L 648.6,306.7 L 649.8,307.3 L 649.2,305.9 L 650.5,301.1 L 651.0,300.8 L 651.5,299.7 L 652.3,299.0 L 652.8,298.7 L 653.1,298.5 L 654.4,297.4 L 661.1,288.9 L 661.7,288.0 L 661.9,287.8 L 661.7,287.2 L 662.2,285.4 L 663.3,284.2 L 665.8,282.9 L 667.8,282.0 L 669.1,281.4 L 670.8,281.0 L 671.2,281.3 L 672.1,281.6 L 673.2,281.6 L 673.7,281.7 L 674.0,282.0 L 674.6,281.9 L 675.2,281.8 L 674.5,281.1 L 675.1,280.7 L 676.8,279.9 L 677.1,280.4 L 676.8,282.1 L 676.3,282.7 L 675.6,282.6 L 676.9,284.8 L 676.8,285.7 L 675.7,286.8 L 675.5,286.4 L 676.6,287.4 L 676.0,286.7 L 677.1,285.3 L 677.7,283.8 L 678.2,279.7 L 678.2,279.4 L 678.5,278.4 L 678.6,278.0 L 679.8,271.9 L 680.4,269.6 L 680.7,267.8 L 681.1,265.8 L 681.9,261.8 L 682.6,258.8 L 682.6,258.9&quot;, &quot;M 682.6,258.9 L 683.0,257.8 L 683.6,256.8 L 683.8,254.9 L 684.7,252.9 L 685.3,252.9 L 685.8,251.4 L 688.9,244.4 L 689.1,243.8 L 688.0,242.6 L 687.8,242.0 L 688.5,241.5 L 689.5,241.0 L 690.0,239.1 L 690.0,238.3 L 689.8,237.5&quot;, &quot;M 689.8,237.5 L 689.9,235.5 L 691.2,234.7 L 691.6,236.6 L 692.0,236.9&quot;, &quot;M 693.1,237.3 L 692.3,235.2 L 692.6,233.2 L 692.7,233.0&quot;, &quot;M 693.4,231.5 L 692.3,228.5 L 691.8,228.7 L 692.8,230.3&quot;, &quot;M 690.7,227.3 L 692.4,226.6 L 691.3,226.3 L 690.9,224.0 L 690.9,224.0&quot;, &quot;M 690.9,224.0 L 690.1,221.9 L 690.5,221.7 L 690.1,220.5&quot;, &quot;M 690.1,220.5 L 688.0,215.5 L 686.7,214.5 L 686.0,213.6 L 685.3,212.2 L 685.0,211.3 L 684.3,210.4 L 683.8,208.9 L 683.3,207.8 L 682.1,206.1 L 681.6,205.4 L 681.9,204.5 L 681.7,204.4 L 681.6,203.8&quot;, &quot;M 681.6,203.8 L 680.7,203.0 L 679.9,200.1 L 679.6,198.6 L 679.3,197.1 L 680.0,192.5 L 680.3,192.1 L 680.6,191.1 L 681.2,191.0 L 680.9,189.7 L 682.6,188.6 L 683.9,185.4 L 684.4,183.4 L 683.9,182.7 L 684.0,182.0 L 684.3,181.5 L 685.7,177.0 L 685.8,176.7 L 686.1,175.8 L 686.6,172.9 L 687.0,172.8 L 687.5,173.4 L 687.7,172.6 L 689.5,172.1 L 688.0,170.8 L 689.4,161.8 L 691.5,161.9 L 694.2,161.4 L 694.8,161.3 L 695.3,161.8 L 695.0,162.5 L 694.8,166.0 L 695.0,166.0 L 695.3,162.3 L 695.3,161.6 L 694.9,161.2 L 694.4,161.2 L 692.6,160.7 L 690.9,157.6 L 690.4,156.1 L 689.4,152.6 L 688.4,148.0 L 688.5,147.5 L 688.5,147.4 L 688.4,146.8 L 688.2,146.5 L 688.6,144.0 L 688.8,140.1 L 688.8,139.3 L 689.1,136.5 L 689.9,132.9 L 690.6,131.5 L 690.7,131.0 L 691.1,128.5 L 693.6,124.2 L 701.8,116.1 L 707.0,116.0 L 707.9,116.0 L 702.2,116.9 L 705.9,118.2 L 712.2,109.7 L 715.4,107.2 L 716.1,106.4 L 719.2,100.7 L 719.9,97.7 L 723.1,94.2 L 723.5,93.8 L 724.1,92.6 L 726.6,90.9 L 726.5,87.0 L 727.7,85.0 L 730.4,76.9 L 733.5,73.9 L 736.5,70.9 L 738.8,66.2 L 739.7,64.3 L 741.7,61.4 L 743.7,57.0 L 745.6,54.1 L 747.5,51.0 L 748.8,49.6 L 749.7,48.9 L 750.0,48.1 L 750.2,48.0&quot;, &quot;M 750.2,48.0 L 750.4,47.2 L 754.3,45.1 L 758.0,41.2 L 759.7,39.8&quot;, &quot;M 689.5,243.1 L 691.5,237.8 L 690.8,238.1 L 690.2,240.4 L 689.7,242.0 L 689.3,243.2 L 689.4,243.3 L 689.4,243.2&quot;, &quot;M 689.4,243.2 L 691.2,244.7 L 690.0,243.5 L 689.5,243.1&quot;, &quot;M 646.1,534.8 L 645.8,534.8 L 644.8,534.9 L 640.6,535.2 L 639.3,534.4 L 638.1,535.5 L 637.8,535.6 L 637.5,534.2 L 636.2,534.2 L 635.8,532.8 L 634.6,533.0 L 634.7,532.3 L 635.5,531.4 L 638.5,533.1 L 642.5,534.6 L 643.1,534.3 L 643.6,534.7 L 645.2,534.7 L 646.1,534.8 L 646.1,534.8&quot;, &quot;M 690.0,172.0 L 694.2,172.2 L 694.9,172.4 L 695.5,171.9 L 695.4,171.2 L 695.0,167.5 L 694.8,167.6 L 695.3,171.2 L 695.4,171.8 L 694.9,172.3 L 694.2,172.1 L 690.0,172.0&quot;, &quot;M 646.2,534.8 L 645.3,534.5 L 645.2,534.4 L 645.9,534.4 L 646.3,534.7 L 645.9,535.1 L 646.2,534.8 L 646.2,534.8&quot;, &quot;M 664.6,538.4 L 665.0,538.9 L 664.0,537.4 L 664.3,537.7 L 664.6,538.4&quot;, &quot;M 642.9,534.0 L 643.2,534.2 L 642.9,534.0 L 642.9,534.0&quot;], &quot;border&quot;: [&quot;M 402.6,367.3 L 401.6,366.5 L 400.7,365.5 L 393.4,367.2 L 391.7,368.5 L 390.1,369.9 L 387.4,373.0&quot;, &quot;M 270.4,424.6 L 253.7,410.0 L 244.4,401.3 L 242.7,399.8 L 232.0,409.0 L 228.9,412.8 L 226.4,415.5 L 220.8,420.0 L 220.6,420.1 L 219.4,419.7 L 218.1,420.3 L 217.3,420.9 L 216.8,422.9 L 217.0,423.3 L 216.1,424.9 L 214.7,425.0 L 214.0,425.8 L 213.2,425.6 L 212.2,425.8 L 211.7,425.6 L 211.1,425.4 L 209.9,425.4 L 209.2,426.0 L 208.6,426.5 L 208.3,427.1 L 208.0,427.6 L 207.3,427.3 L 206.6,427.8 L 205.2,428.3 L 204.3,428.3 L 203.8,428.1 L 202.9,427.9 L 202.8,428.3 L 202.7,429.2 L 202.4,429.4 L 201.4,429.1 L 201.2,429.4 L 200.6,429.4 L 200.3,429.5 L 199.7,430.0 L 199.1,429.7 L 198.4,429.9 L 197.9,430.2 L 197.8,431.5 L 197.3,431.5 L 196.7,431.9 L 196.2,431.4 L 195.2,431.7 L 194.5,431.6 L 194.2,431.7 L 194.0,432.0 L 193.8,432.5 L 193.0,432.4 L 192.8,432.7 L 191.8,432.5 L 191.5,432.9 L 191.1,432.8 L 190.2,432.7 L 189.8,432.8 L 188.0,431.8 L 186.4,430.9 L 186.3,430.7&quot;, &quot;M 510.2,270.1 L 510.4,270.0 L 512.9,268.7 L 513.5,269.1 L 519.4,272.2 L 525.1,275.5 L 525.4,276.2 L 518.9,282.0 L 525.3,290.4 L 524.3,294.4&quot;, &quot;M 420.7,359.2 L 412.7,364.5 L 412.7,364.2 L 412.3,363.5 L 408.5,359.8 L 406.1,361.9 L 403.8,365.2 L 402.6,367.3&quot;, &quot;M 526.2,352.7 L 527.7,355.1 L 495.8,386.5 L 482.1,387.4 L 465.6,402.9&quot;, &quot;M 563.3,-9.1 L 562.8,-8.4 L 562.6,-7.0 L 562.9,-5.1 L 560.6,-3.0 L 559.0,-2.1 L 558.4,-1.5 L 557.8,0.1 L 555.1,2.3 L 554.2,3.1 L 552.7,6.0 L 551.4,7.0 L 548.3,8.1 L 547.5,10.2 L 546.5,11.8 L 545.8,13.0 L 545.1,15.4 L 542.7,17.2 L 542.3,17.8 L 542.3,18.6 L 542.9,19.4 L 542.9,20.3 L 543.6,21.8 L 544.2,22.7 L 544.9,23.4 L 545.1,24.2 L 545.1,25.0 L 544.4,25.2 L 544.1,26.3&quot;, &quot;M 563.3,-9.1 L 564.9,-10.1 L 566.5,-11.8 L 567.6,-14.9 L 569.7,-19.0 L 570.6,-21.0 L 571.1,-22.4 L 570.6,-23.9 L 571.7,-24.6 L 573.0,-25.0 L 575.3,-25.0 L 577.4,-25.4 L 577.9,-26.1 L 577.7,-26.4 L 574.8,-26.8 L 575.2,-27.8 L 576.6,-28.8 L 576.6,-29.0 L 575.1,-30.1 L 575.7,-31.3 L 578.3,-34.2 L 579.9,-36.1 L 580.6,-36.3 L 581.3,-37.0 L 580.9,-37.7 L 579.0,-38.5 L 579.0,-39.7 L 578.8,-40.6 L 578.2,-42.4 L 578.4,-43.3 L 579.6,-44.4 L 582.0,-47.1 L 582.6,-48.2 L 583.4,-48.6 L 583.7,-48.6&quot;, &quot;M 587.8,-56.2 L 586.2,-56.9 L 585.4,-57.6 L 584.1,-58.8 L 581.9,-59.3&quot;, &quot;M 132.7,487.3 L 131.2,482.4 L 131.0,481.8 L 130.2,480.8 L 129.7,479.9 L 128.8,479.7 L 128.1,479.0 L 127.4,478.3 L 125.7,477.3 L 124.2,476.8 L 123.3,476.8 L 122.5,476.8 L 121.3,476.2 L 120.5,476.2 L 119.4,475.9 L 118.0,475.6 L 117.3,475.0 L 116.4,475.5 L 115.5,475.8 L 114.4,475.9 L 114.0,475.9 L 113.2,475.6 L 112.4,475.1 L 111.7,474.7 L 111.1,474.7 L 110.6,474.2 L 109.9,473.7 L 109.2,473.5 L 101.9,480.8 L 103.3,483.9 L 104.3,487.4 L 105.3,488.7 L 109.9,493.6 L 110.0,493.8 L 111.0,496.2 L 111.6,498.7 L 111.6,500.4 L 110.8,502.8 L 110.4,505.4 L 109.2,509.6 L 109.0,510.1 L 108.0,510.0 L 106.7,508.9 L 106.0,508.6 L 104.8,509.0 L 104.0,507.4 L 103.4,507.2 L 102.5,507.5 L 101.7,507.3 L 100.9,506.6 L 100.3,506.9 L 99.9,506.7 L 99.0,505.5 L 98.2,505.7 L 96.7,506.0 L 95.5,505.8 L 94.1,504.5 L 93.0,504.1 L 92.8,504.3 L 92.3,503.5 L 91.5,503.0 L 89.8,503.3 L 89.0,502.8 L 88.2,502.8 L 87.6,502.6 L 86.8,502.4 L 86.2,502.8 L 85.5,502.3 L 84.7,502.2 L 83.4,501.9 L 83.2,501.5 L 82.7,501.0 L 82.4,501.2 L 82.1,502.3 L 81.7,502.4 L 81.3,501.9 L 81.3,501.3 L 80.7,500.5 L 80.3,500.6 L 80.0,501.3 L 79.0,502.1 L 77.7,502.3 L 76.9,502.3 L 76.0,502.1 L 74.9,501.8 L 72.9,501.5 L 71.8,501.1 L 70.8,500.5 L 69.4,501.1 L 69.2,500.7 L 68.6,500.5 L 67.9,501.9 L 67.6,502.1 L 66.9,501.5 L 66.0,501.1 L 65.5,500.6 L 65.0,500.9 L 64.3,500.6 L 49.8,511.0 L 49.4,511.1&quot;, &quot;M 465.6,402.9 L 456.7,397.3 L 443.5,383.7 L 437.9,379.2 L 434.6,374.9 L 429.3,368.7 L 421.0,363.1 L 420.7,359.2&quot;, &quot;M 524.3,294.4 L 533.4,306.8 L 532.1,307.7 L 530.2,309.1 L 530.7,309.9 L 534.2,314.9 L 533.8,315.6 L 532.3,316.7 L 530.9,317.6 L 529.7,319.6 L 528.1,321.9 L 527.9,323.5 L 528.5,325.3 L 529.0,326.6 L 531.4,328.9 L 532.3,329.4 L 533.2,329.9 L 534.4,330.7 L 535.0,330.8 L 535.5,331.8 L 536.2,332.0 L 536.4,332.6 L 536.7,332.9 L 538.2,333.3 L 539.4,333.2 L 537.8,336.8 L 537.8,337.0 L 536.9,342.5&quot;, &quot;M 526.7,121.2 L 527.8,122.9 L 525.8,125.2 L 524.0,126.0 L 522.2,126.6 L 520.9,127.4 L 520.6,128.7 L 521.8,131.6 L 523.7,133.0 L 524.5,134.4 L 524.3,135.6 L 523.9,135.9 L 523.2,135.5 L 522.9,135.4 L 522.6,135.4 L 522.3,135.2 L 522.0,135.1 L 521.7,135.3 L 521.0,135.1 L 520.7,134.9 L 519.8,134.7 L 519.2,134.6 L 518.9,134.6 L 518.5,134.8 L 517.8,135.0 L 517.4,135.2 L 516.6,135.5 L 515.6,136.1 L 515.2,136.2 L 515.1,136.7 L 514.7,136.9 L 514.5,137.3 L 514.1,137.4 L 513.6,137.3 L 513.5,137.1 L 513.1,137.2 L 512.4,136.6 L 512.1,136.3 L 511.7,136.2 L 510.9,135.8 L 510.1,135.4 L 508.2,134.6 L 507.8,134.9 L 505.8,134.0 L 505.6,135.6 L 503.1,136.8 L 502.4,140.7 L 499.9,144.2 L 497.7,149.2 L 491.9,155.4 L 483.8,162.5 L 474.6,170.6 L 472.1,175.1 L 471.4,176.9 L 469.5,179.0 L 467.4,180.3&quot;, &quot;M 583.7,-48.6 L 584.8,-48.0 L 586.5,-47.3 L 587.2,-47.3 L 587.8,-48.0 L 588.1,-49.2 L 587.4,-50.9 L 587.3,-52.8 L 587.5,-54.9 L 588.0,-55.4 L 587.8,-56.2&quot;, &quot;M 544.1,26.3 L 543.8,26.8 L 542.9,26.9 L 542.1,26.6 L 540.5,26.8 L 539.0,27.4 L 539.3,28.4 L 539.3,29.2 L 539.1,29.5&quot;, &quot;M 539.1,29.5 L 538.6,31.0 L 539.0,32.0 L 538.9,32.5 L 538.9,33.1 L 539.2,33.7 L 539.1,34.3 L 538.2,36.0 L 537.7,36.6 L 537.2,37.0 L 534.3,39.0 L 534.1,39.5 L 534.2,40.1 L 534.5,40.7 L 534.6,41.2 L 534.2,41.6 L 532.9,42.2 L 532.3,42.6 L 531.9,43.0 L 531.7,43.8 L 530.9,44.9 L 530.1,45.9 L 528.9,46.6 L 528.4,46.6 L 527.0,45.9 L 526.2,46.2 L 526.5,46.6 L 526.7,47.1 L 526.5,47.5 L 525.4,48.3 L 524.5,49.7 L 524.6,50.2 L 524.9,50.6 L 525.1,50.8 L 526.0,51.1 L 526.3,51.5 L 526.2,52.0 L 525.6,52.8 L 525.4,53.6 L 525.2,54.1 L 525.3,54.9 L 525.4,55.4 L 525.5,56.5 L 525.5,57.2 L 525.2,57.8 L 524.6,58.8 L 523.9,59.2 L 523.6,59.5 L 523.9,59.9 L 524.6,60.4 L 524.8,61.5 L 524.9,62.1 L 525.6,62.6 L 525.8,63.1 L 525.7,63.3 L 525.4,63.5 L 524.6,63.6 L 524.4,63.7 L 524.3,64.2 L 524.8,65.9 L 524.8,66.2 L 524.8,67.2 L 524.8,68.7 L 524.6,69.4 L 524.2,69.7 L 523.5,70.0 L 523.0,70.6 L 522.6,71.5 L 522.6,72.0&quot;, &quot;M 387.4,373.0 L 379.8,376.0 L 377.5,376.1 L 373.2,375.4 L 373.9,382.1 L 367.5,382.6 L 364.6,386.7 L 360.2,387.3 L 355.7,383.6 L 352.8,384.4 L 352.4,383.9 L 352.0,383.5 L 351.0,382.2 L 350.4,381.2 L 350.2,380.9 L 349.6,380.4 L 349.2,379.7 L 348.8,379.6 L 348.2,378.3 L 347.7,377.8 L 347.3,377.0 L 346.5,376.1 L 345.9,375.0 L 345.3,374.1 L 344.4,372.8 L 343.7,372.1 L 342.5,370.9 L 341.5,368.9 L 339.9,365.6 L 336.1,367.3 L 331.7,368.9 L 329.2,370.0 L 322.9,378.7 L 319.6,382.5 L 317.6,383.6 L 315.3,385.1 L 311.0,390.5 L 306.7,396.1 L 303.2,401.0 L 303.2,402.0 L 301.7,404.9 L 300.0,409.0 L 298.9,412.4 L 296.1,417.2 L 294.5,419.9 L 289.6,425.3 L 287.8,424.1 L 284.7,431.3 L 283.5,433.6&quot;, &quot;M 467.4,180.3 L 471.6,182.2 L 474.0,183.8 L 474.8,185.4 L 473.9,187.0 L 476.2,189.7 L 475.1,195.9 L 474.5,200.5 L 474.3,201.6 L 473.0,205.0 L 470.4,209.9 L 474.6,211.6 L 475.5,212.1 L 476.0,213.0 L 476.6,214.0 L 476.8,214.8 L 477.0,215.2 L 477.4,215.7 L 477.9,216.5 L 478.0,217.0 L 478.2,218.1 L 478.4,218.4 L 478.8,218.5 L 479.4,218.4 L 479.7,218.6 L 480.2,219.1 L 481.2,219.0 L 481.7,219.1 L 482.8,219.7 L 483.2,220.3 L 483.6,220.8 L 484.1,221.4 L 484.3,221.6 L 484.5,222.3 L 484.8,222.9 L 484.9,223.2 L 485.2,223.9 L 485.3,224.6 L 485.4,224.9 L 485.5,225.3 L 485.6,225.7 L 486.7,227.0 L 487.1,227.7 L 487.5,228.2 L 487.8,228.6 L 488.5,228.5 L 488.8,228.4 L 492.5,229.7 L 493.2,231.2 L 496.3,233.4 L 497.9,235.3 L 503.1,239.8 L 501.8,240.4 L 501.5,240.6 L 498.3,243.1 L 496.0,245.0 L 493.3,247.4 L 493.0,247.7 L 492.3,248.5 L 497.9,255.5 L 504.1,262.2 L 510.2,270.1&quot;, &quot;M 522.6,72.0 L 522.7,72.6 L 526.2,73.4 L 526.9,74.1 L 527.3,76.1 L 527.1,79.8 L 526.3,80.5 L 524.6,80.8 L 523.5,82.0 L 523.2,82.9 L 524.0,83.9 L 525.5,84.4 L 525.9,85.8 L 524.1,88.3 L 523.6,89.7 L 524.7,90.7 L 524.9,91.6 L 523.3,92.5 L 522.1,93.5 L 521.2,94.7 L 521.4,96.4 L 523.3,102.1 L 524.8,104.3 L 525.9,105.2 L 529.2,105.1 L 529.9,107.1 L 530.8,110.1 L 531.0,112.5 L 530.5,114.0 L 527.7,115.8 L 525.6,117.4 L 525.0,118.4 L 525.1,119.4 L 526.7,121.2&quot;, &quot;M 186.3,430.7 L 185.9,431.6 L 185.7,432.8 L 185.2,434.0 L 183.5,437.2 L 182.9,437.9 L 182.1,438.1 L 181.0,437.9 L 178.4,436.5 L 176.7,435.2 L 175.9,434.9 L 175.3,435.1 L 174.4,436.2 L 173.9,438.9 L 174.2,439.8 L 176.1,441.7 L 176.5,443.5 L 176.2,444.8 L 173.8,446.9 L 172.8,447.2 L 169.9,446.8 L 167.5,445.8 L 165.3,444.7 L 164.5,444.7 L 163.8,446.1 L 164.5,447.4 L 166.3,449.6 L 166.2,450.4 L 164.1,453.5 L 161.0,455.8 L 159.5,457.0 L 158.4,457.2 L 155.1,455.8 L 154.5,456.0 L 154.1,456.5 L 154.2,458.5 L 155.0,460.5 L 155.6,464.4 L 155.6,466.7 L 156.3,469.2 L 155.8,469.4 L 152.6,469.7 L 148.4,471.2 L 146.0,472.9 L 141.6,477.2 L 139.5,481.4 L 138.0,484.6 L 137.5,485.1 L 132.7,487.3&quot;], &quot;sps&quot;: [&quot;M 302.4,414.2 L 298.0,412.7 L 293.8,410.8 L 289.8,408.5 L 286.0,405.8 L 282.6,402.7 L 279.4,399.3 L 276.6,395.6 L 274.2,391.7 L 272.2,387.5 L 270.7,383.6 L 269.6,379.5 L 268.8,375.3 L 268.5,371.1 L 268.5,366.8 L 268.9,362.6 L 269.7,358.4 L 270.9,354.3 L 272.4,350.4 L 274.3,346.6 L 276.5,343.0 L 279.0,339.6 L 281.9,336.4 L 285.1,333.4 L 288.6,330.7 L 292.3,328.4 L 296.2,326.4 L 300.3,324.8 L 304.5,323.6 L 308.9,322.8 L 313.2,322.4 L 317.6,322.4 L 322.0,322.9 L 326.3,323.7 L 330.5,324.9 L 334.6,326.6 L 338.5,328.6 L 342.2,330.9 L 345.7,333.6 L 348.9,336.6 L 351.8,339.9 L 354.4,343.5 L 356.6,347.3 L 358.5,351.2 L 360.0,355.4 L 361.1,359.6 L 361.8,363.9 L 362.1,368.3 L 362.0,372.6 L 361.4,376.9 L 360.5,381.2 L 359.2,385.4 L 357.5,389.4 L 355.5,393.2 L 353.0,396.9 L 350.3,400.3 L 347.3,403.4 L 344.0,406.2 L 340.4,408.7 L 336.6,410.9 L 332.6,412.7 L 328.5,414.1 L 324.3,415.2 L 320.0,415.8 L 315.6,416.0 L 311.3,415.9 L 306.9,415.3 L 302.4,414.2&quot;], &quot;ps&quot;: [&quot;M 290.9,434.3 L 290.6,434.2 L 290.2,434.1 L 289.9,434.0 L 289.5,433.8 L 289.2,433.6 L 288.9,433.3 L 288.7,433.1 L 288.4,432.8 L 288.2,432.5 L 288.0,432.2 L 287.9,431.9 L 287.7,431.5 L 287.6,431.1 L 287.5,430.7 L 287.5,430.3 L 287.5,429.8 L 287.5,429.4 L 287.6,429.0 L 287.7,428.6 L 287.9,428.2 L 288.1,427.9 L 288.3,427.5 L 288.6,427.2 L 288.9,426.9 L 289.2,426.6 L 289.6,426.4 L 289.9,426.2 L 290.3,426.1 L 290.6,426.0 L 291.0,425.9 L 291.3,425.8 L 291.7,425.8 L 292.1,425.8 L 292.5,425.9 L 292.8,425.9 L 293.2,426.0 L 293.5,426.2 L 293.8,426.3 L 294.2,426.5 L 294.5,426.7 L 294.7,427.0 L 295.0,427.3 L 295.2,427.5 L 295.4,427.9 L 295.6,428.2 L 295.8,428.5 L 295.9,428.9 L 296.0,429.2 L 296.0,429.6 L 296.1,430.0 L 296.1,430.3 L 296.0,430.7 L 296.0,431.0 L 295.9,431.4 L 295.7,431.8 L 295.6,432.1 L 295.4,432.4 L 295.2,432.7 L 294.9,433.0 L 294.7,433.3 L 294.4,433.5 L 294.1,433.7 L 293.8,433.9 L 293.4,434.1 L 293.1,434.2 L 292.7,434.3 L 292.4,434.3 L 292.0,434.4 L 291.6,434.4 L 291.3,434.4 L 290.9,434.3&quot;], &quot;psb&quot;: [&quot;M 286.1,427.3 L 286.3,427.5 L 286.5,427.5 L 286.7,427.6 L 286.9,427.6 L 287.1,427.5 L 287.3,427.4 L 287.5,427.3 L 287.6,427.2 L 287.7,427.0 L 287.8,426.8 L 287.9,426.5 L 287.8,426.3 L 287.8,426.1 L 287.7,425.9 L 287.5,425.8 L 287.4,425.6 L 287.2,425.5 L 287.0,425.4 L 286.8,425.4 L 286.5,425.5 L 286.3,425.5 L 286.1,425.6 L 286.0,425.8 L 285.8,425.9 L 285.8,426.1 L 285.7,426.4 L 285.7,426.6 L 285.7,426.8 L 285.8,427.0 L 285.9,427.2 L 286.1,427.3&quot;], &quot;linac4&quot;: [&quot;M 285.0,433.0 L 285.3,432.9 L 285.1,432.1 L 284.3,432.4 L 284.4,432.7 L 284.1,432.8 L 284.3,433.6 L 284.1,433.6 L 284.6,435.3 L 284.8,435.2 L 285.2,436.7 L 285.6,436.5 L 286.3,436.4 L 286.1,435.6 L 285.7,435.7 L 285.0,433.0&quot;], &quot;ip&quot;: { &quot;ATLAS&quot;: { &quot;x&quot;: 313.8, &quot;y&quot;: 413.3 }, &quot;CMS&quot;: { &quot;x&quot;: 385.9, &quot;y&quot;: 62.7 }, &quot;ALICE&quot;: { &quot;x&quot;: 200, &quot;y&quot;: 337.1 }, &quot;LHCB&quot;: { &quot;x&quot;: 448.3, &quot;y&quot;: 385.8 } }, &quot;ti&quot;: { &quot;ti2&quot;: &quot;M 267.8,408.1 L 262.0,406.9 L 256.2,405.5 L 252.2,404.1 L 248.3,402.3 L 244.6,400.2 L 241.2,397.7 L 238.0,394.9 L 235.1,391.8 L 232.5,388.4 L 230.1,384.9 L 226.9,379.7 L 200.0,337.1&quot;, &quot;ti8&quot;: &quot;M 369.7,380.1 L 371.7,383.9 L 374.0,387.4 L 376.7,390.7 L 379.7,393.7 L 383.0,396.5 L 386.5,398.8 L 390.3,400.8 L 394.2,402.4 L 398.3,403.6 L 402.5,404.4 L 406.7,404.7 L 410.9,404.6 L 415.2,404.1 L 419.3,403.2 L 423.3,401.7 L 427.3,400.0 L 431.0,397.9 L 434.5,395.4 L 438.0,392.7 L 448.3,385.8&quot; }, &quot;tiApprox&quot;: false, &quot;tt&quot;: [&quot;M 287.9,431.9 L 282.1,420.5 L 281.6,419.2 L 272.2,387.5&quot;, &quot;M 306.9,415.3 L 267.8,408.1&quot;], &quot;accelLabels&quot;: [{ &quot;t&quot;: &quot;SPS&quot;, &quot;x&quot;: 315.1, &quot;y&quot;: 369.6 }, { &quot;t&quot;: &quot;PS&quot;, &quot;x&quot;: 291.9, &quot;y&quot;: 430.2 }, { &quot;t&quot;: &quot;PSB&quot;, &quot;x&quot;: 286.8, &quot;y&quot;: 426.5 }], &quot;poi&quot;: [{ &quot;t&quot;: &quot;CERN Meyrin (CH)&quot;, &quot;x&quot;: 314.5, &quot;y&quot;: 424.6, &quot;a&quot;: &quot;mid&quot; }, { &quot;t&quot;: &quot;CERN Pr\xE9vessin (FR)&quot;, &quot;x&quot;: 314.5, &quot;y&quot;: 293.1, &quot;a&quot;: &quot;mid&quot; }, { &quot;t&quot;: &quot;St-Genis-Pouilly (FR)&quot;, &quot;x&quot;: 202.6, &quot;y&quot;: 370.7, &quot;a&quot;: &quot;start&quot; }, { &quot;t&quot;: &quot;Ferney-Voltaire (FR)&quot;, &quot;x&quot;: 486.9, &quot;y&quot;: 318.2, &quot;a&quot;: &quot;mid&quot; }, { &quot;t&quot;: &quot;Flughafen Genf (GVA)&quot;, &quot;x&quot;: 488.9, &quot;y&quot;: 401.9, &quot;a&quot;: &quot;mid&quot; }], &quot;lakeLabel&quot;: { &quot;x&quot;: 658, &quot;y&quot;: 303.3 } };

  // cern/app/src/geo.js
  var E4 = App.els;
  var DET_COL = { ATLAS: &quot;#58a6ff&quot;, CMS: &quot;#17becf&quot;, ALICE: &quot;#e377c2&quot;, LHCB: &quot;#ff7f0e&quot; };
  function mk(tag, attrs) {
    const el = document.createElementNS(SVG_NS, tag);
    for (const k in attrs) el.setAttribute(k, attrs[k]);
    el.classList.add(&quot;geo-element&quot;);
    el.setAttribute(&quot;vector-effect&quot;, &quot;non-scaling-stroke&quot;);
    return el;
  }
  function path(d, attrs) {
    return mk(&quot;path&quot;, Object.assign({ d, fill: &quot;none&quot; }, attrs));
  }
  function label(x, y, t, attrs) {
    const el = mk(&quot;text&quot;, Object.assign({ x, y }, attrs));
    el.textContent = t;
    return el;
  }
  function drawGeo() {
    const g2 = E4.geoLayer;
    if (!g2 || !GEO) return;
    while (g2.firstChild) g2.removeChild(g2.firstChild);
    GEO.lake.forEach((d) => g2.appendChild(path(d, {
      fill: &quot;rgba(88,166,255,0.10)&quot;,
      stroke: &quot;rgba(88,166,255,0.32)&quot;,
      &quot;stroke-width&quot;: 1
    })));
    GEO.border.forEach((d) => g2.appendChild(path(d, {
      stroke: &quot;rgba(255,255,255,0.26)&quot;,
      &quot;stroke-width&quot;: 1.1,
      &quot;stroke-dasharray&quot;: &quot;6,5&quot;
    })));
    GEO.lhc.forEach((d) => g2.appendChild(path(d, { stroke: &quot;rgba(88,166,255,0.85)&quot;, &quot;stroke-width&quot;: 2 })));
    (GEO.sps || []).forEach((d) => g2.appendChild(path(d, { stroke: &quot;rgba(255,127,14,0.85)&quot;, &quot;stroke-width&quot;: 1.8 })));
    (GEO.ps || []).forEach((d) => g2.appendChild(path(d, { stroke: &quot;rgba(46,164,79,0.9)&quot;, &quot;stroke-width&quot;: 1.5 })));
    (GEO.psb || []).forEach((d) => g2.appendChild(path(d, { stroke: &quot;rgba(88,166,255,0.9)&quot;, &quot;stroke-width&quot;: 1.5 })));
    (GEO.tt || []).forEach((d) => g2.appendChild(path(d, {
      stroke: &quot;rgba(46,164,79,0.6)&quot;,
      &quot;stroke-width&quot;: 1.3,
      &quot;stroke-dasharray&quot;: &quot;4,3&quot;
    })));
    if (GEO.ti) {
      [&quot;ti2&quot;, &quot;ti8&quot;].forEach((k) => {
        if (GEO.ti[k]) g2.appendChild(path(GEO.ti[k], {
          stroke: &quot;rgba(46,164,79,0.8)&quot;,
          &quot;stroke-width&quot;: 1.7,
          &quot;stroke-dasharray&quot;: &quot;5,4&quot;
        }));
      });
    }
    for (const name in GEO.ip || {}) {
      const p = GEO.ip[name], c = DET_COL[name] || &quot;#fff&quot;;
      const circ = mk(&quot;circle&quot;, { cx: p.x, cy: p.y, r: 4, fill: c, stroke: &quot;#0e141d&quot;, &quot;stroke-width&quot;: 1 });
      const lab = label(p.x, p.y - 7, name, { fill: c, &quot;font-size&quot;: &quot;8px&quot;, &quot;font-family&quot;: &quot;monospace&quot;, &quot;font-weight&quot;: &quot;bold&quot;, &quot;text-anchor&quot;: &quot;middle&quot; });
      circ.classList.add(&quot;geo-far&quot;);
      lab.classList.add(&quot;geo-far&quot;);
      g2.appendChild(circ);
      g2.appendChild(lab);
    }
    (GEO.accelLabels || []).forEach((p) => {
      const el = label(p.x, p.y, p.t, {
        fill: &quot;rgba(205,214,228,0.7)&quot;,
        &quot;font-size&quot;: &quot;7px&quot;,
        &quot;font-family&quot;: &quot;monospace&quot;,
        &quot;text-anchor&quot;: &quot;middle&quot;
      });
      el.classList.add(&quot;geo-far&quot;);
      g2.appendChild(el);
    });
    if (GEO.ti) [&quot;ti2&quot;, &quot;ti8&quot;].forEach((k) => {
      const d = GEO.ti[k];
      if (!d) return;
      const cs = d.replace(&quot;M &quot;, &quot;&quot;).split(&quot; L &quot;).map((s5) => s5.split(&quot;,&quot;).map(Number));
      const m = cs[Math.floor(cs.length / 2)];
      if (m &amp;&amp; m.length === 2) g2.appendChild(label(m[0], m[1] - 3, k.toUpperCase().replace(&quot;TI&quot;, &quot;TI &quot;), {
        fill: &quot;rgba(46,164,79,0.9)&quot;,
        &quot;font-size&quot;: &quot;7px&quot;,
        &quot;font-family&quot;: &quot;monospace&quot;,
        &quot;text-anchor&quot;: &quot;middle&quot;
      }));
    });
    (GEO.poi || []).forEach((p) => {
      g2.appendChild(mk(&quot;circle&quot;, { cx: p.x, cy: p.y, r: 2, fill: &quot;rgba(255,255,255,0.55)&quot; }));
      g2.appendChild(label(p.x + (p.a === &quot;start&quot; ? 5 : 0), p.y - 4, p.t, {
        fill: &quot;rgba(255,255,255,0.5)&quot;,
        &quot;font-size&quot;: &quot;7px&quot;,
        &quot;font-family&quot;: &quot;monospace&quot;,
        &quot;text-anchor&quot;: p.a
      }));
    });
    if (GEO.lakeLabel) g2.appendChild(label(GEO.lakeLabel.x, GEO.lakeLabel.y, &quot;LAC L\xC9MAN&quot;, {
      fill: &quot;rgba(88,166,255,0.6)&quot;,
      &quot;font-size&quot;: &quot;8px&quot;,
      &quot;font-family&quot;: &quot;monospace&quot;,
      &quot;text-anchor&quot;: &quot;middle&quot;
    }));
    g2.appendChild(label(112, 252, &quot;FRANKREICH (FR)&quot;, { fill: &quot;rgba(255,255,255,0.3)&quot;, &quot;font-size&quot;: &quot;8.5px&quot;, &quot;font-family&quot;: &quot;monospace&quot;, &quot;text-anchor&quot;: &quot;middle&quot; }));
    g2.appendChild(label(610, 150, &quot;SCHWEIZ (CH)&quot;, { fill: &quot;rgba(255,255,255,0.3)&quot;, &quot;font-size&quot;: &quot;8.5px&quot;, &quot;font-family&quot;: &quot;monospace&quot;, &quot;text-anchor&quot;: &quot;middle&quot; }));
    g2.appendChild(label(64, 38, &quot;JURA (FR)&quot;, { fill: &quot;rgba(255,255,255,0.24)&quot;, &quot;font-size&quot;: &quot;7px&quot;, &quot;font-family&quot;: &quot;monospace&quot; }));
    g2.appendChild(label(6, 474, &quot;\xA9 OpenStreetMap-Mitwirkende (ODbL) \xB7 Web-Mercator&quot;, {
      fill: &quot;rgba(255,255,255,0.3)&quot;,
      &quot;font-size&quot;: &quot;6px&quot;,
      &quot;font-family&quot;: &quot;monospace&quot;
    }));
    drawInjector(g2);
    drawFCC(g2);
  }
  function drawFCC(g2) {
    const LHC = { cx: 350, cy: 240, r: 180 };
    const k = 90.7 / 26.7, R3 = LHC.r * k;
    const ne = [0.6, -0.8], off = R3 - LHC.r - 4;
    const cx = LHC.cx + ne[0] * off, cy = LHC.cy + ne[1] * off;
    const view = padToAspect([[cx - R3, cy - R3], [cx + R3, cy + R3], [LHC.cx, LHC.cy]], 700 / 480, 60);
    App.geoFccView = view;
    const FC = &quot;rgba(210,120,255,&quot;;
    const fcc = mk(&quot;g&quot;);
    fcc.setAttribute(&quot;class&quot;, &quot;geo-element geo-fcc&quot;);
    fcc.appendChild(mk(&quot;circle&quot;, { cx, cy, r: R3, fill: FC + &quot;0.05)&quot;, stroke: FC + &quot;0.85)&quot;, &quot;stroke-width&quot;: 2, &quot;stroke-dasharray&quot;: &quot;10,7&quot; }));
    const fs = (s5) => (s5 * view.w / 700).toFixed(1) + &quot;px&quot;;
    const ti = label(
      cx,
      cy - R3 + 24 * view.w / 700,
      &quot;FCC \u2014 Future Circular Collider (geplant, ~91 km)&quot;,
      { fill: FC + &quot;0.95)&quot;, &quot;font-size&quot;: fs(16), &quot;font-family&quot;: &quot;monospace&quot;, &quot;font-weight&quot;: &quot;bold&quot;, &quot;text-anchor&quot;: &quot;middle&quot; }
    );
    fcc.appendChild(ti);
    fcc.appendChild(label(
      cx,
      cy - R3 + 44 * view.w / 700,
      &quot;LHC 27 km \xB7 SPS 7 km \xB7 FCC 91 km   (\xD73,4)&quot;,
      { fill: FC + &quot;0.7)&quot;, &quot;font-size&quot;: fs(11), &quot;font-family&quot;: &quot;monospace&quot;, &quot;text-anchor&quot;: &quot;middle&quot; }
    ));
    g2.appendChild(fcc);
    if (GEO.lakeLabel) {
      const t = mk(&quot;text&quot;, {
        x: GEO.lakeLabel.x + 26,
        y: GEO.lakeLabel.y + 20,
        &quot;font-size&quot;: &quot;11px&quot;,
        &quot;font-family&quot;: &quot;monospace&quot;,
        fill: FC + &quot;0.45)&quot;,
        &quot;text-anchor&quot;: &quot;middle&quot;
      });
      t.textContent = &quot;\u2726&quot;;
      t.classList.add(&quot;fcc-trigger&quot;);
      const tip = document.createElementNS(SVG_NS, &quot;title&quot;);
      tip.textContent = &quot;?&quot;;
      t.appendChild(tip);
      t.addEventListener(&quot;click&quot;, () => {
        if (App.revealFCC) App.revealFCC();
      });
      g2.appendChild(t);
    }
  }
  function ptsOf(paths) {
    const o = [];
    (paths || []).forEach((d) => d.slice(2).split(&quot; L &quot;).forEach((s5) => {
      const v = s5.split(&quot;,&quot;);
      o.push([+v[0], +v[1]]);
    }));
    return o;
  }
  function bboxC(pts) {
    const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
    const x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
    return { cx: (x0 + x1) / 2, cy: (y0 + y1) / 2, r: Math.max(x1 - x0, y1 - y0) / 2 || 1 };
  }
  function edgePath(A, B) {
    const dx = B.cx - A.cx, dy = B.cy - A.cy, d = Math.hypot(dx, dy) || 1, ux = dx / d, uy = dy / d, f = (n) => n.toFixed(2);
    return `M ${f(A.cx + ux * A.r)},${f(A.cy + uy * A.r)} L ${f(B.cx - ux * B.r)},${f(B.cy - uy * B.r)}`;
  }
  function roundedRectPath(cx, cy, w, h, r) {
    r = Math.min(r, w / 2, h / 2);
    const x = cx - w / 2, y = cy - h / 2, f = (n) => n.toFixed(2);
    return `M ${f(x + r)},${f(y)} H ${f(x + w - r)} A ${f(r)},${f(r)} 0 0 1 ${f(x + w)},${f(y + r)} V ${f(y + h - r)} A ${f(r)},${f(r)} 0 0 1 ${f(x + w - r)},${f(y + h)} H ${f(x + r)} A ${f(r)},${f(r)} 0 0 1 ${f(x)},${f(y + h - r)} V ${f(y + r)} A ${f(r)},${f(r)} 0 0 1 ${f(x + r)},${f(y)} Z`;
  }
  function padToAspect(pts, aspect, m) {
    let x0 = Math.min(...pts.map((p) => p[0])) - m, x1 = Math.max(...pts.map((p) => p[0])) + m;
    let y0 = Math.min(...pts.map((p) => p[1])) - m, y1 = Math.max(...pts.map((p) => p[1])) + m;
    let w = x1 - x0, h = y1 - y0;
    if (w / h < aspect) {
      const nw = h * aspect;
      x0 -= (nw - w) / 2;
      w = nw;
    } else {
      const nh = w / aspect;
      y0 -= (nh - h) / 2;
      h = nh;
    }
    const r = (n) => +n.toFixed(1);
    return { x: r(x0), y: r(y0), w: r(w), h: r(h) };
  }
  function drawInjector(g2) {
    const labs = GEO.accelLabels || [];
    const PS = labs.find((l) => l.t === &quot;PS&quot;), PSB = labs.find((l) => l.t === &quot;PSB&quot;);
    if (!PS) return;
    const P = &quot;#58a6ff&quot;, I = &quot;#e377c2&quot;, PSc = &quot;#2ea44f&quot;;
    (GEO.linac4 || []).forEach((d) => g2.appendChild(path(d, { stroke: P, &quot;stroke-width&quot;: 1, fill: &quot;rgba(88,166,255,0.14)&quot; })));
    const l4p = ptsOf(GEO.linac4), psPts = ptsOf(GEO.ps), psbPts = ptsOf(GEO.psb);
    const psC = psPts.length ? bboxC(psPts) : { cx: PS.x, cy: PS.y, r: 4 };
    const psbC = psbPts.length ? bboxC(psbPts) : null;
    const l4C = l4p.length ? bboxC(l4p) : null;
    const gpm = psC.r / 101, M = (m) => m * gpm;
    const leirW = M(24), leirH = M(18), leirCr = M(4);
    const dir = [-0.29, 0.96];
    const dist = psC.r + M(14) + leirW / 2;
    const leirC = { cx: psC.cx + dir[0] * dist, cy: psC.cy + dir[1] * dist, r: leirW / 2 };
    const l3len = M(30), l3y = leirC.cy + M(2);
    const l3b = [leirC.cx - leirW / 2, l3y];
    const l3a = [leirC.cx - leirW / 2 - l3len, l3y];
    const view = padToAspect(
      psPts.concat(
        psbPts,
        l4p,
        [[leirC.cx - leirW / 2, leirC.cy], [leirC.cx + leirW / 2, leirC.cy + leirH / 2], l3a, [psC.cx, psC.cy]]
      ),
      700 / 480,
      6
    );
    App.geoInjectorView = view;
    const FS = (13 * view.w / 700).toFixed(2) + &quot;px&quot;;
    const det = mk(&quot;g&quot;);
    det.setAttribute(&quot;class&quot;, &quot;geo-element geo-inj-detail&quot;);
    const beam = (d, c, dash) => det.appendChild(mk(&quot;path&quot;, Object.assign(
      { d, fill: &quot;none&quot;, stroke: c, &quot;stroke-width&quot;: 1.1 },
      dash ? { &quot;stroke-dasharray&quot;: dash } : {}
    )));
    det.appendChild(mk(&quot;path&quot;, { d: roundedRectPath(leirC.cx, leirC.cy, leirW, leirH, leirCr), fill: &quot;none&quot;, stroke: I, &quot;stroke-width&quot;: 1.1, &quot;stroke-dasharray&quot;: &quot;3,2&quot; }));
    beam(`M ${l3a[0].toFixed(2)},${l3a[1].toFixed(2)} L ${l3b[0].toFixed(2)},${l3b[1].toFixed(2)}`, I, &quot;3,2&quot;);
    beam(edgePath(leirC, psC), I);
    if (psbC) {
      if (l4C) beam(edgePath(l4C, psbC), P);
      beam(edgePath(psbC, psC), P);
    }
    const dl = (x, y, t, c, anc) => det.appendChild(label(x, y, t, { fill: c, &quot;font-size&quot;: FS, &quot;font-family&quot;: &quot;monospace&quot;, &quot;text-anchor&quot;: anc || &quot;middle&quot;, &quot;font-weight&quot;: &quot;bold&quot; }));
    dl(psC.cx, psC.cy + psC.r * 0.12, &quot;PS&quot;, PSc, &quot;middle&quot;);
    if (psbC) dl(psbC.cx, psbC.cy - psbC.r - 0.8, &quot;PSB&quot;, P, &quot;middle&quot;);
    if (l4C) dl(l4C.cx - l4C.r - 0.6, l4C.cy + 1.5, &quot;LINAC4&quot;, P, &quot;end&quot;);
    dl(leirC.cx, leirC.cy + leirH / 2 + 1.2, &quot;LEIR&quot;, I, &quot;middle&quot;);
    dl(l3a[0] - 0.6, l3y + 0.4, &quot;LINAC3&quot;, I, &quot;end&quot;);
    g2.appendChild(det);
    const hint = mk(&quot;g&quot;);
    hint.setAttribute(&quot;class&quot;, &quot;geo-element geo-inj-hint&quot;);
    hint.appendChild(mk(&quot;circle&quot;, { cx: PS.x, cy: PS.y, r: 8, fill: &quot;none&quot;, stroke: &quot;rgba(46,164,79,0.55)&quot;, &quot;stroke-width&quot;: 0.9, &quot;stroke-dasharray&quot;: &quot;2.5,2&quot; }));
    hint.appendChild(label(PS.x - 11, PS.y + 18, &quot;\u2295 Injektor-Komplex (Zoom)&quot;, { fill: &quot;rgba(205,214,228,0.72)&quot;, &quot;font-size&quot;: &quot;6.5px&quot;, &quot;font-family&quot;: &quot;monospace&quot;, &quot;text-anchor&quot;: &quot;start&quot; }));
    g2.appendChild(hint);
  }
  var _real = false;
  function setViewMode(real) {
    _real = !!real;
    if (E4.schematic) E4.schematic.style.display = _real ? &quot;none&quot; : &quot;&quot;;
    if (E4.geoLayer) E4.geoLayer.style.display = _real ? &quot;&quot; : &quot;none&quot;;
  }
  function isRealMode() {
    return _real;
  }
  App.drawGeo = drawGeo;
  App.setViewMode = setViewMode;
  App.isRealMode = isRealMode;

  // cern/app/src/handlers.js
  var fc2 = () => App.state.isIon ? FILL.ion : FILL.proton;
  var totalBatches2 = () => Math.round(fc2().total / fc2().psBatch);
  function fmtBunch(beam) {
    const b = beam === 1 ? App.state.b1Batches : App.state.b2Batches;
    return (b * fc2().psBatch).toLocaleString(&quot;de-DE&quot;);
  }
  function totalStr() {
    return fc2().total.toLocaleString(&quot;de-DE&quot;);
  }
  var s4 = App.state;
  var E5 = App.els;
  var realMode = false;
  var currentVB = { x: 0, y: 0, w: 700, h: 480 };
  var zoomTarget = null;
  function animateViewBox(tx, ty, tw, th, dur = 500) {
    const startX = currentVB.x, startY = currentVB.y, startW = currentVB.w, startH = currentVB.h;
    let t0 = null;
    function step(ts) {
      if (!t0) t0 = ts;
      let p = Math.min((ts - t0) / dur, 1);
      let ep = p * p * (3 - 2 * p);
      currentVB.x = startX + ep * (tx - startX);
      currentVB.y = startY + ep * (ty - startY);
      currentVB.w = startW + ep * (tw - startW);
      currentVB.h = startH + ep * (th - startH);
      E5.svg.setAttribute(&quot;viewBox&quot;, `${currentVB.x} ${currentVB.y} ${currentVB.w} ${currentVB.h}`);
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  function selectDetector(name) {
    document.querySelectorAll(&quot;.cv4-dtab&quot;).forEach((t) => t.classList.remove(&quot;act&quot;));
    const tab = $(&quot;dt-&quot; + name.toLowerCase());
    if (tab) tab.classList.add(&quot;act&quot;);
    s4.selDet = name;
    if (E5.spInfo) E5.spInfo.innerText = `Kandidaten (${name}): ${Math.round(s4.collStore[name] || 0).toLocaleString(&quot;de-DE&quot;)}`;
    App.drawDetBg();
    App.drawHist();
  }
  function zoomToDetector(name) {
    if (zoomTarget === name) {
      resetView();
    } else {
      zoomTarget = name;
      E5.svg.classList.remove(&quot;inj-zoom&quot;);
      E5.btnZoomMeyrin.style.display = &quot;none&quot;;
      E5.btnZoomOut.classList.remove(&quot;off&quot;);
      let tx, ty, tw = 160, th = 120;
      if (name === &quot;ATLAS&quot;) {
        tx = 270;
        ty = 360;
      } else if (name === &quot;CMS&quot;) {
        tx = 270;
        ty = 0;
      } else if (name === &quot;ALICE&quot;) {
        tx = 90;
        ty = 180;
      } else if (name === &quot;LHCB&quot;) {
        tx = 450;
        ty = 180;
      }
      animateViewBox(tx, ty, tw, th);
      selectDetector(name);
    }
  }
  function resetView() {
    zoomTarget = null;
    E5.svg.classList.remove(&quot;inj-zoom&quot;);
    E5.svg.classList.remove(&quot;fcc-on&quot;);
    E5.btnZoomOut.classList.add(&quot;off&quot;);
    E5.btnZoomMeyrin.style.display = realMode ? &quot;&quot; : &quot;none&quot;;
    animateViewBox(0, 0, 700, 480);
  }
  function revealFCC() {
    if (!realMode) return;
    const v = App.geoFccView;
    if (!v) return;
    zoomTarget = &quot;FCC&quot;;
    E5.svg.classList.remove(&quot;inj-zoom&quot;);
    E5.svg.classList.add(&quot;fcc-on&quot;);
    E5.btnZoomMeyrin.style.display = &quot;none&quot;;
    E5.btnZoomOut.classList.remove(&quot;off&quot;);
    App.setStatus('\u{1F52D} FCC \u2014 Future Circular Collider: der geplante 91-km-Ring (\xD73,4 LHC), ma\xDFst\xE4blich. \u201EAnsicht zur\xFCcksetzen&quot; kehrt zur\xFCck.', &quot;on&quot;);
    animateViewBox(v.x, v.y, v.w, v.h, 1700);
  }
  App.revealFCC = revealFCC;
  function zoomMeyrin() {
    const v = App.geoInjectorView;
    if (!v) return;
    zoomTarget = &quot;MEYRIN&quot;;
    E5.svg.classList.add(&quot;inj-zoom&quot;);
    E5.btnZoomMeyrin.style.display = &quot;none&quot;;
    E5.btnZoomOut.classList.remove(&quot;off&quot;);
    animateViewBox(v.x, v.y, v.w, v.h);
  }
  async function fuellProtokoll() {
    const totB = totalBatches2();
    if (s4.filling || s4.ramped || s4.cryoRecovery || s4.dumping || s4.b1Batches >= totB &amp;&amp; s4.b2Batches >= totB) return;
    s4.filling = true;
    s4.resetFlag = false;
    const gen = s4.fillGen;
    E5.btnAuto.classList.add(&quot;off&quot;);
    E5.sliEnergy.disabled = true;
    E5.sliIntensity.disabled = true;
    E5.sliRampSpeed.disabled = true;
    E5.selP.style.pointerEvents = &quot;none&quot;;
    E5.selI.style.pointerEvents = &quot;none&quot;;
    App.setStatus(&quot;F\xDCLLPROTOKOLL: PS-Batches laufen einzeln zum SPS und verschmelzen dort zu Z\xFCgen \u2026&quot;, &quot;on&quot;);
    const bpt = fc2().batchesPerTrain;
    const sizes = [];
    for (let r = totB; r > 0; r -= bpt) sizes.push(Math.min(bpt, r));
    const proms = [];
    for (let t = 0; t < sizes.length; t++) {
      for (const beam of [1, 2]) {
        if (s4.resetFlag) break;
        proms.push(App.injectTrain(beam, sizes[t], gen));
        App.setStatus(`F\xDCLLPROTOKOLL: SPS-Z\xFCge entstehen \u2026  B1 ${fmtBunch(1)}/${totalStr()}  \xB7  B2 ${fmtBunch(2)}/${totalStr()} Bunches`, &quot;on&quot;);
        await sleep(App.trainCadenceMs() / 2);
      }
      if (s4.resetFlag) break;
    }
    await Promise.all(proms);
    s4.filling = false;
    E5.selP.style.pointerEvents = &quot;&quot;;
    E5.selI.style.pointerEvents = &quot;&quot;;
    if (s4.resetFlag) return;
    E5.btnAuto.classList.remove(&quot;off&quot;);
    if (s4.b1Batches >= totB &amp;&amp; s4.b2Batches >= totB) {
      E5.btnRamp.classList.remove(&quot;off&quot;);
      App.setStatus(`LHC GEF\xDCLLT \u2014 ${totalStr()} Bunches/Strahl (${sizes.length} Z\xFCge), beide Strahlen stabil. Ramping m\xF6glich!`, &quot;on&quot;);
    } else {
      App.setStatus(`F\xFCllung beendet: B1 ${fmtBunch(1)}/${totalStr()}, B2 ${fmtBunch(2)}/${totalStr()} Bunches.`, &quot;on&quot;);
    }
  }
  App.selectDetector = selectDetector;
  App.zoomToDetector = zoomToDetector;
  App.fuellProtokoll = fuellProtokoll;
  function wireHandlers() {
    E5.btnSpeedToggle.addEventListener(&quot;click&quot;, () => {
      s4.isFastMode = !s4.isFastMode;
      if (s4.isFastMode) {
        E5.btnSpeedToggle.innerText = `\u23F1\uFE0F Tempo: Zeitraffer \xB7 1 s \u2248 ${SIM_SCALE.fast} s real`;
        E5.btnSpeedToggle.style.background = &quot;rgba(88,166,255,.08)&quot;;
        E5.btnSpeedToggle.style.borderColor = &quot;rgba(88,166,255,.3)&quot;;
        E5.btnSpeedToggle.style.color = &quot;#58a6ff&quot;;
      } else {
        E5.btnSpeedToggle.innerText = `\u23F1\uFE0F Tempo: Didaktisch \xB7 1 s \u2248 ${SIM_SCALE.slow} s real`;
        E5.btnSpeedToggle.style.background = &quot;rgba(227,119,194,.08)&quot;;
        E5.btnSpeedToggle.style.borderColor = &quot;rgba(227,119,194,.3)&quot;;
        E5.btnSpeedToggle.style.color = &quot;#e377c2&quot;;
      }
    });
    E5.btnToggleGeo.addEventListener(&quot;click&quot;, () => {
      realMode = !realMode;
      App.setViewMode(realMode);
      E5.btnToggleGeo.classList.toggle(&quot;act&quot;, realMode);
      E5.btnToggleGeo.innerText = realMode ? &quot;\u{1F3AC} Didaktik-Modus&quot; : &quot;\u{1F30D} Reale Ansicht&quot;;
      resetView();
      App.setStatus(realMode ? &quot;REALE ANSICHT \u2014 echte OSM-Geometrie. Tipp: \u{1F52C} Injektor-Komplex zoomt auf Meyrin.&quot; : &quot;DIDAKTIK-MODUS \u2014 schematische, animierte Beschleuniger-Kette&quot;, &quot;on&quot;);
    });
    [&quot;atlas&quot;, &quot;cms&quot;, &quot;alice&quot;, &quot;lhcb&quot;].forEach((d) => {
      const t = $(&quot;dt-&quot; + d);
      if (t) t.addEventListener(&quot;click&quot;, () => selectDetector(d.toUpperCase()));
    });
    E5.btnZoomOut.addEventListener(&quot;click&quot;, resetView);
    E5.btnZoomMeyrin.addEventListener(&quot;click&quot;, zoomMeyrin);
    if (E5.btnDiagramFull) {
      const root = E5.root || document.getElementById(&quot;cern-v4&quot;);
      const setFull = (on) => {
        root.classList.toggle(&quot;diagram-full&quot;, on);
        E5.btnDiagramFull.innerHTML = on ? &quot;\u2715 Schlie\xDFen&quot; : &quot;\u26F6 Gro\xDFansicht&quot;;
      };
      E5.btnDiagramFull.addEventListener(&quot;click&quot;, () => setFull(!root.classList.contains(&quot;diagram-full&quot;)));
      document.addEventListener(&quot;keydown&quot;, (e) => {
        if (e.key === &quot;Escape&quot; &amp;&amp; root.classList.contains(&quot;diagram-full&quot;)) setFull(false);
      });
    }
    E5.grpAtlas.addEventListener(&quot;click&quot;, () => {
      App.showInfo(&quot;ATLAS&quot;);
      zoomToDetector(&quot;ATLAS&quot;);
    });
    E5.grpCms.addEventListener(&quot;click&quot;, () => {
      App.showInfo(&quot;CMS&quot;);
      zoomToDetector(&quot;CMS&quot;);
    });
    E5.grpAlice.addEventListener(&quot;click&quot;, () => {
      App.showInfo(&quot;ALICE&quot;);
      zoomToDetector(&quot;ALICE&quot;);
    });
    E5.grpLhcb.addEventListener(&quot;click&quot;, () => {
      App.showInfo(&quot;LHCB&quot;);
      zoomToDetector(&quot;LHCB&quot;);
    });
    $(&quot;hit-linac4&quot;).addEventListener(&quot;click&quot;, () => App.showInfo(&quot;LINAC4&quot;));
    $(&quot;hit-linac3&quot;).addEventListener(&quot;click&quot;, () => App.showInfo(&quot;LINAC3&quot;));
    $(&quot;hit-psb&quot;).addEventListener(&quot;click&quot;, () => App.showInfo(&quot;PSB&quot;));
    $(&quot;hit-leir&quot;).addEventListener(&quot;click&quot;, () => App.showInfo(&quot;LEIR&quot;));
    $(&quot;hit-ps&quot;).addEventListener(&quot;click&quot;, () => App.showInfo(&quot;PS&quot;));
    $(&quot;hit-sps&quot;).addEventListener(&quot;click&quot;, () => App.showInfo(&quot;SPS&quot;));
    $(&quot;hit-lhc&quot;).addEventListener(&quot;click&quot;, () => App.showInfo(&quot;LHC&quot;));
    $(&quot;info-close&quot;).addEventListener(&quot;click&quot;, App.hideInfo);
    document.querySelectorAll(&quot;.cv4-pi-btn&quot;).forEach((btn) => {
      btn.addEventListener(&quot;click&quot;, (e) => {
        e.stopPropagation();
        const key = btn.dataset.pi;
        const box = $(&quot;pi-&quot; + key);
        if (!box) return;
        if (!box.textContent &amp;&amp; App.PARAM_INFO[key]) box.textContent = App.PARAM_INFO[key];
        const wasOpen = box.classList.contains(&quot;open&quot;);
        document.querySelectorAll(&quot;.cv4-param-info.open&quot;).forEach((x) => x.classList.remove(&quot;open&quot;));
        if (!wasOpen) box.classList.add(&quot;open&quot;);
      });
    });
    E5.btnPrePp.addEventListener(&quot;click&quot;, () => {
      App.setMode(false);
      App.resetLHC();
      E5.sliEnergy.value = 6.8;
      s4.paramEnergy = 6.8;
      E5.lblEnergy.innerText = &quot;6.8 TeV&quot;;
      E5.sliIntensity.value = 1.4;
      s4.paramIntensity = 1.4;
      E5.lblIntensity.innerText = &quot;1.40e11 p&quot;;
      E5.sliBeta.value = 0.3;
      s4.paramBetaStar = 0.3;
      E5.lblBeta.innerText = &quot;0.30 m&quot;;
      E5.sliRampSpeed.value = 0.05;
      s4.paramRampSpeed = 0.05;
      E5.lblRampSpeed.innerText = &quot;0.05 T/s (Sicher)&quot;;
      E5.lblRampSpeed.style.color = &quot;#58a6ff&quot;;
      App.updateReadouts();
      selectDetector(&quot;CMS&quot;);
      App.setStatus(&quot;PRESET: Protonen-Physik (Run 3 \xB7 13.6 TeV) \u2014 Higgs (CMS), Z\u2070 (ATLAS) &amp; CP (LHCb) laufen GLEICHZEITIG auf diesem Strahl (Tab wechseln zeigt jeden Stand). Spektren: echte CMS-Open-Data \u2014 \u03BC\u03BC (Record 545) UND die 278 echten 4\u2113-Higgs-Kandidaten (Record 5200).&quot;, &quot;on&quot;);
    });
    E5.btnPreQgp.addEventListener(&quot;click&quot;, () => {
      App.setMode(true);
      App.resetLHC();
      E5.sliEnergy.value = 2.7;
      s4.paramEnergy = 2.7;
      E5.lblEnergy.innerText = &quot;2.70 TeV/u&quot;;
      E5.sliIntensity.value = 0.9;
      s4.paramIntensity = 0.9;
      E5.lblIntensity.innerText = &quot;0.90e11 p&quot;;
      E5.sliBeta.value = 0.5;
      s4.paramBetaStar = 0.5;
      E5.lblBeta.innerText = &quot;0.50 m&quot;;
      E5.sliRampSpeed.value = 0.05;
      s4.paramRampSpeed = 0.05;
      E5.lblRampSpeed.innerText = &quot;0.05 T/s (Sicher)&quot;;
      E5.lblRampSpeed.style.color = &quot;#58a6ff&quot;;
      App.updateReadouts();
      selectDetector(&quot;ALICE&quot;);
      App.setStatus(&quot;PRESET: Schwerionen (Pb-Pb \xB7 2.7 TeV/u, \u221As_NN=5.36 TeV) \u2192 ALICE: J/\u03C8-QGP-Unterdr\xFCckung \xB7 CMS: \u03A5-Sequenzunterdr\xFCckung \xB7 ATLAS: Z\u2070-Standardkerze \xB7 LHCb spezialisiert. Massen echt (CMS-p-p), QGP-Unterdr\xFCckung modelliert.&quot;, &quot;on&quot;);
    });
    E5.btnPrePilot.addEventListener(&quot;click&quot;, () => {
      App.setMode(false);
      App.resetLHC();
      E5.sliEnergy.value = 0.45;
      s4.paramEnergy = 0.45;
      E5.lblEnergy.innerText = &quot;0.45 TeV (Injektion)&quot;;
      E5.sliIntensity.value = 0.1;
      s4.paramIntensity = 0.1;
      E5.lblIntensity.innerText = &quot;0.10e11 p&quot;;
      E5.sliBeta.value = 1.5;
      s4.paramBetaStar = 1.5;
      E5.lblBeta.innerText = &quot;1.50 m&quot;;
      E5.sliRampSpeed.value = 0.02;
      s4.paramRampSpeed = 0.02;
      E5.lblRampSpeed.innerText = &quot;0.02 T/s (Sicher)&quot;;
      E5.lblRampSpeed.style.color = &quot;#58a6ff&quot;;
      App.updateReadouts();
      selectDetector(&quot;ATLAS&quot;);
      App.setStatus(&quot;PRESET GELADEN: Pilot-Strahl (Inbetriebnahme \xB7 0.45 TeV \u2014 zu wenig Energie f\xFCr Entdeckungen)&quot;, &quot;on&quot;);
    });
    E5.btnAutoColl.addEventListener(&quot;click&quot;, App.toggleAutoCollide);
    E5.btnAuto.addEventListener(&quot;click&quot;, fuellProtokoll);
    E5.sliEnergy.addEventListener(&quot;input&quot;, () => {
      s4.paramEnergy = parseFloat(E5.sliEnergy.value);
      E5.lblEnergy.innerText = App.fmtEnergy(s4.paramEnergy);
      App.updateReadouts();
      App.drawHist();
    });
    E5.sliIntensity.addEventListener(&quot;input&quot;, () => {
      s4.paramIntensity = parseFloat(E5.sliIntensity.value);
      E5.lblIntensity.innerText = s4.paramIntensity.toFixed(2) + &quot;e11 p&quot;;
    });
    E5.sliBeta.addEventListener(&quot;input&quot;, () => {
      E5.lblBeta.innerText = parseFloat(E5.sliBeta.value).toFixed(2) + &quot; m&quot;;
    });
    E5.sliRampSpeed.addEventListener(&quot;input&quot;, () => {
      s4.paramRampSpeed = parseFloat(E5.sliRampSpeed.value);
      if (s4.paramRampSpeed > 0.1) {
        E5.lblRampSpeed.innerText = s4.paramRampSpeed.toFixed(2) + &quot; T/s (\u26A0\uFE0F RISIKO)&quot;;
        E5.lblRampSpeed.style.color = &quot;#f85149&quot;;
      } else {
        E5.lblRampSpeed.innerText = s4.paramRampSpeed.toFixed(2) + &quot; T/s (Sicher)&quot;;
        E5.lblRampSpeed.style.color = &quot;#58a6ff&quot;;
      }
    });
  }

  // cern/app/src/main.js
  function initDom() {
    const E6 = App.els, g2 = App.g, s5 = App.state;
    E6.sdot = $(&quot;sdot&quot;);
    E6.stxt = $(&quot;stxt&quot;);
    E6.btnRamp = $(&quot;btn-ramp&quot;);
    E6.btnColl = $(&quot;btn-coll&quot;);
    E6.btnAuto = $(&quot;btn-auto&quot;);
    E6.btnSqueeze = $(&quot;btn-squeeze&quot;);
    E6.btnAutoColl = $(&quot;btn-autocoll&quot;);
    E6.btnSpeedToggle = $(&quot;btn-speed-toggle&quot;);
    E6.b1c = $(&quot;b1c&quot;);
    E6.b2c = $(&quot;b2c&quot;);
    E6.b1bar = $(&quot;b1bar&quot;);
    E6.b2bar = $(&quot;b2bar&quot;);
    E6.rbar = $(&quot;rbar&quot;);
    E6.vE = $(&quot;v-e&quot;);
    E6.vB = $(&quot;v-b&quot;);
    E6.vG = $(&quot;v-g&quot;);
    E6.vT = $(&quot;v-t&quot;);
    E6.spInfo = $(&quot;sp-info&quot;);
    E6.sliEnergy = $(&quot;sli-energy&quot;);
    E6.sliIntensity = $(&quot;sli-intensity&quot;);
    E6.sliBeta = $(&quot;sli-beta&quot;);
    E6.sliRampSpeed = $(&quot;sli-rampspeed&quot;);
    E6.lblEnergy = $(&quot;lbl-energy&quot;);
    E6.lblIntensity = $(&quot;lbl-intensity&quot;);
    E6.lblBeta = $(&quot;lbl-beta&quot;);
    E6.lblRampSpeed = $(&quot;lbl-rampspeed&quot;);
    E6.trInj = $(&quot;tr-inj&quot;);
    E6.selP = $(&quot;sel-p&quot;);
    E6.selI = $(&quot;sel-i&quot;);
    E6.btnToggleGeo = $(&quot;btn-toggle-geo&quot;);
    E6.btnPrePp = $(&quot;btn-pre-pp&quot;);
    E6.btnPreQgp = $(&quot;btn-pre-qgp&quot;);
    E6.btnPrePilot = $(&quot;btn-pre-pilot&quot;);
    E6.btnZoomOut = $(&quot;btn-zoom-out&quot;);
    E6.btnZoomMeyrin = $(&quot;btn-zoom-meyrin&quot;);
    E6.btnDiagramFull = $(&quot;btn-diagram-full&quot;);
    E6.root = $(&quot;cern-v4&quot;);
    E6.grpAtlas = $(&quot;grp-atlas&quot;);
    E6.grpCms = $(&quot;grp-cms&quot;);
    E6.grpAlice = $(&quot;grp-alice&quot;);
    E6.grpLhcb = $(&quot;grp-lhcb&quot;);
    E6.svg = $(&quot;svg&quot;);
    E6.geoLayer = $(&quot;geo-layer&quot;);
    E6.schematic = $(&quot;schematic&quot;);
    g2.trSteps = [&quot;tr-src&quot;, &quot;tr-inj&quot;, &quot;tr-ps&quot;, &quot;tr-sps&quot;, &quot;tr-lhc&quot;].map($);
    g2.paths = {
      linac4: $(&quot;p-linac4&quot;),
      psb: $(&quot;p-psb&quot;),
      psbPs: $(&quot;p-psb-ps&quot;),
      linac3: $(&quot;p-linac3&quot;),
      leir: $(&quot;p-leir&quot;),
      leirPs: $(&quot;p-leir-ps&quot;),
      ps: $(&quot;p-ps&quot;),
      psSps: $(&quot;p-ps-sps&quot;),
      sps: $(&quot;p-sps&quot;),
      ti2: $(&quot;p-ti2&quot;),
      ti8: $(&quot;p-ti8&quot;),
      lhc: $(&quot;p-lhc&quot;)
    };
    g2.nodes = {
      linac4: $(&quot;n-linac4&quot;),
      psb: $(&quot;n-psb&quot;),
      linac3: $(&quot;n-linac3&quot;),
      leir: $(&quot;n-leir&quot;),
      ps: $(&quot;n-ps&quot;),
      sps: $(&quot;n-sps&quot;),
      atlas: $(&quot;d-atlas&quot;),
      cms: $(&quot;d-cms&quot;),
      alice: $(&quot;d-alice&quot;),
      lhcb: $(&quot;d-lhcb&quot;)
    };
    E6.cvEv = $(&quot;cv-ev&quot;);
    E6.ctxEv = E6.cvEv.getContext(&quot;2d&quot;);
    E6.cvHist = $(&quot;cv-hist&quot;);
    E6.ctxHist = E6.cvHist.getContext(&quot;2d&quot;);
    s5.dpr = window.devicePixelRatio || 1;
  }
  function start() {
    initDom();
    wireEngine();
    wireHandlers();
    App.drawGeo();
    App.setViewMode(false);
    App.resizeCanvases();
    App.updateReadouts();
    App.drawDetBg();
    App.drawHist();
    App.setStatus(&quot;BEREIT \u2014 W\xE4hle Teilchenart und starte Injektion&quot;, &quot;on&quot;);
    const redraw = () => {
      App.resizeCanvases();
      App.state.lastEvent ? App.drawCollisionEvent(App.state.lastEvent) : App.drawDetBg();
      App.drawHist();
    };
    if (typeof ResizeObserver !== &quot;undefined&quot;) {
      const ro = new ResizeObserver(redraw);
      ro.observe(App.els.cvEv);
      ro.observe(App.els.cvHist);
    } else {
      window.addEventListener(&quot;resize&quot;, redraw);
    }
  }
  function ready() {
    return document.getElementById(&quot;cern-v4&quot;) &amp;&amp; document.getElementById(&quot;svg&quot;) &amp;&amp; document.getElementById(&quot;btn-auto&quot;);
  }
  function boot() {
    const root = document.getElementById(&quot;cern-v4&quot;);
    if (!root || root.__cernBooted || !ready()) return !!(root &amp;&amp; root.__cernBooted);
    root.__cernBooted = true;
    try {
      start();
    } catch (e) {
      try {
        console.error(&quot;[CERN-Widget] Init fehlgeschlagen:&quot;, e);
      } catch (_) {
      }
    }
    return true;
  }
  if (!boot()) {
    let n = 0;
    const iv = setInterval(() => {
      if (boot() || ++n > 200) clearInterval(iv);
    }, 25);
    if (document.readyState === &quot;loading&quot;) {
      document.addEventListener(&quot;DOMContentLoaded&quot;, boot);
    }
  }
})();
</script><script>(function(){function r(){try{var h=Math.ceil(document.getElementById('cern-v4')?document.getElementById('cern-v4').getBoundingClientRect().height:document.documentElement.scrollHeight);parent.postMessage({cernV4Height:h},'*');}catch(e){}}window.addEventListener('load',r);setTimeout(r,250);setTimeout(r,1200);if(window.ResizeObserver){new ResizeObserver(r).observe(document.body);}})();</script></body></html>"></iframe><script>(function(){var f=document.getElementById('cern-v4-frame');if(!f)return;window.addEventListener('message',function(e){if(e.source===f.contentWindow&&e.data&&e.data.cernV4Height){f.style.height=(e.data.cernV4Height+6)+'px';}});})();</script>'''))



# %% [markdown]
# ---
# ## Teil 2 · Von Rohdaten zur Masse
#
# > **Lernziel:** Aus den *gemessenen Impulsen* zweier Myonen die **invariante Masse** ihres
# > Mutterteilchens berechnen — die Brücke von der Messung zur Physik.
#
# Ein Detektor misst nicht „Teilchen", sondern **Spuren**: aus der Krümmung im Magnetfeld folgt der
# **Impuls** p⃗ und die **Ladung** Q. Weil wir wissen, dass es Myonen sind (Masse $m_\mu = 0{,}10566$ GeV),
# rekonstruieren wir ihre Energie relativistisch:
#
# $$E = \sqrt{p^2 + m_\mu^2}\,.$$
#
# Stammen beide Myonen aus dem Zerfall **eines** kurzlebigen Teilchens, so verrät dessen Masse sich über die
# **invariante Masse** des Paares — eine Lorentz-Invariante (in jedem Bezugssystem gleich):
#
# $$M^2 = \left(E_1 + E_2\right)^2 - \left|\vec p_1 + \vec p_2\right|^2\,.$$
#
# So „sehen" wir Teilchen, die nach $10^{-20}\,$s längst zerfallen sind. Wir rechnen es selbst und prüfen
# gegen die offizielle CMS-Massenspalte.

# %%
cu.apply_cern_style()
m_mu = cu.M_MYON   # Myonmasse = 0.105658 GeV/c²

# Energie aus dem gemessenen Impuls rekonstruieren: E = sqrt(p^2 + m^2)
def energie(px, py, pz, m): return np.sqrt(px**2 + py**2 + pz**2 + m**2)
E1 = energie(EV['px1'], EV['py1'], EV['pz1'], m_mu)
E2 = energie(EV['px2'], EV['py2'], EV['pz2'], m_mu)

# Invariante Masse:  M^2 = (E1+E2)^2 - |p1+p2|^2
E_sum  = E1 + E2
px_sum = EV['px1'] + EV['px2']
py_sum = EV['py1'] + EV['py2']
pz_sum = EV['pz1'] + EV['pz2']
MASSEN = np.sqrt(np.maximum(E_sum**2 - (px_sum**2 + py_sum**2 + pz_sum**2), 0.0))

# Ein konkretes Ereignis Schritt für Schritt
i = 4
print(f"Ereignis #{i}: zwei Myonen, entgegengesetzte Ladung (Q1={EV['Q1'][i]:+d}, Q2={EV['Q2'][i]:+d})")
print(f"  μ1: p=({EV['px1'][i]:7.2f},{EV['py1'][i]:7.2f},{EV['pz1'][i]:7.2f}) GeV  ->  E1 = {E1[i]:6.2f} GeV")
print(f"  μ2: p=({EV['px2'][i]:7.2f},{EV['py2'][i]:7.2f},{EV['pz2'][i]:7.2f}) GeV  ->  E2 = {E2[i]:6.2f} GeV")
print(f"  => invariante Masse M = {MASSEN[i]:.3f} GeV")

# Verifikation gegen die offizielle CMS-Massenspalte
resid = np.abs(MASSEN - EV['M'])
print(f"\n✅ Über alle {MASSEN.size:,} Ereignisse: Median-Abweichung {np.median(resid):.1e} GeV, "
      f"max {resid.max():.1e} GeV")
print("   -> Unsere Kinematik reproduziert die CMS-Massen (Restabweichung = CSV-Rundung).")

# Kontrollplot: selbst berechnet vs. CMS — muss auf der Diagonale liegen
fig, ax = plt.subplots(figsize=(6.6, 6.6))
ax.scatter(EV['M'], MASSEN, s=2, alpha=.20, color='#58a6ff')
ax.plot([0, 120], [0, 120], color='#f85149', lw=1.3, ls='--', label='M(selbst) = M(CMS)')
ax.set_xlabel('CMS-Massenspalte M [GeV]'); ax.set_ylabel('Selbst berechnete Masse [GeV]')
ax.set_title('Von Rohimpulsen zur Masse', color='#58a6ff', fontweight='bold')
ax.set_xlim(0, 120); ax.set_ylim(0, 120); ax.legend(loc='upper left')
plt.tight_layout(); plt.show()

# %% [markdown]
# ---
# ## Teil 3 · Das Massenspektrum — die Teilchen-Leiter
#
# > **Lernziel:** Erkennen, dass ein Histogramm aller invarianten Massen die bekannten Teilchen als
# > **Resonanz-Peaks** offenbart — ein „Periodensystem" der Dimuon-Resonanzen.
#
# Wir tragen **alle** selbst berechneten Massen in ein Histogramm ein. Weil sowohl die Massen (0,3–120 GeV)
# als auch die Häufigkeiten über viele Größenordnungen reichen, nutzen wir eine **doppelt-logarithmische**
# Darstellung. Jeder Buckel ist ein eigenes Teilchen, das in zwei Myonen zerfällt. Dieser eine Datensatz
# enthält jahrzehntelange Entdeckungsgeschichte.

# %%
cu.apply_cern_style()
if 'MASSEN' not in globals():
    MASSEN = cu.dimuon_invariante_masse(EV)

fig, ax = plt.subplots(figsize=(13, 7))
m = MASSEN[(MASSEN > 0.25) & (MASSEN < 120)]
bins = np.logspace(np.log10(0.25), np.log10(120), 180)
ax.hist(m, bins=bins, color='#58a6ff', alpha=.85, edgecolor='none')
ax.set_xscale('log'); ax.set_yscale('log')

labels = {'rho/omega': 'ρ/ω', 'phi': 'φ', 'J/psi': 'J/ψ', 'psi(2S)': 'ψ(2S)',
          'Upsilon1S': 'Υ(1S)', 'Upsilon2S': 'Υ(2S)', 'Upsilon3S': 'Υ(3S)', 'Z0': 'Z⁰'}
ymax = ax.get_ylim()[1]
for name, r in cu.RESONANZEN.items():
    if r['kanal'] != 'μ⁺μ⁻' or not (0.25 < r['m'] < 120):
        continue
    ax.axvline(r['m'], color=r['farbe'], ls='--', lw=1, alpha=.55)
    ax.text(r['m'], ymax*0.5, ' ' + labels.get(name, name), rotation=90,
            color=r['farbe'], fontsize=9.5, va='top', ha='center', fontweight='bold')

ax.set_xlabel('Invariante Dimuon-Masse  m(μ⁺μ⁻)  [GeV]')
ax.set_ylabel('Ereignisse pro Bin')
ax.set_title('Das Dimuon-Massenspektrum — eine Leiter aus Teilchen (echte CMS-Daten, 7 TeV)',
             color='#58a6ff', fontweight='bold')
ax.set_xlim(0.25, 120)
ticks = [0.5, 1, 2, 3, 5, 10, 20, 50, 100]
ax.set_xticks(ticks); ax.set_xticklabels([str(t) for t in ticks])
plt.tight_layout(); plt.show()
print("Von ρ/ω (0.78 GeV) über J/ψ, ψ(2S), das Υ-Triplett bis zum Z⁰ (91 GeV) — alles in EINEM Datensatz.")
print("Das Higgs fehlt hier bewusst: H→μμ ist extrem selten — der echte Entdeckungskanal kommt in Teil 5.")

# %% [markdown]
# ---
# ## Teil 4 · Eine Resonanz vermessen
#
# > **Lernziel:** Eine Resonanz durch **Kurvenanpassung** quantitativ vermessen — Masse und Auflösung
# > mit Unsicherheit bestimmen und gegen den Literaturwert (PDG) prüfen.
#
# Wir zoomen auf **eine** Resonanz und passen ein physikalisch motiviertes Modell an:
#
# - **Signal:** ein **Voigt-Profil** = Faltung aus der natürlichen Breite Γ (Breit-Wigner, durch die
#   Lebensdauer via $\tau=\hbar/\Gamma$ bestimmt) und der **Detektorauflösung** σ (Gauß).
# - **Untergrund:** lokal linear.
#
# Γ ist aus dem PDG bekannt und wird **fest** vorgegeben — so *messen* wir die Masse μ und die
# Auflösung σ. Wechsle `RESONANZ`, um z. B. das scharfe J/ψ mit dem breiten Z⁰ zu vergleichen.

# %%
from scipy.optimize import curve_fit
from scipy.special import voigt_profile
cu.apply_cern_style()
if 'MASSEN' not in globals():
    MASSEN = cu.dimuon_invariante_masse(EV)

# Wählbar: "J/psi", "psi(2S)", "Upsilon1S", "Z0", "phi", "rho/omega"
RESONANZ = "J/psi"

# Echte natürliche Breiten Γ (PDG, aus physics.json/RESONANZEN) — NICHT die Detektorauflösung!
GAMMA_NAT = {name: r['breite'] for name, r in cu.RESONANZEN.items()}
m0 = cu.RESONANZEN[RESONANZ]['m']; farbe = cu.RESONANZEN[RESONANZ]['farbe']
gamma = GAMMA_NAT[RESONANZ]

halb = max(0.5, 12 * max(gamma, 0.04*m0))           # Fensterbreite
lo, hi = max(0.15, m0 - halb), m0 + halb
sel = MASSEN[(MASSEN >= lo) & (MASSEN <= hi)]
h, e = np.histogram(sel, bins=70, range=(lo, hi)); c = .5*(e[1:]+e[:-1])

def modell(x, A, mu, sigma, b0, b1):
    sigma = abs(sigma)
    peak  = A * voigt_profile(x - mu, sigma, gamma/2)
    unter = np.maximum(b0 + b1*(x - m0), 0)
    return peak + unter

p0   = [h.max()*(0.04*m0 + gamma), m0, max(0.02, 0.012*m0), np.median(h), 0.0]
bnds = ([0, m0-halb/2, 0.004, 0, -np.inf], [np.inf, m0+halb/2, halb, np.inf, np.inf])
p, pc = curve_fit(modell, c, h, p0=p0, bounds=bnds, maxfev=40000)
perr = np.sqrt(np.diag(pc))
m_fit, m_err, sig_fit = p[1], perr[1], abs(p[2])

fig, ax = plt.subplots(figsize=(12, 7))
ax.errorbar(c, h, yerr=np.sqrt(np.maximum(h, 1)), fmt='o', color='#8b949e', ms=4,
            label=f'CMS-Daten (n={sel.size})')
xf = np.linspace(lo, hi, 800)
ax.plot(xf, modell(xf, *p), color=farbe, lw=2.5, label='Voigt-Fit + Untergrund')
ax.axvline(m0, color='#2ea44f', ls=':', lw=1.5, label=f'PDG: {m0:.4g} GeV')
ax.set_xlabel('Invariante Masse [GeV]'); ax.set_ylabel('Ereignisse')
ax.set_title(f'Resonanz vermessen: {RESONANZ}', color=farbe, fontweight='bold')
rel  = (m_fit - m0)/m0*100                         # relative Abweichung [%]
txt = (f'Gemessen:  M = {m_fit:.4g} ± {m_err:.2g} GeV\n'
       f'PDG-Wert:  M = {m0:.4g} GeV   (Δ = {rel:+.2f} %)\n'
       f'Detektorauflösung σ ≈ {sig_fit*1000:.0f} MeV\n'
       f'natürliche Breite Γ = {gamma*1000:.3g} MeV (PDG, fix)')
ax.text(.03, .97, txt, transform=ax.transAxes, va='top', fontsize=10.5,
        bbox=dict(boxstyle='round', fc='#161b22', ec=farbe, alpha=.9), color='#fff')
ax.legend(loc='upper right', framealpha=.85)
plt.tight_layout(); plt.show()

hbar = 6.582e-25  # GeV·s
print(f"Lebensdauer aus der natürlichen Breite:  τ = ħ/Γ = {hbar/gamma:.2e} s")
pull = abs(m_fit - m0)/m_err if m_err > 0 else float('nan')
print(f"Hinweis: der statistische Fehler ist nur ±{m_err*1000:.1f} MeV. Bei so viel Statistik dominieren\n"
      f"systematische Effekte (Binning, Kalibrierung, Strahlungsschwänze) den {pull:.0f}σ-Pull — die Masse\n"
      f"selbst stimmt auf {abs(rel):.2f}% mit dem PDG-Wert überein.")

# %% [markdown]
# ---
# ## Teil 5 · Entdeckung & Signifikanz
#
# > **Lernziel:** Quantifizieren, *wann* ein Peak eine **Entdeckung** ist — über die statistische
# > Signifikanz und das **5σ-Kriterium** — und verstehen, warum mehr Daten (Luminosität) entscheidend sind.
#
# Ein Buckel ist erst dann eine Entdeckung, wenn er **nicht** als zufällige Untergrund-Fluktuation erklärbar
# ist. Eine einfache, gängige Kennzahl ist
#
# $$Z \approx \frac{S}{\sqrt{B}}\,,$$
#
# mit Signalzahl $S$ und Untergrund $B$ unter dem Peak (aus den **Seitenbändern** geschätzt). Die Konvention
# der Teilchenphysik: **5σ** (Wahrscheinlichkeit einer Fluktuation ≈ 1 zu 3,5 Mio.) = *Entdeckung*, 3σ =
# *Hinweis*. Weil $S\propto N$ und $B\propto N$ wächst, gilt $Z\propto\sqrt{N}$ — **mehr Statistik schärft das
# Signal**. Genau deshalb brauchte das seltene **Higgs** (Goldkanal H→ZZ\*→4ℓ) Jahre an Daten bis zur
# Entdeckung am **4. Juli 2012**.

# %%
cu.apply_cern_style()
if 'MASSEN' not in globals():
    MASSEN = cu.dimuon_invariante_masse(EV)

# --- (A) Signifikanz des Z⁰-Peaks DIREKT aus den Daten ---
m0 = cu.RESONANZEN['Z0']['m']
sig_region = (m0 - 6, m0 + 6)                       # Signalfenster
seiten     = [(m0 - 18, m0 - 8), (m0 + 8, m0 + 18)] # Seitenbänder (reiner Untergrund)
zähle = lambda a, lo, hi: int(np.sum((a >= lo) & (a < hi)))

def signifikanz(massen):
    n_sr = zähle(massen, *sig_region)
    b_cts = sum(zähle(massen, a, b) for a, b in seiten)
    b_wid = sum(b - a for a, b in seiten)
    B = b_cts * (sig_region[1] - sig_region[0]) / b_wid   # Untergrund auf Signalbreite skaliert
    S = max(n_sr - B, 0.0)
    return S, B, (S/np.sqrt(B) if B > 0 else 0.0)

S, B, Z = signifikanz(MASSEN)
print(f"Z⁰-Fenster {sig_region} GeV:  S ≈ {S:.0f} Signal,  B ≈ {B:.0f} Untergrund  ->  Z = S/√B = {Z:.1f}σ")

# √N-Gesetz: Signifikanz bei wachsender Statistik (Subsampling)
rng = np.random.default_rng(0)
frac = np.linspace(0.05, 1.0, 20)
Zf = np.array([signifikanz(MASSEN[rng.choice(MASSEN.size, int(f*MASSEN.size), replace=False)])[2]
               for f in frac])
Nv = frac * MASSEN.size

fig, (axA, axB) = plt.subplots(1, 2, figsize=(14, 6))
axA.scatter(Nv, Zf, color='#58a6ff', s=28, zorder=3, label='Z⁰-Signifikanz (Subsample)')
k = np.sum(Zf*np.sqrt(Nv))/np.sum(Nv)                 # Ursprungsgerade Z = k·√N
axA.plot(Nv, k*np.sqrt(Nv), color='#f85149', lw=2, label='Z = k·√N  (Fit)')
axA.axhline(5, color='#2ea44f', ls='--', lw=1.2, label='5σ – Entdeckung')
axA.set_xlabel('N  (Anzahl Ereignisse)'); axA.set_ylabel('Signifikanz Z [σ]')
axA.set_title('Das √N-Gesetz: mehr Daten → mehr Signifikanz', color='#58a6ff', fontweight='bold')
axA.legend(loc='upper left', framealpha=.85)

# --- (B) Der echte Entdeckungskanal: Higgs → ZZ* → 4ℓ (ATLAS-kalibrierte Simulation) ---
m4l, info4 = cu.lade_higgs_4l()
h4, e4 = np.histogram(m4l, bins=42, range=(80, 200)); c4 = .5*(e4[1:]+e4[:-1])
axB.bar(c4, h4, width=(e4[1]-e4[0]), color='#30363d', edgecolor='#aec7e8', lw=.5,
        label='4-Lepton-Ereignisse')
axB.axvline(125, color='#2ea44f', ls='--', lw=1.5, label='Higgs (125 GeV)')
disc = cu.HISTORIE['discovery']
axB.annotate(f"{disc['datum']}\n{disc['text']}", xy=(125, h4.max()*0.92),
             xytext=(150, h4.max()*0.78), color='#2ea44f', fontsize=9,
             arrowprops=dict(arrowstyle='->', color='#2ea44f'))
axB.set_xlabel('4-Lepton-Masse  m(4ℓ)  [GeV]'); axB.set_ylabel('Ereignisse')
axB.set_title('Goldkanal H→ZZ*→4ℓ — kleines Signal, viel Untergrund', color='#aec7e8', fontweight='bold')
axB.legend(loc='upper right', framealpha=.85)
axB.text(.5, -.16, info4['quelle'], transform=axB.transAxes, ha='center', fontsize=7.5, color='#8b949e')
plt.tight_layout(); plt.show()

print(f"\nDas Z⁰ ist mit {Z:.0f}σ ein müheloses Signal. Das Higgs dagegen liefert nur ~{info4['n_signal']} "
      f"Signal-Ereignisse auf großem Untergrund — erst genug Luminosität brachte 2012 die 5σ.")

# %% [markdown]
# ---
# ## Teil 6 · Maschinenphysik & Reichweite
#
# > **Lernziel:** Quantifizieren, warum **höhere Energie schwerere Teilchen** zugänglich macht — und warum
# > das Dipolfeld die LHC-Energie begrenzt.
#
# Um ein Teilchen der Masse $M$ zu erzeugen, muss die **Schwerpunktsenergie** $\sqrt{s}$ mindestens $M$
# betragen (notwendige Bedingung). Bei zwei gegenläufigen Strahlen der Energie $E$ gilt $\sqrt{s}=2E$.
# Gehalten werden die Teilchen von Dipolmagneten:
#
# $$B = \frac{p}{0{,}3\,\rho}\,,$$
#
# mit Krümmungsradius $\rho\approx 2804\,$m. Die supraleitenden Dipole quenchen oberhalb von **8,33 T** — das
# deckelt die LHC-Energie bei **7 TeV** pro Strahl. Für **Blei-Ionen** (Ladung $Z{=}82$, Massenzahl $A{=}208$)
# skaliert das nötige Feld mit $A/Z$, und der Lorentz-Faktor wird **pro Nukleon** gerechnet,
# $\gamma = E_\text{Nukleon}/m_N$.

# %%
cu.apply_cern_style()
rho   = 2803.95                 # Krümmungsradius der LHC-Dipole [m]
k     = 0.299792458 * rho       # Rigiditäts-Faktor: B = p / k
B_max = 8.33                    # Quench-Grenze der supraleitenden Dipole [T]

E = np.linspace(0.45, 7.0, 200) * 1000   # Strahlenergie pro Strahl [GeV] (p ≈ E bei v≈c)
B_p = E / k

fig, (axL, axR) = plt.subplots(1, 2, figsize=(14, 6))
# Links: Dipolfeld vs. Energie — warum 7 TeV das Limit ist
axL.plot(E/1000, B_p, color='#58a6ff', lw=2.5, label='Protonen:  B = p/(0.3·ρ)')
axL.axhline(B_max, color='#f85149', ls='--', lw=1.5, label=f'Quench-Grenze {B_max} T')
axL.axvline(7.0, color='#2ea44f', ls=':', lw=1.4, label='LHC-Maximum 7 TeV')
axL.set_xlabel('Strahlenergie pro Strahl [TeV]'); axL.set_ylabel('benötigtes Dipolfeld B [T]')
axL.set_title('Warum 7 TeV das Limit ist', color='#58a6ff', fontweight='bold')
axL.legend(loc='upper left', framealpha=.85)

# Rechts: Schwerpunktsenergie √s = 2E setzt die Massen-Reichweite
axR.plot(E/1000, 2*E, color='#58a6ff', lw=2.5, label='√s = 2·E (erreichbare Massenobergrenze)')
for name, r in cu.RESONANZEN.items():
    axR.axhline(r['m'], color=r['farbe'], ls='--', lw=.8, alpha=.6)
    axR.text(7.02, r['m'], name.replace('Upsilon', 'Υ').replace('psi', 'ψ'),
             color=r['farbe'], fontsize=7, va='center')
axR.set_yscale('log'); axR.set_xlim(0.45, 7.0)
axR.set_xlabel('Strahlenergie pro Strahl [TeV]'); axR.set_ylabel('Energie / Masse [GeV]')
axR.set_title('Energie bestimmt die Reichweite (√s ≥ M nötig)', color='#58a6ff', fontweight='bold')
axR.legend(loc='lower right', framealpha=.85)
plt.tight_layout(); plt.show()

print("Blei-Ionen (Pb⁸²⁺, A=208):")
for E_n in [0.177, 2.56]:
    Eg = E_n*1000; B = (208/82)*Eg/k; g = Eg/0.9315
    print(f"  @ {E_n:5.3f} TeV/u:  B = {B:5.2f} T   γ = {g:>6,.0f}")
print(f"  Die 2.56-TeV/u-Obergrenze entspricht genau dem {B_max}-T-Quench-Limit der Dipole.")

# %% [markdown]
# ---
# ## Teil 7 · Zusammenfassung & Übungen
#
# Du hast den vollständigen Weg der experimentellen Teilchenphysik durchlaufen:
#
# 1. **Die Maschine** — Beschleunigung, Speicherung und Kollision im LHC (Stellwerk).
# 2. **Rohdaten → Masse** — invariante Masse aus gemessenen Impulsen ($M^2=(\sum E)^2-|\sum\vec p|^2$).
# 3. **Das Spektrum** — die Resonanz-Leiter von ρ/ω bis Z⁰ in echten CMS-Daten.
# 4. **Resonanz vermessen** — Voigt-Fit, Masse & Auflösung vs. PDG, Lebensdauer aus der Breite.
# 5. **Signifikanz** — $Z=S/\sqrt B$, das √N-Gesetz und das 5σ-Kriterium (Higgs, 4. Juli 2012).
# 6. **Maschinenphysik** — $\sqrt s=2E$, das 8,33-T-Limit und die Massen-Reichweite.
#
# ### 🧩 Übungen für den Begabtenkurs
# 1. **Υ-Triplett auflösen:** Setze in Teil 4 `RESONANZ="Upsilon1S"` und vergrößere das Fenster. Kannst du
#    Υ(1S/2S/3S) trennen? Welche **Detektorauflösung** σ wäre dafür nötig (Abstand der Zustände ≈ 0,56 GeV)?
# 2. **Lebensdauer des Z⁰:** Bestimme aus Γ(Z⁰)=2,495 GeV die Lebensdauer $\tau=\hbar/\Gamma$. Vergleiche
#    mit dem J/ψ — warum ist das eine so viel „schärfer" als das andere?
# 3. **Wie viel Statistik für 5σ?** Wenn ein Signal anfänglich nur $Z=1{,}2\sigma$ liefert: um welchen Faktor
#    muss die Datenmenge $N$ wachsen, um 5σ zu erreichen? (√N-Gesetz)
# 4. **Volle Statistik:** Setze in Teil 1 `LADE_VOLLEN_DATENSATZ=True`, lade den vollen CMS-Datensatz und
#    wiederhole Teil 3–5. Wie verändern sich Peaks und Signifikanz?
# 5. **Warum kein Higgs im Dimuon-Spektrum?** Recherchiere das Verzweigungsverhältnis von H→μμ (~0,02 %) und
#    schätze, wie viele Ereignisse man bräuchte, um es im Spektrum aus Teil 3 zu sehen.
# 6. **Collider-Design:** Welche Strahlenergie pro Strahl bräuchte man, um ein hypothetisches Teilchen von
#    1 TeV zu erzeugen? Welches Dipolfeld wäre bei gleichem Radius $\rho$ nötig?
#
# > **Ausblick:** Dieselben Methoden — invariante Masse, Spektren, Fits, Signifikanz — tragen von hier bis zur
# > Forschungsfront: zu Präzisionsmessungen, der Suche nach Dunkler Materie und neuer Physik jenseits des
# > Standardmodells.

# %%
