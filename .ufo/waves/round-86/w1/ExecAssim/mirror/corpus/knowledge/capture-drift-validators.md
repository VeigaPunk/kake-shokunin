source: S455 — RFC 9110 §8.8.1 Weak versus Strong and §8.8.3 ETag — https://www.rfc-editor.org/rfc/rfc9110.txt — §8.8.1 lines 3393-3478, §8.8.3 lines 3570-3617 and §8.8.3.2 lines 3643-3669 of `.ufo/waves/round-81/w1/ScoutSources/rfc9110.txt` (502,941 B, sha256 21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a, fetched 2026-11-04T10:44:53Z, HTTP 200; this entry's author re-hashed the retained copy on 2026-11-04 and opened no socket)
verified-at: 2026-11-04 — every quote below located by line in the retained bytes; `scripts/capture_delta.py` (sha256 4b0dc25233542696988ef91b62872068cbc5d56f58d0ef3f988ac60e558d9680) read in full and its selftest run once (`selftest: 14/14 passed`, exit 0); capture B and its delta record were absent at authoring time
recheck: 365d (an RFC changes only by a new publication)
ground: freshness — C2's capture-to-capture drift gate, `.ufo/waves/round-82/contract.md` §C2
scope: what RFC 9110 §8.8.1 and §8.8.3 make a strong validator establish about representation bytes, what a weak one does not, and how the lane's `scripts/capture_delta.py` compares two dated GET-only captures of the same three surfaces. Not ETag generation by any server, not cache policy, not conditional requests, not any property's correctness, not provenance of a capture

# Capture-to-capture drift: what a validator settles, and what the delta decides

The lane keeps a change-detection instrument, not a conformance instrument. It compares two
captures of the same surfaces taken at two dated instants and prints one stable line per surface.
Everything it can say is bounded by two things: what RFC 9110 makes a validator mean, and what the
instrument actually compares. This entry states both, then the two captures and the limits.

## 1. What the source fixes

RFC 9110 §8.8.1 defines validator strength by the relation between the validator and the
representation-data bytes; §8.8.3 fixes the entity tag's opacity and its weak marking; §8.8.3.2
names two comparison functions over entity tags. Quoted spans are exact; a trailing `…` marks a
clause whose sentence continues beyond the span, and the word count is for the quoted span only.

| Fact | Retained `file:line` | Exact quote | Words |
|---|---|---|---|
| A strong validator tracks representation-data changes | `rfc9110.txt:3403-3405` | A "strong validator" is representation metadata that changes value whenever a change occurs to the representation data that would be observable in the content of a 200 (OK) response to GET. | 31 |
| A strong validator may also change without a data change | `rfc9110.txt:3407-3409` | A strong validator might change for reasons other than a change to the representation data, such as when a semantically significant part of the representation metadata is changed (e.g., Content-Type)… | 30 |
| Uniqueness is per resource, not across resources | `rfc9110.txt:3417-3422` | A strong validator is unique across all versions of all representations associated with a particular resource over time. … no implication of uniqueness across representations of different resources | 18 + 9 |
| A hash of the data is a sufficient strong validator | `rfc9110.txt:3428-3429` | A collision-resistant hash function applied to the representation data is also sufficient… | 12 |
| A weak validator may not move when the data moves | `rfc9110.txt:3438-3439` | In contrast, a "weak validator" is representation metadata that might not change for every change to the representation data. | 19 |
| A validator shared by simultaneous representations is weak | `rfc9110.txt:3463-3465` | a validator is weak if it is shared by two or more representations of a given resource at the same time, unless those representations have identical representation data. | 28 |
| An entity tag is opaque, not a content literal | `rfc9110.txt:3574-3576` | An entity tag is an opaque validator for differentiating between multiple representations of the same resource… | 16 |
| Strong is the default; a failing tag is marked weak | `rfc9110.txt:3607-3612` | An entity tag can be either a weak or strong validator, with strong being the default. … then the origin server MUST mark the entity tag as weak by prefixing its opaque value with "W/" (case-sensitive). | 16 + 19 |
| Strong comparison over tags | `rfc9110.txt:3648-3649` | two entity tags are equivalent if both are not weak and their opaque-tags match character-by-character. | 15 |
| Weak comparison over tags | `rfc9110.txt:3651-3653` | two entity tags are equivalent if their opaque-tags match character-by-character, regardless of either or both being tagged as "weak". | 19 |

