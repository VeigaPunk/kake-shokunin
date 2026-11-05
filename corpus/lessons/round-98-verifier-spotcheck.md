# Round 98 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_zfl)

Lane-round: kake r98 (hyaku run 15, attempt 1). Base `e51328b63690c8aaa78c9c8f3b87d8735c0ccbf7`,
tip `77adb17e9e0225f3cf36f7b74681353bfbe3d26b`. Report `.ufo/reports/round-98/kake.md` (fleet repo).
Driver digest (copied from mutable `.ufo/watchdog.log`):
`2026-11-05T18:39:48-03:00 launch kake round=98 pgid=1367933 driver=hyaku-inline attempt=1`;
`2026-11-05T19:38:28-03:00 complete kake round=98; hyaku-inline attempt=1`.

**Closure verdict: status `ok`, admitted `false`, verdict `rejected-honest-stop`.** C1 is unmet
under its own frozen kill rule (a live reviewer's `disagree`), so not every claim verifies. C2
verifies. No axis is harmed.

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-98/kake.md` | `kake-shokunin f2557a6fe465ded16d43a621c34277f6952f193f` (19:38:01, after tip 19:37:17, before complete 19:38:28) | pass |
| `SHONEN` heading, one line per box | read report §SHONEN | 4 lines: `[~]` 1, `[ ]` 2 (ledger `gap`), `[~]` 3, `[~]` 4 | pass |
| Cited commits exist + ancestry | `git cat-file -e <h>^{commit} && git merge-base --is-ancestor <h> master` for 2db76835, c3eace8b, 4446ce21, 7838981e, 0f48ada0, 76f834aa, 77adb17e, base e51328b6 | all 8 `ok`; linear first-parent chain base→tip | pass |
| Lane pushed, clean | `scripts/hyaku/jj-lane.sh state …/kake-shokunin`; `git status --porcelain` | `branch=master local=remote=77adb17e… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty; `ls-remote origin refs/heads/master` = `77adb17e…` | pass |
| Prompt carries template contract | `diff <(sed -n 1,140p templates/round-prompt.md) <(sed -n 1,140p .ufo/prompts/kake-round-98.md)`; `cmp templates/round-prompt.md ~/Projects/kimi-shokunin/templates/round-prompt.md` | only `{{LANE}}/{{ROUND}}/{{FLEET_ROOT}}/{{AXES}}` substitutions differ; fleet template = canonical; hyaku addendum §6 present | pass |
| Marker? | — | real report, 7 commits, receipts | not a marker → `ok` |

Conformance notes (status-neutral):

- **Gate without a registry row.** The report and LOG.md:3289 call
  `scripts/knowledge_metatext_lint.py` a gate (R98-D1), but `git grep -n -i metatext 77adb17e -- SKILL.md`
  prints nothing. Per PROTOCOL §Gate standard (Delivery), closure grades it **not conformant**
  until its row exists at the registry home (SKILL.md). Its self-test evidence exists
  (`w1/ExecMetaLint/selftest.txt`: `selftest 13/13`) and the red run at `7838981e`
  (`at-master.txt`: `gate_findings=1`), but the "0 after the fix" run is committed only over a
  scratch fixture commit `8631b66c` (`fixture-fixed.txt`), not over the landed `0f48ada0`.
  Plain check: `git show 0f48ada0:corpus/knowledge/revalidation-exchange.md | sed -n 128,131p` shows
  the leaked handoff line gone.
- Report says the C1 tip receipt is at `77adb17e`; `controls/tip-c1.txt` was measured at
  `76f834aa`. `git diff --stat 76f834aa 77adb17e` touches only two receipt files, so the
  SCORECARD bytes are identical; wording defect only.
- The C2 capability row (round 98) was written into the `## Capabilities` table before any
  admitted closure exists. This closure does not admit the round, so that row is now an
  unbacked row by the lane's own C1 definition (the r34/r35/r37/r61/r64 case the round itself
  moved out). Routed below.

## 2. Claims — re-checks

### C1 — calibration (Capabilities table vs admitted closures)

Re-measured (plain, independent of the lane counter):

