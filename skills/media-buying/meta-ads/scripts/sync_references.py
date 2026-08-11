#!/usr/bin/env python3
"""Check or update skill references from the canonical research directory."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
TARGET_DIR = SKILL_DIR / "references"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        required=True,
        type=Path,
        help="Canonical research directory containing numbered Markdown files.",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Report drift without writing.")
    mode.add_argument("--write", action="store_true", help="Copy changed references.")
    return parser.parse_args()


def numbered_markdown(directory: Path) -> dict[str, Path]:
    return {
        path.name: path
        for path in sorted(directory.glob("[0-9][0-9]-*.md"))
        if path.is_file()
    }


def main() -> int:
    args = parse_args()
    source_dir = args.source.expanduser().resolve()
    if not source_dir.is_dir():
        print(f"Source directory does not exist: {source_dir}", file=sys.stderr)
        return 2

    source_files = numbered_markdown(source_dir)
    if not source_files:
        print(f"No numbered Markdown references found in: {source_dir}", file=sys.stderr)
        return 2

    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    target_files = numbered_markdown(TARGET_DIR)
    changed = [
        name
        for name, source in source_files.items()
        if name not in target_files or source.read_bytes() != target_files[name].read_bytes()
    ]
    extra = sorted(set(target_files) - set(source_files))

    if args.write:
        for name in changed:
            shutil.copy2(source_files[name], TARGET_DIR / name)
            print(f"updated {name}")
        if not changed:
            print("references already synchronized")
    else:
        for name in changed:
            print(f"out of sync: {name}")

    for name in extra:
        print(f"extra target file (not removed): {name}", file=sys.stderr)

    if args.check and (changed or extra):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
