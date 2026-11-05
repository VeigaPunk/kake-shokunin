# ReviewC2 — scoped findings (C2 independent conformance review)

VERDICT: C2 instrument conforms — 93/97 agreement, 0 tool defects; all 4 disagreements resolve to three contract ambiguities (A2/A3/A4), each flagged before the run. Full deliverable: `.ufo/waves/round-92/w1/ReviewC2/{cases.json,agreement.txt,runs.jsonl,Review.md,run_cases.py}`.

Scope and independence: contract `c2-contract.md` (sha256 `5fc49c7a…f14c944`) read alone; `c92_heuristic.py` and its
hand cases NOT read; counter NOT executed. Candidate `scripts/heuristic_freshness.py` measured at sha256
`7bfe82da8e1a1d541930ef1b4ee64cfe9b3fa5b8169680795bcc8626d2f37f5c` (22985 B, landed 21:40:47 -03:00, stable through 21:41:22).
Command per case: `python3 -B scripts/heuristic_freshness.py` with the case JSON on stdin (one process per case), run from LANE.

## Findings

- **F1 — no tool defect (97/97 protocol-clean).** Every success row exited 0 with empty stderr and exactly the three
  keys `decision`/`lifetime`/`heuristic`; every refusal row exited 1 with empty stdout and an `invalid_input:` stderr.
  18 distinct reason strings, none pinned by the contract (free-form by design) — recorded as protocol debt, not a defect.
- **F2 — ambiguity A2 (clause 4, name/argument split), case D44.** `Cache-Control: max-age = 60` + `Last-Modified`:
  candidate `explicit 60` (name re-trimmed after the `=` split), reviewer `heuristic 10` (clause 4 trims only the whole
  directive, so the name is `"max-age "` — unknown → ignored). Disagreed; both readings defensible.
- **F3 — ambiguity A3 (clause 4, "bare"), case R31.** `s-maxage= 60` shared: candidate `explicit 60` (argument trimmed
  before the bare-digits check), reviewer refusal (`" 60"` is not a bare non-negative decimal integer). Disagreed.
- **F4 — ambiguity A4 (clauses 5/6/7, integer grammar), cases D48/D49.** `Expires: -10` and `Date: -100`: candidate
  refuses ("not a decimal integer"), reviewer accepts (clauses 5–7 omit clause 4's "non-negative", and clause 6 says
  Expires "may precede Date"; negative lifetime is expressly allowed in clause 10). Disagreed. Candidate grammar is
  unsigned digits with leading zeros accepted (D57 agrees).
- **F5 — contract debt list (13 entries), in `Review.md`.** A1 s-maxage-when-not-shared vs clause 11's gate; A2 name trim;
  A3 bare; A4 integer grammar; A5 requiredness inside `stored`; A6 float-vs-int; A7 Vary member parsing; A8 presence with
  argument (`private="…"`, D41 — candidate agrees with name-presence); A9 duplicate-argument equality; A10 empty
  Cache-Control value; A11 roleless-but-known directives (`no-cache`); A12 trim-before-parse; A13 quoted-string grammar.
  A1/A5–A13 produced **no** disagreements (candidate and reviewer read them the same way), but the text alone does not
  force that agreement — a second implementer can diverge.

## Coverage

97 hand-computed cases (40 refusal / 57 decision): every clause 1–13 plus Input, every vocabulary member
(explicit 20 / heuristic 17 / not-heuristically-cacheable 5 / heuristic-undecided 7 / not-storable 8), cap boundary
(D35–D37, D51), floor boundary (D32/D33/D38/D46), LM==Date (D32), LM>Date (D39), s-maxage shared vs not
(D02/D03/D04/D10/D43/D47/D53), Expires before Date (D07/D08), private shared vs not (D18/D19/D41), Vary star vs
members (D20–D23/D45/D55), duplicate header name case-only (R32/R34), signed delta-seconds (R26/R27/R30),
empty directive (R20–R23), malformed-field-despite-not-storable (R33/R34/R35).

## Residual risk

Candidate bytes may still be iterated by its author seat — re-pin the digest before scoring. Whether the frozen
counter's 28 hand cases pin the reviewer's or the candidate's side of A2/A3/A4 is unknowable from this seat (counter
unread by design); if they pin the reviewer's side, the counter will diverge from the candidate on exactly these four
inputs and the fix belongs in the contract, not the candidate. Generated population, forgeries and the sandbox are the
counter's conjuncts and were not exercised here. No installs, no network GETs, no LANE git mutations; scratch root
deleted empty.
