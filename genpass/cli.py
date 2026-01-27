import argparse
import secrets
import string
import sys

def generate_password(length, pools, ensure_each=True):
    if not pools:
        raise ValueError("No character sets selected")
    password = []
    if ensure_each:
        if length < len(pools):
            raise ValueError("Password length too small")
        for pool in pools:
            password.append(secrets.choice(pool))
    all_chars = "".join(pools)
    while len(password) < length:
        password.append(secrets.choice(all_chars))
    secrets.SystemRandom().shuffle(password)
    return "".join(password)

def main():
    parser = argparse.ArgumentParser(prog="genpass", description="Secure password generator")
    parser.add_argument("-l", "--length", type=int, default=16)
    parser.add_argument("-n", "--count", type=int, default=1)
    parser.add_argument("--lower", action="store_true")
    parser.add_argument("--upper", action="store_true")
    parser.add_argument("--digits", action="store_true")
    parser.add_argument("--symbols", action="store_true")
    parser.add_argument("--symbol-set", default="!@#$%^&*()-_=+[]{};:,.<>?")
    parser.add_argument("--no-ensure", action="store_true")
    args = parser.parse_args()

    pools = []
    if args.lower: pools.append(string.ascii_lowercase)
    if args.upper: pools.append(string.ascii_uppercase)
    if args.digits: pools.append(string.digits)
    if args.symbols: pools.append(args.symbol_set)

    if not pools:
        print("Select at least one character set", file=sys.stderr)
        sys.exit(1)

    for _ in range(args.count):
        print(generate_password(args.length, pools, ensure_each=not args.no_ensure))

if __name__ == "__main__":
    main()
