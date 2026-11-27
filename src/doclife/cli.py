"""Command line entry point."""

import argparse
from collections.abc import Sequence
from importlib.metadata import version


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="doclife", description="Frontmatter checks for docs in git."
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {version('doclife')}"
    )
    parser.parse_args(argv)
    return 0
