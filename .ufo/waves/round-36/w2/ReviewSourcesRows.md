# Wave 2 — Review rows S088-S094 against retained texts (ReviewSourcesRows)

Attacked: teaches-cell fidelity of corpus/SOURCES.md rows S088-S094 (lines 96-102) at f3a38bf8e68f6cee386125d34b5e95ac9b2df66e against the retained texts in `.ufo/waves/round-36/sources/`; scope distinctness vs S010/S028/S029/S030/S031/S033 (lines 17-18, 36-39, 41); anchor sha256 prefixes vs receipts.json; S094 reject-reason location; census validate. All work read-only against the lane working tree; no fetches (offline check by design); no installs needed.

## Commands (all exit 0 unless noted)
- `git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse HEAD` → `f3a38bf8e68f6cee386125d34b5e95ac9b2df66e`; `git status --porcelain -- corpus/SOURCES.md .ufo/waves/round-36/sources/` → empty (0 lines).
- `sha256sum .ufo/waves/round-36/sources/S0{88..94}.txt` → all 7 match receipts.json `textSha256` exactly (S088 `81c71974…b07a`, S089 `656b0d76…4ba7`, S090 `a1370869…399b`, S091 `517c1892…3e96`, S092 `2fb98770…6adb3`, S093 `5ddaebd8…7cbd`, S094 `458c6cc9…1208`), and each equals the row anchor prefix.
- `gzip -dc SXXX.html.gz | sha256sum` for all 7 → all match receipts `bodySha256` (S088 `d4317606…`, S089 `28869fb6…`, S090 `e1421f17…`, S091 `efcf19da…`, S092 `0128a08f…`, S093 `877c4dab…`, S094 `4c73d89c…`). Receipt chain text→body→row intact end-to-end.
- Span extraction: `grep -oE -m1/2/3 '<pattern>.{0,N}' <SXXX.txt>` per claim below (retained texts are single-line; tool grep would dump whole files). Two patterns missed on wording and were re-run: ISO date `2026-10-19` in S090.txt → actually "Last Updated 19 October 2026"; `feed readers` in S094.txt → actually "RSS readers".
- Census: `timeout 120 /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → exit 0 (header confirms read-only: "writes only stdout or --out"; no `--out` given).

## Census output (pasted verbatim)
```
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	W04	S088 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
kake	W04	S092 duplicate url html.spec.whatwg.org/multipage/syntax.html across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
```
exit=0. Three W04 warnings are pre-existing URL pairs (S010/S088, S028/S033, S030/S092 base URLs), allowed by contract ("warnings do not affect clean lanes").

## Per-row verdicts (teaches cell quoted spans from SXXX.txt)

**S088 — CLEAN.** Supports: 301 "the target resource has been assigned a new permanent URI and any future references to this resource ought to use one of the enclosed URIs"; 302 "the target resource resides temporarily under a different URI"; 303 "as indicated by a URI in the Location header field, which is intended to provide an indirect response to the original request"; 307 "resides temporarily under a different URI and the user agent MUST NOT change the request method"; 308 same "new permanent URI" formula; relative Location (§10.2.2) "When it has the form of a relative reference ([URI], Section 4.2), the final value is computed by resolving it against the target URI ([URI], Section 5)"; 404 §15.5.5 "does not indicate whether t[he lack of representation is] temporary or permanent" vs 410 §15.5.11 "this condition is likely to be permanent". All four anchor sections present (TOC: "15.4 Redirection 3xx", "10.2.2 Location", "15.5.5 404 Not Found", "15.5.11 410 Gone"). Scope disjoint from S010 (§8.8 validators), S028 (§4.2 URI schemes), S033 (§8.3/§5.6 media types); scope cell names all three.

**S089 — CLEAN.** Supports: §5.2 "This section describes an algorithm for converting a URI reference that might be relative to a given base URI into the parsed components of the reference's target"; §5.3 "Parsed URI components can be recomposed to obtain the corresponding URI reference string"; the "same results" clause "Applications may implement relative reference resolution by using some other algorithm, provided that the results match what would be given by this one." Distinct from S029 (§3 authority-vs-path observation, different URL `.txt` vs `.html#section-5.2`).

