# ScoutReopenS094 — S094 (MDN "Redirections in HTTP") re-opened live and judged

No sealed-key tree touched; no lane file mutated; only this report written in the lane.

## Fetch (ordinary means, GET only)
Sandbox `/fast/scratch/hyaku/kake-r36w1/ScoutReopenS094/`, `TMPDIR` inside it.
```
curl -sSL -A 'shokunin-recheck/1.0 (research audit; contact: local)' -o s094.live.html \
  -w 'http=%{http_code} final=%{url_effective} type=%{content_type} size=%{size_download} redirs=%{num_redirects}' \
  https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Redirections      # exit 0
```
Observed: `http=200 final=https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Redirections type=text/html size=228453 redirs=0`; header `date: Fri, 23 Oct 2026 01:35:25 GMT`, `last-modified: Fri, 23 Oct 2026 01:05:43 GMT`, `etag: "2ab5384a724101722d84d51dd928bcbd"`.

Body sha256 `4c73d89cf7b0d6c73e4c5846fb36a72ba29c29c5592d84474ce4130fbf9c854d` = `receipts.json["S094"].bodySha256` (byte-identical to the 01:09:01Z retained body). Text regenerated with the receipts' `textRule`: 2865 words; word sequence identical to retained `S094.txt` (`difflib` opcodes: none differ); retained `S094.txt` sha256 `458c6cc9…b8911208` = `textSha256`; my re-extraction differs only by a trailing newline (`46caa4f3…`). So no content drift and no extractor drift.

## The two quotes the ticket asks for (live text = `S094.txt`, offsets/word numbers)
Permanent (offsets 3158 / 3317, words 479 / 505):
> "Permanent redirections These redirections are meant to last forever. They imply that the original URL should no longer be used, and replaced with the new one. Search engine robots, RSS readers, and other crawlers will update the original URL for the resource."

Temporary (offset 4098, word 630), covering 302/303/307:
> "Search engine robots and other crawlers don't memorize the new, temporary URL."

Method/permanence table rows (301 "GET methods unchanged. Others may or may not be changed to GET"; 308 "Method and body not changed") restate S088 §15.4.2/§15.4.9 and §15.4.3/§15.4.8; the 307/308 rationale ("was created to remove the ambiguity … when using non-GET methods") restates S088 §15.4's POST-to-GET note.

## Additions vs RFC 9110 (S088), against the C1 contract
Bullet (b) needs exactly one predicate per hop: is it permanent? The permanent set is `{301, 308}`, stated positively in S088: §15.4.2 "has been assigned a new permanent URI and any future references to this resource ought to use one of the enclosed URIs" (S088.txt 320714, word 51705) and §15.4.9 heading + same sentence (327146). "302, 303 and 307 are temporary" is then the complement; S088 also says 302 and 307 "resides temporarily" (321977, 326520). So the rule is fully determined by S088.
- Only genuinely new bit: MDN files **303 under "Temporary redirections"**. S088 §15.4.4 uses neither "temporary" nor "permanent" (checked the whole 15.4.4 segment: both words absent) and only says the new URI "is not considered equivalent to the target URI". A tool can still implement bullet (b) from S088 alone because permanence is a positive property; 303's membership is needed only if a case turn on a positive citation for it.
- Not needed at all: the crawler/feed-reader sentences (no rule emulates a crawler), the order of precedence of HTTP vs JavaScript vs `<meta>` (contract manifests carry only HTTP hops, offset 7116), and the 300/304 "special" framing (contract's redirect set is five codes).
Verdict on the question: **restates S088, plus one unused-by-rule classification (303) and one crawler-behavior assertion**. It adds nothing the re-check needs.

## Conflicts with RFC 9110 (both located)
1. Blanket 3xx definition. S094 (offset 2711, word 413): "Redirect responses have status codes that start with 3, and a Location header holding the URL to redirect to."
   S088 §15.4.5 (325972, word 52597): "A 304 response is terminated by the end of the header section; it cannot contain content or trailers." — and its MUST-generate list (Content-Location, Date, ETag, Vary; Cache-Control, Expires) contains no Location. S088 §15.4.1 (318942, word 51421): "If the server has a preferred choice, the server SHOULD generate a Location header field …", i.e. optional for 300. 305/306 are deprecated/unused 3xx. This is the conflict that matters: it is on the exact bullet it would be cited for. A tool that took it literally would treat any 3xx as a hop needing `location`, whereas bullet (b)/(g) makes only 301/302/303/307/308 hops and calls every other status a final outcome.
2. Strength of the crawler claim. S094 (3317): "Search engine robots, RSS readers, and other crawlers will update the original URL for the resource."
   S088 §15.4.2 (320834 / 321019, words 51727 / 51757): "The server is suggesting that a user agent with link-editing capability can permanently replace references to the target URI with one of the new references sent by the server. However, this suggestion is usually ignored unless the user agent is actively editing references (e.g., engaged in authoring content), the connection is secured, and the origin server is a trusted authority for the content being edited."
   Not a contradiction of the code's meaning (crawler indexing is outside HTTP semantics, which S088 does not address), but S094 asserts as certain what S088 explicitly hedges, and its RSS-reader clause — the one line this lane would care about, since feed readers carry stale URLs — has no primary behind it. Minor third: 304 "redirects a page to the locally cached copy (that was stale)" (5079) reads against §15.4.5's "would have resulted in a 200 (OK) … the client … already has a valid representation"; S094's own table row says "still fresh", so it is loose prose, not a rival rule.

## Recommendation: reject (tier B if kept, narrowly scoped)
Location: the page's permanent/temporary grouping restates S088 §15.4.2-§15.4.9, and its only distinct generalisation, "3xx and a Location header", is contradicted by S088 §15.4.5 (304 has no content; Location is not among its required fields) and §15.4.1 (Location is SHOULD for 300) — on the very bullet (b) it would be cited for.
`REJECTED: restates RFC 9110 section 15.4 (S088) for the only rule the re-check needs, the permanent set {301,308}; its distinct generalisation that every 3xx carries a Location is contradicted by S088 15.4.5 (304 has no content and no Location) and 15.4.1 (300 Location is SHOULD), and its crawler/feed-reader permanence is a strength claim S088 15.4.2 hedges with "this suggestion is usually ignored"; flip: a C1 case turns on a positive citation for 303's group membership, or MDN restates crawler behaviour as S088 does and drops the blanket 3xx/Location sentence.`
If the L1 prefers to keep a row for the 303 bit: tier B, scope "MDN's grouping of 3xx into permanent and temporary groups; not HTTP semantics where S088 governs, not crawler behaviour, and not a statement that every 3xx carries Location", anchor "Permanent redirections / Temporary redirections sections, offset 3158-4300; fetched 2026-10-23T01:34Z, body sha256 4c73d89c…f9c854d", recheck 90d.

## Not verified / residual unknowns
- Did not check MDN's page history or the CC-licensed source of the crawler sentence; the conflict is recorded as text-vs-text.
- Did not test whether any sealed case uses a 303-led chain (no key; that would decide the narrow-admit alternative).
- Nothing installed or upgraded. No processes left running.
Artifacts: `/fast/scratch/hyaku/kake-r36w1/ScoutReopenS094/{s094.live.html, s094.live.txt, headers.txt, live.headers, receipt.json, extract.py}`.
