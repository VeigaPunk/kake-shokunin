source: S456 — RFC 9111: HTTP Caching — https://www.rfc-editor.org/rfc/rfc9111.txt — quoted spans at §3.1 lines 340-342 (heading 338), §3.2 lines 375-377 and 387 (heading 369), §4 lines 468-469 (heading 466), §4.2 lines 583-599 (heading 581), §4.2.3 lines 721-724 and 736-738 (heading 719), §4.3.1 lines 827-829, 831-834 and 838-844 (heading 812), §4.3.4 lines 986-988 (heading 951) of `.ufo/waves/round-83/w1/ScoutSources/rfc9111.txt` (84,477 B, sha256 aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e, HTTP 200, response Date 2026-11-04T13:29:41Z; fetched once by the round-83 ScoutSources seat; this entry's author re-hashed the retained copy and opened no socket)
verified-at: 2026-11-04, base revision 826b0061f233ce1dffb9bd6874abc1342a864247 — every span in §2 re-opened in the retained bytes and checked as a literal substring of the single physical line named (18/18; 17 occur once in the file, the 18th `response, as per Section 3.2.` occurs twice and is pinned by its line number 988); `scripts/header_change_class.py` read in full; the C2 selftest receipt `.ufo/waves/round-83/controls/c83-selftest-c2.txt` reads `selftest: 9/9 passed` with `selftest_c2_exit=0`
recheck: 365d (an RFC changes only by a new publication). Re-open: `T=$(mktemp -d) && curl -sSL --max-time 90 -o "$T/rfc9111.txt" https://www.rfc-editor.org/rfc/rfc9111.txt && sha256sum "$T/rfc9111.txt"` — expect the digest above; then `python3 -B scripts/header_change_class.py --a .ufo/waves/round-81/capture --b .ufo/waves/round-82/capture --declared .ufo/waves/round-81/capture-expectations.json` and `python3 -B .ufo/waves/round-83/c83_drift_class.py --root . --revision <rev>`
ground: freshness — C2's capture-to-capture drift gate, `.ufo/waves/round-83/contract.md` §C2
scope: What RFC 9111 makes a stored response contain (unrecognised fields included), what Age measures, and what makes a field a validator, so that a moved response header between two dated captures is read against the object rather than waved through. Not a definition of the lane's class names or of which header belongs in which class (that table is lane policy, frozen in the contract); not any server's cache policy; not ETag generation, opacity or comparison strength (RFC 9110 §8.8, S455); not a claim that any capture observed origin bytes

# Header change classes — what a moved response header can prove

## 1. Why a header diff needs classes at all

RFC 9111 makes reuse conditional: a cache must not reuse a stored response unless it is fresh, is
allowed to be served stale, or has been validated (`468`). A fresh response in turn may be used to
satisfy subsequent requests without contacting the origin server (lines 597-599). That is the mechanism
behind the drift gate's central observation: two captures taken minutes apart can return identical
bodies while their header maps differ, because the second capture is evidence about the same stored
object, not about a second origin read.

Under that reading, a bare header difference is neither harmless nor decisive on its own. A stored response
is not a body plus an arbitrary set of transport notes: the header fields are part of what the cache
holds, and a newer response's fields are merged into it (`375-377`) with narrow exceptions. So a
comparison of two captures has to say, per moved field, what kind of fact the move is.

## 2. What the source fixes

Each span below is a literal substring of the single physical line named in the retained file; where
the RFC's hard wrap cuts a sentence, the line range in the first column gives the rest. All quotes
are reproduced exactly, including the RFC's `--` and its doubled spaces.

