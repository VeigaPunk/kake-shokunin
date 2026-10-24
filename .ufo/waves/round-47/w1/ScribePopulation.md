# ScribePopulation — round 47 / w1 / axis: freshness

**Target:** recount the adjudication ledger's table *data rows only*; verify
20 total = 12 `LOG.md` + 8 `SCORECARD.md`; check the append-only R3 correction
in `LOG.md` and `SCORECARD.md` names those units accurately.

**Verdict:** the population claim and both R3 corrections are **true on measured
bytes** (20 data rows, split 12/8). Two precision defects found, neither of which
changes the count: (a) the C2 gate's R3 predicate is a substring test that is
blind to the 12/8 split and never reads `SCORECARD.md`; (b) `LOG.md:1796-1797`
says the SCORECARD correction lives in SCORECARD's *round-46 section*, but it is
appended inside SCORECARD's *Round 47 — declared claims* section. No claim here
is a pass-by-intent; every number below is a command output.

Lane repo: `/home/vgpnk/Projects/shokunin/kake-shokunin`, HEAD
`766f4610b64f35a0f402b37eb1d8be2d4d634c0f`, frozen base
`cd42e3c310ba442e89dde638ba6401adaefaf3e8`. Read-only on all lane bytes.

## 1. Recount — 20 data rows, 12 LOG.md + 8 SCORECARD.md

Ledger: `corpus/quality/citation-adjudications.md` (sha256
`e75bc3a746539d86651f4b31f578480702fc325cbe1e1555cd76aa38d5058669`, 5043
bytes, 54 lines). Table structure: header at line 8, separator at line 9, data
rows at lines **10–29**.

| Check | Command | Observed |
|---|---|---|
| total data rows | `grep -c '^| \`' corpus/quality/citation-adjudications.md` | `20` |
| LOG.md rows | `grep -c '^| \`[^\`]*\` \| LOG\.md \|' …` | `12` |
| SCORECARD.md rows | `grep -c '^| \`[^\`]*\` \| SCORECARD\.md \|' …` | `8` |
| per-file tally | `grep '^| \`' … \| awk -F'\|' '{gsub(/^ +\| +$/,"",$3); c[$3]++} END{…}'` | `SCORECARD.md 8`, `LOG.md 12` |
| header/separator | `grep -n '^|' … \| grep -v '^[0-9]*:| \`'` | only `8:| Token \| File \| Class \| Reason \|` and `9\|---\|---\|---\|---\|` |

Independent structural parse (Python, local read): 22 pipe lines = 1 header + 1
separator + **20 data rows**; 0 malformed rows (all 20 have 4 non-empty cells in
Token/File/Class/Reason order); no cell contains an embedded `|`.
Unit detail: **18 unique tokens**, **20 unique (token,file) pairs** (tokens
`e5455253` and `dcef39b5` each carry one row per file), 30 adjudicated
occurrences. The occurrence figure was re-measured at HEAD, not copied:
`python3 -B scripts/citation_lint.py --root . --json -` → exit 0, violations 0,
adjudicated 30, pairs 20, by file `{'LOG.md': 12, 'SCORECARD.md': 8}`. The
correction's unit word "data rows" is the correct unit; "20 unique tokens" would
be 18 and is *not* what the ledger or the gate counts.

Third count, via the production parser (not my reimplementation):

```
citation_lint.load_adjudications(root, "corpus/quality/citation-adjudications.md", "HEAD")
→ production parser adjudication keys: 20
→ by file: Counter({'LOG.md': 12, 'SCORECARD.md': 8})
→ duplicate (token,file) keys collapsed: 0
```

Fourth, receipt-grounded count from the r46 gate receipt
`.ufo/waves/round-46/verification/c2-after-ee43e66.json`:

```
occurrences: 30  pairs: 20  by file: {'SCORECARD.md': 8, 'LOG.md': 12}
ledger pairs == receipt pairs: True   (ledger-only: set(), receipt-only: set())
```

So the ledger's row split is exactly the pair split the r46 gate consumed.
Class column tally (context only): 10 `external-repo commit`, 7
`sandbox-control commit`, 2 `quoted-dead-token`, 1 `external-repo pin`.

## 2. R3 correction text vs. the measured units

`LOG.md:1793-1797` (verbatim):

```
- [r47-correction R3] The adjudication ledger's population is **20 data rows**
  (12 naming LOG.md + 8 naming SCORECARD.md), not the "12 rows" written in this
  entry and the round-46 report; the correction is append-only per the
  round-20 post-review ruling. Same correction appended to SCORECARD.md's
  round-46 section.
```

