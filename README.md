# cebiusdaten

Gebäudereferenzen können hier abgerufen werden:
<https://www.opengeodata.nrw.de/produkte/geobasis/lk/akt/gebref_txt/>

Copyright 2026 Thilo Berger

## Lizenz

Dieses Projekt steht unter der **GNU General Public License v3.0 oder spaeter**
(`GPL-3.0-or-later`).

Das passt zur gewuenschten Vorgabe:

- Der Quellcode darf genutzt, verändert und weitergegeben werden.
- Bei Weitergabe veränderter oder unveränderter Fassungen muss der Quellcode
  ebenfalls wieder unter derselben freien Copyleft-Lizenz verfügbar bleiben.

Der vollstaendige Lizenztext liegt in [COPYING](/home/thilo/p/cebiusdaten/COPYING).

## Überblick

Die Anwendung läuft als Desktop-GUI auf Basis von `PySide6` und verarbeitet die
NRW-Gebäudereferenzen dateibasiert ohne Datenbank.

Die bisherigen Kernfunktionen der TUI bleiben erhalten:

- Gebäudereferenzen prüfen oder herunterladen
- Landkreise aus der Quelldatei einlesen
- Auswahl eines Landkreises in einer filterbaren, scrollbaren Liste
- Export von `__Gemeindeliste.txt` sowie Straßen- und Hausnummerndateien
- Automatisches Öffnen des Ausgabeordners nach erfolgreichem Export

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
- Aktualisierung der Desktop-Datenbank, falls verfügbar

Danach sollte die Anwendung im KDE-Anwendungsmenü erscheinen.

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

Ziel dieser Vorbereitung ist ein `--onedir`-Bundle, das möglichst ohne
nachzuinstallierende Python-Bibliotheken läuft. Verifizieren lässt sich das
endgültig nur durch einen echten Build und Test auf Windows.

## Verhalten im Bundle

- Die Anwendung arbeitet relativ zum Verzeichnis der ausfuehrbaren Datei.
- `gebref.txt`, `gebref.zip` und `output/` liegen neben dem Bundle.
- Falls `gebref.txt` fehlt oder älter als 24 Stunden ist, wird die Datei beim Start heruntergeladen.
- Der GUI-Start kann mit `--smoke-test` kurz automatisiert getestet werden.

## Dokumentierte Änderungen

Stand: 15.03.2026

- Umstellung auf die dateibasierte `geopandas`-Verarbeitung
- Desktop-GUI auf Basis von `PySide6`
- Speicherschonender Landkreis-Ladevorgang für die GUI
- Vorbereitung für `PyInstaller --onedir` unter Linux und Windows
- Linux-Installationsskripte inklusive KDE-Menüeintrag
