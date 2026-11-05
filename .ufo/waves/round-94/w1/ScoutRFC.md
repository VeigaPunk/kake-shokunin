VERDICT: S477 (§9.1) and S478 (§5.6.1.2) quotes are located and both verified exact substrings of the fetched RFC 9110 body; S471–S476 anchors re-open byte-identical; two anchor-coverage defects found in the drafted S477/S478 registry rows (the HTAB/OWS rule and the empty-element sentences sit outside the cited line ranges).

# ScoutRFC — round 94 w1 — primary-source reconnaissance for S477/S478 and the C2 v2 grammar behind M37/M40

Seat: ScoutRFC (scout, leaf, no dispatch). Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Scope: one GET of the URL named in the item (`https://www.rfc-editor.org/rfc/rfc9110.txt`), location of the
§9.1 case-sensitivity sentence and the §5.6.1 list-syntax material, re-opening of the S471–S476 anchor
lines, and the two new registry rows' quote evidence.

## 1. The one GET

```
$ mkdir -p /fast/scratch/hyaku/kake-r94/ScoutRFC && cd /fast/scratch/hyaku/kake-r94/ScoutRFC \
  && curl -sS -o rfc9110.txt -w '%{http_code} %{size_download}\n' https://www.rfc-editor.org/rfc/rfc9110.txt
200 502941
$ ls -l rfc9110.txt   # 502941 bytes
$ sha256sum rfc9110.txt
21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a  rfc9110.txt
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-11-05T15:00:17Z
```
Exit status 0 for every command above. Exactly one GET was issued; no other URL was fetched, no other
network read was performed.

Receipt: `.ufo/waves/round-94/w1/ScoutRFC/fetch.txt` (HTTP status 200, 502941 bytes, sha256
`21c1cdce…7232a`, accessed_utc `2026-11-05T15:00:17Z`).

The body is 502941 bytes (< 1 MB), so the retained copy was written to
`.ufo/waves/round-94/w1/ScoutRFC/rfc9110.txt` (sha256 identical to the fetched body, verified with
`sha256sum`; `stat -c %s` = 502941).

**Cross-check against the lane's own retained body:** the fetched body is byte-identical to the
round-93 retained copy:
```
$ cmp /fast/scratch/hyaku/kake-r94/ScoutRFC/rfc9110.txt \
      .ufo/waves/round-93/L1/src/rfc9110.txt   # exit 0, no output
```
and the round-93 retained copy is the tracked file
`.ufo/waves/round-93/L1/src/rfc9110.txt` (git: `git ls-tree -r --name-only HEAD` lists it; last touched by
commit `bb8012fe`). So every S471–S475 line number in the registry still denotes the same bytes, and the
sha256 recorded in S471–S475 (`21c1cdce…7232a`) is the digest of the body read this round.

## 2. (a) §9.1 — the method-token case-sensitivity sentence (row S477)

Heading line: **3728** — `9.1.  Overview`
Body lines: **3748–3749** (the sentence itself); the sentence continues into 3750–3751 ("By convention …").

Verbatim body, lines 3748–3751:
```
3748:    The method token is case-sensitive because it might be used as a
3749:    gateway to object-based systems with case-sensitive method names.  By
3750:    convention, standardized methods are defined in all-uppercase US-
3751:    ASCII letters.
```
Located quote (20 words, exact substring of the whitespace-normalized body):
> The method token is case-sensitive because it might be used as a gateway to object-based systems with case-sensitive method names.

`exact_substring = true`, checked by a script that normalizes the body with `re.sub(r"\s+", " ", body)`
and tests membership (see §6).

Grounding for the C2 v2 expectation **M37** (`inm/lowercase-method-is-not-get`, hand case in
`.ufo/waves/round-94/c94_conditional.py:325`): §9.1 makes the method token case-sensitive, so `get` is a
different method token from `GET`; combined with the already-registered S473 (§13.1.2, lines 5928–5932:
304 "if the request method is GET or HEAD", 412 for all other methods), the lowercase-`get` case yields
412, not 304 — which is what the frozen hand case asserts. The counter's own docstring names M37 as
"method compared case-insensitively in the 304/412 test"
(`.ufo/waves/round-94/c94_conditional.py:305` region).

