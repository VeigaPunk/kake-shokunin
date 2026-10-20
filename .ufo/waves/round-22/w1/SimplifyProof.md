# SimplifyProof — r22 C1 evidence set (minimal, non-redundant)

Seat: `KakeR22.SimplifyProof` (simplifier, leaf). Date 2026-10-20.
Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Base observed: `7c61c8cc791bde36dd5e3688bdfea2678d90146c` (`git rev-parse HEAD`).
Contract: `.ufo/waves/round-22/contract.json`, sha256
`f9a65a8ade6acb77f013104c60dcd2cfc7b63a0f65e855e710036f26ab746fe4` (observed).
Scope: read-only. No code edits, no commits, no runs of tools that do not exist yet,
no installs. This report recommends the evidence set only; it does not implement it.

## Axes named

- **Operability** — can a reader re-derive C1's before and after from committed artifacts,
  with the exact command in the claim, at closure time?
- **Evidence integrity** — does the set show the negative controls, the honest baseline,
  and the digest pinning instead of hiding them behind an `accepted: 32` summary?

Both axes point the same way: keep one authority per fact, and make every fail-closed
path visible as its own receipt.

## Bottom line

Minimal C1 set = **one oracle directory plus four receipts**:

| # | Artifact | Produced by | Unique claim | Drop instead |
|---|---|---|---|---|
| E1 | `.ufo/waves/round-22/cases.json` + `fixtures/**` | Matrix | independent expected verdict per case + digests of every committed input | — |
| E2 | `.ufo/waves/round-22/measure-before.json` | L1 (receipt of `measure.py`) | base `7c61c8c` has no validator; honest `accepted 0 / 32`, instrument pinned | a "baseline matrix" run, which cannot exist |
| E3 | `.ufo/waves/round-22/measure-after.json` | L1 (receipt of the contract count command) | all 32 cases match exit **and** finding id at one integrated revision; read-only | standalone `matrix-after.json`, `measurement-summary.json`, `gate-digest.json` |
| E4 | `.ufo/waves/round-22/selftest.json` | L1 (receipt of `--selftest`) | validator exit map incl. `64`, isolated temp fixtures, no live-tree write | duplicating the 32 matrix cases in selftest |
| E5 | `.ufo/waves/round-22/controls.json` | L1 (receipt of two harness mutations) | the pin check and the comparison both fail closed (can fail) | — |

The contract's `count` command is exactly E3's command. E1 is the frozen oracle;
E2/E3/E4/E5 are receipts in the r21 `{argv, exit, stdout, stderr}` shape, with `cwd`
and a caller-computed blob map added. Do not add a fifth receipt type.

## What the frozen contract forces

From `contract.json` (observed):

- Claim C1: before = no runnable lane validator, `0/32` accepted; after = every frozen
  matrix case classified with expected exit **and finding id**, conflicts/mismatches
  rejected, clean positive controls proven.
- `count`: `python3 .ufo/waves/round-22/measure.py --root . --revision <master-tip>`.
- Exit map: `0` clean, `1` failed policy, `2` could-not-evaluate input/unsupported shape,
  `64` could-not-evaluate usage.
- Vocabulary (exactly 10): `canonical_missing`, `canonical_multiple`,
  `canonical_outside_head`, `canonical_href_missing`, `canonical_url_invalid`,
  `canonical_fragment`, `canonical_mismatch`, `base_url_invalid`, `input_invalid`,
  `html_unsupported`.
- `limits`: explicit-head serialized static HTML only; policy comparison, not search-engine
  selection, JS, HTTP, redirects, network freshness, or publishing readiness.

## Contract-derived control classes (32 cases)

This table is my contract-derived reading, **not** the oracle of record. Matrix must freeze
the literals independently before the validator lands; L1 arbitrates a disagreement against
the contract text, never against validator output.

