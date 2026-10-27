# ScribeQualityCriterion — round-63 QUALITY criterion (counter semantics binding)

Seat item: "Review the round-63 QUALITY criterion (counter semantics binding): is it falsifiable as
written, does its falsifier command actually run, does it cite its grounding, and does it avoid
banning legitimate future counters? Suggest exact wording fixes or confirm it. Do not edit the file."

No file was edited. Every command below was run read-only against the fleet repo; the two fixture
repos were scratch-only and are deleted (§7).

## 1. Object under review

| Item | Value (verified) |
|---|---|
| Criterion | `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/QUALITY.md:1416` (section header `:1414`, one bullet, 1 physical line) |
| File at measured commit | `git show 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f:corpus/QUALITY.md`, 1416 lines, sha256 `cec4e6b7b578151baa6cc65caea3b50fc3fe820ad0704e38fae312322eaa1e0f` |
| Working tree vs measured | `git diff --stat 05b0d7f4 -- corpus/QUALITY.md` → empty; `sha256sum corpus/QUALITY.md` = same digest |
| Criterion sha (line only) | not recorded anywhere; the bullet has no per-criterion id or digest |
| Counter it governs | `.ufo/waves/round-63/c63_calibration.py`; sha256 at measured = `bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91` (matches contract) |
| Round-62 counter (cited as defect) | `.ufo/waves/round-62/c62_calibration.py`; sha256 at measured = `ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d`; unchanged since round 62 |

Append-only check (contract §No-harm): `git diff 13d45198 05b0d7f4 -- corpus/QUALITY.md` is
`@@ -1410,3 +1410,7 @@` with four `+` lines and zero `-` lines. The base file is untouched.

Criterion text as committed (line 1416, verbatim):

> **A frozen calibration counter's `resolved` predicate binds semantic evidence, not marker
> strings.** Every component of `resolved` re-derives from committed bytes at the measured revision:
> a quote correction is checked against the retained blobs' own sha256 digests and a match class
> re-derived from those blobs (the lane tool `scripts/quote_class.py` derives the same class as
> round-63 C2 evidence; a counter never gates on the tool, keeping claims separable); a criterion
> check names the located proposition; a lesson-gate check records the outside verdict it claims.
> Freeze rule: the counter's sha256, its red-before/green-after receipts, and its do-nothing and junk
> controls commit before any after-state measurement; no calibration green from a counter that fails
> these bindings is citable, and a counter that changes predicate is itself frozen anew (round-60
> rule). Grounding: round-62 routed defect 1 — `c62_calibration.py` printed `met=true` on a
> marker-only fixture while the S432 disagreement stood and no source body existed (receipt
> `.ufo/waves/round-62/controls/counter-false-green-l1.txt`); `corpus/lessons/round-63.md` §Mistakes.
> Falsifier: `python3 -B .ufo/waves/round-63/c63_calibration.py --root <fixture> --revision <fixture
> rev>` over the round-62 marker-only fixture must print `met=false`; the old c62 counter on the same
> fixture prints `met=true` (family defect documented, not repaired in place).

## 2. Answers to the four asked questions

| Question | Verdict |
|---|---|
| Falsifiable as written? | **No, not literally** — the falsifier's `<fixture>` is undefined, its literal use prints exit 2 *or the forbidden green* (F1); the freeze clause is unsatisfiable (F2); the "do-nothing" control is unlocatable (F3); no "example that fails it" instance is given for the rule itself (F9). The rule's *content* is checkable once the fixture recipe is added. |
| Does the falsifier command run? | **Only after an unstated reconstruction step.** Against a standalone fixture repo: `met=false`, exit 1. Against the committed fixture directory (the natural reading): `could-not-evaluate: verifier spot-check absent`, exit 2; with a fleet revision instead of the fixture rev: `met=true`, exit 0 (F1). |
| Does it cite its grounding? | **Partly.** Two of three citations resolve and say what is claimed (§4 C2–C3). The third, "(round-60 rule)", has no locator and the round-60 bullet it points at does not state the freeze order; the contract §C1 that does state it is not cited (F4). |
| Does it avoid banning legitimate future counters? | **No** in three places: absolute "a counter never gates on the tool" (F6), sha256-mechanism hardcoding plus unqualified "every component re-derives from committed bytes" (F7), and control-class vocabulary that must be guessed (F3). |

