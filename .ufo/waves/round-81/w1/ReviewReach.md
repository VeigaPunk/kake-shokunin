# LabratCtl (agent id ReviewReach) — do-nothing reachability review §9, kake round 81 w1

**Verdict: no shortcut to either target** — a round performing none of the claimed work reads
C1 `open≥3 met=false` at best and C2 `surfaces=0 met=false`; the kill rules hold. Two item-level
weaknesses found: **R80-1..R80-3 close on transcribed words alone**, and **R80-5 is already closed
at the freeze commit** with zero round work.

Read-only seat: no edits to any lane byte, no network, no tool installs. Scratch
`/fast/scratch/hyaku/kake-r81/ReviewReach` removed before yield (verified absent).
This report exists twice with identical bytes: `w1/LabratCtl.md` (item-named) and
`w1/ReviewReach.md` (dispatch trailer). Receipts: `w1/LabratCtl/`.

## Instruments pinned

- C1 `.ufo/waves/round-81/c81_defect_queue.py` sha256 `eae0c578…faaad`, selftest `15/15 passed` rc=0.
- C2 `.ufo/waves/round-81/c81_capture_audit.py` sha256 `a59525ce…c12d8`, selftest `12/12 passed` rc=0.
- Receipt `LabratCtl/instrument-pins.txt`. Note: the dispatch prompt cites the C1 selftest receipt
  as `13/13`; the committed `controls/c81-selftest-c1.txt` and the counter now both read `15/15`
  (two `r80-4-empty-seat-*` checks added). Bytes agree with each other; the prompt citation is stale.
  The counter also now excludes empty-output seats from `settled` (visible at
  `c81_defect_queue.py:200`), implementing the "empty output does not count as settled" clause.

## Fixture 1 — do-nothing (base tree, no round-81 bytes)

`git archive 2e11925… | tar -x` → 22,119 files; `git ls-tree 2e11925 .ufo/waves/` ends at round-80,
so every round-81 byte is absent at the base.

- C1: `C1v1 … open=6 closed=0 met=false`, exit=1 — detail lines byte-identical to
  `controls/base-c81-defect-queue.txt` (`LabratCtl/donothing-c1.txt`).
- C2: `C2v1 … surfaces=0 failures=1 audit_rc=- met=false`, exit=1 (`LabratCtl/donothing-c2.txt`).

## Fixture 2 — work in words (donothing + lesson prose + plausible accounting, nothing else)

Added exactly `corpus/lessons/round-81.md` (claims all six closures in prose) and
`.ufo/waves/round-81/w1-accounting.json` (plausible 15-seat wave numbers) — additions-only,
proven by `LabratCtl/fixture-manifests.txt`; payloads retained as
`fixture-words-lesson.md` / `fixture-words-accounting.json`.

- C1: `C1v1 … open=3 closed=3 met=false`, exit=1 (`LabratCtl/words-c1.txt`) —
  **R80-1, R80-2, R80-3 read `closed` on the fabricated prose.**
- C2: `surfaces=0 met=false`, exit=1 (`LabratCtl/words-c2.txt`).
- Kill rule NOT falsified: `met=false` exit=1.

