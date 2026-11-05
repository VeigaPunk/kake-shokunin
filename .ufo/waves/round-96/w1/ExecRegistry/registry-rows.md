# Round-96 gate-registry draft rows (ExecRegistry, append-only diff against SKILL.md line 218)
# Apply: insert the two `+` lines after SKILL.md line 218 (the c95_conditional.py row). No existing line modified.
--- a/SKILL.md
+++ b/SKILL.md
@@ -218,1 +218,3 @@
 | c95_conditional.py | gate (round-95 C2 conditional request evaluation, contract v2 clauses C1-C5; population-pinned; mutant kill target 40/40) | `python3 -B .ufo/waves/round-95/c95_conditional.py --root . --revision <REV> --work <scratch>` | `0=met=true` (candidate=present, population=ok, anti_table=ok, hand 66/66, generated 120/120, forgeries_refused 7/7, positive=admitted, mutants 40/40); `1=met=false` (any disagreement, admitted forgery, population drift); `2=could-not-evaluate or usage` | `python3 -B .ufo/waves/round-95/c95_conditional.py --selftest` (isolated fixture battery; drifted-reference check) | `.ufo/waves/round-95/c2-contract-v2.md`; `.ufo/waves/round-95/frozen/c2-population.sha256`; `.ufo/waves/round-95/frozen/pos-good-v2.py`; `.ufo/waves/round-95/frozen/c2-equiv-receipts.json` | reads committed bytes at `--revision`; scratch under `--work`; no lane writes | kake |
+| c96_selfassess.py | gate (round-96 C1 strict self-assessment conformance, successor to c95_selfassess.py; battery-covered) | `python3 -B .ufo/waves/round-96/c96_selfassess.py --root . --revision <REV> --work <scratch>` | `0=met=true` (E1-E5=0, `pins=ok`, `battery=23/23`, `admit=5/5`, `shadow=absent`, `predecessor_admits>=4`, `ng_pred_admits=3/3`, `self_pin=ok`); `1=met=false`; `2=self-pin mismatch or could-not-evaluate`; `--verdict-only` prints `met=n/a` with `verdict=clean` or `verdict=failed` and never `met=true` | `python3 -B .ufo/waves/round-96/c96_selfassess.py --selftest` (plants one defect per strict class; asserts each named finding) | `.ufo/waves/round-96/freeze.md`; `.ufo/waves/round-96/frozen/c1-surfaces.json` (presence-pinned, digest `c1caa585…`) | reads committed bytes at `--revision`; scratch under `--work`; no lane writes | kake |
+| c96_reval.py | gate (round-96 C2 revalidation exchange, contract v1; population-pinned; mutant kill target 14/14) | `python3 -B .ufo/waves/round-96/c96_reval.py --root . --revision <REV> --work <scratch>` | `0=met=true` (candidate=present, population=ok, anti_table=ok, hand 37/37, generated 120/120, forgeries_refused 6/6, positive=admitted, mutants 14/14); `1=met=false` (any disagreement, admitted forgery, population drift); `2=could-not-evaluate or usage` | `python3 -B .ufo/waves/round-96/c96_reval.py --selftest` (isolated fixture battery) | `.ufo/waves/round-96/reval-contract-v1.md`; `.ufo/waves/round-96/frozen/c2-population.sha256` (digest `d9c8f96e…`); `.ufo/waves/round-96/frozen/pos-good-reval.py`; `.ufo/waves/round-96/frozen/mutants-reval.json` | reads committed bytes at `--revision`; scratch under `--work`; no lane writes | kake |
 
## Resolution receipts

See `resolution-receipts.txt` (same directory): sha256 digests match the frozen
`controls/instrument-sha256.txt` for both counters, the c1-surfaces.json
(`c1caa585…`) and c2-population.sha256 (`d9c8f96e…`) digests, the contract,
pos-good and mutants files; `git cat-file -e HEAD:<path>` OK for every path
named in the two rows at HEAD=`049e8eca2f0fa5e981232eb4efe367357dce578c`;
both counters parse (`--help` rc=0). Candidate-note: `scripts/reval_exchange.py`
is not named as a row path (the verdict map says `candidate=present`); at the
freeze tip it is ABSENT from HEAD per the base control `controls/base-c2.txt`
(`candidate=absent … met=false`) — expected before the C2 author lands it.

EXEC-REGISTRY rows=2 resolved=8/8
