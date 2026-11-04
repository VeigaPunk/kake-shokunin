#!/usr/bin/env python3
"""Round-80 ConnectorC — staged (merge/kake) vs registry (corpus/SOURCES.md) id/URL census.

Read-only: opens two files, writes nothing, prints a TSV-ish report and exits 0 when the
counts it derives are internally consistent, 2 on a shape surprise.

Row rule is the fleet census's own (scripts/sources-census.sh header: "Maintained parser
accepts 0-3 leading ASCII spaces before Markdown rows/headings; 4 or more spaces are
indented code and ignored"): a row is a line with 0-3 leading spaces that carries the
11-column schema (13 fields after splitting on unescaped pipes). Escaped pipes (\\|) inside
cells do not split a cell.
"""
from __future__ import annotations

import hashlib
import re
import sys

STAGED = "/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md"
REGISTRY = "/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md"
ROW_RE = re.compile(r"^( {0,3})\|")
#: registry row count / max id / S453 presence are asserted per --expect; the default
#: expectation is the frozen base revision (9998dc7) of corpus/SOURCES.md.
EXPECT = {"rows": 190, "max_id": "S452", "s453": False}
URL_RE = re.compile(r"https?://[^\s|]+")


def split_cells(line: str) -> list[str]:
    body = line.rstrip("\n")
    out, cur, i = [], [], 0
    while i < len(body):
        ch = body[i]
        if ch == "\\" and i + 1 < len(body):
            cur.append(body[i:i + 2])
            i += 2
            continue
        if ch == "|":
            out.append("".join(cur))
            cur = []
            i += 1
            continue
        cur.append(ch)
        i += 1
    out.append("".join(cur))
    return [c.strip() for c in out]


def rows(path: str) -> tuple[dict[str, tuple[int, str, list[str]]], int]:
    found: dict[str, tuple[int, str, list[str]]] = {}
    dup = 0
    with open(path, encoding="utf-8", errors="replace") as fh:
        for lineno, line in enumerate(fh, 1):
            if not ROW_RE.match(line):
                continue
            cells = split_cells(line)
            if len(cells) != 13:
                continue
            ident = cells[1]
            if not re.fullmatch(r"S[0-9]{3,}", ident):
                continue
            if ident in found:
                dup += 1
            found[ident] = (lineno, line, cells)
    return found, dup


def norm_url(cells: list[str]) -> str | None:
    for cell in cells[2:4]:
        hit = URL_RE.search(cell)
        if hit:
            u = hit.group(0).rstrip(").,;")
            u = re.sub(r"^https?://", "", u).rstrip("/").lower()
            return u
    return None


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv: list[str]) -> int:
    registry_path = argv[1] if len(argv) > 1 else REGISTRY
    expect = dict(EXPECT)
    for arg in argv[2:]:
        if arg == "--any-shape":
            expect = None
    staged, sdup = rows(STAGED)
    reg, rdup = rows(registry_path)
    print(f"staged_file\t{STAGED}")
    print(f"staged_sha256\t{sha256(STAGED)}")
    print(f"registry_file\t{registry_path}")
    print(f"registry_sha256\t{sha256(registry_path)}")
    print(f"staged_rows\t{len(staged)}\tdup_ids\t{sdup}")
    print(f"registry_rows\t{len(reg)}\tdup_ids\t{rdup}")

    collisions = sorted(set(staged) & set(reg))
    print(f"id_collisions\t{len(collisions)}")
    for cid in collisions:
        sl, sline, scells = staged[cid]
        rl, rline, rcells = reg[cid]
        print(
            "\t".join(
                [
                    "collision",
                    cid,
                    f"registry:L{rl}",
                    f"staged:L{sl}",
                    "bytes_identical=" + str(rline.strip() == sline.strip()),
                    "same_url=" + str(norm_url(scells) == norm_url(rcells)),
                    "registry_opened=" + (rcells[9] if len(rcells) > 9 else "?"),
                    "staged_opened=" + (scells[9] if len(scells) > 9 else "?"),
                ]
            )
        )

    su: dict[str, list[str]] = {}
    ru: dict[str, list[str]] = {}
    for ident, (_, _, c) in staged.items():
        u = norm_url(c)
        if u:
            su.setdefault(u, []).append(ident)
    for ident, (_, _, c) in reg.items():
        u = norm_url(c)
        if u:
            ru.setdefault(u, []).append(ident)
    hit_rows = [(u, ids) for u, ids in su.items() if u in ru]
    same_id_rows = sum(1 for u, ids in hit_rows if any(rid in ids for rid in ru[u]))
    other_id_rows = sum(len(ids) for _, ids in hit_rows) - same_id_rows
    print(f"staged_distinct_urls\t{len(su)}")
    print(f"registry_distinct_urls\t{len(ru)}")
    print(f"staged_rows_with_url_held\t{sum(len(ids) for _, ids in hit_rows)}")
    print(f"staged_urls_held\t{len(hit_rows)}")
    print(f"staged_urls_absent_from_registry\t{len(set(su) - set(ru))}")
    print(f"held_rows_same_id\t{same_id_rows}")
    print(f"held_rows_other_id\t{other_id_rows}")
    print(f"registry_max_id\t{max(reg)}")
    print(f"registry_has_S453\t{'S453' in reg}")
    print(f"staged_id_range\t{min(staged)}..{max(staged)}")

    ok = (
        len(staged) == 129
        and sdup == 0
        and rdup == 0
        and len(collisions) == 8
        and all(norm_url(staged[c][2]) == norm_url(reg[c][2]) for c in collisions)
    )
    if expect is not None:
        shape = (
            len(reg) == expect["rows"]
            and max(reg) == expect["max_id"]
            and ("S453" in reg) == expect["s453"]
        )
        print(f"registry_shape_expected\t{str(shape).lower()}")
        ok = ok and shape
    print(f"consistent\t{str(ok).lower()}")
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
