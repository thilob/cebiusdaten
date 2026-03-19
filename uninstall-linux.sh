#!/usr/bin/env bash

# Copyright (C) 2026 Thilo Berger
# SPDX-License-Identifier: GPL-3.0-or-later

set -euo pipefail

APP_NAME="adressdatentool"
INSTALL_BASE="${HOME}/.local/bin/${APP_NAME}"
DESKTOP_FILE="${HOME}/.local/share/applications/${APP_NAME}.desktop"

rm -f "${DESKTOP_FILE}"
rm -rf "${INSTALL_BASE}"

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "${HOME}/.local/share/applications" >/dev/null 2>&1 || true
fi

echo "Adressdatentool wurde aus der lokalen Benutzerinstallation entfernt."
