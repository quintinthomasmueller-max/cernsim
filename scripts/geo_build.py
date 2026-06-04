#!/usr/bin/env python3
"""
geo_build.py — erzeugt das GEO-genaue Karten-Overlay (Phase 4 der Migration).

Pipeline (siehe docs/MIGRATION.md, Anhang „Karten-Geo-Genauigkeit"):
  1. OSM-Rohdaten (Overpass, `out geom;`) aus scratch/geo_raw.json laden
     (Fetch-Helfer: `python3 scripts/geo_build.py --fetch`).
  2. Web-Mercator-Projektion (lon/lat → x/y), konform → Kreise bleiben Kreise.
  3. **Uniforme** Ähnlichkeitstransformation (fixt den Bug der Spec: KEINE getrennte
     X/Y-Normierung): am echten LHC-Ring ausgerichtet → Ring-Zentroid auf (350,240),
     RMS-Radius auf 180 px (deckt sich mit dem schematischen Ring); Y gespiegelt
     (Mercator ist Nord-oben, SVG ist Y-unten) → Nord = Bildschirm-oben.
  4. Pfade dezimieren + auf 1 Nachkommastelle runden, nur den im 700×480-Frame
     sichtbaren Anteil behalten → cern/app/src/geo.gen.js (ESM-Export GEO).

Ausgabe ist ein **gebackenes** Artefakt (offline; kein Laufzeit-Netz). geo.js
zeichnet GEO beim Boot als <path class="geo-element"> in die #geo-layer-Gruppe.
"""
import json, os, sys, math, urllib.request, urllib.parse, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW  = os.path.join(ROOT, 'scratch', 'geo_raw.json')
OUT  = os.path.join(ROOT, 'cern', 'app', 'src', 'geo.gen.js')

# SVG-Zielrahmen + LHC-Anker (müssen zur shell.html-Geometrie passen)
W, H = 700, 480
LHC_CX, LHC_CY, LHC_R = 350, 240, 180

# Reale Standorte (lon, lat) → werden mit derselben Transformation projiziert,
# damit die Beschriftungen geo-ehrlich sitzen (statt händisch geschätzt).
POI = [
 ('CERN Meyrin (CH)',     6.0556, 46.2333, 'mid'),
 ('CERN Prévessin (FR)',  6.0556, 46.2611, 'mid'),
 ('St-Genis-Pouilly (FR)',6.0214, 46.2447, 'start'),
 ('Ferney-Voltaire (FR)', 6.1083, 46.2558, 'mid'),
 ('Flughafen Genf (GVA)', 6.1089, 46.2381, 'mid'),
]

# ── Overpass-Fetch (nur mit --fetch; sonst Cache nutzen) ────────────────────
EP = 'https://overpass-api.de/api/interpreter'
QUERIES = {
 'lhc':   '[out:json][timeout:120];way["name"~"^Large Hadron Collider"];out geom;',
 'sps':   '[out:json][timeout:120];way(66473762);out geom;',
 'ps':    '[out:json][timeout:120];way(174646428);out geom;',          # Proton Synchrotron
 'psb':   '[out:json][timeout:120];way(309914733);out geom;',          # PS Booster
 'linac4':'[out:json][timeout:120];way(80305783);out geom;',           # LINAC 4 (seit Kurzem in OSM)
 # Detektor-Insertions = echte IP-Positionen auf dem Ring (ATLAS/CMS/ALICE/LHCb).
 # Union-Klammern PFLICHT, sonst behält Overpass nur das letzte way() im Ergebnis.
 'ip':    '[out:json][timeout:120];(way(685422600);way(685422592);way(685422602);way(685422598););out geom;',
 # Echte Transfertunnel SPS→LHC (in OSM als „Tl2"/„Tl-8" geschrieben):
 'ti2':   '[out:json][timeout:120];way(317804188);out geom;',   # TI 2 → Punkt 2 (ALICE)
 'ti8':   '[out:json][timeout:120];way(317804189);out geom;',   # TI 8 → Punkt 8 (LHCb)
 'tt2_10':'[out:json][timeout:120];way(317804190);out geom;',   # interne Transferlinie TT2/TT10 (PS→SPS)
 'tt60':  '[out:json][timeout:120];way(685422589);out geom;',   # interne Transferlinie TT60 (PS→SPS)
 'lake':  '[out:json][timeout:120];rel(332617);out geom;',          # „Le Léman"
 'border':'[out:json][timeout:120];way["boundary"="administrative"]["admin_level"="2"]'
          '(46.22,5.98,46.34,6.16);out geom;',
}
IP_WAYS = {685422600: 'ATLAS', 685422592: 'CMS', 685422602: 'ALICE', 685422598: 'LHCB'}
def fetch():
    raw = {}
    for k, q in QUERIES.items():
        data = urllib.parse.urlencode({'data': q}).encode()
        for i in range(4):
            try:
                req = urllib.request.Request(EP, data=data, headers={'User-Agent': 'cernsim-geo/0.1'})
                raw[k] = json.load(urllib.request.urlopen(req, timeout=130)).get('elements', [])
                print(f"  {k}: {len(raw[k])} elements"); break
            except Exception as ex:
                print(f"  {k} retry {i+1}: {type(ex).__name__}"); time.sleep(3)
        else:
            raise SystemExit(f"Fetch {k} fehlgeschlagen")
    os.makedirs(os.path.dirname(RAW), exist_ok=True)
    json.dump(raw, open(RAW, 'w'))
    print(f"→ {RAW}")

