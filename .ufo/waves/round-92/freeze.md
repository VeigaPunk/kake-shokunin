# Round 92 — freeze (kake)

Frozen before any wave data. Base: `e143faff1b86aad172dd87696da900c70347b8b2` (lane
`master` tip at round open, remote equal). This file, the two counters, the C2
contract, the frozen subjects/pins and the control harness are the frozen
instruments; the control receipts beside this file are the pre-freeze runs.

Author: kake L1 (`KakeR92`). Round shape: one v1 wave of 14 seats (8–16 band).
The L1 holds the canonical planner seat; a bounded planning data-walk rides
`ScoutGround`.

## Declared claims (2)

**C1 — calibration (lowest owned non-retired axis, score 2), instrument repair.**
The four routed round-91 instrument defects **K91-1, K91-2, K91-4, K91-5** close on
committed bytes. Item map: item **A** ← K91-1 (a receipt with no execution was
admitted), item **B** ← K91-2 (no registry row for the round's counter), item **C** ←
K91-5 (a replay counted checks without asserting their labels), and the top-level
`battery`/`differential` conjuncts ← K91-4 (membership instead of exact open sets and
reason strings).

- Counter: `.ufo/waves/round-92/c92_defects.py` (digest pinned in
  `frozen/c1-self.sha256`).
- Counting command:
  `python3 -B .ufo/waves/round-92/c92_defects.py --root . --revision <REV> --work <scratch>`
- Predicate (the same sentence in the plan, the counter's `met` and the receipt):
  `met=true` iff items A, B and C are closed at `<REV>`, the five-fixture battery reads
  each fixture's **exact** open set and declared reason substring, the frozen round-91
  counter still accepts the canned-runner fixture this counter refuses, and the counter
  blob at `<REV>` equals its pinned digest.
- Before (base, do-nothing): `open=3 closed=0 battery=hit differential=fail self=hit
  met=false`, exit 1 — `controls/base-c1.txt`.
- After target (carrier): `open=0 closed=3 battery=exact differential=ok self=ok
  met=true`, exit 0.
- Kill rule: any claim wording that says K91-1 closes while a canned runner or a
  fabricated receipt is admitted fails the claim, whatever the battery reports. The
  counter is not repaired after scoring; a defect it shows is routed.

**C2 — freshness (capability acquisition on open frontier ground).** A heuristic
freshness decision instrument (`scripts/heuristic_freshness.py`) implements
`.ufo/waves/round-92/c2-contract.md` (RFC 9111 §4.2.2, opened this round at
`L1/src/rfc9111.txt`, HTTP 200, 84 477 B, sha256
`aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`).

- Counter: `.ufo/waves/round-92/c92_heuristic.py`; contract v1; 28 hand cases; a
  120-case seeded generated population; five frozen forgery subjects; an audit-hook
  sandbox that denies `open` outside the subject tree and every import outside a frozen
  allowlist.
- Counting command:
  `python3 -B .ufo/waves/round-92/c92_heuristic.py --root . --revision <REV> --work <scratch>`
- Predicate: `met=true` iff the candidate is present, the pins and every forgery digest
  match, the anti-table finds no hand-case input digest and no forgery stem in the
  candidate source, all 28 hand cases decide as declared, all generated cases decide as
  the reference decides, and all five forgery subjects are refused.
- Before (base): `candidate=absent ... met=false`, exit 1 — `controls/base-c2.txt`.
- After target (carrier): `hand=28/28 generated=120/120 forgeries_refused=5/5
  anti_table=ok population=ok met=true`, exit 0.
- Kill rule: a subject that reaches `met=true` by importing the counter's reference, by
  reading the pins, or by a status-only table means the instrument is wrong and the
  claim fails.

## Pre-freeze controls (committed beside this file)

| Control | Receipt | Reading |
|---|---|---|
| C1 do-nothing (base) | `controls/base-c1.txt` | `open=3 closed=0 met=false`, exit 1 |
| C1 known-good fixture (proves `met=true` is reachable and the battery discriminates) | `controls/ctl-c1-known-good.txt` | `open=0 closed=3 battery=exact differential=ok self=ok met=true`, exit 0 |
| C2 do-nothing (base) | `controls/base-c2.txt` | `candidate=absent met=false`, exit 1 |
| C2 positive + sandbox differential | `controls/ctl-c2-positive.txt` | known-good subject `28/28 120/120 5/5 met=true`; the oracle-import forgery answers correctly **without** the sandbox and is refused **with** it |

The known-good C1/C2 fixture lives in scratch and is not evidence of the wave's
deliverables: it proves only that the frozen counters can read `met=true` on conforming
bytes and `met=false` on the base.

## Artifacts the wave must land (measured at the carrier)

- `integration/mutation-tip.txt`, `integration/mutation-tip.log`,
  `integration/mutate-tip.py` (item A; the runner must be differential and stdlib-only).
- A `SKILL.md` registry row for `c92_defects.py` naming its `--revision` command and its
  `met` predicate (item B).
- `scripts/heuristic_freshness.py` (C2 subject) and its knowledge entry, `SOURCES.md`
  row and `SCORECARD.md` capability row (C2).
- The wave's own receipts under `.ufo/waves/round-92/w1/` and `integration/`.

## Not frozen, not claimed

Cache-key storage, revalidation exchanges, serving stale without a client directive,
field-specific header normalisation, live-cache or browser behaviour, and the round-91
routed items K91-3, K91-6 … K91-10 stay open and are reported, not claimed.
