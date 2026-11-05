# ScribeLesson — round-98 mistake mining and the considerthese proposal (draft for the L1)

Seat: ScribeLesson (scribe, leaf member — no subagent dispatch).
Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin` (`LANE`).
Round base `e51328b63690c8aaa78c9c8f3b87d8735c0ccbf7`; instruments
`2db768356cd081092c3abc60f76b25487ec4c535`; freeze `c3eace8b5c70453faff872c89d8443753e5d21b6`;
C1 repair `4446ce219b4f0c9f5f4fc81f7f772e3a7f24c95a`; fleet MANIFEST pin
`f86740064229897f53212e03ae3b6474dac66de4`; lane tip at this seat's start
`7838981e4e40280176085e8aa1f6827eb7133a69` (`git -C LANE rev-parse master`).

## Deliverables

- `.ufo/waves/round-98/w1/ScribeLesson/mistakes.md` — the `## Mistakes` draft, 5 rows in the
  `round-97.md` table shape (`# | Class | Evidence | Captured-by | Fix`), each with a `path:line`
  evidence pointer, plus a "not mined, and why" list.
- `.ufo/waves/round-98/w1/ScribeLesson/quality-criterion.md` — the `corpus/QUALITY.md` criterion
  draft for `considerthese/2026-11-05.md` Part 2 **proposal 2** (seat-yield ledger), with the
  pointer the brief requires.
- Receipts (8 files) in the same directory: `receipt-c1-base-reproduce.txt`,
  `receipt-c1-repair-reproduce.txt`, `receipt-capability-drift.txt`, `receipt-seat-yield.txt`,
  `receipt-seat-yield-two-definitions.txt`, `receipt-attack-share-two-denominators.txt`,
  `receipt-attack-share-instance-r96.txt`, `receipt-r98-live-wave-yield.txt`.
