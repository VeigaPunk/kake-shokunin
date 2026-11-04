# ScoutSources — round 80, wave w1

**Verdict:** both sources open clean and every sentence C2 rests on is located; the `S453` row draft is 11-cell clean and passes the C1 counter's own `row_shape` gate. **Blocker for C1, not for C2:** `p_r79_1` reads the `used-by` cell at index 11 of an 11-cell row, so **R79-1 is unsatisfiable at the frozen counter bytes** no matter what the scribe writes (proof below).

## 1. Fetch receipts (one GET per source, `curl -sSL --max-time 45`)

| source | status | final URL | bytes | sha256 | fetched (UTC) |
|---|---|---|---|---|---|
| RFC 9110 plain text | 200 | `https://www.rfc-editor.org/rfc/rfc9110.txt` (no redirect) | 502,941 | `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` | 2026-11-04T10:44:33Z |
| MDN X-Robots-Tag (S452 re-open) | 200 | `https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Robots-Tag` (no redirect) | 218,816 | `c4216ffb7aa934e309329d3b5adf1e62557464eebcbaab0bb33b60a72b7aaf38` | 2026-11-04T10:44:33Z |

Retained under `.ufo/waves/round-80/w1/ScoutSources/`: `S453-rfc9110.txt` (502,941 B, 10,785 lines / 8,658 non-blank), `S452-mdn-x-robots-tag.raw` (218,816 B), `S452-mdn-x-robots-tag.txt` (17,442 B, 677 lines, sha256 `dd94203e1a38b7efb49092095364ad8298b2a0d46a80f7bc13e87e3cc554bc26`), and `fetch-receipts.json`.

Two freshness cross-checks (both green):

- **RFC 9110 has not drifted.** My 10:44:33Z bytes are `cmp`-identical to the copy already at `.ufo/waves/round-80/sources/rfc9110.txt` (mtime 07:45, another seat), and their sha256 equals the `plain text sha256 21c1cdce…7232a` the lane registered on 2026-10-21 in `corpus/SOURCES.md:36` (S028). Same document identity: `S453-rfc9110.txt:5-15` — `STD: 97`, `Category: Standards Track`, `June 2022`, title `HTTP Semantics`.
- **S452 has not drifted.** My raw is byte-identical (same 218,816 bytes, same sha256) to `.ufo/waves/round-79/sources/S452-mdn-x-robots-tag.raw` retained at 09:39:04Z today. The re-open contradicts nothing in the round-79 row.

*Clock note:* `date -u` returned 10:44:33Z while the written files carry mtime 07:46 — the same ~3 h host offset visible in round-79 (receipt says 09:39:04Z, mtime 06:39). Receipt times are the `date -u` values; mtimes are not authoritative.

## 2. RFC 9110 §5.6.7 — the three formats and the MUST

Section heading `5.6.7.  Date/Time Formats` at `S453-rfc9110.txt:1836`. All line numbers are in **my** retained text.

- Three formats named, `:1838-1853`: "Prior to 1995, there were three different formats…"; `HTTP-date    = IMF-fixdate / obs-date` at `:1844`; the three examples at `:1848` (`Sun, 06 Nov 1994 08:49:37 GMT ; IMF-fixdate`), `:1852` (`Sunday, 06-Nov-94 08:49:37 GMT ; obsolete RFC 850 format`), `:1853` (`Sun Nov  6 08:49:37 1994 ; ANSI C's asctime() format`).
- The recipient MUST, `:1855-1856`: "A recipient that parses a timestamp value in an HTTP field MUST accept all three HTTP-date formats." The sender MUST follows at `:1856-1858`: "When a sender generates a field that contains one or more timestamps defined as HTTP-date, the sender MUST generate those timestamps in the IMF-fixdate format."
- ABNF: `IMF-fixdate  = day-name "," SP date1 SP time-of-day SP GMT` (`:1873`, with `day-name`/`date1`/`month`/`year`/`GMT`/`time-of-day`/`hour`/`minute`/`second` at `:1875-1898`); `obs-date     = rfc850-date / asctime-date` (`:1900`); `rfc850-date  = day-name-l "," SP date2 SP time-of-day SP GMT` (`:1902`); `asctime-date = day-name SP date3 SP time-of-day SP year` (`:1910`); `date3        = month SP ( 2DIGIT / ( SP 1DIGIT ))` (`:1911`, comment `; e.g., Jun  2`).
- Case and whitespace: `HTTP-date is case sensitive` (`:1914`); "A sender MUST NOT generate additional whitespace in an HTTP-date beyond that specifically included as SP in the grammar" (`:1917-1918`).
- **Extra, and load-bearing for amendment A1:** §5.5 *Field Values* (`:1579`) says of commas, `:1625-1633`: "Because commas (\",\") are used as the delimiter between members, they need to be treated with care if they are allowed as data within a member… Fields that expect to contain a comma within a member, such as within an HTTP-date or URI-reference element, ought to be defined with delimiters around that element to distinguish any comma within that data from potential list separators." So the RFC anticipates exactly the round-79 splitter failure. It is a `ought` on field *definers*, and `X-Robots-Tag` is defined by no specification (S452 `:265`), so this sentence explains the failure; it does not by itself forbid a comma-splitting parser.

