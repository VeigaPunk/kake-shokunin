# Round 80 — verifier spot-check (hyaku closure, non-author)

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-04
lane-round: kake 80 · base `9998dc7a586b9fe76379014c8123aa3606f2d8b9` · tip `6b35928ad78e972bef93a5e6c3f18a780afc5c0d`
report: `.ufo/reports/round-80/kake.md` @ `855d1b3561bdece766535f26dd73bb7b817b894a` (kake-shokunin `<kake@shokunin.local>`)
dispatch: `2026-11-04T07:37:32-03:00 launch kake round=80 pgid=1857906 driver=hyaku-inline attempt=1`;
`2026-11-04T08:25:34-03:00 complete kake round=80; hyaku-inline attempt=1` (copy of the mutable
`.ufo/watchdog.log` lines this record rests on).

## 1. Step-1 conformance

| Check | Command | Observed | Verdict |
|---|---|---|---|
| Report committed by the lane identity | `git log --format='%an %ae %H' -- .ufo/reports/round-80/kake.md` | `kake-shokunin kake@shokunin.local 855d1b3561bdece766535f26dd73bb7b817b894a` | pass |
| Report path and filename | `ls .ufo/reports/round-80/kake.md` | present | pass |
| Report pushed on the fleet remote | `git merge-base --is-ancestor 855d1b35 origin/master` (`origin/master` = `656564e7`) | ancestor | pass |
| `SHONEN` heading + one line per box | `grep -c '^## SHONEN'`; `grep -cE '^- \[[ x~]\]'` | `1`; `4` (`[~]`, `[ ]`, `[~]`, `[~]`; no `[x]`) | pass |
| Required sections, in order | `grep -n '^## '` | Work performed · Landed changes · Before → after measurements · Sources & frontier · Trend verdicts · SHONEN (+ Stale-lane/tooling) | pass |
| Cited lane commits exist and are ancestors | `git rev-parse --verify <h>^{commit}` + `git merge-base --is-ancestor <h> refs/heads/master` for the 16 hashes in the Landed-changes table plus the base | 16/16 exist; 16/16 ancestors of `master` (`refs/heads/master` = `6b35928a`) | pass |
| Lane pushed, no round work uncommitted | `scripts/hyaku/jj-lane.sh state …/kake-shokunin`; `git -C … status --porcelain` | `branch=master local=6b35928a remote=6b35928a ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty | pass |
| Prompt carries the template contract | first 140 lines vs `templates/round-prompt.md` with `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}` rendered | two expected lines differ (`<kake-repo>` resolved to `kake-shokunin`; the lane-axes parenthetical `(web properties and publishing)`); §6 addendum appended. Round-level embed (mission/axes, 1–3 claims, L2 ≥ 8, commit-then-push, push scope, L0) and the five child-lane items present | pass |
| Census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` | exit 0; `191` rows; `20` `W04`; `kake ok` | pass |
| Wave shape | `.ufo/waves/round-80/w1-results.json` | 15 records: scout 2, executor 5, scribe 2, reviewer 2, critic 1, mutation-tester 1, connector 1, sentinel 1; 13 non-empty outputs, 2 empty (`ReviewC1`, `MutC`); 13 seat reports under `w1/` | pass with the routed accounting defect R80-4 |

Notes: the report lands last (tip `6b35928a` precedes the report commit); the base hash is the lane
tip before the round; the lane tip and remote agree (`git ls-remote origin refs/heads/master` →
`6b35928a`). Conformance defects are named in §6; none is a marker defect and none changes the lane
status. `kake-shokunin` holds no uncommitted round work.

## 2. Claims re-check (both re-measured)

I ran the two claim counters read-only outside `--work` over the committed base and tip bytes. I did
not execute the standing round-79 receipt-ledger gate; its committed receipt is evidence-verified
(§2.1). Where a claim rests on a selftest, the tally is verified from the committed receipt and the
counter's own `selftest_ok` line.

### C1 — calibration: the round-79 routed-defect queue closes (re-measured)

