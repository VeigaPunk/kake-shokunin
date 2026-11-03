# ReviewerC1 — kake round 74, wave w1, attempt 1 — pre-after-state attack on C1

Seat: ReviewerC1 (leaf member, no subagent dispatch). Date: 2026-11-03.
Measured revision: `ced2878a1e77f57afb4ee3baebf1021e5130399b` (base, committed bytes only; lane
HEAD at measurement time = `b35dd4d7d6a0a633d7c950bf641d3f948e680448`, the freeze commit; the
freeze commit's `SKILL.md` is byte-identical to base — `git diff --quiet base HEAD -- SKILL.md`
exit 0). Lane checkout read-only; no production file touched; no mutating git/jj command run
anywhere; scratch tree `/fast/scratch/hyaku/kake-r74/ReviewerC1/` deleted before yield.
Artifacts: `.ufo/waves/round-74/w1/ReviewerC1-heldout/` (10 fixtures + `MANIFEST.md` +
`run-against-fixtures.sh`).

## 1. Base census reproduced independently from committed bytes

Method: `git show ced2878a…:SKILL.md | grep -cF <filename>` per counter, then a line-numbered
classification pass (`TABLE_ROW` = line starts with `|`, `NON_ROW` = anything else).

| Counter | Mentions | Lines | Classification |
|---|---|---|---|
| `c69_recorded_counts.py` | 0 | — | no row (grep exit 1) |
| `c69_tmp_honour.py` | 0 | — | no row (grep exit 1) |
| `c70_pointer_audit.py` | 0 | — | no row (grep exit 1) |
| `c71_calibration.py` | 0 | — | no row (grep exit 1) |
| `c71_tmp.py` | 0 | — | no row (grep exit 1) |
| `c72_tmp_v2.py` | 1 | 1400 | NON_ROW — prose in "Round 73 gate registry additions": "`c72_tmp_v2.py` has no registry row in this file" |
| `c73_tmp_v3.py` | 2 | 1400, 1404 | 1400 NON_ROW (prose); **1404 TABLE_ROW** (filename in first/Name cell) → the only registered population counter |
| `c73_wave_pointers.py` | 0 | — | no row (grep exit 1) |
| `c74_registry_gap.py` (own row) | 0 | — | no row; file absent at base (`git cat-file -e` non-zero) → `own_row=false` |

Context (outside the population, for §3): `c56_selftally.py` has a table row at line **1253**
(alias `selftest-tally-counter`, filename only in the Entry-command cell); `c66_gate_status_hostportable.py`
has a table row at line **1396** (alias `gate-status-counter-v2-hostportable`, filename only in the
Entry-command cell); `c72_tmp.py` (retired v1) has 0 mentions and is absent from the base tree
(`cat-file -e` exit 128).

Verdict: **7 of 8 unregistered; only `c73_tmp_v3.py` registered (row at line 1404); `own_row`
absent** — exactly reproducing `controls/base-c1-registry.txt` (`rows=0` ×7, `c73_tmp_v3.py rows=1`,
`unregistered=7 met=false`). Additionally all 8 population counter paths resolve at base
(`git cat-file -e base:<path>` exit 0 for each of the 8), so the base failure is conjunct 1
(registration) + conjunct 3 (own row), not conjunct 2. Census matches the frozen receipt with zero
mismatches — the counter's base-reproduction requirement is satisfiable.

## 2. Parser-design attack — 10 held-out fixtures

Authored before the counter exists (`test -f .ufo/waves/round-74/c74_registry_gap.py` exit 1 at
attack time; still absent at report time). Location:
`.ufo/waves/round-74/w1/ReviewerC1-heldout/` (copies of scratch-authored originals; internal
placement validated programmatically — every target sits exactly where the fixture intends,
including `f05` L8 `TABLE_ROW_IN_FENCE`). Per-fixture contract requirement and implementation
outcome; `MANIFEST.md` carries the same table plus the assertion protocol.

