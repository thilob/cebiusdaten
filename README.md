# cebiusdaten

Gebäudereferenzen können hier abgerufen werden:
<https://www.opengeodata.nrw.de/produkte/geobasis/lk/akt/gebref_txt/>

## Überblick

Die Anwendung laeuft als Desktop-GUI auf Basis von `PySide6` und verarbeitet die
NRW-Gebaeudereferenzen dateibasiert ohne Datenbank.

Die bisherigen Kernfunktionen der TUI bleiben erhalten:

- Gebaeudereferenzen pruefen oder herunterladen
- Landkreise aus der Quelldatei einlesen
- Auswahl eines Landkreises in einer filterbaren, scrollbaren Liste
- Export von `__Gemeindeliste.txt` sowie Strassen- und Hausnummerndateien
- Automatisches Oeffnen des Ausgabeordners nach erfolgreichem Export

## Installation unter Linux

### Voraussetzungen

- Python 3.14 oder kompatibel
- `venv`
- ein grafischer Linux-Desktop, z. B. KDE Plasma

### Lokaler Start aus dem Projekt

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python main.py
```

### Build des distributierbaren Bundles

```bash
.venv/bin/pip install pyinstaller
./build-pyinstaller.sh
```

Das Ergebnis liegt danach in `dist/cebiusdaten/`.

### Installation als Benutzeranwendung inklusive KDE-Menüeintrag

Nach dem Build:

```bash
./install-linux.sh
```

Das Skript erledigt:

- Kopieren des Bundles nach `~/.local/opt/cebiusdaten`
- Anlegen eines Starters in `~/.local/bin/cebiusdaten`
- Anlegen eines `.desktop`-Eintrags in `~/.local/share/applications/cebiusdaten.desktop`
- Aktualisierung der Desktop-Datenbank, falls verfuegbar

Danach sollte die Anwendung im KDE-Anwendungsmenue erscheinen.

### Deinstallation unter Linux

```bash
./uninstall-linux.sh
```

## Build unter Windows

Ein Windows-Bundle muss auf Windows selbst erstellt werden.
Der vorbereitete Aufruf ist:

```bat
build-windows.bat
```

Oder manuell:

```bat
.venv\Scripts\pyinstaller.exe --noconfirm --clean cebiusdaten.spec
```

Ziel dieser Vorbereitung ist ein `--onedir`-Bundle, das moeglichst ohne
nachzuinstallierende Python-Bibliotheken laeuft. Verifizieren laesst sich das
endgueltig nur durch einen echten Build und Test auf Windows.

## Verhalten im Bundle

- Die Anwendung arbeitet relativ zum Verzeichnis der ausfuehrbaren Datei.
- `gebref.txt`, `gebref.zip` und `output/` liegen neben dem Bundle.
- Falls `gebref.txt` fehlt oder aelter als 24 Stunden ist, wird die Datei beim Start heruntergeladen.
- Der GUI-Start kann mit `--smoke-test` kurz automatisiert getestet werden.

## Dokumentierte Änderungen

Stand: 15.03.2026

- Umstellung auf die dateibasierte `geopandas`-Verarbeitung
- Desktop-GUI auf Basis von `PySide6`
- Speicherschonender Landkreis-Ladevorgang fuer die GUI
- Vorbereitung fuer `PyInstaller --onedir` unter Linux und Windows
- Linux-Installationsskripte inklusive KDE-Menüeintrag
