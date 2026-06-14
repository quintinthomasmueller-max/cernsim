#!/usr/bin/env python3
"""
accmodels_build.py — bäckt die EXAKTE Injektor-Geometrie aus den offiziellen
CERN-acc-models-Survey-Dateien (MAD-X TFS) in ein Real-Overlay-Artefakt.

Motivation (vgl. docs/GEO_DATENQUELLEN.md): PS/PSB/LINAC4 stehen nur grob in OSM;
LEIR und die internen Transferlinien fehlen dort. Schlimmer: die OSM-PSB-Lage liegt
~52° falsch zur PS (PSB ist real NÖRDLICH der PS, OSM zeichnet sie NW). acc-models
(https://gitlab.cern.ch/acc-models, öffentlich) liefert jede Maschine/Linie als
SURVEY-TFS mit GLOBALEN CERN-Koordinaten (CCS, Meter) in EINEM gemeinsamen Frame.

Georeferenzierung — die entscheidende Lektion:
  • PS/PSB/LEIR + alle Transferlinien teilen EINEN globalen CCS-Frame (Y≈2433,7 m
    vertikal; horizontale Ebene = X/Z). Ihre RELATIV-Lagen sind vermessungsgenau.
  • Ein Fit über NUR PS+PSB scheitert: die beiden Zentren liegen ~6 px auseinander
    → die 2-Punkt-Ähnlichkeit ist rang-defizient (Skala unzuverlässig, Händigkeit/
    Drehung quer zur PS-PSB-Achse beliebig → Cluster spiegelt/dreht falsch).
  • LÖSUNG = LANGE BASISLINIE: die SPS→LHC-Transferlinien TI2/TI8 enden an den
    LHC-Insertionen IP2 (ALICE) / IP8 (LHCb). Deren CCS-Endpunkte + das PS-Zentrum
    sind in OSM gut verortet → 3-Anker-Ähnlichkeit (PS, IP2, IP8) bestimmt Skala,
    Drehung UND Händigkeit robust (RMS ~2 px über die ganze Karte). Translation wird
    danach hart auf das OSM-PS-Zentrum gepinnt, damit der Survey-Cluster nahtlos in
    den bestehenden OSM-Kontext (SPS, TT-Linien, Satellit) passt.

Pipeline (Offline-Bake, kein Laufzeit-Netz):
  1. --fetch : acc-models-Repos klonen (ps, psb, leir, tls) → scratch/acc-models/.
  2. Survey-TFS parsen → globale (X,Z)-Punkte (CCS) je Ring/Linie.
  3. 3-Anker-Fit CCS→SVG (Umeyama, PS+IP2+IP8), Translation auf OSM-PS gepinnt.
  4. Projektion in DENSELBEN SVG-Frame wie geo.gen.js → cern/app/src/inj.gen.js
     (export const INJ = {ps, psb, leir, lines:{…}}).

Selbsttest (headless, kein Netz):  python3 scripts/accmodels_build.py --selftest
"""
import os, sys, math, json, re, subprocess
import numpy as np
import geo_build as gb

ROOT    = gb.ROOT
ACC_DIR = os.path.join(ROOT, 'scratch', 'acc-models')
GEO_GEN = os.path.join(ROOT, 'cern', 'app', 'src', 'geo.gen.js')
OUT     = os.path.join(ROOT, 'cern', 'app', 'src', 'inj.gen.js')
BASE    = 'https://gitlab.cern.ch/acc-models/'

PLANE = (0, 2)   # CCS: horizontale Karten-Ebene = (X, Z); Y ist vertikal.

