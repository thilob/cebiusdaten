#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$ROOT_DIR"

if [[ ! -d ".venv" ]]; then
    echo "Fehler: .venv wurde nicht gefunden."
    echo "Bitte zuerst eine virtuelle Umgebung anlegen und die Abhängigkeiten installieren."
    exit 1
fi

if [[ ! -x ".venv/bin/pyinstaller" ]]; then
    echo "Fehler: PyInstaller ist in .venv nicht installiert."
    echo "Installation: .venv/bin/pip install pyinstaller"
    exit 1
fi

".venv/bin/pyinstaller" --noconfirm --clean cebiusdaten.spec
