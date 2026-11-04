#!/usr/bin/env python3
"""Read-only id census using kake's own 0-3-space-tolerant ROW_RE, restricted to the
`## Registry` section, fence-aware (CommonMark), mirroring scripts/id_resolver.py:21-31,56.
Reports, per file, the sorted id list, the count, and duplicates."""
import re, sys, json

ROW_RE = re.compile(r"^ {0,3}\|\s*([^|]*?)\s*(?:\|(.*))?$")
FENCE_OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
FENCE_CLOSE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})[ \t]*$")
ID_RE = re.compile(r"^S\d{3,}$")


def ids(path):
    out, dup = [], []
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        lines = fh.read().split("\n")
    in_reg = False
    fence = None  # (char, length)
    for line in lines:
        if fence is not None:
            m = FENCE_CLOSE_RE.match(line)
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1]:
                fence = None
            continue
        m = FENCE_OPEN_RE.match(line)
        if m:
            fence = (m.group(1)[0], len(m.group(1)))
            continue
        if re.match(r"^#{1,2}\s", line):
            if in_reg and re.match(r"^#{1,2}\s", line):
                t = line.lstrip("#").strip()
                in_reg = (t == "Registry")
                continue
            in_reg = line.lstrip("#").strip() == "Registry"
            continue
        if not in_reg:
            continue
        r = ROW_RE.match(line)
        if not r:
            continue
        cell = r.group(1).strip()
        if ID_RE.match(cell):
            out.append(cell)
    seen = set()
    for i in out:
        if i in seen:
            dup.append(i)
        seen.add(i)
    return sorted(seen), dup


if __name__ == "__main__":
    res = {}
    for p in sys.argv[1:]:
        try:
            s, d = ids(p)
            res[p] = {"n": len(s), "min": s[0] if s else None, "max": s[-1] if s else None,
                      "ids": s, "dups": d}
        except Exception as e:
            res[p] = {"error": repr(e)}
    print(json.dumps(res, indent=1, sort_keys=True))
