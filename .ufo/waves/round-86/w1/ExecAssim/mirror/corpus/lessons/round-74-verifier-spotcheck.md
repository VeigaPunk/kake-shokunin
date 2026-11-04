author: hyaku closure (non-author integrator, @m_zfl)

# Round 74 — non-author verification spot-check (kake)

Verified lane-round: **kake r74, attempt 1** (hyaku run 15). Lane base `ced2878a1e77f57afb4ee3baebf1021e5130399b`;
round HEAD (report-cited) `c9fd964354b03b163994519ae43d741b3ee3a81d`; report commit
`7e6de8cb7eb65d325b5eb5ad2034cd0a88946876`.

Method: non-author, read-only. Every measurement below runs over committed bytes (`git show`,
`git cat-file`, `git merge-base`, census) or re-runs the round's own counting commands/selftests on the
committed files. I did not execute the lane's standing gates (harm battery evidence-verified per
PROTOCOL §Gate standard *Closure consequence*), and I edited no lane-authored file: this file is the
closure's only lane write.

Driver digest (copied from `.ufo/watchdog.log`, mutable):
`2026-11-03T20:03:04-03:00 launch kake round=74 pgid=1417452 driver=hyaku-inline attempt=1`;
`2026-11-03T20:36:14-03:00 complete kake round=74; hyaku-inline attempt=1`.

## Step-1 conformance

| Check | Observed | Result |
|---|---|---|
| report path / identity | `git log --format='%an %H %ad %s' -- .ufo/reports/round-74/kake.md` → `kake-shokunin 7e6de8cb7eb65d325b5eb5ad2034cd0a88946876 2026-11-03 20:35:14 -0300 round-74: kake report`; lane receipts commit `c9fd9643` at 20:34:57 → report lands after the work | clean |
| report sections | Work performed, Landed changes, Before → after measurements, Sources & frontier, Trend verdicts, `## SHONEN` — all present in order; `grep -n '^## SHONEN'` → line 148; four `[~]` lines, one per `SHONEN.md` box (4 boxes); no `[x]`, no `[ ]` | clean |
| marker test | real report: five committed lane hashes cited and resolvable, receipts under `.ufo/waves/round-74/`, LOG.md round entry present | real report, not a marker |
| cited commits | `git cat-file -t` = `commit` and `git merge-base --is-ancestor <h> refs/heads/master` exit 0 for `b35dd4d7`, `312b531a`, `30c35842`, `a0500653`, `c9fd9643` | clean |
| lane identity | each of the five commits: `author=kake-shokunin <kake@shokunin.local> committer=kake-shokunin <kake@shokunin.local>` | clean |
| lane state / leftovers | `scripts/hyaku/jj-lane.sh state kake-shokunin` → `branch=master local=c9fd9643… remote=c9fd9643… ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` empty; `git ls-remote origin refs/heads/master` → `c9fd964354b03b163994519ae43d741b3ee3a81d` | clean, pushed |
| prompt | `.ufo/prompts/kake-round-74.md` committed by `kake-shokunin` at `cab140a047b1f1f7a254661378f743b2a76147e6` (20:02:18). Carries §1 MISSION/AXES binding, §2 1–3 claims with the lowest-axis rule, §2b frontier step, §3 L2 floor "at least 8 … in ONE batched AgentSwarm call" (matches `MISSION.md` §L2 concurrency, line 55), §4 report contract with the path, `^## SHONEN` check and the citable-`landed <hash>` rule, §5 commit-then-push + push scope + L0, §6 hyaku addendum (run 15, band 8–16) | full template contract present |
| wave shape | `w1-results.json`: 14 seats, all with outputs — scout 2, executor 4, scribe 2, reviewer 2, critic 1, mutation-tester 1, connector 1, sentinel 1; attack share 4/14 = 28.6 % ≥ 25 %; connector 1 ≤ 2; one v1 wave inside the addendum's 8–16 band; L2 floor (≥8) met | conformant with run-15 addendum |
| fleet-root sweep | no untracked fleet-root file names kake/round-74. One stray untracked `after` (24 B, mtime 20:05, content `== SCORECARD diff base-`) sits at the fleet root; content names no lane/round, so the misroot rule cannot attribute it — left untouched, named here (R6). Untracked `round-57/souji.md`, `round-65/kaidoku.md` belong to other lanes, untouched | no kake misroot |

Conformance defects (status-neutral, named in R1–R4/R6): stale draft prose inside the landed
`SKILL.md` round-74 section; the trend line says "improved locally" (a qualified string, not one of the
four enum values — graded `improved` below); the report calls the standing sweep "unchanged" while its
own after receipt shows one more unannotated `~/projects` cite.

