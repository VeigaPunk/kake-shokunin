# KakeR33.ReviewMistakeRow — review of round-33 lesson `## Mistakes` row at `0a0acfb`

Seat: KakeR33.ReviewMistakeRow (reviewer, leaf). Milestone r33-falsify. Axes: operability, freshness.
Sandbox: `/fast/scratch/hyaku/kake-r33/w2/ReviewMistakeRow/` (clone checked out at `0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0`; `TMPDIR=<sandbox>/tmp`).
Verdict: **reproduced** — the row's failing check runs and fails as claimed; no substantive defect found.

## Reproduction of the failing check (Fix column receipt)

```
git -C clone fetch -q clone/.ufo/waves/round-33/verification/hollow-r32-c2-6ffa03e.bundle \
  'refs/heads/hollow-r32-c2:refs/tags/hollow-r32-c2'   → exit 0 (bundle verified okay; requires a0b0dff)
git show 5b32cc7:.ufo/waves/round-32/c2_retained_count.py > r32_c2_counter.py
python3 -B clone/.ufo/waves/round-33/criteria/counter_control_check.py \
  --counter r32_c2_counter.py --repo clone --before a0b0dff --after e9283ec \
  --hollow 6ffa03ea9c1b094f04ddcf65da46903b7cd16c82   → exit 1
```
Output: `before met=0`, `after met=3`, `hollow met=3`, `FAIL: hollow commit scores the declared after-value 3`,
`c1BlobPaths` → `scripts/fixtures/unrelated/{a,b}.txt`, `c2RowIds ["S099"]`, `c3Cites {"S099": 1}` —
byte-identical to the retained receipt `.ufo/waves/round-33/verification/criterion-counter-control-r32-c2.txt`.
The contract ("a fix counts only once shown able to fail") is satisfied.

## Column checks

- **Class** ("a repair counter accepts a faked repair at its declared after-value"): accurate; the hollow commit reaches `met=3`, the r32 after-value.
- **Evidence**: all verified. Counter sha256 `48126fc5…` matches `w1/ScribeMistakeMine.md`'s cited hash; file is unchanged since `5b32cc7` (`git diff 5b32cc7..0a0acf` on it is empty). `git show 6ffa03e` confirms: blobs `d17ab7e5`/`ee0b6381` at `scripts/fixtures/unrelated/{a,b}.txt` (ls-tree), `+| S099 | ds4cc-marketplace 1fbdb8ed | x |…| 2026-10-22 | x | x |` under `## Registry`, `+S099 is unrelated to this entry.` in `render-web-services.md`. `met=3` at `e9283ec` and `6ffa03e`, `met=0` at `a0b0dff` (my run). Seat attribution `ScribeMistakeMine` correct (`w1/ScribeMistakeMine.md`); bundle exists and contains `6ffa03ea…`. "Closure re-measured C2 by hand": `corpus/lessons/round-32-verifier-spotcheck.md:61-62` ("the three conditions were re-measured without it") and its C2 heading "re-measured by hand".
- **Captured-by: none**: defensible, with a tension noted below. r32 w1 `MutC2Conditions.md` (M4–M8 survive at `met 3`) and `CriticC2Scope.md` (Finding 3: hollow `ea1050dd` → `met 3`) did observe it; the row's qualifier ("no rule required a counter to score a hollow control below its after-value before its `met` was read as evidence") is accurate — the round-32 QUALITY section contains only the time and guard-layer criteria; the nearest older rule (QUALITY, round-28 "reject a constant") does not cover a faked repair.
- **Fix**: `corpus/QUALITY.md` "Round-33 criteria" second bullet exists at `corpus/QUALITY.md:590-603` (hollow control below after-value) with check `.ufo/waves/round-33/criteria/counter_control_check.py`; the file exists and is the script I ran. Shown-able-to-fail receipt verified verbatim above.

## Paragraph about this round's counter vs `w1/MutC2HollowCommit.md`

- "bytes at an unrelated path drops c1 and therefore c4, so at most 2 of 4": `c2_pin_count.py` line ~135 makes `c4` conditional on `c1_retained`. Probed: `git mv .ufo/waves/round-33/sources/ds4cc-7fc6aa2f scripts/fixtures/r33-unrelated-moved`, commit `5d24f38a74072f5a15045872154ecb75719c4d70`; `python3 -B c2_pin_count.py --repo . --rev HEAD` → `met 2` (c1 F, c2 T, c3 T, c4 F). Matches.
- "a different hollow shape still scores 4": the report's three `met=4` rows are exactly a junk S065 row + copied metrics (`d1bb9b0`), a misplaced section (`528717b2`), and an even-backslash pipe (`8fc8ecb`) — all three named in the paragraph.
- "checks provenance shape and truth of stated numbers… not that the row's prose came from source study": matches report lines 5 and 26–27.
- "independent draft matched it cell for cell": `w1/ScribeS065RowDraft.md:34` — "cell-for-cell identical to it after trailing-space trim (`diff` empty)".
- The same recipe-shaped hollow run through the landed check on the r33 counter: `--hollow 5d24f38a` → `PASS, hollow=2 < after=4, before=0` (exit 0). The r33 counter satisfies the criterion's recipe; the score-4 shapes above are outside that recipe, which the paragraph itself discloses.

## Findings

1. **(Low)** `counter_control_check.py:4` docstring usage names the script `check_counter_control.py`; the landed filename is `counter_control_check.py`. Copy-paste of the usage line fails; the QUALITY.md check line uses the correct name.
2. **(Low)** The landed fix's only retained run is the exit-1 receipt vs the r32 counter; there is no retained PASS receipt for `counter_control_check.py`. The contract requires only able-to-fail, so compliant; a passing-direction receipt (e.g. my `--hollow 5d24f38a` run) would strengthen it.
3. **(Noted, not a defect)** The criterion's hollow recipe covers only the recipe shape (unrelated path + fabricated id + unrelated mention). MutC2HollowCommit's score-4 hollows (correct `S065` id at the pinned path, copied metrics, misplaced/duplicated context, even-backslash row) remain uncaptured — accurately disclosed in the row's own paragraph, and the r33 counter does pass the check on a recipe-shape hollow.

## Not verified

- r32 w1 reports are untracked files read from the lane working tree (per the task's explicit pointer); nothing in the checked-out tree depends on them.
- Did not re-verify upstream byte identity of the four ds4cc blobs (sibling surface; report line 22 says they were not forged).
- No tools installed; no live requests; no lane mutation besides this report.
