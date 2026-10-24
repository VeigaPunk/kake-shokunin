# ReviewRedirectRegistry — `redirect-expectation-audit` registry row vs tool and r46 matrix

Target: `SKILL.md:1197` (row), `SKILL.md:1187-1202` (section + residual note),
`scripts/redirect_audit.py` (607 lines, blob sha256
`1e1dff18030c9028d833ab108bff140102343f4c5198c35984e7838e54bb748a`), matrix
`.ufo/waves/round-46/c46_matrix.py` (sha256 `7335b001f8a6860fef4d268eecdaac8710aa0224006586ea8435ab292b102164`),
receipts `.ufo/waves/round-47/verification/selftest-redirect-audit.txt` and
`.ufo/waves/round-46/verification/c1-after-ee43e66.json`, and the claim C1 counter
`.ufo/waves/round-47/c47_registry_count.py`.

Verdict: **C1's literal predicate holds** (row present, receipt committed, selftest and matrix
counts reproduce), but the row does **not** fully conform to the Gate standard's exit-map and
receipt-identity requirements. Five findings; F1 and F2 are actionable for round 47.

## Findings

### F1 (MEDIUM) — the declared exit `2` does not mean `could-not-evaluate (input)` on the `--json` write-failure path

Row (`SKILL.md:1197`) declares `0=clean`; `1=failed-policy`; `2=could-not-evaluate` (input);
`64=usage`. The tool computes the audit and then, if the `--json` target cannot be opened,
returns `EXIT_INPUT` after discarding the computed verdict and printing no report
(`scripts/redirect_audit.py:592-602`: `exit_code, report = run_audit(...)`; on `OSError` at
`:601`, `return EXIT_INPUT` at `:602`).

Measured (cwd `/fast/scratch/hyaku/kake-r47/ReviewRedirectRegistry/run`, `python3 -B <lane>/scripts/redirect_audit.py ...`):

| manifest | args | observed exit | stdout |
|---|---|---|---|
| one-finding manifest | `--manifest dirty.json` | **1** | report with one finding |
| one-finding manifest | `--manifest dirty.json --json /nonexistent-dir-r47/x.json` | **2** | empty |
| clean manifest | `--manifest clean.json --json /nonexistent-dir-r47/x.json` | **2** | empty |

Consequences: a consumer mapping `2` to "fix the input manifest" misreads a policy failure; a
clean audit is reported as `could-not-evaluate`; the evaluated result is silently lost. The
verdict map is false for a reachable path. Repair direction (not a patch): return the computed
exit code and emit the report to stdout when the file write fails, or declare the output-error
path explicitly in the row.

### F2 (MEDIUM) — the row's filed counts are not identity-bound (`corpus/QUALITY.md:1071`)

`QUALITY.md:1071`: "Any filed count or verdict against a receipt cites that receipt's path +
sha256; a receipt citation without sha256 violates this criterion."

- Self-test cell files `23/23` against `.ufo/waves/round-47/verification/selftest-redirect-audit.txt`
  with **no sha256**. Committed receipt sha256:
  `0760b0310b166e45585794fb889431e2d5577af76e70cebfbe85d213428ef056`
  (`git cat-file blob HEAD:<path> | sha256sum`). The lane's own round-47 C1 row does cite it
  (`SCORECARD.md:3975`), so the registry row is the outlier.
- Pinned-proof cell files `11/11 witnesses caught, 0 clean false positives, 3/3 controls rejected,
  wall <120 s` against **no receipt at all**. The matching committed receipt is
  `.ufo/waves/round-46/verification/c1-after-ee43e66.json`, sha256
  `8c8d9521b3ddc45f9719ddb13ffdb1468e6662c94c59b246d5dcf2b75a7c90c0`, revision
  `ee43e66367bf23e386ff29029b9ea60515efd9d1`.
- The cell also gives `--revision <rev>` and `--stage before|after` with no measured revision or
  stage label. Measured: `--stage before` at `ee43e66` returns **exit 1**,
  `stage=before ... MATRIX_BEFORE_FAIL` (that stage is defined to fail once the tool exists);
  the row's numbers are the **after** stage only.

