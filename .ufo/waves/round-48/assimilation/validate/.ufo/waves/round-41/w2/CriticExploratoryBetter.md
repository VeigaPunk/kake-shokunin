# CriticExploratoryBetter — round 41 wave 2
Axes: operability (reviewed); freshness (not evaluated; no network).
Conclusion: **not better as a harm-none operability move in its landed form**. The intended URL rule improves substantially, but a previously rejected malformed URI now becomes clean. This is a fixable defect, not a necessary tradeoff or a round/admission verdict.

## What I checked
Read SCORECARD Round 41, the round-39 contract, verification/build and relevant verification/pre receipts, w1/ExecIndependentBuild.md, w1/ReviewReferenceDiff.md, and the base-to-build tool/selftest diff.
Source identity in the live probe: base 4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e; build 0b485431d96268d46c8dc9052eec92520248a03989896bd83f4521f15f13edbf.
Exact primary commands (cwd /home/vgpnk/Projects/shokunin/kake-shokunin):
```sh
timeout 30s prlimit --as=4000000000 git diff 8eb121c81ffebada064eefcabcd94dd2303d646f eae5ae2c7dc5de2ba489f02b936fc5040b07b7d6 -- scripts/sitemap_audit.py scripts/sitemap_audit_selftest.py
timeout 60s prlimit --as=4000000000 python3 -B /fast/scratch/hyaku/kake-r41w2/CriticExploratoryBetter/probe.py
```
Both exited 0. The probe reads exact Git revision bytes, verifies the oracle wheel hash, checks RFC grammar, and runs twelve CLI invocations with bounded, temporary sandbox fixtures; their individual exits are below. An earlier bounded module-only probe found the same three whitespace cases and confirmed the caret fix; the CLI reproduction is the decisive check.

## Counterexample and findings
**Medium — new false-clean URI acceptance**, scripts/sitemap_audit.py:80,92-95 (callers :304-310 and :382-384).
Input `http://[::\t1]/a` contains an actual TAB; LF and CR produce the same regression. The RFC 3986 oracle rejects all three, as does the round-40 tool. The build's bracket branch accepts them, then urlsplit silently deletes the whitespace and sees host `::1`.
For loc, use `<loc>http://[::&#9;1]/a</loc>` with sitemapUrl `http://[::1]/a`; use character references 10 and 13 for LF/CR. These interior characters survive sentence-21 stripping.
For sitemapUrl, put the actual character in the JSON string and use the canonical IPv6 URL in loc.
Observed for each of TAB, LF, CR:
- loc: base exit 1, failed-policy, loc_not_absolute; build exit 0, clean, no findings.
- sitemapUrl: base exit 2, could-not-evaluate, check_invalid; build exit 0, clean, no findings.
This is six end-to-end regressions. The former global TAB/CR/LF guard was removed; merely delegating IP-literal parsing back to urlsplit does not preserve the base's behavior.

**Low — evidence scope cannot establish final-build parity**, SCORECARD.md:2797-2807.
ReviewReferenceDiff.md:7-8,25 reviewed reference 6d7c2dd4 with its own IP-literal validator, not landed 0b485431. ExecIndependentBuild.md:9-13 uses another parser, stricter IP/Unicode rules and different port handling. Its 31,528-value differential is useful independent feasibility evidence, not a differential of the landed build.
The selftest's only new literal-host case is positive (scripts/sitemap_audit_selftest.py:942-945); no new malformed bracket-whitespace case guards the removed global check. Counter v1 host mutations use reg-names (c1_count.py:132-140); v2 does too (c1_count_v2.py:158-164).

## Checked statements
- Prior state lacked RFC character/percent/component validation: **holds**. verification/pre/base-8eb121c8.json:4,14-24 records 1049/1434; losses span five components, not just ports. The diff and ten red fixtures corroborate real missing work.
- Landed build improves the measured URL rule: **holds**. verification/build/c1-v1-at-eae5ae2c-41001.json:4-12 records the exact build at 1434/1434; the random v1 and v2 build receipts also record 1434. These are read receipts, not counter reruns by this seat.
- All 198 fixtures pass at build, with ten failures at base: **holds as recorded**, verification/build/selftest-on-build.txt:1-2 and selftest-on-base-8eb121c8.txt:1-12. Four positive additions and the port-letter parity guard are not new wins. The full suite was not rerun.
- Every new fixture must be red on base (SCORECARD.md:2746-2747): **wrong literally**; the retained base receipt is 188/198, not 183/198. The later paragraph accurately records ten reds.
- IP-literal behavior stays exactly as base (SCORECARD.md:2799-2800): **wrong**, demonstrated above. Excluding literal contents from measurement does not make this unchanged legacy behavior.
- Broad as-written RFC conformance / no operability regression: **overstated**. The measured class improves; the independent CLI counterexample prevents a harm-none conclusion.
- Real-run equality: supplied evidence reports it; this seat did not rerun or rehash it. It cannot exclude the demonstrated malformed-input regression.

## Smallest safe correction
Retain the old global TAB/CR/LF rejection before the new regex (or exclude those three characters from its bracket branch). Add the six loc/manifest regression cases above while preserving sentence-21 edge stripping. Do not adopt a new IP-literal grammar or the independent parser merely to fix this regression. L1 should run the updated selftest and retained real-run check after correction; no correction was applied here.
No tool installs/upgrades. Only this report and a 3.5 KB sandbox probe were written; temporary fixtures were cleaned, all child processes exited, and no services were started.