| Fixture | Contract requires | Reasonable impl | Naive impl (likely defect) |
|---|---|---|---|
| f01 kind-cell | `c71_calibration.py` **registered** — "a row naming the counter in any cell counts" | pass | first-cell-only matcher says unregistered → violates kill rule f2 |
| f02 prose-only | `c70_pointer_audit.py` **not registered** — "a prose mention outside a table row does not count" (f3) | pass | whole-file substring matcher says registered → violates f3 |
| f03 command-path-other | `c69_recorded_counts.py` **not registered** (no cell contains it); the row does register `c69_tmp_honour.py` | pass | round-sibling cross-crediting via `c69_` prefix or path proximity |
| f04 prefix collision | `c72_tmp_v2.py` **not registered** — the only row names `c72_tmp.py`, a file absent at base (exit 128); exact-filename rule; the dead v1 path is out-of-population and must not trip conjunct 2 | pass | stem-normalizing matcher (`c72_tmp` ≈ `c72_tmp_v2`) registers v2, or an over-broad dead-path scan false-fails conjunct 2 |
| f05 fenced row | `c69_tmp_honour.py` **not registered** (recommended reading: a pseudo-row inside a code fence is documentation, not a rendered registry table) | pass if fence-aware | fence-unaware line matcher registers it — any doc example would then self-satisfy the gate. **Ambiguity A3: the predicate text does not say "outside a fenced block"; the impl must pin its choice in `--selftest`** |
| f06 duplicate rows | `c71_tmp.py` registered (conjunct 1) **but overall not met**: the second registering row's command path `c71_tmp_pre_rename.py` is dead, and conjunct 2 says "the counter path named by **each** such row resolves" | fail (met=false) | first-matching-row-only conjunct 2 says met → violates kill rule f4's per-row reading |
| f07 dead path | `c73_wave_pointers.py` registered by Name cell **but overall not met**: the row's only path `c73_wave_pointers_missing.py` is dead (f4) | fail (met=false) | conjunct 2 skipped, or matched against the Name-cell filename instead of the command path |
| f08 leading `./` | registered; conjunct 2 must resolve `./.ufo/waves/round-69/c69_tmp_honour.py` to the same blob | pass (normalize, or run cat-file from `--root`) | environment-dependent verdict — see probe below |
| f09 outside population | rows for `c56_selftally.py`, `c66_gate_status_hostportable.py` and never-committed `c99_absent_probe.py` have **no effect** on the frozen population; no crash; the permanently dead c99 path ignored | pass by construction (population frozen inside the counter) | dynamic "all counters" discovery expands the population; dead-path scan over out-of-population rows false-fails |
| f10 alias command-cell | `c70_pointer_audit.py` **registered** — filename appears only in the Entry-command cell (the real alias-row shape) | pass | first-cell-only matcher says unregistered (f2) |

Measured probe on the f08 question: `git cat-file -e base:./.ufo/waves/round-69/c69_tmp_honour.py`
exit **0** with cwd at the lane root **and** exit **0** from a foreign cwd via `--git-dir` — git
normalizes `./` here, so a literal cat-file implementation is robust on this host; the documented
semantics are still cwd-relative, so normalizing the path (or running from `--root`) and pinning
the behavior in `--selftest` is the safe design. Plain substring matching is safe for the
c72 collision in both directions (`c72_tmp.py` is not a substring of `c72_tmp_v2.py` and vice
versa); the hazard class is stem-normalizing matchers and unescaped-dot regexes.

**Finding H1 (high):** conjunct 2 quantifies over *every* registering row ("each such row"), and
kill rule f4 confirms per-row failure. A first-row or best-row implementation silently reports
`met=true` for a registry containing a dead duplicate row (f06) or a lone dead path (f07). The
frozen text already decides this; any implementation deviating is a contract violation, not a
design choice.

**Finding H2 (high, must be pinned):** the fenced-code-block case (f05) is live ambiguity — kill
rule f3 covers prose only, and the predicate's "table row" is not defined against markdown fences.
Recommendation: structural table detection (fenced rows never count), pinned by a selftest
fixture either way so the behavior is deliberate and frozen by the counter's own `--selftest`.

**Finding M1 (medium):** any-cell matching is not hypothetical — the real base registry places
`c56_selftally.py` and `c66_gate_status_hostportable.py` filenames **only** in the Entry-command
cell (rows at lines 1253 and 1396), so a first-cell-only matcher misclassifies the real registry,
not merely the fixtures.

**Finding M2 (medium):** conjunct-2 scope is population rows only; dead out-of-population paths
(f04's absent `c72_tmp.py`, f09's `c99_absent_probe.py`) must be ignored, else the counter
false-fails on rows the predicate never quantifies over.

**Note N1:** `c74_registry_gap.py` does not exist at base, so "the counter's run at base MUST
reproduce `controls/base-c1-registry.txt`" necessarily means the after-state binary measuring
`--revision base`. Kill-rule f5 (missing/renamed population file → `unevaluable`, never silently
met) has a measured precedent: `c72_tmp.py` is absent at base (exit 128) while `c72_tmp_v2.py`
resolves — a rename scenario the selftest must exercise.

**Note N3:** the registry is a series of per-round tables (`### Round NN gate registry additions`
headers at lines 1188, 1206, 1224, 1243, 1263, 1283, 1297, 1311, 1379, 1398), not one table. The
predicate imposes no section restriction, so a whole-file table-row scan is the safe design; a
parser hard-coded to one section risks future misses.

