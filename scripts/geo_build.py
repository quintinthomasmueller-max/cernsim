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

# Satellitenbild-Hintergrund (Sentinel-2 cloudless, EOX) — deckungsgleich hinter
# die Vektorebene gelegt. Offene Lizenz CC BY 4.0. Gebackenes Base64-Artefakt
# (offline; kein Laufzeit-Netz), analog zu geo.gen.js / data.gen.js.
EOX_WMS    = 'https://tiles.maps.eox.at/wms'
SAT_LAYER  = 's2cloudless-2024_3857'      # EPSG:3857-Variante (CRS der viewBox)
SAT_IMG     = os.path.join(ROOT, 'scratch', 'geo_sat.jpg')
SAT_FCC_IMG = os.path.join(ROOT, 'scratch', 'geo_sat_fcc.jpg')
SAT_INJ_IMG = os.path.join(ROOT, 'scratch', 'geo_sat_inj.jpg')
SAT_OUT    = os.path.join(ROOT, 'cern', 'app', 'src', 'sat.gen.js')
SAT_ATTRIB = 'Sentinel-2 cloudless 2024 © EOX IT Services GmbH (CC BY 4.0)'

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
    lhc_lines = lines_from(raw['lhc'])
    tf = make_transform(lhc_lines)
    fetch_satellite(lhc_lines, raw, tf)

def _wms_tile(xmin, ymin, xmax, ymax, width, height, path_out):
    """Eine Sentinel-2-Kachel (EOX-WMS, EPSG:3857) holen und als JPEG speichern."""
    q = urllib.parse.urlencode({
        'service': 'WMS', 'request': 'GetMap', 'version': '1.3.0',
        'layers': SAT_LAYER, 'styles': '', 'crs': 'EPSG:3857',
        'bbox': f'{xmin:.1f},{ymin:.1f},{xmax:.1f},{ymax:.1f}',
        'width': width, 'height': height, 'format': 'image/jpeg'})
    req = urllib.request.Request(EOX_WMS + '?' + q, headers={'User-Agent': 'cernsim-geo/0.1'})
    data = urllib.request.urlopen(req, timeout=90).read()
    if data[:2] != b'\xff\xd8':
        raise SystemExit(f'Satellitenbild-Fetch {os.path.basename(path_out)}: kein JPEG (EOX-Layer/bbox prüfen)')
    open(path_out, 'wb').write(data)
    import shutil, subprocess
    if shutil.which('sips'):
        subprocess.run(['sips', '--resampleWidth', '1050', '-s', 'format', 'jpeg',
                        '-s', 'formatOptions', '40', path_out],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"  {os.path.basename(path_out)}: {os.path.getsize(path_out):,} B")

def fetch_satellite(lhc_lines, raw=None, tf=None):
    """Drei Sentinel-2-Kacheln holen: Normal-Ansicht (700×480), FCC-Zoom-out,
    Injektor-Zoom-in. Alle auf W/H-Seitenverhältnis zugeschnitten → pixel-
    genau mit den drei SVG-viewBox-Fenstern ausgerichtet."""
    # 1. Normal-Kachel (Vollbild, 0,0–700,480)
    _wms_tile(*sat_bbox_3857(lhc_lines), 1400, 960, SAT_IMG)
    # 2. FCC-Kachel (großer Zoom-out: LHC + FCC-Ring)
    fv = fcc_svg_window()
    _wms_tile(*svg_window_to_bbox_3857(lhc_lines, fv['x'], fv['y'], fv['w'], fv['h']),
              1400, 960, SAT_FCC_IMG)
    # 3. Injektor-Kachel (Meyrin-Cluster, Zoom-in ~20×)
    iv = inj_svg_window(raw, tf) if (raw is not None and tf is not None) else {'x': 270.0, 'y': 410.0, 'w': 48.1, 'h': 33.0}
    _wms_tile(*svg_window_to_bbox_3857(lhc_lines, iv['x'], iv['y'], iv['w'], iv['h']),
              1400, 960, SAT_INJ_IMG)

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

def merc_anchor(lhc_lines):
    """Anker der uniformen Transformation: Mercator-Zentroid (cx,cy) + Skala s,
    sodass der LHC-Ring auf (LHC_CX,LHC_CY) mit RMS-Radius LHC_R landet."""
    pts = [merc(lo, la) for ln in lhc_lines for (lo, la) in ln]
    cx = sum(p[0] for p in pts)/len(pts)
    cy = sum(p[1] for p in pts)/len(pts)
    rms = math.sqrt(sum((p[0]-cx)**2 + (p[1]-cy)**2 for p in pts)/len(pts))
    return cx, cy, LHC_R/rms

def make_transform(lhc_lines):
    cx, cy, s = merc_anchor(lhc_lines)
    def tf(lon, lat):
        x, y = merc(lon, lat)
        return (LHC_CX + (x-cx)*s, LHC_CY - (y-cy)*s)   # Y-Flip: Nord = oben
    return tf

