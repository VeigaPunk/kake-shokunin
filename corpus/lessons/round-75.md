# Round 75 — lessons (kake, attempt 1)

Base `c9c5e484c533aa65f4374b841a3edcf572ed19a9` (lane master at round open). Frozen contract
`.ufo/waves/round-75/contract.md` at `88f2e05f36f008faf01fcf77afedd33ae3c53e40`; amendments 1
(`9a9c4a6f`), 2 (`d599c8be`) and 3 (`7348d37e`), each terms-only and recorded before any
after-state. Measured at the carrier tip `f87d14a949e1b5f8b4ec5807b75f22aa3e337353`. Wave `w1`: one
v1 wave, 14 seats (scout 2, executor 4, scribe 2, reviewer 2, critic 1, mutation-tester 1,
connector 1, sentinel 1; attack share 4/14 = 28.6 %; the L1 held the planner seat).

## Claims

**C1 — calibration (owned score 2, the lane's lowest non-retired axis).** The gate registry stops
claiming states its instruments do not have: every live registry row's claim re-derives by
execution, `mismatches` 2 → 0 over a frozen 16-file population that grows to 18 with the round's own
instruments. Predicate E1–E4 over the row *effective* for each file (the last row naming it; a row
may be superseded by an appended row, never deleted): E1 the row's own `--selftest` exits 0 or its
Kind cell declares `differential` as a whole word (amendment 2: the command must invoke the row's
instrument — a shell comment or a different file never binds); E2 a recorded `a/b` tally equals the
observed pass/total; E3 two or more enumerated `f<N>` ids equal the observed total; E4 every
`.py`/`.mjs` token of every live row resolves at the measured revision. `append_only` holds when
every live row name at `--base` is still present; `missing_frozen` counts floor paths the derivation
no longer produces (amendment 1); `met = (mismatches == 0) and append_only`.

```sh
python3 -B .ufo/waves/round-75/c75_row_truth.py --root . --revision <rev> \
    --base c9c5e484c533aa65f4374b841a3edcf572ed19a9 --work <scratch dir outside the lane>
```

Base `c9c5e484`: `rows=28 live=16 files=16 mismatches=2 classes=E1 E3 append_only=true met=false
missing_frozen=0`, exit 1 — `controls/base-c1-row-truth.txt`. Tip `f87d14a9`: `rows=32 live=20
files=18 mismatches=0 append_only=true met=true missing_frozen=0`, exit 0 —
`controls/after-c1-row-truth.txt`. Counter selftest 29/29 (`--selftest --work <dir>`); the two base
findings are the round-74 closure's R2 (`c69_tmp_honour.py`: Kind `gate`, no self-test mode) and R1
(`c74_registry_gap.py`: five enumerated fixture ids, eight observed).

**C2 — operability (owned score 10, HOLD; capability acquisition).** Every live registry instrument
is bound to a committed receipt that re-derives from committed bytes: `bound` 0 → 18 (the frozen 16
floor plus the round's two instruments), `mismatches` 18 → 0. Receipt
`corpus/knowledge/instrument-receipts.json`, schema `instrument-receipts/v1`, one entry per file
`{path, sha256, bytes, selftest_mode}`; `--check` reads the receipt from committed bytes at the
measured revision (amendment 3 A6 — a worktree-only receipt is a mismatch), validates the declared
revision as a resolvable ancestor (A7), and re-derives the blob digest, length and static
`--selftest` registration. `met = (bound == population) and (mismatches == 0) and missing_frozen == 0`.

```sh
python3 -B scripts/instrument_receipts.py --root . --revision <carrier commit> --check
```

Base (receipt absent): `population=16 bound=0 mismatches=16 met=false`, exit 1 —
`controls/base-c2-receipts.txt`. Carrier `f87d14a9`: `population=18 bound=18 mismatches=0 met=true
missing_frozen=0`, `receipt: source=committed declared_valid=true`, exit 0 —
`controls/after-c2-receipts.txt`. Tool selftest 17/17.

## Gate

- **Admit — S443, in-toto Attestation Framework, Statement v1**
  (<https://raw.githubusercontent.com/in-toto/attestation/main/spec/v1/statement.md>), opened
  2026-11-03 by the L1 and re-fetched independently by the source seat: HTTP 200, 2,492 bytes,
  sha256 `cbe684a18b812b8b613d9202eb43b2ea24477f91a2ad6ca5be935185a455ebea`, byte-identical across
  both fetches. Located quote (6 words, raw substring at line 37): "Each element MUST have `digest`
  set."; the fuller 22-word paragraph spans lines 36–37 and matches only after line-leading
  blockquote-marker removal followed by whitespace collapse (a naive raw or whitespace-collapsed
  search does not find it — `w1/ScoutSources/verify-output.txt`). It grounds C2's receipt shape:
  an artifact is identified by digest, not by a name or a tally written beside one. **Flip
  condition:** a re-fetch differs in bytes or the sentence is absent at line 37 → reject the row and
  retitle the entry as an unsourced lane-internal note.
- **Admit — the superseding row for `c69_tmp_honour.py`** (Kind demoted `gate` → `instrument`).
  Reason: the row's own Self-test cell records "no self-test mode" (the instrument's `--selftest` is
  an argparse error, exit 2, re-run at base), and E1 forbids a `gate` family without a working
  self-test or a declared differential. **Flip condition:** a later row lands a real `--selftest`
  over isolated fixtures, or names a concrete differential the row's own command performs → the row
  may be re-labelled `gate`.
- **Admit — the superseding row for `c74_registry_gap.py`** recording the eight fixtures it runs
  (`selftest 8/8`, exit 0 at base). Reason: the round-74 row claims five enumerated ids; E3 measured
  5 against an observed total of 8. **Flip condition:** if a future counter defines exactly five
  fixtures, this row is itself wrong and must be superseded again.
- **Reject — "add a `--selftest` to `c69_tmp_honour.py`" as this round's repair.** It is a frozen
  round-69 counter whose three terms are already exercised by committed base and after controls;
  adding a suite rewrites a landed instrument's surface and substitutes scope for the declared
  after-state (a Kind demotion). **Flip condition:** a later round freezes a counter with a real
  `--selftest` over the same three terms, or the operator re-scopes the round-69 counter.
- **Reject — deleting the failing row as a repair.** The deletion control measures
  `files=15 append_only=false met=false`, exit 1 (`controls/ctl-deletion.txt`): the append-only
  conjunct catches it and the E3 finding survives. Deletion is not in this round's repair
  vocabulary; supersession is.
- **Reject — `merge/kake/` assimilation as a whole (§10).** The connector seat re-read every staged
  entry: every locator they cite is unreachable in this lane (`.ufo/waves/round-1[456]/` absent,
  `.ufo/waves/corpus-expansion-1/audit-wave.py` absent) and five cited ids (S371, S401, S407, S412,
  S319) are below the registry tip or unheld, so adopting any entry as written would insert ids
  below S443 or cite a row the reader cannot open. **Flip condition:** the locators are re-pointed at
  surviving bytes and the ids assigned above the tip; then the material is an append to
  `corpus/knowledge/receipt-integrity.md`, not a new file. `Assimilation: none` for this round
  (`w1/ConnectorOverlap.md` §3). No source was opened in the staging repo, and nothing was written
  there.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| A registry row landed with stale draft prose and a gate label the row itself contradicts — the label and the fixture count were written before the instrument existed and were never re-derived from it | `corpus/lessons/round-74-verifier-spotcheck.md` R1 and R2; live cells at `SKILL.md:1426` and `SKILL.md:1432` (base); the same stale count in the counter's docstring `.ufo/waves/round-74/c74_registry_gap.py:25` ("the five contract fixtures f1-f5") against `f1`–`f8` in the same file | none at freeze — the round-70 "table row" rule counted a row's presence, never its claim's executability; this round's C1 E1/E3 and the new `corpus/QUALITY.md` round-75 criterion are the criterion that should have caught it | the frozen counter, shown able to fail on the base (`controls/base-c1-row-truth.txt`), on junk rows that repeat the wrong claims (`controls/ctl-cheapcontent.txt`) and on deletion (`controls/ctl-deletion.txt`); the two superseding rows in `SKILL.md` |
| An instrument was reported green while the counter was executing a *different* file's self-test (the claimed file's path appeared only in a shell comment), and `nondifferential` satisfied a substring test for `differential` | `w1/ReviewerC1.md` held-outs F03/F13/F14/F16/F17 (accepted attacks against the frozen v0, exit 0 `met=true` for states that should be red) | the frozen E1 sentence ("the row's claim re-derives") was implemented as "whatever command the cell names"; amendment 2 A3 makes the command's program the instrument, and A4 word-bounds the differential | the delivered counter's `command_program()` (comment strip + interpreter token) and `\bdifferential\b`, with fixtures f17/f18 in its selftest (22/22 → 29/29 after the seat added its own) |
| A committed capability claim (C2) could be met by a receipt that was never committed, and a declared revision that does not exist was accepted | `w1/ReviewerC2.md` §"Tautology assessment and strongest honest claim": worktree-only receipt green; nonexistent declared revision accepted | amendment 3 A6/A7: the claim's own words are "a **committed** receipt"; the v0 tool read the worktree first and validated nothing about `revision` | `load_receipt()` reads `git cat-file blob <rev>:path` only (`source=uncommitted` is a mismatch), and `receipt_revision_invalid` covers unresolved/unanchored revisions; selftest fixtures for both |

## Sources

- **S443 — in-toto Attestation Framework, Statement v1** (open 2026-11-03, HTTP 200, 2,492 bytes,
  sha256 `cbe684a1…a455ebea`): quote "Each element MUST have `digest` set." at raw line 37. Row
  status `mined`, `used-by corpus/knowledge/instrument-receipts.md`. Prior fleet adjacency: tameshi's
  S281 is the same bytes — this row is new inside kake's S-space only, and the capability row is
  scoped as kake's first registry-bound instrument inventory, not a fleet-first digest binding
  (`w1/ConnectorOverlap.md` §1).
- C1 rests on lane instruments and committed receipts, not on a web source: the predicate is contract
  §C1 (with amendments 1–2), the counter `.ufo/waves/round-75/c75_row_truth.py`, and the controls
  under `.ufo/waves/round-75/controls/`.
- **R4 correction (round-74 closure).** Re-derived from the retained round-74 bodies: the S441
  permission false-negative sentence is at tag-stripped lines **327–329** (21 words), not the
  lesson's `326–329`; the Return-True sentence is at **325–326** (20 words). The 26-word form that
  includes the `On` lead-in exceeds the 25-word cap, which is why the recorded 21-word quote starts
  at `may` on line 327. S441's and S442's own `anchors` cells are exact against the retained text
  (`w1/ScoutSources.md` §2–3).

## Routed

1. **E2 ambiguity (ReviewerC1 F15).** A cell carrying two different `a/b` tallies ("0/3 then 3/3")
  passes on the last pair. Rejecting every multi-pair cell without a frozen interpretation would be
  a predicate change mid-round, so it stays an explicitly named ambiguity for the next round to
  freeze.
2. **`--base` optional in C1's counter.** Without it the counter reports `append_only=true` with no
  evidence (`c75_row_truth.py:454`). The registry row now requires `--base`; the next round should
  either make it mandatory or print `append_only=unchecked`.
3. **The carrier receipt is outside the rewrite watch.** `c58_receipt_rewrites.py` watches
  `.ufo/waves/round-<N>/control(s)/`, so `corpus/knowledge/instrument-receipts.json` can be rewritten
  after commit without an event; its identity is bound only by the `receipt_sha256` line in
  `controls/after-c2-receipts.txt` (ConnectorOverlap §5). Binding the checker itself
  (`tool_sha256` in the receipt) changes the schema for every lane — operator decision.
4. **Superseded docstring.** `.ufo/waves/round-74/c74_registry_gap.py:25` still says "the five
  contract fixtures f1-f5"; the round-75 superseding row corrects the `SKILL.md` cell, not the file.
5. **Host-absolute paths in committed evidence** (SentinelScope §5): seat reports and this round's
  receipts name `/fast/scratch/...` scratch roots, a class the repo already carries 5,939 times;
  whether that belongs in a public-facing repo is an operator decision.
