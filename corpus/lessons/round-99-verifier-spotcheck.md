# Round 99 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_zfl)

Lane-round: kake r99 (hyaku run 15, attempt 1). Base `cde408e5817bf1376c701d8decc5469fa82b2985`,
tip `dc89a9064c10ded88f958128acb9702bdf033586`. Report `.ufo/reports/round-99/kake.md` (fleet repo,
commit `4dad2b1355a410a33f7ea3ae212768b93ba578d1`).
Driver digest (copied from mutable `.ufo/watchdog.log`):
`2026-11-05T19:42:19-03:00 launch kake round=99 pgid=1258768 driver=hyaku-inline attempt=1`;
`2026-11-05T22:17:29-03:00 complete kake round=99; hyaku-inline attempt=1`.

**Closure verdict: status `ok`, admitted `false`, verdict `rejected-honest-stop`.** C1 is unmet
under its own frozen kill rule (live `disagree` verdicts from ReviewRegA and ReviewRegB on three
repair rows), and I confirmed each disagreement against the code. So not every claim verifies.
C2 is met on its frozen predicate (evidence-verified). No axis is harmed. The lane recorded C1 as
unmet itself; this is an honest stop, not a harm.

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by the lane identity | `git log --format='%an <%ae> %H %ad' -- .ufo/reports/round-99/kake.md` | `kake-shokunin <kake@shokunin.local> 4dad2b13… Thu Nov 5 22:05:56 2026 -0300`; on `origin/main` | pass |
| `SHONEN` heading, one line per box | read report lines 136-141 | 4 lines (`[~]`, `[ ]`, `[~]`, `[~]`) for the 4 seed boxes | pass |
| 9 cited commits + base exist and are ancestors of `master` | `git cat-file -e <h>^{commit} && git merge-base --is-ancestor <h> master` for each hash in the report's Landed table and the base | all 10 `ok` | pass |
| Lane pushed, no leftovers | `scripts/hyaku/jj-lane.sh state …/kake-shokunin`; `git status --porcelain` | `local=remote=dc89a906… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty; `ls-remote origin refs/heads/master` = `dc89a906…` | pass |
| Report lands last | `git log -1 --format='%cd' 4dad2b13` vs lane tip | report committer date 22:09:26, lane tip `dc89a906` 22:08:23; report cites `dc89a906` | pass (author date 22:05:56 predates `4f2b32da`/`dc89a906`: the report commit was rewritten locally before push; content cites the final tip, so not a defect) |
| Prompt carries the template contract | `grep -n '^#' .ufo/prompts/kake-round-99.md` | §1 MISSION/AXES, §2 claims, §2b frontier, §3 L2 floor (≥8, one batched call), §4 report path/sections/SHONEN/marker rule, §5 commit-then-push, push scope, L0 channel, §6 hyaku addendum | pass |
| Frozen instruments unchanged after the freeze | `git log ab35eace..dc89a906 -- freeze.md c99_registry.py c99_fresh304.py fresh304-contract.md frozen/`; `sha256sum` of tip blobs vs `controls/instrument-sha256.txt` | no commits; `0f39bbbc…` (c99_registry) and `d13bba5d…` (c99_fresh304) match the pin | pass |

Conformance defects (status-neutral):
- D1: §3's minimum role split names `1× planner`; the wave had none ("Planner seat: held by the L1
  (the validator rejects `planner`)"). The planner role was not filled by a seat. This is a template
  vs. validator conflict and goes to the operator; it is not a lane fault.
- D2: SentinelScope W1 (CRITICAL): `c99_fresh304.py run_candidate()` leaves procfs unmasked, so a
  candidate can import the counter's own oracle. The lane mitigated this for the landed blob only
  (see C2). The counter itself still has the hole (routed R99-9).

## 2. Claims — re-checks

### C1 — calibration (SKILL.md tool registry vs committed `scripts/` tools)

Re-measured (plain, my own commands; I did not run the lane's gate):
- Tool population: `git ls-tree --name-only <rev> scripts/` filtered to blobs → `cde408e5`: 54,
  `9d341d1b`: 54, `998b6d5f`: 55, `dc89a906`: 55. This matches the counter's `tools=54/54/55`.
- Repair rows: `git diff 2345e309 9d341d1b -- SKILL.md | grep '^+|' | grep -vE '^\+\|(---| Name)' | wc -l`
  → `26`. Their first column, compared with `comm` against the base `scripts/` listing, gives 0 names
  that are not committed tools.
- A looser presence test is any SKILL.md table row naming the tool. It gives 10 unlisted at base and
  0 at `9d341d1b`/tip. The counter's stricter conformant-row test gives 26 → 0. Both directions agree.
- Review conjunct: `cut -f2 w1/ReviewReg{A,B}/verdicts.tsv | sort | uniq -c` → A `24 agree / 2
  disagree`, B `23 agree / 3 disagree`. The disputed rows are `quote_class.py`, `wave_seat_record.py`
  (both seats) and `sitemap_audit_selftest.py` (B). This matches the report.
- I confirmed each disagreement from code:
  - `quote_class.py`: its row at `9d341d1b` claims `64 usage`. Line 142 is `ap.error(...)`, which
    exits 2, so the `return 64` at line 143 is unreachable.
  - `wave_seat_record.py`: its row claims `64 usage`. The code only returns 2 or 0 (lines 51/82), and
    argparse usage faults exit 2.
  - `sitemap_audit_selftest.py`: its row claims a `2` setup fault. The runner's `main` returns 64 at
    lines 1538-1550, 1 or 0 at 1585, and never 2.
  - Frozen predicate (`freeze.md` lines 35-37): one live `disagree` → unmet. **C1 unmet: verified.**
- Post-review corrections at the tip: I re-read the three rows at `dc89a906`. `quote_class.py` now
  reads "`2` unreadable input or usage fault … the `return 64` after `ap.error` is unreachable".
  `wave_seat_record.py` now reads "`2` … argparse usage fault (… `64 usage` is not reachable)".
  `sitemap_audit_selftest.py` now reads "`64` usage or tool not found; `2` not returned by the
  runner". Each one now matches the code.
- Evidence-verified: committed receipts `controls/base-c1.txt` (`unlisted=26 … met=false`, 26
  `unlisted` lines, exit=1), `controls/after-c1.txt` (`revision=9d341d1b… unlisted=0 … met=true`,
  exit=0), `controls/tip-c1-at-c2.txt` (`tools=55 … met=true` at `998b6d5f`), and
  `controls/ctl-c1-selftest.txt` (`selftest 20/20`, exit=0).

### C2 — freshness (HOLD 10): 304 freshening decision, contract v1 (capability, sourced S484)

This claim rests on the lane's gate `c99_fresh304.py`, so I verified its committed evidence and did
not run it (§Gate standard, Closure consequence):
- Base `controls/base-c2.txt`: `revision=cde408e5… candidate=absent met=false`, exit=1.
- After `controls/after-c2.txt`: `revision=998b6d5f… candidate=present sha256=db3a0f12…
  hand=50/50 generated=240/240 refusals=47/47 seed=2576051551 met=true`, exit=0.
  `controls/after-c2-10seeds.txt` gives 10 lines, all `met=true`.
- `controls/c2-landed-vs-oracle-twin-generator.txt` (independent generator): `inputs=2400
  disagreements=0`.
- Re-measured digests: `git show 998b6d5f:scripts/freshen_304.py | sha256sum` and the same at
  `dc89a906` both give `db3a0f12b91a5a54409ebafcf800204011385a523ff4da9b897b71dd7c0c1d4f`. The
  scored blob equals the landed blob and has not changed since.
- W1 mitigation re-checked: the only imports in `git show dc89a906:scripts/freshen_304.py` are
  `json`, `re`, `sys` (lines 52-54). A grep for `open(|/proc|subprocess|os.|pathlib|__import__|exec(|eval(`
  finds nothing. This blob does not use the oracle-read vector.
- Sourced: `corpus/knowledge/freshening-304.md` opens with the `source: S484, S485 …` / `verified-at`
  / `recheck` trio and cites S484 twice.
- Caveats (routed by the lane, which I agree with):
  - The counter population is blind to the seven CriticClaims classes (R99-8).
  - The runner is not isolated (R99-9).
  - Contract v1 departs from the RFC at F1/F2/F10 (R99-10). These are bounded in the entry's
    known-limits.
- **C2 met: evidence-verified.**

Owned-axis harm check: `git diff cde408e5 dc89a906 -- SCORECARD.md` adds the Round 99 section and
moves the r98 stale-extensions row into the no-admitted-closure table (R98-C2). No axis score changes
(operability 10, freshness 10, calibration 3 at tip lines 17-19). SHONEN.md, PROVINCE.md and AGENTS.md
are not in the diff.

## 3. Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| calibration | improved | Claim C1 is **unmet** on its frozen predicate. The axis state still improved: 26 → 0 unlisted tools, and the three false rows now match the code at the tip (I re-read each one). The score stays 3. |
| freshness | improved | C2 met on the frozen predicate (evidence-verified, digest re-measured). The capability is not entered because the round is not admitted. |
| operability | unchanged | Not claimed; score 10 unchanged; no row regressed. |

## 4. Discernment spot-check (`corpus/lessons/round-99.md` `## Gate`)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S484 RFC 9111 §3.1/§3.2/§4.3.4 | admit (spec, A) | `curl https://www.rfc-editor.org/rfc/rfc9111.txt` → HTTP 200, 84477 bytes, sha256 `aeb52adb…` (= retained body and the row's anchor) | agree | Quote 1 is verbatim at lines 375-377 ("the cache MUST add each header field in the provided response to the stored response, replacing field values that are already present", 22 words). Quotes 3 and 4 are verbatim at lines 971-972 and 976-977. The §4.3.4 heading is at line 951. Primary spec, and the scope is narrow. |
| S485 erratum EID 9185 | admit (dataset, A) | `curl -L https://www.rfc-editor.org/errata/eid9185` → 200 at `errata.rfc-editor.org/eid9185/`, sha256 `83c3b795…` (= retained) | agree | The flattened text reads "Status: Reported Type: Technical … Reported By: Daniel Fox Franke Date Reported: 2026-09-24 Section 4.3.4". This matches the row and the quote «Status: Reported». The scope is limited to erratum status, and tier A is correct for that scope. |
| merge/kake package adoption | reject | `/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md` (129 rows); `.ufo/waves/round-99/assimilation/collisions` (8 ids) | agree | S312 exists on both sides with different scope cells: staged "Baidu's own list of the reasons a **mobile page fails…**" vs registry "**Baidu's own list … desktop page** — the page-side rendering cause…". No renumber map is present (the only `*renumber*` file is a knowledge note), so adopting the package would collide ids. The flip condition is well-formed. |

SOURCES.md row re-opened: S484 (row line 230). The ≤25-word located quote checks out as above. The
row's anchor line ranges (338-366, 369-414, 951-988) match the re-fetched body.
Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → rc=0, `kake ok`,
41 W04 warnings (count with `grep -c W04`). `controls/census-before.txt` has 40; the new one is S484 (an
existing duplicate-URL class). Rows (`git show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`):
220 at `cde408e5` → 222 at `dc89a906`. This matches the report.

## 5. Trend verdicts

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | improved | New RFC 9111 §4.3.4/§3.2 ground: mined rows S484/S485 (A), new knowledge entry `corpus/knowledge/freshening-304.md` with the provenance trio. The ground was named open in the README frontier. |
| quality | improved | All 55 committed tools are registered, and the three false rows were corrected and re-read against code. The C2 candidate matches the reference over 2400 independent inputs. R98-C1/C2 are closed (`metatext-lint-at-master.txt`, `r98c2-captable-after-move.txt`). |
| discernment | improved | 3/3 gate decisions sampled were upheld by me, including a reject with a verified collision. The lane recorded C1 as unmet instead of re-scoring it. Mistake 5 (rows written from docstrings) was mined, with criterion R99-B shown red. |

## 6. Routed defects (lane fixes next round)

- R99-C1: C1 re-entry (lane R99-11). Every registry verdict-map cell must be derived from code paths
  (`return`/`sys.exit`/`ap.error`), never from docstrings. The three docstrings that still claim
  unreachable codes (`quote_class.py`, `wave_seat_record.py`, `sitemap_audit_selftest.py`) should be
  fixed or the gap recorded. The counter's junk-prose limit stays covered only by the review conjunct.
- R99-C2: isolate `c99_fresh304.py run_candidate()` (procfs and shared work dir, SentinelScope
  W1–W4) before any later counter run is cited as capability evidence. The mitigation for this round
  covers blob `db3a0f12…` only.
- R99-C3: contract v2 for the RFC departures F1/F2/F10 and LC6 case sensitivity (lane R99-10). Add
  the seven CriticClaims escape classes to the counter population (R99-8). Mutation survivors:
  registry 10, fresh304 6 (R99-12).
- Operator note (not a lane fault): the L2 template requires `1× planner`, but the wave validator
  rejects `planner`. Reconcile one with the other. SHONEN box 2 is `[ ]` (gap), so the SHONEN boxes
  are not fully checkable by a non-author and there is nothing to promote.
