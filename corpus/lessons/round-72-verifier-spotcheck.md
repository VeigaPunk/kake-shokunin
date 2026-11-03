# Round 72 — verifier spot-check (kake)

author: hyaku closure (non-author integrator, @m_zfl)

Non-author closure of kake round 72 against lane tip `89a5db16fdf72b9a23c5447ce2429688c6d8b06a`
(base `3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1`). This file is the closure's own artifact; no
lane-authored file was edited. All commands below were run by the closure at 2026-11-03 from the
fleet root or the lane repo; receipts are read over committed bytes.

## Step-1 conformance — PASS

- Report committed in the fleet repo by the lane identity: `git log --format='%an <%ae> %H' -- .ufo/reports/round-72/kake.md` → `kake-shokunin <kake@shokunin.local> 2613d99b791fb9459681db9d971fe6f8c826f7e4`.
- `## SHONEN` heading count 1; 4 `[~]` lines, one per box; `SHONEN.md` has the same 4 boxes; no `[x]` written anywhere. Minimum content present (work performed, evidence pointers, landed changes, before→after, Sources & frontier, trend verdicts, SHONEN) — a real report, not a marker.
- Cited lane commits exist and are ancestors of `refs/heads/master` (`git merge-base --is-ancestor`, tested against the branch ref, never `@{u}`): `a19d38ea` (freeze), `999d208b4f8fb20ace3997a0a2a7073eb0296379` (round work), `5013c0ee87bda5fee03024488b4e293c4ca7ff16` (measured tip), `89a5db16fdf72b9a23c5447ce2429688c6d8b06a` (final tip), plus pins `4cb225fb…`, `cc6b4e0b…`, `6d8c52a6` — all ancestor-OK.
- Push state: `scripts/hyaku/jj-lane.sh state` → `branch=master local=89a5db16… remote=89a5db16… ahead=0 behind=0`; `git ls-remote origin refs/heads/master` shows the same hash. `git status --porcelain` → only `.ufo/waves/round-71/w1.ready` and `w1.ready.dispatched`, the inherited dispatcher markers the report names; not round work.
- Prompt fidelity: `.ufo/prompts/kake-round-72.md` renders `templates/round-prompt.md` sections 1–5 verbatim (report path, commit-before-report, SHONEN heading, hash citations, write scope, round-level contract items i–v, L2 minimum) plus the hyaku addendum §6. No L2 route map is quoted, so no MISSION.md bucket check applies.
- Watchdog digest (copied from `.ufo/watchdog.log` lines 2099/2110, matching the dispatch digest): `2026-11-03T18:22:47-03:00 launch kake round=72 pgid=2813037 driver=hyaku-inline attempt=1`; `2026-11-03T19:15:35-03:00 complete kake round=72; hyaku-inline attempt=1`.
- Wave evidence: `w1-results.json` = 15 seats, all with outputs, none errored; `w1-dispatch.json` = same 15 roles (scout 3, executor 2, scribe 2, reviewer 2, critic 2, connector 1, mutation-tester 1, sentinel 1, revenger 1). Attack share 6/15 = 40 % (strict reviewer+critic+mutation-tester 5/15 = 33 %), both ≥25 %. One v1 wave, band 8–16; round total 15; planner held by the L1 (recorded standing waiver); residual none.
- Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → exit 0 (`ok`); W04 duplicate-URL warnings are pre-existing rows, warnings allowed.
- SOURCES rows base→tip: `git show 3c68645a:corpus/SOURCES.md | grep -cE '^\| *S[0-9]{3,} *\|'` → 176; same grep at tip → 177; `git diff base tip -- corpus/SOURCES.md --stat` = 1 insertion (S439 only, no cell edits — "rows touched: none" confirmed).

## Per-claim re-check

Both declared claims rest on lane-owned gates (c66, c72, c56), so per PROTOCOL §Gate standard
(Closure consequence) they are **evidence-verified**: the closure verified the committed receipts,
the revision each was measured against, and the self-test tally, and re-derived the input side with
plain byte measurements. No sibling gate was executed by the closure.

### C1 — calibration (evidence-verified + plain re-derivation). Verdict: improved

