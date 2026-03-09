"""
GenPass - Secure password generator CLI.

This module provides functionality to generate strong, random passwords
with customizable character sets, entropy calculation, and various output formats.
"""

import argparse
import json
import math
import secrets
import string
import sys
from pathlib import Path
from typing import List, Optional

try:
    import pyperclip  # type: ignore

    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False

# Default character sets
DEFAULT_SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?"
AMBIGUOUS_CHARS = "l1IO0"

# Config file path
CONFIG_DIR = Path.home() / ".genpass"
CONFIG_FILE = CONFIG_DIR / "config.json"


def load_config() -> dict:
    """
    Load user configuration from ~/.genpass/config.json.

    Returns:
        Dictionary containing user configuration settings.
        Returns empty dict if config file doesn't exist or is invalid.
    """
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, encoding="utf-8") as f:
                config = json.load(f)
                return config if isinstance(config, dict) else {}
        except (OSError, json.JSONDecodeError):
            return {}
    return {}


def save_config(config: dict) -> None:
    """
    Save user configuration to ~/.genpass/config.json.

    Args:
        config: Dictionary containing configuration settings to save.
    """
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


def calculate_entropy(password: str, pool_size: int) -> float:
    """
    Calculate the entropy (in bits) of a generated password.

    Entropy is calculated as: length * log2(pool_size)
    Higher entropy indicates a stronger password.

    Args:
        password: The generated password.
        pool_size: Total number of possible characters in the pool.

    Returns:
        Entropy value in bits.
    """
    if pool_size <= 1:
        return 0.0
    return len(password) * math.log2(pool_size)


def get_character_pools(
    use_lower: bool,
    use_upper: bool,
    use_digits: bool,
    use_symbols: bool,
    symbol_set: str,
    exclude_ambiguous: bool,
) -> List[str]:
    """
    Build character pools based on user preferences.

    Args:
        use_lower: Include lowercase letters.
        use_upper: Include uppercase letters.
        use_digits: Include digits.
        use_symbols: Include symbols.
        symbol_set: Custom set of symbols to use.
        exclude_ambiguous: Exclude ambiguous characters (l, 1, I, O, 0).

    Returns:
        List of character pool strings.
    """
    pools = []

    if use_lower:
        chars = string.ascii_lowercase
        if exclude_ambiguous:
            chars = chars.replace("l", "")
        pools.append(chars)

    if use_upper:
        chars = string.ascii_uppercase
        if exclude_ambiguous:
            chars = chars.replace("IO", "")
        pools.append(chars)

    if use_digits:
        chars = string.digits
        if exclude_ambiguous:
            chars = chars.replace("10", "")
        pools.append(chars)

    if use_symbols:
        chars = symbol_set
        if exclude_ambiguous:
            for char in AMBIGUOUS_CHARS:
                chars = chars.replace(char, "")
        if chars:
            pools.append(chars)

    return pools


def generate_password(
    length: int,
    pools: List[str],
    ensure_each: bool = True,
) -> str:
    """
    Generate a secure random password.

    Args:
        length: Desired password length.
        pools: List of character pools to choose from.
        ensure_each: Ensure at least one character from each pool.

    Returns:
        Generated password string.

    Raises:
        ValueError: If no character pools provided or length too small.
    """
    if not pools:
        raise ValueError("No character sets selected")

    password: List[str] = []

    # Ensure at least one character from each pool
    if ensure_each:
        if length < len(pools):
            raise ValueError("Password length too small for ensure_each option")
        for pool in pools:
            password.append(secrets.choice(pool))

    # Fill remaining length with random characters from all pools
    all_chars = "".join(pools)
    while len(password) < length:
        password.append(secrets.choice(all_chars))

    # Shuffle to randomize positions
    secrets.SystemRandom().shuffle(password)

    return "".join(password)


def format_output(
    passwords: List[str],
    output_format: str,
    show_entropy: bool = False,
    entropy_value: Optional[float] = None,
) -> str:
    """
    Format passwords for output.

    Args:
        passwords: List of generated passwords.
        output_format: Output format ('plain', 'json', 'delimited').
        show_entropy: Whether to include entropy information.
        entropy_value: Entropy value to include in output.

    Returns:
        Formatted output string.
    """
    if output_format == "json":
        output_data: dict = {"passwords": passwords}
        if show_entropy and entropy_value is not None:
            output_data["entropy_bits"] = round(entropy_value, 2)
        return json.dumps(output_data, indent=2)

    if output_format == "delimited":
        result = "\n".join(passwords)
        if show_entropy and entropy_value is not None:
            result += f"\n# Entropy: {entropy_value:.2f} bits"
        return result

    # Plain format (default)
    result = "\n".join(passwords)
    if show_entropy and entropy_value is not None:
        result += f"\n# Entropy: {entropy_value:.2f} bits"
    return result


def copy_to_clipboard(text: str) -> bool:
    """
    Copy text to system clipboard.

    Args:
        text: Text to copy to clipboard.

    Returns:
        True if successful, False otherwise.
    """
    if not HAS_PYPERCLIP:
        return False
    try:
        pyperclip.copy(text)
        return True
    except Exception:
        return False


