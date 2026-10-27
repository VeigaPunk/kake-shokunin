author: hyaku closure (non-author advisory; decision by Parent)

# Round 27 non-author verification — strict C1 and the full C2 interface both remain unprovable

Review phase was **canonical read-only**: this seat read committed bytes and immutable Git metadata only (`git --no-lazy-fetch show/ls-tree/cat-file/rev-parse/diff`, blob and SHA-256 comparison). **No gate, counter, oracle, selftest or fixture was executed**; no network, browser, account, publication or credential operation; no r24 target or probe; no tool installed or updated. No source, test, claim, report or prior record was edited in the review phase. The decision below is the **Parent's (Main's)**, taken on **three independent advisories**; this note is one advisory input, published by the Parent together with an append-only LOG entry and index row only. Lane: `kake-shokunin`. Author report: `.ufo/reports/round-27/kake.md` (Root commit `3cefad981c5bae2e7cc7966223f6535133ecaa31`).

| Revision | Pin meaning |
|---|---|
| `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba` | prior closed **negative** base — round 26 closed rejected-honest-stop / admitted false, not an accepted state |
| `be375d90afc6fc7aca369ab3cf5247bf460aeed2` | declarations landed **before** implementation: contract, C2 oracle, frozen inputs, baselines |
| `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` | the measured/falsified candidate pin; carries the bounded after-receipts |
| `cd2e95b001161811db526b252a3890be6cb83f2b` | final C1 measurement revision (post-barrier record corrections) |
| `62aeddf4ab939d9bc7844031f707ac04703bb42d` | final durable/pushed lane head |

## Verdict (Parent decision)

**Rejected-honest-stop; admitted false.** The round produced real, reproducible bounded evidence and an honest author stop. It does not complete either frozen claim, and it grants **no scalar change, no capability, no promotion and no minted artifact**.

- **Freshness (C1) — unprovable.** The frozen after-clause requires a durable HOLD or supported STALE per pair and never counts UNVERIFIABLE as decided. Presence is not support. At the **baseline pin**: inherited review coverage **41/57**, strict instrument **38/57 decided, exit 1** (`kake-shokunin/.ufo/waves/round-27/verification/c1-current-baseline.json`, `--revision 83528f7c…`). At the **final C1 pin** `cd2e95b…`: **58 reviewed / 55 status-decided, 7 known unknown units across 3 pairs, exit 1** (`verification/final-record-c1.json`). The legacy 58/58 green (`verification/c1-original-candidate.json`, `verification/c1-guards-candidate.json`, exit 0) is a review-count result retained as historical measurement, not relabelled as strict completion.
- **Operability (C2) — unprovable at the full claimed interface.** At the **measured candidate pin** the finite component is real: **exact 16/16 original identities, 0 false positives, gate exit 1, counter exit 0** (`verification/c2-frozen-candidate.json`), plus real gate **29/29** (`verification/gate-selftest.json`), Git-name **30/30** after against a controlled before-variant that showed 10/30 failures (`verification/git-name-after.json`, `verification/git-name-before.json` — its own pin, isolating NUL framing), both counter selftests and the privacy selftest at 0 failures, and four killed source mutants. The full interface nevertheless fails at the same pin; the failures are recorded by the author in `kake-shokunin/.ufo/waves/round-27/unresolved-acceptance.json` and captured with commands and outputs in `kake-shokunin/.ufo/waves/round-27/w2/CliUsage.md`, `w2/CliJson.md`, `w2/CliPaths.md`.
- **The finite predicate is not an admission predicate.** `kake-shokunin/.ufo/waves/round-27/w2/MutateConstant.md` records a mutant that returns the original 16 pairs unconditionally: on the frozen input its output was byte-identical to the real gate and it passed the finite counter predicate, while the unchanged real fixture suite killed it. A constant therefore satisfies the frozen detection and fails the interface.

