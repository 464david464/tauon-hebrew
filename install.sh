#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FLATPAK_DATA="$HOME/.var/app/com.github.taiko2k.tauonmb/data"
NATIVE_DATA="$HOME/.local/share/TauonMusicBox"

echo "=== מתקין תרגום עברי מלא ל-Tauon Music Box ==="

# סגירת האפליקציה אם היא פועלת כרגע כדי שלא תדרוס הגדרות בעת היציאה
if command -v flatpak >/dev/null 2>&1; then
    flatpak kill com.github.taiko2k.tauonmb 2>/dev/null || true
fi
pkill -f "/app/bin/tauon" 2>/dev/null || true
sleep 1

# 1. התקנה עבור Flatpak
if [ -d "$HOME/.var/app/com.github.taiko2k.tauonmb" ] || (command -v flatpak >/dev/null 2>&1 && flatpak info com.github.taiko2k.tauonmb >/dev/null 2>&1); then
    echo "-> זוהתה התקנת Flatpak של Tauon Music Box"
    TAUON_DIR="$FLATPAK_DATA/TauonMusicBox"
    mkdir -p "$TAUON_DIR/locale/he/LC_MESSAGES"

    cp "$SCRIPT_DIR/locale/he/LC_MESSAGES/tauon.po" "$TAUON_DIR/locale/he/LC_MESSAGES/tauon.po"
    cp "$SCRIPT_DIR/locale/he/LC_MESSAGES/tauon.mo" "$TAUON_DIR/locale/he/LC_MESSAGES/tauon.mo"
    cp "$SCRIPT_DIR/config/tauon_he.conf" "$TAUON_DIR/tauon_he.conf"
    cp "$SCRIPT_DIR/config/input_he.txt" "$TAUON_DIR/input_he.txt"

    if [ ! -f "$TAUON_DIR/tauon.conf" ]; then
        cp "$SCRIPT_DIR/config/tauon_he.conf" "$TAUON_DIR/tauon.conf"
    else
        sed -i 's/^display-language = .*/display-language = "he"/' "$TAUON_DIR/tauon.conf"
    fi
    cp "$SCRIPT_DIR/config/input_he.txt" "$TAUON_DIR/input.txt"

    # התקנת usercustomize.py לכל גרסאות Python הרלוונטיות בסביבת ה-Flatpak
    for pyver in 3.12 3.13 3.14 3.15; do
        SITE_DIR="$FLATPAK_DATA/python/lib/python${pyver}/site-packages"
        mkdir -p "$SITE_DIR"
        cp "$SCRIPT_DIR/usercustomize.py" "$SITE_DIR/usercustomize.py"
    done
    echo "✓ הותקן בהצלחה עבור Flatpak"
fi

# 2. התקנה מקומית (Native) אם קיימת
if [ -d "$NATIVE_DATA" ]; then
    echo "-> זוהתה התקנה מקומית ב-$NATIVE_DATA"
    mkdir -p "$NATIVE_DATA/locale/he/LC_MESSAGES"
    cp "$SCRIPT_DIR/locale/he/LC_MESSAGES/tauon.po" "$NATIVE_DATA/locale/he/LC_MESSAGES/tauon.po"
    cp "$SCRIPT_DIR/locale/he/LC_MESSAGES/tauon.mo" "$NATIVE_DATA/locale/he/LC_MESSAGES/tauon.mo"
    cp "$SCRIPT_DIR/config/tauon_he.conf" "$NATIVE_DATA/tauon_he.conf"
    cp "$SCRIPT_DIR/config/input_he.txt" "$NATIVE_DATA/input_he.txt"
    cp "$SCRIPT_DIR/config/input_he.txt" "$NATIVE_DATA/input.txt"
    if [ -f "$NATIVE_DATA/tauon.conf" ]; then
        sed -i 's/^display-language = .*/display-language = "he"/' "$NATIVE_DATA/tauon.conf"
    fi
    echo "✓ הותקן בהצלחה עבור התקנה מקומית"
fi

echo "=== ההתקנה הושלמה! ניתן להפעיל את Tauon Music Box בעברית ==="
