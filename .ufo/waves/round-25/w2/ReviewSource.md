# ReviewSource — round 25 wave 2 (author-side falsify, S035 re-open)

Seat: `KakeR25.ReviewSource` · axes judged: operability, freshness · milestone
`r25-falsify-accessibility-packet`. Scope: new S035 registry row, round-25 lesson
Gate quote/source SHA, packet knowledge entry provenance trio. No r24 source,
assignment, probe or counter was opened. No production file edited. No suite,
build, formatter or packet command was run. Tools installed or updated: none.

## Verdict

S035 holds. The pinned W3C Recommendation was re-opened in raw mode and is
byte-identical to the retained source. The §5.2.2 quote is exact and located
once. The registry row is well-formed and append-only against base `6883f1d`.
The provenance trio is compliant. Two findings remain, neither a source defect:
F1 (word-count miscount, already captured as an uncommitted erratum) and F2
(Gate quote grounds only one of the five requirements listed in `teaches`).
One freshness move is proposed (M1).

## Evidence

### Pinned source re-open (freshness)

- `curl -sSL https://www.w3.org/TR/2024/REC-WCAG22-20241212/` →
  HTTP 200, 512457 bytes, no redirect. Response `Date: Wed, 21 Oct 2026 13:35:50 GMT`,
  `Last-Modified: Thu, 12 Dec 2024 10:36:22 GMT`, `text/html; charset=utf-8`.
- Fetched SHA256 `6e3c5fe397257cae509a2fb4752b73062cf8cbeb92c2cec618989b17e4cf7057`.
  This equals the retained `.ufo/waves/round-25/source-wcag22.html`, the lesson Gate,
  the S035 anchor cell, `population.json.sourceSha256`, and
  `scripts/accessibility_packet.py` `SOURCE_SHA256` (line 20).
- Revision identity in bytes: title `Web Content Accessibility Guidelines (WCAG) 2.2`;
  `W3C Recommendation 12 December 2024`; `This version: https://www.w3.org/TR/2024/REC-WCAG22-20241212/`.
- Latest-version URL `https://www.w3.org/TR/WCAG22/` → HTTP 200, same SHA256
  `6e3c5fe3…7057`. It still states `W3C Recommendation 12 December 2024` and links
  the pinned dated URL once. No newer WCAG 2.2 release exists as of this re-open,
  so the `on-release` recheck is not triggered.

### §5.2 quote (exact)

The quote was checked against tag-stripped, whitespace-collapsed, entity-decoded
source text using the packet's documented normalization.

- Lesson Gate quote “Conformance (and conformance level) is for full web page(s) only”
  occurs exactly once, in `<section id="cc2">` heading `5.2.2 Full pages`. Full sentence:
  “Conformance (and conformance level) is for full web page(s) only, and cannot be
  achieved if part of a web page is excluded.” The quote is a case-exact,
  word-boundary prefix of that sentence. The raw-byte substring count is 0 because
  “Conformance” sits inside `<a href="#dfn-conform">`; it is located only after
  markup normalization. That is expected, not a defect.
- The packet entry's citation of the same text (lines 89–90) matches.
- The packet entry's paraphrases of §5.2.1, §5.2.3, §5.2.4 and §5.2.5 match sections
  `cc1`, `cc3`, `cc4` and `cc5` in the retained bytes (text located, see F2).

### Registry row S035 (operability)

- `git diff --numstat 6883f1d HEAD -- corpus/SOURCES.md` shows `3 0`, with 0 removed
  lines. Base has 34 `| S0` rows and HEAD has 35. The 34 prior rows are byte-identical
  (`diff` of the base rows against HEAD rows minus S035 printed nothing). No prior
  status, recheck or used-by cell changed, consistent with append-only rule 2.
- The three added lines are the S035 row, a blank line, and the Round 25 search-log
  paragraph (identified 1 / screened 1 / included 1 / excluded 0, with a stop
  rationale). The search-log paragraph satisfies rule 5.
- Cell checks against CORPUS contract v1:

  | Cell | Value |
  |---|---|
  | count | 11 cells |
  | id | `S035`, the next unused id |
  | kind | `spec` |
  | tier | `A`, scoped to "Publisher-side manual-review preparation for WCAG 2.2 Level A and AA, not website conformance" |
  | anchor | REC date 12 December 2024, "success criteria and section 5.2", opened 2026-10-21, saved SHA256 (not a bare homepage) |
  | status | `mined` |
  | opened | `2026-10-21` (ISO date) |
  | recheck | `on-release` (an allowed cadence) |
  | used-by | both paths exist and both contain `S035` |
- Access date: row `opened` 2026-10-21, lesson "accessed 2026-10-21", trio
  `verified-at: 2026-10-21`, and `population.json.opened` 2026-10-21 all agree.
