# ScoutReopenS089 — S089 (RFC 3986) re-opened live, independently

No sealed-key tree touched; no lane file mutated; only this report written in the lane.

## What I did
Fresh GET (ordinary means, UA `kake-r36-scout/1.0 (source freshness recheck)`), sandbox
`/fast/scratch/hyaku/kake-r36w1/ScoutReopenS089/`.

```
curl -sS -L --max-time 100 -o rfc3986.html -w 'http_code=%{http_code} size=%{size_download} url=%{url_effective}'
  https://www.rfc-editor.org/rfc/rfc3986.html          # exit 0
```
Observed: `http_code=200 size=171264 url=https://www.rfc-editor.org/rfc/rfc3986.html` (curl exit 0).
Response headers (`-D headers.txt`, second GET, exit 0): `HTTP/2 200`, `date: Fri, 23 Oct 2026 01:35:58 GMT`,
`content-type: text/html` (**no charset parameter**), `etag: W/"4f71f5a6ddb07d721c167df65994f23c"`,
**no `last-modified`, no `cache-control`, no `age`**. No redirect (single hop).
Body sha256 `28869fb6d1a48e86b4faaf03f9f1b1391ecd191cc619a51931a04cfaf328caac`, 171264 bytes.

## Comparison with the retained copy — byte-identical, not merely similar
1. Body: `gunzip -c .ufo/waves/round-36/sources/S089.html.gz | sha256sum` =
   `28869fb6d1a48e86b4faaf03f9f1b1391ecd191cc619a51931a04cfaf328caac` = my live body.
   `cmp retained.html rfc3986.html` → exit 0 (no output). `diff -u retained.html rfc3986.html` → exit 0, **0 bytes**.
   `receipts.json["S089"]`: `bodySha256` `28869fb6…`, `bodyBytes` 171264, `accessedUtc` `2026-10-23T01:08:57Z`, `status` 200 — agrees.
2. Text: regenerated with `fetch_sources.py::visible_text` (same regexes) from my live body →
   sha256 `656b0d769d8f5446cee8ad984e39f1db2089697fd373898dae95d7d0e9054ba7`, 20809 words.
   `cmp mine.txt S089.txt` → exit 0; `diff -u S089.txt mine.txt` → exit 0, **0 bytes**.
   Equals `receipts.json["S089"].textSha256`. **No content drift between 01:08:57Z and 01:35:58Z (~27 min); nothing changed.**

## Verbatim sentences from my own fetch (my `mine.txt` offsets)
§5.2 Relative Resolution [69835:70000]:
> "This section describes an algorithm for converting a URI reference that might be relative to a given base URI into the parsed components of the reference's target."

§5.2.2 Transform References [71085…]:
> "For each URI reference (R), the following pseudocode describes an algorithm for transforming R into its target URI (T):"
> (pseudocode) "T.path = remove_dot_segments(T.path);" … "T.fragment = R.fragment;"
> (comment lines, which keep their `--` prefix after whitespace collapse) "-- A non-strict parser may ignore a scheme in the reference -- if it is identical to the base URI's scheme."

§5.2.4 Remove Dot Segments [72998…]:
> "The pseudocode also refers to a \"remove_dot_segments\" routine for interpreting and removing the special \".\" and \"..\" complete path segments from a referenced path."
> step 2A: "If the input buffer begins with a prefix of \"../\" or \"./\", then remove that prefix from the input buffer;"
> step 3: "Finally, the output buffer is returned as the result of remove_dot_segments."

§5.4.1 Normal Examples [77118…]: `"g" = "http://a/b/c/g"`, `"//g" = "http://g"`, `"../g" = "http://a/b/g"`, `"../../g" = "http://a/g"`.
§5.4.2 Abnormal Examples [77736…]: `"../../../g" = "http://a/g"`, and
> "\"http:g\" = \"http:g\" ; for strict parsers / \"http://a/b/c/g\" ; for backward compatibility".