The counts themselves are true. Measured with the row's command (matrix stdout first line parsed):

| revision | stage | witnesses | clean FP | controls accepted (=rejected) | wall | verdict |
|---|---|---|---|---|---|---|
| `ee43e66367bf…` | after | 11/11 | 0 | 0 (3/3 rejected) | 1.183 s | `MATRIX_AFTER_PASS`, exit 0 |
| `766f461` (tip) | after | 11/11 | 0 | 0 (3/3 rejected) | 1.159 s | `MATRIX_AFTER_PASS`, exit 0 |
| `ee43e66367bf…` | before | 11/11 | 0 | 0 | 1.195 s | `MATRIX_BEFORE_FAIL`, exit 1 |

Tool sha in both after runs: `1e1dff…`, equal to the receipt and the HEAD blob. Fixtures are
frozen in practice: 19/19 files tracked, and the only post-`ee43e66` change under
`.ufo/waves/round-46/` is commit `861113e` adding the after receipts, so reproduction is stable.
The defect is citation identity, not the numbers.

### F3 (LOW) — `--selftest` short-circuits argv validation, so `64=usage` is not universal

`main` returns `selftest()` whenever `--selftest` appears anywhere in `argv`
(`scripts/redirect_audit.py:584`), before `parse_cli`. The guard intended to reject the
combination (`:76-77`, `--selftest takes no --manifest`) is unreachable.

Measured: `--selftest --manifest /…/nope.json` → **exit 0**, full `23/23` PASS output;
`--selftest --bogus` → **exit 0**. A malformed self-test invocation reads as green, and the
row's `64=usage` claim does not hold for any argv containing `--selftest`.

### F4 (LOW) — the tool advertises a dead `--root`; the row's entry command omits it

The usage string advertises `--root PATH` (`:66`) and `:71` declares it, but `args.root` is never
read (only `args.manifest` `:592`, `args.json` `:594`/`:598`). Measured:
`--manifest clean.json --root /nonexistent-dir-r47` → exit 0 clean, identical to the run without
`--root`; an absolute manifest is read cwd-relative regardless of `--root`. The usage string also
omits `--selftest`, the mode the row's self-test cell cites. The row does not claim `--root`, so
the row makes no false statement; the tool's advertised CLI is the incoherent surface, and a
caller following `--help`/usage gets a silent no-op.

### F5 (LOW) — the manifest field list omits the mandatory `version: 1`

Row: "manifest v1: `rules`, `resources`, `checks`; `resourcePrecedence` and `defaultStatus` host
fields". `load_manifest` additionally requires `manifest["version"] == 1` (`:216`) and treats
`resources` as optional (`:221-222`; required keys `:218-220`). Measured: a manifest with every field the row names but no
`version` → **exit 2**, `manifest must be a version-1 object`. The contract
`corpus/knowledge/redirect-rewrite-rules.md:54-57` defers the v1 schema to the tool docstring,
which also does not enumerate `version`. A manifest authored from the row fails closed on the
first run.

## Verified conformant

- **Eight fields present** (`SKILL.md:1195-1197`): name, kind, entry command, verdict map,
  self-test command + spelling, pinned values, write scope, owner.
- **Owner** `kake` matches every other registry row (`SKILL.md:212`, `:387`, `:411`, `:482`,
  `:537`, `:555`, `:568`, `:587`, `:616`, `:1045`, `:1066`, `:1092`, `:1127`).
- **Kind offline/no-network** holds: imports are `argparse`, `json`, `sys`, `urllib.parse`
  (`:34-39`); selftest-local `tempfile`/`os`/`subprocess`. No network module.
- **Entry command and the core exit map** hold for the normal paths: no args / unknown flag /
  missing value / duplicate `--manifest` → 64; unreadable, malformed, missing-`version`, or
  bad-check-shape manifest → 2; clean → 0; one finding → 1 (all measured).
