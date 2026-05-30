#!/usr/bin/env bash
# Headless-Standardprüfung (kein Browser). Nach jeder Widget-Änderung ausführen.
set -e
cd "$(dirname "$0")/.."

python3 scripts/sync_widget.py >/dev/null
node --check build/widget.js && echo "✓ JS-Syntax (build/widget.js)"

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
