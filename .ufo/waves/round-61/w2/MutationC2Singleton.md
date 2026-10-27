# MutationC2Singleton

Mutant: changed `lowered = [name.lower() for name, _ in headers]` to `lowered = [name.strip(" \t").lower() for name, _ in headers]` in `scripts/header_audit.py`. This makes OWS-padded recorded field names participate in expectation and singleton matching despite remaining invalid under the separate raw-name syntax check. For example, `Content-Type ` with `content_type_present=true` no longer yields the expected missing-field finding, although it still yields `field_name_syntax`. This is a plausible defect on the whitespace/name-boundary axis.

Detector: `python3 -B .ufo/waves/round-61/c61_header_cases.py --root <scratch lane> --revision HEAD --tool <scratch lane>/scripts/header_audit.py --seed 61 --json`.

Observed results:
- Pristine run (seed 1019478096): H1–H18 each passed; `cases_passed=18`. Overall `met=false`, exit 1 because R3 failed with `ambiguous manifests` (capture manifest plus w1 fixture manifests). Thus the full detector baseline is inconclusive, not a killed-mutant baseline.
- Mutated run (seed 61): H1–H18 each passed; `cases_passed=18`. Overall `met=false`, exit 1 for the same R3 ambiguous-manifest failure. The mutation survived all H fixtures; H9 and H10 both passed.
- H9 exercises duplicate Content-Type with uppercase declared name `CONTENT-TYPE`, plus another duplicate singleton and single-occurrence clean case. H10 exercises repeated Set-Cookie both listed and unlisted. H17 covers whitespace in values, not whitespace in field names. The fixtures do not check an OWS-padded field name against a presence/singleton expectation.

Axis observations from these fixtures/code: mixed-case recorded singleton names are normalized with `.lower()`; removing name normalization is expected to be killed by H9's uppercase declared name. Removing the Set-Cookie exemption is expected to be killed by H10. Repeated singleton-list declarations are not covered; the current loop can emit duplicate `singleton_fields` lines for duplicate declarations, and a deduplicating mutation would therefore also be unobserved by H1–H18. Whitespace-only values do not affect name-count singleton logic; H17 does exercise surrounding OWS for values.

Restoration evidence: pristine SHA-256 before mutation `01abd8d4ff628907713b4300adf26b5962924d85132d1f330a33b70110c1d1d4`; restored scratch tool SHA-256 is identical.

VERDICT: SURVIVED H1–H18; overall detector inconclusive because R3 fails on ambiguous manifests in both pristine and mutated runs.