## 3. Findings

### F1 — The falsifier is not runnable as written, and its literal form can print the exact green it forbids (blocking)

`--root` is not defined as "a standalone fixture repo whose HEAD is the named revision". The counter
resolves every path with `git -C <root> show <rev>:<path>` (`c63_calibration.py:69-80`), which is
**repo-toplevel-relative**; `git -C` on a directory that is not its own repo walks up to the enclosing
checkout. The committed fixture is a directory of blobs inside the fleet repo
(`.ufo/waves/round-62/controls/false-green-fixture/corpus/`), and revision
`7833be888760bc7878857aa39362792b02e3ab07` is not an object in the fleet repo
(`git cat-file -t` → `fatal: git cat-file: could not get object info`, rc 128; `git rev-list --all`
contains no such commit).

Observed, exact:

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ python3 -B .ufo/waves/round-63/c63_calibration.py \
    --root .ufo/waves/round-62/controls/false-green-fixture \
    --revision 7833be888760bc7878857aa39362792b02e3ab07
could-not-evaluate: verifier spot-check absent
exit=2
```

The counter's own existence probe does not catch this: `git rev-parse --verify <40-hex>` returns **0**
for a nonexistent object (observed: rc 0 for `7833be88…`, while `git cat-file -t` fails), so the
`could-not-evaluate` path is reached only through the missing blob, not through a bad revision.

Worse, the same command with any revision that *does* resolve in the enclosing repo silently measures
the fleet tree instead of the fixture:

```
$ python3 -B .ufo/waves/round-63/c63_calibration.py \
    --root .ufo/waves/round-62/controls/false-green-fixture \
    --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
