# CriticPredicate — r42-controls

Axes: **operability** (changed executable/cost surface); **freshness** (owned, not demonstrated changed here).
Scope: read-only review of the candidate, counter source, four existing pre receipts and retained manifest. No code, counter, shell command or other runtime was invoked; no command exit codes observed. No tools installed. Only this report was written.

## Statements

- **HOLDS — axis naming.** SCORECARD.md:2922-2927 names the runnable cost of `scripts/sitemap_audit.py`, not a new coverage/depth result. This is operability under fleet AXES.md:13, consistent with round prompt §6.9:361-365.
- **HOLDS — textual predicate identity.** SCORECARD.md:2932, `c42_count.py:52-54` and `verification/pre/{donothing-tip-42001,donothing-tip-42002,base40-42001,absent-42001}.json:2` contain the same sentence. `c42_count.py:571,586-590,604` requires initial equality, all five timing repetitions equal, and five passing ratios. It does not accept timing alone.
- **WRONG — exact numeric condition is identical to that sentence.** `c42_count.py:584` rounds samples to four decimals; :594 rounds the ratio to three; :603 tests that rounded ratio. Algebraic counterexample, not executed: five base samples of 0.5000 s and candidate samples of 1.0002 s produce 2.0004, stored as 2.000, hence accepted although greater than 2.0. Smallest correction: compare unrounded measured medians before presentation rounding.
- **HOLDS, bounded — current do-nothing is below target.** Both unchanged-tip receipts have equality 8/8 but fail T1, T2 and T5. The absent-tool receipt is 0/8. These receipts do not establish that every shortcut fails.
- **HOLDS — a cheap old tool already meets the CPU budget alone; WRONG if described as meeting C1.** Round-40 `base40-42001.json:14,157-162` has all five ratios below 2.0 but equality only 3/8. The conjunctive predicate rejects it. Thus 2.0 is not independently evidence of preserved URL work.
- **OVERSTATED — “keeps every judgment” (`SCORECARD.md:2923`).** The counter enumerates only finite CLI runs, not the domain of `_parse_url`. Its actual predicate is narrower (“on every generated run”). Prompt §6.9:346-347 forbids the universal unless the counter enumerates its full set.
- **OVERSTATED — support coverage under QUALITY (u).** `make_url` chooses only `http`, `https`, `HTTP`, `Https` (:141); B and long-value generators choose lowercase only (:226,:255). Also, userinfo insertion occurs only in `first`, before the optional password suffix (:144-147), not at every position of that component. Random insertion with endpoint support is not enumeration of every position in one receipt. These are limits, not proof of full URL equivalence.
- **WRONG — random file/id names carry no case identity for every run.** `c42_count.py:391-407` copies T4 verbatim and returns `manifest.json`. Retained `round-41/realrun/manifest.json:5-7,10-12` exposes `rfc-editor`, `mdn` and named sitemap paths; :20-32 exposes the other identities. Equality uses the same sandbox, but random mount names do not erase these labels. This violates QUALITY (r) and the unqualified claim at SCORECARD.md:2948-2949 / counter docstring:38. Smallest correction: relocate/rename T4 files and ids inside its generated case, updating manifest references before both oracle and candidate runs, or disclose a deliberate criterion exception before freezing.
- **HOLDS — behavior-based control definition, not construction-based exclusion.** SCORECARD.md:2959-2971 requires a differing judgment witness or demonstrated measurement manipulation, and explicitly excludes fully equivalent implementations. Apply that requirement even to listed regex-mutant constructions; absence of a supplied witness is not a proof of equivalence. This avoids rejecting an honest full implementation merely for being cheap (QUALITY (n)).
- **HOLDS — candidate is explicitly pre-freeze, not validated already.** SCORECARD.md:2912-2913,2988-2991 leaves non-author scoring/receipt commitment ahead of declaration. The inspected pre receipts are identified as L1 receipts (:2951); they do not discharge QUALITY (o). Commit live non-author results with the same counter bytes before declaring. Commitment/timeline was not audited here.

## Strongest closure attack

Static witness candidate: `hTtP://a.test/`. The round-41 source permits alphabetic scheme spelling and normalizes it (`/fast/scratch/hyaku/kake-r42/shared/tip41.py:78,95-108`). No generated scheme has that spelling; a read-only exact search of retained T4 found no `hTtP://` occurrence.
[INFERENCE] A sufficiently fast equivalent implementation can be weakened to reject that spelling without the equality samples noticing; its witness then makes it a control under the candidate's own rule. CPU margin and an actual meeting receipt are **unrun**, so this is not a scored surviving control and does not activate the kill rule by itself. A second omitted-support witness candidate is `http://user:pass|word@example.test/`: the generated userinfo defect is never placed in that password suffix.
Smallest safe correction: before freeze, make the claim explicitly finite-run parity rather than universal preservation, retaining the original wording as history; if universal preservation is essential, use the permitted exploratory route rather than claiming this enumeration proves it. Separately repair numeric comparison and T4 identity exposure, then collect fresh receipts under the declared redesigned bytes. These are fixable pre-freeze defects; no admission, score or round verdict is issued here.
The 2.0 bound is a chosen budget, not proof that every shape speeds up versus round 41: e.g. unchanged T4 is 1.222/1.287, yet a candidate near 2.0 would still pass this cost clause. Do not extrapolate a no-regression claim from it.

## Inspected receipts and provenance

All paths below are under `.ufo/waves/round-42/`; results are existing receipt data, not runs by this seat. Their process exits are not recorded in these JSONs; code :612 would return 1 for `met:false`.
- `verification/pre/donothing-tip-42001.json`: equalRuns 8/8; ratios T1–T5 `[5.367,2.811,1.51,1.222,8.87]`; met false.
- `verification/pre/donothing-tip-42002.json`: equalRuns 8/8; ratios `[5.35,2.732,1.334,1.287,9.354]`; met false.
- `verification/pre/base40-42001.json`: equalRuns 3/8; ratios `[0.968,1.015,1.004,0.999,1.054]`; met false.
- `verification/pre/absent-42001.json`: tool `/nonexistent`; equalRuns 0/8; all five ratios null; met false.
Recorded SHA256 pins (not recomputed):
- Counter `c42_count.py`: `7bfc32c5e76dca942208934cfbe89f166eda2776b40e69de987706b4d97dd2a6`.
- Round-41 `scripts/sitemap_audit.py` at `1ef7a0e95f6884dd113fe583a997c633fe330ddd`, shared copy `/fast/scratch/hyaku/kake-r42/shared/tip41.py`: `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d`.
- Round-40 `scripts/sitemap_audit.py` at `8eb121c81ffebada064eefcabcd94dd2303d646f`, shared copy `/fast/scratch/hyaku/kake-r42/shared/base40.py`: `4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e`.
Checks performed: ranged source/receipt reads and `grep(pattern="hTtP://", path=".ufo/waves/round-41/realrun", case=true)` → “No matches found.” No tests or new control scores are claimed; no processes were started.
