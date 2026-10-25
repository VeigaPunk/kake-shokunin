# Round 43 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_flash)

Round: kake lane round 43. Report `.ufo/reports/round-43/kake.md` (fleet) at
`d0cbc9d49dae90f05035df601b83f28f2a32ea7b`, committed by `kake-shokunin <kake@shokunin.local>`
2026-10-23 17:38:10 -0300, after lane tip `a377c5d0b98e7d5f28171bc47096e9592ac989a5`
(17:36:56 -0300) and therefore lands last. Freeze commit `b49cba9ca7f15bb0dfaae33b638afa7cb4c793ee`
(parent `61046fcffa23898cd93b7a5a0af4906dac9926c9`, the round base).

This file is the outside check `LEARNING.md` requires ("Discernment is checked from outside"): it
verifies the round's declared verdicts, does not relabel them, edits no lane file, and writes no
`[x]` into `SHONEN.md`.

## 1. Step-1 conformance (PROTOCOL §Round-robin closure step 1)

| Check | Command | Observed |
|---|---|---|
| report landed by the lane identity | `git log --format='%an %H' -- .ufo/reports/round-43/kake.md` | `kake-shokunin d0cbc9d49…` — lane identity, committed after the lane tip (lands last) |
| lane clean, pushed, no round work left | `scripts/hyaku/jj-lane.sh state …/kake-shokunin`; `git -C … status --porcelain`; `git -C … ls-remote origin refs/heads/master` | `branch=master local=a377c5d0… remote=a377c5d0… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `a377c5d0…` |
| every cited lane commit exists and is an ancestor | `git merge-base --is-ancestor <hash> master` for `61046fc`, `b49cba9c`, `eddbbf6`, `7c07079`, `a377c5d0`, `020bc457`, `1ef7a0e9`, `5949e66ffe` | all present, all ancestors (`yes` ×8) |
| `SHONEN` heading, one line per box | report `## SHONEN` | 4 lines: `[~] [ ] [~] [~]`, each with a resolvable pointer; no `[x]`; `SHONEN.md` still the canonical 4-box seed |
| dispatch prompt carries the contract | `.ufo/prompts/kake-round-43.md` (tracked, committed `e93ab55`) | §1 mission/axes binding, §2 claims 1–3 + admission, §2b frontier step, §3 L2 floor (≥8, one batched call), §4 report contract (report path, commit-hash rule, `SHONEN` heading, marker rule), §5 commit-then-push / push scope / L0, §6 hyaku addendum + write scope. No L2 route map is quoted, so there is no MISSION bucket to mismatch |
| dispatch evidence (mutable log; digest copied) | `.ufo/watchdog.log` | `2026-10-23T16:05:04-03:00 launch kake round=43 pgid=2199380 driver=hyaku-inline attempt=1`. Completion evidence is the landed report + lane tip: the live log carries no `complete kake round=43` line at closure and `.ufo/state/kake.round` reads `16` (driver runtime, operator-side; see routed defect 10) |
| marker vs report | report content | Real report: work performed, evidence pointers, landed changes tied to commits, checkable citations, `Sources & frontier`, trend verdicts, `SHONEN`. Status `ok` |

Status: **ok** (not a marker). Contract defects found are status-neutral and listed in §8.

## 2. C1 — operability, declared NOT MET: verified

The declaration under test is the negative one: *the build meets counter v4's predicate, but frozen
kill rule (1) fires, so C1 is NOT MET*. Verification targeted the kill-rule evidence.

**(a) Predicate and kill rules were frozen before any seat scored.**

- Predicate text at `SCORECARD.md:3199` @ `b49cba9c` is byte-identical to `PREDICATE`
  (`c43_count_v4.py:78-80`) and to every receipt's `predicate` field (`build-1.json` checked;
  identical in this closure's re-score receipts).
