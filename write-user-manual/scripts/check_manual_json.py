#!/usr/bin/env python3
"""Check manual locale JSON files for consistency.

Usage: python check_manual_json.py th/manual.json en/manual.json [more locales...]

Reports:
  - keys present in some locale files but missing in others
  - empty string values
  - leftover markers: [ต้องตรวจ] (unverified) and [ต้องแปล] (untranslated)
Exit code 0 if no problems, 1 otherwise.
"""
import json
import sys

MARKERS = ("[ต้องตรวจ]", "[ต้องแปล]", "TODO")


def flatten(node, prefix=""):
    out = {}
    if isinstance(node, dict):
        for k, v in node.items():
            out.update(flatten(v, f"{prefix}.{k}" if prefix else k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            out.update(flatten(v, f"{prefix}[{i}]"))
    else:
        out[prefix] = node
    return out


def main(paths):
    if len(paths) < 1:
        print(__doc__)
        return 2
    data = {}
    for p in paths:
        try:
            with open(p, encoding="utf-8") as f:
                data[p] = flatten(json.load(f))
        except Exception as e:  # invalid JSON or unreadable file
            print(f"ERROR  {p}: {e}")
            return 1

    problems = 0
    all_keys = set().union(*(set(d) for d in data.values()))

    for p, d in data.items():
        missing = sorted(all_keys - set(d))
        for k in missing:
            print(f"MISSING  {p}: {k}")
            problems += 1
        for k, v in d.items():
            if isinstance(v, str):
                if not v.strip():
                    print(f"EMPTY    {p}: {k}")
                    problems += 1
                for m in MARKERS:
                    if m in v:
                        print(f"MARKER   {p}: {k} contains {m}")
                        problems += 1

    print(f"\nFiles: {len(data)} | keys (union): {len(all_keys)} | problems: {problems}")
    return 0 if problems == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
