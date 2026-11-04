# ReviewCounter — round 85 / wave 1

Axes: C1 registry discoverability and truthful command maps; C2 frozen-case discrimination and semantic limits; revision/receipt integrity; production isolation.

Recommendation only, not admission or closure. No production edits. The two frozen targets remain **C1 3/3 complete rows** and **C2 all ten original cases, 10/10**; neither is narrowed. No full D84-queue closure claim.

## Findings, by severity

### Medium — a 3/3 C1 result does not establish truthful registry rows

Evidence: `.ufo/waves/round-85/count.py:26-34` scans every leading-pipe line in SKILL.md, not the registry heading; it tests substrings and nonempty cells, not command behavior or proof existence. The retained `ReviewCounter/fixtures/c1-dummy/SKILL.md` contains three eight-cell rows with `echo <filename>`, `0=wrong 1=wrong`, `echo --selftest`, and nonexistent `.ufo/waves/nonexistent`. No instrument or proof file exists in that fixture. Actual result: **exit 0, complete=3/3, missing=0, met=true**.

This is a demonstrated soundness ceiling, not a failure of the contract's explicitly syntactic predicate. Preserve the green dummy receipt alongside the red prose-only receipt. Do not promote C1 into semantic/gate conformance, runnable-command proof, proof-retention verification, or registry-home placement proof. Read all three actual rows independently before integration.

### Medium — blanket `64=usage` promises would contradict the two r84 counters

Read-only definition review, not additional executions:

