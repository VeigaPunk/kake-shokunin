#!/usr/bin/env python3
"""Worktree replica of the frozen c93_selfassess.py E5/E3 scan (ExecC1Fixes receipt).

Replicates the counter's exact PATH_RE / row / brace / strip logic (read from the
frozen counter bytes) but checks existence against the WORKTREE, which is the
state the carrier commit will contain. Read-only; prints only.
"""
import os
import re

root = "/home/vgpnk/Projects/shokunin/kake-shokunin"
PATH_RE = re.compile(r"`((?:scripts|corpus|\.ufo)/[^`\s]+)`")
ID_RE = re.compile(r"S\d{3,}")


def expand_braces(path):
    m = re.search(r"\{([^{}]*)\}", path)
    if not m:
        return [path]
    out = []
    for part in m.group(1).split(","):
        out.extend(expand_braces(path[:m.start()] + part + path[m.end():]))
    return out


def exists(path):
    return os.path.exists(os.path.join(root, path))


# --- E5 over worktree SKILL.md
skill = open(os.path.join(root, "SKILL.md"), encoding="utf-8").read()
rows = 0
tokens = []
missing = []
for line in skill.splitlines():
    if not line.startswith("|"):
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 4:
        continue
    rows += 1
    body = " ".join(cells)
    seen = set()
    for raw in PATH_RE.findall(body):
        raw = re.sub(r":\d+(-\d+)?$", "", raw).rstrip("`,.")
        for path in expand_braces(raw):
            if "<" in path or "*" in path or path in seen:
                continue
            seen.add(path)
            tokens.append(path)
            if not exists(path):
                missing.append(path)
print("E5-worktree rows=%d path_tokens=%d missing=%d" % (rows, len(tokens), len(missing)))
for m in sorted(set(missing)):
    print("E5-MISSING", m)

six = ["scripts/kimi-surface.mjs", ".ufo/waves/round-52/selftest/",
       ".ufo/waves/round-52/selftest/ladder/", ".ufo/waves/round-52/selftest/registry/",
       "corpus/knowledge/google-robots-txt-limits.md"]
for tok in six:
    print("E5-token %-55s bare_matches=%d exists=%s"
          % (tok, tokens.count(tok), exists(tok)))
real = "corpus/knowledge/robots-txt-limits.md"
print("E5-token %-55s bare_matches=%d exists=%s"
      % (real, tokens.count(real), exists(real)))

# --- E3 over worktree knowledge entries
ids = set(ID_RE.findall(open(os.path.join(root, "corpus/SOURCES.md"), encoding="utf-8").read()))
kd = os.path.join(root, "corpus/knowledge")
names = sorted(n for n in os.listdir(kd) if n.endswith(".md"))
e3bad = []
for name in names:
    text = open(os.path.join(kd, name), encoding="utf-8").read()
    head = "\n".join(text.splitlines()[:8])
    problems = []
    for key in ("source", "verified-at", "recheck"):
        if not re.search(r"(?m)^" + key + r":\s*\S", head):
            problems.append("missing %s:" % key)
    m = re.search(r"(?m)^source:.*$", head)
    if m:
        unres = sorted({i for i in ID_RE.findall(m.group(0)) if i not in ids})
        if unres:
            problems.append("unresolved " + ", ".join(unres))
    if problems:
        e3bad.append((name, "; ".join(problems)))
print("E3-worktree entries=%d mismatches=%d" % (len(names), len(e3bad)))
for n, p in e3bad:
    print("E3-MISMATCH", n, p)

# --- meta-robots head, trio lines, id resolution
mr = open(os.path.join(kd, "meta-robots-directives.md"), encoding="utf-8").read().splitlines()[:8]
for i, ln in enumerate(mr, 1):
    if re.match(r"^(source|verified-at|recheck):", ln):
        print("meta-robots trio line %d: %.72s" % (i, ln))
src_line = next((l for l in mr if l.startswith("source:")), "")
src_ids = sorted(set(ID_RE.findall(src_line)))
print("meta-robots source ids=%s all_resolved=%s" % (src_ids, all(i in ids for i in src_ids)))
