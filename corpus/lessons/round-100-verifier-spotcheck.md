# Round 100 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_zfl)

Lane-round: kake r100 (hyaku run 15, attempt 2 after a dead attempt 1). Base
`3989618d9f8310b2eb5fb456aa7c4e58fb0b5ff5`, tip `72a6cd6018b68a7f633e216bdcb164c2eec8d22e`. Report
`.ufo/reports/round-100/kake.md` (fleet repo, commit `747be9716fc52f407d7639df9835cdf6da41039f`).
Driver digest (copied from the mutable `.ufo/watchdog.log`):
- `2026-11-05T22:23:37-03:00 launch kake round=100 pgid=3864071 driver=hyaku-inline attempt=1`
- `2026-11-05T23:31:17-03:00 lane-dead-no-report kake round=100; retry same round (hyaku-inline attempt=1: L1 ended without a landed report: FAIL report_of (missing, unchanged, no SHONEN heading, or < 400B): .ufo/reports/round-100/kake.md)`
- `2026-11-05T23:31:19-03:00 launch kake round=100 pgid=2173724 driver=hyaku-inline attempt=2`
- `2026-11-05T23:50:38-03:00 complete kake round=100; hyaku-inline attempt=2`

**Closure verdict: status `ok`, admitted `true`, verdict `admitted`.** Both claims verify.
- C1 (calibration 3 → 4) I re-measured with plain commands and confirmed against the code.
- C2 (freshness HOLD 10, capability: 304 freshening contract v2) I verified from the gate's committed
  evidence, with plain digest and independence checks.
- No owned axis is harmed.
- The instrument weaknesses the attack seats found (counters that a hostile tree could drive to
  `met=true`) are real. They are routed. My checks found no sign that the landed bytes used them.

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by the lane identity | `git log --format='%H %an %ad \| %cn %cd' --date=iso -- .ufo/reports/round-100/kake.md` | `747be971… kake-shokunin 2026-11-05 23:31:19 -0300 \| kake-shokunin 2026-11-05 23:49:44 -0300`; worktree clean for that path; 9987 bytes | pass |
| `SHONEN` heading, one line per box | read report lines 113-122 | one `## SHONEN` heading; 4 box lines (`[~]`, `[ ]`, `[~]`, `[~]`) | pass |
| 6 cited commits exist and are ancestors of `master` | `git -C kake-shokunin merge-base --is-ancestor <h> master` for `d7b73d16 69cdc1eb e84a1871 06c81f08 2bdec5f8 72a6cd60` | all 6 `anc-ok`; `git log 3989618d..72a6cd60` lists exactly these 6 commits, all by `kake-shokunin` | pass |
| Lane pushed, no leftovers | `scripts/hyaku/jj-lane.sh state …/kake-shokunin`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `local=remote=72a6cd60… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; ls-remote `72a6cd60…` | pass |
| Report lands last | committer date of `747be971` (23:49:44) vs lane tip `72a6cd60` (23:48:29) | report committed after the tip and cites it. The author date 23:31:19 is the attempt-2 launch second, so the commit was rewritten before push. Its content cites the final tip, so this is not a defect. | pass |
| Prompt carries the template contract | `grep -n '^#' .ufo/prompts/kake-round-100.md` | §1 MISSION/AXES, §2 claims (1-3, falsifiable), §2b frontier, §3 L2 floor (≥8, one batched call), §4 report path/sections/SHONEN/marker rule, §5 commit-then-push, push scope, L0 side channel, §6 hyaku addendum, §7 scratch discipline | pass |
| Frozen instruments unchanged after the freeze | `git log 69cdc1eb..72a6cd60 -- freeze.md c100_registry.py c100_fresh304.py fresh304-contract-v2.md frozen/ controls.sh build_frozen.py c1_repair_fixture.py`; `sha256sum` of tip blobs vs `controls/instrument-sha256.txt` | no commits. The tip digests of `c100_registry.py` (`c25d981e…`), `c100_fresh304.py` (`e7dff63b…`), `fresh304-contract-v2.md` (`343b3a55…`), `controls.sh` (`eadfdfe1…`), `frozen/pos-oracle.py` (`be234945…`) and `frozen/neg-theft.py` (`8a5f0000…`) match the pin. | pass |

Conformance defects (status-neutral):
- D1: Seat yield was 13/14. ScribeLesson was lost with the crashed attempt-1 orchestrator. Every
  `w1-results.json` output is null, so the results come only from the seat reports on disk. Attempt
  1 died after dispatch (`lane-dead-no-report`), and attempt 2 integrated its inherited outputs.
  The report discloses this.
- D2: The planner seat was held by the L1, not by a separate seat. This is the same template vs.
  validator conflict as r99 D1, and it goes to the operator.
- D3: The instruments can be gamed (routed by the lane as R100-1…R100-4 and criterion R100-A):
  - CriticClaims found `c1_escapes=6 c2_escapes=5 framing_defects=3`.
  - SentinelScope found `vectors=28 escapes=0 cross_case_leaks=2`. Its R1/R2/R12 receipts show a
    hostile committed tree can reach C1 `met=true`.
  - MutCounters left 11 survivors: registry 8/15 killed, fresh304 13/17 killed.
  - These findings are about counter integrity, not about the landed bytes. §2 gives the
    independent checks that rule out their use here.

## 2. Claims — re-checks

### C1 — calibration: one SKILL.md registry row per committed `scripts/` tool, verdict maps executed

Re-measured (plain, my own commands; I did not run `c100_registry.py`):
- Tool population (`git ls-tree <rev> scripts/ | awk '$2=="blob"' | wc -l`): 55 at `3989618d`,
  `e84a1871`, `06c81f08` and `72a6cd60`. This matches the counter's `tools=55`.
- Duplicated tools. I took the entry-command cell (column 3) of every table row outside fences,
  extracted the `python3 [-B] scripts/X.py` invocations, and listed the tools named by two or more
  rows (`uniq -c | awk '$1>1'`):
  - At `3989618d`: `cache_key_conformance live_snapshot response_snapshot robots_audit
    source_snapshot x_robots_tag_audit`, plus `link_preview_audit`, which is invoked by both the
    decision-table row at SKILL.md:1014 and its registry row. The fenced history block's header
    confirms `cache_key.py` as the seventh duplicate, which my regex did not catch because that row
    invokes the tool through a `printf … \|` pipe.
  - At `72a6cd60`: only `link_preview_audit`. Its line-1014 row sits under the header `| Situation |
    What to check / action | Evidence command … |`, which is not a registry table. The registry
    header is `| Name | Kind | Entry command | Verdict map | …` (line 1054). So among registry rows
    the plain count goes from 7 duplicated tools to 0.
- The 7 removed rows are verbatim:
  - `git diff 3989618d e84a1871 -- SKILL.md`: the 7 `-|` lines and the 7 `+|` lines inside the new
    fenced `## Round 100 — superseded registry rows` block are byte-identical after sort (`cmp` →
    identical).
  - For each of the 7 tools, a grep of the tip for rows that invoke it outside fences gives exactly
    1.