**Finding (medium, routed — counter not edited).** R80-1..R80-3 are token-presence checks over
`corpus/lessons/round-81.md`, and every required token is printed verbatim in the committed
`controls/base-c81-defect-queue.txt` (`corpus/SOURCES.md:200`, `constants_failed=4/4, 47/48, 11/12`,
`rfc9110.txt rows=3`, `rfc9110.html rows=3`). I fabricated the closing prose by transcribing that
one committed file — the registry and the round-80 receipt were never opened. Contract §C1's
do-nothing rationale ("lane bytes the report cannot forge: registry line numbers, receipt
arithmetic") therefore does not hold for these three items at the item level: a words-only seat
closes 3 of 6 items. Round-level `met` stays false only because R80-4/5/6 need artifacts beyond
words (and see the freeze probe: R80-5 needs nothing at all). Route: if item-level forgery
resistance is wanted, the correction rows must be checked against re-derived values the control
receipt does not publish, or the control receipts must stop printing the answers.

## Fixture 3 — one item (donothing + only an S454-shaped registry row)

Appended one 11-cell `| S454 | … rfc9110.html … |` row to `corpus/SOURCES.md` (308→309 lines;
row retained as `LabratCtl/fixture-s454-row.txt`).

- C1: `open=6 closed=0 met=false`, exit=1 (`LabratCtl/oneitem-c1.txt`) — **a registry row alone
  closes nothing**; R80-1's wanted pointer is unchanged.
- C2: `surfaces=0 met=false`, exit=1 (`LabratCtl/oneitem-c2.txt`).
- Note (low): the appended row cites `rfc9110.html`, so R80-3's wanted count flips to
  `rfc9110.html rows=4` in that same tree (visible in `oneitem-c1.txt`). Ordering trap for the real
  round: land the S454 row and write the R80-3 correction row from the same tree state, or the
  correction row carries a stale `rows=3` and R80-4's neighbor stays open.

## Freeze probe (minimal-bytes evidence)

`c81_defect_queue.py --root <lane> --revision a77b8a19… --work <scratch>` (read-only materialise):

- `open=5 closed=1` — **R80-5 already closed at the freeze commit** (`LabratCtl/freeze-c1.txt`):
  the junk builder + spec committed by the freeze rebuild deterministically and round-80's counter
  reads `open=5 closed=1 met=false` over the rebuilt tree. The base control's `R80-5 open` is an
  artifact of the base predating the freeze, not of missing work.

## 4. Minimal committed bytes that flip each counter (the list the round must actually land)

**C1 `met=false → met=true`** — 5 new files, 0 edits to existing bytes (R80-5 needs none):

| Item | Bytes |
|---|---|
| R80-1 | `corpus/lessons/round-81.md` (new): a line with `R80-1` + `corpus/SOURCES.md:200` + `S453` (S453 already at `:200`) |
| R80-2 | same file: a line with `R80-2` + `constants_failed=4/4` + `47/48` + `11/12` (receipt `ctl-c80-constants.txt` already committed) |
| R80-3 | same file: a line with `R80-3` + `rfc9110.txt rows=3` + `rfc9110.html rows=3` — `rows=4` if the S454 row lands in the same tree first |
| R80-4 | `.ufo/waves/round-81/w1-spec.json` + `w1-results.json` (settled = non-empty outputs; attack share ≥ 0.25) + `w1-accounting.json` re-deriving `attack_roles`/requested/settled/share + `spec_sha256` |
| R80-5 | **none** — closed at `a77b8a19` (verified above) |
| R80-6 | `.ufo/waves/round-81/seat-failures.json` equal to `scripts/wave_seat_record.py` output over the R80-4 spec+results (recorder already committed at the freeze) |

**C2 `met=false → met=true`** — 4 new paths, 0 edits: `.ufo/waves/round-81/capture/manifest.json`
(version 1, allowlist, ≥1 check); per-check `response.json` + body file with self-consistent
sha256/bytes, integer status, RFC 3339 `fetchedAt` ≥ `2026-11-04T00:00:00Z`, GET, `truncated:false`,
allowlisted host; `.ufo/waves/round-81/controls/after-c2-audit.txt` byte-equal to `header_audit`
stdout (`scripts/header_audit.py` already committed, blob `8e73f15f`).

**Residual risk (by design, frozen predicate — noted, not a counter defect):** every C2 byte is
forgeable offline — `fetchedAt` is self-asserted and no byte proves a network fetch happened; the
S454/S433 grounding (`capture-expectations.json`) is outside the counter's verify path entirely.
The counter proves internal consistency, not capture provenance. Likewise the C1 minimal list shows
the honest content of the wave JSONs is the only part bytes cannot force.

## Hygiene / gaps

- Commands verbatim in receipts; exit codes recorded (`rc=` lines). C1 scored over 4 trees + 1
  revision + selftest; C2 over 3 trees + selftest.
- Not built (outside the three-fixture scope): a forged R80-4 spec/results/accounting triple and a
  forged offline C2 capture; the counters' own selftests cover those mechanics (15/15, 12/12).
- No tool installs (no RULES.md channel used); no pacman; no git mutation anywhere (only
  `archive`/`ls-tree`/`rev-parse`).
