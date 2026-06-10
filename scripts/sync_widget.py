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

def build_share():
    """EINE vollständig selbstständige HTML-Datei (CSS+JS inline) zum Teilen —
    läuft per Doppelklick ODER gehostet in jedem Browser (Desktop + Handy),
    ohne weitere Dateien. Meta = mobil-/Web-tauglich (Notch, Theme, „Zum
    Startbildschirm", Emoji-Favicon ohne externe Datei)."""
    icon = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
            "viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%E2%9A%9B%EF%B8%8F%3C/text%3E%3C/svg%3E")
    return ('<!doctype html><html lang="de"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            '<meta name="theme-color" content="#131a24">'
            '<meta name="apple-mobile-web-app-capable" content="yes">'
            '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">'
            '<meta name="apple-mobile-web-app-title" content="CERN-Schaltzentrale">'
            '<link rel="icon" href="' + icon + '">'
            '<title>CERN-Schaltzentrale — interaktives Modell</title>'
            '<style>html,body{margin:0;background:#131a24}</style></head><body>'
            + build_inner() + '</body></html>')

# Höhen-Reporter (läuft IM iframe-Dokument): meldet die tatsächliche Inhaltshöhe
# per postMessage an die Notebook-Seite, damit der Loader das iframe exakt skaliert.
RESIZE_REPORTER = (
    "<script>(function(){function r(){try{var h=Math.ceil("
    "document.getElementById('cern-v4')?document.getElementById('cern-v4').getBoundingClientRect().height"
    ":document.documentElement.scrollHeight);"
    "parent.postMessage({cernV4Height:h},'*');}catch(e){}}"
    "window.addEventListener('load',r);setTimeout(r,250);setTimeout(r,1200);"
    "if(window.ResizeObserver){new ResizeObserver(r).observe(document.body);}})();</script>"
)

FALLBACK_H = 1040  # px – greift, falls postMessage in einer Umgebung blockiert ist

def esc_srcdoc(s):
    """Für das srcdoc-Attribut nur & und das Anführungszeichen escapen
    (< und > sind in Attributwerten zulässig und bleiben unangetastet)."""
    return s.replace('&', '&amp;').replace('"', '&quot;')

def build_iframe_cell(inner):
    """Notebook-Zelle als Mini-Loader: bettet die gebaute App per <iframe srcdoc> ein.
    Eigener DOM/Origin → keine Jupyter-Script-Race, keine getElementById-Kollisionen.
    Der `cern-v4`-Marker bleibt im (escapeten) srcdoc enthalten → Zellen-Finder greift."""
    doc = ('<!doctype html><html><head><meta charset="utf-8">'
           '<style>html,body{margin:0;background:#131a24}</style></head><body>'
           + inner + RESIZE_REPORTER + '</body></html>')
    iframe = ('<iframe id="cern-v4-frame" title="CERN Stellwerk" scrolling="no" '
              'style="width:100%;height:' + str(FALLBACK_H) + 'px;border:0;display:block;'
              'overflow:hidden;background:#131a24" '
              'srcdoc="' + esc_srcdoc(doc) + '"></iframe>')
    listener = ("<script>(function(){var f=document.getElementById('cern-v4-frame');"
                "if(!f)return;window.addEventListener('message',function(e){"
                "if(e.source===f.contentWindow&&e.data&&e.data.cernV4Height){"
                "f.style.height=(e.data.cernV4Height+6)+'px';}});})();</script>")
    return iframe + listener

def main():
    # Echtdaten-Blob cern/app/data.js aus der echten CMS-CSV regenerieren (maximal
    # viel echte Massen/Kinematik; reso aus physics.json). Single Source bleibt gewahrt.
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    try:
        import build_data
        build_data.build()
    except Exception as e:
        print(f"⚠ build_data übersprungen ({e}) – cern/app/data.js evtl. veraltet")
    # Resonanztabelle aus physics.json in data.js.reso spiegeln (Single Source of Truth),
    # damit das gebündelte Widget garantiert dieselben Werte wie Python nutzt (no-op nach build_data).
    try:
        import gen_constants
        gen_constants.write()
    except Exception as e:
        print(f"⚠ gen_constants übersprungen ({e}) – data.js.reso evtl. nicht synchron")

    # Bundle frisch bauen (liest cern/app/src/* + spiegelt data.js → src/data.gen.js).
    esbuild()

    inner = build_inner()

    # 1) Notebook-Zelle 4 = Mini-Loader (iframe srcdoc). Phase 2 der Migration:
    #    die App lebt in einem isolierten iframe-Dokument (eigener DOM/Origin).
    payload = build_iframe_cell(inner)
    assert "'''" not in payload, "Inhalt enthält ''' — bricht den Python-Rohstring!"
    nb = json.load(open(NB))
    wi = next(i for i, c in enumerate(nb['cells']) if "cern-v4" in ''.join(c['source']))
    cell = "display(HTML(r'''" + payload + "'''))\n"
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

    # 4) cern/CERN-Stellwerk.html — DIE eine selbstständige Datei zum Teilen/Elternabend
    #     (CSS+JS inline, didaktisch optimiert). Eine separate „-Elternabend"-Kopie gab es
    #     früher, war aber bytegleich → entfernt (überflüssige Datei).
    share = build_share()
    open(os.path.join(ROOT, 'cern', 'CERN-Stellwerk.html'), 'w').write(share)

    print(f"sync OK | Zelle 4 (iframe): {len(payload):,} B | App-Doc: {len(inner):,} B | JS: {len(build_js()):,} B | Teilen-Datei: {len(share):,} B")
    # optionaler Byte-Vergleich gegen Referenz
    ref = sys.argv[1] if len(sys.argv) > 1 else None
    if ref and os.path.exists(ref):
        same = open(ref).read() == inner
        print("Byte-identisch zur Referenz:", "✅ JA" if same else "❌ NEIN")
        sys.exit(0 if same else 2)

if __name__ == '__main__':
    main()
