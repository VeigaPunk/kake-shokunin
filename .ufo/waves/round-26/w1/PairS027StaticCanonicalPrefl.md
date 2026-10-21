# PairS027StaticCanonicalPrefl: S027 × static-canonical-preflight (freshness)

Milestone: r26-recheck-build. Axis: freshness.
Knowledge entry: `corpus/knowledge/static-canonical-preflight.md`. Source: S027, Python `urllib.parse`.

## Result

- 8 statements are attributed to or rely on S027: **7 HOLD, 1 STALE**.
- The re-fetched text still supports every S027-dependent teaching. The one STALE item is provenance only: the S027 date and version in line 2 (2026-10-20, Python 3.15) are superseded by the re-fetched Python 3.15.1 page, last updated 2026-10-21 13:02 UTC.
- The entry has no `r20` correction tails. Its corrections are `[r23-correction]` at lines 140 and 143, and neither cites S027. The round-23 and round-24 sections (lines 96-180) cite no S027 and rely on it nowhere.

## Fetch provenance

- `fetched/manifest.json`, row S027, index 1: url = finalUrl = `https://docs.python.org/3/library/urllib.parse.html`; status 200; fetchedAt `2026-10-21T15:10:49.412345+00:00`; last-modified `Wed, 21 Oct 2026 13:04:29 GMT`; 119730 bytes; sha256 `a27468b3a18380e3f0b86b9326217bfee865d2c81523d0849927dd2b8542d9f1`.
- `fetched/S027-1.raw.gz` gunzips to 119730 bytes with the same sha256. Text view `fetched/text/S027-1.txt`: 30322 characters.
- Every quote below occurs exactly once in the text view (exact string match) and is at most 25 words. `pos` is the character offset in that file.

## Verdicts

| # | Entry location | Statement (entry wording) | S027 link | Verdict | Verbatim quote (S027-1.txt) | anchorObserved | Reason |
|---|---|---|---|---|---|---|---|
| 1 | :1 | `S027 Python URL parsing https://docs.python.org/3/library/urllib.parse.html` | explicit (source header) | HOLD | "This module defines a standard interface to break Uniform Resource Locator (URL) strings up in components" (16 w) | module intro after "Source code: Lib/urllib/parse.py" (pos 727); title (pos 15) | URL equals manifest url and finalUrl, no redirect. The label "URL parsing" matches the page. The cited sections still exist: urlsplit() section (pos 2239) and "URL parsing security" (pos 16630). |
| 2 | :2 | `verified-at: 2026-10-20 (S020-S027)`, S027 part | explicit (date and version anchor) | **STALE** (provenance anchor; teaching holds) | "Last updated on Oct 21, 2026 (13:02 UTC)." (8 w); title "Parse URLs into components — Python 3.15.1 documentation" (8 w) | page footer (pos 30238); title (pos 15) | The 2026-10-20 reading was true when recorded, but the page now reads Python 3.15.1 (SOURCES.md:35 records 3.15, opened 2026-10-20) and was updated 2026-10-21. The entry records no later verification. Teaching unaffected; see the correction below. |
| 3 | :74 | "The URL module's splitting/joining functions do not perform validation" | explicit (sentence ends "(S027)" at :75) | HOLD | "The urlsplit() and urlparse() APIs do not perform validation of inputs." (11 w); joining: "it is generally not secure to use urljoin with an attacker-controlled url." (12 w) | "URL parsing security" first paragraph (pos 16653); urljoin "Warning" paragraph (pos 15198) | Splitting is stated directly. Joining rests only on the urljoin warning, because the no-validation sentence names urlsplit() and urlparse() (precision note P1). |
| 4 | :75 | "cannot be claimed as an exact WHATWG URL implementation" | explicit | HOLD | "These functions incorporate some aspects of both, but cannot be claimed compliant with either." (14 w) | "URL parsing security" third paragraph (pos 17758) | The page says "cannot be claimed compliant with either" (WHATWG or RFC 3986). The entry's "exact" is a stricter paraphrase the page supports. The browser clause at pos 17644 ("the living WHATWG spec describes what user facing web clients such as a web browser require") matches "not exact browser URL equivalence". |
| 5 | :75-76 | "The validator adds its own stated constraints" | implicit (caller-validation premise) | HOLD | "Do some verification within your code before trusting a returned component part." (12 w) | "URL parsing security" second paragraph (pos 17306) | The validator's constraints are in `scripts/canonical_audit.py`, normalize_http_url: fragment rejection :474-475; whitespace, control and backslash rejection :476-478 (these run before urlsplit, so S027's silent stripping never reaches validator input); empty-authority guard :490-492; empty-query normalization :495-496. |
| 6 | :76-77 | "successful normalization does not prove URL identity on a remote server" | implicit (parse success is not validity) | HOLD | "They may also succeed on some inputs that might not be considered URLs elsewhere." (14 w) | "URL parsing security" first paragraph (pos 16803) | S027 supports only the premise that parser success is not validity. The remote-identity clause is local policy that S027 does not address, so it is not judged. |
| 7 | :80-81 | "A reference that starts with `//` but has an empty authority ... is rejected" (mechanism) | implicit (urlsplit netloc detection) | HOLD | "urlsplit() recognizes a netloc only if it is properly introduced by" (11 w) | urlsplit() section, paragraph after the example block (pos 4054) | The guard at canonical_audit.py:490 tests `not initial.netloc`, where `initial = urlsplit(raw)` at :482. S027 documents that netloc rule. The policy citations (S029, S028) are separate. The finding IDs are not checked here. |
| 8 | :85-86 | "Python's `urljoin` instead silently inherits the base host" | implicit (urljoin documentation; uncited in this paragraph) | HOLD | "Informally, this uses components of the base URL, in particular the addressing scheme, the network location and (part of) the path" (21 w) | urljoin section, first paragraph (pos 14303) | S027 says urljoin fills missing components, including the network location, from the base. Kernel check on Python 3.14.8: `urljoin('https://example.test/project/b.html','///project/a.html')` returns `'https://example.test/project/a.html'`. canonical_audit.py:491 records the same behaviour. S027 does not document the empty-authority case, and "silently" is the entry's own wording (precision note P2). |

