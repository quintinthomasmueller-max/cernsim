# 🧪 Playbook — ein Physik-Visualisierungs-Tool agentisch bauen (in dieser Form)

> Destillat aus dem CERN-Stellwerk-Projekt. Diese Anleitung beschreibt **die Form**, in der
> sich ein interaktives, didaktisches Physik-Visualisierungs-Tool **schnell und sicher mit einem
> KI-Agenten** bauen und über viele Sessions hinweg weiterentwickeln lässt — ohne dass Kontext
> im Chat verloren geht und ohne dass „schnelle Fixes" in langsamen Browser-Tests versanden.
>
> Kernidee: **Optimiere nicht den Code für den Menschen, sondern den Feedback-Loop für den
> Agenten.** Jede Entscheidung unten zahlt darauf ein: schnelle, headless, deterministische
> Verifikation + maschinenlesbare Verträge (Typen) + eine einzige Wahrheitsquelle je Sache.

---

## 0. Warum diese Form (die gemessenen Auszahlungen)

Aus diesem Projekt, konkret gemessen:

| Gate | Latenz | fängt |
|---|---|---|
| `tsc --noEmit` (Typprüfung) | **~1,4 s** | Tippfehler/falsche Shapes bei `state.*`, Profilen, Configs |
| `vitest run` (jsdom) | **~2,8 s** | Interaktions- & Physik-Logik-Regressionen |
| `check.sh` (alles, headless) | **~11 s** | die komplette Verifikation, **kein Browser** |

Der Hebel: Ein Tippfehler wie `s.dumpign` oder `sp.taget` kostete früher einen **Browser-Zyklus**
(Rebuild → Notebook/iframe öffnen → durchklicken → kaputtes Verhalten sehen → Ursache raten =
Minuten, oft flaky). Mit getypten Verträgen fällt er in **~1,4 s headless** auf, mit Namen und
„Did you mean …?". Für einen Agenten, der iterativ editiert, ist das der Unterschied zwischen
„10 schnellen Versuchen" und „1 langsamem, unsicheren".

---

## 1. Architektur-Blaupause: App-First

1. **Die Web-App ist das primäre Artefakt** (`app/src/*` als ES-Module). Sie enthält **alles
   Interaktive/Visuelle** — Steuerung, Animationen, Diagramme, Spektren.
2. **Das Notebook (oder die Doku) ist Konsument**, nicht Quelle: es bettet die **gebaute** App per
   **`<iframe srcdoc="…">`** ein. Eigener DOM/Origin → keine Script-Races, keine
   `getElementById`-Kollisionen, keine „läuft im Notebook anders als standalone"-Überraschungen.
3. **Ein Build-Bundle** (esbuild → ein self-contained IIFE) wird in drei Ziele injiziert:
   Notebook-Zelle, Standalone-`index.html`, eine Teilen-Datei (alles aus einem Sync-Skript).
4. **Geteilter Namespace statt globaler Closure:** ein importiertes `App`-Objekt
   (`App.state`/`App.els`/`App.g` + registrierte Funktionen). Module mutieren Properties, nie
   reassignen sie. Boot grabbt DOM-Refs **einmal** idempotent bei DOM-Ready (löst die Jupyter-Race).

**Sprachwahl (Lehre):** Die Runtime ist im Browser/iframe → **JS/TS ist erzwungen**, kein Rust/WASM
nötig (Performance ist bei didaktischen Tools nie der Engpass). Die Build-/Daten-Pipeline ist
**Python** (CSV/numpy-Terrain). Der eigentliche Hebel ist kein Sprachwechsel, sondern eine
**Typ-Schicht (TypeScript)** auf der JS, die man ohnehin hat.

---

## 2. Die Toolchain (und der eine Stolperstein)

- **Bundler: esbuild.** ES-Module → ein IIFE. Kompiliert TS nativ (Typen werden gestript →
  **null Runtime-Kosten**, Bundle identisch).
- **Tests: Vitest + jsdom.** Headless, deterministisch, Millisekunden. Zwei Sorten:
  Logik-Tests importieren `src/`-Module direkt; Interaktions-/Boot-Tests laden das **gebaute Bundle**
  gegen das Markup in jsdom (mit Zugriff aufs `App`-Objekt).
