# ReviewProvinceReadme34 — round-34 wave 2

Axes: operability, freshness. Attacked: PROVINCE.md "Round-34 link-preview
frontier step" (lines 157–200) and corpus/README.md "Coverage — round 34"
(lines 316–330) at 24a16474ee73e20453f3e1be9d2f33573c5196d9. Method:
per-statement comparison against committed receipts, matrix interface, tool
code, lessons and wave-1 reports. No defects found that survive scrutiny.

## Commands run (all in lane clone via `git show`/`git ls-tree`, read-only, exit 0)

- `git diff 1e54c895 24a1647 -- PROVINCE.md corpus/README.md` → 58 insertions,
  0 deletions; adds-only contract holds.
- `git show 24a1647:PROVINCE.md | sed -n '14,30p'` → line 30 is the last line of
  the `## Frontier` paragraph: "Ground moves to Core only with source-backed
  entries and a gate." Round-34 section's reading is consistent: it supplies a
  source-backed entry plus an offline gate, claims held Frontier (not Core), and
  adds no Core line — matches the rule's letter.
- `git show 24a1647:.ufo/waves/round-34/sources/receipts.json` → S067–S072
  accessed 20:57:39–20:57:42Z, S073–S077 21:08:44–21:09:47Z, all status 200; the
  PROVINCE "one public GET each at 20:57Z / 21:08–21:09Z" claim matches every
  `accessedUtc`. S071 requested URL did redirect to docs.x.com/overview (receipt
  finalUrl; wave-1 ScoutXCardsLocation reproduced the 307→308 hops and byte-
  identical body sha256 aa5753ce…), so "grounds nothing" is accurate.
- `git show 24a1647:corpus/SOURCES.md` rows S067–S077 → statuses mined
  (S067–S070, S073), rejected (S071, S072, S074, S075), queued (S076, S077),
  all opened 2026-10-22 — README's enumeration is exact.
- `git show 24a1647:.ufo/waves/round-34/c1-matrix.json` → `interface` matches
  PROVINCE/README wording: exit 0 clean / 1 failed-policy / 2 could-not-evaluate
  / 64 usage; findings og_required_missing, og_type_multiple,
  og_url_not_absolute, og_url_not_canonical; "first canonical link wins",
  urljoin resolution; 28 cases confirmed (`len(cases)=28`).
- `git show 24a1647:scripts/link_preview_audit.py` → implements exactly those
  findings (`og_type_multiple` at :199, `og_url_not_absolute` :210, canonical
  compare via `urljoin(page_url, canonical_href)` :217-224, `self.canonical_href`
  first-wins :86-90); no socket/requests/urllib.request import — "network-free"
  is true of the code, not just asserted.
- `git ls-tree 24a1647 scripts/fixtures/link-preview/ | wc -l` → 29 fixture
  dirs; selftest exists (`scripts/link_preview_selftest.py`, `MIN_FIXTURES=20`).
- `git show 24a1647:corpus/lessons/round-34.md` → `## Mistakes` fourth row is
  "a declared counter gives its full score to a control that does none of the
  claimed work" (lookup-table dcef39b5 + hollow 0cce15f0); PROVINCE's "mistake
  row 4" pointer resolves correctly.
- Census numbers: receipt `verification/c2-at-d08d8de.json` `census.derived` =
  pages 102, title/type/url 87, image 1, all-four 1, url-equals-canonical 87;
  both sections quote them correctly; "101 of 102 pages carry no non-empty
  og:image" (102−1) is arithmetic-true.
- Entry-quote check: extracted all 48 curly-quoted spans from
  `corpus/knowledge/link-preview-metadata.md`; every one is a whitespace-
  collapsed exact substring of the retained S067–S070/S073 texts (0 misses), so
  PROVINCE's "the entry's quotes are exact substrings of the retained text" is
  empirically true, stronger than the C2 counter's lesson-gate scope.
- Wave-1 fetch audit: grepped all 30 w1 reports for URLs/fetch claims. Live
  GETs were ScoutMoreSourceLeads (~18:05Z, discord/telegram/linkedin/raw.g…/
  pages.github.com), ScoutXCardsLocation (x.com/docs.x.com/web.archive.org),
  others offline. Every ds4cc.com URL in w1 reports is a manifest/canonical
  string or round-23 retained snapshot, not a fetch (ScoutOwnedPropertiesOG:
  "No live requests were made"; ScoutOgUrlCanonicalSitemap: "owned host, no
  live requests"). "No operator-owned property was fetched" holds.

## Findings (per-statement defects)

None at defect severity. Two wording nits, below defect bar:

1. PROVINCE "one public GET each" — the S068/S071 fetches followed redirects
   (per receipts `url` vs `finalUrl`), so the literal request count per source
   exceeded one; as "one fetch operation" it is fair, and wave-1 reproduction
   GETs are disclosed in the same sentence's continuation.
2. README audit row lists `c2_source_census.py` under the audit row's counters;
   c2 counts the entry, not the audit. PROVINCE presents both counters
   neutrally, so the table's compact phrasing is only mildly loose.

## Residual risk / not verified

- The 29 fixture dirs were counted, not executed; selftest pass/fail is covered
  by `selftest-link-preview-at-5613071-tool.txt`, not re-run here.
- "Wave-1 seats made further ordinary GETs" is trusted via report disclosure;
  unreported wave-1 fetches cannot be excluded by reading committed bytes.
- No live property checks attempted (owned-host rule); the frontier "open"
  items (live card rendering, X card tags) remain genuinely open, not defects.