- This report is written twice, byte-identically, at `.ufo/waves/round-98/w1/ScribeLesson.md` (the
  trailer path the brief names) and at `.ufo/waves/round-98/w1/ScribeLesson/ScribeLesson.md` (inside
  this seat's own directory). Both are untracked files under `w1/` written by this seat only.

Everything here is a **draft for the L1**. No corpus file, counter, contract, ledger or registry was
edited by this seat; no C1 or C2 verdict is asserted; nothing was committed, pushed, published or
deployed, and no other runtime was invoked.

## Frozen digests verified before use

`sha256sum` against `.ufo/waves/round-98/controls/instrument-sha256.txt`:

| file | pinned | observed | result |
|---|---|---|---|
| `c98_captable.py` | `efd598575c6e377ac76c68c876c96449bf80dc0e4b2fbf8c0436205167ac7cf3` | same | match |
| `c98_stale.py` | `e0331e56378fb5acabe4447a37590cbf3273537aabd8c8d88f842e0a434a9f3f` | same | match |

No frozen byte was touched. The C1 counter was re-run read-only at two committed revisions to
reproduce the two committed controls (`receipt-c1-base-reproduce.txt`, `receipt-c1-repair-reproduce.txt`).

## Re-derivations run by this seat (read-only against the lane)

| receipt | command | observed rc / line |
|---|---|---|
| `receipt-c1-base-reproduce.txt` | `python3 -B .ufo/waves/round-98/c98_captable.py --fleet /home/vgpnk/Projects/shokunin --fleet-revision f8674006… --root . --revision e51328b6… --work <scratch>` | rc=1, `entries=48 rows=14 matched=8 unlisted=40 unbacked=6 mismatches=46 met=false` — identical to committed `controls/base-c1.txt` |
| `receipt-c1-repair-reproduce.txt` | same counter, `--revision 4446ce21…` | rc=0, `entries=48 rows=48 matched=48 unlisted=0 unbacked=0 mismatches=0 met=true` — identical to committed `controls/after-c1.txt` |
| `receipt-capability-drift.txt` | MANIFEST at the pinned fleet revision + the base `## Capabilities` table | 48 admitted kake capability entries (rounds < 98); 8 of them have first-working round > 82 (r83, r85, r87, r88, r90, r93, r97 ×2) and 0 base table rows have round > 82; base table has 14 data rows (`SCORECARD.md:195`–`208` at base) |
| `receipt-seat-yield.txt` | per round: requested = `w1-spec.json` items, settled = `w1-results.json` rows with non-empty output, reports = committed `w1/<Seat>.md` | r89 0/14 settled with 14 reports committed; r90 0/13 settled with 13 reports committed; r93 and r98 have no results file |
| `receipt-seat-yield-two-definitions.txt` | the same waves under two report definitions | wave-root rule: r95 7/12, r96 9/12, r97 10/13; seat-directory rule: 12/12, 12/12, 12/13 |
| `receipt-attack-share-two-denominators.txt` | attack seats over `{reviewer, critic, mutation-tester, labrat}` vs requested/settled | r91 4/13, r92 4/14, r94 4/11, r95 4/12, r96 4/12, r97 6/13 |
| `receipt-attack-share-instance-r96.txt` | the round-96 spec's roles + the run-15 role pin + the published fleet claims | r96 has exactly 4 attack-role seats → strict share 4/12 = 0.3333; published claim is 5/12 ≈ 42 % (fleet `.ufo/reports/round-96/kake.md:73`, lane `LOG.md:3274`), the fifth seat being the sentinel |
| `receipt-r98-live-wave-yield.txt` | the round-98 wave as it stands, read-only | requested 13; wave-root rule 6/13; seat-directory rule 12/13 (`ReviewCapA` the only seat with no report under either); attack-role seats over the run-15 set = 5/13 = 0.3846 |

## Findings
1. **Mistake row 1 — the SCORECARD `## Capabilities` table drifted from the admitted-closure
   record.** Rows stopped entering after round 82 while the lane's own closures kept admitting
   capabilities: eight admitted entries (rounds 83, 85, 87, 88, 90, 93, 97 ×2) were demonstrated and
   recorded in per-round `### Demonstrated repertoire` subsections but never entered the table at
   `SCORECARD.md:191`, and six table rows were unbacked — five naming capabilities whose closures
   were never admitted (rounds 34, 35, 37, 61, 64) and one naming an admitted round-20 capability
   under different wording. Evidence: `controls/base-c1.txt:2`
   (`entries=48 rows=14 matched=8 unlisted=40 unbacked=6 mismatches=46 met=false`, exit 1).
   Captured by **a rule that never reached this case**: `AXES.md` §Capabilities constrains the
   *entry* of a row ("Rows enter only through a round that demonstrates the capability running")
   but nothing checked the reverse direction — that every admitted capability has a row — until
   round 98's `c98_captable.py` (`SKILL.md:223`). The C1 repair at `4446ce2` re-derives to
   `mismatches=0 met=true` (exit 0), which this seat re-ran read-only.
2. **Mistake row 2 — the R98-D1 seat meta-text leak.** `corpus/knowledge/revalidation-exchange.md:130`
   at `7838981e` carries a malformed duplicate heading with an unbalanced backtick and the drafting
   receipt verbatim ("… word-count receipt in quotes-verified.txt, rc 0, count 103. Drafted by
   ScoutErrata; the L1 integrates it (this seat makes no knowledge-entry edit)."), two lines above
   the real `## Errata sweep (round 97)` heading at line 132. Captured by the **round-97 closure**
   (spot-check §1 D-a, §6 R98-D1), not by any lane rule — no criterion covered seat meta-text in
   `corpus/knowledge/`. The round-98 work is seat `ExecMetaLint`'s
   `scripts/knowledge_metatext_lint.py` (selftest 13/13 at `.ufo/waves/round-98/w1/ExecMetaLint/selftest.txt`);
   this seat neither wrote nor ran that instrument and claims no verdict on it.
3. **Mistake rows 3–5 — three routes the lane's own mined corpus never carried.** Row 3: the
   round-94 closure's "landed-tip receipts uncommitted" route
   (`corpus/lessons/round-94-verifier-spotcheck.md:118`) never appears in any lesson's `## Mistakes`
   table, though rounds 95–97 each landed a tip receipt afterwards. Row 4: a live misstatement —
   the published round-96 attack share "5/12 ≈ 42 %" counts the sentinel, the exact defect class the
   round-80 closure routed (R80-4) and `.ufo/waves/round-81/w1-accounting.json:2` pinned ("sentinel
   is not an attack role"); the round-96 spec has four attack-role seats, so the strict figure is
   4/12 = 33.3 %, and no closure or lesson has checked it since. Row 5: the round-95 closure's
   trend-label vocabulary route (`round-95-verifier-spotcheck.md:77`) likewise never reached a
   lesson row.
4. **Proposal 2 is the right pick and it is genuinely unimplemented.** `considerthese/2026-11-05.md`
   Part 2 proposal 3 (held-out vs frozen divergence) is **already** implemented as
   `corpus/QUALITY.md:1848` (R95-D), so it must not be re-implemented. Proposal 2 (seat-yield
   ledger) is open: `.ufo/waves/round-<N>/w1-accounting.json` exists for rounds 81–86 only and in
   four different shapes, and no lane artifact carries a yield line for rounds 87–98.
5. **The proposal's own three examples re-derive exactly** from committed bytes — r91 9/13, r92
   13/14 with `SentinelQuote` empty, r93 with no results file at all — which is why the criterion
   can be written against real numbers rather than against a description of numbers.
6. **Two definitional gaps make a naive yield line wrong**, and both are measured here: "a seat
   that committed a report" has two live readings that differ by up to five seats on the same
   committed bytes (r95 7/12 vs 12/12), and "settled" as "non-empty output" reads 0/14 and 0/13 for
   rounds 89 and 90, in which every seat's report is committed and the results rows are `null`
   because of an orchestrator kernel restart. The criterion therefore requires the population to be
   stated in words before the numbers.
7. **The daily note is not the lane's file.** `git log --format='%an' -- considerthese/` shows the
   lane's `considerthese/` entries are authored by the operator. A lane criterion must not require
   the lane to write there; the criterion is written so a round satisfies it with a lane-side
   artifact instead.
8. **Overlap with the L1's landed lesson, found mid-task.** After the drafts were written, this seat
   found `corpus/lessons/round-98.md` already present (untracked, authored by the L1), carrying an
   M1 (the Capabilities drift), an M2 (the R98-D1 leak) and an **R98-B** criterion for
   `considerthese/2026-11-05.md` proposal 2. Rows 1–2 of this seat's draft agree with the L1's M1/M2
   on the evidence and the fix and add the `path:line` pointers; rows 3–5 are **new**
   (`grep -n 'landed-tip\|improved-bounded\|attack share' corpus/lessons/round-98.md` → no hit).
   The criterion draft is written to **extend** R98-B, not to replace it.
9. **The round-98 wave is the live instance of the definitional gap.** Measured read-only while the
   wave was still running (`receipt-r98-live-wave-yield.txt`): under the wave-root rule the wave
   reads 6/13 and under the seat-directory rule 12/13, and the L1's own R98-B line ("this round's
   line reads 12/13 with ReviewCapA producing no file") uses the seat-directory rule without naming
   it. The criterion's R98-Y2 requirement — the population stated in words before the number — is
   exactly what would make that line unambiguous.

## Out of scope for this seat (not touched, not claimed)

- No product code, instrument, counter, contract, ledger, registry or corpus file was edited.
- No verdict is asserted for C1 or C2. The C1 predicate's second conjunct (`w1/ReviewCapA/verdicts.tsv`
  + `w1/ReviewCapB/verdicts.tsv`) and the C2 verdict line are the L1's to record; this seat read
  neither reviewer verdict.
- No mutating git or jj command was run in the lane or the fleet repo; `git status --porcelain` in
  the lane shows only files other seats and the L1 are already editing (`corpus/knowledge/revalidation-exchange.md`
  modified, `scripts/stale_extensions.py`, `scripts/knowledge_metatext_lint.py` and `.ufo/waves/round-98/`
  untracked) — none of them this seat's.
- No commit, push, publish or deploy; no other runtime invoked.
- This seat's own scratch tree (`/fast/scratch/hyaku/kake-r98/ScribeLesson/`) was removed after its
  receipts were copied into this seat's `w1/` directory. No ancestor or sibling of it was touched.
- Disclosed residue: while measuring the fleet `MANIFEST.json` this seat wrote a 4.7 MB copy to
  `/fast/scratch/hyaku/kake-r98-manifest.json` — one level **above** its own seat directory. The
  round-98 brief says to delete only its own seat directory and never an ancestor or sibling, so
  that file was deliberately **left in place** rather than removed. It is this seat's own file and
  is safe to delete by its owner.

## Tooling

No tool was installed or upgraded by this seat; the work used only the repository's committed Python 3
counter, `git` and standard shell tools already present on the host. No `pacman`, `uv`, `npx` or
`~/.local/bin` action was taken.

## Out-of-lane note (reported, not acted on)

While sweeping for unmined routes this seat observed that the published round-96 attack share in the
**fleet** repo (`.ufo/reports/round-96/kake.md:73`) counts the sentinel as an attack seat, against
the run-15 role set the lane itself pinned. The lane's `LOG.md:3274` repeats the same figure. Both
are filed bytes in files this seat may not edit; the correction belongs to the L1 or to the fleet
closure, and it is routed here rather than repaired here.

SCRIBE-LESSON mistakes=5 proposal=2