- The ordering rule holds. `git show e84a1871:SKILL.md | sha256sum` gives `397b6dec…`, which equals
  `controls/fixture-c1-pos-SKILL.sha256`. After `e84a1871`, SKILL.md changes only once, in
  `06c81f08`: the `freshen_304.py` row is updated in place. No second row was added.
- The repair touched no tool (`git diff --stat 3989618d e84a1871 -- scripts/` is empty). A
  `git grep -e zz-bogus -e getpid e84a1871 -- scripts/` finds nothing (rc=1). So the probe-gaming
  vectors R1/R2 are absent from the scored tree.
- I checked the three rows the base counter flagged against the code at the tip:
  - `response_snapshot.py`: argparse `SystemExit` → `return 0 if exc.code == 0 else 64` (lines
    227-229). The row names `64` usage. Match.
  - `source_snapshot.py`: plain `ap.parse_args` exits 2 on an unknown flag (line 266), and the code
    also has `return 2` at 273/276. The row names `2` bad input. Match.
  - `robots_audit.py`: `main` returns `EXIT_USAGE = 64` when argv is not `--manifest PATH` (lines
    112, 654-659). The row names `64` usage. The kept self-test `scripts/robots_audit_selftest.py`
    exists at the tip, which closes R99-6.
- Review conjunct: `cut -f2 w1/ReviewReg{A,B}/verdicts.tsv | sort | uniq -c` gives A `8 agree` and
  B `8 agree`. Both files cover the 8 frozen units (7 kept rows plus the history block), with no
  `disagree`. ExecRegProbe re-implemented the count independently and got `REGPROBE tools=55
  not_one_row=0 probe_contradictions=0 selftest_fail=0 history_verbatim=7/7 other_changes=0`.
