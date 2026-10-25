# ReviewerC2Citations — C2 cited w1-filename derivation (round-54 w1)

Scope: how `.ufo/waves/round-54/c54_ops_debt.py` derives "cited" w1 seat-report
filenames from committed `corpus/lessons/round-53.md` +
`corpus/lessons/round-53-verifier-spotcheck.md` versus the seven required names,
and whether the 4-vs-7 distinction is explicit, robust, and non-vacuous.
Read-only review; I ran only `git show`/`git diff` and the named read-only
counter. No installs.

## Answer summary

- **4-vs-7 distinction: numerically explicit, textually misexplained.** The
  contract (C2 do-nothing note) records `uncovered=4` and the code separates
  `NAME_RE`-derived `cited` from hardcoded `REQUIRED_SEAT_NAMES` (7). But the
  contract's parenthetical — the 4 "are the names explicitly cited in the
  lane's round-53 lesson/closure file bytes" — is factually wrong: **all 7 are
  explicitly cited in the lesson bytes**; 4 is the *regex* count, not the
  citation count.
- **Non-vacuous: yes.** Both coverage checks are load-bearing; each
  independently flips the verdict on real revisions (evidence below).
- **Robust: partially.** Three brittleness findings, the worst being that the
  committed repair commit `8e408e0` cannot be validated by the committed
  counter; the fixes exist only as uncommitted working-tree edits.

## Findings (by severity)

### F1 — High: committed state is self-inconsistent; counter fixes uncommitted

At HEAD (`acae1dc` + repair commit `8e408e0` "repair S374 calibration and
settle r53 ops debt"):

- Committed counter (`git show HEAD:c54_ops_debt.py` run in /tmp):
  `registry=absent manifest=incomplete uncovered=4` exit 1.
- Committed settlement `.ufo/waves/round-53/settlement.md` writes rows as
  ``| `ReviewerProvenance.md` | lost | ...`` — backtick-quoted names — but the
  committed `MANIFEST_RE` is
  `^\|\s*([A-Za-z0-9_-]+\.md)\s*\|\s*(?:resolved|lost)\s*\|` (no `` `? ``), so
  `settled=[]` → `manifest=incomplete`.
- Committed `SKILL.md` registry row names the gate `c53-gate-truth` (lacks the
  required token `c53_gate_truth.py`) and its write-scope cell lacks the
  literal token `read-only` → `registry=absent`.
- `git diff HEAD` shows both fixes are **uncommitted working-tree edits**:
  `MANIFEST_RE` gains `` `? `` around the name, and the registry row is renamed
  to `c53_gate_truth.py` with "read-only" added to the scope cell. With the
  working-tree script at HEAD: `registry=absent(committed SKILL.md)
  manifest=present uncovered=0 settled=7` exit 1.

The repair commit therefore lands artifacts its own committed counter scores
as failing; conformity requires an uncommitted edit landing.

### F2 — Medium: contract mischaracterizes where "4" comes from

Verified byte counts at base `68228b2d`:

- Prefixed occurrences (`\.ufo/waves/round-53/w1/<name>.md`): lesson has
  `ReviewerProvenance`, `CriticCrossLane`, `ScoutS329`, `ScoutQuarantine`
  (1 each); spotcheck has `ReviewerProvenance` only. Union = **4**.
- Bare-name citations in the same lesson bytes: line 13 cites
  `ScoutS329.md`, `ScoutS312.md`, `CriticLocators.md` in a comma list (only
  the first prefixed); `ScribeGate.md` appears as
  ``see `ScribeGate.md` `` — bare. Spotcheck §Dead-seat lists all 7 with only
  the first prefixed.

So "the 4 are the names explicitly cited" under-counts explicit citation: 7/7
names are cited, 4/7 in the regex-recognized form. The predicate is still
defensible, but the contract's stated rationale for 4 is wrong — a reviewer
relying on the note would believe only 4 names are cited anywhere in the
files.

### F3 — Medium: `NAME_RE` under-capture makes `uncovered` a partial check

`cited = set(NAME_RE.findall(lesson + spotcheck))` captures only full-path
citations. Consequences:

- A bare-name citation of an *additional* seat report never enters `cited`,
  so `uncovered` cannot flag it; coverage of bare-cited names rides entirely
  on `REQUIRED_SEAT_NAMES` matching the closure's loss list.
- That equality holds today — I verified `REQUIRED_SEAT_NAMES` equals the
  spotcheck "Dead-seat reconciliation" 7-name list and routed-defect #2's
  name list exactly (7/7). But it is asserted by the author, not derived: the
  counter never extracts the 7-name loss list from the spotcheck bytes, so
  drift between prose list and constant would be silent.
- The name class `[A-Za-z0-9_-]+` also cannot represent dotted basenames.

Acceptable for a frozen predicate (constants are frozen by design), but the
code carries no comment distinguishing "cited = regex-derived" from
"required = closure list"; the distinction is discoverable only by reading
the regex against the files.

### F4 — Low: lexical brittleness vs contract prose

- `has_loss_basis` requires literal `40 spawned` AND
  `0 (committed )?seat reports`; contract C2 prose says "40 seats spawned, 0
  committed reports". A contract-faithful "0 committed reports" phrasing
  fails. The committed manifest happens to say "0 committed seat reports" →
  passes.
- `MANIFEST_RE` mandates pipe-table rows `| name | lost |`; contract P2.2
  says "records, per cited seat-report filename, `resolved:` or `lost:` with
  a reason" — a colon-prose form fails the regex.

## Non-vacuous evidence (positive)

- Base receipt reproduces byte-identically: my run at `68228b2d` prints
  `registry=absent manifest=absent uncovered=4`, the same cited list as
  `controls/base-c2-ops-debt.txt`, exit 1.
- Each coverage check is load-bearing on real data: committed-counter@HEAD
  fails via `uncovered=4`/`settled=[]` (MANIFEST_RE), working-tree
  counter@HEAD passes manifest (`uncovered=0`, `settled=7`). A 7-name
  manifest still fails `settled_required` if any required name is missing;
  `uncovered` adds the converse direction for extra prefixed citations.
- Settlement rows name all 7 with `lost` + per-name reasons; `has_loss_basis`
  terms are present in committed bytes.

## Residual risk / verification gaps

- Whether the two uncommitted working-tree fixes land is outside this seat's
  remit; if they land as-is, counter@that-commit should be re-run — expected
  `registry=present manifest=present uncovered=0` exit 0, but the WT
  SKILL.md edit's other cells were not re-verified token-by-token beyond the
  REQUIRED tuple.
- No selftest exercises manifest-format variants (backtick, colon-prose) or
  bare-name citation forms; `--selftest` exists for C1 only.
- This wave is read-only and the lane tree is owned by other seats; if the WT
  edits are an in-flight sibling repair, F1 resolves on their commit — flag,
  don't treat as final.
