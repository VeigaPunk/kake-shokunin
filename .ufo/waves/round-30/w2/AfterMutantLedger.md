# Wave 2 — AfterMutantLedger: after-repair mutant ledger of citing-set reason codes

Seat KakeR30.AfterMutantLedger (leaf), milestone r30-falsify, axis operability. Target: C1 repair
revision 71c6bfabd7aa957d15732d9224888bb32849238a, with the same per-code rename procedure the
wave-1 base ledger used (`.ufo/waves/round-30/mutant-ledger/mutate.py`, base
035668132250b75b38d399e86e540b0a0371efbc).

## What I attacked

The wave-1 base ledger measured 23 reason codes and found 0 of 23 killed: the base runner compared
finding ids and exit codes only, never the reason field. C1 claims the repair closes that gap (the
runner now compares the sorted multiset of `(id, reason)` pairs, and fixtures 30-41 name reasons).
This seat repeats the identical rename procedure against the repair revision.

## Instrument and procedure (same as wave 1, two recorded differences)

* Detector `python3 -B <tree>/scripts/citing_set_selftest.py --root <tree> --tmpdir <scratch>`: killed =
  runner exit != 0, survived = runner exit == 0. Mutation: every double-quoted occurrence of `"<code>"`
  in `scripts/citing_set.py` becomes `"<code>_mutated"`; one tree copy per code; exported tree bytes never
  written. Probe: one tree per code that provokes the code, pristine and mutated gate compared on it (an
  unobservable rename would be an equivalent mutant, not a survivor).
* Difference 1: the extractor now resolves module-level string constants. The repair routes
  `document_duplicate_key` and `document_nonfinite_number` through `F_DUPLICATE_KEY` /
  `F_NONFINITE_NUMBER`, so the wave-1 extractor saw 23 codes and this one sees 25. Completeness verified:
  the only reason sites in the gate are the `InputInvalid` arguments and the two literal `"reason"` dict
  values (`base/scripts/citing_set.py:203,573,575,582,678,690`).
* Difference 2: fixture coverage is measured with the committed runner's own `case.json` setup (fifo,
  mkdir, git_init, git_commit), so the observed reasons are the ones the fixtures really produce.
* Wave-1 note for the L1: the wave-1 probes for `absolute_path_not_allowed`, `empty_path` and
  `path_escapes_root` appended a second `--population`; the repair makes a repeated `--population` a
  usage error (exit 64), so a verbatim copy of the wave-1 driver reports `probeProvokesCode=false` for
  those three codes at 71c6bfa. My driver replaces the single `--population` value instead.

## Commands (all exit codes observed)

```
git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin clone            exit 0
git -C clone archive 71c6bfa... | tar -x -C base                          exit 0
TMPDIR=.../scratch python3 -B mutate_after.py                              exit 0
venv/bin/python -B mte_report_after.py                                     exit 0
node official_metrics_after.mjs                                            exit 0
```

Driver output `codes 25, killed 13, survived 12`; all 25 probes provoked their code and all 25 mutants
changed the gate's own JSON output (`codesProvokedByProbe 25`, `codesChangingGateOutput 25`,
`codesWithEquivalentMutant []`). Controls in the ledger: K-baseline pristine tree, runner exit 0, 41
cases, 0 failed; K-positive `"input_invalid"` renamed to `"input_invalid_control"`, runner exit 1, 41
cases, 14 failed — the detector kills a mutation of the field it compares, so a survivor is a coverage
gap, not a broken detector.

## Per-code result (25 codes)

Killed, runner exit 1 (13): corpus_directory_missing (32-corpus-directory-missing); corpus_empty
(33-corpus-empty); descending_range (13-descending-range); document_duplicate_key
(38-document-duplicate-key); document_nonfinite_number (39-document-nonfinite-number,
41-document-nonfinite-overflow); document_not_json (15-invalid-json-population,
31-document-not-json); document_not_regular_file (30-document-not-regular-file); document_shape_invalid
(16-invalid-population-shape); not_a_directory (34-not-a-directory); population_id_unreachable
(35-population-id-unreachable, 40-population-id-short-digits); revision_not_found (36-revision-not-found);
root_not_repository_top_level (37-root-not-repository-top-level); span_too_large (14-oversize-range).

