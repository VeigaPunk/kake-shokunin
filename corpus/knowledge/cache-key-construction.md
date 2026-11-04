source: S464 — RFC 9111 HTTP Caching, section 4.1 Calculating Cache Keys with the Vary Header Field — https://www.rfc-editor.org/rfc/rfc9111.txt; opened 2026-11-04; retained body `.ufo/waves/round-89/L1/src/rfc9111.txt` (84477 bytes, sha256 aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e). S465 carries the token and empty-list-element rules; S462 keeps age arithmetic and S463 keeps the match-rule reading of the same section.
verified-at: 2026-11-04 — own GET completed 21:16:51Z; HTTP 200, 84477 bytes, sha256 aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e; byte-identical to the round-87 and round-88 retained copies of the same URL. The RFC 9110 body was fetched in the same pass (21:16:52Z, HTTP 200, 502941 bytes, sha256 21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a).
recheck: 180d, due 2027-05-03, or sooner after a source change. Re-fetch both plain-text URLs into a scratch directory of your own, compare the two sha256 values above, and re-locate section 4.1 before reusing the conclusions. The scratch path is yours to choose and is not recorded here; no ephemeral path is named in this line.
ground: freshness — round-89 C2, a bounded capability: constructing the stored-response key a presented request maps to.
scope: key construction from a supplied URI, request header map and `Vary` value. Not storability, freshness, revalidation, reuse, serving, or any server, CDN or browser behaviour.

# Constructing the key a `Vary` response is stored under

A cache distinguishes stored responses for one URI by the request header fields
that `Vary` nominates. RFC 9111 makes that explicit in the section title itself:
section 4.1 is *Calculating Cache Keys with the Vary Header Field*, and its first
paragraph conditions reuse on every nominated field matching. This entry covers
the construction half — given a URI, a presented request header map and a `Vary`
value, what key does that request map to — and nothing about whether the
response may be stored, whether it is fresh, or whether it may be reused.

## Located quotes

Retained plain-text body `.ufo/waves/round-89/L1/src/rfc9111.txt`
(sha256 aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e).

**The section title** — plain-text line 526:

> 4.1.  Calculating Cache Keys with the Vary Header Field

**The reuse condition** — section 4.1 first paragraph, plain-text lines 530–535:

> the cache MUST NOT use that stored response without revalidation unless all the presented request header fields nominated by that Vary field value match

**The wildcard** — section 4.1, plain-text lines 555–557: a stored response with
a `Vary` value containing a member `"*"` always fails to match. The member is the
single asterisk character; there is no field behind it, so no key can be built
for it and this lane refuses the input rather than inventing one.

Retained plain-text body `.ufo/waves/round-89/L1/src/rfc9110.txt`
(sha256 21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a).

**What a member and a field name may contain** — RFC 9110 section 5.6.2,
plain-text lines 1730–1738:

> Tokens are short textual identifiers that do not include whitespace or delimiters.

The production that follows is `token = 1*tchar`; the `tchar` alphabet is the
punctuation characters exclamation, hash, dollar, percent, ampersand,
apostrophe, asterisk, plus, hyphen, dot, caret, underscore, backtick and tilde,
plus digits and letters. SP, HTAB, comma, CR and LF are all outside it.

**Empty list elements** — RFC 9110 section 5.6.1.2, plain-text lines 1695–1699:

> A recipient MUST parse and ignore a reasonable number of empty list elements

This is why refusing `Vary: "a,"` is a declared adapter convention and not an
RFC requirement: the source tells a recipient to ignore empty elements, so a
zero-member remainder nominates nothing. The lane refuses it anyway, because a
trailing comma in a publisher's configuration is more likely a mistake than an
intention, and a silently empty member set would collapse every request for that
URI onto one key.

## Decision table

Applied in order; the first rule that fires decides. Success is exit 0 with
`{"key": ...}` on stdout; refusal is exit 1 with `invalid_input: <reason>` on
stderr and nothing on stdout.

| # | Rule | Outcome |
|---|---|---|
| K1 | Input is not a JSON object, or `uri` is missing or not a string | `invalid_input:` |
| K2 | `request_headers` is not an object | `invalid_input:` |
| K3 | A header name is not a string, is empty, or is not a token (section 5.6.2) | `invalid_input:` |
| K4 | A header value is not a string, or contains CR or LF | `invalid_input:` |
| K5 | Two header names in the map differ only in case | `invalid_input:` |
| K6 | `vary` is present and is not a string | `invalid_input:` |
| K7 | A `Vary` member is `*` | `invalid_input:` (no key exists) |
| K8 | A `Vary` member is empty after edge SP/HTAB trimming, or is not a token | `invalid_input:` |
| K9 | Two `Vary` members are equal case-insensitively | `invalid_input:` |
| K10 | Otherwise | build the key |

