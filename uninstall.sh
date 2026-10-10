#!/usr/bin/env bash
set -euo pipefail

INSTALL_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/media-tui"
SYSTEM_BIN_DIR="/usr/local/bin"

printf "Uninstalling terminal-media-monitoring-tool...\n"

if [[ -d "$INSTALL_DIR" ]]; then
    rm -rf "$INSTALL_DIR"
    printf "Removed %s\n" "$INSTALL_DIR"
fi

if [[ -e "$SYSTEM_BIN_DIR/media_tui" || -L "$SYSTEM_BIN_DIR/media_tui" ]]; then
    if [[ -w "$SYSTEM_BIN_DIR" ]]; then
        rm -f "$SYSTEM_BIN_DIR/media_tui"
        printf "Removed %s/media_tui\n" "$SYSTEM_BIN_DIR"
    elif command -v sudo >/dev/null 2>&1; then
        sudo rm -f "$SYSTEM_BIN_DIR/media_tui"
        printf "Removed %s/media_tui using sudo\n" "$SYSTEM_BIN_DIR"
    else
        printf "Warning: Could not remove %s/media_tui (requires sudo).\n" "$SYSTEM_BIN_DIR" >&2
    fi
fi

if [[ -e "$HOME/.local/bin/media_tui" || -L "$HOME/.local/bin/media_tui" ]]; then
    rm -f "$HOME/.local/bin/media_tui"
    printf "Removed %s/.local/bin/media_tui\n" "$HOME"
fi

printf "Uninstallation complete.\n"