Harness status: `run-against-fixtures.sh` → `NOT_RUN: counter absent`, exit **3** (honest; rerun
after the counter lands). Fixture repos are throwaway `git init` trees with stub population files;
`git rev-parse --show-toplevel` asserted equal to the fixture dir before every commit; throwaway
identity (`fixture <fixture@example.invalid>`) used inside fixtures only.

## 3. Population honesty

Each of the 8 is the claim counter of the frozen contract section the population table cites,
verified by grepping each contract at base:

| Counter | Contract anchor verified |
|---|---|
| `c69_recorded_counts.py` | round-69 §C1 (line 9, "Recorded counts re-derive or are relabelled") — filename present |
| `c69_tmp_honour.py` | round-69 §C2 (line 21, TMPDIR operability) — filename present |
| `c70_pointer_audit.py` | round-70 §C1 (line 22, evidence pointers) — filename present |
| `c71_calibration.py` | round-71 §C1 (line 9) — filename present |
| `c71_tmp.py` | round-71 §C2 (line 48, stale /tmp citations) — filename present |
| `c72_tmp_v2.py` | round-72 §C2 (line 41) — 7 mentions |
| `c73_tmp_v3.py` | round-73 §C2 (line 44) — 5 mentions |
| `c73_wave_pointers.py` | round-73 §C1 (line 23) — 2 mentions |

Union of distinct counter filenames across the round-69–73 contracts = **10**. The two outside the
population are named by round-72 §C1 *as instruments, not as claim counters*: `c66_gate_status_hostportable.py`
(the calibration run whose `agreement` the round measures) and `c56_selftally.py` (the allowed
disagreement member: "any member **other than** `c56_selftally.py` changes its agreement", plus pin
receipts). Both have their own home-round contracts (round-56, round-66 — 2 mentions each) and both
are already registered (SKILL.md rows 1253, 1396); `c56_selftally` is additionally red-at-later-tips
by design per its own row, which is exactly why it is a harm/observability check and not part of a
registration census. Round-73 §C3 names no numbered counter (it uses the standing sweep), so nothing
is missed there. Round-74's harm battery names `c66`, `c70_pointer_audit`, `c72_tmp_v2`,
`c73_wave_pointers`, `c73_tmp_v3` — all in or overlapping the population — and never mentions
`c56_selftally` (grep count 0).

