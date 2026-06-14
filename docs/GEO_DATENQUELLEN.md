# Geo-Datenquellen für den Injektor-Komplex (Reale Ansicht)

Kontext: Der Injektor-Zoom (`inj_svg_window` in `scripts/geo_build.py` /
`geo.ts#drawInjector`) zeichnet PS/PSB/LINAC4 aus groben OSM-Ways; **LEIR,
LINAC2/3 und die internen Transferlinien fehlen oder sind nur schematisch**
(vgl. CLAUDE.md: „LEIR/LINAC3 ∉ OSM → schematisch", „TI 2/8 approx.").
Frage: aus den Lageplänen exakte Daten ziehen ODER eine bessere Quelle finden.

**Kurzantwort:** Es gibt eine bessere, maschinenlesbare Quelle — **acc-models**
(CERN, öffentlich, vermessungs­genau). Die gescannten Lagepläne sind damit nur
noch Fallback bzw. Plausibilitätskontrolle, kein Nachzeichnen nötig.

---

## Ist-Zustand: was in OSM steht (und was nicht)

In OSM real verortet (WGS84), aktuell von der Pipeline als Einzel-Ways geholt:

- LHC `310046324`, SPS `66473762`, PS `174646428`, PSB `309914733`
- Transferlinien: TT2-TT10 `317804190`, PS↔PSB `317804187`, TI8 `317804189`,
  TT60-TI2 `317804188`, SPS-North `66473761`

**Nicht in OSM:** alle LINACs, LEIR, AD, AWAKE, n-TOF (Quelle: OSM-Wiki CERN).
→ Genau die fehlenden Stücke (LINAC2/3/4, LEIR, BT/BTP) sind unser Problem.

Quick win unabhängig vom Rest: statt der Einzel-Ways die Sammelabfrage nutzen —
holt alle gemappten Beschleuniger-Korridore in einem Request:

```overpassql
way[highway=corridor](46.2,5.7,46.4,6.2); (._;>;); out body;
```

---

## Rang 1 (Empfehlung): acc-models — exakte MAD-X-/Survey-Geometrie

`https://gitlab.cern.ch/acc-models` — öffentlich, klonbar **ohne Login**
(`git clone https://gitlab.cern.ch/acc-models/acc-models-psb.git`), zusätzlich
gespiegelt auf CERN-EOS (`/eos/project/a/acc-models/public/…`) und AFS. Es ist
der offizielle **Nachfolger der alten Seite `cern-accelerators-optics`**, die
genau unsere fehlenden Linien aufgelistet hatte:

- **LINAC2 → BOOSTER** (LT, LTB, BI)
- **LINAC4** (LINAC4 → LT)
- **BT/BTP/BTM** (Booster → PS)
- **LEIR-Linien** (LINAC3 → LEIR)
- TT2 / TT10 … plus die Ringe PS, PSB, LEIR, AD, ELENA.

**Warum exakt:** Die MAD-X-Sequenzen tragen die echten Element-Abstände; der
MAD-X-Befehl `SURVEY` erzeugt daraus globale Koordinaten (X, Z, θ) jedes
Magneten im CERN-Survey-Frame. Das ist Vermessungsdaten-Niveau — kein
Abzeichnen, kein Schätzen.

**Verfahren (fügt sich in die bestehende Pipeline):**

1. Repo klonen, Sequenz mit MAD-X `SURVEY` rechnen → Tabelle X/Z/θ pro Element
   (oder eine bereits mitgelieferte `survey*.tfs` direkt parsen).
2. acc-models liefert die **relative** Geometrie im lokalen Frame. Den
   **absoluten** Geo-Bezug liefert OSM: die in beiden Quellen vorhandenen Anker
   (PS-Ring-Zentrum, PSB-Zentrum, TT2-Richtung) → eine 2D-Ähnlichkeits­trans­for­ma­tion
   (Rotation + Skalierung + Translation) bildet den lokalen Frame auf WGS84 ab.