## 3. S452 re-open — what the page actually says

Line numbers in my tag-stripped text; the round-79-derived numbering used in `corpus/knowledge/x-robots-tag-header.md` (which cites `S452:211`, `:212`, `:215`, `:239`) runs **2 lower in the directives block and 4 lower at the example**. Raw bytes are identical; only the stripper differs. Map: my `:213`=`211`, `:214`=`212`, `:217`=`215`, `:243`=`239`.

- Directive and date value: `:211` `unavailable_after: <date/time>`; `:212` "Requests not to show this page in search results after the specified `<date/time>`."; `:213` "Ignored if no valid `<date/time>` is specified."
- **(a) The accepted date shapes — yes, named, as three families:** `:214` "A date must be specified in a format such as RFC 822, RFC 850, or ISO 8601." (17 words.) Note what it says and does not say: it names **RFC 822**, not RFC 9110 and not IMF-fixdate; it never mentions **asctime**; the list is "such as", i.e. open-ended. So A2's asctime shape is grounded in S453 alone, not in S452 — the amendment already states it that way, and this confirms the attribution is right.
- **(b) Not part of a specification — yes, twice:** `:137` "While not part of any specification, it is a de-facto standard method for communicating with search bots, web crawlers, and similar user agents."; and the Specifications section at `:265` "Not part of any current specification."
- The comma example: `:243` `X-Robots-Tag: unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT`, inside "Multiple headers" (`:238-243`). The page shows the comma-bearing value; it never writes a sentence saying the comma belongs to the date.
- Also located, for the round-79 row's completeness: `:215-217` default is no expiry, omitted means shown indefinitely, crawlers are expected to decrease crawl rate after the date; `:153-160` the syntax block where `,` is the rule separator (`X-Robots-Tag: <indexing-rule>, …, <indexing-ruleN>` at `:156`); section offsets for the scribe — `Description` `:218`, `Examples` `:230`, `Multiple headers` `:237` (example `:243`), `Specifying user agents` `:244`, `Specifications` `:264`.

## 4. Deliverable (i) — `S453` row draft (11 cells)

Validated by importing the counter itself: `row_shape` → `''` (no complaint), `len(cells) = 11`, source contains `rfc 9110` → True, contains `9309` → False, `kind/tier/status = spec A queued`.

```
| S453 | RFC 9110: HTTP Semantics, §5.6.7 Date/Time Formats — https://www.rfc-editor.org/rfc/rfc9110.txt | spec | A | The three HTTP-date formats a timestamp recipient must accept — IMF-fixdate, the obsolete RFC 850 shape and asctime — and their ABNF; not the unavailable_after field (defined by no specification), not robots.txt semantics, not ISO 8601, not any crawler's parsing behaviour | §5.6.7 Date/Time Formats lines 1836-1858 and ABNF lines 1844, 1873, 1900-1912, plus §5.5 lines 1625-1633 on a comma inside a member; fetched 2026-11-04T10:44:33Z, HTTP 200, 502,941 bytes, raw sha256 21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a | A recipient that parses a timestamp value in an HTTP field MUST accept all three HTTP-date formats while a sender MUST generate IMF-fixdate; a field that may carry a comma inside a member ought to be defined with delimiters around that member | queued | 2026-11-04 | 365d | — |
```

`used-by` is `—` as instructed. **Do not leave it there if R79-1 is to close:** `p_r79_1` requires the `used-by` cell to name an existing file whose text contains `S453`. Candidates: `corpus/knowledge/x-robots-tag-header.md` (exists, already discusses the date families at its lines 85-93, would need one `S453` citation added) or `corpus/lessons/round-80.md` (absent as of this writing).

## 5. Deliverable (ii) — located quotes

**For the `S453` row** — 17 words, `S453-rfc9110.txt:1855-1856`:

> A recipient that parses a timestamp value in an HTTP field MUST accept all three HTTP-date formats.

