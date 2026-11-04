# ScoutSpec — kake round 88, wave 1

Seat: `ScoutSpec` (leaf member, no subagent dispatch).
Lane root: `/home/vgpnk/Projects/shokunin/kake-shokunin` (LANE).
Scope of this seat: open the primary sources for RFC 9111 §4.1 and RFC 9110 §12.5.5 / §5.2
byte-exactly, state what they do not prove, and answer the SOURCES-row id / duplicate-class
question for the round's new RFC 9111 row. Finders only; no production writes.

---

## 1. Source access receipts

All GETs were single unauthenticated `curl` requests to the URLs named in the seat item. No
credentials, cookies, session values, or account state were sent. No publish/deploy occurred.

| URL | HTTP | bytes | sha256 | accessed (UTC) | response headers |
|---|---|---|---|---|---|
| `https://httpwg.org/specs/rfc9111.html` | 200 | 178573 | `999f401328ed8991d172aeb1cd4ab048630928437af2401d3e39552c4a073f64` | 2026-11-04T18:52:06Z | `headers-9111.txt` (last-modified `Mon, 19 Oct 2026 01:13:54 GMT`, etag `"6ad56ed2-2b98d"`) |
| `https://httpwg.org/specs/rfc9110.html` | 200 | 915065 | `5313be9ca076b6470ca9e6fecc3c2deaecb1eb9f6d79cd53c51b3bd65f4fbac6` | 2026-11-04T18:52:10Z | `headers-9110.txt` (last-modified `Mon, 19 Oct 2026 01:13:54 GMT`, etag `"6ad56ed2-df679"`) |

Raw HTML retained under this seat's wave directory
`LANE/.ufo/waves/round-88/w1/ScoutSpec/`: `rfc9111.html`, `rfc9110.html`,
`headers-9111.txt`, `headers-9110.txt`. The two sha256 values above are re-verified against
those retained files. Both are the httpwg.org rendered HTML (the RFC Editor XML/other mirrors
were not fetched — the item named these two URLs only).

Byte-exactness method: each paragraph was extracted from the raw HTML by taking the
`rfc.section.<n>.<m>.p.<k>` div, stripping tags, unescaping entities and collapsing runs of
spaces/tabs (the RFC 9111 §4.1 transformation list is a `<ul>`, so its three items were
extracted individually). Every quote below was then asserted to be an exact substring of the
extracted paragraph text (`q in src`), and its word count checked ≤ 25. **23 / 23 verified.**

---

## 2. Located quotes (23 verified, each ≤ 25 words, byte-exact)

### RFC 9111 §4.1 — Calculating Cache Keys with the Vary Header Field

| # | Locator | Quote | words |
|---|---|---|---|
| Q1 | §4.1 p.1 — the MUST NOT sentence | "the cache MUST NOT use that stored response without revalidation unless all the presented request header fields nominated by that Vary field value match" | 24 |
| Q2 | §4.1 p.2 | "if and only if those in the first request can be transformed to those in the second request by applying any of the following" | 24 |
| Q3 | §4.1 p.3, item 1 | "adding or removing whitespace, where allowed in the header field's syntax" | 11 |
| Q4 | §4.1 p.3, item 2 | "combining multiple header field lines with the same field name (see Section 5.2 of [HTTP])" | 15 |
| Q5 | §4.1 p.3, item 3 | "normalizing both header field values in a way that is known to have identical semantics, according to the header field's specification" | 21 |
| Q6 | §4.1 p.3, worked example | "reordering field values when order is not significant; case-normalization, where values are defined to be case-insensitive" | 16 |
| Q7 | §4.1 p.4 — a field absent from a request | "If (after any normalization that might take place) a header field is absent from a request, it can only match another request" | 22 |
| Q8 | §4.1 p.5 — a Vary member `*` | "A stored response with a Vary header field value containing a member \"*\" always fails to match." | 17 |

Full §4.1 p.4, for the record (28 words, so it is *not* one of the ≤25-word quotes — quoted
here only because the seat item asks for "the sentence on a field absent from a request"):

> If (after any normalization that might take place) a header field is absent from a request, it can only match another request if it is also absent there.

### RFC 9110 §12.5.5 — Vary (definition and ABNF)

