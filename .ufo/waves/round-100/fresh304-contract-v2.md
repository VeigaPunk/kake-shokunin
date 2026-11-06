# Round 100 C2 — contract v2: freshening stored responses upon a 304

Contract v2 supersedes contract v1 (`.ufo/waves/round-99/fresh304-contract.md`). Everything v1
says holds unless a clause below marked **V2-n** changes it. The v2 clauses close the round-99
findings that were routed as R99-8 and R99-10 (`corpus/lessons/round-99.md`):
`w1/ReviewFresh/contract-findings.md` F1, F2, F3 and F10, the LC6 case question
(`w1/ExecTwinFresh/disagreements.md`), and the seven escape classes e1-e7
(`w1/CriticClaims/attacks.md` lines 92-98).

Sources (opened this round, retained under `.ufo/waves/round-100/sources/`):
- RFC 9111 §5.2 Cache-Control (grammar, case-insensitive directive names, both argument forms),
  §5.2.2.4 no-cache and §5.2.2.7 private (qualified forms), §5.2.3 Extension Directives
  ("A cache MUST ignore unrecognized cache directives"), §3.1 bullet 4 (proxy-specific fields
  MUST NOT be stored). Body: `.ufo/waves/round-99/sources/rfc9111.txt`, sha256 `aeb52adb…`,
  re-fetched 2026-11-06T01:28Z and byte-identical.
- RFC 9110 §5.5 Field Values ("A field value does not include leading or trailing whitespace"),
  §5.6.1.2 list recipient requirements (empty elements), §5.6.2 tokens, §5.6.4 quoted strings.
  Body: `.ufo/waves/round-100/sources/rfc9110.txt`, sha256
  `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`, 502 941 bytes, fetched
  2026-11-06T01:28Z, HTTP 200.

Candidate path: `scripts/freshen_304.py` (same path as v1; v2 replaces it). Standard library only.

## V2-1 — Cache-Control of the 304 (replaces v1 LC6; closes F1, F10 and the LC6 case question)

If the 304 carries a `Cache-Control` field (name compared case-insensitively), its value is parsed
as an RFC 9111 §5.2 list:

    Cache-Control   = #cache-directive
    cache-directive = token [ "=" ( token / quoted-string ) ]

with the RFC 9110 §5.6.1.2 recipient list syntax `[ element ] *( OWS "," OWS [ element ] )`
(empty elements are accepted and ignored; OWS = any run of SP / HTAB), token = RFC 9110 §5.6.2
tchar+, quoted-string per RFC 9110 §5.6.4 (qdtext = HTAB / SP / `!` / `#`-`[` / `]`-`~` /
obs-text; quoted-pair = `\` followed by HTAB / SP / VCHAR / obs-text; obs-text = U+0080-U+00FF as
in v1). A comma inside a quoted-string does not split the list. Whitespace is allowed only as OWS
around commas and at the two ends of the value (not around `=`).

- **V2-1a.** A value that does not parse is refused: `invalid_input: malformed cache-control`.
  **LC8:** refusing is the lane's choice (fail closed: an unparseable list cannot be checked for
  the qualified forms); RFC 9111 does not require it.
- **V2-1b.** A directive whose name equals `no-cache` or `private` **ignoring ASCII case** and that
  carries an argument in **either** form (token or quoted-string, including the empty quoted
  string `""`) is a qualified form (RFC 9111 §5.2.2.4, §5.2.2.7; §3.1 bullet 3). Such a 304 is
  refused as outside this contract: `invalid_input: qualified cache-control outside contract`.
- **V2-1c.** Any other directive — including an unrecognised extension whose name merely contains
  or ends in `no-cache` / `private` (`x-no-cache="a"`, `no-cachex=1`) — is ignored for this test
  (RFC 9111 §5.2.3). Unqualified `no-cache` / `private` (no `=`) are ignored for this test too.

Only the 304's Cache-Control is examined; stored Cache-Control values are copied as data.

## V2-2 — output values are field values without surrounding whitespace (closes F2)

Every header value in the output (`updated[*].headers`), whether it came from the stored response
or from the 304, has leading and trailing SP / HTAB removed (RFC 9110 §5.5). Inner whitespace is
kept byte-for-byte. ETag and Last-Modified comparison is unchanged from v1 (trimmed before
comparison). This replaces v1's "values are copied byte-for-byte (no trimming)".

## V2-3 — no proxy-specific field in an updated response (closes F3)

`proxy-authenticate`, `proxy-authentication-info` and `proxy-authorization` never appear in an
updated response: v1 already withheld them from the 304's copy; v2 also drops them when the stored
response carries them (RFC 9111 §3.1 bullet 4: they "MUST NOT be stored"; the updated header map
is the new stored response). No other stored field is dropped: stored `connection`, hop-by-hop
(LC4 names), `content-length` and any other stored fields stay (e1).

## Clarifications binding the escape classes (v1 text, now with hand cases)

- **e1:** the update starts from ALL stored fields except V2-3's three names.
- **e2:** a malformed ETag in ANY stored response is refused, whether or not selection reads it.
- **e3:** Last-Modified comparison trims SP **and** HTAB at both ends.
- **e4:** on refusal stdout is EMPTY (zero bytes). On a decision stdout is one JSON object with
  no leading whitespace, optionally followed by exactly one `\n`, nothing else.
- **e5:** stdin that is not valid JSON (or not UTF-8) is refused with `invalid_input:` on stderr
  and exit 1, never a traceback.
- **e6:** `age` and every other 304 field not excluded by v1/V2-3 is copied (LC5 unchanged).
- **e7:** LC3 (tie at the largest `received` → refuse) applies whatever validators the 304 carries
  (ETag, Last-Modified, or both).

## Scoring (counter `.ufo/waves/round-100/c100_fresh304.py`)

The candidate is run inside a `bwrap` sandbox per case: new user, PID, network, IPC and UTS
namespaces, read-only `/usr`, a private `/tmp`, its own `/proc` (it cannot see the counter's
process), empty environment except PATH/LANG, only the candidate file bound in, cwd `/tmp`
(closes R99-9 W1-W4 for this counter). If `bwrap` cannot start, the counter exits 2
(could-not-evaluate) and scores nothing.

## Not covered (unchanged from v1, plus F12's items)

The initial-set computation (§4, erratum EID 9185), HEAD freshening (§4.3.5), invalidation
(§4.4), §3.4 partial-content combination, §4.1 selecting-header re-association, trailer fields,
storing the 304 itself, Age/Date recalculation, any clock, network or live cache. Conformance is
not evidence about a deployed cache. F4-F9, F11 stay open (routed).
