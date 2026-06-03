# AGENTS.md — Arbeitsanleitung für KI-Agenten (CERN-Projekt)

Didaktisches Jupyter-Notebook (Begabtenkurs Teilchenphysik): 7-teiliges Curriculum mit echten
CMS-Open-Data + eingebettetem interaktivem „Stellwerk"-Widget (HTML/JS-Canvas).
Hauptdatei: `cern/notebooks/CERN_Beschleuniger_Schaltzentrale.ipynb`.

> 🧭 **AKTIVER UMBAU — zuerst `docs/MIGRATION.md` lesen (Abschnitt STATUS / RESUME HERE).**
> Wir migrieren auf eine App-First-Architektur (Web-App als primäres Artefakt, esbuild+Vitest
> headless-Tests, Notebook bettet per `<iframe srcdoc>` ein). Der fortsetzbare Plan + Status
> leben in `docs/MIGRATION.md` — der Chat kann gecleart werden, ohne dass der Plan verloren geht.
> Die untenstehende „Karte"/„Widget editieren" beschreibt den **Ist-Zustand** bis zum Umbau.

## ⚡ Verifikations-Politik (WICHTIG — spart Quota)
- **Standard = headless.** Pro Änderung nur:
  1. `node --check` auf das extrahierte/gebündelte JS,
  2. `nbformat.validate` + `ast.parse` aller Code-Zellen,
  3. bei Physik/Mathe: Node-Logik-Test (ohne Browser).
- **Browser-Screenshots NUR** auf ausdrückliche Anfrage des Nutzers ODER bei reinen
  Layout-/Rendering-Änderungen. **Niemals als Default.**
- **Nie** den vollen Füllen→Ramp→Squeeze→Kollidieren-Ablauf (30–45 s) scripten, um Logik zu
  prüfen — Logik headless testen (oder Debug-Hook, siehe Plan).
- Kein `nbconvert --execute` für reine Widget-Änderungen (Python-Zellen sind unberührt).

## Karte (wo liegt was)
- **Notebook-Zellen 0–15**: Curriculum (Markdown + Python). **Zelle 4 = Widget-Loader**
  (`display(HTML(r'''<iframe srcdoc=…>'''))`, Phase 2 — bettet das esbuild-Bundle isoliert ein).
- **Widget** (esbuild-Bundle aus `cern/app/src/`, im iframe):
  - Physik-Engine: `timeScale`, `getDurations`, `injectBunch`, `flowStep`, `fuellProtokoll`, `startLHCLoop`, Ramp.
  - Event-Display: `DETKONFIG`, `drawDetBg`, `drawParticleBarrel/Forward`, `drawCollisionEvent`, `drawLegend`.
  - Spektrum/Signifikanz: `sampleEvent`, `generateMassData`, `classify`, `getSignificance`, `drawHist`.
  - Zwei Modi (Phase 4): `#svg` hat `<g id="schematic">` (Didaktik, animiert) + `<g id="geo-layer">`
    (Reale Ansicht). `geo.js#setViewMode(real)` schaltet per `display` hart um (kein Overlap; Default
    Didaktik). Real = komplett OSM-Geodaten in echter Größe (`geo.js#drawGeo` aus `geo.gen.js`,
    generiert von `scripts/geo_build.py`, Web-Mercator/uniform, ODbL; TI 2/8 approx., da nicht in OSM).
  - Daten: `CERN_REAL` (echte CMS-Massen/Topologien, ~37 KB) — eingebettet.
- **Python-Datenschicht**: `cern/scripts/cern_utils.py` (`RESONANZEN`, `HISTORIE`, `lade_cms_dimuon`,
  `lade_dimuon_4vektoren`, `dimuon_invariante_masse`, `lade_higgs_4l`).
- **Echte Daten**: `cern/data/cms_dimuon_subset.csv` (12 000 Events — **nie ganz lesen**).

