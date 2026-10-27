# ScribeSkillRows

Scope: draft the round-58 `SKILL.md` gate-registry edits. No lane file was edited (the L1 applies the draft).
Lane revision read: `master` = `cc8da1674d6e590ae2d05e1f48944ac7939e9ecd` (contract commit `fff3eea6aa349c8635fd84a791cc32de350ee1c2`,
base `044048597d62f3199494b63b36e90dd57825e350`). All counters were run read-only from the lane with
`TMPDIR=/fast/scratch/hyaku/kake-r58/ScribeSkillRows`; nothing was written in the lane except this report and
`ScribeSkillRows.files/`.

Facts taken from source, not from a run: each c58 counter's docstring, `PREDICATE`, `main()` exit paths and
`--selftest` stub (`.ufo/waves/round-58/c58_*.py`); the tool-fix contract in `.ufo/waves/round-58/w1-spec.json`
(`ExecResolverFix`: fence-aware `parse_registry`, `git ls-tree -r -z` for F1); the candidate tool's own receipt
`.ufo/waves/round-58/w1/ExecResolverFix.files/{selftest.txt,gate-run.txt}` (`selftest: 59/59`, C2 gate `12/12` at
`58976c081091`); the C3 selftest pin `KAKE_R58_SELFTEST_REV=fff3eea6aa349c8635fd84a791cc32de350ee1c2` from the
`ExecC3SelftestPort` seat prompt. The candidate has **not** landed in `scripts/id_resolver.py` (still the round-57
49-check file at `master`); the `source-id-resolver` rewrite below is the post-landing text.

## CURRENT ROWS:

`SKILL.md` line 1216 (r52), verbatim:
| quote-truth-counter | gate (offline, committed bytes only; no network) | `python3 -B .ufo/waves/round-52/c52_quote_truth.py --root . --revision <commit>` | `0=met` (`conditions_passed == 8 of 8`); `1=not met` (any C1–C8 sub-condition fails); `2=could-not-evaluate` (malformed receipt or mirror-pin JSON, exception); `64=usage` | `KAKE_R52_SELFTEST_REV=1ae8de5d4dee python3 -B .ufo/waves/round-52/c52_quote_truth.py --selftest` (18 fixtures, sandbox repos; the leading pin fixes the fixture revision — without it the fixtures rebuild from `HEAD` and the pass case fails; receipt `.ufo/waves/round-52/control/c2-quote-selftest.txt`) | `.ufo/waves/round-52/baselines.json` pins the counter sha256, the three retained-body sha256s, the mirror-pin sha256 and both receipt digests; C8 reads the mirror BYTES (`show(root, rev, MIRROR)`) and requires append-only equality with the measured registry minus the adopted rows | read-only `git show`/`git ls-tree`/`git log`; selftest writes only sandbox fixture repos under `.ufo/waves/round-52/selftest/` and removes them | kake |

`SKILL.md` line 1234 (r55), verbatim:
| yahoo-robots-quote-truth-counter | gate (offline, committed bytes only; no network) | `python3 -B .ufo/waves/round-55/c55_quote_truth.py --root . --revision <commit>` | `0=met` (`conditions_passed == 8 of 8`); `1=not met` (any C1–C8 sub-condition fails); `2=could-not-evaluate` (malformed receipt or mirror-pin JSON, an exception); usage errors also exit 2 (`ap.error`) | `KAKE_R55_SELFTEST_REV=64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6 python3 -B .ufo/waves/round-55/c55_quote_truth.py --selftest` (54 sandbox-repo fixtures built from the committed round-55 evidence at the pinned revision, including 3 unit-rule checks; receipt `.ufo/waves/round-55/controls/c2-selftest.txt`) | `contract.json` `claims.C2`; base control `.ufo/waves/round-55/controls/base-c2-quote-truth-v2.txt` (`0/8`, exit 1); retained-body receipts `.ufo/waves/round-55/sources/receipts.json`; pre-append mirror pin `.ufo/waves/round-55/assimilation/mirror-pin.json` | none (reads `git show` / `git log` only; selftest writes only `mktemp -d` sandboxes) | kake |