- Evidence-verified receipts:
  - `controls/base-c1.txt`: `duplicated=7 probe_mismatch=2 exec_fail=1 … met=false`, exit=1.
  - `controls/after-c1.txt`: `revision=e84a1871… tools=55 rows=146 … mismatches=0 met=true`,
    exit=0.
  - `controls/tip-c1-at-c2.txt`: the same values at `06c81f08`.
  - `controls/ctl-c1-selftest.txt`: `selftest 29/29`.
  - The `deleteall` and `keepold` controls give `met=false`. `everycode` gives `met=true`, which is
    the declared counter limit, and the review conjunct covers it.
- **C1 met on its frozen predicate: verified (re-measured plus code reads).**

### C2 — freshness (HOLD 10), capability: 304 freshening contract v2, sourced S486/S487

This claim rests on the lane's gate `c100_fresh304.py`. Under §Gate standard (Closure consequence) I
verified its committed evidence and did not run it:
- Base `controls/base-c2.txt`: the v1 blob `db3a0f12…` scores `hand=72/91 generated=224/300
  met=false`, exit=1. This is the do-nothing control.
- After `controls/after-c2.txt`: `revision=06c81f08… candidate=present sha256=00edf6c4…
  hand=91/91 generated=300/300 refusals=122/122 seed=113778440 met=true`, exit=0.
- The seed follows the frozen rule: `int('06c81f08', 16)` = 113778440 (re-computed).
- Self-test `selftest 2/2`.
- Negative controls: the 13 single-mutation forgeries and `neg-theft` all give exit=1.
  `post-freeze-pos-oracle-8seeds.txt` shows the oracle at `met=true` on every seed.

Re-measured (plain):
- `git show 06c81f08:scripts/freshen_304.py | sha256sum` and the same at `72a6cd60` both give
  `00edf6c4f5daad497042e997ed54ef9da022acfb7da3a6a35f6922b263672c04`. The scored blob is the landed
  blob and has not changed since. The base blob is `db3a0f12…` (v1).
- The landed blob's only imports are `json`, `re` and `sys` (lines 40-42). A grep for
  `open(|/proc|subprocess|os.|pathlib|__import__|exec(|eval(` finds only a docstring mention. So the
  oracle-read vector is not used.
- CriticClaims raised a framing concern that the predicate cannot tell an independent
  implementation from a copy of the published reference. Checked: the landed blob has 767 lines,
  `frozen/pos-oracle.py` has 214, and `difflib.SequenceMatcher` line ratio is 0.031. The blob is not
  a reformatted copy of the oracle.
- ExecTwinFresh, an independent generator, gives `TWIN inputs=3600 disagreements=0`.
  `post-freeze-heldout-critic-probes-landed.txt` gives `heldout_same=4/4` on the CriticClaims X1-X5
  probe inputs. ReviewFresh found `hand=43/43 agree`, `rfc_contradictions=0`.
- Sourced: `corpus/knowledge/freshening-304.md` opens with `source: S484, S485, S486, S487`,
  `verified-at: 2026-11-06` and `recheck: 180d`, and cites S486/S487 26 times.
- **C2 met on its frozen predicate: evidence-verified.**

### Owned-axis harm check

`git diff 3989618d 72a6cd60 -- SCORECARD.md`:
- calibration moves `3` → `4` (line 19).
- operability (10) and freshness (10) at lines 17-18 are byte-unchanged in their first cells.
- The diff adds the Round 100 claims, move-log, repertoire and planned sections.

`git diff --stat 3989618d 72a6cd60 -- SHONEN.md PROVINCE.md AGENTS.md` is empty.

## 3. Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| calibration | improved | C1 met. Registry duplicates go 7 → 0 by plain count, all 55 tools keep exactly one current row, the history rows are verbatim, the three flagged rows match the code, and the reviewers agree 16/16. |
| freshness | improved | C2 met (evidence-verified, digest re-measured). The contract-v2 capability is admitted. The score holds at 10. |
| operability | unchanged | Not claimed. The score stays 10 and no row regressed. |

