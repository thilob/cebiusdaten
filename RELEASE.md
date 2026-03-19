# Release-Checkliste

Stand: 19.03.2026

## Vor dem Push

1. Abhängigkeiten in `.venv` installieren.
2. Linux-Build neu erzeugen:

```bash
./build-pyinstaller.sh
```

3. Build prüfen:

```bash
./dist/cebiusdaten/cebiusdaten --help
QT_QPA_PLATFORM=offscreen ./dist/cebiusdaten/cebiusdaten --smoke-test
```

4. Optional lokale Benutzerinstallation prüfen:

```bash
./install-linux.sh
./uninstall-linux.sh
```

5. Auf Windows separat prüfen:

```bat
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\pip install pyinstaller
build-windows.bat
dist\cebiusdaten\cebiusdaten.exe
```

## GitHub-Push

1. Änderungen prüfen:

```bash
git status
git diff
```

2. Relevante Dateien stagen:

```bash
git add cebiusdaten.spec run.sh README.md RELEASE.md
```

3. Commit erstellen:

```bash
git commit -m "Harden PyInstaller release build"
```

4. Branch `neueGUI` nach GitHub pushen:

```bash
git push origin neueGUI
```
