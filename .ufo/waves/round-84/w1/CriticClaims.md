# CriticClaims — round 84 wave w1

Seat: falsify C1 (calibration) and C2 (freshness/capability). Leaf, read-only over the lane;
receipts in `.ufo/waves/round-84/w1/CriticClaims/`. Scratch `/fast/scratch/hyaku/kake-r84/CriticClaims/`
was used and deleted before this yield; everything quoted below was re-run or copied into receipts first.
Counters scored from the lane's own frozen files at `.ufo/waves/round-84/`; the lane worktree was at
`87cbfd99` (freeze `f358022f` ancestor-verified) with wave products landing uncommitted during this seat's run.

## 1. Do-nothing controls

### C1 — cheapest tree that makes the frozen counter read `met`

Five files, of which only two are fabricated (receipts: `c1-control-lesson-round-84.md`,
`c1-control-w1-results.json`, run log `c1-donothing-and-s457-probe.txt`):

1. `corpus/lessons/round-84.md` — four short lines: one `[r84-correction 2026-11-04]` line naming
   `round-83.md`, `Gate`, and the four heading strings `5.2.  Cache-Control`,
   `5.2.1.  Request Directives`, `5.2.2.  Response Directives`, `5.2.3.  Extension Directives`
   (two spaces, as the counter freezes them); one `D2 count=66 span=838-844 measure=words-full-span`
   line (66 is the true count I re-derived from the retained `rfc9111.txt` lines 838–844 with
   `len(re.findall(r"\S+", "\n".join(lines[837:844])))`); one line naming
   `controls/census-before.txt`; one line naming the connector seat.
2. `.ufo/waves/round-84/w1-results.json` — `{"results":[{"name":"ConnectorSibling","agent":"connector","output":"sibling scan done"}]}`.
3–5. Copied unchanged from the lane: retained `.ufo/waves/round-83/w1/ScoutSources/rfc9111.txt`,
   `corpus/SOURCES.md`, frozen `controls/census-before.txt`, plus the already-committed
   `w1-spec.json` (its `connector` role pre-dates the wave, so D3's spec half is free).

Score: `python3 -B .ufo/waves/round-84/c84_defect_queue.py --root <tree>` →
`C1v1 … open=0 closed=4 met=true`, **exit 0**. So the whole C1 closure reduces to two files whose
content the counter only token-checks; the counter decides state, not labor. That is the control's
point, and it is exactly what the frozen junk-prose control already disclosed (prose alone opens 2;
prose + the two artifact files closes 4).

### C2 — cheapest receipts that make the frozen counter read `met`

The receipts: the six real-pair receipts `.ufo/waves/round-8{1,2}/capture/<sid>/response.json`
(+bodies) and the twelve control-pair receipts `.ufo/waves/round-84/capture-control/{control,equivalent}/{a,b}/<sid>/response.json`
are frozen and verify (`receipts_ok=1`); `policy-expectations.json` and
`round-81/capture-expectations.json` are frozen; the only non-frozen inputs are
`scripts/policy_value_class.py` and the record `.ufo/waves/round-84/controls/tool-real-pair.txt`,
both written by the same wave that is graded. I built the least tool that can satisfy them: a ~50-line
path-keyed lookup (`canned_policy_value_class.py.txt`) that prints the frozen CLI lines for the three
fixture pairs and nothing else. Its own `--selftest` exits 0; it imports no network module.

Score: counter over the scratch tree with the canned tool and a record generated from its own stdout →
all conjuncts green, `met=true`, **exit 0** (`c2-donothing-control-run.txt`). Negative probe: flipping
one class string (`reordered`→`numeric_parameter` on the equivalent pair) correctly gives
`eq_mismatch=2`, `met=false`, exit 1 (`c2-negative-probe-wrong-eq-class.txt`) — the counter is not
vacuous; it just cannot tell an implementation from a table keyed on the fixtures it was written for.
The live tool landed mid-run (`scripts/policy_value_class.py`, 9976 bytes) and the lane worktree now
scores green everywhere except `record_equal=0` (record not yet committed), i.e. C2 is one receipt
away from `met` at the time of writing.

## 2. Axes moved, axes harmed

- C1 moves **calibration** (SCORECARD line 19: score 2, lowest non-retired) by closing the four
  routed defects from `round-83-verifier-spotcheck.md` §6; C2 moves **freshness** (line 18: 10, a
  legacy hold, "not a fresh whole-corpus verdict") as a declared capability acquisition.
- Diff inspected: `git diff --stat fe42ad11..f358022f` = 39 files, **8512 insertions, 0 deletions**
  (contract, counters, control pairs, expectations, base receipts — pure additions);
  `git status --short` during the wave shows only untracked additions (`w1/`, the tool). No scored
  artifact was modified or removed, so no axis is harmed by anything I could diff.
- One conditional harm found and closed in-round: D4's conjunct re-derives W04 collisions from the
  **after** tree and compares them to the frozen before-receipt (22 rows), so any same-URL-new-scope
  registry append in the same round reopens D4. Probed with three S457 shapes: same-URL (`…/rfc9111.txt`)
  + new scope → `derived_w04=23`, `item=D4 closed=0`, `met=false`, exit 1; distinct URL or S456's exact
  scope → stays closed. As landed, S457 cites `https://httpwg.org/specs/rfc9111.html`, which
  ScribeRegistry retained and receipted this round (fetch 200, sha256 recorded), and the live counter
  still reads `receipt_w04=22 derived_w04=22` — so the coupling did not fire and the provenance is
  honest. Residual: the coupling is structural (C1's before/after census equality silently assumes
  census-stable registry appends), and citing the honestly-retained `rfc-editor.org/rfc/rfc9111.txt`
  — the URL ScoutSources' item names — would have broken C1. Worth one line in the round's limits.

## 3. Is C2 a capability acquisition under AXES.md §Capabilities?

Yes, by the section's letter: a `capabilities:` row needs name → what it can now do → evidence
pointer → first-working round, and "rows enter only through a round that demonstrates the capability
running." The lane could already say **which** policy header moved (`header_change_class.py` freezes
the policy class table); it could not say **what about the value moved**. Now it can: the tool emits
value-level classes (`numeric_parameter`, `reordered`, `directive_added/removed/changed`,
`header_added/removed`, `unclassified`) and the decisive verdict distinction
`policy-rewritten-equivalent` vs `policy-changed`, offline, over retained receipts — demonstrated
running by the frozen counter (ctl_changed=3/0 mismatch policy-changed; eq_changed=1/0 mismatch
policy-rewritten-equivalent) on pairs the round built itself at the freeze. The demonstration is the
round's own, not borrowed. Caveat the closure should carry: it is **synthetic-only**. I diffed all 21
POLICY-class fields across the real pair myself (canonicalized from the six committed receipts):
zero value differences, which is exactly why the contract freezes `real_changed == 0` — the claimed
capability has never classified a real-world changed policy value, only manufactured ones. The
control/equivalent design (an order-only rewrite cannot pass as a change; a real change cannot pass
as a rewrite) is the right falsification shape, so I would not reject on this — but the capability
row should say "demonstrated on synthetic pairs" until a live drift exercises it.

