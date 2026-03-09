#!/usr/bin/env bash
set -e

if ! command -v pipx >/dev/null; then
    echo "[!] pipx not found. Install it first:"
    echo "  python3 -m pip install --user pipx"
    echo "  pipx ensurepath"
    exit 1
fi

pipx install .

PREFIX="${XDG_DATA_HOME:-$HOME/.local/share}"

mkdir -p "$PREFIX/bash-completion/completions"
mkdir -p "$PREFIX/zsh/site-functions"
mkdir -p "$PREFIX/fish/vendor_completions.d"

cp completions/genpass.bash "$PREFIX/bash-completion/completions/genpass"
cp completions/genpass.zsh  "$PREFIX/zsh/site-functions/_genpass"
cp completions/genpass.fish "$PREFIX/fish/vendor_completions.d/genpass.fish"

echo "[✓] Installation complete. Restart your shell."
echo "[✓] Clipboard support: pipx inject genpass pyperclip"
