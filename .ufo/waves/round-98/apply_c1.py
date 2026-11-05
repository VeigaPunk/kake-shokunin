#!/usr/bin/env python3
"""Apply the round-98 C1 repair to SCORECARD.md (run once by the L1).

1. Rename the `Curated source registry` row's capability cell to the admitted
   closure's name (`Sources-registry (curated source registry)`, round 20).
2. Move the five rows whose closures were not admitted (r34, r35, r37, r61,
   r64) out of the Capabilities table into a history table directly below it,
   each with its MANIFEST closure verdict; no row text is changed.
3. Append the 39 rows of gen_cap_rows.py to the Capabilities table.
"""
import os, re, sys
W = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, W)
import gen_cap_rows as g  # noqa: E402

P = os.path.join(W, "..", "..", "..", "SCORECARD.md")
t = open(P).read()
MOVE = [("Offline link-preview (Open Graph) audit", "34", "rejected-honest-stop"),
        ("Link-preview audit, round-35 contract", "35", "rejected-honest-stop"),
        ("Offline robots.txt expectation audit", "37", "no capability admitted (round-37 closure correction; the row already says not admitted)"),
        ("Offline response-header expectation audit", "61", "rejected-harmed"),
        ("Standalone retained-span quote classifier (round-64 re-entry)", "64", "rejected-honest-stop")]
i = t.index("\n## Capabilities\n")
h = t.index("| Capability |", i)
end = t.index("\n\n", h)
table = t[h:end].split("\n")
moved = []
for name, r, verdict in MOVE:
    idx = [k for k, l in enumerate(table) if l.startswith("| " + name + " |")]
    assert len(idx) == 1, name
    moved.append((table.pop(idx[0]), r, verdict))
k = [n for n, l in enumerate(table) if l.startswith("| Curated source registry |")]
assert len(k) == 1
table[k[0]] = table[k[0]].replace("| Curated source registry |", "| Sources-registry (curated source registry) |", 1)
for r, cap, what, ev in g.ROWS:
    table.append(f"| {cap} | {what} | {ev} | {r} |")
hist = ["", "### Capability rows without an admitted closure (round 98: moved out of the table above)", "",
        "These rows sat in the Capabilities table, but the non-author closure of the round named in their",
        "last cell did not admit the capability (fleet `MANIFEST.json` at `f8674006`; counter",
        "`.ufo/waves/round-98/c98_captable.py`). The tools exist; the table no longer claims them as",
        "admitted capabilities. Row text is unchanged; the closure verdict is the added first cell.", "",
        "| Closure verdict | Capability | What it can now do | Evidence pointer | First-working round |",
        "|---|---|---|---|---|"]
for line, r, verdict in moved:
    hist.append(f"| r{r} {verdict} " + line)
t = t[:h] + "\n".join(table) + "\n" + "\n".join(hist) + t[end:]
open(P, "w").write(t)
print("applied: rows", len(g.ROWS), "moved", len(moved))