```
git show f8674006:MANIFEST.json | jq '[.rounds[]|select(.lane=="kake" and .type=="closure" and .admitted==true)|.capabilities_added[]]|length'
→ 48
per-round admitted capability counts (jq, same pin):
20:1 22:1 23:1 25:1 29:1 36:1 39:1 44:1 46:1 50:1 51:1 52:4 55:2 56:3 57:3 58:3 60:1 74:1 75:1 76:1 77:2 78:1 79:2 80:3 81:1 82:1 83:1 85:1 87:1 88:1 90:1 93:1 97:2
Capabilities-table rows by last-cell round (awk over git show <rev>:SCORECARD.md):
e51328b6 → 14 rows: 20 22 23 29 34 35 36 37 39 50 60 61 64 82
4446ce21 → 48 rows, per-round counts identical to the MANIFEST list above
77adb17e → 49 rows (the above + 98:1)
r34/r35/r37/r64 closures: admitted=false rejected-honest-stop; r61: admitted=false rejected-harmed
```

This reproduces the counter's structure: base 9 admitted-round rows + 5 non-admitted rows, one
of the 9 (r20) failing name match → `matched=8 unbacked=6 unlisted=40 mismatches=46`; repair
48/48. Receipts agree (`controls/base-c1.txt` exit 1, `controls/after-c1.txt` `mismatches=0
met=true` exit 0, `controls/tip-c1.txt` `unbacked=1` = the C2 row). Counter digest at tip
`efd59857…` = `controls/instrument-sha256.txt` pin; `git diff --stat c3eace8b 77adb17e` over both
counters, the contract, `frozen/` and `freeze.md` is empty (evidence-verified; registered gate
not executed).

Review conjunct (frozen predicate): `git show 77adb17e:.ufo/waves/round-98/w1/ReviewCapB/verdicts.tsv | cut -f3 | sort | uniq -c`
→ `43 agree`, `2 disagree`; ReviewCapA: 0 files in the tree. I re-checked both disagreements at
`4446ce21`: `id_resolver.py` row claimed "ambiguous" ids, `git show 4446ce21:scripts/id_resolver.py | grep -ci ambiguous` → `0`
(agree with the reviewer); `selftest-tally-counter` row claimed "every registered instrument",
`c56_selftally.py:4` says "ten rows" (agree with the reviewer). The kill rule therefore fires:
**C1 unmet**, as the lane reported. Calibration score stays 3 by the frozen rule.

### C2 — freshness: RFC 5861 stale-serving extensions (capability)

- Landed blob: `git show 0f48ada0:scripts/stale_extensions.py | sha256sum` and the same at
  `77adb17e` → `f43895f1a6b4bbaf806a026d5687c08e622e082110750ad1eb30c4f52079ab0f` (= scored
  sha256 in `controls/after-c2.txt`: `hand=60/60 generated=240/240 refusals=35/35 met=true`, exit 0).
- Counter `c98_stale.py` digest `e0331e56…` and contract `ec077b4f…` at tip = freeze pins
  (evidence-verified; registered gate not executed). Pre-freeze controls: base `candidate=absent`
  exit 1; pos-oracle met; six forgeries met=false (receipts under `controls/ctl-c2-*`).
- Independent plain probe of the landed candidate (my own six cases, `python3 -I` in scratch,
  contract §Decision):

| Input | Expected (contract) | Observed |
|---|---|---|
| `max-age=600, stale-while-revalidate=30`, L=600 A=620, request | serve-stale-revalidate, 20 | `serve-stale-revalidate`, 20, rc 0 |
| same, A=631 | revalidate, 31 | `revalidate`, 31, rc 0 |
| `max-age=600, stale-if-error=1200`, A=900, error 503 | serve-stale-error, 300 | `serve-stale-error`, 300, rc 0 |
| + `must-revalidate` | error-through (prohibited) | `error-through`, 300, rc 0 |
| response sie=1200, request `stale-if-error=60`, network error, A=900 | error-through (request limit first) | `error-through`, 300, rc 0 |
| request `max-stale=5` | refuse | `invalid_input: request directive 'max-stale' is outside this contract`, rc 1 |

