# Round 89 C2 contract — conservative Vary-nominated cache-key construction

Frozen before data, together with `.ufo/waves/round-89/c89_key.py`. This file is
the declared form a candidate must implement; the counter's own reference
implementation is checked against the worked examples below before any candidate
is scored, so an oracle/contract drift fails the counter's selftest rather than
passing silently.

## Input

One JSON object on stdin:

```
{"uri": <string>, "request_headers": {<name>: <value>, ...}, "vary": <string, optional>}
```

`vary` absent is the same as `vary: ""`.

## Output

Success: one JSON object on stdout, `{"key": <string>}`, exit 0.
Refusal: `invalid_input: <reason>` on stderr, exit 1, nothing on stdout.

## Canonical key form

A key is built from exactly three ingredients: the request URI, the field names
nominated by `Vary`, and those fields' presented values.

1. **Members.** Split `vary` on `,`. Each member is trimmed of leading and
   trailing SP and HTAB and must be an RFC 9110 `token`. Members are compared
   case-insensitively and sorted; a duplicate member is refused.
2. **Names.** A nominated field name is lowercased (ASCII `A`–`Z` only). Lookup
   in `request_headers` is case-insensitive; two header names that differ only in
   case are refused as a duplicate.
3. **Values.** A value is trimmed of leading and trailing SP and HTAB and is
   otherwise compared byte-exactly: no case folding, no internal whitespace
   collapse.
4. **Escaping.** In the URI, each name and each value, `%` becomes `%25`, and the
   four separators below become `%1C`, `%1D`, `%1E`, `%1F`. No separator can then
   occur raw inside a component.
5. **Layout.** With `US` = U+001F, `RS` = U+001E and `GS` = U+001C:

   ```
   key = ESC(uri) + US + join(US, [ESC(name) + RS + (ESC(value) if present else GS)])
   ```

   with the pairs sorted by the lowercased name. When `Vary` nominates no member the key
   is `ESC(uri)` alone — every request for that URI shares one key.

A nominated field that is **absent** from the request contributes `GS`; a
nominated field **present with an empty value** contributes the empty string.
Those two are different keys.

## Refusals (`invalid_input:`, exit 1)

- input is not a JSON object, or `uri` is missing or not a string;
- `request_headers` is missing or not an object;
- a header name is not a string, is empty, or is not an RFC 9110 `token`;
- a header value is not a string, or contains CR or LF;
- `vary` is present and is not a string;
- a `Vary` member is `*` (the wildcard nominates no field, so no key exists);
- a `Vary` member is empty after trimming (for example a trailing comma) or is
  not a `token`;
- two `Vary` members are equal case-insensitively;
- two header names are equal case-insensitively.

## Worked examples (the counter's reference must reproduce these before scoring)

| # | input | key |
|---|---|---|
| 1 | `{"uri":"https://e.test/a","request_headers":{}}` | `https://e.test/a` |
| 2 | `{"uri":"https://e.test/a","request_headers":{"Accept-Encoding":"gzip"},"vary":"Accept-Encoding"}` | `https://e.test/a` + US + `accept-encoding` + RS + `gzip` |
| 3 | `{"uri":"https://e.test/a","request_headers":{"accept-encoding":"gzip","Accept":"text/html"},"vary":" Accept ,Accept-Encoding "}` | `https://e.test/a` + US + `accept` + RS + `text/html` + US + `accept-encoding` + RS + `gzip` |
| 4 | `{"uri":"https://e.test/a","request_headers":{"a":"50%"},"vary":"a"}` | `https://e.test/a` + US + `a` + RS + `50%25` |
| 5 | `{"uri":"https://e.test/a","request_headers":{"a":"x<US>b<RS>y"},"vary":"a"}` | `https://e.test/a` + US + `a` + RS + `x%1Fb%1Ey` |
| 6 | `{"uri":"https://e.test/a","request_headers":{"Accept-Encoding":""},"vary":"Accept-Encoding"}` | `https://e.test/a` + US + `accept-encoding` + RS |
| 7 | `{"uri":"https://e.test/a","request_headers":{},"vary":"Accept-Encoding"}` | `https://e.test/a` + US + `accept-encoding` + RS + GS |

`US`, `RS` and `GS` in the table are the literal control characters, not
backslash escapes; the JSON input in example 5 carries them raw.

## Scope

This contract decides **key construction only**: it says which stored-response
key a presented request maps to. It does not decide storability, freshness,
revalidation, reuse, or what any server or browser does. RFC 9111 §4.1 is the
ground for *why* the nominated fields participate; the canonical form, the
escaping and the refusal list are this lane's adapter conventions and are
declared as such.

## Candidate rules

The candidate is a standalone script: read one JSON object on stdin, write the
result, exit. It must not import the counter (`c89_key`), must not read the
frozen case file or any file under `.ufo/waves/`, and must not embed a table of
this round's cases. Those four rules are checked textually (disclosed limit) and
the property population is generated at scoring time from a seed printed in the
receipt, so a table over committed cases cannot reach the target.
