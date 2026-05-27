"""
cern_utils.py
=============
Gemeinsame Hilfsfunktionen, Konstanten und Farbschemata für die
CERN-Experiment-Visualisierungs-Suite.
"""

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