## 3. (b) §5.6.1 — list syntax (row S478)

Three separate items were requested; only two of them live in §5.6.1 itself.

**(b1) Recipients accept empty list elements.** Sub-section heading line **1693** —
`5.6.1.2.  Recipient Requirements`. Body lines **1695–1699**:
```
1695:    Empty elements do not contribute to the count of elements present.  A
1696:    recipient MUST parse and ignore a reasonable number of empty list
1697:    elements: enough to handle common mistakes by senders that merge
1698:    values, but not so much that they could be used as a denial-of-
1699:    service mechanism.  In other words, a recipient MUST accept lists
```
**(b2) OWS / whitespace around list members, and the recipient grammar.** Body lines **1699–1702**:
```
1699:    service mechanism.  In other words, a recipient MUST accept lists
1700:    that satisfy the following syntax:
1701:
1702:      #element => [ element ] *( OWS "," OWS [ element ] )
```
Located quote for S478 (23 words, exact substring of the whitespace-normalized body, spanning 1699–1702):
> a recipient MUST accept lists that satisfy the following syntax: #element => [ element ] *( OWS "," OWS [ element ] )

`exact_substring = true`.

**(b3) "tab is whitespace" — `OWS = *( SP / HTAB )` is NOT in §5.6.1.** It is defined in **§5.6.3
Whitespace**, heading line **1745**, production at lines **1774–1775**:
```
1774:      OWS            = *( SP / HTAB )
1775:                     ; optional whitespace
```
and §5.6.1 only *points* at it, at lines 1670–1672:
```
1670:    indicating at least <n> and at most <m> elements, each separated by a
1671:    single comma (",") and optional whitespace (OWS, defined in
1672:    Section 5.6.3).
```
Two further §5.6.3 lines bear on M40 and are the strongest single-sentence ground for "a recipient must
tolerate HTAB where OWS is expected", lines **1762–1764**:
```
1762:    OWS and RWS have the same semantics as a single SP.  Any content
1763:    known to be defined as OWS or RWS MAY be replaced with a single SP
1764:    before interpreting it or forwarding the message downstream.
```
Located supporting quotes (all exact substrings after whitespace normalization; not stored in
`quotes.json`, which carries only the two registry rows):
- `A recipient MUST parse and ignore a reasonable number of empty list elements` (13 words; §5.6.1.2,
  lines 1695–1699) — exact_substring true.
- `each separated by a single comma (",") and optional whitespace (OWS, defined in Section 5.6.3)` (15 words;
  §5.6.1, lines 1670–1672) — exact_substring true.
- `OWS = *( SP / HTAB ) ; optional whitespace` (10 words; §5.6.3, lines 1774–1775) — exact_substring true.

Grounding for the C2 v2 expectation **M40** (`inm/htab-around-list-members`, hand case at
`.ufo/waves/round-94/c94_conditional.py:327`): the recipient grammar of §5.6.1.2 places OWS around each
comma, and OWS is `*( SP / HTAB )` (§5.6.3 lines 1774–1775) with "the same semantics as a single SP"
(1762–1764), so a recipient must treat HTAB as whitespace there; the frozen hand case feeds
`if_none_match: '"9",\t"1"'` and expects 304. The v1 counter
`.ufo/waves/round-93/c93_conditional.py` contains neither new hand case
(`grep -c 'lowercase-method-is-not-get\|htab-around-list-members'` → 0, exit 1), while the v2 counter
contains both (`.ufo/waves/round-94/c94_conditional.py:325` and `:327`) — consistent with the round's
"v1 = 44 hand cases, v2 = 53" description.

## 4. (c) S471–S476 anchors re-opened — every cited line still reads the same

Method: the fresh 9110 body for S471–S475; the lane's tracked retained 9111 body
`.ufo/waves/round-93/L1/src/rfc9111.txt` for S476 (the item named only the 9110 URL for the GET; S476's
source is RFC 9111, whose retained copy is sha256 `aeb52adb…302cf3e`, the same digest S476 records).
All lines copied verbatim, not paraphrased.

