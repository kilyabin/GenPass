# GenPass

**Secure password generator CLI** written in Python.
Generate strong, random passwords from the command line with customizable character sets.

---

## Features

- **Default behavior**: All character types enabled by default (lowercase, uppercase, digits, symbols)
- Specify password length (`-l`) and quantity (`-n`)
- Include/exclude character types:
  - `--lower` - Lowercase letters
  - `--upper` - Uppercase letters
  - `--digits` - Digits
  - `--symbols` - Symbols
- `--no-ambiguous` - Exclude confusing characters (l, 1, I, O, 0)
- `--symbol-set` - Custom symbol set
- `--no-ensure` - Disable "at least one from each type" rule
- `--entropy` - Calculate and display password entropy
- `--clipboard` / `-c` - Copy password to clipboard
- `--format` - Output format: `plain`, `json`, `delimited`
- `--save-config` - Save current options as defaults
- `--config` - Show current configuration
- Shell completions for **bash**, **zsh**, and **fish**

---

## Installation

### 1. Via pipx (recommended)

```bash
pipx install git+https://github.com/kilyabin/GenPass
```

### 2. Local installation

Clone the repo and run the install script:

```bash
git clone https://github.com/kilyabin/GenPass.git
cd GenPass
./install.sh
```

### 3. Development installation

```bash
pipx install --editable .
# or
pip install -e .
```

---

## Usage

### Basic Usage

Generate a single password (default 16 characters, all character types):

```bash
genpass
```

Generate a password with specific character types:

```bash
genpass --lower --upper --digits --symbols
```

### Length and Quantity

Generate 5 passwords of length 20:

```bash
genpass -l 20 -n 5
```

Generate a 32-character password:

```bash
genpass -l 32
```

### Character Sets

Password without symbols (only letters and digits):

```bash
genpass --lower --upper --digits
```

Only lowercase and digits:

```bash
genpass --lower --digits
```

Use a custom symbol set:

```bash
genpass --symbols --symbol-set "!@#%&"
```

### Excluding Ambiguous Characters

Exclude confusing characters like `l`, `1`, `I`, `O`, `0`:

```bash
genpass --no-ambiguous
```

Combine with other options:

```bash
genpass -l 20 --no-ambiguous --lower --upper --digits
```

### Output Formats

Plain text (default):

```bash
genpass -n 3
```

JSON format:

```bash
genpass -n 3 --format json
```

Output:
```json
{
  "passwords": [
    "abc123...",
    "def456...",
    "ghi789..."
  ]
}
```

Delimited format (one per line):

```bash
genpass -n 3 --format delimited
```

### Entropy Calculation

Display password entropy (in bits):

```bash
genpass --entropy
```

Output:
```
Kx9#mP2$vL5@nQ8w
# Entropy: 94.56 bits
```

### Clipboard Support

Copy the generated password to clipboard:

```bash
genpass --clipboard
# or
genpass -c
```

Output:
```
✓ Copied to clipboard
Kx9#mP2$vL5@nQ8w
```

> **Note**: Clipboard support requires `pyperclip`. Install with `pip install pyperclip`.

### Configuration

Save default settings:

```bash
genpass -l 24 --no-ambiguous --save-config
```

Show current configuration:

```bash
genpass --config
```

Configuration is stored in `~/.genpass/config.json`.

---

## Examples

### Real-world Usage

**Generate a password for a website:**
```bash
genpass -l 16 --clipboard
```

**Generate multiple passwords and save to file:**
```bash
genpass -n 10 -l 20 --format json > passwords.json
```

**Generate a memorable password (no ambiguous chars):**
```bash
genpass -l 12 --no-ambiguous
```

**Generate a high-entropy password:**
```bash
genpass -l 32 --entropy
```

**Script-friendly JSON output:**
```bash
genpass --format json | jq -r '.passwords[0]'
```

**Set default password length for all future sessions:**
```bash
genpass -l 20 --save-config
genpass  # Now generates 20-char passwords by default
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

1. Install in editable mode:
```bash
pipx install --editable .
# or
pip install -e .
```

2. Install dev dependencies:
```bash
pip install -e ".[dev]"
```

3. Run linting:
```bash
ruff check genpass/
mypy genpass/
black --check genpass/
```

4. Run tests:
```bash
pytest
```

---

## API Usage

Use GenPass as a Python library:

```python
from genpass import generate_password, get_character_pools, calculate_entropy

# Get character pools
pools = get_character_pools(
    use_lower=True,
    use_upper=True,
    use_digits=True,
    use_symbols=True,
    symbol_set="!@#$%",
    exclude_ambiguous=False,
)

# Generate password
password = generate_password(length=16, pools=pools)
print(password)

# Calculate entropy
entropy = calculate_entropy(password, sum(len(p) for p in pools))
print(f"Entropy: {entropy:.2f} bits")
```

---

## Command-Line Options

```
positional arguments:
  (none)

options:
  -h, --help            Show help message
  -l, --length LENGTH   Password length (default: 16)
  -n, --count COUNT     Number of passwords (default: 1)
  --lower               Include lowercase letters
  --upper               Include uppercase letters
  --digits              Include digits
  --symbols             Include symbols
  --symbol-set SET      Custom symbol set
  --no-ensure           Disable ensure-each-type rule
  --no-ambiguous        Exclude ambiguous characters
  --entropy             Show password entropy
  -c, --clipboard       Copy to clipboard
  --format FORMAT       Output format: plain, json, delimited
  --config              Show current configuration
  --save-config         Save options as defaults
```

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting (`pytest`, `ruff check`, `mypy`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style

This project uses:
- **Black** for code formatting
- **Ruff** for linting
- **MyPy** for type checking

Install dev dependencies and set up pre-commit hooks:

```bash
pip install -e ".[dev]"
pre-commit install
```

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.