## Widget editieren (ES-Module — Phase 1 abgeschlossen)
Quelle der Wahrheit: `cern/app/src/` (echte ES-Module, einzeln node-prüfbar). **Niemals**
Zelle 4 oder `cern/app/index.html` von Hand editieren (beide generiert).
- Geteilter Namespace `App` (`src/core.js`): `App.state` (Querschnittsvariablen), `App.els`
  (DOM-Refs, bei Boot via `main.js#initDom` befüllt), `App.g` (SVG-Geometrie R/J/paths/nodes),
  registrierte Funktionen `App.drawHist` usw. Module mutieren `App.*`-Properties (kein Reassign).
- Relevante Datei in `src/` direkt mit dem **Edit-Tool** bearbeiten:
  - `engine.js` — timeScale, injectBunch, flowStep, Ramp, Squeeze, LHC-Loop, Readouts (+ `wireEngine`)
  - `display.js` — DETKONFIG, drawDetBg, drawParticle*, drawCollisionEvent, Legende
  - `spectrum.js` — sampleEvent, generateMassData, classify, getSignificance, drawHist
  - `geometry.js` (R/J → App.g), `state.js` (App.state + getDurations), `info.js` (INFO_DB/PARAM_INFO),
    `handlers.js` (Listener-Verdrahtung `wireHandlers` + Presets + Füllprotokoll), `main.js` (Boot/initDom)
  - `../styles.css`, `../shell.html` (CSS/Markup), `../data.js` = CERN_REAL-Blob (~37 KB) —
    **nicht lesen/editieren**, außer Daten ändern sich (Build spiegelt es nach `src/data.gen.js`).
- Danach **immer**: `bash scripts/check.sh` (esbuild-Build + sync + node --check + nbformat/ast + vitest).
- Build/Sync: `npm run build` → `build/app.bundle.js` (esbuild, IIFE). `scripts/sync_widget.py`
  baut das Bundle und injiziert es in Notebook-Zelle 4 (self-contained) + `build/widget_bundle.html`
  + `cern/app/index.html` (Standalone). `main.js` bootet idempotent bei DOM-Ready (löst die Jupyter-Race).
- Headless-Tests (30, alle grün): `tests/physics.test.mjs` (importiert `src/`-Module direkt:
  Signifikanz ∝ √N, Rate ∝ I²/β*, PDG-Klassifikation), `tests/interactions.test.mjs`
  (Tabs/SVG-Hits/Info-Panel/Slider/Presets im esbuild-Bundle) + Boot-Sonden
  `app-boot.test.mjs`/`widget-boot.test.mjs`.

## Standard-Befehle
```
bash scripts/check.sh          # esbuild + sync + node --check + jupytext --sync + nbformat/ast + vitest (headless)
npm run build                  # nur esbuild: cern/app/src/* → build/app.bundle.js
python3 scripts/sync_widget.py # baut Bundle + injiziert (Zelle 4 + build/ + index.html)
npx vitest run                 # nur Headless-Tests (jsdom)
```
Standalone-App im Browser (nur bei Layout/Render-Fragen): `cern/app/index.html` öffnen.

## Notebook-Workflow (jupytext + nbstripout)
- Das `.ipynb` ist mit einem **`.py`-Spiegel** (`py:percent`) gepaart — *die* diffbare/reviewbare
  Quelle für das **Curriculum** (Markdown + Python-Zellen). Zelle 4 (Widget) bleibt generiert.
- Curriculum editieren: entweder `.py` ODER `.ipynb` ändern, dann `jupytext --sync` (läuft in `check.sh`).
- **`nbstripout`** ist als Git-Filter installiert (`.gitattributes`) → Outputs werden beim Commit
  automatisch entfernt. Kein manuelles „Outputs leeren" mehr nötig.

## Commits
- Branch `feat/echte-cern-daten-event-display`. Outputs werden via `nbstripout`-Filter auto-gestrippt.
- `scratch/`, `CERN_Visualisierung/`, `.DS_Store`, `cern/resources/ai_studio_code*.html`
  sind jetzt in `.gitignore` (nicht committen).
- `Co-Authored-By:`-Zeile beibehalten.

## Konventionen
- Sprache: Deutsch. Physik ehrlich (Messung vs. „kalibrierte Simulation" kennzeichnen).
- Plan-Modus nur für große/mehrdeutige Aufgaben; kleine Fixes direkt + headless-Check.
- Antworten knapp halten; keine großen Code-Blöcke/Tabellen echoen.