| # | Locator | Quote | words |
|---|---|---|---|
| Q9 | §12.5.5 p.1 | "The \"Vary\" header field in a response describes what parts of a request message, aside from the method and target URI, might have influenced" | 24 |
| Q10 | §12.5.5 p.2 — **ABNF** | "Vary = #( \"*\" / field-name )" | 7 |
| Q11 | §12.5.5 p.3 | "A Vary field value is either the wildcard member \"*\" or a list of request field names, known as the selecting header fields" | 23 |
| Q12 | §12.5.5 p.4 | "A proxy MUST NOT generate \"*\" in a Vary field value." | 11 |
| Q13 | §12.5.5 p.9 | "Vary expands the cache key required to match a new request to the stored cache entry." | 16 |

### RFC 9110 §5.2 / §5.3 — combining field lines with the same name

| # | Locator | Quote | words |
|---|---|---|---|
| Q14 | §5.2 p.2 — combined field value | "its combined field value consists of the list of corresponding field line values within that section, concatenated in order" | 19 |
| Q15 | §5.3 p.1 | "A recipient MAY combine multiple field lines within a field section that have the same field name into one field line" | 21 |
| Q16 | §5.3 p.2 | "The order in which field lines with the same name are received is therefore significant to the interpretation of the field value" | 22 |

Full §5.2 p.2 (28 words, so not a ≤25-word quote):

> When a field name is only present once in a section, the combined field value for that field consists of the corresponding field line value. When a field name is repeated within a section, its combined field value consists of the list of corresponding field line values within that section, concatenated in order, with each field line value separated by a comma.

Supporting (used for the defect analysis in §5):

| # | Locator | Quote | words |
|---|---|---|---|
| Q17 | §5.1 p.2 — **ABNF** | "field-name = token" | 3 |
| Q18 | §5.1 p.3 | "Field names are case-insensitive and ought to be registered within the \"Hypertext Transfer Protocol (HTTP) Field Name Registry\"" | 18 |
| Q19 | §5.5 p.3 | "A field value does not include leading or trailing whitespace." | 10 |
| Q20 | §5.6.2 p.2 — **ABNF** | "token = 1*tchar" | 3 |
| Q21 | §5.6.1.2 p.1 | "A recipient MUST parse and ignore a reasonable number of empty list elements" | 13 |
| Q22 | §5.6.1.2 p.2 — **ABNF** | "#element => [ element ] *( OWS \",\" OWS [ element ] )" | 13 |
| Q23 | §8.4.1 p.3 | "All content codings are case-insensitive and ought to be registered within the \"HTTP Content Coding Registry\"" | 16 |

### Answers to the four required quote targets

- **(a) the §4.1 MUST NOT sentence** → Q1 (§4.1 p.1).
- **(b) all three permitted transformations** → Q3, Q4, Q5 (§4.1 p.3 items 1–3), with Q6 as
  the spec's own worked examples of item 3.
- **(c) the sentence on a field absent from a request** → Q7 (§4.1 p.4, trimmed to ≤25 words)
  plus the full 28-word sentence quoted above.
- **(d) the sentence on a Vary member `*`** → Q8 (§4.1 p.5).

---

## 3. What none of this proves

The retrieved text establishes **only** the §4.1 matching rule as a normative statement about
when a cache may reuse a stored response. None of it proves, and none of it may be cited for:

- **Cache-key construction.** RFC 9110 §12.5.5 p.9 says Vary "expands the cache key required
  to match a new request to the stored cache entry" — that is a *statement about cache keys*,
  not a construction algorithm. No canonical key format, no key serialisation, no key
  ordering, no hashing, no per-field key composition is specified here.
- **Storage.** Nothing here says what a cache stores, how a stored response is indexed, how
  variants are enumerated, or how many stored responses may exist for one URI. §4.1 p.6–p.8
  (choosing among multiple matches; the `If no stored response matches` path) are selection
  rules *conditional on* a storage model that this text does not define.
- **Revalidation.** §4.1 p.1 is a constraint *on* revalidation ("MUST NOT use … without
  revalidation unless …"), not a specification of revalidation. §4.3 (validating a stored
  response) was not retrieved and is not quoted. No validator selection, no conditional
  request construction, no 304 handling is established.
