# AGENTS.md — Arbeitsanleitung für KI-Agenten (CERN-Projekt)

Didaktisches Jupyter-Notebook (Begabtenkurs Teilchenphysik): 7-teiliges Curriculum mit echten
CMS-Open-Data + eingebettetem interaktivem „Stellwerk"-Widget (HTML/JS-Canvas).
Hauptdatei: `cern/notebooks/CERN_Beschleuniger_Schaltzentrale.ipynb`.

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

## Widget editieren
- **Jetzt (vor Refactor)**: Zelle-4-String via Python-Patch-Skript (`rep()` mit exakten Matches,
  große Blöcke per Anker-Slicing). Fragil bei Whitespace → exakte Strings aus dem extrahierten
  `/tmp/cell3.html` nehmen, nicht abtippen.
- **Nach Refactor**: Quelldateien unter `cern/app/` direkt mit dem Edit-Tool; `scripts/sync_widget.py`
  baut die Notebook-Zelle neu. → siehe `docs/agent-workflow-plan.md`.

## Standard-Befehle
```
# Widget-JS extrahieren + Syntax prüfen (headless)
python3 - <<'PY'
import json,re; nb=json.load(open('cern/notebooks/CERN_Beschleuniger_Schaltzentrale.ipynb'))
w=next(c for c in nb['cells'] if "cern-v4" in ''.join(c['source'])); s=''.join(w['source'])
open('/tmp/widget.js','w').write(re.search(r'<script>(.*)</script>',s,re.S).group(1))
PY
node --check /tmp/widget.js
# Notebook validieren + alle Code-Zellen parsen
python3 -c "import json,ast,nbformat as nf; nb=json.load(open('cern/notebooks/CERN_Beschleuniger_Schaltzentrale.ipynb')); nf.validate(nb); [ast.parse(''.join(c['source'])) for c in nb['cells'] if c['cell_type']=='code']; print('OK')"
```

## Commits
- Branch `feat/echte-cern-daten-event-display`. **Outputs vor Commit leeren** (Trust + Größe).
- `.DS_Store` und `cern/resources/ai_studio_code (5).html` nicht committen (nicht von uns).
- `Co-Authored-By:`-Zeile beibehalten.

## Konventionen
- Sprache: Deutsch. Physik ehrlich (Messung vs. „kalibrierte Simulation" kennzeichnen).
- Plan-Modus nur für große/mehrdeutige Aufgaben; kleine Fixes direkt + headless-Check.
- Antworten knapp halten; keine großen Code-Blöcke/Tabellen echoen.
