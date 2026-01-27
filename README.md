# GenPass

**Secure password generator CLI** written in Python.  
Generate strong, random passwords from the command line with customizable character sets.

---

## Features

- Specify password length and quantity
- Include/exclude:
  - Lowercase letters (`--lower`)
  - Uppercase letters (`--upper`)
  - Digits (`--digits`)
  - Symbols (`--symbols`)
- Optional custom symbol set (`--symbol-set`)
- Ensure at least one character from each selected type (can be disabled with `--no-ensure`)
- Shell completions for **bash**, **zsh**, and **fish**
- Easy installation via **pipx** or local script

---

## Installation

### 1. Via pipx (recommended)
```bash
pipx install git+https://github.com/yourusername/genpass
````

### 2. Local installation

Clone the repo and run the install script:

```bash
git clone https://github.com/yourusername/genpass.git
cd genpass
./install.sh
```

This will also set up shell completions for bash, zsh, and fish.

---

## Usage

Generate a single password (default 16 characters):

```bash
genpass --lower --upper --digits --symbols
```

Generate 5 passwords of length 20:

```bash
genpass -l 20 -n 5 --lower --upper --digits --symbols
```

Use a custom symbol set:

```bash
genpass --symbols --symbol-set "!@#%&"
```

Disable "ensure each type" rule:

```bash
genpass --lower --upper --digits --no-ensure
```

---

## Shell Completion

After installation, completions are automatically copied to your shell folders.
Restart your shell or source the completion files manually:

**Bash**

```bash
source ~/.local/share/bash-completion/completions/genpass
```

**Zsh**

```bash
source ~/.local/share/zsh/site-functions/_genpass
```

**Fish**

```fish
source ~/.local/share/fish/vendor_completions.d/genpass.fish
```

---

## Development

1. Install in editable mode for development:

```bash
pipx install --editable .
```

2. Make changes in `genpass/cli.py` and test immediately.

---

## Contributing

Contributions are welcome! Please fork the repo and submit pull requests.
Ensure code follows PEP8 style and add shell completion tests if applicable.

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

```