- **Freshness.** §4.1 is under "4.1" and sits *before* §4.2 Freshness. No age, freshness
  lifetime, staleness, `Cache-Control` directive, or `Age` computation is grounded here. (The
  lane's separate rows S456/S457/S461/S462 cover those; this seat did not re-open them.)
- **Browser behaviour.** No user-agent cache, no browser cache partitioning, no
  heuristic-freshness rule, no private-vs-shared distinction, and no `Vary` handling in a
  user agent is established. §12.5.5 p.8 mentions informing user agents that a response was
  subject to content negotiation — that is a stated purpose of the field, not a description
  of any user agent's behaviour.
- Also not established: any statement about a specific cache implementation, any live surface,
  or any assertion that a surface is clean.

Two further limits the round's own profile statement depends on:

- **"Conservative" is one-directional.** The §4.1 transformation list (Q3–Q5) is permissive:
  it enumerates transformations under which two requests' fields *may* be considered equal.
  A reader that applies none of them is strictly more conservative and never mis-matches in
  the "match" direction; a reader that applies item 3 wrongly can produce a *false* `match`.
  The round's profile (contract.md, C2 "Profile (declared, bounded)") correctly forbids
  field-specific normalisation, which is what keeps the false-`match` direction closed.
- **Field-specific normalisation is genuinely field-dependent.** Q6's "reordering … when
  order is not significant; case-normalization, where values are defined to be
  case-insensitive" is conditioned on the *field's own specification*. Q23 shows one concrete
  instance: RFC 9110 §8.4.1 says content codings are case-insensitive, so `GZip` and `gzip`
  *are* equal for `Accept-Encoding` under item 3 — yet frozen case 3 labels that
  `mismatch` because the profile declines to apply item 3. That is a legal conservative
  choice, but the knowledge entry must say so: it is a *profile choice*, not a reading of
  RFC 9111. The RFC's own §4.1 permits a `match` there.

---

## 4. SOURCES row: next free id, and duplicate classification

### 4.1 Registry state read (LANE/corpus/SOURCES.md)

Last rows, read verbatim (id / kind / tier / status / opened / recheck / used-by):

- **S460** — Chrome UX Report API, keyless caller observation (lane own-work) — own-work / B /
  mined / 2026-11-04 / 180d / `corpus/knowledge/crux-keyless-check.md`
- **S461** — RFC 9111 newly grounded duplicate and explicit lifetime rules —
  `https://httpwg.org/specs/rfc9111.html` — spec / A / mined / 2026-11-04 / 180d /
  `corpus/knowledge/cache-control-effective.md`; its `teaches` opens `supersedes S457`
- **S462** — RFC 9111, Calculating Age — `https://httpwg.org/specs/rfc9111.html#age.calculations`
  — spec / A / mined / 2026-11-04 / 180d / `corpus/knowledge/cache-current-age.md`

Registry census (measured, not assumed):

```
rows 200 · unique ids 200 · max id S462 · min id S001
gap ranges (unused, never voided): 140-248, 250-261, 264-272, 275-285, 287-311,
                                    313-328, 330-366, 368-371, 375-389, 391-408, 410-415
```

**Next free id = `S463`.** Evidence, three ways:

1. `S463` does not occur anywhere in `LANE/corpus/SOURCES.md` (grep for `\bS4[6-9][0-9]\b`
   returns only S460/S461/S462), and it is not in the `## Paths` / `## Search log` sections.
2. `CORPUS.md` §SOURCES "Shape" — *"`id` — `S` + 3 or more digits, the next unused; never
   reused."* The lane's own working rule, recorded in `corpus/lessons/round-57.md` and
   `round-58.md`, is *"the registry's next unused id"*, and round-58 states the operative
   practice explicitly: *"renumbered by document, not arithmetically — the registry's next
   unused id after S422"*. The next unused id after the highest used id (S462) is **S463**.
   The large unused ranges above are historical: the merge package occupies S287–S415, and
   the merge package's ids were never assimilated into this lane's registry (see §4.3).
3. `S463` is **not** claimed by the pending merge package: `/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md`
   stages S287–S415 only, and the highest staged id is S415.

Note the gap structure is *not* an argument for reusing a lower id: the rule is "the next
unused", and the lane has never reused or back-filled the 140–248 band. `S463` is the answer.

### 4.2 Is a third RFC 9111 row a within-scope duplicate (E04) or a cross-scope W04 warning?

**Answer: a cross-scope W04 warning — not an E04 — provided the new row's `scope` cell
differs in text from S461's and S462's, and it is not an error either way (W04 does not affect
a clean lane's exit code).** This is measured, not reasoned.

The rule text relied on, from `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`
(maintained parser; the frozen manual examples in `CORPUS.md` do not spell out E04/W04):

```
E04 duplicate URL+scope (no supersedes)          # sources-census.sh:25
W04 same URL across scopes (warnings do not affect clean lanes)   # sources-census.sh:33

scope_key=u SUBSEP scope
if (u!="" && (u in url_seen) && !(scope_key in url_scopes))
  printf "%s\tW04\t%s duplicate url %s across scopes\n",lane,id,u
if (u!="" && (scope_key in url_scopes) && status!="rejected" &&
    url_scope_nonrejected[scope_key] &&
    teaches !~ /supersedes S[0-9]{3}/)
  printf "%s\tE04\t%s duplicate url %s within scope %s\n",lane,id,u,scope
```

Two consequences that matter for this round:

- The duplicate key is **(normalised URL, scope cell text)** — `u` is the URL after
  `url_of()` normalisation (scheme stripped, host lower-cased, trailing `/` and `#fragment`
  stripped). So `https://httpwg.org/specs/rfc9111.html` and
  `https://httpwg.org/specs/rfc9111.html#age.calculations` are the **same** `u`
  (`httpwg.org/specs/rfc9111.html`). S457, S461 and S462 therefore already share one `u`
  with three distinct scope cells, and the census already reports W04 for S461 and S462.
- **E04 requires an identical `scope` cell.** The scope cell is free text. If the new
  §4.1 row's `scope` cell is not textually identical to S457's, S461's or S462's, it lands
  in a new `scope_key` → **W04**, not E04. If it *were* textually identical, it would be
  E04 — and E04 is suppressed only if the row's `teaches` cell opens `supersedes S###`
  (the row would then also need to *not* be `rejected`).

**Measured, both branches** (census run in my scratch dir on a copy of the lane registry;
LANE untouched; `bash scripts/sources-census.sh validate --today 2026-11-04 <dir>`):

| Fixture | New row's `scope` cell | Census output | Classification |
|---|---|---|---|
| A | new text (Vary-match semantics) | `W04 S463 duplicate url httpwg.org/specs/rfc9111.html across scopes` — **no E-code for S463** | **cross-scope W04 warning** |
| B | byte-copy of S462's `scope` cell | `E04 S463 duplicate url httpwg.org/specs/rfc9111.html within scope Conservative current-age arithmetic on supplied timestamps only; not header extraction, storage/reuse or browser behavior` | within-scope E04 **error** |

The baseline confirms the warning is the ordinary, tolerated case: the lane as committed
already carries 24 W04 rows (S033, S088, S092, S098, S099, S102, S110, S111, S115–S117,
S127, S416, S417, S427, S433, S445, S450, S451, S453–S455, S461, S462), and
`bash scripts/sources-census.sh validate --today 2026-11-04 kake-shokunin` exits **0**.

So for L1: open S463 with its own distinct `scope` cell (Vary-match semantics, explicitly
not age-arithmetic and not Cache-Control lifetime) and the row is a **W04 warning**, the
lane stays clean, and the round needs no `supersedes` clause. If L1 reuses S462's scope text
verbatim, it becomes an **E04 error** (lane exits 1). S461's `supersedes S457` teaches-cell
convention is the established precedent for *superseding* an earlier row's claim, but a
§4.1 Vary row supersedes neither S461 nor S462 — it occupies new ground — so a `supersedes`
clause is neither required nor correct here.

### 4.3 Merge-package id collisions (re-derived, for the record)

`/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md` stages S287–S415. Eight of
those ids are already used in the lane registry — **S312, S329, S367, S372, S373, S374,
S390, S409** — which reproduces the contract's "collides on eight registry ids" exactly
(8 collisions, independently re-derived). S463 is outside the staged range, so it is
unaffected. `Assimilation: none` stands.

---

## 5. Defects found

### 5.1 The round's frozen C2 counter was amended after the candidate existed, and the amendment is outcome-determinative (severity: high)

The seat item names the freeze as **v2 = `8063739791e21a8d7966fd968913e552e1433881`**. The
lane HEAD when I read it was **`52e41d2d` — "round-88: freeze amendment v3"**, committed
15:58:05, which **edits the frozen counter and the frozen contract**:

```
$ git diff 8063739791e21a8d7966fd968913e552e1433881 -- .ufo/waves/round-88/c88_vary.py
-    if star:
-        return 'mismatch'
-
     def normalise(side):
...
+    if star:
+        return 'mismatch'          # input validation precedes the wildcard rule
```

and `contract.md` was amended in the same commit (freeze history restated to "v3 … still
before any candidate was scored", control scores restated from `112/200`+`21/200` to
`109/200`+`24/200`). The committed base control `controls/base-c2.txt` was also rewritten in
that commit (its `random_sha256` moved `004a8eb7…` → `52714a5f…`).

The behavioural effect is small but real: exactly **three** of the 200 seeded expected
verdicts changed, and only because the reference now refuses a malformed header map even when
the Vary value contains `*`:

```
r53 : exit=0 verdict=mismatch  ->  exit=1 verdict=None
r150: exit=0 verdict=mismatch  ->  exit=1 verdict=None
r193: exit=0 verdict=mismatch  ->  exit=1 verdict=None
```

**Why this matters for the round's own claim, not for the RFC.** The contract's C2 section
claims the counter's reference "must reproduce all 20 hand-labelled frozen verdicts
(counter selftest), so the generated batch cannot drift from the spec-derived one". That
guarantee holds for the 20 frozen cases; it does **not** cover the seeded 200, whose expected
verdicts are produced by the same reference that was just edited. Measured consequence for the
two candidate implementations now in the wave tree:

| candidate | sha256 | v2 counter (80637397) | v3 counter (52e41d2d, HEAD) |
|---|---|---|---|
| `w1/ExecReader/vary_match.py` | `fdceef47…` | frozen 20/20, random **197/200**, met=false | frozen 20/20, random **197/200**, met=false |
| `w1/L1/vary_match.py` | `2da573d3…` | frozen 20/20, random **197/200**, met=false | frozen 20/20, random **200/200**, met=true |

The `ExecReader` candidate scores 197/200 under *both* counter versions — it checks `star`
before normalising, so it returns `mismatch` where the v3 reference returns `invalid`. The
`L1` candidate scores 197/200 under the assigned v2 freeze and 200/200 under v3. **The C2
verdict for the L1 candidate is therefore a function of which counter version the validator
runs**, and the contract's kill rule ("the case set, the seed, the generator and the
reference are not edited after scoring") is on the line.

There is a legitimate defence of v3 on the merits: the v2 reference returned `mismatch` for
input that its own profile calls invalid, and refusing is the conservative choice for a
reader that "never applies field-specific normalization". The v3 change is one line and
improves the reference. But two process facts are not defensible by the change itself:

- **Timing.** The v3 commit is dated 15:58:05. `w1/L1/vary_match.py` has mtime **15:56:39**
  and `w1/ExecReader/vary_match.py` mtime **15:59:20**; the counter file's mtime is
  15:57:12 and `contract.md`'s is 15:58:05. The L1 candidate therefore **already existed
  on disk ~86 s before** the counter was amended, and the amendment moved exactly the three
  cases on which that candidate disagreed. The contract asserts v3 landed "still before any
  candidate was scored"; the file mtimes show the candidate file predating the amendment.
  (A *scoring* is not the same as a candidate *existing*, and I found no receipt in
  `w1/ExecCases/receipts/` predating 15:58 that scores a candidate — so I cannot claim the
  amendment was made *after* a score was recorded; I can claim the candidate predates it.)
- **The frozen receipt was rewritten.** `controls/base-c2.txt` is a *base control* — the
  round's claim is "Base control receipts were written before any production byte changed".
  Rewriting it inside the amendment commit changes a control that is supposed to be
  immutable evidence.

Recommendation for L1 (not my call to execute): either (i) pin the C2 measurement to
`8063739791e21a8d7966fd968913e552e1433881` as the seat item and the contract's "Freeze = v2"
line state, and score the L1 candidate against **v2**, where it is 197/200 and `met=false`;
or (ii) treat v3 as a genuine contract version bump — which it is not, since it changes
expected verdicts — and re-freeze with a fresh base control, a new `cases_sha256`/
`random_sha256` pair, and the kill rule restated to cover the reference's error precedence.
Under (i) C2 is a miss at the carrier. The honest statement is that C2's outcome is
currently ambiguous rather than met.

### 5.2 The reference oracle accepts a trailing LF inside a field name, producing a false `match` (severity: medium, latent)

`is_token()` uses `re.match(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$", text)`. Python's `$` matches
at end of string **or just before a trailing newline**, so a member with a trailing LF passes
the token test. The member then becomes a *different* key from the field it names, so it is
"absent from both requests" and the reader returns `match`:

```
reference('accept-encoding\n', {'accept-encoding':'gzip'}, {'accept-encoding':'br'})
  -> 'match'          # should be 'mismatch': the nominated field differs
```

This is the **false-match direction** — the one the profile is supposed to close. It is
**latent in the round's populations**: no frozen case and no seeded case contains an LF
anywhere (verified: `'\n' in str(vary)` and over every key/value of both maps — 0 hits in
both sets), so it does not currently change any score. It is also present in the L1
candidate, which uses the same regex shape (`TOKEN.match(m)`, `TOKEN.match(key)`).

Why it is wrong on the source's own terms: RFC 9110 §5.6.2 p.2 defines
`token = 1*tchar` (Q20) and `tchar` excludes CR/LF; §5.5 p.5 (not quoted above) makes
field values containing CR or LF invalid. So `"accept-encoding\n"` is not a `field-name`
(Q17, Q10) and must not be treated as one. A one-character fix (`\Z` instead of `$`, or
`fullmatch`) closes it. **Not exercised by the current case set — report as a defect in the
round's own counter and candidate, and as a hardening item, not as a scoring defect.**

### 5.3 The profile's refusal rules are stricter than RFC 9110 requires, and 9/200 seeded verdicts rest on rules no frozen case states (severity: medium, disclosure)

The reference refuses (exit 1, `invalid_input:`) a Vary value whose member list has an empty
member, and an empty Vary value. RFC 9110 §5.6.1.2 (Q21, Q22) says a recipient **MUST parse
and ignore a reasonable number of empty list elements**, and the recipient-side list
production `#element => [ element ] *( OWS "," OWS [ element ] )` admits empty elements
explicitly. So `"accept-encoding,"` is a list with one member plus an ignorable empty
element, and `""` is an empty list — the RFC's recipient rules do not require refusing
either.

This is a **local adapter choice** and the contract does say the reader refuses input
("for refused input — on exit 1, empty stdout and an `invalid_input:` stderr prefix"), so
refusing is within the declared contract. But the *shape* of the refusal rule is undeclared
in the contract's Profile paragraph, and only 4 of the 20 frozen cases carry a refusal at
all (ids 14, 15, 19, 20 — empty Vary, non-token member, non-string field value, non-string
Vary). Measured on the seeded 200:

| refusal cause | count in 200 | represented in the 20 frozen cases? |
|---|---|---|
| trailing-comma / empty list member in Vary | 7 | **no** |
| Vary value empty | 4 | yes (case 14) |
| non-string field value | 5 | yes (case 19) |
| Vary value not a string | 4 | yes (case 20) |
| Vary member not a token (contains SP) | 2 | yes (case 15) |
| field value is an empty array `[]` | 2 | **no** |

**9 of 200 expected verdicts (4.5 %) are decided by refusal rules that no frozen case
states**, and the seeded generator's own comment ("the generated batch cannot drift from the
spec-derived one") overstates what the 20-case agreement check buys: the agreement check
pins the *match/mismatch* rules, not the *refusal* rules. A candidate that refuses a
trailing-comma Vary but accepts an empty-array field value, or vice versa, can be right on
every frozen case and still miss 9 seeded cases — and nothing in the frozen set tells it
which way to go. The knowledge entry and the Gate must state the adapter's refusal set
explicitly, or the seeded population must be reduced to rules the frozen cases state.

### 5.4 The counter's "empty array" and "case-variant duplicate" refusals contradict RFC 9110 §5.1/§5.2 in a way the RFC does not support (severity: medium, declaration only)

Two more adapter refusals, both exercised by the seeded population and both unreachable
from the frozen set:

- **Case-variant duplicate names.** `normalise()` refuses a header map containing both
  `Accept-Encoding` and `accept-encoding` as "ambiguous duplicate name". But RFC 9110 §5.1
  p.3 (Q18) says field names are case-insensitive, and §5.2 p.2 (Q14) says a repeated field
  name's combined value is the list of its field-line values concatenated in order. So
  `{"Accept-Encoding": "gzip", "accept-encoding": "br"}` is one field named
  `accept-encoding` with the combined value `gzip, br` — it is **not** ambiguous and
  **not** invalid. Refusing it is a local adapter policy, and the contract does not declare
  it. (Note the frozen case 13, `Vary: Accept-Encoding, accept-encoding`, is a *different*
  question — duplicate Vary *members*, not duplicate request fields — and is labelled
  "redundant", which is fine: §12.5.5 p.3 (Q11) makes the member list a set of field names.)
- **Empty array field value.** `{"accept-encoding": []}` is refused. An empty array is
  ambiguous between "the field was absent" and "the field was present with an empty value";
  RFC 9110 §5.2 p.2 says a field present once has "the corresponding field line value",
  which for a zero-length list is the empty string. Refusing is a defensible local choice
  but again is undeclared in the contract's Profile paragraph.

Neither is exercised by the frozen 20 (verified: 0 frozen cases have a case-variant
duplicate key, 0 have an empty-array value), so again the seeded population scores rules the
frozen set does not state.

### 5.5 The `*` rule and RFC 9110 §12.5.5 p.4 disagree about who may produce `*` (severity: low, wording)

Q12 (§12.5.5 p.4) is *"A proxy MUST NOT generate \"*\" in a Vary field value."* — a
constraint on **generators**, whereas RFC 9111 §4.1 p.5 (Q8) is *"always fails to match"* —
a constraint on **recipients**. The frozen cases 7 and 8 (Vary `*`, and `accept-encoding, *`)
model the recipient side correctly. But a knowledge entry must not quote Q12 as if it
required a reader to refuse a `*`-bearing Vary: the RFC requires the *reader* to fail the
match (Q8), and separately forbids a *proxy* from *producing* one. The round's profile
("any `*` member always fails") is the recipient-side rule and is right; the citation for it
is §4.1 p.5, not §12.5.5 p.4.

### 5.6 Two contract statements about the C2 counter are now stale (severity: low, bookkeeping)

- `contract.md` line "Before: base `f4479c14` → tool absent, `frozen=0/20 random=0/200
  met=false`, exit 1 (`controls/base-c2.txt`)" — the base control now carries the **v3**
  `random_sha256` `52714a5f…`, not the v2 `004a8eb7…` that the v2 freeze committed. The
  statement is still true of the *claim* (tool absent at base → 0/20, 0/200, met=false,
  exit 1) but the receipt it points at is no longer the one the freeze published.
- The contract's "Controls committed: … constant-`mismatch` stub `9/20 + 112/200`,
  always-`invalid` stub `4/20 + 21/200`" was updated in v3 to `109/200` and `24/200`. The
  v2 numbers are the ones the freeze published; the v3 numbers match HEAD. Both sets are
  internally consistent with their own counter version — the point is that the pair has
  changed, so a reader holding only the v2 freeze will compute different stub scores.

### 5.7 No defect found in: the case set's frozen labels, the seed, or the generator's determinism (severity: none — recorded as checked)

- **Frozen 20 ↔ reference agreement:** the counter's own selftest asserts it and it holds —
  `PASS reference oracle reproduces all 20 frozen verdicts` (17/17 selftest, exit 0, run
  against HEAD's counter). I re-derived the histogram independently: match 7, mismatch 9,
  exit-1 4, ids 1–20 sequential and unique.
- **Seed/generator determinism:** three independent imports of the counter produce the same
  `random_sha256` `52714a5f4ae9b66ee444f39284b6e5ce575c6ae5760965fb8736e6983444b981` and
  the same verdict histogram. No `PYTHONHASHSEED` dependence.
- **Constant-stub control scores** re-derived against HEAD's counter: match 7/20 + 67/200,
  mismatch 9/20 + 109/200, invalid 4/20 + 24/200, silent-failure 0/20 — matching the v3
  contract text and `controls/c2-selftest.txt` (17/17, exit 0).

---

## 6. Commands run (all read-only against LANE; all writes confined to my scratch and my
wave directory)

```
# sources (single GET each; headers + body retained)
curl -sS -D headers-9111.txt -o rfc9111.html -w 'HTTP=%{http_code} BYTES=%{size_download} URL=%{url_effective}\n' \
     https://httpwg.org/specs/rfc9111.html            # HTTP=200 BYTES=178573 ; sha256 999f4013…
curl -sS -D headers-9110.txt -o rfc9110.html -w 'HTTP=%{http_code} BYTES=%{size_download} URL=%{url_effective}\n' \
     https://httpwg.org/specs/rfc9110.html            # HTTP=200 BYTES=915065 ; sha256 5313be9c…

# quote extraction + byte-exactness assertion (script in scratch, output quotes.json)
python3 <extract paragraphs, assert `q in src`, assert len(q.split())<=25>   # 23/23 verified

# registry state
grep -nE '^\|[[:space:]]*S(45[5-9]|46[0-9])[[:space:]]*\|' LANE/corpus/SOURCES.md
python3 <ids, gaps, max>                                                 # 200 rows, max S462, 262 gaps
grep -oE '\bS4[6-9][0-9]\b' LANE/corpus/SOURCES.md | sort -u             # S460 S461 S462 only

# census, both branches, on scratch copies of the registry
bash scripts/sources-census.sh validate --today 2026-11-04 kake-shokunin   # EXIT=0, 24 W04, no E
bash scripts/sources-census.sh validate --today 2026-11-04 <scratch A>    # W04 S463, no E04 for S463
bash scripts/sources-census.sh validate --today 2026-11-04 <scratch B>    # E04 S463 (identical scope)

# counter behaviour, v2 (80637397) vs v3 (52e41d2d)
git show 80637397:…/c88_vary.py  > scratch/v2/c88_vary.py
python3 <import both, diff RANDOM_CASES verdicts>                          # 3 cases differ: r53 r150 r193
python3 LANE/…/c88_vary.py --tool <candidate> --work <scratch>            # 200/200 (v3) vs 197/200 (v2)

# counter selftest (HEAD)
TMPDIR=<scratch>/tmp python3 LANE/…/c88_vary.py --selftest                # 17/17 PASS, exit 0
```

Exit codes and outcomes are as quoted inline above. Nothing outside
`LANE/.ufo/waves/round-88/w1/ScoutSpec/` and
`/fast/scratch/hyaku/kake-r88/ScoutSpec/` was written; no git or jj mutation, no commit,
no push, no production edit, no sibling-lane or fleet-repo write, no `/tmp` tree, no
subagent dispatch.

**Scratch:** `/fast/scratch/hyaku/kake-r88/ScoutSpec/` — one clone-equivalent (a copy of the
counter at the v2 freeze plus the registry copies used by the census fixtures), no inherited
`TMPDIR` (`TMPDIR` was set explicitly for the selftest run), all files < 50 MB. Deleted
before this report was finalised; the retained raw HTML and headers were copied into my wave
directory first, and the receipts cited above are the wave-directory copies.

**Tooling:** no package was installed or upgraded for this seat. `curl`, `python3` (3.x,
stdlib only), `git` (read-only: `show`, `log`, `cat-file`, `diff`, `status`, `rev-parse`,
`reflog`) and `gawk`/`bash` (via the maintained `scripts/sources-census.sh`) were already
present and were used as-is. PACMAN was not invoked; the host's `pacman` pause was respected.

---

## 7. Summary for L1

1. **New SOURCES row id = `S463`** — free in the registry, not claimed by the merge package
   (which stages S287–S415 and collides on eight ids: S312, S329, S367, S372, S373, S374,
   S390, S409).
2. **A third RFC 9111 row is a cross-scope W04 warning, not an E04 error** — provided its
   `scope` cell text differs from S457's/S461's/S462's. Measured both branches. W04 does not
   affect the lane's exit code (lane baseline: exit 0 with 24 W04s). **No `supersedes`
   clause is warranted**: a §4.1 Vary row supersedes neither S461 nor S462.
3. **All 23 quotes are byte-exact and ≤ 25 words**, with section/paragraph locators, from
   fresh GETs recorded in §1. The four required targets are Q1, Q3+Q4+Q5, Q7, Q8.
4. **The knowledge entry must state what is not claimed** — no cache-key construction,
   storage, revalidation, freshness or browser behaviour (§3), and must distinguish the
   RFC's permissive "match" rule (Q3–Q5, incl. the field-specific `GZip`/`gzip` case at
   Q23) from the round's deliberately conservative profile.
5. **C2's verdict is currently ambiguous, not met.** The frozen counter was amended
   (`80637397` → `52e41d2d`) *after* the L1 candidate existed on disk; the amendment moved
   exactly the three seeded verdicts on which that candidate disagreed, and it rewrote the
   base control receipt. Against the assigned v2 freeze the L1 candidate scores 197/200 and
   `met=false`; against HEAD's v3 it scores 200/200 and `met=true`. L1 must either pin C2 to
   v2 (C2 is then a miss) or re-freeze v3 properly with fresh base controls.
6. **Two latent defects in the counter and in the L1 candidate**, both unreachable from the
   current case set: the trailing-LF false-`match` in `is_token` (§5.2), and the undeclared
   refusal rules that decide 9/200 seeded verdicts no frozen case states (§5.3, §5.4).
