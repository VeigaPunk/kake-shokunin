# Knowledge09 — ghp-served-set.md provenance audit (round 21, w1)

## Behavior
Target: `corpus/knowledge/ghp-served-set.md`. The provenance trio already opens the file, so the target was left **unchanged** (no edits, no prefix added). Only field truth was audited. Read the entire entry (80 lines, 4843 bytes).

## Exact prefix
- Existing prefix = lines 1–4: `source:`, `verified-at:`, `recheck:`, and a blank line 4.
- Measured: 504 bytes for lines 1–4 (blank line 4 confirmed). File total 4843 bytes / 80 lines.
- No new bytes were written; no pre-existing byte was altered.

## Field audit

| Field | Result | Evidence |
|---|---|---|
| `source:` | IDs resolve; body cites S001, S002, S003, S004, S006, S008, all of which appear in the source field. S005/S007 are registered but not cited by this entry and are correctly absent. The URL pins `7b1f4a7…` with `§Archive artifact`, matching SOURCES.md S001. | `corpus/SOURCES.md` rows S001–S008 |
| `verified-at:` | Date `2026-10-19` is the original evidence date (SOURCES `fetched 2026-10-19`; body “quotes reopened 2026-10-19”). It is not today's date (2026-10-20), so it does not claim a domain recheck. Revisions `7b1f4a7` and `5f327015` match SOURCES S001. **Gap:** the field does not say `historical-not-live-reverified`, which the contract requires. A reader cannot tell from the field that nothing was live-rechecked. |
| `recheck:` | Concrete command present, but it is a **network** command (`curl` to `raw.githubusercontent.com`), not a local reading command. It loops over `v3.0.1 v4.0.0 main`; `main` is a moving ref, which conflicts with the pinned `verified-at` basis. No local copy of upstream `action.yml` exists in the workspace (glob `**/action.yml` found none), so no local command is possible from this repo. The source has not vanished (pinned URL still referenced), so the restore-or-retire clause is not triggered. |

## Other checks
- Preserved: round-20 S008 version erratum (GNU tar “1.35” withdrawn; cite commit `cfdb891`), named debt for ds4cc/plazir, and the dotfile/`CNAME` predictions flagged as unprobed. None were altered.
- `S019` metadata contract: **not registered.** `corpus/SOURCES.md` stops at S018 and `corpus/CORPUS.md` does not exist (corpus top-level holds only QUALITY.md, README.md, SOURCES.md). The entry does not cite S019, so nothing in the target depends on it. L1 must register CORPUS.md/S019 before any prefix-writing seat can reference it.
- Body rechecks (2026-10-19 counts `v3.0.1 0`, `v4.0.0 3`, `main 3`) are historical; not reverified here.
- Field-count coverage is L1's job; not counted.

## Findings for L1 / operator
1. Add `historical-not-live-reverified` wording to `verified-at:` (requires a target edit by the owner of this entry; not done here because the trio is present).
2. Decide whether `recheck:` should move to a local clone at pinned `7b1f4a7` (`git -C <clone> show 7b1f4a7…:action.yml | grep -cF -- '.[^/]*'`) or stay a remote recheck; `main` in the loop is unpinned.
3. Register S019 / CORPUS.md before referencing the metadata contract.

## Out of scope / not done
- No target edits. No rechecks or network reads run. No credential or auth files touched. No subagent dispatch (leaf).
- No tools installed or updated.
- No commits.
