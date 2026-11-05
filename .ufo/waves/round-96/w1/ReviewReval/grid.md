# ReviewReval — independent 24-case reval grid (round 96, w1)

REVIEW-REVAL agree=24/24 tooldefects=0 contractdefects=0 referencedefects=0

Seat: ReviewReval (leaf, independent non-author review of the C2 line).
Derived from: `.ufo/waves/round-96/reval-contract-v1.md` (frozen, sha
`65f0a347…`, digest-verified) + RFC 9111 §4.3 read from the retained body
`.ufo/waves/round-90/L1/src/rfc9111.txt` (sha256 `aeb52adb…`, equal to the
freeze's comparison digest; quote anchors at lines 848, 852, 861, 935, 938,
944 — each verified present at exactly the line the freeze names) and
RFC 9110 §8.8.3 read from the retained S455 body
`.ufo/waves/round-81/w1/ScoutSources/rfc9110.txt` (lines 3570–3617).

## What was scored

- Delivered candidate `scripts/reval_exchange.py`, sha256
  `192b3bf7596abad8ef76a7a8262ecc29c0d565587153547ee61b5ee7566c7212`
  (untracked worktree file at scoring time; digest stable before/after the
  run and at report time). **The candidate was present when I ran** — the
  absent-candidate fallback (frozen positive control as scored subject) was
  not needed; the control was run anyway as corroboration.
- Frozen positive control `.ufo/waves/round-96/frozen/pos-good-reval.py`
  sha256 `47c65725…` — equal to the population pin — also 24/24.
