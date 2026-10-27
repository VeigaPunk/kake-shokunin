# SimplifyToolReview — round-63 simplification review

## Assignment

Can `scripts/quote_class.py`, `.ufo/waves/round-63/quote-class/extract_text.py`, or
the two round-63 counters be materially smaller without losing the frozen
semantics? Propose concrete deletions only where behavior is preserved; otherwise
certify each file at its honest minimum. Do not edit.

Lane root: `/home/vgpnk/Projects/shokunin/kake-shokunin`. Measured commit
`05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`, base `13d4519818db28cd0aa912e49020659140d7b9fa`.

## Verdict

**No file is materially larger than its honest minimum.** Across the four files
(519 lines, 267 AST statements) exactly **8 lines are provably dead or redundant**,
all in two files, and landing even those costs a contract re-freeze because
`scripts/quote_class.py` is byte-pinned. Nothing lands in round 63.

| file | lines | AST stmts | provably dead lines | reduced size | judgment |
|---|---|---|---|---|---|
| `scripts/quote_class.py` | 147 | 69 | 5 (3.4% lines, 4.3% stmts) | 142 / 66 | two dead items; behavior-identical (proven below); **pinned sha, cannot land** |
| `.ufo/waves/round-63/quote-class/extract_text.py` | 103 | 64 | 3 (2.9% lines, 4.7% stmts) | 100 / 61 | one unreachable-false check; behavior-identical (proven); no sha pin, still not landed mid-round |
| `.ufo/waves/round-63/c63_calibration.py` | 177 | 83 | 0 | 177 | certified honest minimum |
| `.ufo/waves/round-63/c63_quote_tool.py` | 92 | 51 | 0 | 92 | certified honest minimum |

Measured composition (docstring / comment / code / blank):

```
quote_class.py      15 / 1 / 114 / 17
extract_text.py     13 / 2 /  71 / 17
c63_calibration.py  32 / 6 / 119 / 20
c63_quote_tool.py   12 / 1 /  68 / 11
```

The docstrings are the largest non-code share and are load-bearing: the C1
counter's docstring is the component map that `corpus/QUALITY.md:1416` (round-63
criterion) and the contract's "Component semantics" paragraph refer to. Cutting
them would delete the binding between predicate prose and code, not weight.

## Baseline reproduced (frozen claim untouched)

The four artifacts are unmodified; their digests equal the contract pins
(`.ufo/waves/round-63/contract.md:23,56,65`):

```
$ sha256sum scripts/quote_class.py .ufo/waves/round-63/c63_calibration.py \
    .ufo/waves/round-63/c63_quote_tool.py .ufo/waves/round-63/quote-class/extract_text.py
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  scripts/quote_class.py
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91  .ufo/waves/round-63/c63_calibration.py
9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e  .ufo/waves/round-63/c63_quote_tool.py
6b0a88cddfa3b712e8fdbe69c4c2803c816490cd43893972dfe0d39d5f362405  .ufo/waves/round-63/quote-class/extract_text.py
```

Each counter run at the measured commit and at base reproduces its committed
receipt line and exit code **byte-identically**:

```
.ufo/waves/round-63/controls/after-c1.txt   stdout_identical=True exit_identical=True rc=0
.ufo/waves/round-63/controls/base-c1.txt    stdout_identical=True exit_identical=True rc=1
.ufo/waves/round-63/controls/after-c2.txt   stdout_identical=True exit_identical=True rc=0
.ufo/waves/round-63/controls/base-c2.txt    stdout_identical=True exit_identical=True rc=1
```

The tool at the measured commit is the worktree tool
(`git show 05b0d7f4…:scripts/quote_class.py | sha256sum` → `431e75e8…`).

## Deletion candidates in `scripts/quote_class.py` (behavior-identical)

1. **`class UsageError(Exception): pass` — lines 28–30, plus one following blank.**
   Dead adapter: the class is never raised, caught, imported or referenced.
2. **`return 64` — line 143, immediately after `ap.error(...)`.**
   Unreachable: `ArgumentParser.error` ends in `self.exit(2, …)`, and
   `ArgumentParser.exit` calls `_sys.exit(status)`; `return` is never evaluated.

Proof of death (no `lsp` device is mounted in this session — the LSP path is
unavailable, so this is an AST + instrumented-run proof, not a semantic server
proof):