`SKILL.md` line 1254 (r56), verbatim:
| yahoo-crawl-handling-quote-truth-counter | gate (offline, committed bytes only; no network) | `python3 -B .ufo/waves/round-56/c56_quote_truth.py --root . --revision <commit>` | `0=met` (`conditions_passed == 8 of 8`); `1=not met` (any C1-C8 sub-condition fails); `2=could-not-evaluate` (malformed receipt or mirror-pin JSON, an exception); usage errors also exit 2 (`ap.error`) | `KAKE_R56_SELFTEST_REV=f8438a282d5946b386812d784cc617edcbc9201d python3 -B .ufo/waves/round-56/c56_quote_truth.py --selftest` (86 checks: 83 sandbox-repo fixtures built from the committed round-56 evidence at the pinned revision, plus 3 unit-rule checks) | `contract.json` `claims.C2`; base control `.ufo/waves/round-56/controls/base-c2-quote-truth.txt` (`0/8`, exit 1); retained bodies `.ufo/waves/round-56/sources/` with `receipts.json`; held-row body pin `HELD_BODY_SHA256` (S367); pre-append mirror pin `.ufo/waves/round-56/assimilation/mirror-pin.json` | none (reads `git show` / `git log` only; selftest writes only `mktemp -d` sandboxes) | kake |

`SKILL.md` line 1274 (r57):
| id-resolver-gate | gate (differential: a reference implementation inside the gate against the tool, over randomised fixtures and the real revisions; reads sibling registries) | `python3 -B .ufo/waves/round-57/c57_idresolver_gate.py --root . --revision <commit> [--fleet <fleet root>]` | `0=met` (`gate_conditions_passed == 5 of 5`); `1=not met` (G1 tool present, G2 selftest, G3 fixtures, G4 red-before at `3994101`, G5 green at the measured revision); `2=could-not-evaluate` (revision unresolved, no sibling registries, live sibling ownership differs from `sibling-snapshot.json`); `64=usage` | the gate has no selftest of its own; the tool it gates has `python3 -B scripts/id_resolver.py --selftest` (49 checks, generated sandbox lanes and siblings); measured on the shipped gate by `.ufo/waves/round-57/w2/ExecGateFlake.md`: the genuine tool 5/5 in ten of ten runs, a constant printer 2/5, a working-tree reader 4/5, and a green-only printer failing G3, G4 and G5 (`w2/ReviewerQualitySkill.md`) | `contract.json` `claims.C2`; base control `.ufo/waves/round-57/controls/base-c2-idresolver-v2.txt` (`0/5`, exit 1); `sibling-snapshot.json` | none (clones into `mktemp -d`) | kake |

`SKILL.md` line 1275 (r57):
| baidu-dead-link-quote-truth-counter | gate (offline, committed bytes only; no network) | `python3 -B .ufo/waves/round-57/c57_quote_truth.py --root . --revision <commit>` | `0=met` (`conditions_passed == 8 of 8`); `1=not met` (any C1-C8 sub-condition fails); `2=could-not-evaluate` (malformed receipt or mirror-pin JSON, an unreadable base revision, an exception); `64=usage` (a missing `--revision` or any argparse error) | `KAKE_R57_SELFTEST_REV=b9a5d012f7fd python3 -B .ufo/waves/round-57/c57_quote_truth.py --selftest` (120 checks: 105 sandbox-repo fixtures built from the retained round-57 bodies at the pinned revision, plus the unit-rule, kill-matrix, unreadable-base and usage-exit checks) | `contract.json` `claims.C3`; base control `.ufo/waves/round-57/controls/base-c3-quote-truth-v2.txt` (`0/8`, exit 1); retained bodies pinned by sha256 in the counter; `sources/receipts.json`; `assimilation/mirror-pin.json` | none (read-only; its selftest builds `mktemp -d` repos) | kake |

`SKILL.md` line 1276 (r57), verbatim:
| source-id-resolver | tool (read-only; stdlib python) | `python3 -B scripts/id_resolver.py --root . [--revision REV] [--fleet FLEET]` (lists every `S###` id cited in `corpus/knowledge/**/*.md` that the lane registry lacks and names the sibling registries that hold it) | `0=no dangling id`; `1=dangling ids found` (one `DANGLING` line each, then `ids_cited=N ids_resolved=N dangling=N owned_elsewhere=N unowned=N`); `2=could-not-evaluate` (revision unresolved, registry absent, no knowledge file); `64=usage` | `python3 -B scripts/id_resolver.py --selftest` (49 checks) | red-before: at lane revision `3994101` it reports exactly S367 S372 S373 S390 S409, each held by kotodama-shokunin (`.ufo/waves/round-57/w1/ExecResolverGroundTruth.md`, gate condition G4) | none | kake |

