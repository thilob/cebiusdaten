# Adressdatentool

Copyright (C) 2026 Thilo Berger
Lizenz: `GPL-3.0-or-later`

Gebäudereferenzen können hier abgerufen werden:
<https://www.opengeodata.nrw.de/produkte/geobasis/lk/akt/gebref_txt/>

## Lizenz

Dieses Projekt steht unter der **GNU General Public License v3.0 oder spaeter**
(`GPL-3.0-or-later`).

Das passt zur gewuenschten Vorgabe:

- Der Quellcode darf genutzt, verändert und weitergegeben werden.
- Bei Weitergabe veränderter oder unveränderter Fassungen muss der Quellcode
  ebenfalls wieder unter derselben freien Copyleft-Lizenz verfügbar bleiben.

Der vollstaendige Lizenztext liegt in [COPYING](COPYING).
Eine kompakte Projekt- und Lizenznotiz liegt in [NOTICE.md](NOTICE.md).

## Überblick

Die Anwendung läuft als Desktop-GUI auf Basis von `PySide6` und verarbeitet die
NRW-Gebäudereferenzen dateibasiert ohne Datenbank.

Der Repository-Zustand ist dabei bewusst schlank gehalten:

- Beispiel- und Exportverzeichnisse werden nicht mehr mit ausgeliefert.
- `output/` entsteht erst zur Laufzeit auf dem Zielsystem und wird nicht mit ausgeliefert.
- Das distributierbare Artefakt ist ein PyInstaller-`--onedir`-Bundle.

Die bisherigen Kernfunktionen der TUI bleiben erhalten:

- Gebäudereferenzen prüfen oder herunterladen
- Landkreise aus der Quelldatei einlesen
- Auswahl eines Landkreises in einer filterbaren, scrollbaren Liste
- Export von `__Gemeindeliste.txt` sowie Straßen- und Hausnummerndateien
- Auswahl eines Ausgabeordners direkt beim Start des Exports
- Automatisches Öffnen des gewählten Ausgabeordners nach erfolgreichem Export

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

Alternativ steht unter Linux auch das Hilfsskript bereit:

```bash
./run.sh
```

### Build des distributierbaren Bundles

```bash
.venv/bin/pip install pyinstaller
./build-pyinstaller.sh
```

Das Ergebnis liegt danach in `dist/adressdatentool/`.
Die startbare Datei liegt unter Linux in `dist/adressdatentool/adressdatentool`.

Verifiziert wurde der aktuelle Linux-Build mit:

```bash
./dist/adressdatentool/adressdatentool --help
QT_QPA_PLATFORM=offscreen ./dist/adressdatentool/adressdatentool --smoke-test
```

Hinweis:
Im aktuellen Linux-Build gibt PyInstaller weiterhin eine Warnung zu
`libtiff.so.5` fuer ein optionales Qt-Bildformat-Plugin aus. Der verifizierte
Programmstart des Bundles wird dadurch derzeit nicht blockiert.

### Installation als Benutzeranwendung inklusive KDE-Menüeintrag

Nach dem Build:

```bash
./install-linux.sh
```

Das Skript erledigt:

- Kopieren des Bundles nach `~/.local/bin/adressdatentool`
- Anlegen eines `.desktop`-Eintrags in `~/.local/share/applications/adressdatentool.desktop`
- Aktualisierung der Desktop-Datenbank, falls verfügbar

Danach sollte die Anwendung im KDE-Anwendungsmenü erscheinen.
Bei der installierten Linux-Variante liegt `output/` damit direkt neben der
Binärdatei `~/.local/bin/adressdatentool/adressdatentool`.

### Deinstallation unter Linux

```bash
./uninstall-linux.sh
```

## Installation unter Windows

Plattformneutrale GitHub-Releases koennen neben dem Linux-Archiv auch ein
Windows-Archiv enthalten. Falls kein passendes Windows-Asset verfuegbar ist,
kann die Anwendung auf einem Windows-System lokal gebaut werden.

### Voraussetzungen

- Windows 10 oder neuer
- Python 3.14 oder kompatibel
- `pip`

### Lokaler Start aus dem Projekt

In einer Eingabeaufforderung oder PowerShell im Projektverzeichnis:

```bat
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python main.py
```

### Build des distributierbaren Bundles

Ein Windows-Bundle muss auf Windows selbst erstellt werden.
Der vorbereitete Aufruf ist:

```bat
build-windows.bat
```

Oder manuell:

```bat
.venv\Scripts\pyinstaller.exe --noconfirm --clean adressdatentool.spec
```

Ziel dieser Vorbereitung ist ein `--onedir`-Bundle, das möglichst ohne
nachzuinstallierende Python-Bibliotheken läuft. Die Spec sammelt dafür jetzt
auch die Laufzeit-Submodule und Metadaten von `geopandas`, `pyproj` und
`shapely` ein.

Die erwartete startbare Datei liegt auf Windows in:

```text
dist\adressdatentool\adressdatentool.exe
```

### Start und Nutzung unter Windows

Nach einem erfolgreichen Windows-Build kann die Anwendung direkt über
`dist\adressdatentool\adressdatentool.exe` gestartet werden.

Ein separater Windows-Installer wird derzeit nicht erzeugt. Das `dist`-
Verzeichnis muss daher als Ganzes zusammenbleiben.

Die erzeugten Exportdateien landen zur Laufzeit in dem Verzeichnis, das beim
Start des Exports ausgewählt wird.

Ohne native Windows-Laufzeitumgebung lässt sich das endgültig nicht
verifizieren; der Buildpfad und die Spec wurden aber plattformneutral dafür
vorbereitet.

## Verhalten im Bundle

- Die Anwendung arbeitet relativ zum Verzeichnis der ausfuehrbaren Datei.
- `gebref.txt` und `gebref.zip` liegen neben dem Bundle.
- `output/` wird erst zur Laufzeit bei Bedarf erzeugt und nicht mit ausgeliefert.
- Schon der Download-Vorgang kann `output/` vorbereiten, auch wenn noch kein Export erfolgt ist.
- Falls `gebref.txt` fehlt oder älter als 24 Stunden ist, wird die Datei beim Start heruntergeladen.
- Der GUI-Start kann mit `--smoke-test` kurz automatisiert getestet werden.

## Release-Hinweise

Eine kompakte Checkliste fuer Build, Verifikation und GitHub-Push liegt in
[RELEASE.md](RELEASE.md).

Fuer veroeffentlichte Versionen ist kuenftig ein gemeinsames Tag-Schema wie
`v0.1.1` vorgesehen, unter dem getrennte Linux- und Windows-Assets liegen.

## Dokumentierte Änderungen

Stand: 19.03.2026

- Umstellung auf die dateibasierte `geopandas`-Verarbeitung
- Desktop-GUI auf Basis von `PySide6`
- Speicherschonender Landkreis-Ladevorgang für die GUI
- Vorbereitung für `PyInstaller --onedir` unter Linux und Windows
- Linux-Installationsskripte inklusive KDE-Menüeintrag
- Windows-Installation und Windows-Build in der README dokumentiert
- GitHub-Actions-Workflow fuer Linux- und Windows-Release-Assets vorbereitet
- PyInstaller-Spec für `geopandas`-, `pyproj`- und `shapely`-Runtime gehärtet
- Linux-Build erneut verifiziert, inklusive Smoke-Test des Dist-Artefakts
- Mitgelieferte Output-Verzeichnisse aus dem Repository entfernt
- Release-Build durch Schutzpruefung gegen versehentlich mitverpackte Laufzeitdaten abgesichert
