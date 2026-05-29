"""
cern_utils.py
=============
Gemeinsame Hilfsfunktionen, Konstanten und Farbschemata für die
CERN-Experiment-Visualisierungs-Suite.
"""
from __future__ import annotations  # Typ-Hints (X | Y) als Strings → auch <3.10 importierbar

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import FancyArrowPatch
from collections import namedtuple

# ──────────────────────────────────────────────────────────────────────────────
# PHYSIKALISCHE KONSTANTEN (SI-Einheiten)
# ──────────────────────────────────────────────────────────────────────────────
PhysConstants = namedtuple('PhysConstants', [
    'c',        # Lichtgeschwindigkeit [m/s]
    'hbar',     # Reduziertes Planck-Quantum [J·s]
    'e',        # Elementarladung [C]
    'me',       # Elektronenmasse [kg]
    'mp',       # Protonenmasse [kg]
    'k_B',      # Boltzmann-Konstante [J/K]
    'alpha',    # Feinstrukturkonstante [dimensionslos]
    'GeV',      # 1 GeV in Joule
    'TeV',      # 1 TeV in Joule
    'fm',       # 1 Femtometer in Meter
])

PC = PhysConstants(
    c      = 2.99792458e8,
    hbar   = 1.054571817e-34,
    e      = 1.602176634e-19,
    me     = 9.1093837015e-31,
    mp     = 1.67262192369e-27,
    k_B    = 1.380649e-23,
    alpha  = 1 / 137.035999084,
    GeV    = 1.602176634e-10,
    TeV    = 1.602176634e-7,
    fm     = 1e-15,
)

# Bequeme Einheitenumrechnung (Einheitensystem: hbar=c=1)
# Protonmasse in GeV/c²
MP_GEV   = 0.938272046   # GeV/c²
ME_GEV   = 0.000510999   # GeV/c²
MHIGGS   = 125.25        # GeV/c²
MZ       = 91.1876       # GeV/c²
MW       = 80.377        # GeV/c²
MTOP     = 172.69        # GeV/c²

# ──────────────────────────────────────────────────────────────────────────────
# CERN-EXPERIMENTE: METADATEN
# ──────────────────────────────────────────────────────────────────────────────
EXPERIMENTS = {
    'ATLAS': {
        'farbe':       '#1f77b4',
        'beschreibung': 'A Toroidal LHC Apparatus – Allzweck-Detektor',
        'schwerpunkt':  'Higgs-Boson, Suche nach neuer Physik',
        'kollision':    'pp bei 13.6 TeV',
    },
    'CMS': {
        'farbe':       '#d62728',
        'beschreibung': 'Compact Muon Solenoid – Allzweck-Detektor',
        'schwerpunkt':  'Higgs-Boson, Präzisionsmessungen',
        'kollision':    'pp bei 13.6 TeV',
    },
    'ALICE': {
        'farbe':       '#2ca02c',
        'beschreibung': 'A Large Ion Collider Experiment',
        'schwerpunkt':  'Quark-Gluon-Plasma, Schwerionenkollisionen',
        'kollision':    'Pb-Pb bei 5.02 TeV/n',
    },
    'LHCb': {
        'farbe':       '#ff7f0e',
        'beschreibung': 'Large Hadron Collider beauty experiment',
        'schwerpunkt':  'B-Physik, CP-Verletzung',
        'kollision':    'pp bei 13.6 TeV',
    },
    'LHCf': {
        'farbe':       '#9467bd',
        'beschreibung': 'LHC forward – Vorwärtsdetektor',
        'schwerpunkt':  'Kosmische Strahlung, Hadronenproduktion',
        'kollision':    'pp bei 13.6 TeV',
    },
    'TOTEM': {
        'farbe':       '#8c564b',
        'beschreibung': 'Total Cross Section, Elastic Scattering and Diffraction',
        'schwerpunkt':  'Elastische Streuung, Proton-Struktur',
        'kollision':    'pp bei 13.6 TeV',
    },
}