**Verdict: no missing counter, no extra counter.** The frozen table is the operative enumeration and
is faithful to the §C1/§C2 claim counters of rounds 69–73. One looseness to record (**Note N2**): the
contract's prose gloss "the counters named by the frozen contracts of rounds 69–73" read hyper-literally
would sweep in `c56_selftally`/`c66` (they *are* named in round-72's text); the per-row §-anchor table
is what defines the population, and it is honest.

## 4. Do-nothing reachability

With no rows added: the 7 zero-row counters stay at 0 rows (measured at base; `SKILL.md` identical
base↔HEAD), `unregistered=7 ≠ 0` fails the kill rule, and `own_row` cannot exist without a round-74
section row — so C1 stays **not met, exit 1**. The base receipt is that control. Stronger: at attack
time no standing instrument can even see the gap — `c73_tmp_v3.py` (row 1404) checks `/tmp` literals
and the frozen round-73 corpus, and the freshness sweep checks sidecar bindings; neither parses
registry rows — and `c74_registry_gap.py` itself is not in the tree. In the do-nothing world the
`controls/base-c1-registry.txt` receipt is the **only** witness of the gap. The contract's do-nothing
control is therefore faithful, and the counter's base-reproduction requirement is what makes the
control falsifiable.

## 5. Command ledger (exact commands, exit codes)

```
mkdir -p /fast/scratch/hyaku/kake-r74/ReviewerC1                 # ok
git -C <lane> rev-parse HEAD                 -> b35dd4d7d6a0a633d7c950bf641d3f948e680448, exit 0
git -C <lane> cat-file -t ced2878a…          -> commit, exit 0
git -C <lane> ls-tree -r --name-only ced2878a… | grep -i 'SKILL.md$'   -> root SKILL.md identified
git -C <lane> show ced2878a…:SKILL.md | grep -cF <counter>          # per-counter census:
#   c69_recorded_counts.py 0 (exit 1)  c69_tmp_honour.py 0 (exit 1)   c70_pointer_audit.py 0 (exit 1)
#   c71_calibration.py 0 (exit 1)      c71_tmp.py 0 (exit 1)          c72_tmp_v2.py 1 (exit 0)
#   c73_tmp_v3.py 2 (exit 0)           c73_wave_pointers.py 0 (exit 1) c74_registry_gap.py 0 (exit 1)
#   c56_selftally.py 1 (exit 0, L1253) c66_gate_status_hostportable.py 1 (exit 0, L1396) c72_tmp.py 0 (exit 1)
git -C <lane> show … | grep -nF <counter>    # line-number classification pass (TABLE_ROW / NON_ROW)
git -C <lane> cat-file -e ced2878a…:<population path>   # all 8 -> exit 0; c74, c72_tmp.py -> exit 128 class
git -C <lane> cat-file -e ced2878a…:.ufo/waves/round-56/c56_selftally.py -> exit 0 (real path)
git -C <lane> show ced2878a…:.ufo/waves/round-{69,70,71,72,73}/contract.md | grep -oE 'c[0-9]+_[a-z0-9_]+\.py' | sort | uniq -c
git -C <lane> show ced2878a…:.ufo/waves/round-56/contract.md | grep -cF c56_selftally.py   -> 2, exit 0
git -C <lane> show ced2878a…:.ufo/waves/round-66/contract.md | grep -cF c66_gate_status_hostportable.py -> 2, exit 0
grep -cF c56_selftally <lane>/.ufo/waves/round-74/contract.md -> 0
git -C <lane> cat-file -e ced2878a…:.ufo/waves/round-69/c69_tmp_honour.py            -> exit 0 (plain path)
git -C <lane> cat-file -e ced2878a…:./.ufo/waves/round-69/c69_tmp_honour.py          -> exit 0 (cwd = lane root)
(cd /fast/scratch/…/ReviewerC1 && git --git-dir=<lane>/.git cat-file -e ced2878a…:./…) -> exit 0 (foreign cwd)
git -C <lane> cat-file -e ced2878a…:.ufo/waves/round-73/c73_wave_pointers_missing.py -> exit 128 (dead path)
git -C <lane> diff --quiet ced2878a… HEAD -- SKILL.md                                 -> exit 0 (identical)
test -f <lane>/.ufo/waves/round-74/c74_registry_gap.py                                -> exit 1 (absent)
python3 placement-validation over ReviewerC1-heldout/                                 -> exit 0, all placements as designed
bash <heldout>/run-against-fixtures.sh                                                -> NOT_RUN, exit 3
git -C <lane> log --oneline ced2878a…..HEAD -> b35dd4d7 only; git status --porcelain | wc -l -> 10 (untracked wave artifacts)
```

Tooling: no installs or upgrades performed (git + python3 stdlib only); nothing to record under the
2026-10-19 operator authorization.

## Findings by severity

- **H1 (high):** conjunct 2 is per-row ("each such row") — first-row implementations silently pass dead
  duplicate rows (f06/f07); frozen kill rule f4 already decides the correct behavior.
- **H2 (high, pin it):** fenced-code-block pseudo-rows (f05) are unresolved by the frozen text; pin the
  choice (recommended: never count) in the counter's `--selftest`.
- **M1 (medium):** any-cell matching is mandatory and exercised by the real registry (base lines 1253,
  1396 place the filename only in the Entry-command cell).
- **M2 (medium):** conjunct-2 scope = population rows only; dead out-of-population paths must be ignored
  (f04 v1 row, f09 c99 row).
- **L1 (low):** `./`-prefixed row paths resolve on this host from any probed cwd (exit 0 twice); still
  normalize-or-pin, since documented semantics are cwd-relative (f08).
- **L2 (low):** exact-filename matching required; plain substring is safe for the c72 collision, stem
  normalizers and unescaped-dot regexes are the hazard class (f04).
- **L3 (low):** mismatched rows (filename in one cell, command runs another counter) are counted for the
  named counter by the frozen text with conjunct 2 resolving the other counter's path — an accepted
  registry-quality hole; implementations must not "fix" it by reinterpretation (f03).
- **N1/N2/N3 (notes):** after-state binary measures base (f5 selftest precedent: `c72_tmp.py` absent at
  base, exit 128); population prose gloss looser than its table; registry is many per-round tables —
  scan whole file.

## Residual risk and verification gaps

The counter does not exist yet, so the 10 fixtures were **never executed against an implementation**;
every fixture verdict above is derived from the frozen predicate, not from a measured run
(`run-against-fixtures.sh` exit 3 = NOT_RUN). Whether the counter's `--json` exposes per-counter
registration granularity sufficient for the manifest's assertions is unknown until it lands. The
f05 and f08 ambiguities remain contract-live until the implementer pins them in `--selftest`; if
pinned opposite to my recommendation they are still contract-defensible, provided the choice is
deliberate and tested. Scratch tree `/fast/scratch/hyaku/kake-r74/ReviewerC1/` deleted before yield
(verified below); all fixture bytes survive in `.ufo/waves/round-74/w1/ReviewerC1-heldout/`.