| Class | Cases | Expected exit | Expected finding id set |
|---|---|---|---|
| clean positive controls | `absolute_match`, `relative_same_dir`, `relative_parent`, `root_relative`, `scheme_relative`, `first_base`, `second_base_ignored`, `rel_token_list`, `rel_uppercase`, `attr_uppercase`, `entity_href`, `query_preserved` | 0 | `[]` (verdict `clean`) |
| missing canonical | `missing_link`, `comment_decoy`, `script_decoy`, `template_decoy` | 1 | `canonical_missing` |
| multiple canonical | `duplicate_same`, `duplicate_different` | 1 | `canonical_multiple` |
| canonical outside head | `body_link` | 1 | `canonical_outside_head` |
| href absent/empty | `href_absent`, `href_empty` | 1 | `canonical_href_missing` |
| unusable URL | `invalid_url`, `javascript_url`, `data_url` | 1 | `canonical_url_invalid` |
| fragment | `fragment_url` | 1 | `canonical_fragment` |
| mismatch | `wrong_host`, `wrong_path`, `wrong_query` | 1 | `canonical_mismatch` |
| invalid base | `base_invalid` | 1 | `base_url_invalid` |
| unsupported document shape | `missing_head` | 2 | `html_unsupported` |
| input rejected | `manifest_traversal`, `symlink_html` | 2 | `input_invalid` |

Totals: **12 clean, 17 policy failures, 3 could-not-evaluate** = 32. This mapping exercises
all 10 finding ids; if Matrix freezes `missing_head` differently, `html_unsupported` has no
other matrix case and becomes dead vocabulary — call that out in the report rather than
leaving an unreachable id unlabelled.

Two decisions need to be frozen explicitly because both readings are defensible:

1. `missing_head` — `html_unsupported` / exit 2 is the better fit for the `limits` line
   "Explicit-head serialized static HTML only"; `canonical_missing` / exit 1 is the better
   fit for "no canonical link present". Pick one, encode it, and do not let the validator
   choose dynamically.
2. `href_empty` — treat an empty `href` as `canonical_href_missing` (failed policy). An empty
   relative reference resolves to the document URL under RFC 3986; if treated as resolution,
   the case silently becomes a clean positive control, which is not what the case name means.

Cross-check available at write time (not authority): the live, still-untracked
`corpus/knowledge/static-canonical-preflight.md` tabs exit `2` as
`input_invalid`/`html_unsupported` and calls the explicit-head unsupported-shape rejection part
of the interface. That supports the `missing_head` → `html_unsupported` recommendation. It does
not pin individual case mappings; `cases.json` must.

## E1 — `cases.json` + `fixtures/**` (the single oracle)

This fills the role r21's `initial.json` filled for the population oracle, extended with
per-case expected exit/id/page literals and digests of every committed input.

Minimum schema (recommendation):

```json
{
  "version": 1,
  "contractSha256": "f9a65a8ade6acb77f013104c60dcd2cfc7b63a0f65e855e710036f26ab746fe4",
  "caseCount": 32,
  "inputs": {
    "fixtures/01/manifest.json": "<sha256>",
    "fixtures/01/a.html": "<sha256>"
  },
  "cases": [
    {
      "name": "absolute_match",
      "manifest": "fixtures/01/manifest.json",
      "expectedExit": 0,
      "expectedFindingIds": [],
      "expectedPageUrls": []
    },
    {
      "name": "duplicate_same",
      "manifest": "fixtures/09/manifest.json",
      "expectedExit": 1,
      "expectedFindingIds": ["canonical_multiple"],
      "expectedPageUrls": ["https://example.test/project/a.html"]
    }
  ],
  "runtimeInputs": [
    {
      "case": "symlink_html",
      "kind": "symlink",
      "target": "fixtures/<n>/a.html",
      "targetSha256": "<sha256>"
    }
  ]
}
```

Rules that make E1 an oracle instead of a second implementation:

- Expected values are **literals authored from the contract**, never captured from a validator
  run. If they are captured, E3 proves only that the validator agrees with itself.
- Do not store a second `positive` boolean. A clean control is exactly
  `expectedExit == 0 and expectedFindingIds == []`; a stored flag is a second copy of the same
  fact and can disagree after an edit. `caseCount` is likewise an assertion to check against
  `len(cases) == 32`, not an authority.
- `expectedFindingIds` is an **exact sorted set**, not "contains". A validator that emits the
  right id plus an extra finding must fail; exit `0` must imply `[]`.
- `expectedPageUrls` pins `findings[].page`; id-only comparison would accept a finding attached
  to the wrong page.
- `inputs` covers **every** committed file the validator may read: each manifest JSON and each
  page file. Set equality is required between `inputs` keys and materialized fixture files;
  an unlisted file or a missing listed file is a pin failure.
- The case-name set must equal the contract's `matrixCases` exactly (32, no extras). A one-line
  population check reading the frozen `contract.json` and comparing the digest to
  `contractSha256` is enough; report `population: {expected, found, missing, extra}` in E3.
- Fixture directories should be neutral (`01`, `02`, …); semantic names such as
  `wrong_host.html` leak the oracle to a validator that inspects its own argv.
- `symlink_html` and `manifest_traversal` must be constructed so that following the link or
  `..` path would produce a **clean** verdict. Only rejection can produce exit 2, so the case
  distinguishes enforcement from a no-op. The symlink is runtime-only (do not commit a link);
  `runtimeInputs` names its target and target digest, and matrix records the generated link.
- `cases.json` cannot pin itself. Its own bytes are pinned by the measured commit and by the
  `blobs` map in E3, not by an `inputs` entry.

## E2 — `measure-before.json` (honest absence, the first negative control)

Receipt of the baseline form (record the exact argv Measure implements; `--cases-root` takes
the candidate lane root as specified):

```bash
cd /home/vgpnk/Projects/shokunin/kake-shokunin
python3 .ufo/waves/round-22/measure.py \
  --root . \
  --revision 7c61c8cc791bde36dd5e3688bdfea2678d90146c \
  --cases-root .
```

Expected content (contract-derived, `[INFERENCE]` until run):

```json
{
  "root": ".",
  "revision": "7c61c8cc791bde36dd5e3688bdfea2678d90146c",
  "validator": {"present": false, "reason": "not-in-revision"},
  "available": false,
  "accepted": 0,
  "total": 32,
  "population": {"expected": 32, "found": 32, "missing": [], "extra": []},
  "instrument": {"casesSha256": "<sha256>", "inputs": {"...": "<sha256>"}},
  "blobs": {"scripts/canonical_audit.py": null},
  "exit": 0
}
```

Why this is not redundant with E3:

- It is the only evidence that the base revision genuinely lacks the validator. `available:false`
  alone could mean a broken measure. The receipt must name the reason as `not-in-revision`, and
  the independent cross-check is `git cat-file -e 7c61c8c…:scripts/canonical_audit.py`, which
  exits 128 (verified now: `fatal: path 'scripts/canonical_audit.py' does not exist in 'HEAD'`).
- **Exit 0 here is not "clean".** It is the spec's explicit baseline-unavailable path. State that
  next to the receipt; never roll it into a green tally. The before claim is `0/32 accepted`, not
  `clean`.
- It pins the **instrument** (cases root) and requires the same `casesSha256` and `inputs` map as
  E3. Before/after measured against different oracles would be an invalid comparison.
- It proves pin verification still runs when the validator is absent: run it on a tampered
  `--cases-root` copy (E5) and it must exit 2 rather than fall through to `available:false`.

Record `casesRevision` (the code+oracle commit) and `treeClean: true` in the receipt header.
`--cases-root .` is only a frozen instrument if the working tree equals that commit at run time;
otherwise a dirty tree silently changes the oracle.

