#!/usr/bin/env bash
set -euo pipefail
REPO="jadhavdurvesh/MAINTAIN-AI-IoT-Gateway"
BASE_URL="https://github.com/${REPO}/releases/latest/download"
if [ ! -f /etc/os-release ]; then echo "Unsupported OS" >&2; exit 1; fi
. /etc/os-release
case "${ID:-}" in raspbian|debian|ubuntu) ;; *) echo "Unsupported OS: ${PRETTY_NAME:-unknown}" >&2; exit 1 ;; esac
ARCH="$(dpkg --print-architecture)"
case "$ARCH" in
  arm64) ASSET="MAINTAIN-AI-IoT-Gateway-linux-arm64.deb" ;;
  amd64) ASSET="MAINTAIN-AI-IoT-Gateway-linux-amd64.deb" ;;
  armhf) echo "32-bit ARM is not published yet. Use 64-bit Raspberry Pi OS." >&2; exit 1 ;;
  *) echo "Unsupported architecture: $ARCH" >&2; exit 1 ;;
esac
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
PKG="$TMP_DIR/$ASSET"
echo "Downloading MAINTAIN AI IoT Gateway ($ARCH)..."
curl --fail --location --silent --show-error --retry 3 "$BASE_URL/$ASSET" -o "$PKG"
echo "Installing MAINTAIN AI IoT Gateway..."
sudo apt-get update
sudo apt-get install -y "$PKG"
echo "Installation complete. Run: maintain-ai-iot-gateway"