# Standardmäßige Teilchenfarben (Feynman-Diagramm-Konvention)
TEILCHEN_FARBEN = {
    'proton':   '#1f77b4',
    'neutron':  '#aec7e8',
    'elektron': '#ff7f0e',
    'positron': '#ffbb78',
    'photon':   '#ffd700',
    'muon':     '#2ca02c',
    'tau':      '#98df8a',
    'quark_u':  '#d62728',
    'quark_d':  '#ff9896',
    'quark_s':  '#9467bd',
    'quark_c':  '#c5b0d5',
    'quark_b':  '#8c564b',
    'quark_t':  '#c49c94',
    'gluon':    '#e377c2',
    'W+':       '#7f7f7f',
    'W-':       '#bcbd22',
    'Z0':       '#17becf',
    'Higgs':    '#aec7e8',
    'neutrino': '#ffffff',
}

# ──────────────────────────────────────────────────────────────────────────────
# MATPLOTLIB-STIL: CERN-DARK-THEME
# ──────────────────────────────────────────────────────────────────────────────
CERN_DARK_PARAMS = {
    "figure.facecolor":     "#0d1117",
    "axes.facecolor":       "#161b22",
    "axes.edgecolor":       "#30363d",
    "axes.labelcolor":      "#e6edf3",
    "axes.grid":            True,
    "grid.color":           "#21262d",
    "grid.linewidth":       0.8,
    "grid.alpha":           0.6,
    "text.color":           "#e6edf3",
    "xtick.color":          "#8b949e",
    "ytick.color":          "#8b949e",
    "xtick.labelsize":      11,
    "ytick.labelsize":      11,
    "axes.labelsize":       13,
    "axes.titlesize":       15,
    "axes.titleweight":     "bold",
    "figure.figsize":       (14, 8),
    "font.family":          "DejaVu Sans",
    "legend.facecolor":     "#161b22",
    "legend.edgecolor":     "#30363d",
    "legend.labelcolor":    "#e6edf3",
    "lines.linewidth":      2.0,
    "lines.antialiased":    True,
    "patch.antialiased":    True,
}

def apply_cern_style():
    """Aktiviert das CERN-Dark-Theme für alle folgenden Matplotlib-Plots."""
    plt.rcParams.update(CERN_DARK_PARAMS)

def reset_style():
    """Setzt den Matplotlib-Stil auf die Standardwerte zurück."""
    plt.rcParams.update(plt.rcParamsDefault)

# ──────────────────────────────────────────────────────────────────────────────
# HILFSFUNKTIONEN
# ──────────────────────────────────────────────────────────────────────────────

def relativistischer_impuls(masse_GeV: float, energie_GeV: float) -> float:
    """
    Berechnet den relativistischen Impuls p [GeV/c].

    Parameters
    ----------
    masse_GeV  : Ruhemasse in GeV/c²
    energie_GeV: Gesamtenergie in GeV

    Returns
    -------
    float: Impuls in GeV/c
    """
    return np.sqrt(np.maximum(energie_GeV**2 - masse_GeV**2, 0.0))


def lorentz_gamma(beta: float | np.ndarray) -> float | np.ndarray:
    """Lorentz-Faktor γ = 1/√(1-β²)."""
    return 1.0 / np.sqrt(1.0 - np.clip(beta, 0.0, 1.0 - 1e-12)**2)


def invariante_masse(E1, p1x, p1y, p1z, E2, p2x, p2y, p2z) -> float:
    """
    Berechnet die invariante Masse zweier Teilchen [GeV/c²].
    Alle Eingaben in GeV (Energie) bzw. GeV/c (Impuls).
    """
    E_ges  = E1 + E2
    px_ges = p1x + p2x
    py_ges = p1y + p2y
    pz_ges = p1z + p2z
    m2     = E_ges**2 - (px_ges**2 + py_ges**2 + pz_ges**2)
    return np.sqrt(np.maximum(m2, 0.0))


def breit_wigner(E: np.ndarray, M: float, Gamma: float) -> np.ndarray:
    """
    Breit-Wigner-Resonanzprofil (relativistisch).

    Parameters
    ----------
    E     : Energie-Array [GeV]
    M     : Resonanzmasse [GeV/c²]
    Gamma : Zerfallsbreite [GeV]

    Returns
    -------
    np.ndarray: Wirkungsquerschnitt (relative Einheiten)
    """
    return (Gamma / 2)**2 / ((E - M)**2 + (Gamma / 2)**2)


