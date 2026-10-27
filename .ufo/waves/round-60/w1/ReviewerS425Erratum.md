# ReviewerS425Erratum

Scope: routed defect R59-D4 (S425 `scope` cell overstates robots.txt posture). Evidence opened: base registry row `corpus/SOURCES.md:171`; retained bodies `.ufo/waves/round-59/sources/S425.html` (74,477 B, sha256 `ff2b9fd7…f5caa`) and `.ufo/waves/round-60/sources/S427.html` (74,477 B, sha256 `d70ce6f5…82175`, fetched 2026-10-27T04:03:36Z). The article blocks (`class="devsite-article-body` .. `<devsite-content-footer`) are byte-identical between the two fetches (verified by extraction+compare), so every finding below holds for both. Span truth via the round-59 helper `span_tools.py check S425` (the counter's own node code); round-60 bodies re-counted with the same whitespace collapse.

POSTURE SENTENCES:
The article's only robots.txt content is the `crawler-types` category table (S425.html = S427.html, lines 1094-1120); every other `robots.txt` match is sidebar-nav href text (lines 738-748, outside the article block). Per category:

- Common crawlers — posture stated, categorical.
  "They always respect robots.txt rules for automatic crawls." — span_tools: units 8, chars 58, in_text_node True, count_in_body 1. The text node opens `). They always…`; the subject sits in the previous node after the Googlebot link, so the sentence is quotable only without its subject.
- Special-case crawlers — posture stated only as one named example (permissioned exception, not a general rule).
  "ignores the global robots.txt user agent" — units 6, chars 40, in_text_node True, count_in_body 1, unique True. Subject `AdsBot` and tail `(*) with the ad publisher's permission.` sit in separate nodes around `<code>` spans; the full sentence is multi-node and cannot be quoted whole — the Gate must name AdsBot outside the quote.
- User-triggered fetchers — NO robots.txt statement anywhere in its row.
  "User-triggered fetchers are part of tools and product functions where the end user triggers" — units 14, chars 91, in_text_node True, count_in_body 1, unique True. The cell names tools (Site Verifier) and a user request; no posture. Article-wide `robots\.txt` grep confirms no other mention.

So the overview states a posture for two of the three categories — common crawlers as a general rule, special-case crawlers via the AdsBot example — and none for user-triggered fetchers. That is exactly the R59-D4 gap: S425's scope clause "the three crawler categories and their robots.txt posture" claims the page says something it does not say. The missing sentence lives on S428: "Because the fetch was requested by a user, these fetchers generally ignore robots.txt rules." (S428.html:1086-1087; one collapsed article text node, count 1, units 14, chars 92).

Uniqueness note: span_tools' `unique` flag is computed across the round-59 pair (S425+S426); the common-crawlers span is flagged False only because S426 embeds the same category table (count 1 in each). Against the round-60 set all three S427 spans count S427:1, S428:0, S429:0 — page-unique under the C5 rule.

OTHER OCCURRENCES:
No other S425-citing file repeats the overstatement.

- `corpus/knowledge/crawler-identity-signals.md` (S425 used-by): zero matches for `robots` and `categor` in the whole file — it covers signals, fleet distribution and egress only.
- `corpus/knowledge/crawler-identity.md` (S425 used-by): its robots.txt lines (25-27, 55-57) are S263-scoped (Googlebot Smartphone/Desktop subtypes obey the same product token) — a different subject; no three-category posture claim.
- S425's `teaches` cell itself is clean — the overstatement lives only in the `scope` cell (verified by cell extraction).
- Lane-wide grep `robots\.txt posture|three crawler categories`: hits only in the defective row (SOURCES.md:171), its evidence copies (round-59 `w1/ScribeRegistryGate.md:8` + `rows.md`), the defect record (`corpus/lessons/round-59-verifier-spotcheck.md:102,142-143`), and the round-60 contract/spec texts that mandate the fix. `corpus/README.md:77` summarizes the S425 entry with no posture claim.

FIX FORM:
Superseding row is the right form; the contract's choice (S427) is correct.

- CORPUS.md SOURCES rule 2 (CORPUS.md:116-118): registry is append-only — only `status`, `recheck`, `used-by` change in place, each logged old→new in the round lesson; "A correction is a new row whose `teaches` opens `supersedes S0NN —`." The `scope` cell is not in the editable-in-place set, so a lesson-only erratum would leave the standing row asserting a posture the page does not give, to every future reader and census consumer of the registry. Rule 2's mechanism exists for exactly this case.
- The round-59 spotcheck itself offered both forms ("Correct by an appended superseding row or a scoped erratum in the next lesson (registry is append-only)", spotcheck §6 R59-D4). Between them the row form adds: machine-checkability (contract C3 pins S427's scope: must not contain `their robots.txt posture`, must contain `common crawlers` and `special-case crawlers`) and a fresh pinned receipt (S427 fetched 2026-10-27, sha256 in `sources/receipts.json`), which prose cannot carry. A lesson-only erratum remains the fallback only if the row form were blocked; it is not.
- Census acceptance: yes, a same-URL row passes. E04 (`scripts/sources-census.sh:645-652`) fires only when the same URL+scope already has a non-rejected row AND `teaches !~ /supersedes S[0-9]{3}/`; S425 (mined) sets `url_scope_nonrejected`, so S427 without the tag would trip E04, but `supersedes S425` matches the exemption regex `[0-9]{3}`. Both allowed shapes pass `validate` with exit 0: (a) scope cell byte-identical + tag → no E04, no W04; (b) scope cell corrected (what the contract requires) → new scope key → E04 inapplicable, one W04 `duplicate url across scopes` warning, which the script documents as non-failing ("exit: 0 clean or warnings"; "warnings do not affect clean lanes"; precedent: 14 pre-existing W04 at round-59 build). E03 not applicable (new id); E11 makes `corpus/lessons/round-60.md` (S427 used-by) a must-exist path at validation time.
- Constraints for the appending seat: leave S425 untouched (`mined` stands; the enum has no superseded status — the pointer lives in S427's teaches); log the old→new in the round lesson per rule 2; keep the accurate remainder of S425's scope (three signals, fleet distribution — both verified true in round 59) and narrow only the posture clause; S427's anchor/`Last updated` re-pin on the re-fetched body.

VERDICT: Overstatement confirmed — the overview states robots.txt posture for common crawlers ("always respect… automatic crawls") and special-case crawlers (AdsBot example) only, none for user-triggered fetchers; no citing entry repeats it; superseding row S427 (rule 2, `teaches` opens `supersedes S425 —`) is the correct, census-accepted fix — proceed.
