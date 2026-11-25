#!/usr/bin/env python3
"""One-line office joke for make.fun's "One-Line Office Jokes".

The joke is a module constant: one line about office life, kept in the
source so the entry is fully self-contained and deterministic. Running
this program validates the line against the bounty gate (UTF-8, one
line, 1 to 199 characters, not only whitespace) and writes it to
``entry.txt`` in the output directory.

Usage:
    python3 main.py [--out-dir DIR] [--check-only]

The output directory defaults to $MAKEFUN_OUTPUT_DIR, else /output.
With --check-only the joke is validated and nothing is written.
"""

import argparse
import os
import sys
from pathlib import Path

JOKE = (
    "Our manager calls us a family, which is why the Wi-Fi password "
    "is a secret and nobody is allowed to leave the group chat."
)

MAX_CHARS = 199
OUT_NAME = "entry.txt"


def parse_args(argv):
    """Parse the command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out-dir",
        default=None,
        help="directory to write entry.txt into (default: $MAKEFUN_OUTPUT_DIR or /output)",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="validate the joke and exit without writing anything",
    )
    return parser.parse_args(argv)


def out_dir(cli_value):
    """Resolve the output directory from the flag, the env, or the default."""
    if cli_value:
        return Path(cli_value)
    env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env:
        return Path(env)
    return Path("/output")


def checked_bytes(joke):
    """Encode the joke and check it against the gate; return its bytes."""
    if "\n" in joke or "\r" in joke:
        raise ValueError("joke must be a single line")
    if not joke.strip():
        raise ValueError("joke must not be blank")
    if len(joke) > MAX_CHARS:
        raise ValueError(f"joke is {len(joke)} chars; the gate allows {MAX_CHARS}")
    return joke.encode("utf-8")


def main(argv=None):
    args = parse_args(argv)
    try:
        data = checked_bytes(JOKE)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if args.check_only:
        print(f"ok: {len(JOKE)} chars, one line")
        return 0
    target_dir = out_dir(args.out_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / OUT_NAME
    target.write_bytes(data + b"\n")
    written = target.read_bytes()
    if written != data + b"\n":
        print(f"error: {target} did not round-trip byte-for-byte", file=sys.stderr)
        return 1
    print(f"wrote {target} ({len(JOKE)} chars, verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
