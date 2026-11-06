# ReviewFresh — contract v2 review against the RFC text (round 100, kake)

Scope: `.ufo/waves/round-100/fresh304-contract-v2.md` (clauses V2-1, V2-1a, V2-1b, V2-1c, V2-2,
V2-3, LC8, the e1-e7 binding clarifications), the 43 HAND cases tagged `v2-*` or `e1`-`e7` in
`.ufo/waves/round-100/c100_fresh304.py`, and the round-99 findings F1-F12
(`.ufo/waves/round-99/w1/ReviewFresh/contract-findings.md`). Read-only: nothing in the lane was
edited; findings are routed, not repaired. Per-case verdicts: `hand-review.tsv` (43 lines).

Sources (all digests verified before use, rc=0):
- RFC 9111 retained body `.ufo/waves/round-99/sources/rfc9111.txt`, sha256 `aeb52adb…` — §5.2
  (grammar, case-insensitive names, both argument forms), §5.2.2.4, §5.2.2.7, §5.2.3, §3.1,
  §3.2, §4.3.4 read in the retained bytes.
- RFC 9110 retained body `.ufo/waves/round-100/sources/rfc9110.txt`, sha256 `21c1cdce…` — §5.5,
  §5.6.1.2, §5.6.2, §5.6.3, §5.6.4 read in the retained bytes.
- Instruments `c100_fresh304.py` + `fresh304-contract-v2.md` match
  `controls/instrument-sha256.txt` (`sha256sum -c`, rc=0).

Receipts: counter selftest in-process (no sandbox, no candidate):
`python3 -B .ufo/waves/round-100/c100_fresh304.py --selftest` →
`hand=91/91 reference agrees; generated classes {…all 7 decision classes…}`, `selftest 2/2`,
rc=0. The frozen expectations judged here have zero drift against the frozen reference.

## Part 1 — V2 clause judgments (contradicts / open / requires)

Key text relied on: RFC 9111 §5.2 ("Cache directives are identified by a token, to be compared
case-insensitively, and have an optional argument that can use both token and quoted-string
syntax … recipients ought to accept both forms"; `cache-directive = token [ "=" ( token /
quoted-string ) ]`); §5.2.3 ("A cache MUST ignore unrecognized cache directives."); §3.1 b3 (the
directives "can have arguments that prevent storage of header fields"); §3.1 b4 (proxy-specific
fields "MUST NOT be stored"); §3.2 (MUST add each header field, replacing, with §3.1
exceptions); §4.3.4 (first-match identification; MUST update for each identified response; MUST
NOT update on strong-none). RFC 9110 §5.5 ("A field value does not include leading or trailing
whitespace … MUST exclude such whitespace prior to evaluating"; `field-value = *field-content`);
§5.6.1.2 (recipient MUST accept lists with empty elements); §5.6.2 (tchar ASCII-only); §5.6.3
(OWS = *( SP / HTAB )); §5.6.4 (qdtext, quoted-pair).

**V2-1 (parse the 304's Cache-Control per §5.2 + §5.6.1.2/§5.6.2/§5.6.4).** REQUIRED in its
parse mechanics: the grammar is §5.2 verbatim; accepting empty list elements is a §5.6.1.2
recipient MUST (v2's `#element => [ element ] *( OWS "," OWS [ element ] )` is quoted exactly);
tchar and qdtext/quoted-pair sets match §5.6.2/§5.6.4; "a comma inside a quoted-string does not
split the list" follows from §5.6.4 atomicity; "whitespace only as OWS around commas and at the
two ends" is what the productions leave (OWS exists only in the list rule; end-of-value OWS is
removed per §5.5 before evaluation). The RFC contradicts nothing here. What the RFC leaves open
is the *disposition* on a value that does not parse — taken by V2-1a below. "Only the 304's
Cache-Control is examined; stored Cache-Control values are copied as data" is RFC-consistent
(qualified no-cache permits storing listed fields, restricting only reuse; see however G3 for
the private-qualified stored-side corner).