def svg_window_to_bbox_3857(lhc_lines, x0, y0, w, h):
    """EPSG:3857-bbox (minx,miny,maxx,maxy) für ein beliebiges SVG-Fenster
    (x0,y0,w,h). Da die Transformation im Mercator-Raum linear ist, deckt ein
    WMS-Bild dieser bbox, auf das exakte Fenster gelegt, pixelgenau die Vektoren."""
    cx, cy, s = merc_anchor(lhc_lines)
    def inv(sx, sy):                          # SVG-px → (lon, lat)
        mx = cx + (sx-LHC_CX)/s
        my = cy - (sy-LHC_CY)/s
        return math.degrees(mx), math.degrees(2*math.atan(math.exp(my)) - math.pi/2)
    R = 6378137.0
    to3857 = lambda lo, la: (R*math.radians(lo), R*math.log(math.tan(math.pi/4 + math.radians(la)/2)))
    xmin, ymax = to3857(*inv(x0, y0))         # oben-links
    xmax, ymin = to3857(*inv(x0+w, y0+h))     # unten-rechts
    return xmin, ymin, xmax, ymax

def sat_bbox_3857(lhc_lines):
    """Shortcut: EPSG:3857-bbox der Standard-viewBox (0,0,700,480)."""
    return svg_window_to_bbox_3857(lhc_lines, 0, 0, W, H)

def pad_to_aspect(pts, aspect, m):
    """Bounding-Box von pts (+ Marge m) auf Seitenverhältnis aspect aufpolstern."""
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    x0, x1 = min(xs)-m, max(xs)+m
    y0, y1 = min(ys)-m, max(ys)+m
    w, h = x1-x0, y1-y0
    if w/h < aspect:
        nw = h*aspect; x0 -= (nw-w)/2; w = nw
    else:
        nh = w/aspect; y0 -= (nh-h)/2; h = nh
    return {'x': round(x0,1), 'y': round(y0,1), 'w': round(w,1), 'h': round(h,1)}

def bboxc(pts):
    """Mittelpunkt + Hüll-Radius einer Punktwolke (analog zu geo.js#bboxC)."""
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    x0, x1 = min(xs), max(xs); y0, y1 = min(ys), max(ys)
    return {'cx': (x0+x1)/2, 'cy': (y0+y1)/2, 'r': max(x1-x0, y1-y0)/2 or 1}

def fcc_svg_window():
    """SVG-Fenster des FCC-Zoom-out (identische Geometrie wie geo.js#drawFCC)."""
    k = 90.7/26.7; R = LHC_R*k
    ne = [0.6, -0.8]; off = R-LHC_R-4
    cx = LHC_CX+ne[0]*off; cy = LHC_CY+ne[1]*off
    return pad_to_aspect([[cx-R,cy-R],[cx+R,cy+R],[LHC_CX,LHC_CY]], W/H, 60)

def inj_svg_window(raw, tf):
    """SVG-Fenster des Injektor-Zoom-in (identische Geometrie wie geo.js#drawInjector)."""
    def pts_from(key):
        return [tf(p['lon'],p['lat']) for e in raw.get(key,[]) if 'geometry' in e for p in e['geometry']]
    psPts = pts_from('ps'); psbPts = pts_from('psb'); l4Pts = pts_from('linac4')
    if not psPts:
        return {'x': 270.0, 'y': 410.0, 'w': round(W*48.1/700,1), 'h': round(H*33.0/480,1)}
    psC = bboxc(psPts)
    M = lambda m: m * psC['r'] / 101
    leirW, leirH = M(24), M(18)
    dv = [-0.29, 0.96]; dist = psC['r']+M(14)+leirW/2
    leirCx = psC['cx']+dv[0]*dist; leirCy = psC['cy']+dv[1]*dist
    l3a = [leirCx-leirW/2-M(30), leirCy+M(2)]
    all_pts = (psPts+psbPts+l4Pts+
               [[leirCx-leirW/2,leirCy],[leirCx+leirW/2,leirCy+leirH/2],
                l3a,[psC['cx'],psC['cy']]])
    return pad_to_aspect([list(p) for p in all_pts], W/H, 6)

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

def stitch_ring(members, role='outer', tol=1e-7):
    """Relation-Member-Ways (in Reihenfolge, Endpunkte geteilt) zu EINEM
    geschlossenen Ring [(lon,lat),…] verketten. Für Wasserflächen (multipolygon):
    Overpass liefert die Außenkontur als viele Ways — erst verkettet ergibt sich
    eine füllbare Fläche (sonst füllt jeder Way nur seinen eigenen Schnipsel)."""
    near = lambda a, b: abs(a[0]-b[0]) < tol and abs(a[1]-b[1]) < tol
    ring = []
    for m in members:
        if m.get('role') != role or not m.get('geometry'): continue
        g = [(p['lon'], p['lat']) for p in m['geometry']]
        if not ring: ring = g[:]
        elif near(ring[-1], g[0]):  ring.extend(g[1:])
        elif near(ring[-1], g[-1]): ring.extend(list(reversed(g))[1:])
        else: ring.extend(g)        # Lücke: trotzdem anhängen (Frame-Clip glättet)
    return ring