| Axis | Verdict | Basis |
|---|---|---|
| freshness | unprovable | 41/57 presence; strict base 38/57; final 55/58 decided with 7 unknown units / 3 pairs; exit 1 |
| operability | unprovable | finite 16/16 real at the measured candidate; full interface fails; constant mutant passes the finite predicate |
| expansion | unchanged | no new domain ground, source row, capability or repertoire |
| quality | improved, bounded | source-grounded adjudications and visible corrections on named entries; no blanket code-quality or universal no-harm claim |
| discernment | improved | outside spot-check agrees with the recorded admits/rejects and keeps the completeness defect open |
| depth / coverage / calibration / adjacency | unchanged | no independent claim on these axes in this round |

## Original targets unchanged (independent, Git metadata only)

- `kake-shokunin/.ufo/waves/round-27/c2-oracle.json`, `frozen/expected.json`, `frozen/population.json` and `frozen/ledger.json` are byte-identical at the declarations commit, at the measured candidate and at the final lane head.
- The 28 frozen inputs were re-verified here: the 26 corpus pins match the baseline blobs; the frozen `population.json` and `ledger.json` are byte-identical to the r26 originals `.ufo/waves/round-26/population.json` and `.ufo/waves/round-26/statements.json`.
- The original 16 target identities are unchanged, and the counter itself re-checks the declarations and the frozen digests (`kake-shokunin/.ufo/waves/round-27/c2_count.py`, `frozen_input_changed` / `snapshot_tampered`).
- One disclosed registry edit remains: 6 monotone `used-by` cells in `kake-shokunin/corpus/SOURCES.md` (0 entries lost; every other column byte-equal; rows still 35). The round-27 sentence claiming row cells were not rewritten was itself corrected before the final head, so no false statement of that kind survives at `62aeddf`.

## Bounded no-harm, independently reproduced (static, no gate/counter run)

- **26/26** knowledge byte prefixes preserved: for each baseline `corpus/knowledge` path the baseline blob is an exact byte-prefix of both the `ac46a74` and the `62aeddf` blob (22 files byte-identical, 4 append-only).
- **7/7** pre-existing `kake-shokunin/scripts/*` files byte-identical at all three revisions.
- **279/279** r26 wave files unchanged: `ls-tree` counts 279 paths at the baseline and the diffs baseline→`ac46a74`→`62aeddf` are empty.
- The lane's own bounded receipt is `kake-shokunin/.ufo/waves/round-27/verification/no-harm.json` (26/26 prefixes, 7/7 scripts, 279 r26 files, 6 logged registry cells).
- This is **not** a universal no-harm proof: it does not cover `corpus/SOURCES.md` byte-wise, does not certify that the retained corpus statements are true (pair presence ≠ semantic support), and does not certify arbitrary CLI safety.

## Measured candidate vs final lane head — code identity, not a new execution

The lane states that all measured algorithm/test files stayed identical from `ac46a74` to `62aeddf`. The lane record does **not** enumerate that set, so the "8 files" count is ambiguous and is not resolved here by invention: all **9** Python files added by the round (7 under `.ufo/waves/round-27/`, plus `scripts/citing_set.py` and `scripts/citing_set_selftest.py`) are byte-identical between the two revisions, so either reading of the count holds.

What this does **not** mean: **no C2 or fixture measurement exists at the final head.** The bounded after-receipts belong to the measured candidate pin and the final C1 number to `cd2e95b`; the baseline and the controlled before-variant have their own named pins. This closure ran nothing at `62aeddf`, and a measurement at `62aeddf` would be a new datum, not a confirmation. Corpus inputs did move after the measured pin (`corpus/knowledge/ghp-served-set.md`, `corpus/knowledge/sitemap-orphan-audit.md`, `corpus/SOURCES.md`, and the LOG/SCORECARD/SKILL/QUALITY/README/lesson surfaces), so the code identity must not be read as "the final head was measured".

## Identities and conformance exceptions

