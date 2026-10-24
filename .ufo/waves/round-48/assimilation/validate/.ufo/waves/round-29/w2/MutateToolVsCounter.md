# Round 29 wave 2 — C2 counter strength against scripts/base_path_audit.py (mutation probe)
Seat MutateToolVsCounter (leaf, falsify), axis operability. Item attacked: the C2 counter
`.ufo/waves/round-29/c2_matrix_count.py` (matrix `c2-matrix.json`, sha256 75c08f64…) as a detector for
the landed tool `scripts/base_path_audit.py` at lane commit 7697990cbca20291f3b0367b8ff4220e93b38b03, tool
blob sha256 e3264615…. The lane working tree is dirty from other seats; I did not use it.
## Commands (sandbox /fast/scratch/hyaku/kake-r29/w2/MutateToolVsCounter/)

    git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin clone && git -C clone checkout -q 7697990cbca20291f3b0367b8ff4220e93b38b03
    TMPDIR=$PWD/tmp python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-29/c2_matrix_count.py --root $PWD/clone --revision <commit>
    # exit 0 = every case passed, exit 1 = a case failed

Driver `mutants.py` (23 single-change mutants, one per behaviour-bearing point, each committed on branch
`mutant/<name>`, reverted byte-exactly afterwards); probes `probe.py`/`probe_cli.py`; raw data in
`mutant_results.json` and `probe*_results.json`. Baseline (pristine 7697990): exit 0, `C2 30/30 at
7697990…`, constant gates rejected (constant-clean 7/30, constant-failed-empty 0/30, constant-refuse
7/30). The baseline passes, so every kill below is a real kill and every survival a real blind spot.
## Mutant table (23 mutants: 11 killed, 12 survived)

| mutant | change (anchor line in base_path_audit.py) | verdict | failing case ids |
|---|---|---|---|
| A01-segment-boundary | base compared as string prefix of base-minus-slash (:432) | KILLED 29/30 exit 1 | D8-segment-prefix-not-string-prefix |
| A02-first-base-rule | last `<base href>` wins (:526) | KILLED 29/30 | K6-first-base-element-wins |
| A03-srcset-handling | srcset value used whole (:547) | KILLED 29/30 | D3-srcset-one-candidate-outside |
| A04-case-sensitive-path | base compare lower-cased (:432) | KILLED 29/30 | D9-case-sensitive-path |
| A05-cross-origin-ignore | same-site test removed (:581) | KILLED 29/30 | K3-external-and-nonhttp-ignored |
| A06-whitespace-strip | ASCII strip removed in `_clean_reference` (:383) | SURVIVED 30/30 | — |
| A07-confinement | traversal-component check removed (:286) | SURVIVED 30/30 | — |
| A08-verdict-mapping | verdict renamed (:721) | KILLED 16/30 | all 14 D cases |
| A09-reason-name | `REASON_OUTSIDE` renamed (:65) | KILLED 16/30 | all 14 D cases |
| A10-exit-code-policy | `EXIT_POLICY` 1→3 (:61) | KILLED 16/30 | all 14 D cases |
| A11-exit-code-input | `EXIT_INPUT` 2→3 (:62) | KILLED 22/30 | all 8 I cases |
| A12-exit-code-usage | `EXIT_USAGE` 64→2 (:63) | KILLED 29/30 | U1-missing-manifest-option |
| G01-base-trimmed-equality | path==base-minus-slash no longer inside (:434) | KILLED 29/30 | K4-base-without-final-slash-clean |
| G02-srcset-descriptor-validation | invalid srcset descriptor list no longer skips (:497) | SURVIVED 30/30 | — |
| G03-finding-id-index | finding occurrence index 0-based (:586) | SURVIVED 30/30 | — |
| G04-resolved-serialization | resolved URL always renders the port (:421) | SURVIVED 30/30 | — |
| G05-counts | pagesChecked/referencesChecked always 0 (:712) | SURVIVED 30/30 | — |
| G06-percent-2e-dot | lone `%2e` no longer a dot (:331) | SURVIVED 30/30 | — (equivalent) |
| G09-percent-2e-dot-pair | `%2e` handling dropped from both branches (:331/:334) | SURVIVED 30/30 | — |
| G07-template-contents | `<template>` contents scanned (:518) | SURVIVED 30/30 | — |
| G08-scheme-guard | non-http(s) scheme guard removed (:396) | SURVIVED 30/30 | — (equivalent) |
| G11-repeated-manifest | repeated `--manifest` no longer rejected (:120) | SURVIVED 30/30 | — |
| G12-help-option | `--help` removed from the parser (:159) | SURVIVED 30/30 | — |
## Survivors: live behaviour the counter cannot see (probed)

Each survivor was re-run on a fixture the matrix lacks; ten are live (output differs, so matrix gaps),
two are equivalent mutants (G06, G08).
- A06 — pristine `resolved` `https://o.github.io/x.css`, mutant `…/x.css ` (space kept).
- A07 — with `../index.html` present one level above the manifest directory, pristine exits 2
  `input_invalid`, mutant exits 1 `failed-policy` and reads the escaped file. Case I6 passes for the
  wrong reason: the case work dir's parent holds no `index.html`, so the mutant's traversal attempt
  hits "file missing" and yields the same `input_invalid`; the traversal rule is never exercised.
- G02 `srcset="/x.png 1x 2x"`: pristine clean, mutant reports `outside_base_path`. G07
  `<template><img src="/x.png">`: pristine clean, mutant reports the finding. G09 `%2e%2e/x`: pristine
  resolves to `/x` and reports it, mutant keeps the literal segment and reports clean.
- G03 / G04 / G05 change only uncompared fields: finding id `#1`→`#0`; `resolved` `…/x.css`→
  `…:443/x.css`; `pagesChecked`/`referencesChecked` → 0. G11 pristine exits 64 "may be given only
  once", mutant exits 2; G12 pristine exits 0 with help text, mutant exits 64.
- Root cause: `c2_matrix_count.py:62-72` (`project`) compares only the keys present in each expected
  finding (defect cases: attribute, element, reason, value; input cases: reason), so `id`, `page` and
  `resolved` are never compared, `pagesChecked`/`referencesChecked` are never compared, and `judge`
  returns "ok" for exit 64 at `c2_matrix_count.py:81` without parsing stdout. The matrix interface block
  declares findings as `{id, reason, page, element, attribute, value, resolved}`, so the counter is weaker
  than the interface it certifies.
## Verdict for the attacked item

C2 counter strength: **holds with a stated limit**. It kills 11 of 23 mutants and pins the
segment-boundary, first-base, srcset-candidate, case-sensitivity, cross-origin, verdict, reason and
exit-code rules to one case each. It does not cover the whitespace strip rule (A06), the
path-confinement rule (A07; case I6 passes for a different reason than the rule it names), srcset
descriptor validity, `%2e` dot handling, template exclusion, the finding `id`/`page`/`resolved` fields,
the two counters, or the CLI shape (`--help`, repeated `--manifest`).
Not verified: I did not run the committed selftest `scripts/base_path_selftest.py` against these survivors
(another seat's scope) and claim nothing about it; the lane's in-flight untracked
`scripts/fixtures/base-path/X0*` were not evaluated; no network fetch, no live probe of any web property;
wave-1 seat reports were not relied on. No package was installed or upgraded.
Restoration evidence: sandbox clone back at 7697990cbca20291f3b0367b8ff4220e93b38b03, tool sha256
e3264615… identical to the pre-mutation value, `git status --porcelain` in the clone empty. The only file
this seat wrote in the lane is this report.
