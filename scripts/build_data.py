#!/usr/bin/env python3
"""
build_data.py — regeneriert cern/app/data.js (CERN_REAL) aus ECHTEN CMS-Open-Data.

Quelle der Echtdaten: cern/data/cms_dimuon_subset.csv
  = CMS Open Data, Record 545, Run2011A DoubleMu, √s = 7 TeV (p-p), volle Kinematik.
physics.json bleibt Single Source der Resonanzwerte (reso-Block via gen_constants).

Erzeugt maximal viel ECHTES:
  • Massen-Pools je Fenster (Z⁰, Quarkonia inkl. Substruktur ψ(2S)/Υ-Familie, Niedrigmasse)
    direkt aus den echten invarianten Massen.
  • topo: echte μ⁺μ⁻-Kinematik je Resonanz + ein `bg`-Bucket echter Off-Peak-Paare
    (→ Untergrundspuren im Event-Display sind ECHT, nicht zufällig).
  • higgs4l: BLEIBT kalibrierte Simulation (CMS-Dimuon-Set enthält keine 4ℓ-Events) — als Sim
    markiert (meta.higgs4l_sim = true).
  • meta: Provenienz IN den Daten (source, record, √s, run, n, Fenster).

DETERMINISTISCH (fester Seed nur für die Higgs-Sim) → check.sh bleibt stabil.
Aufruf: python3 scripts/build_data.py   (wird auch von sync_widget.py vor esbuild getriggert)
"""
import os, sys, csv, json, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV  = os.path.join(ROOT, "cern", "data", "cms_dimuon_subset.csv")
H4L_DIR = os.path.join(ROOT, "cern", "data", "higgs4l")   # echte CMS-4ℓ-Kandidaten (Record 5200)
OUT  = os.path.join(ROOT, "cern", "app", "data.js")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_constants  # reso_fragment() = byte-identischer reso-Block aus physics.json

RECORD = "https://opendata.cern.ch/record/545"

# ── Massen-Fenster für die Histogramm-Pools (echte invariante Massen) ─────────
MASS_WINDOWS = {
    "pp":  (50.0, 150.0),   # Z⁰-Region (ATLAS/CMS) — Z-Peak + Drell-Yan-Kontinuum
    "ion": (1.0,  12.0),    # Quarkonia (ALICE): J/ψ, ψ(2S), Υ(1S/2S/3S) + Kontinuum
    "low": (0.4,  3.5),     # Niedrigmasse (Pilot): ρ/ω/φ + J/ψ
}
# ── Resonanz-Fenster für ECHTE Kinematik (topo) ──────────────────────────────
TOPO_WINDOWS = {
    "Z0":    (85.0, 97.0),
    "Jpsi":  (2.90, 3.30),
    "psi2S": (3.55, 3.85),
    "Ups":   (9.00, 10.60),
    "low":   (0.50, 1.30),   # ρ/ω/φ
}
# Off-Peak-Kontinuum für echte Untergrundspuren (meidet alle Peaks).
def _is_bg(m):
    return (13.0 <= m <= 60.0) or (100.0 <= m <= 140.0)

POOL_CAP = 1600   # max. Massen je Pool (Blob-Größe zähmen)
TOPO_CAP = 220    # max. Kinematik-Sätze je Bucket
BG_CAP   = 280


def _stride(seq, cap):
    """Deterministisches Ausdünnen auf <= cap (gleichmäßiger Stride, keine Zufallsauswahl)."""
    n = len(seq)
    if n <= cap:
        return seq
    step = n / cap
    return [seq[int(i * step)] for i in range(cap)]


def read_real():
    masses = {k: [] for k in MASS_WINDOWS}
    topo   = {k: [] for k in TOPO_WINDOWS}
    bg     = []
    n_total = 0
    with open(CSV, newline="") as f:
        for row in csv.DictReader(f):
            try:
                m = float(row["M"])
            except (KeyError, ValueError):
                continue
            n_total += 1
            for key, (lo, hi) in MASS_WINDOWS.items():
                if lo <= m <= hi:
                    masses[key].append(round(m, 2))
            kin = None
            def K():
                return [round(float(row["pt1"]), 2), round(float(row["eta1"]), 2),
                        round(float(row["phi1"]), 2), int(float(row["Q1"])),
                        round(float(row["pt2"]), 2), round(float(row["eta2"]), 2),
                        round(float(row["phi2"]), 2), int(float(row["Q2"]))]
            try:
                for key, (lo, hi) in TOPO_WINDOWS.items():
                    if lo <= m <= hi:
                        topo[key].append(K()); break
                else:
                    if _is_bg(m):
                        bg.append(K())
            except (KeyError, ValueError):
                pass
    masses = {k: _stride(v, POOL_CAP) for k, v in masses.items()}
    topo   = {k: _stride(v, TOPO_CAP) for k, v in topo.items()}
    topo["bg"] = _stride(bg, BG_CAP)
    return masses, topo, n_total


