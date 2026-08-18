#!/usr/bin/env bash
# Render all frame HTML files to 4K PNGs with headless Chromium.
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
OUT="$SRC/../frames"
CHROME="/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
mkdir -p "$OUT"
for f in "$SRC"/[0-9][0-9]-*.html; do
  name="$(basename "$f" .html)"
  "$CHROME" --no-sandbox --disable-gpu --hide-scrollbars \
    --force-device-scale-factor=2 --window-size=1920,1080 \
    --virtual-time-budget=6000 \
    --screenshot="$OUT/$name.png" "file://$f" 2>/dev/null
  echo "rendered $name.png"
done
