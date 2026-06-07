# 🧭 MIGRATION — App-First-Architektur (autoritativer, fortsetzbarer Plan)

> **Dies ist die Single Source of Truth für den laufenden Umbau.**
> Jeder Agent liest zuerst den Abschnitt **STATUS / RESUME HERE**, arbeitet die nächste
> offene Phase ab, hakt sie ab und committet diese Datei mit. Der Chat darf jederzeit
> wegen Kontextlänge gecleart werden — der Plan lebt hier, nicht im Chatverlauf.

---

## 🟢 STATUS / RESUME HERE

- **Aktive Phase:** Phase 4 (Curriculum-Visualisierungen → App-Komponenten) — **in Arbeit**
  (1. Komponente „Geo-Overlay" ✅; weitere offen).
- **Entscheidungen:** gelockt (siehe „Gelockte Entscheidungen"). Modul-Modell = **leichter Namespace** (`App`-Objekt).
- **Zuletzt erledigt (diese Session):**
  - **Injektor-Zoom (Meyrin) brauchbar gemacht** (Nutzer: „man erkennt nichts, müsste näher
    + feiner"). Drei Ursachen behoben in `geo.js`/`styles.css`: (1) **Zoom-Fenster enthielt das
    riesige SPS** → Cluster nur ein ~12px-Fleck. Jetzt rahmt `App.geoInjectorView` NUR den Cluster
    (LINAC4/PSB/PS/LEIR), aufs SVG-Seitenverhältnis gepolstert (`padToAspect`) → **~20× statt ~6×**.
    (2) **Strokes skalierten mit** → fette Klötze: `mk()` setzt jetzt `vector-effect:non-scaling-stroke`
    (Linien bleiben Bildschirm-px bei jedem Zoom). (3) **Labels explodierten** (PS/PSB 7px + ATLAS-IP
    8px, ~20×): accelLabels **und** IP-Detektor-Kreise/-Labels tragen jetzt Klasse `geo-far`
    → im Zoom ausgeblendet (`#svg.inj-zoom .geo-far{opacity:0}`); die Detail-Ebene liefert eigene
    feine, zoom-skalierte Labels (`FS = 13·view.w/700`). Headless 45 grün, `check.sh` grün; visuell
    bestätigt (Cluster mit PS-Ring/LEIR/LINAC3-4 klar lesbar, keine Riesen-Labels mehr).
  - **Injektor-Topologie/Maßstab korrigiert** (Folge-Feedback: „Formen überlappen, nicht richtig
    connected; sind die Größen akkurat?"). `drawInjector` nutzt jetzt echte Ring-Geometrie via
    `bboxC` (Mittelpunkt+Radius aus OSM-Punkten) und `edgePath` (Kante-zu-Kante statt Linien ins
    Zentrum). **Maßstab ehrlich:** PS/PSB/LINAC4 sind OSM → maßstäblich zueinander (PSB real 0,256× PS);
    **LEIR + LINAC3 ∉ OSM → schematisch (jetzt gestrichelt)**, LEIR auf realistische 0,15× PS
    verkleinert (vorher ~0,36×) und **außerhalb** des PS-Rings platziert (Lücke 0,6 → kein Überlapp).
    Klare Ketten: Protonen LINAC4→PSB→PS (blau, durchgezogen), Ionen LINAC3→LEIR→PS (pink, gestrichelt).
    Visuell bestätigt.
  - **Injektor maßstabsgenau + reale Formen** (Folge-Feedback: „Real-Ansicht muss perfekt nach
    Maßstab, richtige Formen/Radien — PSB z.B. 25 m"). Verifiziert: OSM ist exakt maßstäblich
    (PS RMS 101 m, **PSB 25,4 m**, SPS 1102 m — Overpass nachgemessen). **LEIR + LINAC3 in KEINER
    Geodatenquelle** (OSM-Name/-Tag, Nominatim, Wikidata-Koord. alle leer) → werden in `geo.js` aus
    dem OSM-abgeleiteten Maßstab `gpm = psC.r/101` (geo/Meter) gezeichnet: **LEIR = abgerundetes
    Rechteck 24×18 m** (Umfang ~77 m ≈ real 78,5 m; `roundedRectPath`), nicht mehr Kreis. Reale
    Verhältnisse erreicht: LEIR/PS 0,119 (real 0,120), PSB/PS 0,256 (0,250), LEIR/PSB 0,464 (0,480).
    ⚠ **LEIR/LINAC3-Position ist approximiert** (S-SW des PS, ∉ OSM → gestrichelt); Größe/Form/Maßstab
    real. Falls echte LEIR/LINAC3-Koordinaten auftauchen → in `geo_build.py` projizieren (wie LINAC4).
    Tests 45 grün, visuell bestätigt.
  - **Easter Egg: FCC (Future Circular Collider)** (Nutzerwunsch). In der Realen Ansicht ein
    versteckter Auslöser — dezenter **✦ im Genfersee** (`.fcc-trigger`, `pointer-events:auto` trotz
    `#geo-layer{pointer-events:none}`; nur sichtbar/aktiv in der Realen Ansicht). Klick →
    `handlers#revealFCC` (gated auf `realMode`): blendet `#svg.fcc-on .geo-fcc` ein und macht einen
    **dramatischen Heraus-Zoom** (`animateViewBox(..., 1700ms)`, ~2,8× heraus auf `App.geoFccView`).
    FCC **maßstäblich** gezeichnet (`geo.js#drawFCC`): R = LHC_R·(90,7/26,7) ≈ ×3,40 (real), Zentrum
    NE → LHC sitzt innen ~tangential am SW-Rand (real); Léman liegt im FCC-Areal. Labels „FCC …91 km"
    + Vergleich „LHC 27 · SPS 7 · FCC 91 km (×3,4)" (zoom-skalierte Schrift). `resetView` löscht
    `fcc-on` und zoomt zurück. Visuell bestätigt; Tests 45 grün.
  - **Canvas-Skalierungs-Bug behoben** (Event-Display + Histogramm): `resizeCanvases` schrieb die
    per `getBoundingClientRect` gemessene Pixelgröße als Inline-`style.width/height` zurück — lief das
    beim Boot (`readyState==="loading"`, Layout 0 breit), fror es eine falsche/überdimensionierte
    Größe ein und überschrieb das responsive CSS dauerhaft. Fix: Anzeigegröße bleibt CSS-gesteuert,
    nur Backing-Store = `clientWidth·dpr`, gekoppelt per **ResizeObserver** (`engine.js#fitCanvas`,
    `main.js#start`). Lehre → Memory `canvas-sizing-pitfall`.
  - **Massenspektrum-Engine überarbeitet (Ziel: max. logische Konsequenz):** Spektrum ist jetzt
    **strahlkonfigurations-getrieben** statt rein detektor-getrieben — hängt von ZWEI Achsen ab:
    (1) **Detektor** (Kanal/Fenster), (2) **Strahl-Programm/Preset**. `spectrum.js#DETSPEC` hat pro
    Detektor `beam` ("pp"/"PbPb") + `bg(v)` + `reson[]` mit Schwelle `thr` (TeV/Strahl), optional
    `pp:true` (nur mit Protonen erzeugbar) und `qgp:true` (im Ionen-Lauf unterdrückt).
    `energyVis/prodVis/drawVis`: Peak erscheint erst beim Hochrampen über die Schwelle (darunter nur
    Kontinuum); EW/B-Peaks (Z⁰/Higgs/B⁰) verschwinden im Ionen-Lauf; QGP unterdrückt Quarkonia.
    **`getSignificance` gated durch `beamMatches`** → Entdeckung nur im richtigen Programm (CMS-Higgs
    nur in pp, ALICE-QGP nur in Pb-Pb) — behebt „QGP-Preset → CMS entdeckt Higgs". Signifikanz sonst
    kontinuierlich ∝ prodVis (ersetzt binäre `minE`-Schranke). Daten **und** Fit aus EINEM Modell
    (`sampleMass`/`fitVal`). Energie-Slider koppelt live an `drawHist`. Drei klare Status-Gründe:
    falsches Strahl-Programm / Energie zu gering / kein Signal. Tests **42 grün**. Visuell bestätigt
    (ATLAS 0.45→6.8 TeV: Z⁰-Peak taucht auf; ALICE Pb-Pb: J/ψ unterdrückt; QGP-Lauf+CMS: 0σ „braucht Protonen").
  - **Strahl-Logik verfeinert „pro Resonanz" (Realismus-Audit):** Strahl-Gating jetzt korrekt
    physikalisch: **Z⁰ = QGP-blinde Standardkerze** → in pp UND Pb-Pb messbar (`discoBeam:"any"`, kein
    pp-Flag); Higgs/B⁰ bleiben pp-exklusiv (`pp:true`); Quarkonia in beidem (in pp = unverdrängte
    **p-p-Referenz**, in Pb-Pb QGP-unterdrückt). Detektor-Gating über `discoBeam` (`discoBeamOK`)
    statt fixem Detektor-Strahl. Energie-Schwellen ehrlich als **Raten-Schwellen** beschriftet
    („Produktionsrate zu gering", nicht „nicht erzeugbar"). Matrix (Preset×Detektor) gegen reale
    Physik geprüft: Higgs/LHCb-Preset (pp) → ATLAS/CMS/LHCb produktiv + ALICE p-p-Referenz;
    QGP-Preset (Pb-Pb) → **ATLAS-Z⁰ ✅ (Standardkerze)**, CMS/LHCb pp-blockiert, ALICE QGP.
    CP-Verletzung im Higgs-Preset ist KORREKT (alle Experimente laufen gleichzeitig auf pp-Strahl).
    Tests **43 grün** (u.a. „Z⁰ in pp UND Pb-Pb", „LHCb-CP nur pp"). UI-Matrix verifiziert.
  - **Reale Ansicht: LHC verifiziert + Injektor-Komplex an reale Lage + Zoom.**
    LHC-Geometrie frisch aus Overpass neu gezogen (`geo_build.py --fetch`, jetzt vollständig:
    `tt2_10`/`tt60` + neu `linac4` in `QUERIES`) und **verifiziert**: 16 Segmente / 290 Punkte,
    **max. Endpunkt-Lücke 0,00 px** = perfekt geschlossen, identisch zur vorigen Version → der
    Ring ist bereits maximal akkurate echte OSM-Geometrie (wirkt rund, weil der echte LHC fast
    rund IST). **LINAC 4 ist neu in OSM** (way 80305783) → als echtes Gebäude eingebaut; LEIR/
    LINAC 3 weiterhin ∉ OSM. **Injektor-Inset-Box entfernt** (`geo.js#drawInset` raus): der
    Komplex sitzt jetzt an der REALEN relativen Lage zu PS/PSB (Meyrin, CH-Seite, tangential nahe
    ATLAS); im Vollbild nur ein dezenter Hinweis-Ring (`.geo-inj-hint`), die Detail-Beschriftung
    (`.geo-inj-detail`, LINAC4/LINAC3/LEIR) erscheint per **Zoom-Button „🔬 Injektor-Komplex"**
    (`#svg.inj-zoom`, geo-genaues Fenster `App.geoInjectorView`). `resetView()`/`zoomMeyrin()` in
    handlers, Button nur in der Realen Ansicht sichtbar. Tests **45 grün** (Inset-Test → Real-Lage-
    Test). Visuell verifiziert (Vollbild-Hinweis + Zoom auf Meyrin-Cluster). Hinweis: `animateViewBox`
    nutzt `requestAnimationFrame` → im Headless-Preview keine Frames (nur dort), im echten Browser/
    Notebook animiert es normal.
  - **Presets auf die 3 realen LHC-Betriebsmodi reduziert (4 → 3):** Da Higgs UND CP-Verletzung
    auf DEMSELBEN pp-Strahl entdeckt werden, „Higgs"+„CP/LHCb" zu **„Protonen-Physik (13.6 TeV)"**
    zusammengeführt (`btn-pre-pp`, Default-Tab CMS; Higgs/Z⁰/CP via Detektor-Tab). Bleibt: QGP
    (jetzt reale Pb-Pb-Energie **2.70 TeV/u**, √s_NN 5.36 TeV) + Pilot (0.45 TeV Inbetriebnahme).
    Reale Run-Werte (Run 3: pp 6.8 TeV/Strahl=13.6 TeV, β* 0.30 m). `btn-pre-lhcb`/`preLhcb`
    entfernt (shell/handlers/main/info). Tests **44 grün** (neu: „nur 3 Presets"). UI verifiziert
    (3 Buttons in einer Reihe, alle Presets laden korrekte Werte, keine Konsolenfehler).
- **Zuletzt erledigt (Phase 4, Komponente 1 — Perf-Fix + ZWEI MODI):**
  - **Perf:** Bunch-Animation ruckelte (gefühlt 5 fps). Ursache: `drop-shadow`-SVG-Filter auf den
    12 kreisenden Bunches UND auf dem 360px-LHC-Ring (`.lit`) → jeder Frame komplett neu gerastert.
    Filter entfernt (Glow jetzt billig per Stroke). Gemessen: LHC-Loop **60 fps** (p95 17,6 ms,
    0 Frames > 20 ms). `#geo-layer{pointer-events:none}`.
  - **Zwei harte Modi statt Overlay (löst Overlapping):** `#svg` enthält `<g id="schematic">`
    (Didaktik) und `<g id="geo-layer">` (Real). `geo.js#setViewMode(real)` schaltet per `display`
    HART um (kein Doppelbild). Default = **Didaktik** (animiertes Schema). Button „🌍 Reale Ansicht"
    ⟷ „🎬 Didaktik-Modus". Bunches werden in `#schematic` gehängt → im Real-Modus mit ausgeblendet.
  - **Reale Ansicht = komplett OSM-Geodaten, echte Größen:** echter LHC-Ring, **SPS ≈ ¼ LHC, PS/PSB
    winzig** (reale Größenverteilung), Detektoren an echten IP-Positionen (Insertion-Zentroide),
    Lac Léman/Grenze/POI, Nord oben. `geo_build.py` holt SPS/PS/PSB + die 4 Insertions.
  - **TI 2/TI 8 = echte gekrümmte OSM-Trassen** (Datenlücke geschlossen): in OSM als `way(317804188)`
    „Tl2" und `way(317804189)` „Tl-8" (l statt I!). Trasse SPS-Ende→IP; letztes Stück bindet an den
    echten Injektionspunkt an (TI8 12 px, TI2 50 px Rest) → **Einlauf aus realer Richtung**.
  - **Übrige Transfers real:** TT2/TT10 + TT60 (PS↔SPS-Bereich) aus OSM ergänzt (`GEO.tt`).
  - **Zoom-Inset „Injektorkomplex Meyrin"** (links neben dem Ring, verdeckt keinen Detektor):
    zeigt die Kette LINAC4→PSB→PS / LINAC3→LEIR→PS + →SPS. **LINAC3/4 & LEIR sind NICHT in OSM**
    (mehrfach geprüft, auch Rel. 27005) → im Inset **schematisch/topologisch**, klar so betitelt.
    Damit sind die im Maßstab winzigen Vorbeschleuniger (sonst sub-px) sichtbar.
  - **LHC nicht perfekt rund** ist KORREKT (real 8 Bögen + 8 Geraden, OSM-Rel. 9512017 bestätigt es) —
    echte Form bleibt im Real-Modus. Didaktik-Detektoren sitzen auf den Strahlrohr-Crossovern.
  - **Visuell verifiziert** (Screenshots beide Modi) + Perf gemessen. Tests → **36 grün**; `check.sh` grün.
  - ⚠ **nbstripout ist in dieser Umgebung NICHT aktiv** (Git-Filter greift nicht). Falls das `.ipynb`
    ausgeführt wurde: vor Commit Outputs strippen (`nbstripout <nb>` oder `outputs=[]`/`execution_count=None`
    je Code-Zelle), sonst landen Outputs im Commit.
- **Zuvor erledigt (Phase 3 ABGESCHLOSSEN):** Headless-Test-Suite ausgebaut → **30 Tests / 4 Dateien**,
  alle grün: `tests/physics.test.mjs` (importiert `src/`-Module direkt; Signifikanz ∝ √N inkl.
  5·√(N/target) & Energie-Schwelle, Rate ∝ I²/β* deterministisch, Klassifikation Z⁰/J-ψ/Υ/Untergrund/
  Higgs-Kanal), `tests/interactions.test.mjs` (Tabs, SVG-Hits grp-*/hit-*, Info-Panel auf/zu,
  Param-Info-Akkordeon, Tempo-Toggle, Slider inkl. Quench-Warnung, Pilot/Higgs-Presets) plus die
  bestehenden Boot-Sonden. `check.sh` (esbuild+sync+node --check+nbformat/ast+vitest) grün.
- **Visuelle Kontrolle Phase 1+2 DURCHGEFÜHRT (✅):** Standalone `index.html` bootet
  (`__cernBooted`, 62 SVG-Kinder, keine Konsolenfehler), Presets/Tabs/Geo-Toggle reagieren;
  iframe-srcdoc-Simulation bootet **im iframe** isoliert und der postMessage-Auto-Resizer skaliert
  die Höhe korrekt (Screenshots gesichtet). Damit sind Phase 1 & 2 auch visuell bestätigt.
- **Nächster Schritt (Phase 4):** nächste Komponente migrieren — Kandidaten: Dimuon-„Teilchen-Zoo"-
  Spektrum (Vollspektrum mit allen Resonanzen) oder Z⁰-Fit (Gauss+Untergrund). Je Komponente
  Tests + 1× visuell. (Geo-Overlay ✅ erledigt.)

**Fortschritt:**
- [x] Phase 0 — Headless-Sonde (risikolos, kein Architekturwechsel) ✅
- [x] Phase 1 — Toolchain (esbuild+Vitest) + Modul-Isolation (ES-Module) ✅ (visuell bestätigt)
- [x] Phase 2 — Notebook bettet die gebaute App per `<iframe srcdoc>` ein ✅ (visuell bestätigt)
- [x] Phase 3 — Headless-Test-Suite (Interaktion + Physik-Logik) als Default-Verifikation ✅
- [ ] Phase 4 — Curriculum-Visualisierungen → App-Komponenten
- [ ] Phase 5 — Cleanups (Pfade generieren, `.py`-Spiegel ohne Widget, Legacy entfernen)

---

## 🎯 Ziel & Motivation

Kleine Fixes dauern heute >10 Min, weil die Architektur **headless schwer testbar** ist und
Verifikation deshalb in den langsamen, flakigen Browser fällt. Zielbild:

1. **Die Web-App (`cern/app/`) wird das primäre Artefakt** — entwickelt, getestet, debuggt als
   App. Sie enthält **alle interaktiven Elemente und Veranschaulichungen** (Stellwerk-Widget
   *und* die Curriculum-Visualisierungen).
2. **Verifikation headless-by-default** über **Vitest + jsdom** (Interaktions- & Physik-Logik
   in Millisekunden, deterministisch, kein Browser-/Cache-Tanz). Browser nur noch selten für
   Pixel/Layout.
3. **Das Notebook wird Konsument**: bettet die gebaute App per **`<iframe srcdoc>`** ein
   (isolierter DOM → die Jupyter-Script-Race und globale `getElementById`-Kollisionen
   verschwinden prinzipiell). Das Notebook behält das didaktische Narrativ (Markdown + ggf.
   Datenanalyse-Text).

---

## 🔒 Gelockte Entscheidungen (vom Nutzer bestätigt — nicht neu aufrollen)

1. **Bundler: JA.** `package.json` + **esbuild** (Build) + **Vitest** (Test/jsdom) sind im Repo
   erwünscht. Node-Toolchain neben Python ist okay.
2. **App = alles Interaktive/Visuelle.** Nicht nur das Stellwerk — auch die Curriculum-
   Visualisierungen (Z⁰-Fit, Higgs→4ℓ usw.) wandern als Komponenten in die App.
3. **Notebook-Einbettung per `<iframe srcdoc>`: JA.** Kein „inline im Output" mehr.
4. **Verifikation: Headless-Tests ausbauen** ist die Priorität (Vitest+jsdom).

---

## 🧱 Zielstruktur (Soll)

```
cern/app/                       # DIE App = primäres Artefakt
  package.json                  # scripts: dev / build / test (esbuild + vitest)
  esbuild.mjs                   # Build → dist/ (ein self-contained Bundle)
  index.html                    # Dev-Entry (lädt src/main.js); zugleich Standalone
  src/
    main.js                     # Entry: bootet bei DOM-Ready, mountet Komponenten
    core/
      data.js                   # GENERIERT aus cern/data/physics.json (gen_constants)
      geometry.js state.js engine.js display.js spectrum.js info.js handlers.js
    components/                  # die „Veranschaulichungen"
      stellwerk/                # heutiges Widget
      zboson-fit/  higgs-4l/  … # aus Notebook-Zellen 10/12/14 migriert
    styles.css  shell.html
  dist/                         # GEBAUT: self-contained html+js (für iframe & Standalone)
tests/                          # vitest + jsdom
  interactions.test.mjs  physics.test.mjs
scripts/
  gen_constants.py              # physics.json → src/core/data.js (bleibt)
  sync_widget.py                # injiziert dist/ in Notebook-Zelle(n) als <iframe srcdoc>
  check.sh                      # npm run build && npm test && nbformat/ast (headless-Tor)
```

---

## 🪜 Phasen (inkrementell, jede einzeln auslieferbar & verifizierbar)

### Phase 0 — Headless-Sonde *(risikolos, kein Architekturwechsel)*
- `tests/`-Skelett anlegen; das **aktuelle** `build/widget.js` (+ minimal gemocktes
  Canvas/DOM) in **jsdom** laden und 3–4 Interaktionen asserten: Geo-Toggle setzt
  `#svg.geo-dimmed`; Preset setzt Energie-Label; Füll-Button bekommt `.off`; Detektor-Tab
  wird `.act`.
- Ziel: beweisen, dass der Bundle headless durchläuft + Test-Muster etablieren.
- **Verifikation:** Test grün. Kein Notebook-/Browser-Schritt nötig.

### Phase 1 — Toolchain + Modul-Isolation *(größter struktureller Hebel)*
Modul-Modell = **leichter Namespace**: ein importiertes `App`-Objekt (`src/core.js`), dessen
Properties modulübergreifend gelesen/mutiert werden (kein Reassign importierter Bindungen).

**Konvertierungs-Pattern (pro Modul) — `cern/app/<m>.js` → `cern/app/src/<m>.js`:**
1. Oben: `import { App } from './core.js';` (+ benötigte Helfer/Refs).
2. Mutable Querschnittsvariablen: `foo` → `App.state.foo` (oder `const s=App.state; s.foo`).
3. DOM-Refs: `btnAuto` → `App.els.btnAuto` (werden bei Boot in `main.js#initDom` befüllt,
   NICHT mehr beim Modul-Laden — das fixt zugleich das Timing-Problem sauber).
4. Geometrie: `R`/`J`/`paths`/`nodes` → `App.g.*`.
5. Modulübergreifende Funktionsaufrufe: `setStatus(…)` → `App.setStatus(…)`.
6. Öffentliche Funktionen registrieren: `App.fuellProtokoll = fuellProtokoll;`.
7. Logik/Reihenfolge sonst 1:1 erhalten.

**Modul-Checkliste:**
- [x] `core.js` (neu: App/state/els/g + `$`, `SVG_NS`, `sleep`)
- [x] `esbuild.mjs` (Build + Datenblob-Spiegel `src/data.gen.js`)
- [x] `geometry.js` (R, J → App.g)
- [x] `state.js` (App.state + getDurations; + resetFlag/autopilotActive/Canvas-Maße)
- [x] `data.gen.js` (auto-generiert vom Build; CERN_REAL export)
- [x] `engine.js` (timeScale, injectBunch, flowStep, Ramp, Squeeze, LHC-Loop; Listener in `wireEngine`)
- [x] `display.js` (DETKONFIG, drawDetBg, drawParticle*, drawCollisionEvent, Legende)
- [x] `spectrum.js` (sampleEvent, generateMassData, classify, getSignificance, drawHist)
- [x] `info.js` (INFO_DB, PARAM_INFO, showInfo, buildPhotoHdr)
- [x] `handlers.js` (Listener-Verdrahtung `wireHandlers` + Presets + Füllprotokoll)
- [x] `main.js` (Entry: `initDom()` grabbt alle DOM-/SVG-Refs in App.els/App.g, dann
  `wireEngine`/`wireHandlers` + Init-Draw; **bootet bei DOM-Ready**, idempotent — ersetzt `__cernInit`/Bootstrap)

Danach: `npm run build` → `build/app.bundle.js`; neuen Test (oder bestehenden umhängen) gegen
das Bundle + `shell.html`-Markup laufen lassen; bei grün `sync_widget.py` auf das esbuild-Bundle
umstellen (Zelle 4/Standalone/iframe) und die alten `cern/app/*.js` entfernen.
- **Verifikation:** `npm test` grün **+ einmalig visuell** (Refactor ist riskant).

### Phase 2 — iframe-Einbettung ✅
- ~~`sync_widget.py` umstellen: Notebook-Zelle(n) werden **Mini-Loader**, die die App als
  `<iframe srcdoc="…">` einbetten (Höhe/Resize beachten). `id="cern-v4"`-Marker beibehalten,
  damit der Zellen-Finder greift.~~ **Erledigt:** `build_iframe_cell()` + `RESIZE_REPORTER`
  (postMessage-Auto-Höhe, Fallback `FALLBACK_H`); `esc_srcdoc` escapet nur `&`/`"`.
- Folge: Jupyter-Race weg; **Mini-Diffs** im `.ipynb` (nur Loader, nicht 1700 Zeilen).
- **Verifikation:** headless grün (`check.sh`, Finder/Re-Sync idempotent); **1× visuell in Jupyter
  noch offen** (Boot/Klicks/iframe-Höhe) — auf Nutzer-Anfrage.

### Phase 3 — Headless-Test-Suite als Default ✅
- ~~Interaktionstests (jsdom) für alle Buttons/Tabs/SVG-Hits **+ Physik-Logik-Tests**:
  `getSignificance ∝ √N`, Rate `∝ Intensität²/β*`, Klassifikation trifft PDG-Fenster.~~
  **Erledigt:** `tests/physics.test.mjs` (importiert `src/`-Module direkt) +
  `tests/interactions.test.mjs` (esbuild-Bundle in jsdom) + Boot-Sonden = **30 Tests**.
- `check.sh` baut (via `sync_widget.py`→esbuild) und läuft `vitest`. Browser nur noch Ausnahme.

### Phase 4 — Curriculum-Visualisierungen → App
- Interaktive/visuelle Teile der Python-Zellen (Z⁰-Fit, Higgs→4ℓ, Spektren …) als
  App-Komponenten nachbauen; Notebook behält Narrativ + bettet Komponenten per iframe ein.
- **Inkrementell**: eine Komponente nach der anderen, jeweils Tests + 1× visuell.
- **Geo-Overlay als eigene Komponente** ✅ **erledigt** (Komponente 1): handdigitalisiertes
  Overlay durch offline geo-projiziertes ersetzt (`geo_build.py` → `geo.gen.js` → `geo.js`).
  Vollständiger Befund + Plan: Anhang **„🗺️ Karten-Geo-Genauigkeit"**.

### Phase 5 — Cleanups
- Hardcodierte SVG-Pfade (`lhc-pipe1/2`, je ~4 KB) zur Laufzeit aus `R.LHC` **generieren**;
  für den **geo-genauen** Ring-Umriss siehe Anhang „🗺️ Karten-Geo-Genauigkeit".
- Widget aus dem `.py`-Spiegel ausnehmen (jupytext nur fürs Curriculum) → keine 166-KB-Dublette.
- Legacy entfernen (`cern/scripts/create_notebook.py`?), Docs final, `AGENTS.md`/`CLAUDE.md` glätten.

---

## 🚧 Invarianten (bei JEDER Phase wahren)

- **`physics.json` = Single Source of Truth** (Python *und* JS lesen daraus; `gen_constants.py`
  bleibt). Resonanzwerte nie doppelt pflegen.
- **`id="cern-v4"`-Marker** bleibt, sonst findet `sync_widget.py` die Zelle nicht.
- **Sprache Deutsch; Physik ehrlich** (Messung vs. „kalibrierte Simulation" kennzeichnen).
- **nbstripout** (Git-Filter) + **jupytext** (.py-Spiegel) fürs Curriculum bleiben aktiv.
- **Commits:** Feature-Branch (nicht direkt `main`), `Co-Authored-By:`-Zeile behalten.
- **Verifikation headless-default**; Browser nur bei Layout/Render oder auf Anfrage.

---

## 📓 Resume-Protokoll für den nächsten Agenten

1. Diese Datei + `CLAUDE.md` lesen. **STATUS / RESUME HERE** gibt die aktive Phase.
2. Nur die nächste offene Phase angehen (klein, verifizierbar).
3. Nach Abschluss: Checkbox + `Zuletzt erledigt` + `Nächster Schritt` aktualisieren, Datei mitcommitten.
4. Bei Unklarheit über Scope: erst fragen, nicht raten. Entscheidungen oben sind gelockt.

*Vorgeschichte/Detaildiagnose: `docs/agent-workflow-plan.md` (älter, durch dieses Dokument abgelöst).*

---

## 🗺️ Karten-Geo-Genauigkeit (Befund + Plan, gehört zu Phase 4/5)

**Auslöser:** Vorschlag, die Beschleuniger-Karte über echte OSM-Daten (Overpass API) +
Web-Mercator-Projektion (EPSG:3857) geografisch korrekt zu machen (LHC/SPS/PS/PSB + Lac Léman
+ CH/FR-Grenze).

### Kernbefund: Geo-Treue ⟂ Didaktik (bei den Beschleunigern)
Maßstabsgetreue Größenverhältnisse machen die Injektoren unsichtbar und damit den Füll-/Flow-
Effekt (wandernde Bunches) unmöglich:

| Ring | reale Ø | Verhältnis zum LHC | heute (r, SVG) | Verhältnis |
|---|---|---|---|---|
| LHC | 8 486 m | 1,0 | 180 | 1,0 |
| SPS | 2 200 m | **0,26** | 52 | 0,29 ✓ (zufällig ok) |
| PS | 200 m | **0,024** | 38 | 0,21 (~9× zu groß) |
| PSB/LEIR | ~50 m | **0,006** | 18 | 0,10 (~17× zu groß) |

Maßstäblich wäre der PS ein ~4-px-Punkt, der Booster praktisch unsichtbar. Zudem liegen
PS/SPS/Booster real **nicht konzentrisch im LHC**, sondern als kleiner Cluster **tangential am
Rand** (Meyrin, CH-Seite). Die heutige „verschachtelte Ringe"-Darstellung ist also bewusst
schematisch — didaktisch korrekt, geografisch falsch. **Fazit: nicht maßstabsgetreu beibehalten,
aber ehrlich labeln** (Invariante „Physik/Geometrie ehrlich").

### Bug im vorgeschlagenen Referenz-Code (wichtig)
Die Mercator-Formeln sind richtig (konform → Kreise bleiben Kreise; Verzerrung über ~10 km
vernachlässigbar). **Aber** die Beispiel-`to_svg_coords` skaliert X und Y **unabhängig**
(`(x-minx)/Δx*width` bzw. `…*height`) → zerstört das Seitenverhältnis und macht aus dem runden
LHC eine Ellipse, sobald `width/height ≠ Δx/Δy`. **Korrekt:** *uniformer* Faktor
`s = min(width/Δx, height/Δy)` + Zentrierung — genau das tut `d3.geoMercator().fitSize()`.
Über 0,2° Breite ist EPSG:3857 ohnehin Overkill; lokale equirektanguläre Projektion
(`x=lon·cos(lat₀)`, `y=lat`) wäre visuell identisch.

Weitere Risiken: feste OSM-IDs (`way(310046324)` …) sind **nicht versionsstabil** (LHC ist in
OSM eher eine *relation*); und das Widget läuft **offline im Notebook-iframe** → Overpass darf
**nur zur Build-/Preprocessing-Zeit** laufen, **nie** zur Laufzeit.

### Empfehlung: zwei Ebenen mit unterschiedlichem Wahrheitsanspruch
- **Ebene A — Geo-Overlay „Wo steht der LHC?" (echte Projektion lohnt sich):** Lac Léman,
  Staatsgrenze, Jura, FR/CH, Campusse **und LHC-Ring-Umriss** in *einer* gemeinsamen Projektion
  mit **uniformer** Skalierung. Macht die relative Lage See/Grenze ↔ Ring ehrlich; der echte
  achteckige Ringverlauf (8 Bögen + 8 Geraden) kommt gratis mit. → **Phase 4** als Komponente.
- **Ebene B — operatives Schema (bleibt nicht maßstäblich):** Kette PSB→PS→SPS→LHC + wandernde
  Bunches, Injektoren bewusst 10–40× vergrößert. Bester Kompromiss: **Topologie/Orientierung
  korrekt, Größe falsch** (Detektoren IP1/2/5/8 + Injektor-Einspeisung relativ zu See/Grenze in
  die richtige Himmelsrichtung). Klar labeln: „schematisch, nicht maßstabsgetreu".

### Pipeline (offline, ohne Laufzeit-Netz)
Overpass-Query → `d3.geoMercator().fitSize()` (oder GeoPandas `.to_crs(3857)`) **offline** →
projizierte Polylines als **statische** SVG-`<path>` in `shell.html` backen (wie `lhc-pipe1/2`
schon gebacken sind). Passt zur `geo-element`-Struktur und zur Phase-5-Idee „Pfade generieren".

**Einordnung:** kein Phase-1/2/3-Thema. Erster risikoarmer Schritt = Ebene A (geo-korrektes
Overlay) in Phase 4; maßstäbliche Beschleuniger-Größen werden **bewusst nicht** übernommen.
