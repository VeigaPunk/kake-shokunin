DEFECT: S129/S130 quote paragraph locators are wrong; the requested census, counts, sourced-claim, failure-proof and novelty checks hold.

Scope: CriticFrontier, r43-verify, freeze b49cba9ca7f15bb0dfaae33b638afa7cb4c793ee. This is a scoped conformance finding, not a round/claim admission verdict.
Axes: freshness (assigned); operability is collateral provenance only, not scored here.

## Checked statements
- Census — holds. `.ufo/waves/round-43/verification/freeze/census-after-r43.txt:1-13` is committed at the freeze; validation independently exits 0 with the same twelve W04 warnings and final `kake\tok` line. The receipt contains stdout, not a separate captured exit field.
- Registry 128 -> 130 — holds. The r42 tip registry and r43 base registry are byte-identical; the checker derives 128 rows at that tip. Frozen SOURCES equals the independently counted worktree: 130 rows, mined 101, queued 8, rejected 21. The freeze diff adds only S129/S130 (`corpus/SOURCES.md:137-138`), both mined; no existing registry row changes.
- Sourced claim — holds. `SCORECARD.md:3188-3190` explicitly attributes the freeze/control method to S129; `:3277-3278` explicitly binds that method to C1. The citation is in the round introduction, rather than repeated inside the C1 subsection.
- Mistake 7 able-to-fail fix — holds. `corpus/lessons/round-43.md:27-36` records class/evidence/captured-by/fix. The identical checker and revision pair reject r42's stated counts (exit 1; seven specific mismatches) and accept the corrected counts (exit 0). Both claims files and observed outputs are committed under `verification/freeze/registry-count-r4{2,3}-{claims.json,check.txt}`. This demonstrates the named arithmetic correction, not universal checker soundness.
- Opened-this-round novelty — holds on the specified documentary test. IDs, exact source paths and source titles have no match in the r43 base tree or its prior committed history. The freeze adds the two rows; `corpus/lessons/round-43.md:12-23` records opening them on 2026-10-23. This does not independently reconstruct the author's actual read event.
- Located quotes — wrong. `corpus/lessons/round-43.md:16` says S129's quote is in Verdict paragraph 2; it is in paragraph 1, at `tameshi-shokunin/.ufo/waves/round-33/w1/CtlDoNothing.md:9-11`. `corpus/SOURCES.md:137` instead anchors paragraphs 2-4, which exclude that paragraph. S130's quote is likewise in paragraph 1 (`kama-shokunin/corpus/knowledge/self-assessment-at-writing.md:7`), not paragraph 2 as `round-43.md:17` and `SOURCES.md:138` say. Both quotations themselves hold after whitespace normalization.
- S129 provenance qualification — the source explicitly says its scoring numbers came from amended counter 27902a16, while the original f6d8a89 invocation exited 2 without scoring (`CtlDoNothing.md:9-17`). It supports the pre-data method, not a claim that the original frozen counter produced those numbers.

## Counterexample and smallest safe correction
Opening the named paragraph 2 does not yield either quoted sentence. This is a fixable quote-location defect under CORPUS.md's located-quote rule, not evidence of a freshness tradeoff or a failed C1 predicate. Append a locator erratum giving the exact source lines/revisions and preserving the amended-counter qualification. If correcting immutable SOURCES anchor cells, use superseding rows rather than rewriting the frozen rows. No integration performed here.

