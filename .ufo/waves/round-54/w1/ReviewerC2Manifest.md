# ReviewerC2Manifest — C2 settlement-manifest check review

Scope: `c54_ops_debt.py` manifest leg (`MANIFEST_RE`, `settled`, `uncovered`,
`has_loss_basis`, `REQUIRED_SEAT_NAMES`) against the contract's C2 predicate —
seven required report names, duplicate rows, malformed dispositions, arbitrary
filenames. Lane: `kake-shokunin`. Fix revision measured: `8e408e0` (HEAD);
do-nothing base `68228b2d`. All results below were reproduced against committed
bytes (counter run via `git show HEAD:… | python3 -B -`, zero writes).

## Findings by severity

### High

**H1 — `MANIFEST_RE` cannot read the committed manifest (backtick gap).**
At `8e408e0`, the committed `.ufo/waves/round-53/settlement.md` writes every seat
name as `` `Name.md` `` inside backticks (lines 17–23), but the committed regex
`^\|\s*([A-Za-z0-9_-]+\.md)\s*\|…` requires the first cell to begin with the bare
name. Verified: `git show HEAD:settlement.md` yields `settled=[]` →
`manifest=incomplete`, exit 1. All seven required names are present yet counted
as omitted — a required-name-omission false negative on the real artifact.
(Working-tree edit adds `` `? `` to the name group — correct direction; see
Residual risk: the same uncommitted edit currently crashes the counter with
`NameError: REQUIRED` at line 69, so at this instant no runnable counter exists.)

**H2 — Phantom `resolved` is indistinguishable from `lost`.**
`MANIFEST_RE` captures the name but discards which disposition was recorded;
`settled` mixes both. The counter never opens `.ufo/waves/round-53/w1/<name>` at
the measured revision. Verified: a manifest listing all seven names `resolved`
alongside the text "0 committed seat reports" still returns `manifest_ok=True`.
A dishonest or self-contradictory settlement ("resolved" pointers to files that
exist nowhere) passes while the repo itself calls `resolved` unverifiable.
Disposition is checked for shape, never for truth.

**H3 — "Every cited w1 seat-report name" is enforced only by the hardcoded
seven.** `NAME_RE` requires the literal prefix `.ufo/waves/round-53/w1/`;
the lane's own documents cite three of the seven loss names bare —
`ScoutS312.md`, `CriticLocators.md`, `ScribeGate.md` (lesson lines 13/15;
spotcheck line 73 lists six of seven without the prefix). Verified `cited` =
exactly the 4 prefix-spelled names, matching the `uncovered=4` receipt. The
other three are covered solely because `REQUIRED_SEAT_NAMES` happens to equal
the closure's enumerated list. Any cited seat-report name outside that constant
(future rounds, renamed seats) is silently unenforced — the predicate's
"every cited name" clause is really "the hardcoded seven plus prefix-spelled
citations."

### Medium

**M1 — Duplicate rows are undetectable.** `set(MANIFEST_RE.findall(…))` collapses
repeats. Verified: an extra `| ScoutS312.md | resolved |` row *and* an identical
duplicate `lost` row both keep `manifest_ok=True`. The predicate records no row
count or per-name disposition consistency — a manifest asserting one seat both
lost and resolved is accepted.

**M2 — Reason column is optional in the check though required by the contract.**
The regex ends at the disposition pipe; `| Name.md | lost |` (no reason cell)
matches. Contract P2.2 requires "`resolved:` or `lost:` with a reason." Verified
pass with all seven rows reasonless.

**M3 — Loss-basis text accepts dishonest counts via substring match.**
`re.search(r"40\s+spawned", m)` has no boundaries — `"240 spawned"` satisfies it;
`"10 committed seat reports"` satisfies `0\s+(committed )?seat reports`.
Verified `has_loss_basis=True` on a manifest claiming 240 spawned / 10
committed. The only required basis is the literal digits appearing somewhere.

**M4 — Arbitrary filenames are silently absorbed.** Any `[A-Za-z0-9_-]+\.md`
row — `InventedSeat.md`, misspelled seat names, names never spawned — enters
`settled` with no diagnostic or allowlist check against `w53-spec.json`
`items[].report`. Verified. (Traversal-shaped names are rejected only
incidentally, by the charset.)

**M5 — Decoy rows match outside the table.** `re.M` `^\|` matches `| name |
lost |` lines inside fenced code blocks or anywhere at column 0. Verified: a
manifest whose visible table is empty but whose fenced block lists all seven
rows still passes — coverage can be hidden while rendered prose contradicts it.

**M6 — Citation inputs are mutable at the measured revision.** `lesson` and
`spotcheck` are `git show`n at `--revision`, not pinned to base `68228b2d`. A
commit may strip `.ufo/waves/round-53/w1/` citations the same revision it adds
the manifest, shrinking `uncovered` — only `REQUIRED_SEAT_NAMES` then guards
the seven. Combined with H3, the citation scan is advisory, not a coverage gate.

### Low

**L1 — Disposition spelling is fail-closed brittle.** `resolved|lost` is
case-sensitive, the row must start `|` at column 0, and the disposition must be
the second cell. `LOST`, `Resolved`, indented rows, or column reorder → treated
as absent (verified). Fails safe but produces false `uncovered` on cosmetically
different manifests.

**L2 — Name charset blind spot.** `[A-Za-z0-9_-]` makes stems containing dots
(e.g. `Seat.A.md`) invisible to both `NAME_RE` and `MANIFEST_RE` — such a seat
can be neither cited-covered nor settled. Real spawn names avoid dots, so no
live exposure; still an unenforced edge of "every cited name."

**L3 — Registry leg brittleness (observed, adjacent to scope).** Committed row
`c53-gate-truth` names a display string, not `c53_gate_truth.py`; the row only
matched because the entry command contains the script name, and it lacks the
`read-only` token → `registry=absent` at HEAD. Seven conjunctive substring
tokens make the row fail on any single missing word.

## Residual risk

- The in-flight working-tree edit fixes only the backtick gap (H1). H2, M1–M6,
  L1–L3 remain in both committed and edited regexes.
- The check stays correct-by-construction for the *omission* of any of the seven
  names only because `REQUIRED_SEAT_NAMES` exactly equals the closure's list —
  verified identical to spotcheck §Dead-seat reconciliation (`ScoutS312`,
  `CriticLocators`, `ScribeGate`, `ScoutQuarantine`, `ReviewerProvenance`,
  `CriticCrossLane`, `ScoutS329`). Any drift between that constant and the
  closure's enumerated names reopens H3 silently.

## Verification gaps

- Mid-edit working tree: `c54_ops_debt.py` mtime 10:50, changed during this
  review; the landed regex/`REQUIRED` tuple must be re-run before scoring.
  Committed counter at HEAD: `registry=absent manifest=incomplete uncovered=4`,
  exit 1; at base `68228b2d` reproduces the frozen receipt
  `registry=absent manifest=absent uncovered=4`, exit 1 exactly.
- Non-UTF8 manifest bytes not fuzzed (decoded `errors="replace"`; plausible but
  unverified).
- `w53-spec.json` confirmed `items=40`, `maxLanes=40`; zero
  `.ufo/waves/round-53/w1/` files in HEAD tree or history — the "0 committed"
  basis is factually true for this lane, so M3/H2 are dishonesty gaps, not
  current-fact errors.

No installs performed; pacman paused per wave rules. Recommendation only —
not an admission.