**S090 — CLEAN.** Supports: §4.2 "Remove any leading and trailing ASCII whitespace from label. If label is an ASCII case-insensitive match for any of the labels listed in the table below…"; §6.1 heading "Legacy hooks for standards"; BOM override in the decode hook "Let BOMEncoding be the result of BOM sniffing ioQueue. If BOMEncoding is non-null: Set encoding to BOMEncoding", decoding runs with " replacement " error mode; windows-1252 label row contains `" iso-8859-1 " … " latin1 " " us-ascii "`, and the spec prose names "labels, such as \" latin1 \", \" iso-8859-1 \", and \" ascii \"" as confusing synonyms — "ascii is a label for windows-1252" is supported. Anchor date: "Living Standard — Last Updated 19 October 2026" = 2026-10-19. No overlap claim with any existing row; scope negations (charset-header precedence, implementation subset) are exclusions, not claims.

**S091 — CLEAN.** Supports: "Form KC (NFKC) Compatibility Decomposition, followed by Canonical Composition"; Table 8 narrative "when the same strings are normalized in forms NFKD and NFKC … they do result in the same strings"; warning "Normalization Forms KC and KD must not be blindly applied to arbitrary text. Because they erase many formatting distinctions…". Anchor: "Version Unicode 18.0.0 Editors Ken Whistler Date 2026-08-12"; §1.2 and §1.3 headings present. Scope cell's "not a general quote-matching rule" is a declared exclusion.

**S092 — CLEAN.** Supports: "There are six different kinds of elements: void elements, the template element, raw text elements, escapable raw text elements, foreign elements, and normal elements."; "Raw text elements script, style"; template contents "stored in a DocumentFragment associated with a different Document — without a browsing context". Anchor: "HTML Living Standard — Last Updated 22 October 2026" = 2026-10-22; §13.1.2 heading present. Distinct from S030 (§13.1.2.1 slash rules) and S031 (§13.2.6 parsing); S092's teaches does not restate either.

**S093 — CLEAN (reject reason located).** Supports the anchor and reject: lead "HTTP 301, or 301 Moved Permanently, is the HTTP status code used for permanent redirecting"; quoted RFC 2616 passage "RFC 2616 [1] states that: If a client has link-editing capabilities, it should update all references to the Request URL…" with reference "10.3.2 301 Moved Permanently … RFC 2616"; Search engines section "Both Bing and Google recommend using a 301 redirect…" citing only "Site Move Tool" (Bing Webmaster Help) and "301 redirects" (Google Webmaster Tools Help) — tertiary, no primary protocol evidence, as the teaches cell states.

**S094 — CLEAN (reject reason located).** Supports the anchor and reject: Principle section "Redirect responses have status codes that start with 3, and a Location header holding the URL to redirect to" (the universal Location claim); permanent/temporary split "Permanent redirections These redirections are meant to last forever…" / "Temporary redirections…"; page date "This page was last modified on Aug 27, 2026". The S088 contradiction is real: RFC 9110 §15.4.1 300 "If the server has a preferred choice, the server SHOULD generate a Location header field" (conditional, not mandatory), and §15.4.5 304's MUST list is "Content-Location, Date, ETag, and Vary / Cache-Control and Expires" with a SHOULD NOT beyond it — no Location. "Cannot ground a re-check rule" follows. Attribution "wave-1 ScoutReopenS094" not independently verifiable from my seat (wave-1 reports not cross-checked; out of scope).

## Findings by severity

No high or medium findings. Rows S088-S094 pass teaches-fidelity, scope-distinctness, and hash-chain checks.

- LOW (advisory): S094 scope cell says "what crawlers and feed readers do with them"; S094.txt contains no "feed" — the text's wording is "Search engine robots, RSS readers, and other crawlers will update the original URL for the resource" (and "Search engine robots and other crawlers don't memorize the new, temporary URL"). Substance supported; "feed readers" is a paraphrase of "RSS readers" never used by the text. Teaches cell unaffected; row is rejected. SOURCES.md:102.
- OBSERVATION: S092's anchor section 13.1.2 is the parent of S030's material; S092.txt necessarily contains the void-element slash span S030 teaches ("On void elements, it does not mark the start tag as self-closing but instead is unnecessary and has no effect"). Distinctness is declared in both scope cells and census flags it only as W04, but this pair has the tightest section overlap of the six.

## Residual risk and verification gaps
- No live refetch (offline audit of retained artifacts only); live-page drift is out of scope for this seat.
- Comparison rows S010/S028-S033 audited only for scope distinctness, not their own teaches fidelity.
- The windows-1252 label-row grep span began mid-row ("csisolatin1"); support for "ascii" rests on the spec's prose note naming it a label/synonym, judged sufficient.
- Census run once on 2026-10-22 against the current lane checkout; not rerun per-row.
