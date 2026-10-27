# ExecutorCounterDoNothing — do-nothing assessment against the frozen C1 counter

Seat: ExecutorCounterDoNothing (executor, wave kake-r62-w1).
Item: "Using committed base bytes only, independently assess whether do-nothing reaches the counter predicate; provide per-condition result, no lane writes."

Advisory only. No claim, counter, criterion, score, lane file, or corpus file was modified. All writes were to
`/fast/scratch/hyaku/kake-r62/ExecutorCounterDoNothing/` (removed before yield) and to this report path.

## Verdict

**Do-nothing does NOT reach the counter predicate.** `met=false`, exit `1`, reproduced independently of the frozen
counter's own verdict and re-derived condition-by-condition from committed Git blobs.

## Frozen artifact identity (verified)

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ sha256sum .ufo/waves/round-62/c62_calibration.py
ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d  .ufo/waves/round-62/c62_calibration.py
```
Matches the sha256 declared in the round-62 prompt and contract. Counter file unmodified by this seat.

Base revision: `c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13` = current `HEAD` of the lane repo
(`git rev-parse HEAD` → same hash); `git status --porcelain` shows only the untracked `.ufo/waves/round-62/` wave
directory, and `git diff --stat <base>` over all tracked paths is empty. So "committed base bytes" and "current
worktree" are identical for every measured path today.

## Frozen counter, run on the committed base (reproduces the recorded base-control)

```
$ python3 -B .ufo/waves/round-62/c62_calibration.py --root . --revision c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13
revision=c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13 disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false
EXIT=1
```
Byte-identical to the base-control recorded in the contract/prompt (`unresolved=1 quote_correction=0 criterion=0
lesson_gate=0 source_row=1 met=false exit 1`). Re-run from a different cwd with an absolute `--root` gave the same
line and the same exit code.

## Independent per-condition assessment (not trusting the counter's own printout)

I re-implemented each conjunct from the counter's source and re-derived it against `git show <base>:<path>` blobs
only (`/fast/scratch/hyaku/kake-r62/ExecutorCounterDoNothing/indep_eval.py`). Result:

| # | Condition | Measured at base `c341a7a` | Value | Evidence |
|---|---|---|---|---|
| 1 | `unresolved_round61_spotcheck_disagreements` | 1 (the unique S432 `Disagree` row) | **1 → blocks** | `corpus/lessons/round-61-verifier-spotcheck.md:33` — `\| S432 / Fetch \| Admit \| https://fetch.spec.whatwg.org/, §3.6; … \| Disagree \| “Web developers and conformance checkers must use the following” is only a generic lead-in, not substantive evidence…` |
| 2 | `substantive_quote_correction` | 0 — quote conjunct missing, `Round-62 correction` conjunct missing | **0 → blocks** | `corpus/knowledge/response-header-expectations.md` at base: `QUOTE in entry = False`, `"Round-62 correction" in entry = False`; `"S432 §3.6" in entry = True` already (lines 75, 86). Base entry still carries the rejected lead-in at line 79 (`> "Web developers and conformance checkers must use the following"`) and the truncated fragment at line 77 (`> "can be used to require checking of a"`). |
| 3 | `criterion_present` | 0 — criterion phrase absent, lesson filename absent | **0 → blocks** | `corpus/QUALITY.md` at base: `"substantive located quote" in QUALITY = False`, `"round-61-verifier-spotcheck.md" in QUALITY = False` (grep returned nothing, rc=1). |
| 4 | `lesson_gate` (counter's `resolved` term) | 0 — `corpus/lessons/round-62.md` does not exist at base | **0 → blocks** | `git ls-tree -r --name-only <base> -- corpus/lessons/round-62.md` → empty; `git show <base>:corpus/lessons/round-62.md` → no such path. |
| 5 | `source_row` | 1 — S432 registry row present | **1 (satisfied)** | `corpus/SOURCES.md:178` — `\| S432 \| WHATWG Fetch — https://fetch.spec.whatwg.org/ \| spec \| A \| X-Content-Type-Options nosniff value rule \| …` |

Composite at base: `disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1`,
`resolved=False` → `met=false`, exit 1. Under the contract-literal predicate
(`unresolved==0 AND substantive_quote_correction==1 AND criterion_present==1`) the result is also `false`, so the two
readings of the frozen predicate agree at base.

**Independent conclusion: 4 of 5 counter conditions are unmet at base; do-nothing cannot reach the predicate.**
Conditions 1, 2, 3 (and 4) are each independently sufficient to block `met=true`.

## Discriminating-power check (scratch fixture only, no lane writes)

A scratch clone at `/fast/scratch/hyaku/kake-r62/ExecutorCounterDoNothing/fixture` (`git rev-parse --show-toplevel`
asserted to equal that fixture dir before every mutation) was used to confirm the counter is not vacuously false and
that each conjunct is load-bearing. The frozen counter was run unmodified against fixture commits.

```
$ python3 -B mutate.py
fixture toplevel=/fast/scratch/hyaku/kake-r62/ExecutorCounterDoNothing/fixture
[do_nothing]      exit=1 :: disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false
[full]            exit=0 :: disagreements=1 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true
[no_quote]        exit=1 :: disagreements=1 unresolved=1 quote_correction=0 criterion=1 lesson_gate=1 source_row=1 met=false
[no_criterion]    exit=1 :: disagreements=1 unresolved=1 quote_correction=1 criterion=0 lesson_gate=1 source_row=1 met=false
[no_lesson_gate]  exit=1 :: disagreements=1 unresolved=1 quote_correction=1 criterion=1 lesson_gate=0 source_row=1 met=false
[no_source_row]   exit=1 :: disagreements=1 unresolved=1 quote_correction=1 criterion=1 lesson_gate=1 source_row=0 met=false
```
Every conjunct is necessary; the "full" state reaches `met=true`, so the base `met=false` is a real discrimination,
not a permanently-false counter. Note the counter's `unresolved` is *derived*: `unresolved = disagreements if not
resolved else 0`, so the S432 `Disagree` row may legitimately remain in the record (the mission requires it be kept,
not marked rejected) — `disagreements=1` with `unresolved=0` in the `full` row is exactly that case.

## Additional counter-behavior probes (advisory for the implementers)

```
$ python3 -B probes.py
B1 worktree has after-state, HEAD still base:
    (1, 'revision=c341a7a… disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false')
B2 after commit: (0, 'revision=8ee2d70… disagreements=1 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true')
A1 spot-check blob removed -> exit=2 :: could-not-evaluate: missing verifier spot-check
```
- The counter reads **committed blobs only** (`git show <rev>:<path>`); uncommitted worktree edits do not move it.
  The after-state must be *committed* to be measured.
- Exit code `2` (not `1`) is reserved for the missing-spot-check evaluation failure path. A lane that deletes or
  renames `corpus/lessons/round-61-verifier-spotcheck.md` would make the counter non-evaluable (exit 2) rather than
  merely unmet.

Quote-literal sensitivity (same fixture, each case committed separately):
```
[C1_exact]               exit=0 :: quote_correction=1 … met=true
[C2_wrapped]             exit=1 :: quote_correction=0 … met=false   (quote hard-wrapped across lines)
[C3_ascii_apostrophe]    exit=1 :: quote_correction=0 … met=false   (U+2019 ’ replaced by ASCII ')
[C4_backticked_content_type] exit=1 :: quote_correction=0 … met=false  (`Content-Type` in backticks)
```
The frozen `QUOTE` constant (counter line 20) is byte-exact:
`"response header can be used to require checking of a response’s Content-Type header against the destination of a request"`
— U+2019 right single quote at offset 61, plain hyphen in `Content-Type`, no backticks, no line breaks. An appended
correction must carry the quote in that single-line plain-text form. The quote as rendered in the retained source
uses inline `<code>` markup around `X-Content-Type-Options` and `Content-Type`; the counter's constant is the
markup-stripped reading of the same sentence, so it matches the source text only after removing tags and backticks.

Source-grounding cross-check of that sentence against the committed retained body
`.ufo/waves/round-61/sources/S432.html` (tracked at base; `git ls-tree` confirms):
- §3.6 heading at line 6149 (`<h3 … data-level="3.6" id="x-content-type-options-header">`).
- Substantive prose spans lines 6151–6154 (line 6150 is `<p>The`); after tag-stripping and whitespace-normalising,
  the sentence reads: `The X-Content-Type-Options response header can be used to require checking of a response’s
  Content-Type header against the destination of a request.` It occurs exactly **once** in the whole retained page
  (occurrence count = 1 over the tag- and backtick-stripped page text), immediately under the §3.6 heading and
  before the `determine nosniff` algorithm (lines 6157+), which is a separate normative block and must not be merged
  into the quotation.
- The counter's `QUOTE` constant is a contiguous substring of that markup-normalised sentence (it starts at
  `response header`, dropping the leading `The X-Content-Type-Options`), so it is grounded in the source, but it is
  *not* present in the raw tag-stripped text while backticks are retained — hence the C4 result above.

## Risks / blockers

- None blocking for this seat. No blocker encountered; the frozen counter hash matches and the base-control is
  reproducible.
- Advisory for the implementing lanes (does not change the frozen predicate): the appended knowledge correction must
  (a) contain the exact single-line `QUOTE` literal (U+2019, no backticks, no wrapping), (b) contain the literal
  string `S432 §3.6`, and (c) contain the literal string `Round-62 correction`. The QUALITY criterion must contain
  both `substantive located quote` and `round-61-verifier-spotcheck.md`. `corpus/lessons/round-62.md` must exist with
  a `## Gate` section mentioning `S432`, `Agree` and `Reject`, and the `| S432 |` row in `corpus/SOURCES.md` must be
  preserved verbatim (the counter counts `"| S432 |"` as a prefix match and would drop `source_row` to 0 if the row
  were renamed).
- The mission requires the round-61 S432 `Disagree` row to be kept, not marked rejected. The counter supports that:
  it derives `unresolved=0` from the `resolved` conjunction, not from deleting the row. A mutation that flipped the
  row's verdict to `Agree` in isolation yields `disagreements=0 unresolved=0 … met=false` — still not met, and it would
  destroy the audit record.

## Exact commands used (lane read-only; all writes in scratch)

```
cd /home/vgpnk/Projects/shokunin/kake-shokunin
sha256sum .ufo/waves/round-62/c62_calibration.py
git rev-parse HEAD ; git status --porcelain ; git diff --stat c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13 -- .
python3 -B .ufo/waves/round-62/c62_calibration.py --root . --revision c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13
git show c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13:corpus/lessons/round-61-verifier-spotcheck.md | grep -n "S432"
git show c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13:corpus/knowledge/response-header-expectations.md | grep -n -i -E "S432|Round-62|substantive located quote|Content-Type header against"
git show c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13:corpus/QUALITY.md | grep -n -i -E "substantive located quote|round-61-verifier-spotcheck"
git show c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13:corpus/SOURCES.md | grep -n "| S432 |"
git ls-tree -r --name-only c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13 -- corpus/lessons/round-62.md .ufo/waves/round-61/sources/S432.html
sed -n '6145,6160p' .ufo/waves/round-61/sources/S432.html
python3 -B indep_eval.py ; python3 -B mutate.py ; python3 -B probes.py ; python3 -B probe_quote.py ; python3 -B probe_robust.py
```
No `git`/`jj` mutation was performed on the lane repo, the fleet repo, any sibling repo, or any source tree. The only
git mutations were in the scratch fixture clone, each preceded by an asserted `git rev-parse --show-toplevel`, with
fixture-only identities (`user.name=fixture`, `user.email=fixture@example.invalid`) supplied per-command via `-c`.
No pacman transaction was run; no tool was installed (none was needed).