def validate_args(args: argparse.Namespace) -> None:
    """
    Validate command-line arguments.

    Args:
        args: Parsed command-line arguments.

    Raises:
        ValueError: If arguments are invalid.
    """
    if args.length <= 0:
        raise ValueError("Password length must be positive")

    if args.length > 1000:
        raise ValueError("Password length cannot exceed 1000")

    if args.count <= 0:
        raise ValueError("Password count must be positive")

    if args.count > 100:
        raise ValueError("Password count cannot exceed 100")

    if args.symbol_set and len(args.symbol_set) < 1:
        raise ValueError("Symbol set cannot be empty")


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="genpass",
        description="Secure password generator CLI - Generate strong, random passwords",
        epilog="Examples:\n"
        "  genpass                          Generate one 16-char password (all char types)\n"
        "  genpass -l 20 -n 5               Generate 5 passwords of length 20\n"
        "  genpass --lower --upper --digits Generate password without symbols\n"
        "  genpass --no-ambiguous           Exclude confusing characters\n"
        "  genpass --entropy                Show password entropy\n"
        "  genpass --format json            Output as JSON\n"
        "  genpass --clipboard              Copy to clipboard\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Password options
    parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=None,
        help="Password length (default: 16)",
    )
    parser.add_argument(
        "-n",
        "--count",
        type=int,
        default=None,
        help="Number of passwords to generate (default: 1)",
    )

    # Character sets
    parser.add_argument(
        "--lower",
        action="store_true",
        default=None,
        help="Include lowercase letters (default: yes)",
    )
    parser.add_argument(
        "--upper",
        action="store_true",
        default=None,
        help="Include uppercase letters (default: yes)",
    )
    parser.add_argument(
        "--digits",
        action="store_true",
        default=None,
        help="Include digits (default: yes)",
    )
    parser.add_argument(
        "--symbols",
        action="store_true",
        default=None,
        help="Include symbols (default: yes)",
    )
    parser.add_argument(
        "--symbol-set",
        type=str,
        default=None,
        help="Custom symbol set (default: " + DEFAULT_SYMBOLS.replace("%", "%%") + ")",
    )

    # Options
    parser.add_argument(
        "--no-ensure",
        action="store_true",
        help="Disable ensuring at least one char from each selected type",
    )
    parser.add_argument(
        "--no-ambiguous",
        action="store_true",
        help="Exclude ambiguous characters (l, 1, I, O, 0)",
    )
    parser.add_argument(
        "--entropy",
        action="store_true",
        help="Calculate and display password entropy",
    )
    parser.add_argument(
        "--clipboard",
        "-c",
        action="store_true",
        help="Copy the first password to clipboard",
    )

    # Output options
    parser.add_argument(
        "--format",
        choices=["plain", "json", "delimited"],
        default="plain",
        help="Output format (default: plain)",
    )
    parser.add_argument(
        "--config",
        action="store_true",
        help="Show current configuration and exit",
    )
    parser.add_argument(
        "--save-config",
        action="store_true",
        help="Save current options as defaults",
    )

    return parser


def apply_defaults(args: argparse.Namespace, config: dict) -> argparse.Namespace:
    """
    Apply default values from config to arguments.

    Args:
        args: Parsed command-line arguments.
        config: Loaded configuration dictionary.

    Returns:
        Updated arguments with defaults applied.
    """
    if args.length is None:
        args.length = config.get("length", 16)

    if args.count is None:
        args.count = config.get("count", 1)

    # For boolean flags, use config if not explicitly set
    if args.lower is None:
        args.lower = config.get("lower", True)

    if args.upper is None:
        args.upper = config.get("upper", True)

    if args.digits is None:
        args.digits = config.get("digits", True)

    if args.symbols is None:
        args.symbols = config.get("symbols", True)

    if args.symbol_set is None:
        args.symbol_set = config.get("symbol_set", DEFAULT_SYMBOLS)

    if not getattr(args, "no_ambiguous", False):
        args.no_ambiguous = config.get("no_ambiguous", False)

    return args


def main() -> None:
    """Main entry point for the genpass CLI."""
    parser = create_parser()
    args = parser.parse_args()

    # Load config
    config = load_config()

    # Show config if requested
    if args.config:
        if config:
            print(json.dumps(config, indent=2))
        else:
            print("No configuration file found. Using defaults.")
        return

    # Apply defaults from config
    args = apply_defaults(args, config)

    # Validate arguments
    try:
        validate_args(args)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Build character pools
    try:
        pools = get_character_pools(
            use_lower=args.lower,
            use_upper=args.upper,
            use_digits=args.digits,
            use_symbols=args.symbols,
            symbol_set=args.symbol_set,
            exclude_ambiguous=args.no_ambiguous,
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if not pools:
        print("Error: Select at least one character set", file=sys.stderr)
        sys.exit(1)

    # Generate passwords
    passwords: List[str] = []
    entropy_value: Optional[float] = None

    try:
        for _ in range(args.count):
            pwd = generate_password(
                length=args.length,
                pools=pools,
                ensure_each=not args.no_ensure,
            )
            passwords.append(pwd)

        # Calculate entropy for the first password
        if args.entropy:
            pool_size = sum(len(pool) for pool in pools)
            entropy_value = calculate_entropy(passwords[0], pool_size)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Format output
    output = format_output(
        passwords=passwords,
        output_format=args.format,
        show_entropy=args.entropy,
        entropy_value=entropy_value,
    )

    # Copy to clipboard if requested
    if args.clipboard and passwords:
        if copy_to_clipboard(passwords[0]):
            print("✓ Copied to clipboard", file=sys.stderr)
        else:
            print(
                "Warning: Clipboard functionality unavailable. Install 'pyperclip'.",
                file=sys.stderr,
            )

    # Print output
    print(output)

    # Save config if requested
    if args.save_config:
        new_config = {
            "length": args.length,
            "count": args.count,
            "lower": args.lower,
            "upper": args.upper,
            "digits": args.digits,
            "symbols": args.symbols,
            "symbol_set": args.symbol_set,
            "no_ambiguous": args.no_ambiguous,
        }
        save_config(new_config)
        print(f"✓ Configuration saved to {CONFIG_FILE}", file=sys.stderr)


if __name__ == "__main__":
    main()
