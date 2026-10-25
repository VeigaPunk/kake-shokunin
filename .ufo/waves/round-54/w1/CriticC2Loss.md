# CriticC2Loss — can an all-`lost` settlement pass without evidence?

Scope: round-54 C2 (`.ufo/waves/round-54/c54_ops_debt.py`, frozen predicate in
`contract.md`): "registry row present, settlement manifest committed, and every
cited w1 seat-report name recorded resolved or lost; met when all three hold."
Question attacked: does a settlement that lists all seven cited report names as
`lost` need evidence behind the `lost`, and does the counter distinguish
evidence-backed *lost pointer* from inferred *individual seat death*?

**Verdict: yes, it passes without evidence — by predicate construction and by
instrument weakness, not by accident. The committed manifest happens to be the
honest version of the settlement, but the counter cannot tell the honest version
from a fabricated one, and it structurally presupposes the all-lost outcome.**

## Counterexamples (all reproduced against `c54_ops_debt.py` at `acae1dc`)

### 1. The predicate itself is bookkeeping, not truth
The frozen predicate requires each cited name be "recorded resolved or lost."
Recording ≠ evidence. The counter enforces this faithfully:

- `MANIFEST_RE` (line 35): `^\|\s*`?([A-Za-z0-9_-]+\.md)`?\s*\|\s*(?:resolved|lost)\s*\|`
  matches on name + bare disposition token only. The **reason cell is never
  read**. Verified: `| ScribeGate.md | lost |` (two cells, no reason) parses;
  `| ScoutS329.md | lost | seat died, trust me |` parses identically. An
  evidence-bearing reason ("non-author census found no committed w1/ report")
  and a null/junk reason are counter-indistinguishable.
- `resolved` rows are never checked against file existence. A manifest that
  lists all seven names `resolved` with zero corresponding files anywhere in
  the tree produces the identical `settled` set. `resolved` and `lost` are
  symmetric — the disposition carries no constraint. This is the
  false-provenance hole: the predicate certifies that a claim was *written*,
  never that it is *true*.

### 2. `has_loss_basis` checks prose about evidence, not evidence
Lines 78–79 require the manifest to contain literal `40 spawned` and
`0 (committed )?seat reports`. The counter never recomputes either number:

- `w53-spec.json` `items` length is never parsed; `git ls-tree` /
  `git show <rev>:.ufo/waves/round-53/w1` is never invoked. A manifest claiming
  "140 spawned, 10 committed seat reports" still passes — the substrings
  "40 spawned" and "0 committed seat reports" match unanchored inside the wrong
  numbers (verified by regex test).
- **The check presupposes the all-lost outcome.** Any manifest that recovers
  some reports and truthfully writes "3 committed seat reports recovered" or
  "4 reports resolved" fails `has_loss_basis` even though the predicate's
  "resolved or lost" would cover it. `resolved` is admitted by the row regex
  but vetoed by the basis check — an inconsistent pair that admits exactly one
  shape of settlement: all-lost or resolved-only-without-evidence.
- Basis is self-certifying prose, so a manifest can state a false 40-vs-0 basis
  and pass; and the honest basis fails on a one-word paraphrase — during this
  wave I observed an earlier worktree snapshot of `settlement.md` reading
  "records **zero** committed seat reports" (committed bytes now read
  "**0** committed seat reports"; HEAD tree now carries the file under
  `acae1dc`). "zero" does not match the regex: identical truth, flipped verdict.
  The edit history suggests the wording was tuned to the regex — the counter
  shaping the evidence it was meant to check.

### 3. Citation coverage is partial and backstopped, not derived
`NAME_RE` extracts only `.ufo/waves/round-53/w1/<name>.md`-prefixed mentions.
The round-53 lesson cites all 7 with the prefix; the spotcheck cites 4
path-prefixed + 7 bare names. Base control shows `cited=4` — the bare-name
mentions are invisible, so "every cited w1 seat-report name" is effectively the
hardcoded `REQUIRED_SEAT_NAMES` (7 names). Two consequences:

- Any *additional* `w1` path cited in a future lesson/spotcheck revision passes
  unrecorded unless it duplicates the hardcoded list — coverage is not
  under-verifyable today but is not future-proof.
- A fabricated name in the manifest adds noise harmlessly (`uncovered` is
  `cited - settled`; extra settled names are not penalized and not checked for
  seat validity). All 7 names do happen to be members of `w53-spec.json` items
  (verified), but the counter never checks name↔seat correspondence — a
  non-seat `FakeSeat.md | lost` row passes.

### 4. What the evidence actually is, and what "spawned" means
The cited-names' provenance itself is weaker than the word "cited" implies:
`w53-spec.json` items carry only `{name, prompt, role}` — **no report field, no
declared `w1` path** (verified; only one `w1` substring in the whole spec, the
registry `reportDir`). The seven `.ufo/waves/round-53/w1/<Name>.md` paths are
pointers invented by the lesson's prose, never by the dispatch spec. The
spotcheck's "unresolvable pointers" framing is therefore exactly right: the
loss exists at pointer level only.

