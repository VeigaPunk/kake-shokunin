# ExecSpecLint — round-51 wave-1 dispatch payload lint

Seat: `L1Kake51.ExecSpecLint-2` (leaf, role `executor`). Axis owned: operability.
Mode: read-only over the lane; the only file written is this report.

## Which file was linted

**`w51-taskcall.json`** — the dispatch payload exists, so the `w51-spec.json` fallback was
not used. Both were read; `w51-spec.json` served only as the cross-check source.

| artifact | bytes | sha256 |
|---|---|---|
| `.ufo/waves/round-51/w51-taskcall.json` | 105665 | `135364c5dae91b86344082a9f2ebb4e65957d08f350da428bdb630a0a5cdd9a2` |
| `.ufo/waves/round-51/w51-spec.json` | 32121 | `1f2ed6a2cbfa72a1720b7c61ad35622e94526471fe54c39fc4cc6c7e100c1340` |
| `.ufo/waves/round-51/w1/swarm-registry.json` | 36917 | `24d33636b0f3ebdb779ee911755b31501aad36a689ee74ce091ec2f6231b94f4` |

Lane tip under test: `9d13768c4fdd0e9a2688d2ecf1616b539cf57658`.

## Verdict — the four asked-for checks

| # | check | result |
|---|---|---|
| A1 | seat count | **48** |
| A2 | unique-name check | **48 unique of 48** — no duplicate; name sets identical across taskcall / spec / registry (0 delta each way) |
| A3 | role histogram | **10 roles, sums to 48** — see below; byte-identical between `spec.items[].role`, `taskCall.tasks[].agent`, `registry.members[].role` (48/48 seats agree) |
| A4 | every item text names an absolute report path under `<lane>/.ufo/waves/round-51/w1` | **48 of 48** — 0 misses, exactly one target per seat, 48 distinct targets |
| A5 | band 32–64 holds | **TRUE** — `spawn=48` in `[waveMinLanes=32, waveMaxLanes=64]` |

### Role histogram (identical in all three artifacts)

```
reviewer 10 | critic 10 | executor 9 | scout 6 | mutation-tester 5
scribe   4 | connector 1 | sentinel 1 | revenger 1 | simplifier 1     = 48
```

### Count agreement

`tasks=48 == counts.spawn=48 == counts.total=48 == policy.maxLanes=48 ==
policy.declaredMaxLanes=48 == spec.items=48 == spec.maxLanes=48 == registry.members=48 ==
wave-grant.txt seats=48`. `counts.resume=0` and `resumeSends=[]` agree. Hard ceiling 256 and
`waveMaxLanes=64` are both far from binding.

## A4 in detail — report-path coherence

Every seat satisfies, verified per seat rather than by aggregate count:

- exactly **one** absolute path matching `<lane>/.ufo/waves/round-51/w1/<name>.md`;
- exactly **one** relative path `.ufo/waves/round-51/w1/<name>.md`;
- both basenames equal the seat's own `name` + `.md`;
- 48 distinct absolute targets, so no two seats are pointed at the same file.

All 48 also carry the `Write ONLY <abs path>` clause, and all 48 carry a `Report:` line naming
the same file relatively. The absolute and relative mentions therefore agree everywhere.

Result: `48 / 48` coherent, `violations: []`.

## Findings beyond the four asked-for checks

**F1 (structural, benign).** `w51-taskcall.json` is a single task call — `{context, tasks}` —
with `compaction.applied=false` (`reason: template_invocation`), `w51-validator.err` is
**0 bytes**, and `taskCall.context` is byte-identical to `spec.context` (3802 chars). The
"one batched task call per wave" note in the payload is respected: one `taskCall`, zero
`resumeSends`.

**F2 (structural, worth knowing).** `spec.template` is a 455-byte template holding exactly one
`{{item}}` placeholder at offset 447. The dispatched task text is *not* `template.replace(item)`
alone: the generator appends a four-line per-seat tail (`Lane bounds:`, `Judged on:`,
`Milestone:`, `Report:`). All 48 seats carry all four lines. So the payload is not a pure
function of `spec.json` — the tail lives only in `make_spec_w1.py`/the payload. This is not a
defect for dispatch (the tail is present and consistent), but it means the payload cannot be
regenerated from `spec.json` alone.

**F3 (small, real).** 45 seats carry one axis in `spec.axes[]`; **3 carry two** —
`ConnectorSiblingOverlap`, `CriticZeroControl`, `CriticHarm` (both `operability` and
`freshness`). The dispatched text names only one axis per seat via `Judged on:`, and it is
always a *member* of that seat's `axes[]` (48/48 valid), but for those 3 dual-axis seats the
second axis never reaches the seat as prose. Axis distribution in the tail: `freshness 25`,
`operability 23`; membership in the spec: `freshness 28`, `operability 23` — the 3-seat
difference is exactly those dual-axis seats. A seat reading only its dispatched text will
optimise one axis and can neglect the other.

## Claim-critical finding — the payload is not committed (bears directly on C1/L1)

`w51-taskcall.json`, `w51-spec.json`, `w1/`, `route-map.json`, `route-probes/`,
`wave-grant.txt`, `wave-start-utc.txt` are all **untracked** at the lane tip:

