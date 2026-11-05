author: hyaku closure (non-author integrator, @m_zfl)
round: kake 92
date: 2026-11-04
report: .ufo/reports/round-92/kake.md
lane_base: e143faff1b86aad172dd87696da900c70347b8b2
lane_head: 027faf79bba2600c0852f1ec2b51774c868cf321
freeze: a5640ca02c20f94a0fa03af41b977b46ae99808e
carrier: 2a4447c1a4696cbfb40b17014e47fc6af716c06d

# Round 92 verifier spot-check — kake (hyaku closure, non-author)

I did not author this round and edited no lane-authored file. Every measurement
below was re-run on committed bytes with plain `git`/`grep`/`awk`/`wc`/`sha256sum`
/`curl`. The lane's two frozen counters (`.ufo/waves/round-92/c92_defects.py`,
`c92_heuristic.py`) were **not executed** (`PROTOCOL.md` §Gate standard, Closure
consequence); their committed receipts were read and each printed revision was
checked against the commit it names. The one lane-owned **probe**
(`scripts/heuristic_freshness.py`, registered as a probe, stdlib only, no network,
no file writes) was run once from an extracted blob as a capability check.

## Conformance results

- Report `.ufo/reports/round-92/kake.md` (20 047 B) is committed by the lane
  identity: `git log --format='%an %ae %H %ci' -- .ufo/reports/round-92/kake.md` →
  `kake-shokunin kake@shokunin.local 3ebedf2f111796e3c2fa94455847c07e1a3b00c3
  2026-11-04 22:07:09 -0300`, i.e. before the driver completion line
  (`22:07:24`), and contained in `origin/main` and `origin/master`
  (`git branch -r --contains 3ebedf2f`). ✓
- Driver digest (copied from the closure prompt; not re-derived from the mutable
  log): `21:13:09 launch kake round=92 pgid=1046723 attempt=1`;
  `21:58:46 lane-dead-no-report kake round=92`; `21:58:48 launch … attempt=2`;
  `22:07:24 complete kake round=92; hyaku-inline attempt=2`. Two attempts, the
  first recorded dead without a report, the second landed. ✓
