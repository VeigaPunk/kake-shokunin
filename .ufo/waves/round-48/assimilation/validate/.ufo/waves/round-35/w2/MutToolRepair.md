# Round 35 wave 2 — mutation test of the repaired C1 rules (KakeR35.MutToolRepair)

Attacks the C1 test strength: 14 single-rule mutants of `scripts/link_preview_audit.py` scored with the selftest, the round-34 matrix counter and the sealed C1 counter, to show whether the declared C1 contract (a)-(c) is pinned by any detector. Axes: operability. Milestone: r35-falsify.

## Setup (sandbox only)

- Clone at `/fast/scratch/hyaku/kake-r35/w2/KakeR35.MutToolRepair/clone` of the lane, checked out at `7deacc4629c1d05a34fb919d8095e99efc7b712f` (exit 0). Base tool SHA-256 `1a8b27243a00cede1b93f8d3e95201476c75b70a3bcaa59a7e51f2220e5f5ef4`, blob `cab236496f84b408f7e14b1df6b5e1919981a491`.
- Sandbox branch `mutprep` (`80d9e560e6191170e1f4bbbe7ae6fc43105848f5`) removes only the three files under `.ufo/waves/round-35/sealed/` from the tree, because the sealed counter refuses (exit 2) to measure a revision that already holds a key file. The key was read at revision `4c6be2bdec5630166c4013e53c226b1119ec63cc` via `--key-revision`; the tool bytes are the only mutated bytes. Driver `mutate.py` and results `results.json` sit beside the clone in the same sandbox directory.
- After each mutant the tool file was rewritten with the exact base bytes and asserted back to `1a8b2724…f5ef4`; the clone tree is back at the base blob. The lane file is unchanged (`sha256sum` = `1a8b2724…f5ef4`; `git diff -- scripts/link_preview_audit.py` empty). No tool installed (no pacman, no uv, no npm): system python3 and git only.

## Mutant table

Killed = the detector's declared threshold fails (selftest < 45/45, matrix < 28/28, sealed `met` false). Sealed shows `passed/24 (met)`; the declared target is >= 22 of 24.

| id | single-rule change (tool line) | selftest | matrix | sealed | killed by |
|---|---|---|---|---|---|
| BASE | pristine bytes | 45/45 | 28/28 | 24/24 (met) | baseline, all clean |
| M01 | suppression never closes, end tag does not pop (:106) | 42/45 | 28/28 | 23/24 (met) | selftest |
| M02 | only svg suppressed (:77) | 43/45 | 28/28 | 20/24 (no) | all three |
| M03 | self-closed svg opens suppression (:114) | 44/45 | 28/28 | 24/24 (met) | selftest only |
| M04 | og_url_multiple only for distinct values (:271) | 44/45 | 28/28 | 23/24 (met) | selftest |
| M05 | og_url_multiple counts empty og:url values (:271) | 44/45 | 28/28 | 23/24 (met) | selftest |
| M06 | policy findings suppressed on any input fault, old rule (:302) | 42/45 | 28/28 | 22/24 (met) | selftest |
| M07 | pagesChecked 0 on input faults (:302) | 41/45 | 28/28 | 24/24 (met) | selftest |
| M08 | path escape reported as page_unreadable (:206, :238) | 44/45 | 27/28 | 24/24 (met) | selftest, matrix |
| M09 | first og:url not compared when several og:url values exist (:278) | **45/45** | **28/28** | **23/24 (met)** | **none: survivor of all three** |
| M10 | page_unreadable findings duplicated (:240) | 39/45 | 27/28 | 21/24 (no) | all three |
| M11 | last canonical link wins (:134) | 43/45 | 28/28 | 24/24 (met) | selftest |
| M12 | any end tag closes every open suppressed element (:106) | 43/45 | 28/28 | 24/24 (met) | selftest |
| M13 | og_url_multiple needs three values (:271) | 43/45 | 28/28 | 21/24 (no) | all three |
| M14 | exact round-34 old rule for bullet (c), policy suppressed and pagesChecked 0 (:302) | 42/46 | 28/28 | 22/24 (met) | selftest |

Mutant commits (sandbox clone): M01 `1ccb67d18cda`, M02 `215a9672d07d`, M03 `40f8e06e5997`, M04 `208b76395ae7`, M05 `3584d115a6a5`, M06 `151cc4c5b4b1`, M07 `690719826fd2`, M08 `11df087ba6b4`, M09 `469f2d511896`, M10 `b6d601df2a52`, M11 `1604ea0a439d`, M12 `77b18ffa69de`, M13 `0d8b4f818d8d`, M14 `e5ddfc7966a9`.

