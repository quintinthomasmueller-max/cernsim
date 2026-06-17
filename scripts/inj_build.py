#!/usr/bin/env python3
"""
inj_build.py — bäckt die Injektor-Geometrie aus dem HAND-Lageplan des Nutzers
(cern/data/injector_drawing.svg, in Inkscape von der CERN-PS-Komplex-Karte
abgepaust) in cern/app/src/inj.gen.js.

Warum hand-gezeichnet statt Auto-Fit: OSM ist am Injektor-Maßstab zu ungenau, und
die acc-models-Einzel-Surveys setzen sich nicht zu einem korrekten Gesamt-Layout
zusammen (LEIR/Linac landen im PS). Der Hand-Lageplan hat die richtige Topologie
und (über den PS) die richtigen Proportionen.

Pipeline:
  1. drawing.svg parsen (Inkscape; Pfad-IDs unten sind für GENAU diese Datei).
  2. EINE Ähnlichkeit: am PS verankern (PS-Ring → geo.gen.js-PS, Radius 100 m) und
     starr drehen, bis die gezeichnete TT2 (C) auf die echte Widget-TT2 (→SPS) zeigt.
     → Winkel/relative Lagen bleiben exakt wie gezeichnet.
  3. Kategorisieren: rings(ps/psb/leir), accel(Linac3=erste 34 m von B, Linac4=F),
     transfer(Rest). C (TT2) dient NUR als Rotations-Anker und wird NICHT gezeichnet
     (die echte PS→SPS-Trasse liegt schon grün im geo.gen.js-Vollbild). TT70 (A) und
     Maßstabsbalken werden ebenfalls NICHT übernommen.
  4. → cern/app/src/inj.gen.js (von geo.ts#drawInjector gezeichnet).

Danach: npm run build && python3 scripts/sync_widget.py  (bzw. bash scripts/check.sh).
"""
import os, re, json, math
from svgelements import SVG, Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVG_IN = os.path.join(ROOT, 'cern', 'data', 'injector_drawing.svg')
GEO_GEN = os.path.join(ROOT, 'cern', 'app', 'src', 'geo.gen.js')
OUT = os.path.join(ROOT, 'cern', 'app', 'src', 'inj.gen.js')

# Pfad-IDs aus GENAU diesem drawing.svg (bei Neu-Export ggf. anpassen):
ID_PS, ID_PSB, ID_C = 'path18108', 'path18106', 'path18277'     # PS-Ring, PSB-Ring, C = TT2
ID_B, ID_LINAC4 = 'path18273', 'path19098'                      # B = Linac3+Transfer, F = Linac4
ID_TT70 = ('path18281', 'path18285')                            # TT70 (löschen)
LEIR_IDS = ['path18299', 'path18301', 'path18303', 'path18305', 'path18307',
            'path18309', 'path18311', 'path18313', 'path18315', 'path18317']
TRANSFER_IDS = ['path19094', 'path18291', 'path18275', 'path19092', 'path19096']
SCALEBAR_ID = 'path19100'                                       # 200-m-Strich (löschen)
LINAC3_LEN_M = 34.0


def geo_pts(paths):
    return [[(float(x), float(y)) for x, y in re.findall(r'(-?\d+\.?\d*),(-?\d+\.?\d*)', d)]
            for d in (paths or [])]


