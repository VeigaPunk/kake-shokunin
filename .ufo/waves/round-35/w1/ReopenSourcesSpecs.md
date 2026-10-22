# ReopenSourcesSpecs — re-open S078, S082, S083 live and check retained copies (r35 w1)

Sandbox: /fast/scratch/hyaku/kake-r35/w1/ReopenSourcesSpecs (bodies/, headers/, tmp/; TMPDIR pointed there).
Sealed tree untouched. No lane mutation: this report is the only file written in the lane. No tool installs (preinstalled curl, python3, sha256sum, gunzip sufficed).

## Commands run (all exit 0 unless noted)
1. `curl -sS --max-time 60 -o bodies/rfc9116.txt -D headers/rfc9116.hdr -w "S078 status=%{http_code} bytes=%{size_download} url=%{url_effective}" https://www.rfc-editor.org/rfc/rfc9116.txt` → `S078 status=200 bytes=45129 url=https://www.rfc-editor.org/rfc/rfc9116.txt`.
2. Same for https://www.rfc-editor.org/rfc/rfc8615.txt → `S082 status=200 bytes=26866`.
3. Same for https://www.iana.org/assignments/well-known-uris/well-known-uris.xhtml → exit 0 but `S083 status=302 bytes=0` (bodies/wku body empty); headers/wku.hdr:1-8 shows `HTTP/2 302`, `location: /assignments/well-known-uris`.
4. Refetch S083 with `curl -sSL` → `S083 status=200 bytes=69309 url=https://www.iana.org/assignments/well-known-uris` — final URL equals receipts.json:78 `finalUrl`.
5. `sha256sum bodies/*; wc -c bodies/*` → hashes/byte counts below.
6. eval python3: re-derived fetch_sources.py `visible_text()` on each live body; compared sha256 against receipt `textSha256` and byte-equality against retained `<id>.txt`.
7. `for s in S078 S082 S083; do gunzip -c sources/$s.html.gz | sha256sum; done` → all three equal the live body hashes.

## Acceptance — three rows
| src | live GET status | sha match vs receipts bodySha256 | located quote (<=25 words each) | tier/kind check |
|---|---|---|---|---|
| S078 RFC 9116 "A File Format to Aid in Security Vulnerability Disclosure", April 2022, Informational | 200, 45129 bytes | YES — live `79d19ce7a4a35496981095a27fd992797a9fc4d6f3649c2a1e14f494607c61f9` = receipts.json:17; `gunzip S078.html.gz` gives same; live text == retained S078.txt | §2.5 (bodies/rfc9116.txt:237): "Unless otherwise stated, all fields MUST be considered optional." (9w) — §3 (:439-441): "organizations MUST place the \"security.txt\" file under the \"/.well-known/\" path" (10w) — §4 (:492-493): "The file format of the \"security.txt\" file MUST be plain text (MIME type \"text/plain\")" (14w) | kind=spec, tier=A: the RFC text is primary/authoritative for scope "serving a valid security.txt from Pages" (CORPUS.md:91-97; precedent S032-S034 RFC rows tier A, SOURCES.md:119). Quotes present in retained S078.txt (single line; ~col 9045 / 16118 / 18387). |
| S082 RFC 8615 "Well-Known Uniform Resource Identifiers (URIs)", May 2019, Standards Track, obsoletes 5785 | 200, 26866 bytes | YES — live `02d45caeb86c00197d30428472102bb558881fa61937804330c1242a0be5b5dc` = receipts.json:65; gzip and .txt also match | §3 (bodies/rfc8615.txt:138-139): "A well-known URI is a URI [RFC3986] whose path component begins with the characters \"/.well-known/\"" (15w) | kind=spec, tier=A for scope "why /.well-known/security.txt is the required path" (CORPUS.md:91-97). Present in retained S082.txt ~col 5365. |
| S083 IANA Well-Known URIs registry | 302 → 200, 69309 bytes at /assignments/well-known-uris | YES — live `16c650e403110c08cd9b5de5198d69d0da278f9a7e967a7891b27cb3ea5fe995` = receipts.json:77; gzip and .txt also match | security.txt row (bodies/well-known-uris.xhtml:814-817; retained S083.txt ~col 9101): "security.txt RFC 9116 permanent IETF" (6w; row also shows changed 2021-07-13) | kind=dataset, tier=A: authoritative IANA registry data, not a spec and not community, so A is allowed (CORPUS.md:91-97). Present in retained S083.txt. |

## Retained-copy verdict
All three retained copies still match live, verified at three independent levels:
- Body: live sha256 == receipts.json `bodySha256` == sha256 of gunzipped retained `<id>.html.gz`.
- Text: re-deriving `visible_text()` per fetch_sources.py from live bodies reproduces receipt `textSha256` (S078 `4954ddcd…`, S082 `0746e9da…`, S083 `aceda87b…`) and is byte-identical to retained `<id>.txt`; word counts equal `textWords` (5590 / 3505 / 1424).
- Redirect: S083 302 `location: /assignments/well-known-uris` matches receipt `finalUrl` (receipts.json:78), so the retained final-URL record is still accurate.

## Publisher sections named
- RFC 9116 §2.5 Field Definitions (bodies/rfc9116.txt:235-391): the field catalogue (Contact, Expires, Canonical, Preferred-Languages, ...) and optionality rule.
- RFC 9116 §3 Location of the security.txt File (:437-457): must be served at /.well-known/security.txt, https only, Content-Type text/plain; /.well-known wins over legacy top-level placement.
- RFC 9116 §4 File Format Description and ABNF Grammar (:490-677): text/plain, UTF-8 Net-Unicode, and the normative ABNF (Contact + Expires mandatory).
- RFC 8615 §3 Well-Known URIs (bodies/rfc8615.txt:136-159): defines the /.well-known/ prefix, scheme support, and registration duty.
- IANA well-known-uris registry, security.txt row (well-known-uris.xhtml:813-817): name security.txt, reference RFC 9116, status permanent.

## Evidence pointers
- Live copies + headers: /fast/scratch/hyaku/kake-r35/w1/ReopenSourcesSpecs/bodies/{rfc9116.txt,rfc8615.txt,well-known-uris.xhtml}, headers/{rfc9116.hdr,rfc8615.hdr,wku.hdr}.
- Retained: kake-shokunin/.ufo/waves/round-35/sources/S078.txt, S082.txt, S083.txt, S0{78,82,83}.html.gz; receipts.json:14-25 (S078), :62-73 (S082), :74-85 (S083); fetcher .ufo/waves/round-35/fetch_sources.py (fetcherSha256 e2b9db84… matches receipt for all three).

## Not verified
- S079, S080, S081, S084, S085, S006 not re-opened (out of scope for this item).
- Single GET per URL with curl default TLS verification; no encoding-variant fetch (e.g., gzip transfer-encoding), so match is for the identity representation; the 302 on the .xhtml URL is observed as of 2026-10-22T22:26Z only.