```
$ python3 - <<'PY'   # AST scan of all four files: unreferenced module defs,
                     # Name stores never loaded, unused imports, dead local stores
quote_class.py            imports_unused=['annotations'] unreferenced_defs=['UsageError']
extract_text.py           imports_unused=['annotations'] unreferenced_defs=[]
c63_calibration.py        imports_unused=['annotations'] unreferenced_defs=[]
c63_quote_tool.py         imports_unused=['annotations'] unreferenced_defs=[]
per_func_dead_stores: {} in every file
module_names_stored_never_loaded: [] in every file
```

`annotations` is the false positive of `from __future__ import annotations` (a
compiler directive, not a name). So `UsageError` is the **only** dead symbol in
the four files — it does not even appear as a `Name` node, only as its
`ClassDef` binding.

Unreachability demonstrated by instrumenting the reduced copy (`ap.error(...)`
followed by `print("REACHED-RETURN-64")`):

```
$ python3 -B <scratch>/quote_class.instr.py
usage: quote_class.instr.py [-h] [--selftest] [--json] {classify} ...
quote_class.instr.py: error: one of --selftest or classify is required
instr-noargs-exit=2          # no REACHED-RETURN-64 line
```

## Deletion candidate in `extract_text.py` (behavior-identical)

**Lines 85–87**, the second selftest assertion:

```python
        if "&lt;" in got or "var a" in got:
            print("selftest FAIL: double-escape or script leak")
            return 1
```

Unreachable-false: it executes only when line 82's `got != want` was false, i.e.
`got == "Tom & Jerry multi line text second a b\n"`, a string containing neither
`&lt;` nor `var a`. Any leak makes `got != want` and is caught by the first
assertion. Instrumented copy prints the condition at the reached point:

```
$ python3 -B <scratch>/extract_text.instr.py --selftest
CHECK-REACHED False
selftest 1/1
instr-selftest-exit=0
```

## A/B equivalence harness (original vs reduced)

Both variants were copied to scratch under the *same basename* so argparse
`prog` output is comparable; the oracle is the lane root (the tool binds fixture
resolution to `cwd`).

```
quote_class selftest         exitA=0 exitB=0 identical=True
quote_class selftest-json    exitA=0 exitB=0 identical=True
quote_class classify-hit     exitA=0 exitB=0 identical=True
quote_class classify-json    exitA=2 exitB=2 identical=True
quote_class classify-absent  exitA=0 exitB=0 identical=True
quote_class classify-missing exitA=2 exitB=2 identical=True
quote_class noargs           exitA=2 exitB=2 identical=True
quote_class bogus-sub        exitA=2 exitB=2 identical=True
quote_class all-identical: True

A render exit 0 stdout: extracted 1854393 bytes -> 286933 chars
B render exit 0 stdout: extracted 1854393 bytes -> 286933 chars
render sha A: 8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69
render sha B: 8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69
committed  : 8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69
extract selftest     exitA=0 exitB=0 identical=True
extract missing-args exitA=2 exitB=2 identical=True
```

The reduced tool also satisfies the C2 counter's predicate if its sha were
re-frozen (`total=4 passed=4`, the four frozen ids exact, `derived==expected`,
`met=True`). Both reduced files lose their pins: `quote_class.py` 147→142 lines
`431e75e8…`→`8579080b…`, `extract_text.py` 103→100 lines `6b0a88cd…`→`05ca66d2…`.

## Why even the free deletions do not land in round 63

