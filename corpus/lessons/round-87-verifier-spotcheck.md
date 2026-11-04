author: hyaku closure (non-author integrator, @m_zfl)
round: kake 87
date: 2026-11-04
report: .ufo/reports/round-87/kake.md
lane_base: 86ca7803fd964db7ae2a628c7e9048741c78a45f
lane_carrier_head: fbecc02033ca2be36e9f176dfedede224c79f5a9
lane_head_closed: 992461d3b26d557a600666b5ae16cb42447ca6ae

# Round 87 verifier spot-check — kake (hyaku closure, non-author)

Re-measurements below were run by this integrator on committed bytes. Lane-owned
counters and selftests were NOT executed; their committed receipts were read and
their revision bindings checked (§Gate standard, "Two evidences"). Scratch runs
lived in `/tmp/kake-r87-verify` and were used only to re-execute the committed
tool on committed fixtures; no evidence pointer here depends on that directory.

## Conformance results

- Report commit: `846e2633d4a664e8e3b327d26c6be5475bc30049`, author `kake-shokunin`,
  `2026-11-04 15:32:05 -0300`, in the fleet repo. Lane commit `992461d3` is
  `15:31:01 -0300`, so the report lands after the cited commit and before the driver
  completion line (`15:32:51`). ✓
- Driver digest (`.ufo/watchdog.log`, copied to closure notes):
  `2026-11-04T15:16:32-03:00 launch kake round=87 pgid=257246 driver=hyaku-inline attempt=1`
  and `2026-11-04T15:32:51-03:00 complete kake round=87; hyaku-inline attempt=1`. ✓
- `SHONEN` heading present with one line per box (4 boxes in `SHONEN.md` at
  `992461d3`, 4 report lines: `[~]`, `[ ]`, `[~]`, `[~]`). No `[x]` written by the
  lane. ✓
- Cited lane commits, each checked with `git merge-base --is-ancestor <hash> master`
  (branch ref, lane repo `kake-shokunin`): `86ca7803` ✓, `58fee726` ✓, `0f5739f9` ✓,
  `fbecc020` ✓, `992461d3` ✓ (all ancestors of `master`).
- Push state: `scripts/hyaku/jj-lane.sh state …kake-shokunin` →
  `branch=master local=992461d3… remote=992461d3… ahead=0 behind=0`;
  `git ls-remote origin refs/heads/master` → `992461d3…`;
  `git status --porcelain` in the lane → empty. ✓
- Dispatched prompt `.ufo/prompts/kake-round-87.md` is tracked (commit `5c4c9962`).
  Grep-level check of the template contract items (round-level §1–§5 and the
  child-lane report path, commit-before-report, SHONEN heading, commit-hash citation,
  write scope) found each present. A byte-level re-render against the operator-side
  template was not performed by this integrator. ✓ (grep only)
- Misroot sweep (`controls/fleet-misroot-sweep.txt`) was not re-run here. Fleet
  root currently shows unrelated dirty entries (`.scratch/*`, `after`) that are not
  round-87 lane work and were left untouched.
- Status-neutral conformance notes (not marker predicates):
  (a) round shape was one validated v1 wave of 12 seats under host mapping, not a
  literal ≥8-L2 batched AgentSwarm call; the literal L2-planner conflict (D84-4) is
  open and operator-owned; (b) "stale-lane" line states no open mission and does not
  grade progressing/silent — none was open, so no grading was required.

## Per-claim re-check

### C1 calibration — historical gate-agreement metadata (re-measured, plain)

Before: `git show 86ca7803:corpus/knowledge/gate-agreement-ledger.json` → file absent
(`base-no-ledger`). Eight expected rows are therefore absent: 8 of 8 mismatches,
population 8. This matches the lane's `controls/base-c1.txt`
(`mismatches 8, population 8, met false, exit 1`).

After (committed bytes at `992461d3`):
- `git show 992461d3:corpus/knowledge/gate-agreement-ledger.json | jq length` → `8`.
- `jq -S . ledger.json | diff - <(jq -S . expected-ledger.json)` → no output
  (sorted-key JSON identical).
- Snapshot digests versus the protocol-lane origin closure files at `86ca7803`:
  - `corpus/lessons/round-84-verifier-spotcheck.md` `80f48887…` = snapshot `80f48887…` ✓
  - `corpus/lessons/round-85-verifier-spotcheck.md` `948c3168…` = snapshot `948c3168…` ✓
  - `corpus/lessons/round-86-verifier-spotcheck.md` `47499686…` = snapshot `47499686…` ✓
- Each of the 8 ledger rows checked against the origin closure tables (decision and
  outside verdict): r84 S457 admit/agree, §4.1 reject/agree, §5.2.2.2 reject/agree;
  r85 S458 admit/agree, blanket reorder reject/agree; r86 S459 admit/agree,
  S461 admit/agree, RFC 7234 minimum-duplicate reject/agree. All 8 match. ✓