| Fact | `rfc9111.txt` lines | Raw span (one physical line) |
|---|---|---|
| Reuse gate | 468-469 | `When presented with a request, a cache MUST NOT reuse a stored` |
| Freshness is age versus lifetime | 583-585 | `A "fresh" response is one whose age has not yet exceeded its` |
| A fresh response may skip the origin | 597-599 | `When a response is fresh, it can be used to satisfy subsequent` |
| Age is elapsed time | 594-595 | `A response's "age" is the time that has passed since it was generated` |
| Age is the cache's own estimate | 721-724 | `the cache's estimate of the number of seconds since the origin server` |
| Storage includes unrecognised fields | 340-342 | `Caches MUST include all received response header fields` |
| …continued | 341 | `unrecognized ones -- when storing a response` |
| …and the stated purpose | 342 | `HTTP header fields can be successfully deployed` |
| A newer response's fields are merged | 375-377 | `When doing so, the cache MUST add each header field in the provided` |
| …into the stored response | 376 | `response to the stored response, replacing field values that are` |
| …with exceptions | 377 | `already present, with the following exceptions:` |
| Content-Length is one exception | 387 | `The Content-Length header field.` |
| Validators decide equivalence | 827-829 | `The precondition header fields are then compared by recipients to` |
| …to a current representation | 829 | `representation of the resource.` |
| Last-Modified is one validator | 831-834 | `One such validator is the timestamp given in a Last-Modified header` |
| ETag is the other | 838-844 | `Another validator is the entity tag given in an ETag field` |
| A 304 freshens the stored response | 986-988 | `For each stored response identified, the cache MUST update its header` |
| …from the 304's fields | 988 | `response, as per Section 3.2.` |

The sentence that carries the unknown-field rule, as the RFC prints it (exact bytes of lines
340-342, hard wraps included):

```
   Caches MUST include all received response header fields -- including
   unrecognized ones -- when storing a response; this assures that new
   HTTP header fields can be successfully deployed.