def gaussian(x: np.ndarray, mu: float, sigma: float, amplitude: float = 1.0) -> np.ndarray:
    """Normierte Gauß-Funktion."""
    return amplitude * np.exp(-0.5 * ((x - mu) / sigma)**2) / (sigma * np.sqrt(2 * np.pi))


def pseudorapidity(theta_rad: float | np.ndarray) -> float | np.ndarray:
    """
    Pseudorapidität η = -ln(tan(θ/2)).

    Parameters
    ----------
    theta_rad : Polarwinkel in Radiant

    Returns
    -------
    Pseudorapidität η
    """
    return -np.log(np.tan(theta_rad / 2.0))


def transversalimpuls(px: np.ndarray, py: np.ndarray) -> np.ndarray:
    """Transversalimpuls pT = √(px² + py²) [GeV/c]."""
    return np.sqrt(px**2 + py**2)


# ──────────────────────────────────────────────────────────────────────────────
# PLOT-HILFSFUNKTIONEN
# ──────────────────────────────────────────────────────────────────────────────

def cern_figure(nrows: int = 1, ncols: int = 1, figsize: tuple = None,
                titel: str = None, **kwargs):
    """
    Erstellt eine Matplotlib-Figure mit CERN-Stil und optionalem Haupttitel.
    """
    apply_cern_style()
    if figsize is None:
        figsize = (7 * ncols, 6 * nrows)
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize, **kwargs)
    if titel:
        fig.suptitle(titel, fontsize=16, fontweight='bold', color='#58a6ff', y=1.01)
    return fig, axes


def beschrifte_achsen(ax, xlabel: str = '', ylabel: str = '', titel: str = '',
                      einheit_x: str = '', einheit_y: str = ''):
    """Setzt Achsenbeschriftungen mit optionalen Einheiten."""
    if einheit_x:
        xlabel = f"{xlabel} [{einheit_x}]"
    if einheit_y:
        ylabel = f"{ylabel} [{einheit_y}]"
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if titel:
        ax.set_title(titel, color='#58a6ff')


def cern_legende(ax, **kwargs):
    """Fügt eine stilisierte Legende hinzu."""
    defaults = dict(framealpha=0.8, loc='best')
    defaults.update(kwargs)
    ax.legend(**defaults)


def colorbar_label(fig, sc, ax, label: str):
    """Fügt eine beschriftete Farbleiste hinzu."""
    cb = fig.colorbar(sc, ax=ax, pad=0.02)
    cb.set_label(label, color='#e6edf3')
    cb.ax.yaxis.set_tick_params(color='#8b949e')
    plt.setp(cb.ax.yaxis.get_ticklabels(), color='#8b949e')
    return cb


# ──────────────────────────────────────────────────────────────────────────────
# SIMULATIONSFUNKTIONEN
# ──────────────────────────────────────────────────────────────────────────────

def simuliere_zerfallsprodukte(n_ereignisse: int = 10_000,
                                M_mutter: float = MZ,
                                sigma_det: float = 2.5,
                                untergrund: bool = True,
                                seed: int = 42) -> np.ndarray:
    """
    Simuliert invariante Massen von Zerfallsprodukten.

    Parameters
    ----------
    n_ereignisse : Anzahl der simulierten Ereignisse
    M_mutter     : Masse des Mutterteilchens [GeV/c²]
    sigma_det    : Detektorauflösung (Gauß-Breite) [GeV]
    untergrund   : Ob ein kombinatorischer Untergrund hinzugefügt wird
    seed         : Zufallsseed für Reproduzierbarkeit

    Returns
    -------
    np.ndarray: Array der invarianten Massen [GeV/c²]
    """
    rng = np.random.default_rng(seed)
    # Signal: Breit-Wigner-Resonanz + Detektorauflösung
    n_signal = int(0.3 * n_ereignisse) if untergrund else n_ereignisse
    bw_sample = M_mutter + 2.5 * rng.standard_cauchy(n_signal)
    signal    = bw_sample + rng.normal(0, sigma_det, n_signal)
    if not untergrund:
        return signal
    # Untergrund: exponentiell fallend
    n_ug  = n_ereignisse - n_signal
    ug    = rng.exponential(scale=30, size=n_ug) + M_mutter - 40
    return np.concatenate([signal, ug])


