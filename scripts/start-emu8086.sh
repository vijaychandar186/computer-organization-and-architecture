#!/bin/bash

pkill Xvfb || true
pkill x11vnc || true
pkill websockify || true
sleep 1

Xvfb :1 -screen 0 1280x800x24 &
sleep 2

export DISPLAY=:1

openbox &
sleep 2

x11vnc -display :1 -nopw -forever -shared -quiet &
sleep 2

websockify --web=/usr/share/novnc/ 6080 localhost:5900 &
sleep 1

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WINEARCH=win64 WINEPREFIX=~/.wine64 wine "$SCRIPT_DIR/../simulators/emu8086/setup.exe" &

echo "✅ noVNC ready at http://localhost:6080/vnc.html"
