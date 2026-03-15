# cebiusdaten

Gebäudereferenzen können hier abgerufen werden:
<https://www.opengeodata.nrw.de/produkte/geobasis/lk/akt/gebref_txt/>

## Dokumentierte Änderungen

Stand: 15.03.2026

- Die Dateinamenerzeugung wurde auf `python-slugify` umgestellt.
- Das bisherige Dateinamenschema bleibt erhalten: Kreis und Gemeinde werden mit Unterstrich getrennt, Umlaute bleiben in den Ausgabedateien erhalten.
- Die alte, nicht mit Python 3 kompatible Abhängigkeit `slugify==0.0.1` wurde ersetzt.
- `requirements.txt` wurde auf die direkt für das Projekt benötigten Pakete reduziert:
  `geopandas`, `pandas`, `python-slugify`, `requests`, `rich`, `tqdm`.
- Die lokale virtuelle Umgebung wurde bereinigt; nicht benötigte Alt- und Fremdpakete wurden entfernt.

## PyInstaller (`--onedir`)

Das Projekt ist für einen Build mit PyInstaller im Modus `--onedir` vorbereitet.

### Vorbereitung

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/pip install pyinstaller
```

### Build

```bash
./build-pyinstaller.sh
```

Alternativ direkt:

```bash
.venv/bin/pyinstaller --noconfirm --clean cebiusdaten.spec
```

Das Build-Ergebnis liegt danach unter `dist/cebiusdaten/`.

### Verhalten im Bundle

- Die Anwendung arbeitet im Verzeichnis der erzeugten ausführbaren Datei.
- `gebref.txt`, `gebref.zip` und das Verzeichnis `output/` werden relativ zum Bundle abgelegt.
- Falls `gebref.txt` fehlt oder älter als 24 Stunden ist, wird die Datei beim Start erneut heruntergeladen.
