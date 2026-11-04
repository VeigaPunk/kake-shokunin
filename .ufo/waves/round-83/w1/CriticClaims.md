# CriticClaims — round 83 wave w1

Role: predicate critic (leaf, no dispatch). No production file written. Every run below is
read-only against the lane and the fleet; the crafted trees were built in
`/fast/scratch/hyaku/kake-r83/CriticClaims/` (deleted after the runs) and the evidence that matters,
with reconstruction recipes, is copied to `.ufo/waves/round-83/w1/CriticClaims/` (`runs/`,
`records-only-tree/`, `TREES.md`). Runs were taken
2026-11-04 between 13:31Z and 13:39Z while the wave was still in flight; that is stated where it
matters.

## 1. The two claims as a sceptical reader would state them

### C1

> **Population:** the six items filed at `corpus/lessons/round-82-verifier-spotcheck.md` §6 (D1
> attack floor, D2 byte units, D3 instrument receipt, D4 erratum quotes, D5 mutation survivors,
> D6 Gate provenance); nothing added or dropped after the freeze.
> **Before:** at `826b0061` the counter reads `open=6 closed=0 met=false`, exit 1.
> **After:** at the measured tree the same counter reads `open=0`, exit 0.
> **Counting command:** `python3 -B .ufo/waves/round-83/c83_defect_queue.py --root <tree>
> [--revision <rev>] [--fleet <dir>]`.
> **Falsified by:** any of the six state conjuncts failing to re-derive from the tree, or the
> base/junk control reading `met=true`.

### C2

> **Population:** the three surfaces declared at `.ufo/waves/round-81/capture-expectations.json`
> (ids *and* urls `https://ds4cc.com/`, `/robots.txt`, `/sitemap.xml`).
> **Before:** at `826b0061` the tool is absent and the counter reads `tool_absent=1 … met=false`,
> exit 1.
> **After:** every header that moved between capture A (round-81) and capture B (round-82) is
> classified by the frozen table; no validator/representation/unknown movement exists;
> `verdict=same-object`; the committed record equals a fresh run; two runs agree; a control pair
> flips to `representation-changed` with `validator>=1`; the tool is offline and its selftest is
> green; counter exit 0.
> **Counting command:** `python3 -B .ufo/waves/round-83/c83_drift_class.py --root <tree>
> [--revision <rev>]`.
> **Falsified by:** any flag false, or the target pair producing a substantive difference.

## 2. Divergences between that sentence, the contract text, and what the counters measure

### C1

1. **The population is never read.** `c83_defect_queue.py` never opens
   `round-82-verifier-spotcheck.md`. D1..D6 are hard-coded tuples; nothing binds them to §6, so
   "nothing added or dropped" is unfalsifiable by the measurement. A §6 with a seventh item would
   still score `open=0`.
2. **Five of six "non-lesson" files are lane-authored, not independent.** D1/D2 read
   `w1-spec.json` + `w1-results.json` + `w1-accounting.json`; D3 reads a receipt; D5 reads
   `run_killers.py`; D6 reads a `QUALITY.md` line. All are produced by this round's own seats or
   the L1. Only D4 touches bytes outside the lane (fleet git), and even that is a copy task.
3. **D1 measures the wave that is scoring it.** The ratio is derived from this wave's
   `w1-results.json`. This seat is one of the five attack rows; writing anything into
   `w1-results.json` raises the numerator. `settled` is `len(output) > 0`: a **single character**
   settles a seat (proved below). Round 82's actual defect was four empty attack seats; the round-83
   predicate accepts 1-byte placeholders, so "settle, not relabel" is not tested — "produce a byte"
   is.
4. **D1's floor is set below the dispatch's own supply.** 14 seats, 5 attack roles: any wave whose
   attack seats settle at all lands at 35.7 %, and with 2 attack seats settling the share passes
   for any total ≤ 8. `requested` is computed (line 138) and **used by no item**; `settled ==
   requested` is not required. Consequence: 10 of 14 seats can return empty and D1 still closes
   (proved below).
