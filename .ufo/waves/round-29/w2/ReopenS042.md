# ReopenS042 — round 29 wave 2, freshness (falsify)

Attacked: row S042 (corpus/SOURCES.md:50) and every line citing S042, at lane commit 7697990cbca20291f3b0367b8ff4220e93b38b03. I read committed bytes from a sandbox clone; the lane is untouched except this report. Installs: none; used the system curl, git and python3.

## Commands and exit codes
- git clone -q <lane> <sandbox>/clone; git checkout -q 7697990… → exit 0; HEAD 7697990…; status clean.
- curl -sS --max-time 60 -D raw/headers.txt -o raw/page.html -w 'HTTP=%{http_code} URL=%{url_effective} BYTES=%{size_download}\n' https://jekyllrb.com/docs/liquid/filters/ → exit 0; `HTTP=200 URL=https://jekyllrb.com/docs/liquid/filters/ BYTES=40985`. This was the only network request. curl sent its default User-Agent, not the author's; the bytes still match the receipt.
- python3 -B hash and text check (fetch_sources.py visible-text rule) → exit 0.
- python3 -B .ufo/waves/round-29/c1_quote_truth.py --root . --revision 7697990… → exit 0; `C1 4/4`; controlBroken false.
- git grep -n -e S042 7697990… -- corpus README.md PROVINCE.md SKILL.md → exit 0.
- Sandbox-only mutation: "Prepend" → "Prepand" in corpus/lessons/round-29.md:38, committed as a3f2dc6d… by plumbing → counter exit 1; `C1 3/4`; S042 d_quote_in_retained_text false.
- git cat-file -t 609e6777… and 1f9ffdc… → not found (non-zero exit).

## Freshness evidence
- Live body sha256 610d127b… equals receipts.json S042 bodySha256; 40985 bytes equals bodyBytes.
- Live visible-text sha256 b66fefc1… equals receipts textSha256 and the retained .ufo/waves/round-29/sources/S042.txt. The retained file is byte-equal to my live text (9266 bytes, 1432 words).
- Origin headers: last-modified Tue, 13 Oct 2026 18:44:50 GMT; etag "6ace7c22-a019" (hex a019 = 40985); Date Thu, 22 Oct 2026 11:17:30 GMT.
- Cache caveat: cache-control max-age=600; x-cache HIT; age 0; Expires 10:36:12 GMT, earlier than Date. The body may be a cached copy; the headers do not prove origin currency beyond that.
- Version: the page header reads "v4.4.1" (raw HTML). Whether 4.4.1 is the newest Jekyll release was not checked; no other GET was permitted.

## Row S042 (corpus/SOURCES.md:50)
- id, source URL, kind docs, tier A: HOLDS. URL equals receipt url and finalUrl; no redirect.
- scope: HOLDS. Page: "This is recommended for a site that is hosted on a subpath of a domain."
- anchor "Standard filters table, the Relative URL and Absolute URL rows": BROKEN (label). "standard filters" occurs 0 times, any case. The rows sit in the page's only table (raw HTML offset 7333), under <h1>Liquid Filters, with headers "Description" and "Filter and Output". Anchors: #relative-url (offset 7549), #absolute-url (offset 8084). The "Standard Liquid Filters" heading (h3, id standard-liquid-filters) introduces a name list that omits both filters. The quotes are right; the label is wrong.
- teaches: HOLDS. "Prepend baseurl config value to the input to convert a URL path into a relative URL." and "Prepend url and baseurl values to the input to convert a URL path to an absolute URL."
- "Jekyll v4.4.1 docs", fetched and opened 2026-10-22, status mined, recheck 90d: HOLDS as far as the page shows; see the version caveat.
- used-by (pages-base-path.md, lessons/round-29.md): HOLDS; both cite S042. corpus/README.md:253 and SKILL.md:712-714 also cite it and are not listed. No written used-by rule was found in corpus/QUALITY.md or corpus/README.md (grep).

## Entry lines citing S042 (corpus/knowledge/pages-base-path.md)
- L1 source header, S042 URL: HOLDS.
- L2 verified-at, "S042 b66fefc1…": HOLDS; the prefix matches the full hash.
- L14 "Liquid URL filters driven by `baseurl` for Jekyll (S041, S042)": LIMIT. S042 says absolute_url prepends "url and baseurl values"; "driven by baseurl" understates it.
- L33 relative_url quote and worked example: HOLDS. Both quote sentences occur in the live and retained text. `{{ "/assets/style.css" | relative_url }}` → `/my-baseurl/assets/style.css` is one table row (offset 7549).
- L34 absolute_url quote and worked example: HOLDS. The quote is found; `{{ "/assets/style.css" | absolute_url }}` → `http://example.com/my-baseurl/assets/style.css` is in the same table (offset 8084). The host is a documentation placeholder.

## Other lines citing S042
- corpus/lessons/round-29.md:38 (gate): quote HOLDS (counter checks c and d pass). Locator "Standard filters table": BROKEN, as in the row.
- corpus/lessons/round-29.md:85 (mutation claim): mechanism HOLDS on my reproduction (3/4, exit 1). The two commits it cites are absent from the lane: NOT VERIFIED.
- corpus/SOURCES.md:52 (S044 row): "the relative_url filter that S042 recommends for subpath hosting": HOLDS.
- corpus/SOURCES.md:54 (S046 row): "already carried by S041 and S042": HOLDS.
- corpus/SOURCES.md:70 (Paths line): "the filters that prepend that base to a path": HOLDS.
- corpus/README.md:253: "the Liquid relative_url and absolute_url filters that prepend the baseurl (S042)": LIMIT, as L14.
- SKILL.md:712: "write the reference through relative_url (S041, S042)": HOLDS.
- SKILL.md:713: "relative_url prepends the baseurl config value (S042)": HOLDS.
- SKILL.md:714 (S042 in the sources cell of a custom-domain and repository-name row): BROKEN, low: over-citation. S042 has 0 hits for "custom", "custom domain", "repositor", "user site", "project site", and "CNAME".

## Adjacent finding (outside the target lines)
- corpus/knowledge/pages-base-path.md:32: "`relative_url` for assets with static names, `absolute_url` for page URLs that can change (S041)." BROKEN, misattributed. Retained S041.txt has 0 hits for absolute_url. Its "For documents/pages whose URLs can change" example uses `{{ page . url | relative_url }}` (offsets 2030, 2161). The S041 registry row (SOURCES.md:49) says the page "says nothing about absolute_url".

## Residual risk and gaps
- Not verified: Jekyll 4.4.1 currency; live GitHub Pages behavior; the two lesson:85 commits; mutation-fixture copies under .ufo/waves/round-29 (not corpus lines, not scored).
- Only the C1 counter and my sandbox probe ran. No lane file changed.
