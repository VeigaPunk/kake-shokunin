# ExecTwinFresh — round 100: C2 contract v2 held-out disagreements

Differential: twin `twin.py` (written from contract v2 only) vs frozen
`frozen/pos-oracle.py` as a black box (`python3 -I -B`, stdin bytes).
Corpus: 3600 own inputs (seed 100226; see `gen_run.py`, `results.jsonl`).

Result: 3600 agree, 0 disagreements. There is no disagreement to decide;
no oracle defect, no twin defect, no contract ambiguity found.

## Counts per class

| Class | Count |
|---|---|
| inputs | 3600 |
| disagreements | 0 |
| identical rc=0 JSON | 2106 |
| identical rc=1 (empty stdout + `invalid_input:`) | 1494 |
| oracle defects | 0 |
| twin defects | 0 |
| contract ambiguities | 0 |

## Coverage notes (agreeing behaviour, not disagreements)

- Qualified Cache-Control (V2-1b): matched on token/quoted/empty-quoted
  forms, mixed case, extension names containing `no-cache`/`private`,
  quoted strings with commas and escapes, empty list elements, OWS
  around commas/ends — e.g. `no-cache="a,b"`, `No-Cache=""`,
  `private="a\\"` and malformed forms (`no-cache =x`, `no-cache=`,
  unterminated quotes, lone backslash, `;`, DEL/control/non-ASCII tokens).
  Both sides refuse exactly the same subset.
- Output trimming (V2-2), stored proxy-field drop (V2-3), stored
  `connection`/LC4/`content-length` keep (e1), malformed stored ETags
  refused regardless of selection (e2), LM SP+HTAB trim (e3), refusal
  stdout empty (e4), non-JSON/non-UTF-8 stdin refused without traceback
  (e5), `age` copied (e6), LM ties refuse (e7), both-refuse shape scored
  equal (reason text not compared).

## Quoted deciding sentences

None — zero disagreements, so no deciding sentence was needed for any case.
The agreement is symmetric: the twin implements V2-1/V2-2/V2-3 + e1-e7 as
written; the oracle matches it on this corpus.

Verdict:
TWIN inputs=3600 disagreements=0 oracle_defects=0 twin_defects=0 ambiguities=0
