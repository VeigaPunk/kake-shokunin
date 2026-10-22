# ReviewDocstringContract — C1 hunk: docstring vs behavior, exit codes, interface narrowing

Seat: KakeR28a3.ReviewDocstringContract (leaf reviewer). Axes: operability (docstring/contract
conformance of `scripts/citing_set.py`), freshness of the routed defect evidence. Read-only on the
lane; all execution in `/fast/scratch/hyaku/kake-r28a3/w1/ReviewDocstringContract/` (TMPDIR set
there). No installs or updates were performed (none needed). No LSP device is provisioned in this
session, so caller/definition checks were done by direct source reading plus execution, not by a
language server.

## What I attacked

The single hunk `git diff 22c1669c1fec83d1a0769de6b9ce686c75657e66 b5d423fc02057f67a6f3a255808313ce40d29069 -- scripts/citing_set.py` (60 insertions, 13 deletions), read whole at both pins
(`citing_set_new.py` 715 lines, `citing_set_base.py` 668 lines in scratch). Checks:

1. Every `input_invalid` reason code the repaired code can emit vs the docstring enumeration
   (module docstring lines 57–72 of the new file).
2. Exit codes remain exactly {0, 1, 2, 64}.
3. The round-27 interface in `.ufo/waves/round-27/contract.json` (gateInterface) is not narrowed.
4. No over-rejection of legitimate input.

## Commands and evidence

- `python3 -B -m py_compile citing_set_new.py` → exit 0. Gate sha256
  `28ba996524b444b2e1c23e3751f3fa662a9a44adbfcb6337a0d23fcebaf8f415` = blob at b5d423f; base copy
  sha256 `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228` = the r27 integration
  receipt's `codeSha256` for this file (both verified by hashing the extracted bytes).
- `git archive b5d423f scripts | tar -x -C tree && python3 -B tree/scripts/citing_set_selftest.py
  --root tree --tmpdir <scratch>/selftest` → **exit 0, 29/29 cases**, exact finding-id multisets
  (includes 01/18/20/21/28 positive cases → exit 0, so no legitimate fixture is over-rejected).
- `python3 -B probes.py` (my 14-probe harness, exit 0, ALL PASS; script + per-case output kept in
  scratch): usage→64; blank `--revision ""`→2 `revision_not_found`; `--revision "   "`→2;
  corpus dir removed→2 `corpus_directory_missing`; corpus holding only an empty subdir→2
  `corpus_empty`; population row `T999`→2 `population_id_unreachable`; row `" S001"`→2 same;
  FIFO as population document→2 `document_not_regular_file` (no hang, 20 s timeout not hit);
  JSON nested 60000→2 `document_not_json`, no traceback on stderr; repo-nested root with
  `--revision HEAD`→2 `root_not_repository_top_level`; same tree as its own repo top with
  `--revision HEAD`→**0 clean**; no-`--revision` working-tree mode→**0 clean**; empty ledger→1
  `failed` with `citingPairs:1`. Exit codes observed across probes+fixtures: exactly 0, 1, 2, 64.
- Base witness (same harness, base gate): `--revision ""` on a clean tree → **exit 0 clean**,
  silently measuring the working tree — the fail-open the `arguments.revision is not None` change
  closes; matches docstring line "a blank or unknown ``--revision``".
- Frozen real input unaffected: `.ufo/waves/round-27/frozen/population.json` has 32 rows,
  0 non-S-form (checked with a one-line python read).

## Findings