The retained plain text folds the compound `opaque-tags` across lines 3651-3652 (`opaque-` then
`tags`); the weak-comparison quote renders it joined. Every other quoted span above occurs verbatim
in the retained bytes after whitespace collapse, checked by replaying the spans against the file.

Three readings of the table matter for a byte delta:

1. **Strong is a change-detection guarantee, not an identity proof.** The guarantee runs from bytes
   to validator: a change in the representation data observable in a 200 GET body is accompanied by a
   change in the validator. It does not run the other way as a proof that equal bytes produced the
   validator — the tag is opaque, and the RFC only requires uniqueness across versions of *one*
   resource (:3417-3422).
2. **A strong validator may move with no byte change** (:3407-3409). So a validator flip is never,
   by itself, evidence that the representation bytes changed.
3. **A weak validator cannot exclude a byte change.** It "might not change for every change to the
   representation data" (:3438-3439), and a tag shared by simultaneous representations — a gzip and
   an identity coding, for example — is weak unless the data is identical (:3463-3468). A match under
   weak comparison therefore leaves the byte question open; only exact data comparison closes it.

This is why the lane's drift gate computes a digest of the bytes instead of reading `ETag`. The
mechanism it uses is the one :3428-3429 names as sufficient: a collision-resistant hash of the
representation data, computed by the gate from the retained body, not taken from the response.

## 2. What the lane's delta compares

`scripts/capture_delta.py` reads two capture trees, each a `manifest.json` plus one directory per
surface holding `response.json` and (when the body is retained) `body.bin`. Before comparing
anything it verifies every receipt: `method` exactly `GET`; `status` an integer in 100..599
(booleans rejected); `truncated` exactly `false`; `fetchedAt` an RFC 3339 instant; `bytes` a
non-negative integer equal to the retained body length; `sha256` 64 lowercase hex digits equal to
the digest of the retained body. A surface whose `bytes` is 0 may omit `body.bin`; any nonzero claim
without a body is a fault.

Surfaces are paired by manifest `id`, over the union of both trees. A per-surface line prints:

    surface=<id> url=<url> status=<a>-><b> body=<same|changed> bytes=<a>-><b> headers=<n> added=<n> removed=<n> changed=<n> verdict=<identical|changed>

and the record ends with `surfaces=<n> identical=<k> changed=<k> added=<k> removed=<k>`. A surface
present in only one tree prints `verdict=added` or `verdict=removed` with its status and byte count;
for a changed surface the gate adds one `  field=<name> change=<added|removed|changed>` line per
differing header field name.

`identical` requires all four of: equal status, equal body sha256, equal body length, and an equal
header mapping. The mapping is built by lower-casing each field name and appending its value in wire
order, so field-name case is normalized away while value bytes are compared verbatim and a change in
the order of repeated values is detected.

**The verdict is not a body verdict.** Because `identical` also requires the whole header mapping to
match, any field that differs between two responses — a per-response `Date`, a request identifier, an
`ETag` — makes the surface `changed` while its line still reads `body=same`. The body question is
answered by the `body=` token, not by the verdict; a reader who takes `verdict=changed` as "content
changed" is wrong on exactly the case the RFC warns about (:3407-3409). `[INFERENCE]` for the named
example fields; the code relation is observed.

A further consequence of the mapping rule: the gate never reads `ETag` as a validator. If an `ETag`
differs it shows up as one more `field=etag change=changed` entry with `body=same`, which is the
record saying a header moved, not that the representation bytes did.

## 3. The two captures

| Capture | Tree | Receipt instants (`fetchedAt`) | Record |
|---|---|---|---|
| A | `.ufo/waves/round-81/capture/` | three receipts, all `2026-11-04T12:05:06Z` | `.ufo/waves/round-81/capture/manifest.json` |
| B | `.ufo/waves/round-82/capture/` | **pending** — the tree did not exist at authoring time | `.ufo/waves/round-82/controls/after-c2-delta.txt` — **pending** |

Capture A's three receipts, read from their `response.json` files: `ds4cc-primary`
`https://ds4cc.com/` status 200, 78,897 bytes, sha256 `f2c5d2b3…342e93`; `ds4cc-robots`
`https://ds4cc.com/robots.txt` status 200, 62 bytes, sha256 `70f9ea28…d0264c05`; `ds4cc-sitemap`
`https://ds4cc.com/sitemap.xml` status 200, 7,810 bytes, sha256 `55cb947f…7006ef`. All three
`truncated` false and `method` GET.

