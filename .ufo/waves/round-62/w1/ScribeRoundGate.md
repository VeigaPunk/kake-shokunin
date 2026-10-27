# ScribeRoundGate — round-62 lesson `## Gate record` draft (advisory)

Seat: scribe, leaf, no dispatch. Base `c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13`.
Lane files were read only; nothing outside this report path was written. No counter, claim, criterion or
score was changed, and `corpus/lessons/round-61-verifier-spotcheck.md:33` (`Disagree`) stands.

No scratch directory was created: every check below streamed or read in place, so `/fast/scratch/hyaku/kake-r62/ScribeRoundGate/`
does not exist and needed no cleanup.

## Draft to append by the owning seat

Intended destination: the `## Gate` section of `corpus/lessons/round-62.md` (file absent at base — `ls corpus/lessons/`
shows `round-60.md`, `round-61.md`, `round-61-verifier-spotcheck.md`, no `round-62.md`). Append verbatim; the frozen
counter's `lesson_gate` condition reads `"## Gate"`, `"S432"`, `"Agree"`, `"Reject"` as substrings of that file.

```markdown
## Gate record — S432 correction

- S432 — https://fetch.spec.whatwg.org/ — opened 2026-10-27 (HEAD `date:` 2026-10-27T11:59:41Z, HTTP/2 200, `last-modified` 2026-10-19T12:03:15Z; the GET body's sha256 equals the retained body's) — §3.6 — "response header can be used to require checking of a response’s Content-Type header against the destination of a request" (19 units, 120 chars; retained body `.ufo/waves/round-61/sources/S432.html`, sha256 `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b`, 1854393 bytes, 18915 lines; heading line 6149, sentence lines 6151–6154, `determine nosniff` algorithm from 6157).
  - Location measured this round: the span is a run of adjacent text nodes crossing the `<code>`/`<a>` inline
    boundaries at 6151–6154 and is contiguous in the body's collapsed text only after the body's literal backticks
    around the inline `<code>` elements are dropped (`raw=0`, `collapsed-with-backticks=0`,
    `collapsed-backticks-removed=1`). It is page-unique: the only other occurrence of the fragment
    "can be used to require checking" is §3.7's `Cross-Origin-Resource-Policy` sentence.
  - Re-opened, not re-fetched from a stale copy: the live GET's body sha256 equals the retained body's
    `63b0a018…bad911b` and its byte count equals 1854393, so the corrected span is the current page's text.
  - Admit — the span names the field's job (a response header requiring a check of a response's `Content-Type`
    against a request's destination) and the same §3.6 carries the one-production `nosniff` value ABNF the entry's
    `xcto_nosniff_value` class compares against, so quote and audit rule share one location. Row
    `corpus/SOURCES.md:178` stays admitted at tier A, and the entry's old prose is preserved with the correction
    appended.
  - Reject — the round-61 admitted span "Web developers and conformance checkers must use the following" names no
    field, response or check; it is a lead-in to the value block and cannot ground a response-header expectation,
    so the verifier's `Disagree` (`corpus/lessons/round-61-verifier-spotcheck.md:33`) is upheld on that span and the
    correction replaces the quote rather than defending it. No row rejection is recorded: the disagreement is about
    a quote, not about the row's tier or its §3.6 scope.
  - Agree — with the corrected span the row's §3.6 evidence meets the verifier's bar (19 units, page-unique,
    located in the section that carries the value rule), so the `Disagree` is closed on the quote and no other
    disagreement remains open against S432.
  - Independent spot-check — **pending**: no non-author seat has re-opened this correction in round 62. The
    measurement above is this lane's own; the frozen counter's `lesson_gate` reads substrings only, so this
    pending status cannot turn red on its own and must be carried as prose until a non-author re-check lands.
```

## Evidence for each claim in the draft

| Claim | Command | Output |
|---|---|---|
| Live page opens | `curl -sS -o /dev/null -w 'http_code=%{http_code} size_download=%{size_download} url=%{url_effective}\n' -L --max-time 30 https://fetch.spec.whatwg.org/` | `http_code=200 size_download=1854393 url=https://fetch.spec.whatwg.org/` |
| Live body = retained body | `curl -sS --max-time 60 https://fetch.spec.whatwg.org/ \| sha256sum` | `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  -` |
| Retained body digest | `sha256sum .ufo/waves/round-61/sources/S432.html` | `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b` |
| Access date / revision | `curl -sSI --max-time 30 https://fetch.spec.whatwg.org/` (first line + `date:`/`last-modified:`) | `HTTP/2 200`, `date: Tue, 27 Oct 2026 11:59:41 GMT`, `last-modified: Mon, 19 Oct 2026 12:03:15 GMT` |
| Span bounds and node fragmentation | `python3` over the retained body: strip tags, collapse whitespace, count the quote with and without the body's literal backticks | `raw occurrences: 0` / `collapsed occurrences: 0` / `collapsed+nobacktick occurrences: 1`; collapsed context `… 3.6. X-Content-Type-Options header The X-Content-Type-Options response header can be used to require checking of a response’s Content-Type header against the destination of a request. To determine nosniff, given …` |
| Uniqueness of the fragment | same script, `re.finditer('can be used to require checking', collapsed)` | two hits: §3.6 `X-Content-Type-Options` and §3.7 `Cross-Origin-Resource-Policy` (`… require checking a request’s current URL’s origin …`); the full quote occurs once |
| Line numbers | `sed -n '6148,6158p'` equivalent read of the retained body | 6149 `<h3 … data-level="3.6" …>`; 6150 `<p>The`; 6151 `…<code>X-Content-Type-Options</code>…`; 6152 `response … header can be used to require …`; 6153 `…<code>Content-Type</code>…`; 6154 `…request</a>.`; 6157 `<div class="algorithm" data-algorithm="determine nosniff">` |
| Unit count | `len(q.split())` on the quote, no CJK characters | `words: 19 chars: 120` → 19 units under the round-60 one-unit-per-non-CJK-whitespace-token rule, inside the 6..25 and ≤160-char bounds |
| Row still admitted | `grep -n '| S432 |' corpus/SOURCES.md` | `178:| S432 | WHATWG Fetch — https://fetch.spec.whatwg.org/ | spec | A | X-Content-Type-Options nosniff value rule | Section 3.6 … accessed 2026-10-27 … | mined | 2026-10-27 | 180d | corpus/knowledge/response-header-expectations.md |` |
| Disagreement row untouched | `grep -n 'S432' corpus/lessons/round-61-verifier-spotcheck.md` | line 33 carries the unique `Admit`/`Disagree` row; lines 36/41/42/46 carry the unlearned-finding routing |
| No criterion yet at base | `grep -n 'round-61-verifier-spotcheck' corpus/QUALITY.md` | no match |
| Draft block satisfies `lesson_gate` | `python3` over the fenced block in this file: `all(k in block for k in ("## Gate","S432","Agree","Reject"))` and a per-line search for the quote | `lesson_gate: 1`, `quote single-line in draft: True`, `draft block bytes: 2875` |