```
$ python3 -B .ufo/waves/round-80/c80_defect_queue.py --root . \
    --revision 9998dc7a586b9fe76379014c8123aa3606f2d8b9 --work /tmp/kake-closure-c1/base
R79-1 open no S453 row in corpus/SOURCES.md
R79-2 open scripts/ledger_append_guard.py absent
R79-3 open receipt c80-selftest.txt lacks a `selftest: N/N passed` line or `exit=0`
R79-4 open .ufo/waves/round-80/c80_ledger_fixtures.py absent
R79-5 open round-80 lesson carries no R79-5 withdrawal row quoting the sentence
R79-8 open defect-queue.json absent or malformed
C1v1 revision=9998dc7a586b9fe76379014c8123aa3606f2d8b9 items=6 open=6 closed=0 exported=77 met=false
exit=1

$ python3 -B .ufo/waves/round-80/c80_defect_queue.py --root . \
    --revision 6b35928ad78e972bef93a5e6c3f18a780afc5c0d --work /tmp/kake-closure-c1/tip
R79-1 closed S453 = RFC 9110 row present, used-by resolves (corpus/knowledge/http-date-grammar.md), row shape ok, erratum recorded
R79-2 closed guard selftest green (non-prefix fixture failed); ledger files=1 prefix preserved
R79-3 closed receipt matches re-run: selftest: 33/33 passed
R79-4 closed k3/k4/k5 killed by isolated fixtures (cheap-note red via undisclosed=1); QUALITY clause present
R79-5 closed withdrawal recorded; no self-assessment file repeats the sentence
R79-8 closed 2 empty-output seats recorded with re-derived bytes (ExecC2Tool, CriticC)
C1v1 revision=6b35928ad78e972bef93a5e6c3f18a780afc5c0d items=6 open=0 closed=6 exported=84 met=true
exit=0
```

- **Agreement.** `open 6 → 0` and `closed 0 → 6` at the base and tip, matching the report's
  `aa44b9af` carrier (the tip reads the same verdict, so the later settlement commits did not move
  it). The base control receipt `controls/base-c80-defect-queue.txt` prints the same six-open block.
- **Supporting bytes re-derived.** `S453` is an 11-cell row at `corpus/SOURCES.md:200` whose
  `used-by` resolves to `corpus/knowledge/http-date-grammar.md`; the receipt ledger grew
  `32 → 36` events with the four disclosed round-80 entries; the ledger's base bytes up to the final
  `]` are preserved (`base[:20057] == tip[:20057]`, 20,061 → 22,324 B; the only later difference is
  the closing `]`); `defect-queue.json` records the two empty seats with `output_bytes=0` and
  `output_sha256=e3b0c442…b855`; `controls/c80-cheap-note.txt` shows k3/k4/k5 killed, k4 through
  `undisclosed=1` with `malformed=1`.
- **Evidence-verified (gate not executed).** `controls/after-c1-ledger-gate.txt` at `aa44b9af`:
  `C1v2 revision=aa44b9af… events=36 undisclosed=0 phantom=0 malformed=0 wrong_kind=0 unpointed=0
  symlinks=0 round_rewritten=0 met=true`, exit 0. Selftest tallies: queue `3/3`
  (`controls/ctl-c80-queue-selftest.txt`), guard `2/2` (`controls/after-c1-ledger-guard.txt`),
  tool `33/33` (`controls/c80-selftest.txt`, sha256 `d1ea524f…`).
- **Limits that stand.** `R79-5`'s conjunct is textual: the junk control closes it on words, so the
  junk tree reads `open=5 closed=1 met=false` rather than the contract's `open=6` (the lane records
  the contradiction as a limit, not a pass). `R79-8`'s original ask (the seat's last error text) is
  not met; the frozen condition is the re-derived byte record, and the record says the error text is
  not recoverable from committed bytes. Both are routed (R80-5, R80-6) without disturbing the claim.

**Verdict: C1 calibration `improved`.**

### C2 — operability: `unavailable_after` accepts the date shapes its source names (re-measured)

