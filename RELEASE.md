# Release-Checkliste

Copyright (C) 2026 Thilo Berger
Lizenz: `GPL-3.0-or-later`

Stand: 19.03.2026

## Vor dem Push

1. Abhängigkeiten in `.venv` installieren.
2. Linux-Build neu erzeugen:

```bash
./build-pyinstaller.sh
```

Das Build-Skript bricht jetzt ab, falls `dist/adressdatentool/` versehentlich
`gebref.txt`, `gebref.zip` oder `output/` enthält.

3. Build prüfen:

```bash
./dist/adressdatentool/adressdatentool --help
QT_QPA_PLATFORM=offscreen ./dist/adressdatentool/adressdatentool --smoke-test
```

4. Optional lokale Benutzerinstallation prüfen:

```bash
./install-linux.sh
./uninstall-linux.sh
```

Bei der Linux-Benutzerinstallation liegt `output/` danach neben der
Binärdatei in `~/.local/bin/adressdatentool/`.

5. Auf Windows separat prüfen:

```bat
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\pip install pyinstaller
build-windows.bat
dist\adressdatentool\adressdatentool.exe
```

## GitHub-Push

1. Änderungen prüfen:

```bash
git status
git diff
```

2. Relevante Dateien stagen:

```bash
git add build-pyinstaller.sh build-windows.bat adressdatentool.spec run.sh README.md RELEASE.md
```

3. Commit erstellen:

```bash
git commit -m "Harden PyInstaller release build"
```

4. Branch `main` nach GitHub pushen:

```bash
git push origin main
```

5. Release-Assets optional ueber GitHub Actions bauen:

Workflow: `.github/workflows/build-release-assets.yml`
