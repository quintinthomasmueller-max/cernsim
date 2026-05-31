# ⚙️ CERN-Sim Project Command Runner (justfile)
# Verwende 'just <recipe>' zum Ausführen der Befehle.

default:
    @just --list

# Bündelt cern/app/* -> Notebook-Zelle 4 + build/ + cern/app/index.html
sync:
    python3 scripts/sync_widget.py

# Headless-Prüfung: sync + node --check + nbformat.validate + ast.parse
check:
    bash scripts/check.sh

# Startet den Jupyter Notebook Server im Root-Verzeichnis
jupyter:
    jupyter notebook --NotebookApp.default_url="/tree"

# Startet Jupyter Lab (falls bevorzugt)
lab:
    jupyter lab

# Generiert das CERN-Stellwerk-Notebook von Grund auf neu (Legacy-Generator)
generate:
    python3 cern/scripts/create_notebook.py

# Startet den interaktiven Streamlit-Simulator für die Familienstiftung
streamlit:
    streamlit run stiftung/stiftung_simulator.py

# Installiert alle benötigten Python-Bibliotheken
setup:
    pip install -r requirements.txt