## Finding 1 — one mutant survives all three detectors (M09)

M09 changes `if og_urls:` to `if len(og_urls) == 1:` at `scripts/link_preview_audit.py:278`, so the absolute-URL check and the canonical comparison are skipped whenever a page has two or more `og:url` elements. That violates contract bullet (a) ("The first non-empty og:url still gets the absolute check and the canonical comparison"). It passes the selftest 45/45, passes the round-34 matrix 28/28, and still meets the declared sealed target at 23 of 24 (case-24 fails; the target tolerates two failures). Only the sealed case set has power over it, and the declared threshold swallows the signal.

Killing fixture (validated in the sandbox, commit `08fa52c91364ba32b9de529c9bbe93803163ce3b`, directory `clone/scripts/fixtures/link-preview/og_url_multiple_first_value_checked/`): `index.html` has valid og:title/og:type/og:image, a first `og:url` of `/relative-only/` (not absolute), a second `og:url` equal to the page URL, and a canonical equal to the page URL. `expected.json`: exit 1, verdict failed-policy, pagesChecked 1, findings `og_url_multiple` then `og_url_not_absolute` (both property `og:url`), findingIds in that order. `manifest.json`: version 1, one page `index.html` at `https://cards.example/og-url-multiple-first-value-checked`. Observed: pristine tool 46/46 clean (exit 0); M09 tool 45/46 with the new case the only failure (exit 1), reason "findings mismatch: expected [('og_url_multiple','og:url'), ('og_url_not_absolute','og:url')], observed [('og_url_multiple','og:url')]". The same fixture also kills M13. Hashes: expected.json `c1539e8ea6c8f4aff6e67d4c325ebadddc3696efc5c4d95af40e2eb2be197f75`, index.html `21d83009175fb6612a5d29ddf1076d95967290fe31d4959de03cee96bc7c4a28`, manifest.json `97b36032f33fa799f4604d885f0e9ded1117f6e5b978090871b07f03a42573c9`. A coverage finding, not a contract change.

## Finding 2 — the declared C1 threshold does not discriminate the round-35 repairs

11 of the 14 mutants still satisfy the declared sealed target of >= 22 of 24 (only M02 at 20, M10 at 21 and M13 at 21 fall below). Most telling is M14: the exact round-34 old behaviour for bullet (c) scores 22/24 and is "met" by the sealed counter. The round-34 matrix counter flags none of the round-35 repairs (28/28 for 12 of 14 mutants). The power against M01-M07 and M11-M13 comes almost entirely from the selftest fixtures, not from the sealed counter or the matrix. The declared C1 evidence line ("24/24 at b1cbbc39") is therefore weaker than it reads: 22 of 24 would have been accepted for a tool reintroducing the pre-round-35 rule.

## Commands run (sandbox, exit codes)

- `python3 -B mutate.py` (driver, sandbox cwd, `TMPDIR` inside the sandbox): exit 0, 106 s wall.
- Per mutant, inside the clone: `python3 -B scripts/link_preview_selftest.py --tool scripts/link_preview_audit.py` (baseline exit 0, 45/45); `python3 -B .ufo/waves/round-34/c1_matrix_count.py --root <clone> --revision <mutant>` (baseline exit 0, 28/28, constantGatesAllRejected true; exit 1 for M08 and M10); `python3 -B .ufo/waves/round-35/sealed_count.py c1 --root <clone> --revision <mutant> --key-revision 4c6be2bdec5630166c4013e53c226b1119ec63cc` (baseline exit 0, 24/24, met true; exit 1 for M02, M10, M13). Fixture check: the same selftest command exits 0 on the pristine tool (46/46), exit 1 on the M09 tool (45/46), exit 1 on the M13 tool.

## Not verified

- I did not re-run the C1 claim on the lane tip through the L1's receipt path; the sealed counter ran against my sandbox commits only, with the key read at the reveal revision as instructed.
- I did not mutate the JSON manifest layer (duplicate keys, manifest size bound) or the CLI usage layer.
- The lane working tree also shows `M SKILL.md`, `M corpus/SOURCES.md` and other w2 files from other seats; I wrote none of them and touched none.

Report path: `.ufo/waves/round-35/w2/MutToolRepair.md`
