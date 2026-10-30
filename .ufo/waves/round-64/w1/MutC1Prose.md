# MutC1Prose — mutation test of the C1 prose bindings (round-64)

Seat: MutC1Prose (leaf, no subagents). Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Measured T0 `4c8295fa5e3b628f1fdf3840299ae415c01849fb`; lane HEAD `cc8add1f`; base `1a481315`.

## Verdict

- The counter's **quote-correction** (K), **criterion** (Q) and **located/recipe/class** components resisted every mutant asked for. The lesson **Gate** (G) is the weak point: its checks are substring tests, so a one-word suffix edit to the verdict span and a single-occurrence `collapsed-only`→`raw-substring` swap both stay green.
- Of the 14 mutants, **10 are KILLED** (named component `0`, `met=false`, exit 1, no other component moved except `unresolved` and `met` as a consequence). **4 SURVIVE** (named component still `1`, `met=true`, exit 0): G3, G4b, G6a, Q3x. Details in §3.
- Q3x is the one that matters most against the contract: the criterion sentence is still in the Round-62 section, but only inside an HTML comment, so it is not rendered. That is a marker-only green reproduced on the prose layer. Under the contract's kill-rule wording ("any wave attack reproduces a marker-only … green, C1 is `unprovable`") this is a breach to adjudicate. I report it; I do not rule on the claim.

## 1. Method (reproducible)

- Clone of the lane made into scratch: `git clone -q --no-hardlinks --no-checkout file:///home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r64/MutC1Prose/clone`, then `git -C <clone> checkout -q --detach 4c8295fa5e3b628f1fdf3840299ae415c01849fb`. `git -C <clone> rev-parse --show-toplevel` asserted equal to the clone dir before every mutation. The lane was read-only throughout.
- Frozen counter copied byte-identically to scratch and sha-checked: `5489eb2f3ac498e0383d841c677f036231fbf6933717d8da447f3193ff088adf` (matches contract). Driver runs it unmodified:
  `python3 -B /fast/scratch/hyaku/kake-r64/MutC1Prose/bin/c64_calibration.py --root <clone> --revision <mutant-rev>`, with `TMPDIR` set to the scratch `tmp/`.
- Each variant = one commit on top of T0 in the clone (`git reset -q --hard T0`, edit the file, `git add -A`, `git commit --allow-empty`). The driver applies each edit with an exact-count assertion (e.g. "found 2, want 1" aborts), so every variant is verified to be the edit it names. Diffs saved and reviewed (§4).
- Driver: `/fast/scratch/hyaku/kake-r64/MutC1Prose/driver.py` (scratch only; deleted after this report).

Baseline checks:
- Frozen counter at T0, lane root, read-only: `revision=4c8295fa5e3b628f1fdf3840299ae415c01849fb disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true`, exit 0 — matches `controls/after-c1.txt`.
- C0 control (T0 tree re-committed unchanged, mutant rev `9affce57bde0`): identical line, exit 0, `met=true`. The harness is faithful.

Tools: none installed or upgraded. Used `python3` 3.14.8 and `git` 2.56.0 already on the host. No pacman, no uv, no PATH writes.

## 2. Matrix

Target components: `lesson_gate` for G, `criterion` for Q, `quote_correction` for K. Required outcome for each mutant: named component `0`, `met=false`, exit 1.