Boilerplate (observed): `STD: 66`, `Category: Standards Track`, `Obsoletes: 2732, 2396, 1808`, `January 2005`. Anchors `id="section-5.2"`, `-5.2.1`…`-5.2.4`, `-5.4`, `-5.4.1`, `-5.4.2` all present, so the retained `finalUrl` fragment `#section-5.2` is valid.

## Falsifier-relevant notes for C1 (advisory)
- **Page-break running headers sit inside the body text.** At §5.2.2 a break inserts `Berners-Lee, et al. Standards Track [Page 31] RFC 3986 URI Generic Syntax January 2005` between the `-- if ((not strict) …` comment and `if defined(R.scheme)`. A quote spanning that point cannot match; quotes must be taken from one page box.
- **The retained text rule leaves spacing artifacts inside quoted examples**: `.txt` has `"g" = " http://a/b/c/g "` (tags→space) while the source `<pre>` has `"g" = "http://a/b/c/g"`. C1 bullet (d) deletes all `isspace()`, so both sides collapse to `"g"="http://a/b/c/g"` — neutralized. A raw-substring matcher (the "naive reader" control) is not neutralized, and only the artifact-free form is quotable.
- **Encoding is a non-issue for this source**: body decodes as strict UTF-8, **0 non-ASCII bytes** (pure ASCII), no BOM; server sends `text/html` with no `charset`, so C1 (f) falls to its "no BOM, no charset → UTF-8" default. Nothing here can exercise the windows-1252/BOM paths.
- **No freshness metadata and no update status on the page**: 0 occurrences of `Errata`/`errata`, `6874`, `7320`, `Obsoleted by`, `Updated by`, `Last-Modified`. A row cannot use this body to prove the source is not superseded, only that it is byte-stable. Freshness must be judged by body hash (the weak ETag `W/"4f71f5a6…"` is the only cache signal).
- **`urllib.parse.urljoin` conforms to §5.2 on all 41 tabulated cases** (5.4.1 + 5.4.2), verified: 0 mismatches. It takes the **lenient** reading of `"http:g"` → `http://a/b/c/g`, not the strict `http:g`. If a sealed case feeds a same-scheme reference like `http:g` as a `location`, a urljoin-based resolver matches the backward-compatibility column and not the strict column — the builder must pick deliberately.
- Candidate quotes verified against the **live** body under C1 bullets (c)+(d) (comments→script/style/template→tags→`html.unescape`, NFKC, delete `isspace`): §5.2 prose, §5.2.2 intro, `T.path = remove_dot_segments(T.path);`, §5.2.4 routine sentence, §5.2.4 step 2A, §5.2.4 step 3, §5.4.1 `"../g"`, §5.4.1 `"//g"`, §5.4.2 `"http:g"` strict line, §5.4.2 dot-segment rule — all **HOLD**. Two deliberate misses that show where a careless row quote dies: a curly apostrophe in "reference’s" (body contains **zero** U+2019; the source is ASCII `'`), and the non-strict comment quoted without its `-- ` prefixes.

## Sandbox artifacts (absolute)
- `/fast/scratch/hyaku/kake-r36w1/ScoutReopenS089/rfc3986.html` (171264 B, sha 28869fb6…), `retained.html` (same sha), `headers.txt`
- `mine.txt` (text rule output, sha 656b0d76…), `sec5_2_prose.txt`, `sec5_2_2.txt`, `sec5_2_4.txt`, `sec5_4_1.txt`, `sec5_4_2.txt`
- `diff_body.txt`, `diff_text.txt` (both empty), `urljoin_check.txt`

## Not verified / residual unknowns
- Did not verify obsoletion/update status against IETF datatracker or an errata page (neither is the named URL; not fetched). The live page itself carries no such metadata.
- Did not fetch `rfc3986.txt` (a different URL than the one my item names) to cross-check the TXT rendering against the HTML.
- Did not run the sealed counter or inspect any sealed path (no key). No claim about the 28 cases.
- No tool installed or upgraded; nothing to record. Two GETs only (one body, one headers), both to rfc-editor.org, not an owned site. No processes left running.
