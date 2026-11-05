# Round 99 C2 — contract v1: freshening stored responses upon a 304 (RFC 9111 §4.3.4 + §3.2)

Source: RFC 9111 (June 2022) §4.3.4 "Freshening Stored Responses upon Validation" and §3.2
"Updating Stored Header Fields", plus the §3.1 storage exceptions §3.2 points at
(retained body `.ufo/waves/round-99/sources/rfc9111.txt`, sha256
`aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`, registry row S484).
Reported (unverified) erratum EID 9185 on the §4.3.4 initial-set paragraph is on record
(S485); this contract does not compute the initial set, so the erratum does not change it.

Candidate path: `scripts/freshen_304.py`. Standard library only. Reads ONE JSON object on
stdin, writes ONE JSON object on stdout, exit 0. Refusal: `invalid_input: <reason>` on
stderr, nothing on stdout, exit 1. It opens no file, socket or process.

## Input

```
{"stored": [{"id": <str>, "received": <int>, "headers": {<name>: <str>, ...}}, ...],
 "response": {"status": 304, "headers": {<name>: <str>, ...}}}
```

- `stored` is the **initial set** (§4.3.4 paragraph 2) as the caller computed it: the lane
  does not evaluate §4 reuse conditions, keys or Vary. It may be empty.
- `received` is an integer (receipt order; larger = more recent). `bool` is not an integer.
- Exactly the keys shown; any other key at any level is refused. `id` values are non-empty
  strings, unique within `stored`.
- Header names are tokens (RFC 9110 §5.6.2 tchar: ``!#$%&'*+-.^_`|~``, digits, ASCII
  letters), compared case-insensitively; two names in ONE map that are equal ignoring case
  are refused. Values are strings containing no CR, LF or NUL.

## Validators (lane conventions marked LC)

- ETag (RFC 9110 §8.8.3): a single entity-tag `"opaque"` or `W/"opaque"`, where opaque is
  zero or more of `!` / `#`–`~` / obs-text (0x80–0xFF code points). Leading/trailing
  spaces/tabs are trimmed first. Anything else (a list, missing quotes, lowercase `w/`) in
  the 304 OR in a stored response is refused.
- A strong validator is an ETag without `W/`. **LC1:** Last-Modified is always treated as a
  weak validator (RFC 9110 §8.8.2.2 makes it implicitly weak unless strength can be
  deduced; this contract never deduces it). A weak validator is a `W/` ETag or a
  Last-Modified field (any string value, compared after trimming spaces/tabs, exact
  octet equality).

## Selection — first match of (§4.3.4)

1. **strong**: the 304 carries a strong ETag S. Identified: every stored response whose
   ETag is strong and equal to S character-for-character (strong comparison). None → the
   decision is `must-not-update` (the MUST NOT of §4.3.4 bullet 1).
2. **weak**: no strong validator, but the 304 carries a weak ETag and/or Last-Modified.
   **LC2:** a stored response *corresponds* when, for every validator the 304 carries, the
   stored response carries the same field and it matches (ETag by weak comparison:
   opaque-tags equal ignoring `W/`; Last-Modified by trimmed equality). Identified: the
   single corresponding stored response with the largest `received`. **LC3:** if two or
   more corresponding responses share that largest `received`, refuse
   (`invalid_input: ambiguous most recent`). None correspond → `no-update`.
3. **no-validator**: the 304 carries neither ETag nor Last-Modified. Identified: the only
   stored response iff `stored` has exactly one element and it has neither ETag nor
   Last-Modified. Otherwise → `no-update`.

## Update (§3.2, applied to every identified response)

The updated header map starts from the stored headers and adds every 304 header field,
replacing a present field of the same (case-insensitive) name, EXCEPT these 304 fields,
which are never copied:

- `content-length` (§3.2 bullet 4);
- `connection`, and every field name listed in the 304's Connection value (comma-separated
  tokens, case-insensitive, empty members ignored) (§3.1 bullet 1);
- **LC4:** `keep-alive`, `proxy-connection`, `te`, `transfer-encoding`, `upgrade` — the
  lane's fixed reading of "some fields' semantics require them to be removed before
  forwarding" (§3.1 bullet 2; RFC 9110 §7.6.1 examples);
- `proxy-authenticate`, `proxy-authentication-info`, `proxy-authorization` (§3.1 bullet 4).

**LC5:** §3.2's "fields the stored response depends upon" and "automatically processed and
removed" exceptions, and the §3.2 MAY-omit allowance, are not modelled: no other field is
excluded. **LC6:** a 304 whose Cache-Control value contains `no-cache="` or `private="`
(qualified forms, §3.1 bullet 3) is refused as outside this contract.

Names in the output are lowercased; values are copied byte-for-byte (no trimming).

## Output

```
{"decision": "update" | "must-not-update" | "no-update",
 "rule": "strong" | "weak" | "no-validator",
 "updated": [{"id": <str>, "headers": {<lowercase name>: <str>, ...}}, ...]}
```

- `rule` is the first-match rule that applied (decided by the 304 alone).
- `decision` is `update` iff `updated` is non-empty.
- `updated` lists identified responses in input order. Empty for the other two decisions.
- Exit 0. Key order inside objects is not scored; list order is.

## Refusals (exit 1, stderr `invalid_input: …`, stdout empty)

Non-object input or invalid JSON; missing/extra keys; `status` other than the integer 304;
`stored` not a list; element not an object; `id` empty/non-string/duplicate; `received`
non-integer or bool; `headers` not an object; invalid header name; case-duplicate names
in one map; non-string value; CR/LF/NUL in a value; malformed ETag in the 304 or in any
stored response; LC3 ambiguity; LC6 qualified Cache-Control.

## Not covered

The initial-set computation (§4, erratum 9185), HEAD freshening (§4.3.5), invalidation
(§4.4), trailer fields, storing the 304 itself, Age/Date recalculation, any clock, network
or live cache. Conformance to this contract is not evidence about a deployed cache.
