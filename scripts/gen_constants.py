#!/usr/bin/env python3
"""
gen_constants.py — hält die Resonanztabelle in cern/app/src/data.gen.js synchron zur
Single Source of Truth cern/data/physics.json.

Hintergrund: Die PDG-Resonanzen (Masse, Breite, Farbe) existierten doppelt —
in Python (cern_utils.RESONANZEN) und im JS-Widget (CERN_REAL.reso). Diese
Doppelpflege ist driftanfällig. physics.json ist jetzt die einzige Quelle:
  * Python liest sie via cern_utils._load_resonanzen()
  * data.gen.js.reso wird hier aus ihr GENERIERT (Widget-Untermenge).

Befehle:
  python3 scripts/gen_constants.py verify   # Default: prüft Sync, Exit 2 bei Drift
  python3 scripts/gen_constants.py write     # patcht data.gen.js.reso aus physics.json

Nur der "reso"-Block in data.gen.js wird angefasst (die echten CMS-Datenarrays
bleiben unberührt). Bei korrektem Sync ist die Ersetzung byte-identisch.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHYSICS = os.path.join(ROOT, "cern", "data", "physics.json")
DATA_JS = os.path.join(ROOT, "cern", "app", "src", "data.gen.js")

# Matcht genau das reso-Objekt: "reso":{ ... } (keine verschachtelten Klammern darin).
_RESO_RE = re.compile(r'"reso":\{[^}]*\}')


def widget_reso() -> dict:
    """Baut die Widget-Untermenge {label: [m, breite, farbe]} aus physics.json.

    Reihenfolge folgt der Definition in physics.json (dict ist insertion-ordered),
    damit die erzeugte JS-Zeile stabil/diff-arm bleibt.
    """
    with open(PHYSICS, encoding="utf-8") as f:
        physik = json.load(f)
    reso = {}
    for eintrag in physik["resonanzen"].values():
        label = eintrag.get("widget")
        if not label:
            continue  # nicht im Widget sichtbar (z. B. psi(2S), Upsilon2S/3S)
        reso[label] = [eintrag["m"], eintrag["breite"], eintrag["farbe"]]
    return reso


def reso_fragment() -> str:
    """Erzeugt den exakten JS-Textbaustein '"reso":{...}' (kompakt, wie in data.gen.js)."""
    return '"reso":' + json.dumps(widget_reso(), separators=(",", ":"), ensure_ascii=False)


def _split() -> tuple:
    """Liest data.gen.js und gibt (quelltext, treffer, neues_fragment) zurück."""
    src = open(DATA_JS, encoding="utf-8").read()
    treffer = _RESO_RE.search(src)
    if not treffer:
        raise RuntimeError('"reso"-Block in cern/app/src/data.gen.js nicht gefunden')
    return src, treffer, reso_fragment()


def write() -> bool:
    """Patcht data.gen.js.reso aus physics.json. Gibt True zurück, wenn geändert."""
    src, treffer, neu = _split()
    if treffer.group(0) == neu:
        return False
    open(DATA_JS, "w", encoding="utf-8").write(src[: treffer.start()] + neu + src[treffer.end():])
    return True


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "verify"
    try:
        src, treffer, neu = _split()
    except RuntimeError as e:
        print(f"✗ {e}", file=sys.stderr)
        return 1
    aktuell = treffer.group(0)

    if cmd == "verify":
        if aktuell == neu:
            print("✓ data.gen.js.reso ist synchron zu physics.json")
            return 0
        print("✗ DRIFT: data.gen.js.reso weicht von physics.json ab.", file=sys.stderr)
        print(f"  data.gen.js:     {aktuell}", file=sys.stderr)
        print(f"  physics.json:{neu}", file=sys.stderr)
        print("  Beheben mit: python3 scripts/gen_constants.py write", file=sys.stderr)
        return 2

    if cmd == "write":
        print("✓ data.gen.js.reso aus physics.json neu geschrieben" if write()
              else "✓ data.gen.js.reso bereits synchron — keine Änderung")
        return 0

    print(f"Unbekannter Befehl: {cmd!r} (verify|write)", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
