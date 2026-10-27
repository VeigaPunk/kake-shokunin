# ScribeMistakeRow — round 62 · required `## Mistakes` row (class / evidence / captured-by / fix)

Seat: `ScribeMistakeRow` (advisory leaf, no dispatch). Base `c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13`.
Item: assess the required `## Mistakes` row for `corpus/lessons/round-62.md` against the round-61 verifier
disagreement and the frozen counter, and propose evidence-grounded wording only.

**Non-actions, attested.** No edit to the contract, the counter, the knowledge entry, `QUALITY.md`,
`SOURCES.md`, the verifier spot-check, any lesson file or any score; no git/jj command that mutates lane,
fleet, index or worktree; no counter change; no claim change. The one command that touched lane bytes was a
read-only counter run (`git show` inside the counter) whose output is quoted below. No file outside this
report path was written; scratch `/fast/scratch/hyaku/kake-r62/ScribeMistakeRow/` was created empty and
removed before yield.

## 1. Axes this seat could move

1. **row-class fidelity** — use a class token the lane already uses, or justify a descriptive one.
2. **evidence provenance** — every cell fact bound to a revision, a line and a digest.
3. **captured-by accuracy** — name the reader that actually caught it, and say whether any lane mechanism could have.
4. **fix traceability** — the fix cell names the artefact and the frozen literal that measures it, not an intention.
5. **harm avoidance** — the row must not upgrade an unmeasured after-state, must not flip the verifier row,
   must not call the landed span a raw substring, must not claim `unresolved` is independently counted.

## 2. Ground facts (commands and outputs, verbatim)

### 2.1 Frozen counter at base (read-only; reproduces the recorded control)

```
$ python3 -B .ufo/waves/round-62/c62_calibration.py --root . --revision c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13
revision=c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13 disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false
exit=1
```

`sha256sum .ufo/waves/round-62/c62_calibration.py` → `ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d`
(matches the seat brief). `corpus/lessons/round-62.md` does not exist at base (`ls` → "No such file or directory"),
which is why `lesson_gate=0`.

Counter conditions (`.ufo/waves/round-62/c62_calibration.py`):

| line | code | literal the after-state must carry |
|---|---|---|
| 16 | `QUOTE = …` | `response header can be used to require checking of a response’s Content-Type header against the destination of a request` (120 chars, 19 units, U+2019 at offset 61) |
| 17 | `CRITERION = "substantive located quote"` | `QUALITY.md` |
| 31–32 | `disagreements = sum("S432" in line and "Disagree" in line …)` | counts **lines** of the spot-check file carrying both tokens |
| 33–34 | `correction = int(QUOTE in knowledge and "S432 §3.6" in knowledge and "Round-62 correction" in knowledge)` | entry must contain all three |
| 35 | `criterion = int(CRITERION in quality and "round-61-verifier-spotcheck.md" in quality)` | `QUALITY.md` must contain both |
| 36–37 | `lesson_gate = int("## Gate" in lesson and "S432" in lesson and "Agree" in lesson and "Reject" in lesson)` | `round-62.md` must contain all four |
| 38 | `source_row = int("\| S432 \|" in sources)` | registry row stays |
| 39–41 | `resolved = correction == 1 and criterion == 1 and lesson_gate == 1 and source_row == 1`; `unresolved = disagreements if not resolved else 0`; `met = unresolved == 0 and resolved` | — |

### 2.2 The verifier disagreement (round 61, non-author closure)

`corpus/lessons/round-61-verifier-spotcheck.md`, blob at base sha256
`b4faa46bb618399b02d8dc52e14a7f785bb87c17697737f5a92c92621203d013`:

- `:3` `author: hyaku closure (non-author integrator, @m_opus)`.
- `:33` the closure's only `Disagree` row (`grep -c 'S432.*Disagree'` → `1`):
  `| S432 / Fetch | Admit | https://fetch.spec.whatwg.org/, §3.6; retained body `.ufo/waves/round-61/sources/S432.html` | Disagree | “Web developers and conformance checkers must use the following” is only a generic lead-in, not substantive evidence for a response-header expectation. Lesson itself identifies it as a generic lead-in. |`
- `:36` "The S432 disagreement leaves discernment **harmed**: an admitted row's quote does not ground its
  teaching. The lane has not yet learned this finding into a criterion."
- `:41` quality **harmed**; `:42` discernment **harmed**; `:46` routed defect: "fix S432 via a substantive
  located excerpt and an append-only correction/new row; add a grounded QUALITY.md criterion citing this
  lesson. Keep routed until landed."

### 2.3 The admitted entry (pre-state)

