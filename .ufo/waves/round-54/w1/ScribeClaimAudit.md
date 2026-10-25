# ScribeClaimAudit — round-54 w1 (C1/C2 predicate & counter audit)

Seat: `L1Kake54.ScribeClaimAudit`. Read-only; the only file written is this report.
Scope: `.ufo/waves/round-54/contract.md` (frozen at `acae1dcc`), the committed
counters at HEAD, and the **uncommitted workspace revisions** of both counters
(both show `git status: M`, edited 10:31–10:52 local). Findings flag which state
each applies to.

## Verified-OK

- **Predicate wording.** `PREDICATE` in each counter is verbatim the contract's
  bold sentence (worktree adds only a trailing `.`). `--predicate` prints it.
- **Do-nothing controls (committed receipts + re-verified on both versions).**
  C1 base `68228b2d` → `mismatches=1 met=False`, exit 1. C2 base →
  `registry=absent manifest=absent uncovered=4`, exit 1 (committed counter only;
  worktree C2 currently crashes, below).
- **Committed C2 coverage set.** `REQUIRED_SEAT_NAMES` (7 names) matches the
  closure's lost list in `corpus/lessons/round-53-verifier-spotcheck.md:73,79`;
  full-path cited names = 4 (`ReviewerProvenance, CriticCrossLane, ScoutS329,
  ScoutQuarantine`) matching `uncovered=4`.
- **Falsifiability.** Both counters read only committed bytes via
  `git show <rev>:<path>`; checks are concrete, deterministic, and yield
  0/1/2 verdicts. C1 grounds the quote in the retained body
  `round-52/sources/S374.html` (sha256 pinned in `source-reopen.txt`).

## Findings

### F1 (committed C1 — resolved in worktree): supersede direction inverted
Committed `run_checks`: `mismatch = suspects with pos < corr_at` — a suspect
cell *preceding* the correction counts as a mismatch. That is backwards for an
appended correction: appending a valid `[r54-correction]` block at end of file
yields `mismatches=1 met=False` (simulated against base entry bytes). Under the
contract's append-only repair, the committed counter can only pass if the
correction block *precedes* the cell it supersedes — the opposite of
"superseded by an appended block". The worktree fixes this correctly:
`corr_at <= end` → appended correction yields `met=True` (re-verified).

### F2 (committed C1 — incidental): old selftest green for the wrong reason
Committed `run_checks_fix` scanned per line; the fixture's `(rendered:` cell
spans two lines so `suspects` was always empty, masking F1. Worktree selftest
now shares `qualifier_findings` and genuinely exercises the cases.

### F3 (worktree C1 — BLOCKING): selftest is currently RED
`python3 -B c54_s374_calib.py --selftest` → exit 1:
`FAIL corrected: exit 1 expected 0`. Two stacked causes in the `corrected`
fixture: (a) the correction sentence drops the Japanese `QUOTE` — C1.3 requires
it inside the block; (b) the fixture's base cell wraps differently
(`…one it\n does not recommend, or…`) than `BASE_RENDER`, so
`base_copy_count=0` → `run_checks_fix` adds `mismatch += 1`.

### F4 (worktree C1 — enforcement gap): base-copy count not gated in `run_checks`
The worktree adds `base_copy_count` (the round-open cell preserved exactly
once) to `run_checks_fix`'s met condition but not to `run_checks`'s — the
production path prints `FAIL C1.2_cells` yet `met` stays `True` if the cell is
duplicated/deleted. Gate it in `run_checks` or drop it.

### F5 (worktree C1 — spec tightening vs contract): marker/binding requirements
Contract names the marker `[r54-correction 2026-10-25]` and requires quote +
English crawl vocabulary. Worktree requires `**[r54-correction 2026-10-25]**`
bold-anchored at line start, `NEGATIVE_CRAWL_RE` ("not recommend crawl|crawling"),
and `BOUND_CORRECTION_RE` ("earlier rendering…endorsement…supersedes…gloss").
A literal contract-shaped correction (plain bracket, "does not recommend the
crawl") **fails** (`corr_at=-1`, verified). Direction repair executors must
know the enforced grammar exceeds the contract text.

### F6 (worktree C2 — BLOCKING): `NameError` — `NAME_RE` deleted, still called
`registry_row_ok` refactor removed `NAME_RE`; line 86 still does
`NAME_RE.findall(...)`. Any real run (`--revision`) crashes with a traceback —
no verdict line, no defined exit code. Base run reproduces the crash.

### F7 (both versions — C2 manifest): format assumed, not stated
Contract P2.2 requires "records, per cited seat-report filename, `resolved:` or
`lost:` with a reason". Both counters require markdown table rows
`| name.md | resolved|lost | reason |` (worktree: optional backticks, non-empty
reason, plus unique-required-rows). A `name.md resolved: <reason>` manifest
matching the literal contract would score `manifest=incomplete`. Also, the
fourth conjunct `has_loss_basis` ("40 spawned" ∧ "0 committed seat reports")
and the hardcoded 7-name subset are enforced requirements beyond the predicate
sentence — stricter is fine, but they are invisible in the frozen wording.

### F8 (both versions — kill rule): usage errors exit 2, not 64
Contract: `64 usage`. `argparse`/`parser.error` exit **2**, colliding with
`unevaluable` — a usage error is indistinguishable from an unevaluable state by
exit code.

### F9 (hygiene): stale `__pycache__` diverges from source
`__pycache__/c54_s374_calib.cpython-314.pyc` (mtime 10:52, newer than the 10:51
source) compiles an older source lacking `EN_CRAWL_RE`/the refactor; `import`
loads it and `run_checks` dies on `NameError`. `-B` contract invocation is
unaffected, and the dir is gitignored — flag only as an import path trap.

### F10 (version skew): counters are unfrozen
The contract says the counter's code carries the same sentence "in the counter's
code", but both counters carry uncommitted mid-flight edits; the committed
version (receipt-validated) and the workspace version (selftest red, C2 crash)
give different answers. Any executor running today hits the worktree state.

## Causal separability — OK
C1 touches `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md` only; C2
touches `SKILL.md` + `.ufo/waves/round-53/settlement.md` only. Read sets
(C1: entry + `round-52/sources/S374.html`; C2: SKILL.md, lesson, spotcheck,
manifest) are disjoint; no cell/marker/row text can satisfy both predicates;
repairs do not interact. Claims are separable.

## Tool installs
None.
