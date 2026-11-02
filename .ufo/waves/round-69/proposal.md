# Round 69 proposal — before implementation

Base 4c48bf24eb1033748e444480820ed3262684ad35. One claim C1 on calibration
(lowest non-retired, score HOLD2): acquire a bounded offline Google text-result
noindex evidence-triage capability, separating applicable declaration,
crawl-inaccessible declaration, no applicable declaration, and unevaluable
input. This is publisher preparation, not indexing observation or deployment.

Gap search: `grep -n -i 'noindex\|robots meta' corpus/SOURCES.md` finds CrUX
eligibility and Yahoo link-target rules, not this combined Google triage.
Existing robots_audit.py reads robots access; header_audit.py only reads
response-header expectations. Neither claims an indexing outcome.

Proposed input is a strictly keyed JSON record of manually extracted evidence:
version=1, resource=html|non-html, context=standalone|embedded|unknown,
access=allowed|blocked|unknown, declarations=[{channel:meta|header|robots_txt,
target:string, tokens:[strings], placement:head|body|na}]. Only Google text
results; header target empty means unqualified, meta target robots is generic;
googlebot is applicable, other targets are ignored. Structured tokens are not
raw header parsing. Only noindex, none, index, all, follow, nofollow, nosnippet
are within the bounded evaluator; any applicable unrecognized token is
unsupported, not a claim that Google ignores it. Embedded/unknown contexts
are unevaluable (indexifembedded prevents extrapolation).

Decision order: schema error -> input_invalid exit2; unsupported context or
applicable unsupported token -> unsupported exit2; no applicable noindex or
none -> no_applicable_noindex exit1; access blocked -> crawl_blocked exit1;
access unknown -> access_unknown exit2; otherwise declaration_supported exit0.
Every output includes index_state=not_observed, publication_authorized=false.
Access is supplied evidence, not measured by the tool. No HTML/HTTP parser,
robots matching, browser, account, crawl, search result, indexing or publication.

Freeze plan: commit contract plus cases and counter before implementation;
measure absent-tool at base as unavailable, not 0% expertise. Test fixed cases,
ID/permutation metamorphisms and cheap constant/keyword-only stubs. Independent
review must judge source semantics and add held-out cases, including admits and
rejects; finite tests cannot prove universal semantics. Kill C1 if a cheap stub
meets the target, source mapping is false, or any required case fails.

No-harm: byte-identical old scripts/counters/receipts; old corpus bytes preserved;
source census before/after; full offline sweep compare finding identities,
not exit alone, preserving inherited red misses; c66 member-by-member compare
on cloud with /usr/bin/python3 --jobs1 when resource clearance arrives. No exact
Windows agreement18 or clean sweep assumption. No new failures allowed.

Pre-freeze reviewer clarifications (2026-11-02): body and head both count for
HTML; meta on non-HTML is ignored (only header supplies this channel). Negative
rules accumulate across generic and crawler-specific declarations; index never
cancels noindex. Strip only ASCII SP/HTAB and ASCII-lowercase targets/tokens;
reject non-ASCII strings. Target after stripping is an ASCII letter followed by
ASCII letters/digits/underscore/hyphen, or empty ONLY for header. This grammar
is local extraction schema, not Google's wire grammar. Meta placement must be
head/body; header/robots_txt placement must be na. Tokens must be nonempty
printable ASCII strings after trimming; punctuation-bearing unknown tokens
are unsupported if applicable, not silently split. Empty token lists allowed.
Unknown keys, wrong types, bool version, duplicate keys, nonfinite JSON,
missing fields, invalid combinations -> input_invalid. Unknown resource,
context or access enum -> input_invalid. Irrelevant-target or robots_txt
unknown tokens do not affect applicable declarations. Unsupported context
wins over absence; applicable unknown tokens win over known noindex.