## Gate status of this draft (not this seat's to score)

- `lesson_gate` substrings present in the draft block, measured on the block itself rather than assumed:
  `"## Gate"`, `"S432"`, `"Agree"`, `"Reject"` → `lesson_gate: 1`; the 19-word quote stands on one line in the
  block, so a line-wise reader finds it verbatim. I deliberately did **not** run
  `.ufo/waves/round-62/c62_calibration.py`; the base control (`unresolved=1 quote_correction=0 criterion=0
  lesson_gate=0 source_row=1 met=false`, exit 1) is the orchestrator's recorded pre-wave measurement and re-running it
  here would only decorate the report.
- The counter's after-state also needs `corpus/knowledge/response-header-expectations.md` to carry the exact
  `QUOTE` constant plus `S432 §3.6` plus `Round-62 correction`, and `corpus/QUALITY.md` to carry
  `substantive located quote` plus `round-61-verifier-spotcheck.md`. Those are other seats' surfaces; nothing here
  asserts they landed.

## Findings

- **F1 — the draft's `Agree` is a labelled verdict line, and the substring test is what a scorer sees.** The frozen
  `lesson_gate` condition is a four-substring test, so any `Agree` in prose would satisfy it. The draft therefore
  spells it as its own labelled line (`Agree — with the corrected span …`) rather than relying on incidental
  wording, and the prose verdict is separable from the token that makes the counter green. A seat that edits this
  block must keep that line: dropping it silently turns `lesson_gate` from 1 to 0 with no other visible change.
- **F2 — "substantive §3.6 body lines 6151–6154" is accurate for the sentence without its leading "The".**
  Line 6150 is `<p>The`; the quoted span begins on 6151. A future re-derivation that greps 6151 only will see the
  sentence intact, but any claim that line 6150 is part of the quote is loose by one token.
- **F3 — the quote is not one collapsed text node.** Round-61's gate convention requires "one collapsed text node,
  page-unique". This span crosses `<code>`/`<a>` boundaries and only becomes contiguous after dropping the body's
  literal backticks; the draft states that measurement instead of claiming node contiguity. A reader who applies the
  old convention mechanically would reject the span; the honest record is the one above.
- **F4 — the retained body is byte-identical to today's live page, so the correction is not at risk from a drifted
  snapshot.** `last-modified` 2026-10-19 predates the round-61 retention, which is consistent with 2026-10-27
  fetches having captured the same revision. This strengthens the record but is **not** an independent semantic
  spot-check: it is the same lane fetching the same bytes twice.
- **F5 — the pending spot-check cannot be forced by the frozen predicate.** `measure()` sets `unresolved = 0` as
  soon as `correction and criterion and lesson_gate and source_row` are all 1, so a lane-green run coexists with a
  still-pending non-author check. The draft keeps the pending status explicit; the round-62 report must not upgrade it,
  and round-63 should carry it as the next round's lesson input rather than a closed item.

## Touched surfaces

- Written: `.ufo/waves/round-62/w1/ScribeRoundGate.md` (this file) only.
- Read: `.ufo/waves/round-62/contract.md`, `.ufo/waves/round-62/c62_calibration.py`,
  `.ufo/waves/round-61/sources/S432.html:6145-6163`, `corpus/lessons/round-61-verifier-spotcheck.md`,
  `corpus/lessons/round-61.md`, `corpus/knowledge/response-header-expectations.md`, `corpus/QUALITY.md`,
  `corpus/SOURCES.md:178`; network reads to `https://fetch.spec.whatwg.org/` (one web-reader fetch, then three
  GETs and one HEAD, all 2026-10-27).
- Not modified: `corpus/lessons/round-62.md` (absent), `corpus/knowledge/response-header-expectations.md`,
  `corpus/QUALITY.md`, `corpus/SOURCES.md`, the verifier spot-check, the counter, Git/jj state, fleet repo, siblings,
  `~/.local/bin`. No installs, no pacman transactions.

## Out of scope / not done

- Not written: the lesson file, the knowledge correction, the QUALITY criterion.
- Not run: the frozen counter at any revision; any scoring or verdict.
- Not claimed: a resolved disagreement count of 0, a green gate, or any independent verification.