# Ringe mit globaler Survey-TFS:  name -> (repo, branch, tfs-relpfad)
RINGS = {
    'ps':   ('acc-models-ps',   '2021', 'survey/ps_survey.tfs'),
    'psb':  ('acc-models-psb',  '2021', 'survey/psb_survey.tfs'),
    'leir': ('acc-models-leir', '2021', 'survey/leir_survey.tfs'),
}
# Transferlinien-Repo (TI-Anker + reale Transferlinien fürs Rendering).
TLS = ('acc-models-tls', '2021')
# Lange-Basislinie-Anker: SPS→LHC-Linien, enden an den LHC-IPs (CCS-Endpunkt).
TI_LINES = {
    'ip2': 'sps_extraction/tt60ti2_q26/line/survey_ti2.tfs',   # → IP2 (ALICE)
    'ip8': 'sps_extraction/tt40ti8_q26/line/survey_ti8.tfs',   # → IP8 (LHCb)
}
# Reale, im Injektor-Zoom sichtbare Transferlinien (optional; werden gezeichnet,
# falls vorhanden).  name -> tls-relpfad.
LINES = {
    'l3leir': 'leir_injection/ith_ite_etl_ei/line/survey_leir_injection.tfs',  # LINAC3 → LEIR
}
# Welche acc-models-Repos --fetch klont.
FETCH_REPOS = (
    [(r, b) for (_n, (r, b, _t)) in [(n, RINGS[n]) for n in RINGS]] + [TLS]
)


# ── --fetch (NETZ; läuft auf dem Nutzer-Rechner, analog geo_build.py --fetch) ──
def fetch():
    os.makedirs(ACC_DIR, exist_ok=True)
    for repo, branch in FETCH_REPOS:
        dst = os.path.join(ACC_DIR, repo)
        if os.path.isdir(os.path.join(dst, '.git')):
            subprocess.run(['git', '-C', dst, 'pull', '--ff-only'], check=False)
        else:
            subprocess.run(['git', 'clone', '--depth', '1', '-b', branch,
                            BASE + repo + '.git', dst], check=True)
    print('acc-models geklont/aktualisiert →', ACC_DIR)


# ── TFS-Parser (MAD-X) ───────────────────────────────────────────────────────
def parse_tfs(path):
    """MAD-X-TFS → (cols, rows[dict]). Spalten per Header-Zeile (*) benannt."""
    cols, rows = None, []
    with open(path) as f:
        for line in f:
            s = line.strip()
            if not s or s[0] in '@$':
                continue
            if s[0] == '*':
                cols = s[1:].split()
                continue
            if cols is None:
                continue
            toks = re.findall(r'"[^"]*"|\S+', s)
            if len(toks) < len(cols):
                continue
            rows.append({c: t.strip('"') for c, t in zip(cols, toks)})
    return cols, rows


def survey_points(rows):
    """Geordnete globale Punkte (X,Y,Z) [m, CCS] aus einer Survey-TFS."""
    return [(float(r['X']), float(r['Y']), float(r['Z']))
            for r in rows if {'X', 'Y', 'Z'} <= r.keys()]


def survey_xz(path):
    """Survey-TFS → geordnete (X,Z)-Punkte (CCS, horizontale Ebene)."""
    return [(p[PLANE[0]], p[PLANE[1]]) for p in survey_points(parse_tfs(path)[1])]


def horizontal_plane(pts):
    """Indizes (i,j) der beiden horizontalen Achsen (größte Spannweite); die
    dritte (≈konstant) ist vertikal. Für CERN-CCS hier: (0,2) = (X,Z)."""
    cols = list(zip(*pts))
    span = [max(c) - min(c) for c in cols]
    i, j = sorted(sorted(range(3), key=lambda k: -span[k])[:2])
    return i, j


def to_plane(pts, ij):
    i, j = ij
    return [(p[i], p[j]) for p in pts]


# ── Geometrie-Helfer (numpy) ────────────────────────────────────────────────
def fit_circle(pts):
    """Kasa-Kleinste-Quadrate-Kreis → (cx, cy, r)."""
    P = np.asarray(pts, float)
    x, y = P[:, 0], P[:, 1]
    A = np.c_[2 * x, 2 * y, np.ones(len(P))]
    a, b, c = np.linalg.lstsq(A, x * x + y * y, rcond=None)[0]
    return float(a), float(b), math.sqrt(max(c + a * a + b * b, 0.0))


