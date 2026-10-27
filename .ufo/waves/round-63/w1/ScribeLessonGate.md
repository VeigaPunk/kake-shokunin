# ScribeLessonGate — round-63 lesson vs CORPUS.md / LEARNING.md

Seat: ScribeLessonGate (scribe, leaf; no subagent dispatch, no commits, no mutations).
Item: review `corpus/lessons/round-63.md` against the fleet corpus contract
(`/home/vgpnk/Projects/shokunin/CORPUS.md`) and learning path
(`/home/vgpnk/Projects/shokunin/LEARNING.md`): Mistakes table shape, Gate
completeness, census record. Read-only; this file is the only write.

## Behavior

Reviewed the committed round-63 lesson at measured commit
`05b0d7f4b4a23513390f7b92547e2b0f1fccb06f` (added in `6d8c52a6`; working tree
clean for the file: `git status --porcelain -- corpus/lessons/round-63.md`
printed nothing). Cross-checked every evidence pointer the lesson makes against
the committed bytes. No product, counter, contract, receipt, registry or state
file was edited; nothing was committed.

Lesson line map used below:
`18` `## Mistakes`, `20` table header, `22` row; `24` `## Gate`, `26`
candidates, `32` Admit (a), `40` Reject (b), `43` Reject (c), `49`
Assimilation, `53` rule-1 record, `56-58` located quote, `58` "No registry row
added or changed", `61-66` outside verdict, `67` `## Sources census`, `69`
round-start census.

## Gates

Contract rules applied:
- `CORPUS.md:171-177` — `## Mistakes`, one row per mistake:
  class · evidence · captured-by · fix; **classes come from the `mistakes.md`
  §5 vocabulary** (`vacuous`, `survivor`, `stale-premise`, `reference-drift`,
  `number-drift`, `scope`, `attribution`, `landing`, `provider`).
- `CORPUS.md:179-184` — a fix must ship a committed red-before state.
- `CORPUS.md:34-38` — a count carries its command.
- `CORPUS.md:39-41` — a negative claim carries its sweep.
- `CORPUS.md:42-44` — a quote names its location.
- `CORPUS.md:102` — a rejection reads `REJECTED: <reason>; flip: <what would
  change the verdict>` (SOURCES registry rows; applied here as the Gate-reject
  shape the seat was asked to check).
- `LEARNING.md:19-20` — a mistake with no capturing criterion adds a
  `QUALITY.md` criterion citing the lesson.
- `LEARNING.md:42-46` — each round's non-author spot-check covers at least one
  admit and one reject of *that round's* decisions and is recorded in the
  round lesson.
- `LEARNING.md:69-71` — `## Gate` = candidates, admitted, rejected (with
  reasons), spot-check result.

## Findings

### D1 — DEFECT (contract): Mistakes class is outside the frozen vocabulary

`corpus/lessons/round-63.md:22` states the class as
`false-green (marker-only counter predicate)`. `CORPUS.md:173-176` fixes the
allowed classes to the `mistakes.md` §5 vocabulary and that list contains no
`false-green` (confirmed verbatim at
`/home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w1/mistakes.md:447-449`). The
round-62 precedent row for the same defect family uses `vacuous`
(`corpus/lessons/round-62.md:9`), and `mistakes.md` §5 C04 groups
"cannot fail / inert / negative control" under `vacuous`. Consequence: the row
does not sort against the fleet taxonomy. Fix would be to class the row
`vacuous` (the parenthetical can stay).

### D2 — DEFECT (count/command): "171 rows" is attributed to a command that does not print it

