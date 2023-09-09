#!/usr/bin/env python3
import sys
import argparse

sys.path.append("../../libs/pybackpack")
from pybackpack.cryptography import SecretGenerator


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a random password.")

    parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=20,
        help="The length of the password.",
    )
    parser.add_argument(
        "--exclude", nargs="*", help="List of punctuation groups to exclude."
    )

    parser.add_argument(
        "--alphanumeric",
        action="store_true",
        help="Create an alphanumeric password.",
    )

    parser.add_argument(
        "--use-only-safe-chars",
        action="store_true",
        help="Use only alphanumeric characters and safe characters (- and _).",
    )

    # Add number of punctionation occurrences
    parser.add_argument(
        "--punctuation-occurrences",
        type=int,
        default=4,
        help="Number of punctuations in the password.",
    )

    args = parser.parse_args()

    pass_gen = SecretGenerator(
        length=args.length,
        punctuation_occurrences=args.punctuation_occurrences,
        exclude_groups=args.exclude if args.exclude else [],
        alphanumeric=args.alphanumeric,
        use_only_safe_chars=args.use_only_safe_chars,
    )
    print(pass_gen.generate())