`scripts/quote_class.py`'s sha256 is the C2 freeze. The counter does **not**
hash the tool blob it runs (`c63_quote_tool.py:56-60` reads the blob and writes
it to a temp file); the sha pin lives only in the contract prose. So a reduced
tool would still print `met=true`, but the contract's stated pin and the
freeze-note would be false — a re-freeze with re-issued receipts, which the
contract forbids mid-round ("a counter, control or predicate changed after a
seat has scored is not this round's rule"). Deleting 5 lines for a byte-pin
invalidation is a net loss.

## Rejected candidates (each changes behavior or the freeze, or trades an axis)

| candidate | saving | why rejected |
|---|---|---|
| Trim `BLOCK` in `extract_text.py` to the tags in S432.html (13 of 35 absent; `br` kept for the selftest) | 3 lines | Output on the pinned input is byte-identical (proven: `cmp S432.trim.txt …/S432.txt` → `TRIM_OUTPUT_BYTE_IDENTICAL`, selftest `1/1`), but the documented contract is *textContent semantics*, so trimming narrows the recipe to one input. Harms fidelity for a 3% win. |
| Share the verbatim `git_show` block (9 lines, byte-identical in both counters) | ~6 net | Adds a third frozen artifact and decouples counter semantics from the pinned per-counter sha; the wave's freezable unit is the single file named by each counting command. |
| Drop C1's inline `classify()` (6 lines) | 6 | Contract-mandated separability: C1 must be verifiable where the C2 tool never landed, and must never gate on it. |
| Drop C1's `unresolved` field (1 line) | 1 | Printed in `after-c1.txt`, `base-c1.txt`, both control receipts; removing it makes the committed receipts unreproducible. Display-only to `met`, so no predicate gain. |
| Drop C1's `spot` precondition (`exit 2`) | 2 | Changes exit `2`→computed on a tree missing the round-61 verdict; the counter would evaluate against a tree that lost the evidence it is resolving. |
| Drop C2's `total == passed` conjunct | 1 | Deliberate defense-in-depth against a stub reporting `ok` with a different case set; not semantic dead weight. |
| Collapse the four `FROZEN_QUOTE` authorities (counter, tool case, ledger, prose) | 0 | Each is a distinct authority and the counter cross-checks them (`row.get("quote") == FROZEN_QUOTE`); collapsing removes a check. |
| Move `--json` onto the `classify` subparser | 0 | Would add a flag, not delete. See stale-doc finding below. |

Marker conjuncts that remain in `resolved` (`criterion`, `lesson_gate`,
`[r63-correction`/`LEDGER_REL` locator inside `quote_correction`) are all
narrowing AND-terms; none is the sole truth-maker, because `quote_correction`
is gated by `blobs_match` and `class_match`, re-derived from committed bytes.
The round-62 false-green class is therefore not reachable by deleting anything —
nothing here is safe to cut.

## Stale documented path (finding, not a deletion)

`scripts/quote_class.py:12` documents
`quote_class.py classify --quote "..." --raw <file> --text <file> [--json]`, but
`--json` is registered on the top-level parser, so the documented placement
fails:

```
$ python3 -B scripts/quote_class.py classify --quote "quick brown fox" \
    --raw scripts/fixtures/quote-class/inline.raw.html \
    --text scripts/fixtures/quote-class/inline.txt --json
quote_class.py: error: unrecognized arguments: --json      # exit 2
$ python3 -B scripts/quote_class.py --json classify ... → {"derived": "raw-substring"}   # exit 0
```

One-line doc correction (or moving the flag to the subparser); no size win, and
it touches a pinned file, so it is deferred with the deletions above.

## Recommendation

Round 63: **change nothing** — every artifact is at its honest minimum for the
frozen claim, and the only provable deletions (5 + 3 lines = 1.5% of the four
files) cannot pay their re-freeze cost mid-round. In a future round that
already re-freezes the tool, take both deletions together (single sha churn +
one receipt re-issue), prioritizing `quote_class.py`'s dead class/return
(zero-semantics) over `extract_text.py`'s redundant assertion (zero-semantics
but not sha-pinned, so it can land alone cheaply).

## Hygiene

- Read-only against the fleet root: no commits, no git/jj mutation, no edits to
  tracked files. `git status --porcelain` before and after this seat's work is
  identical (`?? .ufo/waves/round-63/w1.ready`, `?? …w1.ready.dispatched`,
  `?? …w1/`); `git diff --stat` empty.
- Scratch: `/fast/scratch/hyaku/kake-r63/SimplifyToolReview/` (created with
  copies only, no git fixture, no commits) and `/tmp/r63sim_c{1,2}.txt` were
  deleted; no residue. Nothing written outside this Report.
- No tool installs (no pacman; nothing needed).
- `lsp` device is not mounted in this session (`read xd://lsp` → "No such tool"),
  so absence of callers is evidenced by AST reference analysis plus an
  instrumented run, with grep used only as a literal cross-check
  (`grep -rn "import quote_class\|from quote_class\|import extract_text\|from extract_text"` → `none`). No grep result is presented as semantic proof.