`corpus/lessons/round-63.md:69` writes:
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake
→ 171 rows, 16 W04 cross-scope duplicate-URL warnings, exit 0`.

I ran exactly that command from `/home/vgpnk/Projects/shokunin`:

```
bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake
exit=0, 17 output lines, 16 lines matching W04, final line
`kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`
```

The command emits no row count. The 171 is produced by the contract's census
grep (`CORPUS.md` census block):

```
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md   # 171 (lane root)
```

So the W04 count (16) and exit 0 are correct for the named command; the row
count is not. `CORPUS.md:34-38` requires the number to carry the command that
yields it. (Round-62 has the same shape at `corpus/lessons/round-62.md`
"Sources census"; precedent does not make it conformant.)

### D3 — DEFECT (negative claim without sweep)

Two absences are asserted with no producing sweep:
- `corpus/lessons/round-63.md:58` — "No registry row added or changed; S432
  stays `mined`."
- `corpus/lessons/round-63.md:69` — "No `corpus/SOURCES.md` row was added or
  changed this round."

`CORPUS.md:39-41` requires the search/diff that produced the absence. Both
claims are true, and I verified them read-only:
`git diff --stat 13d4519..HEAD -- corpus/SOURCES.md` → empty; registry rows
`171` at base (`git show 13d4519:corpus/SOURCES.md | grep -cE ...`) → `171` at
HEAD; S432 row still `mined` (`corpus/SOURCES.md:178`). The lesson does not
carry either command.

### D4 — DEFECT (quote precision): the rule-1 "Located quote" is a de-backticked rendering not present in any committed blob

`corpus/lessons/round-63.md:56-58` prints the located quote as:

```
response header can be used to require checking of a response’s Content-Type header against the destination of a request
```

The committed span (ledger + flat-text rendering) is:

```
The `X-Content-Type-Options` response header can be used to require checking of a response’s `Content-Type` header against the destination of a request.
```

Substring tests over the committed bytes:
- lesson quote in `.ufo/waves/round-63/quote-class/S432.txt` → `False`
  (the flat text carries literal backticks around `Content-Type`; occurrence
  at offset 100629);
- ledger quote in the same file → `True`;
- lesson quote in the tag-stripped raw HTML span (lines 6150-6154) → `False`;
- ledger quote in the tag-stripped raw span → `True`.

The Gate's Admit (a) at `round-63.md:32-39` does print the span with backticks
and is byte-accurate, so the lesson contradicts itself between lines 32 and 56.
This is the exact normalization class the round's own bar excludes; the
inaccuracy is confined to the rule-1 record, and the committed ledger
(`.ufo/waves/round-63/quote-class/quote-classes.json`, quote field) is correct.

### D5 — DEFECT (low severity, flip): Reject (b) records no flip condition

`corpus/lessons/round-63.md:40-42` ends `Flip: none — superseded by (a).`
"Superseded by (a)" is not a flip: admitting a different span (a) does not
change the verdict on the fragment/lead-in, and the row names no condition
that would change that verdict. Contrast Reject (c) at
`round-63.md:43-48`, which states a falsifiable flip (repeated verifier/gate
comparisons showing the semantic counter misses a receipt-rewrite class).
`CORPUS.md:102`'s flip rule is written for SOURCES registry rows, so this is a
Gate-shape defect, not a registry violation.

### O1 — OPEN (correctly labelled, not yet satisfied): the round-63 outside spot-check is absent

`round-63.md:61-66` names the round-61 non-author verdict and labels this
round's own decisions author-side. That matches the contract's `lesson_gate`
component (contract.md C1: "record the round-61 outside verdict and label its
own assessment author-side"). However `LEARNING.md:42-46` requires the
non-author spot-check of *this round's* gate decisions in the round lesson, and
no `corpus/lessons/round-63-verifier-spotcheck.md` exists (lessons directory
listing ends at `round-62-verifier-spotcheck.md`). The lesson is honest about
the deferral; the per-round outside verdict remains open until the non-author
closure writes it. Not counted as a lesson defect; counted as an unfinished
learning-path gate at this artifact.

### O2 — OBSERVATION: the re-open quote grounds the field-purpose sentence, not S432's `teaches`

`corpus/SOURCES.md:178` gives S432 `teaches` = "The field has one defined
value, nosniff, compared ASCII case-insensitively against the split field
values…". The admitted §3.6 span states only that the header "can be used to
require checking of a response's Content-Type header against the destination of
a request" — the field's purpose, not the value rule. `CORPUS.md:112-115`
(rule 1) attaches the ≤25-word quote duty to new rows; no row was added or
changed, so the duty is not triggered — but the lesson labels the record
"(rule 1)", and a reader could infer the purpose quote grounds `teaches`. It
does not. `corpus/QUALITY.md` round-62 criterion (`QUALITY.md:1412`) explicitly
requires keeping a field's purpose separate from claims about its exact value.
The lesson's narrower wording ("the proposition the `xcto_nosniff_value`
section attributes to S432") is accurate for the purpose sentence; the
registration as rule-1 grounding is the imprecision.

### O3 — OBSERVATION: assimilation has a reason but no flip

`round-63.md:49-52` ("Assimilation: none") gives a reason and no flip. Rounds
60-62 use the same shape (`round-60.md:72`, `round-61.md:59`,
`round-62.md:25`), so this is consistent with precedent and arguably not a
scoreable candidate rejection.

### O4 — OBSERVATION: "one GET, HTTP 200" has no committed receipt

`round-63.md:53-55`. The committed live body
`.ufo/waves/round-63/sources/S432.live.html` verifies `1854393` bytes and
sha256 `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b`
(byte-identical to `.ufo/waves/round-61/sources/S432.html`). The HTTP status and
request count are not recorded as a receipt; they are falsifiable only by a
fresh fetch, which this seat did not perform.

## Confirmations (verified, no defect)

- Mistakes table shape: header `| Class | Evidence | Captured-by | Fix |`
  (`round-63.md:20`); exactly one row (`:22`); evidence pointer
  `.ufo/waves/round-62/controls/counter-false-green-l1.txt` exists and records
  `met=true, exit 0` with no source body on the marker-only fixture;
  "ReviewerCounterControls" occurs twice in `.ufo/waves/round-62/w1-results.json`.
- Captured-by `none` is an allowed value (`CORPUS.md:171-173`), and the
  LEARNING follow-up is satisfied: `corpus/QUALITY.md:1416` is the round-63
  criterion and cites `corpus/lessons/round-63.md` §Mistakes.
- Fix carries red-before evidence: `base-c1.txt` (`met=false`, exit 1),
  `control-marker-fixture.txt` (old c62 `met=true`; new c63 `met=false`),
  `control-junk-fixture.txt` (`met=false`); `after-c1.txt` (`met=true`, exit 0)
  and `after-c2.txt` exist. (Receipt contents were read; counters were not
  re-run by this seat.)
- Gate candidates: four named, (a)-(d) (`:26-31`); admit (a) carries class,
  both blob digests, recipe, ledger path and the `s432_real` selftest case
  (`scripts/quote_class.py:63`).
- Frozen digests claimed by the lesson/contract match the bytes:
  `c63_calibration.py` `bcd16f68…fc91`, `quote-classes.json`
  `5f48e26b…c42d`, `scripts/quote_class.py` `431e75e8…1f14`,
  `c63_quote_tool.py` `9fcbfad0…f01e`.
- Ledger composition: `matchClass` = `collapsed-only`; `rawSha256`
  `63b0a018…911b`; `textSha256` `8b90d096…2a69`; `locatedRawLines`
  `6150-6154`; raw lines 6150-6154 carry the sentence across inline markup.
- Rule-1 quote length: 19 words (≤25).
- Outside verdict naming: `corpus/lessons/round-61-verifier-spotcheck.md:33`
  is the S432 row, decision `Disagree`, reason "generic lead-in".
- Author-side labelling: `round-63.md:63-66` states the round's own decisions
  are lane self-assessment, author-side.
- Census components that the named command does produce: 16 W04 warnings and
  exit 0 (verified run, above); census run date 2026-10-27 present.
- The knowledge correction the Gate says grounds the entry exists:
  `corpus/knowledge/response-header-expectations.md:224` `[r63-correction
  2026-10-27]`, appended (29 added lines, `git diff --stat 13d4519..HEAD`); no
  in-place rewrite of the round-62 held correction.

## Touched surfaces

- Wrote only this file:
  `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/w1/ScribeLessonGate.md`.
- Read-only reads in `kake-shokunin/` (corpus, `.ufo/waves/round-6{1,2,3}`,
  `scripts/quote_class.py`) and `/home/vgpnk/Projects/shokunin/`
  (`CORPUS.md`, `LEARNING.md`, `scripts/sources-census.sh`,
  `.ufo/waves/kaika-w1/mistakes.md`).
- Ran one read-only census (`scripts/sources-census.sh validate`; the script's
  header states it writes only stdout or `--out`, and no `--out` was passed)
  and `git diff`/`git show`/`git status` read-only queries. No counter re-runs,
  no git/jj mutation, no fixture, no pacman, no tool install.

## Out of scope / not verified

- Did not judge C1 or C2 claim truth; only lesson-vs-contract consistency.
- Did not re-run `c63_calibration.py`, `c63_quote_tool.py` or the c62 counter;
  receipt text was read as committed evidence.
- Did not fetch `https://fetch.spec.whatwg.org/`; the HTTP-200 claim (O4) is
  unverified by artifact.
