author: hyaku closure (non-author integrator, @m_zfl)
round: kake 86
date: 2026-11-04
report: .ufo/reports/round-86/kake.md
lane_base: 376ac5dcdf86457ef1f8dd490dada735dad81f68
lane_carrier_head: eb42d5a38249061af9b3321ec44f381eed6f59fa

# Round 86 verifier spot-check — kake (hyaku closure, non-author)

## Conformance results

- Report committed in the fleet repo by the lane identity
  `kake-shokunin <kake@shokunin.local>`, commit `3431d313a981737b5fb5106d369096ed51a50c07`
  (2026-11-04 12:57:33 -03:00), before the driver completion line (12:58:05 -03:00). ✓
- `SHONEN` heading present with one line per box (4 boxes: `[~]`, `[ ]`, `[~]`, `[~]`);
  no `[x]` written by the lane — correct, non-author verification is closure's. ✓
- All five cited lane commits exist and are ancestors of `refs/heads/master`
  (`git merge-base --is-ancestor` per hash): `efc2ad65…`, `2dd355bb…`, `3f2de0fd…`,
  `2854f765…`, `eb42d5a3…`. ✓
- Push state via `scripts/hyaku/jj-lane.sh state`: `branch=master
  local=eb42d5a38249061af9b3321ec44f381eed6f59fa remote=eb42d5a38249061af9b3321ec44f381eed6f59fa
  ahead=0 behind=0`. ✓ (`git ls-remote` re-confirmed during closure.)
- Dispatched prompt `.ufo/prompts/kake-round-86.md` = canonical
  `templates/round-prompt.md` rendering + hyaku addendum §6. Byte diff vs rendered
  template shows one line-1 substitution only (`<{{LANE}}-repo>` → `kake-shokunin`,
  the canonical path resolution); all round-level items and five child-lane items
  embedded verbatim. Quoted routing conflicts with no `MISSION.md` bucket (MISSION
  pins advisory role-class buckets only, no role→model map). ✓
- Defects (status-neutral): (a) one untracked round artifact left in the lane repo,
  `.ufo/waves/round-86/w1/ExecAssim/mirror/corpus/lessons/round-81-gate/rfc9110.html`
  (1.2 M fetched RFC mirror byproduct; `git status --porcelain` shows it as `??`);
  (b) the register data-row quarantine sweep ran after the SOURCES append (late;
  disclosed by the lane in the report and lesson supplement); (c) W04 census
  warnings 22→23 — the new S461 cross-scope duplicate URL is intentional and
  disclosed.

## Per-claim re-check (commands + observed output)

Re-measured on committed bytes (plain measurements run by this verifier):

- SOURCES rows: `git show <rev>:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`
  → base `376ac5dc…` = **196**, carrier `3f2de0fd…` = **199**, head `eb42d5a3…` = **199**.
- knowledge Markdown: `git ls-tree -r --name-only <rev> -- corpus/knowledge | grep -c '\.md$'`
  → 71 → 73 → 73. Matches `controls/committed-corpus-counts.json` and the report.
- Delivered reader exists at carrier: `git show 3f2de0fd…:scripts/cache_control_effective.py | wc -l` → **241**;
  still present at head. My own functional spot-call (fresh input, not the lane's
  fixtures): `printf '{"cache_control":["max-age=600"],"shared":true}' | python3
  scripts/cache_control_effective.py` →
  `{"storable":true,"freshness_lifetime_seconds":600,"basis":"max-age",…}` exit **0**.
- Both new knowledge entries open with the provenance trio (`source:` citing mined
  rows S461 / S459+S460, `verified-at:`, `recheck:`); `corpus/README.md` gains two
  round-86 coverage rows; SCORECARD gains the bounded-reader capability row.
- C1 ground truth: fleet commit `44de6cb69439f23173ba7c3bfecace7faed9c797` exists
  (kake L0 line, D84-4 planner routing); round-85 closure notes name the four routed
  dispositions; D84-4 remains unresolved (open). C1 receipt shows the disposition
  counter at **closed=3/open=1, met=false, exit 1** — the reported honest stop.

