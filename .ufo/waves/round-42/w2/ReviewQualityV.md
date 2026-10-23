# Wave 2 — ReviewQualityV — attack: harm-rule criterion check (QUALITY (v) candidate)

VERDICT: FOOLED-AS-GATE, SOUND-AS-SMOKE — `harm_rule_check.py` returns the correct exit codes on both real
rounds (41→1, 42→0), but as a lexical gate it is bypassable in both directions: two synthetic false passes
and two synthetic false negatives demonstrated below.

Target: `.ufo/waves/round-42/criteria/harm_rule_check.py`
sha256 `df32595dcd60558188eb29095d479349c6a62658a10637242054a936ea9422b1` (312 lines). No tools installed.

## Real rounds (exact commands, exit codes)

1. `git -C …/kake-shokunin show 1ef7a0e9:SCORECARD.md > sandbox/r41_SCORECARD.md`
   `python3 -B harm_rule_check.py - 41 < r41_SCORECARD.md` → **EXIT=1** (expected 1). Judged bullet lines
   2746-2748: "must be red on `8eb121c8`" — no guard word, no numeric bound → genuine miss, faithful.
2. `python3 -B harm_rule_check.py /home/vgpnk/Projects/shokunin/kake-shokunin/SCORECARD.md 42` → **EXIT=0**
   (expected 0). Judged bullet lines 2976-2987 (lane SCORECARD sha256
   `fa64e5ee07a70e53a0090ddf536a9346459698347c7bb7d372bb8a71d9b3921b`): "guards only" (2978),
   "no change fixture" (2979), "red on `50287ac6…`" (2979), "green on" (2981), "each ≤ 2.0" (2983) — real
   statement, faithful pass. Both real-round verdicts: **holds**.

## Synthetic probes (sandbox /fast/scratch/hyaku/kake-r42w2/ReviewQualityV/)

| probe | file (sha256 8 chars) | should be | check says | result |
|---|---|---|---|---|
| A vacuous rule | probeA_vacuous.md `817ab6be` | FAIL | EXIT=0 pass | **fooled** |
| B legit rule, plain words | probeB_legit_twice.md `28162d52` | PASS | EXIT=1 fail | **fooled** |
| C wrapped "guards only" + decoy | probeC_decoy_shadow.md `47d7301b` | FAIL (operative) | EXIT=1, operative bullet never judged | **fooled** |
| D one-line decoy shadows failing rule | probeD_decoy_oneline.md `6d9211ea` | FAIL | EXIT=0 pass | **fooled** |
| E operative rule of D, alone | probeE_operative_alone.md `9179b967` | FAIL | EXIT=1 fail | holds (control) |

- A: bullet "the audit tool guards only its own exit code … commits at most 0 times the round-40 budget,
  and the 4x grid below is internal" → classes via "guards only", cost via "4x" and "0 times". A bound of
  **zero** and an unrelated "4x" both satisfy (b); the check cannot tell a commitment from any
  `<digit>(x|times|s|ms)` token (`RATIO_UNIT`/`TIME_BOUND_SHORT`).
- B: complete rule — change fixtures "red on", guards "green on", cost "within **twice** the round-40
  tool's median" → EXIT=1. "twice"/"double" are not in the lexicon; a correct freeze in ordinary English
  is rejected.
- C: `line_hits` matches per line, so "guards\n  only" (Markdown wrap) yields no GUARDS_ONLY hit — a
  phrase split by line wrap loses its signal; also only `bullets[0]` gates, the second (operative) bullet
  is printed as "further" and never judged.
- D: same decoy on one line → EXIT=0 while its operative bullet alone (E) fails. A vacuous first
  "harm rule" bullet makes the whole round pass. **Strongest finding.**

## Findings

1. `harm_rule_check.py:241` (`bullets[0]`): only the first harm-rule bullet is gated; later bullets are
   advisory. A decoy bullet placed above the operative rule turns any fail into a pass (probe D). — wrong
   behavior for a gate; holds as stated.
2. `harm_rule_check.py:73-84`: cost bound is any `N times|x|×|ms|s|min` or `≤/at most N` token; no
   comparison to what is bounded, no minimum plausibility. "0 times", "4x grid", "at most 0" pass (probe A).
   — overstated as "numeric cost bound"; it is "contains a number-shaped token".
3. `harm_rule_check.py:120-133` (`line_hits` per-line matching): wrapped phrases ("guards⏎ only") are
   missed; continuation lines are joined only for display, not matching (probe C). False negative surface.
4. `harm_rule_check.py:56-71` (`pick_declared_section`): the section literally titled "C1 declared (frozen
   before the build is scored)" (lane SCORECARD.md:3057) is silently excluded — `pool[1:]` contains only
   other *pre-freeze* sections, so the "(other candidate ignored)" note never prints for it. Targeting
   pre-freeze is defensible (frozen-before-scoring is the point), but the output understates what was
   skipped. — holds; minor.
5. Real-round discrimination: r41 fail and r42 pass are both faithful to the bytes; the check orders the
   rounds correctly and reports matched text with line numbers for hand re-checking. — holds.

## Residual risk and verification gaps

- I did not fuzz `HEADING_RE`/round parsing (e.g. "Round 42" inside a fenced code block creating a phantom
  section); single hand-built probes only, all with plain `## Round 42 — … (pre-freeze …)` headings.
- The "ignored declared section" behavior was read from source and observed implicitly (no note printed on
  the r42 run); I did not construct a round where a declared-titled section alone contains the bullet, so
  its fail-direction behavior is unverified.
- Verdict for the L1: keep as QUALITY (v) smoke evidence only (exit codes on real rounds are correct and
  reproducible); do not present it as proof that the frozen harm rule constrains anything — probes A/D are
  standing witnesses that a lexical pass is purchasable with one vacuous bullet.

Sandbox: /fast/scratch/hyaku/kake-r42w2/ReviewQualityV/ (5 probes + r41 snapshot, <10 KB). No lane file
other than this report was written; no git/jj mutation; all processes finished.
