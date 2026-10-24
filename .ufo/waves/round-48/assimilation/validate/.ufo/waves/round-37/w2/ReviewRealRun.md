# ReviewRealRun — round 37 wave 2 (falsify): live robots run

Attacked: the 55 expectations in `realrun/robots/manifest.json`, the lesson's "Real-input run" paragraph
(`corpus/lessons/round-37.md:102-110`) and the wave-1 claims behind it (`w1/ExecLiveRobotsSnapshot.md`).
Sandbox `/fast/scratch/hyaku/kake-r37w2/ReviewRealRun/` (clone at 79d3c780; harnesses `make_extra.py`,
`stdlib_decide.py`, `make_mutants.py`, `match_lines.py`; `extra/manifest.json` sha256 6492b2b8…c2c9). Python 3.14.8. No network, nothing installed, no lane writes except this file.

## Commands (all in the clone, TMPDIR set)
- `python3 -B scripts/robots_audit.py --manifest .ufo/waves/round-37/realrun/robots/manifest.json` → exit 0,
  `{"verdict":"clean","checksEvaluated":55,"findings":[]}`; the same on `manifest.strict.json` (exit 0). Tool sha256 5eb767ec…cabae = `9dbc88bb:scripts/robots_audit.py`.
- Body sha256 of all 12 `robots/*.txt` = `bodySha256` in all 55 checks; every one of the 71 quotes equals its recorded line byte for byte (0 mismatches).
- Live 55 on `CtlC1NaiveReader`, `CtlC1Shortcut-followup` and `retained/independent/independent_robots_audit.py`: all exit 0, clean, 55 evaluated. My pure stock harness (`RobotFileParser.parse(splitlines)` + `can_fetch`): 0 of 55 differ.

