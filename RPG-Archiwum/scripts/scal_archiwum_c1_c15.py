#!/usr/bin/env python3
"""Rebuild the shareable C1-C15 combined archive from its existing 15 parts.

Run from any directory:
    python RPG-Archiwum/scripts/scal_archiwum_c1_c15.py
Only reads the already redacted 'wersja_do_udostepniania' files.
Does not modify originals, memory cards or current scene.
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "01_ARCHIWA_CZATY" / "wersja_do_udostepniania"
DEST = SOURCE / "01_ARCHIWUM_CZAT_1-15_SCALONE.txt"
COUNTS = [2389, 1800, 1412, 1333, 766, 436, 710, 757, 418, 506, 409, 1109, 1029, 704, 1350]
EXACT = re.compile(r"(?m)^\[(C\d+-M\d+)\]\s*$")

def main():
    sections = []
    total = 0
    for i, count in enumerate(COUNTS, 1):
        path = SOURCE / f"01_ARCHIWUM_CZAT_{i}.txt"
        if not path.is_file():
            raise SystemExit(f"Missing source part: {path}")
        value = path.read_text(encoding="utf-8")
        ids = EXACT.findall(value)
        expected = [f"C{i}-M{j:04d}" for j in range(1, count + 1)]
        if ids != expected:
            raise SystemExit(f"ID order or completeness failed: C{i} got {len(ids)} expected {count}")
        sections.append(value.rstrip())
        total += len(ids)
    if total != 15128:
        raise SystemExit("Unexpected number of messages")
    text = "\n\n\n".join(sections) + "\n"
    DEST.write_text(text, encoding="utf-8")
    print(f"Created {DEST}: {total} messages, {DEST.stat().st_size} bytes")
    print("Source files unchanged; source redactions remain in place.")

if __name__ == "__main__":
    main()