### S471 — §13.2.2 Precedence of Preconditions (heading line 6222)
```
6222: 13.2.2.  Precedence of Preconditions
6233:    A recipient cache or origin server MUST evaluate the request
6234:    preconditions defined by this specification in the following order:
6236:    1.  When recipient is the origin server and If-Match is present,
6237:        evaluate the If-Match precondition:
6239:        *  if true, continue to step 3
6241:        *  if false, respond 412 (Precondition Failed) unless it can be
6242:           determined that the state-changing request has already
6243:           succeeded (see Section 13.1.1)
6245:    2.  When recipient is the origin server, If-Match is not present, and
6246:        If-Unmodified-Since is present, evaluate the If-Unmodified-Since
6247:        precondition:
6249:        *  if true, continue to step 3
6251:        *  if false, respond 412 (Precondition Failed) unless it can be
6252:           determined that the state-changing request has already
6253:           succeeded (see Section 13.1.4)
6255:    3.  When If-None-Match is present, evaluate the If-None-Match
6256:        precondition:
6258:        *  if true, continue to step 5
6260:        *  if false for GET/HEAD, respond 304 (Not Modified)
6262:        *  if false for other methods, respond 412 (Precondition Failed)
6264:    4.  When the method is GET or HEAD, If-None-Match is not present, and
6265:        If-Modified-Since is present, evaluate the If-Modified-Since
6266:        precondition:
6268:        *  if true, continue to step 5
6270:        *  if false, respond 304 (Not Modified)
6272:    5.  When the method is GET and both Range and If-Range are present,
6273:        evaluate the If-Range precondition:
6275:        *  if true and the Range is applicable to the selected
6276:           representation, respond 206 (Partial Content)
6278:        *  otherwise, ignore the Range header field and respond 200 (OK)
6280:    6.  Otherwise,
6282:        *  perform the requested method and respond according to its
```
Matches the registry row's cited ranges (6222; 6233–6234; 6236–6282). Note the ordered-steps range ends
mid-sentence at 6282; 6283 is `          success or failure.`

### S472 — §13.1.1 If-Match (heading line 5785)
```
5785: 13.1.1.  If-Match
5794:    An origin server MUST use the strong comparison function when
5795:    comparing entity tags for If-Match (Section 8.8.3.2), since the
5796:    client intends this precondition to prevent the method from being
5797:    applied if there have been any changes to the representation data.
5799:      If-Match = "*" / #entity-tag
5820:    To evaluate a received If-Match header field:
5822:    1.  If the field value is "*", the condition is true if the origin
5823:        server has a current representation for the target resource.
5825:    2.  If the field value is a list of entity tags, the condition is
5826:        true if any of the listed tags match the entity tag of the
5827:        selected representation.
5829:    3.  Otherwise, the condition is false.
5831:    An origin server that evaluates an If-Match condition MUST NOT
5832:    perform the requested method if the condition evaluates to false.
5833:    Instead, the origin server MAY indicate that the conditional request
```
Matches the row's cited ranges (5785; 5794–5797; 5799; 5820–5829; 5831–5833).

### S473 — §13.1.2 If-None-Match (heading line 5872)
```
5872: 13.1.2.  If-None-Match
5880:    A recipient MUST use the weak comparison function when comparing
5881:    entity tags for If-None-Match (Section 8.8.3.2), since weak entity
5882:    tags can be used for cache validation even if there have been changes
5883:    to the representation data.
5885:      If-None-Match = "*" / #entity-tag
5917:    To evaluate a received If-None-Match header field:
5919:    1.  If the field value is "*", the condition is false if the origin
5920:        server has a current representation for the target resource.
5922:    2.  If the field value is a list of entity tags, the condition is
5923:        false if one of the listed tags matches the entity tag of the
5924:        selected representation.
5926:    3.  Otherwise, the condition is true.
5928:    An origin server that evaluates an If-None-Match condition MUST NOT
5929:    perform the requested method if the condition evaluates to false;
5930:    instead, the origin server MUST respond with either a) the 304 (Not
5931:    Modified) status code if the request method is GET or HEAD or b) the
5932:    412 (Precondition Failed) status code for all other request methods.
```
Matches the row's cited ranges (5872; 5880–5883; 5885; 5917–5926; 5928–5932).

