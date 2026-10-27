# ScribeQualityCriterion — round 62 (kake)

Seat: advisory scribe, leaf member, no subagent dispatch. Item: draft one concise
`corpus/QUALITY.md` criterion grounded in `round-61-verifier-spotcheck.md` that
distinguishes substantive evidence from a generic section lead-in, with
admit/reject behavior and a resolvable pointer.

Behavior: read-only on all lane files. No lane file, Git/jj state, frozen claim,
predicate, criteria set or score was written or altered. This report is the only
artifact written. Scratch `/fast/scratch/hyaku/kake-r62/ScribeQualityCriterion/`
was created, used, and deleted before yield (`ls /fast/scratch/hyaku/kake-r62/`
no longer lists it). No installs, no pacman, no network fetch (the S432 body was
used from the committed round-61 retain).

## Frozen inputs at HEAD

Command: `cd /home/vgpnk/Projects/shokunin/kake-shokunin && sha256sum .ufo/waves/round-62/c62_calibration.py corpus/QUALITY.md corpus/lessons/round-61-verifier-spotcheck.md corpus/knowledge/response-header-expectations.md .ufo/waves/round-61/sources/S432.html`

```
ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d  .ufo/waves/round-62/c62_calibration.py
c37bad48518210951771760924e5af6c5b0ea8fd06c19a3d2398d03757a78820  corpus/QUALITY.md
b4faa46bb618399b02d8dc52e14a7f785bb87c17697737f5a92c92621203d013  corpus/lessons/round-61-verifier-spotcheck.md
3f469deef0b14f596683c2d9fdd753687cb3c5c4a7c59b04cf5ba7dbbea7e1dd  corpus/knowledge/response-header-expectations.md
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  .ufo/waves/round-61/sources/S432.html
```

Counter digest matches the frozen `ba7b7737…78548d`. Retained body digest matches
its receipt digest in the entry front matter (`:5`) and the round-61 Gate line
(`corpus/lessons/round-61.md:43`). `git rev-parse HEAD` → `c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13`;
`git status --porcelain` → `?? .ufo/waves/round-62/` only.

## Base state for the criterion leg (scratch, read-only derived)

`corpus/QUALITY.md` is 1408 lines and contains neither `substantive located quote`
nor `round-61-verifier-spotcheck.md`, so the frozen counter's criterion expression
`CRITERION in quality and "round-61-verifier-spotcheck.md" in quality` is 0 at the
base — consistent with the orchestrator-recorded base-control line
`unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false exit 1`
(recorded, not re-run by this seat).

## Evidence for the substantive-vs-lead-in distinction

Rendering of the retained body with tags stripped, code-span backticks dropped and
whitespace collapsed (scratch `python3 -B`, no writes):

```
S36_RENDER (lines 6151-6154): The X-Content-Type-Options response header can be used to require checking of a response’s Content-Type header against the destination of a request.
QUOTE_IN_S36: True   (only after code-span backticks are dropped)
S37_RENDER (lines 6229-6236): 3.7. `Cross-Origin-Resource-Policy` header The Cross-Origin-Resource-Policy response header can be used to require checking a request’s current URL’s origin against a request’s origin when request’s mode is "no-cors".
lead_in (line 6183): Web developers and conformance checkers must use the following value ABNF for X-Content-Type-Options:
page occurrences — frozen span: 1 ; full sentence as rendered above: 1 ; lead-in: 1
units/chars — full sentence: 21 / 148 ; frozen span alone: 19 / 120 ; lead-in: 9 / 62
```

Rejected fragments in the entry, with coordinates (grep):
`corpus/knowledge/response-header-expectations.md:77` → `> "can be used to require checking of a"`;
`:79` → `> "Web developers and conformance checkers must use the following"`.
Line 6183 is the lead-in that introduces the value ABNF block; it asserts nothing
about the field's job. Lines 6151–6154 are the sentence that gives the field its
job, inside the §3.6 section whose heading is `:6149` (`data-level="3.6"`,
`id="x-content-type-options-header"`).

## Draft criterion (verbatim; append after `corpus/QUALITY.md:1408`)

