# ReviewMistakesRows — round 31 wave 2 (falsify)

Seat: KakeR31a2.ReviewMistakesRows (leaf). Audited `corpus/lessons/round-31.md` `## Mistakes`
(4 rows) at fde133a / tip 92235a0. Sandbox: /fast/scratch/hyaku/kake-r31/a2-w2/ReviewMistakesRows/
(clones `clone` @ fde133a, `clone2` for git-state demo). No installs, no network, no lane mutation
except this file.

## Verdict table

| Row | Pointers ok | Able-to-fail shown | Issues |
|---|---|---|---|
| 1 repair-claim wider than its guards | yes | yes — reproduced | "(N1–N6)" names a range whose N4 the closure never defines; "gained commits" is inferred from `victimUnchanged: false` (minor) |
| 2 closure command that cannot pass as written | yes | yes — reproduced | none |
| 3 partial reports not marked | yes | n/a (no run claimed; practice) | `<wave>/seat-status.json` exists for w1 only; no w2 file at fde133a or 92235a0 (minor today, must land at w2 close) |
| 4 dead route not planned for | yes (counts) | **no — cited record absent** | "wave 2 dead-seat count is recorded in its seat-status.json": `.ufo/waves/round-31/w2/` is empty at both audited revisions; nothing records any wave-2 dead seat. Moderate |

## Row 1 — repair-claim wider than its guards

- `git log -1 f80bd8f`: "wave-2 sentinel repairs to the fixture runner (contained setup and root
  paths, no fixture .git, hooks disabled, symlinked cases skipped, bounded case.json)" — matches
  "described as making the runner's fixture setup safe".
- round-30-verifier-spotcheck.md:145-170 lists exactly five gaps, labeled N1, N2, N3, N5, N6;
  the routing at :250-262 also skips N4. `grep N4` over the whole spotcheck: 0 matches. The
  lesson's "(N1–N6)" is a label range that reads as six; five is correct.
- Receipt c1-before-f1ffb81.json: passed 0/5, controlK1 true (exit 0, 45 cases),
  runnerSha256 9f2d1ecb…4d3. P1 canary true (planted script ran), P2/P3 victimUnchanged false,
  P4 timedOut true (FIFO), P5 exit 0 (silent skip) — the four harms the row lists.
- My re-run of the cited counter (clone @ fde133a, TMPDIR in sandbox):
  `python3 -B .ufo/waves/round-31/c1_sandbox_probes.py --root . --revision f1ffb81… --scratch …/counter-before2` → exit 1, "C1 0/5 K1=hold", per-probe details byte-identical to the receipt.
  Same at `--revision fde133a…` → exit 0, "C1 5/5 K1=hold" (corroborates c1-after receipts).
- Hostile selftest, my runs: repaired (tree runner) → exit 0, 5/5 pass; base runner extracted via
  `git show f1ffb81:scripts/citing_set_selftest.py` (sha256 9f2d1ecb280b7dc314886c79264fb5461c400d8f7c762ea62bb4018fc49e14d3
  — equals the receipt's runnerSha256) → exit 1, 5/5 fail. Matches hostile-selftest-base-runner.json
  (passed false) and hostile-selftest-c88b97e.json (passed true). My JSONs:
  out/selftest-base.json (2b8a6199…27b), out/selftest-after.json (5a4a1810…eaf).
- All five hostile specs committed: scripts/fixtures/citing-set-hostile/P1-selftest-argv …
  P5-symlinked-case. New QUALITY criterion present: corpus/QUALITY.md:488-499 ("A containment
  repair is backed by one hostile probe per shape it claims").

## Row 2 — closure command that cannot pass as written

- round-30-verifier-spotcheck.md:101-106 says verbatim: `git diff --quiet 4580c78 91b60bd -- …sources/ …fetch_sources.py` exits 1, only changes 7 added files under `sources/screened/`. Exact.
- SCORECARD @ a16602a :886-888 declares the exact-file list (receipts.json, S057–S061.txt,
  fetch_sources.py) and keeps screened material in `.ufo/waves/round-31/screened/`, outside it.
- wave-1 CriticRoutedDispositions.md re-ran the declared command at D=C=a16602a: exit 0. Matches
  the lesson's citation.
- Receipt closure-command-check.txt (5 lines) reproduced in clone2 (own commits on branch r2demo):
  exact-file a16602a..a16602a → 0; dir form + added sources/screened/x.txt → 1; exact form +
  same addition → 0; exact form + altered S057.txt → 1. All four observed values match the receipt.

## Row 3 — partial reports not marked

- round-30-verifier-spotcheck.md:176-187 says verbatim: 34 seats, 15 returned, 19 cancelled,
  20 reports committed, "Which 5 are partial is not marked." Exact.
- .ufo/waves/round-30/w2/partial-reports.json: 20 entries, statuses {complete: 15, partial: 5};
  ScoutR30PartialReports.md documents the two-signal method and agrees with the L1 count.
- w1/seat-status.json exists: 33 seats, counts {dead-at-spawn 18, returned 13, refused 1,
  returned-after-safety-filter 1}. PARTIAL: first-line rule present in w1-spec.json, w1-dispatch.json
  and, at tip, in w2-spec.json and w2-dispatch.json (1 hit each).
- Gap: the `<wave>` template promises a w2 seat-status.json; it does not exist at fde133a or
  92235a0 (tip adds only w2-dispatch.json, w2-spec.json, three after-receipts, SCORECARD).
  Wave 2 is in flight, so this is a commitment, not yet a defect — but the row states it in the
  present tense.

## Row 4 — dead route not planned for

- w1/dead-seats.json: 18 dead — executor 3, scribe 13, mutation-tester 2; 18/33 = 54.5% ≈ the
  row's 55%. Matches the row exactly; w1/seat-status.json corroborates 18 of 33.
- "Shown able to fail: wave 2 dead-seat count is recorded in its seat-status.json" — **not
  verifiable**: `.ufo/waves/round-31/w2/seat-status.json` exists at neither audited revision, and
  w2-spec/w2-dispatch contain no recorded end states. This is the only Mistakes-row able-to-fail
  claim with no artifact behind it. It also demonstrates bookkeeping, not a failing check.
- "the session route notice warned of it" (captured-by): evidenced only by the note inside
  dead-seats.json; I did not open the L1 transcript. Accepted on that receipt.

## Findings by severity

1. MODERATE — Row 4 able-to-fail cites `.ufo/waves/round-31/w2/seat-status.json`, absent at
   fde133a and 92235a0 (verified via `git ls-tree -r 92235a0 | grep seat-status`: w1 files only).
   Must land when wave 2 closes or the row overstates. Row 3's same template sentence is
   w1-only true today (minor).
2. MINOR — Row 1 "(N1–N6)": N4 is defined nowhere in round-30-verifier-spotcheck.md (0 grep
   hits); the closure routing itself uses N1,N2,N3,N5,N6. Reword to the explicit five labels.
3. MINOR — Row 1 "two victim repositories gained commits": receipts record `victimUnchanged:
   false`; commit-count gain is the probe design's implication, not a field I saw. Harm claim
   itself (victim changed) is solid.

## Not verified

- The session route notice itself (row 4 captured-by) — not opened in history.
- Lane content after 92235a0: the working checkout already contains a "Round-31 wave-2
  corrections" QUALITY section citing a2-w2 critic files not in 92235a0; my audit stops at the
  pinned revisions and does not judge those in-flight edits.
- No counters or selftests were run against the live lane; all executions were in my sandbox
  clones with TMPDIR set inside it.