- Kill rules and control classes: `SCORECARD.md:3230-3242` @ `b49cba9c` ("(1) after the wave opens,
  any live-seat control receipt meeting v4 means C1 is NOT MET").
- Counter bytes: `sha256sum .ufo/waves/round-43/c43_count_v4.py` →
  `1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab`, equal to
  `verification/freeze/counter-v4.sha256` and to the blob at `b49cba9c`.
- Chronology: freeze commit 16:44:33 -0300; wave spec `eddbbf6` 16:51:44; wave dispatched
  19:51Z (16:51 -0300). Earliest artifact under `/fast/scratch/hyaku/kake-r43` is 16:53. No seat
  artifact predates the freeze.

**(b) Build verification evidence (3 fresh-seed met receipts, r42 controls red, timing held).**

```
build-1.json  met=true  equal 11/11  seed 9325990526163   T1 1.005 T2 1.201 T3 1.334 T4 1.266 T5 1.105
build-2.json  met=true  equal 11/11  seed 265206435053987 T1 1.009 T2 1.250 T3 1.318 T4 1.252 T5 1.144
build-3.json  met=true  equal 11/11  seed 269853680553917 T1 1.004 T2 1.213 T3 1.327 T4 1.211 T5 1.215
r42ctl-M8-port-five-digits  met=false 9/11   r42ctl-v1_casefold  met=false 9/11
r42ctl-v2_prefix32          met=false 7/11   r42ctl-v4_hosttable met=false 9/11
r42ctl-junk_constant        met=false 0/11   ref41-base (do-nothing) met=false T1 4.207 T5 7.047
```

These are the corrected numbers the report quotes in Before → after; the freeze section's
4.272 / 8.679 / 1.002–1.020 are the discarded pre-T2-fix values and are superseded by SCORECARD
correction 1. Timing channel: `CtlTiming` receipts `forge/fork/cache` are all `met=false`,
`equalRuns 11/11`, ratios T1 4.13–4.20 and T5 8.57–10.26 — no attack lowered measured CPU.

**(c) Independent re-scores (this closure, fresh `os.urandom` seeds, frozen counter read-only).**

```
python3 -B .ufo/waves/round-43/c43_count_v4.py --root . --tool-file <tool> \
  --label closure-<name> --out /fast/scratch/hyaku/kake-r43/closure/<name>.json

V7_prefix_cache45 (CtlHeadTail)              met=true  11/11  T1 1.048 T2 1.214 T3 1.441 T4 1.060 T5 1.135
v7_memo_value_lower_nonascii (CtlCaseMemo)   met=true  11/11  T1 1.117 T2 1.250 T3 1.481 T4 1.296 T5 1.293
A_expanded46_fixed (CtlHostTable)            met=true  11/11  T1 1.065 T2 1.201 T3 1.504 T4 1.356 T5 1.145
controls-r42/v2_prefix32 (round-42 control)  met=false  8/11  exit 1
```

**(d) Witnesses reproduced by this closure (the "judges URL values differently" half of the kill
rule), round-41 tool at sha256 `50287ac6…dde7d` vs the control on the same manifest:**

```
head/tail: two locs sharing the first 45 code points, second defective just after
  ref41.py              -> {"findings":[{"code":"loc_not_absolute","entry":2}]} exit 1
  V7_prefix_cache45.py  -> {"verdict":"clean","findings":[]} exit 0
case fold (seat fixture witness/w2_fold_nonascii, locs .../Éseg/x and .../éseg/x)
  ref41.py                          -> loc_out_of_scope entry 2, exit 1
  v7_memo_value_lower_nonascii.py   -> clean, exit 0
```

Three live-seat control classes meet v4 while diverging in CLI output from the round-41 tool, so
the frozen kill rule (1) fires. **C1 NOT MET verified as declared** — the receipts are the claim's
evidence, and they hold.

**Tally spot-check (27).** HeadTail ×5 (V1,V2,V4,V7,V8), PortLen ×3 (v1,v4,v5), CaseMemo ×4
(v3,v4,v7,v8), Repeat ×5 (band memos + deep/late), HostTable ×3 (A,B,F), PortValue ×2, PrefixCache
×1 (p48), build mutants ×4 (Scope m4/m5, Scheme M5, Port m6) = 27; each seat table shows the met
receipt, its seeds and its witness. One seat (`ExecRerunControls`, scoped to the four committed r42
controls) wrote "No live-seat control meets v4" inside its own scope; the lane did not adopt that
overreach.

## 3. C2 — freshness, declared verified with bounds: verified

- Before receipt `verification/freeze/sweep-before.txt` + `.exit`: exit 1, "2 unannotated miss ·
  2 NOT in pins.pathsMissSet", citing `corpus/lessons/round-29.md:102` and `round-33.md:43`.
- Base state re-derived at `61046fc`: the annotation rows are absent
  (`git show 61046fc:corpus/lessons/round-29.md | grep -c "absent-path annotation (r43 re-census"`
  → 0; same for round-33) while the citing rows sit at `:102` / `:43`; `pathsMissSet` holds 63
  entries without either token.
- After, re-run by this closure at `a377c5d0`:
  `node scripts/freshness-sweep.mjs --section=paths` → exit 0,
  `§paths 102 files · 623 occurrences · 101 unique tokens`,
  `citation base: 101 targets · missSet 65 · files 102`, `set-delta miss: no new miss`,
  `VERDICT: OK (exit 0)`.
- Annotations landed at `round-29.md:104` and `round-33.md:45`, inside each Mistakes table, each
  naming the absent fleet path, the removal event and the surviving lane copy; the fleet paths are
  absent and the lane copies exist. `pathsMissSet` 63 → 65 at `b49cba9c` with exactly the two tokens.
- Movement census: the insertion adds two lines. Blob slices match:
  `round-29.md:118-122@61046fc` md5 `6eb7f8fb040c23ce1d85fb3360f17500` == `:120-124@b49cba9c`;
  `:124-132@61046fc` md5 `380d4298fe987db531ec2ac45ff9bb76` == `:126-134@b49cba9c`. Superseding dated
  EOF notes are present in `.ufo/waves/round-30/w2/CriticC1Scope.md` and
  `.ufo/waves/round-34/w1/CriticFrontierNovelty.md`.
- Bounds (as declared): the claim is `--section=paths` only. The full sweep is red at §armed
  (PQ-2 / sitemap / plazir gates), pre-existing at the base and outside this claim; this closure did
  not re-run §armed.

## 4. Registry arithmetic (routed repair 1): verified

Independent census (`git show <rev>:corpus/SOURCES.md`, CORPUS §Census commands):

```
1ef7a0e9    rows=119  mined=92  queued=8  rejected=19
5949e66ffe  rows=128  mined=99  queued=8  rejected=21   -> +9 rows, mined +7, queued +0, rejected +2
61046fc     rows=128  mined=99  queued=8  rejected=21
b49cba9c    rows=130  mined=101 queued=8  rejected=21   -> freeze +2 rows, mined +2
```

This matches the correction (the r42 "128 → 131; mined +1" is false) and the freeze transition.
Checker receipts agree (`registry-count-r42-check.txt` `ok:false`, `…-r43-check.txt` `ok:true`,
`…-r43-freeze-check.txt` `ok:true`). The checker is a smoke aid, not a gate (SCORECARD correction 5);
the numbers above rest on the census commands.

## 5. Axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| operability | `unchanged` | C1 declared NOT MET; the build and counter are verified, but no axis move landed and the score row is untouched |
| freshness | `improved` | C2: §paths exit 1→0 re-derived at HEAD, pins 63→65, annotations and movement census verified |
| depth | `unchanged` | not a kake-owned axis; no change claimed |
| coverage | `unchanged` | not owned |
| calibration | `unchanged` | not owned |
| adjacency | `unchanged` | not owned; S129/S130 are named imports with located quotes |

No axis harmed: `git diff --diff-filter=D --name-only 61046fc a377c5d0` is empty; `SKILL.md`,
`PROVINCE.md` and `corpus/QUALITY.md` are untouched; the SCORECARD settle diff
(`b49cba9c..a377c5d0`, +108 lines) changes no axis row; every corpus change is an addition except
`freshness-pins.json` (+4/−2, the two miss-set entries).

## 6. Discernment spot-check (LEARNING.md)

| Gate decision | Re-opened | Result |
|---|---|---|
| S129 admit | `tameshi-shokunin/.ufo/waves/round-33/w1/CtlDoNothing.md` §Verdict | **agree** — "The do-nothing shortcut never reaches `predicate_pass=true`" is verbatim at lines 10–11, in the section's first paragraph; the `kill=0/18 accept=8/8 predicate_pass=False` line is there too, and the method import (score control classes against a frozen counter before any build is judged) is real |
| S130 admit | `kama-shokunin/corpus/knowledge/self-assessment-at-writing.md` §"Checking self-assessment statements at writing" | **agree** — "A mismatch therefore records a calibration error present when the statement was written" is verbatim at line 7, in the section's first paragraph; the statement-class parenthetical sits in paragraph 2 (paragraph 3 under file-wide blank-block counting), exactly as the appended erratum states |
| reject sample | the round's Gate screened two candidates and rejected none ("Rejections: none this round"), so the reject was sampled from the standing registry: **S101 WHATWG URL Standard (tier A, `rejected`)** | **agree** — fetched `https://url.spec.whatwg.org/` 2026-10-23: sha256 `08cb42a9a8575dab006676378c846fdd8a72d06897c27929aa51eaf099656be4` equals the row's retained hash; its Goals text says the standard aligns RFC 3986/3987 "and obsolete[s] the RFCs in the process" (spaces and illegal code points "not entirely shared, or defined"), and `robots_audit.py:104` / `sitemap_audit.py:22` import `urllib.parse` — the stated rejection reason holds |

Rows: S129's `teaches` quote is 6 words, S130's 13 (both ≤25), both `status: mined`, `used-by` paths
resolve (`corpus/lessons/round-43.md`, `SCORECARD.md`, `corpus/knowledge/claim-count-derivation.md`).
`sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → exit 0 (`kake ok`; W04
duplicate-URL warnings only). Manual census: 130 rows, 0 malformed, no duplicate ids, no enum/tier
violations, no missing used-by paths.

Erratum: landed in `corpus/lessons/round-43.md` ("Gate locator erratum") and is correct under
section-prose counting. The SOURCES anchor cells still carry the old locator — see §8.7.

Limitation recorded: with zero rejects in this round's Gate, no reject sample can come from that
gate itself (the round-28 routed-defect-4 class recurs); the outside reject above is the standing
registry's.

## 7. Trend verdicts

- **expansion: improved** — one new admitted knowledge entry
  (`corpus/knowledge/claim-count-derivation.md`, `source:` cites mined S130) on ground the coverage
  map did not hold, with its new `Claim-count derivation (r43)` coverage row. Count:
  `git ls-tree --name-only <rev> corpus/knowledge/ | grep -c '\.md$'` → 30 at `61046fc`, 31 at
  `a377c5d0`. The lane self-graded `unchanged` (it read expansion as capability-table entry only);
  CORPUS §SOURCES rule 4's observable is satisfied, so the closure records the broader verdict.
- **quality: improved** — counter v4 closes all four round-42 control classes (seats red
  9/11, 9/11, 7/11, 9/11; this closure's `v2_prefix32` re-run 8/11 exit 1); the build receipts are
  met ×3; the timing channel held ×3; S126/S127 were re-opened (S127 byte-equal); the stale r42
  counts are superseded by re-derived numbers; no admitted entry failed a re-check. Bounds are the
  lane's own disclosure (counter generator defects, §armed debt).
- **discernment: improved** — 27 meeting controls were reported and not relabelled (the round turned
  its own build's C1 to NOT MET), Mistake 9 was disclosed against the lane's interest, and the r42
  arithmetic was corrected from committed bytes; this outside check agrees on both admits and the
  sampled reject. Blemish: the L1 re-score tally overstates its receipts (§8.1).

## 8. Routed defects (status-neutral; none changes a verdict)

1. **Re-score tally overstates its receipts.** Report Before → after and `SCORECARD.md:3393` say
   "L1 re-scored 18 of 27"; `verification/l1-rescores/` holds **14** re-score receipts (11 in
   `exits.txt` + 3 in `exits2.txt`, 14 distinct `toolSha256`), and no other committed set carries
   the remaining four. The 27 tally itself verifies. Third instance this round of the
   stale-numbers class mined as Mistakes 7/9. Route to r44.
2. **Dead seat cited as evidence.** The report's freeze-order line cites `w1/RevengerCounterLineage`;
   the settle line lists that seat dead with "no report on disk", and no such file exists. Pointer
   does not resolve.
3. **Commit attribution.** The report attributes `corpus/README.md`'s index row to the freeze
   commit; `git diff --stat 61046fc b49cba9c -- corpus/` shows it landed in `a377c5d0` (settle).
4. **Wave composition drift.** `SCORECARD.md` (settle section) and the LOG "Round 43 correction"
   entry say "47 reports, 15 dead, 4 live-at-settle"; the settle line and `w1/`'s 50 `.md` files say
   50 reports, 15 dead, 1 live.
5. **LOG keeps superseded ratios.** `LOG.md:1659-1661` quotes do-nothing T1 4.27 / T5 8.68 and build
   T1 1.00–1.02 / T5 1.13–1.18; the committed receipts are 4.207 / 7.047 and 1.004–1.009 /
   1.105–1.215. Corrections swept SCORECARD and the report but not LOG; append-only LOG needs a
   superseding line.
6. **Role-mix arithmetic.** "build 16 — 14 executor, 3 scribe, 1 connector" sums to 18; the registry
   totals 66 seats (14 executor, 3 scribe, 1 connector, 48 attack) with two scribes counted in the
   attack mix as scribe-falsify.
7. **SOURCES anchor locators.** S129/S130 anchors still say "paragraphs two to four" / "paragraph 2"
   while the quotes are in paragraph 1; the lesson erratum is the only correction, and the SOURCES
   contract's correction path is a superseding row.
8. **Learning-path duty.** Mistakes 7, 9, 10 and 11 carry `captured-by: none`, but
   `corpus/QUALITY.md` gained no criterion citing the lesson this round (`git log -2 -- corpus/QUALITY.md`
   still ends at round 42), as `LEARNING.md` requires.
9. **One kill-rule control without a durable report.** `CtlPrefixCache` (1 of the 27) has no seat
   report on disk; the durable evidence is `verification/l1-rescores/p48_noreval.json` and the L1's
   scratch receipt. Recorded as a bound, not a relabel.
10. **Driver runtime (operator-side).** The live `.ufo/watchdog.log` carries the launch line only
    (no `complete kake round=43`), `.ufo/state/kake.round` reads `16`, and
    `.ufo/state/kake.report-baseline` carries the empty-string sha256. Not lane debt.

## 9. Admission note

Every declared claim verifies **as declared**: C1's declaration is NOT MET and the kill-rule
evidence holds; C2's declaration is verified with its disclosed bounds; the registry correction
re-derives. No axis is observed harmed. Round verdict: honest stop — `rejected-honest-stop`
(no operability axis move admitted). This file is the outside check; the closure entry records
`admitted=true` under PROTOCOL step-5's "every claim verifies as declared" criterion.

`SHONEN.md` is fully checkable by a non-author: all four boxes carry resolvable pointers and box 2's
`[ ]` honestly records the second consecutive C1 not-met. This closure writes no `[x]`.
