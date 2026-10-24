# W2 RerunC1Counter — re-ran the C1 counter, diffed against L1 receipts

Axes: operability (counter reproducibility; judged axis), freshness (receipts vs landed bytes).
Verdict: **all five revisions reproduce field-for-field; zero mismatches.** One minor freshness
observation on receipt tracking (F1 below). No tool installs were needed (python3 3.14, git present).

## Setup
- Sandbox clone: `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin …/clone` then
  `git checkout -q 24a16474ee73e20453f3e1be9d2f33573c5196d9` → HEAD verified `24a1647…`.
- GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset; TMPDIR=/fast/scratch/hyaku/kake-r34/w2/RerunC1Counter/tmp.
- Receipts frozen at copy time into the sandbox and hashed (lane only read, never written).

## Runs (exit codes as observed)
`python3 -B .ufo/waves/round-34/c1_matrix_count.py --root <clone> --revision <rev>` (cwd=clone):

| revision | passed | constants (all rejected) | toolSha256 | exit | equal-to-receipt |
|---|---|---|---|---|---|
| 1e54c895 | 0/28 | true — clean 6/28, failed-empty 0/28, refuse 6/28, all-missing 1/28 | None (tool absent) | 1 | **YES** |
| d08d8de | 0/28 | true — same four gate counts | None (tool absent) | 1 | **YES** |
| 5613071 | 28/28 | true — same four gate counts | 8dd0018248e04d4e… | 0 | **YES** |
| 9ef758c | 28/28 | true — same four gate counts | 8dd0018248e04d4e… | 0 | **YES** |
| 24a1647 | 28/28 | true — same four gate counts | 8dd0018248e04d4e… | 0 | **YES** |

"Equal" = every top-level field identical (`counter`, `counterSha256`, `revision`, `tool`,
`toolPresent`, `toolSha256`, `matrixSha256`, `passed`, `total`, `byKind`, `constantGatesPassed`,
`constantGatesAllRejected`) **and** the full 28-case lists byte-equal as parsed JSON (sorted
comparison not needed — lists equal in order, n=28 each).

## Extra cross-checks (all pass)
- Counter+matrix pin: at my 24a1647 checkout `c1_matrix_count.py` = `fc72d855cde3656f…b71c51e` and
  `c1-matrix.json` = `246a6a3ba67a842c…6fac14f7`; `git show d08d8de:<same>` gives the identical
  pair of digests; `git log d08d8de..24a1647 -- <both paths>` is empty (no commits touched them).
- The counter self-enforces `MATRIX_SHA256=246a6a3b…` and exits 2 on mismatch; exit 2 never
  observed, so matrix bytes matched the pin at every run — independent of my sha256 check.
- toolSha256 vs blob: `sha256(git show <rev>:scripts/link_preview_audit.py)` equals the reported
  `toolSha256` at 5613071, 9ef758c, 24a1647 (same blob `8dd00182…` — tool unchanged since landing).
- Receipt inputs vs landed bytes: tracked receipts `c1-at-1e54c895/1c75a2ec…`→`61c123b6…`,
  `d08d8de`→`1c75a2ec…`, `5613071`→`fca7e53b…`, `9ef758c`→`97618ba4…` identical between
  `git show 24a1647:…` and my frozen copies.
- Note: gate counts are revision-independent (constant gates run fixed scripts over the same
  matrix), so identical counts across revisions are expected, not a copying artifact.

## Findings
- **F1 (minor, freshness, advisory):** `c1-at-24a1647.json` is **not tracked** at 24a1647
  (`git ls-tree 24a1647 -- .ufo/waves/round-34/verification/` lists only the other four receipts;
  `git show` of the path returns empty). It exists only in the lane working tree
  (sha256 `188c53a81da91dd1…37dfba8b93c`, which my frozen copy matches). My rerun equals its
  content field-for-field, so the receipt is honest; but as of the declared landed state the
  HEAD receipt has no committed bytes to verify against. Likely lands in the closure commit.
- No mismatch of any field at any revision; no other defect found in what this seat exercised.

## Not verified / gaps
- Receipts carry no exit-code field, so exit codes could not be diffed against receipts; I checked
  them against the counter's documented contract (source lines 130-184: exit 0 iff
  `passed==total and constantGatesAllRejected`, else 1; 2 unusable input) — observed 1,1,0,0,0 fit.
- No `lsp` server answers for the sandbox clone (plain checkout, no editor session); all
  definition/diagnostic conclusions above come from direct source reads of
  `clone/.ufo/waves/round-34/c1_matrix_count.py` (1-184) and runtime output, not from a language
  server — textual, not semantic proof.
- I did not re-derive the 28 matrix cases' correctness (out of scope; counter executed them as
  pinned data), and did not run the C2 counter (other seats' assignment).
- Known prior findings not re-reported: lookup-table tool passes 28/28; transcription commit
  passes C2 5/5 (disclosed by L1).

## Artifacts (sandbox, absolute paths)
- Clone: /fast/scratch/hyaku/kake-r34/w2/RerunC1Counter/clone (HEAD 24a16474ee73e20453f3e1be9d2f33573c5196d9)
- Rerun outputs: tmp/rerun-{1e54c895,d08d8de2,5613071e,9ef758c9,24a16474}.json (+ .stderr.txt),
  tmp/rerun-summary.json; frozen receipts tmp/c1-at-*.json (hashes in "Extra cross-checks").
- Commands all exited 0 unless printed otherwise above; comparison script exit 0 after fixing a
  receipt-filename map (receipts use 7-char shorts, `1e54c895` 8-char — first diff attempt crashed
  on that, rerun used saved outputs; no counter rerun was skipped).
- Lane files written: only this report. No pacman/install activity; no network fetches.