## E3 — `measure-after.json` (the count command, all 32 rows visible)

Receipt of the contract command, against the **code+oracle commit** (not a mid-wave tree):

```bash
cd /home/vgpnk/Projects/shokunin/kake-shokunin
python3 .ufo/waves/round-22/measure.py \
  --root . \
  --revision "$(git rev-parse HEAD)"
```

Minimum per-case row (recommendation):

```json
{
  "name": "wrong_query",
  "expected": {"exit": 1, "ids": ["canonical_mismatch"], "pages": ["https://example.test/project/a.html"]},
  "observed": {"exit": 1, "verdict": "failed", "ids": ["canonical_mismatch"], "pages": ["https://example.test/project/a.html"]},
  "match": true
}
```

Required properties of the receipt:

- `accepted` is the count of rows where **exit, exact id set, and page set all match**. Not exit
  alone, not "expected id is present".
- All 32 rows are in stdout. A summary of `accepted: 32, total: 32` without rows is not evidence;
  it can hide a case that passed for the wrong reason.
- Top-level schema checks: `verdict` matches the exit class (`0→clean`, `1→failed`,
  `2→could-not-evaluate`), `pagesChecked` is an integer, and every finding has `id` and `page`.
  `pagesChecked` counts pages that reached policy comparison: `1` for clean and
  policy-failing pages, `0` for `input_invalid` (no page was read), and `1` for
  `html_unsupported` (the page was read, then rejected as a shape). Freeze that rule in
  `matrix.py`.
- `observed ids ⊆ contract findingIds`; an unknown id is a failure even if it happens to match
  the oracle's typo.
- `blobs` maps every measured blob to sha256: `scripts/canonical_audit.py`, `measure.py`,
  `matrix.py`, `cases.json`, `contract.json`, every fixture, and the runtime symlink target.
  These hashes are of the bytes materialized from `git cat-file <revision>:<path>`, not mtimes,
  sizes, or working-tree bytes.
- `pins`: `verifiedBefore: true`, `verifiedAfter: true`, `inputsUnchanged: true`.
- `readonly`: `statusBefore` and `statusAfter` around the subprocess plus
  `workingTreeMatchesRevision: true` for every code/oracle blob. The normal path must not write
  the live tree; the validator only reads the materialized files.
- Run the matrix twice inside the same receipt (`runs: 2`) and require byte-identical parsed
  results / identical stdout digest. A single run does not prove deterministic classification;
  order and hash-seed drift is a real failure mode for a 32-case loop.
- `population` as in E2, and `instrument.casesSha256` equal to E2's value.
- The receipt's `revision` is a full 40-hex SHA (`rev-parse --verify <ish>^{commit}`), never a
  tag or `<master-tip>` placeholder. The final master tip contains the same code/oracle blobs, so
  the evaluator can re-run the count command there and get the same code hashes even though the
  evidence commit itself is later.

## E4 — `selftest.json` (capability, exit map, isolation)

Receipt of:

```bash
cd /home/vgpnk/Projects/shokunin/kake-shokunin
python3 scripts/canonical_audit.py --selftest
```

The gate standard (PROTOCOL.md §Gate standard, read in full) requires a self-invocation over
isolated fixtures asserting both exit code and a stable expected finding id, with expected values
committed and independent of recomputation. Concretely for C1:

- Cover the outer interface the matrix does not exercise: a clean multi-page manifest
  (`0`, `[]`), one policy failure per finding **class** (`1`, named id), an unsupported/input
  rejection (`2`), and usage errors (`64`: unknown flag, missing `--manifest` value).
  Eight to twelve controls are enough; do not duplicate all 32 matrix cases.
- Expected literals live in the validator source (committed), not read from `cases.json`. A
  selftest that imports the matrix oracle is not independent.