5. **D2 tests a schema, not the defect.** §6 item 2 is a *report prose* defect ("wave-prose byte
   counts are character counts"). The conjunct reads `bytes_basis == "utf-8"` in a JSON plus a
   lesson token; the round-83 report's own prose is never checked, so the same error could ship.
6. **D3 is a self-certifying receipt.** The counter parses the receipt's *own* fields
   (`bound == population`, `mismatches=0`, `met=true`) and never re-derives population, bindings or
   mismatches. A one-line fabricated file passes. The live wave demonstrates this arithmetically:
   `D3 closed` was already printed while `w1-results.json` and `w1-accounting.json` did not exist
   (receipt `runs/c1-worktree-midwave.txt`).
7. **D4's anchor is history position, not the frozen commit.** The contract names fleet commit
   `7678247a…`; the counter takes `git log` on the report path and uses `commits[0]`/`commits[1]`.
   Move one more fleet commit onto that path and the item opens even though the lesson still quotes
   the contract's commit (proved below). The contract also requires an `[r83-erratum]` *block* and
   "each quoted line absent from the amended blob"; the counter checks neither — only ≥4 substrings
   anywhere in the lesson.
8. **D5 is a six-line text test.** The contract says each row is `killed` on its named fixture, or
   `equivalent` with the guarding source line printed. The counter accepts any line containing the
   name plus the substring `killed` or `equivalent`, plus exit 0 and `distinguished=5/5` anywhere in
   stdout. `killed=0 fixture=NONE verdict=not-run` passes (proved below). Its own green fixture is
   such a stub (`write_fixture` prints the rows).
9. **D6 is one prose line**, by the contract's own admission. It adds a forward rule; it does not
   check that the filed misstatement (§6 item 6, the round-82 report's Gate rejects) was corrected,
   nor that the round-83 report cites the lesson.
10. **The kill rules are unmeasured.** The counter has no mode that re-runs `base-c83-…` or builds
    the junk tree; `junk_tree_build.py` is invoked by nothing in the counter. The base/junk
    receipts are static text committed at freeze, so "a control that reads met=true means C1 is not
    scored" is a human step, not a predicate.

### C2

11. **Urls are declared and never checked.** The counter's `declared_surfaces()` returns
    `id`s only, and `load_surface()` never reads `url`/`finalUrl`. The claim's population is "ids and
    urls"; the measurement is ids. Any receipt from any host satisfies a surface slot.
12. **No fresh observation exists.** Both capture trees are frozen from rounds 81/82; the round adds
    no capture. `diffs=14` is the round-81→82 header churn, unchanged. The `freshness` claim is
    therefore re-derivation over last round's exchange, not a freshness measurement.
13. **Everything except `control_ok` is already true at the freeze commit.** `--revision 64b71992`
    prints `record_equal=1 determinism=1 tool_offline=1 selftest_ok=1 … control_ok=0 met=false`; the
    *only* after-state input the wave must add is the control pair.
14. **`control_ok` tests the counter's own copy of the table, not the tool.** `measure()` calls
    `tree_receipts()` + local `classify()` on `capture-control/{a,b}`; it never runs
    `header_change_class.py` against the control pair, although the contract says "the classifier
    prints verdict=representation-changed". A tool that disagreed with the counter would still pass.
15. **The tool's printed totals are never cross-checked with the counter's totals.** `record_equal`
    compares the record with the tool's stdout; the predicate's `diffs/validator/…` come from the
    counter's own `classify()`. Proved: a tool whose summary prints
    `verdict=representation-changed` while its own per-surface lines say `same-object`, with the
    record regenerated, still reads `met=true` (below).
16. **`tool_offline` is an import-name regex, not a reachability test.** It strips only the first
    docstring and searches for `socket|urllib|requests|http.client|httpx` as words: `subprocess`
    (`curl`), `ctypes`, `importlib` and `os.system` all pass; a comment mentioning `socket` fails.
17. **`record_equal` strips all trailing newlines** (`rstrip(b"\n")`), not "one … per side" as the
    contract says — a more lenient comparison than the frozen text.
18. **`selftest_ok` does not cover the path the record exercises.** `header_change_class.py`'s
    `selftest()` calls `load_surface()`/`classify()` directly and never calls `run()`; the CLI block
    that produces the committed record has no selftest coverage, so its aggregation/printing can
    regress green.
19. **The target requires no finding.** `verdict == same-object` plus zero validator/representation/
    unknown is a *null result*: the ideal outcome of doing nothing. `diffs > 0` is satisfied by the
    `date` header alone, i.e. by two capture instants of an unchanged object — exactly what the
    frozen pair already is (all three bodies are byte-identical across rounds 81 and 82).

## 3. Strongest trivial path to `met=true` a do-nothing round could take

**C1.** `records-only` (tree kept at `.ufo/waves/round-83/w1/CriticClaims/records-only-tree/`):
base `826b0061` production bytes, plus `w1-spec.json` (copied from the freeze), a hand-written
`w1-results.json` (14 rows, `output: "x"`), a hand-written `w1-accounting.json`, a fabricated
one-line instrument receipt, a 6-line `run_killers.py` that prints `killed=0 fixture=NONE
verdict=not-run` five times and `distinguished=5/5`, a lesson carrying the six token lines, and one
appended `QUALITY.md` line. **No production code changes** (delta = 6 added record/doc files +
1 appended line; `scripts/` untouched; no `make_accounting_v2.py`, no killer fixtures, no
`population.json`). Reads `open=0 closed=6 met=true`, exit 0.

Answer to "does anything outside the lane decide any item?": **only D4**, and only as text copied
from a caller-selected `--fleet` repo. The population, all six thresholds, and the other five state
conjuncts are authored in the same freeze commit that authors the counter. D1's attack share is a
portrait of the wave's own roster and its own assembled results file, not an external test.

**C2.** `c2-base-records`: base `826b0061` + the frozen `scripts/header_change_class.py` + the
frozen `after-c2-classes.txt` + a fabricated control pair (copy round-82 capture to `a/` and `b/`,
flip one body byte, refresh `bytes`/`sha256`, change the primary ETag). No network, no new capture,
no wave work. Reads `met=true`, exit 0.

Answer to "three identical captures plus a fabricated control pair?": **no** — identical receipts
give `diffs=0` and `record_equal=0` (`met=false`, proved below). But identical *bodies* with one
moved `date` — the actual frozen pair — do pass, so the predicate needs only the appearance of an
exchange while forbidding any substantive movement.

## 4. Do-nothing control — exact lines

| tree | counter | line | exit |
|---|---|---|---|
| base `826b0061` | C1 | `C1v1 revision=826b0061f233ce1dffb9bd6874abc1342a864247 items=6 open=6 closed=0 met=false` | 1 |
| records-only | C1 | `C1v1 revision=worktree items=6 open=0 closed=6 met=true` | 0 |
| records-only, 10/14 seats dead | C1 | `D1 closed settled=4 settled_attack=2 settled_share=0.5` … `C1v1 revision=worktree items=6 open=0 closed=6 met=true` | 0 |
| records-only, fleet history +1 commit | C1 | `D4 open removed=0 quoted=0 amendment=ecdf37ba log=no` … `open=1 closed=5 met=false` | 1 |
| base `826b0061` | C2 | `C2v1 revision=826b0061… declared=3 … diffs=14 … record_equal=0 determinism=0 control_ok=0 tool_offline=0 selftest_ok=0 tool_absent=1 met=false` | 1 |
| freeze `64b71992` | C2 | `C2v1 revision=64b71992… diffs=14 validator=0 representation=0 unknown=0 verdict=same-object record_equal=1 determinism=1 control_ok=0 tool_offline=1 selftest_ok=1 tool_absent=0 met=false` | 1 |
| base + tool + record + fabricated control | C2 | `C2v1 revision=worktree … record_equal=1 determinism=1 control_ok=1 tool_offline=1 selftest_ok=1 … met=true` | 0 |
| identical captures (round-82 copied over round-81) | C2 | `… diffs=0 … record_equal=0 … met=false` | 1 |
| doctored tool (summary says `representation-changed`) | C2 | `… diffs=14 validator=0 … record_equal=1 … selftest_ok=1 … met=true` | 0 |
| live worktree, mid-wave | C1 | `D1 open … D2 open … D3 closed … D4 closed … D5 closed … D6 closed` → `open=2 closed=4 met=false` | 1 |
| live worktree, mid-wave | C2 | `… control_ok=1 … met=true` | 0 |

## 5. Universal clauses, reachable targets, undeclared axes

- **Universal clauses (C2):** `record_equal`, `determinism`, `tool_offline`, `selftest_ok` are
  properties of the frozen artifact set, true in every tree at or after the freeze commit. They are
  satisfied by construction and cannot be moved by any wave behaviour. `diffs > 0` is true of the
  frozen capture pair for every tree.
- **Universal clauses (C1):** D3's `bound == population ∧ mismatches=0 ∧ met=true` is true of any
  tree that can write one text line. D5's clause is true of any tree that can write six text lines.
  D1's share clause is true of any 14-seat dispatch whose attack seats settle at all.
- **Targets a do-nothing control reaches:** C1 `open=0` (proved) and C2 `met=true` (proved). Both
  are reached with zero production change; for C2 the only new bytes are the fabricated control
  pair.
- **Axis touched without declaration: `operability`.** The round ships a new 326-line production
  script (`scripts/header_change_class.py`) and a new killer harness, and the wave spec drafts a
  SCORECARD "capability row for the header-change classifier", but the contract declares only
  `calibration` (C1) and `freshness` (C2). `selftest_ok` also launders the tool's operability
  evidence into the freshness predicate instead of scoring it on its own axis. Scores are held, so
  nothing is mis-scored yet — but the instrument inventory grew without a declared operability
  claim or receipt.

## 6. Live-wave observations (honesty, not a substitute for the control)

At 13:31Z–13:39Z the wave had added `after-c83-instrument-check.txt`, `killers/run_killers.py`,
`corpus/lessons/round-83.md` and the `QUALITY.md` line, but not `w1-results.json` or
`w1-accounting.json`; C1 read `open=2` (D1, D2) and C2 read `met=true`. So four of six C1 items
were already closed by seat-authored files before the wave finished. The live killer suite is
*substantive* (it copies the frozen round-82 counters, checks their sha256 against
`population.json`, patches a literal anchor, builds fixtures from the counters' own builders and
compares pristine vs mutant; `--check` reproduced `distinguished=5/5`, exit 0). The predicate cannot
tell it from the 6-line stub above — that is the finding, not a claim that the seat cheated.
Likewise the lesson does carry an `[r83-erratum 2026-11-04]` block with five quoted lines, but the
counter never checks the block, only the substrings.

## 7. Commands and exit codes

| command | exit |
|---|---|
| `c83_defect_queue.py --root <lane> --revision 826b0061 … --work <scratch>` | 1 |
| `c83_defect_queue.py --root <records-only> --fleet /home/vgpnk/Projects/shokunin --work <scratch>` | 0 |
| `c83_defect_queue.py --root <sparse-seats> --fleet … --work <scratch>` | 0 |
| `c83_defect_queue.py --root <records-only> --fleet <drift-fixture> --work <scratch>` | 1 |
| `c83_defect_queue.py --selftest` | 0 (`9/9 passed`) |
| `c83_drift_class.py --root <lane> --revision 826b0061 … --work <scratch>` | 1 |
| `c83_drift_class.py --root <lane> --revision 64b71992 … --work <scratch>` | 1 |
| `c83_drift_class.py --root <c2-base-records> --work <scratch>` | 0 |
| `c83_drift_class.py --root <c2-identical-captures> --work <scratch>` | 1 |
| `c83_drift_class.py --root <c2-tool-diverges> --work <scratch>` | 0 |
| `c83_drift_class.py --selftest` | 0 (`9/9 passed`) |
| `python3 -B .ufo/waves/round-83/killers/run_killers.py --check` | 0 (`distinguished=5/5`) |

Full transcripts with argv, stdout and exit are in
`.ufo/waves/round-83/w1/CriticClaims/runs/`; the crafted trees' bytes are in
`.ufo/waves/round-83/w1/CriticClaims/records-only-tree/` with `SHA256SUMS.txt`.

## 8. Smallest safe correction

- C1: bind D1 to `settled == requested` **and** a substance floor (e.g. `len(output) >= 200`) taken
  from both spec and results; require `w1-accounting.json` to be produced by an invoked tool, not
  hand-written. Bind D3 to re-running `instrument_receipts.py --check` and comparing its stdout to
  the receipt, not to parsing the receipt. Bind D5 to the runner's fixture count and to the
  pristine/mutant pair, not to the substring `killed`. Bind D4 to `git diff cb02b705 7678247a`
  literally and to the `[r83-erratum]` block, not to `git log` position. Rename the claim to "six
  proxies close" until D2/D6 check the report prose they diagnose.
- C2: require the tool's printed summary to equal the counter's `classify()` totals; run the tool on
  the control pair (contract already says so); check declared `url` against receipt `url`;
  either add a fresh capture at the measured revision or state the claim as "the classifier
  reproduces the round-81→82 classification". Declare `operability` and give the new script its own
  receipt, or drop the capability row.

## Verdict

**Both predicates are falsified as tests of the stated property, and the claims are nonetheless
reachable by a do-nothing round.** C1: `met=true` on a tree with zero production change
(`open=0` from records alone), on a tree with 10 of 14 seats dead, and `met=false` on the same
records merely because the fleet's report history moved — so D4 measures history position, not the
frozen commit, while the other five items measure files this round's own seats write. C2: already
`met=true` at dispatch once a fabricated control pair is dropped in; the only after-state input is
that pair, the target requires no finding, and the tool's output is never required to agree with the
counter. Impacted axes: `calibration` (C1, proxy not defect), `freshness` (C2, null result over a
frozen pair), and `operability` (new production script, undeclared). The lane's live artifacts are
substantive where I looked (killer suite, erratum block), so this is a predicate defect, not
evidence of seat dishonesty.