- **Typen: `jsconfig.json` mit `checkJs`** (lenient: `strict:false`, `noImplicitAny:false`) +
  **ambiente `types.d.ts`** mit den zentralen Shapes. `tsc --noEmit` ist ein Gate, keine .js muss
  umbenannt werden. Inkrementell später `.js`→`.ts`.
- **`satisfies <Typ>`** auf Init-/Konfig-Objektliteralen prüft sie **an der Quelle** gegen den
  Vertrag (fehlende/vertippte/überzählige Felder → Fehler mit „Did you mean …?").

> ⚠ **Stolperstein, den dieses Projekt teuer gelernt hat:** esbuild löst `import './x.js'`
> **automatisch** auf `x.ts` auf, sobald man ein Modul migriert — **Vite/vitest tut das NICHT**.
> Folge: nach der ersten `.js`→`.ts`-Konversion sind Build grün, Tests rot. **Fix einmalig** in
> `vitest.config.mjs`: relativen Importen die `.js`-Endung strippen, dann greift Vites
> Extension-Resolution (`.ts` wird gefunden, vorhandene `.js` bleiben):
> ```js
> resolve: { alias: [{ find: /^(\.{1,2}\/.*)\.js$/, replacement: '$1' }] }
> ```
> Danach funktionieren ALLE künftigen Konversionen in beiden Toolchains, ohne ein Import-Statement
> anzufassen. **Diesen Alias von Anfang an setzen** spart die ganze Verwirrung.

> ⚠ **Zweiter Stolperstein (noch teurer):** **JSDoc-Typen (`/** @type {} */`, `@param`, JSDoc-Casts)
> gelten nur in `.js`-Dateien (mit `checkJs`) — in `.ts`-Dateien werden sie IGNORIERT.** Wer in der
> checkJs-Phase den zentralen Namespace per `/** @type {AppNamespace} */` typt und dann das Modul
> auf `.ts` umbenennt, verliert die Typung schlagartig: das Objekt fällt auf seinen Literaltyp
> zurück → in diesem Projekt **747 Folgefehler aus EINER Ursache** („Property X does not exist on
> `{}`"). **Regel:** beim `.js`→`.ts`-Umstieg jede JSDoc-Annotation/-Cast auf native TS-Syntax
> heben (`const App: AppNamespace = …`, `x as T`). Danach blieben nur ~40 echte Strenge-Funde, die
> sich in vier Klassen abräumen lassen: `new Promise<void|T>(…)`, optionale Trailing-Params
> (`fn(a, b?)`), Konfig-Objekte als `Record<string, DetConfig>` annotieren (statt inferierter Union),
> und `Object.values(anyVal)` ergibt `unknown[]` → forEach-Param als `any` annotieren oder Quelle
> auf `any` setzen. **Generierte Daten-Blobs als `.js` lassen** — reine Daten, kein Typnutzen, sonst
> fasst man die Build-Pipeline an.

---

## 3. Daten-Disziplin (Wahrheit + eine Quelle)

- **Single Source of Truth je Sache.** Physikkonstanten in EINER Datei (`physics.json`); ein
  Generator spiegelt sie deterministisch nach Python UND JS (`gen_constants.py → data.gen.js.reso`).
  Nie zweimal pflegen, nie generierte Dateien von Hand editieren.
- **Generierte Daten als versioniertes ES-Modul** (`data.gen.js`/`geo.gen.js`), deterministisch aus
  den Rohdaten gebaut — eingecheckt, damit ein frischer Clone/CI ohne Netz baut. Netz-Abfragen
  (z. B. Overpass/WMS) laufen **nur zur Build-Zeit**, nie zur Laufzeit (das Tool läuft offline).
- **Echte Daten ehrlich kennzeichnen.** Messung vs. „kalibrierte Simulation" vs. „Modell" überall
  deklarieren (Histogramm-Kopf, Captions, Status). Bei einem Beweis-Mechanismus (Entdeckung) die
  **Nullhypothese** als Overlay zeigen — das ist didaktisch der Kern, nicht Beiwerk.
- **Bytes ≠ Code-Zeilen.** Was „groß" wirkt, ist oft eingebettete Asset-Last (z. B. ein
  Satelliten-Basemap-Bild), nicht die Logik. Erst messen (Bytes pro Datei/Block), dann den größten,
  nicht-essenziellen Block angehen (Bild kleiner reprocessen) — Frontend & echte Daten unberührt.

---

## 4. Verifikations-Politik (spart Quota & Zeit)

- **Standard = headless.** Ein `check.sh` komponiert die Gates in einer Kette, jede mit ✓/✗:
  Konstanten-Sync → Bundle-Build → `node --check` → Notebook-Validierung → **`tsc`** → **vitest**.
  Jede Stufe bricht laut ab (Exit ≠ 0) mit Hinweis, wie man Details bekommt.
- **Browser nur auf Anfrage oder bei reinen Render-/Layout-Änderungen.** Nie als Default, nie zum
  Logik-Prüfen. Lange End-to-End-Abläufe (Animationen) nie scripten, um Logik zu testen — Logik
  headless testen (Debug-Hook/direkter Modul-Import).
- **Determinismus erzwingen:** keine Timestamps in generierte Artefakte (kein tägliches Git-Rauschen);
  Zeit über eine geklemmte, injizierbare Zeitbasis statt `Date.now()` direkt.

---

## 5. Resumierbarkeit über Sessions (das „lebende Zustands-Dokument")

- **EIN autoritatives Status-Dokument** (`docs/MIGRATION.md` / hier dieses Repo) hält pro Bereich:
  *Umsetzungsgrad (✅/🟡/⬜) + wie es funktioniert + Schlüsseldateien*. Der Chat darf jederzeit
  gecleart werden — der Zustand lebt im Repo, nicht im Verlauf.
- **Ein Modulindex** in der Agenten-Anleitung (`CLAUDE.md`): pro Modul die exportierten
  Schlüsselfunktionen → ein Agent springt zur richtigen Datei mit 0–1 Lesevorgängen statt 3–4.
- **Detail-Chronik gehört in `git log`**, nicht ins Status-Dokument (das bleibt klein & orientierend).
- **Konventionen explizit** machen: Sprache, „keine Emojis im nutzersichtbaren Frontend-Text",
  Physik-Ehrlichkeit, „kleine Fixes direkt + headless-Check, Plan-Modus nur für Großes".

---

## 6. Bootstrap-Checkliste (neues Tool, Tag 1)

1. **Repo-Skelett:** `app/src/` (Module), `app/shell.html` + `styles.css`, `app/esbuild.mjs`
   (Entry = `main.js`, `bundle:true`, `format:'iife'`), `package.json` (scripts: `build`,
   `typecheck`, `test`).
2. **Namespace zuerst:** `core.js` mit `App = { state:{}, els:{}, g:{} }` + Helpers (`$`, `sleep`).
   `main.js` bootet idempotent bei DOM-Ready, grabbt Refs in `App.els`.
3. **Typen ab Zeile 1:** `jsconfig.json` (`checkJs`, lenient) + `types.d.ts` mit `AppState` &
   den 2–3 Kern-Shapes deiner Domäne. `App` als getypten Namespace annotieren. `App.state` via
   `satisfies AppState` initialisieren.
4. **Toolchain angleichen:** `vitest.config.mjs` mit jsdom **und dem `.js`→`.ts`-Alias** (§2) —
   sofort, nicht erst nach dem ersten Schmerz.
5. **`check.sh` als Gate-Kette** (§4). In CI/„nach jeder Änderung" verdrahten.
6. **Daten-Pipeline:** Rohdaten → Generator → versioniertes `*.gen.js`. Konstanten in einer
   `physics.json`, gespiegelt. Provenienz-/Ehrlichkeits-Labels von Anfang an.
7. **Status-Dokument + Modulindex** anlegen (§5), bevor der erste Chat gecleart wird.
8. **Erst dann Features bauen** — jeweils: ändern → `check.sh` → Status-Dokument nachziehen.
   Browser nur 1× je Feature, auf Sicht.

---

## 7. Die Reihenfolge, die sich bewährt hat

Architektur (App-First + Bundle + iframe) → headless Test-Suite → **Typ-Gate** → Daten-Ehrlichkeit
→ Feinschliff (Didaktik/UX) → Asset-/Tooling-Politur. Die Typen früh: sie sind das billigste,
am häufigsten zahlende Sicherheitsnetz fürs agentische Iterieren — und das Einzige, das einem
Agenten *Verträge* gibt, statt ihn alles lesen zu lassen.

*Konkrete Referenz-Implementierung: dieses Repo. Status/Ist-Zustand: `docs/MIGRATION.md`.
Arbeitsanleitung/Konventionen: `CLAUDE.md`.*