## PROPOSED ROWS:

Insert after the round-57 section (new `### Round 58 gate registry additions` prose + table). `<N>` / `<N>/<N>` are
the tallies the L1 fills after the final selftest run of each hardened counter.

Prose:

> Round 58 ships three counters whose predicates are frozen in `.ufo/waves/round-58/contract.json` before any data; all three are offline and read
> committed bytes (C2 runs the tool at a revision over gate-built fixture lanes). C1 calibrates the receipt-rewrite class the round-57 spot-check routed
> as D1 (`events=19 undisclosed=19` at the base), C2 gates the two disclosed false-green defects of `scripts/id_resolver.py` (fence-blind registry,
> `git ls-tree`-quoted paths; base `7/12`), C3 is the freshness claim for two Baidu crawler-identification entries on new rows S423/S424 (base `0/8`).
> Receipts: `.ufo/waves/round-58/controls/`; a receipt is committed once, after the run it records, and a re-run lands under a new file name (C1
> enforces `new_rewritten == 0` for this round's own receipts). Withdrawal rule: a row goes when its counter leaves the tree.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| receipt-rewrite-counter | gate (offline, committed bytes only; whole-ancestry history walk over every receipt path of every round, against the round-58 ledger) | `python3 -B .ufo/waves/round-58/c58_receipt_rewrites.py --root . --revision <tip>` (`--json`, `--list` optional; the tip must hold the C2 and C3 after-receipts) | `0=met` (`undisclosed == 0 AND phantom == 0 AND malformed == 0 AND wrong_kind == 0 AND unpointed == 0 AND new_rewritten == 0 AND new_receipts == 2`); `1=not met` (an undisclosed event, a phantom/malformed/mistyped/unpointed ledger entry, a rewritten round-58 receipt, or either after-receipt missing); `2=could-not-evaluate` (any exception in the measurement: an unresolved tip, a ledger present but not JSON, a git failure); `64=usage` (a missing `--revision` or any argparse error) | `python3 -B .ufo/waves/round-58/c58_receipt_rewrites.py --selftest` (`<N>/<N>` checks; 18 in version 1 — `controls/c1-selftest-v1.txt` — hardened in wave 1 with merge-side, quoted/non-ASCII path, binary, revert, symlink and pointer-format fixtures) | `contract.json` `claims.C1`; base control `.ufo/waves/round-58/controls/base-c1-receipt-rewrites.txt` (`events=19 undisclosed=19`, exit 1); the ledger `.ufo/waves/round-58/receipt-rewrites.json` | none (read-only; its selftest builds `mktemp -d` repos) | kake |
| resolver-cases-counter | gate (differential: the tool at the revision against gate-built fixture lanes; every fixture repo is `git init` in its own dir, verified by `rev-parse --show-toplevel`) | `python3 -B .ufo/waves/round-58/c58_resolver_cases.py --root . --revision <rev> [--work <scratch>]` | `0=met` (`cases_passed == 12 of 12`); `1=not met` (any of K1-K5 — fenced heading/row before and inside `## Registry`, non-ASCII and quote-character path at a revision — or P1-P7 — 3-space row, row after a closed fence, 4-space line is code, committed sibling owns, absent `--fleet` exit 2, tool selftest N/N with N >= 49, real lane green with `ids_cited >= 106`); `2=could-not-evaluate` (revision unresolved, tool absent at the revision); `64=usage` | `python3 -B .ufo/waves/round-58/c58_resolver_cases.py --selftest` (`<N>/<N>` checks; version 1 has none, wave 1 adds five stub tools — a constant green printer, an always-1 printer, a first-fence-dropping tool, the base tool at `7/12`, one stub at `11/12`) | `contract.json` `claims.C2`; base control `.ufo/waves/round-58/controls/base-c2-resolver-cases.txt` (`7/12`, exit 1); the tool it gates is `source-id-resolver` below | fixtures only, under `--work` / `$TMPDIR` | kake |
| baidu-crawler-identification-quote-truth-counter | gate (offline, committed bytes only; no network) | `python3 -B .ufo/waves/round-58/c58_quote_truth.py --root . --revision <commit>` (`--base` defaults to the frozen base revision) | `0=met` (`conditions_passed == 8 of 8`); `1=not met` (any C1-C8 sub-condition fails); `2=could-not-evaluate` (malformed receipt or mirror-pin JSON, an unreadable base revision, an exception); `64=usage` (a missing `--revision` or any argparse error) | `KAKE_R58_SELFTEST_REV=fff3eea6aa349c8635fd84a791cc32de350ee1c2 python3 -B .ufo/waves/round-58/c58_quote_truth.py --selftest` (`<N>/<N>` checks; version 1 is a stub, wave 1 ports the 120-check round-57 v2.1 block to the S423/S424 bodies, target 120/120) | `contract.json` `claims.C3`; base control `.ufo/waves/round-58/controls/base-c3-quote-truth.txt` (`0/8`, exit 1); retained bodies `.ufo/waves/round-58/sources/S423.html`, `S424.html` pinned by sha256 in the counter; `sources/receipts.json`; `assimilation/mirror-pin.json` | none (read-only; its selftest builds `mktemp -d` repos) | kake |

Row 1276 replacement (post-landing `scripts/id_resolver.py`; the fence and quoted-path behaviour is the C2 build):

| source-id-resolver | tool (read-only; stdlib python; fence-aware registry, NUL-split `git ls-tree`) | `python3 -B scripts/id_resolver.py --root . [--revision REV] [--fleet FLEET]` (lists every `S###` id cited in `corpus/knowledge/**/*.md` that the lane registry lacks and names the sibling registries that hold it; a CommonMark fence in `corpus/SOURCES.md` — 0-3 spaces then >= 3 backticks or tildes, closed by the same character with at least the opening length, or by EOF — registers no heading and no row, while a 4-space-indented line stays code and a row after a closed fence resolves; with `--revision` paths are listed by `git ls-tree -r -z --name-only`, so quoted/non-ASCII names are read) | `0=no dangling id`; `1=dangling ids found` (one `DANGLING` line each, then `ids_cited=N ids_resolved=N dangling=N owned_elsewhere=N unowned=N`); `2=could-not-evaluate` (revision unresolved, registry absent, no knowledge file, absent `--fleet`); `64=usage` | `python3 -B scripts/id_resolver.py --selftest` (`<N>/<N>` checks; 49 through round 57, 59 in the round-58 candidate — checks 50-59 are the fence cases (backtick, tilde, 3-space indent, longer closing run, shorter run, unclosed fence, row after a closed fence) and the non-ASCII / quote-character path cases) | red-before: at lane revision `3994101` the round-57 tool reports exactly S367 S372 S373 S390 S409, each held by kotodama-shokunin (`.ufo/waves/round-57/w1/ExecResolverGroundTruth.md`, gate condition G4); round-58 C2: `c58_resolver_cases.py` `12/12` at the fixed revision against base `7/12` (`.ufo/waves/round-58/controls/base-c2-resolver-cases.txt`) | none | kake |

Companion edit forced by the same build — row 1274, Self-test cell `(49 checks, generated sandbox lanes and siblings)`
becomes `(<N> checks; 49 through round 57, 59 in the round-58 candidate — generated sandbox lanes and siblings)`.
Verified in `.ufo/waves/round-57/c57_idresolver_gate.py` that G2 accepts any `selftest: N/N` with `N >= MIN_SELFTEST`
(49), so the row's gate stays satisfiable at 59 — but the row must not keep claiming 49.

Build constraint found while reading that gate (report to the L1, not a row edit): G2 rejects a tool whose source
contains any of `c57_idresolver_gate`, `.ufo/`, `reference(` (`judge_ref` in `evaluate()`). The landed tool must not
name the gate.

## HISTORICAL GATES:

Measured at `master` = `cc8da1674d6e590ae2d05e1f48944ac7939e9ecd` on 2026-10-26, lane cwd, `TMPDIR` in my scratch.

| gate (row line) | run | result |
|---|---|---|
| c52_quote_truth (1216) | `--root . --revision master` | exit 1, `6/8` — C5 (S374 span) + C8 `registry rows 160 != mirror rows 145 + 3` |
| c52_quote_truth (1216) | `--revision 1ae8de5d4dee8300624b0db2a94497ff905942c5` | exit 0, `8/8` |
| c55_quote_truth (1234) | `--revision master` | exit 1, `6/8` — C7 + C8 `registry rows 160 != mirror rows 155 + 1` |
| c55_quote_truth (1234) | `--revision 64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6` | exit 0, `8/8` |
| c56_quote_truth (1254) | `--revision master` | exit 1, `6/8` — C7 + C8 `registry rows 160 != mirror rows 156 + 2` |
| c56_quote_truth (1254) | `--revision 4cb225fb032b04166fb0232bc98a7bcce72675ec` | exit 0, `8/8` |
| c57_quote_truth (1275) | `--revision 32754df75774dd38e8a96fcda375fc93adf97f1e` | exit 0, `8/8` |
| c57_quote_truth (1275) | `--revision master` | exit 0, `8/8` (160 == 158 + 2) |
| c52_wave_ledger (1215) | `--revision master` | exit 0, `3/3` |
| c55_readme_index (1233) | `--revision master` | exit 0, `knowledge_files=54 coverage_rows=56` |
| c56_selftally (1253) | `--revision master` | exit 0, `tally_mismatches=0 rows_checked=10` |
| c57_receipt_pins (1273) | `--revision master` | exit 0, `new_receipts=3 scorecard_pin=1` |
| c57_idresolver_gate (1274) | `--revision master` | exit 0, `5/5`, G2 `selftest: 49/49` |
| c53_gate_truth (213) | `--revision master` | exit 1, `2/7` |
| c53_gate_truth (213) | `--revision 3994101dba28896830604fd0b08c7f00faca8ed6` | exit 1, `2/7` |

Proposed marking (cell rewrite; the row's command and verdict map stay as they are):

- 1254: Kind cell → `gate (historical: green at its round's measured revision 4cb225fb032b only; red on every later tree by design — mirror-pin 158 rows)`, and its Pinned-values cell gains `historical pin: 4cb225fb032b04166fb0232bc98a7bcce72675ec`.
- 1234: Kind cell → `gate (historical: green at 64c0ce12ffe3 only; red on later trees by design — mirror-pin 156 rows)`, Pinned-values gains `historical pin: 64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6`.
- 1216: Kind cell → `gate (historical: green at 1ae8de5d4dee only; red on later trees by design — mirror-pin 148 rows)`, Pinned-values gains `historical pin: 1ae8de5d4dee8300624b0db2a94497ff905942c5`.
- 1275: Kind cell → `gate (historical from round 58: green at 32754df75774 and at pre-append trees; red once a later round appends a registry row — mirror-pin 158 rows + 2 adopted rows)`, Pinned-values gains `historical pin: 32754df75774dd38e8a96fcda375fc93adf97f1e`.

Why the round-58 tip turns 1275 red: `c57_quote_truth.py` line 560 is `if len(rows) != len(mirror_rows) + len(NEW_ROWS)` —
with S423/S424 appended the registry holds 162 rows against `158 + 2`. That tip result is **[INFERENCE]** (derived
from the code and the contract's `registry 162 rows`; the same check is observed failing in c52/c55/c56 above). The
`master` result (green, 160) is observed.

Not marked historical: `c53_gate_truth` is red at both its own revision (`3994101`, `2/7`, exit 1) and at `master`
(`2/7`, exit 1) — a standing measured defect, not a later-tree artefact; the r57 rows 1273/1274 are green at `master`.
Row 213's `c53_gate_truth.py` receipt `.ufo/waves/round-53/exec-quality-gate/real-round52-tip.txt` already records
`L3_revision_notes FAIL` at `3994101`, so the red-at-home state is the lane's own record, not a new finding.

Receipts for the redirected runs are beside this report in `ScribeSkillRows.files/` (`c52_quote_truth.py.out`,
`c52-at-measured.out`, `c55_quote_truth.py.out`, `c55-at-measured.out`, `c56-at-measured.out`, `c57-at-measured.out`,
`c52_wave_ledger.py.out`, `c55_readme_index.py.out`, `c53.out`, `c53-at-3994101.out`); the two runs whose stdout was
read inline (`c56_selftally`, `c57_idresolver_gate`) are quoted verbatim in the table above. Scratch
`/fast/scratch/hyaku/kake-r58/ScribeSkillRows` was deleted after the copy.

VERDICT: six row edits drafted (three new c58 gates, the fence-aware `source-id-resolver` rewrite, its 1274 tally companion, and four historical markings with verified pins); no gate remains unexplained red at `master`.
