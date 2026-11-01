# Round 65 — lessons (kake)

Round opened 2026-10-30 on the prior Linux host; round 65 was re-run to
completion on a fresh Windows host (attempt 2, 2026-11-01). Inherited
state: base `d3a4e40228c307954fa6ced6cab03654faac1ffa` (round-64 wrap-up
tip, which also landed the round-64 late wave file that closure had marked
an untracked durability debt); the prior attempt's frozen contract
`.ufo/waves/round-65/contract.md` (predicates frozen before any seat ran,
v1→v2 repairs pre-data) and a dispatched 32-seat w1 (`w1-dispatch.json`)
that never settled — no seat report exists. This attempt inherited the
frozen predicates, built the pending instruments, and took every receipt
on the new host. Instruments: `.ufo/waves/round-65/c65_semantics.py`,
`fixtures/build_attack_fixtures.py`, `check_s432_pin.py`,
`sources/s432-pin.json`; measured revision `74cabcdf` (instruments +
freeze); receipts commit `67f9b5c9`.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| stale-premise (inherited, repaired by the prior attempt pre-data; mirrored here per the contract's reference) | contract §C1 v1 required `met=false at base`, but the round-64 lesson bytes the counter authenticates already exist at base `d3a4e402` — any faithful byte-authenticating counter greens there (receipt `.ufo/waves/round-65/controls/base-c1.txt`, c65 at base prints met=true) | the prior L1's ExecDoNothing pre-derivation, before any after-state measurement | predicate v2 (then v3, below) drops the base-red clause; the falsifiable delta is the fixture differential + instrument existence; the copied-prose control `donothing-c1-copied` documents the frozen limitation honestly |
| stale-premise, host-relative (repaired this attempt, before any after-state receipt) | contract §C2 v2 froze "sweep exits 0 on the measured tree" — true at base on the prior host (`controls/l1-c2-prederivation.txt`, taken there), false on this host for host reasons: 29 §paths NEW MISS paths, every one an old-host `~/` home path (receipt `controls/sweep-base-thishost.txt`, foreign=0) | this attempt's base sweep on the new host, run before the C2 after-receipt | predicate v3: the sweep may exit non-zero, but zero NEW MISS paths may sit under the lane root and no unannotated cite may be created this round; the v2 exit-0 clause is recorded NOT met here; the §paths migration re-pin (SKILL.md annotations + pathsMissSet re-measure, round-18 pattern) is routed as carried debt |
| contract-internal tension (caught at build time) | A1's parenthetical ("no verdict span, no attribution") cannot hold with the frozen differential (c64 must print met=true on A1) because c64's lesson_gate substring-requires the verdict span | this attempt's fixture build, which reproduced the ReviewerC1Prose `minimal` shape instead and re-read the predicate | A1 carries the span as a bare token with no attribution/admission span; spot_auth fails on the missing attribution (contract amendment 2, pre-data) |
| control-shape gap | the first c2-drift/c2-wrongpin fixtures omitted the pin file, so the receipts showed `pin=0 absent` instead of the contract's shapes (match=0 under a correct pin; pin=0 under a wrong-digest pin) | receipt review against contract §C2's do-nothing spec | builder fixed and re-pinned pre-data (commit `711fe582`); corrected shapes measured (`controls/donothing-c2-drift.txt`: pin=1 match=0; pin=0 digest_mismatch named) |
| dirty fixture-directory reuse | rebuilding fixtures into the same scratch directories chained an empty commit on top of each fixture (same tree, new parent), silently changing every recorded HEAD (A1 `a1ffe1ff…` → `fb04a2db…`) | the receipts step's cross-check of the new heads against the recorded ones | rebuild into fresh directories per run; determinism asserted across two fresh builds; the supersession is recorded in `controls/fixture-builds.txt`; all dependent receipts regenerated |
| claim-before-receipt (this attempt) | an earlier draft of this lesson's Gate reject (e), the SCORECARD round-65 block and the LOG entry stated "one standing mismatch, unchanged (c60-paired.txt)" while the paired c60 run was still executing; the finished receipt showed a different, stronger result (28/28 host-bound mismatches; targeted c56 runs identical at base and final) | the receipts step itself: the cited `controls/c60-paired.txt` did not exist at write time | the three sites were corrected to the measured result in the same round, the corrected receipt committed as `controls/c60-paired-thishost.txt`, and this row records the slip; the round-57 class (claim first, receipt later) is exactly what the draft repeated |
| inherited-attempt shape (recorded, not repaired here) | the frozen w1 (32 seats) was dispatched and never settled; the AgentSwarm/Kimi L2 surface does not exist on the new host, and no subagent dispatch tool was available, so the MISSION.md L2 floor and the contract's wave clauses could not be exercised | this attempt's round open | routed around honestly: the wave clauses fire on nothing and attest nothing; recorded as an L0 question (`.ufo/l0-questions.md`), never treated as answered; the non-author closure remains the outside check |

## Gate

Candidates: (a) C1 measured met — admit as calibration 2→2 HOLD;
(b) C2 measured met — admit as freshness 10→10 HOLD; (c) a third claim
from the probe findings; (d) repairing the §paths sweep drift this round;
(e) considerthese adoption.

- **Admit (a):** the four routed green classes are now counter-enforced
  and the outside-verdict artifact is byte-authenticated. At the measured
  revision `74cabcdf`, c65 prints met=true (exit 0) while each differential
  fixture prints met=false naming its component and the round-64 counter
  still greens the same three fixtures: A1 marker-only (no attribution)
  spot_auth=0 / c64 met=true; A2 contradictory Gate
  gate_noncontradictory=0 (span named) / c64 met=true; A3 hidden-comment
  criterion criterion_visible=0 / c64 met=true; A4 spot-flip tamper
  pins=0 disagreements=0 (c64 also red via its disagreements gate —
  recorded as-is, not a differential; ScoutSpotSpan A1's reword shape is
  additionally turned red in selftest t8 via the spot sha pin). Selftest
  38/38; builder deterministic across two fresh runs. The claim does NOT
  assert semantic resolution (the round-64 QUALITY addendum's rule
  stands); receipts `.ufo/waves/round-65/controls/{base-c1,after-c1,
  selftest-c1,fixture-builds}.txt`.
- **Admit (b):** the S432 retained live re-open body is byte-pinned.
  At `74cabcdf`: `pin=1 blob=1 match=1 met=true` exit 0; at base
  `pin=0 met=false` (no pin file); drift fixture (one byte off, correct
  pin) match=0; wrongpin fixture (verbatim blob, wrong digest) pin=0 with
  the mismatch named — the frozen constant is enforced inside the tool,
  not read from the pin file alone. §2b sourced evidence: the source was
  re-opened this round — https://fetch.spec.whatwg.org/, accessed
  2026-11-01T02:36:27Z, ONE GET (curl), HTTP 200, 1,854,393 bytes,
  sha256 `63b0a018…911b` byte-identical to the retained body (receipt
  `.ufo/waves/round-65/sources/receipt.json`). Located quote (18
  whitespace units, collapsed-only, raw lines 6150–6154, unchanged from
  the round-63/64 record): "The `X-Content-Type-Options` response header
  can be used to require checking of a response's `Content-Type` header
  against the destination". Existing row S432 re-opened; no registry row
  added or changed.
- **Reject (c):** a third, probe-derived freshness claim. The live probes
  (five properties, GET-only) produced real findings — the canonical
  sitemap now serves 100 locs (the standing "sitemap 404" records are
  historical), PQ-12's charter-ghp pin is byte-identical to its r18
  baseline, ds4cc.com was redeployed 2026-10-25 — but they were run
  before any claim could be frozen, so a claim built on them would be a
  post-data predicate. The frozen contract's two claims stand; the probe
  findings are recorded as protocol work (PROVINCE surfaces correction,
  publish-queue dated corrections, probe receipts), not scored.
- **Reject (d):** repairing the §paths migration drift this round. Going
  green needs absent-annotations inside SKILL.md (cites at SKILL.md:442,
  476–477, 512–521 and others), which the frozen no-harm list forbids
  this round; half a repair (pins JSON without annotations) would leave
  the gate red anyway. Routed as the lane's carried freshness debt with
  the round-18 pattern as the recipe (`.ufo/waves/round-65/controls/
  sweep-base-thishost.txt`).
- **Reject (e):** assimilation none. The `merge/kake/` package stays
  staged; `considerthese/2026-10-26.md` proposal 5 stays rejected from
  round 64 — this round adds the defect-3
  evidence its flip demanded — with the honest outcome that the full c60
  re-derivation is host-bound here (28/28 members mismatch: every pinned
  argv invokes an absent `python3`) and the targeted c56 selftally is
  IDENTICAL at base and final (exit 2, one unparsable row, inner spawn
  exit 9009): unchanged across the round, so no round-caused regression,
  and the r64 standing red is neither reproduced green nor cleared on
  this host. Receipt `controls/c60-paired-thishost.txt`; the registry
  reconciliation stays with the operator's calibration ruling. Assimilation: none — shokuknow unreachable (its checkout is
  absent on this host).

## Sources census

Round-start (this host, fleet-root clone):
`bash .../shokunin-clone/shokunin/scripts/sources-census.sh validate --root .../shokunin-clone/shokunin kake`
→ 17 lines: 16 W04 duplicate-URL warnings + `kake ok`, **exit 0**
(`scratch` copy retained; recorded 2026-11-01 before any registry edit).
The inherited attempt's own census-before (prior host) is committed at
`.ufo/waves/round-65/controls/census-before.txt` (171 rows, 16 W04,
exit 0). No `corpus/SOURCES.md` row was added or changed this round
(re-open of S432 only); the round-end census output is pasted in the
round report with the same counting command.
