# ReviewerC1Prose — block-level prose bindings

## Verdict and scope

**High severity: semantic-resolution false green reproduced.** The frozen counter accepts a correction with no derivation story and accepts a Gate that explicitly denies resolving the disagreement. The prose gates prove block-scoped substring presence, not that the correction applies the round-62 substantive-support criterion or resolves the external verdict. Recommendation: do not treat `met=true` as proof of semantic disagreement resolution. This is a review recommendation, not settlement/admission.

This is **not** a forged raw/recipe/ledger admission: all four pinned artifacts are genuine T0 bytes, the canonical counter actually re-executes the recipe, and the located-line/class evidence remains genuine. Therefore it does not demonstrate the stronger claim that arbitrary marker prose *without retained evidence* passes. Whether this narrower marker-prose survivor triggers the contract's C1 kill rule is for the canonical adjudicator; it demonstrably defeats a semantic-resolution reading of C1.

Axes: semantic calibration validity; faithful canonical execution; reproducible evidence; lane/scratch non-mutation.

## Finding H1: token-bearing non-resolution sets unresolved=0

Absolute implementation: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py`:

- Lines 151–160 select blocks by Markdown heading/correction marker only.
- Lines 247–248 require only the frozen quote and ledger path within the correction block. No derivation assertion or actual use of the ledger is checked.
- Lines 249–251 require the round-62 sentence and the three purpose terms somewhere in its criteria block. They do not relate those terms to the proposition.
- Lines 252–259 require `S432 / Fetch`, a constant verdict span, `collapsed-only`, counter name, and `author-side` or `self-assessment`; no affirmation, resolution, entailment, or contradiction check exists.
- Lines 260–265 require only that the S432 source row has `mined` in cell 8.
- Lines 267–270 subtract one disagreement on the strength of `lesson_gate`, then allow `met=true` when unresolved becomes zero. Thus a contradictory Gate has the same effect as an actual resolution.
- Lines 193–198 count S432/Disagree lines in the spot-check. The actual spot-check was retained byte-for-byte for this attack; no invented verdict file was needed.

Contract: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/contract.md:28–61` calls C1 the repaired semantics-binding resolution, pins retained evidence, and names marker-only greens among its kill cases. The exact frozen pass predicate at lines 35–41 concerns the measured revision and four named control fixtures: this attack does not claim those historical receipts fail or that their bytes changed.

Definition/caller inspection: `evaluate()` is the canonical evaluator (lines 185–278); `main()` passes root/revision directly to it, prints its output, and returns its exit status (lines 432–449). No alternate evaluator or patched imports were used.

## Materials, identity, and execution method

Source revision: `4c8295fa5e3b628f1fdf3840299ae415c01849fb` (T0).
Frozen canonical counter SHA-256 observed: `5489eb2f3ac498e0383d841c677f036231fbf6933717d8da447f3193ff088adf`.

For each of these paths, source bytes were read with the exact command form:

```text
git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:<path>
```

Paths:

```text
.ufo/waves/round-64/c64_calibration.py
.ufo/waves/round-61/sources/S432.html
.ufo/waves/round-63/quote-class/S432.txt
.ufo/waves/round-63/quote-class/quote-classes.json
.ufo/waves/round-63/quote-class/extract_text.py
corpus/lessons/round-61-verifier-spotcheck.md
corpus/SOURCES.md
```

All commands succeeded. Each fixture retained the last six paths verbatim. Only the three prose files were supplied by the attack. The source table was genuine, not a fake `mined` row.

Fixture repositories were built directly by Python writing standard zlib-compressed Git objects and a `refs/heads/fixture` ref under the seat scratch. No Git mutation command (including init/add/commit) ran. Objects use SHA-1 over `type + space + decimal length + NUL + content`; blobs feed sorted recursive tree objects, then a commit with author/committer `ReviewerC1Prose <review@example.invalid> 1793318400 +0000`, and message `Prose binding attack: <variant>`. HEAD points at `refs/heads/fixture`; config declares repositoryformatversion 0, bare false. Before creating commit objects, each repository identity was asserted using:

```text
git -C /fast/scratch/hyaku/kake-r64/ReviewerC1Prose/<variant> rev-parse --show-toplevel
```

Outputs exactly matched each absolute fixture directory (`minimal`, `contradictory`, `missing-quote`). This object construction avoided all mutating Git commands while allowing an unmodified counter to read real committed blobs via Git.

## Exact fixture prose

`minimal/corpus/knowledge/response-header-expectations.md` (lines 1–3):

```markdown
[r63-correction]
The `X-Content-Type-Options` response header can be used to require checking of a response’s `Content-Type` header against the destination of a request.
.ufo/waves/round-63/quote-class/quote-classes.json
```

`minimal/corpus/QUALITY.md` (lines 1–3), also used in both other variants:

