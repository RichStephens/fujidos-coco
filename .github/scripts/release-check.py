#!/usr/bin/env python3
"""Check the ROM's banner version against CHANGELOG.md and an optional tag; print the release notes."""

import re
import sys

BANNER = b"FUJI-DOS "
HEADING = re.compile(r"^## \[([^\]]+)\]")


def fail(message):
    print(f"::error::{message}", file=sys.stderr)
    sys.exit(1)


def rom_version(path):
    with open(path, "rb") as f:
        rom = f.read()
    start = rom.find(BANNER)
    if start < 0:
        fail(f"{path} has no sign-on banner.")
    start += len(BANNER)
    return rom[start:rom.index(b" ", start)].decode("ascii")


def changelog_section(path):
    with open(path) as f:
        lines = f.read().splitlines()
    for i, line in enumerate(lines):
        match = HEADING.match(line)
        if match and match.group(1) != "Unreleased":
            end = next((j for j in range(i + 1, len(lines)) if lines[j].startswith("## ")), len(lines))
            return match.group(1), "\n".join(lines[i + 1:end]).strip()
    fail(f"{path} has no numbered section.")


def main():
    if len(sys.argv) < 3:
        sys.exit("usage: release-check.py ROM CHANGELOG [TAG]")
    rom, changelog = sys.argv[1], sys.argv[2]
    version = rom_version(rom)
    newest, notes = changelog_section(changelog)

    if newest != version:
        fail(f"The banner says {version}, but the newest section in {changelog} is [{newest}].")
    if len(sys.argv) > 3 and sys.argv[3] != version:
        fail(f"The banner says {version}, but the tag is {sys.argv[3]}.")
    if not notes:
        fail(f"The [{version}] section in {changelog} is empty.")
    print(notes)


if __name__ == "__main__":
    main()
