# ReviewCounterC1Code — C1 counter code review (kake round 29, wave 1)

Axes: freshness (primary), operability.
Target: `.ufo/waves/round-29/c1_quote_truth.py`, sha256
`1b8225b570cb458e2ab765d49902651365105899b64327c8a562d0b98abc20d9` — identical for the lane
worktree copy and the `e58b66c2` blob; `git log e58b66c2..9e541a1 -- <script>` is empty, so the
code reviewed is the landed code. Python 3.14.8. No installs were needed (pacman untouched).

## Declared-revision runs (0/4 confirmed at both)
- `python3 -B .ufo/waves/round-29/c1_quote_truth.py --root . --revision fe1805cf32a7…` → exit 1,
  0/4, every check 0 (`/fast/scratch/hyaku/kake-r29/w1/ReviewCounterC1Code/fe1805.json`).
- Same for `e58b66c203be…` → exit 1, 0/4 (`…/e58b66c2.json`).
- Why 0/4 at `e58b66c2`: `git ls-tree e58b66c2` has no `corpus/knowledge/pages-base-path.md` and
  no `corpus/lessons/round-29.md`; `git show e58b66c2:corpus/SOURCES.md | grep S04` exits 1 (no
  registry rows). Sources/receipts ARE committed: all four blob sha256 equal `receipts.json`
  `textSha256` (verified: S040 625f2b07…, S041 86a77ee2…, S042 b66fefc1…, S043 d665dd23…).
  Consistent with the claim's before/after story.

## Findings (each reproduced in the sandbox battery; order a_row,b_entry,c_gate,d_sha)
- D1 (low, fail-open) — 8-line skip is positional, not header-aware. `entry.splitlines()[8:]`
  (script line "entry_body = entry.splitlines()[8:]") counts ANY line ≥ 9, so a 9-line metadata
  header leaks. Repro (battery commit "m2"): entry whose only id mention sits on line 9 of a
  9-line header, body empty → b=1 for all ids, 4/4, exit 0. Docstring intent "the metadata header
  alone does not count" is violated whenever the header is not exactly 8 lines. Mirror case
  (M2b): 7-line header with ids on the first real body line (line 8) → b=0, 0/4 (fail-closed
  off-by-one). Real entry not yet in tree, so no live impact today.
- D2 (low, fail-open) — registry lookup takes the FIRST line matching `^\|\s*S0xx\s*\|`
  (`row = next((l for l in registry.splitlines() if …), None)`). Repro (M8): stale valid
  `mined`/`2026-10-22` row placed above a canonical `rejected` row → a=1, 4/4, exit 0. Any later
  canonical row is ignored.
- D3 (low, fail-closed but self-flagging) — control over-fires on short quotes:
  `flip_letter` changes only the first alpha char and the check is `flip in text` (substring,
  no boundaries). Repro (M5b): quote "a" over text "request a" → all checks pass (4/4) yet
  `controlBroken=true`, exit 1. A future one-word Gate quote would spuriously report the counter
  broken. Also flips to lowercase regardless of original case (cosmetic). Planted-mutant case
  (M5, "alpha" vs "qlpha") proves genuine detection works: 4/4, cb=1, exit 1.
- D4 (low, fail-closed) — pipes/backticks in registry cells: any `|` in a cell before `opened`
  shifts the columns → a=0 (M1a: escaped `\|` inside the source cell). Pipes after `opened`
  are harmless (M1b: `|` in used-by → 4/4). Backticks alone are harmless (S041/S042 real quotes
  contain `|` and `•` and pass d). Net: parsing is naive split, but it fails closed.
- D5 (info, lenient) — `\bS043\b` matches inside hyphenated compounds: body "Citations: S0401
  XS041 S042x S043-yet" gives S043 b=1 (Mwb). S0401/XS041/S042x correctly rejected.
- D6 (info, fail-closed) — check c requires the gate line to contain EXACTLY one curly-quoted
  span: a second “…” fragment on the line voids the quote (M3: c=0). Straight ASCII quotes also
  void it (M4) — per spec, but authors must not add e.g. “GitHub Pages” to a Gate line.
- D7 (cosmetic) — missing `--root` reports `{"error": "revision not found"}` exit 2; message
  mislabels the cause.

## Positive verifications
- Happy path built from real e58b66c2 blobs + real receipts (11-column rows matching the real
  header `| id | source | … | status | opened | … |`: source=1, status=7, opened=8 — the tool's
  hardcoded indices are correct), 8-line header entry, `## Gate` lesson with one 5-word curly
  quote per id → 4/4, exit 0, control holds (battery.out "happy_base").
- Gate boundaries: quote line after a following `## Notes` is excluded (M9 c=0); `### Gate` and
  `## Gatehouse` do not toggle the section.
- sha path: `text_raw` bytes hashed directly; corrupted `textSha256` → d=0 (M6), localized.
- Bad revision → exit 2 JSON error (M7).
- Lane reads only: no lane file written except this report; all commits in sandbox clone
  `/fast/scratch/hyaku/kake-r29/w1/ReviewCounterC1Code/clone` (branch `battery`).

## Residual risk / verification gaps
- Checks b and c were validated only synthetically; the real entry and lesson do not exist at
  either declared revision, so the counter's pass path on the real artifacts is unverified until
  they land. D1's fail-open only matters if that real entry has a header ≠ 8 lines.
- `gate_lines` has no fenced-code-block awareness (a `## ` line inside a fence toggles);
  not reproduced, judged unlikely to matter for the authored lesson.
- Receipts `bodySha256`/`status` not re-fetched (live probes out of bounds); only the committed
  `textSha256`↔blob equality was checked.
- Battery harness: `battery.py` (sandbox), full output `battery.out`; M7b shows missing-root
  exit 2.

## Commands and exits (summary)
- in-lane counter runs: exit 1 (both revisions) — see JSONs above.
- `python3 -B battery.py` in sandbox → exit 0; table above in battery.out lines 3-19.
- `git show e58b66c2:…/S04x.txt | sha256sum` — 4/4 match receipts.json.