```

So a reader applying the falsifier "over the round-62 marker-only fixture" with the committed fixture
path sees either no verdict or a **`met=true` on a marker-only fixture** — the precise defect the
criterion exists to forbid. The reconstruction the receipts used (`counter-false-green-l1.txt`: `cp -a
…/false-green-fixture/corpus "$D/"`, `git -C "$D" init -q`, commit, toplevel assertion) is not in the
criterion text.

With the reconstruction (my scratch, throwaway identity, `git -C "$D" rev-parse --show-toplevel` =
`$D`): `met=false`, exit 1 (§5). So the falsifier *works* once specified; it just is not specified.

### F2 — The freeze clause is self-contradictory for green-after receipts

"its sha256, its red-before/green-after receipts, and its do-nothing and junk controls commit before
any after-state measurement". A green-after receipt is produced *by* the after-state measurement; it
cannot commit before it. The round's own history shows this:

```
6d8c52a6  round-63: freeze contract; …          (counter, base-c1, control-marker-fixture, control-junk-fixture)
05b0d7f4  round-63: bind quote-class tool …     (measured commit)
7f77d12b  round-63: green-after receipts at measured commit 05b0d7f4   (parent = 05b0d7f4)
```

`git log --diff-filter=A` confirms `base-c1.txt`, `control-marker-fixture.txt`,
`control-junk-fixture.txt` were added in `6d8c52a6` (pre-measurement) and `after-c1.txt` in
`7f77d12b` (post-measurement, parent = measured). Read literally, the criterion condemns the round it
was written for. Fix: split red-before (pre) from green-after (post, at the measured revision).

### F3 — "its do-nothing and junk controls" names no locatable artifact

`.ufo/waves/round-63/controls/` contains exactly six files: `after-c1.txt`, `after-c2.txt`,
`base-c1.txt`, `base-c2.txt`, `control-junk-fixture.txt`, `control-marker-fixture.txt`. No receipt is
labelled "do-nothing". The wave's seat text uses "do-nothing" as a synonym for the base run
(`w1-spec.json` seat `ExecDoNothingControl`: "verify that at base 13d45198… both counters print
met=false"), and the contract §C1 labels that receipt "base → `met=false`, exit 1". A reader holding
only `QUALITY.md` cannot locate the control the criterion declares mandatory. Same for "junk"
(one receipt, `control-junk-fixture.txt`, covers three fixtures per `ExecJunkControl`).

### F4 — Grounding citation "(round-60 rule)" is unlocatable and does not state the cited rule

There is no `round-60` section in `corpus/QUALITY.md` that states a sha/receipt/control
commit-before-measurement order. The nearest round-60 bullet is `QUALITY.md:1404-1408`
("Mutation-surviving counter fixtures are carried as criteria…"; "a round that changes a frozen
counter's predicate freezes the fix") — it grounds the *predicate re-freeze* half of the parenthetical,
not the freeze order. The freeze order actually lives in `.ufo/waves/round-63/contract.md` §C1
("All receipts below commit before any after-state measurement"), which the criterion does not cite.
The two other citations are correct (§4 C2–C3).

### F5 — "the retained blobs' own sha256 digests" overclaims what the check establishes

`c63_calibration.py:132-143` compares `row["rawSha256"]/["textSha256"]` against `sha256()` of the two
blobs read **at the same revision**, then re-derives the class. Nothing anchors the digests outside the
ledger, so the check proves *ledger ↔ blob consistency*, not that the blobs are the retained Fetch
body. Demonstrated: a scratch tree with a one-line fabricated "raw" HTML (quote absent), a text blob
holding the quote, a ledger recording those two digests, plus marker text in knowledge/QUALITY/lesson/
SOURCES, prints:

```
revision=99ea2263fd7916460f9dde944ce2ed7de33f65bd disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
```

That is outside the round's committed junk control (which tests *mismatched* digests and blobs-absent
variants, `control-junk-fixture.txt`: `quote_correction=0`). The criterion's word "retained" should
either be narrowed to "the two blobs committed at the measured revision" or backed by an external pin
(e.g. the digest the source registry or round-61 retained-body receipt records).

### F6 — "a counter never gates on the tool" is an absolute that would ban legitimate designs

The separability rationale is C1-vs-C2 in *this* round, but the sentence is fleet-wide. Counters whose
measured subject *is* a tool exist as precedent, e.g. `.ufo/waves/round-42/c42_count.py`:
`TOOL_PATH = "scripts/sitemap_audit.py"` (`:57`), read at `:522,:530` and executed in the sandbox
harness at `:413-416`. Read globally, the clause condemns such counters. Scope it: "this round's C1
counter never gates on that tool".

### F7 — Mechanism hardcoding risks banning legitimate alternative bindings

"checked against the retained blobs' **own sha256 digests**" and "Every component of `resolved`
**re-derives from committed bytes**" are mechanism/breadth constraints, not the intended property
(bind the evidence, not markers). A future counter that binds a correction by git blob OID, by a
normalized-text digest, or by a single canonical blob would fail the text while satisfying its intent;
a calibration counter over externally fetched evidence would fail "committed bytes". Suggested:
state the property (digest-pinned committed evidence re-derived at the measured revision) and name
sha256-of-two-blobs as the round-63 instance.

### F8 — Headline ("semantic evidence, not marker strings") is not what three of the four components do

`c63_calibration.py`: `correction` is three substring tests (`:121-125`, `"[r63-correction"`,
`FROZEN_QUOTE`, `LEDGER_REL`); `criterion` is substring presence of `"substantive"`,
`"round-61-verifier-spotcheck"` and three terms (`:148-150`); `lesson_gate` is five substring tests
(`:153-159`); `source_row` is a row regex (`:162`). Only `quote_correction` (`:145`) binds blobs by
digest + re-derived class. The enumeration half of the criterion ("a criterion check names the located
proposition; a lesson-gate check records the outside verdict it claims") describes this honestly, but
the umbrella sentence "Every component of `resolved` re-derives from committed bytes" and the headline
"not marker strings" do not. A strict reader can therefore turn the criterion against the round's own
counter — the criterion is falsifiable in the wrong direction. Fix: state per-component evidence and
say explicitly that presence checks against committed files are acceptable for the criterion,
lesson-gate and registry-row components.

Observation O1 (counter weakness, not a criterion defect; for the C1 assessors): `names_purpose` scans
the whole 1416-line file (`:149`, `all(term in quality …)`), not the round-62 criterion block. At the
measured commit `destination` occurs only at `QUALITY.md:1412`, and line 1412 contains all five
markers (`X-Content-Type-Options`, `Content-Type`, `destination`, `substantive`,
`round-61-verifier-spotcheck`; verified term-by-term), so the check is currently sound but unscoped.
Observation O2 (same class): `disagreements` is a substring count; `unresolved` is set to 0 whenever
`resolved` is true (`:164-165`), so `unresolved=0` carries no independent information.

### F9 — Falsifier polarity: it states the round's pass condition, not an instance that fails the rule

Elsewhere in the same file the form is "Falsifier: <command/observation>. Example that fails it:
<concrete artifact>" (e.g. `QUALITY.md:1360-1408`). Here the falsifier ends with "must print
`met=false`", i.e. the C1 counter's acceptance, and no "example that fails it" clause is given. The
c62 green *is* that example and should be labelled as such; without it the bullet reads as a
one-round acceptance check rather than a standing bar.

## 4. What is correct (confirmation, with evidence)

- **C1 append-only.** `git diff 13d45198 05b0d7f4 -- corpus/QUALITY.md` = four added lines at EOF,
  no changed/deleted base line.
- **C2 grounding receipt resolves and says what is claimed.**
  `.ufo/waves/round-62/controls/counter-false-green-l1.txt` exists at the measured commit; it records
  the marker-only fixture, the c62 output `disagreements=1 unresolved=0 quote_correction=1 criterion=1
  lesson_gate=1 source_row=1 met=true`, exit 0, and states the route to repair. Matches the criterion's
  "routed defect 1" description.
- **C3 lesson grounding resolves.** `git show 05b0d7f4:corpus/lessons/round-63.md` has `## Mistakes` at
  line 18 and its first row is "false-green (marker-only counter predicate)" citing the same receipt and
  naming the routed defect.
