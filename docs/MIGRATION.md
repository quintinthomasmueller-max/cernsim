# 🧭 PROJEKTZUSTAND — CERN-Stellwerk (App-First, Politur-Endphase)

> **Single Source of Truth für den Stand des Projekts.** Diese Datei sagt einem neuen Agenten
> in einem Blick: *Wo stehen wir, was ist zu welchem Grad umgesetzt, was ist noch offen.*
> Der Chat darf jederzeit gecleart werden — der Zustand lebt hier + im `git log`.
>
> **Architektur-Umbau (App-First, Phasen 0–4) ist abgeschlossen.** Wir sind in der
> **Feinschliff-/Verbesserungs-Endphase**: keine Struktur-Umbrüche mehr, sondern Didaktik,
> Physik-Genauigkeit, UX und Tooling-Politur. Erst **CLAUDE.md** lesen (Karte + Modulindex +
> Verifikations-Politik), dann hier den relevanten Bereich.

**Legende Umsetzungsgrad:** ✅ fertig & verifiziert · 🟡 grundsätzlich da, Feinschliff/Rest offen · ⬜ offen

---

## 🟢 STATUS / RESUME HERE

- **Phase:** Feinschliff (Architektur steht). Verifikation **headless-default** (`bash scripts/check.sh`,
  88 vitest-Tests grün). Browser nur bei Layout/Render oder auf Nutzer-Anfrage.
