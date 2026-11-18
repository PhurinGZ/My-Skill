#!/usr/bin/env python3
"""
build_tree.py — Walk a local directory and produce a clean, noise-free
project tree, plus a list of likely documentation files worth reading
for annotation context.

This does the deterministic, mechanical part (walking the filesystem,
skipping junk directories, respecting .gitignore, capping huge folders)
so the model doesn't have to write ad-hoc traversal code every time and
doesn't burn context listing thousands of files.

Usage:
    python3 build_tree.py <path> [--max-depth 4] [--max-entries 15]
                           [--format text|json] [--exclude "pattern,pattern"]
"""

import argparse
import fnmatch
import json
import os
import sys

DEFAULT_EXCLUDES = [
    ".git", ".hg", ".svn",
    "node_modules", "bower_components",
    "__pycache__", "*.pyc", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".venv", "venv", "env", ".env",
    "dist", "build", "out", "target", ".next", ".nuxt", ".turbo", ".parcel-cache",
    ".idea", ".vscode", ".DS_Store",
    "coverage", ".coverage", "htmlcov",
    "vendor", ".terraform",
    "*.egg-info", ".tox",
]

# Files worth reading to understand what a project / subfolder is for.
DOC_HINT_PATTERNS = [
    "README*", "readme*",
    "CONTRIBUTING*", "CHANGELOG*", "ARCHITECTURE*",
    "docs", "doc",
    "package.json", "pyproject.toml", "setup.py", "setup.cfg",
    "Cargo.toml", "go.mod", "composer.json", "pom.xml", "build.gradle",
    "*.md",
]


def load_gitignore_patterns(root):
    """Very lightweight .gitignore reader — good enough to skip the
    obvious noise a repo already declared, not a full git-match engine."""
    patterns = []
    gi_path = os.path.join(root, ".gitignore")
    if os.path.isfile(gi_path):
        try:
            with open(gi_path, "r", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    patterns.append(line.rstrip("/"))
        except OSError:
            pass
    return patterns


def is_excluded(name, patterns):
    return any(fnmatch.fnmatch(name, pat) for pat in patterns)


def is_doc_hint(name):
    return any(fnmatch.fnmatch(name, pat) for pat in DOC_HINT_PATTERNS)


def walk(path, patterns, max_depth, max_entries, depth=0):
    """Returns a nested dict tree and collects doc-hint file paths."""
    node = {"name": os.path.basename(path.rstrip("/")) or path, "type": "dir", "children": []}
    doc_hits = []

    try:
        entries = sorted(os.listdir(path), key=lambda s: s.lower())
    except (PermissionError, FileNotFoundError, NotADirectoryError):
        return node, doc_hits

    dirs, files = [], []
    for e in entries:
        if is_excluded(e, patterns):
            continue
        full = os.path.join(path, e)
        if os.path.isdir(full):
            dirs.append(e)
        else:
            files.append(e)

    for e in files:
        if is_doc_hint(e):
            doc_hits.append(os.path.join(path, e))

    if depth >= max_depth:
        total = len(dirs) + len(files)
        if total:
            node["truncated"] = total
        return node, doc_hits

    visible = dirs + files
    shown = visible[:max_entries]
    hidden_count = len(visible) - len(shown)

    for e in shown:
        full = os.path.join(path, e)
        if e in dirs:
            child, sub_hits = walk(full, patterns, max_depth, max_entries, depth + 1)
            node["children"].append(child)
            doc_hits.extend(sub_hits)
        else:
            node["children"].append({"name": e, "type": "file"})

    if hidden_count > 0:
        node["children"].append({"name": f"... {hidden_count} more", "type": "note"})

    return node, doc_hits


def render_text(node, prefix=""):
    lines = []
    children = node.get("children", [])
    for i, child in enumerate(children):
        last = i == len(children) - 1
        connector = "└── " if last else "├── "
        suffix = "/" if child.get("type") == "dir" else ""
        lines.append(f"{prefix}{connector}{child['name']}{suffix}")
        if child.get("type") == "dir":
            extension = "    " if last else "│   "
            lines.extend(render_text(child, prefix + extension))
        if child.get("truncated"):
            extension = "    " if last else "│   "
            lines.append(f"{prefix}{extension}└── ... {child['truncated']} more items (max depth reached)")
    return lines


def main():
    ap = argparse.ArgumentParser(description="Build a clean project tree from a local folder.")
    ap.add_argument("path", help="Path to the repo/folder to scan")
    ap.add_argument("--max-depth", type=int, default=4, help="Max folder depth to descend (default 4)")
    ap.add_argument("--max-entries", type=int, default=15, help="Max entries shown per folder before summarizing (default 15)")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    ap.add_argument("--exclude", default="", help="Comma-separated extra glob patterns to exclude")
    args = ap.parse_args()

    root = os.path.abspath(args.path)
    if not os.path.isdir(root):
        print(f"Error: not a directory: {root}", file=sys.stderr)
        sys.exit(1)

    patterns = list(DEFAULT_EXCLUDES)
    patterns += load_gitignore_patterns(root)
    if args.exclude:
        patterns += [p.strip() for p in args.exclude.split(",") if p.strip()]

    tree, doc_hits = walk(root, patterns, args.max_depth, args.max_entries)

    # De-dupe doc hits, keep relative paths, cap the list so it stays skimmable.
    seen = set()
    rel_docs = []
    for d in doc_hits:
        rel = os.path.relpath(d, root)
        if rel not in seen:
            seen.add(rel)
            rel_docs.append(rel)
    rel_docs.sort()

    if args.format == "json":
        print(json.dumps({"root": root, "tree": tree, "doc_hints": rel_docs[:40]}, indent=2))
    else:
        print(f"{os.path.basename(root)}/")
        for line in render_text(tree):
            print(line)
        print()
        print("Likely documentation files to read for annotations:")
        if rel_docs:
            for d in rel_docs[:40]:
                print(f"  - {d}")
            if len(rel_docs) > 40:
                print(f"  ... and {len(rel_docs) - 40} more")
        else:
            print("  (none found — consider inferring from file/folder names only)")


if __name__ == "__main__":
    main()
