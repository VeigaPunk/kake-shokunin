# BindArtifact03 — byte/locator binding attack on the S003 artifact record

Target item: `.ufo/waves/round-27/pairs.json` (at candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`),
pair `{"row":"S003","file":"corpus/knowledge/sitemap-orphan-audit.md","kind":"artifact","verdict":"HOLD"}`,
evidence `corpus/lessons/round-20.md`, `contains` = ``C3: S001/S002/S003/S004/S006/S008 rows plus `ghp-served-set`; annotate `round-7.md` append-only``.
Scope: artifact identity / coordinates only. No semantic re-adjudication; no new current-source observation.

Independently calculated evidence hash: `corpus/lessons/round-20.md` @ candidate =
sha256 `5f62ef0bce7492f094b8a08982087c2fad116f01a3bd96abdebd98266723a22a`, 44612 bytes.
Blob `f02db6fb839ba0ed5b67f90307df2cace74bd026` is **identical at base 83528f7 and at candidate** → the evidence file is
not a candidate-authored or wave-authored artifact.

## Positive verifications (byte-exact, right record)

- Declared expected result before running: the `contains` string is byte-exact in the evidence blob, occurs once,
  and sits in a row that also names the citing file.
  Actual: `contains in blob` = **True**; occurrences = **1**; row = **line 261, `| A2 |`**; that row's
  evidence-pointer cell = ``corpus/README.md:26,52-53`; `SKILL.md:227`; `corpus/lessons/round-7.md:21-25`; `corpus/knowledge/sitemap-orphan-audit.md:20-24` `` → names the citing file. ✔
- Not another source's boilerplate: the only other `C3:` fix cells are A1 `{S009,S010}` (l.260) and A3 `{S003,S005,S007}` (l.262) — distinct sets; the located cell is unique in the file. ✔
- Not self-citation: evidence path is `corpus/lessons/…` (not `corpus/knowledge/…`, not `.ufo/waves/round-27/…`); `count_c1.py` `artifact_self_support` rejects only those prefixes + the r26 population/statements files → the row passes legitimately. ✔
- Historical date/base asserted by the row are preserved: base `cb807bc8d8bc94be1268e4741191bb3d5e518565` is the direct parent of r20 commit `02b6dd0` (2026-10-19 19:38 -0300); the corrections-block header ``base `cb807bc` `` and the `2026-10-19` stamps are intact; citing-file lines 1–149 are **byte-identical** base↔candidate (sha `553ad1006e9e5800…` both sides). ✔
- Retry not implicated: `.ufo/waves/round-26/fetched/manifest-retry.json` contains **only S008** (attempt 2); S003 has `attempt:null` in both r26 and r27 manifests. ✔
- Base coordinates cited by the disposition resolve in the base blob: `:14,:18,:21,:25,:28,:32,:38,:112` all carry the claims the record asserts. ✔
- Ledger's own factual claims check out: "Inline correction sources are exactly S001/S002/S004/S006" — the union of S-tokens on citing-file lines 120–127 is exactly `{S001,S002,S004,S006}`, no S003/S005 ✔; "A2 at r20 lesson261" ✔.
- Independent C1 consumer re-run (read-only): `count_c1.py --revision ac46a74` → exit 1, `citingPairs 58`,
  `decided 55`, `knownUnverifiableUnits 7`, `knownUnverifiablePairs 3`, S003×sitemap-orphan-audit outcome
  `{"verdict":"HOLD","valid":true}` — matches the frozen-candidate strict-C1 declaration (55/58, 7 units/3 pairs).
  C2 oracle re-run → `expected 16, detected 16, falsePositive 0, passed true`.

## F1 — HIGH: the committed locator is substitutable; it does not mechanically bind to the citing file

Expected result declared before running: swapping the A2 row's pointer cell to an unrelated file, while leaving
the fix cell intact, must make the S003 artifact row fail if the committed `contains` binds it to the citing file.

Probe (isolated scratch clone `/fast/scratch/hyaku/kake-r27/bindartifact03/probe-repo`, shared clone of the real
repo, detached @ ac46a74, one local commit `130e29da`; real repo untouched, `git status` shows only wave `??`
files, HEAD still ac46a74):
mutation = `` `corpus/knowledge/sitemap-orphan-audit.md:20-24` `` → `` `corpus/knowledge/UNRELATED-FILE.md:20-24` ``
in `corpus/lessons/round-20.md` (fix cell untouched).
Actual: `count_c1.py --revision 130e29da` → **exit 1**, S003 outcome **`{"verdict":"HOLD","valid":true}`**,
`decided 55`, S003 **not** in missing. The mutant passes.

Root cause: `count_c1.py` line 115 tests only `p['contains'] not in blob(p['evidence'])` — a bare substring test.
The committed `contains` is the A2 **fix cell**, a class-wide remediation token list that carries no pointer to the
citing file; the file binding lives in an *adjacent* cell of the same row that the checker never reads. The same
mutation is rejected by the pointer-bearing variant Pair03A itself proposed in `w1/Pair03A.md`
(`` `corpus/knowledge/sitemap-orphan-audit.md:20-24` | `none` | C3: … ``, unique in the evidence file) — so the
ledger took a **weaker locator than its own reviewer recommended**, and the weaker one is what the frozen gate measures.
Remedy (author-side, needs L1): re-express the S003 artifact row with the pointer-bearing `contains` (or add a
checker rule that the located record's pointer cell names the pair's file).

## F2 — MEDIUM: the S003 token has no entry-level support record; A2's pointer misses this entry's origin/main claim

Expected result declared before running: if S003 is an entry-level attribution for this file, the r20 per-location
disposition for `corpus/knowledge/sitemap-orphan-audit.md` must list S003 among that file's own source sets.
Actual: `.ufo/round-20/resume/citation-disposition.json` (`platformCorrections`, 8 rows for this file) lists only
`{S001,S004}` or `{S001,S002,S004,S006}`; **S003 appears in no row for this file** — it appears only for
`SKILL.md:16` and `publish-channels.md:9,12` (the CNAME/custom-domain family = A3). Separately, A2's pointer for
this file is base `:20-24`, which contains the `:21` snapshot claim but **not** `:28`
("the live tree IS the last-pushed `origin/main` tree") — the origin/main-equivalence claim that A2's own class
label names. So the artifact proves "A2 (a class-wide row) lists S003 in its remediation set", not "S003 supports
this entry's claim". The ledger's `reason` says the former ("A2 … explicitly maps this entry's served-set
misconception to the S003-containing source group") — true of the group; the group→entry hop is unverified at
entry level. Consistent with the frozen-candidate note "raw313 is mixed field sum, not semantic denominator".

## F3 — MEDIUM/LOW: the candidate rewrote the registry cell that a falsification step relied on

Expected result declared before running: Pair03B's step 6 ("The registry does not tie S003 to this entry;
`grep sitemap-orphan-audit corpus/SOURCES.md` returns no match") must still reproduce at the frozen candidate.
Actual: at **base 83528f7** that grep exits 1 (no match) and S003's used-by cell reads
`corpus/knowledge/ghp-custom-domain.md, corpus/knowledge/ghp-served-set.md`; at **candidate ac46a74** the same grep
returns **6 matches** and S003's used-by cell now includes `corpus/knowledge/sitemap-orphan-audit.md`. The only
commit between them touching that file is the candidate commit itself (`git log 83528f7..ac46a74 -- corpus/SOURCES.md`
→ ac46a74 only). The change is disclosed in `corpus/lessons/round-27.md` ("only allowed used-by cells"; only the
used-by cell changed — status/opened/recheck/teaches/anchor/tier identical, confirmed by column-level diff), but the
S003 ledger row rejects B's conclusion **without citing that disclosure and without noting that the fact B tested
was changed by this very candidate**. Falsification evidence is therefore not reproducible against the frozen
candidate, and the newly-added used-by cell is candidate-era (not "historical") and must not be read as independent
historical corroboration of the S003↔file link.

## Uncertainties / residual risk

- I did not adjudicate whether HOLD is *semantically* right at the batch scope the row declares; that is the semantic reviewer's lane. My findings bound only identity, coordinates and reproducibility.
- The `contains` string occurs in 5 blobs tree-wide (round-20.md, `.ufo/round-20/resume/mistakes.md` l.31, r21 frozen pre-copy l.261, `pairs.json`, `w1/Pair03A.md`) — all copies of the same A2 record, so no cross-source ambiguity; uniqueness holds *within* the cited evidence file (1 occurrence).
- F1 was demonstrated in a scratch clone with one local commit; the real repo was not modified (no commits, no index/branch changes there; probe clone remains in scratch only).
- Pair03A's prose "Base lines 20-24 sit inside the corrected span (18/21/25)" is imprecise: `:25` is not inside `:20-24`. The committed ledger row does not repeat this, so it does not affect the pair.
- Scope note: `corpus/SOURCES.md` used-by widening also touches the S004/S006/S022/S023 artifact rows (evidence `corpus/SOURCES.md`); out of this seat's row, flagged for the sibling seats.
- No tooling installed (none needed). My writes are confined to `/fast/scratch/hyaku/kake-r27/bindartifact03/` and this report; `TMPDIR=/fast/scratch/hyaku/kake-r27` for consumer runs. No source file was edited. Note: an untracked `scripts/__pycache__/` (bytecode only, no semantic effect) appeared in the tree during this window from concurrent consumer runs; left in place rather than racing other seats.