- The wave registries report **153 actual author identities** (67 build + 1 privacy + 85 falsify), each with a nonempty report, **0 dead, 0 replacements, 0 terminal provider errors** (`kake-shokunin/.ufo/waves/round-27/w1-outcomes.json`, `w2-outcomes.json`, `start-evidence.json`, `residual-identities.json`). This is a **reported census from the recorded registries and outcomes**, not a live per-event authenticity proof; the original source-freeze interval is not fully authenticated. The counts are not derived from pre-wave planner names, and the same-identity BuildGate resumptions are already among the 67.
- The **3 Root advisory identities** behind this decision are separate late seats, outside the pre-wave registries and not part of the author census above.
- Disclosed, not laundered as PASS: BuildSelftest's prohibited mid-flight stub-gate smoke is **VOID acceptance evidence** with no acceptance credit (`w1-outcomes.json`, `scopeVoidAcceptance`); the AttackOracleFreeze scratch job hit a **3600 s timeout with no counter or output** before later explicit-hash probes (`w2-outcomes.json`, `probeTimeouts`); report-length overruns W1 Pair07A 200 / CritIndependence 217 and W2 JudgePair06 124 / BindQuoteS001 115 / BindQuoteS004 106 / BindArtifact07 103 / AuditNoHarm 102. No prior failure was re-run to confirm it.

## Policy, population and privacy limits

- The **round-24 policy-stop / L0 disposition stays unresolved**; nothing from it was retried, rephrased or routed elsewhere.
- The **18 knowledge pairs for rows outside the frozen 32-row population (S014/S019/S035)** and the broader corpus-policy census remain explicit debt, not a silent drop. (The gate's own `outsidePopulation: 18` counter in `verification/consumer-current.json` is a different quantity — citations whose row id is outside the population — and must not be read as that debt.)
- **No whole-privacy certificate is issued here, and none is implied.** What is actually observed: the 8 delivered manifest records are locally shape-consistent, with 2 rows of kind `received_code_bytes` (received bytes retained verbatim) and 6 rows of kind `public_visible_text` (received and retained sizes and digests recorded and differing); no content type or headers are retained for any of the 8 rows, so the HTML-versus-plaintext decision is not re-derivable from the artifact that asserts it. A path census over the inspected local Git refs found **no R27 `.raw.gz` path** (the round-27 fetched paths present among those refs are the manifest, the 8 filtered payloads and the 8 text sidecars; the `.raw.gz` paths that do appear are pre-existing r26 ones). That is a **path observation only**: a misclassified HTML capture stored under another filename would not be detected by it, and no received-body bytes, source provenance, network route or authenticity is established by it. The recorded marker, symlinked-ancestor, helper-execution and destination-policy concerns remain **conditional/static** — no private target, no auth workflow and no incident was exercised.

## No cleanup

No cleanup was performed and none is claimed. The untracked round-26 `__pycache__` item and every other untracked or foreign-root artifact were left exactly as found; no history purge, no unowned deletion, no scratch removal outside this closure's own directory.

## Routed defects (do not rewrite this round)

1. The C2 interface clause is unmet: unusable input documents must yield the contracted JSON report and exit 2, and an absent or unreachable corpus surface must not return `clean`. Keep the finite 16/16 result separate from the interface claim.
2. Keep the C1 distinction between review presence and strict support; the 7 unknown units in 3 pairs are unresolved and are not counted decided.
3. Keep the recorded conformance exceptions visible (void stub smoke, the 3600 s timeout, the report overruns) and keep the fixture-oracle granularity limitation on the record: the runner compares exit plus finding-id multiset only.
4. Preserve the bounded no-harm scope, the r24 policy-stop and the out-of-population debt as they are.

No promotion, no state advance, no new round dispatch and no scalar grant is claimed by this note. The Parent's own canonical census, native Root CLI proof and Root ledger step follow the publication of this note; nothing here preclaims them.
