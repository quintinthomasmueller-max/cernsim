# 🧭 MIGRATION — App-First-Architektur (autoritativer, fortsetzbarer Plan)

> **Dies ist die Single Source of Truth für den laufenden Umbau.**
> Jeder Agent liest zuerst den Abschnitt **STATUS / RESUME HERE**, arbeitet die nächste
> offene Phase ab, hakt sie ab und committet diese Datei mit. Der Chat darf jederzeit
> wegen Kontextlänge gecleart werden — der Plan lebt hier, nicht im Chatverlauf.

---

## 🟢 STATUS / RESUME HERE

- **Aktive Phase:** Phase 2 (Notebook bettet App per `<iframe srcdoc>` ein) — **offen**.
- **Entscheidungen:** gelockt (siehe „Gelockte Entscheidungen"). Modul-Modell = **leichter Namespace** (`App`-Objekt).
- **Zuletzt erledigt (Phase 1 ABGESCHLOSSEN):** ALLE Module nach `cern/app/src/` als echte
  ES-Module konvertiert (`core/geometry/state/engine/display/spectrum/info/handlers` + neuer Entry
  `src/main.js` mit `initDom()` + idempotentem Bootstrap; ersetzt `__cernInit`). `npm run build`
  → `build/app.bundle.js` (esbuild IIFE). `sync_widget.py` baut jetzt das esbuild-Bundle und
  injiziert es in Zelle 4 / `index.html` / `widget_bundle.html` (alte IIFE-Slice-Konkatenation weg).
  **Legacy `cern/app/{geometry,state,engine,display,spectrum,info,handlers}.js` entfernt.**
  Neuer Test `tests/app-boot.test.mjs` (esbuild-Bundle) + bestehender `widget-boot.test.mjs` grün.
  `bash scripts/check.sh` (esbuild+sync+node --check+nbformat/ast+vitest) komplett grün.
  **Noch offen aus Phase 1:** einmalige **visuelle** Browser-Kontrolle (Refactor war riskant) —
  bisher nur headless verifiziert; auf Nutzer-Anfrage durchführen.
- **Nächster Schritt (Phase 2):** `sync_widget.py` so umstellen, dass Zelle 4 ein **Mini-Loader**
  wird, der `build/app.bundle.js`+CSS+Markup als `<iframe srcdoc="…">` einbettet (Höhe/Resize,
  `id="cern-v4"`-Marker behalten). Folge: Jupyter-Race endgültig weg + Mini-Diffs im `.ipynb`.

**Fortschritt:**
- [x] Phase 0 — Headless-Sonde (risikolos, kein Architekturwechsel) ✅
- [x] Phase 1 — Toolchain (esbuild+Vitest) + Modul-Isolation (ES-Module) ✅ (visueller Check noch offen)
- [ ] Phase 2 — Notebook bettet die gebaute App per `<iframe srcdoc>` ein
- [ ] Phase 3 — Headless-Test-Suite (Interaktion + Physik-Logik) als Default-Verifikation
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

### Phase 2 — iframe-Einbettung
- `sync_widget.py` umstellen: Notebook-Zelle(n) werden **Mini-Loader**, die `dist/` als
  `<iframe srcdoc="…">` einbetten (Höhe/Resize beachten). `id="cern-v4"`-Marker beibehalten,
  damit der Zellen-Finder greift.
- Folge: Jupyter-Race weg; **Mini-Diffs** im `.ipynb` (nur Loader, nicht 1700 Zeilen).
- **Verifikation:** einmal in Jupyter öffnen + klicken; danach headless.

### Phase 3 — Headless-Test-Suite als Default
- Interaktionstests (jsdom) für alle Buttons/Tabs/SVG-Hits **+ Physik-Logik-Tests**:
  `getSignificance ∝ √N`, Rate `∝ Intensität²/β*`, Klassifikation trifft PDG-Fenster.
- `check.sh` ruft `npm run build && npm test`. Browser nur noch Ausnahme (Pixel/Layout).

### Phase 4 — Curriculum-Visualisierungen → App
- Interaktive/visuelle Teile der Python-Zellen (Z⁰-Fit, Higgs→4ℓ, Spektren …) als
  App-Komponenten nachbauen; Notebook behält Narrativ + bettet Komponenten per iframe ein.
- **Inkrementell**: eine Komponente nach der anderen, jeweils Tests + 1× visuell.

### Phase 5 — Cleanups
- Hardcodierte SVG-Pfade (`lhc-pipe1/2`, je ~4 KB) zur Laufzeit aus `R.LHC` **generieren**.
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
