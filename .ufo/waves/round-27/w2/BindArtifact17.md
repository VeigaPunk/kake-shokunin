# BindArtifact17 — byte/locator binding attack on the S013 artifact record (freshness lane)

- Attacked item: `pairs.json` pair `row=S013, file=corpus/knowledge/ghp-served-set.md, kind=artifact, verdict=HOLD`,
  `evidence=.ufo/waves/round-26/w2/Rejection07S013.md`,
  `contains="It is true of the round but irrelevant to this entry. This is a provenance-precision nit, not staleness."`
- Frozen candidate: `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` (all source reads via this hash; working tree proven byte-identical to candidate blobs first).
- Lane scope: artifact identity / coordinates only. Semantic support of the HOLD is the separate reviewer's lane.
- Declared expectations (stated before running each probe): (E1) evidence file exists at the candidate and its bytes contain the `contains` string exactly once, byte-for-byte; (E2) the string sits in the record that actually adjudicates the ghp-served-set S013 reference, not another source's boilerplate; (E3) the historical date/base/retry/filename asserted inside the evidence report are independently reproducible; (E4) the pair is not self-citation (evidence path outside pairs.json/knowledge/population/statements) and the consumer counter admits it.

## Results

| # | Probe (command) | Expected | Observed | Status |
|---|---|---|---|---|
| 1 | `git hash-object` vs `git rev-parse ac46a74:<path>` for `Rejection07S013.md`, `ghp-served-set.md`, `pairs.json` | working tree == candidate blob | all three `same=YES` (blob `59fca3d1…`, `95bfdd1d…`, `fb87451a…`) | PASS |
| 2 | `sha256sum` of evidence blob content and of worktree file | equal | both `c31e10a4a523b4d661f7c26b7634f88429d0677407603bd35db4328f4c446fa1` | PASS |
| 3 | python: `contains.encode() in blob(evidence)` | True, exactly 1 | True, occurrences=1 at line 70 / offset 6103; substring sha256 `2e0e7246…`; 18 words | PASS (E1) |
| 4 | context read around offset 6103 | record that names ghp-served-set | "Low-severity adjacent observations" item 2 "Copied boilerplate provenance"; preceding sentence enumerates 5 files incl. `ghp-served-set` | PASS (E2), caveat D2 |
| 5 | `git ls-tree -r … | grep Rejection07` | single unambiguous target | only `.ufo/waves/round-26/w2/Rejection07S013.md` | PASS |
| 6 | line locator: `grep -n Rejection07S013` at candidate and at base `83528f7c` | line 95 in both | line 95 in both (base file = 95 lines; candidate adds 33 lines after) | PASS |
| 7 | header source list of `ghp-served-set.md` | no S013 source | `S001, S002, S003, S004, S006, S008` — S013 absent → "not a source teaching served-set semantics" holds | PASS |
| 8 | report contains the boilerplate it adjudicates | `S008 via \`manifest-retry.json\`` + retry row = S008 only | literal present; `manifest-retry.json` = 1 row `{row:S008, file:S008-1-retry.raw.gz}` | PASS |
| 9 | `git show -s --format=%cI %s cb807bc`; `merge-base --is-ancestor` | 2026-10-17 "kake: ignore interactive session logs"; ancestor of base | exactly that; ancestor of base and of candidate; `97404de` ancestor of candidate | PASS (E3) |
| 10 | window digests at `cb807bc` (report table) | `2e99136e79baae18` / `9207a3727db72e25` / `dc6105acfa2a4b1d` | identical 16-hex values recomputed | PASS |
| 11 | `gzip -dc S013-1.raw.gz | sha256sum; wc -c` | `492e22cf…`, 191341 | exactly `492e22cf133333d6202bbfd6c47370eac981612d7952b1e851d31e06dd78920b`, 191341 | PASS |
| 12 | `git grep -c -F 'S008 via \`manifest-retry.json\`' e28312b -- corpus/knowledge` | 5 files incl. ghp-served-set | 5 files, ghp-served-set present | PASS |
| 13 | consumer: `python3 -B .ufo/waves/round-27/count_c1.py --root . --revision ac46a74…` | 58 cited / 58 reviewed / 55 decided; S013 row valid; 3 carried-UNVERIFIABLE findings; exit 1 | `citingPairs 58, reviewedPairs 58, decided 55, missing 3, findings 3`; S013 outcome `{verdict:HOLD, valid:true}`; missing = (S001,ghp-served-set,3u),(S007,ghp-custom-domain,1u),(S033,static-canonical-preflight,3u) = 7 units; exit 1 | PASS (E4) |
| 14 | self-citation check | evidence path outside `corpus/knowledge/`, r27 wave, population/statements | `.ufo/waves/round-26/w2/…` — passes the gate's `artifact_self_support` rule; `contains` is absent from the citing file and from pairs.json-as-evidence | PASS |

