# Round 73 — frozen claim contract (kake, attempt 1)

Frozen before any seat of wave `w1` ran. Base revision: `c1f3d8d4ed9470ecbaaf3353952a374b079e68cc`
(lane master at round open; `jj-lane.sh state` local = remote = base). Predicates, counters, controls and kill
rules below are the ones the closure re-derives; they are not restated later.

## Pre-freeze diagnosis (disclosed)

Before freezing, the L1 ran the frozen counters at base once to locate defects (c70 pointer counter, c72
counter, c66 gate-status counter, offline freshness sweep). Their base outputs are committed as controls in this
freeze commit (`controls/`). No claim was chosen from a green/red that a counter could not express; the choice
rests on: (a) round-72 closure routed defects (dead receipt pointers; the c72 registry row; the c72 residual holes),
and (b) the offline sweep exit 2 at base, which is the freshness gate unable to evaluate. The c70 pointer counter
exits 0 at base while two round-72 self-assessment pointers are dead; §C1 shows why.

## Claims

Axes: calibration (score 2, HOLD — the lowest non-retired axis, so C1 is the lowest-axis claim), operability
(score 10, HOLD), freshness (score 10, HOLD). Three distinct axes; causally separable (each predicate reads only its
own file set; C3 touches `freshness-sidecar.json` only; C1 touches `LOG.md`/`SCORECARD.md` only; C2 touches
`.ufo/waves/round-73/` and one appended `SKILL.md` registry row beyond line 935).

### C1 — calibration: round-72 receipt pointers resolve or carry a dated correction

- Before (base `c1f3d8d4`): wave-relative receipt pointers `controls/c1-tip.txt` and `controls/c2-tip.txt` cited in
  the round-72 LOG entry and round-72 SCORECARD rows name files that do not exist under
  `.ufo/waves/round-72/`. Counter: `controls/c1-pointer-base-c70.txt` shows c70 `unannotated=0 … met=true` exit 0,
  because c70 parses only repo-rooted SCORECARD pointers (blind spot). The new counter below reads the same two
  pointers and reports them dead.
- Counter (new, frozen by this commit): `.ufo/waves/round-73/c73_wave_pointers.py --root <lane> --revision <rev>`.
  It reads `LOG.md` section `## Round 72` and SCORECARD lines whose first cell is `72`, extracts every token
  `controls/…` or `sources/…` or `w1/…`, resolves it under `.ufo/waves/round-72/`, and classifies each dead token
  as **annotated** iff an appended correction line at the end of the same file (after the base line count) names
  the superseded token and a corrected repo path that resolves under `.ufo/waves/round-72/`.
- Predicate (one sentence, same in plan, counter, receipt): **C1 met iff `unannotated == 0` and `dead ≥ 2`
  (both dead tokens still named, annotated by a resolving correction) and the append-only conjunct holds
  (every base line of LOG.md and SCORECARD.md survives as a prefix line)**, at the measured tip.
- Before: `dead=2 unannotated=2 met=False exit 1` at base (expected; measured in c1 receipts at the tip build).
- Do-nothing control: base revision. A control that appends a bare errata line naming the token but no resolving
  path must stay red (fixture in the counter selftest).
- Kill rule: any unannotated dead round-72 pointer at the tip → C1 not met, reported as unmet.
- Score: calibration HOLD 2 (no scalar move claimed; evidence row carries the counter receipt).

### C2 — operability: c73 counter closes the four routed c72 holes

- Before (base `c1f3d8d4`): `c72_tmp_v2.py --lane . --revision c1f3d8d4` exits 0 `met=True`
  (`controls/c2-c72-base.txt`). The round-72 closure (`corpus/lessons/round-72-verifier-spotcheck.md` routed items
  1–3) and the round-72 attack seats demonstrated these holes against c72: (H1) `${TMPDIR:-/tmp}` fallback repoint
  escapes both regexes; (H2) command verbs outside the 17-word list (`rsync`, `rm`, `cd … &&`, env prefix
  `TMPDIR=… python3`, `sudo` prefix, double-backtick spans) take the phrase-only annotation and pass; (H3) a
  symlinked SKILL.md (mode 120000) reads as its link text; (H4) the `PHRASE` constant is not pinned: a truncated
  phrase (`not an executable`, `historical record`) passes.
- Frozen attack corpus: `.ufo/waves/round-73/attack-corpus.txt` (written by the executor seat `ExecC2Counter` into
  `w1/` and promoted by the integrator before the counting command runs). Each line: `<class> | <expected> | <line>`
  where `<class>` ∈ {`attack`, `legit`} and `<expected>` ∈ {`finding`, `clean`}. Attack lines carry H1–H4 shapes;
  legit lines are the lane's own dated-absence annotations.
- Counter (new, frozen by this commit at the path below once the executor delivers it): `.ufo/waves/round-73/c73_tmp_v3.py`.
  Command: `python3 -B .ufo/waves/round-73/c73_tmp_v3.py --selftest` and `python3 -B .ufo/waves/round-73/c73_tmp_v3.py --lane <clone> --revision <rev> --corpus .ufo/waves/round-73/attack-corpus.txt`.