def build():
    geo = json.loads(re.search(r'export const GEO = (\{.*\});', open(GEO_GEN).read(), re.S).group(1))
    allp = lambda key: [p for s in geo_pts(geo.get(key, [])) for p in s]
    psp = allp('ps'); xs = [p[0] for p in psp]; ys = [p[1] for p in psp]
    Wc = ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)
    Wr = max(max(xs) - min(xs), max(ys) - min(ys)) / 2
    tt = geo_pts(geo['tt'])[0]
    Wo = max(tt, key=lambda p: math.hypot(p[0] - Wc[0], p[1] - Wc[1]))
    Wi = min(tt, key=lambda p: math.hypot(p[0] - Wc[0], p[1] - Wc[1]))
    angW = math.atan2(Wo[1] - Wi[1], Wo[0] - Wi[0])

    P = {e.id: e for e in SVG.parse(SVG_IN).elements() if isinstance(e, Path)}
    bx = P[ID_PS].bbox(); Dc = ((bx[0] + bx[2]) / 2, (bx[1] + bx[3]) / 2)
    Dr = max(bx[2] - bx[0], bx[3] - bx[1]) / 2
    SCALE = Wr / Dr; MPP = 100.0 / Dr            # PS-Radius = 100 m
    ce = [(P[ID_C].point(0).x, P[ID_C].point(0).y), (P[ID_C].point(1).x, P[ID_C].point(1).y)]
    Ci = min(ce, key=lambda p: math.hypot(p[0] - Dc[0], p[1] - Dc[1]))
    Co = max(ce, key=lambda p: math.hypot(p[0] - Dc[0], p[1] - Dc[1]))
    th = angW - math.atan2(Co[1] - Ci[1], Co[0] - Ci[0]); cs, sn = math.cos(th), math.sin(th)

    def T(x, y):
        dx, dy = x - Dc[0], y - Dc[1]
        return (Wc[0] + SCALE * (cs * dx - sn * dy), Wc[1] + SCALE * (sn * dx + cs * dy))

    # Gerade Pfade: NUR die 2 Endpunkte (kein 49-Punkt-Sampling). Sampling+0,1-Rundung
    # machte aus geraden Diagonalen sichtbare Treppen, weil das Injektor-Fenster nur
    # ~18 Einheiten breit, aber gross dargestellt wird. Kurven (arc=False) brauchen
    # Sampling; dort genuegt feinere Rundung (3 Nachkommastellen).
    def dstr(e, n=48, arc=False):
        if not arc:                                   # gerade Linie -> Start/Ende reichen
            a, b = e.point(0), e.point(1)
            return seg(T(a.x, a.y), T(b.x, b.y))
        pp = [T(e.point(t).x, e.point(t).y) for t in [i / n for i in range(n + 1)]]
        return 'M ' + ' L '.join(f'{x:.3f},{y:.3f}' for x, y in pp)

    def seg(a, b):
        return f'M {a[0]:.3f},{a[1]:.3f} L {b[0]:.3f},{b[1]:.3f}'

    # B (Linac3 + Transfer): Linac3 = erste LINAC3_LEN_M am unteren Ende, Rest = Transfer
    b0 = (P[ID_B].point(0).x, P[ID_B].point(0).y); b1 = (P[ID_B].point(1).x, P[ID_B].point(1).y)
    src = max([b0, b1], key=lambda p: p[1]); dst = min([b0, b1], key=lambda p: p[1])
    L = math.hypot(dst[0] - src[0], dst[1] - src[1]); f = (LINAC3_LEN_M / MPP) / L
    split = (src[0] + (dst[0] - src[0]) * f, src[1] + (dst[1] - src[1]) * f)
    l3a, l3b, trB = T(*src), T(*split), T(*dst)

    # ── Verbindungs-Snap (Vorbereitung Batch-Animation in der Realansicht) ──
    # Gerade Segmente als [Kategorie, A, B] (Widget-Koord); A/B werden in-place
    # geschnappt: (1) NUR echte Duplikate (<NODE_TOL, Rundungs-Mikroluecken) auf ihren
    # Schwerpunkt -> reale Knicke bleiben (z.B. die zwei 35-Grad-Winkel nach Linac4);
    # (2) jedes Segment, das einen Ring erreicht/kreuzt, am EINTRITTSpunkt stoppen
    # (Tangente/Beruehrung, NIE Sekante quer durch); knapp daneben -> radial aufsetzen;
    # (3) echte Null-Laengen verwerfen. Freie Linac-Quellen bleiben unberuehrt.
    def ep(e):
        return [T(e.point(0).x, e.point(0).y), T(e.point(1).x, e.point(1).y)]
    segs = [['accel', l3a, l3b], ['accel'] + ep(P[ID_LINAC4]),         # Linac3 (34 m), Linac4
            ['transfer', l3b, trB]] + [['transfer'] + ep(P[i]) for i in TRANSFER_IDS]

    rp = lambda ids, n: [T(P[i].point(t).x, P[i].point(t).y) for i in ids for t in [j / n for j in range(n + 1)]]
    def ring_of(ids, n):
        q = rp(ids, n); xs = [p[0] for p in q]; ys = [p[1] for p in q]
        return ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, (max(xs) - min(xs) + max(ys) - min(ys)) / 4)
    RINGS = [ring_of([ID_PS], 24), ring_of([ID_PSB], 24), ring_of(LEIR_IDS, 1)]

    # Zusatz-TT (geschaetzt, keine Geodaten): kurz nach Linac3 (am Knoten l3b) schraeg
    # hinueber an den PS-Ring. CERN-plausibel als Anschluss des Ionen-Zweigs an PS;
    # gezielt als TANGENTE vom Knoten an PS (oberer Beruehrpunkt) -> stop_at_ring clippt
    # sie unten sauber auf den Eintritt (grazing, wie PSB->PS).
    pscx, pscy, psr = RINGS[0]; gx, gy = l3b
    dPS = math.hypot(gx - pscx, gy - pscy)
    if dPS > psr:
        gam = math.atan2(gy - pscy, gx - pscx); phi = math.acos(psr / dPS)
        tang = min(((pscx + psr * math.cos(gam + s * phi), pscy + psr * math.sin(gam + s * phi)) for s in (1, -1)), key=lambda p: p[1])
        segs.append(['transfer', list(l3b), list(tang)])   # exakter Tangentenpunkt -> volle Diagonale, beruehrt PS sauber

    NODE_TOL, RING_TOL = 0.12, 0.40
    refs = [(si, j) for si in range(len(segs)) for j in (1, 2)]        # (Segment, A=1/B=2)
    seen = [False] * len(refs)
    for a in range(len(refs)):                                        # (1) nur Duplikate mergen
        if seen[a]: continue
        grp = [a]; seen[a] = True; pa = segs[refs[a][0]][refs[a][1]]
        for b in range(a + 1, len(refs)):
            pb = segs[refs[b][0]][refs[b][1]]
            if not seen[b] and math.hypot(pa[0] - pb[0], pa[1] - pb[1]) < NODE_TOL:
                grp.append(b); seen[b] = True
        cx = sum(segs[refs[g][0]][refs[g][1]][0] for g in grp) / len(grp)
        cy = sum(segs[refs[g][0]][refs[g][1]][1] for g in grp) / len(grp)
        for g in grp: segs[refs[g][0]][refs[g][1]] = (cx, cy)

    def stop_at_ring(p_keep, p_end):
        # NUR p_end an die Ringoberflaeche ziehen, lokal. Es zaehlt ein Ring nur, wenn
        # p_end an/in ihm liegt (de <= r+RING_TOL) -> ferne Enden/freie Quellen bleiben.
        #  - Segment kreuzt den Ring  -> p_end auf den ERSTEN Eintritt von p_keep aus
        #    (min t): die Linie stoppt, wo sie den Ring zuerst beruehrt (Tangente, keine
        #    Sekante quer durch),
        #  - kein Schnitt, aber p_end knapp neben der Kante -> radial aufsetzen (Luecke zu).
        # Es gewinnt der Ring mit der kleinsten Verschiebung.
        best = None
        for cx, cy, r in RINGS:
            ex, ey = p_end[0] - cx, p_end[1] - cy; de = math.hypot(ex, ey)
            if de > r + RING_TOL:                                    # p_end nicht am Ring -> ignorieren
                continue
            dx, dy = p_end[0] - p_keep[0], p_end[1] - p_keep[1]      # p_keep(t=0) -> p_end(t=1)
            fx, fy = p_keep[0] - cx, p_keep[1] - cy
            A = dx * dx + dy * dy; B = 2 * (fx * dx + fy * dy); C = fx * fx + fy * fy - r * r
            disc = B * B - 4 * A * C
            ts = [t for t in ((-B - math.sqrt(disc)) / (2 * A), (-B + math.sqrt(disc)) / (2 * A)) if 0 <= t <= 1] if (A > 1e-9 and disc >= 0) else []
            if ts:                                                   # erster Ring-Eintritt von p_keep aus
                t = min(ts); cand = (p_keep[0] + t * dx, p_keep[1] + t * dy)
            elif de > 1e-6:                                          # kein Schnitt -> radial auf die Kante
                cand = (cx + ex / de * r, cy + ey / de * r)
            else:
                continue
            mv = math.hypot(cand[0] - p_end[0], cand[1] - p_end[1])
            if best is None or mv < best[0]: best = (mv, cand)
        return best[1] if best else p_end

    for s in segs:                                                   # (2) Ring-Eintritt/Tangente
        s[1] = stop_at_ring(s[2], s[1]); s[2] = stop_at_ring(s[1], s[2])
    segs = [s for s in segs if math.hypot(s[1][0] - s[2][0], s[1][1] - s[2][1]) > 0.05]   # (3)

    # TT2 (C) wird NICHT mehr gezeichnet: die echte PS->SPS-Trasse liegt schon als
    # geo.gen.js-'tt' (gruen) im Vollbild. C dient hier nur als Rotations-Anker (oben,
    # th), sonst gaebe es eine versetzte rote Dublette desselben Tunnels.
    INJ = {
        'ps': [dstr(P[ID_PS], arc=True)],
        'psb': [dstr(P[ID_PSB], arc=True)],
        'leir': [dstr(P[i]) for i in LEIR_IDS],
        'accel': [seg(s[1], s[2]) for s in segs if s[0] == 'accel'],
        'transfer': [seg(s[1], s[2]) for s in segs if s[0] == 'transfer'],
    }
    # Labels (PS/Booster/LEIR/LINAC3/LINAC4). PSB wird als "Booster" beschriftet
    # (gelaeufiger Name, didaktisch klarer); Farbzuordnung in geo.ts#drawInjector.
    cw = lambda e: T((e.bbox()[0] + e.bbox()[2]) / 2, (e.bbox()[1] + e.bbox()[3]) / 2)
    psbc = cw(P[ID_PSB])
    lx = [cw(P[i])[0] for i in LEIR_IDS]; ly = [cw(P[i])[1] for i in LEIR_IDS]
    leirc = (sum(lx) / len(lx), sum(ly) / len(ly))
    l4s = T(P[ID_LINAC4].point(1).x, P[ID_LINAC4].point(1).y)
    INJ['labels'] = [
        {'t': 'PS', 'x': round(Wc[0], 1), 'y': round(Wc[1] + 2.5, 1)},
        {'t': 'Booster', 'x': round(psbc[0] - 2.1, 1), 'y': round(psbc[1] - 0.3, 1)},
        {'t': 'LEIR', 'x': round(leirc[0] + 1.5, 1), 'y': round(leirc[1] + 0.5, 1)},
        {'t': 'LINAC3', 'x': round(l3a[0], 1), 'y': round(l3a[1] + 0.6, 1)},
        {'t': 'LINAC4', 'x': round(l4s[0], 1), 'y': round(l4s[1] + 0.6, 1)},
    ]
    # Zoom-Fenster (padToAspect aller Injektor-Punkte, 700/480)
    allpts = [(float(a), float(b)) for k in ('ps', 'psb', 'leir', 'accel', 'transfer')
              for d in INJ[k] for a, b in re.findall(r'(-?\d+\.?\d*),(-?\d+\.?\d*)', d)]
    X = [p[0] for p in allpts]; Y = [p[1] for p in allpts]; m = Wr * 0.18
    x0, y0, x1, y1 = min(X) - m, min(Y) - m, max(X) + m, max(Y) + m
    w, h, asp = x1 - x0, y1 - y0, 700 / 480
    if w / h < asp:
        nw = h * asp; x0 -= (nw - w) / 2; w = nw
    else:
        nh = w / asp; y0 -= (nh - h) / 2; h = nh
    INJ['view'] = {'x': round(x0, 1), 'y': round(y0, 1), 'w': round(w, 1), 'h': round(h, 1)}

    body = ('// GENERIERT (scripts/inj_build.py) aus cern/data/injector_drawing.svg — NICHT von Hand editieren.\n'
            '// Hand-Lageplan (Nutzer), an PS verankert (PS R=100 m), gedreht bis TT2 auf die\n'
            '// echte Widget-TT2 (->SPS) zeigt. Kategorien: rings(ps/psb/leir), accel(Linac3/4),\n'
            '// transfer. C (TT2) nur Anker, NICHT gezeichnet. TT70 + Massstabsbalken NICHT uebernommen.\n'
            'export const INJ = ' + json.dumps(INJ, ensure_ascii=False) + ';\n')
    open(OUT, 'w').write(body)
    print('INJ ->', OUT, '| keys:', list(INJ), '| view:', INJ['view'])


if __name__ == '__main__':
    build()
