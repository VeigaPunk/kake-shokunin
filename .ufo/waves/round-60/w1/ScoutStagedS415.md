# ScoutStagedS415

C3 assimilation screen: staged entry `merge/kake/knowledge/corpus/knowledge/google-robots-txt-limits.md` + staged row S415
(`merge/kake/SOURCES.append.md:135`) screened sentence by sentence against retained body `.ufo/waves/round-60/sources/S429.html`
(collapsed article text, `class="devsite-article-body` .. `<devsite-content-footer`, extracted with the round-59 counter's
`content_window`/`text_segments` code verbatim). Span counts are raw `body.count()` over the whitespace-collapsed file;
`in-window` means inside the article block.

Article facts (S429): `<title>` before ` | ` = `Robots.txt Introduction and Guide`; article H2/H3s = "What is a robots.txt
file used for?", "Understand the limitations of a robots.txt file", "Create or update a robots.txt file" (the two limits the
entry cites are `<dt>` items under the limitations H2, not headings); `Last updated 2025-12-10 UTC.` inside
`<devsite-content-footer`. `How robots.txt works` occurs 0 times anywhere in the body.

SENTENCES:

Entry header lines:
- `source: S415 — <url> — § How robots.txt works → the limits the page states on the file — Last updated 2025-12-10 UTC —
  fetched 2026-10-24` — URL and `Last updated` supported; `§ How robots.txt works` unsupported (count 0, wrong section name;
  the limits sit under § "Understand the limitations of a robots.txt file"); `fetched 2026-10-24` stale vs round-60 access date
  2026-10-27; `S415` correctly renumbered S429 by document (contract).
- `verified-at: 2026-10-24` — lane header field, stale date (must be 2026-10-27).
- `recheck: 180d — curl … grep -F -c 'Different crawlers interpret syntax differently.' -> 1 (ran 2026-10-24)` — the grepped
  sentence is page-unique (count 1, in a single text node); ran-date stale.
- `ground: per-host crawl hygiene — the western first-party statement … beside the Baidu and Yahoo refusals this lane already
  holds` — lane meta-prose + cross-document attribution (lane-held Baidu S424 and Yahoo S372/S418 rows exist in corpus/SOURCES.md);
  `western`/`Baidu`/`Yahoo` count 0 in S429 (expected — naming the lane's other traditions, not the page).
- H1 `The file states a preference, and each crawler reads it its own way` — supported paraphrase of the two `<dt>` limits.

Body sentences:
- S1 `The lane holds the refusal-file rules from three directions now, and this is the western one:` — lane meta-prose.
- S2 `the operator's own documentation of its own crawler, in the same tradition as Baidu's robots Q&A and Yahoo! JAPAN's
  refusal-file page.` — lane meta-prose + cross-document attribution.
- S3a `a robots.txt file tells search engine crawlers which URLs they may access on a site` — supported: `A robots.txt file
  tells search engine crawlers which URLs the crawler can access on your site` (count 1, one text node). "expected one" is
  editorial.
- S3b `The two limits are the useful part, and neither is usually stated this plainly.` — lane meta-prose (count 0; the two
  limits are real `<dt>` items).
- S4 `the instructions in the file cannot enforce crawler behaviour … obeying is the crawler's choice, and while this
  operator's crawlers obey, other crawlers might not, so a site that needs real protection has to use other blocking methods`
  — supported: `The instructions in robots.txt files cannot enforce crawler behavior to your site; it's up to the crawler to
  obey them.`, `While Googlebot and other respectable web crawlers obey the instructions in a robots.txt file, other crawlers
  might not.`, `it's better to use other blocking methods` (each count 1, same node).
- S5 `different crawlers interpret the syntax differently — respectable crawlers follow the rules, but each does it its own
  way, and some do not understand every instruction` — supported: `Different crawlers interpret syntax differently.`,
  `each crawler might interpret the rules differently`, `some might not understand certain instructions` (each count 1).
- S6 `Baidu documents the same three fields and their prefix semantics from the crawler side, and Yahoo! JAPAN tells a server
  administrator to identify a crawler by the address its DNS points at` — cross-document attribution (count 0 in S429;
  attributes S424 and S372/S418 content, not this page).
- S7 `a refusal file is a request made of each crawler separately, so a publisher's rule has to be stated per crawler, and it
  is never a security control` — synthesis supported by the page's two limits; the literal phrases are authorial
  (`per crawler` count 0, `security` count 0 in article — the page says `keep information secure` / `other blocking methods`).
- S8 `A site that treats one robots.txt as one global switch is relying on behaviour that only one operator has promised.` —
  supported-in-substance inference (`other crawlers might not` obey; `robots.txt rules may not be supported by all search
  engines`, count 1); the "one global switch" framing is authorial [INFERENCE].

Row S415 teaches cell: `a robots.txt file tells search engine crawlers which URLs they may access` (supported, see S3a),
`the instructions in it cannot enforce crawler behaviour because obeying is the crawler's choice` (supported, see S4),
`different crawlers interpret the syntax differently` (supported, count 1), `one file is read differently by each crawler`
(supported by S5 spans), `not a security control` (authorial paraphrase of the secure/blocking-methods clause), `a publisher's
rule has to be stated per crawler rather than once` — unsupported (count 0; conclusion drawn from the limits).

ROW DEFECTS:
- Wrong anchor: row cell `§ How robots.txt works` and entry `source:` § ref name a heading absent from the page (count 0);
  the two limits are the `<dt>` items under H2 `Understand the limitations of a robots.txt file`.
- Stale dates: row `opened` = `2026-10-24` and recheck `(ran 2026-10-24)`, entry `verified-at`/`fetched`/`ran` = 2026-10-24;
  contract requires 2026-10-27 (round access date). Page `Last updated 2025-12-10 UTC` is correct as printed.
- used-by/filename: `corpus/knowledge/google-robots-txt-limits.md` is the staged name; contract lands the entry as
  `corpus/knowledge/robots-txt-limits.md` and forbids the staged name (C1).
- No census defects: 11 logical cells; the single `\|` inside the backticked recheck command is the same escaped-pipe
  convention staged rows S287/S289/S290/S302 use; no unescaped pipe inside any cell; status `mined`; grade `A`; title cell
  matches `<title>`; recheck is a runnable curl|grep, not bare prose, and its grepped sentence is page-unique.
- Teaches tail clause `stated per crawler rather than once` has no page span (count 0).

KEPT:
- Both limits verbatim-supported: `cannot enforce crawler behavior` / `it's up to the crawler to obey` / `use other blocking
  methods`, and `Different crawlers interpret syntax differently` / `each crawler might interpret the rules differently` /
  `some might not understand certain instructions`.
- Definition sentence (S3a), the "not a security control" conclusion (as paraphrase of `keep information secure` /
  `other blocking methods`), `robots.txt rules may not be supported by all search engines` (available third span).
- Recheck command shape and its grepped sentence; `Last updated 2025-12-10 UTC`; URL; title; `mined | A`.
- Carry to the re-grounded entry: rename file, renumber `source: S415` → `S429`, fix anchor to the limitations H2, normalize
  all dates to 2026-10-27, and either drop or rephrase the unsupported `per crawler` teaches tail; sentences S6–S8 must keep
  their attribution marks (they attribute Baidu/Yahoo lanes, not S429).

VERDICT: Staged S415 is substantially faithful to S429 — every factual claim traces to a page-unique article span — but needs the wrong anchor (§ How robots.txt works → § Understand the limitations of a robots.txt file), stale 2026-10-24 dates, the staged filename, and one unsupported teaches clause fixed before append.
