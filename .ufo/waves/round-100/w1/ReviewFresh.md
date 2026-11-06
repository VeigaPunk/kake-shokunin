# ReviewFresh — round 100, C2 contract v2 review (seat report)

Lane tip read: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse master` →
`e84a18714b6be7fd2456a2dcc5f28c0cb0ab981f` (= HEAD; the C1 repair commit is the tip).

## Scope and method

Target: contract v2 (`.ufo/waves/round-100/fresh304-contract-v2.md`) and its hand expectations
against the RFC text. Findings routed; the frozen C2 predicate untouched; nothing in the lane
edited beyond my two w1 files plus this report.

1. Digests verified before use (`sha256sum -c` against
   `.ufo/waves/round-100/controls/instrument-sha256.txt`): `c100_fresh304.py OK`,
   `fresh304-contract-v2.md OK`; RFC 9110 retained body re-hashed `21c1cdce…` (matches the
   frozen digest and the contract's quote), RFC 9111 retained body `aeb52adb…` (matches the
   round-99 freeze value).
2. Counter selftest run in-process (read-only; no sandbox, no candidate):
   `python3 -B .ufo/waves/round-100/c100_fresh304.py --selftest` →
   `hand=91/91 reference agrees; generated classes {"must-not-update/strong": 821, "no-update/no-validator": 330, "no-update/weak": 508, "refusal": 939, "update/no-validator": 20, "update/strong": 174, "update/weak": 208}` / `selftest 2/2`, observed rc=0. The 43 expectations
   judged here have zero drift against the frozen reference.
3. Normative text read in the retained bytes: RFC 9111 §5.2, §5.2.2.4, §5.2.2.7, §5.2.3, §3.1,
   §3.2, §4.3.4; RFC 9110 §5.5, §5.6.1.2, §5.6.2, §5.6.3, §5.6.4.

Deliverables: `w1/ReviewFresh/hand-review.tsv` (43 verdict lines: 43 agree / 0 disagree),
`w1/ReviewFresh/contract-findings.md` (V2 clause + LC8 judgments, F1-F12 closure table, new
findings G1-G3).

## Headline

- **hand=43/43 agree.** Every `v2-*` / `e1`-`e7` expectation follows from the cited RFC text or
  from a marked lane convention (V2-1a/LC8, LC1-LC6 lineage). No expectation contradicts an RFC
  MUST. (As in r99, unmarked-but-permitted interface checks are counted agree with an explicit
  contract-interface basis, not as RFC-grounded.)
- **V2 clauses: nothing contradicted, several required.** V2-1's parse mechanics are
  RFC-required (§5.2 grammar; §5.6.1.2 recipient MUST for empty elements; §5.6.2 tchar; §5.6.4
  qdtext/quoted-pair); V2-2 is required by RFC 9110 §5.5 (and is the F2 fix); V2-3 is required
  by §3.1 b4 once the updated map is the new stored response. V2-1a/V2-1b's refusal dispositions
  are left open by the RFCs and taken as marked lane choices — refusing leaves zero identified
  responses, so §4.3.4's update MUST never fires and §5.2.3's MUST-ignore does not apply to the
  recognized no-cache/private. LC8's claim ("RFC 9111 does not require it") is accurate and its
  fail-closed rationale sound.
- **v2 newly contradicts no RFC MUST** (systematic scan: §5.2.3, §3.1 b3/b4, §3.2, §4.3.4, §5.5,
  §5.6.1.2, §5.2 case rule). `rfc_contradictions=0`.
- **Closure: 5 of the r99 F-findings closed — F1, F2, F3, F10, F12 — exactly the set v2 claims;
  F4-F9 and F11 remain open, exactly as v2 declares.** The two r99 `disagree` hand cases are
  correctly flipped (v2-strong-trim, v2-upd-value-trimmed).

## Findings by severity (routed; details in contract-findings.md)

- **G3 (M).** Stored-side qualified Cache-Control asymmetry: v2 refuses a 304 carrying
  `no-cache=`/`private=` qualified forms but copies a *stored* `private="Set-Cookie"` (with
  Set-Cookie) verbatim into the updated response that V2-3 declares the new stored response;
  §5.2.2.7 MUST-NOTs exactly that storage for a shared cache. Conditional MUST + unknowable
  caller context → not counted as a direct RFC contradiction (same discipline as r99-F3). No
  hand or generated case covers a stored qualified directive, so the counter cannot see it.
  Routed: refuse fail-closed on the stored side too, or mark the corner Not-covered/LC; add a
  hand case next freeze.
- **G1 (L).** e2's binding clarification (refuse on a malformed ETag in ANY stored response,
  even one selection never reads) is broader than the RFC requires and now explicit + hand-pinned
  (e2-stored-bad-etag-lm304, e2-stored-bad-etag-noval), but still carries no LC mark — half of
  F11's "mark the choice" route. Routed: add the mark.
- **G2 (L).** The obs-text mapping (contract code points U+0080-U+00FF vs RFC octets %x80-FF) is
  now stated in V2-1 but not LC-marked; a multi-byte UTF-8 ETag (`"€"`) remains refused while
  being RFC-valid. F6 stays open, half-landed. Routed: mark it.

## Residual risk and verification gaps

- I judged the frozen expectations against the RFC text and the frozen reference's agreement
  (selftest receipt above); I did not run any candidate — `candidate=present hand=91/91
  generated=300/300` at the C2 content commit is ExecFresh/L1's check against the frozen
  predicate, and the bwrap-sandboxed counter run is theirs to exercise.
- G3's classification (conditional-MUST, not an RC) rests on the caller-context argument; a
  stricter reviewer could count it. Either way the fix is a routing decision, not mine.
- e4 (stdout discipline) has no dedicated hand case; it is enforced structurally by `judge()` on
  every case, so this is a coverage observation, not a gap in the expectations.

## Tooling

No tools installed or upgraded (none needed beyond stock python3/git/sha256sum).

REVIEWFRESH hand=43/43 v2_findings=3 rfc_contradictions=0 closed=F1,F2,F3,F10,F12