```
$ git status --porcelain .ufo/waves/round-51/
?? .ufo/waves/round-51/...   (all payload + wave-evidence paths)
$ git cat-file -e HEAD:.ufo/waves/round-51/w51-taskcall.json   -> ABSENT
$ git cat-file -e HEAD:.ufo/waves/round-51/w51-spec.json       -> ABSENT
$ git cat-file -e HEAD:.ufo/waves/round-51/w1/swarm-registry.json -> ABSENT
```

This matters because the C1 counter reads the payload **at a revision**:
`c51_wave_ledger.py` sets `TASKCALL = ".ufo/waves/round-51/w51-taskcall.json"` and `check_l1`
does `show_json(root, rev, TASKCALL)` via `git show <rev>:<path>`, hard-failing with
`"dispatch payload absent at the measured revision"` when it is missing. Therefore:

- **C1/L1 is unsatisfiable until `w51-taskcall.json` is committed together with the
  settlement.** A perfect settlement committed without the payload still fails L1.
- Today that branch is **masked**: the ledger returns earlier on
  `"settlement receipt absent at the measured revision"`, so the payload dependency is not
  currently visible in the counter output. The L1 order is settlement → payload; the payload
  is the second, silent prerequisite.

**The naming convention is load-bearing, and it holds.** `check_l1` compares
`reported = sorted(e["name"] for e in seats if e.get("report"))` against
`committed = basenames of *.md under REPORT_DIR=".ufo/waves/round-51/w1"`. This lint's A4 result
— 48 unique names, each mapping to exactly `<name>.md`, no collisions — is precisely the
invariant that makes that set equality *satisfiable*. Had any two seats shared a name, or any
seat's declared filename differed from its name, L1 could never pass even with a perfect
settlement. Also confirmed: `swarm-registry.json` is excluded by the `.md` suffix filter, so it
cannot be miscounted as a seat report.

## Retained evidence (commands actually run, read-only)

```
$ python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root <lane> --revision 9d13768c...
C1 ledger 0/3 met=False  (met: ledger_checks_passed == 3 of 3)
  L1 FAIL  - settlement receipt absent at the measured revision
  L2 FAIL  - route map absent at the measured revision
  L3 FAIL  - settlement receipt absent at the measured revision
  revision: 9d13768c4fdd0e9a2688d2ecf1616b539cf57658
EXIT=1

$ python3 -B .ufo/waves/round-51/c51_quote_truth.py --root <lane> --revision 9d13768c...
C2 quote-truth 8/8 met=True  (met: conditions_passed == 8 of 8)
  C1_entries_exist .. C8_append_after_mirror all pass
EXIT=0

$ git ls-tree -r --name-only HEAD -- .ufo/waves/round-51/w1/ | grep -c '\.md$'
0
```

So at the lane tip: **C2 met (8/8), C1 honestly unmet (0/3)**, both as the dispatch note
stated. The counter scripts are read-only — `c51_wave_ledger.py` contains no
`write_text`/`open(...,"w")`/`mkdir`/`shutil`/`unlink`/`rename` call.

## Write-scope audit

No seat is authorised to write outside `w1`. 48/48 carry `Write ONLY <abs w1 path>`. Nine
seats name `corpus/`, `scripts/`, `SHONEN.md`, `PROVINCE.md` or `corpus/lessons/round-51.md`,
but every such mention is a **read/inspect** target (audit, parse, apply, read, compare). The
only two write-verb-adjacent hits were false positives: `ExecCensusMirrorValidate` copies
`corpus/` **into `/tmp/r51-mirror/`** (corpus is the read side), and `ReviewAppendOnly` matched
the word `append` inside the phrase "append-only discipline". No seat is told to modify
`considerthese/`, the fleet repo, or a sibling lane.

## Risks

1. **Untracked payload (highest).** C1/L1 silently depends on `w51-taskcall.json` being
   committed at the measured revision. If the wave evidence is committed without it, L1 fails
   on the payload branch even with a correct settlement — and the current counter output would
   not have warned anyone, because settlement absence short-circuits first.
2. **Three dual-axis seats get single-axis prose (F3).** `ConnectorSiblingOverlap`,
   `CriticZeroControl`, `CriticHarm` are asked for both axes but judged in text on
   `operability` only. This is an under-specification, not a broken path.
3. **Declared ceiling equals the batch.** `declaredMaxLanes = maxLanes = 48 = spawn`, so the
   wave sits exactly on its declared ceiling and inside `waveMaxLanes=64`. Any added seat
   would exceed the declared cap while still passing the 32–64 band test — the band check alone
   would not catch it; the `spawn == len(tasks) == maxLanes` agreement does, today, hold.
4. **No defect found in the asked-for checks.** Seat count, uniqueness, histogram and report
   paths all pass 48/48; I am not manufacturing a failure here.

## Tooling

No tool was installed or upgraded; no package manager was invoked. All analysis used the
already-present `jq`, `git`, `sha256sum` and the system `python3` — no new channel needed.
No build, lint, formatter or test was run (leaf: the parent owns the post-integration gate).

## Files read but not written

Read: `w51-taskcall.json`, `w51-spec.json`, `w1/swarm-registry.json`, `contract.json`,
`wave-grant.txt`, `wave-start-utc.txt`, `w51-validator.err`, `c51_wave_ledger.py` (lines 55–148
plus a read-only write-verb scan), both counter runs. `c51_quote_truth.py` was executed but not
read line-by-line — its 8/8 output is reported as printed, not as verified by inspection.
No file was unreadable. `w1/ExecSpecLint.md` did not exist before this write.