**F1 (Low, docstring-accuracy — the seat's exact check):** the hunk's new
`GitSource._require_top_level` adds an `InputInvalid("git_unavailable", …)` emit at
`scripts/citing_set.py:307` (new-file numbering, OSError branch around `git rev-parse
--show-toplevel`), but the docstring's `input_invalid` enumeration (lines 57–72) describes
"a blank or unknown ``--revision``" and "a ``--revision`` root that is not the top level of its
Git repository" and nothing for an unavailable git binary. Every other reason code this hunk
introduces is described: `document_not_regular_file` ("a FIFO or device is refused without
blocking"), `corpus_directory_missing`/`corpus_empty`/`not_a_directory` ("a ``corpus/knowledge``
surface that is absent, empty or not a directory"), `population_id_unreachable` ("unreachable
population id", plus a Population-section paragraph), blank/unknown `--revision`
(`revision_not_found`), `root_not_repository_top_level`. Mitigation: `git_unavailable` already
existed at base (`citing_set_base.py:282,295`) and was equally undocumented there, so this is a
pre-existing incompleteness the hunk extended rather than created; behavior stays
contract-conformant (input_invalid finding + exit 2). Suggested one-line fix: add "or git is
unavailable" after "unknown ``--revision``". Recommendation: accept the hunk; patch the sentence.

**F2 (Info, pre-existing, not introduced by the hunk, recorded for the same check):** four
reason codes emitted at both revisions are not itemized in the docstring paragraph:
`git_command_failed` (:338), `root_not_a_directory` (:694), `absolute_path_not_allowed` (:173),
`empty_path` (:170,:178) — the last two are at least adjacent to "missing" / "path that resolves
outside the root". No regression; noting so "every reason code described" is not overclaimed.

**F3 (Info, deliberate narrowing — judged acceptable, flagged for the L1):** the contract's
"inputs" line says only "population object rows list of {id}"; the hunk now rejects population
ids that are not `S`+digits (`population_id_unreachable`). This is a real restriction of
previously-accepted documents, declared in the docstring. It is not over-rejection of legitimate
input: the citation grammar (`_TOKEN_RE`/`_RANGE_RE`, `S[0-9]{3,}`) can never cite such a row, so
at base it silently shrank the measured denominator (fail-open); now it fails closed. Zero impact
on the frozen 32-row population and on 29/29 fixtures. Same class: blank `--revision` (base
returned exit-0-clean on the working tree — witnessed above), absent/empty corpus surface (base
returned `[]` → misleading findings or clean-with-empty-ledger), nested `--revision` root (base
enumerated nothing). Each is a routed-defect-class fail-open closed, not a legitimate-use removal;
all callers in the repo (counter `c1_interface_count.py`, `c2_count.py`, selftest runner,
`verification/consumer-current.json`) pass a real revision or omit the flag.

## Verdict on the three target checks

- Docstring vs behavior: **holds for every code the hunk introduces, except F1** (one Low gap).
- Exit codes: **hold** — only EXIT_CLEAN/FAILED/CANNOT_EVALUATE/USAGE constants exist; the only
  `SystemExit` is `EXIT_USAGE` (:619), `sys.exit(main())` at :715; empirically {0,1,2,64} only.
- Round-27 interface not narrowed: **holds**. CLI/parser untouched by the hunk; JSON keys
  `verdict|citingPairs|ledgerPairs|findings` and the five finding ids unchanged (29/29 fixture
  comparison is exit+sorted-finding-id exact); input_invalid gains only payload detail, allowed by
  `findings:[{id,row?,file?,...}]`; C1 claim ("absent or unreachable corpus surface must not
  return clean") is implemented exactly as documented and probed.

## Residual risk and not verified

- I did not run `c1_interface_count.py` or the C2 counter myself (L1/other seats own those
  measurements; my 14 probes and the 29-fixture selftest are independent but narrower).
- Git-mode edge cases (corpus/knowledge present as a git blob, submodule at the path, symlink in
  tree) were not probed here — sibling seats ReviewGitCorpusBlob/ReviewGitTopLevel own them; my
  git-mode coverage is own-top clean, nested-root reject, working-tree parity.
- `git_unavailable` path was verified by code reading only (no environment with git missing from
  PATH was constructed).
- Scratch clone `tree/` and probe artifacts remain under
  `/fast/scratch/hyaku/kake-r28a3/w1/ReviewDocstringContract/` for recheck; lane repo untouched
  except this report.
