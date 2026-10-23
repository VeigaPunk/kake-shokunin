# ReviewKillRuleRecord — wave 2a3, round 39 (leaf attack seat)

Reviewed the SCORECARD kill-rule (1) section at tip (HEAD `bb4a1e1`, master `bb4a1e1e4ffa4757bde8275764a8526659a9ed8c`; line 2442+ per `grep -n`) against the frozen declaration at `ceecb1b1` (SCORECARD.md:2385-2403) and the a3 receipts. No subagents; no counter run; receipts read only via `label/passed/met/toolSha256/counterSha256/keySha256` (never `rows`/`why`). No tools installed.

## Statements attacked

**S1 — every receipt cited in the section exists, says `met: true`, and carries the frozen hashes — holds.**
Commands: `jq -rs '{...}' .ufo/waves/round-39/verification/a3/*.json` (exit 0), `for n in …; do test -f "$n.json" …` (exit 0). All 16 cited met receipts exist (NamespaceBinding cited as `w1a3-MutNamespaceBinding__M0x`, actual filenames carry suffixes, e.g. `__M02_root_trailing_slash.json` — unique, fine), all `met:true`. All 77 receipts carry `counterSha256` `f3a0cd60…4593` and `keySha256` `16440f62…7c10b` (jq aggregate: 77/77). `v21-A.txt`/`v21-B.txt` echo the same counter SHA.

**S2 — counts: 15 of 54 mutants scored, controls' totals — holds (with one duplicate-image note).**
jq aggregate over the 77 receipts: `mutants=54`, `mutantsMet=15`; met mutants exactly
EntryNumbering M02; NamespaceBinding M02,M03,M04,M07,M08,M09,M10,M11; StdlibSubstitution M09; UrlAuthority M03,M04,M05,M09,M10 (labels match the table). Controls: RegexTweak 24/met, GuessTweak 23, HandTokenizer 23, StdlibConvenience 21, XsdTweak 20, HtmlParserReader 20, StructureOnly 16, ValuesOnly 14, EngineLenient 14; ref 24/met; dead Controls: RegexOnly 19, XsdDelegate 19, ConstClean 5, ConstClean_manifest_only 6, ConstError 4, ConstFindings 1, FirstFinding 12, Junk 2, LabelIds 7, NoReader 5, ShallowStdlib 13, CodeGuess 23; `at-915e9e87` 0. NOTE: two of the 54 scored mutants are byte-identical (`toolSha256` `4deee24e…` for `MutNumericBoundaries__M06` and `MutStdlibSubstitution__M04`, both passed 23) — 54 receipts, 53 distinct mutant tools. The 15 met receipts are all distinct; the kill rule is unaffected.
Exit-code cross-check: `cat *.exit | sort | uniq -c` = 17× `0`, 60× `1` — matches met(17 incl. ref)/non-met.

**S3 — no key/counter/predicate/target text changed between ceecb1b1 and tip — holds.**
`git diff ceecb1b1 master -- .ufo/waves/round-39/sealed_count.py .ufo/waves/round-39/c1-contract.md` → empty, exit 0. SCORECARD frozen bullets unchanged: `git diff ceecb1b1 master -- SCORECARD.md | grep -E '^-(Kill rule|Control classes|Order)'` → no matches (exit 1). Receipt `predicate` reads `met: passed >= 24 of 24 sealed cases` (from v21-A/B runs), matching the section's wording.

**S4 — kill rule (1) fired before any build is dispatched — holds.**
Order verified: ceecb1b1 author 02:09:27Z; w1a3 dispatch log line 1: 06:52:48Z, 32 seats (`w1a3-dispatch.json`: spawn 32); kill-rule receipts committed 06:59:44Z (4c080d3, 26 receipts); wave-1 additions 07:01:41Z (57bdd80, 37 receipts); j-check v2.1 07:03:37Z (77b2a86); w2a3 (build seat present in `w2a3-dispatch.json` registry members) committed 07:40:23Z (bb4a1e1). All control evidence precedes the wave-2 dispatch. NOTE: the section's recorded times (06:59Z, 07:05Z, 07:12Z) postdate the corresponding evidence commits by ~2–9 min; ordering still holds — loose timestamps only.

**S5 — the six-mutant table and "9 more reference mutants" — holds.**
Received `toolSha256` prefixes match the seat report hashes for all six (e.g. M03 `f867398ec86b…` report `w1a3/MutUrlAuthority.md:19`; M10 `aa54ad12ffc5…` at :26) and descriptions match ("sitemapUrl empty port"→ sentence 4, "loc userinfo"→22, "IPv6 literal"→22, "fragment"→4, "trailing /"→25). MollEntryNumbering M02 → sentence 11 (`/fast/scratch/hyaku/kake-r39a3w1/MutEntryNumbering/mutants.json`: "sentence 11; foreign children remain ignored for findings"), matching the table's "11/33". Of the 15 met mutants, 6 committed at 4c080d3 (5 UrlAuthority + EntryNumbering M02) and 9 at 57bdd80 (8 NamespaceBinding + StdlibSubstitution M09) — "nine more reference mutants" verified.

**S6 — regex shortcut control characterization — holds.**
`sha256sum a3-controls/w1a3/CtlRegexTweak.py` = `2d941dab16fb…` = receipt; no `xml`/`html` import (`grep -nE '^\s*(import|from)\s+(xml|html)\b'` → exit 1); the materialized `w1a3-materialized/CtlRegexTweak.diff` (a/control.py → b/control.py) has 25 added + 14 removed = 39 changed lines; its base `a3-controls/dead-w1/CtlRegexOnly.py` hashes to the dead-seat receipt `b7667eaf…` (19). Checksum bindings also verified for CtlEngineLenient (`56652e5d…`, report `w1a3/CtlEngineLenient.md:3`), StructureOnly, ValuesOnly.

## Findings
- F1 (minor): two of 54 scored mutant receipts are the same bytes (`w1a3-MutNumericBoundaries__M06` == `w1a3-MutStdlibSubstitution__M04`, toolSha256 `4deee24e…`), so the "15 of 54" counts receipts, not distinct tools; no impact on the kill rule.
- F2 (minor): "recorded/07:05Z/07:12Z" timestamps postdate their evidence commits (06:59:44Z / 07:01:41Z / 07:03:37Z) by a few minutes; ordering claims still hold.
- F3 (note): "refused seat's leftover file" is real (`/fast/scratch/hyaku/kake-r39a3w1/CtlStructureOnly/control.py`, 7180 B, 03:55Z — matches the dispatch-log refusal at 06:55:29Z, trailing the refusal by 4 min).

## Residual risk / verification gaps
- `MutCcCheckV2` "8 of 16" and the v2.1 selftest fixture counts are quoted from `w1a3/MutCcCheckV2.md` (row lines 21-30) — the run artifacts (`*-results.json`) live under /fast/scratch; not re-executed (out of scope, and the counter/ceals remain untouched).
- Receipt `rows`/`why`/case content never read; the 24-case key itself never inspected; that is by design.

## Verdict
All five primary claims hold. Findings F1–F3 are minor factual notes; none contradict the kill rule (1) firing (C1 exploratory) or the "15 of 54 / controls' totals" counts.