- **Branch:** `feat/geo-infos-fotos-geometrie` (Feature-Branch, nicht direkt `main`).
- **Wenn du eine Aufgabe bekommst:** den passenden Bereich unten finden (Umsetzungsgrad +
  „wie es funktioniert" + Schlüsseldateien), ändern, `check.sh`, diesen Abschnitt + den
  Bereich aktualisieren, mitcommitten.
- **Nächste sinnvolle Schritte (keiner blockierend):** siehe **„🔧 Offene Punkte"** unten —
  Phase-5-Cleanups (SVG-Pfade generieren, Widget aus `.py`-Spiegel) + Tooling-Politur
  (paralleles `check.sh`, vitest-Projects) + physikalische Restabweichung φ(1020).

---

## 📦 Was ist umgesetzt — Bereiche & Umsetzungsgrad

### Architektur / Toolchain — ✅
App-First-Umbau komplett: `cern/app/src/*` = echte ES-Module, gebündelt per **esbuild** →
`build/app.bundle.js` (IIFE). `scripts/sync_widget.py` injiziert das Bundle als **`<iframe srcdoc>`**
in Notebook-Zelle 4 (isolierter DOM → Jupyter-Script-Race & `getElementById`-Kollisionen sind
prinzipiell weg) + `cern/app/index.html` (Standalone) + `cern/CERN-Stellwerk.html` (Teilen-Datei).
`main.js` bootet idempotent bei DOM-Ready. Test-Default = **Vitest + jsdom** (88 Tests, 5 Dateien:
`physics` importiert `src/`-Module direkt; `interactions` + `audit-fixes` booten das Bundle gegen
`shell.html`; `app-boot`/`widget-boot` = Boot-Sonden).

### Physik-Engine (Füllen → Ramp → Squeeze → Datennahme) — ✅
- **Füllen realistisch:** 1 Punkt = 1 PS-Batch (72 B Protonen / 37 B Ionen), Fan-in
  LINAC→PSB/LEIR→PS→SPS, **Akkumulation + Fusion** zu Zügen, dann via TI 2/8 in den LHC
  (Protonen 2808 B/Strahl, Pb 592). Zeitskala im Speed-Button deklariert.
- **Tempo kohärent:** EINE px/ms-Geschwindigkeits-Leiter (`state.js#getStageVel`),
  dur = Pfad-/Bogenlänge / Geschwindigkeit → kein Stau in kurzen Transferlinien.
- **Burn-off:** N(t)=N₀·e^(−t/τ) (τ=15 h), L∝N², Bunches verblassen ∝ N, Dump bei N<35 %.
- **Datennahme:** koppelt an integrierte Luminosität ∝ I²/β* (Squeeze hat sichtbaren Payoff);
  echte `performance.now()`-Zeitbasis (tab-throttle-fest); Mehr-Fill-Summierung (`keepData`).
- **Logik-Härtung:** `s.fillGen` gegen Zombie-Batches, `s.dumping`-Gate, Pause friert Burn-off,
  Quench probabilistisch. (Detail-Regression in `tests/audit-fixes.test.mjs`.)
- Schlüssel: `engine.js`, `state.js`, `core.js#FILL/DT_SCALE`.

### Massenspektrum (Daten ↔ Kurve ↔ Physik) — 🟡 (eine bekannte Restabweichung)
- **Datenkalibriert:** `spectrum.js#calib` baut die Modellkurve EINMAL pro Profil aus dem echten
  Pool (KDE-Untergrund mit Randkorrektur + Pool-Anteil×Gauß) → χ²/ndf 0,8–2,8 (vorher 14–157,
  handgetunt). `bg()/amp` in DETSPEC nur noch Fallback.
- **Rejection-Sampling** (`sampleMass`): unterdrückte Resonanz → echtes Kontinuum statt
  Uniform-Plateau; R_AA senkt Peak-zu-Kontinuum korrekt.
- **Nullhypothese-Overlay** (`drawHist`, gestrichelt „ohne Higgs"/„ohne QGP (R_AA=1)"): der
  historische Beweis-Mechanismus (Überschuss/Defizit ggü. Untergrund-Hypothese). API:
  `App.fitValFor`/`App.nullValFor`.
- **Strahl-bewusste Matrix:** 8 Profile (Detektor × {pp,PbPb}); jeder Detektor zeigt IMMER nur
  das im aktuellen Strahl real Mögliche (`getSignificance` durch `beamMatches` gegated —
  kein „QGP-Preset → CMS entdeckt Higgs"). Signifikanz wächst √-förmig ∝ √(collStore/target).
- **4ℓ kohärent:** `sampleEvent` gated ALLE Resonanzen, zieht Masse+Leptonen als EIN Event;
  `higgsCands` zählt via `pushMass` (konsistent zum Histogramm). Reservoir-Sampling am HIST_CAP.
- 🟡 **Restabweichung:** φ(1020)-Buckel am linken ALICE-Rand ~4σ (KDE-Glättung am Rand).
- Schlüssel: `spectrum.js`, `cern/data/physics.json` (Konstanten).

### Event-Display (Detektor) — ✅
„Zwiebelschalen": gefüllte Materialschichten mit Klartext-Callout-Spalte (alle 4 Detektoren,
LHCb = Stations-Platten + Flugrichtung). Maßstab (Meterleiste + Strichmännchen 1,8 m).
**Interaktiv:** Klick auf Schicht → Info-Panel mit echtem Wikimedia-Foto (`display.js#evLayerHit`,
Fotos via Commons-API verifiziert). **Signaturen-Tour** (`#btn-ev-tour`, 6 Schritte): pro Schritt
1 Teilchen + leuchtende Ziel-Schicht. Untergrundspuren aus echter `topo.bg`-Kinematik.

### Reale Ansicht / Geo — 🟡 (LEIR/LINAC3 approximiert, sonst echt)
Zwei harte Modi in `#svg`: `<g id="schematic">` (Didaktik, animiert) ⟷ `<g id="geo-layer">`
(real), Umschaltung per `display` (`geo.js#setViewMode`). Real = komplette OSM-Geodaten in echter
Größe (`geo.gen.js`/`sat.gen.js`, generiert von `scripts/geo_build.py`, uniform Web-Mercator,
ODbL): LHC-Ring (16 Segmente, geschlossen), SPS/PS/PSB maßstäblich, Detektoren an echten
IP-Zentroiden, TI 2/8 echte gekrümmte Trassen, Lac Léman/Grenze. **Injektor-Zoom** „🔬 Meyrin"
(`#svg.inj-zoom`, non-scaling-stroke). **FCC-Easter-Egg** (✦ im Genfersee → maßstäblicher
FCC-Ring ×3,4, `handlers#revealFCC`).
- 🟡 **LEIR + LINAC3 ∉ OSM** → Größe/Form/Maßstab real, **Position approximiert** (gestrichelt,
  S-SW des PS). Falls echte Koordinaten auftauchen → in `geo_build.py` projizieren (wie LINAC4).

### Mobil / Teilen — ✅
Responsive (`@media max-width:860px`: einspaltig, Presets-Grid, Info-Panel als Modal),
SVG fluid (Ring am Handy voll sichtbar), **Vollbild-Ring** „⛶ Großansicht" (CSS-Overlay, kein
Fullscreen-API wg. iOS). Teilen-Artefakt `cern/CERN-Stellwerk.html` (self-contained, Share-Metas:
viewport-fit, theme-color, apple-web-app, Emoji-Favicon). QR-Generator `scripts/make_qr.mjs`
(`npm run qr "<URL>"`).

### Echtdaten — ✅
- Dimuon: CMS Open Data **Record 545** (Run2011A DoubleMu, √s=7 TeV, 12 000 Events) →
  echte Massen/Kinematik je Resonanz-Fenster + echter `topo.bg`-Untergrund.