**V2-1a (non-parsing value refused, `invalid_input: malformed cache-control`).** Left open by
the RFCs; permitted as a choice. No MUST addresses a malformed Cache-Control value (RFC 9110
§5.5's reject-or-replace MUST covers only CR/LF/NUL, which v1 already refuses). The refusal
cannot trigger §4.3.4's update MUST because zero responses are identified. Correctly LC8-marked.

**V2-1b (qualified no-cache/private, either argument syntax, any case, refused as outside the
contract).** The RFC *requires* recognizing these qualified forms as qualified (§5.2.2.4/§5.2.2.7
define them; §5.2 makes the name comparison case-insensitive — a required rule; §5.2's grammar
admits the token argument, and "recipients ought to accept both forms" — an ought, not a MUST).
The *refusal* disposition is left open by the RFCs and permitted: refusing leaves zero identified
responses, so §4.3.4's update MUST never fires; §5.2.3's MUST-ignore does not apply because
no-cache/private are recognized directives; the stricter-than-RFC behavior cannot violate
§3.1 b3 or §5.2.2.7 (it forecloses rather than commits the storage). Including the empty quoted
string `""` and escape-bearing arguments (`v2-cc-empty-quoted`, `v2-cc-quoted-escape-arg`) goes
beyond what the RFCs settle (a zero-name/degenerate `#field-name` argument is undefined
behavior); pinning it fail-closed is a lane choice in the LC6 lineage and is stated in the
clause. No new MUST contradiction.

**V2-1c (any other directive ignored; unqualified no-cache/private ignored for this test).**
REQUIRED for unrecognized extensions: §5.2.3 "A cache MUST ignore unrecognized cache
directives", and v2 matches at token identity (`x-no-cache` ≠ `no-cache`, `no-cachex` ≠
`no-cache`), which is exactly the F10 defect removed. Copying the whole field as data while
ignoring the directive is simultaneously required by §3.2 (the Cache-Control field itself is
added to the stored response). Ignoring *unqualified* no-cache/private is RFC-consistent:
§3.1 b3 is argument-scoped, and unqualified reuse semantics are §4 scope, which the contract
declares not covered. No contradiction.

**V2-2 (output values trimmed of leading/trailing SP/HTAB, inner whitespace kept).** REQUIRED:
RFC 9110 §5.5 makes leading/trailing whitespace not part of the field value and orders field
parsing implementations to exclude it before evaluation; a stored field value therefore never
carries OWS, so the trimmed copy is the only faithful representation of "add each header field"
(§3.2). This clause is the fix for round-99 F2 (the two r99 `disagree` cases `strong-trim` and
`upd-value-bytes-kept` are flipped to RFC-conforming expectations as `v2-strong-trim` and
`v2-upd-value-trimmed`). No new MUST contradiction; v1's byte-for-byte rule was the contradiction.

**V2-3 (proxy-authenticate / proxy-authentication-info / proxy-authorization never appear in an
updated response).** REQUIRED once "the updated header map is the new stored response" is
granted: §3.1 b4 "MUST NOT be stored". Dropping stored-side occurrences is the same handling F3
routed, and the clause keeps every other stored field (e1), which §3.1 b1/b2 permit (removal
before storage is MAY). No contradiction. Residual corner: see G3.

