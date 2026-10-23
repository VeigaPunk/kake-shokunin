# ReviewShortcutDisposition — kake r37 wave 2 (falsify), operability

Attacked: SCORECARD `79d3c780` lines 1949-1972 (shortcut follow-up disposition, `ccc3b2b9`), the
selftest figure at line 1990, and the capability row's evidence clause at line 2009. Tool
`retained/controls/CtlC1Shortcut-followup-robots_audit.py`, sha256 `61724ead…6f7d` (matches the
disclosed pin). Sandbox `/fast/scratch/hyaku/kake-r37w2/ReviewShortcutDisposition/` (clone at
`79d3c780`), Python 3.14.8, TMPDIR in sandbox. Installs: none.

## Commands (exit codes)
1. `python3 -B scripts/robots_audit_selftest.py --tool <T>` on the shortcut → 1, **126/131**; landed
   `scripts/robots_audit.py` → 0, 131/131; `CtlC1NaiveReader` → 1, 119/131. The shortcut fails
   b09, b10, c10, d07, d13, the same 5 cases as `verification/robots-selftest-on-CtlC1Shortcut-followup.json`.
2. `sealed_count.py --root . --tool-file <V> --key-revision 424aa248` on the shortcut and on ablations
   built by `make_variants.py` (one patch removed per variant) → shortcut 28 (exit 0); noS1 24,
   noS2 24 (b1-b4 fail); noS5 24, noS6 24 (e1-e4 fail), all exit 1; **noS3 28, noS4 28, noS3S4 28 (exit 0)**;
   noAll 20 (exit 1). Receipts: `cnt/*.json` in the sandbox.
3. Selftest on the ablations: noS1 125, noS2 125, noS3 124 (b16, b17), **noS4 126 (same as the
   full shortcut)**, noS5 124, noS6 125, noAll 119, noS3S4 124.
4. `probes.py` (sha256 `df8251f4…`): 9 contract-derived checks whose `expect` is the contract
   decision → exit 0. Landed tool 9/9 clean; independent implementation 9/9 clean; **shortcut 3/9**;
   naive reader 3/9. The shortcut's errors:
   - P1 `user-agent: googlebot` with UA `googlebot-news` → blocked (stdlib substring match).
   - P2 `*: Disallow /admin` plus `Googlebot: Allow /` with UA `Googlebot-Image` on `/admin` → **exposed**.
   - P3 `Allow /abc` plus `Disallow /*` on `/abcdef` → blocked.
   - P4 `Disallow /private/` plus `Allow /*.html` on `/private/a.html` → **exposed**.
   - P5 `Disallow /*.php` plus `Allow /index` on `/index.php` (a tie, so allow wins) → blocked.
   - P6 `Disallow /a$b` → exposed (stdlib drops a rule with a non-final `$`).
   P3-P5 come from the stdlib ranking a wildcard rule by how much of the URL it matched (`m.end()+1`,
   `/usr/lib/python3.14/urllib/robotparser.py` `RuleLine.applies_to`), not by the rule's length.
5. P10 `user-agent: bot / crawl-delay: 5 / user-agent: other / disallow: /x` with UA bot on `/x`
   (contract: one group, so disallow): landed tool exit 0, shortcut exit 0, **noS4 exit 1 (exposed)**.

## Both sides
- Implementation: the shortcut never reads `expect`, ids, file names, or URL words. Every decision
  comes from the robots bytes. Each of S1-S6 copies a real contract sentence of (b) or (e). With all
  six removed it scores 20 (noAll, a true ablation of this file). The 3.14 stdlib does longest match,
  `*`/`$`, and group merging, so it is not a stub.
- Shortcut: the author lists "No group, precedence, wildcard, `$` or length code of mine" in
  `ctl/CtlC1NoReader-shortcut.md`, and steered the patches by the public per-case receipts and the
  ablation names. It hands (c) and (d) to a library that disagrees with the contract on 6 of 9
  ordinary-looking probes, in both directions, including `exposed` on realistic files (P2, P4).
  It skips the work the claim names, "the RFC 9309 decision under the lane readings", and the
  counter still reads 28 of 28.

## Verdicts
- "This control does not skip the claimed work" (line 1962): **overstated**. It skips the contract's
  (c)/(d) logic and still meets the predicate. Under the round rule ("a control that meets a
  predicate means that counter or target is wrong", lines 1892-1894), the disposition avoids that trigger
  by reclassifying the control rather than by showing it does the work. The limit sentence (lines
  1967-1972) does name substring UA, non-final `$`, and `*`/`$` length, so the gap is disclosed, not
  hidden. What the evidence supports: "the sealed cases cannot tell a stdlib-delegating tool from
  the contract on (c)/(d)".
- "six one-line patches, each copying one contract rule… without the six rule patches it scores
  20" (lines 1955-1965): **20 holds; the necessity framing is overstated**. Only S1, S2, S5 and S6
  are load-bearing for the counter. S3 and S4 can both go and the score stays at 28. S4 is a real
  contract rule (P10) that neither instrument sees: sealed b2 puts `crawl-delay` between
  `user-agent` and `disallow` (harmless for the stdlib), and selftest b13
  (`scripts/robots_audit_selftest.py:303`) uses `sitemap`, which the stdlib ignores for state.
- "on the shortcut follow-up 126/131" (line 1990): **holds**, reproduced exactly. But the selftest
  understates the shortcut's divergence: c09 (`robots_audit_selftest.py:360`) tests UA `googlebot`
  against group `googlebot-news`, the opposite of the stdlib's group-name-in-UA match. There is no
  fixture for `*` rule-length ranking, and none for crawl-delay between agents. P1-P5 and P10 all
  pass the selftest's blind spots.
- Capability row (line 2009): **holds for the landed tool** (131/131 and probes 9/9, agreeing with
  the independent implementation). Its evidence clause "at most 20 for the controls that skip
  rules" is **overstated**: it holds only because the 28/28 stdlib control was classified out, and
  the row does not mention it.

## Residual risk / gaps
- The probe expectations are my reading of the contract. Two independent contract implementations
  agree with it; I did not run the L1 private reference (`sealed/reference/ref.py`) on the probes.
- Selftest additions that would separate the stdlib (not mine to land): reverse substring UA (P1/P2),
  wildcard length (P3-P5), crawl-delay between agents (P10).
- All processes I started have exited; I wrote only the sandbox and this report.

Report: .ufo/waves/round-37/w2/ReviewShortcutDisposition.md
