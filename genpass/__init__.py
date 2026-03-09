"""
GenPass - Secure password generator.

This package provides functionality to generate strong, random passwords
with customizable character sets and various security features.

Example usage:
    >>> from genpass import generate_password, get_character_pools
    >>> pools = get_character_pools(True, True, True, True, "!@#$%", False)
    >>> password = generate_password(16, pools)
    >>> print(password)
"""

from genpass.cli import (
    AMBIGUOUS_CHARS,
    DEFAULT_SYMBOLS,
    calculate_entropy,
    generate_password,
    get_character_pools,
)

__version__ = "2.0.0"
__all__ = [
    "generate_password",
    "get_character_pools",
    "calculate_entropy",
    "DEFAULT_SYMBOLS",
    "AMBIGUOUS_CHARS",
    "__version__",
]