6/6 agree. **C2 met** (re-measured blob + probes; counter verdict evidence-verified).

## 3. Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| calibration | improved | Table re-measured 14 → 48 rows matching the 48 admitted entries by round; five non-admitted rows moved to a history table; two over-claims corrected at `0f48ada0`. The claim itself is unmet (review conjunct), so the score stays 3 — the surface is better, the claim did not verify. |
| freshness | improved | C2 met; sourced on S482; capability verified (blob + 6/6 probes). Admission withheld at round level by C1, so no capability is recorded as admitted. |
| operability | unchanged | `git diff e51328b6 77adb17e -- SCORECARD.md` changes no score; no operability surface touched. |

No axis harmed.

## 4. Discernment spot-check (`corpus/lessons/round-98.md` `## Gate`)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S482 RFC 5861 | admit | `curl https://www.rfc-editor.org/rfc/rfc5861.txt` → 200, 10359 B, sha256 `1193f1c8…` (= retained) | agree | Quote "caches MAY serve the response in which it appears after it becomes stale, up to the indicated number of seconds" (20 words) present at lines 107-109 (sentence opens line 106); tier A spec, scope matches the tool. |
| S483 RFC 5861 errata search | admit | `curl -L https://www.rfc-editor.org/errata_search.php?rfc=5861` → 302 → `errata.rfc-editor.org/search/?rfc_number=5861`, 200, 17788 B, sha256 `9603a690…` (= retained) | agree | Quote "Section 3, pg.3 says:" at line 174; status heading "Verified (2)" present; byte-identical to the retained body. |
| Draft `source:` line citing S480 | reject | `git show 77adb17e:corpus/SOURCES.md` row S480 | agree | S480 scope is RFC 9111 §4.3.1/§4.3.3 (validation); the entry's quotes come from §4.2.x/§5.2.x/§1.2.2, held by S469/S457/S461. |
| merge/kake package adoption | reject | `comm -12` of `assimilation/reg-ids` (218) and `staged-ids` (129) | agree | Re-derived 8 collisions `S312 S329 S367 S372 S373 S374 S390 S409`; with no renumber map, appending would collide. |

SOURCES.md re-open: rows `S482`, `S483` exist at tip with `status mined`, opened 2026-11-05;
row count `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` 218 → 220 (matches report).
Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → rc 0,
`kake ok`, W04 duplicate-url warnings only (pre-existing class).

## 5. Trend verdicts

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | improved | S482/S483 re-opened byte-identical; `corpus/knowledge/stale-extensions.md` new; working RFC 5861 decision tool verified. |
| quality | improved | Capabilities table realigned to the closure record (re-measured 48/48); 2 over-claiming rows corrected; R98-D1 leak removed (line gone at `0f48ada0`). The new lint gate is not registry-conformant yet (routed). |
| discernment | improved | The lane's own reviewer rejected 2 L1-written rows and the lane recorded C1 unmet instead of re-scoring; non-author sample 4/4 agree (2 admits, 2 rejects). |

## 6. Routed defects (lane fixes next round)

- **R98-C1 (gate registry):** add a SKILL.md gate-registry row for `scripts/knowledge_metatext_lint.py`
  (entry command, verdict map, self-test spelling and tally 13/13, write scope) and commit a run at
  the landed revision (`gate_findings=0` at `0f48ada0` or later); until then the gate is not conformant.
- **R98-C2 (unbacked capability row):** round 98 is not admitted, so the "Stale-serving extensions
  decision, contract v1" row in `## Capabilities` has no admitted closure. Move it to the
  "Capability rows without an admitted closure" table (or re-earn admission in a later round with
  a closure that records it); the C1 counter at tip reads `unbacked=1` for exactly this row.
- **R98-C3 (report wording):** the C1 tip receipt is at `76f834aa`, not `77adb17e`; cite the
  measured revision.
- C1 re-entry: the repaired table is in place; a later round can re-claim C1 with both review
  seats live and the corrected rows judged. Lane-owned routes R98-1…R98-5 stand as filed.

SHONEN: box 2 is `gap`; boxes 1, 3, 4 are `[~]` — not fully checkable by a non-author from this
round; no promotion note for the operator.
