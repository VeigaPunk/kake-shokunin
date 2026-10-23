# ReviewC2RepairFixtures — are the five 528a6d02 selftest fixtures contract-grounded?

Seat: KakeR37.ReviewC2RepairFixtures (leaf, wave 2 falsify; axis operability). Sandbox
/fast/scratch/hyaku/kake-r37w2/ReviewC2RepairFixtures/ (clone at 79d3c780, TMPDIR inside it).
No lane writes besides this file. Nothing installed. No network. No processes left running.

## What I attacked
The statement in corpus/lessons/round-37.md:114-118 and in w1/ExecC2Fixtures.md:20 that the five
fixtures added at 528a6d02 come from the round-36 contract (SCORECARD.md:1563-1660, "Round 36 —
declared claims", C1 contract), not from E1's behaviour. Also checked against the inputs in
w1/RevengerSurvivors.md.

## Commands (all exit 0)
1. `git diff 621fb528 528a6d02 -- scripts/source_recheck_selftest.py`: exactly 5 `add(...)` blocks
   added (b12, b13, c11, c12, f17) and nothing else changed. Fixture count goes 101 → 106.
   `git diff --stat 528a6d02 79d3c780 -- scripts/source_recheck_selftest.py` is empty. Selftest
   sha256 is 9a554004…a8e3, the same as ExecC2Fixtures.md:48.
2. `timeout 600 python3 -B probe.py E1.py E1h.py E2.py M07.py M08.py M09.py M11.py M24.py X1overrun.py`
   (probe.py sha256 362f43de…4755). It imports the selftest's FIXTURES and judges with the
   selftest's own `run_case`. The **independent oracle** uses only the stdlib, not E1 or E2 code:
   `urllib.parse.urljoin` (RFC 3986 §5.2) for (b); for (c), a regex for comments, raw-text
   elements and tags plus `html.unescape`; for (d), NFKC and `isspace` deletion.
   Tool shas: E1 577b2d7d… (4d5b3d55), E1h 37a8a8ef… (hardened tool at 528a6d02), E2 a5176fee…
   (1a16b8e3), M07 e06ee963…, M08 3d6713dd…, M09 aba84e1d…, M11 00d17e22…, M24 eaac16cc….
   X1overrun is my sandbox-only change to E1: in `moved_target`, `range(end)` becomes
   `range(min(end+1, len(hops)))`, so it resolves one hop past the permanent run.

## Per fixture: contract sentence → derived expectation → fixture → verdict
- **b12** (selftest.py:340-346). Contract (b): "Each location is resolved against the URL that hop
  answered (the check url for the first hop, then the previous resolved location) … the target is
  the resolved location of the last hop of that leading permanent run." Derivation: url
  …/dir/page; `next/step` resolves to …/dir/next/step; `final` resolves to
  https://example.com/dir/next/final. The final hop is 200 and the quote is present, so the only
  finding is moved, with exit 1 and failed-policy. Oracle: same target. Fixture: same. **Agree.**
  M07 gives …/dir/final and fails this fixture.
- **b13** (347-353). Contract (b): "by RFC 3986 section 5.2, with no further normalization".
  Derivation: §5.2.2 computes remove_dot_segments(merge(`/dir/page`, `../final`)), which is
  `/final`. So moved https://example.com/final, exit 1. Oracle: same. Fixture: same. **Agree.**
  M08 gives …/dir/../final and fails.
- **c11** (403-408). Contract (c): "comments removed (`<!--` to the next `-->`)" happens before
  "every remaining tag removed". Derivation: `<p>ok</p><!-- x > hidden note -->` becomes `ok`;
  the quote "hidden note" is missing, so quote_missing, exit 1. Oracle: holds=False. Fixture:
  same. **Agree.** M09 exits 0.
- **c12** (409-415). Contract (c): "every remaining tag removed (`<` followed by an ASCII letter,
  `/` or `!`, up to the next `>`)". Derivation: `<b>Hel</b>lo world` becomes `Hello world`; the
  quote holds, so clean, exit 0. Oracle: holds=True. Fixture: same. **Agree.** M11 exits 1.
- **f17** (553-559). Contract (f): "decoded in that encoding with the mark dropped, whatever
  charset says". Contract (d): NFKC, then delete `isspace()` characters. Derivation: the text is
  "Hello world" with no U+FEFF. The quote keeps U+FEFF, because NFKC leaves it unchanged and
  `'\ufeff'.isspace()` is False (both observed). The normalized quote is not a substring, so
  quote_missing, exit 1. Fixture: same. **Agree.** M24 exits 0.

Judged runs: E1, E1h and E2 pass all 5. Each mutant fails only its own fixture: M07 fails b12,
M08 b13, M09 c11, M11 c12, M24 f17. Matches ExecC2Fixtures.md:34-42 and
verification/c2-evidence-at-528a6d02.json (fixtures 106, valid 106, killed 32, survivors []).

## Against RevengerSurvivors' independent inputs
The same structure in every case, with different strings:
- M07: a relative hop-2 location (`three` there, `final` here).
- M08: `../top` versus `../final`.
- M09: `<!-- >PAYLOAD -->` versus `<!-- x > hidden note -->`. Both avoid the false killer
  `<!--q-->`.
- M11: a tag splitting the quote (`PA<b>YLOAD` versus `<b>Hel</b>lo world`).
- M24: a quote holding U+FEFF. text/plain there, text/html here; the result is the same.
Agree on all five.

## Findings (by severity)
- LOW, b13 confound (selftest.py:349,353 with NON_REDIRECT_LOCATION="/final" at :93). The
  expected target https://example.com/final is also what you get by resolving the benign `/final`
  location of the 200 hop. X1overrun gets that target wrong in general yet **passes b13**, so b13
  alone cannot tell "last permanent hop" from "one hop too far". The defect is still caught in the
  set: X1overrun fails b12 (observed). b13 still kills M08. A distinct target (for example
  `../top`) would remove the overlap.
- INFO, not blind, already disclosed (ExecC2Fixtures.md:54-59). The inputs were chosen by reading
  E1 and the mutant diffs. "Expectations were written from the contract before either tool ran"
  (ExecC2Fixtures.md:20) has no timestamped pre-run receipt, so it is **unverifiable**. This does
  not matter much, because my independent oracle reproduces every expectation from the contract.
- INFO: f17 rests on Python's `isspace`/NFKC treatment of U+FEFF. Contract (d) names Python
  `str.isspace()` explicitly, so the reading is contract-grounded, not E1-specific.

## Verdicts
- "Five fixtures are grounded in the round-36 contract text": **holds** for all 5. In each case
  the contract sentence, the derived expectation and the fixture agree.
- "Each named for its contract sentence" (round-37.md:115): **holds**. The `contract` field is
  CONTRACT["b"], ["b"], ["c"], ["c"], ["f"], and the names describe the rule.
- "C2 27 → 32 of 32, 106 valid on E1 and E2": **holds** at fixture level (5/5 on E1, E2 and E1h;
  each survivor killed by its own fixture). I did not rerun the full c2_mutkill counter or its
  bwrap jail; that belongs to RerunC2Evidence.
- "RevengerSurvivors independently found the same five distinguishing inputs" (round-37.md:117):
  **holds** in structure; the strings differ.
- "Expectations written before either tool ran": **unverifiable**.

Residual risk: the oracle is my own reading of the contract. urljoin matches RFC 3986 on these
inputs, but it is not a strict RFC 3986 implementation in general.

Report: .ufo/waves/round-37/w2/ReviewC2RepairFixtures.md