def read_higgs4l():
 """Liest die ECHTEN CMS-4ℓ-Higgs-Kandidaten (Record 5200, 2011+2012, Kanäle
 4μ/4e/2e2μ). Gibt (massen, topo) zurück: M = 4-Lepton-invariante Masse [GeV];
 topo-Eintrag je Event = [pt,eta,phi,q,flavor]×4 (flavor 0=μ, 1=e) für das
 Event-Display. Leer, falls der Ordner fehlt (→ Sim-Fallback)."""
 import glob
 masses, topo = [], []
 for path in sorted(glob.glob(os.path.join(H4L_DIR, "*.csv"))):
  with open(path, newline="") as f:
   for row in csv.DictReader(f):
    try:
     M = float(row["M"])
    except (KeyError, ValueError):
     continue
    masses.append(round(M, 2))
    ev = []
    for i in (1, 2, 3, 4):
     try:
      ev += [round(float(row["pt%d" % i]), 3), round(float(row["eta%d" % i]), 3),
             round(float(row["phi%d" % i]), 3), int(float(row["Q%d" % i])),
             1 if abs(int(float(row.get("PID%d" % i, 13)))) == 11 else 0]  # 11=e, 13=μ
     except (KeyError, ValueError):
      ev += [10.0, 0.0, 0.0, 1, 0]
    topo.append(ev)
 return masses, topo


def sim_higgs4l(n=1500, seed=2):
    """Kalibrierte H→ZZ*→4ℓ-Simulation (KEINE Messung): schmaler 125-GeV-Peak (~6 %)
    auf glattem ZZ*-Kontinuum. Deterministisch (stdlib random, fester Seed)."""
    rng = random.Random(seed)
    out = []
    n_sig = max(1, round(0.06 * n))
    for _ in range(n_sig):
        out.append(round(rng.gauss(125.0, 2.0), 2))
    for _ in range(n - n_sig):
        out.append(round(80.0 + rng.expovariate(1 / 40.0), 2))
    return [m for m in out if 80.0 <= m <= 250.0]


def build():
    masses, topo, n_total = read_real()
    # ECHTE 4ℓ-Higgs-Kandidaten (Record 5200) bevorzugen; sonst kalibrierte Simulation.
    h4l_M, h4l_topo = read_higgs4l()
    if h4l_M:
        higgs4l, higgs4l_sim = h4l_M, False
        h4l_src = "CMS Open Data, Record 5200 (2011+2012, 4μ/4e/2e2μ)"
    else:
        higgs4l, h4l_topo, higgs4l_sim = sim_higgs4l(), [], True
        h4l_src = "kalibrierte Simulation (kein 4ℓ-Datensatz unter cern/data/higgs4l/)"
    topo["h4l"] = h4l_topo   # echte 4-Lepton-Kinematik fürs Event-Display
    meta = {
        "source": "CMS Open Data — Run2011A DoubleMu (μμ) + Record 5200 (4ℓ)",
        "record": RECORD,
        "record_4l": "https://opendata.cern.ch/record/5200",
        "sqrt_s_TeV": 7,
        "sqrt_s_4l_TeV": 8,       # 4ℓ-Kandidaten: CMS 2011 (7) + 2012 (8 TeV)
        "run": "2011A DoubleMu",
        "channel_real": "μ⁺μ⁻ (echte Massen + Kinematik)",
        "higgs4l_sim": higgs4l_sim,        # jetzt False = ECHTE CMS-4ℓ-Kandidaten
        "higgs4l_source": h4l_src,
        "higgs4l_n": len(higgs4l),
        "pbpb_real": False,       # KEIN echtes Pb-Pb — QGP-Effekte sind modelliert auf p-p
        "n_events": n_total,
        # KEIN Datum hier: meta.generated machte data.js (und damit alle 4 Artefakte)
        # täglich byte-verschieden → Git-Rauschen, Repro-Checks brachen über Tagesgrenzen.
    }
    J = lambda o: json.dumps(o, separators=(",", ":"), ensure_ascii=False)
    parts = [
        '"meta":' + J(meta),
        '"pp":' + J(masses["pp"]),
        '"ion":' + J(masses["ion"]),
        '"low":' + J(masses["low"]),
        '"higgs4l":' + J(higgs4l),
        '"topo":' + J(topo),
        gen_constants.reso_fragment(),   # byte-identischer reso-Block aus physics.json
    ]
    h4l_label = "ECHTE CMS-4ℓ-Kandidaten (Record 5200)" if not higgs4l_sim else "kalibrierte Simulation"
    header = (
        "\n// ── ECHTE CERN-OPEN-DATA — generiert von scripts/build_data.py (NICHT HAND-EDITIEREN) ──\n"
        "// μμ-Quelle: CMS Open Data, Record 545, Run2011A DoubleMu, √s = 7 TeV (p-p).\n"
        "// 4ℓ-Quelle: CMS Open Data, Record 5200 (Higgs→ZZ*→4ℓ-Kandidaten 2011/2012).\n"
        "// pp/ion/low + topo(μμ,bg) = ECHTE invariante Massen & Kinematik; higgs4l + topo.h4l = "
        + h4l_label + ".\n"
        "// Kein echtes Pb-Pb vorhanden → QGP-Effekte werden im Widget modelliert (siehe meta).\n"
        "// reso aus physics.json (Single Source).\n"
    )
    body = "const CERN_REAL = {" + ",".join(parts) + "};\n"
    open(OUT, "w", encoding="utf-8").write(header + body)
    sizes = {k: len(v) for k, v in masses.items()}
    sizes["higgs4l" + ("(echt)" if not higgs4l_sim else "(sim)")] = len(higgs4l)
    sizes["topo"] = {k: len(v) for k, v in topo.items()}
    return n_total, sizes


if __name__ == "__main__":
    n, sizes = build()
    print(f"build_data OK | echte Events gelesen: {n:,} | Pools: {sizes} | → {os.path.relpath(OUT, ROOT)}")