def simuliere_kollisionsvertices(n: int = 5000, sigma_xy: float = 15e-6,
                                  sigma_z: float = 45e-3, seed: int = 0):
    """
    Simuliert Primärvertexpositionen eines LHC-Bunch-Crossings (in Metern).

    Returns
    -------
    x, y, z : np.ndarray je (n,)
    """
    rng = np.random.default_rng(seed)
    x   = rng.normal(0, sigma_xy, n)
    y   = rng.normal(0, sigma_xy, n)
    z   = rng.normal(0, sigma_z,  n)
    return x, y, z


def simuliere_jet_ereignis(n_jets: int = 4, ET_max: float = 500,
                            seed: int = 7):
    """
    Simuliert ein vereinfachtes Jet-Ereignis mit zufälligen (η, φ, ET)-Werten.

    Returns
    -------
    dict mit Arrays: 'eta', 'phi', 'ET'
    """
    rng  = np.random.default_rng(seed)
    eta  = rng.uniform(-4.5, 4.5, n_jets)
    phi  = rng.uniform(-np.pi, np.pi, n_jets)
    ET   = np.sort(rng.exponential(ET_max / 3, n_jets))[::-1]
    return {'eta': eta, 'phi': phi, 'ET': ET}


# ──────────────────────────────────────────────────────────────────────────────
# EXPERIMENTELLE DATEN (synthetisch, basierend auf realen Werten)
# ──────────────────────────────────────────────────────────────────────────────

def higgs_signifikanz_data():
    """
    Gibt beispielhafte (synthetische) Daten für die Higgs-Signifikanz-
    Entwicklung über die Zeit zurück (angelehnt an den echten LHC-Verlauf).
    """
    jahre = np.array([2011.5, 2012.0, 2012.4, 2012.7])
    signifikanz = np.array([2.3, 3.1, 4.8, 5.9])  # in σ
    return jahre, signifikanz


def standardmodell_teilchen():
    """
    Gibt ein Dictionary mit den Standardmodell-Teilchen und ihren Massen zurück.
    """
    return {
        # Quarks
        'u': {'masse': 2.2e-3,  'ladung':  2/3, 'typ': 'Quark',   'farbe': '#d62728'},
        'd': {'masse': 4.7e-3,  'ladung': -1/3, 'typ': 'Quark',   'farbe': '#ff9896'},
        's': {'masse': 0.096,   'ladung': -1/3, 'typ': 'Quark',   'farbe': '#9467bd'},
        'c': {'masse': 1.27,    'ladung':  2/3, 'typ': 'Quark',   'farbe': '#c5b0d5'},
        'b': {'masse': 4.18,    'ladung': -1/3, 'typ': 'Quark',   'farbe': '#8c564b'},
        't': {'masse': 172.69,  'ladung':  2/3, 'typ': 'Quark',   'farbe': '#c49c94'},
        # Leptonen
        'e':   {'masse': 0.511e-3, 'ladung': -1, 'typ': 'Lepton', 'farbe': '#ff7f0e'},
        'mu':  {'masse': 0.1057,   'ladung': -1, 'typ': 'Lepton', 'farbe': '#2ca02c'},
        'tau': {'masse': 1.777,    'ladung': -1, 'typ': 'Lepton', 'farbe': '#98df8a'},
        # Eichbosonen
        'gamma': {'masse': 0.0,    'ladung':  0, 'typ': 'Boson',  'farbe': '#ffd700'},
        'W':     {'masse': 80.377, 'ladung':  1, 'typ': 'Boson',  'farbe': '#7f7f7f'},
        'Z':     {'masse': 91.188, 'ladung':  0, 'typ': 'Boson',  'farbe': '#17becf'},
        'g':     {'masse': 0.0,    'ladung':  0, 'typ': 'Boson',  'farbe': '#e377c2'},
        # Higgs
        'H':     {'masse': 125.25, 'ladung':  0, 'typ': 'Higgs',  'farbe': '#aec7e8'},
    }


# ──────────────────────────────────────────────────────────────────────────────
# ECHTE DATEN: CERN OPEN DATA  (Single Source of Truth)
# ──────────────────────────────────────────────────────────────────────────────
import os, csv, urllib.request

