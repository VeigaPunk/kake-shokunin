#!/usr/bin/env python3
"""Independent second implementation of the round-57 C2 cross-registry source-id resolver.

Written from the CLI contract in `.ufo/waves/round-57/c57_idresolver_gate.py`'s docstring only,
for differential testing against `scripts/id_resolver.py`. Stdlib only.

Contract restated:

    python3 -B alt_resolver.py --root <lane dir> [--revision <rev>] [--fleet <fleet root>]

  - cited ids: every token `S` + 3 or more digits (word-bounded) in each `corpus/knowledge/**/*.md`
    file; with `--revision` the files are read through git, never the working tree.
  - registry ids: first cell of each table row of `corpus/SOURCES.md` under `## Registry`,
    0 to 3 leading spaces before the pipe.
  - siblings: every `<fleet>/*-shokunin/` other than the lane; `git show HEAD:corpus/SOURCES.md`
    when the directory is a git repo, else the file on disk.
  - stdout: one `DANGLING ...` line per dangling id, then the totals line.
  - exit: 0 dangling == 0; 1 dangling > 0; 2 unevaluable; 64 usage.

No `--selftest` (out of scope for this oracle seat).
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

ID_RE = re.compile(r"(?<![A-Za-z0-9_])S\d{3,}(?![A-Za-z0-9_])")
ROW_RE = re.compile(r"^ {0,3}\|")
REGISTRY_HEAD = re.compile(r"^##\s+Registry\s*$")
H2 = re.compile(r"^##\s")
ID_CELL = re.compile(r"^S\d{3,}$")
URL_RE = re.compile(r"https?://[^\s|<>\"']+")


class Unevaluable(Exception):
    pass


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def knowledge_paths_from_rev(root: str, rev: str) -> list[str]:
    p = git("-C", root, "ls-tree", "-r", "-z", "--name-only", rev, "--", "corpus/knowledge")
    if p.returncode != 0:
        raise Unevaluable(f"git ls-tree failed for {rev}")
    return sorted(x for x in p.stdout.decode("utf-8", "replace").split("\0") if x.endswith(".md"))


def knowledge_paths_from_tree(root: str) -> list[str]:
    base = os.path.join(root, "corpus", "knowledge")
    out: list[str] = []
    for dirpath, _dirnames, filenames in os.walk(base):
        for name in filenames:
            if name.endswith(".md"):
                full = os.path.join(dirpath, name)
                out.append(os.path.relpath(full, root).replace(os.sep, "/"))
    return sorted(out)


def batch_read(root: str, rev: str, paths: list[str]) -> dict[str, str]:
    """Read many `rev:path` blobs through one `git cat-file --batch`."""
    if not paths:
        return {}
    req = "".join(f"{rev}:{p}\n" for p in paths).encode()
    p = subprocess.run(["git", "-C", root, "cat-file", "--batch"], input=req,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise Unevaluable(f"git cat-file --batch failed: {p.stderr.decode('utf-8', 'replace').strip()}")
    data = p.stdout
    out: dict[str, str] = {}
    pos = 0
    for path in paths:
        nl = data.find(b"\n", pos)
        if nl < 0:
            raise Unevaluable(f"short cat-file output at {path}")
        header = data[pos:nl].decode("utf-8", "replace")
        pos = nl + 1
        parts = header.split()
        if len(parts) != 3 or parts[1] != "blob":
            raise Unevaluable(f"cat-file miss for {rev}:{path} ({header})")
        size = int(parts[2])
        out[path] = data[pos:pos + size].decode("utf-8", "replace")
        pos += size + 1
    return out


def read_registry_text(root: str, rev: str | None) -> str:
    if rev is None:
        path = os.path.join(root, "corpus", "SOURCES.md")
        if not os.path.isfile(path):
            raise Unevaluable("registry absent: corpus/SOURCES.md")
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    p = git("-C", root, "show", f"{rev}:corpus/SOURCES.md")
    if p.returncode != 0:
        raise Unevaluable(f"registry absent at {rev}: corpus/SOURCES.md")
    return p.stdout.decode("utf-8", "replace")


def parse_registry(text: str) -> dict[str, list[str]]:
    """id -> list of source URLs, rows under `## Registry` with 0-3 leading spaces."""
    ids: dict[str, list[str]] = {}
    inside = False
    for line in text.splitlines():
        if REGISTRY_HEAD.match(line):
            inside = True
            continue
        if inside and H2.match(line):
            inside = False
        if not inside or not ROW_RE.match(line):
            continue
        cells = line.split("|")
        if len(cells) < 2:
            continue
        sid = cells[1].strip()
        if not ID_CELL.match(sid):
            continue
        source = cells[2] if len(cells) > 2 else line
        urls: list[str] = []
        for raw in URL_RE.findall(source):
            u = raw.rstrip(".,;:\"'")
            if u and u not in urls:
                urls.append(u)
        ids.setdefault(sid, [])
        for u in urls:
            if u not in ids[sid]:
                ids[sid].append(u)
    return ids


def sibling_registry(sib: str) -> dict[str, list[str]] | None:
    path = os.path.join(sib, "corpus", "SOURCES.md")
    if os.path.exists(os.path.join(sib, ".git")):
        p = git("-C", sib, "show", "HEAD:corpus/SOURCES.md")
        if p.returncode != 0:
            return None
        return parse_registry(p.stdout.decode("utf-8", "replace"))
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8", errors="replace") as fh:
        return parse_registry(fh.read())


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--root", required=True)
    ap.add_argument("--revision")
    ap.add_argument("--fleet")
    try:
        args = ap.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 64
    root = os.path.abspath(args.root)
    fleet = os.path.abspath(args.fleet) if args.fleet else os.path.dirname(root)

    rev: str | None = None
    if args.revision:
        p = git("-C", root, "rev-parse", "--verify", f"{args.revision}^{{commit}}")
        if p.returncode != 0:
            print(f"unevaluable: revision {args.revision} unresolved", file=sys.stderr)
            return 2
        rev = p.stdout.decode("utf-8", "replace").strip()

    try:
        lane_registry = parse_registry(read_registry_text(root, rev))
        if rev is None:
            paths = knowledge_paths_from_tree(root)
            texts = {}
            for rel in paths:
                full = os.path.join(root, rel)
                with open(full, encoding="utf-8", errors="replace") as fh:
                    texts[rel] = fh.read()
        else:
            paths = knowledge_paths_from_rev(root, rev)
            texts = batch_read(root, rev, paths)
        if not paths:
            raise Unevaluable("no knowledge file under corpus/knowledge/**/*.md")

        citations: dict[str, set[str]] = {}
        for rel in paths:
            for m in ID_RE.finditer(texts[rel]):
                citations.setdefault(m.group(0), set()).add(rel)

        try:
            sibs = sorted(
                name for name in os.listdir(fleet)
                if name.endswith("-shokunin") and os.path.isdir(os.path.join(fleet, name))
                and os.path.abspath(os.path.join(fleet, name)) != root
            )
        except OSError as exc:
            raise Unevaluable(f"fleet root unreadable: {exc}")
        sibling_ids: dict[str, dict[str, list[str]]] = {}
        for name in sibs:
            reg = sibling_registry(os.path.join(fleet, name))
            if reg is not None:
                sibling_ids[name] = reg
    except Unevaluable as exc:
        print(f"unevaluable: {exc}", file=sys.stderr)
        return 2

    dangling = sorted((i for i in citations if i not in lane_registry), key=lambda s: (int(s[1:]), s))
    owned_elsewhere = 0
    for sid in dangling:
        owners = [name for name in sorted(sibling_ids) if sid in sibling_ids[name]]
        cited_by = sorted(citations[sid])
        citing_text = "\n".join(texts[rel] for rel in cited_by)
        url_match = [
            name for name in owners
            if any(u in citing_text for u in sibling_ids[name][sid])
        ]
        if owners:
            owned_elsewhere += 1
        print(f"DANGLING {sid} cited-by={','.join(cited_by)} owners={','.join(owners) or '-'} "
              f"url-match={','.join(url_match) or '-'}")

    cited = len(citations)
    resolved = sum(1 for i in citations if i in lane_registry)
    print(f"ids_cited={cited} ids_resolved={resolved} dangling={len(dangling)} "
          f"owned_elsewhere={owned_elsewhere} unowned={len(dangling) - owned_elsewhere}")
    return 0 if not dangling else 1


if __name__ == "__main__":
    sys.exit(main())