Capture B had not been taken when this entry was written, so **this entry states no delta finding**.
The contract's C2 floor for B's instants is `2026-11-04T12:42:00Z`, and its ordering rule is that
every B instant must be strictly after its A instant; both are the round counter's conjuncts, not
the tool's (see the limits). When B lands, the record is re-derived by one command and the committed
file is the tool's stdout:

    python3 -B scripts/capture_delta.py --a .ufo/waves/round-81/capture --b .ufo/waves/round-82/capture

The result of that run is data, not a policy outcome: `identical` says the three compared facets
matched between two instants, `changed` says at least one did not, and neither says a surface is
correct, reachable by a crawler, or current beyond the second instant it was read.

## 4. Procedure and exit codes

| Invocation | Exit | Meaning |
|---|---|---|
| `python3 -B scripts/capture_delta.py --a DIR --b DIR` | 0 | every receipt in both trees verified and a complete record printed |
| same | 1 | a receipt or manifest fault; prints `fault <surface> <reason>` |
| same | 2 | a tree is missing or unreadable; prints `fault (tree) unreadable (<Exception>: …)` |
| same | 64 | usage error (a `--a` or `--b` missing, or an unrecognized option) |
| `python3 -B scripts/capture_delta.py --selftest` | 0 | `selftest: 14/14 passed` (observed; the contract asks for >= 12) |

The selftest fixtures cover a green identical pair, a changed body, a changed status, header
added / value-changed / removed, a tampered body, a byte-count mismatch, a truncated receipt, a
non-GET method, an added surface, a removed surface, a missing tree and a missing surface directory.
Fixtures are built under a temporary directory; the run opens no socket.

## 5. Limits

- **Offline by construction.** The module imports `argparse, datetime, hashlib, json, os, re,
  shutil, sys, tempfile` and contains no socket, `urllib`, `http.client` or `requests` reference. It
  cannot observe a surface; it can only compare trees that some capture step already wrote.
- **Two instants only.** A record describes A versus B. It does not show when a change happened
  between them, whether the surface changed again after B, or that a future change would be caught.
- **Provenance is not checked.** A fabricated capture tree carrying correct internal digests passes:
  the gate verifies receipt-to-body consistency, never that the bytes came from a socket. The capture
  transcript is the provenance evidence; the delta record is not.
- **The tool does not order the instants or enforce the floor.** It parses `fetchedAt` as RFC 3339
  but compares no instants; `order_ok` and `floor_ok` are separate conjuncts of the round counter
  (`c82_capture_delta.py`). Do not read a green delta record as proof that B was fetched after A.
- **Surfaces are paired by manifest id, not by URL.** The receipt's `url` and `finalUrl` are not
  cross-checked against the manifest `url`, so a redirect that changes `finalUrl` alone is invisible
  unless a header or the body differs.
- **A zero-byte surface need not retain a body.** When `bytes` is 0 the receipt digest is accepted
  without re-derivation; only a nonzero claim without `body.bin` faults.
- **String equality is not semantic equality.** The header comparison is exact string equality on
  lower-cased names and verbatim values; a semantically equivalent re-serialization (spacing, value
  order within a list) reads as `changed`, and a header the capture step did not record cannot be
  compared at all.
- **A digest match is not a content claim.** Equal sha256 across the two captures is evidence about
  two retained byte strings, modulo the collision resistance of SHA-256. It is not a statement about
  the served representation beyond those bytes, and it is not a freshness guarantee for any later
  instant.

## Lane readings — marked, not sourced

- **`body=same` is the content token; `verdict` is a composite.** The code's `identical` predicate
  conjoins status, body and the full header map, so a header-only difference yields `changed` with
  `body=same`. This is a reading of the printed contract, not a sentence of the RFC. `[INFERENCE]`
- **Choosing sha256 over `ETag` is a lane policy grounded in :3428-3429.** The RFC says a
  collision-resistant hash of the representation data is a sufficient strong validator; it does not
  require this gate to compute one, and it does not make the server's `ETag` usable as a byte
  identity. `[INFERENCE]`
- **The weak-validator reading is used only negatively here.** The entry claims that a weak validator
  cannot exclude a byte change (:3438-3439, :3463-3468); it makes no claim about when a weak check
  would be adequate, which is a conditional-request question outside this entry. `[INFERENCE]`
