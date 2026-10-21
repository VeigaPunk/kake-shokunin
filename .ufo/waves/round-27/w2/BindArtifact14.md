# BindArtifact14 — byte/locator binding attack on the S008 artifact record

Seat `KakeR27.BindArtifact14` (read-only reviewer, leaf). Axis: freshness. Milestone: r27-fresh-falsification. Target: candidate
`ac46a7472d945a6d7ff135e4d7f07b0b6913d835`; row `(S008, corpus/knowledge/static-canonical-preflight.md)` in `.ufo/waves/round-27/pairs.json`; evidence
`.ufo/waves/round-26/fetched/manifest-retry.json`. Lane: artifact identity/coordinates only (no semantic re-adjudication). No network GET, no installs, no
source edits.

**Attacked item (exact bytes).** `pairs.json` @ candidate blob `fb87451a42eaddf719359085e7625c7ffafcd7b2`, sha256
`f1fa20cab67053fea3945330d14efa59f095ede22b6dacbb058d688d0b376a6a` = worktree file = `frozen-candidate.json` pin. Row (pairs.json:159–168): `row S008`,
`file corpus/knowledge/static-canonical-preflight.md`, `kind artifact`, `verdict HOLD`, `evidence .ufo/waves/round-26/fetched/manifest-retry.json`,
`contains "\"file\": \"S008-1-retry.raw.gz\""`, reason "The only row mention is r26 EOF retrieval provenance locating S008 in the retry manifest, not
attribution of any platform claim to GNU tar. The named subject rows exclude S008. Historical retry fact is verified from retained r26 artifacts, not a
fresh S008 opening." Evidence blob @ candidate `637e278d069d6e9378b281a495f4a19768a7c993`, sha256
`84e83fb0cf5bf431eb029a9ab8cab69b661054e6e992b862e87b514786a65d1b`, 902 B. Cited file @ candidate blob
`40ebd1dabc122e620d09974ac973b3262649be9520fea2fa42ebe4dce1ca8a12` (= freeze pin); base blob sha256 `833b28f2…` (= `frozen/expected.json` pin). All reads
use the explicit candidate hash.

## Findings by severity