- Fixtures are built with `tempfile.mkdtemp`, cleaned in `finally`. Assert the temp root's
  `realpath` is **outside** the lane root; r21 Confinement F5 showed `TMPDIR` can place a
  "temp" tree inside the live lane. Record `tmpOutsideLane: true` and `tmpRemoved: true` in the
  receipt.
- No shell: subprocess children use argv arrays, no `shell=True`, no network. The selftest
  receipt records the child argv shape, not just "PASS".
- Print deterministic `PASS/FAIL <case> expect=<exit,id> got=<exit,id>` lines and a final
  `SELFTEST: N/N` tally; exit 0 iff all pass. The receipt stores the full stdout so expected and
  observed are both visible; a bare `PASS 7/7` would hide a changed expectation.

This is the only evidence for exit `64` (the matrix never invokes a bad CLI) and for the
validator's isolated-fixture behavior. Keep it, but keep it narrow.

## E5 — `controls.json` (prove the evidence machinery can fail)

One receipt, two runs, both against temp copies. These are controls of the **harness**, not a
second measurement of the validator.

1. **Pin tamper.** Copy `cases.json`, `matrix.py`, and `fixtures/` to a temp case root; flip one
   byte in a pinned HTML page (not the manifest, so the control isolates pin verification from
   JSON parsing; or delete that page). Run E2's command with `--cases-root <temp-case-root>` at
   the base revision. Expected: exit `2`, error/status `snapshot_tampered`, **no** `accepted`
   tally, no matrix invocation. This proves the digest check runs before the missing-validator
   short-circuit; without it, a baseline "0/32" can be produced from an unpinned oracle.