- Frozen predicate (contract `§ C1`): c66 `agreement == 25`, `evaluated == 28`, only `c56_selftally.py` changes label; relabel must carry an ancestor pin and a green pin run.
- Plain measurement (closure-run): `git diff 3c68645a 89a5db16 -- SKILL.md` → exactly **1 hunk**; the only changed line is the `selftest-tally-counter` registry row's Kind cell, now `gate (historical from round 72: green at its round-56 measured revision 4cb225fb… (pin run receipt .ufo/waves/round-72/controls/c56-pin-linux.txt))…`. No other registry row changed — "only c56_selftally changes label" holds over committed bytes.
- Receipts (committed, contents read):
  - `controls/c1-base.txt` (committed at freeze `a19d38ea`): `members=28 evaluated=28 mismatches=4 structural=0 agreement=24 … met=True`, `exit=0`; mismatch set = `c56_selftally` (`live_not_green`), `c57_idresolver_gate`, `c58_resolver_cases`, `c59_resolver_cases`. Matches the reported before.
  - `controls/c1-tip-final.txt` (committed at `89a5db16`): `mismatches=3 agreement=25 … met=True`, `exit=0`; `c56_selftally` now `label=historical e_T=1 e_P=0 eval=ok ok` with `argv@pin --revision 4cb225fb…`; the only remaining mismatches are c57/c58/c59 (`live_not_green`). Matches the reported after; the mismatch set loses c56 only.
  - `controls/c56-pin-linux.txt` (committed at freeze): `tally_mismatches=0 rows_checked=10 met=True`, `revision: 4cb225fb…`, `EXIT=0` — the green pin run the historical label requires.
  - `controls/c56-tip-final.txt`: `tally_mismatches=6`, all `tool_changed`, at the tip — c56 is red at the tip, so the c66 rule "a historical row with a green tip is never counted as agreement" is not tripped.
- Corrected cause check: the relabel cell attributes the tip red to the counter's `scripts/fixtures` tree gaining four `quote-class` files at `6d8c52a6` (ancestor-OK), not to changed audited scripts — consistent with the tip receipt (all six mismatches `tool_changed`, three rows OK unchanged) and with the round-63 commit existing. The first draft's "six audited tools changed" was corrected before landing (ReviewerC1/CriticClaims); the landed text is the measured one.

### C2 — operability (evidence-verified). Verdict: improved

- Frozen predicate (contract `§ C2`): selftest 11/11 exit 0; c71 exit 0 and c72 exit 1 on the J3 control; base `cc6b4e0b` exit 1; tip exit 0. The contract requires the same sentence in plan, counter and receipt.
- Receipts (committed, contents read):
  - `controls/c2-selftest.txt` (at freeze): `C2v2 selftest 11/11`, `selftest_exit=0`, including the discriminating legs `j3_phrase_only_on_command_is_command_finding` and `v1_accepted_j3_rejected_here`.
  - `controls/c2-base-red.txt` (at freeze): `C2v2 revision=cc6b4e0b… command_findings=2 … met=False`, `exit=1`; `controls/c2-base-head.txt`: revision `3c68645a` → `findings=[] met=True`, `exit=0`.
  - `controls/c2-tip-final.txt` (at `89a5db16`): `revision=5013c0ee… brace=0 command=0 prose=0 findings=[] guard=ok met=True`, `exit=0`.
  - `controls/c2-j3-control-r3.txt` (at `999d208b`): `c71_exit=0` (round-71 counter accepts the control), `c72_exit=1` (round-72 counter rejects: `command_findings=1`), `j3_script_exit=1`. The harness `controls/j3-control.sh` deterministically rebuilds the fixture (base clone + one fixed phrase-only command annotation on line 27) under `$HYAKU_SCRATCH`, so the receipt's `J3_CONTROL_COMMIT=70c23642…` (a scratch hash, not in the lane) is reproducible content-wise; the committed harness keeps `set -e` with explicit `|| rc=$?` capture and exits with the c72 code (M4 fix; the earlier set-e receipt `c2-j3-control.txt` stays as history).
- The M4/M2 mistake chain is shown able to fail: the first receipt cannot print `c72_exit`, the repaired one does; the `set -u` variant that exited 0 when unevaluable was rejected (SentinelC2 R1) — the landed harness exits 127 with the tools missing per the report.
- Counter source read: `c72_tmp_v2.py` passes the revision after `--end-of-options` to `git show` (the S439-sourced mitigation) and classifies command-bearing `/tmp` tokens independently of a phrase annotation. Two evidences satisfied: function-level selftest fixtures + frozen runs at named revisions.

### No axis harmed

`git diff 3c68645a 89a5db16 -- SCORECARD.md` = +21 lines (round-72 measured-claims section and planned-73 note only); scores unchanged (operability 10, freshness 10, calibration 2, all HOLD). freshness untouched → unchanged; LOG.md round-72 entry present and tied to the landed commits.

## Spot-check table (LEARNING.md — sampled from `corpus/lessons/round-72.md` § Gate)

