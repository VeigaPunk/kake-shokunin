# ScoutReopenS090 — S090 (WHATWG Encoding) re-opened live

Seat KakeR36.ScoutReopenS090, wave 1, leaf. I did not list, read, stat or search the sealed tree, and did not run the counter. No tools installed. Everything wrote only under /fast/scratch/hyaku/kake-r36w1/ScoutReopenS090/.

## What I did (commands, exit codes)
```
mkdir -p /fast/scratch/hyaku/kake-r36w1/ScoutReopenS090/tmp
timeout 60 curl -sS -L -o S090-live.html -w 'http=%{http_code} size=%{size_download} url=%{url_effective}\n' https://encoding.spec.whatwg.org/
  -> exit 0, http=200 size=591022 url=https://encoding.spec.whatwg.org/
timeout 60 curl -sS -D headers-live.txt -o S090-live2.html https://encoding.spec.whatwg.org/
  -> exit 0, http=200 size=591022
```
Both bodies: sha256 `e1421f1791b202717883c452a6267129ce5fb3ca13652e5022a2b6d2a11fc262`, 591022 bytes.
Response headers (second GET, headers-live.txt): `date: Fri, 23 Oct 2026 01:36:12 GMT`, `last-modified: Mon, 19 Oct 2026 23:30:10 GMT`, `etag: "6ad6a802-904ae"`, `content-length: 591022`.

## Comparison with retained .ufo/waves/round-36/sources/
- Body: `gunzip -c sources/S090.html.gz` = 591022 bytes, sha256 `e1421f17…c262`; `cmp` against my live body printed nothing and returned 0 (IDENTICAL). Retained gzip mtime field is 0.
- Text: applied the retained fetcher's own rule (`fetch_sources.py:visible_text`) to my body: 1 line, 97814 bytes, 16827 words, sha256 `a137086931ac8720d6c3adacd2242a18231c3e1bb96b83eaae8820b938f9399b` — byte-identical to retained `sources/S090.txt` (same sha256; Python `live_txt == retained_txt` is True).
- Timing: retained receipt `accessedUtc 2026-10-23T01:08:57Z`; server `last-modified 2026-10-19T23:30:10Z` predates it, so the page had not changed between the L1 fetch and mine. **No drift: the retained snapshot is faithful and current.**

## Verbatim from my fetch (offsets: S090-live.html / S090-live.txt)
1. BOM sniff table — html §6.1 `id="bom-sniff"` @106357, text @31379 (table @31752):
   "To BOM sniff an I/O queue of bytes ioQueue: Let BOM be the result of peeking 3 bytes from ioQueue, converted to a byte sequence. For each of the rows in the table below, starting with the first one and going down, if BOM starts with the bytes given in the first column, then return the encoding given in the cell in the second column of that row. Otherwise, return null.
   Byte order mark | Encoding — `0xEF 0xBB 0xBF` UTF-8; `0xFE 0xFF` UTF-16BE; `0xFF 0xFE` UTF-16LE."
2. decode's BOM handling — html §6 `id="decode"` @104622, text @30691:
   "Let BOMEncoding be the result of BOM sniffing ioQueue. If BOMEncoding is non-null: Set encoding to BOMEncoding. Read three bytes from ioQueue, if BOMEncoding is UTF-8; otherwise read two bytes. (Do nothing with those bytes.) For compatibility with deployed content, the byte order mark is more authoritative than anything else. In a context where HTTP is used this is in violation of the semantics of the `Content-Type` header."
3. get an encoding — html @58818 (`id="concept-encoding-get"`, in §4.2 `id="names-and-labels"` @56841), text @13614:
   "To get an encoding from a string label: 1. Remove any leading and trailing ASCII whitespace from label. 2. If label is an ASCII case-insensitive match for any of the labels listed in the table below, then return the corresponding encoding; otherwise return failure."
   Both terms link out (html @59119): `https://infra.spec.whatwg.org/#ascii-whitespace` and `#ascii-case-insensitive`; S090 itself does not define the whitespace set.