- `## SHONEN` appears once with exactly four box lines (`[~]`, `[ ]`, `[~]`,
  `[~]`, no `[x]`), matching `SHONEN.md`'s four boxes; `git diff e143faff 027faf79
  -- SHONEN.md` is empty. The box-2 gap is real: `git cat-file -e
  027faf79:.ufo/waves/round-47/verification/offline-sweep-r46-verdict-time.txt`
  fails, and `corpus/knowledge/shonen-ledger.json` reads `1 evidenced, 2 gap,
  3 evidenced, 4 evidenced`. ✓
- Every cited lane hash resolves and is an ancestor of the branch ref
  (`git merge-base --is-ancestor <full> master`): `a5640ca0`, `f0b2dc63`,
  `2a4447c1`, `9f15115b`, `027faf79` — 5/5 ok (plus the base `e143faff`). ✓
- `jj-lane.sh state` → `branch=master local=027faf79 remote=027faf79 ahead=0
  behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` prints
  nothing. No uncommitted round work; pushed. ✓
- Prompt `.ufo/prompts/kake-round-92.md` (846 lines): carries the round contract
  (1–3 claims on distinct axes with a lowest-axis claim, L2 floor of 8 in one
  batched swarm, commit-then-push, push scope, the L0 side channel) and all five
  child-lane items — report path/filename (line 100), report-lands-last with the
  pushed lane hash cited (line 516), `SHONEN` one-line-per-box rule (line 118),
  commit-hash citation rule (lines 106–110), lane write scope (line 582) — then
  addendum §6. No L2 route map is quoted, so the MISSION.md bucket comparison is
  vacuous (`MISSION.md:61-65` is role-class advisory with no pins). ✓
- Wave: `w1-spec.json` `maxLanes=14`; `w1-results.json` `seats=14`, agents
  executor 4, scout 2, scribe 2, reviewer 2, connector 1, sentinel 1, critic 1,
  mutation-tester 1 — attack seats 4/14 = 28.6 % (≥25 %), connector 1 (≤2). 13
  seat directories carry files; `SentinelQuote` has 0 (`git ls-tree -r` → 0
  lines), as the report states. ✓
- Counters and contract are byte-identical freeze → head
  (`git rev-parse <rev>:<path>` equal for `c92_defects.py` `c796e03f`,
  `c92_heuristic.py` `d2ac4af0`, `c2-contract.md` `c04648d8`): no post-freeze edit
  of a scored predicate. ✓
- **Defects (status-neutral, routed below).** (1) The report's C1 item-A bullet
  says "the log records a `base` and an `M01` run that differ"; the committed
  `integration/mutation-tip.log` holds **30 mutant lines with base excluded** —
  the seat's own `w1/ExecMutation.md` says so — and the base/M01 differential
  lives in `w1/ExecMutation/run.log` [5]. (2) `c92_heuristic.py` is registered as
  a **gate** (`SKILL.md:1664`) with "no `--selftest` mode", which §Gate standard
  Self-test does not accept for a gate. (3) `corpus/QUALITY.md` §Round 92 grounds
  its criterion on the considerthese proposal and the measured receipt but names
  no `corpus/lessons/` file, which `LEARNING.md` asks a criterion to cite.
  (4) `corpus/lessons/round-92.md` §Mistakes row 5 is detached from the table by
  a blank line, splitting it into two tables. None of these changes the round's
  status.

## Per-claim re-check

| Claim | Reported | Re-check (mine) | Mode |
|---|---|---|---|
| C1 calibration (lowest owned non-retired axis, 2 HOLD) — K91-1/2/4/5 close | `open=3 closed=0 battery=hit differential=fail self=hit met=false` exit 1 at base → `open=0 closed=3 battery=exact differential=ok self=ok met=true` exit 0 at `2a4447c1` | Receipts read line for line (`controls/base-c1.txt` `revision=e143faff…`, `exit` 1; `controls/after-c1-carrier.txt` `revision=2a4447c1…`, `exit=0`; `controls/attempt2-reverify.txt` reproduces both). The artifacts each item rests on exist and measure as declared (below). **The claim sentence does not verify**: the round's own attack seats reach `met=true` without doing the work. | evidence-verified + **falsified as worded** |
| C2 freshness — heuristic freshness decision instrument under contract v1 | `candidate=absent … met=false` exit 1 at base → `hand=28/28 generated=120/120 forgeries_refused=5/5 anti_table=ok population=ok met=true` exit 0 at `2a4447c1` | Receipts match; the instrument is absent at the base and present at head with the declared digest; the entry, registry rows, coverage row and capability row all exist; my own probe reads `selftest 54/54` exit 0 and returns the three decisions the entry claims. The frozen counter under-proves conformance (13/24 tool mutants survive, 5 clause-violating subjects admitted) — that is routed R92-4/R92-5, not part of this claim. | re-measured (probe) + evidence-verified |
| Counts | rows 206→207, knowledge `.md` 79→80, 0 deletions, 1059 added / 0 removed outside `.ufo/` | `git show <rev>:corpus/SOURCES.md \| grep -cE '^ {0,3}\| *S[0-9]{3,}'` → 206, 207; `git ls-tree -r --name-only <rev> -- corpus/knowledge \| grep -c '\.md$'` → 79, 80; `git diff --diff-filter=D --name-only e143faff 2a4447c1` → 0 lines; `git diff --numstat e143faff 2a4447c1 -- . ':!.ufo'` → added 1059 removed 0. | re-measured, matches |

**C1, re-derived without the counter.**

- *Item B (K91-2) closes.* `git show e143faff:SKILL.md | grep -c c92_defects.py`
  → 0; at head → 2. The row is `SKILL.md:1663` and names the counter, its
  `--revision` command, its exit map, `--selftest` 12/12 and the `met` predicate;
  `SKILL.md:1667` is the "How to verify" line for both counters. The line numbers
  the report cites are exact.
- *Item A (K91-1) artifacts exist and bind.* `integration/mutation-tip.txt` line 1
  reads `gate_sha256=d7bca38ec146727087a2d2e37a64c5154214e2dd069553fb5594372d2064b65e
  mutants=30 killed=20 survivors=10 met=true`; `sha256sum` of
  `git show 027faf79:scripts/cache_key_conformance.py` is exactly that digest at
  base, carrier and head; `integration/mutation-tip.log` holds 30 lines, 20
  `killed` and 10 `survived`, matching the receipt counts; `run.log` [5] records
  `base verdict=survived rc=0` against `M01 verdict=killed rc=2`.
- *Item C (K91-5) asserts nine labels.* `grep -cE '^\s*echo "[a-z-]+='` on
  `controls/run_controls.sh` → 9 (`base-open base-met base-exit carrier-open
  carrier-met carrier-exit selftest noharm self`); the counter's `C_labels`
  conjunct reads them from the `ONLY=c1` replay (`attempt2-reverify.txt`).
- *Battery and differential (K91-4).* Five frozen `neg-*.py` subjects exist; the
  carrier receipt reads `battery=exact differential=ok`, and `ctl-c1-known-good.txt`
  records the frozen predecessor accepting the canned-runner fixture this counter
  refuses.
- *Why the claim fails anyway.* The round's own seats falsify it by construction:
  `w1/ReviewC1/Attack.md` classes 3 (canned-verdict runner), 5c (constant-label
  harness) and 6 (self-pin rewritten in the same commit); `w1/CriticClaims/C1.md`
  F1 (runner executes a different gate, `333230ce`), F2 (row naming a refusing
  counter, `605a0026`), F3; `w1/ExecMutation.md` D1 (only `sorted(verdicts)[0]` is
  ever executed, so a forged unsampled line is admitted) and D3
  (`--skip-battery` prints `differential=ok … met=true` with no differential run).
  A `met=true` that a canned printer reaches is not a closure of K91-1/K91-4, so
  the claim sentence "the defects close" does not verify. The lane filed it as
  **not admitted** and routed R92-1…R92-3 instead of patching after scoring; that
  honesty is what the calibration grade below records.

**C2, re-derived without the gate.**

- Instrument: absent at `e143faff` (`git cat-file -e` fails), present at head,
  22 985 B, `sha256` `7bfe82da8e1a1d541930ef1b4ee64cfe9b3fa5b8169680795bcc8626d2f37f5c`
  — equal to the `candidate_sha256` the counter receipt prints and to the value
  the report cites.
- My probe (extracted blob, run outside the lane tree):
  `python3 -B <blob> --selftest` → `selftest 54/54`, exit 0;
  `{"stored":{"status":200,"headers":{"date":"1000","last-modified":"0"}},"now":2000}`
  → `{"decision": "heuristic", "heuristic": true, "lifetime": 100}` (10 % of a
  1000 s interval);
  `…"cache-control":"max-age=600"` → `{"decision": "explicit", "lifetime": 600}`;
  `…"cache-control":"no-store"` → `{"decision": "not-storable", "lifetime": null}`;
  `…"cache-control":"max-age=\"600\""` → `invalid_input: max-age argument is not a
  bare non-negative decimal integer`, exit 1 — the shipped tool refuses the quoted
  form the counter's reference accepts, which is R92-5's point, confirmed here.
- Corpus side: `corpus/knowledge/heuristic-freshness.md` 480 lines with the
  `source:`/`verified-at:`/`recheck:` trio first, `source:` citing S470;
  `corpus/README.md` gains the r92 coverage row (0 → 1 `Heuristic freshness
  decision` match) and the frontier narrative at 736–753; `SCORECARD.md` gains the
  capability row and both move-log rows; `SKILL.md:1665` registers the tool as a
  **probe** with its stdin/stdout contract and `--selftest`.
- Independent review and trial (lane seats, evidence-verified): `ReviewC2` 97
  cases, `cases: 97 agree: 93 disagree: 4` with 0 tool defects;
  `ExecTrial/trial.txt` `surfaces=18 exit0=18 refused=0
  agree_with_pre_run_contract_derivation=18/18`.

## No-harm check

`git diff --diff-filter=D --name-only e143faff 2a4447c1` prints nothing: 0 files
deleted; 1059 added / 0 removed outside `.ufo/`. `git diff e143faff 027faf79 --
SCORECARD.md` adds the round-92 sections and changes no axis score (operability
10, freshness 10, calibration 2 — all HOLD). `SOURCES.md` gains one row (S470);
no existing row's `status`, `recheck` or `used-by` cell moved
(`git diff e143faff 027faf79 -- corpus/SOURCES.md` is one added line). `SHONEN.md`
untouched. No owned axis is harmed.

## Spot-check (`corpus/lessons/round-92.md` `## Gate`; 4 admits, 3 rejects)

