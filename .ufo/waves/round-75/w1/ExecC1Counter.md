# ExecC1Counter — C1 counter hardening (kake, round 75, wave w1)

## Deliverable

| Item | Value |
|---|---|
| Counter | `.ufo/waves/round-75/w1/ExecC1Counter/c75_row_truth.py` |
| sha256 | `63e321b28e509781405f1b4209a66b99460bc2512c92a8615fec06f2423e944b` |
| Bytes / mode | 47,446 B, `-rwxr-xr-x` |
| Lands at (contract §C1) | `.ufo/waves/round-75/c75_row_truth.py` — L1 lands it; the lane tree was not edited by this seat |
| Receipts | same dir: `base-c1-row-truth.txt`, `base-c1-row-truth.json`, `ctl-cheapcontent.txt`, `ctl-deletion.txt`, `selftest.txt`, `population.txt` |

`--revision c9c5e484 --base c9c5e484` reproduces the frozen base control; the
other two controls were rebuilt in scratch from a `git clone --shared` of the
lane (sandbox commits `e17db307`, `153fa2a9`; the sandbox clones and their work
trees were removed with the scratch root).

## Measurement (frozen predicate, unchanged)

Population rule, effective-row rule (last row naming a file wins), E1–E4,
`append_only`, `met = (mismatches == 0) and append_only` and the 0/1/2/64 exit
contract are the contract's. Amendment 1 and Amendment 2 terms are implemented
as landed, not restated:

- `missing_frozen=<N>` is appended to the summary line (contract fields keep
  their order, so the frozen base line remains an exact prefix); one finding per
  frozen path the derivation no longer produces; `--population FILE` is a
  newline-separated floor, default the contract's 16 paths in contract order.
- E1/E2 own-self-test: the recorded command's *program* must be the effective
  row's instrument. Shell comments are stripped; leading `VAR=value`/`env` are
  skipped; the file after `python`/`python3`/`python3.N` (optional `-B`) or
  `node` is compared with the instrument. A mismatch is
  `E1 command names <other> not <instrument>`, whatever the exit code.
- `differential` is matched with `\bdifferential\b` against the **Kind cell
  only** (`nondifferential` does not exempt; the word elsewhere in the row does
  not exempt).
- E4 covers **every live row's** cells, not only the effective row; findings are
  attributed to the row's instrument (or `row <line>` when it derives none) and
  deduplicated by finding text.
- E2 measures only a bound command's output, and an ambiguous tally in the claim
  segment is an `E2 ambiguous tally` finding.

Summary line: `C1v1 revision=<rev> rows=N live=N files=N mismatches=M
classes=… append_only=<bool> met=<bool> missing_frozen=N`.

## Added surface

- `--selftest`: 23 isolated fixture repositories + 6 harness checks = **29
  checks**. Fixtures: red/green for E1, E2, E3, E4; superseding row; deleted
  base row (`append_only=false`); historical-relabel floor loss; retired-in-place
  floor loss (ReviewerC1 F11: committed file survives, row rewritten with no path
  token, prose Name retained, 3-path floor → `missing_frozen=1`); file deleted
  with the row retained (E4 red); distinct fixture-id count; all green;
  ambiguous tally (`0/3 then 3/3`); `nondifferential`; comment-laundered and
  argument-laundered command binding; non-interpreter program; `differential`
  word outside the Kind cell. Each fixture is `git init -b main` in its own dir
  under `--work/selftest/<id>/repo`, measured through a fresh `clone --shared`
  tree and a scratch tree outside it.
- Harness checks: frozen floor is the 16-path list; `--emit-population`; usage
  exit 64; non-repository exit 2; missing `--work` exit 64; `--population FILE`
  loads a 3-path newline-separated floor.
- `--json`: schema `c1-row-truth/v1` with the per-file result list
  (`file,row_line,family,frozen,command,program,exit,status,mismatch`), counts,
  classes, population, derived files, missing-frozen paths and findings.
- `--emit-population`: the effective floor, one path per line; equals contract
  §C1's 16 exactly.

## Verification (final bytes)