- **S010 already carries the earlier lesson on this document.** S010 cites the HTML serialization
  (`rfc9110.html#section-8.8`) for ETag opacity and for a strong validator changing on a metadata
  change; this entry does not re-teach that as new. Its added ground is the strong/weak definition,
  the hash-as-validator sentence (:3428-3429) and the two tag-comparison functions, read against a
  byte delta that never consumes a server `ETag`. `[INFERENCE]`

## 6. Recorded delta — appended 2026-11-04 after capture B (L1 integration)

The "pending" cells of §3 are superseded here by append; §3's sentences are not rewritten. Capture
B was taken GET-only with the lane's frozen population and the same three declared surfaces, one
request each:

| Capture | Tree | Receipt instants (`fetchedAt`) | Status / bytes / sha256 |
|---|---|---|---|
| B | `.ufo/waves/round-82/capture/` | `2026-11-04T13:00:27Z` (primary), `2026-11-04T13:00:28Z` (robots, sitemap) | 200 / 78,897 / `f2c5d2b3…342e93`; 200 / 62 / `70f9ea28…d0264c05`; 200 / 7,810 / `55cb947f…7006ef` |

All three B digests and byte counts equal A's, and B's instants are 55 minutes after A's and after
the round's `2026-11-04T12:42:00Z` floor. The committed record is
`.ufo/waves/round-82/controls/after-c2-delta.txt`, the tool's stdout with no command line; two runs
were byte-identical (`sha256 d43c0231…bd644a` each). Its summary line:

    surfaces=3 identical=0 changed=3 added=0 removed=0

and its three surface lines all read `body=same` with `status=200->200` and `added=0 removed=0`,
while the header mapping moved:

- `ds4cc-primary` — `changed=4`: `date`, `x-fastly-request-id`, `x-served-by`, `x-timer`.
- `ds4cc-robots` and `ds4cc-sitemap` — `changed=5`: the same four plus `x-cache`.

The reading is exactly the case §1 fact 2 names: a whole-header-map change with no representation
byte change. The content answer is the `body=` token (same on all three at these two instants); the
`verdict=changed` is the composite the tool prints when any facet differs, and it is not a claim that
the served content changed. The four/five differing fields are per-response delivery metadata
(`date`, Fastly request/routing identifiers, a timer, a cache-status string) whose variability
between two responses is expected and is reported as data, not as drift in the property's content.
`[INFERENCE]` for the "delivery metadata" characterisation; the field names and counts are the
record's own bytes.

What this finding does **not** support: that `ds4cc.com`, its `robots.txt` or its `sitemap.xml` is
correct, current beyond `2026-11-04T13:00:28Z`, or reachable by any crawler. It also does not support
"the site has not changed since round 81" as a content claim about anything not captured here.

## 7. Erratum — what `body=same` across these two captures does not mean (appended 2026-11-04)

Section 6's reading that the two captures are separated by 55 minutes is true of the *fetch* instants
and must not be read as two independent origin reads. The edge cached both: `x-github-request-id`'s
trailing hex is the cache-fill epoch and `expires` is that epoch plus `max-age` (600 s), and both are
identical across A→B — primary `…6AEB18EA` = `2026-11-04T11:37:14Z`, robots/sitemap `…6AEB1F72` =
`2026-11-04T12:05:06Z`, with `expires − fill = 600` on all six rows. Capture B therefore observed the
same stored objects as capture A (robots and sitemap as a HIT on the entry A's MISS created; primary
on an entry filled 28 minutes before A), and `Age: 0` with `expires` already past indicates
revalidation, not a re-fill. So `body=same` means "the edge served identical bytes at two recorded
instants"; it does not mean the property re-read its origin. This is RFC 9111 cache-selection ground
(S594 in mori, §4.1 `Vary`; S237 in kumitate, §4.2.3 `Age`) applied to this delta, reported as
adjacency rather than re-taught. Evidence: `.ufo/waves/round-82/w1/ConnectorC/cachefill.py` (exit 0)
and `…/ConnectorC/cachefill.txt`; `corpus/lessons/round-82.md` §Appended erratum. A future instrument
could compare `x-github-request-id` per surface across the two trees, since equality there is a
stronger statement than the `userAgent` comparison §6's follow-on names.