Re-opened live: `GET https://www.rfc-editor.org/rfc/rfc9111.txt` → HTTP 200,
84 477 B, sha256 `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`
— byte-identical to the retained body `.ufo/waves/round-92/L1/src/rfc9111.txt`
(same size and digest) and to the row's anchor cell. Line numbers below are
plain-text lines of that body; every quote was checked as an exact substring of
its cited line span.

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| §4.2.2 permission | admit (S470, tier A) | line 686 heading; lines 688–690 "a cache MAY assign a heuristic expiration time when an explicit time is not specified" | agree | Verbatim, 15 words ≤25; it is the permission the instrument's `heuristic` branch rests on, and the lesson keeps it scoped to "explicit time not specified". |
| §4.2.2 prohibition | admit | lines 695–696 "A cache MUST NOT use heuristics to determine freshness when an explicit expiration time is present in the stored response." | agree | Verbatim, 20 words; grounds `explicit` taking precedence over any heuristic lifetime. |
| §4.2.2 cacheability gate | admit | lines 697–699 and 700–701 ("…heuristically cacheable" / "…marked as explicitly cacheable (e.g., with a public response directive)") | agree | Both fragments verbatim, 18 words each; the `public` override and the `not-heuristically-cacheable` member follow from the text as quoted. |
| §4.2.2 fraction / 10 % | admit | lines 707–708 "caches are encouraged to use a heuristic expiration value that is no more than some fraction of the interval since that time."; line 709 "A typical setting of this fraction might be 10%." | agree | 22 and 9 words; "encouraged"/"typical" is exactly why the entry marks the 10 % as a convention, not a requirement. |
| "the 86400-second cap is RFC 9111's" | reject (proposition) | full body, `grep -n '86400\|86,400'` → 0 hits; §4.2.2 line 693 "it does impose worst-case constraints on their results." | agree | The section names no value; a cap attributed to the RFC would be a fabricated citation. The flip (a section that names a bound) is the right condition. |
| "a second row for the heuristically-cacheable status set" | reject (row candidate) | line 700 "(e.g., see Section 15.1 of [HTTP])" — §4.2.2 defers and lists no codes | agree | The anchor for such a row would be RFC 9110 §15.1, not RFC 9111; a second §4.2.2 row would misattribute the ground. |
| "a row for the RFC-Editor errata page" | reject (row candidate) | `GET https://www.rfc-editor.org/errata/rfc9111` → 200, 40 383 B; exactly four records (`eid7695`, `eid9004`, `eid9166`, `eid9185`); `grep -c '4\.2\.2'` → 0, sections named are 4.1, 4.3.1, 4.3.2, 4.3.4 | agree | No erratum touches §4.2.x, so the page grounds nothing about this round's ground; the stated flip (an erratum touching §4.2.2) is correct. |

