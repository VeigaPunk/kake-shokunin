# ReviewToolDocsConsistency — wave-2 falsify report

Attacks the C1 documentation at `7deacc4`: tool docstring (`scripts/link_preview_audit.py`), SKILL.md
round-35 registry row + exit-2 correction (`SKILL.md:1035-1054`), SCORECARD capability row
(`SCORECARD.md:196`), against the tool at `b1cbbc39`. The script is byte-identical at both revisions
(`git diff b1cbbc39 7deacc4 -- scripts/link_preview_audit.py` empty; sha256 `1a8b2724…`, equals the
receipt `toolSha256`). Sandbox: `/fast/scratch/hyaku/kake-r35/w2/ReviewToolDocsConsistency/`
(clone, `tool_at_b1cbbc39.py`, `probes/`).

## False statements (1)
- SKILL.md:1045 registry-row Verdict map: `` `64=could-not-evaluate` usage `` is FALSE. Exit 64 is
  usage, not could-not-evaluate. Evidence: docstring line 53 (`0 clean, 1 failed-policy, 2
  could-not-evaluate, 64 usage`), code `EXIT_USAGE = 64` (line 67), and probe: no-args run → exit 64,
  stdout 0 bytes, stderr only `link_preview_audit.py: the following arguments are required: --manifest`.
  The parenthetical "(message on stderr, no JSON on stdout)" is correct. Fix: `64=usage`.

## Confirmed true statements (all others probed)
- Docstring checked/not-checked lists: probes c1 (two non-empty og:url: one `og_url_multiple` finding,
  first URL only gets absolute+canonical checks; identical values still count; exit 1 failed-policy),
  c2 (meta/link inside open template/svg/math ignored; `<svg/>` opens nothing; clean exit 0), c6
  (relative canonical resolves equal → clean), c7 (scheme-only canonical difference →
  `og_url_not_canonical`), c3 (unreadable binary + directory page → exit 2 , `pagesChecked` 1,
  `page_unreadable` + policy findings together), c4 (manifest version 2 → exit 2, `pagesChecked` 0,
  only `input_invalid`), usage → exit 64. Exit codes 0/1/2/64 confirmed.
- SCORECARD:196 "keeps auditing readable pages when one page cannot be read (exit 2 with input and
  policy findings together)" — confirmed (c3).
- Registry-row Self-test column: 45 top-level fixture dirs at `b1cbbc39` (`git ls-tree -d`), `MIN_FIXTURES` 20 in code; selftest exit 2 when tool/fixture root absent or <20 dirs (code lines 157-178); compares exit, verdict, findings (reason,property) and pagesChecked/findingIds when present (lines 80-132). Receipt `selftest-link-preview-at-b1cbbc39.txt`: 45 caseNames, passed 45, exit=0.
- Registry-row pinned-values column: matrix sha256 `246a6a3b…` matches rerun; `c1-at-76fac3b.json` exists (28/28, `constantGatesAllRejected` true); reveal `4c6be2bd` matches receipt `keySource`.
- Exit-2 correction (SKILL.md:1047-1054): fixture `input_policy_suppressed_on_input` existed at base
  `16a6b8b8` with expected `{"exit":2,"verdict":"could-not-evaluate","findings":[{"reason":"page_unreadable"}]}`; now expects `pagesChecked` 1 plus the readable page's `og_required_missing` findings — "keeps its name but now expects the readable page's findings" TRUE. `pagesChecked` counts readable pages, manifest-level `input_invalid` audits nothing — both confirmed by probes.
- SCORECARD:196 evidence row: sealed counter rerun at `b1cbbc39` → 24/24, met true, exit 0
  (receipt `c1-at-b1cbbc39.json` matches); base 14/24 (`c1-at-16a6b8b8.json`, also `bd14096a` 14/24);
  lookup and constant controls 7/24 each (`control-v2-c1-lookup-dcef39b5.json`,
  `control-v2-c1-constant-clean.json`); round-34 matrix rerun 28/28 (receipt `c1r34-matrix-at-b1cbbc39.json`); selftest 45/45 (receipt above).

## Minor / verification gaps
- Registry-row verdict map parenthetical for exit 2 says `input_invalid` manifest-level only; per-page
  `input_invalid` (path escape) also yields exit 2 with `pagesChecked` 0 — under-specified, not false.
- Docstring omits the read bounds (16 MiB page / 4 MiB manifest → `page_unreadable`/`input_invalid`)
  and the `og:image:url` alias; neither contradicts a statement in the four places.
- Not verified: selftest exit-2 branches (tool/fixture absent, <20 dirs) were read from code, not run;
  base-revision 14/24 was read from receipts, not rerun.

## Commands (exit codes)
`python3 -B scripts/link_preview_selftest.py` → 0; `python3 -B .ufo/waves/round-34/c1_matrix_count.py --root . --revision b1cbbc39` → 0; `python3 -B .ufo/waves/round-35/sealed_count.py c1 --root . --revision b1cbbc39 --key-revision 4c6be2bd` → 0; probes c1/c2/c3/c4/c6/c7/usage → 1/0/2/2/0/1/64.