`SCORECARD.md:3962-3964` (verbatim):

```
[r47-correction R3] The round-46 section's "adjudication ledger … (12 rows)"
above is misstated: the ledger holds 20 data rows (12 naming LOG.md + 8
SCORECARD.md); corrected append-only here and in LOG.md.
```

Against the recount: total `20` ✓, `12` LOG ✓, `8` SCORECARD ✓, `12+8=20` ✓.
Both files name the same corrected unit and split. The "12 rows" statements the
corrections point at exist and are unedited: `LOG.md:1780` ("`…(12 rows, each
target re-verified non-resolving)`") and `SCORECARD.md:3912` ("`…(12 rows, every
target re-verified non-resolving in the lane repo at round 46)`").

## 3. Append-only — verified byte-level, not asserted

- `git diff --numstat cd42e3c…..HEAD -- corpus/quality/citation-adjudications.md LOG.md SCORECARD.md`
  → `101 0 LOG.md`, `77 0 SCORECARD.md`, `25 0 corpus/quality/citation-adjudications.md`
  (added/deleted; **zero deleted lines** anywhere in the interval).
- `git diff cd42e3c…..HEAD -- LOG.md SCORECARD.md | grep -c '^-[^-]'` → `0`;
  hunks are `@@ -1790,3 +1790,104 @@` and `@@ -3915,3 +3915,80 @@` — three
  context lines then pure additions.
- Ledger: base has 29 lines, HEAD 54; `diff <(git show base:ledger) <(head -29 ledger)`
  → empty (`IDENTICAL-1..29`); the only difference is 25 appended lines
  (blank line 30 + the `## Round-47 corrections` block, lines 31-54).
  Base sha256 `432a36a2f9a6a20e6083ea223b63aa3c337e1fee4a9a938a08f8f61e57269394`
  → HEAD `e75bc3a7…d5058669`.
- The ruling the corrections cite is real and in-lane: `corpus/QUALITY.md:31`
  `## Post-review append-only ruling — round 20`, `corpus/QUALITY.md:20`
  (stripped-diff criterion), `corpus/lessons/round-20-verifier-spotcheck.md:17`
  ("every correction now a pure addition"), `corpus/lessons/round-24.md:21`.

## 4. Findings (adversarial)

**F1 — PASS: population and split are accurate.** Measured four ways (grep,
structural parse, production parser, r46 receipt pair set); all agree on 20 =
12 LOG + 8 SCORECARD. No falsification of the R3 claim itself.

**F2 — PASS: append-only is mechanical, not prose-only.** Base→HEAD shows 0
deleted lines in all three files; the ledger prefix is byte-identical for all 29
base lines; the original "12 rows" lines survive at `LOG.md:1780` and
`SCORECARD.md:3912` exactly as the ruling requires.

**F3 — GATE-COVERAGE GAP (instrumentation, claim still true).** The frozen
predicate says the fix is "an R3 correction line naming the 20 data rows
(12 LOG.md + 8 SCORECARD.md) in LOG.md" (`SCORECARD.md:3947-3948`), but the
counter implements it as a literal-substring over LOG lines only:

```
c47_routed_count.py:134
    r3_fixed = any("R3" in line and "20 data rows" in line for line in log_lines)
```

Scratch mutation control (repo built under
`/fast/scratch/hyaku/kake-r47/ScribePopulation/mut`, local `git init`, no push,
lane checkout untouched):

| variant | counter output | counter exit |
|---|---|---|
| faithful copy of HEAD bytes | `outstanding=0/4 C2_MET` | 0 |
| LOG R3 line mutated to `(3 naming LOG.md + 17 naming SCORECARD.md)` | `outstanding=0/4 C2_MET` | 0 |
| LOG R3 line mutated to `**19 data rows**` | `outstanding=1/4 C2_NOT_MET` | 1 |

(The harness shell returned 1 on the last control because the counter exits 1;
that is the expected NOT_MET exit, not a harness error.) So the gate
anchors the *literal total and label* but cannot detect a false split, and it
never opens `SCORECARD.md` (the script `git show`s only `LOG.md`, the ledger, and
the receipt tree). The committed after-receipt
`.ufo/waves/round-47/verification/c2-after-714e707.json` records only
`{"fixed": {"R3": true, …}, "outstanding": 0}` — it carries **no counted
population**, so the 20/12/8 numbers are committed nowhere as machine-checked
data. The claim is saved by my independent recount, not by the gate.

