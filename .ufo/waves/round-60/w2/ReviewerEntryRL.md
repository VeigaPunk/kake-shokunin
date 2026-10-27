# ReviewerEntryRL

ATTACKS: `corpus/knowledge/robots-txt-limits.md` at B1 (`8b33fd2…`), sentence by sentence, against
the S429 article block (`.ufo/waves/round-60/sources/S429.html`); all 15 double-quoted spans
re-extracted with my own Python (not the frozen counter's code); page facts (title, h1/h2s, footer
revision line, receipt digest/bytes, recheck grep) re-derived; duplication against
`corpus/knowledge/robots-txt-rules.md` and the held entries the w1 report names; the 15 staged-
sentence refusals of `w1/EntryRobotsLimits.md` checked both against the B1 entry (absence) and
against the staged shokuknow source (truthfulness). Evidence: `.files/EVIDENCE.txt` (§ numbers
below), extractor in `.files/analyze_s429.py` / `dump_nodes.py`. Scratch deleted.

## SENTENCES:

Clean (each re-derived, not trusted from w1):
- 15/15 spans: substring of ONE whitespace-collapsed article text node, 6..25 units, <=160 chars,
  occ(S429)=1, occ(S427)=occ(S428)=0 (§1). Two quotes are truncated mid-sentence ("…but the search
  result", "…to your site") — both continue in the same node; continuations support the entry's
  glosses ("won't have a description", "; it's up to the crawler…").
- Title "Robots.txt Introduction and Guide" before " | "; exactly 3 article `<h2>`s as listed, 0
  `<h3>`; "Last updated 2025-12-10 UTC." inside `<devsite-content-footer>` — the page's only other
  "Last updated" hit is after the footer close, in neither article nor footer (§2).
- sha256/bytes = receipts.json S429 exactly; receipt fields as contract C6 requires (§3). Row S429:
  11 cells, anchor cell names the §, used-by = this entry (§3).
- Negative claims hold: baidu/yahoo/prefix/wildcard/user-agent/dns/crawl-delay/sitemap/404/error/
  unavailable/"server error" = 0 in the article; googlebot = 1; noindex = 3 (§2). Recheck predicate
  `grep -F -c 'Different crawlers interpret syntax differently.'` -> 1 (§2). Structure claims that
  hold: frame paragraph precedes the limits; first limit = li 1's bold lead "…may not be supported
  by all search engines."; enforcement limit li 2; purpose sentence is one sentence (§4, §6).

Defects (F1–F4, same class: reallocation across document locations). The page's "disallowed URL
can still be indexed" material lives in TWO places: limits-section `<li id="robotted-but-indexed">`
and the section-1 table "robots.txt effect on different file types". The entry stitches them into
continuous narratives without telling the reader, and misattributes two quotes (§2, §5, §6).
The limits are a four-item bulleted `<ul>` of bold-lead `<li>`s, which the entry calls paragraphs.

## DUPLICATION:

- Against `robots-txt-rules.md` (B1): no rule/parse/matching mechanic restated; its "listing a path
  makes that path discoverable" is discovery, not the linked-from-elsewhere index path; only the
  advisory-character reading (S011 §§1, 3) overlaps — see F6.
- `js-rendering-queue.md:41-45` (B1) holds the noindex-on-disallowed interplay, not the
  linked-from-elsewhere case — the w1 HELD BEFORE claim is accurate (§7).
- `crawler-identity.md:27,55` "both crawler types obey the same product token" verified as cited (§7).

## FINDINGS:

| Sev | Target (B1) | Issue | Evidence command | Fix |
|---|---|---|---|---|
| med | corpus/knowledge/robots-txt-limits.md:80-83 | Quote reallocation: "its URL can still appear in search results, but the search result" is the section-1 table's Web-page row ("If your web page is blocked with a robots.txt file, …"), presented ("so the result can print…") as the continuation of the limits-li sentences "A page that's disallowed…" / "we might still find…"; the anchor-text claim is supported by a different, unquoted li sentence ("As a result, the URL address and, potentially, other publicly available information such as anchor text…") | `python3 .files/analyze_s429.py` (node 26 vs 49/50) + §5/§6 | Attribute the quote to the table cell (or quote the li's own 25-unit "As a result…" sentence for the address/anchor-text claim) |
| med | corpus/knowledge/robots-txt-limits.md:96-101 | Quote reallocation: "If you want to hide the page completely from Search" is the section-1 Web-page table cell ("…use another method."), yet "The opening section… sends a publisher…"; and the remedy triple that follows (password protection / `noindex` meta tag or response header / removing the page entirely) is the limits-li `#robotted-but-indexed` list, not the opening section and not that cell (cell names only "password protection or noindex"; "remove the page entirely" is unlinked text there absent) | §4 intro nodes 0-11 vs §5 r1c1 vs §6 li; `grep -n 'hide the page completely' S429.html` (1 hit) | State each quote's location: intro ("it is not a mechanism…"), table cell (hide sentence), limits li (remedy list) |
| low | corpus/knowledge/robots-txt-limits.md:62 | "The syntax limit is a second, separate paragraph" — it is the third `<li>` of a four-item bulleted `<ul>` (enforcement is the second item); nothing here is a paragraph | `grep -c '<li>' ` limits ul slice, §6 | "a third bulleted limit with its own bolded lead" |
| low | corpus/knowledge/robots-txt-limits.md:85 | "The same table warns…" — no table is introduced anywhere in the entry, and the two preceding quotes in that section are from the limits `<li>`, not the table; the quote is the table's Media-file row | §5 r2c1 | "The page's file-types table warns…" |
| low | corpus/knowledge/robots-txt-limits.md:9 | h1 called "page chrome": `<h1 class="page-title">` sits INSIDE the devsite-article-body block (offset 137273 > marker 137194) — it is the article's own title (and A1 makes article-block h1s anchor-eligible); sibling S428 entry uses "article `<h1>`" | §1 offsets; `grep -o 'class="page-title"[^>]*' S429.html` | "the article block's own `<h1>`" |
| low | corpus/knowledge/robots-txt-limits.md:21,25-26 | "None of that is repeated here." is contradicted by the H1 ("A robots.txt states a preference a crawler may ignore") and point 1, which restate the advisory-character reading `robots-txt-rules.md:9` holds from RFC 9309 §§1,3 (re-grounded on S429, but restated); point 2's gloss also drops the page's modal: "some do not understand every instruction" vs "some might not understand certain instructions" | `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 8b33fd2…:corpus/knowledge/robots-txt-rules.md` (§ Scope) + entry lines 21, 25-26 | "re-stated in the engine's own words below" (or drop the sentence); restore "might" |

Gaps / residual risk: no live fetch (retained body is the evidence base; recheck grep run against it
only); `c60_quote_truth.py` not executed — unnecessary here, since every C5-relevant property of
this entry passed my independent extraction (§1), but the C3 9/9 verdict itself is the L1's to
measure; S427/S428 entries and the other C3 artifacts are other seats' scope and unreviewed here.
No pacman/install performed; no lane mutation (report + .files only); scratch deleted.

VERDICT: Entry and refusals are page-faithful at B1 — 15/15 spans verbatim, page-unique, single-node, and all 15 refusals honoured — but three quotes are reallocated across two document locations (table vs limits li) and the limits list is misdescribed as paragraphs: six findings, none touching quote truth itself.