## Hand check (24 checks; group selection and every matching rule listed by `match_lines.py`, judged by me against the contract)
| # id | verdict | note |
|---|---|---|
| 1 rfc9309-html | holds | none of the 3 quoted Disallows is a prefix; the quote lists the whole rule set |
| 2 rerendered | holds | only match is line 3 (16 octets) |
| 7 youtube-partner-hub | holds | `/youtube/partner` is shorter than the rule `/youtube/partner/`; no match |
| 9 google-sitemap-xml | holds, quote irrelevant | the quoted line is a `Sitemap` record, which the contract ignores; the allow rests on the unquoted line 2 not matching |
| 10 account-login | holds | line 364 is the only match; no Googlebot group (grep: 0 `googlebot` lines in either file) |
| 11 search | holds | `/search$` anchored, exact |
| 12 gist, 13 raw-file | holds | 370 `/gist/`; 378 `/*/raw/` (`*` spans two segments) |
| 14 features, 15 repository-page | holds, quote insufficient | quote is only `User-agent: *`; the allow depends on none of the 165 rules matching (machine-checked: none) |
| 16 achievements-tab | holds | 361 Allow (33 octets) beats 522 Disallow (8 octets); no other rule matches |
| 17 docs-pages-landing | holds | `*` group with 0 rules |
| 21 sitemaps-protocol | holds | no user-agent record anywhere, so no group applies |
| 26 mdn-files, 27 mdn-media | holds | `/*/files/` matches `/en-US/docs/files/…`; `/media` is a prefix of `/media/` |
| 30 wiki-main-page | holds, quote insufficient | only `User-agent: *` quoted; the allow depends on none of 432 rules matching (none does) |
| 31 special-search, 35 api-query, 42 commit-snapshots | holds | single matching Disallow, quoted |
| 33 loesungkandidaten | expectation holds; justification wrong | decided by line 170 `…L%C3%B6schkandidaten/` (same `*` group, same normalized value), not by the quoted line 171 |
| 34 mobileview-api | holds | 149 Allow (29 octets) over 153 Disallow (3 octets) |
| 36 robotstxt-home | holds | the empty `Disallow:` never matches |
| 48 ds4cc-home, 55 veiga-deep-page | holds | `Allow: /` (both hosts were fetched under the w1 item's named owned-site exception, `w1-spec.json`) |
All 24 expectations are correct under the contract. Across all 55: 25 are decided by a quoted rule, 4 by the implicit `/robots.txt` allow (20, 47, 49, 53),
and 26 by no rule matching; in 4 of those 26 (9, 14, 15, 30) the quote does not carry the evidence.

## Extra checks: live files where the contract and Python 3.14 urllib.robotparser differ (expect = contract reading)
| id | file, UA, URL | contract (tool / independent) | stock stdlib | shortcut ctl |
|---|---|---|---|---|
| x1 | github, `baidu`, /search | disallow: `User-agent: *` (l.360) joins baidu (l.357), because `crawl-delay` (l.358) does not end a group | allow | ok |
| x2 | github, Googlebot, /marketplace/actions?tab=readme | disallow: l.392 (32 octets) beats l.362 Allow (26 octets) | allow (stdlib counts both as equal-length matches, so Allow wins the tie) | **allow (fails)** |
| x3 | github, Googlebot, /search? | disallow (an empty query is dropped) | allow (`?` kept) | ok |
| x4 | github, Googlebot, /search#results | disallow (fragment dropped) | allow | ok |
| x5 | wikipedia, `SemrushBot`, /wiki/Special:Search | disallow: l.148 `*` joins SemrushBot (l.129), because `Crawl-delay` (l.130) does not end a group | allow | ok |
| x6 | wikipedia, `wget-mirror`, /wiki/Main_Page | allow (no exact name match, so the `*` group applies) | disallow (substring match to the `wget` group, l.103) | **disallow (fails)** |
| x7 | wikipedia, Googlebot, /w%2Findex.php | allow (`%2F` ≠ `/`) | disallow (stdlib decodes `%2F`) | ok |
| x8 | github, `baiduspider`, /search | disallow (the `*` group applies) | allow (substring match to `baidu`) | ok |
Commands: `robots_audit.py` and the independent implementation → exit 0, clean, 8 evaluated. `CtlC1NaiveReader` → exit 1, 8 findings.
`CtlC1Shortcut-followup` → exit 1, findings x2 `exposed` and x6 `blocked`. The shortcut, which met 28 of 28 sealed cases, fails 2 of 8 on these live files.

## Mutation probe of what the live 55 can detect (single-point mutants of the tool, `mut/*.py`)
Caught by the live 55 (1 of 10): empty rule matches everything (exit 1, robotstxt-home/spec-page/orig/monster).
Not caught by the live 55 (9 of 10): no BOM strip; no non-ASCII percent-encoding; first match in file order instead of longest match; other keys end a group;
fragment kept; disallow wins ties; reserved escapes decoded; substring user-agent matching; no implicit `/robots.txt` allow.
The 8 extras catch first-match (x2), other-keys-end-group (x1, x5), fragment (x4), reserved-decoded (x7) and substring user agents (x6).
None of my probes catches no-BOM, no-non-ASCII, disallow-wins-ties or no-robots.txt-exempt.

## Verdicts
- The 55 expectations: **hold**. All 24 hand checks are correct, and three implementations agree on all 55.
- Lesson l.105-106, "55 checks whose expectations each quote the robots line that justifies them": **overstated**. 26 checks rest on no rule matching;
  4 of them (9, 14, 15, 30) quote a line that does not justify the decision; check 33's quoted line is not the deciding line (line 170 decides on its own).
- Wave-1 report l.62-64, "the encoded-URL check proves the escape is preserved, not decoded": **wrong**. Line 170 matches the path with or without normalization;
  the no-non-ASCII mutant stays clean on the live 55.
- Lesson l.107-108, "the stock-parser control gives the same … the live set does not separate them": **holds** (reproduced). The cause is the chosen URLs and
  user agents, not the files: 8 extra checks on the same files separate them 8 of 8.
- Lesson l.109, "runs on real files (BOM-led Wikipedia file, 165-record GitHub group, empty `Disallow:`)": **holds as "runs"; the BOM part is inert**.
  The BOM precedes a comment line (`﻿# robots.txt for …`), and the no-BOM-strip mutant stays clean. The 165-record count holds (lines 361-525).
  Only the empty `Disallow:` is decision-relevant.
- Wave-1 report l.59-61, "longest-match allow wins twice live": **holds but does not discriminate**. Both Allows precede their Disallows,
  so first match in file order gives the same answers (mutant clean).
- Lesson l.110, "not that it is more correct than the stdlib on them": **holds for the 55**. The extras show the tool *is* more correct than the stock parser on these files (8 of 8 contract readings).

## Residual risk and gaps
- Freshness: `receipts.json` `headers` points to `../raw/*.headers`, which was never committed (`git ls-tree` at 79d3c780 and HEAD a5ae0280: no `realrun/raw`;
  `fetch_robots.py:31` writes them to the w1 sandbox). No control receipt in `verification/*.json` records the Python version. Python 3.14's `robotparser`
  implements `*`, `$` and longest match (`/usr/lib/python3.14/urllib/robotparser.py:236-326`), so "stock urllib.robotparser 20 of 28" depends on the Python version [INFERENCE: older versions score lower].
- No re-fetch: no URL was named in this item, so drift since 03:23Z is unchecked here. 4xx/5xx and the 500 KiB limit have no live evidence (the w1 report says the same).
- The extra-check expectations are my contract reading. x1 and x5 (a group surviving a `crawl-delay` line) follow contract (b) and RFC 9309 2.2.4; the publishers' intent there is not documented.
