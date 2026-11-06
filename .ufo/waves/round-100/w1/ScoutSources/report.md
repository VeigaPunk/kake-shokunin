# ScoutSources — round 100 W1 — C2 source re-open for S486/S487

Seat: ScoutSources (leaf, no subagent dispatch). Lane tip read: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse master` → `e84a18714b6be7fd2456a2dcc5f28c0cb0ab981f` (observed rc 0; equals the C1 repair commit). Task: re-open the two sources C2 rests on (S486, S487) — one GET each, digest comparison against the retained bodies, ten located verbatim quotes, two draft registry rows.

## 1. Fetch receipts (one GET per RFC, no retry)

| item | rfc9111 | rfc9110 |
|---|---|---|
| command | `curl -sS -o rfc9111.txt -w '...' https://www.rfc-editor.org/rfc/rfc9111.txt` | `curl -sS -o rfc9110.txt -w '...' https://www.rfc-editor.org/rfc/rfc9110.txt` |
| HTTP status | 200 | 200 |
| final URL | https://www.rfc-editor.org/rfc/rfc9111.txt | https://www.rfc-editor.org/rfc/rfc9110.txt |
| bytes | 84477 | 502941 |
| sha256 (fetched) | aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e | 21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a |
| retained copy | LANE/.ufo/waves/round-99/sources/rfc9111.txt | LANE/.ufo/waves/round-100/sources/rfc9110.txt |
| sha256 (retained, computed this run) | aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e | 21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a |
| verdict | match (byte-identical) | match (byte-identical) |

Receipt time (UTC, `date -u` after both GETs, observed rc 0): 2026-11-06T01:48:09Z. Byte counts match the retained copies (84477 and 502941) and the counts recorded in S484 (84477 bytes) and S466 (502941 bytes). Freeze cross-check: freeze.md lines 68-69 assert "RFC 9111 byte-identical to the round-99 retained body; RFC 9110 retained at `sources/rfc9110.txt`, sha256 `21c1cdce…`" — confirmed by this re-open; no defect found. All ten quotes below are from the fetched bodies; because the digests are byte-identical, the same plain-text line numbers hold for the retained copies. Bodies live only in the seat scratch (/fast/scratch/hyaku/kake-r100/ScoutSources/), deleted at yield.

## 2. Ten located verbatim quotes (plain-text line numbers; word/token counts ≤ 25)

RFC 9111 (fetched body, 1956 lines):

1. §5.2 "identified by a token, to be compared case-insensitively" sentence — lines 1098-1100 (heading §5.2 line 1081; the word is hyphen-wrapped across lines 1098/1099 as "case-" + "insensitively"):
   > Cache directives are identified by a token, to be compared case-insensitively, and have an optional argument that can use both token and quoted-string syntax.
   (24 words)

2. §5.2 "recipients ought to accept both forms" — lines 1100-1102:
   > For the directives defined below that define arguments, recipients ought to accept both forms, even if a specific form is required for generation.
   (23 words)

3. §5.2 the cache-directive rule — line 1106 (same rule repeated in Appendix A at line 1783):
   > cache-directive = token [ "=" ( token / quoted-string ) ]
   (11 tokens)

4. §5.2.2.4 qualified no-cache, the field-name argument sentence — opening 18 words of the sentence spanning lines 1273-1279 (heading §5.2.2.4 line 1258; "Argument syntax: #field-name" lines 1260-1262):
   > The qualified form of the no-cache response directive, with an argument that lists one or more field names
   (18 words; sentence continues "…, indicates that a cache MAY use the response to satisfy a subsequent request … if the listed header fields are excluded … or … successfully revalidated … (updating or removing those fields).")

5. §5.2.2.7 qualified private — opening 23 words of the sentence spanning lines 1334-1339 (heading §5.2.2.7 line 1321; "Argument syntax: #field-name" lines 1323-1325):
   > If a qualified private response directive is present, with an argument that lists one or more field names, then only the listed header fields
   (23 words; sentence continues "… are limited to a single user: a shared cache MUST NOT store the listed header fields …")