```

## 3. The three verdict-deciding classes

The classifier's per-surface verdict is `representation-changed` when the status differs, when the
body sha256 differs, or when any changed header falls in `validator`, `representation` or `unknown`;
otherwise it is `same-object`. Those three classes are the ones that decide, and each corresponds to
a different kind of source fact.

**`per-request`.** Fields whose value is a function of the exchange, not of the object: `date`,
`age`, `cf-ray`, `x-cache`, `x-served-by`, `x-timer`, `x-fastly-request-id`, `x-request-id` and the
rest of the frozen list. RFC 9111 supplies the two time-valued members of this class directly.
`Age` is not a property of the stored bytes; it is the cache's estimate of the number of seconds
since the origin server generated or validated the response (lines 721-724), computed from the clock
(§4.2.3) and, at the origin end, from the `Date` value (line 736). A moved `date` or `age` says the
two requests met different instants — or different caches — not different content. The edge
identifiers are the same kind of fact by construction: their names carry routing and timing, and
nothing in the source makes them payload metadata.

The reading has a floor. A moved `x-cache` does not tell you the origin was re-read; it tells you
which edge answered and whether it served from storage. An `Age` of zero does not distinguish a
response the origin generated from one the cache freshened from a 304 (Not Modified): §4.3.4
requires the cache to update the stored response's header fields from the 304's fields (`986-988`),
and §4.2.3 recomputes age from those clocks. This class is *not evidence of object change*, never
*proof that nothing happened*.

**`validator`.** `etag` and `last-modified`. §4.3.1 defines the validation exchange: the precondition
fields are compared to determine whether any stored response is equivalent to a current
representation of the resource (lines 827-829), and names the timestamp (`831-834`) and the
entity tag (`838-844`) as the validators that carry it. A moved validator withdraws the ground for a
`same-object` verdict. It is not by itself proof that the payload bytes moved — RFC 9110 §8.8.1 allows
a strong validator to change for metadata reasons (S455, adjacent and not re-taught here) — but this
gate decides identity, and a moved identity token is decisive against identity.

**`representation`.** Fields that name the payload or decide which payload answers: `content-length`,
`content-type`, `content-encoding`, `content-language`, `content-location`, `content-md5`, `digest`,
`accept-ranges`, `vary`. For the first group a move is direct evidence that the payload metadata
differs. `vary` is the instructive member: it does not describe bytes, but §4.1 makes it the field
that selects a stored response for a request, so a moved `vary` changes the object-to-request mapping
the capture is evidence about. It stays decisive.

## 4. Two further classes: `policy` and `unknown`

`policy` — `cache-control`, `expires`, `server`, `link`, `alt-svc`, and the security and CORS
families — is recorded in its own counter but does not flip the verdict by itself. A move there
changes how the object may be stored or delivered, not which object it is. That is a statement about
this instrument's evidence, not about the importance of the header.

`unknown` — any changed name absent from the frozen table — is counted and is decisive.

The names are the lane's. RFC 9111 uses `validator` and names exactly two members (Last-Modified and
the entity tag); it does not use `per-request`, `representation` or `policy` as header classes, and it
states no rule for unrecognised fields beyond the storage and merging duties above. `[INFERENCE]` The
class table applies lane policy to those mechanics, and §5's derivation is this entry's reading of the
source rather than a sentence the source states.

## 5. Why an unknown changed header must be treated as representation-bearing

Two source rules and one design argument:

1. **Storage is open-ended.** §3.1 requires caches to include all received response header fields,
   including unrecognized ones, when storing a response, and gives the reason: this assures that
   new HTTP header fields can be successfully deployed (lines 340-342). The stored response is
   therefore not body plus a known list of headers; an unrecognised field is part of the object the
   cache holds.
2. **Update is additive.** §3.2 requires that, when a stored response's header fields are updated
   from a newer response, the cache add each header field in the provided response to the stored
   response, replacing field values that are already present (lines 375-377), with narrow
   exceptions: fields excepted from storage by §3.1, fields the stored response itself depends upon,
   automatically processed fields, and `Content-Length` (`387`). A changed unknown field is thus
   merged into the stored response; it is part of what the cache will present next.
3. **There is no closed list to appeal to.** The frozen table can demote a name only by naming it.
   A name it does not name has no demotion argument available — not because the field is known to be
   representation-bearing, but because nothing establishes the contrary. RFC 9111's own reason for
   storing unrecognised fields is that new fields are expected to carry semantics a cache does not
   yet know.

The asymmetry is deliberate. A false `representation-changed` costs one more capture and one more
comparison; a false `same-object` asserts identity on evidence that does not support it. The frozen
predicate makes `unknown == 0` a necessary condition, so a single unrecognised moved field forces the
stricter verdict. `[INFERENCE]` That is the conservative reading of §3.1: the specification stores
unknown fields precisely so that their semantics are not silently discarded, and a classifier that
dropped them would work against that purpose.

The `Content-Length` exception at `387` does not contradict the table's placement of that field in
`representation`. §3.2's exception governs *updating* a stored response's headers during validation,
because a cache must not rewrite the length of the body it already holds. Classifying two fresh 200
responses is a different operation: different `content-length` values on two 200s mean different
payload sizes, and the table keeps the field decisive.

## 6. Measured record

The committed receipt is `.ufo/waves/round-83/controls/after-c2-classes.txt` (524 B, sha256
`2623e070bb4192e9d65a744c5f89ccd1f0ccf5e9b3a68b43282c4c4e5bfa659a`). Its summary line:

```
summary surfaces=3 diffs=14 per_request=14 validator=0 representation=0 policy=0 unknown=0 verdict=same-object
```

and its three surface lines:

```
surface=ds4cc-primary status_a=200 status_b=200 diffs=4 per_request=4 validator=0 representation=0 policy=0 unknown=0 verdict=same-object
surface=ds4cc-robots status_a=200 status_b=200 diffs=5 per_request=5 validator=0 representation=0 policy=0 unknown=0 verdict=same-object
surface=ds4cc-sitemap status_a=200 status_b=200 diffs=5 per_request=5 validator=0 representation=0 policy=0 unknown=0 verdict=same-object
```

Independent re-derivation from the two committed capture trees (this seat, 2026-11-04): the moved
names are `date`, `x-fastly-request-id`, `x-served-by`, `x-timer` on `ds4cc-primary`, and those four
plus `x-cache` on each of `ds4cc-robots` and `ds4cc-sitemap`. 4 + 5 + 5 = 14, every name is in the
frozen `per-request` set, and all three body sha256 values are equal across the pair. This is the
same field set that `corpus/knowledge/capture-drift-validators.md` §6 reports from the earlier delta
tool, so the two instruments agree on *what* moved; the classifier adds *what each move means*.

The record therefore supports exactly one reading: at the two recorded instants the three surfaces
presented the same stored representations, and the 14 moved fields are per-request metadata of the
exchange. It does not support the stronger claim that the origin was consulted between the two
captures — that is what §4.2.3's `Age` and the edge's cache-status field are for, and neither is
evidence of an origin read.

## 7. Limits

- The verdict is about the 14 fields that moved. It cannot detect a change that leaves both the
  header map and the body digest identical; `same-object` is a statement about observed captures,
  not about the origin.
- The class membership is lane policy frozen in the contract, not a semantic theorem about headers.
  A `per-request` field can still be informative (`x-cache: HIT` says storage answered); it is simply
  not evidence of object change.
- Bodies are compared as sha256 over retained bytes: byte equality, not semantic equivalence.
- Header names are lower-cased and multi-valued fields joined with `, ` before comparison, so a
  re-ordering or re-splitting of the same values could appear as a diff. No such case occurs in this
  pair, and the classifier carries no fixture for one.
- The table is hand-maintained. An edge that begins emitting a new field lands in `unknown` and
  forces `representation-changed` until the table is amended — the safe direction, and visible in the
  `unknown` column rather than hidden.