Evidence-verified, never executed (lane-owned counter/selftests; §Gate standard):
`controls/after-c1-carrier.txt` (C1v1 revision=3f2de0fd… freeze=efc2ad65… items=4
closed=3 open=1 met=false, R1 ok=false self-referential, exit 1);
`controls/after-c2-carrier.txt` (C2v1 revision=3f2de0fd… cases=15/15 selftest_ok=1
tool_offline=1 met=true, exit 0); `controls/decoder-selftest.txt` (29 fixtures, exit 0);
`controls/preservation.json`, `controls/integrated-trial.json` (three real round-82
retained captures decoded max-age=600), `wave-done-receipt.txt`, `w1-accounting.json`
— all committed at head, revision-bound to the named carrier. **C2: re-measured
(plain) + evidence-verified. C1: re-measured (ground truth) + evidence-verified;
unprovable stands.**

## Per-axis verdicts

- **calibration: unprovable.** R1 requires the counter's own green receipt after
  receipt plus C2's success — self-certifying and cross-claim dependent; the lane
  never seeded a fabricated green, reported met=false itself, and D84-4 stays open.
  Honest stop agreed.
- **freshness: improved (bounded).** Reader delivered and exercised on my own input;
  frozen receipts green at the named revision; capability row + coverage rows +
  provenance-complete entries landed. Bounded scope honestly declared (no full
  parser/cache/network conformance).
- **operability: unchanged.** No score move; scoped preservation evidence
  (`preservation.json`, retained RP selftest 32/32 receipt); no whole-corpus claim made.

No owned axis harmed: `git diff 376ac5dc… eb42d5a3… -- SCORECARD.md` shows calibration
2→2 HOLD, freshness 10→10 HOLD, capability row added, no score reduction.

## Spot-check table (item · decision · re-opened source · agree/disagree · reason)

| Item | Decision | Re-opened source (live, 2026-11-04) | Verdict | Reason |
|---|---|---|---|---|
| S459 CrUX Vis docs | admit (A) | GET https://developer.chrome.com/docs/crux/vis → 200, 114607 B | **agree** | Exact quote present: "If your origin is not included in the CrUX dataset, there will be no data to display." (17 words, "Does it work for all websites?"); teaching scoped, no overclaim. |
| S461 RFC 9111 slice | admit (A) | GET https://httpwg.org/specs/rfc9111.html → 200, 178573 B | **agree** | Exact quote present: "either the first occurrence should be used or the response should be considered stale" (14 words, §4.2.1 ¶4); ≤25-word located quotes for all three new rows check out; supersedes-S457 scope correctly narrow. |
| RFC 7234 minimum-duplicate attribution | reject proposition | GET https://www.rfc-editor.org/rfc/rfc7234.txt → 200, 90647 B | **agree** | §4.2.1 says "the directive's value is considered invalid"; no first-occurrence/minimum-duplicate rule exists there (grep sweep), so the historical attribution was false and the primary-source correction is grounded. |

New-row re-open (duty 3): S461 row re-opened live (above) and its ≤25-word located
quote verified verbatim; S459 likewise. S460 is lane own-work (authorized 403 probe);
its retained receipt `probe.json`/`receipts.md` is committed and internally consistent
— not re-executed (authorization boundary).

## Trend verdicts (closure)

- **expansion: improved** — 196→199 mined rows, 71→73 provenance-complete entries on
  ground the round-83 coverage map did not hold (bounded value-level Cache-Control
  slice now held; CrUX route adopted from `merge/kake`), re-derived from git.
- **quality: improved (bounded)** — reader + 15-case frozen verdict + selftest 29 at
  the named revision; false RFC7234 attribution corrected via primary source without
  rewriting frozen bytes; prior counterexamples byte-preserved.
- **discernment: improved** — outside spot-check (this file) agrees with the round
  gate on the sampled admits and the sampled reject, all sources re-opened live; the
  round-86 QUALITY criterion ("measurement evidence must be downstream of its
  predicate") cites the lesson and is shown able to fail.

## Routed defects (lane fixes next round)

1. Remove or explicitly dispose of the untracked mirror byproduct
   `.ufo/waves/round-86/w1/ExecAssim/mirror/…/rfc9110.html` (uncommitted round
   artifact in the lane repo; commit receipts only, or clean the scratch tree).
2. Run the register data-row quarantine sweep **before** the SOURCES append next
   time (this round's sweep was late, after append; disclosed).
3. Keep D84-4 open pending the operator ruling (existing debt, not a new defect).

## Closure ruling

status **ok** (real, substantive report); **not admitted** — verdict
`rejected-honest-stop`: C1 unprovable (lane-declared, agreed), C2 verified bounded;
no axis harmed. SHONEN promotion not ripe: boxes remain author-asserted (`[~]`) and
box 2 carries a genuine historical-receipt gap; promotion is operator-owned.