# PDG-Massen/-Breiten der im Myon-Spektrum sichtbaren Resonanzen (GeV).
# Diese Tabelle ist die gemeinsame "physikalische Wahrheit" für Python UND das
# JS-Widget – beide Anzeigen sampeln an exakt denselben Werten.
RESONANZEN = {
    'rho/omega': dict(m=0.780,  breite=0.100, kanal='μ⁺μ⁻',  region='PILOT', farbe='#9467bd'),
    'phi':       dict(m=1.019,  breite=0.004, kanal='μ⁺μ⁻',  region='PILOT', farbe='#8c564b'),
    'J/psi':     dict(m=3.097,  breite=0.093, kanal='μ⁺μ⁻',  region='QGP',   farbe='#2ca02c'),
    'psi(2S)':   dict(m=3.686,  breite=0.030, kanal='μ⁺μ⁻',  region='QGP',   farbe='#98df8a'),
    'Upsilon1S': dict(m=9.460,  breite=0.054, kanal='μ⁺μ⁻',  region='QGP',   farbe='#d62728'),
    'Upsilon2S': dict(m=10.023, breite=0.032, kanal='μ⁺μ⁻',  region='QGP',   farbe='#ff9896'),
    'Upsilon3S': dict(m=10.355, breite=0.020, kanal='μ⁺μ⁻',  region='QGP',   farbe='#ffbb78'),
    'Z0':        dict(m=91.19,  breite=2.490, kanal='μ⁺μ⁻',  region='HIGGS', farbe='#17becf'),
    'Higgs':     dict(m=125.0,  breite=0.004, kanal='ZZ*→4ℓ', region='HIGGS', farbe='#aec7e8'),
}

# Historische LHC-Meilensteine der Higgs-Suche (für die Signifikanz-Zeitachse).
HISTORIE = {
    'evidence': dict(datum='13. Dez 2011', lumi=5.0,  sigma=3.0,
                     text='Erste Hinweise (ATLAS+CMS, 7 TeV)'),
    'discovery': dict(datum='4. Juli 2012', lumi=10.0, sigma=5.0,
                      text='Higgs-Entdeckung – 5σ'),
}

# Bestätigte, öffentlich erreichbare Quelle (CMS Run2011A DoubleMu, √s = 7 TeV).
CMS_DIMUON_URL = 'https://opendata.cern.ch/record/545/files/Dimuon_DoubleMu.csv'
_DATA_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'data'))
_SUBSET   = os.path.join(_DATA_DIR, 'cms_dimuon_subset.csv')   # echter Subset im Repo
_FULL     = os.path.join(_DATA_DIR, 'cms_dimuon_full.csv')     # optionaler Voll-Cache


def _lese_dimuon_csv(pfad, mit_kinematik=False):
    """Liest die CMS-Dimuon-CSV. Gibt M [GeV] (np.ndarray) bzw. zusätzlich
    eine Liste von Myon-Paar-Kinematiken zurück."""
    M, kin = [], []
    with open(pfad, newline='') as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                M.append(float(row['M']))
            except (KeyError, ValueError):
                continue
            if mit_kinematik:
                kin.append(dict(
                    pt1=float(row['pt1']), eta1=float(row['eta1']), phi1=float(row['phi1']), Q1=int(float(row['Q1'])),
                    pt2=float(row['pt2']), eta2=float(row['eta2']), phi2=float(row['phi2']), Q2=int(float(row['Q2'])),
                    M=M[-1]))
    return (np.asarray(M), kin) if mit_kinematik else np.asarray(M)