Survived, runner exit 0 (12), none named by a committed fixture: absolute_path_not_allowed;
corpus_directory_unreadable; corpus_file_not_utf8; document_not_utf8; document_unreadable; empty_path;
git_command_failed; git_unavailable; not_a_regular_file; path_escapes_root; root_not_a_directory;
symlink_rejected.

Every kill is a `finding mismatch` on the `(id, reason)` pair, e.g. `expected [["input_invalid",
"corpus_empty"]], observed [["input_invalid", "corpus_empty_mutated"]]`.

## Totals

* Before (base 0356681, wave-1 ledger): 23 codes, **0 killed, 23 survived**. After (71c6bfa, this
  ledger): 25 codes, **13 killed, 12 survived**. The 13 killed codes are exactly the 13 codes a
  committed fixture names; the 12 survivors are exactly the 12 codes with no fixture (cross-check: the
  reasons actually observed across all 41 fixture runs are 13 distinct codes, none of them a survivor).
* Official-style metrics from the vendored mutation-testing-metrics 3.9.0 library: totalMutants 25, killed
  13, survived 12, totalCovered 25, mutationScore 52. The MTE report validates against the vendored
  official schema 3.9.0 (`schema 3.9.0 validation: OK`).

## Reading of the survivors (coverage finding, not a contract change)

The 12 survivors are reason codes no committed fixture produces, so renaming them is invisible to the
runner. Each is nevertheless observable (pristine gate reports the code, mutant reports
`<code>_mutated`), so none is an equivalent mutant. Closing them needs a fixture per code; that is a
work item, not a reason to change the gate's contract.

## Evidence pointers

* Sandbox ledger `/fast/scratch/hyaku/kake-r30/w2/AfterMutantLedger/after-71c6bfa-ledger.json` (sha256
  14fdb7d98d45c93eac07bd24cf901e17d0414fd2832a11947b564148fb5116c1); MTE-shaped file
  `/fast/scratch/hyaku/kake-r30/w2/AfterMutantLedger/after-71c6bfa-ledger.mte.json` (sha256
  86241963dcd3d0cb77208e48c66944356b3884865d28cb0cf5ba9e7a2207b4d7). Driver and reporters
  (`mutate_after.py`, `mte_report_after.py`, `official_metrics_after.mjs`) sit in the same sandbox; the
  vendored schema and metrics library were copied from the wave-1 sandbox.
* Pristine gate at 71c6bfa sha256 dbfade45e59351fb5edc010dfc45a4e15e1213fdb6fad9ec1668ffd3b77b7f02;
  pristine runner sha256 0fc87d5b8134c841b02d0db33d8a3262fb774d0c8aacaefc6b6811f190b6530a; both equal
  `git show 71c6bfa:<path> | sha256sum` and are unchanged after the run (`gateSha256AfterLedger` ==
  `gateSha256`): every mutant ran in its own copy under `work/`, deleted after each code. No lane
  repository file was written by this seat except this report; the working-tree modifications in
  `git status` (PROVINCE.md, SKILL.md, corpus/*) are other seats' edits.

## Not verified

* I did not re-run the C1 counter or the strict checker; this seat measured gate and runner directly. I
  did not attempt mutations other than the rename, and did not test the usage-error paths (repeated
  options, exit 64) or the deep-directory walk. The "before" column comes from the wave-1 ledger; I did
  not re-measure base revision 0356681. Tooling: `jsonschema` 4.26.0 installed with `uv pip install
  --python venv/bin/python jsonschema` (PyPI through uv) into the sandbox venv only, because the MTE
  report validates against the vendored official schema with it; no system package was installed.
