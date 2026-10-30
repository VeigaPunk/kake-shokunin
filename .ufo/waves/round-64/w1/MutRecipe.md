# MutRecipe — mutation test of the C1 recipe binding (round 64)

Seat: MutRecipe (leaf, no subagents). Target: frozen counter
`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py`
(sha256 `5489eb2f3ac498e0383d841c677f036231fbf6933717d8da447f3193ff088adf`, verified on disk),
measured revision T0 `4c8295fa5e3b628f1fdf3840299ae415c01849fb`, base `1a481315`.

## Verdict

- All required mutants make the frozen counter print `met=false`, exit 1, no traceback.
  Recipe mutants R1, R2a, R2b, R3a, R3b are caught by `pin_drift=drift:recipe`. Text
  mutants T1, T2, T3, T5 are caught by `pin_drift=drift:text`. The `recipe_output_differs`
  path is not reached in the unpatched runs, because the recipe block runs only when
  `pins` is 1 (line 221).
- Two gaps found, both outside the frozen predicate's control set:
  1. **Block-tag mutants R3a/R3b escape the in-counter recipe re-execution.** With the recipe
     pin bypassed, the counter prints `met=true`. Only the recipe byte pin catches them.
  2. **Re-pinning the counter's own constants defeats it.** A circular fabrication (recipe
     R1 plus text regenerated from R1, both constants re-pinned in a copy of the counter)
     prints `met=true`. The counter does not check its own bytes; the external sha freeze
     is the only guard.
- Minor diagnostic defect: with any pin drift, `ledger_state` prints `ledger_absent` even
  though the ledger blob exists. It is set by `parse_ledger(None)` (line 220, label at line 136).
  It does not affect `met`.