Result: **met, re-measured 8→0**, with fidelity to closure-owned records verified
by this integrator. The lane's own caveat stands: this proves record fidelity, not
that a calibration assessment was performed or that decision accuracy improved.
Score held at 2 (`SCORECARD.md`, `git diff` additive only).

### C2 freshness capability — conservative current-age arithmetic (re-measured, plain)

Before: `git show 86ca7803:scripts/cache_current_age.py` → absent. 0/17 (lane
`base-c2.txt`: `cases 0/17`, exit 1).

After: extracted `scripts/cache_current_age.py` and `.ufo/waves/round-87/age-cases.json`
from `992461d3` and ran each of the 17 frozen inputs through `python3 -B` on stdin.
Command: `printf '%s' "$input" | python3 -B cache_current_age.py`, compared with the
frozen expected output (exit 0) or expected exit code (exit 1).
- Observed: `case 1..12 exit=0 PASS`, `case 13..17 exit=1 PASS`; **17/17 PASS**, 0 FAIL.
- Independent recompute (my own formula, not the tool's): `apparent_age =
  max(0, response_time-date_value)`, `response_delay = response_time-request_time`,
  `corrected_age_value = age_value+response_delay`, `corrected_initial_age =
  max(apparent_age, corrected_age_value)`, `current_age = corrected_initial_age +
  (now-response_time)` over the 12 exit-0 cases → **0 mismatches**.
- `TMPDIR=/tmp/kake-r87-verify python3 -B cache_current_age.py --selftest` →
  `selftest: 61 isolated CLI fixtures passed`, exit 0 (re-executed plain; the
  committed `controls/decoder-selftest.txt` agrees).
- Frozen identity: `git diff --stat 58fee726 fbecc020 -- .ufo/waves/round-87/{count.py,
  expected-ledger.json,age-cases.json,contract.md,snapshots}` → empty (unchanged).
- Edge probes (my own, not in the frozen set):
  - valid object → exit 0, six integer terms;
  - `"extra":1` key → `invalid_input: unknown input key`, exit 1;
  - `"age_value":3.0` and `"date_value":7.0` → exit 1 (non-int rejected), **but**
    the message reads `… must be an integer, not boolean` (misleading wording; see
    routed defect R2).

Result: **met, re-measured 0/17→17/17**, bounded to supplied-integer-time
arithmetic. No Date parser, network/clock, storage/reuse or browser claim is made or
checked here.

### Lane-owned gates — evidence verified, not executed

- `controls/counter-selftest.txt`: `selftest 6/6` (C1 counter).
- `controls/decoder-selftest.txt`: `selftest: 61 isolated CLI fixtures passed`, exit 0.
- `controls/integrated-trial.txt`: retained real GET replay, six integer terms
  matching, exit 0; `w1/ExecTrial/trial-record.json` + `trial-run.json` present
  (this integrator did not re-fetch ds4cc.com).
- `controls/base-*.txt` and `after-*-carrier.txt`: revision-bound to `86ca7803` and
  `fbecc020` respectively; the measured carrier is the last production change
  (`git diff --name-status fbecc020 992461d3 | grep -v .ufo/waves` → only `LOG.md`,
  `SCORECARD.md`, `corpus/lessons/round-87.md`).
- `count.py` was not executed by this integrator.

## Sources & frontier re-check

- `git show <rev>:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`:
  `86ca7803` = **199**, `992461d3` = **200**. ✓ matches report.
- `git ls-tree -r --name-only <rev> -- corpus/knowledge | grep -c '\.md$'`:
  `86ca7803` = **73**, `992461d3` = **74**. ✓ matches report. The ledger JSON is
  excluded from this count, as the report states.
- `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` →
  24 × `W04` lines (S033…S462), last line `kake ok …/corpus/SOURCES.md`, `exit: 0`.
  Pre-round was 23 W04; S462's cross-scope duplicate URL is the disclosed increment. ✓

## Per-axis verdicts (owned axes; SCORECARD additive-only, no score cell changed)

| Axis | Verdict | Basis |
|---|---|---|
| calibration | **improved (bounded)** | C1 re-measured 8→0 with closure-record fidelity verified. Bounded to record fidelity: score held 2, no decision-accuracy credit (same grading basis as the r85 calibration precedent). |
| freshness | **improved (bounded)** | C2 capability re-measured 0/17→17/17 with independent recompute; capability row entered SCORECARD round 87. Score held 10 at saturation. Axis-fit is a bounded capability move, as in r86. |
| operability | **unchanged** | No claim targeted it. `git diff --name-status 86ca7803 992461d3 -- scripts/` shows only the addition `scripts/cache_current_age.py`; no existing script modified; no harm observed. |

No owned axis harmed.

## Spot-check table (LEARNING.md discernment, from `corpus/lessons/round-87.md` `## Gate`)

| Item | Decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| S462 conservative age arithmetic | admit, A/mined | `GET https://httpwg.org/specs/rfc9111.html` → 200, 178573 B, 2026-11-04. Located in §4.2.3 (txt lines 771–775). Quote `"The corrected_age_value MAY be used as the corrected_initial_age."` (8 words): present byte-exact in the HTML text and in `GET https://www.rfc-editor.org/rfc/rfc9111.txt` (84477 B). | **agree** | The quote sits after the first equation block; the next paragraph says "corrected_initial_age can be calculated more conservatively as" `max(apparent_age, corrected_age_value)` (txt 775). That supports the conservative-max profile. Tier A (IETF spec) is correct for the scope "six-term arithmetic on supplied integer times". The row's teaches line does not claim header extraction or reuse. |
| "current_age alone proves reuse" | reject (proposition) | `GET https://www.rfc-editor.org/rfc/rfc9111.txt` (84477 B), §4.2 Freshness, txt line 621. Quote `response_is_fresh = (freshness_lifetime > current_age)` (5 tokens): byte-exact. | **agree** | The text continues "freshness_lifetime is defined in Section 4.2.1", so freshness needs a lifetime and age alone cannot prove reuse. The gate's reject is correct; the flip condition (a separately bounded applicable-reuse procedure) is reasonable. |
| SOURCES row S462 (new, ≤25-word quote check) | (registry write) | Row read at `992461d3`: 13 columns; anchor `§4.2.3`; `used-by corpus/knowledge/cache-current-age.md` (exists); `recheck 180d`. Census validate exit 0. | **agree** | Row is a claim and its quote re-opened above. Columns, tier, and scope are consistent with CORPUS.md contract v1. |

Gate sample coverage: 2 of 2 candidates (1 admit, 1 reject). Both agree.

## Trend verdicts (closure)

- **expansion: improved** — one provenance-complete knowledge entry (`cache-current-age.md`,
  opens with `source:`/`verified-at:`/`recheck:`) citing mined A-row S462 on frontier
  ground (supplied-time Age arithmetic). Knowledge `.md` 73→74 re-derived. The ledger
  JSON earns no expansion credit.
- **quality: improved (bounded)** — the new reader is verified, not just asserted:
  independent recompute 0 mismatches, 61-fixture selftest green, quote re-opened
  byte-exact. Defects stay on the routed queue, not hidden: the JSON under
  `knowledge/` has no provenance trio (R1), the diagnostic wording (R2), and an
  ephemeral recheck path (R3). Nothing in the admitted set fails its re-check.
- **discernment: improved** — the outside spot-check agrees with the gate on the
  sampled admit (S462) and the sampled reject. The report's "unchanged pending outside
  spot-check" is superseded by this file.

## Routed defects (lane fixes next round; status-neutral)

- **R1 (kake, corpus layout).** `corpus/knowledge/gate-agreement-ledger.json` sits in
  `knowledge/`, which CORPUS.md defines as sourced domain notes. A JSON file cannot
  open with `source:`/`verified-at:`/`recheck:`. Relocate it to a metadata path or
  add a sourced companion entry. Note: the frozen counter reads this path, so the move
  must go through the lane's own next-round instrument, never by editing the frozen
  counter.
- **R2 (kake, tool diagnostic).** `scripts/cache_current_age.py` reports a non-integer
  number as `… must be an integer, not boolean` (observed for `date_value: 7.0`, exit 1).
  Exit code is correct; the message is wrong. Fix with a red-before test.
- **R3 (kake, recheck hygiene).** The `cache-current-age.md` recheck line uses
  `TMPDIR=/fast/scratch/hyaku/kake-r87/L1`, an ephemeral scratch path. Use a
  repo-relative or `mktemp` form.
- **Carried, not new:** frozen counter Python equality accepts `3.0` and `True`;
  C1 loads the C2 fixture at startup (both disclosed); D84-2/3 and operator-owned D84-4
  remain open.

## Operator notes (not lane defects)

- `MISSION.md` lists kake axes as `operability + freshness`. The lane's SCORECARD also
  scores calibration, added as a round-54 sub-axis (MISSION allows lane axis add on
  evidence). Operator may reflect this in MISSION.
- Calibration fit: AXES defines calibration as self-assessment against observed state.
  C1 measures record fidelity of closure-owned verdicts. Graded `improved (bounded)`
  under the r85 precedent; operator may rule on axis fit.
- SHONEN: boxes 1 and 3 and 4 remain `[~]` (lane-asserted). Box 2 remains `[ ]`
  (historical round-47 receipt gap, per the lane). Not checkable `[x]` by this
  integrator in this pass; promotion is operator-owned.

## Closure ruling

Status **ok** (real, substantive report with pushed carrier). Both claims verify on
re-measurement; no owned axis harmed; discernment agrees on both sampled decisions.
**admitted = true**, verdict `admitted`.