**F4 — MINOR FALSE CROSS-REFERENCE in the LOG correction.** `LOG.md:1796-1797`
says "Same correction appended to SCORECARD.md's round-46 section." Structurally
the SCORECARD section `## Round 46 — measured verdicts` spans lines 3897-3918;
the correction sits at `SCORECARD.md:3962-3964`, i.e. inside
`## Round 47 — declared claims` (3919-3967), 44 lines after the round-46 section
ends and immediately after the frozen C2 declaration. The sentence is wrong
about placement (content is right). Same defect class as R3 — a filed statement
about the record that does not match the record — at lower severity; it does not
affect the 20/12/8 numbers or append-only status. `SCORECARD.md:3962`'s own
wording ("The round-46 section's … *above* is misstated … corrected append-only
here") is accurate.

**F5 — PROVENANCE LIMIT, not a defect.** `LOG.md:1795` also points at "the
round-46 report". No lane file is that report; the only in-lane support is a
residual review quoting it: `.ufo/waves/round-46/residual/ReviewReceiptIdentity.md:42`
("`SCORECARD.md:3912` and `LOG.md:1780` and fleet report lines 13, 40"). I did
not inspect the fleet-root report (lane-only bound), so that half of the pointer
is **unverified by me**.

**F6 — no remaining unqualified "12 rows" claim in round-47 material.** Every
occurrence in the touched material is either the two preserved r46 originals
(`LOG.md:1780`, `SCORECARD.md:3912` — each immediately rebutted by an appended
correction) or an explicit quotation/qualification (`LOG.md:1794`,
`SCORECARD.md:3942`, `SCORECARD.md:3962`, `corpus/lessons/round-47.md:7`,
`corpus/lessons/round-46-verifier-spotcheck.md:69`,
`c47_routed_count.py:8`). Other `12 rows` hits in the tree are unrelated tables
(rounds 23/35/45) or task text under `.ufo/waves/round-4{5,6,7}/`.

## 5. Conflicts to preserve for the canonical judge (verbatim)

1. Frozen predicate, `SCORECARD.md:3947-3948`: "an R3 correction line naming the
   20 data rows (12 LOG.md + 8 SCORECARD.md) in LOG.md" **vs.**
   `c47_routed_count.py:134`: `any("R3" in line and "20 data rows" in line for line in log_lines)`.
2. `LOG.md:1796-1797`: "Same correction appended to SCORECARD.md's round-46
   section." **vs.** measured placement: correction at `SCORECARD.md:3962-3964`,
   section `## Round 47 — declared claims` (3919-3967); round-46 section is
   3897-3918.

## 6. Gates

- Ran: `python3 -B .ufo/waves/round-47/c47_routed_count.py --root . --revision <rev>`
  at `cd42e3c` → `outstanding=4/4 C2_NOT_MET` exit 1; at `714e707` → `0/4
  C2_MET` exit 0; at `766f461` → `0/4 C2_MET` exit 0.
- Ran: `citation_lint.load_adjudications` on HEAD (in-process import, read-only)
  → 20 keys, 12/8 split.
- Ran: `python3 -B scripts/citation_lint.py --root . --json -` → exit 0,
  0 violations, 30 adjudicated occurrences, 20 pairs, 12 LOG / 8 SCORECARD.
- NOT run: `citation_lint.py --selftest`, `freshness-sweep`, any jj/git mutation
  in the lane, any network check. Not needed for this seat and not claimed.

## 7. Touched surfaces / limits

- Wrote only this report. Lane production files, `.jj`, lane Git index/refs,
  fleet repo, sibling repos, `.ufo/state/`, `.ufo/watchdog.log` untouched. No
  mutating jj/git command in the lane checkout.
- Scratch only: `/fast/scratch/hyaku/kake-r47/ScribePopulation/mut` (disposable
  local git repo for the F3 mutation control; never pushed; contains copies of
  `LOG.md`, the ledger and the one rerun receipt from HEAD).
- Lane `git status --porcelain` observed before my writes:
  `M .ufo/waves/round-47/w1/swarm-registry.json` and
  `?? .ufo/waves/round-46/residual/` — pre-existing, not mine.
- Tool installs: none (no pacman, no uv, no npx).
- Artifacts referenced: `corpus/quality/citation-adjudications.md`,
  `.ufo/waves/round-46/verification/c2-after-ee43e66.json`,
  `.ufo/waves/round-47/verification/c2-{before-cd42e3c,after-714e707}.json`,
  `.ufo/waves/round-47/c47_routed_count.py`, `LOG.md`, `SCORECARD.md`,
  `corpus/QUALITY.md`, `corpus/lessons/round-47.md`.