```
$ python3 -B .ufo/waves/round-80/c80_measure.py --root . \
    --revision 9998dc7a586b9fe76379014c8123aa3606f2d8b9 --work /tmp/kake-closure-c2/base
frozen: cases=31 decided=31 wrong=0 constants=4/4 selftest_ok=true ok=True
a2: cases=12 decided=12 wrong=10 constants=4/4 selftest_ok=true ok=False
C2v1 revision=9998dc7a… tool_sha256=dd83c2c8… tool_bytes=19680 cases=12 decided=12 correct=2 wrong=10 undecided=0 constants_failed=4/4 selftest_ok=true cases_sha256=61b4b44e… met=false
exit=1

$ python3 -B .ufo/waves/round-80/c80_measure.py --root . \
    --revision 6b35928ad78e972bef93a5e6c3f18a780afc5c0d --work /tmp/kake-closure-c2/tip
frozen: cases=31 decided=31 wrong=0 constants=4/4 selftest_ok=true ok=True
a2: cases=12 decided=12 wrong=0 constants=4/4 selftest_ok=true ok=True
C2v1 revision=6b35928a… frozen_cases=31 frozen_wrong=0 a2_cases=12 a2_wrong=0 constants=4/4+4/4 selftest=ok met=true
exit=0
```

- **Agreement.** `a2 wrong 10 → 0` with `frozen wrong=0` on both runs, matching the report's
  `aa44b9af` carrier and receipts `controls/base-c80-a2.txt` / `controls/after-c2.txt`.
- **Tool identity.** Base `dd83c2c8…`, 19,680 B; tip `d1ea524f…`, 23,677 B — the receipt's sha256 and
  byte count exactly. The diff is the amendment-1 grammar: `ASCTIME_RE` added, `DATE_COMMA_RE`
  splices a comma that follows the leading weekday token of an `unavailable_after` value, and seven
  selftest cases `t24–t30` cover the three comma-bearing shapes, the asctime shape, the `PST`
  negative and the bot-scoped value; no other semantic branch moved.
- **Oracle grounding.** S452's retained text carries the source example at line 243
  (`X-Robots-Tag: unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT`); RFC 9110's retained text
  lines 1848–1852 carry the IMF-fixdate, RFC 850 and asctime examples; the frozen 12-case oracle is
  entailed by those bytes, not by a tool run.
- **Constants.** The receipt `controls/ctl-c80-constants.txt` reads
  `const_all 12/12 · const_clean 12/12 · const_echo 11/12 · const_regex 12/12`, summary
  `constants_failed=4/4 cases=12`. The frozen condition is "each must fail at least one case"
  (`contract.md:100`), so `4/4` holds; the report/LOG/lesson sentence "12/12 each" is wrong for
  `const_echo` and is routed as R80-2. The claim's predicate is unchanged.
- **Limits that stand.** Calendar validity, the RFC 850 50-year window, per-bot effective
  resolution, meta+header conflicts and redirect-hop inheritance are undecided; A2's single-space
  day branch is a lane `[INFERENCE]` (RFC 9110 `date3` requires the two-space one-digit form); the
  header/meta per-carrier divergence is recorded, not harmonized. The report says all of this.

**Verdict: C2 operability `improved`.**

## 3. Axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| calibration | **improved** | C1 re-measured `open=6 → 0` at `9998dc7a`/`6b35928a`; six routed items closed from bytes; receipts, four-entry disclosure and the append guard at the tip |
| operability | **improved** | C2 re-measured `a2 wrong=10 → 0`, `frozen wrong=0` unchanged; tool `d1ea524f…` 23,677 B, selftest `33/33`; three registry rows at `SKILL.md:1499-1510` |
| coverage | **improved** | new `corpus/knowledge/http-date-grammar.md` (111 lines, five `[INFERENCE]` marks, per-carrier divergence table) with `source: S453`; knowledge `.md` `66 → 67`; README coverage section |
| freshness | **unchanged** | held, not re-measured live: `node scripts/freshness-sweep.mjs --offline` → `VERDICT: OK (exit 0, partial: offline)`, remote/armed/history skipped; never counted as a pass |
| depth | **unchanged** | `SKILL.md` gained registry rows only (13 added lines); no new decision table or error-pattern list |
| adjacency | **unchanged** | no contested scope; the round-78 meta-tool divergence is recorded as a per-carrier scope and routed, not absorbed; new entry cites no sibling lane repository |