# ── Geometrie-Extraktion (Listen von Polylinien je Feature) ─────────────────
def lines_from(elements):
    """Gibt eine Liste von Polylinien [(lon,lat),…] zurück (Ways + Rel-Member)."""
    out = []
    for e in elements:
        if e.get('geometry'):
            out.append([(p['lon'], p['lat']) for p in e['geometry']])
        for m in e.get('members', []):
            if m.get('geometry'):
                out.append([(p['lon'], p['lat']) for p in m['geometry']])
    return out

# ── Projektion + Transformation ─────────────────────────────────────────────
def merc(lon, lat):
    return (math.radians(lon), math.log(math.tan(math.pi/4 + math.radians(lat)/2)))

def make_transform(lhc_lines):
    pts = [merc(lo, la) for ln in lhc_lines for (lo, la) in ln]
    cx = sum(p[0] for p in pts)/len(pts)
    cy = sum(p[1] for p in pts)/len(pts)
    rms = math.sqrt(sum((p[0]-cx)**2 + (p[1]-cy)**2 for p in pts)/len(pts))
    s = LHC_R / rms
    def tf(lon, lat):
        x, y = merc(lon, lat)
        return (LHC_CX + (x-cx)*s, LHC_CY - (y-cy)*s)   # Y-Flip: Nord = oben
    return tf

# ── Pfad-Erzeugung (dezimieren, in-Frame clippen, runden) ───────────────────
def decimate(line, step):
    if step <= 1 or len(line) <= 2: return line
    out = line[::step]
    if out[-1] != line[-1]: out.append(line[-1])
    return out

def in_frame(x, y, m=60):
    return -m <= x <= W+m and -m <= y <= H+m

def path_d(line, tf, step=1, clip=False, minpts=2):
    """Eine Polylinie → SVG-'d' (gerundet). clip=True behält nur Punkte im Frame;
    minpts verwirft Kurzfragmente (reduziert Rausch-Stummel bei zerstückelten Ways)."""
    proj = [tf(lo, la) for (lo, la) in decimate(line, step)]
    if clip:
        proj = [(x, y) for (x, y) in proj if in_frame(x, y)]
    if len(proj) < max(2, minpts): return None
    return 'M ' + ' L '.join(f'{x:.1f},{y:.1f}' for (x, y) in proj)

