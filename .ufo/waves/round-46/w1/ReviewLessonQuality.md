# ReviewLessonQuality — round-46 attack on the lesson-mistakes draft

Seat: `kake-r46.ReviewLessonQuality` (reviewer, axis **calibration**; evidence lenses:
freshness of the pointers, operability of the proposed checks). Read-only over the lane;
writes only this report and scratch under
`/fast/scratch/hyaku/kake-r46/ReviewLessonQuality/`. No installs or upgrades (none needed;
pacman paused host-wide). No subagent dispatch. No commit/push.

## Named attack

Each mined mistake row must carry (1) a **class**, (2) an **evidence pointer** that resolves
at committed bytes, (3) a **captured-by** naming the criterion/rule that should have caught
it, and (4) a **fix shown able to fail** by a named check with a visible red state.
A candidate-only row is acceptable **only** with that label.

**Verdict: NOT PASS / BLOCKED-ON-ARTIFACT — the target does not exist.**
`.ufo/waves/round-46/drafts/lesson-mistakes.md` was absent at every read (01:59–02:02 local),
and the producing seat's scratch `/fast/scratch/hyaku/kake-r46/ScribeLessonMistakes/` is empty.
Per the item's own rule ("if a needed artifact is absent, record the dependency as a finding
and return"), the attack cannot certify an absent draft. What follows is (a) the decisive
absence evidence, (b) a mechanically runnable acceptance test with positive/negative controls,
and (c) pre-verified traps that any r46 lesson row will hit — all red states are reproduced
from committed bytes now, so the L1 can gate the draft the moment it lands.

## Decisive commands and verbatim output

### 1. Target absent (HIGH-1)

```text
$ ls -la .ufo/waves/round-46/drafts/
total 4
drwxr-xr-x 1 vgpnk vgpnk   40 Oct 24 02:00 .
drwxr-xr-x 1 vgpnk vgpnk 180 Oct 24 01:59 ..
-rw-r--r-- 1 vgpnk vgpnk 1072 Oct 24 02:00 quality-criterion.md

$ ls -la /fast/scratch/hyaku/kake-r46/ScribeLessonMistakes/
total 4
drwxr-xr-x  2 vgpnk vgpnk  6 Oct 24 01:59 .
drwxr-xr-x 49 vgpnk vgpnk 4096 Oct 24 02:00 ..

$ python3 -B /fast/scratch/hyaku/kake-r46/ReviewLessonQuality/lesson_rows.py \
    . .ufo/waves/round-46/drafts/lesson-mistakes.md
FileNotFoundError: [Errno 2] No such file or directory:
'.ufo/waves/round-46/drafts/lesson-mistakes.md'
```