### S474 — §13.1.3 If-Modified-Since / §13.1.4 If-Unmodified-Since (heading lines 5942 and 6023)
```
5942: 13.1.3.  If-Modified-Since
5956:    A recipient MUST ignore If-Modified-Since if the request contains an
5957:    If-None-Match header field; the condition in If-None-Match is
5958:    considered to be a more accurate replacement for the condition in If-
5963:    A recipient MUST ignore the If-Modified-Since header field if the
5964:    received field value is not a valid HTTP-date, the field value has
5965:    more than one member, or if the request method is neither GET nor
5966:    HEAD.
5968:    A recipient MUST ignore the If-Modified-Since header field if the
5969:    resource does not have a modification date available.
6004:    performing the method.
6006:    To evaluate a received If-Modified-Since header field:
6008:    1.  If the selected representation's last modification date is
6009:        earlier or equal to the date provided in the field value, the
6010:        condition is false.
6023: 13.1.4.  If-Unmodified-Since
6037:    A recipient MUST ignore If-Unmodified-Since if the request contains
6038:    an If-Match header field; the condition in If-Match is considered to
6039:    be a more accurate replacement for the condition in If-Unmodified-
6043:    A recipient MUST ignore the If-Unmodified-Since header field if the
6044:    received field value is not a valid HTTP-date (including when the
6045:    field value appears to be a list of dates).
6047:    A recipient MUST ignore the If-Unmodified-Since header field if the
6048:    resource does not have a modification date available.
6072:        earlier than or equal to the date provided in the field value,
6073:        the condition is true.
```
Matches the row's cited ranges (5942; 5956–5958; 5963–5966; 5968–5969; 6004–6011; 6023; 6037–6039;
6043–6045; 6047–6048; 6072–6073). Three of the cited ranges end mid-sentence (5958 ends at `If-`,
6039 ends at `If-Unmodified-`, 6072 starts mid-sentence) — same text as before, no drift.

### S475 — §8.8.3.2 Comparison (heading line 3643)
```
3643: 8.8.3.2.  Comparison
3648:    "Strong comparison":  two entity tags are equivalent if both are not
3649:       weak and their opaque-tags match character-by-character.
3651:    "Weak comparison":  two entity tags are equivalent if their opaque-
3652:       tags match character-by-character, regardless of either or both
3653:       being tagged as "weak".
3658:    +========+========+===================+=================+
3659:    | ETag 1 | ETag 2 | Strong Comparison | Weak Comparison |
3660:    +========+========+===================+=================+
3661:    | W/"1"  | W/"1"  | no match          | match           |
3662:    +--------+--------+-------------------+-----------------+
3663:    | W/"1"  | W/"2"  | no match          | no match        |
3664:    +--------+--------+-------------------+-----------------+
3665:    | W/"1"  | "1"    | no match          | match           |
3666:    +--------+--------+-------------------+-----------------+
3667:    | "1"    | "1"    | match             | match           |
3668:    +--------+--------+-------------------+-----------------+
3670:                            Table 3
```
Matches the row's cited ranges (3643; 3648–3649; 3651–3653; 3658–3668; caption at 3670). The caption
line 3670 is the bare string `Table 3`; the table's own lead-in sentence is at lines 3655–3656.

### S476 — RFC 9111 §4.3.2 Handling a Received Validation Request (heading line 866)
Read from the tracked retained body `.ufo/waves/round-93/L1/src/rfc9111.txt`
(sha256 `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`, the digest the row records).
```
866: 4.3.2.  Handling a Received Validation Request
881:    A cache MUST NOT evaluate conditional header fields that only apply
882:    to an origin server, occur in a request with semantics that cannot be
883:    satisfied with a cached response, or occur in a request with a target
884:    resource for which it has no stored responses; such preconditions are
885:    likely intended for some other (inbound) server.
887:    The proper evaluation of conditional requests by a cache depends on
888:    the received precondition header fields and their precedence.  In
889:    summary, the If-Match and If-Unmodified-Since conditional header
890:    fields are not applicable to a cache, and If-None-Match takes
891:    precedence over If-Modified-Since.  See Section 13.2.2 of [HTTP] for
```
Matches the row's cited ranges (866; 881–885; 887–891).