def umeyama(src, dst):
    """Optimale 2D-Ähnlichkeit (Skala s, Orthogonal-R inkl. Spiegelung,
    Translation t) mit dst ≈ s·R·src + t. Umeyama (1991)."""
    src = np.asarray(src, float); dst = np.asarray(dst, float)
    n = len(src)
    ms, md = src.mean(0), dst.mean(0)
    Xs, Xd = src - ms, dst - md
    U, D, Vt = np.linalg.svd((Xd.T @ Xs) / n)
    R = U @ Vt                                   # Spiegelung erlaubt (optimal)
    s = float(D.sum() / ((Xs ** 2).sum() / n))
    t = md - s * (R @ ms)
    return s, R, t


def apply_sim(s, R, t, pts):
    P = np.asarray(pts, float)
    return (s * (P @ R.T) + t)


def fit_residual(s, R, t, src, dst):
    pr = apply_sim(s, R, t, src)
    return float(np.sqrt(((pr - np.asarray(dst, float)) ** 2).sum(1).mean()))


# ── geo.gen.js (OSM-SVG) lesen — liefert die Ziel-Anker ─────────────────────
def read_geo():
    txt = open(GEO_GEN).read()
    m = re.search(r'export const GEO = (\{.*\});', txt, re.S)
    return json.loads(m.group(1))


def geo_points(paths):
    o = []
    for d in (paths or []):
        for x, y in re.findall(r'(-?\d+\.?\d*),(-?\d+\.?\d*)', d):
            o.append((float(x), float(y)))
    return o


def bbox_center(paths):
    pts = geo_points(paths)
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)


def _svg_path(svg_pts, step=2):
    pts = gb.decimate([tuple(p) for p in svg_pts], step)
    return 'M ' + ' L '.join(f'{x:.1f},{y:.1f}' for x, y in pts)


# ── Georeferenzierung: 3-Anker-Fit (PS, IP2, IP8), auf OSM-PS gepinnt ────────
def georef(rings_ccs, ti2, ti8, geo):
    """Liefert eine Projektionsfunktion CCS(X,Z) → SVG + (RMS, Anker-Info)."""
    osm_ps = bbox_center(geo['ps'])
    alice  = (geo['ip']['ALICE']['x'], geo['ip']['ALICE']['y'])
    lhcb   = (geo['ip']['LHCB']['x'],  geo['ip']['LHCB']['y'])
    ps_c   = fit_circle(rings_ccs['ps'])[:2]
    src = np.array([ps_c, ti2[-1], ti8[-1]], float)         # PS-Zentrum, IP2-, IP8-Ende
    dst = np.array([osm_ps, alice, lhcb], float)
    s, R, _ = umeyama(src, dst)
    t = np.array(osm_ps) - s * (R @ np.array(ps_c))         # Translation auf OSM-PS pinnen
    res = fit_residual(s, R, t, src, dst)

    def proj(pts):
        return apply_sim(s, R, t, pts)

    return proj, res, {'scale': s, 'det': float(np.linalg.det(R)),
                       'ps_r_px': fit_circle(rings_ccs['ps'])[2] * s}


