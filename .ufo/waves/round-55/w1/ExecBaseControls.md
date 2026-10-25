# ExecBaseControls

Scope: replicate the frozen base controls of round 55 (W1) in `/home/vgpnk/Projects/shokunin/kake-shokunin`
at base revision `fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d`. Lane treated read-only: no file under the lane
was written except this report; stdout/stderr of every run went to a `/tmp/r55base.ILzjtN` scratch dir.
All six runs used `python3 -B`. No git state touched (no `git add/commit/stash/checkout/reset/pull/push`,
no jj command); the counters themselves only call `git -C <root> show` / `git ls-tree` (read-only).

COMMANDS:

1. `python3 -B .ufo/waves/round-55/c55_readme_index.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d`
   - cwd `/home/vgpnk/Projects/shokunin/kake-shokunin`, exit **1** (contract kill rule: 1 = not met at base), stderr empty, 25 lines / 1106 bytes.
   - first 3:
     ```
     C1 readme-index index_mismatches=21 knowledge_files=46 met=False  (met: index_mismatches == 0 AND knowledge_files >= 46)
       unindexed=21 thin=0 dangling=0 coverage_rows=27
         unindexed: accessibility-review-cards.json
     ```
   - last 3:
     ```
         unindexed: yahoo-japan-rel-nofollow-semantics.md
       revision: fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d
     EXIT=1
     ```
   - Note: the counter itself emits the trailing `EXIT=<code>` line as part of stdout; it is not added by me.

2. `python3 -B .ufo/waves/round-55/c55_quote_truth.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d`
   - cwd `/home/vgpnk/Projects/shokunin/kake-shokunin`, exit **1** (expected at base), stderr empty, 30 lines / 1861 bytes.
   - first 3:
     ```
     C2 quote-truth 0/8 met=False  (met: conditions_passed == 8 of 8)
       C1_entries_exist FAIL
         - S372: knowledge entry corpus/knowledge/yahoo-japan-robots-txt-refusal-rules.md absent at the measured revision
     ```
   - last 3:
     ```
         - mirror .ufo/waves/round-55/assimilation/pre-append/corpus/SOURCES.md absent at the measured revision
       revision: fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d
     EXIT=1
     ```
   - All eight conditions C1..C8 report FAIL at base, matching the contract's "0 of the 3 entries exist; registry 155 rows" before-state.

3. `python3 -B .ufo/waves/round-55/c55_readme_index.py --selftest`
   - cwd `/home/vgpnk/Projects/shokunin/kake-shokunin`, exit **0**, stderr empty, 1 line / 33 bytes.
   - first 3 = last 3 (file is a single line):
     ```
     c55 readme-index selftest: 10/10
     ```

DIFFS:

All three outputs are byte-identical to the frozen control receipts (`diff -u` exit 0 for each; sha256 re-check):

| produced | control | diff | sha256 (produced = control) |
|---|---|---|---|
| run 1 stdout | `.ufo/waves/round-55/controls/base-c1-readme-index.txt` | none (identical) | `5a62df83bd50e607…` |
| run 2 stdout | `.ufo/waves/round-55/controls/base-c2-quote-truth.txt` | none (identical) | `8c0899ec2ccb6032…` |
| run 3 stdout | `.ufo/waves/round-55/controls/c1-selftest.txt` | none (identical) | `5b1d17530b5e6fe0…` |

So the do-nothing controls reproduce exactly: C1 `index_mismatches=21 knowledge_files=46 met=False` exit 1;
C2 `0/8 met=False` exit 1; C1 selftest `10/10` exit 0.

JSON CHECK:

Both counters were run once more with `--json` appended to the same argv (exit **1** each, stderr empty).

- Raw stdout is **not** a single valid JSON document: each counter prints the JSON object and then its
  unconditional trailing `EXIT=<code>` line, so `json.loads(full_stdout)` fails with
  `Extra data: line 35 column 1` (C1) and `Extra data: line 99 column 1` (C2).
- The JSON document itself (stdout with the final `\nEXIT=…` line stripped) **parses** for both counters,
  and each carries the frozen predicate string verbatim:
  - C1: `schema="kake-r55-c1-readme-index-v1"`, `predicate="met: index_mismatches == 0 AND knowledge_files >= 46"`,
    `revision="fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d"`, `knowledge_files=46`, `coverage_rows=27`,
    `index_mismatches=21` (unindexed 21 entries listed, `thin=[]`, `dangling=[]`), `met=false`.
  - C2: `schema="kake-r55-c2-quote-truth-v1"`, `predicate="met: conditions_passed == 8 of 8"`,
    `revision="fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d"`, `adopted` maps S372/S373/S418 to their target
    entries, `checks` holds C1..C8 each `passed=false state="fail"` with notes, `conditions_passed=0`, `met=false`.
- Predicate-sentence consistency (substring check, unrun anything else): C1's sentence occurs in `contract.md`,
  `contract.json` (`claims.C1.predicate`), and `c55_readme_index.py` (`PREDICATE`, line 41); C2's sentence occurs
  in `contract.md`, `contract.json` (`claims.C2.predicate`), and `c55_quote_truth.py` (`PREDICATE`, line 57).
  Neither sentence appears in the other counter's source. The control receipts' header lines carry the same
  sentence, since the diffs are byte-identical.

Risks / observations (advisory, no fix applied — outside this seat's write scope):

- The `EXIT=` trailer makes `--json` output non-consumable by a strict JSON parser as-is; a consumer must strip
  the last line (or the counter must emit it to stderr). Reported, not changed.
- C1's base JSON carries `thin=[]`/`dangling=[]`, so the whole 21-mismatch base delta is `unindexed`; the
  considered "Frontier ground map" pointers (contract C1) are therefore untested by the base control.
- `__pycache__` observation (not created by this seat, recorded for the parent): the lane now holds
  `.ufo/waves/round-55/__pycache__/{c55_readme_index,c55_quote_truth}.cpython-314.pyc` with mtimes
  `17:46:40.717` / `17:46:52.800` on 2026-10-25. My runs produced output at `17:45:27.28–.76` (three base
  controls) and `17:45:57.81–.91` (`--json`), all under `-B`, so those `.pyc` files postdate my runs by ~43 s
  and ~55 s and come from another lane process running the counters without `-B`. They are untracked and
  matched by `.gitignore` lines 2–3 (`__pycache__/`, `*.pyc`) per `git check-ignore -v`, so they do not enter
  the committed bytes the counters measure; round-52 and round-54 `__pycache__` dirs likewise already exist
  and are untracked. Nothing was deleted (deletion is outside this seat's write scope).

Tooling: no install or upgrade was needed or performed this seat (python3/git already present).

VERDICT: All three base controls reproduced byte-identically (C1 21/46 met=False exit 1, C2 0/8 met=False exit 1, selftest 10/10 exit 0); both `--json` payloads parse after stripping the counter's trailing `EXIT=` line and carry the exact frozen predicate strings — this seat wrote only its report, no git/jj state touched.