## 5. Defects found (all reporting-only; no frozen or other seat's file was edited)

**D1 — S477's anchor range spans a hyphenation break, so the "all-uppercase" clause is not an exact
substring.** The plain-text body breaks the token `US-ASCII` across lines 3750–3751 (`US-` / `ASCII`).
After whitespace normalization the body reads `… all-uppercase US- ASCII letters.`, so the sentence
`By convention, standardized methods are defined in all-uppercase US-ASCII letters.` is **not** an exact
substring (script-checked: `False`). The registry row drafted at `corpus/SOURCES.md:223` cites
`plain-text lines 3748-3751` and its `teaches` clause repeats "standardized methods are all-uppercase by
convention". A knowledge entry that quotes that clause verbatim and checks it as an exact substring of the
body will fail. Fix options for the row owner (ExecSourceRows) and the scribe: quote only the
case-sensitivity sentence (3748–3749, verified exact, and the one actually needed for M37), or cite the
hyphenated form `US- ASCII` / lines 3750–3751 explicitly. The S477 quote I certified avoids the break.

**D2 — S478's anchor range does not cover the clauses its `teaches` field asserts.** The drafted row
(`corpus/SOURCES.md:224`) cites `subsection 5.6.1.2 Recipient Requirements (heading line 1693), plain-text
lines 1699-1702` while its `teaches` clause asserts three things: that a recipient must accept lists with
empty elements, that OWS appears around each comma, and that empty elements do not count toward the number
of elements present. Only the second and part of the first are inside 1699–1702. "Empty elements do not
contribute to the count of elements present" is at line **1695**; "A recipient MUST parse and ignore a
reasonable number of empty list elements" spans **1696–1697**; both are outside the cited range. The
recommended citation is `lines 1695–1702` (empty-element sentence + accept syntax + grammar) — which is
also where the already-registered S465 points (`section 5.6.1.2 empty-element sentence at lines 1695–1699`),
so the two rows overlap and the registry's distinct-scope requirement needs an explicit statement.
Reported to the round, not edited: `corpus/SOURCES.md` is ExecSourceRows' file.

**D3 — the tab-is-whitespace rule the M40 expectation rests on is in §5.6.3, not §5.6.1.** The item text
places `OWS = *( SP / HTAB )` under "§5.6.1 list syntax"; in the document it is §5.6.3 (heading line 1745,
production lines 1774–1775), and §5.6.1 only cross-references it (lines 1671–1672). No registry row
currently cites §5.6.3 (`grep -n '5\.6\.3\|OWS' corpus/SOURCES.md` returns only the drafted S478 row). If the
claim for M40 must cite "a row opened this round" (freeze.md §Sources), S478 as drafted does not by itself
carry the HTAB ground — the row needs the §5.6.3 production (and ideally the "same semantics as a single SP"
sentence at 1762–1764) in its anchor, or a second new row is needed. This is a scoping gap in the drafted
row, not a defect in the RFC.

