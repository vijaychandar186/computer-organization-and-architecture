#!/bin/bash
set -e

sudo apt-get update
sudo apt-get install -y \
  xvfb \
  x11vnc \
  novnc \
  websockify \
  openbox \
  xterm \
  python3 \
  python3-pip \
  g++ \
  cabextract

echo "Installing fonts for PC Building Simulator..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FONTS_DIR=~/.wine64/drive_c/windows/Fonts
mkdir -p "$FONTS_DIR"
for exe in "$SCRIPT_DIR/fonts/"*.exe; do
    cabextract -q -d "$FONTS_DIR" "$exe" 2>/dev/null || true
done
echo "Fonts installed."

echo "Setup done."