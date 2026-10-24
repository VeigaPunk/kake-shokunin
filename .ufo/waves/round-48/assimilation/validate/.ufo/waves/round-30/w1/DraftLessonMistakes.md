# KakeR30.DraftLessonMistakes — round-30 `## Mistakes` draft

Seat: wave-1 scribe, leaf. Lane repo `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Axes judged: operability, freshness.

**Deliverable (sandbox, not integrated by me):**
`/fast/scratch/hyaku/kake-r30/w1/DraftLessonMistakes/mistakes.md`

It contains a ready-to-paste `## Mistakes` section for `corpus/lessons/round-30.md`
(four rows, each with class, evidence pointer, captured-by criterion, and a fix
shown able to fail), plus four drafted `corpus/QUALITY.md` bullets in the file's
existing bullet form, each with a `Fails if:` sentence and the command that
would show it failing. The L1 decides what lands in the lane.

## The four mistakes, their criteria, and their failing-check commands

| # | Mistake | Criterion (QUALITY.md) | Failing-check command (observed exit) |
|---|---|---|---|
| M1 | A falsify seat ran `freshness-sweep.mjs` with no section flag and reached owned sites | Existing: `corpus/QUALITY.md:10` "Replayable claim". New bullet drafted: "A seat names its offline mode before it runs a lane tool that reaches a live surface." | `python3 -B witness_sweep_live_mode.py --root <lane> --round round-29 --revision 234524c` → **exit 1**, names `.ufo/waves/round-29/w2/NoHarmExistingGates.md:30`. Same command `--round round-30 --revision 04637bd` → exit 0. |
| M2 | Receipts named no revision or tool digest | Existing: `corpus/QUALITY.md:10` "Replayable claim", `corpus/QUALITY.md:128-131` (round-22 receipt bullet). New bullet drafted: "A measurement receipt names the revision it measured and the digest of the bytes it measured." | `python3 -B witness_receipt_identity.py --root <lane> --wave round-29 --revision 234524c` → **exit 1**, 7 receipts unidentified (3 anonymous, 4 partial). `--wave round-30 --revision 04637bd` → exit 0. |
| M3 | The report cited re-measurement receipts never committed | Existing: `corpus/QUALITY.md:10` "Replayable claim", `corpus/QUALITY.md:11` "Missing substrate stays visible". New bullet drafted: "A named measurement revision has a committed receipt that names it." | `python3 -B witness_claim_receipt_backing.py --root <lane> --report .ufo/reports/round-29/kake.md --wave all --revision <tip>` → **exit 1**, unbacked `234524c`, `7697990`. Exit 0 at a sandbox commit carrying the four `r29-remeasure` receipts. |
| M4 | The C2 counter compared no id, page, resolved or counts | Existing: `corpus/QUALITY.md:362-374` "A counter compares the reason code, not only the id", `corpus/QUALITY.md:317-322` "Conformance exceptions stay named". New bullet drafted: "A counter compares every field its expectation names, and its usage case is judged on the usage object, not the exit code alone." | `python3 -B witness_c2_field_comparison.py --root <lane> --revision 234524c` → **exit 1**: never compares `id`, `page`, `resolved`, `pagesChecked`, `referencesChecked`; a mutant with all of those wrong still scores 30/30, exit 0. Same at `04637bd`. |

Each witness is a text or byte scan of committed data. None runs the sweep,
`probe-delta.mjs` or `live_snapshot.py`; those tools were read, never executed.
No live request was made to any owned site.

## Evidence the fixes can fail

- M1: the round-30 wave context bars the three owned-surface tools and names
  the offline flags (`--offline`, `--section=paths`, `--section=history`,
  `--selftest`, `--help`). Round-30 wave files scan clean (exit 0).
- M2: the round-30 receipts carry `revision` plus `counterSha256`,
  `gateSha256`, `runnerSha256` (`verification/c1-before-0356681.json`,
  `verification/c2-before-0356681.json`).
- M3: the four receipts under `.ufo/waves/round-30/verification/r29-remeasure/`
  name their revision, the counter path, the counter blob, the counter
  sha256, the exit code and the output.
- M4: an extended matrix whose expectations name `id`, `page`, `resolved` and
  the counts, plus a strict counter that compares them, rejects the shipped
  counter's accepted mutants — 9/30 and 29/30, exit 1 — while scoring the real
  tool 30/30 with all three constant gates rejected.

## Out of scope, left for the L1

- **The four `r29-remeasure` receipts are still untracked** at lane tip
  `04637bd` (`git status` shows `?? .ufo/waves/round-30/verification/r29-remeasure/`).
  Until they are committed, M3 is still failing. The L1 must commit them.
- The witness scripts, the extended matrix and the strict counter live in this
  seat's sandbox. Landing them in the lane (for example under
  `.ufo/waves/round-30/verification/`) is the L1's call; the QUALITY bullets as
  drafted name those lane paths.
- The round-30 `corpus/lessons/round-30.md` does not exist yet; this seat did
  not create it, since the L1 owns the lesson file.

## Bounds honoured

No file in the lane was created or modified by this seat. No git or jj command
that mutates state was run in the lane or the fleet repo; the lane working tree
was read only. The fleet report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-29/kake.md`
was read, not written. The sandbox clone at
`/fast/scratch/hyaku/kake-r30/w1/DraftLessonMistakes/clone` received one
throwaway test commit (since reset) to prove the M3 witness passes once the
receipts land.

## No installs

Nothing was installed. No pacman transaction, no `uv tool install`, no npm or
cargo install. The witnesses use only Python 3.14 standard library and `git`,
both already present.

## Files delivered (all in the sandbox)

- `/fast/scratch/hyaku/kake-r30/w1/DraftLessonMistakes/mistakes.md` — the draft
- `/fast/scratch/hyaku/kake-r30/w1/DraftLessonMistakes/witness_sweep_live_mode.py`
- `/fast/scratch/hyaku/kake-r30/w1/DraftLessonMistakes/witness_receipt_identity.py`
- `/fast/scratch/hyaku/kake-r30/w1/DraftLessonMistakes/witness_claim_receipt_backing.py`
- `/fast/scratch/hyaku/kake-r30/w1/DraftLessonMistakes/witness_c2_field_comparison.py`
- `/fast/scratch/hyaku/kake-r30/w1/DraftLessonMistakes/strict_c2_counter.py`
- `/fast/scratch/hyaku/kake-r30/w1/DraftLessonMistakes/build_extended_matrix.py`
- `/fast/scratch/hyaku/kake-r30/w1/DraftLessonMistakes/extended-matrix.json`
  (sha256 `bfdb9d9473fb00c5abf7e93802cba9eb637958dad91551c768780b81ae1337ad`)

Report: .ufo/waves/round-30/w1/DraftLessonMistakes.md