6. §5.2.3 "MUST ignore unrecognized cache directives" — lines 1411-1412 (heading §5.2.3 line 1408):
   > A cache MUST ignore unrecognized cache directives.
   (7 words)

7. §3.1 proxy-specific fields MUST NOT be stored — lines 358-359 of the sentence ending line 360 (heading §3.1 line 338):
   > Header fields that are specific to the proxy that a cache uses when forwarding a request MUST NOT be stored
   (20 words; sentence continues "…, unless the cache incorporates the identity of the proxy into the cache key. Effectively, this is limited to Proxy-Authenticate …, Proxy-Authentication-Info …, and Proxy-Authorization …")

RFC 9110 (fetched body, 10785 lines):

8. §5.5 "A field value does not include leading or trailing whitespace" — line 1591 (heading §5.5 line 1579):
   > A field value does not include leading or trailing whitespace.
   (10 words; next sentence, same line, begins "When a specific version of HTTP allows such whitespace … MUST exclude such whitespace prior to evaluating the field value.")

9. §5.6.1.2 the recipient accept-syntax rule — line 1702, introduced by "a recipient MUST accept lists that satisfy the following syntax:" (lines 1699-1700; heading §5.6.1.2 line 1693):
   > #element => [ element ] *( OWS "," OWS [ element ] )
   (13 tokens)

10. §5.6.4 quoted-string/qdtext/quoted-pair rules — productions at lines 1786-1787, quoted-pair production at line 1794 (heading §5.6.4 line 1781; quoted-pair handling sentence lines 1789-1792):
   > quoted-string  = DQUOTE *( qdtext / quoted-pair ) DQUOTE
   > qdtext         = HTAB / SP / %x21 / %x23-5B / %x5D-7E / obs-text
   (22 tokens across the two contiguous lines 1786-1787; quoted-pair = "\" ( HTAB / SP / VCHAR / obs-text ) stands alone at line 1794, cited as location, not quoted here to keep the contiguous quote ≤ 25 tokens)

## 3. Draft registry rows

Two rows in the 11-column SOURCES.md shape are in `rows.md` beside this report: S486 (RFC 9111 §5.2/§5.2.2.4/§5.2.2.7/§5.2.3 + §3.1 proxy-fields sentence; status mined, opened 2026-11-06, recheck 365d, used-by corpus/knowledge/freshening-304.md) and S487 (RFC 9110 §5.5/§5.6.1.2/§5.6.2/§5.6.4; same tail columns).

Distinctness checks against held rows:
- S486 vs S484 (§3.1/§3.2/§4.3.4 304-freshening/updating reading): different sections except §3.1, where S484 anchors lines 338-366 broadly and S486 anchors only the proxy-fields sentence (lines 358-360); stated in the scope cell.
- S486 vs S456: S456 explicitly excludes "cache-directive argument syntax" — S486 is exactly that ground; stated.
- S486 vs S457/S461/S469: S457/S461 hold per-directive value semantics (max-age, ordering, duplicates) — S486 is grammar/extension handling, not directive-by-directive values; named as not-clauses.
- S487 vs S433/S453/S465: named per spec; S465 anchors §5.6.2 token production (lines 1730-1738) and the §5.6.1.2 empty-element sentence for the Vary-member alphabet reading — S487's reading is the value-grammar chain (whitespace trim, accept-syntax production, quoted-string), different sentences and purpose; stated.
- Adjacency finding to route (not repair): S478 already anchors §5.6.1.2 plain-text lines 1695-1702 (empty-element parse-and-ignore + §5.6.3 whitespace) and S466 anchors §5.5 lines 1579 and 1606-1612 (invalid characters). S487's §5.6.1.2 anchor (line 1702 production) and §5.5 anchor (line 1591 whitespace sentence) are different sentences but the same sections; the drafted not-clauses name both. L1/reviewers should confirm the distinctness wording before the rows land (freeze lines 68-69 say rows land only after this re-open — re-open is done).

## 4. Tooling

No tools installed or upgraded (seat used curl, git read-only, sha256sum, date only).

SCOUT rfc9111-sha=match rfc9110-sha=match quotes=10/10 rows=2
