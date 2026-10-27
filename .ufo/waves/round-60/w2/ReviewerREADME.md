# ReviewerREADME

ATTACKS: Checked the B1 `corpus/README.md` coverage map, frontier-ground map, and round-60 base-absence statements against the entry files, `SOURCES.md`, and base commit.

ROWS:
- Coverage rows 79–80 name the two B1 entries and their matching source IDs: `google-user-triggered-fetchers.md` → S428; `robots-txt-limits.md` → S429. The descriptions align with the entry subjects; no discrepancy found in the checked coverage claims.
- Frontier row 116 lists exactly the two entry paths and S428/S429. The B1 `SOURCES.md` rows’ `used-by` fields list those paths; S428 also lists `googlebot-verification.md`, which is not a frontier entry claimed by this row. This matches the map’s stated scope.
- Round-60 base-absence statement at line 138 is accurate for the two entry paths and source rows S428/S429: `git cat-file -e 97cdc...:corpus/knowledge/google-user-triggered-fetchers.md` and `...:corpus/knowledge/robots-txt-limits.md` each exit 128 (“path ... exists on disk, but not in ...”); B1 includes the files and rows.

FINDINGS:

| severity | target file:line | issue | evidence command | fix |
|---|---|---|---|---|
| — | — | No actionable finding in assigned README scope. | `git diff 97cdc122379711c2b02a8970752c8782da3ac81d 8b33fd248d126b48d838af5c38bc175850f41a09 -- corpus/README.md`; base `git cat-file -e` checks for both entry paths | — |

VERDICT: Assigned README claims checked; no falsifying discrepancy found.