URL `https://www.rfc-editor.org/rfc/rfc9110.txt`, accessed 2026-11-04, sha256 `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`.

**For the S452 re-open** — 17 words, `S452-mdn-x-robots-tag.txt:214` (= round-79 numbering `:212`):

> A date must be specified in a format such as RFC 822, RFC 850, or ISO 8601.

URL `https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Robots-Tag`, accessed 2026-11-04, raw sha256 `c4216ffb7aa934e309329d3b5adf1e62557464eebcbaab0bb33b60a72b7aaf38`, stripped-text sha256 `dd94203e1a38b7efb49092095364ad8298b2a0d46a80f7bc13e87e3cc554bc26`.

## 6. Deliverable (iii) — sentences I could NOT locate (plainly)

1. **No sentence on S452 says the comma belongs to the date value.** The page demonstrates it (`:243`) and defines `,` as the rule separator (`:124-131`); it never states the segmentation rule. A1's comma rule therefore rests on the RFC §5.5 sentence plus S452's example, not on a statement of S452.
2. **S452 never names `asctime`, `IMF-fixdate`, RFC 9110, or RFC 3339.** Only "RFC 822, RFC 850, or ISO 8601" appears (`:214`). Any claim that asctime is source-named by S452 is unlocatable.
3. **S452 never says "date" and "date/time" consistently**: the directive is `<date/time>` (`:211`), the constraining sentence says "A date" (`:214`). No sentence resolves which governs; the lane reads it as permitting date-only (correctly, but by inference).
4. **RFC 9110 §5.6.7 says nothing about `unavailable_after`, `X-Robots-Tag`, or robots directives**, and nothing about how a field defined outside HTTP's own grammar should segment commas. The bridge from §5.6.7 to the header is the lane's, via S452.
5. **Amendment A2's ABNF is not the RFC's ABNF.** A2 renders the asctime shape as a regex `(...) {1,2}[0-9]{1,2} hh:mm:ss YYYY`; the RFC is `date3 = month SP ( 2DIGIT / ( SP 1DIGIT ))` (`:1911`), i.e. exactly one SP then either two digits or one SP plus one digit. A2's prose ("space-padded to width two (a single space is also accepted)") deliberately widens past the RFC to admit `Nov 6`. No frozen case exercises the widened branch (c34 `Nov  6` and c43 `Nov 16` both fit the RFC), so no oracle conflict — but the transcribed regex is not RFC-verbatim and should not be quoted as such.

## 7. Blocker: C1's R79-1 branch is unsatisfiable (counter defect, frozen bytes)

`.ufo/waves/round-80/c80_defect_queue.py:124`:

```python
    used = row[11] if len(row) > 11 else ""
```

`row` is the 11-cell split (indices 0-10), and the same file's `row_shape` (line 90-92) enforces exactly 11 cells and reads `kind/tier/status` as `cells[2]/[3]/[7]`. So for every shape-valid row `used == ""`, `cited == []`, `resolved == []`, and line 127's `if not resolved:` returns open. Two probes over a scratch tree with a valid 11-cell `S453` row, a `corpus/lessons/round-80.md` carrying `R79-1`/`S453`/`RFC 9309`, and a `corpus/knowledge/xrt-date-grammar.md` containing `S453`:

- `used-by` cell = `corpus/knowledge/xrt-date-grammar.md` → `(False, 'S453 used-by resolves to no file that cites S453')`
- same row padded to 12 cells so `row[11]` holds the path → `(False, 'S453 row fails the registry shape: 12 cells, want 11')`

Hence **R79-1 can never read closed**, and C1's predicate `open == 0` is unreachable at `f20163c1e98cefa863931a5241bae76c8d0af6c1` regardless of scribe work. The base control did not catch it because at base the row is absent and line 115 returns before the buggy branch (`controls/base-c80-defect-queue.txt:2` → `R79-1 open no S453 row`). `c80_defect_queue.py` has no `--selftest`. This needs an L1 decision (amend/re-derive the counter before data, or re-scope C1); I did not touch it.

## 8. Housekeeping

No tool installs or upgrades were needed — `curl 8.x`, `python3` and coreutils from the host only. Scratch lived at `/fast/scratch/hyaku/kake-r80/ScoutSources/` (fetch, strip, `probe-tree`, `probe-tree-12`) and was removed before this report; the retained bytes above are copies made first. I wrote only `.ufo/waves/round-80/w1/ScoutSources.md` and `.ufo/waves/round-80/w1/ScoutSources/`. I did not write `corpus/`.
