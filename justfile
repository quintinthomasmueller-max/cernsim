# ⚙️ CERN-Sim Project Command Runner (justfile)
# Verwende 'just <recipe>' zum Ausführen der Befehle.

default:
    @just --list

# Startet den Jupyter Notebook Server im Root-Verzeichnis
jupyter:
    jupyter notebook --NotebookApp.default_url="/tree"

# Startet Jupyter Lab (falls bevorzugt)
lab:
    jupyter lab

# Generiert das physikalisch kohärente CERN-Stellwerk-Notebook neu
generate:
    python CERN_Visualisierung/scripts/create_notebook.py

# Startet den interaktiven Streamlit-Simulator für die Familienstiftung
streamlit:
    streamlit run stiftung_simulator.py

# Installiert alle benötigten Python-Bibliotheken für die Simulationen
setup:
    pip install numpy scipy matplotlib pandas plotly streamlit jupyter jupyterlab