- Higgs-Goldkanal: CMS Open Data **Record 5200** (278 4ℓ-Kandidaten 2011/2012,
  `cern/data/higgs4l/*.csv`) → echte 4ℓ-Massen (Z→4ℓ 91 + Higgs-Bump 125) + Kinematik.
- Pipeline: `scripts/build_data.py` → `cern/app/src/data.gen.js` (versioniert, deterministisch).
  Pb-Pb/QGP bleibt ehrlich als Modell markiert (kein echtes Pb-Pb im Datensatz).

### Build / Test / Dateistruktur — ✅
Konsolidiert: EIN Daten-Blob (`data.gen.js`, kein `data.js`-Spiegel mehr), kein
`build/widget.js`-Duplikat, `sat.gen.js` versioniert (sonst baut frischer Clone nicht),
Legacy-Generator + Alt-Blueprints entfernt/nach `docs/legacy/`. CLAUDE.md hat Modulindex +
Konstanten-Kette dokumentiert.

---

## 🔧 Offene Punkte (priorisiert, keiner blockierend)

**Physik / Didaktik**
- 🟡 φ(1020)-Restabweichung ~4σ am ALICE-Rand (KDE-Randglättung) — feinschliff-würdig.
- ⬜ Optional: Abort-Gap im Füllschema; animiertes Zug-Verschmelzen (Konvergenz-Tween) statt
  hartem Übergang.

**Phase-5-Cleanups (Migration-Reste)**
- ⬜ Hardcodierte SVG-Pfade (`lhc-pipe1/2`, je ~4 KB in `shell.html`) zur Laufzeit aus `App.g.LHC`
  generieren (geo-genauer Umriss kommt aus `geo.gen.js`).
- ⬜ Widget aus dem `.py`-jupytext-Spiegel ausnehmen (Spiegel nur fürs Curriculum) → keine
  166-KB-Dublette im Diff.

**TypeScript-Einführung — ✅ (Schritte 1–3 erledigt; Verträge statt raten)**
- ✅ **Schritt 1:** `jsconfig.json` (`checkJs`, lenient) + ambiente Shapes in `cern/app/src/types.d.ts`
  (`AppState`, `SpectrumProfile`/`Resonance`, `DetConfig`, `AppNamespace`). Deckte auf: `activeLayerKey`
  nie in `state` initialisiert; 8× `setAttribute(num)`; `__cernBooted`/`dataset`-Narrowing.
- ✅ **Schritt 2:** `tsc --noEmit -p jsconfig.json` als Headless-Gate in `scripts/check.sh` (rot bei
  Typfehler, verifiziert: `s.dumpign` → TS2551, Exit 1).
- ✅ **Schritt 3 KOMPLETT:** alle 9 Logik-Module `.js`→`.ts` (git-Renames, Historie erhalten);
  esbuild-Entry → `main.ts`. **0 tsc-Fehler**, 88 Tests + check.sh grün, Bundle unverändert (677 KB).
  Generierte Daten-Blobs (`data.gen.js`/`geo.gen.js`/`sat.gen.js`) bleiben **bewusst `.js`** (reine
  Daten, kein Typnutzen, würde die Python-Pipeline anfassen). `state.ts` initialisiert via
  `satisfies AppState` (fängt Init-Tippfehler an der Quelle → TS2561).
  **Zwei teure Lehren (im Playbook):** (1) JSDoc-`@type`/Casts gelten in `.js` (checkJs), werden in
  `.ts` IGNORIERT → bei der Konversion auf native Syntax umstellen (kostete einmalig 747 Folgefehler
  aus EINER Ursache: `App` fiel auf den Literaltyp zurück). (2) esbuild löst `'./x.js'` automatisch
  auf `x.ts` auf, **Vite/vitest nicht** → `.js→.ts`-Alias in `vitest.config.mjs` (einmalig, dann
  tragen beide Toolchains alle Konversionen ohne Import-Änderungen).
- ⬜ **Optionaler Rest:** `els`/`g` von `any` auf echte Element-/Geometrie-Typen heben (bewusst
  zurückgestellt — Pilot-lenient). Vorgehen + Lehren als wiederverwendbares Rezept: **`docs/PLAYBOOK.md`**.

**Tooling-Politur (aus Effizienz-Audit, agentisches Arbeiten)**
- ⬜ Satelliten-Tiles in `geo_build.py` kleiner reprocessen (~700 px + moderate Qualität):
  `sat.gen.js` ist 58 % des Bundles, weder CERN-Daten noch Physik → ~45–65 % Bundle-Ersparnis möglich.
