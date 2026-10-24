# S034 freshness recheck (round 26, C1)

```json
{"id":"S034","verdict":"HOLD","fetchIndex":1,"quote":"The names within an object SHOULD be unique.","anchorObserved":"RFC 8259 Section 4 (Objects), raw line 322; fetched/text/S034-1.txt is whitespace-collapsed onto line 1 (offset 8863), where the sentence still sits under the '4. Objects' heading","reason":"Live GET today returned 200 with body sha256 61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7, byte-identical to the digest recorded when the row was opened (corpus/lessons/round-24.md:33), so there is no drift to test. Header still reads December 2017 and 'Obsoletes: 7159' with no 'Obsoleted by'. All four cited sections exist (3 Values, 4 Objects, 6 Numbers, 9 Parsers); §4 keeps SHOULD uniqueness and calls non-unique behavior unpredictable, §6 keeps 'as Infinity and NaN) are not permitted', §3 keeps false/true/null as literal names distinct from number. Duplicate rejection stays local policy because §9 requires parsers to accept all grammar-conforming texts. Teaches, scope and anchor unchanged.","correction":null}
```

Caveats (≤10 lines):

1. Text view is collapsed to one 23,044-char line; section attribution comes from the retained gz (899 lines, 28,360 bytes), which preserves RFC pagination. The quote occurs exactly once in the text view (offset 8863).
2. This is byte equality, not merely same wording: `zcat S034-1.raw.gz | sha256sum` = 61a5378f…5cd2d7, the value recorded at row open (round-24.md:33). RFC 8259 is a fixed published document (no Last-Modified; ETag W/"effcde61d580b8bb9e8eb8fdca283c5f").
3. Freshness risk is availability only; manifest-retry.json has no S034 entry (first attempt 200, fetchedAt 2026-10-21T15:10:52Z).
4. Anchor nuance: §9's title is "Parsers". The row cites section numbers only, so it remains accurate; §9's MUST-accept sentence spans raw 543–544 but is contiguous in the text view.
5. Scope support for "boolean versus number types": §3 (raw 305–316) lists false/null/true as literal names separate from number, and §6's number grammar admits only decimal forms; both intact. §1 raw 154 names four primitive types but is not cited by the row.
6. "Explicit duplicate rejection is local receipt-integrity policy" still holds: §4 (raw 333–344) says non-unique names make receiver behavior unpredictable and implementations differ, while §9 (raw 544) requires parsers to accept all grammar-conforming texts; no RFC MUST mandates duplicate rejection.
7. Citing entry corpus/knowledge/static-canonical-preflight.md:159 cites "S034 (RFC8259 §3/4/6/9)"; section identities are unchanged, so no correction is needed there (knowledge-entry judgement is a separate seat).
8. No supersession marker in the fetched bytes: the header lists only "Obsoletes: 7159", and the errata discussion concerns predecessor RFCs 4627/7159.
9. No tool installs or upgrades were needed; nothing was written outside this report.
