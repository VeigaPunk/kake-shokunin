# ScoutCensusB1

ATTACKS:
- B1 SOURCES census and validation on a detached scratch clone at `8b33fd248d126b48d838af5c38bc175850f41a09`.
- Compared census-validator W04 output with frozen `controls/census-before.txt` (14 W04 warnings; contract's 164-row baseline).
- Inspected the maintained census parser to establish what its output measures. The requested `corpus/CORPUS.md` file is absent from the lane at B1; the repo's applicable corpus documentation is `corpus/README.md`.

CENSUS:

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --file <scratch>/repo/corpus/SOURCES.md`

Observed output:
```
file rows 167
file tier.A 144
file tier.B 6
file tier.C 17
file status.mined 137
file status.queued 8
file status.rejected 22
FLEET rows 167
FLEET tier.A 144
FLEET tier.B 6
FLEET tier.C 17
FLEET tier.invalid 0
FLEET status.queued 8
FLEET status.mined 137
FLEET status.rejected 22
FLEET status.invalid 0
FLEET missing 0
```

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <scratch>/repo/corpus/SOURCES.md`

Observed: exit 0, `ok` line, and 15 W04 rows. First 14 IDs match the frozen census-before warnings; extra W04 is S427, same overview URL across a new scope. Thus the round's expected 164→167 row change and 14→15 W04 change are observed; no validator errors were emitted.

DIFF:

- `git show B1:.ufo/waves/round-60/controls/census-before.txt` confirms 14 W04 warnings and final `kake ok` line.
- At B1 `wc -l` on committed `corpus/SOURCES.md` is 282 (physical lines, not row count). The maintained script reports 167 logical rows (not 164).
- The contract's cited baseline `controls/census-before.txt` is the pre-round 164-row census; it is not an after-state expected-equality file. The observed additional W04 is S427, corroborated by validator output.
- Inspection of `scripts/sources-census.sh` shows census rows are parsed from the registry, while validation checks malformed NF, IDs, duplicate IDs, enums, dates, URL/scope duplicate rules and used-by existence. Its validate exit status treats W warnings as non-fatal; the `ok` line means no E-class finding, not no warnings.

FINDINGS:

| severity | target file:line | issue | evidence command | fix |
|---|---|---|---|---|
| low | `corpus/SOURCES.md` (S427 row) | Census validation now reports one additional W04 warning, not present in the frozen 14-warning pre-round file. This is consistent with the newly added same-URL re-open, so not evidence of malformed data; ensure the round report explicitly accounts for 15 after-state warnings rather than claiming unchanged W04. | `sources-census.sh validate --file <scratch>/repo/corpus/SOURCES.md` → `W04 S427 ... across scopes`; baseline `git show B1:.../census-before.txt` has only S033...S417 (14). | Record the expected S427 W04 as intentional in after-state comparison. |

VERDICT: Census is clean of validator errors at B1; row total is 167 and W04 rises from 14 to 15 due to S427. No high/medium census defect observed. Census formula request's `corpus/CORPUS.md` target does not exist at B1; no such file was inspected.