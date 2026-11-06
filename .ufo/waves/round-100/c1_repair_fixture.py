#!/usr/bin/env python3
"""Round-100 C1 control fixture builder (scratch only; never run against the lane).

Usage: c1_repair_fixture.py <SKILL.md in a scratch clone> <mode>
  pos        delete the seven older duplicate rows (base lines below) and append the
             fenced history block that keeps them verbatim — the planned repair;
  deleteall  delete both rows of each duplicated tool (forgery: rows gone, nothing kept);
  keepold    delete the seven CURRENT rows instead (forgery: the stale answers win);
  everycode  `pos`, then rewrite the kept cache_key.py row's verdict map to name
             0, 1, 2 and 64 (declared counter limit: expected to stay met=true).
Line numbers are the round base 3989618d9f8310b2eb5fb456aa7c4e58fb0b5ff5; the script
asserts each line still names its tool before touching anything.
"""
import sys

OLD = {494: "scripts/live_snapshot.py", 1079: "scripts/source_snapshot.py", 1104: "scripts/robots_audit.py",
       1370: "scripts/response_snapshot.py", 1505: "scripts/x_robots_tag_audit.py", 1621: "scripts/cache_key.py",
       1624: "scripts/cache_key_conformance.py"}
NEW = {1725: "scripts/live_snapshot.py", 1736: "scripts/source_snapshot.py", 1730: "scripts/robots_audit.py",
       1728: "scripts/response_snapshot.py", 1517: "scripts/x_robots_tag_audit.py", 1714: "scripts/cache_key.py",
       1715: "scripts/cache_key_conformance.py"}
CURRENT = {"scripts/live_snapshot.py": "`live_snapshot.py`", "scripts/source_snapshot.py": "`source_snapshot.py`",
           "scripts/robots_audit.py": "`robots_audit.py`", "scripts/response_snapshot.py": "`response_snapshot.py`",
           "scripts/x_robots_tag_audit.py": "`scripts/x_robots_tag_audit.py (round-80 grammar)`",
           "scripts/cache_key.py": "`cache_key.py`", "scripts/cache_key_conformance.py": "`cache_key_conformance.py`"}


def history(lines):
    out = ["", "## Round 100 — superseded registry rows (history, not a registry)", "",
           "Round 100 C1 (calibration; `.ufo/waves/round-100/freeze.md`) leaves exactly one registry row per",
           "committed tool. The seven rows below were a second, older answer for a tool that already had a",
           "current row; they are kept verbatim inside the fence so no fact they carried is lost. Each is",
           "labelled with the line it held at round base `3989618d` and the Name cell of the current row",
           "that now answers for the tool. A fenced row is not a registry row.", "", "```text"]
    for ln in sorted(OLD):
        out.append("[SKILL.md:%d at 3989618d; tool %s; current row Name %s]" % (ln, OLD[ln], CURRENT[OLD[ln]]))
        out.append(lines[ln - 1])
    out.append("```")
    return out


def main():
    path, mode = sys.argv[1], sys.argv[2]
    lines = open(path, encoding="utf-8").read().split("\n")
    for table in (OLD, NEW):
        for ln, tool in table.items():
            if tool not in lines[ln - 1]:
                print("line %d does not name %s" % (ln, tool), file=sys.stderr)
                return 2
    if mode in ("pos", "everycode"):
        drop = set(OLD)
        tail = history(lines)
    elif mode == "deleteall":
        drop = set(OLD) | set(NEW)
        tail = []
    elif mode == "keepold":
        drop = set(NEW)
        tail = []
    else:
        return 2
    kept = [l for i, l in enumerate(lines, 1) if i not in drop]
    if mode == "everycode":
        k = [i for i, l in enumerate(kept) if l.startswith("| cache_key.py |")]
        cells = kept[k[0]].split(" | ")
        cells[3] = "`0` ok; `1` refusal; `2` other; `64` usage"
        kept[k[0]] = " | ".join(cells)
    while kept and kept[-1] == "":
        kept.pop()
    open(path, "w", encoding="utf-8").write("\n".join(kept + tail) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