- **C5 tool claim true.** `python3 -B scripts/quote_class.py --selftest` → four `pass` lines
  (`inline_raw_substring`, `markup_collapsed_only`, `absent_everywhere`, `s432_real`),
  `selftest 4/4`, exit 0; `quote_class.py classify` on the ledger's quote over
  `.ufo/waves/round-61/sources/S432.html` + `.ufo/waves/round-63/quote-class/S432.txt` →
  `derived=collapsed-only`, exit 0. The parenthetical "derives the same class" holds.
- **C6 "family defect documented, not repaired in place" true.** c62 sha at measured is still
  `ba7b77…`; on the reconstructed marker fixture it prints `met=true`, exit 0, while c63 prints
  `met=false`, exit 1.
- **Contract consistency.** The contract's C1 component semantics and the criterion's prose agree on
  what `quote_correction`, `criterion`, `lesson_gate`, `source_row` require (contract §C1 vs
  `QUALITY.md:1416`); only the criterion's freeze order (F2) departs from the committed history.

## 5. Executed falsifier evidence (reconstructed fixture)

```
$ D=/fast/scratch/hyaku/kake-r63/ScribeQualityCriterion/fx
$ cp -a .ufo/waves/round-62/controls/false-green-fixture "$D" && cd "$D" && git init -q
$ git -c user.name=fixture -c user.email=fixture@invalid add -A
$ git -c user.name=fixture -c user.email=fixture@invalid commit -q -m marker-only
toplevel=/fast/scratch/hyaku/kake-r63/ScribeQualityCriterion/fx
rev=395d066702e080666758659b8ae5dc98998da368

$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root "$D" --revision 395d0667…
revision=395d066702e080666758659b8ae5dc98998da368 disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1

$ python3 -B .ufo/waves/round-62/c62_calibration.py --root "$D" --revision 395d0667…
revision=395d066702e080666758659b8ae5dc98998da368 disagreements=1 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true
exit=0
```

Both lines match the polarity the criterion asserts, once the fixture is a standalone repo.

## 6. Exact wording fixes (suggestions only — file not edited)

Replace fragments in `corpus/QUALITY.md:1416` as follows.

