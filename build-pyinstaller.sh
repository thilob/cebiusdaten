#!/usr/bin/env bash

# Copyright (C) 2026 Thilo Berger
# SPDX-License-Identifier: GPL-3.0-or-later

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$ROOT_DIR"

assert_release_clean() {
    local bundle_dir="$1"

    if [[ ! -d "$bundle_dir" ]]; then
        echo "Fehler: Bundle-Verzeichnis fehlt: $bundle_dir"
        exit 1
    fi

    mapfile -t unwanted < <(find "$bundle_dir" \
        \( -name 'gebref.txt' -o -name 'gebref.zip' -o -name 'output' \) \
        -print)

    if (( ${#unwanted[@]} > 0 )); then
        echo "Fehler: Das Bundle enthält Laufzeitdaten, die nicht in ein Release gehören:"
        printf ' - %s\n' "${unwanted[@]}"
        echo "Bitte dist/ bereinigen und den Build erneut erzeugen."
        exit 1
    fi
}

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

".venv/bin/pyinstaller" --noconfirm --clean adressdatentool.spec

assert_release_clean "${ROOT_DIR}/dist/adressdatentool"
