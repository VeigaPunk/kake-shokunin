# Receipts — ConnectorSibling, round 84 w1

All produced by read-only commands; no production file was touched. Times are local, 2026-11-04.

| file | produced | what it is |
|---|---|---|
| `idscan.py` | 11:09 | the tolerant id extractor, transcribing `scripts/id_resolver.py:21-31,56` (`^ {0,3}\|` row prefix, `## Registry` section, CommonMark fences). Run as `python3 idscan.py <SOURCES.md ...>`. |
| `scan_kake.json` | 11:05 | raw JSON of that extractor over three paths. **Known artifact:** the two `SOURCES.append.md` entries read `n=0` because this run restricted extraction to the `## Registry` heading, which those fragment files do not carry. `collision.txt` is the corrected measurement (no section restriction on fragments). The kake registry entry is the 11:05 snapshot: 194 ids, `S457` absent. |
| `ids_kake_registry_1105.txt` | 11:05 (regenerated from `scan_kake.json`) | 194 ids, `S001`…`S456`, no `S457`. |
| `ids_kake_registry_1109.txt` | 11:09 | 195 ids, max `S457` (the sibling scribe's row landed at 11:08; `git diff --stat` → 1 insertion). |
| `ids_kake_staged.txt` | 11:05 | 129 ids, `S287`…`S415`, from `shokuknow/merge/kake/SOURCES.append.md`. |
| `collision.txt` | 11:11 | corrected collision measurement: registry/staged intersection 8, staged-block overlap with `merge/kama` 86, `S457` presence per file, collision count 0. |
| `ids_S457_holders.txt` | 11:12 | `S457` holders at both instants, and the collision count. |
| `row_S457.txt` | 11:09 | the landed `S457` row (truncated at 420 chars) as written by the scribe. |
| `c1_base.txt` | 11:05 | `c84_defect_queue.py --root .` at the worktree: four `item=` lines and `C1v1 … open=3 closed=1 met=false`, exit 1. Reproduces the frozen `controls/base-c84-defect-queue.txt` item lines, including `item=D4 closed=1` with no round-84 lesson in the tree. |