| id | mutation (exact edit) | mutant rev | exit | named = value | met | verdict |
|---|---|---|---|---|---|---|
| C0 | control, no edit | 9affce57bde0 | 0 | — (all components as T0) | true | control-ok |
| G1 | Gate span: `substantive`→`substantial` (in "not substantive evidence…") | a68205f0a9aa | 1 | lesson_gate=0 | false | KILLED |
| G2 | Gate span: `generic`→`general` | 95b0c5b8692c | 1 | lesson_gate=0 | false | KILLED |
| G3 | Gate span: `expectation`→`expectations` (one-word suffix) | e6b78884143d | 0 | lesson_gate=1 | true | **SURVIVED** |
| G4 | Gate: `collapsed-only`→`raw-substring`, all 2 Gate occurrences, span kept | 078abf167a76 | 1 | lesson_gate=0 | false | KILLED |
| G4b | Gate: same swap, first occurrence only (extra) | 864bf9d1215c | 0 | lesson_gate=1 | true | **SURVIVED** |
| G5 | Gate: `c64_calibration.py`→`c63_calibration.py` (its one Gate occurrence) | f62817f6314f | 1 | lesson_gate=0 | false | KILLED |
| G6a | Gate: `author-side` label removed, `self-assessment` kept | a5c734bbd9f4 | 0 | lesson_gate=1 | true | **SURVIVED** |
| G6b | Gate: `author-side` and `self-assessment` both removed | e6c57164919e | 1 | lesson_gate=0 | false | KILLED |
| Q1 | QUALITY: criterion sentence moved out of `## Round-62 criteria` into `## Round-63 criteria` | b8eca28534f3 | 1 | criterion=0 | false | KILLED |
| Q2 | QUALITY: criterion sentence moved out of Round-62 to a new EOF section | 22d7e5cdfb18 | 1 | criterion=0 | false | KILLED |
| Q3x | QUALITY (extra): sentence kept in Round-62 but wrapped in `<!-- … -->` | df4651679585 | 0 | criterion=1 | true | **SURVIVED** |
| K1 | Knowledge: frozen quote moved outside `[r63-correction]` (after a `## ` heading at EOF) | 94c74abfaeb1 | 1 | quote_correction=0 | false | KILLED |
| K2 | Knowledge: frozen quote moved into the `[r62-correction]` block | 564917d09e37 | 1 | quote_correction=0 | false | KILLED |
| K3 | Knowledge (contrast): one word changed inside the quote, still in r63 block | 767eb459f874 | 1 | quote_correction=0 | false | KILLED |

Counts: 14 mutants + 1 control. KILLED 10, SURVIVED 4 (G3, G4b, G6a, Q3x).

Other components per row: every KILLED row changed only its named component plus the consequences the counter defines (`unresolved` 0→1 when `lesson_gate` drops, and `met` true→false). Survivors changed nothing. Raw lines are in `/fast/scratch/…/out/*.out`, deleted with the scratch tree; the exact printed lines are reproduced in §5.

## 3. Survivors — what passes and why