- The lesson's "round-end census output is pasted in the round report"
  (`round-63.md:69`) has no target at this artifact:
  `find .ufo/waves/round-63 -maxdepth 2 -name '*report*' -o -name '*.md'`
  returns only `contract.md`, `w1/ScoutAppendOnly.md`,
  `w1/ScoutLedgerIntegrity.md` (and this file). The round-end census is
  therefore absent, not merely deferred.
- No assessment of `merge/kake/` contents or of `considerthese/` proposal 2
  beyond checking that the lesson states a reason and (for c) a flip.

## Commands run (exact, read-only)

```
sha256sum .ufo/waves/round-63/c63_calibration.py .ufo/waves/round-63/quote-class/quote-classes.json scripts/quote_class.py .ufo/waves/round-63/c63_quote_tool.py .ufo/waves/round-63/sources/S432.live.html .ufo/waves/round-61/sources/S432.html .ufo/waves/round-63/quote-class/S432.txt
sed -n '6150,6154p' .ufo/waves/round-61/sources/S432.html
python3 - # substring test of lesson/ledger quote against S432.txt and tag-stripped raw span
bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
git diff --stat 13d4519818db28cd0aa912e49020659140d7b9fa..HEAD -- corpus/SOURCES.md
git show 13d4519818db28cd0aa912e49020659140d7b9fa:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'
```
