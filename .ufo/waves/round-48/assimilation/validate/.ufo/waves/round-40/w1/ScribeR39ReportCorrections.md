# Round 39 report correction spot-check

Axes: operability. Read-only re-derivation from committed lane bytes; no control was built or scored.

## Appended correction text

1. Correction: at `565ef4c9`, `git -C /home/vgpnk/Projects/shokunin/kake-shokunin ls-tree -r --name-only 565ef4c9 scripts/ | grep -c sitemap_audit` outputs `2` (`scripts/sitemap_audit.py`, `scripts/sitemap_audit_selftest.py`), while `git -C /home/vgpnk/Projects/shokunin/kake-shokunin ls-tree -r --name-only 565ef4c9 scripts/ | grep -cx scripts/sitemap_audit.py` outputs `1`, so the broad match includes the selftest and the exact tool-path count is one.
2. Correction: at committed tip `f043c72146ddb7e3bb1c64d26fd5ae2b01b508f8`, `git -C /home/vgpnk/Projects/shokunin/kake-shokunin ls-tree -r --name-only f043c72146ddb7e3bb1c64d26fd5ae2b01b508f8 .ufo/waves/round-39/w1a3/ | grep -E '/Ctl(EngineLenient|GuessTweak|HtmlParserReader|RegexTweak|StdlibConvenience|XsdTweak)\.md$'` outputs six reports (`CtlEngineLenient`, `CtlGuessTweak`, `CtlHtmlParserReader`, `CtlRegexTweak`, `CtlStdlibConvenience`, `CtlXsdTweak`), while `git -C /home/vgpnk/Projects/shokunin/kake-shokunin ls-tree -r --name-only f043c72146ddb7e3bb1c64d26fd5ae2b01b508f8 .ufo/waves/round-39/a3-controls/w1a3-materialized/ | grep -E '\.diff$'` outputs three diffs (`CtlGuessTweak.diff`, `CtlRegexTweak.diff`, `CtlXsdTweak.diff`), so six critic seats—not seven—returned source/diff handoffs.
3. Correction: at committed tip `f043c72146ddb7e3bb1c64d26fd5ae2b01b508f8`, `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show f043c72146ddb7e3bb1c64d26fd5ae2b01b508f8:.ufo/waves/round-39/w2a3/MutCriterionO.md | grep -Fc 'SCORECARD.md:'` outputs `7` and `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show f043c72146ddb7e3bb1c64d26fd5ae2b01b508f8:.ufo/waves/round-39/w2a3/MutCriterionO.md | grep -Ec '\| P(39|40) / 0 \|'` outputs `5`, so five of seven adversarial negatives were false accepts, not five of all 15 prepared SCORECARD samples.

## Evidence and scope

- Spot-check corrections at committed `corpus/lessons/round-39-verifier-spotcheck.md:162-166` all hold; no spot-check error found.
- Provenance: tool-path counts use `565ef4c9`; critic handoffs, materialized diffs, and MutCriterionO use lane tip `f043c72146ddb7e3bb1c64d26fd5ae2b01b508f8`.
- Relevant claims: `.ufo/reports/round-39/kake.md:59,131-132,144-145`; handoff reports under `.ufo/waves/round-39/w1a3/`; false-accept rows in `.ufo/waves/round-39/w2a3/MutCriterionO.md:29-39`.
- Handoff classification: the six named reports contain three static-source handoffs and three diff handoffs; `CtlValuesOnly` and `CtlHandTokenizer` instead report built controls/self-tests, and committed `w1a3-dispatch-log.txt:4` records `CtlStructureOnly` refused. The materialized directory contains only the three listed diffs; this count is not evidence that six files were materialized there.
- Read-only query batches were bounded by `timeout 30s prlimit --as=4000000000`; successful count queries returned the outputs above (exit 0). No build, test suite, counter, key, reference implementation, judge, network, or installation was used.
- One initial denominator grep used unescaped backticks and triggered shell command substitution; its `0` result was discarded, and the fixed-string query above returned seven rows. No other result was inferred from that attempt.
- Touched surface: this report only. The round-39 report, product code, lane Git index/state, and shared files were not modified.
- Out of scope: changing the original report, running a gate or counter, scoring a control, or making a round verdict.

Artifact: `.ufo/waves/round-40/w1/ScribeR39ReportCorrections.md`
