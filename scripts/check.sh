#!/usr/bin/env bash
# Headless-Standardprüfung (kein Browser). Nach jeder Widget-Änderung ausführen.
set -e
cd "$(dirname "$0")/.."

# Single Source of Truth: physics.json -> src/data.gen.js.reso (vor dem Bündeln synchronisieren)
python3 scripts/gen_constants.py write >/dev/null && echo "✓ data.gen.js.reso aus physics.json synchron"

python3 scripts/sync_widget.py >/dev/null
node --check build/app.bundle.js && echo "✓ JS-Syntax (build/app.bundle.js)"

# jupytext: .py-Spiegel mit dem (gerade gebündelten) .ipynb synchron halten
if python3 -c "import jupytext" 2>/dev/null; then
  python3 -m jupytext --sync cern/notebooks/CERN_Beschleuniger_Schaltzentrale.ipynb >/dev/null 2>&1 \
    && echo "✓ jupytext --sync (.py-Spiegel aktuell)"
else
  echo "⚠ jupytext nicht installiert – .py-Spiegel NICHT aktualisiert (pip install jupytext)"
fi

python3 - <<'PY'
import json, ast, nbformat as nf
nb = json.load(open('cern/notebooks/CERN_Beschleuniger_Schaltzentrale.ipynb'))
nf.validate(nb)
for c in nb['cells']:
    if c['cell_type'] == 'code':
        ast.parse(''.join(c['source']))
print("✓ nbformat valid + alle Code-Zellen geparst")
PY

# TypeScript-Typprüfung (checkJs-Pilot, headless): prüft cern/app/src gegen die Shapes
# in src/types.d.ts (AppState/SpectrumProfile/DetConfig). Build/Runtime unberührt.
if [ -x node_modules/.bin/tsc ]; then
  node_modules/.bin/tsc --noEmit -p jsconfig.json >/dev/null 2>&1 && echo "✓ tsc --noEmit (Typprüfung, checkJs)" \
    || { echo "✗ Typprüfung FEHLGESCHLAGEN — Details: npm run typecheck"; exit 1; }
else
  echo "⚠ tsc übersprungen (npm install ausführen, um die Typprüfung zu aktivieren)"
fi

# Headless-Interaktions-/Logik-Tests (Vitest + jsdom). Bundle ist oben bereits gesynct.
if [ -d node_modules ] && command -v npx >/dev/null 2>&1; then
  npx vitest run >/dev/null 2>&1 && echo "✓ vitest headless tests (jsdom)" \
    || { echo "✗ vitest headless tests FEHLGESCHLAGEN — Details: npx vitest run"; exit 1; }
else
  echo "⚠ vitest übersprungen (npm install ausführen, um Headless-Tests zu aktivieren)"
fi

echo "✓ check.sh OK"