New `corpus/SOURCES.md` row re-opened: **S470**. Row shape is 11 columns
(`awk -F'|'` NF=13), `kind=spec`, `tier=A`, `status=mined`, `recheck 180d`,
`used-by corpus/knowledge/heuristic-freshness.md` (the file exists). The `anchor`
cell resolves (heading 686, permission 688–693, prohibition 695–696,
cacheability 697–701, fraction 706–709) and carries the fetch provenance (HTTP
200, 84 477 B, sha256 `aeb52adb…5302cf3e`). The lesson's Gate quote for the row is
15 words with its location — inside the ≤25-word rule. No tier inflation
(`spec` is A), no duplicate id.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
→ exit 0, `kake ok …/corpus/SOURCES.md`, 31 × W04 (S470 is the fourth scope on
`www.rfc-editor.org/rfc/rfc9111.txt`), matching the report's before/after
(206 → 207 rows, 30 → 31 advisories).

## Per-axis verdicts

| Axis | Verdict | Reason |
|---|---|---|
| calibration (C1, lowest owned non-retired axis) | **unchanged** | The four routed defects' *artifacts* land (registry row, bound gate digest, nine-label harness, five-fixture battery with the frozen-counter differential), but the claim sentence "the defects close" is falsified by the round's own committed attacks: `met=true` is reachable with a canned runner, a constant-label harness and a rewritten self-pin (`w1/ReviewC1/Attack.md` classes 3/5c/6), with a runner executing a different gate (F1) and a row naming a refusing counter (F2), and item A re-executes only one log line (ExecMutation D1). Score stays 2 HOLD; no false claim stands because the report files C1 as not admitted and routes R92-1…R92-3. Not `harmed`: nothing existing regressed and no admitted entry was found false. |
| freshness (C2, capability acquisition on open frontier ground) | **improved** | A capability the lane did not have now runs: `scripts/heuristic_freshness.py` (22 985 B, stdlib only) decides the five members over supplied integer seconds; my non-author probe reads `selftest 54/54` and the three decisions the entry claims; the tool refuses the quoted delta-seconds form the counter's reference accepts; the entry re-verifies the source with a pinned digest and a dated `recheck`, and the capability row is in `SCORECARD.md`. Score stays 10 HOLD — the capability is the move, not a score change. |
| operability (not claimed) | **improved** | Two new registry rows (`SKILL.md:1663` counter, `:1665` probe) and a "How to verify" line at `:1667` make the round's instruments runnable from the registry home; the probe runs from a bare blob with no lane state. The C1 counter's registry row is present but its predicate is falsified (routed), so this grade rests on the probe plus the registry delivery, not on the counter's `met`. |

