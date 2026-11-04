# Round-80 amendment 2 — C1 counter correction (cell index), before any after-state

Found by the wave's `ScoutSources` seat at the freeze bytes `f20163c1`, before any seat produced an
after-state. Terms-only: the claim's written statement, its frozen predicate sentence
(`met <=> open == 0 for the six items R79-1, R79-2, R79-3, R79-4, R79-5, R79-8`), the six item
conditions in `contract.md`, the case set and the C2 predicate are unchanged.

## The defect

`c80_defect_queue.py` split a registry row with `line.strip().strip("|").split("|")`, which yields the
eleven cells at indices 0-10, and then read the `used-by` cell at index 11:

    used = row[11] if len(row) > 11 else ""

`row_shape` in the same file enforces exactly eleven cells, so for every shape-valid row `row[11]` was
always empty: the `used-by` conjunct could never resolve and R79-1 could never read `closed`. A
twelve-cell row that would populate `row[11]` is rejected by `row_shape`. The base control did not
catch it because, at the base revision, the row is absent and the function returns at the earlier
branch (`controls/base-c80-defect-queue.txt`: `R79-1 open no S453 row`).

## The fix

`used = row[10] if len(row) > 10 else ""`, plus a `--selftest` on the counter that builds a scratch
tree three times — a shape-valid `S453` row whose `used-by` names a file that cites `S453` (must read
closed), the same with a `used-by` naming a file that does not cite it (must read open), and a
twelve-cell row (must fail `row_shape`) — so the conjunct is shown able to pass and to fail before any
measurement rests on it. Evidence: `controls/ctl-c80-queue-selftest.txt`.

Regenerated controls after the fix: `controls/base-c80-defect-queue.txt` (still `open=6 met=false`,
exit 1) and `controls/ctl-c80-junk-queue.txt` (junk tree, still not met). No measured number moved.