2. **Oracle mutation.** Copy the whole code+oracle tree to a neutral temp lane root (validator
   bytes copied and hash-checked equal to E3's). Change one `expectedFindingIds` or
   `expectedExit` in the copied `cases.json` only. Run `matrix.py --root <temp-lane>`. Expected:
   exit `1`, exactly one mismatch row naming the mutated case with expected vs observed. This
   proves the comparison is not a rubber stamp and that the validator does not depend on the
   lane-relative paths or case directory names.

Schema per control: `{name, argv, exit, expected: {exit, status/mismatch}, observed, pass}`.
For the pin tamper, record the original pinned digest and the tampered digest; for the mutation,
record the case name and both tuples. The temp paths are run details, not evidence pointers; the
committed receipt is the pointer.

Do not hide a failed control by editing the control's expectation after the fact. If either
control does not produce its declared outcome, the C1 evidence set is invalid, not green.

## Fail-closed order inside `measure.py` (recommended)

1. Parse args; unknown/missing values → `64` before any filesystem access.
2. Resolve `<revision>` with `rev-parse --verify <ish>^{commit}`; failure → `2`.
3. Materialize validator, matrix, cases, fixtures from git (or `--cases-root`) into a fresh temp
   dir; no writes outside it.
4. Verify the instrument: `contract.json` digest, 32-name population, `cases.json.inputs` against
   every materialized fixture, and the runtime symlink target. Any mismatch → `2`
   (`snapshot_tampered`), **before** checking validator availability or running matrix.
5. If the validator blob is absent: emit `available:false, accepted:0, total:32` and exit `0`
   (baseline only). If the script is present but unreadable, that is an error (`2`), not absence.
6. Run matrix over all 32; compare exit + exact id set + page set + top-level schema.
7. Re-verify every input digest after the run; require unchanged. Emit the JSON receipt.
8. Exit `0` iff `accepted == total == 32`; otherwise exit nonzero (`1` policy/measurement
   mismatch, `2` could-not-evaluate). An undeclared exception is `2`, never `0`.

The ordering of steps 4 and 5 is the hidden-negative-control boundary. A cheap implementation
that checks "is the validator present?" first will make E5's pin tamper unreachable at the base
and will hide a tampered oracle.

## Digest-pinning rules

- Algorithm: SHA-256 over exact bytes read from git, no normalization, no line-ending or
  metadata involvement.
- Pin set: `contract.json`, `scripts/canonical_audit.py`, `measure.py`, `matrix.py`,
  `cases.json`, every committed fixture file, and each runtime-generated symlink target.
- Two independent computations: `measure.py`'s own `blobs` map (inside E3 stdout) and the
  caller's `sha256sum`/`git cat-file` values in the receipt header. They must agree; a tool that
  hashes itself is not the only witness.
- `cases.json.inputs` pins the snapshot inputs before comparison; the measured commit pins
  `cases.json` itself. Do not add a separate `gate-digest.json` for one file; the commit plus
  the `blobs` map covers it.
- `contract.json`'s digest goes in E1/E2/E3 and the round report. It is the vocabulary pin
  (`expectedFindingId` must be one of the 10 contract ids).
- A pin that is printed but never compared is not a pin. E5 is the proof that a mismatch fails
  closed; without E5, the pin is a fingerprint printer.

## Commit sequencing (two commits, pathspec-limited)

1. Commit **A** = `scripts/canonical_audit.py`, `.ufo/waves/round-22/{matrix.py,cases.json,fixtures/**,measure.py}`.
   Verify `git status --porcelain` is empty and `HEAD` is A before measuring.
2. Run E2, E3, E4, E5 against A; write the four receipts.
3. Commit **B** = the four receipts, `.ufo/waves/round-22/w1/*.md` (including this report), and
   the round report. Never `git add -A`; use explicit pathspecs.
4. The count command is re-runnable at B because B has the same code/oracle blobs as A; E3's
   `revision` names A, the revision it actually measured. Recording B in E3 would be false: B
   did not exist when the receipt was produced.

If L1 tries to use a single commit, the receipt either cites a revision that did not contain the
receipt (impossible) or measures a dirty tree (not comparable). Two commits is the minimal
honest sequence.

## Redundancy ledger — do not copy these r21 habits

Observed r21 artifacts and why the r22 set drops them:

- `measurement-summary.json` — a derived convenience; every number is re-derivable from the two
  receipts. A summary that disagrees with a receipt creates a second authority. Put a derived
  table in the round report, not a new JSON file.
- `gate-digest.json` — one script's digest. E3's `blobs` map plus the commit pin covers all
  measured blobs; a separate file adds a second place to update.
- A standalone matrix output file — E3 embeds every per-case row; a separate file duplicates
  the same evidence and can drift.
- A working-tree after run — r21 CountingRecipes showed mid-wave counts moving 4→8→13→21; only
  a revision-bound run names what it measured. `--root .` is fine only when the tree equals the
  cited commit (record `treeClean: true`).
- A prose per-case expected table as authority — the table above is advisory; `cases.json` is
  the oracle. Duplicating literals in markdown drifts.
- A second "baseline matrix" run — the validator does not exist at base; `available:false` is
  the honest zero. Do not synthesize a matrix run.
- Any `/tmp` or clone path as a pointer — receipts are committed under `.ufo/waves/round-22/`;
  `/tmp/kake-r22-*` paths are run details and do not resolve at closure.

## What C1 does and does not prove

Does prove: the committed validator, at a named revision, returns the frozen expected exit and
finding id for all 32 matrix cases; the 12 clean controls produce zero findings; missing,
multiple, outside-head, malformed, fragment, mismatch, invalid-base, unsupported, and unsafe-path
cases fail closed; the before revision has no validator and scores 0/32; pins are enforced and
the comparison can fail.

Does not prove: WHATWG URL conformance (stdlib `urllib.parse` is RFC 3986-ish; differences in
default-port removal, backslash handling, percent-encoding sets, and IDN are not covered by the
matrix); full HTML5 tree construction (`HTMLParser` has no implied `<head>`, no template-content
model, and no adoption-agency behavior); absence of network calls at runtime (no sandbox proof
was run here; `strace -f -e trace=network` is available if L1 wants a runtime control, but it is
not part of this minimal set); search-engine selection or live publishing readiness (explicit
contract limits); independence of oracle authorship beyond the procedural split (Matrix and
Implement are same-wave authors; the frozen contract and pre-commit oracle are the mitigation,
not a proof).

## Residual decisions for L1 (freeze before E1 is written)

1. `missing_head` exit/id (recommendation: `2` / `html_unsupported`).
2. `href_empty` (recommendation: `1` / `canonical_href_missing`).
3. `base_invalid` must not fall back to the document URL; `1` / `base_url_invalid`.
4. `duplicate_same` must not deduplicate identical hrefs; `1` / `canonical_multiple`.
5. `page` value in findings = manifest `url`; `pagesChecked` semantics as above.
6. The baseline-unavailable exit `0` is not a clean verdict; label it in the round report.

## Checks for L1 (the first execution; this seat ran none)

```bash
cd /home/vgpnk/Projects/shokunin/kake-shokunin
# A exists and is clean
git rev-parse HEAD
git status --porcelain

# E4
python3 scripts/canonical_audit.py --selftest; echo "selftest exit=$?"

# E2 (base validator absent; candidate instrument)
python3 .ufo/waves/round-22/measure.py --root . \
  --revision 7c61c8cc791bde36dd5e3688bdfea2678d90146c --cases-root .
# expect exit 0, available false, accepted 0, total 32, snapshot_tampered not reported

# E3 (contract count command)
python3 .ufo/waves/round-22/measure.py --root . --revision "$(git rev-parse HEAD)"
# expect exit 0, available true, accepted 32, total 32, 32 rows match, before/after digests equal

# E5 controls (as implemented by measure.py/matrix.py; record exact argv)
# pin tamper: expect exit 2, no accepted tally
# oracle mutation: expect exit 1, one named mismatch

# independent digest cross-check
git cat-file blob "$(git rev-parse HEAD):scripts/canonical_audit.py" | sha256sum
git cat-file blob "$(git rev-parse HEAD):.ufo/waves/round-22/cases.json" | sha256sum
```

## File changes

- Created: `.ufo/waves/round-22/w1/SimplifyProof.md` (this report) under
  `/home/vgpnk/Projects/shokunin/kake-shokunin`.
- No other file written, no code edited, no commit, no package transaction, no service.

Live-tree observation at write time: `git rev-parse HEAD` is still
`7c61c8cc791bde36dd5e3688bdfea2678d90146c`, but the working tree acquired uncommitted
changes while this report was being written — `LOG.md`, `PROVINCE.md`, `SKILL.md`,
`corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md` modified; untracked
`corpus/knowledge/static-canonical-preflight.md` and `corpus/lessons/round-22.md`.
None are mine; this seat wrote only this report. They are the concrete reason E2/E3 must
cite a clean code+oracle commit rather than measure the live tree: a mid-wave tree is not a
revision, and its instrument can change under the measurement.

## Tool log

- Installs/upgrades: none.
- Existing tools used: `read`, `bash`, `write`, `python3` (3.14.8), `git`, `sha256sum`, and
  read-only shell utilities (`ls`, `find`, `sed`, `grep`, `wc`, `cat`, `head`).
- Read-only observations: contract bytes and digest; `git rev-parse HEAD`; `git cat-file -e`
  absence of `scripts/canonical_audit.py`; r21 `measure.mjs`/`replay-proof.mjs`/`expected.json`/
  `measure-*.json` shapes; r21 `GateContract.md`, `Confinement.md`, `CountingRecipes.md`,
  `FrozenMeasurement.md`; `PROTOCOL.md` §Evidence standard/§Gate standard; `SKILL.md` registry
  precedent; the live (untracked at write time) r22 `corpus/knowledge/static-canonical-preflight.md`
  and `corpus/lessons/round-22.md` for a policy cross-check. No live-network reads; no credential
  paths opened.