# ── Bake ────────────────────────────────────────────────────────────────────
def build():
    if not os.path.isdir(ACC_DIR):
        print('!! scratch/acc-models/ fehlt — erst `python3 scripts/accmodels_build.py --fetch`')
        return
    missing = [n for n, (repo, _b, tfs) in RINGS.items()
               if not os.path.exists(os.path.join(ACC_DIR, repo, tfs))]
    if missing:
        print('!! fehlende Ring-Survey-TFS:', missing, '— --fetch ausführen.')
        return
    tip = os.path.join(ACC_DIR, TLS[0], TI_LINES['ip2'])
    if not os.path.exists(tip):
        print('!! acc-models-tls/TI-Linien fehlen — --fetch (klont auch acc-models-tls).')
        return

    rings = {n: survey_xz(os.path.join(ACC_DIR, repo, tfs))
             for n, (repo, _b, tfs) in RINGS.items()}
    ti2 = survey_xz(os.path.join(ACC_DIR, TLS[0], TI_LINES['ip2']))
    ti8 = survey_xz(os.path.join(ACC_DIR, TLS[0], TI_LINES['ip8']))
    geo = read_geo()

    proj, res, info = georef(rings, ti2, ti8, geo)

    INJ = {n: [_svg_path(proj(pts))] for n, pts in rings.items()}
    lines = {}
    for n, rel in LINES.items():
        p = os.path.join(ACC_DIR, TLS[0], rel)
        if os.path.exists(p):
            lines[n] = [_svg_path(proj(survey_xz(p)))]
    if lines:
        INJ['lines'] = lines

    body = ('// GENERIERT von scripts/accmodels_build.py — NICHT von Hand editieren.\n'
            '// Exakte Injektor-Geometrie aus CERN acc-models (MAD-X SURVEY, CCS-Meter).\n'
            '// 3-Anker-Georeferenz: PS-Zentrum + LHC-IP2/IP8 (Enden der TI2/TI8-Linien)\n'
            '// → robuste Skala/Drehung/Händigkeit; Translation auf das OSM-PS-Zentrum\n'
            '// gepinnt. Ringe + reale Transferlinien im geo.gen.js-SVG-Frame.\n'
            f'// Anker PS/IP2/IP8; RMS {res:.2f} px; PS-Radius {info["ps_r_px"]:.2f} px;'
            f' det(R) {info["det"]:+.0f}. Quelle: gitlab.cern.ch/acc-models (ODbL/CERN).\n'
            'export const INJ = ' + json.dumps(INJ, ensure_ascii=False) + ';\n')
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w').write(body)
    print(f'INJ geschrieben → {OUT}')
    print(f'  Anker PS/IP2/IP8, RMS {res:.2f} px, PS-r {info["ps_r_px"]:.2f} px,'
          f' Ringe {list(rings)}, Linien {list(lines)}')


# ── Headless-Selbsttest (kein Netz) ─────────────────────────────────────────
# 16 ECHTE PSB-Ring-3-Punkte (acc-models-psb/2021/survey/psb_survey.tfs), als
# Mini-TFS, um Parser + Einheiten gegen reale Daten zu prüfen (Radius ~25 m).
_REAL_PSB_TFS = """@ NAME %06s "SURVEY"
* NAME S L ANGLE X Y Z THETA PHI PSI TILT SLOT_ID ASSEMBLY_ID
$ %s %le %le %le %le %le %le %le %le %le %le %d %d
 "PSB3$START" 0 0 0 -1880.503 2433.66 2108.400 0 0 0 0 0 0
 "BR3.VVS1L2" 0 0 0 -1878.609 2433.66 2112.487 0 0 0 0 0 0
 "DRIFT_18" 0 0 0 -1874.910 2433.66 2117.465 0 0 0 0 0 0
 "BR3.OSK2L4" 0 0 0 -1870.181 2433.66 2121.255 0 0 0 0 0 0
 "DRIFT_35" 0 0 0 -1863.417 2433.66 2124.267 0 0 0 0 0 0
 "BR3.OSK4L1" 0 0 0 -1857.950 2433.66 2125.145 0 0 0 0 0 0
 "BR.QDE4" 0 0 0 -1851.700 2433.66 2124.545 0 0 0 0 0 0
 "DRIFT_60" 0 0 0 -1844.465 2433.66 2121.830 0 0 0 0 0 0
 "BR3.OSK6L1" 0 0 0 -1839.979 2433.66 2118.585 0 0 0 0 0 0
 "BR.QFO62" 0 0 0 -1835.335 2433.66 2112.781 0 0 0 0 0 0
 "DRIFT_83" 0 0 0 -1832.556 2433.66 2105.572 0 0 0 0 0 0
 "DRIFT_91" 0 0 0 -1831.903 2433.66 2099.766 0 0 0 0 0 0
 "BR3.TSAB8L4" 0 0 0 -1832.599 2433.66 2094.528 0 0 0 0 0 0
 "BR.STSCRAP91" 0 0 0 -1835.022 2433.66 2088.059 0 0 0 0 0 0
 "BR.BHZ101" 0 0 0 -1841.321 2433.66 2080.615 0 0 0 0 0 0
 "P11RING3$START" 0 0 0 -1845.999 2433.66 2077.651 0 0 0 0 0 0
"""