4. §4.2 preamble (text @13033): "The table below lists all encodings and their labels user agents must support. User agents must not support any other encodings or labels. For each encoding, ASCII-lowercasing its name yields one of its labels."

## windows-1252 labels (my fetch: html `rowspan="17"` @68781, labels @68852–70000)
17 labels, pasted: `"ansi_x3.4-1968"`, `"ascii"`, `"cp1252"`, `"cp819"`, `"csisolatin1"`, `"ibm819"`, `"iso-8859-1"`, `"iso-ir-100"`, `"iso8859-1"`, `"iso88591"`, `"iso_8859-1"`, `"iso_8859-1:1987"`, `"l1"`, `"latin1"`, `"us-ascii"`, `"windows-1252"`, `"x-cp1252"`.
All four asked: iso-8859-1 yes, latin1 yes, ascii yes, us-ascii yes.
Note `id="note-latin1-ascii"` @78456: "these are synonyms: 'latin1' and 'ascii' are just labels for windows-1252, and any software following this standard will, for example, decode 0x80 as U+20AC (€) when asked for the 'Latin1' or 'ASCII' decoding of that byte."

Other label sets the same table gives, since C1(f) says "the labels of UTF-8, UTF-16BE, UTF-16LE and windows-1252":
- UTF-8: unicode-1-1-utf-8, unicode11utf8, unicode20utf8, utf-8, utf8, x-unicode20utf8
- UTF-16BE: unicodefffe, utf-16be
- UTF-16LE: csunicode, iso-10646-ucs-2, ucs-2, unicode, unicodefeff, utf-16, utf-16le

## Findings for the build
- OBSERVED: the retained S090 body and text are byte-identical to a fresh fetch; C1(f)'s three BOM rows and their order match the spec table; the four labels the contract names map to windows-1252; 0x80 must decode to U+20AC under any of them (a cheap discriminator between cp1252 and true latin-1).
- Risk, contract wording (trim): C1(f) and (e) say "trimmed" without naming the set. S090 trims ASCII whitespace, which is defined only in Infra as TAB U+0009, LF U+000A, FF U+000C, CR U+000D, SPACE U+0020. Python `str.strip()` also strips U+000B, U+001C–1F, U+0085, U+00A0, U+2000–200A, U+2028/29, U+3000, U+FEFF, so a `.strip()` tool accepts e.g. `"utf-8\x0b"` where the spec returns failure, i.e. `charset_unsupported`. [INFERENCE: the contract does not settle this; S090 does.]
- Risk, label sets: a tool hard-coding only the four canonical labels returns `charset_unsupported` for `charset=unicode`, `utf-16`, `utf8`, `x-cp1252`, all valid labels of supported encodings. Read "the labels of …" as the full sets above.
- Risk, ordering: C1(f) puts the BOM branch first ("whatever `charset` says"), so a BOM-prefixed body whose charset is unsupported should be decoded by BOM with no `charset_unsupported`. S090's decode takes an already-resolved fallback encoding and sniffs first, so it does not contradict this; the ordering is the contract's, not S090's.
- Not from S090: C1(f)'s "surrounding double quotes removed" is HTTP parameter quoting; do not cite S090 for it. "No BOM and no `charset`: UTF-8" is the contract's own rule; §4.2's "Authors must use the UTF-8 encoding" is a requirement on authors, not a decoding default.
- §4.2's "must not support any other encodings or labels" supports `charset_unsupported` for table-valid but unsupported labels such as `iso-8859-2` or `shift_jis`.

## Not verified
Sealed cases, counter and verdict (no key; untouched). I re-opened S090 only, not S088–S094. Nothing here is a claim about any registry row's freshness.

## Artifacts (absolute)
/fast/scratch/hyaku/kake-r36w1/ScoutReopenS090/S090-live.html, S090-live2.html (both 591022 B, sha256 e1421f17…c262), S090-live.txt (1 line, 97814 B, sha256 a1370869…399b), headers-live.txt, retained.html (decompressed retained body).