## Claim re-checks

Two claims, distinct axes, causally separable (C1 touches `SKILL.md`; C2 touches the sidecar JSON, the
knowledge entry and the tool). C1 works calibration (score 2, the lane's lowest non-retired axis).

### C1 — calibration, registry completeness (re-measured)

Counting command, run by me in the lane checkout over committed bytes:

```sh
python3 -B .ufo/waves/round-74/c74_registry_gap.py --root . --revision <rev>
```

- base `ced2878a`: `... c73_tmp_v3.py rows=1 ... unregistered=7 own_row=false met=false`, **exit 1**
- tip `c9fd9643`: all eight population lines `rows=1 file_exit=0`, `unregistered=0 own_row=true met=true`, **exit 0**
- mid `30c35842` (the report's measured commit): identical to the tip, **exit 0**

Matches the reported before→after exactly. Do-nothing control: adding no row leaves `unregistered=7` —
reproduced by the base run above. Control-receipt field difference: `controls/base-c1-registry.txt`
predates the `own_row` conjunct (printed `unregistered=7 met=false`, no `own_row`); Amendment 1 A6
declares exactly this, and `w1/ExecC1Counter.md:62` records the base run with `own_row=false`.

Selftest, re-run on the landed counter (scratch under `/fast/scratch/…`, parent created):
`--selftest --work <scratch>` → `selftest 8/8`, exit 0 (`f1`–`f8` present in `FIXTURES`).
**Re-measured**; no committed receipt binds this tally (R5).

Landed changes checked: `git diff --numstat ced2878a c9fd9643 -- SKILL.md` → `32 0`; the eight rows sit
under `### Round 74 gate registry additions` after line 1404 (below the largest sidecar-pinned
`SKILL.md` line, 935); `c72_tmp_v2.py` — the round-73 routed debt — now has its row; Kind labels follow
A4 (`gate (live …)` for the exit-0 counters; `instrument (historical …)` for `c70`, `c71_calibration`,
`c71_tmp`).

### C2 — freshness, sidecar re-observation (re-measured)

Counting command, run by me:

```sh
python3 -B .ufo/waves/round-74/c74_sidecar_reobserve.py --root . --revision <rev>
```

- base `ced2878a`: `entries=174 absent=148 restored=26 absent_present=144 absent_absent=4 absent_unevaluable=0 restored_present=26 restored_absent=0 restored_unevaluable=0 contradictions=144 annotation_findings=0 met=false`, **exit 1**
- tip `c9fd9643`: `entries=174 absent=4 restored=170 absent_present=0 absent_absent=4 absent_unevaluable=0 restored_present=170 restored_absent=0 restored_unevaluable=0 contradictions=0 annotation_findings=0 met=true`, **exit 0**
- mid `30c35842`: identical to the tip, **exit 0**

Independent re-derivation (not the lane's counter): Python over
`git show <rev>:corpus/knowledge/freshness-sidecar.json`; base and tip have the same 174
`(file,line,token)` keys. Base: 148 `absent`, 26 `restored`; of the 148 absent notes **144** tokens exist
on this host and **4** do not (3 distinct: `~/Projects/plazir-15-site` ×2,
`~/Projects/webzites/bin/webzites.mjs`, `~/Projects/webzites/scripts/kimi-surface.mjs`). Tip: 4 `absent`,
170 `restored`, **0** classification mismatches against the live host. All 144 flipped entries carry
`history` equal to the base `{date,kind,note}` **byte-for-byte** (`history mismatch vs base 0`), each new
note carries `2026-11-03`, host class `linux-x86_64` and `stat ok`, and **0** notes match the sweep's
absence vocabulary. `line`, `lineSha256`, `file`, `token` unchanged for all 174 entries (0 position/hash
changes). Blindness control: `controls/base-c2-sweep.txt` never mentions the 144 contradictions
(`grep -cE 'contradict|144'` → 0) — the standing sweep could not see them.

Selftest, re-run on the landed instrument: `c74_sidecar_reobserve.py --selftest` → `selftest 8/8`, exit 0.
Tool, re-run on the landed file: `scripts/sidecar_reobserve.py --selftest --work <existing scratch parent>`
→ `sidecar_reobserve tests=10 failures=0 errors=0 passed=true`, exit 0. **Re-measured**; R5 applies.

Sweep evidence (evidence-verified, not executed by me): `controls/after-harm-sweep-selftest.txt` tail
`selftest: 36/36 passed`, `selftest=0`; `controls/after-harm-sweep-offline.txt` ends `offline=1` with
`VERDICT: DRIFT` and no `Error:` line (binding accepted). Its counts moved: 193 → 195 files, 712 → 714
occurrences, `~/projects` 6 → 7 unannotated cites (27 → 28 cites) because the new
`corpus/lessons/round-74.md:70` names the token unannotated — same single drift token and exit 1, but
"unchanged" is imprecise (R3).

### Harm battery (evidence-verified)

Receipts measured at `a0500653`; the only later commit (`c9fd9643`) adds receipts, so the tree is the
same. c66 exit 0 (`members=28 evaluated=28 mismatches=3 structural=0 agreement=25 scores_held=3/3
met=True`); c70 exit 0 (`pointers=373 dangling=17 annotated=17 unannotated=0 append_only=true
met=true`); c72 exit 0 (`findings=[] met=True`); c73_wave_pointers `met=true`; c73_tmp_v3
`selftest=41/41 findings=[] met=True`. The three new instrument files carry 0 `/tmp` literals
(`git show <tip>:<file> | grep -c '/tmp'` → 0 each). `SCORECARD.md` diff is +37/−0: no score moved.

## Per-axis verdicts

- **calibration — improved.** C1 is re-measured at base and tip with the claim's own counter (7/8
  unregistered → 0/8, exit 1 → 0; `own_row` false → true) and its selftest re-run green (8/8). The
  registry debt the round-73 spot-check routed (`c72_tmp_v2.py`) is closed. Score stays 2 (lane HOLD),
  but the axis's measured evidence improved.
- **freshness — improved.** C2 is re-measured independently: 144 contradicted `absent` notes become
  dated `restored` observations with the prior note preserved byte-for-byte, the 4 genuine absences
  remain `absent`, and the live-host classification has 0 mismatches. The standing sweep keeps its
  existing red drift (not silenced). No admitted entry failed a re-check.
- **operability — unchanged.** No operability surface was reworked; the harm battery is green at the
  same lines and the new instruments are scratch-honest (0 `/tmp` literals). The round added a
  capability row, not a score move.

No owned axis is harmed.

## Discernment spot-check (`corpus/lessons/round-74.md` `## Gate`)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S441 — `os.path.exists` return contract | admit | live `https://docs.python.org/3/library/os.path.html#os.path.exists` (HTTP 200, 90,223 B, sha256 `aa392ce964293f0919e77c51a35e3007bec1c2a1c81504cde98b308e31e479a8`); retained `.ufo/waves/round-74/sources/python-os-path.html` (+ tag-stripped `.txt`) | **agree** | live bytes hash-identical to the retained copy and to the row; the 21-word quote ("may return False if permission … even if the path physically exists") sits at tag-stripped lines 327-329 (lesson says 326-329 — one line early, R4); the row's 21-word `teaches` quote ("Return True … broken symbolic links") sits at 325-326 exactly; ≤25 words; the false-negative class is real and grounds the three-way probe |
| S442 — `os.stat` and the module OSError note | admit | live `https://docs.python.org/3/library/os.html#os.stat` (HTTP 200, 791,358 B, sha256 `4a8bb54c83fab12232926148f2a8cc72868ce62dffb401c547174c70273d287a`); retained `.ufo/waves/round-74/sources/python-os-stat.html` (+ `.txt`) | **agree** | live bytes hash-identical to the retained copy and the row; the 21-word module-note quote sits at lines 237-238 and the 22-word `stat()` quote at 3520-3521; ≤25 words each; grounds the ENOENT/ENOTDIR vs other-`OSError` split implemented in `observe()` |
| "any cell" registration test | reject | `git show ced2878a:SKILL.md`; `grep -n 'c46_matrix.py'` | **agree** | `c46_matrix.py` appears in exactly one table row (`SKILL.md:1198`, the `redirect-expectation-audit` row's Pinned-values cell) although that row gates `scripts/redirect_audit.py`; an any-cell rule therefore credits a witness citation, and one dump row can satisfy every population counter. A1/A2's credited-cell + basename rule is the correct fix |
| Claiming the freshness gate "clean" | reject | `controls/after-harm-sweep-offline.txt` | **agree** | the tip sweep still exits 1 with `DRIFT` on the single `~/projects` token; "evaluable with the same named drift" is the honest grade and is what the round claimed |
| Draft `gate (offline …)` Kind labels for non-green counters | reject | landed `SKILL.md` rows for `c70`, `c71_calibration`, `c71_tmp` | **agree** | A4's label-honesty rule is applied: the three are `instrument (historical …)` and name their measured non-green state; only exit-0 counters carry `gate (live …)` |

SOURCES.md re-open (new row requirement): S441 and S442 are tier A / `docs` / `mined`, opened
2026-11-03, recheck `90d`, `used-by` `corpus/knowledge/sidecar-reobservation.md` (which cites both in
its `source:` trio); the row ids continue the registry after S440 (178 → 180 rows, diff 2 additions /
0 deletions, no duplicate ids). Census:
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → exit 0, `kake ok`,
180 rows (16 W04 duplicate-URL warnings, pre-existing and allowed).

## Trend verdicts (closure re-grade)

- **expansion: unchanged** — one new knowledge entry (`sidecar-reobservation.md`) on ground the lane
  already holds (the sidecar), two curated rows, no frontier move; the capability row is a capability,
  not uncovered-ground expansion.
- **quality: improved** — the 144 stale `absent` notes re-verify to dated `restored` observations with
  byte-exact history and 0 host mismatches; C1's registry gap closes 7 → 0; no gate was weakened to go
  green (the standing sweep keeps its red drift, selftest 36/36). Documentation defects R1–R5 are routed,
  not hidden.
- **discernment: improved** — the Gate records 5 admits and 5 substantive rejects, this non-author
  spot-check agrees on all five sampled decisions with reasons, and the four mined mistakes carry
  evidence plus fixes.

## Routed items (defects the lane must fix next round; status-neutral)

1. **R1 — stale draft prose landed in `SKILL.md`.** The round-74 section's own row says the counter's
   selftest covers "five frozen fixtures: f1 … f5" and "no run exists at this draft", and the verify
   block says "Expected after line, not yet observed since no after-state exists at this draft". The
   landed counter has eight fixtures (f1–f8; my run `selftest 8/8`, exit 0) and the after-state was
   measured at `30c35842`/`a0500653`/`c9fd9643`. Fix with an appended correction that names the
   superseded sentences (the section's own withdrawal discipline forbids an in-place rewrite of the
   filed row).
2. **R2 — `c69_tmp_honour.py` is registered `gate (live)` without a self-test mode.** Its own row says
   `none (no self-test mode; --selftest is an argparse error, exit 2)`, which fails PROTOCOL §Gate
   standard *Self-test* ("Every gate exposes a self-invocation mode over isolated fixtures … with the
   expected values committed"). Either add a real `--selftest` over isolated fixtures or demote the Kind
   label to `probe`/`instrument` and drop the gate framing.
3. **R3 — "sweep unchanged" is imprecise.** The committed after receipt shows 193 → 195 files,
   712 → 714 occurrences and 6 → 7 unannotated `~/projects` cites; the new
   `corpus/lessons/round-74.md:70` names the token unannotated. The drift token and exit 1 are indeed
   unchanged. Next round: annotate that line with the sweep's phrase ("historical record, not an
   executable instruction") or record the count delta honestly. The open L0 `kake | round-69` ruling
   still governs — do not silence the finding.
4. **R4 — S441 quote line range off by one.** Lesson says "tag-stripped text lines 326-329"; the
   permission sentence is at 327-329 (the row anchor's 325-326 is exact for the return-contract
   sentence). Correct in the next round's lesson, appended.
5. **R5 — landed-instrument selftest tallies are unbound.** No committed receipt carries `selftest 8/8`
   (`c74_registry_gap.py`), `selftest 8/8` (`c74_sidecar_reobserve.py`) or `tests=10 passed=true`
   (`scripts/sidecar_reobserve.py`) for the landed bytes; the wave receipts bind only the delivered 5/5
   and 8/8 versions, and the landed files hash differently. I re-ran all three on the landed bytes and
   they pass, but the tallies are true-and-unbound (same class as round-46 R2). Commit selftest receipts
   naming each landed file's sha256 next round.
6. **R6 — fleet-root stray.** Untracked `after` (24 B, mtime 2026-11-03 20:05, content
   `== SCORECARD diff base-`) sits at the fleet root from the round window; content names no lane/round,
   so it cannot be attributed under the misroot rule and was left untouched. The lane's fleet-root
   writes should be confined to its report path.

## Notes for the operator

- Status: **ok**, admitted. Both claims verify (re-measured), no owned axis is harmed, and the
  round-73 routed debt is closed (registry row + sidecar re-observation). Routed items R1–R6 are
  status-neutral documentation/evidence defects.
- The four `SHONEN.md` boxes look fully checkable by a non-author from the repo: box 1 (SKILL registry
  rows + S441/S442), box 2 (LOG.md round-74 entry with end-to-end frozen claims), box 3 (command cells
  and `scripts/sidecar_reobserve.py` CLI), box 4 (`PROVINCE.md` untouched; `ConnOverlap` found no
  sibling overlap). Promotion is operator-owned; no `[x]` was written by this closure.
- No promotions, no mints, no edits to lane-authored files, no MANIFEST edit from this file.