- Population binding: `population.json` SHA256 `4751dc24…3058` equals
  `POPULATION_SHA256` (line 18). There are 55 criteria and 55 cards with identical
  id sets (31 A, 24 AA), all `not-assessed`. Every card `source` fragment resolves to an
  `id=` in the retained bytes. 4.1.1 is absent from cards; the source marks it
  “Success Criterion 4.1.1 Parsing (Obsolete and removed)”.

### New entry provenance trio

`corpus/knowledge/accessibility-review-packet.md` lines 1–3 open with `source:`,
`verified-at:` and `recheck:`. `source:` cites `S035` alongside the URL and the anchor
(SC 1.1.1–4.1.3, §5.2). This satisfies the additional rule "new knowledge entry opens
with its provenance trio".

## Findings

**F1: Gate word count wrong at HEAD; erratum pending in the working tree.**
Committed `corpus/lessons/round-25.md` (HEAD `9f62cda`) Gate reads "(12
whitespace-delimited words)". The quote has 10 words: `Conformance` `(and`
`conformance` `level)` `is` `for` `full` `web` `page(s)` `only`. The uncommitted
working-tree lesson adds a "Source-quote count erratum … 10 … not 12" bullet. The
quote stays within the ≤25-word rule and inside the packet's 6–25 window either way.
Affected: operability (record accuracy). Status: captured; it lands only when the
working tree is committed.

**F2: Gate quote grounds 1 of the 5 requirements that `teaches` enumerates.**
CORPUS rule 1 requires a ≤25-word quote "with its location grounding `teaches`".
S035 `teaches` lists all A/AA criteria, full pages, complete processes,
accessibility support and non-interference. The single Gate quote (§5.2.2) grounds
only "full pages". The other four requirements are present in the source (located
below) but are not quoted in the Gate. The leading clause "A criterion inventory
prepares review evidence" is the lane's own inference, not W3C text. This does not
falsify the row; it is under-recorded grounding.

## Proposed move (one, bounded)

**M1: append grounding quotes to the lesson Gate and add an executable
version-change recheck to the trio.** This improves operability and freshness and
leaves the source, row and packet tool untouched.

1. Append to `corpus/lessons/round-25.md` `## Gate` → `### Source opened` (the lesson
   is still uncommitted working tree, so no append-only conflict). Each quote below
   was verified to occur exactly once in the normalized retained source:
   - §5.2.1 (`cc1`), 22 words: “the web page satisfies all the Level A and Level AA
     success criteria, or a Level AA conforming alternate version is provided.” The
     full sentence including “For Level AA conformance,” is 26 words, over the
     25-word limit, so this trimmed form is the one to use.
   - §5.2.3 (`cc3`), 13 words: “all web pages in the process conform at the specified
     level or better.”
   - §5.2.4 (`cc4`), 14 words: “Only accessibility-supported ways of using
     technologies are relied upon to satisfy the success criteria.”
   - §5.2.5 (`cc5`), 16 words: “then they do not block the ability of users to access
     the rest of the page.”
2. The trio's `recheck:` currently says "reopen S035 on a WCAG version change", but
   `accessibility_packet.py` is offline and byte-pinned. It cannot detect a new WCAG
   release; it reports a changed local file as `snapshot_tampered`. Other entries
   (`crawl-scope-per-host.md`, `ghp-custom-domain.md`) carry a runnable source probe.
   Proposed addition:
   `curl -fsSL https://www.w3.org/TR/WCAG22/ | grep -cF 'href="https://www.w3.org/TR/2024/REC-WCAG22-20241212/"'`
   This printed `1` on 2026-10-21. `0` means the latest WCAG 2.2 no longer names the
   pinned revision, so S035 must be re-opened. A full-page SHA comparison is stricter
   but would also fire on editorial or errata edits to the latest page, so the
   targeted grep is preferred.

**Risks:**
- Editing the trio changes the packet entry's bytes. The cards and population pins
  are unaffected (the tool pins `population.json` and the source HTML, not this
  Markdown).
- If a freshness sweep parses `recheck:` strictly, the added command must stay on
  line 3.
- The step 2 probe is a network read. It belongs in recheck documentation, not in the
  offline packet command or the selftests.
- Both edits are L1 integration decisions. This seat made neither.

**Verification for main:**
- Re-run the quote-presence check on the retained source with the packet's
  normalization (each M1 quote count = 1, word count ≤25).
- Re-check that `git diff 6883f1d -- corpus/SOURCES.md` shows 0 deletions.
- Run the assigned suite once after integration:
  `python3 -B scripts/accessibility_packet.py --root . --json` and
  `python3 -B .ufo/waves/round-25/measure.py --root . --revision <commit>`.

## Contradictions stated

- The lesson Gate's 12-word count (HEAD) contradicts the quote's actual 10 words.
  The working tree records this; it is not resolved at a committed revision.
- `teaches` enumerates five §5.2 requirements; the Gate quote evidences one.
- The trio says "reopen S035 on a WCAG version change"; its only command is offline
  and cannot observe a version change.
