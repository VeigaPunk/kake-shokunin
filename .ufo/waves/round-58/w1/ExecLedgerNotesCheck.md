# ExecLedgerNotesCheck

Scope: C1 (calibration, receipt rewrites). Read-only check of the evidence-pointer clause (`unpointed`) of
`.ufo/waves/round-58/c58_receipt_rewrites.py` — which pointer forms the C1 ledger (`.ufo/waves/round-58/receipt-rewrites.json`) can
use in its `note` field — plus an existence matrix at base `044048597d62f3199494b63b36e90dd57825e350`. No lane write except this report
and `.files/`; no git/jj mutation; all runs read-only against the lane.

Method: `importlib` load of the counter (`python3 -B`, no bytecode in the lane), `pointed()` called directly with `root=<lane>`,
`tip=<base>`; tip-dependent cases on a `git clone -q --shared` in scratch (`rev-parse --show-toplevel` verified equal to the clone dir
before the single `-c user.name=selftest` commit; clone tip `771796c`).

## EXISTING POINTERS:

Existence at base (the tip every note is graded against is a later tip; round-58 paths below are absent at base because
`.ufo/waves/round-58/` is untracked there — they become valid pointers only once committed at the measured tip).

| candidate | round-52 | round-53 | round-54 | round-55 | round-56 | round-57 |
|---|---|---|---|---|---|---|
| `settlement.md` | absent (never added: 0 add-commits) | EXISTS | absent | EXISTS | EXISTS | EXISTS |
| `contract.md` | absent | absent (never added) | EXISTS | EXISTS | EXISTS | EXISTS |
| `contract.json` | EXISTS | absent | absent | EXISTS | EXISTS | EXISTS |
| `LOG.md` | absent | absent | absent | absent | absent | absent |
| `SCORECARD.md` | absent | absent | absent | absent | absent | absent |
| `receipt-errata.json` | absent | absent | absent | absent | absent | absent | EXISTS |
| `control/` or `controls/` dir | `control/` EXISTS | `exec-quality-gate/` (no `control(s)/`) | `controls/` EXISTS | `controls/` EXISTS | `controls/` EXISTS | `controls/` EXISTS |
| `assimilation/pre-append/SCORECARD.md` or `assimilation/validate/SCORECARD.md` | EXISTS | absent | absent | EXISTS | EXISTS | EXISTS |

Repo-root pointers: `LOG.md` EXISTS (2210 lines), `SCORECARD.md` EXISTS (4378 lines), `SKILL.md` EXISTS, `MANIFEST.json` absent.

Lesson pointers, all twelve EXIST at base: `corpus/lessons/round-{52..57}.md` and `corpus/lessons/round-{52..57}-verifier-spotcheck.md`.
Per-round lesson/settlement seat reports that exist: `.ufo/waves/round-54/w1/ScribeC2Settlement.md`,
`.ufo/waves/round-55/w2/ReviewerLessonGate.md`, `.ufo/waves/round-55/w2/ExecSeatSettlement.md`,
`.ufo/waves/round-56/w2/ExecLessonNumbers.md`, `.ufo/waves/round-56/w2/ReviewerLessonSkill.md`,
`.ufo/waves/round-57/w1/ScribeLessonMistakes.md`, `.ufo/waves/round-57/w2/CriticLessonGate.md`,
`.ufo/waves/round-57/w1/ExecErrataBuild.files/receipt-errata.json`.
All 19 receipt paths the ledger must disclose exist at base, e.g. `.ufo/waves/round-52/control/c1-mutation-ladder.json`,
`.ufo/waves/round-57/controls/after-c1-receipt-pins.txt`.

## POINTED() BEHAVIOUR:

Rule as coded: path arm = `POINTER_PATH_RE` `(?<![\w/.-])((?:\.ufo|corpus|scripts|SCORECARD\.md|SKILL\.md|LOG\.md)[\w./-]*)`,
then `rstrip(".,;:)")`, then `git cat-file -e <tip>:<path>`; hash arm = `(?<![0-9a-zA-Z])[0-9a-f]{7,40}(?![0-9a-zA-Z])` plus
`git rev-parse --verify -q <hex>^{commit}`. True on the first path that exists at the tip, else on the first hex that resolves.

| # | note (verbatim) | pointed |
|---|---|---|
| S1 | ``fill landed in `.ufo/waves/round-55/settlement.md` `` | True |
| S2 | `disclosed in .ufo/waves/round-57/receipt-errata.json.` | True |
| S3 | `(see .ufo/waves/round-54/contract.md)` | True |
| S4 | `see .ufo/waves/round-52/settlement.md` | False |
| S5 | `see settlement.md` | False |
| S6 | `see contract.md` | False |
| S7 | `revision 0440485` (7-hex commit) | True |
| S8 | `revision 044048597d62` (12-hex commit) | True |
| S9 | `revision 044048` (6-hex) | False |
| S10 | `SCORECARD.md:4330` | True |
| S11 | `source https://ziyuan.baidu.com/college/articleinfo?id=3457` | False |
| S12 | `see corpus` (directory) | True |
| S13 | `see .ufo` (directory) | True |
| S14 | `ledger .ufo/waves/round-58/receipt-rewrites.json` (at base) | False |
| S14b | same note at scratch tip carrying that file | True |
| S15 | `object 9b8abf0` (7-hex blob id) | False |
| S16 | `see LOG.md` | True |
| S17 | `see corpus/lessons/round-53.md` | True |
| S18 | `x` | False |
| S19 | `see ./.ufo/waves/round-55/settlement.md` | False |
| S20 | `see kake-shokunin/.ufo/waves/round-55/settlement.md` | False |
| S21 | `revision 0123456789ab` (non-resolving 12-hex) | False |
| S22 | `see .ufo/waves/round-55` (directory) | True |
| S23 | `SCORECARD.md#L4330` | True |
| S24 | `.ufo/waves/round-58/controls/after-c2-x.txt` (absent at base) | False |
| S25 | `see .ufo/waves/round-57/controls/after-c1-receipt-pins.txt` | True |
| S26 | `revision ffffffffffffffffffffffffffffffffffffffff` | False |
| S27 | `SCORECARD.md:99999` | True |
| S28 | `.ufo/waves/round-57/settlement.md#D1` | True |
| S29 | `revision 044048597D62` (uppercase hex) | False |
| S30 | `revision 312acd45a38f44325705e923b558530153dbd248` (40-hex tree id) | False |