`corpus/knowledge/response-header-expectations.md`, blob at base sha256
`3f469deef0b14f596683c2d9fdd753687cb3c5c4a7c59b04cf5ba7dbbea7e1dd`, 216 lines:

- `:77` `> "can be used to require checking of a"` — a fragment that stops before the sentence's object.
- `:79` `> "Web developers and conformance checkers must use the following"` — the span the verifier rejected;
  9 whitespace units.
- `:6` scope already bounds the entry to the six declared classes and says "nothing here says any particular
  site serves or should serve a given field"; `:69–90` is the `xcto_nosniff_value` section carrying those quotes.
- `:202–216` `## Limits` is the file's last section, so an append at end of file keeps the base text a prefix
  (see 2.6).

### 2.4 The retained body (S432)

`.ufo/waves/round-61/sources/S432.html`, sha256
`63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b`, **1,854,393 bytes**:

| line | content |
|---|---|
| 6149 | `<h3 … data-level="3.6" id="x-content-type-options-header">` — §3.6 heading |
| 6150 | `<p>The` |
| 6151–6154 | the substantive sentence (contract's "body lines 6151–6154"): `X-Content-Type-Options` … `response` *header* `can be used to require checking of a` *response's* `` `Content-Type` `` *header* `against the` *destination* `of a` *request* `.` |
| 6156 | `</p>` (paragraph span 6150–6156) |
| 6183 | `<p>Web developers and conformance checkers must use the following` … `value` `ABNF` `for` … — the verifier-rejected lead-in |
| 6187 | `<pre><code class="highlight lang-abnf">X-Content-Type-Options = "nosniff" ; case-insensitive` — what the lead-in actually introduces |
| 6190 | `<h4 … data-level="3.6.1" …>` — next section, so the lead-in is inside §3.6 |

So the verifier's class claim is factually right: the span at 6183 introduces the ABNF value grammar, not the
field's function; the field's function is the 6150–6156 sentence.

### 2.5 Quote-class derivation for the counter's `QUOTE` (round-50 rule)

`QUALITY.md:1100–1108` requires a quoted span's class to be derived from its own blobs, `raw-substring` versus
`collapsed-only`, to stay distinct. Measured on the retained body:

```
$ python3 -B …   # strip script/style, strip <[^>]+>, html.unescape, collapse whitespace
bytes 1854393 sha256 63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b
raw_substring(Q): False
plain_collapse Q_in= False
collapse_no_backticks Q_in= True
  ctx: '6. X-Content-Type-Options header The X-Content-Type-Options response header can be used to require checking of a response’s Content-Type header against the destination of a request. To determine nosniff, given '
```

The sentence exists only after **three** transformations: remove inline `<a>`/`<code>`/`<dfn>` elements,
delete the literal Bikeshed backticks the page prints around `` `X-Content-Type-Options` `` and
`` `Content-Type` ``, and collapse whitespace. Under the r50 classes it is **neither** `raw-substring`
**nor** `collapsed-only`; it is a fourth class the lane has not named (call it "collapsed after markup
removal"). `against the destination of a` has raw count 0; `destination</a> of a` splits it. No ASCII-apostrophe
variant occurs in the body either.

### 2.6 Adjacent live rules the landing touches

- `QUALITY.md:1160–1164` (round-55): "every quoted span in a new entry is at most 25 units …, **a raw
  substring of the retained body**". The counter's `QUOTE` is 19 units (ceiling satisfied) but is **not** a raw
  substring (ceiling is satisfiable, raw-substring is not, for this exact sentence).
- `QUALITY.md:1379–1384` (round-60): an in-file correction opens its run with a visible
  `[rNN-correction YYYY-MM-DD]` tag → `[r62-correction 2026-10-27]`, and `scripts/append_guard.py` must exit 0.
- `.ufo/waves/round-55/c55_readme_index.py:30` `head_changed … full base text is not preserved byte-for-byte as
  a prefix`; its selftest case `pass_entry_appended_correction` (`:330`) expects `head_changed: 0`. Appending
  after `## Limits` keeps it green; an insertion at `:69–90` would turn it red (the round-59 failure mode,
  `QUALITY.md:1350–1358`).
- `corpus/QUALITY.md` has 1,408 lines and its last section heading is `## Round-60 criteria` (`:1360`); there is
  **no** round-61 criteria section, which is the same fact the verifier recorded as "the lane has not yet
  learned this finding into a criterion".

### 2.7 No lane reader could have caught it

```
$ grep -n "corpus/knowledge" .ufo/waves/round-61/c61_header_cases.py .ufo/waves/round-61/c61_recheck_pins.py
(no output)
```

`c61_header_cases.py` scores header-audit behaviour (H1–H18, R3 shape, R4 do-nothing) against a manifest and a
tool; `c61_recheck_pins.py` (docstring `:13`) reads the registry under `## Registry` and the round-61 lesson's
Gate lines. Neither opens a knowledge entry, so neither can compare a quote with the claim it is filed under.

## 3. Proposed row (paste-ready)

Land this as a row of `corpus/lessons/round-62.md` `## Mistakes`, table header
`| Class | Evidence | Captured-by | Fix |` (the form every round 55–61 lesson uses).

```markdown
| vacuous | An admitted S432 row's quote is a generic lead-in, and no counter read it as support. `corpus/lessons/round-61-verifier-spotcheck.md:33` — the closure's only `Disagree` row (`grep -c 'S432.*Disagree'` → 1 at `c341a7a`) — records S432 / Fetch as `Admit` but `Disagree`: “Web developers and conformance checkers must use the following” is only a generic lead-in, not substantive evidence for a response-header expectation; lines 36 and 41–42 read the result as discernment and quality harm. The admitted entry carries that span at `corpus/knowledge/response-header-expectations.md:79` and the object-less fragment at `:77` (“can be used to require checking of a”), while the retained body places the lead-in at line 6183, where it introduces only the ABNF value block at 6187, and states the field's job in the §3.6 paragraph at 6150–6156 (contract's body lines 6151–6154). Blobs at base: spot-check `b4faa46bb618399b02d8dc52e14a7f785bb87c17697737f5a92c92621203d013`, entry `3f469deef0b14f596683c2d9fdd753687cb3c5c4a7c59b04cf5ba7dbbea7e1dd`, retained body `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b` (1,854,393 bytes). Frozen counter at base: `disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false`, exit 1. | `none` in-lane: round-61's C2 counter `c61_header_cases.py` scores header-audit behaviour H1–H18 and reads no quoted span, `c61_recheck_pins.py` reads registry rows and Gate lines, and neither opens `corpus/knowledge/` (grep, no hit) — no lane mechanism compares a quote with the claim it is filed under. Caught by the round-61 non-author closure's discernment spot-check (§Discernment, line 33). | Append-only landing, measured by the frozen counter only: `corpus/knowledge/response-header-expectations.md` gains a `[r62-correction 2026-10-27]` run after `## Limits` that quotes the §3.6 sentence verbatim (19 units, 120 chars — the counter's `QUOTE` literal, U+2019 included) and says the line-6183 lead-in introduces the ABNF block, not the field's job; `corpus/QUALITY.md` gains a criterion that a located quote must substantively support the claim it is filed under, citing `corpus/lessons/round-61-verifier-spotcheck.md`; `corpus/lessons/round-62.md` §Gate re-reads S432 with an explicit `Agree` or `Reject`; the S432 registry row (`corpus/SOURCES.md:178`, `used-by` cell unchanged) and the verifier's `Disagree` row stay as they are. `python3 -B .ufo/waves/round-62/c62_calibration.py --root . --revision <after>` (sha256 `ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d`) is the measurer; base `met=false` exit 1, the after-state is unmeasured until integration. Limits the fix must carry: the landed span is a collapsed-only reconstruction across inline markup and Bikeshed backticks, never called a raw substring; the verifier row is kept, not flipped; the counter's `unresolved=0` is derived from `resolved` and is not an independent count of unresolved disagreements. |
```

### 3.1 Cell-by-cell grounding, and what each cell must **not** say

| Cell | Grounded on | Must not say |
|---|---|---|
| **Class** `vacuous` | lane token used in rounds 55, 56, 57, 58 for "the thing was met/admitted without the work"; here the work is support, and the verifier's own phrase is "does not ground its teaching" (`:36`) | not `attribution` — the span *is* at the cited locator and inside §3.6 (6183 < 6190), so the failure is support, not placement; not `reference-drift` — the line numbers and blob are correct; not `stale-premise` — the body has not moved since the 2026-10-27 open |
| **Evidence** | §2.2–§2.4: line 33 verbatim, the two entry spans, the retained-body lines, three blob digests, counter base line | must not call the entry's span "unsupported by the page" (the page prints it), nor claim the §3.6 sentence is missing (it is at 6150–6156), nor present the counter's `QUOTE` as a raw substring |
| **Captured-by** | §2.7 grep (no hit) + `c61_header_cases.py` H1–H18 scope + `c61_recheck_pins.py:13` docstring | must not credit a lane gate with the catch; the round-61 C2 counter was green (18/18 per `round-61-verifier-spotcheck.md:16`) and could not see this class |
| **Fix** | counter literals §2.1; append-only constraints §2.6; routed defect `:46`; contract C1 sentence | must not assert a green after-state (unmeasured), must not describe the verifier row as superseded/flipped, must not claim calibration credit or a score move, must not claim the random `unresolved` metric proves all disagreements resolved |

### 3.2 Rejected alternatives (short)

- **Class `attribution`** — rejected: `round-61-verifier-spotcheck.md:33` names the right page and §3.6, and the
  lead-in exists there; nothing is misattributed (contrast round-57 `attribution`, QUALITY.md:1233–1239, where a
  reason misstated what the page prints).
- **Class descriptive-only** (`"Admitted quote is a generic lead-in"`, the round-53/54 style) — admissible, but
  every round since 55 uses a token; keeping `vacuous` first and the descriptor inside the Evidence cell keeps
  the table filterable while staying accurate.
- **Evidence that cites the after-artefacts** — rejected: the entry correction, the QUALITY criterion and the
  round-62 lesson do not exist at the base, so citing them as evidence would be a contract-only seat upgraded to
  execution evidence. They belong in **Fix** (intent + measurer), not **Evidence**.
- **A row that calls the S432 registry row defective** — rejected: `corpus/SOURCES.md:178` describes the value
  rule (`nosniff`, ASCII case-insensitive), which the §3.6 algorithm supports; the defect is the entry's quoted
  support, and the contract keeps the row.

## 4. Constraints and hazards the row's Fix must encode (measured, not inferred)

1. **`QUOTE` is not a raw substring** (§2.5). The correction is honest only if it tags the span as a
   reconstruction across inline markup; the round-55 raw-substring rule (QUALITY.md:1160–1164) is *not* met by
   this landing, and the new criterion must not be described as satisfying it. This is a conflict between a
   live rule and the frozen literal, reported here for the canonical judge; I change neither.
2. **U+2019 is required.** The apostrophe in `response’s` is U+2019 at offset 61 of the literal; an ASCII
   apostrophe fails `correction` (0). Measured: ASCII variant absent from the body too.
3. **Append after `## Limits`, not inside `xcto_nosniff_value`.** The base text must stay a byte prefix
   (`c55_readme_index.py:30`, selftest `:330`), and the run must open with `[r62-correction 2026-10-27]`
   (QUALITY.md:1379–1384) while also containing the literal `Round-62 correction` (counter line 34).
4. **Do not append a second `S432 … Disagree` line to the spot-check file.** `disagreements` counts lines
   (counter 31–32) and `unresolved` is overwritten to 0 once `resolved` (39–40), so a second real disagreement
   would be hidden, not reported. The row's Evidence must not present `unresolved=0` as an independent count.
5. **`## Gate` needs all four tokens** (`## Gate`, `S432`, `Agree`, `Reject`, counter 36–37); a Gate that only
   says the correction landed satisfies none of them. Note the round-61 lesson's Gate line for S432 (`:43`)
   carries "9 units" and the rejected span; the round-62 Gate line is where the re-read decision goes.

## 5. For the canonical judge — verbatim conflict lines

- Verifier, `corpus/lessons/round-61-verifier-spotcheck.md:33`:
  `| S432 / Fetch | Admit | https://fetch.spec.whatwg.org/, §3.6; retained body `.ufo/waves/round-61/sources/S432.html` | Disagree | “Web developers and conformance checkers must use the following” is only a generic lead-in, not substantive evidence for a response-header expectation. Lesson itself identifies it as a generic lead-in. |`
- Verifier, `:36`: "The S432 disagreement leaves discernment **harmed**: an admitted row's quote does not ground its teaching. The lane has not yet learned this finding into a criterion."
- Contract C1: "append a correction to `corpus/knowledge/response-header-expectations.md` with a substantive
  quote in S432 §3.6 and explain its support; append a QUALITY.md criterion that located quotes must
  substantively support their associated claims, citing the verifier finding. Preserve the old knowledge
  prose, source row, and verifier record; append only."
- Conflict: `QUALITY.md:1160–1164` requires "a raw substring of the retained body" for every quoted span in a
  new entry; the frozen counter's `QUOTE` line 16 is not a raw substring of
  `.ufo/waves/round-61/sources/S432.html` (measured, §2.5). Satisfying the counter's literal and satisfying the
  r55 raw-substring rule are mutually exclusive for this sentence.

## 6. Limits of this report

- The row's **Fix** half cannot be measured now: no after-state exists at `c341a7a` and the contract measures
  the after-state only after integration. Every after-side statement above is a requirement or an inference,
  not a result.
- Line numbers are the base blobs' line numbers; a later commit that prepends to a file would move them.
- `[INFERENCE]` marks: the claim that the round-62 Gate can satisfy `lesson_gate` while keeping the verifier
  row (the counter's token test makes it possible; the *content* that justifies `Agree`/`Reject` is the
  round-62 Gate seat's to write, not mine).