The only drafts-directory artifact at the time of return is `quality-criterion.md`
(ExecQualityCriterion's, reviewed as evidence below), not the assigned lesson draft.

### 2. Acceptance test, with controls that prove it can fail (HIGH-3 mechanism)

Checker: `/fast/scratch/hyaku/kake-r46/ReviewLessonQuality/lesson_rows.py`. It scopes to a
`## Mistakes` section, then per numbered row checks class / evidence / captured-by / fix /
able-to-fail, marks placeholder language as `able-to-fail-not-shown`, demands a repo pointer
that exists with in-range lines, and demands the candidate label when the word "candidate"
appears.

```text
$ python3 -B .../lesson_rows.py . corpus/lessons/round-45.md          # positive control
== corpus/lessons/round-45.md: rows=2 problems=0
exit=0

$ python3 -B .../lesson_rows.py . .ufo/waves/round-45/drafts/mistakes.md   # negative control
== .ufo/waves/round-45/drafts/mistakes.md: rows=2 problems=1
   row 14 (line 22): missing=able-to-fail-not-shown(placeholder)
     unreachable=.ufo/waves/round-45/fixtures/{counter-error,tool-absent,stale-planted}/=MISSING;
     .ufo/waves/round-45/c45_matrix.py:235-235=LINE-OUT-OF-RANGE(file has 220);
     corpus/lessons/round-44.md:53-68=LINE-OUT-OF-RANGE(file has 66)
exit=1
```

The negative control is the *r45 draft of the same item* — i.e. the check demonstrably fires
on real lesson-row defects, not a synthetic fixture. Two of its three unreachable pointers are
genuine drifts, re-verified independently:

```text
$ awk 'END{print NR}' .ufo/waves/round-45/c45_matrix.py
220
$ grep -n 'stage == "before"' .ufo/waves/round-45/c45_matrix.py
81:    stale = "stale-planted" if stage == "before" else AFTER_STALE_FIXTURE
82:    stale_leg = "stale-planted" if stage == "before" else "stale-backdate"
178:    driver = V1_DRIVER if args.stage == "before" else V2_DRIVER
179:    plant = args.stage == "before"
207:    if args.stage == "before":

$ awk 'END{print NR}' corpus/lessons/round-44.md
66
```

`c45_matrix.py:235` does not exist (file has 220 lines; the cited branch is at :207), and
`round-44.md:53-68` over-runs the 66-line file. These are calibration defects of exactly the
class this item attacks: the r45 draft's `able-to-fail` row 14 was additionally an admitted
placeholder ("The matrix stages have not been run by this seat … so this row's able-to-fail
evidence is a placeholder"). The landed version corrected both the placeholder and the
pointers — that is the bar the r46 draft must meet **before** landing.

### 3. Line pointers drift even in the landed r45 lesson (MEDIUM-2)

```text
$ grep -n '^def _selftest_cohort' .ufo/waves/round-45/c45_audit.py
235:def _selftest_cohort():
$ sha256sum .ufo/waves/round-45/c45_audit.py
9b824d958d1494471f45ad84d6ae38ce600518311b1fb95af51b1098aac8a400
```

`corpus/lessons/round-45.md:23-25` cites "`_selftest_cohort :223`" while the final committed
bytes define it at **:235** (the draft was written against `f3c3171b…`, the file was hardened
to `9b824d95…` afterwards). Function-name-plus-sha binding survives hardening; a bare line
number does not. Any r46 row must either bind instrument citations to sha256 observed at
landing or re-resolve every line pointer at the tip.

### 4. The receipt-identity red state is **not** `0 → 1` (HIGH-2)

Frozen C2 counting sentence: `grep -c '^- .*receipt.*\(path\|sha256\)' corpus/QUALITY.md`
`0 → 1`. Measured at three revisions and with an ERE cross-check:

```text
$ git show 7cdbaefd:corpus/QUALITY.md | grep -c '^- .*receipt.*\(path\|sha256\)'
2
$ git show bd86ee8:corpus/QUALITY.md | grep -c '^- .*receipt.*\(path\|sha256\)'
2
$ git show ded938d:corpus/QUALITY.md | grep -c '^- .*receipt.*\(path\|sha256\)'
2
$ grep -c '^- .*receipt.*\(path\|sha256\)' corpus/QUALITY.md
2
$ grep -Ec '^- .*receipt.*(path|sha256)' corpus/QUALITY.md
2
```

The two base matches are `corpus/QUALITY.md:128` (disposable runner path) and
`corpus/QUALITY.md:951`, an existing criterion: "**(l) A post-measurement receipt pins the
measured tool bytes** (revision and sha256, re-derivable from the revision)". Consequences for
the lesson draft, both binding:

- A row that uses "the criterion went **0 → 1**" as its able-to-fail red state is presenting a
  red state that does not exist at base. That is a fabricated measurement and must be
  rejected, not softened.
- The honest demonstration is either `2 → 3` for one appended criterion row, or the unique
  label the sibling draft chose: `grep -c '^- \*\*Receipt identity for filed counts'
  corpus/QUALITY.md` → measured `0` now (verified below), `1` after append.
- The frozen sentence and the unique-label command are **different commands**. A lesson row
  may record the discrepancy (the sibling `quality-criterion.md` already does, correctly:
  "The broader proposed expression … also matches older criteria, so it is not a reliable
  0 → 1 check"), but it may not present the unique-label count as the frozen count.

```text
$ grep -c '^- \*\*Receipt identity for filed counts' corpus/QUALITY.md
0
```

### 5. sha256-digest prefix is a live false-positive at committed bytes (HIGH-3)

The hard case named in the round contract exists in the frozen population:

```text
$ grep -rn 'd7e79ba1' SCORECARD.md LOG.md corpus | head
SCORECARD.md:724:`be2a1287…c53e`, gate sha256 `d7e79ba1…9d48`, runner sha256 `3c167895…2a1c`).
corpus/lessons/round-30-verifier-spotcheck.md:53:  - The gate is `d7e79ba102ff…` at base and `dbfade45e593…` from `71c6bfa`
corpus/lessons/round-30-verifier-spotcheck.md:61:  - `c1-before-0356681.json`: revision `03566813…`, gate `d7e79ba1…`,
```

`SCORECARD.md:724` is inside the frozen population `{SCORECARD.md, LOG.md}` and carries the
digest `d7e79ba1…9d48` labelled *sha256*. A lesson row whose "able to fail" demonstration does
not exhibit **this exact line** as a classification control has not shown the exclusion does
any work: a linter that flags every `[0-9a-f]{8}` token would also turn this line red, and a
row that only tests ordinary commit tokens cannot distinguish the two.

### 6. Foreign pins do not resolve in-lane; no committed r46 ledger exists (MEDIUM-1)

```text
$ for h in 964f443e 7c243a1d a8f1e2b; do git rev-parse --verify "$h^{commit}"; done
fatal: Needed a single revision
fatal: Needed a single revision
fatal: Needed a single revision
$ find . -path ./.git -prune -o -iname '*ledger*' -print | grep -v node_modules | head
./scripts/fixtures/citing-set/01-single-literal-clean/ledger.json
... (fixtures only)
```

So a lesson row may claim in-lane resolution only for lane commits; the foreign pins named in
the contract (`964f443e`, Pages `7c243a1d`, deploy `a8f1e2b`) must be described as
**adjudicated in the ledger**, and no committed r46 adjudication ledger exists yet (only
`scripts/fixtures/citing-set/*/ledger.json` fixture ledgers). A row that says the gate
"resolves every lane commit citation" without that scope split is false at committed bytes,
and a row whose able-to-fail cites a ledger receipt will cite a path that does not exist —
exactly the placeholder class the negative control above flags.

### 7. Dead short-hash fact used by any citation-hygiene row (verified)

```text
$ git rev-parse --verify e545525
e54552553eaff4d7033dc2df299300fc056f4a0d
$ git rev-parse --verify e5455253
fatal: Needed a single revision
$ git rev-parse --verify 7cdbaefd
7cdbaefd3ecbbc8814eca1f013fcee101a6157b0
```

The 7-char token resolves, the 8-char token does not — the row's evidence pointer to the dead
token must be the *citation site* (`SCORECARD.md:3867`, `LOG.md:1766`) and the red state must
be the linter's own output at base, not a re-statement of the routed-defect ledger. A row that
quotes the ledger as its evidence without running the gate is candidate-only at best.

## Acceptance rubric the landed draft will be judged by

1. Every row has all four fields, each with substantive content (not headings alone).
2. Every evidence pointer resolves at the landing revision: path exists; `:N` and `:N-M` are
   within the file; shorthand `:N` resolves against the nearest full path in the same row.
3. `Able to fail` names a runnable command, its red state, and its green state; any placeholder
   or unrun stage → **UNSHOWN**, not pass (r45 precedent: the draft's entry 14 was corrected
   for exactly this).
4. Candidate rows carry an explicit `candidate only` label; the label is mandatory even when
   the row is otherwise well-evidenced.
5. No row re-declares a frozen claim as met or upgrades a bounded green measurement; the
   receipt-identity row must not rest on `0 → 1`.
6. The sha256-digest exclusion row must use `SCORECARD.md:724` as a negative control.

The checker implements 1–2 and 4 mechanically and 3 by placeholder detection; 5 and 6 remain
reviewer judgment.

## Residual risk and verification gaps

- The verdict on content quality is **unrun**, not passed: the target was absent. When
  `drafts/lesson-mistakes.md` lands it must be re-attacked, at minimum with
  `python3 -B .../lesson_rows.py . .ufo/waves/round-46/drafts/lesson-mistakes.md` plus the
  semantic checks 5–6.
- I did not review `drafts/quality-criterion.md` beyond its bearing on lesson rows; its
  evidence question (0 → 1 vs unique label) is the one that propagates.
- The checker's pointer regex only resolves full repo-relative backticked paths; shorthand
  pointers are checked manually, so a green run is necessary, not sufficient.
- No tooling installed or upgraded; `python3` (3.14) and `git` were already present.

## Files written

1. `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-46/w1/ReviewLessonQuality.md`
   — this report.
2. `/fast/scratch/hyaku/kake-r46/ReviewLessonQuality/lesson_rows.py` — the rubric checker
   (controls above).
3. `/fast/scratch/hyaku/kake-r46/ReviewLessonQuality/` — scratch dir (created empty otherwise).