def clip_poly(poly, m=2):
    """Sutherland-Hodgman: Polygon am Frame-Rechteck [-m,W+m]×[-m,H+m] clippen →
    EIN geschlossenes Polygon, das der Küstenlinie im Frame folgt und sonst dem
    Rand. Die Rand-Segmente liegen knapp außerhalb des viewBox → keine sichtbare
    Kante, nur die echte Uferlinie zeigt sich; SVG füllt die Fläche solide."""
    def half(p, ins, isect):
        out = []
        for i in range(len(p)):
            a, b = p[i], p[(i+1) % len(p)]
            ia, ib = ins(a), ins(b)
            if ia and ib: out.append(b)
            elif ia and not ib: out.append(isect(a, b))
            elif not ia and ib: out += [isect(a, b), b]
        return out
    ix = lambda a, b, x: (x, a[1] + (x-a[0])/(b[0]-a[0])*(b[1]-a[1]))
    iy = lambda a, b, y: (a[0] + (y-a[1])/(b[1]-a[1])*(b[0]-a[0]), y)
    p = poly
    p = half(p, lambda q: q[0] >= -m,   lambda a, b: ix(a, b, -m))
    p = half(p, lambda q: q[0] <= W+m,  lambda a, b: ix(a, b, W+m))
    p = half(p, lambda q: q[1] >= -m,   lambda a, b: iy(a, b, -m))
    p = half(p, lambda q: q[1] <= H+m,  lambda a, b: iy(a, b, H+m))
    return p

def lake_path(elements, tf, step=4):
    """Wasserfläche (Léman) als EINEN gefüllten, geschlossenen Pfad bauen:
    Außenring verketten → projizieren → dezimieren → am Frame clippen → 'M…Z'."""
    if not elements: return None
    ring = stitch_ring(elements[0].get('members', []))
    if len(ring) < 4: return None
    proj = [tf(lo, la) for (lo, la) in decimate(ring, step)]
    poly = clip_poly(proj)
    if len(poly) < 4: return None
    return 'M ' + ' L '.join(f'{x:.1f},{y:.1f}' for (x, y) in poly) + ' Z'

def build():
    raw = json.load(open(RAW))
    lhc_lines = lines_from(raw['lhc'])
    tf = make_transform(lhc_lines)

    GEO = {'lhc': [], 'lake': [], 'border': []}
    for ln in lhc_lines:
        d = path_d(ln, tf)                       # voll auflösen (nur ~290 Pkt)
        if d: GEO['lhc'].append(d)
    d = lake_path(raw.get('lake', []), tf, step=4)        # See: EIN geschlossenes Füll-Polygon
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
    lpts = [tuple(map(float, p.split(','))) for d in GEO['lake'] for p in d.replace(' Z', '')[2:].split(' L ')]
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

    # Satellitenbilder als Base64-ESM einbacken (sat.gen.js) — drei Kacheln für
    # Normal-Ansicht, FCC-Zoom-out und Injektor-Zoom-in. Fehlt eine Datei, bleibt
    # der Export leer; die Real-Ansicht funktioniert dann ohne Foto.
    import base64
    fcc_view = fcc_svg_window()
    inj_view = inj_svg_window(raw, tf)
    def b64img(path):
        return ('data:image/jpeg;base64,' +
                base64.b64encode(open(path,'rb').read()).decode()) if os.path.exists(path) else ''
    sat_body = (
        '// GENERIERT von scripts/geo_build.py — NICHT von Hand editieren.\n'
        f'// {SAT_ATTRIB}\n'
        '// Web-Mercator (EPSG:3857), deckungsgleich mit den SVG-Zoom-Fenstern.\n'
        f'export const SAT     = {json.dumps(b64img(SAT_IMG))};\n'
        f'export const SAT_FCC = {json.dumps(b64img(SAT_FCC_IMG))};\n'
        f'export const SAT_INJ = {json.dumps(b64img(SAT_INJ_IMG))};\n'
        f'export const SAT_FCC_VIEW = {json.dumps(fcc_view)};\n'
        f'export const SAT_INJ_VIEW = {json.dumps(inj_view)};\n'
        f'export const SAT_ATTRIB = {json.dumps(SAT_ATTRIB, ensure_ascii=False)};\n')
    open(SAT_OUT, 'w').write(sat_body)
    print(f"  satellite → {SAT_OUT} ({os.path.getsize(SAT_OUT):,} B)")

    sz = lambda k: sum(len(d) for d in GEO[k])
    print(f"GEO geschrieben → {OUT}")
    print(f"  lhc:    {len(GEO['lhc'])} Pfade, {sz('lhc')} B")
    print(f"  lake:   {len(GEO['lake'])} Pfade, {sz('lake')} B")
    print(f"  border: {len(GEO['border'])} Pfade, {sz('border')} B")
    print(f"  Datei:  {os.path.getsize(OUT):,} B")

if __name__ == '__main__':
    if '--fetch' in sys.argv:
        fetch()
    elif '--fetch-sat' in sys.argv:
        raw = json.load(open(RAW))
        lhc_lines = lines_from(raw['lhc'])
        fetch_satellite(lhc_lines, raw, make_transform(lhc_lines))
    build()
