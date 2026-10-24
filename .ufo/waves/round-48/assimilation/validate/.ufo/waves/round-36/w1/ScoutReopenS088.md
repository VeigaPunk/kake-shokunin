# ScoutReopenS088 — S088 (RFC 9110) reopened live, byte-compared with the retained fetch

Seat KakeR36.ScoutReopenS088 (leaf). Sealed tree untouched; counter not run (no key). No lane file read or written except this report.

## Fetch receipt (mine, independent of the L1's)
- URL `https://www.rfc-editor.org/rfc/rfc9110.html` (no fragment; the receipt's `#section-15.4` is client-side only).
- `curl -sS -D headers-live.txt --compressed -A 'Mozilla/5.0 (X11; Linux x86_64) scout-reopen-check' -o rfc9110-live.html -w ...` → exit 0, `http=200 size_download=212574 time=0.261983`.
- `HTTP/2 200`; `date: Fri, 23 Oct 2026 01:34:53 GMT`; `content-type: text/html`; `etag: "0d9f5fb8eb38d3c08b055f9b0671d68b"` (headers-live.txt:1-6).
- Body 1,187,554 bytes, sha256 `d431760660ea44e130f6e919dab216df2d0b3a490567a98089267523368fe1e5`.

## Verdict: nothing changed since the retained fetch (26 minutes earlier, 01:08:56Z)
```
retained S088.html.gz -> gunzip : 1187554 bytes  d431760660ea44e130f6e919dab216df2d0b3a490567a98089267523368fe1e5
live GET body          ->        1187554 bytes  d431760660ea44e130f6e919dab216df2d0b3a490567a98089267523368fe1e5
live == retained body: True  (cmp of decompressed bytes, not just equal hashes)

retained S088.txt              : 450783 chars  sha256 81c7197438672559e2e6ba2d7cc23ccaccbfc4f5f68ec3be0972238120d0b07a
my text, same rule, + "\n"     : 450783 chars  sha256 81c7197438672559e2e6ba2d7cc23ccaccbfc4f5f68ec3be0972238120d0b07a
common prefix / retained==live+"\n" : 450782 / True
```
So the receipts' `textSha256` and `bodySha256` both reproduce exactly from a fresh fetch; the only difference between retained and live text is the retained file's trailing newline. RFC 9110 is an immutable standard (June 2022) and the rfc-editor rendering is unchanged; the ETag pins the rendering.

## Cited sentences, verbatim from my own fetch (section → quote; retained char offset in S088.txt)
- §15.4, ¶2: "There are several types of redirects: ¶ Redirects that indicate this resource might be available at a different URI, as provided by the Location header field, as in the status codes 301 (Moved Permanently), 302 (Found), 307 (Temporary Redirect), and 308 (Permanent Redirect)." (offset 314647)
- §15.4.2: "The 301 (Moved Permanently) status code indicates that the target resource has been assigned a new permanent URI and any future references to this resource ought to use one of the enclosed URIs." (320639)
- §15.4.9: "The 308 (Permanent Redirect) status code indicates that the target resource has been assigned a new permanent URI and any future references to this resource ought to use one of the enclosed URIs." (327090)
- §15.4.3: "The 302 (Found) status code indicates that the target resource resides temporarily under a different URI." (321961)
- §15.4.8: "The 307 (Temporary Redirect) status code indicates that the target resource resides temporarily under a different URI and the user agent MUST NOT change the request method if it performs an automatic redirection to that URI." (326402)
- §15.4.4: "The 303 (See Other) status code indicates that the server is redirecting the user agent to a different resource, as indicated by a URI in the Location header field, which is intended to provide an indirect response to the original request." — no occurrence of "temporar" anywhere in §15.4.4.
- §15.5.5: "The 404 (Not Found) status code indicates that the origin server did not find a current representation for the target resource or is not willing to disclose that one exists." (330835)
- §15.5.5: "A 404 status code does not indicate whether this lack of representation is temporary or permanent; the 410 (Gone) status code is preferred over 404 if the origin server knows ... that the condition is likely to be permanent." (331009)
- §15.5.11: "The 410 (Gone) status code indicates that access to the target resource is no longer available at the origin server and that this condition is likely to be permanent." (334621)
- §10.2.2: "When it has the form of a relative reference ([URI], Section 4.2), the final value is computed by resolving it against the target URI ([URI], Section 5)." (208031)
- §10.2.2: "If the Location value provided in a 3xx (Redirection) response does not have a fragment component, a user agent MUST process the redirection as if the value inherits the fragment component of the URI reference used to generate the target URI ..." (208463)
- §15.4: "Replace the target URI with the URI referenced by the redirection response's Location header field value after resolving it relative to the original request's target URI." (316747)

All eleven strings are present verbatim in both the retained S088.txt and my live-derived text (substring test over each; True/True for every one).

## Findings for the L1 (quote precision, not contract breakage)
- F1 observed: the C1 contract says "302, 303 and 307 are temporary (S088 section 15.4)". S088 supports this verbatim for 302 (§15.4.3 "resides temporarily") and 307 (§15.4.8 "resides temporarily"), but §15.4.4 never calls 303 temporary. Treating 303 as non-permanent is a lane policy inference (it is a redirection to a different, non-equivalent resource); a registry row or lesson MUST NOT attribute "temporary" for 303 to S088. Confidence high (whole-document substring search for "temporar" in §15.4.4: absent).
- F2 observed: RFC 9110 nowhere uses a fixed term "redirect status codes" and §15.4's taxonomy also places 300 (choice) and 304 (stored result) under "several types of redirects". The contract's set {301,302,303,307,308} is a lane subset (defensible: 300's Location is SHOULD, 304 carries none), but do not claim the RFC enumerates exactly those five; cite §15.4's bullets, not an enumeration. Confidence high.
- F3 observed: §15.5.5 explicitly refuses the permanence inference for 404 ("does not indicate whether ... temporary or permanent"). Contract (a) maps 404 to a `gone` finding; that is fine if `gone` means "no current representation", but the row/lesson MUST NOT gloss 404 as permanent removal. "likely to be permanent" is 410's sentence only (§15.5.11). Confidence high.
- F4 observed: §10.2.2 carries a user-agent MUST on fragment inheritance, which the contract declares out of scope. That is a disclosed deviation from RFC resolution; the row must not claim the tool implements RFC 9110 Location resolution in full. Contract (b)'s per-hop resolution ("against the URL that hop answered") is supported by the §15.4 sentence at offset 316747 ("after resolving it relative to the original request's target URI"). Confidence high.

## Not verified
- No counter run and no case inspected (no key, tree untouched). Nothing here speaks to pass counts.
- S089 (RFC 3986 §5.2) not reopened: outside this seat's target; contract (b)'s resolution algorithm is unchecked here.

## Commands (all exit 0)
- `curl ... -o rfc9110-live.html` (above), exit 0.
- `gunzip`+`sha256sum` comparison body: Python `gzip.decompress`/`hashlib`, `live == ret` True.
- text-rule re-derivation and substring tests: Python cell (script not retained as a file).
- Artifacts: /fast/scratch/hyaku/kake-r36w1/ScoutReopenS088/{rfc9110-live.html,rfc9110-live.txt,headers-live.txt,section-15.4*.txt,section-15.5.5.txt,section-15.5.11.txt,section-10.2.2.txt,sections-live.json}.
Tooling: no installs or upgrades (curl, python3, gzip already present).
