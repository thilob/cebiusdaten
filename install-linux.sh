#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_NAME="cebiusdaten"
INSTALL_BASE="${HOME}/.local/opt/${APP_NAME}"
BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
DESKTOP_FILE="${DESKTOP_DIR}/cebiusdaten.desktop"
WRAPPER_FILE="${BIN_DIR}/cebiusdaten"

mkdir -p "${INSTALL_BASE}" "${BIN_DIR}" "${DESKTOP_DIR}"

if [[ ! -x "${ROOT_DIR}/dist/cebiusdaten/cebiusdaten" ]]; then
    echo "Kein Build gefunden. Erzeuge zuerst das Bundle mit ./build-pyinstaller.sh"
    exit 1
fi

rm -rf "${INSTALL_BASE}"
mkdir -p "${INSTALL_BASE}"
cp -a "${ROOT_DIR}/dist/cebiusdaten/." "${INSTALL_BASE}/"
cp "${ROOT_DIR}/assets/cebiusdaten.svg" "${INSTALL_BASE}/cebiusdaten.svg"

cat > "${WRAPPER_FILE}" <<EOF
#!/usr/bin/env bash
set -euo pipefail
cd "${INSTALL_BASE}"
exec "${INSTALL_BASE}/cebiusdaten" "\$@"
EOF
chmod +x "${WRAPPER_FILE}"

sed "s|\${INSTALL_DIR}|${INSTALL_BASE}|g" "${ROOT_DIR}/linux/cebiusdaten.desktop" > "${DESKTOP_FILE}"

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true
fi

echo "Installation abgeschlossen."
echo "Programmdateien: ${INSTALL_BASE}"
echo "Starter: ${WRAPPER_FILE}"
echo "Menüeintrag: ${DESKTOP_FILE}"