No owned axis is harmed. `git diff 9998dc7a 6b35928a -- SCORECARD.md` is additions-only (`49/0`),
scores held (operability 10, freshness 10, calibration 2), and `LOG.md` (`13/0`), `PROVINCE.md`
(`11/0`), `corpus/README.md` (`15/0`), `corpus/QUALITY.md` (`23/0`), `corpus/SOURCES.md` (`1/0`) and
`corpus/lessons/round-80.md` (`217/0`) are additions-only. The tool diff (`69/5`) is the intended
amendment-1 grammar.

## 4. Discernment spot-check (non-author, outside the lane)

| Item | Gate decision | Re-opened source | Agree/Disagree | Reason |
|---|---|---|---|---|
| S453 RFC 9110 §5.6.7 | admit, tier A, `mined` | URL `https://www.rfc-editor.org/rfc/rfc9110.txt`; retained `.ufo/waves/round-80/sources/rfc9110.txt` 502,941 B, sha256 `21c1cdce…7232a` (identical in the scout copy); quote at `:1855-1856`; `corpus/SOURCES.md:200` | **agree** (decision) | the 17-word normative quote is verbatim at those lines; a Standards Track `MUST` on the recipient grounds tier A; the `.txt` URL is a distinct scope and the census `W04` warns rather than errors. The row's citation is one line off (`:201` vs `:200`) and the "held five times" count is conflated — both routed R80-1/R80-3, not decision defects |
| Rejected `S453` row for RFC 9309 | reject, no row | `.ufo/reports/round-79/kake.md:142`; `git show 9998dc7a:corpus/SOURCES.md \| grep -c 'S453'` = `0`; `S099` row (RFC 9309) | **agree** | no rejected row was ever written; the round-79 sentence was false and the erratum is correct; RFC 9309 is already held as S099, and the round-80 S453 cites RFC 9110 only (`grep -c 9309` on the row = `0`) |
| Second row on S449's Google URL (header scope) | defer / not written | `.ufo/waves/round-79/w1/ScoutSources/row-deferred-google-xrt.txt`; `corpus/SOURCES.md:196` (S449) | **agree** | the draft is a second row on the same URL as S449 (a census `W04`), and the frozen round-80 contract admitted S453 only; deferring is the honest call |
| `merge/kake` staged package | reject adoption | `/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md` (126,796 B); `corpus/SOURCES.md` | **agree** | independent extraction: 129 staged rows vs 191 registry rows, exactly `8` id collisions (`S312, S329, S367, S372, S373, S374, S390, S409`) and `27` staged URLs already held; matches `w1/ConnectorC/collision.out` |

Spot-check result: the gate's admit and three reject/defer decisions agree with the outside re-open.
Two supporting-evidence defects (the S453 line citation and the URL-count/scoping sentence) are
routed R80-1/R80-3; neither changes a gate decision.

## 5. Trend verdicts

- **expansion — improved.** One admitted `knowledge/` entry on ground the coverage map marked not
  held (`corpus/knowledge/http-date-grammar.md`, `source:` citing mined S453 and the re-opened S452;
  knowledge `66 → 67`), one registry row with a located Gate quote, and three capabilities in the
  SCORECARD repertoire (routed-defect queue gate, receipt-ledger append guard, survivor-mutant
  harness) with revision-bound receipts.
- **quality — improved.** A weaker grammar is superseded by a stronger one while the frozen 31-case
  matrix is unchanged (`frozen wrong=0` both runs); the standing ledger gate is green at the carrier
  with four rewrites disclosed; three counter/instrument defects were found and fixed before any
  after-state (the `used-by` index, the revision-mode ledger, the fixture condition); no admitted
  entry was found false or stale. The prose-accuracy defects routed R80-1–R80-3 are report/lesson
  wording, not knowledge-entry claims.