* `.ufo/waves/round-84/c84_defect_queue.py:309-331`: missing `--root` after successful parsing returns 64; nonexistent root returns 2; normal evaluation returns 0 only when all four D1–D4 conjuncts close, otherwise 1 (`:199-211`). But `parse_args` at `:315` is uncaught, so argparse parsing faults use its standard exit **2**, not the docstring's blanket 64. Missing retained evidence generally reopens items and produces 1, not necessarily 2 (`:46-56`, `:119-196`). A bad revision's failed `git show` also becomes missing evidence, not a validated revision error.
* `.ufo/waves/round-84/c84_policy_values.py:263-292`: same uncaught `parse_args` distinction: parsing faults 2; parsed invocation without root 64; nonexistent root 2. Unevaluable declared/expectations input explicitly returns 2 (`:154-162`); evaluated unmet flags return 1 (`:206-225`). Unhandled filesystem/export/conversion exceptions are not normalized to 2. Entry supports `--root`, optional `--revision` and `--work`; selftest is `--selftest` (no fixture writes in that counter's own selftest).
* `scripts/policy_value_class.py:197-221`: catches argparse SystemExit, mapping non-help parse failures to **64**. Missing/conflicting options also 64. Normal classification returns **0 for every printed semantic verdict**, including `policy-changed` and `policy-unclassified` (`:78-85`, `:107-131`); exit 1 is unevaluable input/caught error, not changed-policy rejection. Selftest returns 0/1 (`:192-194`). `--work` is allowed only with selftest. This is an experimental frozen generic classifier, not a publishing gate.

Action: registry maps should state these distinctions, rather than copying docstrings or treating classifier exit 0 as policy approval. No final candidate registry rows were available in the material reviewed; this is a source-backed integration constraint, not an allegation about unseen candidate text. No r84 script was executed by this seat.

### Low — C2 ten-case success cannot establish the full decoder interface

Evidence: `.ufo/waves/round-85/count.py:11-21,39-54` runs only ten valid JSON-list examples, accepts process exit 0 plus JSON-decoded object equality, and does not invoke selftest or invalid/usage paths. Three valid policies never appear: `no-referrer-when-downgrade`, `origin-when-cross-origin`, `strict-origin-when-cross-origin`. The sole uppercase example is followed by recognized `origin`; a wrongly case-insensitive decoder could still pass it. There are no malformed JSON, non-list, non-string element, CLI usage, empty-token-after-valid, or selftest-exit assertions. These are static coverage observations; no extra candidate trials were run.

The counter does distinguish opposite token order (cases 0 and 1), repeated field order, unknown-token fallback, empty list, duplicates and ordinary surrounding spaces. The assigned constant `strict-origin` control passed only cases **0, 7, 9**, giving **3/10, exit 1, met=false**. Finite cases never constitute semantic proof: source review plus independent interface/selftest evidence remain necessary, without changing this ten-case numerator. The separate retained-r84 real trial is not measured here and must not be folded into 10/10.

## Actual controls and receipts

Executed driver (exit **0**):

`python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-85/w1/ReviewCounter/run_controls.py`

The driver launched these six independent frozen-counter measurements concurrently, with each child's exact absolute argv, cwd, TMPDIR, stdout, stderr and exit retained in `.ufo/waves/round-85/w1/ReviewCounter/controls.json`:

| Measurement | Exit | Actual result |
|---|---:|---|
| C1 unchanged base `bdabc6bc8f762a16c6c19c524c4ac84528eb4bf7` | 1 | complete=0/3, missing=3, met=false |
| C2 unchanged base, same revision | 1 | cases=0/10, met=false |
| C1 prose-only declarations | 1 | complete=0/3, missing=3, met=false |
| C1 incomplete two-cell dummy rows | 1 | complete=0/3, missing=3, met=false |
| C1 shape-complete but false dummy rows | 0 | complete=3/3, missing=0, met=true |
| C2 constant `{"effective":"strict-origin"}` | 1 | cases=3/10, met=false |

All measurement stderr was empty. Base and deficient-row/constant controls reject their targets: the frozen contract's specified unchanged-control kill rule is not triggered. The shape-complete dummy's false substantive content demonstrates why green syntax is not truthful content.

Read-only `git -C <absolute lane> show 2f042c370b5f11b84d4f8c9e5d066517aef646b8:<path>` calls both exited 0. Observed files matched frozen bytes:

* contract SHA-256 `4545c1e7bb09f3d0cbfa0e7e66f2037dd20792a57c1585310997aa1112d3a88d`;
* counter SHA-256 `0dde5c7e16aefefdf32f2d98a8185d62a0a33b1ff339a924cf1fea632ee2f059`.

Reproducible driver and exact fixture bytes are retained only under `.ufo/waves/round-85/w1/ReviewCounter/`. All transient work used `/fast/scratch/hyaku/kake-r85/ReviewCounter/`, with per-control `--work` and TMPDIR set there. Fixtures/receipts were copied before removal; `cleanup.json` records scratch removed. No clone, VCS mutation, source request, account/runtime dispatch, package install, production write or sibling artifact write occurred. Installs: none. Assimilation: none.

## Residual risks and verification gaps

* `xd://lsp` is not mounted: the availability request returned “No such tool.” No semantic references/definition/diagnostics service could be used. Findings are grounded in explicitly cited source definitions and captured controls, not text-search claims of caller absence.
* This is review of the frozen counter and r84 command definitions, not an after-state integration diff. No new production implementation or final row content was scored here; no after-state success is claimed.
* Counter C2 subprocesses have no timeout (`count.py:45`), so a hung candidate can stall a canonical measurement. This seat's outer control runner had a 30-second process timeout; none fired. Canonical counter exports only SKILL.md and decoder when using `--revision` (`:69-72`), so sibling-module dependencies would not survive that measurement. The candidate must be executable under that unchanged export contract.
* No resume path or canonical runtime routing was changed or exercised; no continuity/saturation claim is made.

Self-evaluation: accuracy 4/5 (r84 exits are definition-reviewed, not executed); completeness 4/5 (all assigned controls complete, final integrated candidate unavailable); clarity 4/5 (exact receipts separate from interpretation); actionability 4/5 (registry map corrections and frozen thresholds explicit); conciseness 4/5 (detail retained for replay). Overall 4.0/5. Main's remaining evidence obligation is to review the real integrated rows/decoder and retain the unchanged 3/3 and 10/10 after-state measurements plus separate r84 trial; this seat does not run or admit them.