| Item | Decision | Re-opened source (command) | Agree/disagree | Reason |
|---|---|---|---|---|
| c56 relabel (admit) | admit | Committed receipts `c1-base.txt`, `c1-tip-final.txt`, `c56-pin-linux.txt`, `c56-tip-final.txt` + `git diff base tip -- SKILL.md` (1 hunk, c56 row only) | **agree** | Label change matches the counter's documented rule (historical needs ancestor pin + green pin run, both receipted); numbers re-derive from committed bytes; the corrected fixtures-tree cause is the measured one |
| S439 registry row (admit) | admit | Live `curl https://git-scm.com/docs/gitcli` → 51306 bytes, `cmp` byte-identical to retained `sources/gitcli.html`, sha256 `4e1ea3a5…a02714a1e` matches receipt and anchor; `grep -cF` each quote → 1/1/1 on the live body; `--end-of-options` at line 1896 | **agree** | Quotes are ≤25 words (11/7/7), located, raw-substring-verifiable on the live page; tier A (official Git docs) correct for the `--end-of-options` scope; row well-formed, census exit 0 |
| In-place rewrite of the round-70 adopted entry (reject) | reject | `git diff 3c68645a 89a5db16 -- corpus/knowledge/crux-bigquery-origin-membership.md` → 0 lines; grep S303/S304/S352 → 1 citation each, 0 registry rows | **agree** | Append-only guard reads a replaced line as a changed finding; the entry is untouched; the dangling-id residue is real and correctly routed (L0 line 277) instead of silently rewritten |
| Registering S303/S304/S352 as kake rows (reject) | reject | `grep -cE '^\| *S30[34] *\|'` and `S352` on `corpus/SOURCES.md` → 0 rows each | **agree** | CORPUS.md rule 2: adopted ids continue next-unused (S438 was last); registering staged ids would green the resolver while the body still cites foreign ids — taste correct |
| "All gates green" as the round outcome (reject) | reject | `controls/c1-tip-final.txt`: c57/c58/c59 `live_not_green` at the tip | **agree** | Three owned gates stay red on the dangling ids; the ledger and report say so; rejecting the green reading is honest |

5/5 agree. Both sampled admits and both substantive rejects re-opened at their sources (one live URL re-fetch, byte-identical to the retained body; the rest over committed bytes/commands).

## Per-axis and trend verdicts (closure, non-author)

- Axes: **calibration improved** (C1 evidence-verified + plain re-derivation), **operability improved** (C2 evidence-verified), **freshness unchanged** (untouched, no harm).
- **expansion: unchanged** — one curated source row (S439, mined, cited by C2), no admitted knowledge entry on new coverage-map ground; frontier map unchanged. Matches the lane's grade.
- **quality: improved** — the c56 registry cell now states its measured cause (wrong first draft caught by two attack seats and corrected before landing); the C2 counter demonstrably rejects a control the predecessor accepted (J3 receipts); the ledger records the disagreement append-only. Bounded: residual counter holes are routed, not closed. Matches the lane's grade.
- **discernment: improved** — this closure is the round's non-author spot-check; it agrees with the gate on the sampled admits and rejects (5/5), which is the LEARNING.md `improved` signal. The lane conservatively graded unchanged at report time because the check did not yet exist; the closure credits it now that it agrees. (Fleet precedent: kengaku r66 closure, 4/4 agree → discernment improved.)

## Routed defects for round 73 (status-neutral; none bars admission)

1. **Dead receipt pointers in round-72 bookkeeping.** The LOG.md round-72 entry and the SCORECARD round-72 row cite `controls/c1-tip.txt` and `controls/c2-tip.txt`; no file under those names ever existed (`git log --all -- <path>` empty). The actual receipts are `controls/c1-tip-final.txt` and `controls/c2-tip-final.txt`. Fix next round as append-only corrections naming the superseded text (no in-place rewrite).
2. **Gate registry row missing for the new counter.** `grep -c c72_tmp SKILL.md` → 0: the round-72 C2 gate `c72_tmp_v2.py` has no registry row at the lane's registry home (SKILL.md gate registry), which PROTOCOL §Gate standard (Delivery) requires before the closure can grade the gate conformant. Add the row with the round-73 C2 amendment work.
3. Carried from the lane's own routing (confirmed real, not new): C2 residual holes (verb vocabulary, `${TMPDIR:-/tmp}` fallback, symlinked SKILL.md, unpinned `PHRASE`); c57/c58/c59 red on the three dangling staged ids awaiting the operator ruling at `.ufo/l0-questions.md` line 277; round-71 carry-ins.

## Operator notes

- All four SHONEN boxes carry `[~]` with resolvable pointers (gate registry + ledger; LOG round-72 verification run + `c2-j3-control-r3.txt`; the runnable `j3-control.sh`; PROVINCE adjacency note). Nothing observed here blocks a non-author from checking any box; promotion stays operator-owned.
- Inherited untracked dispatcher markers `.ufo/waves/round-71/w1.ready{,.dispatched}` remain in the lane working copy — not round work, left alone correctly.
- Pre-freeze diagnosis (M3) was disclosed in the frozen contract; claims are judged on their frozen predicates, which the receipts satisfy.