**F1 — MEDIUM (record accuracy; verdict/count unaffected): "the only row mention" is false against the frozen candidate.**
Declared expectation: the citing file holds exactly one S008 mention, as asserted by the reason and by both w1 reports (`w1/Pair14A.md` §1 "the only S008
occurrence in this entry"; `w1/Pair14B.md` "Line 184 is the only line that cites S008"). Actual: `git cat-file blob
ac46a747…:corpus/knowledge/static-canonical-preflight.md | grep -n 'S008'` → **two** hits — line 184 (the r26 "Round-26 source recheck" bullet) and line
244 (the r27 block the candidate itself appends: "The line184 S008 retry aside is historical artifact provenance only, not GNU-tar support for this
entry."). At declarations `be375d90…` the count is 1 (203-line file); the candidate appends 44 lines (247 total); line 184 is byte-identical
base↔candidate. Impact: the reason was authored against `be375d9` and is stale by self-reference at the candidate it ships in. It does not change HOLD
(line 244 corroborates rather than contradicts) and creates no new obligation (same `(row,file)` key). Count at candidate: `citingPairs 58, reviewedPairs
58, decided 55, newDecided 18, knownUnverifiableUnits 7, knownUnverifiablePairs 3, missing 3`, exit 1 — reproducing the frozen strictC1 "55/58" figure. But
a byte-level coordinate assertion in the frozen ledger is falsifiable. Localisation: the identical `reason`/`contains` bytes are reused for sibling S008
rows (`crawl-scope-per-host.md`, `ghp-custom-domain.md`, `ghp-etag-anatomy.md`), where the claim still holds (S008 count = 1 each at candidate) — the
defect is specific to this row. Fix must be a wording/citation update in the r27 ledger (or an appended note); never a `[r27-recheck S008 STALE]` marker,
never an r26 file rewrite.

**F2 — LOW/MEDIUM (verification gap): the freeze record does not pin this row's evidence chain.** Declared expectation: the evidence
file and its retained bytes are digest-pinned by the freeze artifact, as r27's own fetched artifacts are. Actual: `frozen-candidate.json` `sourceFiles` has
214 entries, **0** under `.ufo/waves/round-26/` (grep 'round-26' → 0 matches), while `.ufo/waves/round-27/fetched/*` containers and `text/*` are pinned
(e.g. `S001-1.source.gz` = `37099a34…`). The r26 evidence is nonetheless tamper-evident via git history: `manifest-retry.json` blob `637e278d…` and
`S008-1-retry.raw.gz` blob `0b03a05f…` are identical at base `83528f7` and candidate `ac46a74` (`git diff base candidate -- .ufo/waves/round-26/fetched/` →
empty). No tamper observable; the gap is that the freeze artifact asserts no digest for the bytes this row's support rests on.

**F3 — LOW (counter-strength note; no contract violation): artifact support check is presence-only.** `count_c1.py:99` validates
`p['contains'] not in blob(p['evidence']).decode()` — no uniqueness, no row scoping. Here the weakness does not bite: the substring occurs **exactly once**
(byte count = 1) inside the file's only record, whose `"row"` is `"S008"` (`manifest-retry.json` holds exactly one record, `rows: ['S008']`) — the locator
is exact and in the right row, not another source's boilerplate. Self-citation rejected: the evidence is a raw HTTP fetch receipt under
`.ufo/waves/round-26/fetched/`, not `pairs.json`/knowledge; count_c1's `artifact_self_support` guard (paths starting `corpus/knowledge/` or
`.ufo/waves/round-27/`, or the r26 population/statements files) correctly admits it, and the receipt is independent of the ledger under judgment.

**F4 — LOW (cross-wave retention asymmetry; observation only): evidence file retains HTTP response headers.** `manifest-retry.json`
retains the S008 response `headers` (content-type, last-modified, etag, date, content-length). r27's own `fetched/manifest.json` has **no** `headers` key
(checked over all 8 records) and `privacy_selftest.py` enforces that; `retention-migration.json` shows r27 removed legacy raw bodies before first capture
commit. The r26 file is immutable per contract and was **not** rewritten (blob identical base↔candidate), so no action is proposed — recorded because this
row's only evidence dependency is a file whose retained header set r27 policy would not retain.

**F5 — INFO (verified-good; digest-naming note). Manifest digest names the received body, not the retained container.** Declared
expectation: the manifest's `sha256`/`bytes` bind the retained artifact file named in `file`. Actual: independent gunzip of committed candidate blob
`0b03a05f…` (`.ufo/waves/round-26/fetched/S008-1-retry.raw.gz`) yields exactly **512359** bytes, sha256
`93281a63cb9f94a08d4d2ed6dfe9559b02cecc72d6bbd304c9970d8f81606084` = the manifest's declared `bytes`/`sha256`. The gzip **container** is 150267 B, sha256
`1d34183a…`, recorded in no committed file (git grep → no hits). Convention uniform across all 34 r26 manifest rows (every row checked programmatically, 0
mismatches); `population.json`'s S008 fetch entry names the same digest. Consequence: a consumer reading manifest `sha256` as the retained file's digest
would mismatch; the ledger row asserts only the filename substring, so no false digest claim is made by the record. Offline authenticity corroboration (no
fetch): manifest ETag `9b668bb3c441a095e7c39a7baa7f88a93599ab4c` equals `git hash-object` of the decompressed body — the retained bytes are the upstream
git blob served by the commit-pinned URL (`…/plain/doc/tar.texi?id=cfdb891bbd68c920ea75210977593f3cd08f0418`, identical to `corpus/SOURCES.md:16` and
`population.json`'s S008 fetch). Retry chain checks out: `manifest.json`'s S008 slot is `status null`, `error TimeoutError`, `bytes 0`, `sha256 e3b0c442…`
(empty-body digest) and the retained `S008-1.raw.gz` gunzips to 0 bytes with that digest; `fetch_sources.py` uses `timeout=60`, `fetch_retry.py`
`timeout=240`, matching `"attempt": 2`.

**F6 — INFO (verified-good): no fresh S008 observation implied.** r27 fetched manifest rows are S001–S006 only (no S008) and
`.ufo/waves/round-27/fetched/` has no S008 artifact; the row is `kind: artifact` and its reason says "not a fresh S008 opening" — honest and consistent.
Historical dates preserved: SOURCES.md keeps S008 `opened 2026-10-19`; retry receipt dated 2026-10-21T15:11:01Z. Base pointer `at base cb807bc` holds:
`cb807bc` is an ancestor of the candidate and of base `83528f7`. Terminology note (not a defect): "EOF" is the contract's category term ("r26 EOF prose");
literally line 184 is not the last line — line 184 of 247 at candidate (203 at declarations, 194 at r26 commit `e28312b`), under heading "## Round-26
source recheck" at line 182, inside the r26 appended tail. Honest caveat: my row's HOLD does not make the file decided — the same citing file still carries
UNPROVABLE sibling `S033` (3 carried units), one of the 3 remaining missing pairs.

## Residual risk / verification gaps

- Not verified (offline-impossible, no external fetch required or performed): that the upstream server returned these exact bytes for commit `cfdb891b…`. Strength rests on ETag == git blob id, body-digest ↔ manifest ↔ population agreement, and the commit pin existing only in the URL string (the body contains 0 occurrences of the commit id).
- The r26 retry manifest was produced by an inline command; `fetch_retry.py` is a committed post-hoc copy whose docstring states it did not produce the manifest. Provenance is disclosed in r26 material; the manifest remains the evidence — standing r26 debt, out of scope.
- `w1/Pair14A.md` / `w1/Pair14B.md` were authored at `be375d9`, where "only S008 occurrence" was true; the stale wording that reached the frozen ledger is the L1 ledger row, not those reports.

## Verification performed (declared expectation → actual; candidate hash)

1. pairs.json blob equals freeze pin → `fb87451a…` / sha256 `f1fa20ca…` = pin ✓. 2. Evidence blob identical base↔candidate → `637e278d…` both ✓. 3.
`contains` substring exact and unique → 1 occurrence, line 20, only record `"row":"S008"` ✓. 4. Retained bytes match manifest digest → gunzip `0b03a05f…` =
512359 B / `93281a63…` ✓ (container `1d34183a…` unpinned). 5. First attempt failed, empty body → gunzip `86e43ea3…` = 0 B / `e3b0c442…`, manifest.json slot
status null + TimeoutError ✓. 6. S008 count in citing file = 1 (expected) → **2** (lines 184, 244) ✗ → F1. 7. Named subject rows exclude S008 →
S020,S021,S026–S034 ✓. 8. No fresh S008 opening → r27 fetched rows S001–S006 only ✓. 9. C1 counter at candidate (`python3 -B
.ufo/waves/round-27/count_c1.py --root . --revision ac46a747…`) → exit 1; 58/58 reviewed, 55 decided, 7 units/3 pairs, 3 missing ✓ (frozen strictC1
reproduced). 10. Freeze pins evidence chain → 0 of 214 → F2. 11. r26 evidence untouched by r27 → `git diff` empty ✓. 12. No self-citation → evidence
admitted by `artifact_self_support`, independent receipt ✓.

## Tooling

No installs, no pacman transaction, no service mutation, no source/registry/manifest edits. Read-only `git` (`cat-file`, `rev-parse`, `ls-tree`, `diff`,
`blame`, `log`), `grep`, `sha256sum`, `gunzip`, `python3 -B` (stdlib only). Scratch only under `/fast/scratch/hyaku/kake-r27/BindArtifact14/` (TMPDIR set
explicitly); no `/tmp`, no `/dev/shm`. Only this report written.

Report: .ufo/waves/round-27/w2/BindArtifact14.md
