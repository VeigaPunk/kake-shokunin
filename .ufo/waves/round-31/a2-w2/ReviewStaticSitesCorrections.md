# ReviewStaticSitesCorrections — routed defect 3 (falsify)

Axis: freshness. Attacked: the `## Round-31 corrections` section of
`corpus/knowledge/render-static-sites.md` (fde133a) against
`corpus/lessons/round-30-verifier-spotcheck.md` lines 113-117 and 271-276.

Sandbox: /fast/scratch/hyaku/kake-r31/a2-w2/ReviewStaticSitesCorrections/clone
(cloned lane, `git checkout -q fde133a`; all checks run in the clone).

## Verdicts

1. Append-only: PASS. `git diff f1ffb81 fde133a --
   corpus/knowledge/render-static-sites.md` is one hunk at line 137:
   23 insertions, 0 deletions; grep of the diff for removed lines
   (`^-[^-]`) = 0. The section header itself claims append-only and that is
   true.

2. Line 26 corrected: PASS. Physical line 26 contains "the only build-time
   setting it names besides" (the flagged clause spans lines 26-27; the
   correction quotes the continuing line-27 clause "the only build-time
   setting it names besides the branch is dependency installation" verbatim).
   The supersedes bullet asserts S049 also names the build command; S049.txt
   contains exactly one "build command" mention and the correction's quote
   "You can then include your own dependency installation as part of your
   site's build command." is an EXACT substring of S049.txt.

3. Line 53 corrected: PASS. Physical line 53 contains "normalized lowercase
   name". Routed options were "mark 'lowercase' [INFERENCE] or drop it";
   the append-only rules require an appended correction, and the supersedes
   bullet does both effectively: it quotes S051's actual text ("The header
   key is normalized and the value is appended to it to form the
   response:" — EXACT substring of S051.txt) and marks its own lowercase
   inference `[INFERENCE]`. S051.txt has 0 hits for "lowercase"
   (grep -ci = 0), consistent with the defect.

4. Quote exactness: PASS, all 5 typographic quotes in the section.
   quote 0 (S049 build command) — exact substring of S049.txt.
   quote 1 (S051 normalized) — exact substring of S051.txt.
   quotes 2-4 (S061 ANAME/ALIAS, A record 216.24.57.1, AAAA removal) —
   all exact substrings of .ufo/waves/round-31/sources/S061.txt.
   Verified with a Python substring check (UTF-8, curly quotes/apostrophes
   compared byte-for-byte after decoding), not just grep.

5. Routed defect 4 carried along: consistent. The S061 additions
   (ANAME/ALIAS, 216.24.57.1, AAAA warning) match spotcheck line 273-275's
   instruction to open configure-other-dns as a primary row.

## Findings

None. No defect found in scope.

## Residual risk / gaps

- The correction describes the S051 example keys as lowercase in its own
  `[INFERENCE]` clause; verified true (`cache-control`, `x-frame-options`,
  `referrer-policy` appear lowercase in S051.txt's quoted example).
- Quote attribution: all three S061 quotes come from round-31 sources (new
  fetch), S049/S051 from round-30 retained bodies. All sources present in
  the clone at fde133a.
- I did not re-fetch render.com (no live requests per bounds); verdicts
  rest on the retained `.txt` snapshots.
- Did not verify against the lane working tree, only commit fde133a as
  assigned; lane tip is 92235a0 but content files unchanged after fde133a.

## Commands run

- `git clone -q <lane> <sandbox>/clone && git checkout -q fde133a` — exit 0.
- `git diff f1ffb81 fde133a -- corpus/knowledge/render-static-sites.md |
  grep -c '^-[^-]'` — 0; `--stat` shows 23 insertions, 0 deletions.
- `grep -nF <each of 5 quote strings>` against S049.txt, S051.txt, S061.txt
  — all matched.
- Python exact-substring check over the section's 5 “...” quotes — 5/5
  exact in the attributed sources.
- `grep -ci lowercase S051.txt` — 0.
- `awk NR==26 / NR==53 render-static-sites.md` — flagged text confirmed on
  those physical lines.

Tooling: no installs; git/python3/awk/grep already present.
Report: .ufo/waves/round-31/a2-w2/ReviewStaticSitesCorrections.md
