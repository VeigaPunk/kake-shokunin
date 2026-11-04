source: S463 — RFC 9111 §4.1 Calculating Cache Keys with the Vary Header Field — https://httpwg.org/specs/rfc9111.html#caching.negotiated.responses (already a registry row; this entry adds none for §4.1). Line references below are into the plain-text rendering https://www.rfc-editor.org/rfc/rfc9111.txt, retained at `.ufo/waves/round-89/L1/src/rfc9111.txt` (84477 bytes, sha256 aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e). RFC 9110 §5.6.1.2 and §5.6.2 are S465, retained `.ufo/waves/round-89/L1/src/rfc9110.txt` (502941 bytes, sha256 21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a).
verified-at: 2026-11-04 — both plain-text bodies re-fetched by the round-89 ScribeEntry seat at 21:14:38Z (HTTP 200; 84477 and 502941 bytes), byte-identical to the committed `L1/src` copies; each quoted span classified with `scripts/quote_class.py` against the body and its flat rendering; registry ids checked against `corpus/SOURCES.md` at 76225160 (highest S463; next free S464).
recheck: 180d, due 2027-05-03, or sooner after a source change. Re-fetch both plain-text URLs into a scratch directory of your own, compare the two sha256 values above, and re-locate §4.1 lines 526–557 and §5.6 lines 1696–1697 and 1730–1733 before reusing the conclusions.
ground: freshness — round-89 C2, a bounded capability: constructing the stored-response key a presented request maps to.
scope: key construction from a supplied URI, request header map and `Vary` value. Not storability, freshness, revalidation, reuse, serving, or any server, CDN or browser behaviour.

# Constructing the key a `Vary` response is stored under

A cache keeps stored responses under keys. For a response that carries `Vary`,
RFC 9111 §4.1 makes the key depend on the request header fields that `Vary`
nominates; its section title is *Calculating Cache Keys with the Vary Header
Field*. This entry decides one thing: given a URI, a presented request's header
map and a `Vary` value, which key does that request map to. It does not decide
whether anything is stored, whether it is fresh, or whether it may be reused.

## Located quotes

From `rfc9111.txt` (S463, `L1/src`):

Section title, line 526 (raw substring):

> 4.1.  Calculating Cache Keys with the Vary Header Field

Reuse condition, lines 530–532 (24 words; the source wraps the sentence, so this span is collapsed-only against the raw bytes):

> the cache MUST NOT use that stored response without revalidation unless all the presented request header fields nominated by that Vary field value match

Wildcard, lines 556–557 (17 words; the source wraps the sentence, so this span is collapsed-only against the raw bytes, and each physical line is a raw substring):

> A stored response with a Vary header field value containing a member "*" always fails to match.

From `rfc9110.txt` (S465, `L1/src`):

Tokens, lines 1730–1731 (12 words; collapsed-only); the production is `token = 1*tchar` at line 1733:

> Tokens are short textual identifiers that do not include whitespace or delimiters.

Empty list elements, lines 1696–1697 (13 words; collapsed-only):

> A recipient MUST parse and ignore a reasonable number of empty list elements

A `Vary` member and a field name are therefore tokens. Nothing in §4.1 or §5.6.2
turns SP, HTAB, comma, CR or LF into part of one.

## Decision table

Applied in order; the first rule that fires decides. Success is exit 0 with
`{"key": ...}` on stdout. Refusal is exit 1 with `invalid_input: <reason>` on
stderr and nothing on stdout.

| # | Rule | Outcome |
|---|---|---|
| K1 | Input is not a JSON object, or `uri` is missing or not a string | `invalid_input:` |
| K2 | `request_headers` is missing or not an object | `invalid_input:` |
| K3 | A header name is not a string, is empty, or is not a token (§5.6.2) | `invalid_input:` |
| K4 | A header value is not a string, or contains CR or LF | `invalid_input:` |
| K5 | Two header names in the map differ only in case (all headers, not only nominated ones) | `invalid_input:` |
| K6 | `vary` is present and is not a string | `invalid_input:` |
| K7 | A `Vary` member is `*` | `invalid_input:` (no key exists) |
| K8 | A `Vary` member is empty after SP/HTAB trimming, or is not a token | `invalid_input:` |
| K9 | Two `Vary` members are equal case-insensitively | `invalid_input:` |
| K10 | Otherwise | build the key |

The key layout, with the separators named by code point:

```
key = ESC(uri) + US + join(US, [ESC(name) + RS + value_part])
```

`US` is U+001F, `RS` is U+001E and `GS` is U+001C. `value_part` is `ESC(value)`
for a nominated field the request carries (value trimmed of SP/HTAB at both
edges, otherwise byte-exact) and `GS` for one it does not. Pairs are sorted by
the lowercased name. With no nominated member the key is `ESC(uri)` alone.

`ESC` replaces `%` with `%25` first, then U+001C with `%1C`, U+001D with `%1D`,
U+001E with `%1E` and U+001F with `%1F`. After escaping, no component contains
a raw U+001C, U+001E or U+001F, so two logical inputs cannot produce one key by
splitting a value across the layout.

Two naming notes. The contract calls U+001C "GS", which is not its ASCII name
(ASCII GS is U+001D); this entry keeps the contract's name and gives the code
point beside it. U+001D has no structural role in the layout: the contract
escapes it without naming it, and this entry names it here only so the escape
alphabet is closed.

Three consequences that are easy to get wrong:

- **Name case is not value case.** `Accept-Encoding` and `accept-encoding` name
  the same field (RFC 9110 §5.1), so they contribute the same component.
  `gzip` and `GZip` are different values and contribute different components.
- **Absent is not empty.** Section 4.1 says a field absent from one request
  matches another only if it is absent there too, so a nominated field the
  request does not carry contributes `GS`, and one it carries empty contributes
  nothing after `RS`.
- **Member order is not identity.** `Vary: a, b` and `Vary: b, a` nominate the
  same set and must produce the same key; the sort is what makes that true.

## Worked examples

Control characters are written as code points. Each row is one input and the
key it must produce.

| # | Input | Key |
|---|---|---|
| A | `{"uri":"https://e.test/a","request_headers":{"Accept-Encoding":"gzip"},"vary":"Accept-Encoding"}` | `https://e.test/a` + U+001F + `accept-encoding` + U+001E + `gzip` |
| B | `{"uri":"https://e.test/a","request_headers":{},"vary":"Accept-Encoding"}` | `https://e.test/a` + U+001F + `accept-encoding` + U+001E + U+001C |
| C | `{"uri":"https://e.test/a","request_headers":{"a":"x\u001fb\u001ey"},"vary":"a"}` | `https://e.test/a` + U+001F + `a` + U+001E + `x%1Fb%1Ey` |

Example B is the absent case: the request carries no `Accept-Encoding`, so its
component ends in U+001C. Example C shows that a U+001F or U+001E inside a
presented value is escaped, so it cannot be mistaken for a layout separator.

## Error patterns

- **Joining with a printable separator.** A colon or comma inside a header
  value can collide with the separator, so two different requests produce one
  key. Use separators outside the value alphabet and escape them where a value
  could contain one.
- **Sorting by the escaped name.** `%` is a token character, so escaping before
  sorting reorders names that contain it. Sort the lowercased name, then escape.
- **Lowercasing values.** Lowercasing a value changes the key for requests that
  differ only in value case, which section 4.1 treats as different.
- **Collapsing absent and empty.** A key that maps both states to one string
  serves one request's response to another.
- **Building a key for `*`.** A wildcard member nominates no field, so there is
  no key; refusing is the only honest answer.
- **Reading the key as a reuse decision.** The key says which stored response a
  request addresses. Section 4.1's reuse condition, section 3's storability and
  section 4.2's freshness are separate questions.

## Runnable checklist

Run from the lane root. Each command reads one JSON object on stdin.

1. A key with one nominated field:

   ```sh
   printf '%s' '{"uri":"https://e.test/a","request_headers":{"Accept-Encoding":"gzip"},"vary":"Accept-Encoding"}' | python3 -B scripts/cache_key.py
   ```

   Expected: exit 0 and `{"key": "https://e.test/a\u001faccept-encoding\u001egzip"}`.
   JSON writes the separators as escapes; the key itself carries the raw U+001F
   and U+001E characters.

2. Member order does not change the key:

   ```sh
   printf '%s' '{"uri":"https://e.test/a","request_headers":{"a":"x","b":"y"},"vary":"b, a"}' | python3 -B scripts/cache_key.py
   ```

   Expected: the same key as `"vary": "a, b"` on the same headers.

3. The wildcard is refused:

   ```sh
   printf '%s' '{"uri":"https://e.test/a","request_headers":{},"vary":"*"}' | python3 -B scripts/cache_key.py
   ```

   Expected: exit 1, empty stdout, stderr beginning `invalid_input:`.

4. The round-89 counter's offline selftest, which scores its own reference
   against the contract's worked examples:

   ```sh
   TMPDIR=$(mktemp -d) python3 -B .ufo/waves/round-89/c89_key.py --selftest
   ```

   Expected: `selftest: 43/43 passed`, exit 0. This checks the counter, not the
   script; the script's gate is the counter's candidate run, named in
   `.ufo/waves/round-89/c2-contract.md`.

## Limits

- **Key construction only.** This entry decides the key a presented request
  maps to under a `Vary` value. It does not decide storability (RFC 9111 §3),
  freshness or age (§4.2; S462 holds the age arithmetic), revalidation or reuse
  (§4.1's MUST NOT condition is a separate decision), serving, or what any
  server, CDN or browser does with a key. No cache was observed.
- **The key form is this lane's adapter convention.** RFC 9111 names the
  ingredients (the URI, the nominated fields, their presented values) and not a
  separator, an escape alphabet or a sort order. A different cache would build a
  different string for the same request and still follow §4.1.
- **Some refusals are this lane's convention.** K8's refusal of an empty member
  goes against RFC 9110 §5.6.1.2, which tells a recipient to ignore empty list
  elements. The lane refuses instead, because a trailing comma in a publisher's
  configuration is more likely a mistake than an intention, and an empty member
  set would collapse every request for that URI onto one key.
- **The instrument does not establish the whole contract.** The round-89
  counter's 16 frozen cases, 200 generated pairs and 9 refusals are this lane's
  instrument, not a conformance suite. Probes in the round-89 ScribeEntry
  receipts show that the counter still returns `met=true` for seven
  contract-violating variants: an empty header name, a duplicate `Vary` member,
  a non-empty non-token `Vary` member, CR alone in a value, an unescaped URI, an
  unescaped name, and an unescaped U+001D. The production script refuses or
  escapes all seven on the probed inputs; the counter cannot show that.