**D4 — the empty-member refusal the instrument relies on is a lane adapter convention, not an RFC rule.**
§5.6.1.2 says a recipient must *parse and ignore* empty list elements; `scripts/conditional_eval.py:101,103`
refuses them ("has an empty list member"). This is already documented as an adapter convention by S465 and
`corpus/lessons/round-88.md:36` ("refusal is this lane's adapter convention"). Nothing in the M37/M40
expectations depends on it (M40's HTAB case has no empty member), but any S478 text that says "a recipient
MUST accept lists with empty elements" must not be read as endorsing the lane's refusal of them — the
opposite. The row's `teaches` wording ("A recipient MUST accept lists with empty elements and OWS around
each comma") is RFC-accurate; the instrument's behaviour is stricter than the RFC and is declared as such
elsewhere.

**D5 — minor, non-blocking:** S471's cited ordered-steps range ends mid-sentence at 6282
(`*  perform the requested method and respond according to its`); the sentence completes at 6283. S475's
"caption at line 3670" is the bare label `Table 3`; the descriptive lead-in is 3655–3656. Both are
pre-existing in rows opened on 2026-11-04 and neither affects a claim.

## 6. Reproducible check of `quotes.json`

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin && python3 -B - <<'PY'
import json,re,hashlib
D=".ufo/waves/round-94/w1/ScoutRFC"
raw=open(D+"/rfc9110.txt","rb").read(); body=raw.decode("utf-8")
norm=re.sub(r"\s+"," ",body)
for r in json.load(open(D+"/quotes.json")):
    print(r["id"],r["section"],"heading",r["heading_line"],r["body_line_range"],
          "words",r["quote_words"],"exact",r["quote"] in norm,"declared",r["exact_substring"],
          "status",r["http_status"],"bytes",r["bytes"])
PY
S477 9.1 Overview heading 3728 3748-3749 words 20 exact True declared True status 200 bytes 502941
S478 5.6.1.2 Recipient Requirements heading 1693 1699-1702 words 23 exact True declared True status 200 bytes 502941
```
Exit status 0. Heading lines re-read from the body:
`S477 heading text: '9.1.  Overview'`, `S478 heading text: '5.6.1.2.  Recipient Requirements'`.

Files written by this seat (all under the item's own paths):
- `.ufo/waves/round-94/w1/ScoutRFC/fetch.txt` — HTTP status, bytes, sha256, accessed_utc, command, client.
- `.ufo/waves/round-94/w1/ScoutRFC/rfc9110.txt` — retained body (502941 bytes, sha256 `21c1cdce…7232a`).
- `.ufo/waves/round-94/w1/ScoutRFC/quotes.json` — the two rows (S477, S478); sha256
  `3ae2187015cf19e5abbe7cbb85c3e0363995ea9589a1702a3433e459924eb536`.
- `.ufo/waves/round-94/w1/ScoutRFC.md` — this report.

No git/jj mutation was performed in the lane; read-only `git log`/`ls-tree`/`status` were used. No clone
or fixture was needed (no committed-revision measurement was in scope). Scratch directory
`/fast/scratch/hyaku/kake-r94/ScoutRFC/` deleted after the receipts were copied into the lane; a
`/fast/scratch` path is not cited as evidence above — the lane receipts are.

## 7. Tooling

No tool was installed, upgraded or removed. Versions used, all pre-existing on the host:
`curl 8.23.0 (x86_64-pc-linux-gnu) libcurl/8.23.0 OpenSSL/3.6.5` (distribution package, no install),
`Python 3.14.8`, `sha256sum 0.8.0` (coreutils), `git` (read-only commands only). No `pacman`, `uv tool`,
`npm` or `cargo` invocation; no PATH directory touched; no host sysctl touched; no service restarted.

## 8. Honest limits

- One GET, one URL. RFC 9111 (S476's source) was **not** re-fetched; its lines were read from the lane's
  tracked retained body whose sha256 equals the digest S476 records, so "still reads the same" for S476 is a
  statement about the retained copy, not about a fresh network read. S471–S475 are statements about a fresh
  9110 read, but the body is byte-identical to the retained one, so they are equally statements about
  unchanged bytes.
- `exact_substring` was checked against the whitespace-normalized body (`\s+` → single space). Line-break
  hyphenation is *not* undone by that normalization, which is exactly why D1 occurs; my two certified quotes
  contain no hyphenation break.
- The counter files were read, not run: the M37/M40/M40 grounds above are read from the frozen counters'
  hand cases and the mutant list
  (`.ufo/waves/round-93/w1/recovered-partial/MutConditional/mutants-posgood.json`: M37 "1 method compared
  case-insensitively in the 304/412 test", M40 "4 list syntax: HTAB not accepted around list members",
  base file `scripts/conditional_eval.py`, source `.ufo/waves/round-93/frozen/pos-good.py`). Whether the v2
  counter actually kills 40/40 is the C2 seats' measurement, not mine.
- No claim is made about whether the RFC requires a recipient to accept empty members in *this* instrument's
  sense; only what the document says at the cited lines (D4).