```markdown
## Round-62 criteria
A quoted span must substantively support the proposition attributed to its source.
X-Content-Type-Options Content-Type destination
```

`minimal/corpus/lessons/round-64.md` (lines 1–3):

```markdown
## Gate
S432 / Fetch is only a generic lead-in, not substantive evidence for a response-header expectation
collapsed-only c64_calibration.py author-side
```

`contradictory` uses the same three files, appending this line 4 to its knowledge file:

```text
No derivation was performed. The quoted span proves the response-header expectation; the disagreement remains unresolved.
```

and this line 4 to its lesson file:

```text
The verdict above is rejected. No disagreement is resolved by this gate.
```

`missing-quote` retains minimal QUALITY and lesson but its knowledge file has exactly:

```text
[r63-correction]
.ufo/waves/round-63/quote-class/quote-classes.json
```

All paths above were rooted at `/fast/scratch/hyaku/kake-r64/ReviewerC1Prose/<variant>/`. Each displayed file ended with a newline. No source pin or counter was altered.

## Canonical subprocess results

The executable was a byte-identical T0 counter materialized at `/fast/scratch/hyaku/kake-r64/ReviewerC1Prose/c64_calibration.py`. Explicit `TMPDIR` was supplied, including for the counter's internal recipe temporary directory; subprocess cwd was the seat scratch, not the fleet root.

### minimal

```text
$ TMPDIR=/fast/scratch/hyaku/kake-r64/ReviewerC1Prose/tmp python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC1Prose/c64_calibration.py --root /fast/scratch/hyaku/kake-r64/ReviewerC1Prose/minimal --revision a4c630f4b3d1485d38162dd59c3e65b5e77095a4
revision=a4c630f4b3d1485d38162dd59c3e65b5e77095a4 disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
stderr=''
```

### contradictory

```text
$ TMPDIR=/fast/scratch/hyaku/kake-r64/ReviewerC1Prose/tmp python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC1Prose/c64_calibration.py --root /fast/scratch/hyaku/kake-r64/ReviewerC1Prose/contradictory --revision 59da3e2c3c8242494f6821624ef7b93ab1e45bd8
revision=59da3e2c3c8242494f6821624ef7b93ab1e45bd8 disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
stderr=''
```

### missing-quote

```text
$ TMPDIR=/fast/scratch/hyaku/kake-r64/ReviewerC1Prose/tmp python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC1Prose/c64_calibration.py --root /fast/scratch/hyaku/kake-r64/ReviewerC1Prose/missing-quote --revision 6fe26ffb8f4d11b63d31e407fbb6b09441ea4d19
revision=6fe26ffb8f4d11b63d31e407fbb6b09441ea4d19 disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=0 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=false
exit=1
stderr=''
```

The negative control demonstrates that these are actual quote/block gates rather than an always-green harness. The contradictory positive demonstrates that `unresolved=0` is not evidence of an affirmative semantic resolution.

## Actual diff reviewed

```text
git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff 1a48131577ba82c967650561be34e8dba909432a 4c8295fa5e3b628f1fdf3840299ae415c01849fb -- .ufo/waves/round-64/c64_calibration.py corpus/knowledge/response-header-expectations.md corpus/QUALITY.md corpus/lessons/round-64.md
```

Observed: new counter (449 lines), QUALITY +4 lines, new lesson (110 lines); no knowledge-file change in this diff. The new counter strengthens evidence extraction, but its new block-level prose requirements remain presence predicates.

## Residual risk and verification gaps

- LSP unavailable: reading `xd://lsp` returned `No such tool: xd://lsp`. Therefore references/definition/diagnostics could not be obtained; findings use direct source inspection and real canonical subprocess behavior, not grep asserted as semantic proof.
- No changes to the frozen lane, claims, controls, recipe, or lesson. No C2/C3, runtime routing, resume, or saturation claim was evaluated in this prose-only seat.
- This attack does not say the real T0 prose is wrong; it says the counter's green cannot establish the prose's semantic correctness. Real source extraction still passes independently.
- No tools installed or upgraded. Scratch was removed in `finally` after results were captured; observed `scratch_removed=True`. Only this report persists.

## Self-evaluation

Accuracy 4/5: real canonical outputs and intact pins, but closure semantics require human adjudication. Completeness 5/5: requested minimal prose, explicit contradictory variant, negative control, and cleanup completed. Clarity 4/5: separates genuine extraction from false semantic closure, though the distinction is necessarily nuanced. Actionability 4/5: exact commands and fixture bytes supplied; deleted object stores must be rebuilt to rerun. Conciseness 4/5: long evidence section is necessary for scratch deletion. Overall 4.2/5. Improvement priority: treat token-prose gates only as syntax checks and independently assess whether the substantive disagreement was resolved. Would the user agree: likely, given the directly reproducible false semantic green and explicit scope limits.