The key layout, with `US` = U+001F, `RS` = U+001E and `GS` = U+001C:

```
key = ESC(uri) + US + join(US, [ESC(name) + RS + value_part])
```

where `value_part` is `ESC(value)` for a nominated field the request carries and
`GS` for one it does not, and the pairs are sorted by the lowercased name. With
no nominated member the key is `ESC(uri)` alone. `ESC` replaces `%` with `%25`
and the four separators with `%1C`, `%1D`, `%1E` and `%1F`, so no component can
contain a raw separator and two different logical inputs cannot produce the same
key by splitting a value across the layout.

Three consequences worth stating because they are easy to get wrong:

- **Name case is not value case.** `Accept-Encoding` and `accept-encoding` name
  the same field (RFC 9110 section 5.1), so they contribute the same key
  component. `gzip` and `GZip` are different values and contribute different
  components.
- **Absent is not empty.** A nominated field the request does not carry
  contributes `GS`; one it carries with an empty value contributes the empty
  string. Section 4.1 says a field absent from one request can only match
  another request if it is also absent there, which requires the two states to
  be distinguishable in the key.
- **Member order is not identity.** `Vary: a, b` and `Vary: b, a` nominate the
  same set, so they must produce the same key; the sort is what makes that true.

## Error patterns

- **Joining with a printable separator.** A colon or comma inside a header value
  collides with the separator, so `{"a": "x:y"}` and `{"a": "x", "b": "y"}`
  produce one key for two different requests. Use separators outside the value
  alphabet and escape them where a value could contain one.
- **Sorting by the escaped name.** `%` is a token character, so escaping before
  sorting reorders names that contain it. Sort the lowercased name, then escape.
- **Lowercasing the whole request.** Lowercasing values changes the key for
  requests that differ only in value case, which section 4.1 treats as
  different.
- **Collapsing absent and empty.** The two states are different under section
  4.1's absence rule; a key that maps both to the same string silently serves
  one request's response to the other.
- **Building a key for `*`.** A wildcard member nominates no field, so there is
  no key; refusing is the only honest answer.
- **Reading the key as a reuse decision.** The key says which stored response a
  request addresses. Section 4.1's reuse condition, section 3's storability
  condition and section 4.2's freshness arithmetic are separate questions.

## Runnable checklist

Run from the lane root. Each command reads one JSON object on stdin.

1. A key with one nominated field:

   ```sh
   printf '%s' '{"uri":"https://e.test/a","request_headers":{"Accept-Encoding":"gzip"},"vary":"Accept-Encoding"}' | python3 -B scripts/cache_key.py
   ```

   Expected: exit 0, `{"key": "https://e.test/a\u001faccept-encoding\u001egzip"}`
   (JSON escapes the separator; the key itself carries the raw U+001F and
   U+001E characters).

2. Member order does not change the key:

   ```sh
   printf '%s' '{"uri":"https://e.test/a","request_headers":{"a":"x","b":"y"},"vary":"b, a"}' | python3 -B scripts/cache_key.py
   ```

   Expected: the same key as `vary: "a, b"` on the same headers.

3. The wildcard is refused:

   ```sh
   printf '%s' '{"uri":"https://e.test/a","request_headers":{},"vary":"*"}' | python3 -B scripts/cache_key.py
   ```

   Expected: exit 1, empty stdout, stderr beginning `invalid_input:`.

4. Offline gate. The tool has no selftest of its own; its gate is the round-89 counter's
   selftest, which scores the reference against the contract's worked examples:

   ```sh
   TMPDIR=$(mktemp -d) python3 -B .ufo/waves/round-89/c89_key.py --selftest
   ```

   Expected: `selftest: 43/43 passed`, exit 0. The counter's candidate gate is
   `python3 -B .ufo/waves/round-89/c89_key.py --root . --revision <rev> --candidate scripts/cache_key.py --work "$TMPDIR/work"`.

## What this entry does not establish

- **No storability claim.** Whether a response may be stored is section 3's
  question.
- **No freshness, age or revalidation claim.** S462 holds the age arithmetic;
  section 4.2 holds lifetime.
- **No reuse claim.** A key identifies a stored response; section 4.1's
  condition for reuse without revalidation is a separate decision.
- **No serving or CDN claim.** Nothing here was observed on a live cache. The
  key form is this lane's adapter convention: the source names the ingredients
  (URI, nominated fields) and the section title names the operation, but it does
  not fix a separator, an escaping scheme or a sort order. A different cache
  would build a different string for the same request and still satisfy the
  source.
- **The refusal list is partly adapter.** K7 follows the source. K8 and K9
  follow this lane's reading of a malformed publisher configuration, not an RFC
  requirement (see the empty-element quote above).
- **No conformance score.** The counter's 16 frozen cases, 200 generated
  property cases and 9 refusals are this lane's instrument, not a conformance
  suite.