- Predicate (one sentence): **C2 met iff `c73 --selftest` exits 0 with the full case count passing, every `attack`
  line in the corpus is a finding, every `legit` line is clean, `c73 --revision c1f3d8d4` and `--revision <tip>`
  both exit 0 with `findings=[]`, and the SKILL.md gate registry gains exactly one row naming `c73_tmp_v3.py`.**
- Do-nothing control: `c72_tmp_v2.py` run on the same corpus (its `line_findings` function, the frozen counter's
  code, not edited) — reported as `c72_accepts=k of A attack lines`; the claim requires `k ≥ 1`
  (the holes are real; if c72 already rejects every attack line the claim is void and the round reports that).
- Before → after: c72 accepts `k` of A attack lines (k ≥ 1; receipt `controls/c2-c72-corpus.txt`) → c73 accepts 0 of
  A attack lines (receipt `controls/c2-c73-corpus.txt`).
- Kill rule: any attack line the c73 counter accepts, any legit line it rejects, selftest not full, or base/tip
  non-zero → C2 not met.
- Score: operability HOLD 10.
- Sourced claim (§2b.4): the H1 class rests on S440 (GNU Bash manual, Shell Parameter Expansion: `${parameter:-word}`
  substitutes `word` when `parameter` is unset or null — so `${TMPDIR:-/tmp}` falls back to `/tmp`). The row is
  opened this round (`sources/bash-param.html`, sha256 `6b0800fd…a13c8e3`, `sources/receipts.txt`).

### C3 — freshness: offline sweep evaluable at the tip

- Before (base `c1f3d8d4`): `node scripts/freshness-sweep.mjs --offline` exits 2, stderr
  `paths sidecar binding invalid: corpus/SOURCES.md:140` (`controls/c3-sweep-base.txt`). Cause: round-71 commit
  `84dcc841` appended a `used-by` cell to the S132 row on line 140, which changed the line bound by the sidecar entry
  (`corpus/knowledge/freshness-sidecar.json`, file `corpus/SOURCES.md`, line 140, token
  `~/Projects/shokunin/kama-shokunin/corpus/knowledge/self-assessment-at-writing.md`, kind `absent`). The entry's
  `lineSha256` is the only field that no longer matches; the token, the kind, the date and the note are unchanged.
- Change: re-pin that single entry's `lineSha256` to the sha256 of the current line 140 (computed by the sweep's own
  method: the file split on `\n`, sha256 of the line's UTF-8 bytes). Nothing else in the sidecar changes.
- Predicate (one sentence): **C3 met iff `node scripts/freshness-sweep.mjs --offline` at the tip exits 0 or 1 with no
  `Error:` line on stderr, and `freshness-sweep --selftest` (with isolated HOME and KAKE_SELFTEST_DIR) passes, and
  the sidecar diff against base changes exactly one entry's `lineSha256`.**
- Do-nothing control: base revision sweep exit 2 (`controls/c3-sweep-base.txt`).
- Kill rule: exit 2 at tip, any `Error:`, selftest red, or a sidecar diff touching anything other than that one
  `lineSha256` → C3 not met. Exit 1 at tip is reported with its named findings; the claim then means
  *evaluable with named drift*, not *clean*.
- Score: freshness HOLD 10.

## Harm checks (all must hold at the tip; any red is reported as harm)

- c66 gate-status: `agreement` at tip ≥ 25 (base `agreement=25 mismatches=3 evaluated=28`, `controls/c0-gate-status-base-c66.txt`).
- c70 pointer counter exit 0 at tip (base exit 0; `controls/c1-pointer-base-c70.txt`).
- c72 counter exit 0 at tip (base exit 0; `controls/c2-c72-base.txt`).
- Scores unchanged in SCORECARD (calibration 2, operability 10, freshness 10).

## Frontier and mistakes (round lesson)

- Sourced claim: C2 rests on S440 (opened this round).
- Mistakes to mine (see `corpus/lessons/round-73.md` after landing): M1 — wave-relative receipt pointers outside
  c70's parse grammar (captured-by: none; c70 blind spot); M2 — round-71 SCORECARD E13 recorded the sidecar failure as
  "pre-existing host state" when round-71's own edit (`84dcc841`) caused it (captured-by: the round-64 criterion
  "a round that edits a sidecar-pinned file re-runs the standing §paths sweep" was not applied at the landed tip).
- Census (before, measured round start): `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
  exit 0 (`corpus/SOURCES.md` 177 rows; W04 duplicate-URL warnings pre-existing).

## Counter delivery (frozen rule)

The predicates, the attack corpus (`attack-corpus.txt`, committed in this freeze), the base controls and the kill
rules above are frozen here. The counter source files named in C1 and C2 (`c73_wave_pointers.py`, `c73_tmp_v3.py`)
do not exist at freeze: wave `w1` delivers them, and the integrator commits each one (with its selftest output) before
any after-state measurement. A delivered counter that changes a frozen predicate, the corpus or a control is a
predicate change and voids the claim it touches.