Answers to the named questions: a path in backticks counts (S1); a path followed by `.` or `)` counts (S2, S3); a 7-hex commit id
counts (S7); a 12-hex id counts when it resolves, and no ambiguous 7- or 12-hex prefix exists in this lane (`git rev-list --all`,
1270 commits, 0 duplicate 7-hex and 0 duplicate 12-hex prefixes; a non-resolving 12-hex fails, S21); a URL never counts (S11);
`SCORECARD.md:4330` counts as `SCORECARD.md` alone, the line number is discarded unchecked (S10, S27).
12-hex "ambiguous" is unreachable here, so ambiguity is a latent risk only, not a live failure.

## DEFECTS:

1. **No relevance test.** `.ufo` (S13), `.ufo/waves/round-55` (S22), `corpus` (S12) and `LOG.md` (S16) all satisfy `pointed()`.
   A note reading `see .ufo` clears `unpointed=0` while naming no evidence at all.
2. **Line/anchor suffixes are dropped and never validated.** `SCORECARD.md:99999` is True although the file has 4378 lines at base;
   `SCORECARD.md:4330` is True but that line reads "the ownership ruling.", not receipt evidence. `#L4330` and `#D1` behave the same.
3. **Existence is graded at the measured tip, not at the event commit.** `corpus/lessons/round-53.md` (written in a later round)
   counts as the pointer for any round-52 event (S17). A path that existed when the receipt changed but was later deleted cannot be
   cited at all. The clause tests "some file exists now", not "the cited file evidences this change".
4. **Self-reference passes.** At a tip carrying the ledger, `.ufo/waves/round-58/receipt-rewrites.json` is itself a valid pointer
   (S14b), so every note may read `see .ufo/waves/round-58/receipt-rewrites.json` and satisfy the clause. Likewise naming the
   rewrittee (`see <receipt path>`, S25) counts — which is what the build's proof ledger does for all 19 entries.
5. **Common citation forms are rejected, and one rejection fails the whole predicate.** `./.ufo/...` (S19) is blocked by the
   lookbehind guard `(?<![\w/.-])`; a lane-qualified `kake-shokunin/.ufo/...` (S20) is blocked the same way; bare `settlement.md`,
   `contract.md`, `receipt-errata.json` (S5, S6) and any `round-55/...` form are never matched, though `round-52/settlement.md`
   (S4) shows the underlying file may also be absent. One such note costs `met=False`, so note prose must use the narrow
   `.ufo/`-prefixed or root-file form.
6. **URLs and uppercase hex never count** (S11, S29); the hex arm is lowercase-only and requires `^{commit}`, so blob/tree ids (S15,
   S30) and 40-hex ids from another repo (S26) are unpointed. Uppercase is plausible in prose copied from some git frontends.
7. **Latent 7-hex ambiguity.** A 7-hex abbreviation resolves only while unique; a future commit could make a currently passing note
   fail with no ledger change. Measured today: 0 collisions at 7 and 12 hex over 1270 reachable commits, so this is a hazard, not a
   present defect. `corpus/lessons/...` style 12-hex is safe by length.
8. **Consequence for C1 as written:** the `unpointed` clause is satisfiable trivially (defects 1, 4) and is not a check that the
   note's evidence is about the event; that strength lives only in the reviewer-checked "prose truth" limit the contract already
   states. The 19-note ledger must therefore be graded by a reviewer, and notes should cite the receipt path (strongest available
   form) rather than `.ufo` or the ledger itself.

## Risks / notes

* `pointed()` spawns one `git cat-file`/`rev-parse` per match; 19 entries × few matches is fine, no timing risk observed.
* Ledger build's proof notes are `see {path}` (receipt path) — they pass, and per defect 4 they pass for the weakest reason;
  `ExecLedgerBuild.md` already flags that kind-correctness is correct-by-construction, notes are the L1's merge step.
* The lane's `.ufo/waves/round-58/__pycache__/` already existed; all imports ran with `python3 -B`, no bytecode written.
* No tool installed or upgraded; no pacman invocation. Scratch `/fast/scratch/hyaku/kake-r58/ExecLedgerNotesCheck` (probe + json
  transcript copied to `.files/`) deleted at finish.

VERDICT: pointer clause measured — `.ufo`/`corpus`/`scripts`-prefixed paths, the three root files, or a lowercase 7-40 hex commit id count; `./`-prefixed, lane-qualified, bare `settlement.md`/`contract.md`, URL and uppercase-hex forms do not, and `.ufo`, directory, self-ledger and bogus-line-number pointers pass, so the clause detects "a file exists now" and not evidence of the event.