## Precision notes (HOLD; optional, not corrections, not in corrections[])

- P1 (row 3), optional append after line 146: `- [r26-note] S027 (re-fetched 2026-10-21) states the no-validation sentence for urlsplit() and urlparse(); its urljoin warning covers joining (w1/PairS027StaticCanonicalPrefl).`
- P2 (row 8), optional append after line 146: `- [r26-note] S027 (re-fetched 2026-10-21) documents urljoin filling missing components, including the network location, from the base; it does not document the empty-authority case, which rests on observed behavior and the validator guard (w1/PairS027StaticCanonicalPrefl).`

## Correction for row 2 (STALE, append-only)

Insert as a new bullet directly after line 146, the last `[r23-correction]` bullet, inside `### Corrections to earlier text in this entry`. Lines 1-2 stay as they are.

```
- [r26-correction] The S027 date and version in line 2 are superseded for this source. S027 (https://docs.python.org/3/library/urllib.parse.html) was re-fetched 2026-10-21 and now reads Python 3.15.1 documentation, last updated 2026-10-21 13:02 UTC; the 2026-10-20 opening remains the earlier record. The urlsplit() no-validation warning, the URL parsing security section and the WHATWG/RFC non-compliance sentence still hold on that text (w1/PairS027StaticCanonicalPrefl).
```

## Not counted (not attributed to or dependent on S027)

- :27-30 "documented URL normalization": the tool's own rules (usage text, canonical_audit.py:90-94). The code uses urlsplit and urljoin, but the rules are not S027's.
- :77-78 "Query differences remain meaningful local policy changes; fragments are rejected rather than silently stripped": local policy. Code confirms fragment rejection (:474-475) and handling of a bare `?` (:479-480, :495-496). S027 is adjacent only: urlunsplit may yield an RFC-equivalent URL for a bare `?`, and geturl drops empty fragments. No conflict.
- :82-84 RFC 3986 and RFC 9110 sentences: they cite S029 and S028.
- :86-88 WHATWG slash-skipping: no S027 citation. SOURCES.md:71 records that the WHATWG URL spec was not opened as a row.
- :121-123 C1 rejection: the code rejects C0, space, DEL and C1 (:476-478), and the entry mentions C1 only. This is a completeness point, not S027, and not judged.
- :96-180 (round-23 and round-24 sections, corrections :140-146, falsifier clarifications :149-155, receipt replay :157-180): no S027 citation or reliance.

## Notes for L1 (outside this pair; nothing edited)

- SOURCES.md:35 (S027 row) still reads "Python 3.15 documentation accessed 2026-10-20", opened 2026-10-20. The registry row needs the 2026-10-21 anchor (3.15.1).
- corpus/lessons/round-22.md:50 and corpus/lessons/round-22-verifier-spotcheck.md:125 quote "urlsplit() does not perform validation." That sentence still occurs verbatim (count 1). Their "Python 3.15" labels and 2026-10-20 dates are superseded in the same way as row 2.
- The validator imports urlsplit and urljoin (canonical_audit.py:22). The S027 urljoin text confirms the reliance behind the guard comment at :491.
- No 2026-10-20 S027 bytes are retained in round-26, so the page could not be diffed against the earlier reading. Judgments rest on the current text and the code reading above.

## Verification performed

- Read RULES.md, the entry (180 lines), the SOURCES.md S027 row, both fetch manifests (S027 row), the S027 text (30322 characters), and canonical_audit.py lines 22 and 470-503, plus a control-character grep.
- Greps over the corpus: S027 cited in the entry only at :1, :2 and :75; URL-stdlib wording in the entry; `r20` and `[r2*` tags (none beyond `[r23-correction]`); validator stdlib imports and control-character handling.
- Stdlib checks in the eval kernel (Python 3.14.8, read-only): raw digest; quote existence, count and word count; quote positions; the netloc quote; four urljoin cases.
- Not run: builds, tests, linters, network fetches, browsers. No round-24 material was opened.

## Tooling

- No tools were installed or updated. Checks used the kernel's Python 3.14.8 standard library.

```json
{"pair":"S027xstatic-canonical-preflight","statements":8,"hold":7,"stale":1,"corrections":["- [r26-correction] The S027 date and version in line 2 are superseded for this source. S027 (https://docs.python.org/3/library/urllib.parse.html) was re-fetched 2026-10-21 and now reads Python 3.15.1 documentation, last updated 2026-10-21 13:02 UTC; the 2026-10-20 opening remains the earlier record. The urlsplit() no-validation warning, the URL parsing security section and the WHATWG/RFC non-compliance sentence still hold on that text (w1/PairS027StaticCanonicalPrefl)."]}
```
