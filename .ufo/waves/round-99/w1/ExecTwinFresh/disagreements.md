# ExecTwinFresh — disagreements, twin vs frozen/pos-oracle.py (C2 contract v1)

Totals (run.txt): inputs=2400, disagreements=30, all 30 are one divergence class.
Classification: **contract ambiguity** (30 inputs). Oracle defects: 0. Twin defects: 0 by the
literal contract text; see the note on the cited RFC below, which is what makes this an
ambiguity rather than a closed question.

## The class

Every disagreement has the same shape: the 304's `Cache-Control` value carries a qualified
`no-cache="…"` or `private="…"` directive whose directive name is not all-lowercase
(`Private="g"` 15 inputs, `NO-CACHE="x"` 9 inputs; 6 more have the 304 key `cache-control`
in lowercase with those values). The oracle exits 1 (refuses, LC6). The twin exits 0 and
selects a stored response. Zero cases go the other way (twin refuses / oracle accepts), and
no lowercase-directive case disagrees.

Case-matched probes (targeted, stored=[]; oracle rc / twin rc):
`no-cache="x"` 1/1, `private="g"` 1/1, `No-Cache="x"` 1/0, `NO-CACHE="x"` 1/0,
`Private="g"` 1/0, `PRIVATE="g"` 1/0.

## Who is right, from the text

Contract LC6 (fresh304-contract.md, Validators section):
> "**LC6:** a 304 whose Cache-Control value contains `no-cache="` or `private="` (qualified
> forms, §3.1 bullet 3) is refused as outside this contract."

Read literally, this is a case-sensitive substring test, and the twin implements exactly that
(`'no-cache="' in cc304`). Under the literal text the twin is correct and the oracle is
stricter than the contract words.

The contract's own cited source points the other way. RFC 9111 (retained body
`sources/rfc9111.txt`, line 1098):
> "Cache directives are identified by a token, to be compared case-insensitively"

and §3.1 bullet 3 (retained body lines 1273–1284) defines the qualified form of `no-cache` and
`private` by the directive. So `NO-CACHE="x"` *is* the qualified form of the directive the
contract names, and LC6 says it "is refused". The oracle (case-insensitive) follows the cited
RFC; the twin (case-sensitive) follows the bare text.

The contract's LC6 text states no case rule for directive names. Its only case statements are
for header field names (line 27, 61, 66) and for `W/` in ETags (line 34). The lane's control
receipts `controls/ctl-c2-*.txt` contain no Cache-Control text at all (grep, rc 1), so no frozen
control exercises a Cache-Control value, lowercase or otherwise. That is why the differential
is the first thing to surface this class.

Why it matters: LC6 refuses 304s the lane cannot handle under §3.1 bullet 3. If the
case-sensitive reading is kept, a 304 with `NO-CACHE="x"` gets through and the lane freshens
stored responses on a response whose qualified no-cache the contract says is out of scope.
The oracle's stricter reading is the safer one, but the contract needs to say it.

Recommended resolution for the L1 (not applied by this seat; contract is frozen):
- clarify LC6 to say directive names are compared case-insensitively per RFC 9111 (line 1098),
  so the oracle's reading becomes the contract's reading; OR
- keep the literal text and state that the case-sensitive reading is intended. The twin then
  needs no change under the literal reading.
Either way the decision is the contract's, not the oracle's. Per the freeze, no contract or
counter edit is made after scoring; this is a finding to route, not a repair.

## The other 2370 inputs

All other inputs agree on rc and on the parsed JSON (decision, rule, updated list order and
per-header values), or on refusal shape (empty stdout, `invalid_input:` prefix, rc 1). Refusal
reason text is not compared because the contract specifies the `invalid_input:` prefix, not
per-case reason wording. The 525 both-refuse rows are agreement by this rule.

## Notes on the differential's power

- Agreement is not evidence of conformance: the twin and oracle could share a blind spot. The
  differential found one ambiguous class; it did not establish that everything else is correct.
- The corpus covers the requested classes: multiple matching strong ETags (multi-strong, 117
  inputs); weak/strong mixes (strong and weak families); Last-Modified whitespace (lm-whitespace,
  108); `received` ties (weak-tie-corresponding, LC3 refusal; also weak-tie-off); Connection lists
  naming excluded and non-excluded fields and empty/duplicate/mixed-case members (update-*
  families); obs-text ETags and names; bool/float/huge-int `received` (refusal-received, plus
  10^40 and 2^70 values in scenarios); every refusal kind enumerated in the contract (refusal-*).
- Refusal counts: 525 both-refuse rows span 18 refusal kinds.

Verdict line: TWIN inputs=2400 disagreements=30 oracle-defects=0 ambiguities=30