- **Self-test spelling and tally**: `--selftest` → `23/23`, exit 0, PASS list byte-identical to
  the receipt. Receipt committed in `846138c` (2026-10-24 07:05:18Z) after its recorded
  `run_at_utc` 06:46:10Z; it names the command, tool path, tool sha256 (`1e1dff…`, equal to the
  HEAD blob) and `exit=0`.
- **Write scope** for the audit path: only the `--json` target is written (measured: only
  `out.json` created; `--json -` goes to stdout); the selftest leaves no files under a scratch
  `TMPDIR`; `-B` plus no local imports means no `__pycache__`.
- **Pinned sources exist**: S050 (`corpus/SOURCES.md:58`) and S135 (`:143`), both tier A; the
  contract `corpus/knowledge/redirect-rewrite-rules.md` is committed.
- **C1 claim**: `c47_registry_count.py` at base `cd42e3c…` → `0/2 rows, 0/2 receipts`,
  `C1_NOT_MET`, exit 1; at `714e707…` and at tip `766f461` → `2/2, 2/2`, `C1_MET`, exit 0.
  Receipt shas match `SCORECARD.md:3975` (`c98ff62…`, `cc71cc9…`). Only one table line at HEAD
  names `scripts/redirect_audit.py` (`SKILL.md:1197`), so the counter's name-only row predicate
  is not satisfied by an unrelated line.
- **Disclosure**: the semantic-oracle gaps in the matrix (fixtures mirror `_witnesses()`, W12's
  status-200 expectation, basename/doctored-index control, surviving mutants) are disclosed at
  `SKILL.md:1202` and not re-raised here as a row defect.

## Residual risk / verification gaps

- **Gate standard source**: the canonical clause lives in fleet `PROTOCOL.md`, outside this
  seat's lane bounds. The field list used here comes from in-lane restatements
  (`corpus/lessons/round-22-verifier-spotcheck.md:31`;
  `.ufo/waves/round-35/w2/ReviewSkillRegistryRow35.md:8-10`) plus the lane's standing
  `QUALITY.md:1071` criterion.
- **C1's counter is presence-only**: `c47_registry_count.py:113-126` accepts any `|` line
  containing the tool path and any receipt containing that path, a tally, `exit=0` and some
  64-hex string. A row with no verdict map, or a receipt citing another file's digest, would
  still pass. The row happens to be complete; the predicate is weaker than "registered".
- **Matrix proof is not revision-bound**: `index.json` is read from the worktree
  (`c46_matrix.py:122`) and the counter sha is worktree-computed (`:212`); disclosed at
  `SKILL.md:1202` and in the untracked residual report. I re-ran only the canonical path; I did
  not reproduce the basename-matcher / doctored-index counterexamples (that needs a sandbox
  clone and was not required to verify this row's counts).
- **Not run**: `--stage before` at the base revision (base receipt `c1-before-7cdbaefd.json`
  read only; the tool is absent there by design); hostile manifests beyond the input-shape
  cases above; `--json` failure modes other than a nonexistent parent directory.
- **Tally composition**: `23/23` includes one non-independent case — the `always_clean` branch
  (`:459`, `:501-506`) re-evaluates the committed semantics over the same flag cases as the flag
  loop and cannot fail independently (differential mutants = 5, not 6). The tally is an honest
  count of PASS lines, so the row's `23/23` is not false, but one case adds no independent
  failure mode.

## Tools

None installed or updated; all evidence is `python3` stdlib, read-only `git`, and committed lane
artifacts. No tracked lane file was edited. `git status --porcelain` after the runs shows no
modification attributable to this seat; the sole tracked modification
(` M .ufo/waves/round-47/w1/swarm-registry.json`) predates it, and the untracked entries are the
wave-1 seat reports (including this one) plus the pre-existing `.ufo/waves/round-46/residual/`.
Only writes: this report and scratch under `/fast/scratch/hyaku/kake-r47/ReviewRedirectRegistry/`.
