#!/usr/bin/env python3
"""
sync_widget.py — baut die Widget-Quellen aus cern/app/ wieder zusammen.

Quelle der Wahrheit: cern/app/{*.js, styles.css, shell.html}.
Erzeugt:
  1. Notebook-Zelle 4  ->  display(HTML(r'''<gebündeltes Widget>'''))   (self-contained)
  2. build/widget_bundle.html  ->  Standalone-Datei für schnellen Browser-Smoke-Test
  3. cern/app/index.html       ->  Standalone-App mit verlinktem CSS/JS (Dual-Existenz)

Nach jeder Änderung an cern/app/*: `python3 scripts/sync_widget.py` ausführen.
Headless-Verifikation: `bash scripts/check.sh`.
"""
import json, os, sys, shutil, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP  = os.path.join(ROOT, 'cern', 'app')
NB   = os.path.join(ROOT, 'cern', 'notebooks', 'CERN_Beschleuniger_Schaltzentrale.ipynb')
BUILD= os.path.join(ROOT, 'build')
BUNDLE = os.path.join(BUILD, 'app.bundle.js')   # esbuild-Ausgabe (cern/app/src/* → IIFE)

def read(p): return open(os.path.join(APP, p)).read()

def esbuild():
    """cern/app/src/* → build/app.bundle.js (ein self-contained IIFE).
    Ersetzt die alte IIFE-Slice-Konkatenation (Phase 1 der Migration)."""
    node = shutil.which('node')
    if not node:
        raise RuntimeError('node nicht gefunden – für esbuild-Bundle nötig')
    subprocess.run([node, os.path.join(APP, 'esbuild.mjs')], cwd=ROOT, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def build_js():
    return open(BUNDLE).read()

def build_inner():
    """Inhalt für die Notebook-Zelle: CSS+JS inline (self-contained)."""
    shell = read('shell.html')
    css   = read('styles.css')
    js    = build_js()
    return (shell.replace('{{STYLES}}', '<style>' + css + '</style>')
                 .replace('{{SCRIPT}}', '<script>' + js + '</script>'))

def build_standalone():
    """Standalone-App für cern/app/index.html: esbuild-Bundle inline, CSS verlinkt."""
    shell = read('shell.html')
    body  = (shell.replace('{{STYLES}}', '')
                  .replace('{{SCRIPT}}', '<script>' + build_js() + '</script>'))
    return ('<!doctype html><html><head><meta charset="utf-8">'
            '<link rel="stylesheet" href="styles.css"></head><body>'
            + body + '</body></html>')

def main():
    # Resonanztabelle aus physics.json in data.js.reso spiegeln (Single Source of Truth),
    # damit das gebündelte Widget garantiert dieselben Werte wie Python nutzt.
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import gen_constants
        gen_constants.write()
    except Exception as e:
        print(f"⚠ gen_constants übersprungen ({e}) – data.js.reso evtl. nicht synchron")

    # Bundle frisch bauen (liest cern/app/src/* + spiegelt data.js → src/data.gen.js).
    esbuild()

    inner = build_inner()
    assert "'''" not in inner, "Inhalt enthält ''' — bricht den Python-Rohstring!"

    # 1) Notebook-Zelle 4
    nb = json.load(open(NB))
    wi = next(i for i, c in enumerate(nb['cells']) if "cern-v4" in ''.join(c['source']))
    cell = "display(HTML(r'''" + inner + "'''))\n"
    nb['cells'][wi]['source'] = cell.splitlines(keepends=True)
    nb['cells'][wi]['outputs'] = []
    nb['cells'][wi]['execution_count'] = None
    json.dump(nb, open(NB, 'w'), ensure_ascii=False, indent=1)

    # 2) build/widget_bundle.html + build/widget.js (für node --check)
    os.makedirs(BUILD, exist_ok=True)
    open(os.path.join(BUILD, 'widget_bundle.html'), 'w').write(
        '<!doctype html><html><head><meta charset="utf-8"></head><body>' + inner + '</body></html>')
    open(os.path.join(BUILD, 'widget.js'), 'w').write(build_js())

    # 3) cern/app/index.html
    open(os.path.join(APP, 'index.html'), 'w').write(build_standalone())

    print(f"sync OK | Zelle 4: {len(inner):,} B | JS: {len(build_js()):,} B")
    # optionaler Byte-Vergleich gegen Referenz
    ref = sys.argv[1] if len(sys.argv) > 1 else None
    if ref and os.path.exists(ref):
        same = open(ref).read() == inner
        print("Byte-identisch zur Referenz:", "✅ JA" if same else "❌ NEIN")
        sys.exit(0 if same else 2)

if __name__ == '__main__':
    main()
