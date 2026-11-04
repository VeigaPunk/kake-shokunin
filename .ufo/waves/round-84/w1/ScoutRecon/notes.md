# ScoutRecon notes — round 84 w1 (read-only)

Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`. Freeze `f358022f7e1b2f3846be8ceacbe3a7ef22edf4be`.
Base `fe42ad11eb1084ad2ea68d12c5bbb2922a089868` (ancestor of freeze, rc 0). Worktree HEAD
`87cbfd99b677a330c14a68a33f10548f15e6e10c` (`round-84: w1 spec, validated dispatch and ready file`,
descendant of freeze, rc 0). Scratch `/fast/scratch/hyaku/kake-r84/ScoutRecon/` deleted before yield.

## Commands and exit codes (all run from the lane root)

1. `python3 -B .ufo/waves/round-84/c84_defect_queue.py --selftest` → 8 ok lines, `8/8 passed`, rc **0**.
   Fixtures: green-all-closed (0), junk-prose-only (2), mutant-d1-wrong-heading (1),
   mutant-d2-wrong-count (1), mutant-d3-no-connector (1), mutant-d4-wrong-w04 (1),
   mutant-rfc-absent (2), missing-tree-reopens-all (4).
   Committed control `.ufo/waves/round-84/controls/c84-selftest-c1.txt` = same eight lines +
   `selftest_c1_exit=0`.
2. `python3 -B .ufo/waves/round-84/c84_defect_queue.py --root . --revision f358022…` →
   D1 open, D2 open, D3 open, `D4 closed=1 state=1 row=1 receipt_w04=22 derived_w04=22`,
   `C1v1 revision=f358022… items=4 open=3 closed=1 met=false`, rc **1**. Saved at
   `freeze-c1.txt`.
3. `python3 -B .ufo/waves/round-84/c84_policy_values.py --root . --revision f358022… --work <scratch>/c2freeze`
   → `declared=3 surfaces_a=3 surfaces_b=3 receipts_ok=1 real_changed=-1 real_verdict=tool-unevaluable
   ctl_changed=-1 ctl_mismatch=-1 ctl_verdict=tool-unevaluable eq_changed=-1 eq_mismatch=-1
   eq_verdict=tool-unevaluable record_equal=0 determinism=0 tool_offline=0 selftest_ok=0
   counter_selftest_ok=1 met=false`, rc **1**. Saved at `freeze-c2.txt`.
4. `python3 -B .ufo/waves/round-84/c84_policy_values.py --selftest` → `4/4 passed`, rc **0**
   (`canary-parses`, `offline-detects-socket`, `offline-accepts-clean`, `change-regex-rejects-junk`).
5. `grep -Fc` of each of the four headings against
   `.ufo/waves/round-83/w1/ScoutSources/rfc9111.txt` → **2** each, rc 0. Saved at
   `headings-and-d2.txt`.
6. D2 boundary: `len(re.findall(r"\S+", "\n".join(lines[837:844])))` → **66**; `"".join` variant → **66**.
7. `git ls-tree -r --name-only f358022… -- corpus/knowledge | wc -l` → **74** (69 md, 5 json).
   `git grep -il -E 'cache-control|freshness|stale|max-age|etag|policy' f358022… -- corpus/knowledge | wc -l`
   → **48**. `git cat-file -e f358022…:corpus/knowledge/policy-value-classes.md` → rc **128**.
8. Independent census over `f358022…:corpus/SOURCES.md`: 195 registry rows, 194 `S` rows,
   22 `W04` collisions, max id S456. Saved at `census-independent.txt`.
9. `python3 -B .ufo/waves/round-84/c84_defect_queue.py --root . --fleet /home/vgpnk/Projects/shokunin`
   → `error: unrecognized arguments: --fleet …`, usage lists `--root/--revision/--selftest/--work`,
   rc **2**.
10. Prose-row probe (fixture under scratch, no lane write): lesson with the D1 correction line, the
    D2 line, and a closing sentence containing **0** `connector` and **0** `census` tokens; good
    `w1-spec.json`, good `w1-results.json`, the committed `census-before.txt`, the retained RFC and the
    freeze `corpus/SOURCES.md`. Counter → `open=0 closed=4 met=true`, rc **0**. Saved at
    `prose-row-probe2.txt`.

## C1 counter internals that decide the shapes

- Constants: `LESSON=corpus/lessons/round-84.md`, `RFC=.ufo/waves/round-83/w1/ScoutSources/rfc9111.txt`,
  `SPEC=.ufo/waves/round-84/w1-spec.json`, `RESULTS=.ufo/waves/round-84/w1-results.json`,
  `CENSUS=.ufo/waves/round-84/controls/census-before.txt`, `SOURCES=corpus/SOURCES.md`.
- `Tree.read` = `git -C <root> show <rev>:<path>` when `--revision`, else `Path.read_text`; token is
  the revision or the literal `worktree`.
- `item_d1`: `state` = one `[r84-correction` line (after `lstrip()`) that contains all four heading
  literals **and** whose headings all appear in the retained RFC; `row` = any `[r84-correction` line
  containing `round-83.md` and `Gate` while `state`; result = `state and row`.
- `item_d2`: first line matching `D2 count=(\d+) span=838-844 measure=words-full-span`; claim must
  equal `len(re.findall(r"\S+", "\n".join(lines[837:844])))`.
- `item_d3`: `spec["items"]` roles count `connector >= 1` and `results["results"]` has a row with
  `agent == "connector"` and `output.strip()` non-empty. **No lesson/SCORECARD read** despite the
  contract's row conjunct.
- `item_d4`: receipt must contain `census_exit=0` and one `\tok\t…SOURCES.md` line; claimed W04 set =
  sorted `(id, url)` from `\tW04\t` lines via `line.split("\t")[2].split(" duplicate url ")` with
  `" across scopes"` stripped; must equal `census_w04(SOURCES.md)`. **No lesson read** despite the
  contract's row conjunct.
- `--fleet` does not exist in the parser (contract advertises it).

## C2 counter facts relevant to ordering

- `TOOL=scripts/policy_value_class.py`, `RECORD=.ufo/waves/round-84/controls/tool-real-pair.txt`
  (absent at the freeze; the controls dir holds only base-c84-defect-queue, base-c84-policy-values,
  c84-selftest-c1, c84-selftest-c2, census-before, ctl-c84-junk-queue).
- The counter runs the tool with `env={"TMPDIR": str(work), "PATH": "/usr/bin:/bin"}` over
  `REAL_A=.ufo/waves/round-81/capture`, `REAL_B=.ufo/waves/round-82/capture`, `DECLARED=.ufo/waves/round-81/capture-expectations.json`;
  `record_equal` = committed record `rstrip("\n")` equals fresh stdout `rstrip("\n")`.
- `met` conjuncts include `declared==3`, `surfaces_a==surfaces_b==3`, `receipts_ok`,
  `real_changed==0 and real_verdict=="policy-unchanged"`, `ctl_changed==3 and ctl_mismatch==0 and
  ctl_verdict=="policy-changed"`, `eq_changed==1 and eq_mismatch==0 and
  eq_verdict=="policy-rewritten-equivalent"`, `record_equal`, `determinism`, `tool_offline`,
  `selftest_ok`, `counter_selftest_ok`.
- `--work` is created by the caller; without it the counter `mkdtemp(dir=None)` (host TMPDIR) and
  removes it — a seat should always pass an explicit `--work` under its scratch.

## Data-walk evidence (freeze revision)

`corpus/knowledge` = 74 files (69 md, 5 json). 48 match the loose keyword regex. The eleven read as
on-ground are named in the report; anchors used:

- `header-change-classes.md`: §4 heading line 98; line 101 “recorded in its own counter but does not
  flip the verdict by itself”; §2 quote table and §7 limits read.
- `response-header-expectations.md`: line 66 (`does not parse max-age`), lines 110–111
  (`does not parse the policy, does not compare two policies`), limits (`Presence is not policy
  strength`).
- `capture-drift-validators.md`: scope line 5 excludes cache policy; line 216 `expires = fill +
  max-age (600 s)`; §7 erratum.
- `x-robots-tag-header.md`: scope line 6; `x-robots-tag` ∈ `POLICY` (header_change_class.py lines
  54–63).
- `ghp-etag-anatomy.md`, `http-date-grammar.md`, `render-static-sites.md:53`,
  `freshness-sweep.md`/`freshness-pins.json` (schema `kake-freshness-pins-v1`),
  `drift-detection.md`, `sidecar-reobservation.md`/`freshness-sidecar.json` (schema
  `kake-paths-sidecar-v1`), `meta-robots-directives.md`.

## Wave spec at HEAD (for ordering)

13 items: scout 2 (ScoutRecon, ScoutSources), executor 3 (ExecPolicyTool, ExecC1Derive,
ExecControlAudit), scribe 3 (ScribeLesson, ScribeKnowledge, ScribeRegistry), reviewer 2 (ReviewC1,
ReviewC2), critic 1 (CriticClaims), mutation-tester 1 (MutC), connector 1 (ConnectorSibling). So D3's
spec half is satisfied at HEAD; only `w1-results.json` is missing (`ls` rc 2). `reportDir` =
`.ufo/waves/round-84/w1`, `maxLanes` 13.