**G3 — one-word suffix on the verdict span passes.** The Gate check is `SPOT_VERDICT_SPAN in gate` (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py:256`), a bare substring test. Gate line 95 becomes `…not substantive evidence for a response-header expectations")`: the verdict span is still a substring, so `lesson_gate=1`. The contract and lesson say the Gate "quotes the spot-check's actual verdict span"; the counter accepts a span with an appended character. Severity: medium — the "block-level binding" claim is substring-level. [INFERENCE, untested] The same substring semantics apply to the knowledge check (`FROZEN_QUOTE in qblock`, line 248), so an appended-character quote would also pass there; I did not build that variant.

**G4b — contradictory Gate prose still greens.** Replacing one of the two `collapsed-only` occurrences (Gate line 58, `re-derived \`collapsed-only\` from the recipe output`, left as `raw-substring`; line 99 `…class` still says `collapsed-only`) leaves `"collapsed-only" in gate` true (line 257). The counter's `class_match` is derived from the recipe and is unaffected, so the prose contradiction passes unseen. Severity: low on the derived class, but a self-contradictory Gate is a prose-layer green.

**G6a — one of two author-side labels removed.** The check is `"author-side" in gate or "self-assessment" in gate` (line 259), a disjunction. Removing only `author-side` (Gate line 100) leaves `self-assessment` (line 101), so the label survives in another word. Severity: low — the semantic label is still there; the disjunction is the weakness. G6b (both removed) is killed.

**Q3x — criterion sentence inert in an HTML comment (marker-only green).** `CRITERION_SENTENCE in r62` (`c64_calibration.py:250`) is a raw substring test on the Round-62 section text, which does not parse Markdown. The sentence wrapped as `<!-- **A quoted span must substantively support the proposition attributed to its source.** --> A section lead-in…` (QUALITY line 1412) is not rendered, yet `criterion=1`. This is the contract's marker-only green, reproduced on the prose layer. Severity: high relative to the kill rule — see §0.

## 4. Mutation diffs (exact, T0→mutant)

- G1 `round-64.md` L95: `substantive evidence` → `substantial evidence`.
- G2 `round-64.md` L95: `generic lead-in` → `general lead-in`.
- G3 `round-64.md` L95: `…response-header expectation")` → `…response-header expectations")`.
- G4 `round-64.md` L58 and L99 `collapsed-only` → `raw-substring` (Gate only).
- G4b `round-64.md` L58 only: `collapsed-only` → `raw-substring` (L99 unchanged).
- G5 `round-64.md` L54 `c64_calibration.py` → `c63_calibration.py`.
- G6a `round-64.md` L100: `are author-side` → `are` (`self-assessment` L101 unchanged).
- G6b `round-64.md` L100–101: `are author-side\nself-assessment;` → `are not independently checked;`.
- Q1 `QUALITY.md` L1412: sentence bolded removed from the Round-62 bullet; new bullet `- **A quoted span must …source.**` inserted under `## Round-63 criteria` (L1414).
- Q2 `QUALITY.md`: same removal; appended `## Relocated criterion` section with the bullet at EOF.
- Q3x `QUALITY.md` L1412: `**A quoted span …source.**` → `<!-- **A quoted span …source.** -->`.
- K1 `response-header-expectations.md` L230: `> "The \`X-Content-Type-Options\` … request."` removed from `[r63-correction]` (L224 block); appended `## Relocated quote` + the same blockquote at EOF.
- K2 same removal; blockquote inserted before `## Round-63 correction` (L222), inside the `[r62-correction]` block (L218–221).
- K3 quote text: `header can be used` → `headers can be used` inside the r63 block (L230).

## 5. Exact counter output (representative)

```
C0  rev=9affce57bde0  exit=0  revision=9affce57bde0… disagreements=1 pins=1 … lesson_gate=1 source_row=1 unresolved=0 met=true
G1  rev=a68205f0a9aa  exit=1  … lesson_gate=0 source_row=1 unresolved=1 met=false
G3  rev=e6b78884143d  exit=0  … lesson_gate=1 source_row=1 unresolved=0 met=true
G4b rev=864bf9d1215c  exit=0  … lesson_gate=1 source_row=1 unresolved=0 met=true
G6a rev=a5c734bbd9f4  exit=0  … lesson_gate=1 source_row=1 unresolved=0 met=true
Q1  rev=b8eca28534f3  exit=1  … quote_correction=1 criterion=0 lesson_gate=1 … met=false
Q3x rev=df4651679585  exit=0  … quote_correction=1 criterion=1 lesson_gate=1 … met=true
K1  rev=94c74abfaeb1  exit=1  … quote_correction=0 criterion=1 lesson_gate=1 … met=false
```
(Full lines for every row are in the matrix above's components; each run had `pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 source_row=1` and `stderr` empty.)

## 6. Recommendations (for the integrator, not applied)

1. Gate binding: compare the verdict span as a whole, delimited-line match (for example the full `reason` cell of the `S432 / Fetch` row in `corpus/lessons/round-61-verifier-spotcheck.md`, line 33, exactly), rather than a substring test. This kills G3 and the same-class quote suffix risk.
2. Gate class binding: require exactly one `collapsed-only` class assertion in the Gate and no `raw-substring` assertion for S432 (kills G4b).
3. Criterion binding: test against rendered text (strip `<!-- … -->` before the check), so Q3x cannot green. Under the contract's kill rule as written, Q3x is a marker-only green and should be adjudicated before C1 is credited.
4. G6a: accept only the labelled form the lesson actually uses, or require both labels (low priority).

## 7. Scope notes

- Nothing was written in the lane except this report file. The lane's tracked tree and HEAD (`cc8add1f`) are unchanged; untracked entries under `.ufo/waves/round-64/` are other seats' artifacts.
- No mutating git command ran in the lane. All commits are in the scratch clone, which is deleted after this report.
- Selftest of the counter (`controls/selftest-c1.txt`) was not re-run; this seat did not need it.