- Controls: the unmutated T0 fixture prints `met=true` on CPython 3.10–3.15 (see "Interpreter
  stability"), so the fixture builder reproduces the lane result.

## Method (exact)

All work under `/fast/scratch/hyaku/kake-r64/MutRecipe/`. The lane was only read
(`git -C <lane> show 4c8295fa:<path>`; the counter was run with `--root <lane>` only for the
baseline). Nothing in the lane was written. Each fixture is a fresh `git init` repo with
`git -C <dir> rev-parse --show-toplevel` asserted equal to the dir before commit. Each fixture
holds the nine blobs the counter reads at T0 (raw, flat text, ledger, recipe, spot-check,
knowledge, QUALITY, lesson, SOURCES), with one blob overridden per mutant. The frozen counter
is run unchanged as

    TMPDIR=/fast/scratch/hyaku/kake-r64/MutRecipe/tmp \
      python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py \
      --root <fixture> --revision HEAD

Driver: `python3 -B driver.py` (scratch; run time 4.7 s). Baseline run against the lane
(exact output):

    $ python3 -B c64_calibration.py --root $L --revision 4c8295fa5e3b628f1fdf3840299ae415c01849fb
    revision=4c8295fa… disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true   (exit 0)
    $ python3 -B c64_calibration.py --root $L --revision 1a48131577ba82c967650561be34e8dba909432a
    … unresolved=1 met=false   (exit 1)

Fixture control F0 (unmutated T0 blobs in a fresh repo): identical line, `met=true`, exit 0.

### Mutants

Recipe mutants are text edits of `.ufo/waves/round-63/quote-class/extract_text.py` (lines
21–24 BLOCK, 27 SKIP, 57 whitespace collapse, 60 `extract`). The raw blob is the real
T0 blob (sha `63b0a018…911b`) in every case. Each mutant's direct output was compared with the pinned flat text.

| id | mutation | direct output == pinned text? |
|---|---|---|
| R1 | `SKIP = {"script","style","noscript"}` → `{"noscript"}` (script/style skip removed; S432.html has 8 `<script`, 3 `<style`) | no |
| R2a | whitespace collapse `" ".join(...split())` → `"".join(...split())` | no |
| R2b | whitespace collapse → `" ".join(...split(" "))` (ASCII spaces only) | no |
| R3a | BLOCK drops `"p"` | **yes** |
| R3b | BLOCK → `{"div"}` only | **yes** |
| R4 | comment-only append (control for byte-pin strictness) | yes |
| R5 | `extract` raises `RuntimeError` | n/a (raises) |

Text mutants edit `.ufo/waves/round-63/quote-class/S432.txt` with the recipe unchanged:

| id | edit | committed text sha vs pin `8b90d096…2a69` |
|---|---|---|
| T1 | quote word `destination` → `target` (recipe output equals ORIGINAL text) | differs |
| T2 | append `planted trailing line` (outside the quote) | differs |
| T3 | quote sentence replaced with `removed.` | differs |
| T5 | one space doubled (whitespace-only) | differs |

Each mutant was run in two forms:

- **unpatched**: the frozen counter, unchanged, on a fixture holding the mutated blob.
- **pin-bypassed** (mechanism probe): a scratch copy of the counter with only the pinned literal
  for the mutated blob replaced by the mutant's sha, e.g. `RECIPE_SHA` line 69. The diff is
  exactly one line (`diff c64_calibration.py <copy>`, shown for R1 below). This tests whether
  the in-counter re-execution (lines 221–230) catches the mutant with the pin no longer in the way.
  It is not a lane edit and not a claim of a shipped defect.

## Results

Unpatched (frozen counter, unchanged):

| case | exit | pin_drift | recipe_rederive | ledger_state | met | catching mechanism |
|---|---|---|---|---|---|---|
| R1 skip removed | 1 | drift:recipe | 0 | ledger_absent (artifact) | false | recipe sha pin |
| R2a whitespace → nothing | 1 | drift:recipe | 0 | ledger_absent | false | recipe sha pin |
| R2b whitespace spaces-only | 1 | drift:recipe | 0 | ledger_absent | false | recipe sha pin |
| R3a block drop p | 1 | drift:recipe | 0 | ledger_absent | false | recipe sha pin |
| R3b block only div | 1 | drift:recipe | 0 | ledger_absent | false | recipe sha pin |
| R4 comment only | 1 | drift:recipe | 0 | ledger_absent | false | recipe sha pin (output unchanged; byte-strict) |
| R5 raise | 1 | drift:recipe | 0 | ledger_absent | false | recipe sha pin |
| T1 quote word edit | 1 | drift:text | 0 | ledger_absent | false | text sha pin |
| T2 outside-quote append | 1 | drift:text | 0 | ledger_absent | false | text sha pin |
| T3 quote removed | 1 | drift:text | 0 | ledger_absent | false | text sha pin |
| T5 whitespace-only | 1 | drift:text | 0 | ledger_absent | false | text sha pin |

Pin-bypassed (scratch counter copy, recipe or text constant re-pinned to the mutant):

| case | exit | pins | recipe_rederive | ledger_state | met | catching mechanism |
|---|---|---|---|---|---|---|
| R1 skip removed | 1 | 1 | 0 | **recipe_output_differs** | false | in-counter re-execution |
| R2a | 1 | 1 | 0 | **recipe_output_differs** | false | in-counter re-execution |
| R2b | 1 | 1 | 0 | **recipe_output_differs** | false | in-counter re-execution |
| R3a block drop p | **0** | 1 | 1 | ok | **true** | **none — escapes** |
| R3b block only div | **0** | 1 | 1 | ok | **true** | **none — escapes** |
| R5 raise | 1 | 1 | 0 | **recipe_exec_failed:RuntimeError** | false | in-counter re-execution |
| T1 quote word | 1 | 1 | 0 | **recipe_output_differs** | false | in-counter re-execution |
| T2 outside-quote | 1 | 1 | 0 | **recipe_output_differs** | false | in-counter re-execution |
| T3 quote removed | 1 | 1 | 0 | **recipe_output_differs** | false | in-counter re-execution |
| T5 whitespace-only | 1 | 1 | 0 | **recipe_output_differs** | false | in-counter re-execution |

Circular fabrication (scratch counter copy with both `RECIPE_SHA` and `TEXT_SHA` re-pinned;
fixture holds recipe R1 and `S432.txt` regenerated from R1's output):

    exit=0 … pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 … lesson_gate=1 … unresolved=0 met=true

The diff of that scratch counter against the frozen one is two lines only:

    67c67  TEXT_SHA = "8b90…2a69"  →  "ae41e2f2…fe1f3"
    69c69  RECIPE_SHA = "6b0a…5405" →  "8d6b67e2…95387"

## Findings

**F1 — block-tag mutants escape re-execution (gap, medium).** R3a and R3b change block-level
semantics (`extract_text.py` lines 21–24). The recipe's behavior does change, as a synthetic
check shows: `extract(b"<p>a</p><p>b</p>")` gives `'a b\n'` for the base recipe, `'ab\n'` for R3a
and R3b. But the pinned raw never exercises it: over the 7,618 block-tag occurrences in
`.ufo/waves/round-61/sources/S432.html`, a regex found **0** block tags abutting non-whitespace
text, so removing a block boundary changes nothing on that input. The re-execution gate (lines
221–230) therefore cannot tell R3 from the base. Only the recipe byte pin (line 69, sha
`6b0a88cd…`) catches R3. Any change to the recipe that keeps it byte-equivalent in output on
the pinned raw would be invisible to the re-execution. The frozen predicate's controls and
selftest include no recipe-mutation case: the selftest's only recipe fixture is junk
(`counter` lines 367 and 376, `load_recipe` at 411), and the fabrication control reuses the
real recipe. So this gap is not reported by any control receipt.

**F2 — counter does not self-verify; circular fabrication passes if its constants are
re-pinned (residual, not a counter defect within the frozen scope).** The re-execution and
pin logic both depend on the counter's own `RECIPE_SHA`/`TEXT_SHA`/`RAW_SHA` literals (lines
64–69). Edit those literals and regenerate `S432.txt` from a mutated recipe, and the counter
prints `met=true`, exit 0. The only defense is the external freeze: the on-disk counter's sha is
`5489eb2f…` (matches contract). I did not treat this as a C1 kill-rule breach. It needs the
frozen counter to be replaced, which the freeze forbids and which I did not do in the lane. It
does mean the counter's guarantee against circular fabrication is exactly as strong as the
external sha check, and the counter itself cannot tell a re-pinned copy from the original.

**F3 — pin is byte-strict (over-strict, safe).** R4 (comment-only recipe change, output
identical) fails with `drift:recipe`. The check is a sha of the file, not of its behavior, so
legitimate recipe maintenance will be flagged. That is a false-negative risk for maintenance,
not a bypass.

**F4 — misleading `ledger_state` label (diagnostic only).** On any pin drift, line 220 calls
`parse_ledger(None)` (`blobs["ledger"] if pins else None`), and line 136 returns
`"ledger_absent"`. Every pin-drift run in this seat prints `ledger_state=ledger_absent` even
though the ledger blob is present. No effect on `met`; it would mislead a reader.

**F5 — recipe re-execution is redundant with the pins for the recipe bytes (design note).**
Because re-execution is gated on `pins` (line 221), it only runs when the recipe sha already
matches. Its added value is therefore limited to verifying that the pinned recipe reproduces the
pinned text on the pinned raw. That is what F1 shows is blind to block-set semantics.

## Interpreter stability (recipe re-execution is environment-sensitive)

Installed interpreters (already present, no installs): `/usr/bin/python3.14` (3.14.8),
`~/.local/bin/python3.13` (3.13.16), `python3.12` (3.12.15), `python3.11` (3.11.17),
`uv`-managed 3.10.22 and 3.15.0. The unmutated control fixture prints the same
`met=true` line on every one, exit 0. PyPy and 3.14t were not tested.

## Tooling

No tools installed, upgraded or removed. Used `python3` 3.14.8, `git`, `grep`, `diff`, `sha256sum`,
and the already-installed CPython interpreters listed above. No pacman, no ~/.local/bin writes.

## Scope and bounds respected

- Lane working tree untouched: `git -C <lane> status --porcelain --untracked-files=no` = 0 tracked
  changes. No git mutation anywhere. Lane git only read (`show`, `rev-parse`).
- Frozen counter, controls, receipts, contract and lesson not edited (on-disk counter sha confirmed).
- Only written: this report, and scratch under `/fast/scratch/hyaku/kake-r64/MutRecipe/`
  (deleted before yield).
