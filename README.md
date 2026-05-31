# PhytonNotebook

Sammlung von Python-Notebooks und Simulationen rund um Physik-Visualisierung.

## Projektstruktur

```
PhytonNotebook/
├── README.md
├── requirements.txt          # gebündelte Abhängigkeiten
├── .gitignore
│
├── cern/                     # CERN-Beschleuniger-Visualisierung
│   ├── notebooks/
│   │   └── CERN_Beschleuniger_Schaltzentrale.ipynb
│   ├── scripts/
│   │   ├── cern_utils.py
│   │   └── create_notebook.py
│   ├── data/
│   ├── resources/
│   └── output/
│
├── akkretion/                # Akkretions-Physik
│   └── notebooks/
│       ├── Akkretion.ipynb
│       └── Akkretion_Test.ipynb
│
└── stiftung/                 # Streamlit-Stiftungs-Simulator
    └── stiftung_simulator.py
```

## Teilprojekte

### CERN-Beschleuniger-Visualisierung (`cern/`)
Interaktive Simulation und Visualisierung eines Teilchenbeschleunigers.

- `notebooks/CERN_Beschleuniger_Schaltzentrale.ipynb` – Haupt-Notebook (Schaltzentralen-Ansicht)
- `notebooks/CERN_Beschleuniger_Schaltzentrale.py` – jupytext-Spiegel (`py:percent`, diffbar; via `jupytext --sync` gekoppelt)
- `app/` – modulare Widget-Quellen (JS/CSS/HTML), gebündelt von `scripts/sync_widget.py` in Zelle 4
- `scripts/cern_utils.py` – Hilfsfunktionen (Physik, Massenspektrum, Kollisionen)
- `scripts/create_notebook.py` – Legacy-Generator (erzeugt das Notebook von Grund auf)
- `data/`, `resources/`, `output/` – Daten, Ressourcen und Ausgaben

### Akkretions-Notebooks (`akkretion/`)
Physik-Simulationen zur Akkretion.

- `notebooks/Akkretion.ipynb`
- `notebooks/Akkretion_Test.ipynb`

### Stiftungs-Simulator (`stiftung/`)
- `stiftung_simulator.py` – Streamlit-App zur Kapitalstock-Simulation einer deutschen Familienstiftung (UHNW). Parameter wie Rendite, Inflation, interne Stiftungssteuer und Entnahmestrategie sind interaktiv einstellbar.

Starten mit:
```bash
streamlit run stiftung/stiftung_simulator.py
```

## Voraussetzungen

- Python 3.x
- Abhängigkeiten installieren:

```bash
pip install -r requirements.txt
```

## Nutzung

Notebooks öffnen mit:
```bash
jupyter notebook
```

## Repository

Git-Remote: `git@github.com:asmuelle/cernsim.git`