- In-counter reference `c96_reval.py::reference()`, scored from a
  digest-verified scratch copy (`ec40aec1…` = freeze pin; the frozen counter
  bytes were never edited): agrees with my derivation on 22/22 dict cases
  (16 decisions matched exactly, 6 refusals correctly raised `Invalid`);
  the 2 raw cases are byte-level and subject-side only by contract (the
  counter's own `reference_selfcheck` also skips `__raw__` inputs).
- Command per case: `python3 -B <subject>` with the case payload on stdin,
  cwd = my scratch, env `PATH=/usr/bin:/bin HOME=<scratch>` (sandbox-free
  run authorized by the seat spec; my cases are my own). Receipts:
  `receipt-run-candidate.txt` (rc=0, agree=24/24, reference_agree=22/22),
  `receipt-run-control.txt` (rc=0, agree=24/24), `receipt-nonoverlap.txt`
  (intersection=0), `receipt-digests.txt` (all freeze pins verified OK).

## Non-duplication from the frozen hand cases (mechanical)

`receipt-nonoverlap.txt`: sha256 over the exact stdin payload of each of my
24 cases vs each of the 37 frozen hand-case inputs (from the digest-verified
counter copy's `hand_cases()`): **intersection = 0**. Nearest frozen
neighbor and the differing dimension:

| my case | nearest frozen hand case | differs by |
|---|---|---|
| construct/lm-zero-no-etag | construct/etag-zero-lm | no etag (LM-only), LM=0 |
| construct/etag-single-obtext | construct/obs-text-etag | single-byte obs-text opaque part |
| construct/weak-obtext-both | construct/weak-etag-verbatim | obs-text inner byte, LM=5 |
| construct/empty-opaque-tag | (none) | `""` — grammar-valid empty opaque tag |
| construct/exists-false-no-validators | construct/neither-validator | exists=false |
| construct/lm-huge | construct/lm-only | LM=253402300799 (no-ceiling bound) |
| c304/etag-only | c304/lm-only | etag-only validator set |
| c304/lm-zero | c304/lm-only | LM=0 |
| c5xx/500-etag-only | c5xx/500 | etag-only |
| c5xx/501-both | c5xx/500 | status 501 |
| c5xx/599-lm-only | c5xx/599-upper-edge | LM-only |
| c4xx/299-both | c200/replace | status 299 |
| c4xx/300-lm-only | c410/replace | status 300, LM-only |
| c4xx/200-etag-only | c302/replace | status 200, etag-only |
| c4xx/499-both | c499/replace-upper-edge | both validators |
| c4xx/204-lm-only | c410/replace | status 204 (payload-less exclusion) |
| refuse/status-200-exists-false-no-validator | refuse/status-without-validator | exists=false, status 200 |
| refuse/exists-false-etag | refuse/validators-without-representation | etag-only |
| refuse/etag-empty-string | refuse/etag-not-string | zero-length string |
| refuse/etag-space-inner | refuse/etag-quoted-control | SP (0x20) vs control char |
| refuse/status-199 | refuse/1xx-interim | 199 (1xx upper edge) vs 100 |
| refuse/lm-bool-true | refuse/status-bool | bool in LM slot, not status slot |
| refuse/raw-dup-exists-nested | refuse/raw-nested-dup | duplicated key `exists` vs `last_modified` |
| refuse/raw-dup-stored-top | refuse/raw-dup-bytes | duplicated key `stored` vs `received_status` |

The seat-spec example "both validators + received 200" is the frozen
`c200/replace` shape itself; a value-variant would duplicate a frozen case,
so plain 200 is covered by `c4xx/200-etag-only` instead (validator-set
dimension the frozen set lacks).

## The grid (24 cases; full inputs in `cases.json`)

Expected decisions are mine, derived clause-by-clause from the contract
before running; grounding labels say whether the clause is RFC-exact (quote
at the retained-body line) or lane convention as the contract labels it.

| # | case | clause | input (exists/etag/lm/status) | expected | grounding |
|---|---|---|---|---|---|
| 1 | construct/lm-zero-no-etag | C1 | T/–/0/– | construct, IMS=0 | SHOULD-as-sent = lane convention; LM=0 falsy-trap boundary |
| 2 | construct/etag-single-obtext | C1 | T/"\u0086"/–/– | construct INM verbatim | RFC-exact: etagc = %x21 / %x23-7E / obs-text (RFC 9110 §8.8.3) |
| 3 | construct/weak-obtext-both | C1+C2 | T/W/"\u00ff"/5/– | construct both, INM verbatim | RFC-exact MUST (line 848, "MUST send the relevant entity tags … if the entity tags were provided in the stored response(s) being validated") + C2 lane convention |
| 4 | construct/empty-opaque-tag | C1 | T/""/–/– | construct INM=`""` | RFC-exact: `opaque-tag = DQUOTE *etagc DQUOTE`, * allows zero; RFC's own example `ETag: ""` |
| 5 | construct/exists-false-no-validators | C1 | F/–/–/– | cannot-revalidate | contract definition: C6 refusal list has no such entry; C1 keys on validators |
| 6 | construct/lm-huge | C1 | T/–/253402300799/– | construct IMS=253402300799 | lane convention (supplied values; no ceiling fixed) |
| 7 | c304/etag-only | C3 | T/"e1"/–/304 | update-stored | RFC-exact (line 935: "A 304 (Not Modified) response status code indicates that the stored response can be updated and reused") |
| 8 | c304/lm-zero | C3 | T/–/0/304 | update-stored | RFC-exact (line 935) |
| 9 | c5xx/500-etag-only | C4 | T/"x9"/–/500 | may-reuse-stored | RFC-exact (line 944: "if a cache receives a 5xx (Server Error) response while attempting to validate a response, it can either forward this response … or act as if the server failed to respond") |
| 10 | c5xx/501-both | C4 | T/"501"/7/501 | may-reuse-stored | RFC-exact (line 944) |
| 11 | c5xx/599-lm-only | C4 | T/–/3/599 | may-reuse-stored | RFC-exact (line 944; class edge 599) |
| 12 | c4xx/299-both | C5 | T/"a"/11/299 | replace-stored | lane convention (200–499 by status alone), contract-labeled |
| 13 | c4xx/300-lm-only | C5 | T/–/4/300 | replace-stored | lane convention |
| 14 | c4xx/200-etag-only | C5 | T/"r96-b"/–/200 | replace-stored | lane convention for class membership; RFC-exact that a full response MUST be used once it is one (line 938: "A full response (i.e., one containing content) … the cache MUST use the full response to satisfy the request") |
| 15 | c4xx/499-both | C5 | T/"n"/2/499 | replace-stored | lane convention (upper edge 499) |
| 16 | c4xx/204-lm-only | C5 | T/–/6/204 | replace-stored | lane convention — exactly the contract's named payload-less-204 exclusion |
| 17 | refuse/status-200-exists-false-no-validator | C6 | F/–/–/200 | refuse | contract: received_status present while no validator stored |
| 18 | refuse/exists-false-etag | C6 | F/"z"/–/– | refuse | contract: validators present while exists false |
| 19 | refuse/etag-empty-string | C6 | T/"" (empty str)/–/– | refuse | RFC-exact grammar: zero-length string ≠ DQUOTE *etagc DQUOTE |
| 20 | refuse/etag-space-inner | C6 | T/"a b"/–/– | refuse | RFC-exact: 0x20 ∉ etagc |
| 21 | refuse/status-199 | C6 | T/"q"/1/199 | refuse | RFC-grounded: 1xx interim is never a validation response (upper edge 199) |
| 22 | refuse/lm-bool-true | C6 | T/–/true/– | refuse | contract: LM neither null nor non-negative integer; JSON true is not a number (bool⊂int trap) |
| 23 | refuse/raw-dup-exists-nested | C6 | raw, dup `"exists"` in stored | refuse | lane convention (S034): refuse raw duplicate keys, never silently last-win |
| 24 | refuse/raw-dup-stored-top | C6 | raw, dup `"stored"` key | refuse | lane convention (S034) |

Observed: **24/24 agree** on the candidate, 24/24 on the frozen positive
control, 22/22 on the in-counter reference (dict cases; refusals = raised
`Invalid`). Zero disagreements to classify → tooldefects=0,
contractdefects=0, referencedefects=0.

## Clause-by-clause: reference() vs the fetched RFC text

Reading checked against the retained RFC 9111 body (sha `aeb52adb…`) and the
retained RFC 9110 §8.8.3 body (S455). No clause reading disagreed. Verdicts:

- **C1 validator selection — agree, RFC-exact.** Line 848: "MUST send the
  relevant entity tags (using If-Match, If-None-Match, or If-Range) if the
  entity tags were provided in the stored response(s) being validated." The
  reference constructs If-None-Match; that is the right member of the MUST's
  triple because §4.3.2 (lines 887–891) makes the cache's own evaluation
  turn on If-None-Match ("the If-Match and If-Unmodified-Since conditional
  header fields are not applicable to a cache, and If-None-Match takes
  precedence over If-Modified-Since"), and the §4.3.1 bullets themselves
  mark If-Match/If-Range "for representation selection". Verbatim forwarding
  of the stored tag (weak marker included) is what "send the relevant entity
  tags" requires.
- **C2 both validators together — agree; correctly labeled lane
  convention.** Line 852: "SHOULD send the Last-Modified value (using
  If-Modified-Since) if the request is not for a subrange, a single stored
  response is being validated, and that response contains a Last-Modified
  value" — an etag does not exclude the SHOULD (the "only" condition belongs
  to the MAY bullet for If-Unmodified-Since/If-Range), and line 861: "In
  most cases, both validators are generated in cache validation requests,
  even when entity tags are clearly superior". The subrange condition is
  unrepresentable over supplied values; treating the SHOULD as sent is
  exactly the convention the contract labels. Honest.
- **C3 304 → update-stored — agree, RFC-exact at the reported level.**
  Line 935 (quote above). The RFC's "can be updated and reused" is
  permission language, and §4.3.4's update-set selection (strong-validator
  matching, "the cache MUST NOT use the new response to update any stored
  responses" on no match) needs the received 304's validators, which
  supplied values do not carry. The contract names that exclusion; the
  decision reports the §4.3.3 indication only. No disagreement.
- **C4 5xx → may-reuse-stored — agree, RFC-exact at the permission level.**
  Line 944 (quote above). The class is 500–599; the other branches (forward
  the 5xx, retry) are real, and the contract says the instrument "reports
  the permission, not which branch a real cache takes", with §4.2.4
  constraints explicitly outside. The decision name carries "may". No
  disagreement.
- **C5 200–499 → replace-stored — agree; the one designed divergence, and
  the label is present.** Line 938 defines the RFC class by content, not by
  status range: "A full response (i.e., one containing content) indicates
  that none of the stored responses nominated in the conditional request are
  suitable." A payload-less 204 is not RFC-exactly a full response; the
  contract maps 200–499 by status code alone and labels it a lane
  convention with the 204 exclusion named. My case 16 pins this boundary.
  Had C5 been labeled RFC-exact this would be a contract defect; it is not.
- **C6 refusals — agree.** The etag grammar check is byte-exact against
  RFC 9110 §8.8.3 (retained body lines 3579–3585): `entity-tag = [ weak ]
  opaque-tag`, `weak = %s"W/"` (case-sensitive — the reference's
  `startswith("W/")` matches), `opaque-tag = DQUOTE *etagc DQUOTE`,
  `etagc = %x21 / %x23-7E / obs-text`. Consequences all verified by the
  grid: `""` is grammar-valid (the RFC's own example `ETag: ""`) and the
  reference/control/candidate all construct it; a zero-length string, a SP
  inside the opaque part, and code points above U+00FF are refused; the 1xx
  refusal (100–199) matches the interim class; LM/status bool exclusion is
  the contract's "not an integer" over JSON types; the two coherence
  refusals (status without validator; validator without representation) are
  contract definitions with sound RFC grounding (a conditional validation
  exchange presupposes a stored validator); raw duplicate keys are refused
  subject-side through the real stdin path (S034), confirmed on both my raw
  cases.

### Observations (recorded, none rises to a defect)

1. **obs-text over JSON strings is an unpinned mapping.** The contract pins
   the etagc grammar but not how a JSON string maps to octets; the
   reference resolves obs-text as single code points U+0080–U+00FF and
   refuses code points above (e.g. U+65E5). Conservative, internally
   consistent (a raw two-byte UTF-8 é decodes to U+00E9 and is accepted),
   within the supplied-values convention. If a future round cares, contract
   v2 can pin the mapping in one sentence. Routing-worthy note only.
2. **First-run harness miscount, disclosed.** My first runner credited the
   reference's refusal-style (`Invalid` raised) as failure on the six
   expected-refusal dict cases (`reference_agree=16/22` printed in the
   superseded first receipts). The comparison was corrected in my harness
   (refusal-raised = agreement with an expected refusal) and both final
   receipts re-run clean (`reference_agree=22/22`, rc=0). Lane bytes were
   never touched; the error was in my scorer only.
3. **`lsp` device unavailable** in this harness (no lsp route mounted), so
   semantic checks were made by full direct read of the reference/control
   bytes (the reference is ~100 lines, read in full) plus byte-level runs;
   text search was used only for quote anchoring, which the retained bodies
   pin exactly.

## Residual risk and verification gaps

- I scored the **worktree bytes** `192b3bf7…` of the candidate (untracked at
  scoring time). The L1's counter reads committed bytes at `--revision`; if
  the author repairs or commits different bytes, my 24/24 covers only
  `192b3bf7…` (digest printed in both receipts and stable across the run).
- My grid is 24 cases over decisions/refusals; it does not exercise the
  counter's forgery, mutant, anti-table or generated-case machinery — those
  are the frozen counter's own surface and out of this seat's scope.
- Sandbox-free runs per seat authorization; the counter's audit-hook sandbox
  path was not exercised by my grid.
- No mutating git/jj command was run anywhere; fixtures were not needed (no
  clone created). Scratch tree `/fast/scratch/hyaku/kake-r96/ReviewReval/`
  is deleted after receipt copy, per seat bounds.

## Receipts (flat, this directory)

- `receipt-run-candidate.txt` — 24-case run over the candidate; rc=0;
  agree=24/24; reference_agree=22/22; subject digests before/after equal.
- `receipt-run-control.txt` — same grid over the frozen positive control;
  rc=0; agree=24/24; subject sha `47c65725…` equals the population pin.
- `receipt-nonoverlap.txt` — 24×37 input-digest intersection = 0.
- `receipt-digests.txt` — freeze instrument pins re-verified (c96_selfassess
  `a282da65…`, c96_reval `ec40aec1…`, c95_selfassess `8fd27d62…`, pos-good
  `47c65725…`, population pins `d9c8f96e…`, contract `65f0a347…`, RFC body
  `aeb52adb…`), counter scratch copy digest-equal.