| Check | Command | Result |
|---|---|---|
| Self-test | `python3 -B .ufo/waves/round-75/w1/ExecC1Counter/c75_row_truth.py --selftest --work <scratch>` | `C1v1 selftest fixtures=29 passed=29 failed=0` / `selftest 29/29`, exit 0 (`selftest.txt`) |
| Base | `… --root . --revision c9c5e484 --base c9c5e484 --work <scratch> --json` | `C1v1 revision=c9c5e484 rows=28 live=16 files=16 mismatches=2 classes=E1 E3 append_only=true met=false missing_frozen=0`, exit 1 |
| Base findings | same | `E1 .ufo/waves/round-69/c69_tmp_honour.py`; `E3 .ufo/waves/round-74/c74_registry_gap.py` (exact frozen text) |
| Cheap content | sandbox `e17db307`: two appended rows repeating the wrong claims | `rows=30 live=18 files=16 mismatches=2 classes=E1 E3 append_only=true met=false missing_frozen=0`, exit 1 — matches the frozen control exactly |
| Deletion | sandbox `153fa2a9`: the `c69_tmp_honour.py` row removed | `rows=27 live=15 files=15 mismatches=3 classes=E3 append_only=false met=false missing_frozen=1`, exit 1 — `append_only=false` as required; the extra finding is Amendment 1's `missing_frozen` finding (see delta below) |
| Population | `--emit-population` | 16 lines, byte-equal to contract §C1's list in order |
| JSON | base run with `--json` | 16 per-file results: 14 `ok`, 2 `mismatch`; `derived_files` 16; `missing_frozen_paths` `[]` |

Wall times: base 27.2 s, cheap content 27.4 s, deletion 28.5 s, self-test 0.4 s
(all four from the final bytes).

## Deltas the L1 must adjudicate (not silently changed)

1. **Deletion control count.** The frozen table pins `mismatches=2` for the
   deletion control. Amendment 1 requires one finding per missing frozen path;
   deleting the `c69_tmp_honour.py` row drops that frozen path from the
   derivation, so the delivered counter reports `mismatches=3` with
   `missing_frozen=1` (the other two findings are the same E3 and the
   append-only finding). `append_only=false met=false` are unchanged. The
   control receipt row needs re-pinning to 3, or the frozen 2 stands against a
   counter that does not implement A1. I did not weaken A1 to preserve 2.
2. **E2 ambiguity scope (F15).** A literal cell-wide "more than one distinct
   `a/b` pair is a finding" reddens the frozen base: the base row
   `scripts/citation_lint.py` records `9/9` (current) and `8/8` (the round-47
   receipt's then-tally) in the *same* cell, so the base would become
   `mismatches=3 classes=E1 E2 E3` and the frozen base receipt would be false.
   Implemented rule: the claim segment is the text after the recorded command up
   to its first `;`; a contradiction inside that segment (`0/3 then 3/3`, fixture
   f15) is `E2 ambiguous tally`, while a later-segment historical tally is not a
   claim. This keeps the mandated base at 2 and makes the F15 attack red; the
   docstring states the rule and the reason. If the L1 prefers the strict
   cell-wide reading, the frozen base control must be re-pinned first.

## L1-applied changes retained (as instructed)

The L1 patched this file in place at 21:12 with `command_program()`, the
word-boundary `differential`, a whole-live-row E4 pass and fixtures f17 (binding
red), f18 (`nondifferential` red), f19 (secondary-row E4 red). All three
fixtures are retained and pass; `command_program` is the single binding helper
(the interim file carried it beside an equivalent duplicate, which was merged
here) and keeps the L1's clauses plus `node`/`python3.N` interpreters and quote
stripping. No clause was removed or reordered. The L1's reported 22/22 became
**29/29** because this seat added f15 (ambiguous tally), f16 (argument
laundering), f20 (retired-in-place F11), f21 (file-gone row-kept), f22
(`differential` elsewhere), f23 (non-interpreter program) and harness h06
(`--population FILE`).

## Risks / notes for the after-state

- New round-75 registry rows are in-population (A1). Their Self-test command must
  name their own instrument path as the *program* (a comment or trailing argument
  will not bind), and every `.py`/`.mjs` token in every live row must resolve.
- The self-test tally is `29/29` (23 fixtures + 6 harness checks). A registry row
  that enumerates fixture ids must enumerate 29 distinct ids, or omit ids; 23
  ids against the observed total 29 is an E3 mismatch.
- Lane HEAD moved during the wave (`ab939c46` → `4e3fc159`, including amendment 2
  at `d599c8be`); all receipts here name the revision they measured
  (`c9c5e484` plus the two scratch sandbox commits). The seat made no commits
  and ran no mutating git command in the lane; only read-only `git show/status`.
- Editing race: the counter was co-edited by the L1 at 21:12. The delivered bytes
  are this seat's coherent version; if the L1 re-patches, re-run the self-test and
  the base line before landing.

## Write scope and scratch

Written: this report, `w1/ExecC1Counter/c75_row_truth.py` and its six receipts.
No lane production file, no MANIFEST/state/watchdog/scratch of the fleet, no
sibling lane. Scratch root `/fast/scratch/hyaku/kake-r75/ExecC1Counter/` was
used only for work trees, sandbox controls and TMPDIR; it is removed before this
seat yields. No tool installed or upgraded.