Base file sha256 `c37bad48…78820`, 1408 lines, last section `## Round-60 criteria`.
Appending the block below adds 4 lines (new `## Round-62 criteria` section, one
blank line, one bullet, trailing blank line); a scratch byte-prefix check reported
`base_is_prefix = True | added_chars = 2359 | lines = 1412`.

```
## Round-62 criteria

- **A quoted span is a substantive located quote only when it states the proposition the sentence citing it attributes to the source; a heading, a section lead-in or a "use the following" transition is not evidence, however exactly it renders.** Admit a span when it is a deterministic rendering of the entry's digest-pinned retained body — tags stripped, code-span backticks dropped, whitespace collapsed — of 6..25 units and at most 160 characters, occurs once on the page, names the field or other token the sentence turns on, and is printed beside its section and retained-body line range. A span may cross inline element boundaries under that rule; "one collapsed text node" is a shape rule, not permission to quote a fragment. Reject an admitted row whose quote cannot be told apart from its own section's lead-in, and reject a purpose sentence presented as the ground of a value or syntax rule the entry also claims: each part of a two-part claim names its own located ground. Round 61 admitted two S432 fragments (`corpus/knowledge/response-header-expectations.md:77,79`); the second, "Web developers and conformance checkers must use the following" (9 units, 62 characters), is only the lead-in to the value ABNF block at `.ufo/waves/round-61/sources/S432.html:6183`, while the §3.6 sentence that gives the field its job renders from lines 6151–6154 and occurs once on the page. Grounding: `corpus/lessons/round-61-verifier-spotcheck.md:33` (S432 row, Disagree: "only a generic lead-in, not substantive evidence"), `:36,42` (discernment harmed; not yet learned into `corpus/QUALITY.md`). Complements, and does not weaken, quote truth at `corpus/QUALITY.md:375–388` and the locator rule at `:1116`. Falsifier: `git show <rev>:.ufo/waves/round-61/sources/S432.html`; lines 6151–6154 render "The X-Content-Type-Options response header can be used to require checking of a response’s Content-Type header against the destination of a request." (21 units, 148 characters, one occurrence) and line 6183 renders only "Web developers and conformance checkers must use the following value ABNF for …". Example that fails it: keeping the §3.6 heading, the lead-in quote and a "cited by location" ABNF block as one undivided grounding — the row is admitted and the quote grounds nothing, which is the round-61 disagreement left unlearned.
```

Admit/reject behavior, stated as observable cases:

| Case | Decision | Test applied |
|---|---|---|
| `S432.html:6151–6154` rendered sentence, printed with `§3.6` and its line range, attached to the field's-purpose sentence | Admit | renders deterministically from the pinned digest, 21 units / 148 chars, one page occurrence, names `X-Content-Type-Options` and `Content-Type` |
| `S432.html:6183` "…must use the following" attached to a response-header expectation | Reject | lead-in to the ABNF block; asserts no field behaviour; indistinguishable from its section's transition |
| `:77` truncated fragment "can be used to require checking of a" | Reject | rendering is a fragment, not a proposition; the sentence continues past the span |
| Purpose sentence offered as the ground of the `nosniff` literal rule | Reject | two-part claim: the purpose sentence grounds the field's job, the value grammar needs its own located ground (the §3.6 ABNF block) |
| Quote true and section-correct but attached to a different teaching | Reject | quote truth (`QUALITY.md:375–388`) and locator (`:1116`) are necessary, not sufficient |

Resolvable pointer chain (each element re-derivable from committed bytes):
`corpus/lessons/round-61-verifier-spotcheck.md:33` (Disagree row) → `:36` and `:42`
(harm and criterion gap) → `corpus/knowledge/response-header-expectations.md:75–83`
(§3.6 subsection and its two fragments) → `.ufo/waves/round-61/sources/S432.html`
(sha256 `63b0a018…bad911b`), heading `:6149`, sentence `:6151–6154`, lead-in `:6183`
→ `corpus/SOURCES.md:178` (row kept as admitted, untouched).

Scoped simulation (scratch copy only, not a counter run and not a scored state):
appending the block to a scratch copy of `QUALITY.md` gives
`criterion_leg = 1`, i.e. the frozen counter's criterion expression would read 1
at a revision carrying this text. Only that leg was simulated; no after-state of
the other legs or of the predicate is claimed.