## Trend verdicts

- **expansion: improved.** `corpus/knowledge/` 79 → 80 `.md` with
  `heuristic-freshness.md` (480 lines) on ground the coverage map did not hold
  (the r92 row is new in `corpus/README.md`); registry 206 → 207 with S470
  tier A `mined` and cited by the new entry; one frontier row advanced with its
  narrative at `corpus/README.md:736-753`; census clean at both ends.
- **quality: unchanged.** No existing surface weakened: 0 deletions, 0 removed
  lines outside `.ufo/`, one added registry row, no admitted entry found false or
  stale-and-unmarked. The round's falsifications hit its own **new instruments**
  (tools entered with their predicates and their falsification on the record), and
  the one quality asset added is the `corpus/QUALITY.md` §Round 92 criterion. A
  gain is not claimed and not graded: the C2 population leaves five clauses
  unexercised (R92-4), so the counters are not yet a quality proof.
- **discernment: improved.** The outside spot-check agrees with **all seven**
  re-opened gate decisions (4 admits, 3 rejects) and with the new row's quote and
  anchor, which is the `LEARNING.md` condition for this trend. Behind it: the
  round's own seats falsified its C1 claim before filing (classes 3/5c/6, F1–F3,
  D1/D3), four control defects were caught by its own pre-freeze controls
  (Mistakes 1–4), attempt 2 re-measured the inherited readings instead of trusting
  them (Mistake 5), and a QUALITY.md criterion was added from a measured instance
  rather than a proposal's text. Offset, recorded not scored: the C1 claim was
  declared before its own battery could test the class it named, and the counter's
  `--skip-battery` mode prints `met=true` on an unmeasured predicate (D3) — both
  routed.

## Routed defects (lane fixes next round)

- **V92-1.** Report C1 item A says "the log records a `base` and an `M01` run that
  differ"; `integration/mutation-tip.log` holds 30 mutant lines with base excluded
  (`w1/ExecMutation.md` §Deliverables) and the base/M01 differential is in
  `w1/ExecMutation/run.log` [5]. Correct the pointer in the next report/lesson
  (append-only correction), never by rewriting the filed report.
- **V92-2.** `c92_heuristic.py` is registered as a **gate** at `SKILL.md:1664`
  with "no `--selftest` mode". §Gate standard Self-test requires every gate to
  expose a self-invocation mode over isolated fixtures asserting exit code and a
  stable finding-id; its reference self-check is not that mode. Either add the
  mode or register the row as a probe until it exists.
- **V92-3.** `corpus/QUALITY.md` §Round 92 grounds its criterion on the
  considerthese proposal and the measured receipt but names no
  `corpus/lessons/round-92.md` row; `LEARNING.md` asks each criterion to cite the
  lesson that produced it. Append the lesson pointer.
- **V92-4.** `corpus/lessons/round-92.md` §Mistakes row 5 is separated from the
  table by a blank line, splitting it into two tables. Re-append the row inside
  the table (append-only, do not rewrite rows 1–4).
- **Carried, still open from the lane's own routing:** R92-1 (item A executes one
  sampled line; bind every log line to its mutant digest), R92-2 (item C labels
  are constants; bind them to runs through a nonce), R92-3 (item B is text;
  resolve and run the row's command), R92-4 (one case per contract clause and
  refusal class; a type-mismatch case for clause 3), R92-5 (check the counter's
  reference against the contract before the freeze), R92-6 (`SentinelQuote` dead
  seat — the entry's quotes were verified only by ScribeEntry and ScoutSources;
  this spot-check re-verified them independently), R92-7 (K91-3, K91-6, K91-8,
  K91-9, K91-10).

## Note for the operator (promotion is operator-owned)

All four `SHONEN.md` boxes now carry non-author-checkable evidence pointers:
boxes 1, 3 and 4 rest on `corpus/knowledge/shonen-ledger.json` rows whose
populations are re-derivable at a revision, and box 2 stays `[ ]` on one named
missing receipt (`.ufo/waves/round-47/verification/offline-sweep-r46-verdict-time.txt`,
absent at `027faf79`) that this round's `ExecTrial` run does not repair. A
non-author reviewer could execute every check; I write no `[x]` — this file is a
spot-check, not a promotion review.