3. Danach wie gehabt über `make_transform`/Web-Mercator → SVG. Praktisch: ein
   Helfer `scripts/accmodels_build.py` analog zu `geo_build.py`, Ausgabe als
   weiteres `*.gen.js`-Artefakt.

Ergebnis: LEIR, LINAC2/3/4, BT/BTP exakt, in echten Koordinaten, reproduzierbar,
offline baubar — konsistent mit dem LHC-Anker des restlichen Overlays.

### Umsetzung (implementiert + verifiziert)

`scripts/accmodels_build.py` parst MAD-X-Survey-TFS, erkennt die horizontale Ebene
(X,Z; Y vertikal) und georeferenziert per 2D-Ähnlichkeit (Umeyama) → `inj.gen.js`.

**Die entscheidende Lektion zur Georeferenzierung** (erst falsch, dann korrigiert):

- *Erster Versuch (2 Anker PS+PSB) = falsch.* PS- und PSB-Zentrum liegen im SVG nur
  ~6 px auseinander → die 2-Punkt-Ähnlichkeit ist **rang-defizient**: die Skala wird
  unzuverlässig (PS schrumpfte auf 3,6 px statt 4,3 → die OSM-TT-Linie zur SPS riss ab
  → „PS und SPS nicht connected"), und Drehung/Händigkeit **quer** zur PS-PSB-Achse ist
  beliebig. Ergebnis: nur LEIR bewegte sich, der Cluster stand falsch.
- *Unabhängiger Befund:* die **OSM-PSB-Lage liegt ~52° falsch** (OSM zeichnet PSB
  NORDWESTLICH der PS; die acc-models-Survey sagt eindeutig **NÖRDLICH**). PSB als
  OSM-Anker zu nehmen, propagierte diesen Fehler.
- *Lösung = LANGE BASISLINIE.* Die SPS→LHC-Transferlinien **TI2/TI8** (aus
  `acc-models-tls`, vorgerechnete Survey-TFS) enden an den LHC-Insertionen **IP2
  (ALICE) / IP8 (LHCb)** — beide in OSM gut verortet. 3-Anker-Fit **PS + IP2 + IP8**
  bestimmt Skala, Drehung UND Händigkeit robust (RMS ~2–4 px über die GANZE Karte);
  Translation danach hart auf das OSM-PS-Zentrum gepinnt (nahtlose OSM-Integration).
  Damit sind PS/PSB/LEIR + Transferlinien vermessungsgenau relativ zueinander UND
  korrekt zum LHC verankert.

Verifiziert (numpy gegen Rohdaten + Browser, Reale Ansicht → Injektor-Zoom):
**PS R=100,0 m exakt** (→ 4,38 px), PSB R=25,0 m **nördlich** der PS (Survey, korrigiert
OSM), **LEIR R=12,0 m, 21 m vom PS-Zentrum → INNERHALB des PS-Rings** (frühere LEAR-Halle),
LINAC3→LEIR-Linie (`survey_leir_injection.tfs`) endet an LEIR. Die OSM-TT-Linie berührt
den PS-Ring wieder (Spalt −0,1 px) → PS↔SPS verbunden. Selbsttest
`scripts/accmodels_build.py --selftest` → 11/11 PASS (inkl. „2-Anker scheitert,
3-Anker trägt"). `check.sh` grün (esbuild + tsc + 88 vitest).

Bake (Netz nur in Schritt 1, lokal; braucht `numpy`+`cpymad` — venv unter `scratch/venv`):

```
scratch/venv/bin/python scripts/accmodels_build.py --fetch   # klont ps/psb/leir/tls
scratch/venv/bin/python scripts/accmodels_build.py           # → cern/app/src/inj.gen.js
```

Noch offen (separat): **SPS-/LHC-RING-Formen** kommen weiter aus OSM — acc-models liefert
sie nur als `.seq` (kein Survey-TFS, keine globalen Init-Bedingungen committet), und die
TI/TT-Transferlinien georeferenzieren bereits konsistent dazu. `cpymad` ist installiert,
ein MAD-X-Lauf war aber **nicht nötig** (acc-models-tls hat die Transferlinien-Surveys
vorberechnet). Reale interne Transferlinien (BT/BTP PSB→PS, LEIR→PS) sind verfügbar und
können die schematischen Strahllinien in `geo.ts` ersetzen.

---

## Rang 2: Lagepläne georeferenzieren (Fallback / ohne MAD-X)

Wenn der acc-models-Weg zu aufwändig ist: die Pläne **nicht frei nachzeichnen**,
sondern gegen die OSM-Anker einpassen.

- **Methode:** ≥3 Passpunkte, die im Plan UND in OSM (echte Koordinaten)
  vorkommen — PS-Ring, PSB-Ring, TT2, LINAC4-Gebäude. Affine/Ähnlichkeits­trans­for­ma­tion
  Pixel → WGS84 (QGIS-Georeferencer oder ein kleines `skimage`/`numpy`-Skript).
  Dann die fehlenden Elemente (LEIR, LINAC2/3) im Plan digitalisieren → echte
  lon/lat. Vorteil: kein CERN-Login, voll reproduzierbar, nutzt vorhandene Anker.

- **Bild 1** (PS-Komplex-Schema, 100-m-Balken): nur grob maßstabsgetreu und
  stilisiert → form-/topologie-treu, ~10 m genau. Für den didaktischen Zoom ok,
  aber **nicht** vermessungsgenau.
- **Bild 2** (LINAC4→PSB „Green Field", BHZ20/30, 35°-Bögen): technisch genau
  für genau diese Linie. Quelle = CERN-AB-Note-2008-036 bzw. „Update of the
  Linac4-PSB Transfer Line" (CDS-Record 1326339). **Tipp:** das Original-PDF
  (Vektor) von CDS holen statt des Screenshots.
- **Bild 3** (3D-Render): perspektivisch/schräg → nur visuelle Referenz,
  **nicht** georeferenzierbar.

---

## Rang 3: CERN-GIS (gis.cern.ch / maps.cern.ch)

Autoritativ inkl. Untergrund, aber die Fach-Layer sind **login-pflichtig**
(CERN-Account; Betrieb durch SCE/Esri-ArcGIS). Öffentlich frei ist nur ein
POI-Layer. Nur sinnvoll, falls CERN-Zugang vorhanden ist — dann dort messen/
exportieren.

---

## Rang 4: Parametrische Rekonstruktion

Aus publizierten Kennzahlen bauen und an bekannten Ankern platzieren:
PS U = 628.3 m (R ≈ 100 m), PSB R ≈ 25 m (4 gestapelte Ringe), LINAC2 ≈ 30 m,
LINAC4 ≈ 86 m, Injektionswinkel, 35°-Bögen (aus Bild 2). Exakt, wo Parameter
publiziert sind; guter Lückenfüller für Elemente, die auf keinem Plan sauber
abgreifbar sind.

---

## Fazit

Bester Weg = **acc-models (Rang 1)** für die exakte Geometrie der fehlenden
Elemente, ergänzt um die **OSM-Sammelabfrage** für das bereits Gemappte; die
Lageplan-Georeferenzierung (Rang 2) dient nur als Kontrolle/Lückenfüller. Bild 2
als Vektor von CDS ziehen; Bild 1 und 3 **nicht** für Präzision nachzeichnen.

### Quellen

- OSM-Wiki CERN (gemappte/fehlende Ways): <https://wiki.openstreetmap.org/wiki/CERN>
- acc-models GitLab-Gruppe (öffentlich): <https://gitlab.cern.ch/acc-models>
- acc-models-psb: <https://gitlab.cern.ch/acc-models/acc-models-psb>
- acc-models Web (Browser-Ansicht): <https://acc-models.web.cern.ch/acc-models/>
- Alte Optics-Seite (Linien-Index, Vorgänger): <https://cern-accelerators-optics.web.cern.ch/>
- Linac4-PSB-Transferlinie (Bild 2): <https://cds.cern.ch/record/1326339>
- CERN-GIS (SCE): <https://sce-dep.web.cern.ch/geographic-information-system-gis>
