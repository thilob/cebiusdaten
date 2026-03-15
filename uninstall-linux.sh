#!/usr/bin/env bash

set -euo pipefail

APP_NAME="cebiusdaten"
INSTALL_BASE="${HOME}/.local/opt/${APP_NAME}"
BIN_FILE="${HOME}/.local/bin/${APP_NAME}"
DESKTOP_FILE="${HOME}/.local/share/applications/${APP_NAME}.desktop"

rm -f "${BIN_FILE}" "${DESKTOP_FILE}"
rm -rf "${INSTALL_BASE}"

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "${HOME}/.local/share/applications" >/dev/null 2>&1 || true
fi

echo "Cebiusdaten wurde aus der lokalen Benutzerinstallation entfernt."