And "40 spawned" rests on `items` length = 40 — the *declared* dispatch set —
plus a driver launch/complete digest in the spotcheck. It is not an observed
spawn count. The round-52 precedent (0 of 46 seats spawned, host job cap,
reported in `considerthese/2026-10-25.md`) shows spec length ≠ spawned seats.
The committed settlement does hedge correctly ("The 40-seat launch happened,
but the individual dead-seat count remains unverified"), but the counter
certifies the string "40 spawned" as a fact it never re-derives.

## The distinction question — answered directly

- **Evidence-backed `lost` (missing pointer):** `| X.md | lost | <census
  reason>` where the pointer's absence was actually surveyed (spotcheck
  §§Conformance, Dead-seat reconciliation; `git ls-tree` confirms no
  `round-53/w1` at any revision). This is what the committed manifest does and
  what its reasons cite. Legitimate.
- **Inferred individual seat death:** claiming seat X *died in flight* because
  its report is absent. Absence of a committed artifact is consistent with
  died-in-flight, never-spawned (job cap), wrote-elsewhere, and
  spawned-but-uncommitted — all indistinguishable from committed bytes alone.
  The committed manifest explicitly refuses this inference ("individual death
  outcomes are not recoverable and are unverified, not inferred"). Correct.
- **What the counter does:** neither. `lost` with no reason, `lost` with the
  death-inference reason, and `lost` with the census reason produce identical
  verdicts. The instrument certifies token coverage and two magic strings; the
  pointer-vs-death distinction lives only in manifest prose that the counter
  never parses. Evidence-backed and inferred `lost` are equivalent under the
  frozen predicate.

## Impacted axes

- **Operability (primary):** the claim can go green with a ledger that records
  names and a magic sentence — the operability artifact exists but is
  uncoupled from the debt it settles.
- **Discernment (secondary):** a counter that accepts `| X | lost |` bare
  cannot discriminate evidence-backed settlement from assertion; measured
  green would overstate discernment.
- Freshness/quality: not impacted.

## Smallest safe correction

1. In `run_checks`, recompute both basis numbers from committed bytes:
   `items` length of `w53-spec.json` at `<rev>` (declared seats) and
   `git ls-tree <rev> .ufo/waves/round-53/w1` (committed reports). Require the
   manifest's stated numbers to equal the recomputed ones — kills fabricated
   and substring-matched bases, and correctly reports "declared" vs "observed."
2. Enforce the disposition against the tree: `lost` ⇒ path must not exist at
   `<rev>`; `resolved` ⇒ path must exist at `<rev>` and the reason cell must be
   non-empty (extend `MANIFEST_RE` to require a third cell). This makes
   `resolved`/`lost` asymmetric the way the predicate intends and kills the
   false-provenance hole.
3. Remove the all-lost presupposition: make `has_loss_basis` verify
   `declared − committed == count of lost rows` instead of matching literal
   "0 … seat reports," so a partial-recovery settlement can pass truthfully.

Alternative (cheaper, honest): drop `has_loss_basis` from the claim and
restate the predicate as the bookkeeping check it actually is — then a green
verdict asserts only "the debt is on record," not "the record is true." That
is a coherent predicate; the current hybrid (prose check dressed as evidence
check) is the least defensible of the three options.

## Fixable defect vs canonical-judge tradeoff

The defect is fixable and instrument-local: the predicate, the counter, and the
manifest can each be corrected without touching round-53's frozen artifacts
(the manifest is append-only and self-describing; a corrected counter would
still pass the *current* manifest, since its claims are actually true — good).
This is not a tradeoff the judge must reject the correction over; the current
counter passing all-lost-without-evidence is a bug, not a defensible
simplification.

## Basis checks run (read-only, per assignment)

- `python3 -B .ufo/waves/round-54/c54_ops_debt.py --root . --revision 68228b2d…` →
  `registry=absent manifest=absent uncovered=4` EXIT=1 (matches committed
  control `controls/base-c2-ops-debt.txt`).
- Same at `HEAD` (`acae1dc`) → `registry=absent manifest=present uncovered=0`
  EXIT=1 — the committed manifest already satisfies every manifest check;
  only the uncommitted `SKILL.md` registry row (worktree has it, line 213)
  blocks green.
- `git show HEAD:.ufo/waves/round-53/{settlement.md,w53-spec.json}`,
  `git ls-tree` for `round-53/w1` at `68228b2` and `acae1dc` (absent both).
- Regex probes in-process only; no files created or modified in the lane.

## Tools installed

None. (pacman paused host-wide; nothing required.)
