# 🧭 MIGRATION — App-First-Architektur (autoritativer, fortsetzbarer Plan)

> **Dies ist die Single Source of Truth für den laufenden Umbau.**
> Jeder Agent liest zuerst den Abschnitt **STATUS / RESUME HERE**, arbeitet die nächste
> offene Phase ab, hakt sie ab und committet diese Datei mit. Der Chat darf jederzeit
> wegen Kontextlänge gecleart werden — der Plan lebt hier, nicht im Chatverlauf.

---

## 🟢 STATUS / RESUME HERE

- **Aktive Phase:** Phase 0 (noch nicht begonnen).
- **Entscheidungen:** gelockt (siehe „Gelockte Entscheidungen"). Nicht erneut hinterfragen.
- **Zuletzt erledigt (Vorsession):** Interaktions-Bug gefixt — die ganze Widget-Logik lag
  in *einer* sofort ausgeführten IIFE ohne DOM-Ready-Guard → in Jupyter lief das `<script>`
  oft vor dem DOM → `getElementById`=null → komplette Init brach ab (nur native Slider
  „funktionierten" scheinbar). Fix: IIFE → benannte `__cernInit` + Bootstrap (`handlers.js`),
  der erst bei vorhandenem DOM bootet (idempotent pro Knoten). Außerdem: kaputter Standalone
  repariert (`sync_widget.py` bündelt JS jetzt als EIN inline-`<script>`).
- **Nächster Schritt:** Phase 0 — jsdom-Smoke-Test gegen das aktuelle `build/widget.js`.

**Fortschritt:**
- [ ] Phase 0 — Headless-Sonde (risikolos, kein Architekturwechsel)
- [ ] Phase 1 — Toolchain (esbuild+Vitest) + Modul-Isolation (ES-Module)
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
- `package.json` + esbuild + vitest. Die 8 IIFE-Slices in **echte ES-Module** (`import/export`)
  überführen — **Definitionsreihenfolge/Logik erhalten**. Build erzeugt ein einzelnes Bundle.
- Dadurch entfällt der `__cernInit`/Bootstrap-Workaround (Entry/Bundler übernimmt das Booten),
  und **jede Datei ist einzeln gültig** → per-Datei-Lint + Unit-Tests möglich.
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