## Commands and observed exits
Working directory for lane commands: `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Notation: F=b49cba9ca7f15bb0dfaae33b638afa7cb4c793ee; B=61046fcffa23898cd93b7a5a0af4906dac9926c9; T=5949e66ffe803859372adc975dd7392f0f07d626; V=.ufo/waves/round-43/verification/freeze.
Prefix P expands to `timeout 30 prlimit --as=8000000000 --`; H expands to `timeout 60 prlimit --as=8000000000 --`.
- `$P git show --format=fuller --stat $F` -> 0; confirms checker, claims, receipts, lesson, knowledge entry and source additions in freeze.
- `$P git diff $B $F -- corpus/SOURCES.md` -> 0; exactly two added rows.
- `$P git diff --exit-code $T $B -- corpus/SOURCES.md` -> 0; identical pre-round registry.
- `$P bash /home/vgpnk/Projects/kimi-shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin --today 2026-10-23 kake` -> 0.
- `$P bash /home/vgpnk/Projects/kimi-shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin --today 2026-10-23 kake` -> 0; rows 130, mined 101, queued 8, rejected 21, invalid/missing 0.
- `$P python3 -B .ufo/waves/round-43/registry_count_check.py --root . --claims $V/registry-count-r42-claims.json` -> 1; base 119/92/8/19, tip 128/99/8/21 (rows/mined/queued/rejected).
- `$P python3 -B .ufo/waves/round-43/registry_count_check.py --root . --claims $V/registry-count-r43-claims.json` -> 0; same derived counts, no mismatches.
- Pattern Q=`S129|S130|self-assessment-at-writing|round-33/w1/(CtlDoNothing|ReviewFreeze)|Verification-fixture controls and freeze conformance|Checking self-assessment statements at writing`.
- `$P git grep -n -E "$Q" $B -- . ':!scripts'` -> 1, no matches; `$H git log --format='%h %s' -G "$Q" $B -- . ':!scripts'` -> 0, no output.
- `$P git show $F:corpus/SOURCES.md | sha256sum` -> 0; digest below equals worktree. `$P git show $F:.ufo/waves/round-43/registry_count_check.py | sha256sum` -> 0; digest below equals executed checker.
- `$P git show $F:corpus/lessons/round-43.md` -> 0; contains the incorrect paragraph locators and Mistake 7.
- `$P git diff --exit-code $F -- SCORECARD.md corpus/SOURCES.md corpus/lessons/round-43.md corpus/knowledge/claim-count-derivation.md .ufo/waves/round-43/registry_count_check.py $V/census-after-r43.txt $V/registry-count-r42-claims.json $V/registry-count-r43-claims.json $V/registry-count-r42-check.txt $V/registry-count-r43-check.txt` -> 0; inspected/executed lane inputs match freeze.
- In tameshi repo: `$P git log -1 --format='%H %s' -- .ufo/waves/round-33/w1/CtlDoNothing.md` -> 0, 61401c28cee2b3cdd05a0501260586a4cbfcafed; `$P git diff --exit-code 61401c28cee2b3cdd05a0501260586a4cbfcafed -- .ufo/waves/round-33/w1/CtlDoNothing.md` -> 0.
- In kama repo: `$P git log -1 --format='%H %s' -- corpus/knowledge/self-assessment-at-writing.md` -> 0, 6de225c289b7682bf280cffb4a07de3fb7d1275c; `$P git diff --exit-code 6de225c289b7682bf280cffb4a07de3fb7d1275c -- corpus/knowledge/self-assessment-at-writing.md` -> 0.

## SHA256 / bounds
- Executed checker `.ufo/waves/round-43/registry_count_check.py`: 35ca6d40f91215ab59b79ee9ccbf6e920bfc4067c3caf87173a86a6a87c535db.
- Census tool `/home/vgpnk/Projects/kimi-shokunin/scripts/sources-census.sh`: 3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30.
- Frozen `corpus/SOURCES.md`: 9ec92ad6ff29ae4890f7a40955ccf78b31f9724b6c41af0eeefe56693cc7cf2f.
- Census receipt: 2d3ed752fe26ec6ddeac06eff6bd31c437a4b9cc7ccc1784cb1239714e48352e.
- Red/green checker receipts: f50248f309d9481132803717afbdb75ac28174ed721576efdff2281e5972037a / 9fbbae7348f9958db88fe33cc94d1a6da07d063b24f6dc112126766df3044e36.
No installs/upgrades, network requests, subagents, judge invocation or lane changes beyond this report. All started commands completed; no outstanding process trees.