def build():
    raw = json.load(open(RAW))
    lhc_lines = lines_from(raw['lhc'])
    tf = make_transform(lhc_lines)

    GEO = {'lhc': [], 'lake': [], 'border': []}
    for ln in lhc_lines:
        d = path_d(ln, tf)                       # voll auflösen (nur ~290 Pkt)
        if d: GEO['lhc'].append(d)
    for ln in lines_from(raw.get('lake', [])):
        d = path_d(ln, tf, step=6, clip=True, minpts=4)  # See: stark dezimieren, Stummel weg
        if d: GEO['lake'].append(d)
    for ln in lines_from(raw.get('border', [])):
        d = path_d(ln, tf, step=2, clip=True, minpts=5)  # Grenze: Kurzfragmente verwerfen
        if d: GEO['border'].append(d)

    # ── Echte Vorbeschleuniger (geo-akkurate relative Lage) ─────────────────
    def proj_ring(key):
        out = []
        for ln in lines_from(raw.get(key, [])):
            d = path_d(ln, tf)
            if d: out.append(d)
        return out
    GEO['sps'] = proj_ring('sps')
    GEO['ps']  = proj_ring('ps')
    GEO['psb'] = proj_ring('psb')
    GEO['linac4'] = proj_ring('linac4')   # echtes LINAC-4-Gebäude (OSM); LEIR/LINAC3 ∉ OSM → in geo.js schematisch

    def centroid(lines):
        pts = [tf(lo, la) for ln in lines for (lo, la) in ln]
        return (sum(p[0] for p in pts)/len(pts), sum(p[1] for p in pts)/len(pts)) if pts else None
    sps_pts = [tf(lo, la) for ln in lines_from(raw.get('sps', [])) for (lo, la) in ln]
    sps_c = centroid(lines_from(raw.get('sps', [])))

    # Echte IP-Positionen (Zentroid der jeweiligen Insertion)
    GEO['ip'] = {}
    by_id = {e['id']: e for e in raw.get('ip', []) if 'geometry' in e}
    for wid, name in IP_WAYS.items():
        e = by_id.get(wid)
        if e:
            c = centroid([[(p['lon'], p['lat']) for p in e['geometry']]])
            GEO['ip'][name] = {'x': round(c[0], 1), 'y': round(c[1], 1)}

    # TI 2 / TI 8: ECHTE OSM-Trasse (way 317804188 „Tl2" / 317804189 „Tl-8",
    # gekrümmte Tunnel) → SPS-Ende zuerst, dann an den echten Injektionspunkt
    # (Punkt 2 = ALICE, Punkt 8 = LHCb) anbinden. So kommt der Einlauf aus der
    # REALEN Richtung. (Die OSM-Trasse endet 12 px (TI8) bzw. 50 px (TI2) vor dem
    # IP — das letzte Stück folgt der realen Tunnelrichtung in den IP.)
    GEO['ti'] = {}
    GEO['tiApprox'] = False
    for tname, ipname in (('ti2', 'ALICE'), ('ti8', 'LHCB')):
        e = (raw.get(tname) or [{}])[0]
        if not e.get('geometry') or ipname not in GEO['ip']:
            continue
        line = [tf(p['lon'], p['lat']) for p in e['geometry']]
        ip = (GEO['ip'][ipname]['x'], GEO['ip'][ipname]['y'])
        # Reihenfolge so, dass das dem IP NÄHERE Ende zuletzt kommt; dann IP anhängen.
        if math.dist(line[0], ip) < math.dist(line[-1], ip):
            line = line[::-1]
        line = [(round(x, 1), round(y, 1)) for (x, y) in line] + [(round(ip[0], 1), round(ip[1], 1))]
        GEO['ti'][tname] = 'M ' + ' L '.join(f'{x},{y}' for (x, y) in line)

    # Echte interne Transferlinien (PS↔SPS-Bereich): TT2/TT10 + TT60 aus OSM.
    GEO['tt'] = []
    for k in ('tt2_10', 'tt60'):
        e = (raw.get(k) or [{}])[0]
        if e.get('geometry'):
            line = [tf(p['lon'], p['lat']) for p in e['geometry']]
            GEO['tt'].append('M ' + ' L '.join(f'{x:.1f},{y:.1f}' for (x, y) in line))

    # Labels der Vorbeschleuniger (Zentroide)
    GEO['accelLabels'] = []
    for key, txt in (('sps', 'SPS'), ('ps', 'PS'), ('psb', 'PSB')):
        c = centroid(lines_from(raw.get(key, [])))
        if c: GEO['accelLabels'].append({'t': txt, 'x': round(c[0], 1), 'y': round(c[1], 1)})

    # POI projizieren (nur die im Frame)
    GEO['poi'] = []
    for (name, lo, la, anchor) in POI:
        x, y = tf(lo, la)
        if in_frame(x, y, m=0):
            GEO['poi'].append({'t': name, 'x': round(x, 1), 'y': round(y, 1), 'a': anchor})

    # See-Label = Schwerpunkt der im Frame liegenden See-Punkte (oben-rechts)
    lpts = [tuple(map(float, p.split(','))) for d in GEO['lake'] for p in d[2:].split(' L ')]
    lpts = [(x, y) for (x, y) in lpts if in_frame(x, y, m=0)]
    if lpts:
        GEO['lakeLabel'] = {'x': round(sum(p[0] for p in lpts)/len(lpts), 1),
                            'y': round(sum(p[1] for p in lpts)/len(lpts), 1)}

    body = ('// GENERIERT von scripts/geo_build.py — NICHT von Hand editieren.\n'
            '// Reale OSM-Geometrie (Overpass), Web-Mercator + uniforme Skalierung,\n'
            '// am echten LHC-Ring auf das schematische SVG (350,240,r180) ausgerichtet.\n'
            '// Nord = oben. Quelle: © OpenStreetMap-Mitwirkende (ODbL).\n'
            'export const GEO = ' + json.dumps(GEO, ensure_ascii=False) + ';\n')
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w').write(body)
    sz = lambda k: sum(len(d) for d in GEO[k])
    print(f"GEO geschrieben → {OUT}")
    print(f"  lhc:    {len(GEO['lhc'])} Pfade, {sz('lhc')} B")
    print(f"  lake:   {len(GEO['lake'])} Pfade, {sz('lake')} B")
    print(f"  border: {len(GEO['border'])} Pfade, {sz('border')} B")
    print(f"  Datei:  {os.path.getsize(OUT):,} B")

if __name__ == '__main__':
    if '--fetch' in sys.argv:
        fetch()
    build()
