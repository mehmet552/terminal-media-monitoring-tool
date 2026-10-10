#!/usr/bin/env bash
set -euo pipefail

REPOSITORY_URL="https://github.com/mehmet552/terminal-media-monitoring-tool.git"
INSTALL_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/media-tui"
SYSTEM_BIN_DIR="/usr/local/bin"

fail() {
    printf 'Error: %s\n' "$*" >&2
    exit 1
}

if [[ $EUID -eq 0 ]]; then
    fail "Run this installer as your normal user, without sudo. It will request sudo only for system package installation and the /usr/local/bin command link."
fi

install_system_packages() {
    local package_manager=""
    local packages=()

    if [[ -r /etc/os-release ]]; then
        # shellcheck disable=SC1091
        . /etc/os-release
    else
        fail "Cannot identify this Linux distribution (/etc/os-release is missing)."
    fi

    case "${ID:-}" in
        ubuntu|debian|linuxmint)
            package_manager="apt-get"
            packages=(git playerctl python3 python3-venv)
            ;;
        fedora)
            package_manager="dnf"
            packages=(git playerctl python3 python3-pip)
            ;;
        *)
            fail "Automatic installation supports Ubuntu and Fedora. Install git, playerctl, and Python 3 manually, then retry."
            ;;
    esac

    if [[ $EUID -eq 0 ]]; then
        SUDO=()
    elif command -v sudo >/dev/null 2>&1; then
        SUDO=(sudo)
    else
        fail "sudo is required to install system packages."
    fi

    if [[ "$package_manager" == "apt-get" ]]; then
        "${SUDO[@]}" apt-get update
    fi
    "${SUDO[@]}" "$package_manager" install -y "${packages[@]}"
}

if ! command -v git >/dev/null 2>&1 \
    || ! command -v playerctl >/dev/null 2>&1 \
    || ! command -v python3 >/dev/null 2>&1; then
    install_system_packages
fi

command -v git >/dev/null 2>&1 || fail "git was not found after installing system packages."
command -v playerctl >/dev/null 2>&1 || fail "playerctl was not found after installing system packages."
command -v python3 >/dev/null 2>&1 || fail "python3 was not found after installing system packages."

if [[ -r /etc/os-release ]]; then
    # shellcheck disable=SC1091
    . /etc/os-release
fi
case "${ID:-}" in
    ubuntu|debian|linuxmint)
        if ! dpkg-query -W -f='${Status}' python3-venv 2>/dev/null | grep -q 'install ok installed'; then
            install_system_packages
        fi
        ;;
    fedora)
        if ! rpm -q python3-pip >/dev/null 2>&1; then
            install_system_packages
        fi
        ;;
esac

mkdir -p "$(dirname "$INSTALL_DIR")"
if [[ -d "$INSTALL_DIR/.git" ]]; then
    git -C "$INSTALL_DIR" pull --ff-only
elif [[ -e "$INSTALL_DIR" ]]; then
    fail "$INSTALL_DIR already exists and is not a Git clone. Move it aside and retry."
else
    git clone --depth 1 "$REPOSITORY_URL" "$INSTALL_DIR"
fi

python3 -m venv "$INSTALL_DIR/.venv"
"$INSTALL_DIR/.venv/bin/python" -m pip install --disable-pip-version-check -r "$INSTALL_DIR/requirements.txt"

if [[ -e "$SYSTEM_BIN_DIR/media_tui" || -L "$SYSTEM_BIN_DIR/media_tui" ]]; then
    if [[ "$(readlink -f "$SYSTEM_BIN_DIR/media_tui")" != "$(readlink -f "$INSTALL_DIR/media_tui")" ]]; then
        fail "$SYSTEM_BIN_DIR/media_tui already exists and points elsewhere. It was left unchanged; inspect it before replacing it."
    fi
elif [[ -w "$SYSTEM_BIN_DIR" ]]; then
    ln -s "$INSTALL_DIR/media_tui" "$SYSTEM_BIN_DIR/media_tui"
elif command -v sudo >/dev/null 2>&1; then
    sudo ln -s "$INSTALL_DIR/media_tui" "$SYSTEM_BIN_DIR/media_tui"
else
    fail "Cannot install the media_tui command in $SYSTEM_BIN_DIR: write access or sudo is required."
fi

printf '\nInstallation complete. Open any terminal and run: media_tui\n'