def lade_cms_dimuon(n=None, voll=False, timeout=30, seed=1):
    """
    Lädt ECHTE CMS-Open-Data Dimuon-Massen (Run2011A DoubleMu, √s = 7 TeV).

    Reihenfolge (Hybrid-Strategie):
      1. voller Cache  cern/data/cms_dimuon_full.csv      (falls voll=True)
      2. Voll-Download von CERN Open Data + Cachen         (falls voll=True)
      3. Repo-Subset   cern/data/cms_dimuon_subset.csv     (Standard, offline-fähig)
      4. Monte-Carlo-Fallback (PDG-kalibriert)             (wenn nichts vorhanden)

    Returns
    -------
    (M, info) : (np.ndarray invarianter Massen [GeV], dict(quelle, n))
    """
    pfad = quelle = None
    if voll:
        if os.path.exists(_FULL):
            pfad, quelle = _FULL, 'CMS Open Data – voller Cache'
        else:
            try:
                os.makedirs(_DATA_DIR, exist_ok=True)
                urllib.request.urlretrieve(CMS_DIMUON_URL, _FULL)
                pfad, quelle = _FULL, 'CMS Open Data – frisch geladen'
            except Exception:
                pfad = None
    if pfad is None and os.path.exists(_SUBSET):
        pfad, quelle = _SUBSET, 'CMS Open Data – Repo-Subset'
    if pfad is None:
        M = mc_dimuon_spektrum(n or 12000, seed=seed)
        return M, dict(quelle='Monte-Carlo-Fallback (PDG-kalibriert)', n=int(M.size))
    M = _lese_dimuon_csv(pfad)
    if n is not None and M.size > n:
        M = np.random.default_rng(seed).choice(M, n, replace=False)
    return M, dict(quelle=quelle, n=int(M.size))


def mc_dimuon_spektrum(n=12000, seed=1):
    """
    Physikalisch kalibrierter Monte-Carlo-Fallback des Dimuon-Spektrums.
    Resonanzen sitzen exakt auf den PDG-Massen (RESONANZEN); die relativen
    Häufigkeiten sind an den echten CMS-Subset angelehnt – also "physikalisch
    denkbar", nie Nonsens.
    """
    rng = np.random.default_rng(seed)
    # Relative Anteile (≈ CMS DoubleMu, trigger-geprägt): Kontinuum dominiert,
    # darüber die Resonanz-Peaks.
    anteile = {'kontinuum': 0.52, 'rho/omega': 0.05, 'phi': 0.02, 'J/psi': 0.11,
               'psi(2S)': 0.01, 'Upsilon1S': 0.13, 'Upsilon2S': 0.03,
               'Upsilon3S': 0.01, 'Z0': 0.12}
    teile = []
    for name, frac in anteile.items():
        k = max(1, int(round(frac * n)))
        if name == 'kontinuum':
            # fallendes Kontinuum 0.4–120 GeV
            teile.append(np.clip(0.4 + rng.exponential(18, k), 0.4, 120))
        else:
            r = RESONANZEN[name]
            # Voigt-artig: Breit-Wigner (natürliche Breite) + Detektorauflösung
            bw = r['m'] + (r['breite'] / 2) * rng.standard_cauchy(k)
            det = rng.normal(0, max(0.02, 0.012 * r['m']), k)  # ~1.2% Auflösung
            teile.append(bw + det)
    M = np.concatenate(teile)
    return M[(M > 0.4) & (M <= 120)]


def lade_higgs_4l(n=2000, seed=2):
    """
    Higgs-Goldkanal H→ZZ*→4ℓ – kalibriert nach den publizierten ATLAS-Open-Data
    Kennzahlen (13 TeV, 2016, 10 fb⁻¹): schmaler Signal-Peak bei 125 GeV auf
    glattem ZZ*-Kontinuum. KEINE Messung – als Simulation gekennzeichnet.
    Realistisch kleines Signal-zu-Untergrund-Verhältnis.

    Returns
    -------
    (m4l, info) : (np.ndarray 4-Lepton-Massen [GeV], dict)
    """
    rng = np.random.default_rng(seed)
    n_sig = max(1, int(round(0.06 * n)))            # ~6% Signal (rar!)
    n_bg  = n - n_sig
    sig = rng.normal(125.0, 2.0, n_sig)             # Detektoraufgelöster Peak
    bg  = 80 + rng.exponential(40, n_bg)            # ZZ*-Kontinuum
    m4l = np.concatenate([sig, bg])
    m4l = m4l[(m4l >= 80) & (m4l <= 250)]
    return m4l, dict(quelle='ATLAS-kalibrierte Simulation (H→ZZ*→4ℓ, 10 fb⁻¹)',
                     n=int(m4l.size), n_signal=n_sig)
