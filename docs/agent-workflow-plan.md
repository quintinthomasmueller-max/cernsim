# Plan: Agent-Workflow-Optimierung (Token & Zeit)

Ziel: kleine Features/Fixes am CERN-Notebook deutlich billiger & schneller machen.
Drei Hebel: **Architektur** (editierbare Dateien), **Verifikation** (headless-default),
**Doku** (`AGENTS.md`, bereits erstellt).

## Diagnose (gemessen in dieser Session)
1. Widget = 108 KB Python-Rohstring in *einer* Zelle → nicht mit Edit-Tool bearbeitbar →
   fragile Python-Patch-Skripte mit Retries. Ein 1-Zeilen-Fix ≈ 10–15 Tool-Calls.
2. `CERN_REAL`-Datenblob (~37 KB) klebt im Code → jeder Read schleppt ihn mit.
3. Visuelle Verifikation: Server + 30–45 s Füll-Animation + Screenshots (Bild-Tokens) ≈ 15 Calls.
4. Kein schneller Zustands-Sprung zum Testen einer Kollision.
5. Wiederholtes Re-Explorieren der Struktur (jetzt durch `AGENTS.md` adressiert).

## A. Modularer Widget-Refactor (größter Hebel)
Zielstruktur:
```
cern/app/
  index.html     # Standalone-Shell (DOCTYPE, lädt CSS+JS) — erfüllt zugleich die Dual-Existenz
  styles.css     # gesamtes CSS (.cv4-*)
  data.js        # const CERN_REAL = {…}   (37-KB-Blob raus aus dem Code)
  geometry.js    # SVG-Pfade/Knoten/Ringe (R, J, paths, nodes) + DETKONFIG
  engine.js      # timeScale, getDurations, injectBunch, flowStep, fuellProtokoll, Ramp, LHC-Loop
  display.js     # drawDetBg, drawParticleBarrel/Forward, drawCollisionEvent, drawLegend
  spectrum.js    # sampleEvent, generateMassData, classify, getSignificance, drawHist
  main.js        # DOM-Refs, Event-Listener, Init
build/widget_bundle.html   # generiert: CSS+JS+HTML gebündelt, für die Notebook-Zelle
scripts/sync_widget.py     # cern/app/* -> build/widget_bundle.html und Notebook-Zelle 4 (idempotent)
```
- **Notebook-Zelle 4** wird Mini-Loader: liest `build/widget_bundle.html` und `display(HTML(...))`.
  Erzeugt identische Ausgabe wie heute (Trust/Script-Verhalten unverändert).
- **`scripts/sync_widget.py`** bündelt; nur diese eine Stelle berührt das `.ipynb`.

**Vorteile:** Edit-Tool statt Patch-Skripte; Reads nur auf die relevante `.js` (klein);
`node --check` pro Modul; Datenblob nie im Code-Read; minimale Diffs; Standalone-App fällt ab.

**Migrationsschritte:**
1. Zelle 4 zerlegen: HTML→`index.html`, CSS→`styles.css`, `CERN_REAL`→`data.js`,
   JS-Funktionsgruppen→Module (Reihenfolge der Definitionen erhalten).
2. `sync_widget.py` schreiben → `build/widget_bundle.html`; Zelle 4 = Loader.
3. **Einmalig voll verifizieren** (auch visuell — Refactor ist riskant): node --check je Modul,
   Standalone im Browser einmal durchklicken. Danach dauerhaft headless.
4. `AGENTS.md`-Abschnitt „Widget editieren" auf den neuen Pfad umstellen. Commit.

## B. Verifikation headless-by-default
- **`scripts/check.sh`**: extrahiert/bündelt JS → `node --check`; dazu `nbformat.validate` +
  `ast.parse` aller Code-Zellen. Ein Aufruf statt vieler Calls.
- **`scripts/widget_logic_test.mjs`**: lädt `data.js`/`engine.js`/`spectrum.js` in Node, mockt
  Canvas/DOM minimal, prüft reine Funktionen ohne Browser:
  - `getSignificance` wächst ∝ √N (Monotonie + Skalierung),
  - `generateMassData`-Rate ∝ Intensität²/β*,
  - Kinematik/Klassifikation (Massen treffen PDG-Fenster).
- **Debug-Hook im Widget**: `window.__dbg = { seed(mode, nCollisions) }` springt sofort in den
  Zustand „gefüllt + N Kollisionen" (kein 40-s-Ablauf). Nur für Tests, kein Nutzer-UI.
- **Screenshots nur** auf ausdrückliche Anfrage / bei Layout-Änderungen.

## C. Kontext-/Token-Disziplin
- `AGENTS.md` verhindert Re-Exploration (Karte + Befehle + Politik).
- Nie die 12k-CSV oder den 37-KB-Datenblob ganz lesen.
- Reads auf Zeilenbereiche/Funktionen begrenzen (nach Refactor trivial pro Modul).
- Knappe Antworten; keine großen Code-Blöcke/Tabellen wiederholen.
- Plan-Modus nur für große/mehrdeutige Aufgaben.

## Erwarteter Effekt
1-Zeilen-Widget-Fix: heute ~10–15 Tool-Calls + Bilder → künftig ~2–4 (Edit + `check.sh`),
**keine Bilder**. Wegfall der visuellen Default-Verifikation = größter Quota-Posten eliminiert.

## Risiken / Hinweise
- Der einmalige Refactor des Monolithen ist riskant → dabei einmal voll (inkl. visuell)
  verifizieren; danach headless.
- Bundle muss byte-genau dieselbe Ausgabe erzeugen (Trust + `id="cern-v4"`-Marker behalten,
  damit Such-/Loader-Logik weiter greift).
- Reihenfolge der JS-Definitionen wahren (Funktions-Hoisting genügt nicht für `const`-Helfer).

## Nächster Schritt
Auf „los" setze ich Teil A+B um (eigener Commit), aktualisiere `AGENTS.md` und verifiziere
den ausgelagerten Stand einmalig voll.