- ⬜ `check.sh` parallelisieren (esbuild + jupytext sind unabhängig → `&`/`wait`, ~30 % schneller).
- ⬜ `vitest.config.mjs` mit Projects `unit` (physics, kein jsdom) vs. `integration` →
  schneller Mathe-Check `vitest run --project unit`.
- ⬜ Diese Datei klein halten: erledigte Detail-Chronik bleibt im `git log`, nicht hier.

---

## 🔒 Gelockte Entscheidungen (nicht neu aufrollen)

1. **Bundler JA** — esbuild (Build) + Vitest/jsdom (Test). Node-Toolchain neben Python ist okay.
2. **App = alles Interaktive/Visuelle** — Stellwerk *und* Curriculum-Visualisierungen leben in der App.
3. **Notebook-Einbettung per `<iframe srcdoc>`** — kein „inline im Output" mehr.
4. **Verifikation headless-default** (Vitest+jsdom). Browser nur Ausnahme.
5. **Modul-Modell = leichter Namespace** (`App`-Objekt in `core.js`; Properties mutieren, kein Reassign).

---

## 🚧 Invarianten (bei JEDER Änderung wahren)

- **`cern/data/physics.json` = Single Source of Truth** für Resonanzwerte (Python *und* JS lesen
  daraus via `gen_constants.py` → `data.gen.js.reso`). Nie doppelt pflegen, nie `.reso` von Hand.
- **`id="cern-v4"`-Marker** bleibt, sonst findet `sync_widget.py` die Notebook-Zelle nicht.
- **Sprache Deutsch; Physik ehrlich** (Messung vs. „kalibrierte Simulation"/„Modell" kennzeichnen).
- **nbstripout** (Git-Filter) + **jupytext** (.py-Spiegel) fürs Curriculum bleiben aktiv.
  ⚠ Falls nbstripout in einer Umgebung NICHT greift und das `.ipynb` ausgeführt wurde: vor Commit
  Outputs strippen.
- **Generierte Dateien nie von Hand editieren:** Notebook-Zelle 4, `cern/app/index.html`,
  `cern/CERN-Stellwerk.html`, `build/*`, `data.gen.js`, `geo.gen.js`, `sat.gen.js`.
- **Commits:** Feature-Branch (nicht direkt `main`), `Co-Authored-By:`-Zeile behalten.

---

## 📓 Resume-Protokoll

1. **CLAUDE.md** (Karte/Modulindex/Verifikations-Politik) + diese Datei lesen.
2. Aufgabe dem passenden **Bereich** oben zuordnen (Umsetzungsgrad + Schlüsseldateien stehen dort).
3. Klein & verifizierbar ändern → `bash scripts/check.sh` (headless-default).
4. Den Bereich + STATUS-Abschnitt aktualisieren (Umsetzungsgrad nachziehen), Datei mitcommitten.
5. Bei Scope-Unklarheit fragen, nicht raten. Gelockte Entscheidungen oben bleiben gelockt.

*Vollständige Änderungs-Chronik: `git log`. Historische Blueprints: `docs/legacy/`.*

---

## 🗺️ Anhang — Karten-Geo-Genauigkeit (Hintergrund, umgesetzt)

Der Geo-Layer ist umgesetzt (s. „Reale Ansicht / Geo"); dieser Anhang hält die **Designgründe**
fest, falls jemand die Karte erweitert:

- **Geo-Treue ⟂ Didaktik:** Maßstäbliche Größen machen die Injektoren unsichtbar (PS wäre ~4 px,
  Booster sub-px) und liegen real **nicht konzentrisch**, sondern als Cluster tangential am Rand
  (Meyrin). Darum **zwei Modi**: Didaktik (schematisch, nicht maßstäblich, animierbar) vs. Real
  (volle OSM-Geometrie, echte Größen). Beide ehrlich gelabelt.
- **Projektion:** uniformer Faktor `s = min(w/Δx, h/Δy)` + Zentrierung (NICHT X/Y unabhängig
  skalieren — das macht den runden LHC zur Ellipse). Über ~0,2° Breite ist EPSG:3857 ohnehin
  Overkill; lokal-equirektangulär wäre visuell identisch.
- **Offline-Pflicht:** Overpass/OSM-Abfragen laufen **nur** zur Build-Zeit (`geo_build.py --fetch`),
  **nie** zur Laufzeit — das Widget läuft offline im Notebook-iframe. Ergebnis ist als statische
  `geo.gen.js`/`sat.gen.js` eingecheckt.
- **LHC ist nicht perfekt rund** (real 8 Bögen + 8 Geraden) — die OSM-Form bleibt im Real-Modus.