## Findings

- **F1 — the frozen quote literal only matches after code-span backticks are
  dropped.** `c62_calibration.py:15` pins
  `…response’s Content-Type header against the destination of a request`, but the
  retained markup carries literal backticks around `<code>Content-Type</code>` and
  around `<code>X-Content-Type-Options</code>`. A naive tag-strip render contains
  the backticks, so `QUOTE_IN_S36` is `False` until they are removed. A correction
  written straight from the HTML source line will not satisfy the counter; the
  quote-fix scribe must print the backtick-stripped rendering. This is a property
  of the frozen literal, not a defect this seat may correct.
- **F2 — conflict to report verbatim for the canonical judge.** `corpus/lessons/round-61-verifier-spotcheck.md:33`
  states: "Lesson itself identifies it as a generic lead-in." The committed lesson
  `corpus/lessons/round-61.md` contains no occurrence of `generic` or `lead-in`
  (`grep -n "substanti\|generic\|lead-in" corpus/lessons/round-61.md` → no
  matches; its only S432 mention is `:43`, which quotes the lead-in as the row's
  admitted quote). The clause has partial support only in the entry's own prose at
  `corpus/knowledge/response-header-expectations.md:81–83` ("The node after the
  second span introduces the ABNF value block"), which describes the span as an
  introduction without using either word. The criterion draft therefore grounds on
  `:33` as the non-author verdict and does not adopt the "lesson itself" clause.
- **F3 — the §3.6 sentence template repeats in §3.7 with a different field.**
  `S432.html:6232` renders "…response header can be used to require checking a
  request's current URL's origin…" for `Cross-Origin-Resource-Policy`. Quoting
  only from "response header can be used to require checking…" drops the field
  name and weakens field identity against a same-page template; the full rendered
  sentence (21 units / 148 chars, page-unique) keeps the token and still contains
  the frozen literal. Recorded so a later round does not read this as noise.
- **F4 — no existing criterion covers this bar; the neighbours are complementary.**
  Quote truth `corpus/QUALITY.md:375–388` tests substring plus receipt digest;
  locator `:1116` tests that the section containing the quote is the one cited;
  attribution `:1398` tests that a span is placed where the page places it. None
  tests whether the span asserts the attached claim. The draft says so explicitly
  and claims no supersession, per the round-20 append-only ruling.
- **F5 — reviewer caveat absorbed.** `w1/ReviewerQualityCriterion.md` warns
  against claiming the §3.6 purpose sentence proves the `nosniff` value rule; the
  draft's two-part-claim reject case encodes that, and its admit case scopes the
  quote to the field-purpose sentence only.

## Gates and limits

- Not run by this seat: the frozen counter at any revision (the base-control line
  is quoted as recorded by the orchestrator, not re-executed), any census, any
  network fetch, any Git/jj mutation. The only executed code was `sha256sum`,
  `grep`/`wc` reads, `git rev-parse`/`status`/`show` reads, and scratch rendering
  of committed bytes.
- The draft is a proposal: it is not inserted, not reviewed by a non-author after
  insertion, and confers no criterion credit until a committer lands it and the
  counter is measured at the committed revision.
- Scope held to corpus/web-publishing evidence quality; no research-method claim,
  no source-row edit, no rejection of S432, no change to the frozen claim,
  predicate or score.
- `/fast/scratch/hyaku/kake-r62/ScribeQualityCriterion/` deleted; nothing written
  outside this report path.

## Recommended main-agent checks after append

1. `python3 -B scripts/append_guard.py --root . --base c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13 --revision <tip>` — the new section must read as a pure addition.
2. `python3 -B .ufo/waves/round-62/c62_calibration.py --root . --revision <tip>` — expected legs `criterion=1`, `source_row=1`, plus the quote-fix and lesson legs from the sibling seats; this seat claims only the criterion leg's substring test in scratch.
3. Read the landed bullet once against `corpus/lessons/round-61-verifier-spotcheck.md:33,36,42` and `corpus/QUALITY.md:375–388,1116` to confirm the complement wording survived the merge.
