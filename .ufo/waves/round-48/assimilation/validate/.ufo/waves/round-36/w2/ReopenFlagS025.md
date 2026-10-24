# S025 re-opened by hand — verdict: tool miss (extraction), not drift

Seat KakeR36.ReopenFlagS025; lane rev f3a38bf8e68f6cee386125d34b5e95ac9b2df66e (sandbox clone only).
Item: the real-input run reported `quote_missing` for S025.

## Input and row
- `.ufo/waves/round-36/realrun/input.json` index 22: url
  `https://html.spec.whatwg.org/multipage/scripting.html#the-template-element`, quote
  "The template contents of a template element are not children of the element itself.",
  from `round-22.md`. Row: `corpus/SOURCES.md:33` (spec, grade A, 90d).

## Fetches (GET only, sandbox `/fast/scratch/hyaku/kake-r36w2/ReopenFlagS025/`)
```
curl -sS --max-time 60 -D headers-noredir.txt https://html.spec.whatwg.org/multipage/scripting.html            # exit 0
curl -sSL --max-time 90 -o scripting.html https://html.spec.whatwg.org/multipage/scripting.html#the-template-element  # exit 0
```
- No-redirect: `HTTP/2 200`, no `location` header, `content-type: text/html; charset=utf-8`,
  `content-length: 276128`, `last-modified: Thu, 22 Oct 2026 21:25:38 GMT`.
- With redirects: `http=200 ... type=text/html; charset=utf-8 size=276128 redirects=0` — zero hops,
  so the row URL stands; fragment target exists (`scripting.html:1470` `<h4 id=the-template-element>`).
- Saved body `scripting.html` sha256 `a7741016d8120b00995b438a375ddd448894035580c7801d1b4f9a89d87944b9`.
- Recorded body from `realrun/snap-bodies.tar.xz` → `bodies/S025.body`, same sha256, `cmp` exit 0.
  **The page did not change between the recorded fetch and now.**

## Quote present verbatim in the live page (`scripting.html:1553`)
```
<p>The <a href=#template-contents ...>template contents</a> of a <code ...><a href=#the-template-element>template</a></code>
element <a href=syntax.html#template-syntax>are not children of the element itself</a>.</p>
```
Tags stripped this is exactly the Gate quote: not a paraphrase, not JS-rendered content.

## Cause, reproduced
`scripts/source_recheck.py:293-315` `remove_raw_elements()` scans raw bytes with
`_RAW_START_RE = <(script|style|template)(?=[\s/>])` **without attribute context**. First bogus match:
char 4561, line 63, inside an MDN annotation attribute value:
`Element/script title="The <script> HTML element is used to embed executable code ...`.
No `</script` follows it (22 `<script` strings vs 4 `</script` in the file), so the
`end_match is None` branch (lines 306-308, "runs to the end of the document") returns the prefix.

| stage on the recorded body | chars |
|---|---|
| raw | 275983 |
| after `remove_comments` | 275983 |
| after `remove_raw_elements` | **4179** |
| after `strip_tags` = `html_text` | **1441** (0.5 %) |

The template section at line 1553 is past char 4561, so bullet (d) sees no quote → `quote_missing`.

Controls, same body/interpreter:
- `html.parser` (convert_charrefs) extraction: 82,871 chars, `quote in text` **True**; context
  `'... The template contents of a template element are not children of the element itself.\n\n  It is also possible ...'`.
- Tool's own `html_text()` after neutralizing `title="…"`/`alt="…"` values: 82,709 chars, quote **True**;
  unmodified: 1,441 chars, quote **False**. Attribute-embedded `<script` is the sole cause.
- Isolated single-check manifest `single/manifest.json` on the recorded body →
  `{"verdict":"failed-policy",...,"reason":"quote_missing"}`, exit 1. Audit finding reproduced.

## Defect scope
- `S024` is truncated the same way (in-attribute `<script` at char 183552,
  `like <base>, <link>, <script>, <style> or <title>."`, no `</script` after); its quote survives only
  because it precedes the cut — latent, not manifest.
- The sealed key cannot catch this: `.ufo/waves/round-36/sealed/cases.json` has 0 `title=`/`alt=`, and
  `make_cases.py:99` builds a real `<script>…</script>` element for bullet (c). 28/28 is compatible with it.
- Contract bullet (c) (`SCORECARD.md:1619-1624`) says "the contents of `script`, `style` and `template`
  **elements** removed"; a `<script` inside an attribute value is not an element (S092 tokenizer), and the
  "no end tag → to end of document" rule the code uses is not in the contract. The implementation is
  therefore outside its declared rule, not within a permitted simplification.

## Verdict
**Tool miss (extraction miss).** S025's `quote_missing` is a false positive: live page unchanged, quote
verbatim. Not drift, not paraphrase, not a row move; the row needs no change.

## Remaining unknowns / not verified
- Whether other `quote_missing` audit findings share this cause: only S024 was spot-checked (other bodies
  show no in-attribute `<script` under a 200-char lookback).
- Fix direction for the L1, advisory and not applied: skip attribute values when finding raw elements, or
  require an existing end tag before removing; either must be written into bullet (c) and covered by a
  sealed case, else the counter stays blind to it.
- Not run: sealed counter, ablations, selftest, any build. No tools installed or upgraded.
