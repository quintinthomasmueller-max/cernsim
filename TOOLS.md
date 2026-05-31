# 🛠️ CERN-Sim Software & Physics Tools (TOOLS.md)

Dieses Dokument bietet eine vollständige Übersicht über die im Repository vorhandenen Skripte, mathematischen Hilfsfunktionen und geometrischen Layouts. Jeder Coding-Agent **muss** dieses Dokument lesen, bevor er neuen Code schreibt, um Redundanz zu vermeiden und bestehende Schnittstellen korrekt zu nutzen.

---

## 📦 1. Der Physik- & Utility-Kernel (`cern_utils.py`)

Unter `CERN_Visualisierung/scripts/cern_utils.py` liegt das mathematische Herzstück des Projekts. Es enthält physikalische Konstanten, relativistische Kinematik und synthetische Event-Generatoren.

### Physikalische Konstanten (`PhysConstants` / `PC`)
Alle Einheiten sind in standardmäßigen SI-Einheiten definiert, ergänzt durch Umrechnungsfaktoren für das natürliche System ($\hbar = c = 1$, Energie in $\text{GeV}$ bzw. $\text{TeV}$).

| Konstante | Code-Name | Wert (SI) | Beschreibung |
| :--- | :--- | :--- | :--- |
| $c$ | `PC.c` | $2.99792458 \times 10^8\text{ m/s}$ | Lichtgeschwindigkeit |
| $\hbar$ | `PC.hbar` | $1.05457182 \times 10^{-34}\text{ J}\cdot\text{s}$ | Reduziertes Planck-Wirkungsquantum |
| $e$ | `PC.e` | $1.60217663 \times 10^{-19}\text{ C}$ | Elementarladung |
| $m_e$ | `PC.me` | $9.10938370 \times 10^{-31}\text{ kg}$ | Elektronenruhemasse ($511\text{ keV/c}^2$) |
| $m_p$ | `PC.mp` | $1.67262192 \times 10^{-27}\text{ kg}$ | Protonenruhemasse ($938.27\text{ MeV/c}^2$) |
| $\alpha$ | `PC.alpha` | $\approx 1/137.036$ | Feinstrukturkonstante |
| $\text{GeV}$ | `PC.GeV` | $1.60217663 \times 10^{-10}\text{ J}$ | Joule-Äquivalent für 1 GeV |

### Wichtige Kinematik-Funktionen

*   `relativistischer_impuls(masse_GeV, energie_GeV) -> float`:
    Berechnet den relativistischen Impuls $p = \sqrt{E^2 - m^2}$ in $\text{GeV/c}$.
*   `lorentz_gamma(beta) -> float | np.ndarray`:
    Berechnet den Lorentz-Faktor $\gamma = 1/\sqrt{1-\beta^2}$.
*   `invariante_masse(E1, px1, py1, pz1, E2, px2, py2, pz2) -> float`:
    Berechnet die invariante Rekonstruktionsmasse zweier Zerfallsprodukte:
    $$M = \sqrt{(E_1 + E_2)^2 - (\vec{p}_1 + \vec{p}_2)^2}$$
*   `breit_wigner(E, M, Gamma) -> np.ndarray`:
    Berechnet das relativistische Breit-Wigner-Resonanzprofil (Wirkungsquerschnitt) für instabile Teilchen wie das $Z^0$-Boson.
*   `pseudorapidity(theta_rad) -> float | np.ndarray`:
    Berechnet den Raumwinkel-Ersatz $\eta = -\ln(\tan(\theta/2))$.

### Simulations- & Eventgeneratoren
*   `simuliere_zerfallsprodukte(n_ereignisse, M_mutter, sigma_det, untergrund, seed)`:
    Simuliert Detektordaten einer Resonanz mit gaußförmiger Detektorunschärfe und exponentiellem kombinatorischen Untergrund.
*   `simuliere_kollisionsvertices(n, sigma_xy, sigma_z, seed)`:
    Generiert 3D-Bunch-Kreuzungspositionen (Luminous Region) in Metern.
*   `simuliere_jet_ereignis(n_jets, ET_max, seed)`:
    Simuliert Jet-Topologien mit ($\eta, \phi, E_T$)-Vektoren.

---

## 🎛️ 2. Der Dashboard-Generator (`create_notebook.py`)

Die Datei `CERN_Visualisierung/scripts/create_notebook.py` ist ein Metaprogrammierungs-Skript. Es generiert das voll-interaktive Jupyter-Notebook `CERN_Beschleuniger_Schaltzentrale.ipynb` im Hauptverzeichnis. 

### Geometrisches Layout (SVG-Koordinaten)
Damit die Teilchenstrahlen flüssig und physikalisch korrekt von einem Beschleunigerring in den nächsten springen, basiert das SVG-Stellwerk auf exakter Trigonometrie. Wenn du Änderungen am Layout vornimmst, **musst** du diese Radien und Zentren beachten:

*   **LHC**: Zentrum $(350, 240)$, Radius $r = 180\text{ px}$.
*   **SPS**: Zentrum $(400, 148)$, Radius $r = 65\text{ px}$.
*   **PS**: Zentrum $(242, 332)$, Radius $r = 38\text{ px}$.
*   **PSB / LEIR**: Zentrum $(142, 385)$ / $(142, 275)$, Radien $r = 18\text{ px}$.

#### Berechnete Einspeisewinkel (Junctions)
Die Transferlinien (z. B. TI 2 und TI 8) nutzen quadratische Bezier-Kurven (`Q`), deren Start- und Endpunkte exakt auf den Außenradien der Ringe liegen:
*   **SPS Auskopplung TI 2**: Winkel $\approx 2.77\text{ rad}$ (Richtung ALICE).
*   **SPS Auskopplung TI 8**: Winkel $\approx 0.61\text{ rad}$ (Richtung LHCb).
*   **LHC Einspeisung TI 2 (ALICE)**: Exakt bei $180^\circ$ (links im LHC-Ring).
*   **LHC Einspeisung TI 8 (LHCb)**: Exakt bei $0^\circ$ (rechts im LHC-Ring).

### Interaktiver JS-Kernel im Notebook
Das Notebook bettet eine hochoptimierte CSS/JS-Webapplikation direkt in die Output-Zelle ein. Sie steuert:
1.  **Strahl-Injektion**: Führt asynchrone CSS-Animationen entlang der berechneten SVG-Pfade aus.
2.  **LHC-Orbit**: Animiert persistente Teilchenpakete im Uhrzeigersinn (Beam 1) und gegen den Uhrzeigersinn (Beam 2).
3.  **Energie-Ramp**: Erhöht synchron Magnetfeld $B$, Lorentz-Faktor $\gamma$ und Strahlenergie von $450\text{ GeV}$ auf $6.8\text{ TeV}$ (Protonen).
4.  **Kollision & Analyse**: Simuliert Teilchenspuren auf einem HTML5 Canvas und befüllt in Echtzeit ein interaktives Histogramm (Massenspektrum) für Higgs- und $Z^0$-Bosonen bzw. $J/\psi$- und $\Upsilon$-Mesonen.

---

## 📈 3. Der UHNW Familienstiftungs-Simulator (`stiftung_simulator.py`)

Im Root-Verzeichnis befindet sich `stiftung_simulator.py`. Dies ist eine **Streamlit-App**, die das Finanzvermögen einer deutschen Familienstiftung unter Berücksichtigung steuerlicher und inflationärer Effekte simuliert.

### Finanzmathematisches Modell

*   **Bruttoertrag**: $E_{\text{gross}} = C_t \times r_{\text{gross}}$
*   **Stiftungsinterne Steuer**: $T_{\text{inside}} = E_{\text{gross}} \times t_{\text{internal}}$
*   **Nettoertrag im Körperschafts-Mantel**: $E_{\text{net}} = E_{\text{gross}} - T_{\text{inside}}$
*   **Ausschüttungs-Steuer**: Da Ausschüttungen an Destinatäre der Abgeltungsteuer unterliegen, muss für einen gewünschten Netto-Konsum ($K_{\text{net}}$) der Brutto-Ausschüttungsbetrag hochgerechnet werden:
    $$K_{\text{gross}} = \frac{K_{\text{net}}}{1 - t_{\text{abgeltung}}}$$
    *(Mit festem Abgeltungsteuersatz + Solidaritätszuschlag $t_{\text{abgeltung}} = 26,375\%$)*
*   **Kapitalfortschreibung (Nominal)**:
    $$C_{t+1} = C_t + E_{\text{net}} - K_{\text{gross}}$$
*   **Kapitalfortschreibung (Real, inflationsbereinigt)**:
    $$C^{\text{real}}_{t} = \frac{C_t}{(1 + \text{Inflation})^t}$$

### Design & Visualisierung
Die App nutzt ein zweispaltiges Layout (Sidebar für Simulationsparameter, Hauptbereich für Metriken und Plots) und zeichnet die nominalen und realen Vermögenskurven mit hochauflösenden, interaktiven **Plotly-Graphen** (`go.Scatter`).

---

## 🪐 4. Die Akkretions-Simulationen (`AkkretionTest.ipynb`)

Diese Jupyter-Notebooks modellieren die Strömungsdynamik und Masseakkretion (z. B. auf Schwarze Löcher oder stellare Objekte).
*   **Modell**: Disk-Struktur basierend auf der Shakura-Sunyaev-Viskositätsformulierung ($\alpha$-Disk).
*   **Numerik**: Lösung der partiellen Differentialgleichung für den Drehimpulstransport und die viskose Wärmeentwicklung in Polarkoordinaten.
*   **Visualisierung**: Radiale Dichteprofile, Temperaturgradienten und dreidimensionale Darstellungen der Akkretionsscheibe.