## Discrepancies (none blocking)

- **D1 (low, in the evidence artifact's own arithmetic).** `Rejection07S013.md` asserts the S013 source quote sits at `@9094` in `fetched/text/S013-1.txt`. Measured offset of that sentence is **9016**; 9094 is the offset of the trailing fragment "descendants of the parent directory". The text file is byte-identical at `e28312b`, base and candidate (`sha256 e2608c34…`, len 19216), so the number was already off when written. Ordering conclusion (`8213 < 8886 < 9016`) is unchanged → no effect on this pair's binding or verdict; a stale coordinate in an evidence report, not on the S013 row itself.
- **D2 (low, locator precision).** The bound sentence's deictic "this entry" refers to `crawl-scope-per-host.md` (the report's own target), not `ghp-served-set.md`. Applicability to ghp-served-set rests on the *preceding* enumeration sentence (verified to name ghp-served-set). The substring alone is therefore not file-specific; a file-anchored locator (e.g. including `ghp-served-set, static-canonical-preflight). It is true of the round…`) would bind unambiguously. Not a mis-binding to another source's boilerplate.
- **D3 (low, reason completeness).** The pair's reason scopes the occurrence to "embedded evidence-report filename at old line95". The candidate's own r27 append adds two further S013 tokens in new prose (lines 111 and 115; "S013 occurs inside the evidence-report filename at line95, not as a served-set source"). Same `(row,file)` key → no extra obligation, and the file's own lines 111–116 state the scope; the ledger reason simply does not restate it.
- **D4 (historical ordering, informational).** The citing line 95 was committed in `b44daed` (2026-10-21T14:49:11-03:00) while the cited report landed in `a2be0dc` (14:52:48). The citation preceded its target's landing by ~3 minutes; both exist with identical bytes at declarations `be375d9`, base `83528f7c` and candidate (`59fca3d1…`), so the artifact binding resolves at the measured revision and is not circular (the report predates the r27 ledger row that cites it).
- **D5 (informational).** At `e28312b` the boilerplate string occurs once per file; at the candidate `ghp-served-set.md` has 2 occurrences (line 83 paragraph + the line-95 quotation). The report's "5 knowledge files" is a file count and still holds (5) at the candidate.

## Residual risk / verification gaps

- Freshness of the *underlying* r26 adjudication (host/path-scope claim, `Sitemap best practices` anchor) was re-derived only where it bears on this binding (digests, offsets, ancestry); whether the report's HOLD is *semantically* right for ghp-served-set's S013 reference is the semantic reviewer's call, not mine.
- The bound substring lies in a section explicitly labelled "adjacent observations (not the target; no correction required for this verdict)". It is the only sentence in that report matching this row's subject, and it is unique in the file, but it is a thin, indirect locator for a HOLD whose real warrant is the report's target adjudication of `crawl-scope-per-host.md`.
- No new current-source observation is implied or claimed by this row; nothing was fetched; no external source was re-read.

## Tooling

No installs, no upgrades, no network GET. Read-only Git/`sha256sum`/`python3` probes; the only writes are this report and scratch under `/fast/scratch/hyaku/kake-r27/BindArtifact17/` (`c1.json`). Working tree left unchanged (verified blobs unchanged).

```json
{"target":"pairs.json S013 artifact record (corpus/knowledge/ghp-served-set.md)","verdict":"HOLD confirmed; binding verified","blocking_findings":0,"severity":"low","discrepancies":["D1 stale quote offset 9094 vs measured 9016 in evidence report","D2 bound sentence deictic refers to crawl-scope-per-host.md","D3 reason omits r27-append S013 tokens lines 111/115","D4 citation committed 3min before its target landed","D5 occurrence count now 2 in ghp-served-set.md"]}
```