def selftest():
    import tempfile
    ok = True
    def check(name, cond):
        nonlocal ok
        print(('  PASS ' if cond else '  FAIL ') + name); ok = ok and cond

    # 1) Parser + Einheiten gegen ECHTE PSB-Daten
    with tempfile.NamedTemporaryFile('w', suffix='.tfs', delete=False) as f:
        f.write(_REAL_PSB_TFS); fp = f.name
    cols, rows = parse_tfs(fp); os.unlink(fp)
    check('parse_tfs: 13 Spalten', cols and len(cols) == 13)
    check('parse_tfs: 16 Datenzeilen', len(rows) == 16)
    pts = survey_points(rows)
    plane = horizontal_plane(pts)
    check('horizontale Ebene = (X,Z)=(0,2)', plane == (0, 2))
    cx, cy, r = fit_circle(to_plane(pts, plane))
    check(f'PSB-Radius {r:.1f} m ~ 25 m (echt)', 23.0 <= r <= 27.0)
    check(f'PSB-Zentrum ({cx:.0f},{cy:.0f}) ~ (-1857,2101)',
          abs(cx + 1857) < 4 and abs(cy - 2101) < 4)

    # 2) Umeyama exakt: bekannte Ähnlichkeit (Skala+Drehung+Translation) zurückgewinnen
    rng = np.random.default_rng(0)
    A = rng.normal(size=(8, 2)) * 100 + [500, 300]
    th, sc, tr = 0.7, 0.013, np.array([350.0, 240.0])
    Rt = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
    B = sc * (A @ Rt.T) + tr
    s, R, t = umeyama(A, B)
    check('umeyama: Skala', abs(s - sc) < 1e-9)
    check('umeyama: Residuum ~0', fit_residual(s, R, t, A, B) < 1e-6)

    # 3) Umeyama mit SPIEGELUNG (Händigkeit CCS↔geo): wird ebenfalls erkannt
    Bm = sc * (A @ np.array([[1, 0], [0, -1]]) @ Rt.T) + tr
    sm, Rm, tm = umeyama(A, Bm)
    check('umeyama: Spiegelung Residuum ~0', fit_residual(sm, Rm, tm, A, Bm) < 1e-6)
    check('umeyama: Spiegelung erkannt (det<0)', np.linalg.det(Rm) < 0)

    # 4) Warum 2-Anker scheitert, 3-Anker (lange Basislinie) trägt:
    #    PS+PSB liegen eng beieinander → quer dazu ist die Lösung unterbestimmt;
    #    ein 3. weit entfernter Anker (IP) fixiert Skala/Drehung/Händigkeit.
    ps_c  = np.array([-1956.0, 1963.0])
    psb_c = np.array([-1857.0, 2100.0])           # ~169 m von PS (eng, fast 1 Richtung)
    ip2_c = np.array([883.0, 2643.0])             # weit weg (lange Basislinie)
    ip8_c = np.array([-4418.0, 4874.0])
    sc2, th2, tr2 = 0.0438, 1.1, np.array([291.8, 430.1])
    Rk = np.array([[math.cos(th2), -math.sin(th2)], [math.sin(th2), math.cos(th2)]])
    M  = np.array([[1, 0], [0, -1]])              # echte Händigkeit braucht Spiegelung
    def truth(p): return sc2 * ((M @ Rk) @ p) + tr2
    # 3-Anker findet die Ähnlichkeit (inkl. Spiegelung) zurück:
    src3 = np.array([ps_c, ip2_c, ip8_c]); dst3 = np.array([truth(p) for p in src3])
    s3, R3, t3 = umeyama(src3, dst3)
    check('3-Anker (PS,IP2,IP8) Residuum ~0', fit_residual(s3, R3, t3, src3, dst3) < 1e-6)
    psb_proj = apply_sim(s3, R3, t3, [psb_c])[0]
    check('3-Anker: PSB landet an der wahren Lage',
          float(np.hypot(*(psb_proj - truth(psb_c)))) < 1e-6)

    print('\nSELFTEST:', 'OK' if ok else 'FEHLGESCHLAGEN')
    return 0 if ok else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    if '--fetch' in sys.argv:
        fetch()
    build()
