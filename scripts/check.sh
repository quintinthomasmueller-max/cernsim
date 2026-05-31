#!/usr/bin/env bash
# Headless-Standardprüfung (kein Browser). Nach jeder Widget-Änderung ausführen.
set -e
cd "$(dirname "$0")/.."

# Single Source of Truth: physics.json -> data.js.reso (vor dem Bündeln synchronisieren)
python3 scripts/gen_constants.py write >/dev/null && echo "✓ data.js.reso aus physics.json synchron"

python3 scripts/sync_widget.py >/dev/null
node --check build/widget.js && echo "✓ JS-Syntax (build/widget.js)"

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
echo "✓ check.sh OK"
