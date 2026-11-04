#!/usr/bin/env python3
"""Build the round-82 C1 junk control tree from a JSON spec (deterministic).

junk_tree_build.py --spec junk-tree.json --out DIR

Writes every `files[]` entry under DIR and prints one line per file with its
sha256 plus a final `tree_sha256=<digest>` over the sorted (path, sha256)
pairs, so two builds can be compared without a filesystem walk. Exit 0 built,
2 bad spec, 64 usage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--spec", required=True)
    parser.add_argument("--out", required=True)
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 64
    try:
        with open(args.spec, encoding="utf-8") as stream:
            spec = json.load(stream)
        files = spec["files"]
        if not isinstance(files, list) or not files:
            raise ValueError("spec.files must be a non-empty list")
    except (OSError, json.JSONDecodeError, KeyError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    pairs = []
    for entry in files:
        path, content = entry.get("path"), entry.get("content")
        if not isinstance(path, str) or not isinstance(content, str):
            print("error: every file needs string path and content", file=sys.stderr)
            return 2
        if path.startswith("/") or ".." in path.split("/"):
            print(f"error: unsafe path {path}", file=sys.stderr)
            return 2
        target = os.path.join(args.out, path)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        data = content.encode("utf-8")
        with open(target, "wb") as stream:
            stream.write(data)
        digest = hashlib.sha256(data).hexdigest()
        pairs.append((path, digest))
        print(f"{path} sha256={digest}")
    rolled = hashlib.sha256("\n".join(f"{path} {digest}" for path, digest
                                      in sorted(pairs)).encode("utf-8")).hexdigest()
    print(f"files={len(pairs)} tree_sha256={rolled}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