1. Freeze order (F2):
   - old: `its sha256, its red-before/green-after receipts, and its do-nothing and junk controls commit before any after-state measurement;`
   - new: `its sha256, its red-before receipt and its base (do-nothing) and adversarial-junk controls commit before the after-state measurement; the green-after receipt is committed at the measured revision and records that run;`
2. Predicate re-freeze citation (F4):
   - old: `and a counter that changes predicate is itself frozen anew (round-60 rule).`
   - new: `and a counter that changes its predicate is frozen anew (round-60 criteria, "Mutation-surviving counter fixtures…"); the freeze order is `.ufo/waves/round-63/contract.md` §C1.`
3. Tool-gating scope (F6):
   - old: `a counter never gates on the tool, keeping claims separable`
   - new: `this round's C1 counter never gates on that tool, keeping C1 and C2 separable`
4. Evidence wording (F5, F7):
   - old: `a quote correction is checked against the retained blobs' own sha256 digests and a match class re-derived from those blobs`
   - new: `the quote-correction component is checked against the two blobs committed for that span (digests recorded in a committed class ledger and re-derived at the measured revision) and re-derives the span's match class from those blobs`
   - optional provenance strengthening, to be added right after if "retained" is the intent: `the recorded digests must also equal the digest the source registry pins for that body; a ledger that only cites the blobs committed beside it binds consistency, not provenance.`
5. Umbrella sentence (F8):
   - old: `Every component of `resolved` re-derives from committed bytes at the measured revision:`
   - new: `Each component of `resolved` is derived from committed bytes at the measured revision — the quote-correction component by re-derivation as below; the criterion, lesson-gate and registry-row components by reading the committed files and naming what they claim:`
6. Falsifier (F1, F9):
   - old: `Falsifier: `python3 -B .ufo/waves/round-63/c63_calibration.py --root <fixture> --revision <fixture rev>` over the round-62 marker-only fixture must print `met=false`; the old c62 counter on the same fixture prints `met=true` (family defect documented, not repaired in place).`
   - new: `Falsifier: reconstruct the round-62 marker-only fixture as a standalone repo (`cp -a .ufo/waves/round-62/controls/false-green-fixture/corpus "$D/"`, `git -C "$D" init -q`, commit, `REV=$(git -C "$D" rev-parse HEAD)`; `git -C "$D" rev-parse --show-toplevel` must print `$D`), then run `python3 -B .ufo/waves/round-63/c63_calibration.py --root "$D" --revision "$REV"`. Any counter printing `met=true` (exit 0) on that fixture fails this criterion. Example that fails it: the old c62 counter prints `met=true` (exit 0) — family defect documented, not repaired in place; `c63_calibration.py` prints `met=false` (exit 1). The committed fixture directory is not itself a fixture repo: `--root .ufo/waves/round-62/controls/false-green-fixture` resolves to the enclosing checkout and measures that checkout's bytes.`

## 7. Touched surfaces and cleanup

- Wrote: this report only
  (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/w1/ScribeQualityCriterion.md`).
- Read-only: fleet repo git objects, `corpus/QUALITY.md`, `.ufo/waves/round-6{2,3}/*`,
  `scripts/quote_class.py`, `.ufo/waves/round-42/c42_count.py`.
- Scratch (deleted after the runs): `/fast/scratch/hyaku/kake-r63/ScribeQualityCriterion/`
  (fixtures `fx` rev `395d0667…`, `fab` rev `99ea2263…`, each its own repo with a throwaway
  `user.name=fixture` identity, toplevel asserted before the first commit) and
  `/fast/scratch/hyaku/q63.md` (a byte copy of the measured `QUALITY.md`).
- No commits, no pushes, no git/jj mutations outside the two throwaway scratch repos. No pacman.
  No tool installs were needed.

## 8. Out of scope / not claimed

- I did not judge C1's calibration credit, C2's operability, or the S432 semantic admission; sibling
  seats own those. F5's fabricated-tree run is a limitation of the criterion's wording as *evidence*,
  not a claim that the round's committed ledger is fabricated (its digests re-derive from the retained
  blobs at the measured revision, per `after-c1.txt` and O1).
- The suggested wordings are proposals; the criterion was left byte-identical
  (`cec4e6b7…`, verified after all reads).
