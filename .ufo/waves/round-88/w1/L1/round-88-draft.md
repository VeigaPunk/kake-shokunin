# Round 88 — conservative Vary matching and the round-87 defect queue

Base `f4479c14813037ad993a49a3dee4028763470f7a`; freeze v1 `4f8945ea`, v2
`80637397`, v3 `52e41d2d`; validated handoff `add7e49b`; measured carrier
(filled at integration). Evidence: `.ufo/waves/round-88/`; report
`.ufo/reports/round-88/kake.md`; LOG round 88.

## Claims and finite limits

C1 calibration (lowest owned axis, 2 HOLD): three routed round-87 defects —
R1 ledger companion, R2 diagnostic type, R3 ephemeral recheck path — decided by
one counter over committed bytes. D2 is behavioural (exit code, offending key and
JSON type in the message, six-term arithmetic, the tool's own 61-fixture selftest);
D1 binds the ledger's sha256 into the companion prose, so the text cannot be
written without reading the ledger bytes; D3 allows exactly one replaced line (the
`recheck:` metadata line) and otherwise only pure insertions, so a claim line
cannot be rewritten while "fixing" the metadata. D1/D3 remain partly textual: a
tree that writes the right prose and ships the real tool passes, and the non-author
closure is the catch. Closing three recorded defects is not a verdict on the
ledger's decisions.

C2 freshness (10 HOLD): a bounded capability. `scripts/vary_match.py` implements
the conservative subset of RFC 9111 §4.1's match rule; it scores 20/20 on the
hand-labelled frozen cases and 200/200 on a seeded differential population. A
`match` verdict is always produced by transformations §4.1 permits; a `mismatch`
may be stricter than a field-specific rule (no value case-folding, no reordering,
no internal whitespace folding). Not claimed: cache-key construction, storage,
revalidation, freshness, serving or any browser behaviour; no live surface is
asserted clean.

## Gate

Sources opened this round: RFC 9111 §4.1 (httpwg, GET 200 at 178,573 B, sha256
recorded by the L1 and re-opened by ScoutSpec and ScribeVary), RFC 9110 §12.5.5
(Vary field definition) read for the list grammar. Located quotes and access
dates are in the seats' receipts; the registry row carries the L1's own quote.

| Candidate | Decision | URL, access date, located quote ≤25 words | Reason and flip |
|---|---|---|---|
| S463 conservative Vary match rule | admit, A/mined | https://httpwg.org/specs/rfc9111.html#caching.negotiated.responses; 2026-11-04; §4.1: "A stored response with a Vary header field value containing a member \"*\" always fails to match." (17 words) | The same section states the MUST NOT, the permitted transformations and the absence rule the reader implements; the entry scopes only the conservative subset. Flip: a field-level rule that makes the exact profile unsound (a `match` the spec forbids) |
| "Vary match proves cache reuse is safe" | reject proposition | https://httpwg.org/specs/rfc9111.html#caching.negotiated.responses; 2026-11-04; §4.1: "the cache MUST NOT use that stored response without revalidation unless all the presented request header fields nominated by that Vary field value match" (24 words) | A match is one necessary condition among §4's several; freshness, method, URI and directives are separate and none is checked. Flip: a bounded procedure implementing §4's remaining conditions, never Vary alone |

Registry delta: S463 new tier A mined; `used-by` exactly
`corpus/knowledge/vary-matching.md`. Existing rows unchanged; the httpwg RFC 9111
URL is now carried by three scoped rows (S461 lifetime, S462 age, S463 matching),
which is the disclosed W04 increment.

## Mistakes

| Class | Evidence | Captured-by | Fix and observed failing witness |
|---|---|---|---|
| Reference oracle never cross-checked before freeze | freeze v2 `80637397`; `c88_vary.py` v2 returned `mismatch` where validation should refuse (cases r53/r150/r193) | the L1's own fallback implementation scored 197/200 minutes after the freeze | v3 moved validation before the wildcard rule and stated the precedence in contract.md; the same three cases now agree, and `--selftest` still reproduces all 20 frozen verdicts. Witness that can fail: v2's reference bytes still disagree on r150 |
| Scoring a candidate mid-write | `w1/ExecReader/vary_match.py` scored 197/200 at 16:02 and 200/200 minutes later without the file's contract changing | L1 re-scored after noticing the seat was still live (`proc://` showed it running) | Rule for later rounds: score only settled bytes, after the wave's results file names the seat's final output; the mid-write tally is recorded here, never filed as the measurement |
| Commit subject copied from the previous round | `add7e49b` subject says "twelve-seat inline handoff" while the wave has 14 seats | report assembly, reading the commit list | Subjects are written from the current wave's counts; the wrong subject stays in history as a disclosed errata, never rewritten |