## 4. Strongest rejection reason and the smallest fix

**Strongest:** C2's counter cannot see the difference between the instrument and a canned echo of the
frozen fixtures — I proved a 50-line lookup table reaches `met=true` (§1). The contract §C2 requires
the tool to import the class table "imported, never copied" from `scripts/header_change_class.py`,
and the real tool does (`from header_change_class import POLICY, header_class, canonical, …`, line
27), but **no counter conjunct checks that**: `tool_offline` only greps network imports, `selftest_ok`
runs the tool's own selftest, and every other conjunct is agreement between the tool's output and
fixtures the same wave authored. A non-author closure reads a chain in which author, instrument,
fixtures, record and grader share one origin, with the one structural requirement unenforced.

**Smallest change that removes it:** add one counter conjunct `tool_imports_table` to
`c84_policy_values.py`, computed the same way as `tool_offline` (strip the module docstring, regex for
`from header_change_class import` / `import header_change_class` in
`scripts/policy_value_class.py`), require it in the `met` conjunction, and let the mutation-tester
cover it. It is mechanical, offline, catches the cheapest cheat (my canned tool passes everything
else), and would have cost one frozen-contract line. The canned tool I shipped is the standing
counterexample: it passes the current counter and fails this conjunct. (It cannot catch a lookup
table that also performs the import — no file-based counter can; that residual belongs to the
reviewer/mutation seats, which is acceptable and should be named.)

## Commands and exit codes

- `python3 -B .ufo/waves/round-84/c84_defect_queue.py --root <c1-control tree>` → `met=true`, exit 0.
- Same counter over `s457b-txt-new-scope` → `derived_w04=23`, `met=false`, exit 1; over
  `s457b-html-new-scope` and `s457b-txt-same-scope` → `met=true`, exit 0.
- `python3 -B .ufo/waves/round-84/c84_policy_values.py --root <c2-control tree>` → `met=true`, exit 0;
  with the one-class mutant → `met=false`, exit 1.
- Live lane runs (state at 11:0x, mid-wave): C1 `open=3` (D1/D2/D3 pending lesson + results.json),
  D4 closed, exit 1; C2 all green but `record_equal=0`, exit 1.
- `git diff --stat fe42ad11..f358022f` (39 files, +8512/−0); `git merge-base --is-ancestor f358022f HEAD` → yes.

## Verdict

Neither claim is falsified as framed: both counters decide exactly what the contract freezes, both
controls reach `met` with the disclosed minimal inputs, and no axis is harmed by any diff I could
inspect. C2 is a legitimate capability acquisition demonstrated on the round's own synthetic pairs
(real pair genuinely unchanged — verified independently). The one structural weakness worth a
correction: C2's counter never enforces the contract's import-the-class-table requirement, and my
canned-tool control is the proof it can be gamed; the one-conjunct fix above closes the cheapest
version of that gap. The D4×S457 census coupling was a live hazard this round and was navigated
honestly (distinct, actually-retained URL); record it as a limit — the closure's separability is
contingent on registry-append shape, not structural.