**LC8 (refusing an unparseable list is the lane's choice; RFC 9111 does not require it).**
Accurate. No RFC 9111/9110 section imposes a disposition for a malformed Cache-Control value;
LC8's fail-closed rationale is sound — an unparseable list cannot be checked for the qualified
forms whose §3.1 b3/§5.2.2.4/§5.2.2.7 semantics restrict storage, so silently ignoring it could
miss a storage restriction, and refusing cannot violate any MUST. V2-1a correctly carries the
LC mark.

**Does v2 newly contradict any RFC MUST? No.** Systematic scan of the MUSTs in play:
§5.2.3 ignore-unrecognized (v2 complies — required), §3.1 b4 MUST-NOT-store proxy fields
(complies), §3.2 MUST-add-each-field (complies, with §3.1 exceptions), §4.3.4 MUST-update
identified / MUST-NOT-update on strong-none (preserved from v1; refusals leave zero identified
responses so the update MUST never triggers), §5.5 MUST-exclude-OWS (v1 violated it; v2
complies), §5.5 CR/LF/NUL reject-or-replace (v2 refuses = reject), §5.6.1.2 MUST-accept empty
elements (complies), §5.2 case-insensitive comparison (complies). `rfc_contradictions = 0`.

## Part 2 — F1-F12 closure (round-99 findings against v1)

Verified against v2's text and the hand cases; `closed` below = the route is genuinely
discharged, not merely claimed.

| F | Was | Status | Evidence |
|---|-----|--------|----------|
| F1 | token-form qualified no-cache/private missed by LC6 | **closed** | V2-1b accepts both forms, any case; hand cases v2-cc-token-nocache, v2-cc-token-private, v2-cc-token-upper-nocache pin it; CC_POOL carries `no-cache=Set-Cookie` into generated cases |
| F2 | byte-for-byte copy of OWS-bearing values | **closed** | V2-2 trims; v2-strong-trim, v2-upd-value-trimmed, v2-stored-value-trimmed, v2-empty-after-trim; the two r99 `disagree` cases are flipped |
| F3 | stored proxy-specific fields pass through | **closed** | V2-3 drops the three names from the stored map; v2-stored-proxy-dropped pins it |
| F4 | initial-set definition unnamed (erratum EID 9185) | open (as declared) | Not covered still says "initial-set computation (§4, erratum EID 9185)" without naming the caller's definition; F4's route asked for the definition |
| F5 | "most recent" = receipt order, unmarked | open (as declared) | no LC7 added; v2 is silent on `received` |
| F6 | obs-text as code points, unmarked | open, disclosed | V2-1 now states "obs-text = U+0080-U+00FF as in v1" — explicit, but not LC-marked (see G2) |
| F7 | LC2 "all validators must correspond" rests on open text | open (as declared) | LC2 untouched; e7 pins only the tie behavior |
| F8 | §3.1 MAY presented as requirement (Connection) | open (as declared) | v1 update text unchanged; e1 keeps the permitted choice |
| F9 | Last-Modified accepts any string | open (as declared) | e3 adds only trimming; no HTTP-date validation |
| F10 | substring check refuses unrecognized directives | **closed** | V2-1c matches at token identity; v2-cc-ext-xnocache, v2-cc-ext-nocachex, v2-cc-ext-xprivate-token, plus quoted-comma/quoted-escape protecting the boundary inside quotes |
| F11 | stored-side refusal broader than RFC requires | open, disclosed | e2 states the behavior explicitly and pins it with e2-stored-bad-etag-lm304/noval, but no LC mark (see G1) |
| F12 | Not covered omits erratum re-association, §3.4, §4.1 | **closed** | Not covered now lists "§3.4 partial-content combination, §4.1 selecting-header re-association" alongside the erratum reference |

Net: 5 closed (F1, F2, F3, F10, F12) — exactly the set v2 claims; 7 open (F4-F9, F11) — exactly
the set v2 declares open. The contract's own closure claims are honest.

## Part 3 — new findings (severity M / L; routed, not repaired)

**G1 (L). The e2 binding clarification states broader-than-RFC behavior without an LC mark.**
e2 refuses the whole call when ANY stored response carries a malformed ETag, even when selection
would never read it (e2-stored-bad-etag-noval is exactly that shape). The RFCs are silent
(F11's observation stands), yet the clarification reads as binding behavior, not as a marked
lane choice — a future reader cannot tell RFC-derived from chosen. F11's route offered "mark the
choice"; the marking is the missing half. Routed: add an LC mark to e2 (and consider the same
for e5's refusal-never-a-traceback wording, which is interface rather than RFC).

**G2 (L). The obs-text mapping is stated but not marked.**
V2-1 sets `obs-text = U+0080-U+00FF` (code points) where RFC 9110 §5.6.4 defines obs-text as
octets %x80-FF. The mapping is a JSON-transport artifact and does not make any expectation
contradictory (all RFC-valid single-byte obs-text values map into the code-point range, but a
multi-byte UTF-8 ETag such as `"€"` maps outside it and is refused — the r99 F6 case). F6's
route was "mark the mapping as an LC"; v2 disclosed the mapping without the mark. Routed: mark it.

**G3 (M). Stored-side qualified Cache-Control is copied as data; the 304-side is refused — an
asymmetry the counter does not test.**
V2-1 examines only the 304's Cache-Control. A stored response carrying
`Cache-Control: private="Set-Cookie"` together with `Set-Cookie` is copied verbatim into the
updated response, and V2-3 declares that map the new stored response. RFC 9111 §5.2.2.7 says a
*shared* cache MUST NOT store the listed fields; §3.1 b3 describes exactly this
storage-prevention capability. The lane cannot know whether its caller is a shared cache or
which scheme-specific requirements apply, so the dispositions are: silently copy (current v2 —
risks re-stamping storage a shared cache MUST NOT hold), refuse fail-closed (mirroring V2-1b's
treatment of the 304 side), or exclude the listed fields (not derivable without scheme
context). Not counted as a direct RFC contradiction: the MUST is conditional on the caller's
cache kind, the non-conforming storage predates the call, and the contract's conformance
disclaimer applies — the same discipline that kept r99-F3 out of the RC count. No hand case and
no generated case covers a stored qualified directive (the grammar only puts
`max-age=<n>` in stored Cache-Control), so a candidate that copies stored qualified directives
passes the counter. Routed: either extend the outside-contract refusal to a stored qualified
Cache-Control, or add an explicit Not-covered/LC sentence naming this corner; add a hand case at
the next freeze.

## Part 4 — coverage notes (not findings)

- **e4 has no dedicated hand case.** Its two rules (refusal → stdout exactly zero bytes;
  decision → one JSON object with no leading whitespace and at most one trailing `\n`) are
  enforced structurally by `judge()` on every hand and generated case, and "never a traceback"
  follows from `err.startswith("invalid_input:")`. Complete, so no case is missing.
- The e1-e7 clarifications now have hand cases for every class except e4 (structural), which
  discharges the R99-8 route ("seven escape classes as hand cases").
- `v2-cc-empty-quoted` and `v2-cc-quoted-escape-arg` pin the only two qualified-form boundary
  cases where the RFCs leave the disposition genuinely open — good regression anchors.
- The generated population exercises the new refusals: CC_POOL carries six malformed and six
  qualified values; selftest shows refusal=939/3000 with all seven decision classes present.

## Verdict line

`REVIEWFRESH hand=43/43 v2_findings=3 rfc_contradictions=0 closed=F1,F2,F3,F10,F12`