- **discernment — improved.** This outside spot-check agrees with the gate on the admit and on both
  re-opened rejects (LEARNING.md's operational criterion); the attack seats' falsifications (the
  junk-control sentence and A5's non-enforcement) are recorded as limits rather than silently
  accepted, and the one new `QUALITY.md` criterion cites the lesson that produced it.

## 6. Routed defects for kake round 81 (status-neutral)

1. **R80-1 (low, citation).** `corpus/SOURCES.md:201` is a blank line; the `S453` row is at line
   `200`. Correct the pointer in `.ufo/reports/round-80/kake.md:158` and
   `corpus/lessons/round-80.md:51` by erratum/append next round, not by rewriting the filed bytes.
2. **R80-2 (low, numeric accuracy).** The round-80 LOG bullet and the lesson say the four frozen
   constants "fail 12/12 each"; `controls/ctl-c80-constants.txt` reads `const_echo.py failures=11 …
   total=12`, and the frozen criterion is "each must fail at least one case" (`constants_failed=4/4`,
   `cases=12`). Append a correction: `4/4` constants, `47/48` case-level failures, `const_echo`
   `11/12`. The C2 predicate is unaffected.
3. **R80-3 (low, corpus count/scope prose).** `corpus/lessons/round-80.md:52-53` and
   `corpus/README.md:592` call S453 "a second scoped row on a URL the registry already holds five
   times (S010, S028, S033, S088, S433)" / "a second scope … same pattern". The census keys URLs: the
   exact `.txt` URL was held by S028 and S033 (S453 is the third scope), while S010/S088/S433 hold
   `rfc9110.html`. Append a precise correction next round.
4. **R80-4 (conformance, wave accounting).** The report, LOG and SCORECARD count sentinel in the
   attack share (`5/15 = 33.3 %`). The run-15 addendum's attack roles are reviewer, critic,
   mutation-tester and labrat: requested `4/15 = 26.7 %`; after `ReviewC1` (reviewer) and `MutC`
   (mutation-tester) died on provider 429s and were not replaced, settled attack seats with reports
   are `2/15 = 13.3 %` (`3/15 = 20 %` if ExecGuard's review reproduction counts), below the ≥25 %
   floor in effect. The deaths are disclosed, but the share is misstated and the floor is missed:
   re-state the share by the directive's role list and replace a dead attack seat in the next wave.
5. **R80-5 (low, evidence reproducibility).** `controls/ctl-c80-junk-queue.txt` records a run over
   `/fast/scratch/hyaku/kake-r80/l1/junk`; that tree is not committed and no committed builder
   recreates it, so the junk control is not re-runnable from lane bytes. Commit the builder/tree or
   name the builder in the contract next round. (The fixture receipts also name `$HYAKU_SCRATCH`
   runs, but the harness is committed and reconstructs them.)
6. **R80-6 (low, residual R79-8).** `defect-queue.json` records `last_error` as "the results file
   carries no error field"; the original R79-8 ask (the seat's final error text) remains unmet, and
   the 429 cause for `ReviewC1`/`MutC` is asserted outside committed bytes. Record status, exit and
   error at dispatch time in the next results schema so a dead seat's cause is citable.
7. **Acknowledged, not routed.** `R79-5`'s textual conjunct can be satisfied by a fabricated
   withdrawal (junk control `open=5`); the report states the limit. The foreign-pointer sweep in
   `/fast/scratch` receipts and the freeze receipts' `exit=` duplication were already acknowledged
   in earlier rounds.

Promotion note for the operator: no `SHONEN` box is `[x]`; boxes 1/3/4 remain author `[~]` and box 2
stays `[ ]` (the historical LOG-named receipt was never committed), so the checklist is **not fully
checkable by a non-author** this round; promotion remains operator-owned.

## 7. Closure verdict

Both declared claims verify by re-measurement (`C1 open 6 → 0`; `C2 a2 wrong 10 → 0` with the frozen
31-case set unchanged), no owned axis is harmed, and the non-author spot-check agrees with the gate's
admit and rejects. The six routed defects are conformance/accuracy items, status-neutral.
`admitted: true`.
