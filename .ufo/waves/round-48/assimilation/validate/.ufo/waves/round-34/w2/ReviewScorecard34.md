# KakeR34.ReviewScorecard34 — SCORECARD round-34 sections + capability row (wave 2)

Scope: SCORECARD.md "Round 34 — declared claims" (:1193-1239), "Round 34 — measured
results" (:1241-1284) and the new Capabilities row (:195) at
24a16474ee73e20453f3e1be9d2f33573c5196d9. Read-only seat; nothing mutated in the
lane; no tools installed or updated. Sandbox:
/fast/scratch/hyaku/kake-r34/w2/ReviewScorecard34/ (clone checked out at 24a1647,
TMPDIR=…/tmp, GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset).

## Findings

1. LOW — wrong wave-1 pointer in a limits bullet. SCORECARD.md:1277 cites
   "`CriticDeclarationFit` 3, `CriticSeparability` 5" for "S067 and S068 … name no
   `<link rel=canonical>`". That content is finding **6** of
   .ufo/waves/round-34/w1/CriticSeparability.md ("rel=canonical and `<link>` occur
   0 times in S067, S068, S069 and S070 … lane design choice"); its finding 5 is
   "Latent divergences between the C2 counter and the C1 contract" and does not
   support the sentence. `CriticDeclarationFit` 3 is correct. The claim itself is
   true (grep of retained sources: 0 "absolute" hits in S067–S070; S071–S077 only
   S074 has 1 "absolute" hit and 0 "og:url" hits), so this is a pointer fix only.
2. LOW — after-receipts at the landing revision are uncommitted. Read-only
   `git -C <lane> status --porcelain -- .ufo/waves/round-34/verification/` exit 0
   shows `?? c1-at-24a1647.json` and `?? c2-at-24a1647.json`. The measured-results
   table (:1245-1246) therefore cites receipts only at 5613071/9ef758c (C1) and
   9ef758c (C2); a reader of commit 24a1647 cannot re-derive the after-values at
   the landing revision from committed receipts. The two working-tree receipts do
   read 28/28 and met 5/5 (census stated==derived), and the rerun below confirms
   both at 24a1647, so the numbers are true — only the commit is missing.

No HIGH or MEDIUM defect found in the two sections or the capability row.

## Re-derivations (sandbox clone at 24a1647; exit codes observed)

- Append-only: `git diff d08d8de 24a1647 -- SCORECARD.md` exit 0, 61-line patch,
  two hunks, additions only: the capability row (:195) and the measured-results
  section (:1241-1284). Declaration (:1193-1239) untouched.
- Counters rerun at five revisions; every number in :1245-1246 reproduced:
  - C1 `python3 -B .ufo/waves/round-34/c1_matrix_count.py --root . --revision R`:
    1e54c895 exit 1 passed 0/28 gatesAllRejected true; d08d8de exit 1 0/28 true;
    5613071 exit 0 28/28; 9ef758c exit 0 28/28; 24a1647 exit 0 28/28.
  - C2 `…c2_source_census.py …`: 1e54c895 exit 1 met 0/5; d08d8de exit 1 0/5;
    5613071 exit 1 0/5; 9ef758c exit 0 met 5/5 controlBroken false; 24a1647 exit 0
    5/5 false. (At 1e54c895 the census clause reads "retained tree or archive
    missing" — the ds4cc archive lands at d08d8de; consistent.)
  Field-for-field matches of committed receipts c1-at-{1e54c895,d08d8de,5613071,
  9ef758c}.json and c2-at-{1e54c895,d08d8de,9ef758c}.json, including C1 before
  receipts' toolPresent=false and the four constant-gate tallies (6/28, 0/28,
  6/28, 1/28).
- Byte-identity claim (:1250-1251): sha256 of both counters identical at d08d8de
  and 24a1647 — c1_matrix_count.py fc72d855…c51e, c2_source_census.py ee7461b9…
  f892 — and equal to counterSha256 in every receipt; c1-matrix.json 246a6a3b…
  14f7 equals the counter's embedded pin and every receipt's matrixSha256; tool
  sha256 at 24a1647 8dd0018248e0… equals toolSha256 in c1-at-5613071/9ef758c
  (tool unchanged since 5613071).
- Capability row (:195): 28/28 at 5613071 → c1-at-5613071.json; "committed
  selftest 29/29" → selftest-link-preview-at-5613071-tool.txt cases=29 failed=0
  and scripts/link_preview_selftest.py committed (blob 41d7e06 at 24a1647);
  real-input receipt agrees=true with expectedFromCensus = census complements
  (102 pages: og:image missing 101; og:title/og:type/og:url 15 each); first-working
  round 34; the lookup caveat pointer "mistake row 4" is correct —
  corpus/lessons/round-34.md mistakes-table row 4 (:68) is the control row.
- Limits bullets vs the wave-1 reports they cite: dcef39b5 28/28 and 0cce15f0 5/5
  with census copied from the before-receipt and first-six-word quotes =
  CriticDeclarationFit findings 1-2, receipts criterion-lookup-control-c1-dcef39b.txt
  ("score 28/28 … verdict FAIL: control reaches the full score", exit 1) and
  c2-at-critic-hollow-0cce15f.json (met 5/5); ExecIndependentOracle 28/28 on its
  first attempt; ExecCensusIndependentRecount all seven census numbers agree;
  MutC1CounterWrongGates 27/28 killed by D7 — all stated verbatim in those reports.
  "Parses each page with html.parser": scripts/link_preview_audit.py:47,69 at
  24a1647. "The tool docstring says so at 5613071": docstring :8-11 at 5613071
  discloses both og:url rules as lane policy. Conditions a–d separate =
  CriticSeparability finding 4 (a–d are 4 of the 5 points). ExecUpstreamBlobExact:
  head still 7fc6aa2f, retained tar cmp IDENTICAL.
- "None of whose fixtures copy a matrix case" (:1259-1260): stripped-byte
  comparison of all 22 HTML blobs inside c1-matrix.json against all 27 fixture
  .html files under scripts/fixtures/link-preview → 0 exact-content overlaps.

## Residual risk and verification gaps

- Fixture-overlap check was exact-content only; a cosmetically edited copy of a
  matrix page would pass it. Selftest fixtures' expected.json values were not
  validated (another seat's scope).
- "These three checks were written after the finding" (:1262-1264) is a temporal
  claim; committed receipts carry no timestamps proving write order. Not
  falsified, not proven.
- The hollow-control receipt reads "controlBroken": false — SCORECARD never
  claims otherwise, but a reader skimming receipts may expect the control to flip
  it; the counter's own control metric did not fire on the hollow commit.
- C1 constant gates were not rerun under network isolation; CriticDeclarationFit
  finding 4 ("network-free" is unmeasured) stays open and SCORECARD does not
  claim it closed.
- Lane working tree was read only via read-only `git status` and the two
  untracked receipt files; my only lane write is this report.
