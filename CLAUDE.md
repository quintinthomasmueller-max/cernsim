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
- **Notebook-Zellen 0–15**: Curriculum (Markdown + Python). **Zelle 4 = Widget**.
- **Widget** (`display(HTML(r'''…'''))` in Zelle 4, ~108 KB HTML+CSS+JS+Datenblob):
  - Physik-Engine: `timeScale`, `getDurations`, `injectBunch`, `flowStep`, `fuellProtokoll`, `startLHCLoop`, Ramp.
  - Event-Display: `DETKONFIG`, `drawDetBg`, `drawParticleBarrel/Forward`, `drawCollisionEvent`, `drawLegend`.
  - Spektrum/Signifikanz: `sampleEvent`, `generateMassData`, `classify`, `getSignificance`, `drawHist`.
  - Daten: `CERN_REAL` (echte CMS-Massen/Topologien, ~37 KB) — eingebettet.
- **Python-Datenschicht**: `cern/scripts/cern_utils.py` (`RESONANZEN`, `HISTORIE`, `lade_cms_dimuon`,
  `lade_dimuon_4vektoren`, `dimuon_invariante_masse`, `lade_higgs_4l`).
- **Echte Daten**: `cern/data/cms_dimuon_subset.csv` (12 000 Events — **nie ganz lesen**).

## Widget editieren (NEU — modular)
Quelle der Wahrheit: `cern/app/`. **Niemals** Zelle 4 von Hand editieren.
- Relevante Datei direkt mit dem **Edit-Tool** bearbeiten:
  - `engine.js` — timeScale, getDurations, injectBunch, flowStep, fuellProtokoll, Ramp, LHC-Loop
  - `display.js` — DETKONFIG, drawDetBg, drawParticle*, drawCollisionEvent, Legende
  - `spectrum.js` — sampleEvent, generateMassData, classify, getSignificance, drawHist
  - `geometry.js` (SVG/Ringe), `state.js`, `handlers.js` (Listener/Init), `styles.css`, `shell.html`
  - `data.js` = CERN_REAL-Blob (~37 KB) — **nicht lesen/editieren**, außer Daten ändern sich.
- Danach **immer**: `bash scripts/check.sh` (führt sync aus + node --check + nbformat/ast).
- `scripts/sync_widget.py` bündelt `cern/app/*` → Notebook-Zelle 4 (self-contained) +
  `build/widget_bundle.html` + `cern/app/index.html` (Standalone-App).
- Hinweis: Module sind geordnete Slices EINER Funktion `__cernInit` (gemeinsame Closure;
  `geometry.js` öffnet, `handlers.js` schließt + ruft sie via Bootstrap erst bei DOM-Ready auf).
  Einzeln **nicht** node-prüfbar (Syntaxfehler je Datei) — `node --check` läuft auf dem
  gebündelten `build/widget.js` (via check.sh). `index.html` bündelt das JS als EIN inline-`<script>`
  (getrennte `<script src>` wären kaputt). **Phase 1 der Migration löst genau diese Fragilität auf.**

## Standard-Befehle
```
bash scripts/check.sh          # sync + node --check + jupytext --sync + nbformat.validate + ast.parse (headless)
python3 scripts/sync_widget.py # nur neu bündeln (Zelle 4 + build/ + index.html)
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
