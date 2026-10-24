# ScribeQualityCriteria — round 37

- **Axis:** operability (assigned); round context also tracks freshness. This draft improves operability evidence discipline; freshness was not assessed.
- **Behavior:** drafted seven QUALITY criteria covering sandbox-only seat deliverables and L1 post-wave `jj-lane.sh state`; original-key rule of record; bounded coverage wording with listed ablations plus mutation pass; resolving cited hashes or naming bundles; polarity evidence; key-free control-tree proof; and bare-id-only citation rejection.
- **Artifact:** `/fast/scratch/hyaku/kake-r37w1/ScribeQualityCriteria/quality-r37.md` (17 lines), SHA-256 `464eadee4f0b678025fa85a1f30f1e84be6c23e22f021a6d824f10bc80d445ed`.
- **Report surface:** this file only; no lane product files or other lane paths written. No subagents, Git/JJ mutation, network access, or tools installed.

## Evidence and outcomes

- Read-only source review: `corpus/QUALITY.md:860-887`; `corpus/lessons/round-36-verifier-spotcheck.md:151-175`; `corpus/lessons/round-36.md:61-80,134-143`; `SCORECARD.md:1754-1938`; `.ufo/waves/round-37/ctl/MutRefPass.md:1-52`; `.ufo/waves/round-36/w2/ReviewCriteriaChecks.md:1-104`; `.ufo/waves/round-37/make_w1_spec.py:80-83`. Reads completed; these provide the routed lessons, round design, observed mutation result, and exact expected criterion-check coverage.
- `glob` for `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-37/criteria` returned “Path not found”; no corrected criterion-check implementation or receipt was available in the lane at drafting time. Accordingly, the draft labels new-check red-before status `no check yet`, except for the narrow historical full-hash receipt it explicitly describes.
- Hash/length commands (each exit 0): `timeout 30 sha256sum /fast/scratch/hyaku/kake-r37w1/ScribeQualityCriteria/quality-r37.md` → the SHA-256 above; `timeout 30 wc -l /fast/scratch/hyaku/kake-r37w1/ScribeQualityCriteria/quality-r37.md` → `17`.

## Gates and limits

- No build, test, lint, criterion script, C1 counter, or C2 counter was run. In particular, no access to or search/stat/list of `/fast/scratch/hyaku/kake-r37/`, no sealed-key inspection, and no C1 measurement.
- The round-37 `MutRefPass.md` reports 28/42 mutants meeting the predicate and the declaration describes 34 listed ablations; I recorded those as evidence pointers, not as an independent rerun or as proof of complete contract coverage.
- The report distinguishes historical old-check false passes from red-before receipts for proposed fixed checks; no unobserved check is described as executed.
