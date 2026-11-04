# Round-81 amendment 3 — C2 compares instants, not strings

Written 2026-11-04, after the capture landed and before the carrier measurement. Found by the
wave's `ReviewC2` seat (`w1/ReviewC2.md` F2). The predicate sentence does not change
("an RFC 3339 fetch time on or after 2026-11-04T00:00:00Z"); the instrument now measures it.

## A1 — the fetch-time floor is a time comparison, not a string comparison

The freeze and amendment-2 counters tested `fetched < ROUND_FIRST_DAY` on the *text* of
`fetchedAt`, after a regex that permits numeric UTC offsets. Two consequences, both measured by
the seat:

    fetchedAt 2026-11-04T01:00:00+09:00  (= 2026-11-03T16:00:00Z, BEFORE the round)  -> accepted
    fetchedAt 2026-11-03T23:00:00-02:00  (= 2026-11-04T01:00:00Z, genuinely fresh)   -> rejected

A forger could backdate a receipt with a positive offset; an honest capture written with a
negative offset would be refused. `parse_instant()` now parses the value to an aware
`datetime`, converts it to UTC and compares instants; a value that is not an RFC 3339 instant is
reported as such. The selftest gains `utc-offset-ahead-opens` and `utc-offset-behind-accepted`
(tally 18/18 → 22/22).

## Why this cannot move the measured verdict

All three captured receipts carry a `Z` timestamp (`2026-11-04T12:05:06Z`), for which the parsed
instant sorts exactly where the string does. The worktree verdict is identical before and after the
fix — `C2v1 revision=worktree declared=3 surfaces=3 failures=0 audit_rc=1 met=true`, exit 0 — and
the fix only rejects more, never fewer, receipts, so no receipt that passed before can fail because
of it except the two offset shapes no receipt in this round uses.

## The seat's other three findings

- **F1 (limit, not a defect).** A wholly fabricated capture — self-consistent digests, a fresh
  `fetchedAt`, the frozen expectations and a real offline audit run — scores `met=true`. The counter
  verifies internal consistency and the audit's bytes; it has no chain to a socket. Recorded as the
  claim's stated limit in `corpus/lessons/round-81.md`, the capability row and `corpus/QUALITY.md`.
- **F3 (mode asymmetry).** In worktree mode the audit-equality conjunct binds to whatever
  `scripts/header_audit.py` contains at measure time; in `--revision` mode the tool, manifest,
  capture and receipt are all exported from the revision. The **carrier is therefore measured with
  `--revision <commit>`** and its receipt is `controls/after-c2-carrier.txt`; the worktree receipt
  `controls/after-c2.txt` stays as the capture seat's own run and is labelled the weaker mode.
- **F4 (closed by the row, not by this amendment).** `corpus/SOURCES.md` had no `S454` row when the
  seat reviewed; the row was inserted directly after `S453` (registry 191 → 192) with the lesson's
  Gate as its opening record, and the round-end census exits 0 with `W04 20 → 21`.
