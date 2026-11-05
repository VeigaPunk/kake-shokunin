# Conditional request evaluation — contract v2 (round 95)

Frozen with the round-95 instruments before any candidate scoring. The contract
document decides the clauses the round-93/94 routed defects left undecided; each
clause names its grounding (RFC-exact, citing the opened row, or lane
convention).

- C1 (RFC 9110 sections 5.6.1.2 and 5.6.3, row S478): the list syntax
  `#element => [ element ] *( OWS "," OWS [ element ] )` admits empty elements
  and a recipient MUST accept such lists; empty elements contribute no members.
  Decision: empty list members are accepted and ignored. A list of only empty
  members decides as the empty list (matches nothing). A whitespace-only field
  value is not a list and stays refused. `*` mixed with tags stays refused.
- C2 (RFC 9110 section 8.8.3 `etagc`, row S455): an opaque-tag may carry
  obs-text (0x80-0xFF). Decision: obs-text is accepted inside opaque-tags; other
  control characters stay refused. (S455 was opened in an earlier round; the
  round-95 re-read is recorded in the round-95 lesson `## Gate`.)
- C3 (lane convention, extending rows S471/S476): `"role": null` is accepted and
  means the same as omitting the key (origin). The key remains optional.
- C4 (RFC 8259 leaves duplicate-member semantics undefined; row S034): an input
  document whose raw bytes contain duplicate object keys is refused
  (`invalid_input:`) before any decision, rather than silently last-wins.
- C5 (RFC 9110 section 13.1.2 and section 13.1.3/13.1.4 ignore rules, rows
  S473/S474): the GET/HEAD method filter edges are pinned by case —
  If-None-Match under OPTIONS (not GET/HEAD) yields 412 on a match;
  If-Modified-Since under OPTIONS is ignored.

Equivalence rule (R94-4): before this freeze the 40-mutant population of
`.ufo/waves/round-93/w1/recovered-partial/MutConditional/mutants-posgood.json`
was scored against the v2 reference (run 2026-11-05, build log
`.ufo/waves/round-95/controls/mutant-scan-v2.txt`): 40/40 killed, zero
survivors, so the kill target is 40/40 and no equivalence receipt is required by
`frozen/c2-equiv-receipts.json` (empty list). The declared rule stands for any
future re-score: a survivor keeps `met` true only while a digest-pinned receipt
covers it. M11, the round-94 survivor, is killed here by the v2 empty-member
cases; its round-94 equivalence receipt
(`.ufo/waves/round-94/w1/ExecC2Mutants/receipts/equiv_m11.py`) remains the
historical proof that the round-94 39/40 reading was correct.