## 4. Discernment spot-check (`corpus/lessons/round-100.md` `## Gate`)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S486 RFC 9111 §5.2/§5.2.2.4/§5.2.2.7/§5.2.3 | admit (spec, A) | `curl https://www.rfc-editor.org/rfc/rfc9111.txt` → HTTP 200, 84477 bytes, sha256 `aeb52adb…` (equals the retained body) | agree | Quote 1 is verbatim at lines 1098-1100 («Cache directives are identified by a token, to be compared case-insensitively, and have an optional argument that can use both token and quoted-string syntax.», 24 words by my count). Quote 2 is verbatim at lines 1411-1412 («A cache MUST ignore unrecognized cache directives.»). It is the primary spec. The scope is disjoint from S484 (§3.1/§3.2/§4.3.4), so the W04 duplicate URL is intended. |
| S487 RFC 9110 §5.5/§5.6.1.2/§5.6.2/§5.6.4 | admit (spec, A) | `curl https://www.rfc-editor.org/rfc/rfc9110.txt` → HTTP 200, 502941 bytes, sha256 `21c1cdce…` (equals `.ufo/waves/round-100/sources/rfc9110.txt`) | agree | Line 1591 «A field value does not include leading or trailing whitespace.» is verbatim. The productions at line 1702 (`#element => [ element ] *( OWS "," OWS [ element ] )`) and lines 1786 (`quoted-string = DQUOTE *( qdtext / quoted-pair ) DQUOTE`) are verbatim. They ground the V2-2 trimming and argument-grammar clauses. |
| merge/kake package adoption | reject | `/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md` (129 S-rows by `grep -cE`); `corpus/SOURCES.md` | agree | S312 exists on both sides (staged and registry rows for the same Baidu mobile-adaptation page, with different bold emphasis in the scope cell). `ls merge/kake \| grep -i renumber` finds nothing, so appending would reuse ids, which the append-only rule forbids. The flip condition (a renumber map plus per-entry re-grounding) is well-formed. |

SOURCES.md row re-opened: S486 (`corpus/SOURCES.md` line 232). Its anchor cell names §5.2 grammar
lines 1098-1102 and the MUST-ignore sentence at lines 1411-1412. Both match the re-fetched body. The
≤25-word located quote is in the Gate entry, as CORPUS.md rule 1 requires, and checks out as above.
The fetch time 2026-11-06T01:48:09Z (22:48 -03:00) is before the row commit `06c81f08` (23:16:48
-03:00).

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → rc=0,
`kake ok`, 43 W04 warnings (`grep -c W04`).
- The two new warnings are `S486 duplicate url …rfc9111.txt across scopes` and `S487 duplicate url
  …rfc9110.txt across scopes`. This matches `controls/census-after.txt` and the report.
- Rows (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`) go from 222 at `3989618d` to
  224 at `72a6cd60`, matching the report.

## 5. Trend verdicts

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | improved | The RFC 9111 §5.2 Cache-Control argument grammar and RFC 9110 §5.5 field-value trimming are new ground. They come with mined tier-A rows S486/S487 and the v2 knowledge entry `corpus/knowledge/freshening-304.md`, which carries the provenance trio. An admitted contract-v2 capability goes into SCORECARD. |
| quality | improved | The v1 304 candidate (72/91) is superseded by the stronger v2 blob (91/91, 300/300, twin 3600/0). The seven second answers in the registry are removed and kept verbatim as history. Re-checks found no admitted entry failing. |
| discernment | improved | My spot-check upheld 3/3 sampled gate decisions (2 admits, 1 reject with a verified id collision). The attack-seat findings became criterion R100-A, grounded in receipts that were shown able to fail. The lane self-graded `unchanged` pending this outside check, and the outside check agrees with the gate on both admits and rejects. |

## 6. Routed defects (lane fixes next round)

Round 100 is the lane's last training round (amendment 38). These stay on the routed queue for
any successor round or the operator:
- R100-C1: harden `c100_registry.py` per R100-A (lane R100-1): a per-run random probe token, a
  read-only per-row tree with the instrument sources excluded, and could-not-evaluate when bwrap
  fails (SentinelScope R1/R2/R3/R4/R12, CriticClaims C1 escapes 6). Do this before any successor
  freeze cites the counter.
- R100-C2: the fresh304 population and judge (lane R100-2/R100-3). Cover CriticClaims X1-X5 (`\v`
  over-trim, BOM, bare `=`, environment-conditional behavior, stored qualified Cache-Control) in
  the counter's population. Add a provenance or independence check so that a static copy of the
  reference cannot score capability.
- R100-C3: mutation survivors, registry 7 and fresh304 4 (lane R100-4).
- R100-C4: the considerthese branch triage (R100-5). The 14 curated URLs and the
  `cloud-reviewed-export-20261103` entries need an in-round open and lane review before any row
  cites them.
- Operator note (not a lane fault): the template's `1× planner` vs. the validator rejecting
  `planner` is still unreconciled. SHONEN box 2 (an end-to-end domain task in LOG.md) is `[ ]`, so
  the SHONEN boxes are not fully checkable by a non-author and nothing is ready to promote.
